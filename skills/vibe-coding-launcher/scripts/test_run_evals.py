#!/usr/bin/env python3
"""Tests for the vibe-coding-launcher eval harness."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("run_evals.py")
SPEC = importlib.util.spec_from_file_location("run_evals", SCRIPT_PATH)
assert SPEC is not None
run_evals = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = run_evals
SPEC.loader.exec_module(run_evals)


class RunEvalsTests(unittest.TestCase):
    def test_scorecard_includes_fixture_contents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "fixtures" / "recovery" / "AGENTS.md"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("# Agents\n\n## 快速入口\n", encoding="utf-8")

            data = {
                "evals": [
                    {
                        "id": 1,
                        "eval_name": "恢复",
                        "prompt": "接着做",
                        "expected_output": "读取上下文",
                        "assertions": [{"name": "读取", "check": "读取AGENTS.md"}],
                        "files": [
                            {
                                "path": "fixtures/recovery/AGENTS.md",
                                "description": "根级项目入口",
                            }
                        ],
                    }
                ]
            }

            cases, errors = run_evals.validate_suite_data(data)
            self.assertEqual(errors, [])

            output_dir = root / "scorecards"
            run_evals.write_scorecards(cases, output_dir, suite_dir=root)

            scorecard = (output_dir / "001-eval.md").read_text(encoding="utf-8")
            self.assertIn("## Fixture Files", scorecard)
            self.assertIn("fixtures/recovery/AGENTS.md", scorecard)
            self.assertIn("根级项目入口", scorecard)
            self.assertIn("## 快速入口", scorecard)
            self.assertLess(
                scorecard.index("## Fixture Files"),
                scorecard.index("## Response Under Test"),
            )

    def test_results_template_records_raw_response_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {
                "evals": [
                    {
                        "id": 2,
                        "eval_name": "常规迭代",
                        "prompt": "加开关",
                        "expected_output": "不启动流程",
                        "assertions": [{"name": "不启动", "check": "不启动8阶段"}],
                        "files": [],
                    }
                ]
            }
            cases, errors = run_evals.validate_suite_data(data)
            self.assertEqual(errors, [])

            result_path = root / "results.json"
            run_evals.write_results_template(cases, result_path)

            result = json.loads(result_path.read_text(encoding="utf-8"))
            item = result["results"][0]
            self.assertIn("response_under_test", item)
            self.assertIn("artifacts", item)
            self.assertIn("grader", item)
            self.assertIn("graded_at", item)
            self.assertIn("overall_notes", item)
            self.assertEqual(item["assertions"][0]["evidence"], "")

    def test_score_counts_pending_against_all_assertions(self) -> None:
        data = {
            "evals": [
                {
                    "id": 3,
                    "eval_name": "评分",
                    "prompt": "do it",
                    "expected_output": "ok",
                    "assertions": [
                        {"name": "a", "check": "A"},
                        {"name": "b", "check": "B"},
                    ],
                    "files": [],
                }
            ]
        }
        cases, errors = run_evals.validate_suite_data(data)
        self.assertEqual(errors, [])

        summary = run_evals.summarize(cases, {3: {"a": run_evals.Grade(passed=True)}})

        self.assertEqual(summary["totals"]["passed"], 1)
        self.assertEqual(summary["totals"]["missing"], 1)
        self.assertEqual(summary["totals"]["score"], 0.5)


if __name__ == "__main__":
    unittest.main()
