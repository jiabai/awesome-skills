#!/usr/bin/env python3
"""Validate vibe-coding-launcher project documentation.

Checks:
- Core documents exist (AGENTS.md, ARCHITECTURE.md; tasks.md optional)
- AGENTS.md sections complete (simplified or full version)
- tasks.md uses checkbox format (if exists)
- Quick-entry links in AGENTS.md are valid
- Line count within limits

Severity levels:
- ERROR: Must fix before proceeding
- WARN: Should fix, but can continue
- INFO: Status information
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Severity(Enum):
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"


@dataclass
class ValidationResult:
    path: Path
    severity: Severity
    message: str

    def __str__(self) -> str:
        level = self.severity.value
        rel_path = self.path.relative_to(ROOT) if self.path.is_relative_to(ROOT) else self.path
        return f"[{level}] {rel_path}: {self.message}"


# 简化版必需章节（"架构"章节仅 CLI/单文件项目需要，在下方 cli_project 条件检查中单独校验）
SIMPLE_REQUIRED = ["快速入口", "核心信念", "开发流程", "常用命令"]

# 完整版必需章节
FULL_REQUIRED = ["Scope", "Do", "Avoid", "Commands", "Tests", "Related Skills"]

# 行数范围
MIN_LINES = 20
MAX_SIMPLE_LINES = 150
MAX_FULL_LINES = 140

# 生成注释模式
GEN_COMMENT_PATTERN = re.compile(
    r"<!-- 由 vibe-coding-launcher 生成.*-->",
    re.IGNORECASE,
)

# tasks.md checkbox 模式
CHECKBOX_PATTERN = re.compile(r"^- \[[ x]\]")

# 快速入口链接模式
QUICK_ENTRY_PATTERN = re.compile(r"`([^`]+\.md)`")

# 约束配置路径声明模式（匹配 "约束配置：`xxx`" 或 "约束配置: `xxx`"）
CONSTRAINT_CONFIG_PATTERN = re.compile(
    r"约束配置[：:]\s*`([^`]+)`",
)


def is_cli_project(root: Path) -> bool:
    """Detect CLI/single-file project by directory structure.

    A project is considered CLI/single-file if it has no src/ directory
    and either has no docs/ directory, or docs/ only contains exec-plans/
    (which is auto-generated for ExecPlan tracking and does not indicate
    a non-CLI project structure).
    """
    if (root / "src").exists():
        return False

    docs_dir = root / "docs"
    if not docs_dir.exists():
        return True

    # docs/ exists — check if it only contains exec-plans/ (按需生成的目录)
    entries = [p for p in docs_dir.iterdir()]
    if len(entries) == 1 and entries[0].name == "exec-plans":
        return True

    return False


def detect_version(headings: list[str]) -> str:
    """Detect AGENTS.md version (simplified or full)."""
    if "Scope" in headings:
        return "full"
    return "simple"


def validate_agents_md(path: Path, min_level: Severity, *, cli_project: bool = False) -> list[ValidationResult]:
    """Validate one AGENTS.md file."""
    results: list[ValidationResult] = []

    if not path.exists():
        results.append(ValidationResult(path, Severity.ERROR, "文件不存在"))
        return results

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    line_count = len(lines)

    # 检查行数
    if line_count < MIN_LINES:
        results.append(ValidationResult(path, Severity.ERROR, f"行数不足: {line_count} < {MIN_LINES}"))

    # 提取章节标题
    headings: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("## #"):
            heading = stripped[3:].strip()
            headings.append(heading)

    # 判断版本
    version = detect_version(headings)

    if version == "full":
        # 完整版检查
        if line_count > MAX_FULL_LINES:
            results.append(ValidationResult(path, Severity.WARN, f"完整版行数超限: {line_count} > {MAX_FULL_LINES}"))

        for section in FULL_REQUIRED:
            if section not in headings:
                results.append(ValidationResult(path, Severity.ERROR, f"完整版缺少章节: {section}"))

        results.append(ValidationResult(path, Severity.INFO, f"完整版, {line_count} 行"))
    else:
        # 简化版检查
        if line_count > MAX_SIMPLE_LINES:
            results.append(ValidationResult(path, Severity.WARN, f"简化版行数超限: {line_count} > {MAX_SIMPLE_LINES}"))

        for section in SIMPLE_REQUIRED:
            if section not in headings:
                results.append(ValidationResult(path, Severity.ERROR, f"简化版缺少章节: {section}"))

        results.append(ValidationResult(path, Severity.INFO, f"简化版, {line_count} 行"))

    # CLI/单文件项目：AGENTS.md 必须包含"架构"章节
    if cli_project and "架构" not in headings:
        results.append(ValidationResult(path, Severity.ERROR, "CLI/单文件项目缺少'架构'章节（替代 docs/ARCHITECTURE.md）"))

    # 检查快速入口链接有效性
    quick_entry_section = False
    for line in lines:
        if "快速入口" in line or "Quick Entry" in line:
            quick_entry_section = True
            continue
        if quick_entry_section and line.startswith("##"):
            break
        if quick_entry_section:
            for match in QUICK_ENTRY_PATTERN.finditer(line):
                linked_path = match.group(1)
                # 检查链接是否存在（相对于 AGENTS.md 所在目录）
                resolved = (path.parent / linked_path).resolve()
                if not resolved.exists():
                    results.append(ValidationResult(path, Severity.WARN, f"快速入口死链: {linked_path}"))

    # 检查约束配置文件路径声明（AGENTS.md 常用命令中声明了 "约束配置：`xxx`"）
    for line in lines:
        match = CONSTRAINT_CONFIG_PATTERN.search(line)
        if match:
            config_path = match.group(1)
            resolved = (path.parent / config_path).resolve()
            if not resolved.exists():
                results.append(ValidationResult(
                    resolved, Severity.WARN,
                    f"约束配置文件不存在（在 AGENTS.md 中声明）: {config_path}",
                ))

    return results


def validate_tasks_md(path: Path, min_level: Severity) -> list[ValidationResult]:
    """Validate tasks.md file (optional - may be deleted when all tasks complete)."""
    results: list[ValidationResult] = []

    if not path.exists():
        results.append(ValidationResult(path, Severity.INFO, "文件不存在（项目可能已全部完成）"))
        return results

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # 检查 checkbox 格式
    checkbox_count = len(CHECKBOX_PATTERN.findall(content))
    if checkbox_count == 0:
        results.append(ValidationResult(path, Severity.ERROR, "没有使用 checkbox 格式"))

    # 统计待办和已完成
    pending = len(re.findall(r"^- \[ \]", content))
    completed = len(re.findall(r"^- \[x\]", content))

    results.append(ValidationResult(path, Severity.INFO, f"{pending} 项待办, {completed} 项已完成"))

    return results


def validate_architecture_md(path: Path, min_level: Severity, *, cli_project: bool = False) -> list[ValidationResult]:
    """Validate docs/ARCHITECTURE.md file."""
    results: list[ValidationResult] = []

    if not path.exists():
        if cli_project:
            # CLI/单文件项目不需要 docs/ARCHITECTURE.md，架构信息在 AGENTS.md 中
            results.append(ValidationResult(path, Severity.INFO, "文件不存在（CLI/单文件项目，架构信息在 AGENTS.md 中）"))
        else:
            results.append(ValidationResult(path, Severity.ERROR, "文件不存在"))
        return results

    content = path.read_text(encoding="utf-8")

    # 检查必需章节
    required_sections = ["概述", "架构", "模块", "关键文件"]
    # 英文版本
    en_sections = ["Overview", "Architecture", "Module", "Key Files"]

    has_required = False
    for section in required_sections + en_sections:
        if section in content:
            has_required = True
            break

    if not has_required:
        results.append(ValidationResult(path, Severity.WARN, "缺少模块划分章节"))

    line_count = len(content.splitlines())
    results.append(ValidationResult(path, Severity.INFO, f"{line_count} 行"))

    return results


def validate_docs_structure(docs_dir: Path, min_level: Severity, *, cli_project: bool = False) -> list[ValidationResult]:
    """Validate docs/ directory structure."""
    results: list[ValidationResult] = []

    if not docs_dir.exists():
        if cli_project:
            results.append(ValidationResult(docs_dir, Severity.INFO, "docs/ 目录不存在（CLI/单文件项目，无需生成）"))
        else:
            results.append(ValidationResult(docs_dir, Severity.ERROR, "docs/ 目录不存在"))
        return results

    # 必需文件
    required = [
        docs_dir / "ARCHITECTURE.md",
    ]

    for path in required:
        if not path.exists():
            results.append(ValidationResult(path, Severity.ERROR, "必需路径不存在"))

    # 条件目录：exec-plans/ 按需生成，存在时检查子目录结构
    exec_plans_dir = docs_dir / "exec-plans"
    if exec_plans_dir.exists():
        for subdir in ["active", "completed"]:
            if not (exec_plans_dir / subdir).exists():
                results.append(ValidationResult(
                    exec_plans_dir / subdir, Severity.WARN,
                    f"exec-plans 子目录缺失: {subdir}"
                ))
    else:
        results.append(ValidationResult(
            exec_plans_dir, Severity.INFO,
            "目录不存在（按需生成，无需修复）"
        ))

    return results


def validate_project(root: Path, min_level: Severity) -> list[ValidationResult]:
    """Validate entire project documentation."""
    results: list[ValidationResult] = []

    cli = is_cli_project(root)

    # 核心文档
    agents_md = root / "AGENTS.md"
    tasks_md = root / "tasks.md"
    architecture_md = root / "docs" / "ARCHITECTURE.md"
    docs_dir = root / "docs"

    results.extend(validate_agents_md(agents_md, min_level, cli_project=cli))
    results.extend(validate_tasks_md(tasks_md, min_level))
    results.extend(validate_architecture_md(architecture_md, min_level, cli_project=cli))
    results.extend(validate_docs_structure(docs_dir, min_level, cli_project=cli))

    # 检查所有子目录 AGENTS.md
    for agents_path in root.rglob("AGENTS.md"):
        if agents_path != agents_md:
            results.extend(validate_agents_md(agents_path, min_level))

    return results


def filter_by_severity(results: list[ValidationResult], min_level: Severity) -> list[ValidationResult]:
    """Filter results by minimum severity level."""
    severity_order = [Severity.INFO, Severity.WARN, Severity.ERROR]
    min_index = severity_order.index(min_level)
    allowed = severity_order[min_index:]
    return [r for r in results if r.severity in allowed]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate vibe-coding-launcher documentation")
    parser.add_argument(
        "--level",
        choices=["ERROR", "WARN", "INFO"],
        default="INFO",
        help="Minimum severity level to show (default: INFO)",
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=None,
        help="Project root directory (default: script's parent)",
    )
    args = parser.parse_args()

    min_level = Severity(args.level)
    project_root = args.project or ROOT

    if not project_root.exists():
        print(f"[ERROR] Project root not found: {project_root}")
        return 1

    results = validate_project(project_root, min_level)
    filtered = filter_by_severity(results, min_level)

    # 按严重程度排序
    severity_order = [Severity.ERROR, Severity.WARN, Severity.INFO]
    filtered.sort(key=lambda r: severity_order.index(r.severity))

    # 输出结果
    for result in filtered:
        print(result)

    # 统计
    error_count = len([r for r in results if r.severity == Severity.ERROR])
    warn_count = len([r for r in results if r.severity == Severity.WARN])

    print(f"\n验证完成: {error_count} 个错误, {warn_count} 个警告")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())