# 架构约束标准

## 目录

- [分层架构](#分层架构)
- [约束写入方式](#约束写入方式)
- [黄金原则](#黄金原则)

---

## 分层架构

根据项目类型设定分层：

| 项目类型 | 分层 |
|---------|------|
| Web应用 | UI → Runtime → Service → Repo → Config → Types |
| API服务 | Routes → Service → Repo → Config → Types |
| 命令行 | CLI → Service → Config → Types |
| AI应用 | Interface → Agent → Service → Config → Types |
| 单文件/脚本 | 无需分层，在 AGENTS.md 核心信念中声明："保持单文件直到超过 200 行" |

依赖方向只能"向前"（向下），跨层依赖 → 机械禁止。

## 约束写入方式

将约束写入 AGENTS.md 或项目 linter 配置。关键：错误信息本身就是代理可读的指导。

对于简单项目，在 AGENTS.md 中声明架构不变量即可。对于复杂项目，配置 linter 规则。

## 黄金原则

写入 AGENTS.md 核心信念中的架构准则：

| 原则 | 理由 |
|------|------|
| 共享工具包优于手写 helper | 不变量集中，避免重复 |
| 边界验证优于 YOLO 猜测 | 代理不能猜测数据形状 |
| "无聊"技术优于新奇技术 | 训练集覆盖、API 稳定 |
| 自实现优于 opaque 库 | 代理能理解、修改、测试 |
