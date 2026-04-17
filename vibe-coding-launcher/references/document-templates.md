# 文档生成模板

## 目录

- [AGENTS.md](#agentsmd)
- [docs/ARCHITECTURE.md](#docsarchitecturemd)
- [docs/DESIGN.md](#docsdesignmd)
- [docs/QUALITY_SCORE.md](#docsquality_scoremd)
- [docs/SECURITY.md](#docssecuritymd)
- [docs/design-docs/core-beliefs.md](#docsdesign-docscore-beliefsmd)

---

## AGENTS.md

代理的入口地图，不是百科全书。控制在 150 行以内。

模板：

```markdown
# {项目名} AGENTS.md

## 快速入口

- 架构：见 `docs/ARCHITECTURE.md`
- 设计规范：见 `docs/DESIGN.md`（如已生成）
- 核心信念：见 `docs/design-docs/core-beliefs.md`（如已生成，否则见下方）
- 执行清单：见 `tasks.md`
- 执行计划：见 `docs/exec-plans/active/`（如已生成）
- 技术债：见 `docs/exec-plans/tech-debt-tracker.md`（如已生成）

## 核心信念

<3-5 条不可协商的原则>

## 开发流程

<简短描述：描述任务 → 运行代理 → 创建PR → 代理审查>

## 常用命令

<5-10 个最常用命令>
```

注意：快速入口中只列出已生成的文档路径。未生成的文档不要列出，避免死链。

## docs/ARCHITECTURE.md

规范：
- 保持简短（50-150 行）
- 只写稳定内容，不写频繁变化的
- 回答"X 在哪？"和"这段代码做什么？"
- 不链接，用符号名

必须包含：概述、代码地图（模块划分 + 模块关系）、架构不变量、层级边界、横切关注点、关键文件。

单文件项目的精简版：只写概述（项目做什么）+ 关键文件（1个）+ 架构不变量（2-3条），控制在 20 行以内。

## docs/DESIGN.md

**条件**：项目有 UI 或 API 时生成。

设计规范文档，描述项目的视觉/交互/技术设计标准。例如：
- UI 组件规范（颜色、间距、字体）
- API 设计规范（RESTful 风格、错误码格式）
- 代码风格（命名规范、注释规范）

未生成时：将最关键的设计约束（2-3条）写入 AGENTS.md 核心信念。

## docs/QUALITY_SCORE.md

**条件**：项目超过 3 个模块时生成。

质量评分追踪表，按模块评估质量：

```
| 模块 | 可维护性 | 测试覆盖 | 文档完整度 | 综合 |
|------|---------|---------|-----------|------|
| src/ui | 🟢 | 🟡 | 🟢 | 🟢 |
| src/service | 🟢 | 🟢 | 🟡 | 🟢 |
```

评分用 🟢🟡🔴 表示，随里程碑更新。

项目启动时模块不足 3 个则不生成，等模块增长后再创建。

## docs/SECURITY.md

**条件**：项目涉及网络请求、数据存储或 API Key 时生成。

安全规范，声明项目的安全约束。例如：
- 敏感数据（API Key、密码）的存储方式
- 输入验证要求
- 依赖安全扫描频率

未生成时：将关键安全约束（如"API Key 不得硬编码，使用环境变量"）写入 AGENTS.md 核心信念。

## docs/design-docs/core-beliefs.md

**条件**：项目有 3 条以上核心信念需要展开时生成。

根据用户项目类型，生成 3-5 条核心信念。例如：

```
- 数据层不依赖展示层
- 所有外部输入必须验证
- 配置集中在 Config 模块
- 错误处理使用统一 Error 类型
```

未生成时：核心信念直接写入 AGENTS.md 的"核心信念"章节（控制在 5 条以内）。
