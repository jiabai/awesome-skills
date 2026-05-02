# Execution Gates

## Purpose

本文件定义任务完成前必须满足的检查。验证应与风险成比例，并在最终交付中可见。

## Hard Gates

- 受影响代码路径或文档事实来源已 inspect。
- 受影响区域的最小有效测试或检查通过。
- 文档结构验证通过：`python scripts/validate_agents_docs.py --level ERROR`。
- touched active ExecPlan 的 Progress、Decision Log 和验证记录已更新。
- 架构、安全、流程、运行时 contract 或运维行为变化已同步到 durable docs。

## Soft Gates

- 更广范围回归测试：`uv run pytest`
- Lint 检查：`uv run ruff check .`
- 代码格式化：`uv run ruff format .`
- 手动运行时检查（CLI 命令执行验证）

跳过相关软门禁时，在最终说明或 active ExecPlan 中记录原因和残余风险。

## Definition Of Done

1. 请求行为已实现、修复，或明确记录为 out of scope。
2. 所有受影响区域的硬门禁通过。
3. 相关 spec、design doc、reference、AGENTS map 或 ExecPlan 已同步。
4. 新技术债已记录到 active plan 或 `docs/exec-plans/tech-debt-tracker.md`。
5. 最终交付列出 Passed、Not run 和 Residual risk。

## 最终交付格式

```text
Validation:
- Passed: <command or check>
- Not run: <command or check> because <reason>
- Residual risk: <risk, or none>
```
