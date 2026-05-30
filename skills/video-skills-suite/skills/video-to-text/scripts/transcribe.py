#!/usr/bin/env python3
"""
Video/Audio to text transcription with SenseVoiceSmall + ct-punc.
模型链路: SenseVoiceSmall (ASR) -> ct-punc (标点恢复)

Usage:
    python3 transcribe.py <input_file> [options]

Options:
    --output-dir DIR     Output directory (default: same as input)
    --output-name NAME   Output filename stem (default: derived from input)
    --language LANG      Language code: auto, zh, en, yue, ja, ko (default: zh)
    --device DEVICE      cpu or cuda (default: cpu)

Dependencies:
    pip install modelscope funasr
    ffmpeg (SenseVoice 内部通过 ffmpeg 处理视频文件)

Output:
    <name>.txt  - 带标点的纯文本
"""

import argparse
import os
import re
import sys
import time


def _parse_sensevoice_text(text):
    """Parse SenseVoice output, strip tags, return plain text."""
    text = re.sub(r"<\|[a-z]+\|>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<\|NEUTRAL\|>", "", text)
    text = re.sub(r"<\|ANGER\|>", "", text)
    text = re.sub(r"<\|SADNESS\|>", "", text)
    text = re.sub(r"<\|HAPPY\|>", "", text)
    text = re.sub(r"<\|FEAR\|>", "", text)
    text = re.sub(r"<\|SURPRISE\|>", "", text)
    text = text.strip()

    pattern = r"<\|(\d+\.?\d*)\|><\|(\d+\.?\d*)\|>(.*?)(?=<|\d|$)"
    matches = re.findall(pattern, text)
    if matches:
        parts = [m[2].strip() for m in matches if m[2].strip()]
        return " ".join(parts) if parts else text.strip()
    return text.strip()


def _apply_punctuation(punc_model, text):
    """Apply ct-punc for punctuation restoration."""
    if not text or not text.strip():
        return text
    try:
        result = punc_model.generate(input=text)
        if isinstance(result, list) and len(result) > 0:
            punctuated = result[0].get("text", text)
        elif isinstance(result, dict):
            punctuated = result.get("text", text)
        else:
            punctuated = str(result)
        return punctuated.strip() if punctuated else text
    except Exception as e:
        print(f"  [WARN] Punctuation restoration failed: {e}", file=sys.stderr)
        return text


def load_asr_pipeline(device):
    """Load SenseVoiceSmall via modelscope pipeline."""
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks

    print(f"Loading SenseVoiceSmall ASR model...")
    t0 = time.time()
    asr = pipeline(
        task=Tasks.auto_speech_recognition,
        model='iic/SenseVoiceSmall',
        device=device,
    )
    print(f"  ASR model loaded in {time.time() - t0:.1f}s")
    return asr


def load_punc_model():
    """Load ct-punc model."""
    from funasr import AutoModel

    print(f"Loading ct-punc model...")
    t0 = time.time()
    model = AutoModel(model="ct-punc")
    print(f"  Punctuation model loaded in {time.time() - t0:.1f}s")
    return model


def main():
    parser = argparse.ArgumentParser(
        description="Video/Audio to text with SenseVoiceSmall + ct-punc"
    )
    parser.add_argument("input", help="Input video or audio file path")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--output-name", default=None, help="Output filename stem")
    parser.add_argument("--language", default="zh", help="Language: auto, zh, en, yue, ja, ko")
    parser.add_argument("--device", default="cpu", help="cpu or cuda")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or os.path.dirname(input_path)
    os.makedirs(output_dir, exist_ok=True)

    if args.output_name:
        output_stem = args.output_name
    else:
        output_stem = os.path.splitext(os.path.basename(input_path))[0]

    print(f"Input : {input_path}")
    print(f"Output: {output_dir}/{output_stem}.txt")
    print(f"Device: {args.device}  Language: {args.language}")

    asr_pipeline = load_asr_pipeline(args.device)
    punc_model = load_punc_model()

    t0 = time.time()
    result = asr_pipeline(input=input_path, language=args.language)
    print(f"  ASR done in {time.time() - t0:.1f}s")

    raw_text = ""
    if isinstance(result, dict):
        raw_text = result.get("text", result.get("preds", ""))
    elif isinstance(result, str):
        raw_text = result
    elif isinstance(result, list):
        raw_text = " ".join(r.get("text", "") for r in result if isinstance(r, dict))
    else:
        raw_text = str(result)

    plain_text = _parse_sensevoice_text(raw_text)

    print(f"  Restoring punctuation...")
    t0 = time.time()
    punctuated_text = _apply_punctuation(punc_model, plain_text)
    print(f"  Punctuation done in {time.time() - t0:.1f}s")

    txt_path = os.path.join(output_dir, f"{output_stem}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(punctuated_text)
    print(f"Transcript saved: {txt_path}")


if __name__ == "__main__":
    main()