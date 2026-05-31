---
name: video-skills-suite
description: 当用户需要对视频/音频内容进行端到端处理时使用。从原始视频到可发布文章的完整内容加工流水线。覆盖语音转写、观点提炼、智能切片、文章生成，支持单步调用或一键全链路。
---

# Video Skills Suite

视频内容全链路处理：一个视频进去，文字稿+观点摘要+短视频切片+可发布文章全出来。

## 链路

```
视频文件
  │
  ▼
video-to-text ──→ 文字稿 + 带时间戳 JSON
  │
  ├──────────────────┐
  ▼                  ▼
insight-extractor   video-clipper ──→ 短视频切片
  │
  ▼
article-forge ──→ 可发布文章
```

**[video-pipeline](video-pipeline/SKILL.md)** 串联以上全部流程，一键出全套。

## 子技能

| 技能 | 用途 | 前置依赖 | 输入 | 输出 |
|------|------|----------|------|------|
| [video-to-text](video-to-text/SKILL.md) | 视频/音频转文字稿 | 无 | 视频/音频文件 | 带时间戳的文字稿 + JSON（segments + word_segments） |
| [insight-extractor](insight-extractor/SKILL.md) | 长文本观点提炼 | 无 | 文字稿、会议记录、长文 | 结构化观点摘要（论点、金句、争议点、行动项） |
| [video-clipper](video-clipper/SKILL.md) | 长视频智能切片 | `video-to-text` | 视频 + 转写 JSON | 按观点切片并删除较长静音停顿的短视频 |
| [article-forge](article-forge/SKILL.md) | 素材生成文章 | `insight-extractor`（推荐） | 观点摘要 + 原始素材 | 可发布的博客/知乎/公众号文章 |
| [video-pipeline](video-pipeline/SKILL.md) | 全链路一键处理 | 无（内部串联全部） | 视频文件 | 文字稿 + 摘要 + 切片 + 文章 |

## 按场景选择

- **有一个视频，想转文字** → `video-to-text`
- **有一段长文，想提炼观点** → `insight-extractor`
- **有视频想切短视频** → `video-clipper`（依赖 `video-to-text` 的 JSON 输出）
- **有素材想写成文章** → `article-forge`
- **一个视频，全套都要** → `video-pipeline`
