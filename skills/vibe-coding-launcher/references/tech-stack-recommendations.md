# Tech Stack Recommendations (2026)

## Recommendation Priorities

- Prefer technology the user already knows.
- If the user is unfamiliar with the options, choose the gentlest learning curve.
- Among equivalent technologies, choose the lightest option (Flask over Django, Express over NestJS).
- Avoid code when a no-code option is sufficient. Prefer Notion for a content site; use a static generator such as Astro when self-hosting is required.
- Prefer "boring" technologies with broad training-data coverage and stable APIs.
- Default new projects to TypeScript; it is no longer presented as an optional extra (43.6% of developers use it in 2026, making it a professional baseline).
- Prefer full-stack frameworks such as Next.js or Reflex for new projects to reduce technology-selection overhead.

## Recommendation Table

| Project Type | User Experience | Recommended Stack | Alternative | Why |
|--------------|-----------------|-------------------|-------------|-----|
| Website / web app | None | Next.js (React full stack, App Router) | Nuxt.js (Vue full stack) or SvelteKit | React is the global default (46.9% on Stack Overflow); AI toolchains such as v0 and Cursor generate React by default; Next.js App Router + Server Components is a 2026 production standard |
| Website / web app | Python | Reflex (Python-only full stack) or Flask | FastAPI + Jinja2 | Reflex uses Python on both sides; Flask is the lightest option |
| Website / web app | JavaScript | Next.js (React full stack, App Router) | Nuxt.js (Vue full stack) | Next.js is a leading 2026 full-stack choice (selected by roughly 60% of new projects), with Turbopack builds, Server Components by default, and the largest ecosystem |
| Data dashboard / presentation | Python | Streamlit | Gradio | Fastest path from a data script to a web app |
| CLI (simple script) | None | Python | Node.js (Commander.js) | Simple syntax and rich standard library |
| CLI (systems / high performance) | Rust | **Rust** (clap + tokio) | Go (cobra) | Memory safety, no GC latency, single-binary distribution, and strong support for performance, sandboxing, and filesystem operations |
| CLI (TUI) | Rust | **Rust** (ratatui + crossterm) | Go (bubbletea) | ratatui is an active Rust TUI framework suited to full terminal apps with windows, events, render loops, and state management |
| Data processing / analysis | None | Python + pandas + Streamlit | Jupyter + Plotly | Analysis and visualization in one stack |
| API service | None | Python + FastAPI | Flask | Automatic docs, type safety, and strong performance |
| API service | JavaScript | Hono (edge/multi-runtime) or Fastify (traditional Node) | Express | Hono supports Cloudflare Workers, Bun, Deno, and Node with no code changes (14 KB core, 12 ms cold start); Fastify offers about 4× Express throughput and native type safety; reserve Express for existing-project maintenance |
| API service | Rust | **Rust** (axum + tokio) | Go (gin) | axum provides a type-safe middleware system and tokio offers a mature async runtime; suitable for high-concurrency, high-performance, memory-safe services |
| AI application | None | Python + OpenAI SDK / LangChain | Python + Vercel AI SDK | The OpenAI SDK is direct for Python projects; LangChain suits complex agent orchestration; Vercel AI SDK is best paired with Next.js |
| AI application | JavaScript | Next.js + Vercel AI SDK | Next.js + OpenAI SDK | TypeScript + Next.js + Vercel AI SDK is a standard 2026 AI web stack |
| AI application | Rust | **Rust** (axum + llm-chain + tokio) | Python (FastAPI) | Suitable for high-concurrency, memory-safe, sandboxed AI agents and local-LLM workloads; llm-chain provides orchestration |
| AI chat UI | Python | Gradio | Streamlit + chat component | Fastest way to build an ML/AI demonstration UI |
| Web scraping / data collection | None | Python + Crawl4AI or requests + BeautifulSoup | Scrapy | Crawl4AI supports AI-assisted extraction |
| Automation script | None | Python | Node.js | Standard-library coverage for files, networking, and system operations |
| WeChat Mini Program | None | uni-app (cross-platform Vue) | Native WeChat (WXML/WXSS) | Gentle learning curve and multi-platform output; native is suitable for WeChat-only products |
| WeChat Mini Program | React | Taro (cross-platform React) | uni-app | Retains the React ecosystem and strong cross-platform support |
| Mobile app | None | Expo (simplified React Native) | Flutter | No native configuration, a broad JS ecosystem, and the fastest onboarding; Flutter offers strong performance but requires Dart |
| Mobile app | React / JS | React Native + Expo | Flutter | Retains the React stack while Expo supplies a managed development experience |
| Mobile app | Dart / Flutter | Flutter | React Native + Expo | High-performance, consistent UI from one codebase |
| Blog / content site | None | Astro + Markdown | Hugo | Islands architecture with zero default JS and multi-framework components; Cloudflare's 2026 acquisition supports long-term maintenance; strong content-site performance |
| Blog / content site | No-code | Notion + Next.js template | WordPress | No-code writing and automatic publishing |
| Desktop app | None | Tauri 2 + React + TypeScript (frontend SPA) | Electron | Smaller binaries and lower memory use than Electron, with a performant Rust native layer; a Vite SPA is sufficient because desktop apps need neither SSR nor SEO |
| Desktop app | JS / React | Tauri 2 + React + TypeScript | Electron or Wails | Retains React while Rust handles files, processes, and IPC; Electron suits products that require the broader Node ecosystem |
| Desktop app with Python worker | Python | Tauri 2 + React + Python worker subprocess | PyWebView | A subprocess/IPC worker suits local AI or data-intensive workloads; PyWebView is lighter but has a smaller ecosystem |

When the user rejects a recommendation, offer an alternative and explain the tradeoff. If they reject the alternative too, ask for their preference and respect it. Familiar technology always takes priority.
