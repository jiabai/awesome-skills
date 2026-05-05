# Security

## Purpose

本文件定义项目的安全约束，确保自动化操作不会泄露用户敏感信息或触发风控机制。

## 敏感数据处理

- Cookie 数据通过 `scripts/xhs/cookies.py` 持久化存储在本地文件系统
- 发布内容通过文件传递（`--title-file`、`--content-file`），不内联到命令行参数
- 文件路径必须使用绝对路径，避免路径遍历风险
- 禁止在日志或 JSON 输出中打印 Cookie、Token 等敏感信息

## 操作安全

- 发布和评论操作必须经过用户确认后才能执行
- 控制操作频率，保持合理间隔，避免触发小红书风控机制
- 使用 `scripts/run_lock.py` 单实例锁，防止并发操作导致状态混乱
- `scripts/xhs/human.py` 模拟人类行为模式，降低自动化检测风险

## 浏览器安全

- Chrome 扩展仅在用户主动安装后启用
- 扩展通过 WebSocket 与本地 bridge server 通信，不连接外部服务器
- 所有操作发生在用户真实浏览器环境中，使用用户已登录的账号状态

## 依赖安全

- 运行时依赖最小化：`requests`、`websockets`、`python-socks`
- 开发依赖独立管理：`ruff`、`pytest`
- 定期检查依赖更新：`uv sync`

## 约束

- 禁止硬编码 API Key、密码或其他凭据
- 禁止将用户数据发送到第三方服务
- 禁止绕过用户确认机制执行发布类操作
