# 技术栈推荐（2026年）

## 推荐原则（优先级从高到低）

- 用户熟悉的技术优先
- 不熟悉 → 选学习曲线最平缓的
- 同类技术选最轻量的（Flask > Django，Express > NestJS）
- 能不写代码就不写（内容站优先 Notion 等无代码方案；需自建时用 Astro 等静态生成器）
- 优先选择训练集覆盖广、API 稳定的"无聊"技术
- 新项目默认 TypeScript，不再作为可选项（2026 年 43.6% 开发者使用，已为专业开发基线）
- 新项目优先考虑全栈框架（Next.js / Reflex）减少技术选型负担

## 推荐表

| 项目类型 | 用户熟悉 | 推荐技术栈 | 备选方案 | 选择理由 |
|---------|---------|-----------|---------|---------|
| 网站/Web应用 | 无 | Next.js（React全栈，App Router） | Nuxt.js（Vue全栈）或 SvelteKit | React 是全球默认（Stack Overflow 46.9%），AI 工具链（v0/Cursor）默认生成 React，Next.js App Router + Server Components 是 2026 生产标准 |
| 网站/Web应用 | Python | Reflex（纯Python全栈）或 Flask | FastAPI + Jinja2 | Reflex 前后端都用Python；Flask 最轻量 |
| 网站/Web应用 | JavaScript | Next.js（React全栈，App Router） | Nuxt.js（Vue全栈） | Next.js 是 2026 年全栈首选（约 60% 新项目选择），Turbopack 构建，Server Components 默认，生态最大 |
| 数据看板/展示 | Python | Streamlit | Gradio | 最快将数据脚本变Web应用 |
| 命令行工具（简单脚本） | 无 | Python | Node.js (Commander.js) | 语法最简，标准库丰富 |
| 命令行工具（系统级/高性能） | 有 Rust 经验 | **Rust**（clap + tokio） | Go（cobra） | 内存安全、无 GC 延迟、二进制单文件分发，适合需要高性能/沙箱/文件系统操作的 CLI |
| 命令行工具（TUI 应用） | 有 Rust 经验 | **Rust**（ratatui + crossterm） | Go（bubbletea） | ratatui 是 2026 年最活跃的 Rust TUI 框架，社区活跃；适合完整终端应用（窗口/事件/渲染循环/状态管理） |
| 数据处理/分析 | 无 | Python + pandas + Streamlit | Jupyter + Plotly | 分析+可视化一站式 |
| API服务 | 无 | Python + FastAPI | Flask | 自动文档、类型安全、性能优 |
| API服务 | JavaScript | Hono（边缘/多运行时）或 Fastify（传统Node） | Express | Hono 支持 Cloudflare Workers/Bun/Deno/Node（14KB核心，冷启动12ms），多运行时零代码改动；Fastify 是纯 Node 性能最优（4x Express 吞吐，原生类型安全）；Express 仅推荐给已有项目维护 |
| API服务 | 有 Rust 经验 | **Rust**（axum + tokio） | Go（gin） | axum 是最活跃的 Rust Web 框架，类型安全中间件系统；tokio 异步运行时成熟；适合高并发、高性能、内存安全要求的 API 服务 |
| AI 应用 | 无 | Python + OpenAI SDK / LangChain | Python + Vercel AI SDK | 纯 Python 项目用 OpenAI SDK 最直接；LangChain 适合复杂 Agent 编排；Vercel AI SDK 需配合 Next.js（见下一行） |
| AI 应用 | JavaScript | Next.js + Vercel AI SDK | Next.js + OpenAI SDK | TypeScript + Next.js + Vercel AI SDK 是 2026 AI Web 应用的标准组合 |
| AI 应用 | 有 Rust 经验 | **Rust**（axum + llm-chain + tokio） | Python（FastAPI） | Rust 适合需要高性能并发、内存安全、沙箱执行的 AI Agent 项目；llm-chain 提供 Agent 编排；适合 coding agent、本地 LLM 推理等场景 |
| AI 聊天界面 | Python | Gradio | Streamlit + chat component | 最快搭建 ML/AI 演示界面 |
| 爬虫/数据采集 | 无 | Python + Crawl4AI 或 requests+BS4 | Scrapy | Crawl4AI 支持AI驱动的智能爬取 |
| 自动化脚本 | 无 | Python | Node.js | 标准库覆盖文件/网络/系统操作 |
| 微信小程序 | 无 | uni-app（Vue 跨端） | 微信原生（WXML/WXSS） | uni-app 学习曲线低、一次开发多端运行；原生适合纯微信场景 |
| 微信小程序 | React | Taro（React 跨端） | uni-app | Taro 保留 React 生态，跨端能力强 |
| 移动端 App | 无 | Expo（React Native 简化版） | Flutter | Expo 零原生配置、JS 生态、上手最快；Flutter 性能优但需学 Dart |
| 移动端 App | React/JS | React Native + Expo | Flutter | 保留 React 技术栈，Expo 提供托管式开发体验 |
| 移动端 App | Dart/Flutter | Flutter | React Native + Expo | Flutter 单代码库高性能渲染，UI 一致性最强 |
| 博客/内容站 | 无 | Astro + Markdown | Hugo | 岛屿架构零默认 JS、多框架组件支持，2026 年被 Cloudflare 收购保障长期维护，内容站性能最优 |
| 博客/内容站 | 无代码 | Notion + Next.js 模板 | WordPress | 零代码写作，自动发布 |
| 桌面应用 | 无 | Tauri 2 + React + TypeScript（前端 SPA） | Electron | Tauri 体积小（~10MB vs Electron ~150MB）、内存占用低、原生 Rust 层性能优；前端用 Vite SPA（无需 SSR/SEO），适合本地优先、离线场景 |
| 桌面应用 | 有 JS/React 经验 | Tauri 2 + React + TypeScript | Electron 或 Wails | 保留 React 技术栈，Tauri 原生层用 Rust 处理文件/进程/IPC；Electron 适合需要丰富 Node 生态的场景 |
| 桌面应用（Python Worker） | 有 Python 经验 | Tauri 2 + React + Python Worker（子进程） | PyWebView | Python Worker 通过子进程/IPC 与桌面桥通信，适合 AI/数据处理密集的本地应用；PyWebView 更轻量但生态有限 |

当用户拒绝推荐时，提供备选方案并解释差异。如果连备选也不想要，询问用户偏好，尊重用户选择——用户熟悉的技术永远优先。
