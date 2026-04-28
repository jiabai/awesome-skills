# 工作流治理与完成门禁

本文件总结 Open SkillHub 中最值得复用的项目规范。它回答三个问题：

1. 一个 AI 友好项目的治理文档应该怎么分层？
2. 什么任务需要 spec、ExecPlan 和任务清单？
3. 什么时候可以声明工作完成？

---

## 文档分层原则

| 文档 | 职责 | 规则 |
|------|------|------|
| `AGENTS.md` | 自动加载的入口地图 | 保持短小，只放快速入口、核心信念、常用命令和关键约束摘要 |
| `WORKFLOW.md` | 项目怎么推进任务 | 定义从需求到实现的默认流程和轻量路径 |
| `docs/EXECUTION_GATES.md` | 什么条件下算完成 | 定义硬门禁、软门禁、各区域验证和最终交付格式 |
| `docs/DESIGN.md` | 稳定设计规范 | 放跨功能长期有效的设计和代码边界 |
| `docs/SECURITY.md` | 稳定安全基线 | 涉及认证、密钥、存储、权限、外部输入时生成 |
| `docs/design-docs/` | 持久设计决策 | 放跨任务有效的架构决策和设计说明，不放流水账 |
| `docs/product-specs/` | 用户可见意图 | 放功能目标、范围、非目标、场景、约束和验收标准 |
| `docs/exec-plans/` | 实施计划和恢复上下文 | `active/` 放进行中计划，`completed/` 放完成或废弃后的历史 |
| `docs/references/` | 外部资料和接口参考 | 放 LLM 友好的供应商文档、SOP、接口说明 |

规则：

- `AGENTS.md` 是入口，不是百科全书。详细规则进入 `docs/`，然后从 `AGENTS.md` 链接过去。
- 快速入口必须只列真实存在的相对路径，避免死链。
- 文档移动或新增索引时，同步更新对应 `index.md`。
- 长期规则放 `docs/DESIGN.md`、`docs/SECURITY.md` 或 `docs/design-docs/`；任务过程放 ExecPlan；用户意图放 product spec。
- 文档描述已实现行为时，必须 inspect 对应代码路径，避免把目标设计写成事实。

## Constitution

成熟项目应该有一组“宪法”文档，作为非平凡任务开始前的稳定上下文。默认组合：

- 根级 `AGENTS.md`
- `docs/design-docs/core-beliefs.md`
- `docs/ARCHITECTURE.md` 或 `ARCHITECTURE.md`
- `docs/DESIGN.md`
- `docs/SECURITY.md`
- 当前改动区域最近的模块级 `AGENTS.md`

如果项目很小，没有独立 `docs/`，就把 3-5 条核心信念、架构不变量和安全约束写入根级 `AGENTS.md`。项目增长后再拆到 `docs/`。

## 默认五阶段流程

除非任务明显低风险，否则按以下流程推进：

1. **Constitution and context**：从根级 `AGENTS.md` 开始，读最窄相关规则、架构、安全和设计基线。
2. **Spec**：如果改变用户可见行为、新增边界、影响安全/数据/部署，创建或更新 `docs/product-specs/YYYY-MM-DD-<slug>.md`。
3. **Technical plan**：创建 `docs/exec-plans/active/<slug>-plan.md`，说明文件范围、实施顺序、验证方式和需要持续记录的决策。
4. **Task breakdown**：把计划拆成小而可验证的任务；任务多时使用 `docs/exec-plans/active/<slug>-tasks.md`。
5. **Implementation and validation**：先 inspect，再做最小端到端改动，逐步验证，并持续更新 active ExecPlan。

人类确认点：

- 创建或实质修改 spec 后暂停。
- 创建或实质修改 ExecPlan 后暂停。
- 产出大型任务清单后暂停。
- 用户明确要求直接实现且任务满足轻量路径时，可以不暂停。

## 轻量路径

只有同时满足以下条件才可跳过完整 spec -> plan -> tasks 流程：

- 低风险。
- 改动范围小，可直接 review。
- 不新增产品、架构、数据、部署或安全边界。
- 不实质改变认证、权限、持久化、API contract 或运行时行为。

轻量路径仍然必须：

1. 读取 constitution 和最近的 `AGENTS.md`。
2. Inspect 要改的代码路径或文档路径。
3. 做最小端到端修复。
4. 运行相关 focused validation；文档或流程改动必须跑文档结构验证。
5. 最终说明已验证项、未运行项和残余风险。

## Product Spec 标准

当任务改变用户可见行为或引入新边界时，先写 product spec。

推荐文件名：

```text
docs/product-specs/YYYY-MM-DD-<feature-slug>.md
```

推荐结构：

```markdown
# <功能标题>

## 背景
当前问题、用户痛点或现有行为。

## 目标
完成后用户能做什么，列成 2-5 条。

## 非目标
明确本次不做什么，防止范围漂移。

## 使用场景
2-4 个真实使用场景。

## 约束
认证、数据形状、兼容性、部署、安全、性能或 UI 边界。

## 验收标准
可观察、可验证的结果。
```

规则：

- spec 写“要什么”和“不要什么”，不要写流水账式实现过程。
- 实施进度进入 ExecPlan，不进入 spec。
- 当 spec 对应索引存在时，同步更新 `docs/product-specs/index.md`。

## ExecPlan 生命周期

ExecPlan 是活文档。计划处于 active 时，以下章节要随工作推进更新：

- `Progress`
- `Surprises & Discoveries`
- `Decision Log`
- `Outcomes & Retrospective`

完成后：

1. 将计划从 `docs/exec-plans/active/` 移到 `docs/exec-plans/completed/`。
2. 更新 active 和 completed 的 `index.md`。
3. 保留验证结果、遗留风险和后续工作。
4. 若计划被替代或取消，也移动到 completed 并写明原因。

## 任务清单标准

任务清单可以在 ExecPlan 的 `Progress` 里，也可以拆成 sibling 文件：

```text
docs/exec-plans/active/<feature-slug>-tasks.md
```

任务拆分规则：

- 每项任务具体、可独立验证。
- 显式写出依赖关系。
- 写明会触碰的文件或模块区域。
- 每个 meaningful batch 都要附验证期望。
- 执行级小任务可以继续用根级 `TASKS.md`；非平凡功能的任务清单放 `docs/exec-plans/active/<feature-slug>-tasks.md`，不要把同一粒度的内容重复写两处。

## 技术债规则

当问题跨多个文件、多个任务或无法在当前计划内消化时，记录到：

```text
docs/exec-plans/tech-debt-tracker.md
```

推荐字段：

| Topic | Why it matters | Source | Removal Condition |
|------|----------------|--------|-------------------|

规则：

- 技术债要链接回最能解释问题的 plan、design doc 或代码位置。
- 解决后删除或降级，而不是让债务表变成墓地。
- 只属于当前任务的小 TODO 写入 active ExecPlan，不必进入全局债务表。

## 完成门禁

### 硬门禁

硬门禁未通过时，不要声明完成，除非用户明确接受残余风险：

- 已 inspect 受影响代码路径或文档事实来源。
- 受影响区域的最小有效测试或检查通过。
- 文档结构验证通过：

```bash
python scripts/validate_agents_docs.py --level ERROR
```

- touched active ExecPlan 的 `Progress`、`Decision Log`、验证记录是最新的。
- 架构、安全、流程、运行时 contract 或运维行为变化已同步到对应 durable docs。

### 软门禁

相关时应运行，跳过时说明原因：

- 更广范围回归测试。
- 手动运行时检查。
- 依赖或安全扫描。
- 覆盖率报告。

## 按风险选择验证

先跑最小有效验证，再按风险扩大。

| 改动范围 | 默认验证 |
|----------|----------|
| 文档 / 规则 / 计划 | `python scripts/validate_agents_docs.py --level ERROR` |
| 后端 / API / 数据 | focused tests -> 全量测试、lint、typecheck |
| 前端 / UI / runtime config | lint、相关测试；影响构建时跑 build |
| 桌面端 | 相关测试；影响打包或 Electron 类型时跑 build/typecheck |
| 跨区域 contract | 每个区域的门禁都要跑，并同步 spec / architecture / reference |

具体命令由项目技术栈决定。生成项目时，把常用验证命令写入 `AGENTS.md` 和 ExecPlan 的 `Validation and Acceptance`。

## 最终交付格式

最终说明必须透明列出：

```text
Validation:
- Passed: <command or check>
- Not run: <command or check> because <reason>
- Residual risk: <risk, or none>
```

很小的文档改动可以压缩成一句话，但必须说清文档验证结果。
