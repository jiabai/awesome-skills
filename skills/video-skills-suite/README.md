# Video Skills Suite

一套视频内容全链路处理的 Agent Skills，从一个视频文件到文字稿、观点摘要、短视频切片、可发布文章——全自动。

## 链路总览

```
视频文件
  → video-to-text     (转写+时间戳 JSON)
  → insight-extractor  (观点/金句/争议点提炼)
  → video-clipper      (按观点切片/删除较长静音停顿)
  → article-forge      (观点+素材→文章)
```

`video-pipeline` 是编排层，串联以上四个 skill，支持并行执行和子 agent 调度。

## Skills

| Skill | 用途 | 依赖 |
|-------|------|------|
| [video-to-text](./skills/video-to-text/SKILL.md) | 视频/音频转带时间戳的文字稿 | ffmpeg, modelscope, funasr |
| [insight-extractor](./skills/insight-extractor/SKILL.md) | 从长文本提炼核心观点、金句、争议点 | LLM |
| [video-clipper](./skills/video-clipper/SKILL.md) | 长视频按观点切片，删除较长静音停顿 | ffmpeg, bash, awk |
| [article-forge](./skills/article-forge/SKILL.md) | 从观点摘要生成可发布文章 | LLM |
| [video-pipeline](./skills/video-pipeline/SKILL.md) | 全链路编排（一键跑完） | 以上全部 |

## 适用场景

- 直播回放 → 精华切片 + 文章
- 会议录像 → 纪要 + 行动项
- 播客 → 文字版 + 短视频 highlights
- 课程录制 → 逐章文稿 + 知识点提取

## 系统依赖

- **ffmpeg / ffprobe**：视频处理、时长探测、切片
- **modelscope + funasr**：SenseVoiceSmall 语音识别与 ct-punc 标点恢复
- **bash + awk**：运行 `video-clipper/scripts/clip.sh`（Windows 推荐 Git Bash）

## License

MIT
