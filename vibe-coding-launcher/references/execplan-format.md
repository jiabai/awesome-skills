# ExecPlan 格式标准

## 目录

- [必需章节](#必需章节)
- [各章节详细规范](#各章节详细规范)
- [首个 ExecPlan 建议](#首个-execplan-建议)

---

## 必需章节

每个计划必须包含：

```markdown
# <简短、行动导向的描述>

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries,
Decision Log, and Outcomes & Retrospective must be kept up to date as work proceeds.

## Purpose / Big Picture
完成后用户能做什么新事情？如何看到它工作？

## Progress
- [ ] 待完成的里程碑（每条标注时间戳）

## Surprises & Discoveries
工作中发现的事实、证据和影响。

## Decision Log
重要决策、理由、日期和作者。

## Outcomes & Retrospective
完成结果、验证结果、遗留风险和后续工作。

## Context and Orientation
当前状态、关键文件、术语和需要先读的上下文。

## Plan of Work
按顺序列出工作批次。

## Concrete Steps
工作目录、完整命令行、预期输出

## Validation and Acceptance
启动方式、可观察行为、测试命令和预期结果
```

## 各章节详细规范

**Purpose / Big Picture**：用 1-2 句话回答"完成后用户能做什么新事情？"和"怎么看到它工作？"。不要写技术细节，只写用户可感知的结果。

**Progress**：列出所有待完成里程碑，每条前加 `- [ ]`，完成后改为 `- [x]` 并标注时间。里程碑粒度：每个里程碑是子功能可验证的完成节点（如"API 框架就绪"、"数据库 schema 完成"），对应 tasks.md 中的多条执行级任务。里程碑本身的完成条件是该里程碑下所有 tasks.md 任务均已勾选。

**Surprises & Discoveries**：记录工作中发现的新事实，包含 Evidence。不要把猜测写成结论。

**Decision Log**：记录会影响后续维护的选择，格式建议为 Decision / Rationale / Date/Author。

**Outcomes & Retrospective**：计划完成、废弃或被替代时更新。说明实际完成了什么、验证了什么、未验证什么、还有什么风险。

**Context and Orientation**：列出相关路径和为什么重要。恢复模式下先读这一节和 Progress。

**Plan of Work**：描述实施批次，帮助人类 review 范围。

**Concrete Steps**：每个步骤必须包含工作目录（相对于项目根目录）、完整可复制的命令行、预期输出示例。不要写"运行安装命令"，要写"运行 `pip install flask`"。

**Validation and Acceptance**：包含启动方式（如 `python app.py`）、可观察行为（如"浏览器打开 localhost:5000 看到 Hello World"）、测试命令和预期结果。

## 首个 ExecPlan 建议

推荐从最小可运行版本开始：
- Web应用：一个能访问的页面，返回 "Hello World"
- API服务：一个健康检查端点 `/health` 返回 200
- 命令行：一个能打印帮助信息的命令
- AI应用：一个能调用 API 并返回结果的脚本
- 单文件脚本：一个能运行并输出结果的 main 函数

文件保存到 `docs/exec-plans/active/`，文件名格式：`YYYY-MM-DD-简短描述.md`。

## 完成与归档

计划完成后：

1. 更新 `Outcomes & Retrospective`，写明通过的验证、未运行项和残余风险。
2. 将文件从 `docs/exec-plans/active/` 移到 `docs/exec-plans/completed/`。
3. 更新 `active/index.md` 和 `completed/index.md`。
4. 如果产生跨任务技术债，记录到 `docs/exec-plans/tech-debt-tracker.md`。
5. 不要把完成计划继续留在 active 目录。

## 进阶：开发循环

当项目完成首个 ExecPlan 并进入日常迭代后，逐步引入更高效的工作循环：

```
描述任务 → 运行代理（按 ExecPlan 执行）→ 验证结果 → 处理反馈 → 合并
```

核心原则：

| 原则 | 说明 |
|------|------|
| 短生命周期 | 每个 ExecPlan 聚焦一个功能，快速完成 |
| 最小阻塞 | 单个测试失败不阻塞整体，后续运行处理 |
| 修正便宜，等待昂贵 | 先完成再优化，不过度追求完美 |
| 代理自审查 | 代理执行后自行检查 linter 和测试，再交付人类审查 |

日常迭代的 ExecPlan 更轻量——可以省略 Context and Orientation 章节（已有 AGENTS.md 提供），但 Purpose、Progress、Concrete Steps、Validation 仍然必须。
