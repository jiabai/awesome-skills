# Architecture

## 概述

小红书自动化技能集合，通过 Chrome 扩展和 CDP（Chrome DevTools Protocol）协议操作用户真实浏览器，实现小红书的自动化操作。

## 代码地图

```
xhs-automator/
├── scripts/                    # Python 自动化引擎
│   ├── cli.py                  # 统一 CLI 入口（JSON 输出）
│   ├── bridge_server.py        # 本地 WebSocket 通信服务
│   ├── xhs/                    # 核心自动化包
│   │   ├── bridge.py           # 扩展通信客户端
│   │   ├── cdp.py              # CDP 协议实现
│   │   ├── login.py            # 登录 + 用户信息
│   │   ├── search.py           # 搜索 + 筛选
│   │   ├── publish.py          # 图文发布
│   │   ├── publish_video.py    # 视频发布
│   │   ├── publish_long_article.py  # 长文发布
│   │   ├── comment.py          # 评论、回复
│   │   ├── like_favorite.py    # 点赞、收藏
│   │   ├── feed_detail.py      # 笔记详情
│   │   ├── feeds.py            # 首页 Feed
│   │   ├── user_profile.py     # 用户主页
│   │   ├── selectors.py        # CSS 选择器集中管理
│   │   ├── types.py            # 数据类型定义
│   │   ├── errors.py           # 异常体系
│   │   ├── urls.py             # URL 常量
│   │   ├── cookies.py          # Cookie 持久化
│   │   └── human.py            # 行为模拟
│   ├── image_downloader.py     # 媒体下载（SHA256 缓存）
│   ├── title_utils.py          # UTF-16 标题长度计算
│   └── run_lock.py             # 单实例锁
├── extension/                  # Chrome 扩展
│   ├── manifest.json
│   ├── background.js
│   └── content.js
└── skills/                     # Claude Code Skills 定义
    ├── xhs-auth/SKILL.md
    ├── xhs-publish/SKILL.md
    ├── xhs-explore/SKILL.md
    ├── xhs-interact/SKILL.md
    └── xhs-content-ops/SKILL.md
```

## 模块关系

```
CLI (cli.py)
  └── xhs/ (核心自动化包)
        ├── bridge.py ←→ extension/ (Chrome 扩展)
        ├── cdp.py (CDP 协议)
        └── 各功能模块 (login, search, publish, ...)
```

- CLI 是唯一用户入口，负责参数解析和 JSON 输出
- bridge_server.py 提供本地 WebSocket 服务，连接 CLI 和浏览器扩展
- xhs/ 包内各模块通过 bridge 或 CDP 与浏览器交互
- extension/ 在用户真实浏览器中执行 DOM 操作

## 关键文件

- `scripts/cli.py` — 统一 CLI 入口，所有子命令的路由和参数定义
- `scripts/xhs/bridge.py` — 扩展通信客户端，封装 WebSocket 消息协议
- `scripts/xhs/cdp.py` — CDP 协议实现，直接控制浏览器
- `scripts/xhs/selectors.py` — CSS 选择器集中管理，小红书页面元素定位
- `extension/content.js` — 浏览器扩展内容脚本，执行 DOM 操作

## 架构不变量

- 双层结构：`scripts/` 是 Python 自动化引擎，`skills/` 是 Claude Code Skills 定义
- CLI 是唯一执行入口，所有操作通过 `python scripts/cli.py <子命令>` 完成
- 通过 bridge server（WebSocket）连接 CLI 与浏览器扩展，不直接操作页面
- 所有 CSS 选择器集中在 `selectors.py`，不散落在各模块中
- 异常继承 `XHSError`，CLI exit code：0=成功，1=未登录，2=错误
