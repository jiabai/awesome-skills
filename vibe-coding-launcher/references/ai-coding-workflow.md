# AI Coding 执行流程

本文件只负责执行流程、判断方法和回写规则；`TASKS.md` 结构见 `task-management.md`，验证口径见 `validation-standards.md`。

## 目录

- [设计原则](#设计原则)
- [执行流程](#执行流程)
- [关键步骤](#关键步骤)
- [验证策略](#验证策略)
- [与 ExecPlan 的关系](#与-execplan-的关系)

---

## 设计原则

- **入口地图**：`AGENTS.md` 是默认读取入口和关键约束摘要，子文档展开细节但不写冲突规则。
- **层次继承**：从最近的 `AGENTS.md` 起向上继承，模块级只写特有内容。
- **避免重复**：共享规则放上层，本地只补差异。
- **回写触发**：新增或变更子文档时，要同步检查并回写 `AGENTS.md`。
- **自动标注**：生成的文档要带注释，提醒编辑源头而非产物。
- **入口分层**：`AGENTS.md` 只做地图，完整流程放 `WORKFLOW.md`，完成标准放 `docs/EXECUTION_GATES.md`。

---

## 执行流程

### 日常开发流程

1. 定位最近的 `AGENTS.md`，先读它，再向上继承规则。
2. Inspect 现有实现、调用点、测试和相关文档。
3. 判断是否需要创建 `docs/topic.md`、根级 `TASKS.md` 或 `docs/exec-plans/active/<slug>-tasks.md` checklist。
4. 判断是否需要 product spec；改变用户可见行为、新边界、安全/数据/部署语义时，先写 `docs/product-specs/`。
5. 按任务粒度执行；小任务直接实现，大功能交给 ExecPlan。
6. 每完成一项就更新 `TASKS.md`，必要时原子提交。
7. 按最小 → 扩大 → 全量做验证。
8. 提交前检查 `AGENTS.md`、文档同步、约束一致性和完成门禁。

---

## 关键步骤

### 1. 定位最近的 `AGENTS.md`

- 从当前工作目录向上查找最近的 `AGENTS.md`。
- 先读最近的，再向上继承未覆盖规则。

### 2. Inspect 现有实现

- 修改代码前先读当前实现、相邻调用点、最近测试和相关文档。
- 不基于假设直接修改代码。

### 3. 设计判断

- **跨模块变更**：修改多个目录或共享接口/类型时，创建 `docs/topic.md` + `docs/exec-plans/active/<slug>-tasks.md` checklist；根级 `TASKS.md` 只记录当前断点恢复需要。
- **新架构决策**：添加新层级、新依赖方向、新抽象层时，创建 `docs/topic.md` 明确理由。
- **用户可见行为变更**：新增或修改 `docs/product-specs/YYYY-MM-DD-<slug>.md`，先确认目标、非目标和验收标准。
- **非平凡实施**：创建 `docs/exec-plans/active/<slug>-plan.md`，并在人类确认后执行。
- **单模块小改动**：只改单个目录且不触及共享接口/类型时，直接实现。

判断时先列出将修改的文件，再按目录分组，看是否涉及共享类型或共享接口。

### 4. 执行追踪

- `TASKS.md` 记录执行级任务；格式和写法见 `task-management.md`。
- 每完成一项就勾选一项，不要攒着一起改。

### 5. 原子提交

- 每完成一个可独立验证的小任务就更新 `TASKS.md` 并提交。
- 多项相关任务可以合并，但不能把未完成的内容一起提交。

### 6. 渐进验证

- 先跑最小验证，再决定是否扩大。
- 具体验证层次和跳过条件见 `validation-standards.md`。

### 7. 文档同步

- 提交前检查 `AGENTS.md` 是否需要更新。
- 新规则写入、过时规则删除，冲突时以 `AGENTS.md` 为准。

---

## 验证策略

- 只保留验证顺序：最小 → 扩大 → 全量。
- 更细的校验口径、命令和严重程度见 `validation-standards.md`。

---

## 与 ExecPlan 的关系

- 30 分钟内能完成的事，用本流程 + 根级 `TASKS.md`。
- 需要数小时到数天的功能，用 ExecPlan + `docs/exec-plans/active/<slug>-tasks.md`。
- ExecPlan 负责里程碑，本文件负责执行动作。
- ExecPlan 完成后移动到 `docs/exec-plans/completed/`，同步 active/completed 索引；跨任务技术债写入 `docs/exec-plans/tech-debt-tracker.md`。
