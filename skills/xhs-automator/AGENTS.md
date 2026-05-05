# xhs-automator AI Collaboration Rules

## 快速入口

- 架构：见 `docs/ARCHITECTURE.md`
- 工作流：见 `WORKFLOW.md`
- 完成门禁：见 `docs/EXECUTION_GATES.md`
- 安全规范：见 `docs/SECURITY.md`
- 执行清单：见 `TASKS.md`（全部完成后删除）

## 核心信念

- 所有小红书操作只能通过 `python scripts/cli.py` 完成，不得使用外部工具
- 发布和评论操作必须经过用户确认后才能执行
- 文件路径必须使用绝对路径
- 敏感内容通过文件传递，不内联到命令行参数
- 控制操作频率，避免触发风控机制

## 开发流程

1. 从 AGENTS.md 读取项目规则和架构约束
2. 非平凡任务先创建 spec（`docs/product-specs/`）和 ExecPlan（`docs/exec-plans/active/`）
3. 轻量任务可直接实现，但需 inspect、最小验证和文档同步
4. 完成后运行验证：`python scripts/validate_agents_docs.py --level ERROR`

## 架构

概述：小红书自动化技能集合，通过 Chrome 扩展和 CDP 协议操作用户真实浏览器
关键文件：`scripts/cli.py`（CLI 入口）、`scripts/xhs/`（核心自动化包）、`extension/`（Chrome 扩展）
架构不变量：
- 双层结构：`scripts/` 是 Python 自动化引擎，`skills/` 是 Claude Code Skills 定义
- CLI 是唯一执行入口，JSON 结构化输出
- 通过 bridge server 连接 CLI 与浏览器扩展

## 约束机制

- 模式：`linter+agents`
- 配置：`pyproject.toml`

## 常用命令

- `uv sync` — 安装依赖
- `uv run ruff check .` — Lint 检查
- `uv run ruff format .` — 代码格式化
- `uv run pytest` — 运行测试
- `python scripts/cli.py check-login` — 检查登录状态
- `python scripts/cli.py search-feeds --keyword "关键词"` — 搜索笔记
