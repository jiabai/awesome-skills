# 技术栈推荐（2026年）

## 推荐原则（优先级从高到低）

- 用户熟悉的技术优先
- 不熟悉 → 选学习曲线最平缓的
- 同类技术选最轻量的（Flask > Django，Express > NestJS）
- 能不写代码就不写（如博客用 Astro + GitHub Pages）
- 优先选择训练集覆盖广、API 稳定的"无聊"技术
- 新项目优先考虑全栈框架（Next.js / Reflex）减少技术选型负担

## 推荐表

| 项目类型 | 用户熟悉 | 推荐技术栈 | 选择理由 |
|---------|---------|-----------|---------|
| 网站/Web应用 | 无 | Vue.js 或 Svelte（纯前端） | 学习曲线最低，文档友好 |
| 网站/Web应用 | Python | Reflex（纯Python全栈）或 Flask | Reflex 前后端都用Python；Flask 最轻量 |
| 网站/Web应用 | JavaScript | Next.js（React全栈） | React生态最大，Next.js 全栈一体化 |
| 数据看板/展示 | Python | Streamlit | 最快将数据脚本变Web应用 |
| 命令行工具 | 无 | Python | 语法最简，标准库丰富 |
| 数据处理/分析 | 无 | Python + pandas + Streamlit | 分析+可视化一站式 |
| API服务 | 无 | Python + FastAPI | 自动文档、类型安全、性能优 |
| API服务 | JavaScript | Hono 或 Express | Hono 更轻量现代；Express 生态成熟 |
| AI 应用 | 无 | Python + Vercel AI SDK / LangChain | AI SDK 简单直接；LangChain 适合复杂 Agent |
| AI 应用 | JavaScript | Next.js + Vercel AI SDK | TypeScript AI 开发首选组合 |
| AI 聊天界面 | Python | Gradio | 最快搭建 ML/AI 演示界面 |
| 爬虫/数据采集 | 无 | Python + Crawl4AI 或 requests+BS4 | Crawl4AI 支持AI驱动的智能爬取 |
| 自动化脚本 | 无 | Python | 标准库覆盖文件/网络/系统操作 |
| 微信小程序 | 无 | 微信开发者工具 + JavaScript | 官方工具链 |
| 博客/内容站 | 无 | Astro + Markdown | 默认零JS，SEO极佳，性能最优 |
| 博客/内容站 | 无代码 | Notion + Next.js 模板 | 零代码写作，自动发布 |
