# Remove AI Style

> Humanize AI-generated text - make it natural, flowing, with personality

## Core Principles

### 1. Language Style
✅ **Natural flowing rhythm**
- Mix long and short sentences
- Moderate colloquial expressions ("说实话", "实际上")
- Simulate human thinking's slight redundancy

❌ **Avoid mechanical connectors**
- No "首先、其次、最后"
- No "总之、综上所述"
- No "值得注意的是、毫无疑问、一般来说"

### 2. Voice Adjustment
✅ **Active voice priority**
- "我发现" instead of "被发现"
- "这个工具让我" instead of "我被这个工具"

❌ **Passive to active**

### 3. Detail Richness
✅ **Add human elements**
- Personal insights at appropriate places
- Scene descriptions or concrete metaphors
- Moderate qualifiers ("在多数情况下", "或许")

❌ **Avoid perfectionism**
- Slightly adjust arguments to sound like personal views
- Keep moderate uncertainty

### 4. Structure Adjustment
✅ **Break template structure**
- Avoid obvious "总分总" or "并列式"
- Adjust paragraph transitions naturally
- Convert some declarative to rhetorical questions

❌ **Avoid rigid format**

### 5. Word Choice
✅ **Concrete and vivid**
- More specific verbs and nouns
- Fewer abstract words
- Replace AI high-frequency words

## AI Word Blacklist

### Connector Words
```
首先、其次、最后、总之、综上所述、因此、然而
```

### Filler Words
```
值得注意的是、应该注意的是、毫无疑问、一般来说、显而易见
```

### Structure Words
```
一方面、另一方面、除此之外、再者
```

### Other
```
进行、实现、采用、具有 (verb nominalization)
```

## Replacement Suggestions

| Original | Replacement |
|----------|-------------|
| "首先...其次...最后" | Natural paragraph transitions |
| "综上所述" | Direct summary, no connector |
| "值得注意的是" | State the point directly |
| "毫无疑问" | Delete, or use "确实" |

## Examples

### Example 1: Theory Text

**Original**:
```
首先，人工智能技术在教育领域的应用具有重要意义。其次，它可以帮助教师
减轻工作负担。最后，它能够提供个性化的学习体验。值得注意的是，这种
技术在应用过程中也存在一些挑战。
```

**Humanized (Friendly)**:
```
说起来，人工智能在教育里能做的事，比我们想象的要多得多。

它能帮老师分担不少重复性工作——批改作业、整理错题，这些机械的事交给
AI，老师就能把精力放在更重要的事情上。个性化学习也是一大亮点，每个
孩子都能得到量身定制的练习方案。

当然，事情没那么简单。技术落地时遇到的问题，或许比我们预想的还要多。
```

### Example 2: Tool Introduction

**Original**:
```
PromptFill是一款AI辅助的提示词管理工具。它支持模板功能和变量替换。
此外，该工具还具有团队协作和云端同步功能。综上所述，PromptFill能够
有效提高用户的AI创作效率。
```

**Humanized (Friendly)**:
```
用PromptFill的时候，我最大的感受是——为什么没人早点做出这种东西？

模板和变量替换这两个功能搭配起来，就像给提示词装上了乐高积木。以前
每次写提示词都要从头想，现在填几个空就能搞定。团队协作也挺有意思，
几个人可以一起维护一套提示词库，互相借鉴——这比自己闷头搞效率高多了。

效率提升？那是肯定的。但我更在意的是，它让用AI这件事变得没那么枯燥了。
```

### Example 3: Tutorial

**Original**:
```
学习ComfyUI需要掌握以下几个步骤。第一，了解节点编辑的基本概念。第二，
熟悉常用节点的功能。第三，通过实践项目提升技能。应该注意的是，学习过程
需要保持耐心和持续练习。
```

**Humanized (Friendly)**:
```
学ComfyUI这事儿，说来也简单，但刚开始确实容易懵。

节点编辑的概念你得先搞明白——就像搭积木，每个节点是一个小功能块，连
在一起就是完整的工作流。常用的节点其实就那么些，多摆弄几次也就熟了。

接下来就是动手做项目。我个人建议从简单的开始，别一上来就想搞什么大作
业，容易把自己劝退。耐心？那是必须的。但更重要的是，你得享受这个过程
的乐趣，不然很难坚持下来。
```

## Quick Checklist

After humanizing, check:

```
Language Style
  □ No "首先/其次/最后", "总之", "综上所述"
  □ No "值得注意的是", "毫无疑问", "一般来说"
  □ Sentence length varies, rhythm not monotonous
  □ Moderate colloquial expressions (match persona)

Voice
  □ Passive changed to active
  □ Used "我", "我们" pronouns

Detail
  □ Has personal insights or feelings
  □ Has scene descriptions or metaphors
  □ Has moderate qualifiers

Structure
  □ Avoided obvious "总分总", "并列式"
  □ Paragraph transitions natural
  □ Has rhetorical questions

Word Choice
  □ Verbs and nouns concrete vivid
  □ Reduced abstract words
  □ No AI high-frequency words

Persona Match
  □ Matches author-config.md (in skill root) persona tags
  □ Consistent with author's past article style
```

## Persona Adaptation

### Professional Style
- Reduce colloquial expressions like "说实话", "这事儿"
- Strengthen logical connections
- Moderate professional terms with explanations
- Objective statements, less emotional expression

### Friendly Style
- Add colloquial expressions like "说实话", "怎么说呢"
- Use vivid metaphors
- Add emotional words
- Add personal views and吐槽

### Minimalist Style
- Delete redundant expressions
- Hit core points directly
- Fewer adjectives and modifiers
- Strengthen logical structure