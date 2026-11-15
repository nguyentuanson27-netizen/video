"""Render one scene locally with Pillow and FFmpeg."""

import argparse
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
from time import perf_counter

from PIL import Image

from scenes.styles import CAMERAS, MOONLIT_CAMERA, STYLES, demo_layers
from scenes.valley import VIEW, WORLD, valley


FPS = 24
WORK = Path(__file__).resolve().parent / "work"


def frame_at(layers, width, height, progress, camera=MOONLIT_CAMERA):
    scale = width / VIEW[0]
    eased = (1 - math.cos(math.pi * progress)) / 2
    start, end = camera
    pan, tilt, push = (a + (b - a) * eased for a, b in zip(start, end))
    frame = Image.new("RGBA", (width, height))
    for depth, layer in layers:
        image = layer(progress) if callable(layer) else layer
        zoom = 1 + push * depth
        center_x = WORLD[0] / 2 + pan * depth
        center_y = WORLD[1] / 2 + tilt * depth
        half_width, half_height = VIEW[0] / (2 * zoom), VIEW[1] / (2 * zoom)
        box = (
            (center_x - half_width) * scale,
            (center_y - half_height) * scale,
            (center_x + half_width) * scale,
            (center_y + half_height) * scale,
        )
        frame.alpha_composite(image.resize((width, height), Image.Resampling.BILINEAR, box=box))
    return frame.convert("RGB")


def render(output, duration, style=None):
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise OSError("ffmpeg must be on PATH")

    width, height = 1280, 720
    frame_count = FPS * duration
    start = perf_counter()
    WORK.mkdir(exist_ok=True)
    layers = demo_layers(width, style) if style else valley(width)
    camera = CAMERAS[style] if style else MOONLIT_CAMERA
    # Keep the destination intact until FFmpeg closes a complete MP4.
    with tempfile.TemporaryDirectory(dir=WORK, prefix="render-") as staging:
        temporary = Path(staging) / output.name
        command = [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin",
            "-filter_threads", "1", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{width}x{height}", "-framerate", str(FPS), "-i", "pipe:0",
            "-an", "-c:v", "libx264", "-threads", "2", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporary),
        ]
        with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
            try:
                with encoder.stdin as pipe:
                    for index in range(frame_count):
                        frame = frame_at(layers, width, height, index / (frame_count - 1), camera)
                        pipe.write(frame.tobytes())
            except BaseException:
                encoder.kill()
                raise
            if encoder.wait():
                raise subprocess.CalledProcessError(encoder.returncode, command)
        temporary.replace(output)
    elapsed = perf_counter() - start
    print(f"{output}: {width}x{height} @ {FPS} fps, {frame_count} frames; render {elapsed:.2f} s")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, choices=range(10, 21), default=12,
                        metavar="SECONDS", help="clip duration, 10–20 seconds (default: 12)")
    parser.add_argument("--demo", choices=STYLES, help="render a style demo")
    args = parser.parse_args()
    try:
        if args.demo:
            render(WORK / f"demo-{args.demo}.mp4", args.duration, args.demo)
        else:
            render(WORK / "m01-valley.mp4", args.duration)
    except (OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Render failed: {error}\n")


if __name__ == "__main__":
    main()
