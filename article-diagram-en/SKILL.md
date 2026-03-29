---
name: article-diagram
description: Automatically generate professional SVG illustrations for Markdown articles, with JPEG export and bilingual illustration pages. Triggers: (1) User requests diagrams for articles/blogs/docs, (2) Articles need visualization of flows/architecture/concepts, (3) Complex concepts need to be converted to easy-to-understand diagrams, (4) SVG to JPEG conversion needed, (5) S-tier content needs standalone bilingual pages. Supports flowcharts, architecture diagrams, sequence diagrams, and comparison diagrams.
---

# Article Diagram

Automatically generate professional SVG illustrations for Markdown articles, reducing cognitive load for junior engineers and product managers.

## Workflow

```
Article Input → Extract Know-how → Design Illustration List → Generate SVG
             → Validate Syntax → Coverage Check → Merge to Markdown
                                                                        ↓
                                                              S-tier Content
                                                              Generate Bilingual Illustration Page

                                          (Optional) Export JPEG
```

## 1. Analyze Article Structure

Read Markdown, extract heading hierarchy, paragraph content, code blocks, and existing images.

## 2. Extract Know-how List (Critical Step)

**Before generating illustrations, extract know-how points from the article**:

1. Read through the article, list all know-how/methodologies/best practices
2. For each know-how, determine:
   - Does it need visualization?
   - What type of diagram is appropriate?
3. Form an illustration list, ensure complete coverage

**Example**:
```
Article: "Building a C compiler with parallel Claudes"

Know-how List:
1. Harness loop mechanism → Architecture diagram ✅
2. Task lock synchronization → Flowchart ✅
3. GCC Oracle parallelization strategy → Flowchart ✅ (Critical know-how!)
4. Test Harness design principles → Comparison diagram ✅
5. Context pollution issue → Comparison diagram ✅
6. Time blindness issue → Comparison diagram ✅
7. Project results statistics → Stats diagram ✅
```

## 3. Identify Illustration Positions

Use LLM to analyze the article and identify positions needing visualization. Criteria:

- **Flowchart**: ≥3 sequential steps
- **Architecture diagram**: ≥3 component relationships
- **Sequence diagram**: Interactions with temporal order
- **Comparison diagram**: Two or more approaches comparison

**Constraints**: 3-6 illustrations per article, 3-8 components per diagram.

## 4. Generate SVG

See [references/design-spec.md](references/design-spec.md) for design specifications.

**Core Principles**:
- Dark background (#0B0F19)
- Unified CSS class styles
- Components use card + title + description
- Different types use different colors

**Diagram Types**:
| Type | Purpose | Recommended Size |
|------|---------|------------------|
| flowchart | Process steps | 900×400 |
| architecture | System architecture | 1100×600 |
| sequence | Sequential interactions | 1000×500 |
| comparison | Approach comparison | 900×340 |

**Generation Helper**:
Use Python functions from `scripts/generate_diagram.py` to assist in generating standard SVG:
```python
from generate_diagram import ColorScheme, card, step_circle, arrow_marker, connection_line, svg_template
```

## 5. Validate SVG

**Must validate**:
```bash
# Python validation script (recommended)
python scripts/validate_svg.py file.svg

# Linux/macOS/Git Bash - Check unescaped &
grep -E '&[^a]' file.svg | grep -v '&amp;' | grep -v '&lt;' | grep -v '&gt;'

# Windows PowerShell
Select-String -Path "file.svg" -Pattern '&[^a]' | Where-Object { $_.Line -notmatch '&amp;|&lt;|&gt;' }
```

**Common Errors**:
- `&` → `&amp;`
- `<` (in text) → `&lt;`
- `>` (in text) → `&gt;`

## 6. Coverage Check (Critical Step)

**After generating illustrations, must perform coverage check**:

1. Review know-how list
2. Check if each know-how has corresponding illustration
3. Add illustrations for missing know-how

**Checklist**:
```
☐ Architecture overview has diagram?
☐ Key processes have diagrams?
☐ Know-how methodologies have diagrams?
☐ Comparisons/decision points have diagrams?
☐ Data/statistics have diagrams?
```

## 7. Merge to Markdown

Insert after relevant paragraphs:
```markdown
![Diagram Title](./diagrams/filename.svg)
```

## 8. Export JPEG (Optional)

To convert SVG to JPEG format (for platforms that don't support SVG):

```bash
# Convert all SVGs in directory
node scripts/svg-to-jpeg.js ./diagrams

# Convert single file
node scripts/svg-to-jpeg.js ./diagrams/chart.svg

# Specify output directory and quality
node scripts/svg-to-jpeg.js ./diagrams ./output --quality 95 --bg #FFFFFF
```

**Parameters**:
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--quality` | JPEG quality (1-100) | 90 |
| `--bg` | Background color (hex) | #FFFFFF |

## 9. Generate Bilingual Illustration Page (S-tier Content)

**When processing S-tier content, must generate standalone bilingual illustration pages**.

### HTML Structure Requirements

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Title</title>
    <style>/* Responsive styles */</style>
</head>
<body>
    <section>
        <h2>Diagram Title</h2>
        <div class="diagram">
            <!-- Must embed complete SVG code -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550">
                <defs>...</defs>
                <!-- Complete SVG content -->
            </svg>
            <div class="diagram-caption">Figure 1: Description</div>
        </div>
    </section>
</body>
</html>
```

### SVG Embedding Specification (Critical)

**Must embed complete SVG code**, no placeholders:

```html
<!-- ✅ Correct -->
<div class="diagram">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550">
        <defs>
            <style>.bg { fill: #0B0F19; }</style>
            <marker id="arrowhead" .../>
        </defs>
        <rect class="bg" width="1100" height="550"/>
        <text x="550" y="40">Title</text>
        <!-- All graphic elements -->
    </svg>
</div>

<!-- ❌ Wrong: placeholder -->
<div class="diagram">
    <svg>📊 Please see standalone SVG file</svg>
</div>
```

### Validation Checklist

- [ ] SVG fully embedded (not placeholder)
- [ ] Contains `<defs>` and all style definitions
- [ ] Contains `<marker>` and other reference elements
- [ ] All graphic elements complete
- [ ] HTML file size >10KB (including SVG)
- [ ] Mobile responsive (viewport meta tag)
- [ ] SVG uses `max-width: 100%; height: auto;`

## Example

```
Input: Generate illustrations for sources/article.md

Steps:
1. Extract know-how list: 7 key points
2. Design illustration list: 4 diagrams
3. Generate SVG...
4. Coverage check: Missing GCC Oracle strategy, add
5. Final output: 5 illustrations

Output:
✓ Analyzed article: Identified 7 know-how points
✓ Designed list: 5 illustrations
✓ Generated diagrams/arch-1.svg (Architecture diagram)
✓ Generated diagrams/flow-2.svg (Flowchart)
✓ Generated diagrams/flow-3.svg (GCC Oracle strategy)
✓ Generated diagrams/comp-4.svg (Design principles comparison)
✓ Generated diagrams/stats-5.svg (Statistics diagram)
✓ SVG syntax validation passed
✓ Coverage check passed
✓ Merged to article.md
```

## Resources

### references/
- `design-spec.md` - Detailed design specifications (color system, typography, component templates)

### scripts/
- `generate_diagram.py` - Python SVG generation helper script
- `validate_svg.py` - SVG syntax validation script (recommended)
- `svg-to-jpeg.js` - SVG to JPEG conversion script (requires Node.js)
