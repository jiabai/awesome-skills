# 工作流治理与完成门禁

本文件回答三个问题：治理文档怎么分层？什么任务需要 spec、ExecPlan 和任务清单？什么时候可以声明完成？

## 文档分层原则

| 文档 | 职责 | 规则 |
|------|------|------|
| `AGENTS.md` | 自动加载的入口地图 | 保持短小，只放快速入口、核心信念、常用命令和关键约束摘要 |
| `WORKFLOW.md` | 项目怎么推进任务 | 定义从需求到实现的默认流程和轻量路径 |
| `docs/EXECUTION_GATES.md` | 什么条件下算完成 | 定义硬门禁、软门禁和最终交付格式 |
| `docs/DESIGN.md` | 稳定设计规范 | 放跨功能长期有效的设计和代码边界 |
| `docs/SECURITY.md` | 稳定安全基线 | 涉及认证、密钥、存储、权限、外部输入时生成 |
| `docs/design-docs/` | 持久设计决策 | 放跨任务有效的架构决策，不放流水账 |
| `docs/product-specs/` | 用户可见意图 | 放功能目标、范围、非目标、场景、约束和验收标准 |
| `docs/exec-plans/` | 实施计划和恢复上下文 | `active/` 放进行中，`completed/` 放完成或废弃后的历史 |
| `docs/references/` | 外部资料和接口参考 | 放 LLM 友好的供应商文档、SOP、接口说明 |

规则：AGENTS.md 是入口不是百科全书，详细规则进 `docs/` 再链接过去；快速入口只列真实存在的相对路径；文档移动或新增索引时同步 `index.md`；文档描述已实现行为时必须先 inspect 对应代码，避免把目标设计写成事实。

## Constitution

成熟项目在非平凡任务开始前读取的稳定上下文：根级 `AGENTS.md`、`docs/design-docs/core-beliefs.md`、`docs/ARCHITECTURE.md`（或 AGENTS.md 架构章节）、`docs/DESIGN.md`、`docs/SECURITY.md`、当前改动区域最近的模块级 `AGENTS.md`。

小项目没有独立 `docs/` 时，把 3-5 条核心信念、架构不变量和安全约束写入根级 `AGENTS.md`；项目增长后再拆。

## 默认五阶段流程

除非任务明显低风险，否则按以下流程推进：

1. **Constitution and context**：从根级 `AGENTS.md` 开始，读最窄相关规则、架构、安全和设计基线。
2. **Spec**：改变用户可见行为、新增边界、影响安全/数据/部署时，创建或更新 `docs/product-specs/YYYY-MM-DD-<slug>.md`。
3. **Technical plan**：创建 `docs/exec-plans/active/<slug>-plan.md`，说明文件范围、实施顺序、验证方式和需持续记录的决策。
4. **Task breakdown**：把计划拆成小而可验证的任务；任务多时用 `docs/exec-plans/active/<slug>-tasks.md`。
5. **Implementation and validation**：先 inspect，再做最小端到端改动，逐步验证，持续更新 active ExecPlan。

人类确认点：创建或实质修改 spec / ExecPlan 后暂停；产出大型任务清单后暂停。用户明确要求直接实现且任务满足轻量路径时可不暂停。

## 非平凡任务的定义

满足以下**任一**条件即为非平凡任务，需要先形成可审查的 spec 和 plan 再实现：

| 维度 | 判断标准 | 示例 |
|------|---------|------|
| 用户可见影响 | 改变用户可见行为或体验 | 新增功能、修改UI、改API响应格式 |
| 边界新增 | 新增产品/架构/数据/部署/安全边界 | 新增模块、数据表、外部服务依赖 |
| 风险等级 | 影响认证、权限、持久化、数据安全或部署 | 修改认证逻辑、权限控制 |
| 范围大小 | 跨多个模块或目录修改 | 同时改 `ui/`、`service/`、`repo/` |
| 时间预估 | 预估超过 30 分钟 | 数小时到数天的功能开发 |
| 架构变更 | 新增层级、新依赖方向、新抽象层 | 引入设计模式、重构核心架构 |

### 常见场景对照表

| 场景 | 是否非平凡 | 应走流程 |
|------|-----------|---------|
| 修复 typo、调整文案 | ❌ 否 | 轻量路径 |
| 修改单个函数的内部实现（不改变接口） | ❌ 否 | 轻量路径 |
| 添加新的 API 端点 | ✅ 是 | 完整流程（需要 spec） |
| 重构核心模块架构 | ✅ 是 | 完整流程（需要 design doc） |
| 修改数据库 schema | ✅ 是 | 完整流程（需要 spec） |
| 调整 UI 样式（不改变交互） | ❌ 否 | 轻量路径 |
| 新增用户可见功能 | ✅ 是 | 完整流程（需要 spec） |
| 修改认证逻辑 | ✅ 是 | 完整流程（需要 spec） |
| 更新依赖版本（不涉及 breaking change） | ❌ 否 | 轻量路径 |
| 跨模块重构 | ✅ 是 | 完整流程（需要 ExecPlan） |

### 轻量路径的条件

**同时满足以下所有条件**才可跳过完整 spec → plan → tasks 流程：低风险（不影响认证/权限/数据安全/核心功能）；只改单个模块或目录且不触及共享接口/类型；无新边界；无实质变更（不改认证、权限、持久化、API contract、运行时行为）；预估 30 分钟内完成。

轻量路径仍然必须：读 constitution 和最近的 `AGENTS.md`；inspect 要改的代码或文档路径；做最小端到端修复；跑相关 focused validation（文档/流程改动必须跑文档结构验证）；最终说明已验证项、未运行项和残余风险。

## Product Spec 标准

当任务满足以下任一条件时，先写 product spec：改变用户可见行为；新增边界；影响认证/权限/数据/部署/安全；或功能范围需要人类确认。文件名 `docs/product-specs/YYYY-MM-DD-<feature-slug>.md`。

### index.md 模板

```markdown
# Product Specs Index

## Purpose

Product specs describe user-visible intent and boundaries before or alongside implementation work.

## Current Specs

| File | Scope |
|------|-------|
```

### 单个 spec 模板

```markdown
# {功能标题}

## 背景

## 目标

## 用户故事

（编号列表："作为<角色>，我想要<功能>，以便<好处>"；未做过需求采集的项目可省略本章节）

## 非目标

## 使用场景

## 约束

## 验收标准
```

规则：

- spec 写"要什么"和"不要什么"，不写流水账式实现过程；实施进度进 ExecPlan，不进 spec。
- 用户故事使用 `CONTEXT.md` 的标准术语（如已生成），不漂移到被避免的别名。
- spec 对应索引存在时，同步更新 `docs/product-specs/index.md`。

## ExecPlan 生命周期

ExecPlan 是活文档。active 期间 `Progress`、`Surprises & Discoveries`、`Decision Log`、`Outcomes & Retrospective` 随工作推进更新。

完成后：移到 `docs/exec-plans/completed/`；更新两个 `index.md`；保留验证结果、遗留风险和后续工作。被替代或取消的计划也移到 completed 并写明原因。

## 任务清单标准

任务清单可在 ExecPlan 的 `Progress` 里，也可拆成 sibling 文件 `docs/exec-plans/active/<feature-slug>-tasks.md`。

拆分规则：每项任务具体、可独立验证；显式写出依赖关系；写明触碰的文件或模块区域；每个 meaningful batch 附验证期望。执行级小任务用根级 `TASKS.md`；不要把同一粒度的内容重复写两处。

## 技术债规则

问题跨多个文件、多个任务或无法在当前计划内消化时，记录到 `docs/exec-plans/tech-debt-tracker.md`（模板见 `execplan-format.md`）。

规则：技术债链接回最能解释问题的 plan、design doc 或代码位置；解决后删除或降级，不让债务表变墓地；只属于当前任务的小 TODO 写 active ExecPlan，不进全局债务表。

## 完成门禁

### 硬门禁

硬门禁未通过时不要声明完成，除非用户明确接受残余风险：

- 已 inspect 受影响代码路径或文档事实来源。
- 受影响区域的最小有效测试或检查通过。
- 文档结构验证通过：`python scripts/validate_agents_docs.py --level ERROR`。
- touched active ExecPlan 的 `Progress`、`Decision Log`、验证记录是最新的。
- 非平凡任务已完成双轴自审（见下文），问题已修复或记录为技术债。
- 架构、安全、流程、运行时 contract 或运维行为变化已同步到对应 durable docs。

### 软门禁

相关时应运行，跳过时说明原因：更广范围回归测试、手动运行时检查、依赖或安全扫描、覆盖率报告。

### 双轴自审（非平凡任务必做）

声明完成前，对本次全部改动做两轴**独立**检查，分开报告。两轴不许互相掩盖：代码规范但做错了东西，或做对了东西但破坏项目约定，都算没完成。一轴通过一轴失败是常态——不合并成一个结论，也不替用户决定哪轴更重要。

**Spec 轴** — 改动是否忠实实现来源意图：逐条对照 spec 验收标准和用户故事（无 spec 的内部重构对照 ExecPlan 的 Purpose）；报告三类问题——要求了但缺失或只做一半、没要求但做了（范围蔓延）、看起来实现了但行为与描述不符。

**Standards 轴** — 改动是否符合项目自身标准：对照根级 AGENTS.md 核心信念、层间依赖方向（`architecture-constraints.md`）和 `docs/DESIGN.md`（如存在），叠加坏味道基线。每条是判断题不是铁律：linter 已强制的跳过，AGENTS.md 明确认可的以项目为准。

| 坏味道 | 信号 | 处理 |
|--------|------|------|
| 神秘命名 | 名字看不出做什么 | 改名；起不出诚实名字说明设计混浊 |
| 重复代码 | 同一逻辑形状多处出现 | 提取共享，两处调用 |
| 投机泛化 | 为不存在的需求加抽象/参数/配置项 | 删掉，等真实需求再加 |
| 散弹式修改 | 一个逻辑变更迫使多文件各改一点 | 聚拢进一个模块 |

报告两行固定并入下方"最终交付格式"的 Validation 块；两行只写自审结论，不重复验证命令。

## 按风险选择验证

先跑最小有效验证，再按风险扩大：

| 改动范围 | 默认验证 |
|----------|----------|
| 文档 / 规则 / 计划 | `python scripts/validate_agents_docs.py --level ERROR` |
| 后端 / API / 数据 | focused tests → 全量测试、lint、typecheck |
| 前端 / UI / runtime config | lint、相关测试；影响构建时跑 build |
| 桌面端 | 相关测试；影响打包或类型时跑 build/typecheck |
| 跨区域 contract | 每个区域的门禁都要跑，并同步 spec / architecture / reference |

具体命令由项目技术栈决定；生成项目时把常用验证命令写入 `AGENTS.md` 和 ExecPlan 的 `Validation and Acceptance`。

## 最终交付格式

最终说明必须透明列出：

```text
Validation:
- Passed: <command or check>
- Not run: <command or check> because <reason>
- Residual risk: <risk, or none>
Spec 自审：{逐条结论或"无发现"}
Standards 自审：{发现及处理或"无发现"}
```

前三行所有任务必填；自审两行仅非平凡任务必填。本块是最终交付说明的唯一格式来源，其他文件只引用不重复维护。很小的文档改动可压缩成一句话，但必须说清文档验证结果。
