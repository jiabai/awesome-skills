<div align="center">

[**English**](README.md) | **中文**

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=42&duration=3000&pause=1000&color=9B6DFF&center=true&vCenter=true&multiline=false&repeat=true&width=600&height=70&lines=%E2%9A%A1+Awesome+Skills" alt="Awesome Skills" />

<h3>AI 助手技能集合 &middot; Vibe Coding 开发方法论</h3>

<p>一套可直接使用的技能（项目启动、架构可视化、写作、搜索等），<br/>以及 AI 代理驱动开发的完整规范体系。</p>

<p>
  <img src="https://img.shields.io/badge/Skills-10-blueviolet?style=for-the-badge" alt="Skills" />
  <img src="https://img.shields.io/badge/Conventions-3-orange?style=for-the-badge" alt="Conventions" />
  <img src="https://img.shields.io/badge/Vibe_Coding-2026-brightgreen?style=for-the-badge" alt="Vibe Coding" />
  <img src="https://img.shields.io/badge/License-Open_Source-success?style=for-the-badge" alt="License" />
</p>

</div>

---

## 目录

- [项目简介](#项目简介)
- [核心技能](#核心技能)
- [规范与资源](#规范与资源)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [最佳实践](#最佳实践)
- [贡献](#贡献)

## 项目简介

本项目包含两部分核心内容：

**技能集合**：覆盖项目启动、架构可视化、交互序列图、文章插图、公众号写作、搜索、投资分析等领域的即用型 AI 助手技能。

**Vibe Coding 方法论**：AI 代理驱动开发的完整规范体系（知识管理 + 架构约束 + 执行计划 + 熵管理），让 AI 代理高效运转。

**特点**：
- 即用型技能，覆盖多种开发场景
- Vibe Coding 全流程规范（从项目启动到持续交付）
- 架构可视化双引擎（静态架构 + 动态序列图）
- 支持技能评估和迭代优化

## 核心技能

### SOUL — 核心人格框架

AI 助手的行为操作系统，定义了 AI 应如何与人类协作。它不是工具，而是所有技能的底层基座——让 AI 从"被动回答"进化为"主动协作"。

- **跳过客套，直接解决**：不说"好问题！"，直接给答案、给代码、给方案
- **拥有独立判断**：看到糟糕的代码会说，看到优雅的设计会赞赏，不是没有个性的搜索引擎
- **先自己想办法**：读文件、查上下文、去搜索，真的卡住了再问人，目标是带着答案回来
- **用能力赢信任**：不用"可能"、"大概"糊弄，要么确定，要么说清楚不确定的部分

> 适用场景：所有 AI 对话，作为基础行为准则始终生效

---

### claude-code-skill-creator — Claude Code的技能创建与迭代工具

创建、测试、优化 AI 技能的全流程工具。从捕获意图到量化评估，覆盖技能生命周期的每个环节。

**核心工作流**：捕获意图 → 编写草稿 → 运行测试 → 评估结果 → 迭代改进 → 扩大测试规模

- **技能创建**：通过结构化访谈明确目标、触发条件、输出格式，从零生成完整 SKILL.md
- **评估运行**：在多个测试 prompt 上运行技能，收集定性和定量结果
- **基准分析**：通过方差分析衡量技能在不同场景下的稳定性
- **描述优化**：独立脚本优化 description 的触发准确性，让技能在正确的时机被激活
- **灵活适配**：可以走完整评估流程，也可以跟用户一起快速迭代

> 适用场景：想创建新技能、改进现有技能、或量化评估技能表现时使用

---

### vibe-coding-launcher — Vibe Coding 项目启动器

帮用户从零建立 AI 代理友好的项目体系，或从中断处恢复继续开发。核心理念：**Humans steer. Agents execute.** 人类引导方向，代理执行代码。

**七阶段引导流程**：

| 阶段 | 内容 |
|------|------|
| 1. 了解用户 | 3 个关键问题：做什么、技术水平、偏好 |
| 2. 推荐技术栈 | 16 种项目类型推荐表，匹配最佳技术组合 |
| 3. 生成项目结构 | 核心集/扩展集目录树，按项目类型智能调整 |
| 4. 建立知识体系 | AGENTS.md + docs/ 完整目录（ARCHITECTURE.md、DESIGN.md、QUALITY_SCORE.md 等） |
| 5. 配置架构约束 | 分层架构 + 不变量 + 黄金原则，防止代码退化 |
| 6. 创建 ExecPlan | 自包含、活文档、新手友好、可演示验证的执行计划 |
| 7. 执行指导 | 步步验证，渐进交付，每次完成一个原子提交 |

**恢复机制**：当项目已存在（目录中有 AGENTS.md）时，自动读取上下文从断点继续，而非从零开始。

**熵管理**：技术债追踪 + 质量评分 + 知识新鲜度维护，确保项目长期健康。

> 适用场景：想开发项目但不确定技术栈、需要一步步指导、想建立 AI 友好的项目结构、或说"帮我做个东西"时使用。说"继续开发/接着做"时进入恢复模式。

---

### canvas-architect — 项目架构可视化引擎

AI 驱动的架构分析工具，将项目代码转化为富有洞察力的 Obsidian Canvas 架构图。不是简单罗列文件，而是揭示设计哲学、关键数据流和潜在风险。

**三大必须输出**：

- **架构模式识别**：自动判断项目架构（分层单体、微服务、模块化等），输出置信度评分和一句话类比。例如："技能模块化架构，置信度 92%，类似乐高积木式插件系统"
- **潜在风险分析**：系统性识别至少 3 条架构风险（循环依赖、技术债务、外部依赖脆弱性、耦合热点等）
- **Obsidian Canvas 架构图**：生成 `.canvas` 格式的可视化架构图，布局均衡、色彩和谐、信息层次分明

**核心哲学**：洞察力优先于信息量 — 最小认知负荷理解复杂结构。

> 适用场景：想可视化项目结构、了解模块依赖关系、识别架构模式、生成架构洞察图时使用

---

### canvas-sequence — 交互序列图生成引擎

AI 驱动的动态流程分析工具，专注分析代码的**运行时交互流程**，生成 Obsidian Canvas 格式的序列图。与 canvas-architect 互补——后者看静态架构，前者看动态流程。

**与 canvas-architect 的区别**：

| | canvas-architect | canvas-sequence |
|---|---|---|
| 关注点 | 静态架构（模块、依赖） | 动态流程（调用链、时序） |
| 输出 | 架构图 | 序列图 |
| 问的是 | "项目长什么样？" | "请求怎么跑的？" |

**序列图元素**：生命线（参与角色）、激活条（执行周期）、消息（调用/返回/数据传递）、组合片段（循环/条件/并行）

**执行流程**：场景识别（找出核心业务场景）→ 流程追踪（跟踪完整调用链）→ Canvas 生成（时序图输出）

> 适用场景：想可视化业务流程的执行路径、查看模块间的调用顺序、理解请求从入口到数据库的完整流程时使用

---

### article-diagram — 文章插图生成器（中文版）

为 Markdown 文章自动生成专业 SVG 插图，降低读者的认知负荷。不只是"画个图"，而是先提取文章核心 know-how，再决定哪里需要可视化、用什么类型的图。

**完整工作流**：分析文章 → 提取 know-how 列表 → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown

**支持的图表类型**：

- **流程图**：3 步骤以上的顺序操作
- **架构图**：3 组件以上的系统关系
- **时序图**：有时间先后顺序的交互
- **对比图**：两方或多方案对比

**附加功能**：SVG 转 JPEG 格式导出、S 级内容可生成独立双语插画网页

> 适用场景：文章需要可视化流程/架构/概念、复杂概念需要转化为易懂图表时使用。英文版见 [article-diagram-en](article-diagram-en/SKILL.md)。

---

### wechat-article-writer — 公众号文章写作助手

AI 驱动的微信公众号写作全流程助手。从热点选题到成文发布，学习作者风格、生成爆款标题、去除 AI 痕迹，输出像人写的文章。

**五阶段工作流**：

1. **资源加载**：读取作者配置文件学习写作人设，按文章类型加载参考文件
2. **标题生成**：4 类标题 × 3-5 个选项（反差型、提问型、数字+效果型、否定+反转型），推荐最匹配人设的
3. **结构创建**：根据文章类型选择模板，包含各节字数、配图建议、要点清单
4. **内容创作**：用作者的声音写作，分享失败和挫折（真实感），适度自嘲，赋能读者
5. **去 AI 化优化**：消除"首先/其次/最后"等 AI 痕迹，用流畅段落替代条目式输出

> 适用场景：写公众号/推文、生成爆款标题、创建文章大纲、分析热点话题、去除 AI 写作痕迹时使用

---

### baidu-search — 百度 AI 搜索

基于百度千帆平台的 AI 搜索服务，作为中文信息检索的补充工具，弥补英文搜索引擎在中文内容上的覆盖不足。

**四种搜索模式**：

| 模式 | 说明 | 示例 |
|------|------|------|
| 网页搜索 | 通用搜索，支持站点过滤和时间过滤 | `--api-type web` |
| 百度百科 | 结构化的百科知识 | `--api-type baike` |
| 秒懂百科 | 视频形式的百科内容 | `--api-type miaodong_baike` |
| AI 智能生成 | AI 总结生成答案 | `--api-type ai_chat` |

**特性**：JSON 格式输出（方便 AI 解析）、结果数限制、站点过滤、时间范围过滤（周/月/半年/年）、100 次/天免费额度

> 适用场景：搜索中文信息、查询百科知识、获取最新中文资讯、查找资料时使用

---

### cycle-investment-analysis — 周期投资分析框架

使用"三角验证"模型分析周期性投资机会，从需求侧、供给侧、供需错配三个维度交叉验证，判断投资机会的确定性。

**三角验证模型**：

```
需求侧（增长态势）→ 供给侧（收缩/受限）→ 供需错配（价格上涨 → 业绩弹性）
```

**需求侧分析**：判断需求增长类型（稳定增长/快速增长/突发需求/需求萎缩），评估需求持续性和结构性变化

**供给侧分析**：识别供给约束类型（政策限制/资源约束/技术壁垒/周期约束/政策预期），评估供给收缩的确定性

**供需错配验证**：通过错配强度判断矩阵评估机会，将周期机会分为供给收缩型、需求激增型、双轮驱动型、政策预期型四类

> 适用场景：分析某行业/标的的周期属性、判断是否为周期性投资机会、评估供需错配带来的价格上涨潜力时使用

## 规范与资源

### Conventions — 开发规范

Vibe Coding 方法论的核心规范文件，定义 AI 代理驱动开发的标准流程：

| 规范 | 说明 |
|------|------|
| `VIBE-CODING-STANDARD.md` | 全局操作系统：知识管理 + 架构约束 + 开发流程 + 可观测性 |
| `ARCHITECTURE-TEMPLATE.md` | 架构文档模板：如何编写简短、稳定、定位功能的 ARCHITECTURE.md |
| `PLANS-UNIVERSAL.md` | 执行规范模板：如何编写自包含、活文档、可验证的 ExecPlan |

### Resource — 参考资源

| 目录 | 内容 |
|------|------|
| `canvas-visualization-resource/` | Canvas 可视化参考（ASCII 可视化 prompt、Canvas 模板 JSON、白板驱动开发方法论） |
| `docs-resource/` | 工程文档参考（架构文档模板、Codex ExecPlans、Agent-first 工程实践） |
| `glue-engineering-resource/` | Glue 工程参考（代码完整性审计 prompt、需求 prompt、问题描述 prompt） |

---

## 快速开始

### 使用现有技能

1. 选择需要的技能目录（如 `vibe-coding-launcher/`、`canvas-architect/`）
2. 将技能目录复制到你的 AI 助手技能路径下
3. 在对话中提及触发词即可激活技能

各 AI 工具的技能路径：
- **Claude Code**：`.claude/skills/<skill-name>/`
- **Codex / Trae**：`.trae/skills/<skill-name>/`
- **Cursor**：`.cursor/skills/<skill-name>/`

### 使用 Vibe Coding 规范

1. 阅读 `Conventions/VIBE-CODING-STANDARD.md` 了解全局方法论
2. 使用 `vibe-coding-launcher` 技能启动新项目，自动生成规范体系
3. 参考 `Conventions/ARCHITECTURE-TEMPLATE.md` 和 `Conventions/PLANS-UNIVERSAL.md` 编写架构文档和执行计划

### 创建新技能

1. 使用 `skill-creator` 技能创建新技能
2. 定义技能的目标和触发条件
3. 编写测试用例验证技能功能
4. 运行评估并迭代优化

### 技能结构

每个技能是一个独立目录，至少包含 `SKILL.md`：

```
<skill-name>/
├── SKILL.md          # 必须：技能定义和指令（YAML frontmatter + Markdown）
├── scripts/          # 可选：可执行脚本
├── references/       # 可选：按需加载的参考文档
├── assets/           # 可选：模板、图标等资源文件
└── evals/            # 可选：评估配置和测试用例
```

**SKILL.md 文件格式**：

```markdown
---
name: "skill-name"
description: "技能描述，包含功能和触发场景（这是主要的触发机制）"
---

# 技能标题

详细的技能说明和使用指南...
```

## 项目结构

```
awesome-skills/
├── README.md                     # 项目说明文档（英文）
├── README_zh.md                  # 项目说明文档（中文）
├── Conventions/                  # 开发规范
│   ├── VIBE-CODING-STANDARD.md  # Vibe Coding 全局规范
│   ├── ARCHITECTURE-TEMPLATE.md # 架构文档模板
│   └── PLANS-UNIVERSAL.md       # 执行规范模板
├── Resource/                     # 参考资源
│   ├── canvas-visualization-resource/  # Canvas 可视化参考
│   ├── docs-resource/                  # 工程文档参考
│   └── glue-engineering-resource/      # Glue 工程参考
├── SOUL/                         # 核心人格框架
│   ├── SKILL.md
│   └── evals/
├── skill-creator/                # 技能创建工具
│   └── SKILL.md
├── vibe-coding-launcher/         # Vibe Coding 项目启动器
│   ├── SKILL.md
│   └── evals/
├── canvas-architect/             # 项目架构可视化引擎
│   ├── SKILL.md
│   └── evals/
├── canvas-sequence/              # 交互序列图生成引擎
│   ├── SKILL.md
│   └── evals/
├── article-diagram/              # 文章插图生成器（中文）
│   ├── SKILL.md
│   ├── scripts/
│   └── package.json
├── article-diagram-en/           # 文章插图生成器（英文）
│   └── SKILL.md
├── wechat-article-writer/        # 公众号文章写作助手
│   ├── SKILL.md
│   ├── references/
│   └── assets/
├── baidu-search/                 # 百度 AI 搜索
│   ├── SKILL.md
│   └── scripts/
└── cycle-investment-analysis/    # 周期投资分析框架
    └── SKILL.md
```

## 最佳实践

### 技能描述编写

- 明确说明技能的功能和适用场景
- 详细描述触发场景，使用"pushy"风格提高触发率
- description 是主要的触发机制——把"何时使用"写在这里，而非正文
- 包含常见触发词和近义词，覆盖不同表达方式

### 技能开发流程

1. **定义需求**：明确技能目标和预期输出
2. **编写草稿**：创建初始技能文件（SKILL.md）
3. **测试验证**：编写测试用例并运行评估
4. **迭代优化**：根据评估结果改进技能
5. **扩展测试**：在更大规模的测试集上验证

### Vibe Coding 项目实践

- **AGENTS.md 控制在 150 行以内**：做目录地图，不做百科全书
- **文档只写稳定内容**：频繁变化的放别处，避免文档与代码脱节
- **架构约束优先声明**：无约束的代码必然退化，在 AGENTS.md 中声明不变量
- **ExecPlan 保持自包含**：所有知识都在文档内，不依赖外部资源或记忆
- **技术债小额持续偿还**：每次迭代后更新 tech-debt-tracker 和 QUALITY_SCORE

## 相关资源

### 技能文档

- [SOUL](SOUL/SKILL.md) - 核心人格框架
- [Skill Creator](skill-creator/SKILL.md) - 技能创建工具
- [Vibe Coding Launcher](vibe-coding-launcher/SKILL.md) - Vibe Coding 项目启动器
- [Canvas Architect](canvas-architect/SKILL.md) - 项目架构可视化引擎
- [Canvas Sequence](canvas-sequence/SKILL.md) - 交互序列图生成引擎
- [Article Diagram](article-diagram/SKILL.md) - 文章插图生成器（中文）
- [Article Diagram EN](article-diagram-en/SKILL.md) - 文章插图生成器（英文）
- [WeChat Article Writer](wechat-article-writer/SKILL.md) - 公众号文章写作助手
- [Baidu Search](baidu-search/SKILL.md) - 百度 AI 搜索
- [Cycle Investment Analysis](cycle-investment-analysis/SKILL.md) - 周期投资分析框架

### 开发规范

- [Vibe Coding Standard](Conventions/VIBE-CODING-STANDARD.md) - AI 代理驱动开发全局规范
- [Architecture Template](Conventions/ARCHITECTURE-TEMPLATE.md) - 架构文档生成模板
- [Plans Universal](Conventions/PLANS-UNIVERSAL.md) - 执行规范模板

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这些技能！

**贡献方式**：
1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用开源许可证。
