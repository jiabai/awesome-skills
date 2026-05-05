# Vibe Coding Launcher

> 项目脚手架工具 —— 搭好 AI 友好的开发框架，然后退场。

---

## 这个技能解决什么问题

当你想用 AI 辅助开发一个项目时，最大的摩擦往往不是写代码，而是：

- AI 不了解你的项目结构和约定
- 每次对话都要重新解释技术栈和架构
- AI 随意跳过步骤、忘记验证、不更新文档
- 项目大了之后，AI 的上下文混乱，输出质量下降

Vibe Coding Launcher 帮你**一次性解决这些问题**——它为你的项目建立一套 AI 友好的治理体系，让后续的 AI 协作有章可循。

---

## 它能做什么

### 1. 新项目启动

从零开始，按阶段帮你搭建：

- **项目骨架**：目录结构、配置文件、初始代码
- **治理文档**：`AGENTS.md` + `docs/` 体系，让 AI 知道你的约定
- **架构约束**：技术栈选择、代码边界、安全基线
- **首个计划**：把大目标拆成可执行的 Spec 和 ExecPlan

### 2. 旧项目恢复

中断一段时间后，帮你快速恢复上下文：

- 读取 `AGENTS.md` 了解项目现状
- 读取 `TASKS.md` 找到上次断点
- Inspect 代码确认当前状态
- 从断点继续，不重复已完成的工作

---

## 使用时机

| 场景 | 是否使用 |
|------|---------|
| 从零开始一个新项目 | ✅ **使用** |
| 项目已存在，需要恢复上下文继续开发 | ✅ **使用** |
| 项目骨架已搭好，进入日常迭代开发 | ❌ **不再使用** |
| 修复 bug、添加小功能、重构代码 | ❌ **不再使用** |

### 退场信号

当项目完成以下阶段，这个技能就完成了使命：

- `AGENTS.md` 已生成并稳定
- `docs/` 目录结构已建立
- 工作流治理规则已落地
- 首个 Spec / ExecPlan 已创建

之后，日常开发应该依赖**项目内部已沉淀的治理文档**，而不是重新加载这个技能。

---

## 日常开发怎么做

项目进入迭代期后，AI agent 会自动按以下流程工作：

```
读取 AGENTS.md → Inspect 代码 → 判断任务类型 → 执行 → 验证 → 同步文档
```

**轻量任务**（修 typo、调样式、单函数改动）：
直接实现 → 跑相关测试 → 完成。

**非平凡任务**（新功能、跨模块、改架构）：
写 Spec → 写 ExecPlan → 拆任务 → 逐步实现 → 完成门禁 → 归档计划。

详细流程见 [`references/ai-coding-workflow.md`](references/ai-coding-workflow.md) 和 [`references/workflow-governance.md`](references/workflow-governance.md)。

---

## 核心原则

**Humans steer. Agents execute.**

- 人类决定方向和目标
- AI 负责执行和细节
- 每个关键阶段都等人类确认后再推进
- 不跳过验证，不合并计划和执行

---

## 技能文件结构

```
vibe-coding-launcher/
├── SKILL.md                          # 技能入口（AI agent 读取）
├── README.md                         # 本文件（用户指南）
├── references/
│   ├── ai-coding-workflow.md         # 日常开发执行流程
│   ├── architecture-constraints.md   # 架构约束配置
│   ├── document-templates.md         # 文档模板
│   ├── execplan-format.md            # ExecPlan 格式
│   ├── phase-guidance.md             # 阶段互动细则
│   ├── project-structure.md          # 项目结构推荐
│   ├── task-management.md            # 任务管理规范
│   ├── tech-stack-recommendations.md # 技术栈推荐
│   ├── validation-standards.md       # 验证标准
│   └── workflow-governance.md        # 工作流治理与完成门禁
├── scripts/
│   └── validate_agents_docs.py       # 文档结构验证脚本
└── evals/
    └── evals.json                    # 评估用例
```

---

## 关键概念速查

| 概念 | 一句话说明 |
|------|-----------|
| `AGENTS.md` | 项目入口地图，AI 默认读取的上下文入口 |
| `docs/` | 详细规则存放处，避免 `AGENTS.md` 膨胀 |
| Spec | 产品规格文档，回答"做什么、不做什么、验收标准" |
| ExecPlan | 实施计划，回答"怎么做、按什么顺序、怎么验证" |
| 完成门禁 | 代码已 inspect、验证已通过、文档已同步 |
| 轻量路径 | 低风险、小范围、无新边界时的快速执行通道 |

---

## 一句话总结

> Vibe Coding Launcher 是**脚手架**，不是**日常工具**。搭完架子就退场，日常开发靠项目内部的 `AGENTS.md` 和 `docs/` 体系。
