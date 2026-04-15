---
name: wechat-article-writer
description: AI-powered writing assistant for WeChat public account articles. Use this skill whenever the user mentions writing articles, creating content, generating titles, building outlines, analyzing trending topics, optimizing writing style, or removing AI-generated text characteristics — even if they don't explicitly say "WeChat article" or "公众号". Triggers on: "写文章", "写公众号", "推文", "爆款标题", "文章大纲", "热点分析", "内容优化", "去AI味", "WeChat article", "viral content", "content creation", "article outline", "writing assistant".
---

# WeChat Article Writer

AI-powered writing assistant for WeChat public account content. Learns author style, generates viral titles, creates structured articles, and removes AI-generated text characteristics.

**Core principle**: Reduce bullet-point output. Use flowing paragraphs instead of numbered lists.

## When to Use

Use when user mentions:
- Writing WeChat/public account articles
- Generating viral titles
- Creating article outlines
- Analyzing trending topics
- Optimizing content style
- Removing AI text characteristics

## Workflow

### Phase 1: Resource Loading (REQUIRED)

1. Check `author-config.md` exists in skill directory. If missing, guide user to create one from `assets/author-config-template.md`.
2. Read `author-config.md` to learn author persona.
3. Load reference files based on article type — see **Reference Loading Guide** below.
4. Fetch trending topics via WebSearch if needed.

### Phase 2: Title Generation

Generate 4 types × 3-5 options each: Contrast, Question, Number+Effect, Negation+Reversal. Recommend best match for author persona.

### Phase 3: Structure Creation

Choose template based on article type. Include section word counts, image placement suggestions, key points per section.

### Phase 4: Content Creation

**Key requirements**:
- Use author's voice (first-person "I" if configured)
- Share failures and frustrations (authenticity)
- Emotional expression (match persona)
- Moderate self-deprecation (if configured)
- Empower readers: "Even I can do this"
- **CRITICAL**: Reduce bullet-point output — use flowing paragraphs

### Phase 5: Optimization

- Style adjustment (match author-config)
- Remove AI characteristics (read `references/remove-ai-style.md`)
- Check viral elements checklist
- Verify persona consistency

## Reference Loading Guide

Load files based on context — do NOT load all files upfront.

| File | When to Load | Purpose |
|------|-------------|---------|
| `references/viral-writing-method.md` | Tool intro or Tutorial article | Core writing methodology, title formulas, article structures |
| `references/deep-cognition-writing.md` | Deep thinking article | Cognitive upgrade framework, 6-part structure |
| `references/trending-analysis.md` | Need trending topics | Search keywords, analysis dimensions, output format |
| `references/remove-ai-style.md` | Optimization phase | AI word blacklist, replacement suggestions, persona adaptation |
| `references/quick-reference.md` | Quick lookup during writing | One-page summary of commands, templates, checklists |
| `references/workflow-guide.md` | First time or need detailed steps | Complete creation workflow with special scenarios |
| `assets/author-config-template.md` | User has no config yet | Template for author settings |
| `assets/author-config-example.md` | User needs config example | Example filled configuration |

**Loading strategy**: Start with `references/viral-writing-method.md` as the default. Swap to `references/deep-cognition-writing.md` for deep thinking articles. Load `references/remove-ai-style.md` only during Phase 5. Load `references/trending-analysis.md` only when fetching trends. Use `references/quick-reference.md` for quick lookups instead of reloading larger files.

## Article Types

| Type | Structure | Length | Primary Reference |
|------|-----------|--------|-------------------|
| Tool intro | Hook → Pain → Solution → Story → Iteration → Value → CTA | 2000-3000 | `viral-writing-method.md` |
| Tutorial | Quote → Problem → Tool → Demo → Effect → Summary → CTA | 2000-2500 | `viral-writing-method.md` |
| Deep thinking | Question → Background → History → Analysis → 追问 → Open ending | 2500-3500 | `deep-cognition-writing.md` |

## Author Persona Types

| Type | Characteristics |
|------|-----------------|
| Friendly | First-person "I", emotional, moderate self-deprecation |
| Professional | Data-driven, objective analysis, proper terminology |
| Humorous | Light调侃, vivid metaphors, colloquial |
| Minimalist | Concise, direct, few adjectives |

## Commands

| Command | Purpose |
|---------|---------|
| `/热点 [关键词]` | Fetch trending topics |
| `/标题生成 [主题]` | Generate viral titles |
| `/结构生成 [类型] [主题]` | Create article outline |
| `/内容优化 [文本]` | Optimize content style |
| `/金句生成 [观点]` | Generate shareable quotes |
| `/爆款检查 [文章]` | Check viral elements |
| `/去AI化 [文本]` | Remove AI characteristics |

## Critical Principle: Reduce Bullet-Point Output

**AVOID**:
```
1. First, do A
2. Then, do B
3. Finally, do C
```

**USE**:
```
When doing this, most start with A. But I suggest spending time on B first,
then returning to A. Why? Because [reason]. C follows naturally — no rush.
```

**Exceptions**: Checklists, comparison tables, parallel options (keep ≤5 items).

## Quality Checklist

Before publishing, verify:

```
□ Title has contrast/number/surprise
□ Hook grabs attention in 3 seconds
□ Image every 300 words
□ Subheading every 500-800 words
□ Emotional expression (match persona)
□ Shareable quotes
□ Interaction design
□ Call to action
□ Solves real pain point
□ Provides actionable method
```

## Implementation

Invoke this skill when user requests article writing. The skill will:

1. Announce: "Using wechat-article-writer to create article"
2. Load author-config.md (or prompt user to create from `assets/author-config-template.md`)
3. Load relevant reference files based on article type
4. Execute complete workflow
5. Output optimized article

**If author-config.md missing**: Ask user for pen name, identity, field, preferred style, and provide `assets/author-config-template.md`.