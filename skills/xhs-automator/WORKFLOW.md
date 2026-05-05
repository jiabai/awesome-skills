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
- `docs/ARCHITECTURE.md`
- `docs/SECURITY.md`
- 相关模块的 `SKILL.md`

## Spec

当任务改变用户可见行为、新增边界、影响认证/权限/数据/部署/安全时，在 `docs/product-specs/` 创建或更新 spec。

## Plan

非平凡任务在 `docs/exec-plans/active/` 创建 ExecPlan，并在计划确认后实现。

## Lightweight Path

轻量任务可以直接实现，但仍需 inspect、最小验证、必要文档同步和最终验证说明。

轻量路径条件：
- 低风险
- 改动范围小，可直接 review
- 不新增产品、架构、数据、部署或安全边界
- 不实质改变认证、权限、持久化、API contract 或运行时行为

## File Placement

- 用户意图：`docs/product-specs/`
- 设计决策：`docs/design-docs/`
- 外部参考：`docs/references/`
- 进行中计划：`docs/exec-plans/active/`
- 完成计划：`docs/exec-plans/completed/`
- 技术债：`docs/exec-plans/tech-debt-tracker.md`
