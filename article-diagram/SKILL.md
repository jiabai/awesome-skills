---
name: article-diagram
description: 自动为 Markdown 文章生成专业 SVG 插图，支持导出 JPEG 和双语插画网页。触发场景：(1) 用户要求为文章/博客/文档生成图表，(2) 文章需要可视化流程/架构/概念，(3) 需要将复杂概念转化为易懂图表，(4) 需要 SVG 转换为 JPEG 格式，(5) S 级内容需要独立双语网页。支持流程图、架构图、时序图、对比图。
---

# Article Diagram

为 Markdown 文章自动生成专业 SVG 插图，降低初级工程师/产品经理的认知负荷。

## Workflow

```
文章输入 → 提取 know-how → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown → (可选) 导出 JPEG
                                                                                          ↓
                                                                                    S级内容: 生成双语插画网页
```

## 1. 分析文章结构

读取 Markdown，提取标题层级、段落内容、代码块、现有图片。

## 2. 提取 know-how 列表（关键步骤）

**在生成插图前，必须先提取文章中的 know-how 点**：

1. 通读文章，列出所有 know-how/方法论/最佳实践
2. 对每个 know-how 判断：
   - 是否需要可视化？
   - 适合什么类型的图？
3. 形成插图清单，确保覆盖完整

**示例**：
```
文章：《Building a C compiler with parallel Claudes》

Know-how 列表：
1. Harness 循环机制 → 架构图 ✅
2. 任务锁同步机制 → 流程图 ✅
3. GCC Oracle 并行化策略 → 流程图 ✅（关键 know-how！）
4. 测试 Harness 设计原则 → 对比图 ✅
5. 上下文污染问题 → 对比图 ✅
6. 时间盲目性问题 → 对比图 ✅
7. 项目成果统计 → 统计图 ✅
```

## 3. 识别插图位置

使用 LLM 分析文章，识别需要可视化的位置。判断标准：

- **流程图**：≥3 步骤的顺序操作
- **架构图**：≥3 组件的关系
- **时序图**：有时间先后顺序的交互
- **对比图**：两方或多方案对比

**约束**：每篇文章 3-6 张插图，每张图 3-8 个组件。

## 4. 生成 SVG

设计规格详见 [references/design-spec.md](references/design-spec.md)。

**核心原则**：
- 深色背景 (#0B0F19)
- CSS class 统一样式
- 组件用卡片 + 标题 + 描述
- 不同类型用不同颜色区分

**图表类型**：
| 类型 | 用途 | 推荐尺寸 |
|------|------|----------|
| flowchart | 流程步骤 | 900×400 |
| architecture | 系统架构 | 1100×600 |
| sequence | 时序交互 | 1000×500 |
| comparison | 方案对比 | 900×340 |

**生成辅助**：
使用 `scripts/generate_diagram.py` 中的 Python 函数辅助生成标准 SVG：
```python
from generate_diagram import ColorScheme, card, step_circle, arrow_marker, connection_line, svg_template
```

## 5. 验证 SVG

**必须验证**：
```bash
# Python 验证脚本（推荐）
python scripts/validate_svg.py file.svg

# Linux/macOS/Git Bash - 检查未转义的 &
grep -E '&[^a]' file.svg | grep -v '&amp;' | grep -v '&lt;' | grep -v '&gt;'

# Windows PowerShell
Select-String -Path "file.svg" -Pattern '&[^a]' | Where-Object { $_.Line -notmatch '&amp;|&lt;|&gt;' }
```

**常见错误**：
- `&` → `&amp;`
- `<` (文本中) → `&lt;`
- `>` (文本中) → `&gt;`

## 6. 覆盖检查（关键步骤）

**生成插图后，必须做覆盖检查**：

1. 回顾 know-how 列表
2. 检查每个 know-how 是否有对应插图
3. 遗漏的 know-how 补充插图

**检查清单**：
```
☐ 架构概览是否有图？
☐ 关键流程是否有图？
☐ Know-how 方法论是否有图？
☐ 对比/决策点是否有图？
☐ 数据/统计是否有图？
```

## 7. 合并到 Markdown

在相关段落后插入：
```markdown
![图表标题](./diagrams/filename.svg)
```

## 8. 导出 JPEG（可选）

如需将 SVG 转换为 JPEG 格式（用于不支持 SVG 的平台）：

```bash
# 转换目录下所有 SVG
node scripts/svg-to-jpeg.js ./diagrams

# 转换单个文件
node scripts/svg-to-jpeg.js ./diagrams/chart.svg

# 指定输出目录和质量
node scripts/svg-to-jpeg.js ./diagrams ./output --quality 95 --bg #FFFFFF
```

**参数说明**：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--quality` | JPEG 质量 (1-100) | 90 |
| `--bg` | 背景色 (十六进制) | #FFFFFF |

## 9. 生成双语插画网页（S 级内容）

**当处理 S 级内容时，必须生成独立双语插画网页**。

### HTML 结构要求

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题</title>
    <style>/* 响应式样式 */</style>
</head>
<body>
    <section>
        <h2>图表标题</h2>
        <div class="diagram">
            <!-- 必须嵌入完整 SVG 代码 -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550">
                <defs>...</defs>
                <!-- 完整 SVG 内容 -->
            </svg>
            <div class="diagram-caption">图 1: 说明</div>
        </div>
    </section>
</body>
</html>
```

### SVG 嵌入规范（关键）

**必须嵌入完整 SVG 代码**，禁止 placeholder：

```html
<!-- ✅ 正确 -->
<div class="diagram">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550">
        <defs>
            <style>.bg { fill: #0B0F19; }</style>
            <marker id="arrowhead" .../>
        </defs>
        <rect class="bg" width="1100" height="550"/>
        <text x="550" y="40">标题</text>
        <!-- 所有图形元素 -->
    </svg>
</div>

<!-- ❌ 错误：placeholder -->
<div class="diagram">
    <svg>📊 请查看独立 SVG 文件</svg>
</div>
```

### 验证清单

- [ ] SVG 完整嵌入（非 placeholder）
- [ ] 包含 `<defs>` 和所有样式定义
- [ ] 包含 `<marker>` 等引用元素
- [ ] 所有图形元素完整
- [ ] HTML 文件大小>10KB（含 SVG）
- [ ] 移动端响应式（viewport meta tag）
- [ ] SVG 使用 `max-width: 100%; height: auto;`

## 示例

```
输入: 请为 sources/article.md 生成插图

步骤:
1. 提取 know-how 列表：7 个关键点
2. 设计插图清单：4 张图
3. 生成 SVG...
4. 覆盖检查：遗漏 GCC Oracle 策略，补充
5. 最终输出：5 张插图

输出:
✓ 分析文章：识别 7 个 know-how 点
✓ 设计清单：5 张插图
✓ 生成 diagrams/arch-1.svg (架构图)
✓ 生成 diagrams/flow-2.svg (流程图)
✓ 生成 diagrams/flow-3.svg (GCC Oracle 策略)
✓ 生成 diagrams/comp-4.svg (设计原则对比)
✓ 生成 diagrams/stats-5.svg (统计图)
✓ 验证 SVG 语法通过
✓ 覆盖检查通过
✓ 合并到 article.md
```

## Resources

### references/
- `design-spec.md` - 详细设计规范（颜色系统、字体样式、组件模板）

### scripts/
- `generate_diagram.py` - Python SVG 生成辅助脚本
- `validate_svg.py` - SVG 语法验证脚本（推荐使用）
- `svg-to-jpeg.js` - SVG 转 JPEG 转换脚本（需要 Node.js）
