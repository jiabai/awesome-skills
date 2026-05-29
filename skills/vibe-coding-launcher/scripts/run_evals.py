#!/usr/bin/env python3
"""Run and summarize vibe-coding-launcher skill evals.

This harness intentionally avoids pretending that keyword matching can judge
semantic agent behavior. It validates the eval suite, exports scorecards for
fresh-agent/manual review, and summarizes structured grading results.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = ROOT / "evals" / "evals.json"


@dataclass(frozen=True)
class EvalAssertion:
    name: str
    check: str


@dataclass(frozen=True)
class EvalCase:
    id: int
    name: str
    prompt: str
    expected_output: str
    assertions: list[EvalAssertion]
    files: list[str]


@dataclass
class Grade:
    passed: bool | None
    reason: str = ""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None


def validate_suite_data(data: Any) -> tuple[list[EvalCase], list[str]]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [], ["Suite root must be a JSON object"]

    evals = data.get("evals")
    if not isinstance(evals, list):
        return [], ["Suite must contain an 'evals' array"]

    cases: list[EvalCase] = []
    seen_ids: set[int] = set()

    for index, item in enumerate(evals, start=1):
        prefix = f"evals[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue

        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            errors.append(f"{prefix}.id must be an integer")
            continue
        if eval_id in seen_ids:
            errors.append(f"{prefix}.id duplicates {eval_id}")
            continue
        seen_ids.add(eval_id)

        eval_name = item.get("eval_name")
        prompt = item.get("prompt")
        expected_output = item.get("expected_output")
        assertions_data = item.get("assertions")
        files = item.get("files", [])

        if not isinstance(eval_name, str) or not eval_name.strip():
            errors.append(f"eval {eval_id}: eval_name must be a non-empty string")
            eval_name = f"eval-{eval_id}"
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"eval {eval_id}: prompt must be a non-empty string")
            prompt = ""
        if not isinstance(expected_output, str) or not expected_output.strip():
            errors.append(f"eval {eval_id}: expected_output must be a non-empty string")
            expected_output = ""
        if not isinstance(assertions_data, list) or not assertions_data:
            errors.append(f"eval {eval_id}: assertions must be a non-empty array")
            assertions_data = []
        if not isinstance(files, list):
            errors.append(f"eval {eval_id}: files must be an array when present")
            files = []

        assertions: list[EvalAssertion] = []
        seen_names: set[str] = set()
        for assertion_index, assertion in enumerate(assertions_data, start=1):
            assertion_prefix = f"eval {eval_id} assertion {assertion_index}"
            if not isinstance(assertion, dict):
                errors.append(f"{assertion_prefix}: must be an object")
                continue
            name = assertion.get("name")
            check = assertion.get("check")
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{assertion_prefix}: name must be a non-empty string")
                continue
            if name in seen_names:
                errors.append(f"{assertion_prefix}: duplicate assertion name {name!r}")
                continue
            seen_names.add(name)
            if not isinstance(check, str) or not check.strip():
                errors.append(f"{assertion_prefix}: check must be a non-empty string")
                check = ""
            assertions.append(EvalAssertion(name=name, check=check))

        cases.append(
            EvalCase(
                id=eval_id,
                name=str(eval_name),
                prompt=str(prompt),
                expected_output=str(expected_output),
                assertions=assertions,
                files=[str(path) for path in files],
            )
        )

    return sorted(cases, key=lambda case: case.id), errors


def filter_cases(cases: list[EvalCase], ids: str | None) -> list[EvalCase]:
    if not ids:
        return cases

    requested: set[int] = set()
    for raw_id in ids.split(","):
        raw_id = raw_id.strip()
        if not raw_id:
            continue
        try:
            requested.add(int(raw_id))
        except ValueError:
            raise SystemExit(f"Invalid eval id in --ids: {raw_id!r}") from None

    known_ids = {case.id for case in cases}
    unknown_ids = sorted(requested - known_ids)
    if unknown_ids:
        raise SystemExit(f"Unknown eval id(s): {', '.join(map(str, unknown_ids))}")

    return [case for case in cases if case.id in requested]


def write_scorecards(cases: list[EvalCase], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for case in cases:
        path = output_dir / f"{case.id:03d}-{slugify(case.name)}.md"
        lines = [
            f"# Eval {case.id}: {case.name}",
            "",
            "## Prompt",
            "",
            case.prompt,
            "",
            "## Expected Behavior",
            "",
            case.expected_output,
            "",
            "## Response Under Test",
            "",
            "<paste the fresh-agent response or artifact summary here>",
            "",
            "## Assertion Results",
            "",
        ]
        for assertion in case.assertions:
            lines.extend(
                [
                    f"### {assertion.name}",
                    "",
                    f"- Check: {assertion.check}",
                    "- Result: PASS | FAIL | PENDING",
                    "- Reason:",
                    "",
                ]
            )
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_results_template(cases: list[EvalCase], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    template = {
        "results": [
            {
                "id": case.id,
                "eval_name": case.name,
                "notes": "",
                "assertions": [
                    {
                        "name": assertion.name,
                        "passed": None,
                        "reason": "",
                    }
                    for assertion in case.assertions
                ],
            }
            for case in cases
        ]
    }
    output_path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    safe_chars: list[str] = []
    for char in value.lower():
        if char.isascii() and char.isalnum():
            safe_chars.append(char)
        elif char in {" ", "-", "_"}:
            safe_chars.append("-")
    slug = "".join(safe_chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "eval"


def normalize_grades(raw_assertions: Any) -> dict[str, Grade]:
    grades: dict[str, Grade] = {}

    if isinstance(raw_assertions, dict):
        iterable = raw_assertions.items()
        for name, raw_grade in iterable:
            grade = parse_grade(raw_grade)
            grades[str(name)] = grade
        return grades

    if isinstance(raw_assertions, list):
        for raw_grade in raw_assertions:
            if not isinstance(raw_grade, dict):
                continue
            name = raw_grade.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            grades[name] = parse_grade(raw_grade)

    return grades


def parse_grade(raw_grade: Any) -> Grade:
    if isinstance(raw_grade, bool):
        return Grade(passed=raw_grade)

    if not isinstance(raw_grade, dict):
        return Grade(passed=None, reason="Invalid grade entry")

    raw_passed = raw_grade.get("passed")
    if isinstance(raw_passed, bool):
        passed = raw_passed
    elif raw_passed is None:
        passed = None
    else:
        passed = None

    reason = raw_grade.get("reason", "")
    if not isinstance(reason, str):
        reason = str(reason)

    return Grade(passed=passed, reason=reason)


def load_results(path: Path) -> dict[int, dict[str, Grade]]:
    data = load_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise SystemExit("Results file must contain a 'results' array")

    results: dict[int, dict[str, Grade]] = {}
    for item in data["results"]:
        if not isinstance(item, dict):
            continue
        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            continue
        results[eval_id] = normalize_grades(item.get("assertions"))

    return results


def summarize(cases: list[EvalCase], grades_by_eval: dict[int, dict[str, Grade]] | None) -> dict[str, Any]:
    total_assertions = sum(len(case.assertions) for case in cases)
    suite_summary: dict[str, Any] = {
        "eval_count": len(cases),
        "assertion_count": total_assertions,
        "cases": [],
        "totals": {
            "passed": 0,
            "failed": 0,
            "pending": 0,
            "missing": 0,
            "extra": 0,
        },
    }

    for case in cases:
        expected_names = {assertion.name for assertion in case.assertions}
        grades = grades_by_eval.get(case.id, {}) if grades_by_eval is not None else {}
        case_summary = {
            "id": case.id,
            "name": case.name,
            "assertion_count": len(case.assertions),
            "passed": 0,
            "failed": 0,
            "pending": 0,
            "missing": 0,
            "extra": 0,
            "failures": [],
            "pending_assertions": [],
        }

        if grades_by_eval is None:
            case_summary["pending"] = len(case.assertions)
            case_summary["pending_assertions"] = [
                assertion.name for assertion in case.assertions
            ]
        else:
            for assertion in case.assertions:
                grade = grades.get(assertion.name)
                if grade is None:
                    case_summary["missing"] += 1
                    case_summary["pending_assertions"].append(assertion.name)
                elif grade.passed is True:
                    case_summary["passed"] += 1
                elif grade.passed is False:
                    case_summary["failed"] += 1
                    case_summary["failures"].append(
                        {
                            "name": assertion.name,
                            "reason": grade.reason,
                        }
                    )
                else:
                    case_summary["pending"] += 1
                    case_summary["pending_assertions"].append(assertion.name)

            case_summary["extra"] = len(set(grades) - expected_names)

        for key in ("passed", "failed", "pending", "missing", "extra"):
            suite_summary["totals"][key] += int(case_summary[key])
        suite_summary["cases"].append(case_summary)

    suite_summary["totals"]["score"] = (
        suite_summary["totals"]["passed"] / total_assertions
        if grades_by_eval is not None and total_assertions
        else None
    )
    return suite_summary


def print_human_summary(summary: dict[str, Any], *, has_results: bool) -> None:
    print(
        f"Eval suite: {summary['eval_count']} case(s), "
        f"{summary['assertion_count']} assertion(s)"
    )

    if not has_results:
        print("No results file supplied; suite validation only.")
        print("")
        print("Next steps:")
        print("  python scripts/run_evals.py --write-scorecards .eval-runs/scorecards")
        print("  python scripts/run_evals.py --write-results-template .eval-runs/results.json")
        print("  python scripts/run_evals.py --results .eval-runs/results.json")
        return

    for case in summary["cases"]:
        status = "PASS"
        if case["failed"] or case["missing"]:
            status = "FAIL"
        elif case["pending"]:
            status = "PENDING"

        print(
            f"[{status}] {case['id']} {case['name']}: "
            f"{case['passed']}/{case['assertion_count']} passed"
        )
        for failure in case["failures"]:
            reason = f" - {failure['reason']}" if failure["reason"] else ""
            print(f"  FAIL {failure['name']}{reason}")
        for name in case["pending_assertions"]:
            print(f"  PENDING {name}")
        if case["extra"]:
            print(f"  WARN {case['extra']} extra assertion result(s)")

    totals = summary["totals"]
    score = totals["score"]
    score_text = "n/a" if score is None else f"{score * 100:.1f}%"
    print("")
    print(
        "Totals: "
        f"{totals['passed']} passed, "
        f"{totals['failed']} failed, "
        f"{totals['pending']} pending, "
        f"{totals['missing']} missing, "
        f"{totals['extra']} extra; "
        f"score={score_text}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and summarize vibe-coding-launcher evals"
    )
    parser.add_argument(
        "--suite",
        type=Path,
        default=DEFAULT_SUITE,
        help=f"Eval suite JSON path (default: {DEFAULT_SUITE})",
    )
    parser.add_argument(
        "--ids",
        help="Comma-separated eval ids to include, e.g. 1,4,8",
    )
    parser.add_argument(
        "--results",
        type=Path,
        help="Structured results JSON to summarize",
    )
    parser.add_argument(
        "--write-scorecards",
        type=Path,
        help="Directory where markdown scorecards will be written",
    )
    parser.add_argument(
        "--write-results-template",
        type=Path,
        help="Path where a structured results JSON template will be written",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable summary JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any assertion is failed, pending, missing, or extra",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    suite_path = args.suite.resolve()
    suite_data = load_json(suite_path)
    cases, errors = validate_suite_data(suite_data)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2

    cases = filter_cases(cases, args.ids)
    if args.write_scorecards:
        write_scorecards(cases, args.write_scorecards.resolve())
    if args.write_results_template:
        write_results_template(cases, args.write_results_template.resolve())

    grades_by_eval = load_results(args.results.resolve()) if args.results else None
    summary = summarize(cases, grades_by_eval)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human_summary(summary, has_results=args.results is not None)
        if args.write_scorecards:
            print(f"Wrote scorecards to: {args.write_scorecards.resolve()}")
        if args.write_results_template:
            print(f"Wrote results template to: {args.write_results_template.resolve()}")

    if args.strict:
        totals = summary["totals"]
        if totals["failed"] or totals["pending"] or totals["missing"] or totals["extra"]:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
