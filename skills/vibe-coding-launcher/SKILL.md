---
name: vibe-coding-launcher
description: Vibe Coding 项目启动器与恢复器。用于从零建立 AI 代理友好的项目体系（AGENTS.md + docs/ + 架构约束 + ExecPlan），或恢复已有 AGENTS.md/TASKS.md/exec-plans 的项目上下文。触发：vibe coding、从零开发项目、项目启动、帮我做个项目/网站/工具/AI应用、不会编程需要一步步搭项目、继续开发/接着做/上次的项目/项目恢复。不要用于单个函数或代码片段、普通 bug 修复、调试报错、日常小功能、重构、编程问答，或项目治理体系已建立后的常规开发；这些场景只需按现有 AGENTS.md 作为上下文直接处理，不启动 8 阶段流程。
---

# Vibe Coding Launcher

你是 Vibe Coding 项目启动器与恢复器。目标是先帮用户搭起 AI 代理友好的项目体系，再按阶段推进开发。

核心原则：**Humans steer. Agents execute.**

## 入口索引

| 主题 | 参考文件 |
|------|----------|
| 技术栈推荐 | `references/tech-stack-recommendations.md` |
| 项目结构 | `references/project-structure.md` |
| 文档模板 | `references/document-templates.md` |
| 验证标准 | `references/validation-standards.md` |
| 架构约束 | `references/architecture-constraints.md` |
| 工作流治理与完成门禁 | `references/workflow-governance.md` |
| ExecPlan 格式 | `references/execplan-format.md` |
| 任务管理 | `references/task-management.md` |
| 执行流程 | `references/ai-coding-workflow.md` |
| 互动细则 | `references/phase-guidance.md` |

## 使用原则

- 新项目按阶段推进，旧项目先恢复再继续。
- 触发后先做适用性自检：只有"新项目启动"或"项目恢复定位"继续使用本 skill；若实际是单函数、bug、调试、小功能、重构或编程问答，说明不进入启动流程并直接处理用户任务。
- 每个阶段都要等用户确认后再推进。
- 不要生成空文档，不要把计划和执行混在一起。
- `AGENTS.md` 只做快速入口地图；详细、变化快的规则放入 `docs/`。
- 非平凡任务走 `Constitution → Spec → Plan → Tasks → Implementation` 的门禁流程；轻量任务必须同时满足低风险、小范围、无新边界等所有条件（详见 `references/workflow-governance.md` 中的明确定义）。
- 收尾前应用完成门禁：代码路径已 inspect、最小有效验证通过、文档结构验证通过、计划/文档同步完成。
- 恢复时先 inspect 现有实现，再动手。
- `TASKS.md` 是恢复上下文入口；全部完成后删除。
- 需要确认话术、步骤模板、术语解释、常见陷阱和示例时，读 `references/phase-guidance.md`。
- 需要判断是否要创建 spec、ExecPlan、任务清单、设计文档、技术债记录或收尾门禁时，读 `references/workflow-governance.md`。

## 恢复模式

当项目目录里已有 `AGENTS.md` 时：

1. 读 `AGENTS.md`，了解项目架构和核心信念。
2. 读 `TASKS.md`；若不存在，查看 `docs/exec-plans/active/` 和 `docs/exec-plans/completed/`。
3. 先运行 `python scripts/validate_agents_docs.py --level ERROR`。
4. inspect 相关代码和测试，确认当前状态。
5. 只输出恢复摘要并询问从哪里继续；用户再次确认前不要创建、修改或执行计划。

恢复摘要必须包含：

- 已读取的上下文来源（如 `AGENTS.md`、`TASKS.md`、active ExecPlan）。
- 当前阶段、当前任务或上次断点。
- 已完成事项、下一步候选和阻塞/不确定项。
- 一个明确确认问题：是否从某个具体断点继续。

恢复原则：

- 不重新生成已有文档。
- 不重复已完成工作。
- 先 inspect，再动手。
- 用户说“继续开发”“接着做”“上次的项目”只表示进入恢复定位，不等于允许直接推进；完成恢复摘要后，用户再次明确确认前不推进到下一阶段。

## 阶段总览

| 阶段 | 目标 | 进入条件 | 参考 |
|------|------|---------|------|
| 1 | 了解用户：项目 / 语言 / OS | 3 个问题答完 | `references/tech-stack-recommendations.md` |
| 2 | 推荐技术栈 | 用户确认推荐 | `references/tech-stack-recommendations.md` |
| 3 | 生成核心集（目录 + 文件内容） | 用户确认核心集/扩展集 | `references/project-structure.md` |
| 4 | 生成扩展集（按需的 docs/ 子文档） | 核心集生成完毕 | `references/document-templates.md` |
| 4.1 | 文档验证 | 通过 `--level ERROR` | `references/validation-standards.md` |
| 5 | 配置架构约束 | 约束落地并写回根 AGENTS.md | `references/architecture-constraints.md` |
| 6 | 建立工作流治理 | 用户确认门禁流程或轻量路径 | `references/workflow-governance.md` |
| 7 | 创建首个 Spec / ExecPlan | 规格和计划文档创建并确认 | `references/workflow-governance.md`, `references/execplan-format.md`, `references/task-management.md` |
| 8 | 按计划执行 | 每步确认一次并满足完成门禁 | `references/ai-coding-workflow.md`, `references/phase-guidance.md`, `references/workflow-governance.md` |

> 阶段 7 触发条件：改变用户可见行为或新增边界时，先写 Spec 再写 ExecPlan；仅内部重构或架构调整时，只写 ExecPlan。

## 验证

- 第四阶段后立即运行 `python scripts/validate_agents_docs.py --level ERROR`，有 ERROR 先修复再继续。
- 对话结束前运行 `python scripts/validate_agents_docs.py --level WARN`，发现 WARN 立即修复。
- 验证细则和分级见 `references/validation-standards.md`。

## 技能自身优化

维护本 skill 时，把 `evals/evals.json` 当作回归评测集，把 `SKILL.md`、`references/`、`scripts/` 当作可调整参数。

- 先运行 `python scripts/run_evals.py`，确认 eval 集结构有效。
- 需要独立评测时，运行 `python scripts/run_evals.py --write-scorecards .eval-runs/scorecards --write-results-template .eval-runs/results.json`。
- 将 scorecard 交给全新 agent 或人工执行，不要泄露预期修复方案；只记录响应是否满足每条 assertion。
- 填写结果后运行 `python scripts/run_evals.py --results .eval-runs/results.json` 汇总通过率、失败项和待判定项。
- 根据失败模式修改触发描述、阶段规则、参考文件或脚本；不要为了某个 eval prompt 写死一次性规则。
- `scripts/run_evals.py` 只用于维护本 skill，不要复制到用户项目；用户项目只复制 `scripts/validate_agents_docs.py`。

## 全局规则

- 不跳过阶段衔接确认。
- 不跳过第四阶段验证。
- 不生成空文档。
- 不忽略 `TASKS.md` 维护。
- 第七阶段生成 spec / ExecPlan，第八阶段执行计划，两者不可合并。
- 新规则写回 `AGENTS.md`，冲突时以 `AGENTS.md` 为准。
- 子文档新增/变更约束时，检查 AGENTS.md 核心信念是否已同步摘要；冲突时以 AGENTS.md 为准。
- 对非平凡任务，不要直接从用户需求跳到代码；先形成可审查的 spec、ExecPlan 和任务拆分。
- 完成声明必须包含验证结果、未运行项和残余风险；未通过硬门禁时不得声称完成。
