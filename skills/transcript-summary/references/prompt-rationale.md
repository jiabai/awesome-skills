# 提示词设计原理与多语言适配

本技能的提示词源自 FrameQ 桌面客户端 `worker/frameq_worker/insightflow/prompt.py` 的 `build_mindmap_prompt` 与 `build_summary_prompt`，经多轮产物约束验证。SKILL.md 中的中文版为简体中文固化版；本文件记录设计原理与多语言适配方法，供需要深入或切换语言时查阅。

## 核心设计原则

### 1. Source-grounded（忠实原文）

两步提示词均明确要求"不要添加文字稿中不存在的事实、数字、人物或结论"。这是整个提炼流程的底线：产物是对原文的结构化浓缩，不是再创作。任何脑补都会破坏提炼的可信度。

### 2. 脑图与总结的职责分离

- 脑图：只组织逻辑结构（主线/分支/层级），不引入事实。
- 总结：以文字稿为事实来源，脑图仅辅助逻辑组织。

第二步提示词明确："思维导图可组织逻辑，但不增加任何事实。"这防止脑图在生成中"自由发挥"出的事实，被总结当作可信来源二次传播，形成事实漂移。

### 3. 内容偏好与去水

优先提取：观点、方法、因果、步骤、冲突、结论、可迁移经验。
剔除：寒暄、重复、填充词、空洞过渡。

口语转写稿含大量"嗯""那个""然后"等填充与寒暄，本原则确保提炼结果信息密度高、可读性强。

### 4. 产物格式闭集

脑图与总结的输出格式是严格闭集：

- 脑图：仅 Mermaid 源码，首行 `mindmap`，无围栏无解释。
- 总结：仅 Markdown 正文，首标题 `# 要点总结`，次节 `## 总览`，随后 2 到 6 个话题小节。

闭集约束便于下游程序解析与界面直接渲染，也便于自动化质检。

### 5. 节点简短

脑图节点标签要简短，禁止段落级节点。思维导图是结构可视化，不是文本搬运；段落级节点会破坏可读性，背离"导图"本义。

## 多语言适配

SKILL.md 中为简体中文固化版。原始 FrameQ 实现通过 `output_language_semantics()` 注入不同语言的 `prompt_instruction` 与示例值，支持 zh-CN / zh-TW / en-US 三种输出语言。

### 切换输出语言

若需繁体中文或英文输出，把提示词中的"输出语言要求"段、Mermaid 示例节点、总结标题替换为对应值。

**繁体中文（zh-TW）**

- 输出语言要求："所有用户可见的生成值、Markdown 标题与正文、Mermaid 节点标签均使用繁体中文（台湾），不得转换为简体。不要改动 JSON 键名、产物 schema 或 Mermaid 语法。"
- Mermaid 示例节点：`root((核心主題))` / `主要分支` / `關鍵要點`
- 总结标题：`# 重點摘要` / `## 總覽`

**英文（en-US）**

- 输出语言要求："Use clear US English for every user-visible generated value, Markdown heading/body, and Mermaid node label. Do not change JSON keys, artifact schemas, or Mermaid syntax."
- Mermaid 示例节点：`root((Core Topic))` / `Main Branch` / `Key Point`
- 总结标题：`# Key Summary` / `## Overview`

### 指令语言的选择

原始 FrameQ 提示词用英文指令加 `prompt_instruction` 强制输出语言，优点是 LLM 指令遵循更稳定。本技能 SKILL.md 固化为中文指令版以贴合中文使用场景；现代主流 LLM 对中文指令遵循已足够。

若发现某些模型对英文指令遵循更稳（如格式约束被忽略），可改回英文指令版：把"角色""任务""生成规则"等段落标题与指令改回英文，仅保留"输出语言要求"段强制中文输出。

## 原始实现参照

如需对照原始英文指令版与完整实现，对应 FrameQ 源码位置：

- `build_mindmap_prompt`：`worker/frameq_worker/insightflow/prompt.py`
- `build_summary_prompt`：同文件
- 输出语言语义表：`worker/frameq_worker/output_language.py`（`OUTPUT_LANGUAGE_SEMANTICS` 字典）
- 调用编排：`worker/frameq_worker/insightflow/summary.py`（`generate_summary_from_markdown`：先脑图后总结）

原始实现中，脑图与总结各调用一次 LLM，脑图源码经 `normalize_mermaid_mindmap` 规整（剥离围栏、保证首行 `mindmap`）后再喂给总结提示词。
