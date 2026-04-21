# 任务管理标准

本文件只管 `tasks.md` 如何记录和推进；提交节奏、验证深度和执行流程分别见 `ai-coding-workflow.md` 与 `validation-standards.md`。

## 目录

- [tasks.md 与 ExecPlan 的分工](#tasksmd-与-execplan-的分工)
- [tasks.md 格式](#tasksmd-格式)
- [任务写入标准](#任务写入标准)
- [使用规则](#使用规则)
- [知识新鲜度维护](#知识新鲜度维护)
- [原子提交原则](#原子提交原则)
- [渐进验证策略](#渐进验证策略)

---

## tasks.md 与 ExecPlan 的分工

| 维度 | tasks.md | ExecPlan Progress |
|------|----------|----------|
| 定位 | 轻量执行清单 | 功能级计划文档 |
| 粒度 | 执行级任务（1-30 分钟，如"安装 flask"） | 计划级里程碑（30 分钟到数小时，如"API 框架就绪"） |
| 格式 | checkbox 列表 | 完整文档（Purpose/Progress/Steps/Validation） |
| 适合 | 修 bug、小改动、配置调整、依赖安装 | 新功能、架构调整、多步骤开发 |
| 存放位置 | 项目根目录 `tasks.md` | `docs/exec-plans/active/` |
| 生命周期 | 全部完成后删除，历史由 ExecPlan 归档 | 完成后移入 `docs/exec-plans/completed/` |
| 更新时机 | 每完成一项任务立即勾选 | 当一批 tasks.md 任务对应同一里程碑全部完成时，标记该里程碑 |

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

- 小任务直接写入 `tasks.md`；大功能用 `ExecPlan + tasks.md`，里程碑留在 ExecPlan Progress。
- 每次对话开始读取 `tasks.md`，结束时更新它；全部完成后删除，历史由 ExecPlan 归档。
- `tasks.md` 记录执行级任务，ExecPlan Progress 记录计划级里程碑，不要重复写同一粒度的内容。

### 执行流程

1. 按 tasks.md 清单逐项执行
2. 完成一项 → 勾选该项 → 立即原子提交
3. 原子提交：`git add -A && git commit -m "完成：{任务描述}"`
4. 重复直到所有任务完成
5. 全部完成 → 删除 tasks.md → 最终提交

## 知识新鲜度维护

- 过时文档比没有文档更危险。
- 对话结束前检查 `tasks.md` 进度、`AGENTS.md` 快速入口和 `docs/ARCHITECTURE.md`（或 AGENTS.md 架构章节）。
- 新模块或接口变化时，优先回写相关文档；更完整的验证规则见 `validation-standards.md`。

---

## 原子提交原则

每完成一项 tasks.md 任务就更新勾选并立即提交；多项相关任务可合并，但不要把未完成的内容一起提交。

提交前确认三件事：

1. `tasks.md` 已更新
2. 验证命令已通过
3. `AGENTS.md` 不需要同步修改

---

## 渐进验证策略

验证顺序保持最小 → 扩大 → 全量；具体怎么选见 `ai-coding-workflow.md`。

- 单模块代码先跑该模块测试
- 跨模块接口先跑两模块测试，再扩大到集成测试
- 共享 DTO/类型先做所有消费者类型检查，再跑全量测试
