# ExecPlan 格式标准

## 目录

- [必需章节](#必需章节)
- [各章节详细规范](#各章节详细规范)
- [首个 ExecPlan 建议](#首个-execplan-建议)

---

## 必需章节

每个计划必须包含：

```markdown
# <简短、行动导向的描述>

This ExecPlan is a living document.

## Purpose / Big Picture
完成后用户能做什么新事情？如何看到它工作？

## Progress
- [ ] 待完成的步骤（每条标注时间戳）

## Concrete Steps
工作目录、完整命令行、预期输出

## Validation and Acceptance
启动方式、可观察行为、测试命令和预期结果
```

## 各章节详细规范

**Purpose / Big Picture**：用 1-2 句话回答"完成后用户能做什么新事情？"和"怎么看到它工作？"。不要写技术细节，只写用户可感知的结果。

**Progress**：列出所有待完成步骤，每条前加 `- [ ]`，完成后改为 `- [x]` 并标注时间。步骤粒度：每步应能在 10 分钟内完成。

**Concrete Steps**：每个步骤必须包含工作目录（相对于项目根目录）、完整可复制的命令行、预期输出示例。不要写"运行安装命令"，要写"运行 `pip install flask`"。

**Validation and Acceptance**：包含启动方式（如 `python app.py`）、可观察行为（如"浏览器打开 localhost:5000 看到 Hello World"）、测试命令和预期结果。

## 首个 ExecPlan 建议

推荐从最小可运行版本开始：
- Web应用：一个能访问的页面，返回 "Hello World"
- API服务：一个健康检查端点 `/health` 返回 200
- 命令行：一个能打印帮助信息的命令
- AI应用：一个能调用 API 并返回结果的脚本
- 单文件脚本：一个能运行并输出结果的 main 函数

文件保存到 `docs/exec-plans/active/`，文件名格式：`YYYY-MM-DD-简短描述.md`。
