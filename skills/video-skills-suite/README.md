# Video Skills Suite

一套视频内容全链路处理的 Agent Skills，从一个视频文件到文字稿、观点摘要、短视频切片、可发布文章——全自动。

## 链路总览

```
视频文件
  → video-to-text     (转写+时间戳+说话人分离)
  → insight-extractor  (观点/金句/争议点提炼)  ← 与切片并行
  → video-clipper      (去静音/去口吃/短视频)   ← 与观点并行
  → article-forge      (观点+素材→文章)
```

`video-pipeline` 是编排层，串联以上四个 skill，支持并行执行和子 agent 调度。

## Skills

| Skill | 用途 | 依赖 |
|-------|------|------|
| [video-to-text](./skills/video-to-text/SKILL.md) | 视频/音频转带时间戳的文字稿 | ffmpeg, whisperX |
| [insight-extractor](./skills/insight-extractor/SKILL.md) | 从长文本提炼核心观点、金句、争议点 | LLM |
| [video-clipper](./skills/video-clipper/SKILL.md) | 长视频按观点切片，去静音去口吃 | ffmpeg, whisperX |
| [article-forge](./skills/article-forge/SKILL.md) | 从观点摘要生成可发布文章 | LLM |
| [video-pipeline](./skills/video-pipeline/SKILL.md) | 全链路编排（一键跑完） | 以上全部 |

## 适用场景

- 直播回放 → 精华切片 + 文章
- 会议录像 → 纪要 + 行动项
- 播客 → 文字版 + 短视频 highlights
- 课程录制 → 逐章文稿 + 知识点提取

## 安装

将 `skills/` 下的子目录复制或软链到你的 OpenClaw workspace 的 `skills/` 目录即可。

```bash
# Clone
git clone https://github.com/yfge/video-skills-suite.git

# Link to OpenClaw workspace
cd your-workspace/skills
for d in ../video-skills-suite/skills/*/; do
  ln -s "$d" "$(basename $d)"
done
```

## 系统依赖

- **ffmpeg / ffprobe**：视频处理
- **whisperX**：语音识别 + 时间戳对齐 + 说话人分离
- **HF_TOKEN**：说话人分离需要 HuggingFace token

## License

MIT
