# 核心集文档模板（阶段 3）

本文件定义核心集模板——所有项目都必须生成或默认生成的根级治理文档。扩展集（`docs/` 下按需生成的文档、CONTEXT.md、ADR）模板见 `docs-templates.md`；product spec 模板见 `workflow-governance.md`；ExecPlan 及 `docs/exec-plans/` 目录模板见 `execplan-format.md`。

## AGENTS.md（简化版）

代理的入口地图，不是百科全书。控制在 150 行以内。**所有项目都必须生成**。

默认用于**根级 `AGENTS.md`**。子级/模块级 `AGENTS.md` 继承根级的项目级元数据（尤其是 `约束机制`），不要求重复维护。

### 模板

```markdown
# {项目名} AI Collaboration Rules

## 快速入口

<!-- 只列出已生成的文档路径，未生成的不列，避免死链 -->
- 架构：见 `docs/ARCHITECTURE.md`（如已生成），CLI/单文件项目见下方"架构"章节
- 设计规范：见 `docs/DESIGN.md`（如已生成）
- 核心信念：见 `docs/design-docs/core-beliefs.md`（如已生成，否则见下方）
- 执行清单：见 `TASKS.md`（如存在，全部完成后删除）
- 工作流：见 `WORKFLOW.md`（如已生成）
- 完成门禁：见 `docs/EXECUTION_GATES.md`（如已生成）
- 部署：见 `docs/DEPLOYMENT.md`（如已生成）
- 执行计划：见 `docs/exec-plans/active/`（如已生成）
- 技术债：见 `docs/exec-plans/tech-debt-tracker.md`（如已生成）

## 核心信念

<3-5 条不可协商的原则>

## 开发流程

<简短描述：描述任务 → 运行代理 → 创建PR → 代理审查>

## 架构

<!-- 仅 CLI/单文件项目需要此章节（替代 docs/ARCHITECTURE.md），控制在 20 行以内 -->
<!-- 多文件项目删除此章节，架构信息放 docs/ARCHITECTURE.md -->

概述：{一句话描述项目做什么}
关键文件：`{主文件名}`
架构不变量：
- {不变量 1}
- {不变量 2}

## 约束机制

<!-- 所有项目必须保留此章节，供验证脚本机器读取 -->
- 模式：`{agents-only 或 linter+agents}`
- 配置：`{N/A 或 ruff.toml / eslint.config.js / analysis_options.yaml / pyproject.toml}`

## 常用命令

- `{命令}` — 说明
```

要点：

- "架构"章节仅 CLI/单文件项目需要，只写概述 + 关键文件 + 2-3 条不变量。
- `agents-only` 模式的配置必须写 `N/A`；`linter+agents` 模式必须填真实约束文件路径。

## WORKFLOW.md

项目的默认做事流程。**默认生成**；极小一次性脚本可不单独生成，但必须在 AGENTS.md 开发流程中写明轻量路径。

```markdown
# Project Workflow

## Purpose

本文件定义项目默认工作流。目标是让非平凡改动先形成可审查的意图和计划，再进入实现。

## Mandatory Rule

除非任务是低风险、小范围、无新边界的轻量改动，否则按以下流程推进：

1. Constitution and context
2. Spec
3. Technical plan
4. Task breakdown
5. Implementation and validation

## Constitution

- `AGENTS.md`
- `docs/ARCHITECTURE.md`（或根级架构章节）
- `docs/DESIGN.md`（如存在）
- `docs/SECURITY.md`（如存在）
- 相关模块最近的 `AGENTS.md`（如存在）

## Spec

当任务改变用户可见行为、新增边界、影响认证/权限/数据/部署/安全时，在 `docs/product-specs/` 创建或更新 spec。

## Plan

非平凡任务在 `docs/exec-plans/active/` 创建 ExecPlan，并在计划确认后实现。

## Lightweight Path

轻量任务可以直接实现，但仍需 inspect、最小验证、必要文档同步和最终验证说明。

## File Placement

- 用户意图：`docs/product-specs/`
- 设计决策：`docs/design-docs/`
- 外部参考：`docs/references/`
- 进行中计划：`docs/exec-plans/active/`
- 完成计划：`docs/exec-plans/completed/`
- 技术债：`docs/exec-plans/tech-debt-tracker.md`
```

## TASKS.md

执行期间的临时任务清单，位于项目根目录（不要创建 `docs/TASKS.md`）。**所有项目必须生成**。

生命周期：创建（阶段 3）→ 执行期间持续更新 → 全部完成后删除。格式和写入标准见 `task-management.md`。

```markdown
# Tasks

## 进行中
- [ ] {任务描述} ✅ {验证命令或验证标准}

## 待办
- [ ] {任务描述} ✅ {验证命令或验证标准}

## 已完成
- [x] {任务描述}（{YYYY-MM-DD}）✅ {验证命令或验证标准}
```

## scripts/validate_agents_docs.py

**所有项目必须生成（核心集）**。生成方式：读取本 skill 的 `scripts/validate_agents_docs.py`，原样写入用户项目，不要定制。

用途：阶段 5 约束落地后校验核心文档、对话结束前检查知识新鲜度、恢复时确认文档状态。

```bash
python scripts/validate_agents_docs.py --level ERROR   # 只显示 ERROR
python scripts/validate_agents_docs.py --level WARN    # 显示 ERROR + WARN
python scripts/validate_agents_docs.py --project /path/to/project  # 指定项目目录
```

要点：仅用 Python 标准库；默认以脚本所在目录的上一级为项目根，在用户项目中可正确解析；验证规则见 `validation-standards.md`。

## AGENTS.md（成熟项目版）

**适用条件**（满足任一）：项目超过 3 个模块；多人协作；使用多个 AI 工具。默认用于根级 AGENTS.md 的完整版，行数 ≤140；模块级可复用章节结构，`约束机制` 继承根级。

| 章节 | 内容 | 条数 |
|------|------|------|
| **Scope** | 适用范围和边界 | 2-4 条 |
| **Do** | 应遵循的实践 | 3-5 条 |
| **Avoid** | 应避免的反模式 | 3-5 条 |
| **约束机制** | 显式声明约束模式和配置 | 2 条 |
| **Commands** | 常用命令清单 | 4-8 条 |
| **Tests** | 验证策略 | 2-4 条 |
| **Related Skills** | 相关参考链接 | 2-4 条 |

```markdown
# {模块名} AI Collaboration Rules

<!-- 由 vibe-coding-launcher 生成。如需修改，编辑项目元数据。 -->

## Scope

- [适用范围描述]
- [边界说明]

## Do

- [应遵循实践 1]
- [应遵循实践 2]
- [应遵循实践 3]

## Avoid

- [应避免反模式 1]
- [应避免反模式 2]
- [应避免反模式 3]

## 约束机制

- 模式：`linter+agents`
- 配置：`{ruff.toml 或 eslint.config.js / analysis_options.yaml / pyproject.toml，按映射表选择}`

## Commands

- `{命令}` [说明]
- `{命令}` [说明]

## Tests

- [验证策略 1]
- [验证策略 2]

## Related Skills

- `{相关文档路径}` [说明]
- `{相关文档路径}` [说明]
```

## 模板选择

- 刚启动（≤3 模块）→ 简化版（≤150 行）
- 成长中（>3 模块 / 多 AI 工具 / 多人协作 / 出现跨模块协作需求）→ 完整版（≤140 行）
- 层次继承：模块级 AGENTS.md 只写该模块特有内容，共享规则放上层；本地文件覆盖上层，不冲突时继承。
