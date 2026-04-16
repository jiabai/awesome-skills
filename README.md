# Awesome Skills

一个用于创建、管理和优化 AI 助手技能（Skills）的项目。

## 📖 目录

- [项目简介](#项目简介)
- [核心技能](#核心技能)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [最佳实践](#最佳实践)
- [贡献](#贡献)

## 项目简介

本项目提供了一套完整的技能创建和管理框架，帮助你为 AI 助手创建自定义技能，并通过评估和迭代不断优化技能性能。

**特点**：
- 🚀 快速创建自定义技能
- 📊 支持评估和基准测试
- 🔄 迭代优化技能性能
- 📝 标准化的技能格式

## 核心技能

### 🔧 skill-creator

用于创建新技能的核心工具。它提供：

- **技能创建**：从零开始创建新技能
- **技能优化**：改进现有技能的性能
- **评估运行**：测试技能在不同场景下的表现
- **基准分析**：通过方差分析衡量技能性能
- **描述优化**：优化技能触发描述的准确性

### 💎 SOUL

AI 助手的核心人格和行为框架：

- **提供真正的帮助**：跳过客套话，直接解决问题
- **有主见**：独立思考，提出专业建议
- **主动解决问题**：先尝试自己解决，再寻求帮助
- **通过能力赢得信任**：用专业能力建立可靠关系

### 🏗️ canvas-architect

AI 驱动的项目架构可视化引擎：

- **架构模式识别**：自动识别项目架构（分层单体、微服务、模块化等），输出置信度评分
- **潜在风险分析**：系统性识别架构风险（循环依赖、技术债务、外部依赖等）
- **Obsidian Canvas 输出**：生成 `.canvas` 格式的可视化架构图
- **执行摘要**：标准化输出格式（架构模式、置信度、风险数量）
- **适用场景**：项目架构理解、模块依赖分析、架构洞察报告生成

### 🎨 article-diagram

为 Markdown 文章自动生成专业 SVG 插图：

- **流程图**：≥3 步骤的顺序操作
- **架构图**：≥3 组件的系统关系
- **时序图**：有时间先后顺序的交互
- **对比图**：两方或多方案对比
- **核心功能**：提取 know-how 列表 → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown
- **附加功能**：支持 SVG 转 JPEG 格式（`scripts/svg-to-jpeg.js`）

### 📝 wechat-article-writer

微信公众号文章自动化写作助手：

- **爆款标题生成**：4 类标题模板（痛点型、反差型、悬念型、价值型）
- **风格学习**：根据作者配置文件学习写作风格
- **热点分析**：结合 baidu-search 获取热点话题
- **去 AI 化处理**：去除 AI 写作痕迹，保持自然表达
- **完整工作流**：资料搜索 → 文章撰写 → 标题优化 → 排版建议

### 🔍 baidu-search

百度 AI 搜索集成：

- **多模式搜索**：网页搜索、百度百科、秒懂百科、AI 智能生成
- **热点获取**：实时获取热门话题和资讯
- **资料检索**：支持内容研究和信息查询
- **API 集成**：基于百度千帆平台，支持 100 次/天免费额度

### 📊 cycle-investment-analysis

使用周期研究框架分析投资机会：

- **三角验证模型**：需求侧 → 供给侧 → 供需错配
- **需求侧分析**：判断需求增长类型（稳定增长/快速增长/突发需求/需求萎缩）
- **供给侧分析**：识别供给约束类型（政策限制/资源约束/技术壁垒/周期约束/政策预期）
- **供需错配验证**：通过错配强度判断矩阵评估机会
- **业绩弹性评估**：计算价格上涨对业绩的传导效应
- **周期类型分类**：供给收缩型/需求激增型/双轮驱动型/政策预期型
- **输出模板**：标的分析表 + 优先级排序

## 快速开始

### 创建新技能

1. 使用 `skill-creator` 技能创建新技能
2. 定义技能的目标和触发条件
3. 编写测试用例验证技能功能
4. 运行评估并迭代优化

### 技能结构

每个技能包含以下文件：

```
.trae/skills/<skill-name>/
└── SKILL.md
```

**SKILL.md 文件格式**：

```markdown
---
name: "skill-name"
description: "技能描述，包含功能和触发场景"
---

# 技能标题

详细的技能说明和使用指南...
```

## 项目结构

```
awesome-skills/
├── .gitignore                # Git 忽略配置
├── README.md                 # 项目说明文档
├── SOUL/
│   ├── SKILL.md              # 核心人格框架
│   └── evals/
│       └── evals.json        # SOUL 技能评估配置
├── skill-creator/
│   └── SKILL.md              # 技能创建工具
├── canvas-architect/
│   ├── SKILL.md              # 项目架构可视化引擎
│   └── evals/
│       └── evals.json        # canvas-architect 评估配置
├── article-diagram/
│   ├── SKILL.md              # 文章插图生成器（中文）
│   ├── package.json          # Node.js 项目配置
│   └── scripts/
│       └── svg-to-jpeg.js    # SVG 转 JPEG 工具脚本
├── article-diagram-en/
│   └── SKILL.md              # 文章插图生成器（英文）
├── wechat-article-writer/
│   ├── SKILL.md              # 公众号文章写作助手
│   ├── references/           # 写作方法参考
│   └── assets/               # 作者配置模板
├── baidu-search/
│   ├── SKILL.md              # 百度 AI 搜索
│   └── scripts/
│       └── search.py         # 搜索脚本
└── cycle-investment-analysis/
    └── SKILL.md              # 周期投资分析框架
```

## 最佳实践

### 技能描述编写

- ✅ 明确说明技能的功能
- ✅ 详细描述触发场景
- ✅ 使用"pushy"的描述风格以提高触发率
- ✅ 保持描述简洁（200 字符以内）

### 技能开发流程

1. **定义需求**：明确技能目标和预期输出
2. **编写草稿**：创建初始技能文件
3. **测试验证**：编写测试用例并运行评估
4. **迭代优化**：根据评估结果改进技能
5. **扩展测试**：在更大规模的测试集上验证

## 📚 相关资源

- [SOUL Skill](SOUL/SKILL.md) - 核心人格框架文档
- [Skill Creator](skill-creator/SKILL.md) - 技能创建工具文档
- [Canvas Architect](canvas-architect/SKILL.md) - 项目架构可视化引擎文档
- [Article Diagram](article-diagram/SKILL.md) - 文章插图生成器文档（中文）
- [Article Diagram EN](article-diagram-en/SKILL.md) - 文章插图生成器文档（英文）
- [WeChat Article Writer](wechat-article-writer/SKILL.md) - 公众号文章写作助手文档
- [Baidu Search](baidu-search/SKILL.md) - 百度 AI 搜索文档
- [Cycle Investment Analysis](cycle-investment-analysis/SKILL.md) - 周期投资分析框架文档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这些技能！

**贡献方式**：
1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用开源许可证。
