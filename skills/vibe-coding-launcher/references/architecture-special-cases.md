# 特殊架构约束详解

本文件展开桌面应用、TUI 应用、Rust workspace、跨代码库协同和编译型构建系统的详细约束与典型场景；通用分层、模块设计基线和约束决策流程见 `architecture-constraints.md`。项目涉及以下特殊架构时才读本文件。

## 桌面应用

分层：UI(前端SPA) → IPC(桥接层) → Native(原生层) → Worker(子进程/外部服务) → Config → Types。

- **UI**：通常是 React/Vue SPA（WebView 内嵌，无 SSR 需求）。
- **IPC**：前端与原生层的协议边界（Tauri commands / Electron IPC），必须通过类型化契约（JSON Schema / TypeScript 接口）定义。
- **Native**：用 Rust/Tauri 处理文件系统、进程管理、系统 API。
- **Worker**：可选的子进程/外部服务（如 Python AI Worker），通过 stdio/HTTP 与原生层通信。

## TUI 应用

分层：EventLoop → View(渲染) → State(状态) → Command(命令) → Service → Config → Types。

- **EventLoop**：主循环，驱动事件分发和渲染调度。
- **View**：终端渲染（布局、ANSI 输出、滚动区域），通常用 ratatui 的 `Widget`/`Layout` trait；禁止直接修改状态。
- **State**：维护应用状态树（会话、缓冲区、光标位置等），变更必须通过 Command 层提交。
- **Command**：事件处理器，将按键/鼠标事件翻译为状态变更或服务调用。
- 性能约束：单次渲染帧 < 16ms（60fps）；终端兼容性覆盖 xterm/kitty/warp。

## Rust workspace（跨 crate）

分层：Interface → Core → Service → Infra → Config → Types（外层 crate 只能依赖内层 crate 的公共 API）。

以 Codex 项目为例：

- **Interface** crate（如 `codex-cli`、`codex-tui`）是入口点，只依赖 Core 的公共 API。
- **Core** crate（如 `codex-core`）是业务核心，不得依赖任何 Interface 层 crate。
- **Service** crate（如 `codex-exec`、`codex-skills`）提供独立服务，可依赖 Core 但不得互相依赖。
- **Infra** crate（如 `codex-config`、`codex-protocol`、`codex-secrets`）是底层基础设施，可被所有上层 crate 依赖。

关键约束：Core crate 不得"膨胀"——新功能应创建新 crate 而非加入 Core（参见 AGENTS.md 的 "resist adding code to codex-core" 原则）。

## 跨代码库协同约束

当项目由多个独立代码库协同组成时（如桌面应用 = 前端 SPA + 原生层 + Worker + 服务端）：

| 约束项 | 说明 | 强制方式 |
|-------|------|---------|
| **IPC 契约先行** | 跨进程/跨语言通信必须通过类型化契约（JSON Schema / `.d.ts` 接口 / Protobuf）定义，契约变更需版本号 | 声明式（AGENTS.md 核心信念）+ 契约文件走独立 review |
| **单向依赖** | 前端只依赖 IPC 契约，不直接 import 原生层或 Worker 代码；Worker 只依赖契约，不反向依赖 UI | linter 禁止跨代码库 import（`no-restricted-imports`）+ 声明式约束 |
| **协议可回放** | 所有 IPC 消息必须可序列化/反序列化，禁止传递闭包、Generator、不可序列化对象 | 声明式约束 + 集成测试验证序列化/反序列化 |
| **跨代码库边界** | 明确每个代码库的职责边界（如 `app/` 负责 UI，`app/src-tauri/` 负责原生，`worker/` 负责 AI 处理，`server/` 负责账号/额度），禁止跨边界 import | 声明式约束 + 代码审查门禁 |
| **契约同步** | 契约变更时，所有消费方必须同步更新，CI 中需有契约一致性检查 | CI 脚本 + 集成测试 |

典型场景：Tauri 应用的前端（TS）通过 `invoke('command_name', payload)` 调用 Rust 原生层命令，命令的输入输出类型定义在共享的 `.d.ts` 文件或 `contracts/` JSON 文件中，前后端各自实现但共享类型契约。

## 编译型构建系统约束

使用 Bazel、Cargo workspace、Gradle 等编译型构建系统的项目：

| 约束项 | 说明 | 强制方式 |
|-------|------|---------|
| **构建系统主从关系** | 明确主构建系统（如 Bazel 为生产构建，Cargo 为开发调试），主系统的 BUILD 文件必须与源文件同步 | 声明式约束（AGENTS.md 核心信念）+ CI 检查主系统构建是否通过 |
| **依赖声明一致性** | 同一依赖在主从构建系统中版本必须一致（如 Bazel MODULE.bazel.lock 与 Cargo.lock 同步） | CI 脚本（`bazel-lock-update`）+ lockfile 差异检测 |
| **跨 crate 可见性** | Rust `pub mod` 控制 crate 间可见性；禁止 `pub use` 内部实现细节作为公共 API | `clippy::restricted_public_levels` + 代码审查 |
| **Core crate 膨胀防治** | 禁止向 Core crate 添加非核心功能，新功能必须创建独立 crate | 声明式约束 + PR review 门禁 |
| **编译检查前置** | 任何 Rust 代码变更必须先通过 `cargo check`（或 `bazel build` 对应 target） | CI 强制 + `pre-commit` hook |
| **BUILD 文件同步** | 新增源文件/依赖时，必须同步更新 Bazel BUILD 文件（compile_data/build_script_data/test 目标） | 声明式约束 + CI 检查 Bazel 构建 |
| **Feature flag 约束** | `Cargo.toml` 的 `[features]` 必须文档化，禁止隐式 feature 激活 | 声明式约束 + `cargo tree --features` 检查 |

典型场景：Codex 项目用 Bazel 作为主构建系统（生产/CI），Cargo 作为开发调试工具。开发者修改 Rust 代码后运行 `cargo check` 快速验证，提交前运行 `just fix`（含 `rustfmt` + `clippy`）和 `just test` 验证。CI 中运行 `bazel test` 全量测试确保 BUILD 文件与源码同步。

## 多代码库配置示例

项目包含多个代码库（如 `app/` + `worker/` + `server/`）时，根级 `约束机制.配置` 列出各代码库主 linter：

```markdown
- 模式：`linter+agents`
- 配置：`eslint.config.js`（前端）, `ruff.toml`（Worker）, `rustfmt.toml`（Rust 原生层）
```

Rust workspace（如 Codex 项目）：

```markdown
- 模式：`linter+agents`
- 配置：`rustfmt.toml`（全 workspace）, `clippy.toml`（全 workspace）, `deny.toml`（依赖审计）
```

## 特殊架构扩展验证

在 `architecture-constraints.md` 通用验证能力之外，特殊架构追加：

| 验证类型 | 适用项目 | 验证方式 | 示例 |
|---------|---------|---------|------|
| **TUI 渲染验证** | TUI 应用 | 终端渲染快照对比 | 启动应用 → 截取 ANSI 输出快照 → 与预期快照 diff 无差异 |
| **桌面构建验证** | 桌面应用 | 完整打包 + 安装包测试 | `npm run tauri build` 成功产出安装包，安装后可正常启动 |
| **进程生命周期验证** | 桌面应用（含子进程 Worker） | 启动/停止/崩溃恢复测试 | 启动 Worker → 正常运行 → 强制杀进程 → 验证 Watchdog 恢复 |
| **IPC 契约验证** | 跨代码库项目 | 端到端序列化/反序列化测试 | 发送完整 IPC 消息 → 验证原生层正确接收并返回 → 前端正确解析 |
| **平台签名验证** | 需要分发的桌面应用 | 平台签名/公证检查 | macOS: `codesign --verify` + `spctl --assess`；Windows: signtool verify |
