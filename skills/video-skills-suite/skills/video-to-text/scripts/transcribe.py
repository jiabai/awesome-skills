#!/usr/bin/env python3
"""
Video/Audio → Text transcription with whisperX.
Supports: speaker diarization, timestamp alignment, multiple output formats.

Usage:
    python3 transcribe.py <input_file> [options]

Options:
    --output-dir DIR    Output directory (default: same as input)
    --output-name NAME  Output filename stem (default: derived from input)
    --language LANG     Language code (default: zh)
    --model MODEL       Whisper model (default: large-v3)
    --diarize           Enable speaker diarization (requires HF_TOKEN env var)
    --device DEVICE     cpu or cuda (default: cpu)
    --batch-size N      Batch size for transcription (default: 8)

Output:
    <name>.txt   - Human-readable transcript with speaker labels and timestamps
    <name>.json  - Full whisperX output with word-level timestamps
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


def extract_audio(video_path, audio_path):
    """Extract audio from video file to 16kHz mono WAV."""
    print(f"Extracting audio from {video_path}...")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Audio extracted: {audio_path}")


def transcribe(audio_path, model_name, device, compute_type, batch_size, language):
    """Run whisperX transcription."""
    import whisperx

    print(f"Loading model {model_name}...")
    model = whisperx.load_model(model_name, device, compute_type=compute_type)

    print("Transcribing... (this may take a while for long audio)")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=batch_size, language=language)
    print(f"Detected language: {result['language']}")

    # Alignment
    print("Aligning timestamps...")
    try:
        align_model, metadata = whisperx.load_align_model(
            language_code=result["language"], device=device
        )
        result = whisperx.align(
            result["segments"], align_model, metadata, audio, device,
            return_char_alignments=False
        )
    except Exception as e:
        print(f"Alignment skipped: {e}")

    return result, audio_path


def diarize(result, audio_path, device):
    """Run speaker diarization."""
    import whisperx

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("HF_TOKEN not set, skipping diarization")
        return result

    print("Running speaker diarization...")
    try:
        diarize_model = whisperx.DiarizationPipeline(
            use_auth_token=hf_token, device=device
        )
        diarize_segments = diarize_model(audio_path)
        result = whisperx.assign_word_speakers(diarize_segments, result)
        print("Diarization done!")
    except Exception as e:
        print(f"Diarization failed: {e}")

    return result


def format_transcript(result):
    """Format segments into human-readable transcript with speaker grouping."""
    lines = []
    current_speaker = None
    current_texts = []

    for seg in result.get("segments", []):
        speaker = seg.get("speaker", None)
        text = seg.get("text", "").strip()
        start = seg.get("start", 0)

        ts = f"[{int(start // 60):02d}:{int(start % 60):02d}]"

        if speaker != current_speaker:
            if current_texts:
                prefix = f"{current_speaker}: " if current_speaker else ""
                lines.append(prefix + " ".join(current_texts))
            current_speaker = speaker
            current_texts = [ts + " " + text]
        else:
            current_texts.append(text)

    if current_texts:
        prefix = f"{current_speaker}: " if current_speaker else ""
        lines.append(prefix + " ".join(current_texts))

    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Video/Audio → Text transcription")
    parser.add_argument("input", help="Input video or audio file")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--output-name", help="Output filename stem")
    parser.add_argument("--language", default="zh", help="Language code (default: zh)")
    parser.add_argument("--model", default="large-v3", help="Whisper model")
    parser.add_argument("--diarize", action="store_true", help="Enable speaker diarization")
    parser.add_argument("--device", default="cpu", help="cpu or cuda")
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Determine output paths
    if args.output_dir:
        out_dir = args.output_dir
    else:
        out_dir = os.path.dirname(input_path)
    os.makedirs(out_dir, exist_ok=True)

    if args.output_name:
        stem = args.output_name
    else:
        stem = os.path.splitext(os.path.basename(input_path))[0]

    out_json = os.path.join(out_dir, f"{stem}.json")
    out_txt = os.path.join(out_dir, f"{stem}.txt")

    # Determine if we need audio extraction
    audio_exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
    ext = os.path.splitext(input_path)[1].lower()

    if ext in audio_exts:
        audio_path = input_path
        temp_audio = None
    else:
        # Video file — extract audio to temp WAV
        temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_audio.close()
        audio_path = temp_audio.name
        extract_audio(input_path, audio_path)

    compute_type = "int8" if args.device == "cpu" else "float16"

    try:
        result, audio_file = transcribe(
            audio_path, args.model, args.device, compute_type,
            args.batch_size, args.language
        )

        if args.diarize:
            result = diarize(result, audio_file, args.device)

        # Save JSON
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # Save TXT
        txt = format_transcript(result)
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(txt)

        print(f"\nDone!")
        print(f"  Text:  {out_txt}")
        print(f"  JSON:  {out_json}")
        print(f"  Segments: {len(result.get('segments', []))}")

    finally:
        if temp_audio and os.path.exists(temp_audio.name):
            os.unlink(temp_audio.name)


if __name__ == "__main__":
    main()
