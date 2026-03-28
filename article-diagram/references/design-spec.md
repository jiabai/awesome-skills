# SVG Design Specification

## Overview

统一的设计规范确保生成的 SVG 插图风格一致、专业美观。

## Color System

### Background Colors
| 名称 | 色值 | 用途 |
|------|------|------|
| Primary BG | `#0B0F19` | 主背景色 |
| Card BG | `#1E293B` | 卡片背景 |
| Grid | `#1E293B` | 网格线 (opacity 0.25) |

### Text Colors
| 名称 | 色值 | 用途 |
|------|------|------|
| Primary Text | `#F8FAFC` | 主文本 |
| Secondary Text | `#94A3B8` | 次要文本/描述 |
| Muted Text | `#64748B` | 辅助文本 |

### Diagram Type Colors
| 类型 | 强调色 | 用途 |
|------|--------|------|
| flowchart | `#22D3EE` | 流程步骤 |
| architecture | `#A78BFA` | 系统架构 |
| sequence | `#FB923C` | 时序交互 |
| comparison | `#4ADE80` | 方案对比 |
| stats | `#F472B6` | 统计数据 |

### Border & Line Colors
| 用途 | 色值 |
|------|------|
| Card Border | `#334155` |
| Arrow/Connector | `#475569` |
| Highlight | `#38BDF8` |

## Typography

### Font Family
```css
font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
```

### Font Sizes
| 用途 | 字号 |
|------|------|
| 标题 (Card Title) | 16px, font-weight: 600 |
| 描述 (Description) | 14px, font-weight: 400 |
| 标签 (Label) | 12px, font-weight: 500 |
| 小字 (Caption) | 11px, font-weight: 400 |

## Layout

### Grid System
- Grid pattern: 40×40px
- Stroke width: 0.3px
- Pattern opacity: 0.25

### Card Component
```
┌─────────────────────────┐
│ Title                   │  <- 16px, #F8FAFC
├─────────────────────────┤
│ Description text here   │  <- 14px, #94A3B8
└─────────────────────────┘
```
- Background: `#1E293B`
- Border: 1px `#334155`
- Border-radius: 8px
- Padding: 16px

## Diagram Sizes

| 类型 | 宽度 | 高度 |
|------|------|------|
| flowchart | 900px | 400px |
| architecture | 1100px | 600px |
| sequence | 1000px | 500px |
| comparison | 900px | 340px |

## SVG Structure

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 [W] [H]" font-family="system-ui,-apple-system,'Segoe UI',sans-serif">
  <defs>
    <!-- Patterns and gradients -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="0.3"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="[W]" height="[H]" fill="#0B0F19"/>
  <rect width="[W]" height="[H]" fill="url(#grid)" opacity="0.25"/>

  <!-- Content Cards -->
  <g class="card">
    <rect class="card-bg" width="180" height="80" fill="#1E293B" stroke="#334155" rx="8"/>
    <text class="card-title" x="16" y="28" fill="#F8FAFC" font-size="16" font-weight="600">Title</text>
    <text class="card-desc" x="16" y="52" fill="#94A3B8" font-size="14">Description</text>
  </g>

  <!-- Connectors -->
  <g class="connector" stroke="#475569" stroke-width="1.5" fill="none">
    <path d="M startX startY L endX endY" marker-end="url(#arrow)"/>
  </g>
</svg>
```

## CSS Classes

```css
.card { cursor: pointer; }
.card:hover .card-bg { stroke: #38BDF8; }
.title { font-size: 16px; font-weight: 600; fill: #F8FAFC; }
.description { font-size: 14px; fill: #94A3B8; }
.label { font-size: 12px; font-weight: 500; fill: #64748B; }
```

## Best Practices

1. 保持 16px 内边距
2. 使用 `rx="8"` 圆角
3. 确保文字对比度足够
4. 避免超过 8 个组件
5. 使用统一的连接线样式
