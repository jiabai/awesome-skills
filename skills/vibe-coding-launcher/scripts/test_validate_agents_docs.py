#!/usr/bin/env python3
"""Tests for the project documentation validator."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_agents_docs.py")
SPEC = importlib.util.spec_from_file_location("validate_agents_docs", SCRIPT_PATH)
assert SPEC is not None
validate_agents_docs = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validate_agents_docs
SPEC.loader.exec_module(validate_agents_docs)


def write_valid_agents(path: Path, *, include_alternatives: bool = False) -> None:
    workflow_line = "- 轻量流程：低风险小改动可直接 inspect、实现、验证。" if include_alternatives else "- 开发按 WORKFLOW.md 执行。"
    gates_line = "- 完成门禁：最终必须列出验证结果、未运行项和残余风险。" if include_alternatives else "- 完成标准见 docs/EXECUTION_GATES.md。"
    content = f"""# Demo AI Collaboration Rules

## 快速入口

- 架构：见 `docs/ARCHITECTURE.md`
{gates_line}

## 核心信念

- 保持边界清晰。
- 优先验证事实。
- 文档只记录稳定规则。

## 开发流程

{workflow_line}

## 约束机制

- 模式：`agents-only`
- 配置：`N/A`

## 常用命令

- `python scripts/validate_agents_docs.py --level ERROR` - 校验核心文档
- `python -m unittest discover scripts` - 运行脚本测试
"""
    path.write_text(content, encoding="utf-8")


def write_architecture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """# Architecture

## 概述

Demo project.

## 代码地图

- `src/` contains modules.

## 关键文件

- `src/main.py`

## 架构不变量

- Service owns business logic.
""",
        encoding="utf-8",
    )


def write_project_baseline(root: Path, *, include_alternatives: bool = False) -> None:
    write_valid_agents(root / "AGENTS.md", include_alternatives=include_alternatives)
    (root / "scripts").mkdir()
    (root / "scripts" / "validate_agents_docs.py").write_text("# copied validator\n", encoding="utf-8")
    write_architecture(root / "docs" / "ARCHITECTURE.md")


class ValidateAgentsDocsTests(unittest.TestCase):
    def test_missing_workflow_and_execution_gates_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project_baseline(root)

            results = validate_agents_docs.validate_project(root, validate_agents_docs.Severity.ERROR)
            errors = [result for result in results if result.severity == validate_agents_docs.Severity.ERROR]

            messages = {(result.path.name, result.message) for result in errors}
            self.assertIn(("WORKFLOW.md", "文件不存在，且 AGENTS.md 未包含轻量流程替代"), messages)
            self.assertIn(("EXECUTION_GATES.md", "文件不存在，且 AGENTS.md 未包含完成门禁摘要"), messages)

    def test_agents_md_alternatives_allow_missing_workflow_and_execution_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project_baseline(root, include_alternatives=True)

            results = validate_agents_docs.validate_project(root, validate_agents_docs.Severity.ERROR)
            errors = [result for result in results if result.severity == validate_agents_docs.Severity.ERROR]

            self.assertEqual(errors, [])

    def test_workflow_and_execution_gate_files_satisfy_core_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project_baseline(root)
            (root / "WORKFLOW.md").write_text("# Workflow\n\n## Lightweight Path\n", encoding="utf-8")
            (root / "docs" / "EXECUTION_GATES.md").write_text(
                "# Execution Gates\n\n## Hard Gates\n\n- Run validation.\n",
                encoding="utf-8",
            )

            results = validate_agents_docs.validate_project(root, validate_agents_docs.Severity.ERROR)
            errors = [result for result in results if result.severity == validate_agents_docs.Severity.ERROR]

            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
