# 任务管理标准

## 目录

- [tasks.md 与 ExecPlan 的分工](#tasksmd-与-execplan-的分工)
- [tasks.md 格式](#tasksmd-格式)
- [任务写入标准](#任务写入标准)
- [使用规则](#使用规则)

---

## tasks.md 与 ExecPlan 的分工

| 维度 | tasks.md | ExecPlan |
|------|----------|----------|
| 定位 | 轻量执行清单 | 功能级计划文档 |
| 粒度 | 单条任务（1-30 分钟） | 完整功能（数小时到数天） |
| 格式 | checkbox 列表 | 完整文档（Purpose/Progress/Steps/Validation） |
| 适合 | 修 bug、小改动、配置调整、依赖安装 | 新功能、架构调整、多步骤开发 |
| 存放位置 | 项目根目录 `tasks.md` | `docs/exec-plans/active/` |
| 生命周期 | 持续维护，完成的任务勾选即可 | 完成后移入 `docs/exec-plans/completed/` |

## tasks.md 格式

```markdown
# Tasks

## 进行中
- [ ] 安装 flask 依赖 ✅ `pip install flask && python -c "import flask; print(flask.__version__)"`
- [ ] 添加 /health 端点 ✅ `curl localhost:5000/health` 返回 200

## 待办
- [ ] 配置 .gitignore ✅ `cat .gitignore` 包含 __pycache__、.env、node_modules
- [ ] 添加环境变量支持 ✅ `python -c "from config import SETTINGS; print(SETTINGS)"` 不报错

## 已完成
- [x] 初始化项目结构（2026-04-17）✅ `ls AGENTS.md tasks.md docs/` 文件均存在
- [x] 创建 AGENTS.md（2026-04-17）✅ `wc -l AGENTS.md` 输出 ≤ 150
```

## 任务写入标准

每条任务**必须**包含完成验证条件，格式为：

```
- [ ] 任务描述 ✅ 验证命令或验证标准
```

验证条件的三种写法：

| 类型 | 格式 | 示例 |
|------|------|------|
| 命令验证 | `✅ \`具体命令\` 预期输出` | `✅ \`pip install flask\` 无报错` |
| 文件验证 | `✅ \`cat/ls 文件\` 包含/存在` | `✅ \`cat .gitignore\` 包含 node_modules` |
| 行为验证 | `✅ 可观察的运行时行为` | `✅ 浏览器打开 /health 返回 200` |

禁止写入的任务：

- 无验证条件的模糊任务，如"优化性能"、"改进代码" — 必须拆解为可验证的具体任务
- 无法在 30 分钟内完成的任务 — 拆小或升级为 ExecPlan
- 依赖未完成任务的后续任务 — 只写当前可执行的，后续任务放"待办"

勾选标准：

只有当 `✅` 后的验证条件**实际通过**时，才能将 `- [ ]` 改为 `- [x]`。不要凭感觉勾选，必须运行验证命令或确认验证行为。

## 使用规则

- **小任务 → tasks.md**：能在 30 分钟内完成的事，直接写入 tasks.md，无需创建 ExecPlan
- **大功能 → ExecPlan + tasks.md**：创建 ExecPlan 规划整体方案，同时将 ExecPlan 中的拆解步骤同步到 tasks.md 作为执行追踪
- **日常维护**：每次对话开始时，先读取 tasks.md 了解当前进度；对话结束时，更新 tasks.md 记录新增和完成的任务
- **不要重复记录**：同一个任务不要同时在 tasks.md 和 ExecPlan Progress 中维护。tasks.md 是执行入口，ExecPlan Progress 是计划文档中的进度快照
