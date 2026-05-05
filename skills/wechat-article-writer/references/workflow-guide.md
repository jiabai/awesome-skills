# Workflow Guide

> Complete workflow for article creation - AI must follow this

## Phase 1: Resource Loading (REQUIRED)

### When user requests article

```
【Your Input】
"我要写一篇关于[主题]的文章"

【AI Auto Execute】

Step 1: Check author config ✅
├─ Check author-config.md exists
├─ If exists → Read and extract persona
└─ If missing → Guide user to fill or ask core features

Step 2: Load method files (based on article type) ✅
├─ references/viral-writing-method.md (tool intro / tutorial)
├─ references/deep-cognition-writing.md (deep thinking)
├─ references/trending-analysis.md (when fetching trends)
├─ references/remove-ai-style.md (optimization phase)
└─ references/quick-reference.md (quick lookup)

Step 3: Learn user style ✅
├─ Read author-config.md
├─ Read 2-3 existing articles (if provided)
└─ Extract: Opening style, paragraph habits, emotional expression

Step 4: Fetch trending content ✅
├─ Search: [Topic] related trends
├─ Analyze: Viral article angles
└─ Extract: Borrowable viral elements

Step 5: Start creation ✅
├─ Confirm: Article type and topic
├─ Generate: Title options (4 types)
├─ Build: Article outline
├─ Create: Content (strictly follow style)
└─ Optimize: Language and viral elements

Step 6: Quality check ✅
├─ Check: Persona consistency
├─ Check: Style consistency
├─ Check: Viral elements complete
└─ Output: Final article
```

---

## Phase 2: Topic & Title

### Topic Analysis
- Based on trending content, analyze angles
- Combine user positioning, determine differentiated view
- Evaluate viral potential

### Title Generation
Generate 4 types × 3-5 options:

```
【Title Options】
Type: Contrast
Title: [Title text]
Highlight: [Why it's good]
Rating: ⭐⭐⭐⭐⭐
```

---

## Phase 3: Structure Building

### Choose Template
Based on article type:
- Tool Introduction → viral-writing-method.md
- Method Tutorial → viral-writing-method.md
- Deep Thinking → deep-cognition-writing.md

### Generate Outline
- Section word counts
- Image placement suggestions
- Quote insertion points
- Interaction guide points

---

## Phase 4: Content Creation

### Key Requirements
✅ Author's voice (first-person "I" if configured)
✅ Authenticity: Share踩坑 experiences
✅ Emotional expression (match persona)
✅ Moderate self-deprecation (if configured)
✅ Empower readers: "Even I can do this"
✅ **CRITICAL**: Reduce bullet-point output

### Learn Style Features
Reference existing articles:
- Opening hook style
- Paragraph length (≤5 lines)
- Transition style
- Professional term frequency

---

## Phase 5: Optimization & Check

### Content Optimization
- Check language matches persona
- Check paragraph length appropriate
- Check emotional expression到位
- Optimize unattractive parts

### Remove AI Characteristics
- Remove mechanical connectors
- Remove AI high-frequency words
- Add human details
- Adjust rhythm and flow

### Viral Element Check
```
□ Title has contrast/number/surprise
□ Hook grabs in 3 seconds
□ Image every 300 words
□ Subheading every 500-800 words
□ Emotional expression (match style)
□ Shareable quotes
□ Interaction guide
□ Call to action
□ Solves real pain point
□ Has actionable method
```

### Persona Consistency Check
- Compare with learned article style
- Compare with author-config.md
- Check missing elements
- Ensure matches author persona

---

## Special Scenarios

### Quick Trending Follow-up
```
User: Urgent trending follow-up, 1 hour deadline

AI:
1. Simplify learning (skip if already familiar with style)
2. Quick fetch trending content
3. Use existing template quick generate
4. Focus optimize opening and title
5. Simplify check (only key items)
```

### Deep Analysis Article
```
User: Deep thinking article, needs professional perspective

AI:
1. Focus use references/deep-cognition-writing.md framework
2. Search professional background materials
3. Strengthen history review and professional analysis
4. Add philosophical升华 content
5. Design open ending for discussion
```

### Tool/Product Update Announcement
```
User: Tool new version release article

AI:
1. Learn existing update article style
2. Emphasize iteration process and data (XX days, XX stars)
3. Highlight user feedback driving improvements
4. Compare version differences (images)
5. Empowerment ending
```

### Style Adaptation
```
Professional:
- Add data and references
- Reduce colloquial expressions
- Strengthen professional analysis
- Moderate professional terms

Friendly:
- First-person perspective
- Emotional expression
- Moderate self-deprecation
- Colloquial expressions

Humorous:
- Add humor elements
- Use vivid metaphors
- Strengthen调侃 and吐槽

Minimalist:
- Reduce铺垫
- Refine expression
- Strengthen practicality
- Delete redundant modifiers
```

---

## Success Criteria

After completion, should achieve:

```
✅ Persona clear: Reads like author wrote it
✅ Style unified: Consistent with existing articles
✅ Pain point precise: Hits real reader needs
✅ Method practical: Has actionable steps
✅ Elements complete: Title, opening, content, interaction, quotes
✅ Timeliness: Combines trending or industry trends
✅ Spread potential: Has shareable quotes
✅ Empowerment strong: Reader feels "I can too"
✅ Natural flowing: No obvious AI feel
```

---

## First-Time User Handling

If user hasn't filled author-config.md:

**Friendly guide**:
```
"To make article match your style, I need to know:
- Your pen name?
- Your main writing field?
- Preferred style (Friendly/Professional/Humorous/Minimalist)?
- Can you provide 1-2 representative articles?"
```

**Or use default config**: Warn that results may be less personalized.