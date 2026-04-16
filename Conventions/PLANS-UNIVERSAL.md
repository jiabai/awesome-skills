# ExecPlan 通用模板

适用于 Codex 和 Claude Code 的执行规范模板。

---

## 文件定位

这是一个**元规范**文件，定义"如何编写 AI Agent 执行规范（ExecPlan）"。

用户基于此模板创建具体任务的执行规范文件（通常命名为 `PLANS.md` 或放入 `AGENTS.md` 引用）。

---

## 核心原则（不可协商）

违反以下原则会导致执行失败：

| 原则 | 说明 | 反面案例 |
|------|------|----------|
| **完全自包含** | 所有知识都在文档内，不依赖外部博客/文档，无记忆依赖 | "参考外部博客了解 X" |
| **活文档** | 随进度更新，每次修订保持自包含，从文档本身可重启执行 | 只在开始时写一次，后续不更新 |
| **新手友好** | 让不了解项目的人也能端到端实现，定义所有术语 | 假设读者了解架构，使用未定义术语 |
| **可演示验证** | 产出可验证的行为，不只是"代码改动" | "添加了某个 struct" |
| **目的先行** | 先说明用户能做什么新事情，再引导实现步骤 | 直接跳到技术细节 |

---

## 格式约束

| 约束项 | 规则 |
|--------|------|
| **代码块包裹** | 整个规范用单个 `md` 代码块包裹（写入独立 .md 文件时省略三引号） |
| **嵌套处理** | 用 4 空格缩进展示命令/diff，避免嵌套代码块导致提前闭合 |
| **正文风格** | 优先用句子而非列表，仅在 Progress 等特定章节用勾选列表 |
| **标题层级** | 使用 `#` 和 `##`，标题后空两行 |
| **文件引用** | 用完整相对路径（如 `src/modules/foo.rs`），不直接链接 |
| **术语定义** | 引入非普通英语术语时，立即定义并说明在 repo 中的体现位置 |

---

## 规范骨架模板

每个 ExecPlan 必须包含以下章节：

### 必需章节

```
# <简短、行动导向的描述>

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries,
Decision Log, and Outcomes & Retrospective must be kept up to date as work proceeds.

## Purpose / Big Picture

用几句话说明用户视角的价值：
- 完成后用户能做什么新事情？
- 如何看到它工作？

## Progress

用勾选列表追踪进度，每条标注时间戳：

- [x] (YYYY-MM-DD HH:MM) 已完成的步骤
- [ ] 待完成的步骤
- [ ] 部分完成（已完成: X; 剩余: Y）

## Surprises & Discoveries

记录意外行为、bug、性能权衡、反向逻辑等：

- Observation: 发现的内容
  Evidence: 简短证据（测试输出最佳）

## Decision Log

记录每个设计决策：

- Decision: 决策内容
  Rationale: 决策理由
  Date/Author: 日期和作者

## Outcomes & Retrospective

在里程碑或完成时总结：
- 实现了什么
- 遗留什么
- 学到什么

## Context and Orientation

假设读者不了解项目：
- 关键文件的完整路径
- 模块介绍
- 术语定义
- 各部分如何关联

## Plan of Work

用叙述描述编辑序列：
- 编辑哪个文件
- 在什么位置（函数、模块）
- 插入或修改什么

## Concrete Steps

具体命令：
- 工作目录
- 完整命令行
- 预期输出（简短 transcript）

## Validation and Acceptance

如何验证成功：
- 启动或运行系统的方式
- 可观察的行为（具体输入/输出）
- 测试命令和预期结果
- 新测试"修改前失败、修改后通过"的说明
```

### 推荐章节

```
## Idempotence and Recovery

- 步骤是否可安全重复
- 失败时的重试或回滚路径
- 完成后环境清理

## Artifacts and Notes

关键输出、diff、snippet（用缩进嵌入）

## Interfaces and Dependencies

明确指定：
- 使用的库、模块、服务及理由
- 必须存在的类型、接口、函数签名
```

---

## 活文档机制

| 机制 | 触发时机 | 格式 |
|------|----------|------|
| **进度追踪** | 每个停止点 | `- [x] (timestamp) 完成内容` |
| **决策记录** | 做出设计决策时 | `Decision + Rationale + Date` |
| **意外发现** | 发现意外行为时 | `Observation + Evidence` |
| **变更说明** | 规范修订时 | 在末尾添加变更描述和理由 |
| **重启能力** | 始终保持 | 确保从文档本身（无其他工作）能重启 |

---

## 里程碑设计

### 里程碑叙事结构

每个里程碑用叙事而非官僚：

```
里程碑 N: <简短描述>

范围: 解决什么问题
产出: 里程碑结束时新增的内容（之前不存在）
命令: 运行的命令
验收: 预期的可观察结果
```

### 里程碑原则

| 原则 | 说明 |
|------|------|
| **独立可验证** | 每个里程碑产出可独立演示的增量成果 |
| **原型里程碑** | 允许显式原型里程碑，验证库可行性、降低大改动风险 |
| **并行实现** | 迁移期间可保持新旧路径共存，确保测试持续通过 |
| **探索性 Spike** | 复杂依赖时可创建独立 spike，分别验证外部功能 |

---

## 验证标准

### 行为导向

验收用行为描述而非内部属性：

| 正确示例 | 错误示例 |
|----------|----------|
| 启动服务器后，访问 `http://localhost:8080/health` 返回 HTTP 200，body 为 "OK" | 添加了 HealthCheck struct |
| 运行 `pytest tests/auth_test.py`，预期 5 个测试通过 | 实现了认证逻辑 |

### 验收格式模板

```
Validation and Acceptance:

验证方式:
1. 启动服务: <命令>
2. 执行操作: <具体输入>
3. 预期输出: <具体输出或 HTTP 响应>

测试验证:
- 运行 <测试命令>
- 预期 <N> 个测试通过
- 新测试 <测试名>: 修改前失败，修改后通过
```

---

## 框架适配

### Codex

| 概念 | 实现 |
|------|------|
| 规范文件 | `PLANS.md`，通过 `AGENTS.md` 引用 |
| 加载方式 | 自动加载同名文件或通过术语触发（如 `ExecPlan`） |
| 工具集 | `list_files`, `read_file`, `search`, `run` |

### Claude Code

| 概念 | 实现 |
|------|------|
| 规范文件 | `.claude/PLANS.md` 或 `AGENTS.md` 或 skill 文件 |
| 加载方式 | 通过 `Skill` 工具加载，或写入 CLAUDE.md 引用 |
| 工具集 | 见下表映射 |

### 工具映射表

| Codex 工具 | Claude Code 工具 | 用途 |
|------------|------------------|------|
| `list_files` | `Glob` | 按模式匹配文件 |
| `read_file` | `Read` | 读取文件内容 |
| `search` | `Grep` | 搜索文件内容 |
| `run` | `Bash` | 执行命令 |
| `edit_file` | `Edit` | 编辑文件（精确替换） |
| `write_file` | `Write` | 创建或覆盖文件 |
| `ask_user` | `AskUserQuestion` | 向用户提问 |

### Claude Code 特有工具

| 工具 | 用途 |
|------|------|
| `Agent` | 启动子代理处理复杂任务 |
| `TaskCreate/TaskUpdate/TaskList` | 任务追踪（替代 Progress 章节） |
| `WebFetch/WebSearch` | 网络搜索 |
| `Skill` | 加载技能文件 |

---

## 使用流程

### Codex 流程

```
1. 在 AGENTS.md 定义触发词：
   "When writing complex features, use an ExecPlan (described in PLANS.md)"

2. 创建 PLANS.md 文件，按骨架模板填写

3. 触发任务时引用术语：
   "使用 ExecPlan 实现 <功能>"
```

### Claude Code 流程

```
1. 创建规范文件（如 docs/PLANS.md 或 skill 文件）

2. 在 CLAUDE.md 引用：
   "复杂任务请参考 docs/PLANS.md 的 ExecPlan 格式"

3. 或通过 Skill 工具加载：
   Skill(skill: "执行规范名")

4. 触发任务时：
   "按 ExecPlan 格式实现 <功能>"
```

---

## 一句话总结

> ExecPlan = 让无记忆的 AI 代理像有完整指令的新手工程师一样，从单文档独立完成复杂任务。
> 核心要求：自包含、活文档、新手引导、结果可验证。