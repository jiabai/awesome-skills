---
name: article-diagram
description: 自动为 Markdown 文章生成专业 SVG 插图，支持导出 JPEG。触发场景：(1) 用户要求为文章/博客/文档生成图表，(2) 文章需要可视化流程/架构/概念，(3) 需要将复杂概念转化为易懂图表，(4) 需要将 SVG 转换为 JPEG 格式。支持流程图、架构图、时序图、对比图。
---

# Article Diagram

为 Markdown 文章自动生成专业 SVG 插图，降低初级工程师/产品经理的认知负荷。

## Workflow

```
文章输入 → 提取 know-how → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown
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

## 5. 验证 SVG

**必须验证**：

```bash
# Linux/macOS/Git Bash - 检查未转义的 &
grep -E '&[^a]' file.svg | grep -v '&amp;' | grep -v '&lt;' | grep -v '&gt;'
```

```powershell
# Windows PowerShell - 检查未转义的 &
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

## 8. 导出为 JPEG（可选）

如需将 SVG 转换为 JPEG 格式：

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

**使用场景**：
- 平台不支持 SVG 显示（如某些微信公众号编辑器）
- 需要固定尺寸的预览图
- 兼容旧版浏览器或文档系统

## 示例

```
输入：请为 sources/article.md 生成插图

步骤:
1. 提取 know-how 列表：7 个关键点
2. 设计清单：4 张图
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
- `svg-to-jpeg.js` - SVG 转 JPEG 转换脚本
