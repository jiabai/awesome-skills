<div align="center">

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

### skill-creator

用于创建新技能的核心工具。它提供：

- **技能创建**：从零开始创建新技能
- **技能优化**：改进现有技能的性能
- **评估运行**：测试技能在不同场景下的表现
- **基准分析**：通过方差分析衡量技能性能
- **描述优化**：优化技能触发描述的准确性

### SOUL

AI 助手的核心人格和行为框架：

- **提供真正的帮助**：跳过客套话，直接解决问题
- **有主见**：独立思考，提出专业建议
- **主动解决问题**：先尝试自己解决，再寻求帮助
- **通过能力赢得信任**：用专业能力建立可靠关系

### vibe-coding-launcher

Vibe Coding 全流程项目启动器，融合 AI 代理驱动开发方法论：

- **七阶段引导**：了解用户 → 推荐技术栈 → 生成项目结构 → 建立知识体系 → 配置架构约束 → 创建 ExecPlan → 步步指导
- **知识体系建立**：生成 AGENTS.md + docs/ 完整目录（ARCHITECTURE.md、DESIGN.md、QUALITY_SCORE.md 等）
- **架构约束配置**：分层架构 + 不变量 + 黄金原则
- **ExecPlan 工作流**：自包含、活文档、新手友好、可演示验证
- **熵管理**：技术债追踪 + 质量评分 + 知识新鲜度维护

### canvas-architect

AI 驱动的项目架构可视化引擎：

- **架构模式识别**：自动识别项目架构（分层单体、微服务、模块化等），输出置信度评分
- **潜在风险分析**：系统性识别架构风险（循环依赖、技术债务、外部依赖等）
- **Obsidian Canvas 输出**：生成 `.canvas` 格式的可视化架构图
- **执行摘要**：标准化输出格式（架构模式、置信度、风险数量）

### canvas-sequence

AI 驱动的交互序列图生成引擎：

- **动态流程分析**：分析代码的动态执行流程，而非静态架构
- **序列图生成**：生成 Obsidian Canvas 格式的时序图
- **调用链可视化**：可视化请求从入口到数据库的完整流程
- **适用场景**：API 调用链、请求生命周期、模块间调用顺序

### article-diagram

为 Markdown 文章自动生成专业 SVG 插图：

- **流程图**：3 步骤以上的顺序操作
- **架构图**：3 组件以上的系统关系
- **时序图**：有时间先后顺序的交互
- **对比图**：两方或多方案对比
- **核心功能**：提取 know-how 列表 → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown
- **附加功能**：支持 SVG 转 JPEG 格式

### wechat-article-writer

微信公众号文章自动化写作助手：

- **爆款标题生成**：4 类标题模板（痛点型、反差型、悬念型、价值型）
- **风格学习**：根据作者配置文件学习写作风格
- **热点分析**：结合 baidu-search 获取热点话题
- **去 AI 化处理**：去除 AI 写作痕迹，保持自然表达
- **完整工作流**：资料搜索 → 文章撰写 → 标题优化 → 排版建议

### baidu-search

百度 AI 搜索集成：

- **多模式搜索**：网页搜索、百度百科、秒懂百科、AI 智能生成
- **热点获取**：实时获取热门话题和资讯
- **资料检索**：支持内容研究和信息查询
- **API 集成**：基于百度千帆平台，支持 100 次/天免费额度

### cycle-investment-analysis

使用周期研究框架分析投资机会：

- **三角验证模型**：需求侧 → 供给侧 → 供需错配
- **需求侧分析**：判断需求增长类型（稳定增长/快速增长/突发需求/需求萎缩）
- **供给侧分析**：识别供给约束类型（政策限制/资源约束/技术壁垒/周期约束/政策预期）
- **供需错配验证**：通过错配强度判断矩阵评估机会
- **周期类型分类**：供给收缩型/需求激增型/双轮驱动型/政策预期型

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
├── README.md                     # 项目说明文档
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
