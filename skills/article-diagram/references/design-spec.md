# SVG Design Specification

统一的设计规范确保生成的 SVG 插图风格一致、专业美观。

## Overview

本文档定义了 article-diagram 生成的所有 SVG 插图的颜色系统、字体样式、组件模板和布局规范。

## Color System

### 背景色

| 名称 | 色值 | 用途 |
|------|------|------|
| Primary BG | `#0B0F19` | 主背景色 |
| Card BG | `#181C2A` | 卡片背景 |
| Card Alt BG | `#1E283F` | 交替卡片背景 |

### 文字颜色

| 名称 | 色值 | 用途 |
|------|------|------|
| Title | `#FFFFFF` | 标题文字 |
| Subtitle | `#A0A5B5` | 副标题 |
| Heading | `#E2E8F0` | 组件标题 |
| Body | `#94A3B8` | 正文描述 |
| Muted | `#6B7280` | 辅助文字 |

### 图表类型颜色

| 类型 | 强调色 | 浅色变体 | 背景色 | 用途 |
|------|--------|----------|--------|------|
| flowchart | `#22D3EE` | `#67E8F9` | `#0C2D3E` | 流程步骤 |
| architecture | `#A78BFA` | `#B892FA` | `#2D2150` | 系统架构 |
| sequence | `#FB923C` | `#FDBA74` | `#3D2510` | 时序交互 |
| comparison | `#4ADE80` | `#86EFAC` | `#0D3320` | 方案对比 |
| stats | `#F472B6` | `#F9A8D4` | `#3D1530` | 统计数据 |

### 边框和连接线

| 用途 | 色值 |
|------|------|
| Card Border | `#334155` |
| Arrow/Connector | `#64748B` |
| Highlight | `#38BDF8` |

## Typography

### Font Family
```css
font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
```

### Font Sizes

| 用途 | 字号 | 字重 | 颜色 |
|------|------|------|------|
| 标题 (Title) | 26-32px | 800 | #FFFFFF |
| 副标题 (Subtitle) | 13-16px | 400 | #A0A5B5 |
| 组件标题 (Node Heading) | 14-16px | 700 | 类型强调色 |
| 组件描述 (Node Body) | 11-13px | 400 | #94A3B8 |
| 步骤编号 (Step Number) | 16-22px | 900 | #FFFFFF |
| 标签 (Badge) | 10-11px | 700 | 类型强调色 |

## Layout

### Grid System
- Grid pattern: 40×40px
- Stroke width: 0.3px
- Pattern opacity: 0.25
- Pattern color: `#1E293B`

### Card Component

```
┌─────────────────────────────┐
│ Title                      │  <- 14-16px, weight 700, 类型强调色
├─────────────────────────────┤
│ Description text here      │  <- 11-13px, weight 400, #94A3B8
│ Second line                │
└─────────────────────────────┘
```

- Background: `#181C2A`
- Border: 1.5px 类型强调色
- Border-radius: 12px
- Padding: 16px

### Step Circle Component

```
    ┌───┐
    │ 1 │   <- 16-22px, weight 900, #FFFFFF on 类型强调色
    └───┘
```

- Circle radius: 14px
- Fill: 类型强调色
- Text: 居中, white

## Diagram Sizes

| 类型 | 宽度 | 高度 |
|------|------|------|
| flowchart | 900px | 400px |
| architecture | 1100px | 600px |
| sequence | 1000px | 500px |
| comparison | 900px | 340px |

## SVG Structure

```svg
<svg width="[W]" height="[H]" viewBox="0 0 [W] [H]" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title { font-family: system-ui, sans-serif; font-weight: 800; font-size: 28px; fill: #FFFFFF; }
      .subtitle { font-family: system-ui, sans-serif; font-size: 14px; fill: #A0A5B5; }
      .node-h { font-family: system-ui, sans-serif; font-weight: 700; font-size: 14px; }
      .node-b { font-family: system-ui, sans-serif; font-size: 12px; fill: #94A3B8; }
      .step-num { font-family: system-ui, sans-serif; font-weight: 900; font-size: 18px; }
    </style>
    <marker id="arrowBlue" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#22D3EE"/>
    </marker>
    <marker id="arrowGreen" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#4ADE80"/>
    </marker>
    <marker id="arrowPurple" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#A78BFA"/>
    </marker>
    <marker id="arrowOrange" markerWidth="9" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 9 3, 0 6" fill="#FB923C"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="[W]" height="[H]" fill="#0B0F19"/>

  <!-- Title Area -->
  <text x="[W/2]" y="40" text-anchor="middle" class="title">图表标题</text>
  <text x="[W/2]" y="60" text-anchor="middle" class="subtitle">副标题说明</text>

  <!-- Content Cards -->
  <g transform="translate(x, y)">
    <rect width="200" height="100" rx="12" fill="#181C2A" stroke="#22D3EE" stroke-width="1.5"/>
    <text x="15" y="28" class="node-h" fill="#22D3EE">Title</text>
    <text x="15" y="50" class="node-b">Description</text>
  </g>

  <!-- Connectors -->
  <line x1="100" y1="150" x2="200" y2="150" stroke="#64748B" stroke-width="2" marker-end="url(#arrowBlue)"/>
</svg>
```

## Arrow Markers

| 类型 | 颜色 | 用途 |
|------|------|------|
| arrowBlue | `#22D3EE` | 流程图连接 |
| arrowGreen | `#4ADE80` | 对比图/成功 |
| arrowPurple | `#A78BFA` | 架构图连接 |
| arrowOrange | `#FB923C` | 时序图连接 |

## CSS Classes

```css
.card { cursor: pointer; }
.card:hover rect:first-child { stroke: #38BDF8; }
.title { font-size: 26-32px; font-weight: 800; fill: #FFFFFF; }
.subtitle { font-size: 13-16px; fill: #A0A5B5; }
.node-h { font-size: 14-16px; font-weight: 700; }
.node-b { font-size: 11-13px; fill: #94A3B8; }
.step-num { font-size: 16-22px; font-weight: 900; }
```

## XML Escape Rules

| 字符 | 转义为 |
|------|--------|
| & | &amp; |
| < | &lt; |
| > | &gt; |
| " | &quot; |
| ' | &apos; |

## Best Practices

1. 保持 16px 内边距
2. 使用 `rx="12"` 圆角
3. 确保文字对比度足够
4. 避免超过 8 个组件
5. 使用统一的连接线样式
6. 类型强调色用于边框和关键文字
7. 背景变体用于高亮或特殊状态
