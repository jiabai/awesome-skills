# 项目结构标准

## 目录

- [核心集](#核心集所有项目必须生成)
- [扩展集](#扩展集按需生成)
- [扩展集生成判定](#扩展集生成判定)
- [按项目类型调整](#按项目类型调整)

---

## 核心集（所有项目必须生成，阶段 3 完成）

```
project-name/
├── AGENTS.md                  # 代理入口地图（~150行，目录/地图，不写百科全书）
├── WORKFLOW.md                # 项目默认工作流（非平凡任务的门禁流程）
├── TASKS.md                   # 执行清单（轻量任务追踪）
├── README.md                  # 项目说明
├── scripts/
│   └── validate_agents_docs.py  # 文档验证脚本（从本 skill 的 scripts/ 原样写入）
└── docs/
    ├── ARCHITECTURE.md        # 架构地图（CLI/单文件项目不生成 docs/，架构信息写入 AGENTS.md）
    └── EXECUTION_GATES.md     # 完成门禁（验证、风险、收尾标准）
```

> **CLI/单文件项目例外**：命令行/单文件项目的核心集只生成 AGENTS.md + WORKFLOW.md + TASKS.md + README.md + scripts/validate_agents_docs.py，不生成 docs/ 目录。架构信息（概述 + 关键文件 + 2-3 条不变量）和完成门禁摘要写入 AGENTS.md。

## 扩展集（按需生成，阶段 4 完成）

```
project-name/
├── docs/
│   ├── DESIGN.md              # 设计规范
│   ├── QUALITY_SCORE.md       # 质量评分追踪
│   ├── SECURITY.md            # 安全规范
│   ├── design-docs/
│   │   ├── index.md           # 设计文档索引
│   │   ├── core-beliefs.md    # 核心信念和原则
│   │   └── *.md              # 其他设计文档
│   ├── exec-plans/
│   │   ├── active/            # 正在执行的计划
│   │   ├── completed/         # 已完成的计划
│   │   └── tech-debt-tracker.md  # 技术债追踪
│   ├── product-specs/
│   │   ├── index.md           # 产品规格索引
│   │   └── *.md              # 各功能规格
│   ├── references/
│   │   ├── *.txt             # 技术参考（LLM友好格式）
│   │   └── *.md              # API文档等
│   └── generated/
│       └── db-schema.md      # 自动生成的文档
├── src/                       # 源代码
└── .gitignore
```

## 扩展集生成判定

| 文件/目录 | 生成条件 | 不生成时的替代方案 |
|-----------|---------|-----------------|
| `WORKFLOW.md` | 所有项目默认生成；极小一次性脚本可并入 AGENTS.md | AGENTS.md 写明轻量流程 |
| `docs/EXECUTION_GATES.md` | 多文件项目或需要测试/发布/交付标准 | AGENTS.md 写明最小验证和收尾格式 |
| `docs/DESIGN.md` | 项目有 UI 或 API | 设计规范写入 AGENTS.md 核心信念 |
| `docs/QUALITY_SCORE.md` | 项目超过 3 个模块 | 不生成，待模块增长后再创建 |
| `docs/SECURITY.md` | 项目涉及网络请求、数据存储或 API Key | 安全约束写入 AGENTS.md 核心信念 |
| `docs/design-docs/` | 项目有 3 条以上核心信念需要展开 | 核心信念直接写入 AGENTS.md |
| `docs/exec-plans/` | 项目需要多步骤开发计划（见 task-management.md） | 小任务用根目录 TASKS.md 追踪，无需建此目录 |
| `docs/product-specs/` | 项目有多个功能需要规格描述 | 不生成，待功能明确后再创建 |
| `docs/references/` | 项目依赖外部 API 或复杂技术 | 不生成，待需要时再创建 |
| `docs/generated/` | 项目使用数据库 | 不生成 |
| `src/` | 非单文件项目 | 单文件项目直接放根目录 |

判断原则：宁少勿多。项目启动时只生成核心集 + 满足条件的扩展集。不要一次性生成空文档——空文档比没有文档更危险。

经验规则：`AGENTS.md` 只做快速入口地图；流程细节放 `WORKFLOW.md`，收尾标准放 `docs/EXECUTION_GATES.md`，功能意图放 `docs/product-specs/`，实施过程放 `docs/exec-plans/`。不要把这些内容混进一个超长 `AGENTS.md`。

## 按项目类型调整

- **Web应用**：添加 `templates/`、`static/`，src 下按 `ui/` `service/` `repo/` 分层
- **API服务**：src 下按 `routes/` `models/` `services/` 分层
- **命令行**：单文件即可，核心集只生成 AGENTS.md + WORKFLOW.md + TASKS.md + README.md + scripts/validate_agents_docs.py，不生成 docs/ 目录
- **AI应用**：添加 `config.py`（API Key），docs/references/ 放 API 文档
