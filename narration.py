"""Synthesize and time the approved Vietnamese pilot narration."""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from textwrap import fill


ROOT = Path(__file__).resolve().parent
EPISODE = ROOT / "episodes" / "pilot"
WORK = ROOT / "work" / "pilot"
MODELS = ROOT / "work" / "models"
BACKBONE = "pnnbao-ump/VieNeu-TTS-v3-Turbo"
BACKBONE_REVISION = "61b85e3d937fbbacb387714180e8182823512523"
CODEC = "OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX"
CODEC_REVISION = "ceff0d0749bfb3fa2d61149794ec6feef0d1e1ae"
VOICE = "Quang Sơn"
SAMPLE_RATE = 48_000
SENTENCES_PER_CUE = ((1, 1, 1), (2, 1, 1, 1), (2, 1), (1, 2, 1, 1))
PACE = .84


def approved_cues():
    script = (EPISODE / "script.md").read_text(encoding="utf-8")
    digest = sha256(script.encode("utf-8")).hexdigest()
    record = (EPISODE / "approvals.md").read_text(encoding="utf-8")
    if "`SCRIPT_APPROVED`" not in record or f"`{digest}`" not in record:
        raise ValueError("The current script does not match its approval.")
    if "`VOICE_TRIAL_APPROVED`" not in record or f"**{VOICE}**" not in record:
        raise ValueError("Quang Sơn must be approved for the pilot in Codex.")

    narration = script.split("## Lời đọc\n\n", 1)[1].split("\n\n## Chú giải biên tập", 1)[0]
    paragraphs = narration.strip().split("\n\n")
    cues = []
    for beat, (paragraph, layout) in enumerate(zip(paragraphs, SENTENCES_PER_CUE, strict=True), 1):
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        if len(sentences) != sum(layout):
            raise ValueError(f"The sentence layout for paragraph {beat} needs review.")
        start = 0
        for length in layout:
            end = start + length
            cues.append((beat, " ".join(sentences[start:end])))
            start = end
    return digest, cues


def model_paths(fetch):
    from huggingface_hub import snapshot_download

    backbone = Path(snapshot_download(
        BACKBONE, revision=BACKBONE_REVISION, allow_patterns=["onnx_update/*"],
        cache_dir=MODELS, token=False, local_files_only=not fetch, max_workers=2,
    ))
    # The SDK looks up its stock codec by the main ref, including in offline mode.
    codec = Path(snapshot_download(
        CODEC, revision="main", allow_patterns=["*.onnx", "*.data", "codec_browser_onnx_meta.json"],
        cache_dir=MODELS, token=False, local_files_only=not fetch, max_workers=2,
    ))
    if codec.name != CODEC_REVISION:
        raise ValueError(f"Review the codec revision before using it: {codec.name}")
    return backbone


def record_takes(backbone, digest, cues):
    import numpy as np
    import soundfile as sf
    from vieneu import Vieneu

    take_folder = WORK / "takes" / f"quang-son-{digest[:12]}"
    take_folder.mkdir(parents=True, exist_ok=True)
    paths = [take_folder / f"{index:02}.wav" for index in range(1, len(cues) + 1)]
    if all(path.is_file() for path in paths):
        return paths

    tts = Vieneu(mode="v3turbo", device="cpu", backend="onnx", threads=3,
                 backbone_repo=str(backbone), onnx_dir=str(backbone / "onnx_update"))
    if tts.sample_rate != SAMPLE_RATE or VOICE not in {voice_id for _, voice_id in tts.list_preset_voices()}:
        raise ValueError(f"The installed model does not expose {VOICE} at {SAMPLE_RATE} Hz.")
    with TemporaryDirectory(dir=take_folder) as staging:
        for index, (path, (_, line)) in enumerate(zip(paths, cues), 1):
            if path.is_file():
                continue
            np.random.seed(1260 + index)
            speech = tts.infer(line, voice=VOICE, temperature=.72)
            if speech.ndim != 1 or not np.all(np.isfinite(speech)) or speech.size < SAMPLE_RATE // 2:
                raise ValueError(f"Cue {index} did not produce valid mono speech.")
            temporary = Path(staging) / path.name
            sf.write(temporary, speech, SAMPLE_RATE, subtype="FLOAT")
            temporary.replace(path)
            print(f"Take {index:02}: {len(speech) / SAMPLE_RATE:.3f} s", flush=True)
    return paths


def paced_audio(ffmpeg, take):
    import numpy as np
    import soundfile as sf

    speech, rate = sf.read(take, dtype="float32")
    if rate != SAMPLE_RATE or speech.ndim != 1 or not np.all(np.isfinite(speech)):
        raise ValueError(f"Invalid source WAV: {take.name}")
    step = rate // 100
    windows = speech[:len(speech) // step * step].reshape(-1, step)
    audible = np.flatnonzero(np.max(np.abs(windows), axis=1) >= .009)
    if not audible.size:
        raise ValueError(f"No speech detected in {take.name}")
    start = max(0, int(audible[0]) * step - round(rate * .065))
    end = min(len(speech), (int(audible[-1]) + 1) * step + round(rate * .100))
    result = subprocess.run([
        ffmpeg, "-v", "error", "-nostdin", "-i", str(take),
        "-af", f"atrim=start_sample={start}:end_sample={end},asetpts=PTS-STARTPTS,atempo={PACE}",
        "-f", "f32le", "pipe:1",
    ], check=True, stdout=subprocess.PIPE)
    audio = np.frombuffer(result.stdout, dtype="<f4").copy()
    fade = np.linspace(0, 1, round(rate * .01), dtype="float32")
    audio[:len(fade)] *= fade
    audio[-len(fade):] *= fade[::-1]
    return audio


def srt_time(samples):
    milliseconds = round(samples * 1000 / SAMPLE_RATE)
    seconds, fraction = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{fraction:03}"


def assemble(digest, cues, takes):
    import numpy as np
    import soundfile as sf

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise OSError("ffmpeg must be on PATH")

    def silence(seconds):
        return np.zeros(round(SAMPLE_RATE * seconds), dtype="float32")

    pieces = [silence(.72)]
    cursor = len(pieces[0])
    timeline = []
    captions = []
    for index, ((beat, line), take) in enumerate(zip(cues, takes, strict=True), 1):
        speech = paced_audio(ffmpeg, take)
        start, end = cursor, cursor + len(speech)
        timeline.append({"cue": index, "beat": beat, "start_sample": start,
                         "end_sample": end, "text": line})
        wrapped = fill(line, width=45, break_long_words=False, break_on_hyphens=False)
        captions.append(f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{wrapped}\n\n")
        if index == len(cues):
            pause = silence(.24)
        else:
            pause = silence(.48 if cues[index][0] == beat else 1.55)
        pieces.extend([speech, pause])
        cursor = end + len(pause)

    wave = np.concatenate(pieces)
    if len(wave) > 60 * SAMPLE_RATE:
        raise ValueError("The measured narration no longer fits the 60-second pilot.")
    wave *= 10 ** (-3 / 20) / np.max(np.abs(wave))
    with TemporaryDirectory(dir=WORK) as staging:
        stage = Path(staging)
        wav = stage / "narration.wav"
        sf.write(wav, wave, SAMPLE_RATE, subtype="PCM_16")
        timing = {
            "script_sha256": digest,
            "voice": VOICE,
            "sample_rate": SAMPLE_RATE,
            "duration_samples": len(wave),
            "wav_sha256": sha256(wav.read_bytes()).hexdigest(),
            "cues": timeline,
        }
        (stage / "narration-timing.json").write_text(
            json.dumps(timing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n",
        )
        (stage / "narration.srt").write_text("".join(captions), encoding="utf-8", newline="\n")
        for output in ("narration.wav", "narration.srt", "narration-timing.json"):
            (stage / output).replace(WORK / output)
    print(f"Narration: {len(wave) / SAMPLE_RATE:.3f} s, {len(timeline)} cues")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-models", action="store_true", help="download the public model files")
    args = parser.parse_args()
    os.environ["HF_HUB_CACHE"] = str(MODELS)
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    os.environ["HF_HUB_OFFLINE"] = "0" if args.fetch_models else "1"
    try:
        if args.fetch_models:
            print(model_paths(fetch=True))
        else:
            digest, cues = approved_cues()
            takes = record_takes(model_paths(fetch=False), digest, cues)
            assemble(digest, cues, takes)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Narration failed: {error}\n")


if __name__ == "__main__":
    main()
