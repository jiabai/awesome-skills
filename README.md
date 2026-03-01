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

### 🎨 article-diagram

为 Markdown 文章自动生成专业 SVG 插图：

- **流程图**：≥3 步骤的顺序操作
- **架构图**：≥3 组件的系统关系
- **时序图**：有时间先后顺序的交互
- **对比图**：两方或多方案对比
- **核心功能**：提取 know-how 列表 → 设计插图清单 → 生成 SVG → 验证语法 → 覆盖检查 → 合并到 Markdown
- **附加功能**：支持 SVG 转 JPEG 格式（`scripts/svg-to-jpeg.js`）

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
└── article-diagram/
    ├── SKILL.md              # 文章插图生成器
    ├── package.json          # Node.js 项目配置
    ├── package-lock.json     # 依赖锁定文件
    └── scripts/
        └── svg-to-jpeg.js    # SVG 转 JPEG 工具脚本
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
- [Article Diagram](article-diagram/SKILL.md) - 文章插图生成器文档

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
