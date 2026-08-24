# 扩展集文档模板（阶段 4，按需生成）

本文件定义扩展集模板——`docs/` 下按条件生成的文档，以及 CONTEXT.md 和 ADR。核心集（AGENTS.md、WORKFLOW.md、TASKS.md、验证脚本）模板见 `document-templates.md`；部署完整模板与引导规则见 `deployment-spec.md`。

## docs/EXECUTION_GATES.md

完成门禁，回答"什么时候可以说完成"。**生成条件**：多文件项目、Web/API/桌面项目、或任何需要测试/发布/交付标准的项目。

```markdown
# Execution Gates

## Purpose

本文件定义任务完成前必须满足的检查。验证应与风险成比例，并在最终交付中可见。

## Hard Gates

- 受影响代码路径或文档事实来源已 inspect。
- 受影响区域的最小有效测试或检查通过。
- 文档结构验证通过：`python scripts/validate_agents_docs.py --level ERROR`。
- touched active ExecPlan 的 Progress、Decision Log 和验证记录已更新。
- 非平凡任务完成双轴自审：Spec 轴（是否忠实实现来源意图）与 Standards 轴（是否符合项目自身标准）分开检查、分开报告；问题已修复或记录为技术债。
- 架构、安全、流程、运行时 contract 或运维行为变化已同步到 durable docs。

## Soft Gates

- 更广范围回归。
- 手动运行时检查。
- 依赖或安全扫描。
- 覆盖率报告。

跳过相关软门禁时，在最终说明或 active ExecPlan 中记录原因和残余风险。

## Definition Of Done

1. 请求行为已实现、修复，或明确记录为 out of scope。
2. 所有受影响区域的硬门禁通过。
3. 相关 spec、design doc、reference、AGENTS map 或 ExecPlan 已同步。
4. 新技术债已记录到 active plan 或 `docs/exec-plans/tech-debt-tracker.md`。
5. 最终交付列出 Passed、Not run、Residual risk；非平凡任务另加 Spec 自审、Standards 自审两行。
```

## CONTEXT.md

项目术语表，位于项目根目录（与 AGENTS.md 平级）。让用户和 AI 用同一套语言；spec 标题、任务名、测试名、代码命名都使用标准术语。

**生成条件**：阶段 1.5 澄清的项目特有术语 ≥ 3 个（采集方法见 `requirements-elicitation.md`）。不足时不生成，关键概念写入 AGENTS.md 核心信念。

**AGENTS.md 联动**：生成后在快速入口追加 `- 术语表：见 CONTEXT.md`；未生成不列出。

```markdown
# {项目名} 术语表

本文件定义项目关键概念的标准叫法。AI 生成的 spec、任务、测试和代码命名必须使用标准术语，不使用"避免"列中的别名。

## 语言

**{标准术语}**：
{一两句话定义：它是什么。}
_避免_：{别名 1}、{别名 2}
```

要点：定义写"它是什么"，一两句话为限；只收本项目特有概念（超时、缓存等通用词不入表）；同一概念多个叫法时选定一个，其余列入"避免"；术语必须来自真实澄清，不编造。

## docs/ARCHITECTURE.md

架构地图，回答"X 在哪？"和"这段代码做什么？"。**所有项目必须提供架构信息**：

- **多文件项目**：生成 `docs/ARCHITECTURE.md`，50-150 行，必须包含概述、代码地图（模块划分 + 关系）、架构不变量、层级边界、横切关注点、关键文件。
- **CLI/单文件项目**：不生成 `docs/`。架构概述 + 关键文件 + 2-3 条不变量写入 AGENTS.md"架构"章节（≤20 行）；演变为多文件项目后再创建。

规范：只写稳定内容，不写频繁变化的；不链接，用符号名。

## docs/DESIGN.md

设计规范。**生成条件**：项目有 UI 或 API 时。内容如 UI 组件规范、API 设计规范、代码风格。未生成时把 2-3 条关键设计约束写入 AGENTS.md 核心信念。

## docs/QUALITY_SCORE.md

按模块的质量评分追踪表，随里程碑更新。**生成条件**：项目超过 3 个模块。启动时不足 3 个模块不生成，也无需在 AGENTS.md 补充。

```
| 模块 | 可维护性 | 测试覆盖 | 文档完整度 | 综合 |
|------|---------|---------|-----------|------|
| src/ui | 🟢 | 🟡 | 🟢 | 🟢 |
| src/service | 🟢 | 🟢 | 🟡 | 🟢 |
```

## docs/SECURITY.md

安全规范。**生成条件**：项目涉及网络请求、数据存储或 API Key。内容如敏感数据存储方式、输入验证要求、依赖扫描频率。未生成时把关键安全约束（如"API Key 不得硬编码，使用环境变量"）写入 AGENTS.md 核心信念。

## docs/DEPLOYMENT.md

部署规范。**生成条件**：Web/API/需长期运行的服务端项目，且用户有云服务器部署需求。完整模板和引导规则见 `deployment-spec.md`；生成的文档必须自包含并填入项目实际信息。CLI 本地工具或无服务器项目不生成；后续需要时按模板补生成并同步 AGENTS.md 快速入口。

## docs/design-docs/core-beliefs.md

核心信念展开文档。**生成条件**：项目有 3 条以上核心信念需要展开时。未生成时核心信念直接写入 AGENTS.md（≤5 条）。

## 设计决策记录（ADR）

记录"为什么这么做"的轻量决策文档，存放 `docs/design-docs/`，文件名 `NNNN-<slug>.md`（从 `0001` 递增）。

**生成条件**：同时满足以下三条才记录，任何一条不满足都跳过：

1. **难以逆转** — 现在改主意代价可感知（数据库选型、是否上框架）；随手能改的不记。
2. **无上下文会困惑** — 未来读者（包括以后的 AI 代理）会问"当初为什么这么搞"。
3. **真实权衡** — 存在合理备选项，且因具体理由选定；顺理成章的不记。

与 ExecPlan Decision Log 的分工：只影响单个任务的决策写 ExecPlan；跨任务长期有效的才写 ADR，同一决策不写两处。

```markdown
# {决策的短标题}

{1-3 句话：什么背景下、决定了什么、为什么。}
```

仅在真正需要时追加可选章节：**备选项**（被否方案值得记住时）、**后果**（下游影响不明显时）。编号取现有最大号 +1；新增后同步 `docs/design-docs/index.md`；不批量预生成空 ADR。
