# 文档验证标准

这是文档验证的唯一 canonical 来源；`SKILL.md` 和其他流程文档只引用这里，不重复维护校验细则。

## 目录

- [验证时机](#验证时机)
- [验证清单](#验证清单)
- [严重程度分级](#严重程度分级)
- [简化版与完整版标准](#简化版与完整版标准)
- [验证命令](#验证命令)

---

## 验证时机

| 时机 | 检查范围 | 严重程度 |
|------|---------|---------|
| 约束机制落地后 | 核心文档（AGENTS.md + WORKFLOW.md + 架构信息 + 完成门禁 + scripts/validate_agents_docs.py；TASKS.md 可选） | ERROR |
| 每次对话结束前 | TASKS.md 进度一致性 | WARN |
| 项目恢复时 | 文档完整性 + 知识新鲜度 | ERROR + WARN |
| 提交前 | 全量检查 | INFO |

---

## 验证清单

### 核心文档验证（必须通过）

| 文件 | 检查项 | 说明 |
|------|--------|------|
| `AGENTS.md` | 存在 | 项目根目录必须有 |
| `AGENTS.md` | 章节完整 | 根级/子级分别按各自标准检查 |
| `AGENTS.md` | 行数范围 | 简化版≤150，完整版≤140 |
| `AGENTS.md` | 快速入口无死链 | 引用的文档都存在 |
| `WORKFLOW.md` | 存在或在 AGENTS.md 中有轻量流程替代 | 项目默认工作流 |
| `scripts/validate_agents_docs.py` | 存在 | 所有项目的核心验证脚本 |
| `TASKS.md` | 存在时检查标准区段（`进行中` / `待办` / `已完成`）和每条任务的 `✅` 验证条件 | 不存在不算错误，全部完成后可删除 |
| `tasks.md` | 旧命名兼容检查 | 存在时提示重命名为根目录 `TASKS.md` |
| `docs/ARCHITECTURE.md` | 存在（多文件项目必须；CLI/单文件项目替代方案：AGENTS.md 包含"架构"章节） | 描述项目架构 |
| `docs/ARCHITECTURE.md` | 内容完整性（概述/模块或代码地图/关键文件/架构约束信息） | 缺项记 WARN，不阻断下一阶段 |
| `docs/EXECUTION_GATES.md` | 多文件项目存在；CLI/单文件项目替代方案：AGENTS.md 包含完成门禁摘要 | 描述验证、风险和收尾标准 |
| 根 `AGENTS.md` | `约束机制` 章节存在 | 项目级元数据只在根级声明 |
| 根 `AGENTS.md` | `约束机制.模式` 合法 | 只能是 `agents-only` 或 `linter+agents` |
| 根 `AGENTS.md` | `约束机制.配置` 合法 | `agents-only` 时必须为 `N/A`；`linter+agents` 时必须为真实配置文件路径 |

> 子级/模块级 `AGENTS.md` 继承根级 `约束机制`，不要求重复声明；若为了可读性保留也允许，但不是校验必需项。

### 条件文档验证（存在时检查）

| 文件 | 检查项 | 说明 |
|------|--------|------|
| `docs/exec-plans/` | 子目录结构 | 按需生成，存在时检查 active/completed 子目录 |
| `docs/product-specs/` | 索引和 spec 结构 | 存在时检查 index.md 和单个 spec 的目标/非目标/验收标准 |
| `docs/DESIGN.md` | 章节结构 | 设计规范存在时检查 |
| `docs/QUALITY_SCORE.md` | 评分表格式 | 质量追踪存在时检查 |
| `docs/SECURITY.md` | 安全约束 | 安全文档存在时检查 |
| AGENTS.md 中声明的约束配置文件 | 文件存在性 | `模式=linter+agents` 时，`配置` 指向的文件必须存在 |

### 知识新鲜度验证

| 检查项 | 说明 | 严重程度 |
|--------|------|---------|
| 快速入口无死链 | AGENTS.md 中引用的文档都存在 | WARN |
| TASKS.md 进度一致 | 已完成的已勾选，新增的已记录 | WARN |
| ARCHITECTURE.md 模块表准确 | 反映当前代码结构 | WARN |

---

## 严重程度分级

| 级别 | 含义 | 处理方式 |
|------|------|---------|
| **ERROR** | 必须修复 | 不修复不能进入下一阶段 |
| **WARN** | 建议修复 | 记录但可继续，尽快修复 |
| **INFO** | 状态信息 | 纯信息，无需处理 |

### ERROR 类问题

- 核心文档不存在（AGENTS.md；WORKFLOW.md 且 AGENTS.md 无轻量流程替代；多文件项目缺少 docs/ARCHITECTURE.md 且 AGENTS.md 无"架构"章节；CLI/单文件项目 AGENTS.md 缺少"架构"章节；多文件项目缺少 docs/EXECUTION_GATES.md 且 AGENTS.md 无完成门禁摘要）
- 缺少 `scripts/validate_agents_docs.py`
- 必需章节缺失
- 根 AGENTS.md 缺少 `约束机制` 章节或 `模式`
- 根 AGENTS.md 的 `模式=agents-only` 但 `配置` 不是 `N/A`
- 根 AGENTS.md 的 `模式=linter+agents` 但缺少真实配置文件路径，或路径不存在
- TASKS.md 存在但无法识别任务状态
- TASKS.md 缺少标准区段（`进行中` / `待办` / `已完成`）
- TASKS.md 中存在缺少 `✅` 验证条件的任务

### WARN 类问题

- 存在旧命名 `tasks.md`，应重命名为根目录 `TASKS.md`
- 行数超限（可读性下降）
- 快速入口有死链
- ARCHITECTURE.md 缺少概述 / 模块或代码地图 / 关键文件 / 架构约束信息中的任一概念组

### INFO 类信息

- 文件行数统计
- TASKS.md 任务统计
- 版本识别结果

---

## 简化版与完整版标准

### 版本判断

| 判断条件 | 版本 |
|---------|------|
| 包含 `## Scope` 章节 | 完整版 |
| 不包含 `## Scope` | 简化版 |

### 简化版标准

**适用**：≤3模块、新手项目、单人开发

**根级 AGENTS.md 必需章节**：
- 快速入口
- 核心信念
- 开发流程
- 常用命令
- 架构（仅 CLI/单文件项目必需，替代 docs/ARCHITECTURE.md）
- 约束机制（仅根级 AGENTS.md 必需）

**行数限制**：≤150 行

### 完整版标准

**适用**：>3模块、多人协作、多AI工具

**根级 AGENTS.md 必需章节**：
- Scope
- Do
- Avoid
- 约束机制
- Commands
- Tests
- Related Skills

**行数限制**：≤140 行

### 根级与子级 AGENTS.md 规则

- 根级 `AGENTS.md` 必须声明项目级 `约束机制`
- 子级/模块级 `AGENTS.md` 继承根级 `约束机制`，不要求重复声明
- 子级/模块级 `AGENTS.md` 仍需满足其采用模板的其余章节完整性

---

## 验证命令

### 基本用法

```bash
python scripts/validate_agents_docs.py
```

### 按严重程度过滤

```bash
# 只显示 ERROR
python scripts/validate_agents_docs.py --level ERROR

# 显示 ERROR + WARN
python scripts/validate_agents_docs.py --level WARN

# 显示全部（默认）
python scripts/validate_agents_docs.py --level INFO
```

### 指定项目目录

```bash
python scripts/validate_agents_docs.py --project /path/to/project
```

说明：当脚本在项目本地运行时，如果 `scripts/validate_agents_docs.py` 本身已被删除，命令会先失败；从 skill 包或其他项目使用 `--project` 校验目标项目时，仍应检测并报告这一缺失。

### 输出示例

```
[INFO] AGENTS.md: 简化版, 45 行
[INFO] TASKS.md: 5 项待办, 3 项已完成
[INFO] docs/ARCHITECTURE.md: 32 行
[INFO] docs/exec-plans/: 目录不存在（按需生成，无需修复）
[WARN] AGENTS.md: 快速入口死链: docs/DESIGN.md

验证完成: 0 个错误, 1 个警告
```

---

## 验证流程嵌入

### 约束机制落地后验证

生成核心文档、按需扩展文档，并在根 `AGENTS.md` 写入有效 `约束机制` 后立即验证：

```
完成阶段 5 → 运行验证 → 有 ERROR 则修复 → 进入阶段 6
```

### 每次对话结束验证

更新 TASKS.md 后验证：

```
对话结束 → 更新 TASKS.md → 运行验证 --level WARN → 发现问题立即修复
```

### 项目恢复验证

恢复时先尝试验证文档状态；如果项目内 `scripts/validate_agents_docs.py` 缺失，改用本 skill 自带脚本加 `--project` 校验，或把缺失记录到恢复摘要中，不阻断恢复定位：

```
读取 AGENTS.md → 尝试运行验证 --level ERROR → 记录 ERROR/WARN/缺失脚本 → 输出恢复摘要并等待确认
```

---

## 总结

vibe-coding-launcher 的验证更注重**结构完整性**而非**内容逐字匹配**，因为项目内容会随用户需求变化。
