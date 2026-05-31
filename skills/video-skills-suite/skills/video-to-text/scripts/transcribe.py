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
    <name>.txt   - 带时间戳的文字稿
    <name>.json  - 结构化转写结果，含 segments 和 word_segments
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time


TAG_RE = re.compile(r"<\|[^|]+?\|>")
TIMESTAMP_PAIR_RE = re.compile(
    r"<\|(?P<start>\d+(?:\.\d+)?)\|>\s*<\|(?P<end>\d+(?:\.\d+)?)\|>"
)
TOKEN_RE = re.compile(r"[\u3400-\u9fff]|[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
SENTENCE_RE = re.compile(r"[^。！？!?；;]+[。！？!?；;]?")
SILENCE_START_RE = re.compile(r"silence_start:\s*(?P<start>\d+(?:\.\d+)?)")
SILENCE_END_RE = re.compile(r"silence_end:\s*(?P<end>\d+(?:\.\d+)?)")
SENSEVOICE_MODEL_ID = "iic/SenseVoiceSmall"
CT_PUNC_MODEL_ID = "ct-punc"
CT_PUNC_CACHE_NAME = "punc_ct-transformer_cn-en-common-vocab471067-large"


def _collapse_ws(text):
    """Collapse whitespace while preserving CJK text."""
    return re.sub(r"\s+", " ", text).strip()


def _strip_tags(text):
    """Remove SenseVoice markup tags, including language/emotion/time tags."""
    return _collapse_ws(TAG_RE.sub("", text or ""))


def _format_ts(seconds):
    seconds = max(0.0, float(seconds))
    millis = int(round((seconds - int(seconds)) * 1000))
    whole = int(seconds)
    if millis == 1000:
        whole += 1
        millis = 0
    h, rem = divmod(whole, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}.{millis:03d}"
    return f"{m:02d}:{s:02d}.{millis:03d}"


def _timestamp_scale(pairs, duration=None):
    """Infer whether timestamps are seconds or milliseconds."""
    if not pairs:
        return 1.0
    max_end = max(end for _, end in pairs)
    if duration and duration > 0:
        if max_end > duration * 1.5 and max_end / 1000 <= duration * 1.5:
            return 1000.0
        return 1.0
    durations = [end - start for start, end in pairs if end > start]
    if durations:
        sorted_durations = sorted(durations)
        median = sorted_durations[len(sorted_durations) // 2]
        if median > 120:
            return 1000.0
    return 1.0


def _normalize_pairs(pairs, duration=None):
    scale = _timestamp_scale(pairs, duration)
    return [(round(start / scale, 3), round(end / scale, 3)) for start, end in pairs]


def _safe_float(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and value:
        value = value[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_present(mapping, keys):
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None


def _tokenize_for_timestamps(text):
    return [match.group(0) for match in TOKEN_RE.finditer(text or "")]


def _json_safe(value):
    """Convert model outputs with numpy/scalar values into JSON-safe data."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "tolist"):
        return _json_safe(value.tolist())
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            pass
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def _modelscope_cache_root():
    return os.environ.get(
        "MODELSCOPE_CACHE",
        os.path.join(os.path.expanduser("~"), ".cache", "modelscope", "hub"),
    )


def _cached_model_dir(*parts):
    path = os.path.join(_modelscope_cache_root(), "models", *parts)
    return path if os.path.isdir(path) else None


def _iter_result_dicts(result):
    if isinstance(result, dict):
        yield result
        for value in result.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item
    elif isinstance(result, list):
        for item in result:
            if isinstance(item, dict):
                yield item


def _extract_raw_text(result):
    if isinstance(result, dict):
        if "text" in result:
            return str(result.get("text") or "")
        if "preds" in result:
            return str(result.get("preds") or "")
    if isinstance(result, str):
        return result
    if isinstance(result, list):
        parts = []
        for item in result:
            if isinstance(item, dict):
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return " ".join(part for part in parts if part)
    return str(result)


def _parse_sensevoice_tagged_segments(text, duration=None):
    matches = list(TIMESTAMP_PAIR_RE.finditer(text or ""))
    if not matches:
        return []

    raw_segments = []
    pairs = []
    for index, match in enumerate(matches):
        start = float(match.group("start"))
        end = float(match.group("end"))
        content_start = match.end()
        content_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        segment_text = _strip_tags(text[content_start:content_end])
        if not segment_text:
            continue
        raw_segments.append({"start": start, "end": end, "text": segment_text, "speaker": None})
        pairs.append((start, end))

    normalized_pairs = _normalize_pairs(pairs, duration)
    segments = []
    for idx, (segment, (start, end)) in enumerate(zip(raw_segments, normalized_pairs)):
        segments.append(
            {
                "id": idx,
                "start": start,
                "end": end,
                "text": segment["text"],
                "speaker": segment["speaker"],
            }
        )
    return segments


def _parse_timestamp_pairs(value):
    if not isinstance(value, list):
        return []
    pairs = []
    for item in value:
        if isinstance(item, dict):
            start = _safe_float(_first_present(item, ("start", "begin", "start_time")))
            end = _safe_float(_first_present(item, ("end", "finish", "end_time")))
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            start = _safe_float(item[0])
            end = _safe_float(item[1])
        else:
            continue
        if start is not None and end is not None and end >= start:
            pairs.append((start, end))
    return pairs


def _parse_structured_segments(result, duration=None):
    segment_keys = ("segments", "sentence_info", "sentences", "chunks")
    start_keys = ("start", "begin", "start_time", "begin_time")
    end_keys = ("end", "finish", "end_time", "stop", "stop_time")
    text_keys = ("text", "sentence", "value")

    for item in _iter_result_dicts(result):
        for key in segment_keys:
            value = item.get(key)
            if not isinstance(value, list):
                continue

            raw_segments = []
            pairs = []
            for entry in value:
                if not isinstance(entry, dict):
                    continue
                start = _safe_float(_first_present(entry, start_keys))
                end = _safe_float(_first_present(entry, end_keys))
                if start is None or end is None:
                    timestamp_pairs = _parse_timestamp_pairs(entry.get("timestamp"))
                    if timestamp_pairs:
                        start, end = timestamp_pairs[0][0], timestamp_pairs[-1][1]
                text = next((str(entry.get(k) or "") for k in text_keys if k in entry), "")
                text = _strip_tags(text)
                if start is None or end is None or not text:
                    continue
                speaker = entry.get("speaker") or entry.get("spk") or entry.get("speaker_id")
                raw_segments.append({"start": start, "end": end, "text": text, "speaker": speaker})
                pairs.append((start, end))

            if raw_segments:
                normalized_pairs = _normalize_pairs(pairs, duration)
                segments = []
                for idx, (segment, (start, end)) in enumerate(zip(raw_segments, normalized_pairs)):
                    segments.append(
                        {
                            "id": idx,
                            "start": start,
                            "end": end,
                            "text": segment["text"],
                            "speaker": segment["speaker"],
                        }
                    )
                return segments, key

    return [], None


def _extract_segments(result, raw_text, duration=None):
    segments, source = _parse_structured_segments(result, duration)
    if segments:
        return segments, source

    tagged_segments = _parse_sensevoice_tagged_segments(raw_text, duration)
    if tagged_segments:
        return tagged_segments, "sensevoice_tags"

    return [], "none"


def _parse_word_entries(result, duration=None):
    for item in _iter_result_dicts(result):
        for key in ("word_segments", "words"):
            value = item.get(key)
            if not isinstance(value, list):
                continue
            raw_words = []
            pairs = []
            for entry in value:
                if not isinstance(entry, dict):
                    continue
                word = entry.get("word") or entry.get("text") or entry.get("value")
                start = _safe_float(_first_present(entry, ("start", "begin", "start_time")))
                end = _safe_float(_first_present(entry, ("end", "finish", "end_time")))
                if word and start is not None and end is not None:
                    raw_words.append({"word": str(word), "start": start, "end": end, "speaker": entry.get("speaker")})
                    pairs.append((start, end))
            if raw_words:
                normalized_pairs = _normalize_pairs(pairs, duration)
                words = []
                for entry, (start, end) in zip(raw_words, normalized_pairs):
                    words.append(
                        {
                            "word": entry["word"],
                            "start": start,
                            "end": end,
                            "speaker": entry["speaker"],
                        }
                    )
                return words, key
    return [], None


def _words_from_root_timestamps(result, text, duration=None):
    for item in _iter_result_dicts(result):
        pairs = _parse_timestamp_pairs(item.get("timestamp"))
        if not pairs:
            continue
        tokens = _tokenize_for_timestamps(text or item.get("text", ""))
        if not tokens:
            continue
        normalized_pairs = _normalize_pairs(pairs[: len(tokens)], duration)
        return [
            {"word": token, "start": start, "end": end, "speaker": None}
            for token, (start, end) in zip(tokens, normalized_pairs)
        ], "timestamp"
    return [], None


def _estimate_word_segments(segments):
    words = []
    for segment in segments:
        tokens = _tokenize_for_timestamps(segment["text"])
        if not tokens:
            continue
        start = float(segment["start"])
        end = float(segment["end"])
        span = max(end - start, 0.0)
        step = span / len(tokens) if tokens else 0.0
        for idx, token in enumerate(tokens):
            word_start = round(start + step * idx, 3)
            word_end = round(end if idx == len(tokens) - 1 else start + step * (idx + 1), 3)
            words.append(
                {
                    "word": token,
                    "start": word_start,
                    "end": word_end,
                    "speaker": segment.get("speaker"),
                }
            )
    return words


def _split_text_units(text, max_chars=90):
    text = _collapse_ws(text)
    if not text:
        return []

    units = [match.group(0).strip() for match in SENTENCE_RE.finditer(text)]
    units = [unit for unit in units if unit]
    if not units:
        units = [text]

    expanded = []
    for unit in units:
        if len(unit) <= max_chars:
            expanded.append(unit)
            continue
        for start in range(0, len(unit), max_chars):
            expanded.append(unit[start : start + max_chars].strip())
    return [unit for unit in expanded if unit]


def _parse_silence_intervals(log_text, duration=None):
    intervals = []
    pending_start = None
    for line in (log_text or "").splitlines():
        start_match = SILENCE_START_RE.search(line)
        if start_match:
            pending_start = float(start_match.group("start"))

        end_match = SILENCE_END_RE.search(line)
        if end_match and pending_start is not None:
            end = float(end_match.group("end"))
            if end >= pending_start:
                intervals.append((pending_start, end))
            pending_start = None

    if pending_start is not None and duration and duration > pending_start:
        intervals.append((pending_start, float(duration)))
    return intervals


def _speech_ranges_from_silences(silences, duration, min_speech=0.25):
    if not duration or duration <= 0:
        return []

    ranges = []
    cursor = 0.0
    for start, end in sorted(silences):
        start = max(0.0, min(float(start), float(duration)))
        end = max(start, min(float(end), float(duration)))
        if start - cursor >= min_speech:
            ranges.append((round(cursor, 3), round(start, 3)))
        cursor = max(cursor, end)

    if float(duration) - cursor >= min_speech:
        ranges.append((round(cursor, 3), round(float(duration), 3)))
    return ranges


def _fixed_ranges(duration, max_segment_duration=25.0):
    if not duration or duration <= 0:
        return []
    ranges = []
    start = 0.0
    while start < duration:
        end = min(float(duration), start + max_segment_duration)
        if end > start:
            ranges.append((round(start, 3), round(end, 3)))
        start = end
    return ranges


def _group_speech_ranges(ranges, max_gap=1.2, max_segment_duration=25.0, min_segment_duration=3.0):
    if not ranges:
        return []

    grouped = []
    current_start, current_end = ranges[0]
    for start, end in ranges[1:]:
        gap = start - current_end
        would_span = end - current_start
        if gap <= max_gap and would_span <= max_segment_duration:
            current_end = end
        else:
            grouped.append([current_start, current_end])
            current_start, current_end = start, end
    grouped.append([current_start, current_end])

    merged = []
    for start, end in grouped:
        if merged and end - start < min_segment_duration:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return [(round(start, 3), round(end, 3)) for start, end in merged if end > start]


def _merge_ranges_to_count(ranges, target_count):
    if target_count <= 0 or len(ranges) <= target_count:
        return ranges

    total_duration = sum(max(end - start, 0.0) for start, end in ranges)
    target_duration = total_duration / target_count if target_count else total_duration
    merged = []
    current_start, current_end = ranges[0]
    current_duration = current_end - current_start

    for start, end in ranges[1:]:
        remaining_ranges = len(ranges) - len(merged)
        remaining_targets = target_count - len(merged)
        if current_duration >= target_duration and remaining_ranges > remaining_targets:
            merged.append((round(current_start, 3), round(current_end, 3)))
            current_start, current_end = start, end
            current_duration = end - start
        else:
            current_end = end
            current_duration += end - start

    merged.append((round(current_start, 3), round(current_end, 3)))
    if len(merged) > target_count:
        merged[target_count - 1] = (merged[target_count - 1][0], merged[-1][1])
        merged = merged[:target_count]
    return merged


def _assign_text_to_ranges(text, ranges):
    units = _split_text_units(text)
    if not units or not ranges:
        return []

    if len(ranges) > len(units):
        ranges = _merge_ranges_to_count(ranges, len(units))

    weights = [max(1, len(_tokenize_for_timestamps(unit)) or len(unit)) for unit in units]
    total_weight = sum(weights)
    total_duration = sum(max(end - start, 0.0) for start, end in ranges) or 1.0
    cumulative_duration = 0.0
    consumed_weight = 0
    unit_index = 0
    segments = []

    for idx, (start, end) in enumerate(ranges):
        remaining_ranges = len(ranges) - idx
        if idx == len(ranges) - 1:
            segment_units = units[unit_index:]
        else:
            cumulative_duration += max(end - start, 0.0)
            target_weight = total_weight * (cumulative_duration / total_duration)
            segment_units = []
            while unit_index < len(units) - (remaining_ranges - 1):
                if segment_units and consumed_weight >= target_weight:
                    break
                segment_units.append(units[unit_index])
                consumed_weight += weights[unit_index]
                unit_index += 1

        segment_text = _collapse_ws("".join(segment_units))
        if segment_text:
            segments.append(
                {
                    "id": len(segments),
                    "start": round(float(start), 3),
                    "end": round(float(end), 3),
                    "text": segment_text,
                    "speaker": None,
                }
            )

    return segments


def build_audio_activity_segments(
    input_path,
    text,
    duration,
    silence_noise="-30dB",
    silence_duration=0.5,
    max_segment_duration=25.0,
):
    """Build approximate transcript segments from ffmpeg silencedetect output."""
    if not text or not duration or duration <= 0:
        return []

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-nostats",
                "-i",
                input_path,
                "-af",
                f"silencedetect=noise={silence_noise}:d={silence_duration}",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        print(f"  [WARN] ffmpeg unavailable for audio-activity timestamps: {exc}", file=sys.stderr)
        return []

    if result.returncode != 0:
        message = result.stderr.strip().splitlines()[-1:] or ["unknown ffmpeg error"]
        print(f"  [WARN] ffmpeg silencedetect failed: {message[0]}", file=sys.stderr)
        return []

    silences = _parse_silence_intervals(result.stderr, duration)
    speech_ranges = _speech_ranges_from_silences(silences, duration)
    if speech_ranges:
        ranges = _group_speech_ranges(
            speech_ranges,
            max_segment_duration=max_segment_duration,
        )
    else:
        ranges = _fixed_ranges(duration, max_segment_duration=max_segment_duration)
    return _assign_text_to_ranges(text, ranges)


def _build_duration_fallback_segment(text, duration):
    if not text or duration is None or duration <= 0:
        return []
    return [
        {
            "id": 0,
            "start": 0.0,
            "end": round(float(duration), 3),
            "text": text,
            "speaker": None,
        }
    ]


def build_transcript_payload(result, input_path, language, duration=None, punc_model=None):
    """Build the stable transcript JSON contract consumed by downstream skills."""
    raw_text = _extract_raw_text(result)
    segments, timestamp_source = _extract_segments(result, raw_text, duration)

    if segments:
        if punc_model:
            for segment in segments:
                segment["text"] = _apply_punctuation(punc_model, segment["text"])
        plain_text = _collapse_ws(" ".join(segment["text"] for segment in segments))
    else:
        plain_text = _strip_tags(raw_text)
        if punc_model:
            plain_text = _apply_punctuation(punc_model, plain_text)
        segments = _build_duration_fallback_segment(plain_text, duration)
        if segments:
            timestamp_source = "duration_fallback"

    word_segments, word_timestamp_source = _parse_word_entries(result, duration)
    if not word_segments:
        word_segments, word_timestamp_source = _words_from_root_timestamps(result, plain_text, duration)
    if not word_segments and segments:
        word_segments = _estimate_word_segments(segments)
        word_timestamp_source = "estimated_from_segments"

    return {
        "source": os.path.abspath(input_path),
        "language": language,
        "duration": duration,
        "text": plain_text,
        "segments": segments,
        "word_segments": word_segments,
        "raw": _json_safe(result),
        "metadata": {
            "model": "iic/SenseVoiceSmall",
            "punctuation_model": "ct-punc" if punc_model else None,
            "timestamp_source": timestamp_source,
            "word_timestamp_source": word_timestamp_source or "none",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        },
    }


def format_timestamped_text(payload):
    segments = payload.get("segments") or []
    if not segments:
        return payload.get("text", "")

    lines = []
    for segment in segments:
        speaker = segment.get("speaker")
        speaker_prefix = f"{speaker} " if speaker else ""
        lines.append(
            f"[{_format_ts(segment['start'])} - {_format_ts(segment['end'])}] "
            f"{speaker_prefix}{segment['text']}"
        )
    return "\n".join(lines) + "\n"


def write_transcript_outputs(payload, output_dir, output_stem):
    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(output_dir, f"{output_stem}.txt")
    json_path = os.path.join(output_dir, f"{output_stem}.json")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(format_timestamped_text(payload))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return txt_path, json_path


def apply_audio_activity_fallback(payload, input_path, duration):
    if payload.get("metadata", {}).get("timestamp_source") != "duration_fallback":
        return payload

    segments = build_audio_activity_segments(input_path, payload.get("text", ""), duration)
    if len(segments) <= 1:
        return payload

    payload["segments"] = segments
    payload["word_segments"] = _estimate_word_segments(segments)
    payload["metadata"]["timestamp_source"] = "audio_activity_fallback"
    payload["metadata"]["word_timestamp_source"] = "estimated_from_audio_activity"
    return payload


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

    model_path = _cached_model_dir("iic", "SenseVoiceSmall") or SENSEVOICE_MODEL_ID
    print(f"Loading SenseVoiceSmall ASR model...")
    t0 = time.time()
    asr = pipeline(
        task=Tasks.auto_speech_recognition,
        model=model_path,
        device=device,
    )
    print(f"  ASR model loaded in {time.time() - t0:.1f}s")
    return asr


def load_punc_model():
    """Load ct-punc model."""
    from funasr import AutoModel

    model_path = _cached_model_dir("iic", CT_PUNC_CACHE_NAME) or CT_PUNC_MODEL_ID
    print(f"Loading ct-punc model...")
    t0 = time.time()
    model = AutoModel(model=model_path, disable_update=True)
    print(f"  Punctuation model loaded in {time.time() - t0:.1f}s")
    return model


def probe_duration(input_path):
    """Return media duration in seconds when ffprobe is available."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                input_path,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        print(f"  [WARN] ffprobe unavailable, duration omitted: {exc}", file=sys.stderr)
        return None

    if result.returncode != 0:
        message = result.stderr.strip()
        print(f"  [WARN] ffprobe failed, duration omitted: {message}", file=sys.stderr)
        return None

    try:
        return round(float(result.stdout.strip()), 3)
    except ValueError:
        return None


def run_asr(asr_pipeline, input_path, language):
    """Run ASR, requesting sentence timestamps when the backend supports it."""
    try:
        return asr_pipeline(input=input_path, language=language, sentence_timestamp=True)
    except TypeError as exc:
        if "sentence_timestamp" not in str(exc):
            raise
        print(f"  [WARN] ASR backend rejected sentence_timestamp; retrying without it: {exc}", file=sys.stderr)
        return asr_pipeline(input=input_path, language=language)


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
    print(f"        {output_dir}/{output_stem}.json")
    print(f"Device: {args.device}  Language: {args.language}")
    duration = probe_duration(input_path)
    if duration:
        print(f"Duration: {duration:.1f}s")

    asr_pipeline = load_asr_pipeline(args.device)
    punc_model = load_punc_model()

    t0 = time.time()
    result = run_asr(asr_pipeline, input_path, args.language)
    print(f"  ASR done in {time.time() - t0:.1f}s")

    print(f"  Restoring punctuation...")
    t0 = time.time()
    payload = build_transcript_payload(
        result,
        input_path=input_path,
        language=args.language,
        duration=duration,
        punc_model=punc_model,
    )
    payload = apply_audio_activity_fallback(payload, input_path, duration)
    print(f"  Punctuation done in {time.time() - t0:.1f}s")

    txt_path, json_path = write_transcript_outputs(payload, output_dir, output_stem)
    print(f"Transcript saved: {txt_path}")
    print(f"Transcript JSON saved: {json_path}")
    print(
        "Timestamp source: "
        f"{payload['metadata']['timestamp_source']} "
        f"(word_segments: {payload['metadata']['word_timestamp_source']})"
    )


if __name__ == "__main__":
    main()
