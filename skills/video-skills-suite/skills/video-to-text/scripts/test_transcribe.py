import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("transcribe.py")
SPEC = importlib.util.spec_from_file_location("transcribe", SCRIPT_PATH)
transcribe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transcribe)


class TranscriptOutputTests(unittest.TestCase):
    def test_builds_segments_from_sensevoice_timestamp_tags(self):
        result = {
            "text": (
                "<|zh|><|NEUTRAL|><|Speech|><|withitn|>"
                "<|0.0|><|2.0|>大家好"
                "<|2.0|><|4.5|>欢迎回来"
            )
        }

        payload = transcribe.build_transcript_payload(
            result,
            input_path="demo.mp4",
            language="zh",
            duration=5.0,
            punc_model=None,
        )

        self.assertEqual(payload["text"], "大家好 欢迎回来")
        self.assertEqual(payload["metadata"]["timestamp_source"], "sensevoice_tags")
        self.assertEqual(
            payload["segments"],
            [
                {"id": 0, "start": 0.0, "end": 2.0, "text": "大家好", "speaker": None},
                {"id": 1, "start": 2.0, "end": 4.5, "text": "欢迎回来", "speaker": None},
            ],
        )
        self.assertGreater(len(payload["word_segments"]), 0)
        self.assertEqual(payload["word_segments"][0]["start"], 0.0)

    def test_normalizes_millisecond_sentence_info(self):
        result = {
            "text": "hello world",
            "sentence_info": [
                {"start": 0, "end": 1200, "text": "hello world"},
            ],
        }

        payload = transcribe.build_transcript_payload(
            result,
            input_path="demo.wav",
            language="en",
            duration=1.2,
            punc_model=None,
        )

        self.assertEqual(payload["metadata"]["timestamp_source"], "sentence_info")
        self.assertEqual(payload["segments"][0]["start"], 0.0)
        self.assertEqual(payload["segments"][0]["end"], 1.2)

    def test_keeps_zero_start_word_segments_from_structured_result(self):
        result = {
            "text": "hello",
            "word_segments": [
                {"word": "hello", "start": 0, "end": 500},
            ],
        }

        payload = transcribe.build_transcript_payload(
            result,
            input_path="demo.wav",
            language="en",
            duration=0.5,
            punc_model=None,
        )

        self.assertEqual(payload["metadata"]["word_timestamp_source"], "word_segments")
        self.assertEqual(payload["word_segments"][0]["start"], 0.0)
        self.assertEqual(payload["word_segments"][0]["end"], 0.5)

    def test_builds_duration_fallback_segment_when_timestamps_missing(self):
        result = {"text": "hello world"}

        payload = transcribe.build_transcript_payload(
            result,
            input_path="demo.wav",
            language="en",
            duration=3.5,
            punc_model=None,
        )

        self.assertEqual(payload["metadata"]["timestamp_source"], "duration_fallback")
        self.assertEqual(
            payload["segments"],
            [{"id": 0, "start": 0.0, "end": 3.5, "text": "hello world", "speaker": None}],
        )
        self.assertEqual(payload["metadata"]["word_timestamp_source"], "estimated_from_segments")
        self.assertGreater(len(payload["word_segments"]), 0)

    def test_writes_timestamped_txt_and_json_outputs(self):
        payload = {
            "source": "demo.mp4",
            "language": "zh",
            "duration": 2.0,
            "text": "大家好",
            "segments": [
                {"id": 0, "start": 0.0, "end": 2.0, "text": "大家好", "speaker": None}
            ],
            "word_segments": [],
            "raw": {},
            "metadata": {"timestamp_source": "sensevoice_tags"},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            txt_path, json_path = transcribe.write_transcript_outputs(
                payload,
                output_dir=tmpdir,
                output_stem="transcript",
            )

            self.assertEqual(Path(txt_path).name, "transcript.txt")
            self.assertEqual(Path(json_path).name, "transcript.json")
            self.assertIn("[00:00.000 - 00:02.000] 大家好", Path(txt_path).read_text(encoding="utf-8"))
            saved = json.loads(Path(json_path).read_text(encoding="utf-8"))
            self.assertEqual(saved["segments"][0]["text"], "大家好")

    def test_builds_audio_activity_segments_from_silence_log(self):
        log = "\n".join(
            [
                "[silencedetect] silence_start: 4.0",
                "[silencedetect] silence_end: 5.0 | silence_duration: 1.0",
                "[silencedetect] silence_start: 9.0",
                "[silencedetect] silence_end: 10.0 | silence_duration: 1.0",
            ]
        )

        silences = transcribe._parse_silence_intervals(log, duration=12.0)
        ranges = transcribe._speech_ranges_from_silences(silences, duration=12.0)
        segments = transcribe._assign_text_to_ranges(
            "第一句。第二句。第三句。",
            ranges,
        )

        self.assertEqual(silences, [(4.0, 5.0), (9.0, 10.0)])
        self.assertEqual(ranges, [(0.0, 4.0), (5.0, 9.0), (10.0, 12.0)])
        self.assertEqual(len(segments), 3)
        self.assertEqual(segments[0]["start"], 0.0)
        self.assertEqual(segments[-1]["end"], 12.0)

    def test_replaces_duration_fallback_with_audio_activity_segments(self):
        payload = {
            "text": "第一句。第二句。",
            "segments": [{"id": 0, "start": 0.0, "end": 8.0, "text": "第一句。第二句。", "speaker": None}],
            "word_segments": [],
            "metadata": {"timestamp_source": "duration_fallback"},
        }

        original = transcribe.build_audio_activity_segments
        try:
            transcribe.build_audio_activity_segments = lambda *_args, **_kwargs: [
                {"id": 0, "start": 0.0, "end": 3.0, "text": "第一句。", "speaker": None},
                {"id": 1, "start": 4.0, "end": 8.0, "text": "第二句。", "speaker": None},
            ]
            updated = transcribe.apply_audio_activity_fallback(payload, "demo.mp4", 8.0)
        finally:
            transcribe.build_audio_activity_segments = original

        self.assertEqual(updated["metadata"]["timestamp_source"], "audio_activity_fallback")
        self.assertEqual(len(updated["segments"]), 2)
        self.assertGreater(len(updated["word_segments"]), 0)


if __name__ == "__main__":
    unittest.main()
