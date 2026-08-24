# 架构约束标准

## 分层架构

根据项目类型设定分层：

| 项目类型 | 分层 |
|---------|------|
| Web应用 | UI → Runtime → Service → Repo → Config → Types |
| API服务 | Routes → Service → Repo → Config → Types |
| 命令行 | CLI → Service → Config → Types |
| 命令行（TUI 应用） | EventLoop → View(渲染) → State(状态) → Command(命令) → Service → Config → Types |
| AI应用 | Interface → Agent → Service → Config → Types |
| 单文件/脚本 | 无需分层，在 AGENTS.md 核心信念中声明："保持单文件直到超过 200 行" |
| 桌面应用 | UI(前端SPA) → IPC(桥接层) → Native(原生层) → Worker(子进程/外部服务) → Config → Types |
| Rust 系统级项目（workspace 跨 crate） | Interface → Core → Service → Infra → Config → Types |

依赖方向只能"向前"（向下），跨层依赖 → 机械禁止。

表中为概念分层，未必逐一对应目录（如 Web 应用的 Runtime 指运行时编排层，简单项目可并入 Service，无需单独建 `runtime/`，参见 `project-structure.md`）。

特殊架构要点：

- **桌面应用**：UI 是 WebView 内嵌 SPA（无 SSR）；IPC 是前后端协议边界（Tauri commands / Electron IPC），必须通过类型化契约（JSON Schema / TS 接口）定义；Native 处理文件系统、进程、系统 API；Worker 是可选子进程，经 stdio/HTTP 与原生层通信。
- **TUI 应用**：EventLoop 驱动事件分发与渲染调度；View 只渲染（布局、ANSI 输出），禁止直接修改 State；State 维护状态树；Command 将事件翻译为状态变更或服务调用。性能约束：单帧 < 16ms。
- **Rust workspace**：Interface crate 是入口点，只依赖 Core 公共 API；Core 不得依赖任何 Interface crate；Service 可依赖 Core 但不得互相依赖；Infra 可被所有上层依赖。Core 不膨胀——新功能创建新 crate 而非加入 Core。

各特殊架构的层职责展开、典型场景和扩展验证见 `architecture-special-cases.md`。

## 模块设计基线

划分模块边界、编写 `docs/ARCHITECTURE.md` 和审查模块形状时的判据：

- **接口小，实现深**：让调用者学的少、能做的多。设计接口先问：方法能更少吗？参数能更简单吗？还能藏更多复杂度吗？
- **删除测试**：想象删掉这个模块——复杂度直接消失说明它只是转发层，删；复杂度扩散到调用点说明它承担真实工作，留。
- **接受依赖，不自己创建**：协作对象从参数传入，不在内部 `new` 数据库连接/外部客户端——这是可测试性的来源。
- **返回结果，不做隐蔽副作用**：计算型函数返回新值，不就地修改传入对象。

适用于函数、类、文件、目录任何粒度。符合"接口小实现深"的关键模块可作为架构不变量写入 `docs/ARCHITECTURE.md` 或 AGENTS.md 架构章节。

## 约束写入方式

### 决策流程

1. 简单项目（≤3 模块、单人）→ 根级 AGENTS.md 声明 `模式=agents-only`，配置=`N/A`，所有约束直接写 AGENTS.md。
2. 复杂项目（>3 模块或多层架构）→ 声明 `模式=linter+agents`，查下方映射表选择真实配置文件并写回 AGENTS.md。
3. 需要层间依赖方向强制时，启用进阶配置文件；不可被 linter 强制的约束，始终写根级 AGENTS.md 核心信念。
4. 约束是新增或变更时，同步摘要到根级 AGENTS.md 核心信念。

关键原则：

- **错误信息就是代理可读的指导**：linter 报错比 AGENTS.md 声明更有效，因为它是机械强制。
- **回写原则**：AGENTS.md 是默认读取入口和关键约束摘要，所有项目级约束源（linter 配置、子文档）的核心摘要必须回写根级；回写时机见 `ai-coding-workflow.md`。
- **模式优先**：脚本以根级 AGENTS.md 的显式声明为准，不根据目录结构推断复杂度。

### 硬约束配置文件映射表

按语言生态（而非框架）分组，与 `tech-stack-recommendations.md` 对齐：

| 语言生态 | 默认配置文件 | 进阶配置文件 | 可强制约束 | 声明式约束（写根级 AGENTS.md） |
|---------|------------|------------|-----------|----------------------|
| **Python** | `ruff.toml`（或 `pyproject.toml` `[tool.ruff]`） | `pyproject.toml` `[tool.importlinter]`（层间依赖方向） | 代码风格、import 排序、未使用导入、行长度 | 层间依赖方向（未配 import-linter 时）、架构不变量 |
| **JS / TS** | `eslint.config.js`（flat config） | 同文件 + `eslint-plugin-import` | 代码风格、import 限制、no-restricted-imports、层间依赖方向 | 设计原则、技术选型约束 |
| **Vue / Svelte** | `eslint.config.js`（含对应插件） | 同 JS/TS 进阶 | 同 JS/TS + 框架特定规则 | 同 JS/TS |
| **Dart** | `analysis_options.yaml` | — | lint 规则、类型检查严格度 | 架构不变量、层间依赖方向 |
| **Rust** | `rustfmt.toml` + `clippy.toml` | `cargo audit`（安全审计）等 | 代码风格、lint 规则、类型安全、`cargo check` 编译检查 | 架构不变量、FFI 边界、内存安全约定、IPC 契约、workspace 跨 crate 依赖方向 |

语言特殊说明：

- **Python**：Ruff 不支持 import 路径限制；需强制层间依赖方向要额外配 `import-linter`，否则只能作声明式约束。
- **Rust**：cargo 无内建层间依赖方向工具，靠 `pub mod` 可见性控制 + 代码审查 + 声明式约束实现；workspace 跨 crate 方向见上文特殊架构要点。
- **多代码库项目**（如 `app/` + `worker/` + `server/`）：`约束机制.配置` 列出各代码库主 linter，如 `` `eslint.config.js`（前端）, `ruff.toml`（Worker）, `rustfmt.toml`（Rust 原生层） ``。

### 跨代码库与编译型构建系统约束

多代码库协同（桌面应用 = 前端 SPA + 原生层 + Worker + 服务端）和编译型构建系统（Bazel、Cargo workspace、Gradle）有附加约束，完整约束表（含强制方式）和典型场景见 `architecture-special-cases.md`。核心要点：

- **IPC 契约先行**：跨进程/跨语言通信必须经类型化契约（JSON Schema / `.d.ts` / Protobuf）定义，契约变更需版本号且所有消费方同步更新，CI 有契约一致性检查。
- **单向依赖**：前端只依赖 IPC 契约，不直接 import 原生层或 Worker 代码（`no-restricted-imports` + 声明式约束）。
- **协议可回放**：IPC 消息必须可序列化/反序列化，禁止传闭包、Generator 等不可序列化对象。
- **职责边界**：明确每个代码库边界（`app/` 管 UI、`app/src-tauri/` 管原生、`worker/` 管 AI、`server/` 管账号），禁止跨边界 import。
- **构建系统主从一致**：主构建系统（如 Bazel 生产 / Cargo 调试）的 BUILD 文件与源文件同步，同一依赖在主从系统版本一致（lockfile 差异检测）。
- **Core crate 膨胀防治**：禁止向 Core crate 添加非核心功能，新功能创建独立 crate（声明式约束 + PR review）。
- **编译检查前置**：Rust 变更先过 `cargo check`（或对应 Bazel target），CI 强制。
- **Feature flag 文档化**：`Cargo.toml` 的 `[features]` 禁止隐式激活。

### 可强制 vs 声明式约束

| 约束类型 | 判断标准 | 写入位置 | 示例 |
|---------|---------|---------|------|
| **可强制约束** | linter 规则能直接检测并报错 | linter 配置文件 | `no-console`、`unused-imports` |
| **声明式约束** | 需要人类判断，linter 无法机械检测 | 根级 AGENTS.md 核心信念 | "数据层不依赖展示层" |

### 约束机制声明

在根级 AGENTS.md 中固定保留机器可读章节：

```markdown
## 约束机制

- 模式：`agents-only` 或 `linter+agents`
- 配置：`N/A` 或真实配置文件路径
```

规则：`agents-only` 配置必须写 `N/A`；`linter+agents` 必须写真实路径；CLI/单文件和简单多文件项目默认 `agents-only`；复杂项目和多代码库协同项目用 `linter+agents`。作用：代理无需猜测约束如何落地；验证脚本直接读取根级模式决定是否要求真实配置文件。

## 黄金原则

写入 AGENTS.md 核心信念的架构准则：

| 原则 | 理由 |
|------|------|
| 共享工具包优于手写 helper | 不变量集中，避免重复 |
| 边界验证优于 YOLO 猜测 | 代理不能猜测数据形状 |
| "无聊"技术优于新奇技术 | 训练集覆盖、API 稳定 |
| 自实现优于 opaque 库 | 代理能理解、修改、测试 |
| 本地优先优于云端 | 桌面应用默认本地处理，离线可用，隐私可控 |
| Core crate 不膨胀 | 新功能创建独立 crate，防止核心库成"垃圾桶" |

## 验证能力

代理自治的前提是能自己验证工作。按项目复杂度配置：

| 验证类型 | 适用项目 | 示例 |
|---------|---------|------|
| **端点验证** | Web/API | `curl localhost:5000/health` 返回 200 |
| **页面验证** | Web 应用 | 浏览器打开 `localhost:3000` 看到渲染结果 |
| **输出验证** | 命令行/脚本 | `python main.py` 输出预期结果 |
| **测试验证** | 所有项目（推荐） | `pytest` 全部通过 |
| **类型验证** | 有类型系统 | `mypy src/` 或 `tsc --noEmit` 无错误 |
| **编译验证** | Rust/C++/Go | `cargo check` / `bazel build //...` 通过 |
| **格式化验证** | 所有项目 | `cargo fmt --check` / `ruff check` |

特殊架构的扩展验证（TUI 渲染快照、桌面打包、进程生命周期、IPC 契约、平台签名）见 `architecture-special-cases.md`。

原则：**每个 ExecPlan 的 Validation 章节必须包含至少一种可执行的验证方式**。验证命令必须具体到可直接复制运行，不写"手动检查"这类模糊描述。
