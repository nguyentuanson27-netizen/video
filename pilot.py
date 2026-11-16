"""Render the approved 60-second pilot from its ink-wash scene sources."""

import argparse
from hashlib import sha256
import json
from math import ceil, cos, floor, pi
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from textwrap import fill
from time import perf_counter
from urllib.request import urlopen

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf

from narration import EPISODE, SAMPLE_RATE, WORK, approved_cues, srt_time
from scenes.pilot_board import DRAW_SCENE, SHOT_FRAMES
from scenes.valley import VIEW, WORLD
from studio import FPS


FONT_REVISION = "cc39c4c2c304bc368c9b7c311ea2bcc6013299fe"
FONT_HASH = "bd8e27eb02720b9d91e59e4f10a90878643219f25ce6a8d9a4f06a8a88d3bb71"
FONT = WORK / "fonts" / "BeVietnamPro-SemiBold.ttf"
CAMERAS = (
    ((-14, 3, .025), (21, -3, .075)),
    ((10, -2, .030), (13, -3, .105)),
    ((8, -10, .027), (13, 16, .068)),
    ((7, 3, .050), (12, 0, .103)),
)


def digest(path, normalize=False):
    data = path.read_text(encoding="utf-8").encode("utf-8") if normalize else path.read_bytes()
    return sha256(data).hexdigest()


def approved_timing():
    script_hash, script_cues = approved_cues()
    approvals = (EPISODE / "approvals.md").read_text(encoding="utf-8")
    if "`BOARD_APPROVED`" not in approvals or "`VOICE_READY`" not in approvals:
        raise ValueError("The storyboard and narration need owner approval.")
    timing_file = EPISODE / "narration-timing.json"
    for value in (digest(EPISODE / "storyboard.md", True), digest(timing_file, True),
                  digest(WORK / "narration.wav")):
        if f"`{value}`" not in approvals:
            raise ValueError("Storyboard, timing, or WAV differs from its approved revision.")
    timing = json.loads(timing_file.read_text(encoding="utf-8"))
    if timing["script_sha256"] != script_hash or timing["sample_rate"] != SAMPLE_RATE:
        raise ValueError("The approved timing does not match the script or sample rate.")
    if [(cue["beat"], cue["text"]) for cue in timing["cues"]] != script_cues:
        raise ValueError("The timing captions do not match the approved narration text.")
    for cue in timing["cues"]:
        beat = cue["beat"]
        if not (SHOT_FRAMES[beat - 1] * SAMPLE_RATE // FPS <= cue["start_sample"]
                < cue["end_sample"] <= SHOT_FRAMES[beat] * SAMPLE_RATE // FPS):
            raise ValueError(f"Cue {cue['cue']} crosses its scene boundary.")
    return timing


def fetch_font():
    FONT.parent.mkdir(parents=True, exist_ok=True)
    base = f"https://raw.githubusercontent.com/google/fonts/{FONT_REVISION}/ofl/bevietnampro"
    with TemporaryDirectory(dir=FONT.parent) as staging:
        for name in (FONT.name, "OFL.txt"):
            target = Path(staging) / name
            with urlopen(f"{base}/{name}", timeout=30) as source:
                target.write_bytes(source.read(1_000_001))
            if target.stat().st_size > 1_000_000 or (name == FONT.name and digest(target) != FONT_HASH):
                raise ValueError(f"Unexpected font asset: {name}")
            target.replace(FONT.parent / name)


def caption_image(text, width, font):
    padding = round(width * .014)
    wrapped = fill(text, width=45, break_long_words=False, break_on_hyphens=False)
    draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    left, top, right, bottom = draw.multiline_textbbox((0, 0), wrapped, font=font,
                                                       spacing=4, align="center")
    box = floor(left), floor(top), ceil(right), ceil(bottom)
    canvas = Image.new("RGBA", (box[2] - box[0] + padding * 2, box[3] - box[1] + padding * 2))
    if canvas.width > width * .91:
        raise ValueError("A subtitle exceeds the safe area.")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, canvas.width - 1, canvas.height - 1), radius=padding // 2,
                           fill=(29, 41, 35, 225))
    draw.multiline_text((padding - box[0], padding - box[1]), wrapped,
                        fill="#fff4db", font=font, spacing=4, align="center")
    return canvas


def prepare_layer(image):
    bounds = image.getbbox()
    if bounds is None:
        return None
    return bounds, image.crop(bounds)


def render_frame(layers, size, progress, camera):
    width, height = size
    paint_scale = width / VIEW[0]
    start, stop = camera
    eased = (1 - cos(pi * min(progress / .89, 1))) / 2
    pan, tilt, push = (a + (b - a) * eased for a, b in zip(start, stop))
    frame = Image.new("RGBA", size, "#f5ead4")
    for depth, layer in layers:
        prepared = prepare_layer(layer(progress)) if callable(layer) else layer
        if prepared is None:
            continue
        (left, top, right, bottom), image = prepared
        zoom = 1 + push * depth
        dx = (WORLD[0] / 2 + pan * depth) * paint_scale - width / (2 * zoom)
        dy = (WORLD[1] / 2 + tilt * depth) * paint_scale - height / (2 * zoom)
        x0, y0 = max(0, floor((left - dx) * zoom)), max(0, floor((top - dy) * zoom))
        x1, y1 = min(width, ceil((right - dx) * zoom)), min(height, ceil((bottom - dy) * zoom))
        if x1 <= x0 or y1 <= y0:
            continue
        if image.mode == "RGB":
            sky = image.resize(size, Image.Resampling.BILINEAR,
                               box=(dx, dy, dx + width / zoom, dy + height / zoom))
            frame.paste(sky)
        else:
            segment = image.transform(
                (x1 - x0, y1 - y0), Image.Transform.AFFINE,
                (1 / zoom, 0, dx + x0 / zoom - left, 0, 1 / zoom, dy + y0 / zoom - top),
                resample=Image.Resampling.BILINEAR,
            )
            frame.alpha_composite(segment, (x0, y0))
    return frame


def shot_layers(index, width):
    layers = DRAW_SCENE[index](width / VIEW[0], animate=True)
    depth, sky = layers[0]
    layers[0] = (depth, sky.convert("RGB"))
    return [(depth, image if callable(image) else prepare_layer(image)) for depth, image in layers]


def render_shot(ffmpeg, index, size, timeline, output):
    width, height = size
    layers = shot_layers(index, width)
    camera = CAMERAS[index]
    font = ImageFont.truetype(FONT, round(width * .026))
    captions = [(cue["start_sample"], cue["end_sample"], caption_image(cue["text"], width, font))
                for cue in timeline if cue["beat"] == index + 1]
    first, end = SHOT_FRAMES[index:index + 2]
    start = perf_counter()
    with TemporaryDirectory(dir=output.parent) as staging:
        temporary = Path(staging) / output.name
        command = [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin",
            "-filter_threads", "1", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-video_size", f"{width}x{height}", "-framerate", str(FPS), "-i", "pipe:0",
            "-an", "-c:v", "libx264", "-threads", "2", "-preset", "veryfast",
            "-crf", "17", "-pix_fmt", "yuv420p", "-video_track_timescale", "24000",
            str(temporary),
        ]
        with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
            try:
                with process.stdin as pipe:
                    for number in range(first, end):
                        progress = (number - first) / (end - first - 1)
                        frame = render_frame(layers, size, progress, camera)
                        sample = number * SAMPLE_RATE // FPS
                        for begin, stop, caption in captions:
                            if begin <= sample < stop:
                                frame.alpha_composite(caption, ((width - caption.width) // 2,
                                                                height - caption.height - round(height * .07)))
                                break
                        pipe.write(frame.convert("RGB").tobytes())
            except BaseException:
                process.kill()
                raise
            if process.wait():
                raise subprocess.CalledProcessError(process.returncode, command)
        temporary.replace(output)
    print(f"{output.name}: {end - first} frames in {perf_counter() - start:.2f}s", flush=True)


def write_soundtrack(timing):
    count = SHOT_FRAMES[-1] * SAMPLE_RATE // FPS
    time = np.arange(count, dtype=np.float32) / SAMPLE_RATE
    score = np.zeros(count, dtype=np.float32)
    notes = (
        (0.65, 50), (3.2, 57), (6.0, 60), (9.7, 53), (12.4, 55),
        (15.7, 50), (19.4, 55), (22.5, 53), (25.4, 50),
        (28.7, 57), (31.3, 60), (34.2, 62), (37.8, 65),
        (41.0, 57), (44.7, 60), (49.2, 62), (53.8, 57), (57.0, 50),
    )
    note_time = time[:round(2.8 * SAMPLE_RATE)]
    envelope = np.minimum(1, note_time * 105) * np.exp(-note_time * 2.1)
    for offset, note in notes:
        phase = 2 * pi * (440 * 2 ** ((note - 69) / 12)) * note_time
        pluck = envelope * (.065 * np.sin(phase) + .025 * np.sin(2 * phase) + .012 * np.sin(3 * phase))
        start = round(offset * SAMPLE_RATE)
        score[start:start + len(pluck)] += pluck
        echo = start + 9120
        score[echo:echo + len(pluck)] += pluck * .29
    rng = np.random.default_rng(175)
    air = np.interp(time, np.arange(0, 60.02, .006), rng.normal(0, 1, 10004))
    wind = np.clip((time - 13.9) / 2.7, 0, 1) * np.clip((28.2 - time) / 3.1, 0, 1)
    water = np.exp(-((time - 37.75) / .42) ** 2)
    score += air * (.012 * wind + .004 * water)
    score *= np.minimum(1, time * 2) * np.clip((60 - time) / 2.1, 0, 1)
    sf.write(WORK / "music-sfx.wav", score, SAMPLE_RATE, subtype="PCM_16")
    voice, rate = sf.read(WORK / "narration.wav", dtype="float32")
    if rate != SAMPLE_RATE or voice.ndim != 1 or len(voice) != timing["duration_samples"]:
        raise ValueError("The approved narration has unexpected audio properties.")
    ramps = np.ones(count, dtype=np.float32)
    ramp = round(.13 * SAMPLE_RATE)
    for cue in timing["cues"]:
        start, end = cue["start_sample"], cue["end_sample"]
        ramps[start - ramp:start] = np.linspace(1, .47, ramp)
        ramps[start:end] = .47
        ramps[end:end + ramp] = np.linspace(.47, 1, ramp)
    mix = score * ramps
    mix[:len(voice)] += voice * 1.32
    mix *= min(1, .865 / np.max(np.abs(mix)))
    sf.write(WORK / "pilot-mix.wav", mix, SAMPLE_RATE, subtype="PCM_16")


def assemble(ffmpeg, clips, output):
    with TemporaryDirectory(dir=WORK) as directory:
        stage = Path(directory)
        manifest = stage / "scenes.ffconcat"
        manifest.write_text("ffconcat version 1.0\n" + "".join(
            f"file '../{clip.parent.name}/{clip.name}'\nduration {(end - first) / FPS:.9f}\n"
            for clip, first, end in zip(clips, SHOT_FRAMES, SHOT_FRAMES[1:])
        ), encoding="ascii")
        temporary = stage / output.name
        subprocess.run([
            ffmpeg, "-v", "error", "-nostdin", "-f", "concat", "-safe", "0", "-i", str(manifest),
            "-i", str(WORK / "pilot-mix.wav"), "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-video_track_timescale", "24000", "-movie_timescale", "24000",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(temporary),
        ], check=True)
        temporary.replace(output)


def write_subtitles(timing, output):
    captions = []
    for cue in timing["cues"]:
        start, end = srt_time(cue["start_sample"]), srt_time(cue["end_sample"])
        text = fill(cue["text"], width=45, break_long_words=False, break_on_hyphens=False)
        captions.append(f"{cue['cue']}\n{start} --> {end}\n{text}\n\n")
    output.write_text("".join(captions), encoding="utf-8", newline="\n")


def render_preview():
    timing = approved_timing()
    if digest(FONT) != FONT_HASH:
        raise ValueError("The subtitle font differs from the pinned asset.")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise OSError("ffmpeg must be on PATH.")
    scene_dir = WORK / "preview-scenes"
    scene_dir.mkdir(exist_ok=True)
    clips = [scene_dir / f"s{index + 1:02}.mp4" for index in range(len(DRAW_SCENE))]
    for index, clip in enumerate(clips):
        render_shot(ffmpeg, index, (1280, 720), timing["cues"], clip)
    write_soundtrack(timing)
    write_subtitles(timing, WORK / "preview.srt")
    assemble(ffmpeg, clips, WORK / "preview.mp4")
    print(WORK / "preview.mp4", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-font", action="store_true", help="download the pinned OFL subtitle font")
    args = parser.parse_args()
    try:
        fetch_font() if args.fetch_font else render_preview()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Pilot failed: {error}\n")


if __name__ == "__main__":
    main()
