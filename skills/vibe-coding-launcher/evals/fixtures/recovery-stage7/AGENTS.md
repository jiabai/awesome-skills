# Agents

## 快速入口

- 当前任务：见 `TASKS.md`
- 活跃计划：见 `docs/exec-plans/active/login-feature.md`
- 工作流：见 `WORKFLOW.md`

## 核心信念

- 先恢复上下文，再继续执行。
- 用户确认前不要跳到下一阶段。
- 所有任务必须带验证条件。

## 开发流程

1. 读取本文件和 `TASKS.md`。
2. 查看 active ExecPlan 的 Progress。
3. 输出当前断点和下一步候选。
4. 等用户确认后再执行。

## 常用命令

- `python scripts/validate_agents_docs.py --level ERROR`

## 约束机制

- 模式：`agents-only`
- 配置：`N/A`
