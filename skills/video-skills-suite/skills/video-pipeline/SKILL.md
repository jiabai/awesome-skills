---
name: video-pipeline
description: 视频内容全链路处理。一个视频进去，文字稿+观点摘要+短视频切片+可发布文章全出来。串联 video-to-text → insight-extractor → video-clipper → article-forge 四个 skill 的完整流水线。适用于：直播回放、播客、会议录像的一站式内容加工。
user-invocable: true
metadata: {"openclaw": {"emoji": "🎬"}}
---

# Video Pipeline — 视频内容全链路

## 一句话

丢一个视频进来，出一套完整的内容产品：文字稿 + 观点摘要 + 短视频切片 + 可发布文章。

## 链路总览

```
输入: 视频文件 (直播回放/播客/会议录像)
  │
  ▼
┌─────────────────────────────────────────────┐
│ Stage 1: video-to-text                       │
│ 转写 → 带时间戳的文字稿 + JSON               │
└──────────────────┬──────────────────────────┘
                   │
        ▼
┌───────────────┐   ┌─────────────────────┐
│ Stage 2:       │   │ Stage 3:             │
│ insight-       │   │ video-clipper        │
│ extractor      │   │ 按观点切片 →         │
│ 提炼观点/金句  │   │ 删除较长静音停顿 →    │
│ /争议点        │   │ 短视频成品           │
└───────┬───────┘   └─────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│ Stage 4: article-forge                     │
│ 观点摘要 + 原始文稿 → 可发布文章            │
│ (博客/知乎/公众号)                          │
└───────────────────────────────────────────┘

输出目录: workspace/pipeline/<project-name>/
  ├── transcript.txt          # 完整文字稿
  ├── transcript.json         # 带时间戳 JSON
  ├── insights.md             # 观点摘要
  ├── clips/                  # 短视频切片
  │   ├── 01-xxx.mp4
  │   ├── 02-xxx.mp4
  │   └── ...
  └── articles/               # 生成的文章
      ├── blog-xxx.md
      └── zhihu-xxx.md
```

## 执行流程

### 输入参数

用户给出：
1. **视频文件路径**（必须）
2. **项目名**（可选，默认从文件名生成）
3. **目标产出**（可选，默认全部）：
   - `transcript` — 只要文字稿
   - `insights` — 文字稿 + 观点
   - `clips` — 文字稿 + 切片
   - `articles` — 文字稿 + 观点 + 文章
   - `all` — 全部（默认）
4. **文章平台**（可选）：blog / zhihu / wechat
5. **切片数量**（可选，默认 5-8 条）

### Stage 1: 转写（video-to-text）

1. 读取 `video-to-text` SKILL.md
2. 创建项目目录：`workspace/pipeline/<project-name>/`
3. 确定用于后续步骤的输入视频路径：优先使用原始路径；如果文件名含 CJK 字符或 shell 处理不稳定，先创建英文 symlink，并在 Stage 3 复用同一个路径。
4. 用 nohup 后台执行转写脚本：
   ```bash
   nohup python3 {video-to-text-skillDir}/scripts/transcribe.py \
     {input-video-path-or-symlink} \
     --output-dir workspace/pipeline/<project-name>/ \
     --output-name transcript \
     > /tmp/pipeline-transcribe.log 2>&1 &
   ```
5. 等待完成（用 process poll 或检查 `transcript.txt` 和 `transcript.json`）
6. 产出：`transcript.txt` + `transcript.json`

`transcript.json` 必须包含：
- `segments`: 句子/片段级时间戳
- `word_segments`: 词/字级时间戳；如果 ASR 未返回精确词级时间戳，则由 `video-to-text` 按片段时间估算
- `metadata.timestamp_source` 和 `metadata.word_timestamp_source`: 标明时间戳来源，方便判断切片精度

**⚠️ 这是最耗时的阶段**，30 分钟视频大约需要 10-20 分钟转写。后续阶段都很快。

### Stage 2: 观点提炼（insight-extractor）

1. 读取 `insight-extractor` SKILL.md
2. 输入 `transcript.txt`
3. 按 insight-extractor 流程提炼：
   - 话题边界识别
   - 核心论点提取
   - 金句标注（保留时间戳）
   - 争议点标注
4. 产出：`insights.md`

**关键：** 金句和观点的时间戳要精确，Stage 3 切片需要用。

### Stage 3: 视频切片（video-clipper）

默认等待 Stage 2 完成后再执行，因为切片候选优先来自 `insights.md`。只有用户已经明确给出切片主题或起止时间时，才可以跳过 `insights.md`，直接基于 `transcript.json` 定位。

1. 读取 `video-clipper` SKILL.md
2. 基于 `insights.md` 的观点 + `transcript.json` 的时间戳定位切片边界；如果没有 `insights.md`，必须由用户提供明确候选片段或主题
3. 生成 `clips.txt`，每行一条 `start|end|name`
4. 用 `video-clipper/scripts/clip.sh` 批量切片：
   ```bash
   nohup bash {video-clipper-skillDir}/scripts/clip.sh \
     --input {input-video-path-or-symlink} \
     --clips workspace/pipeline/<project-name>/clips.txt \
     --output workspace/pipeline/<project-name>/clips \
     > /tmp/pipeline-clip.log 2>&1 &
   ```
5. 产出：`clips/01-xxx.mp4`, `clips/02-xxx.mp4`, ...

**优化：** 优先切 insights 中标记为「金句」和「争议点」的片段——这些做短视频最有传播力。

### Stage 4: 文章生成（article-forge）

1. 读取 `article-forge` SKILL.md
2. 输入 `insights.md` + `transcript.txt`
3. 根据目标平台选择文体和风格
4. 生成文章，严格执行去 AI 味
5. 产出：`articles/blog-xxx.md` 或 `articles/zhihu-xxx.md`

**可选：** 如果用户要求发布，调用 ZhiForge 的发布流程。

## 并行策略

```
时间线:
─────────────────────────────────────────────────>
  Stage 1 (转写)     Stage 2 (观点)     Stage 3 (切片)
  ████████████████    ████████           ████████████████
                                      Stage 4 (文章)
                                      ████████
```

- 默认串行：Stage 3 依赖 Stage 2 的 `insights.md`
- Stage 4 依赖 Stage 2 的输出；如果不需要切片，可以和 Stage 3 分别启动
- 只有用户已给出切片起止时间或明确候选主题时，Stage 3 才能和 Stage 2 并行
- Stage 1 最慢，占总时间 60-70%

## 子 agent 编排

如果运行环境支持子 agent，可在 Stage 2 完成后并行执行文章生成和视频切片：

```
主 agent:
  1. 启动 Stage 1（转写，等待完成）
  2. 执行 Stage 2（观点提炼，产出 insights.md）
  3. spawn 子 agent A → Stage 3（视频切片）
  4. spawn 子 agent B → Stage 4（文章生成）
  5. 等 A/B 完成 → 汇总输出
```

## 输出汇总模板

全部完成后，向用户汇报：

```
🎬 视频内容处理完成

📹 源文件：xxx.mp4 (时长 XX:XX)
📁 项目目录：workspace/pipeline/<name>/

📝 文字稿：transcript.txt (XXXX 字)
💡 观点提炼：insights.md
   - X 个核心观点
   - X 条金句
   - X 个争议点

🎞️ 短视频切片：X 条
   - 01-xxx.mp4 (XX:XX) — 主题
   - 02-xxx.mp4 (XX:XX) — 主题
   - ...

📄 文章：X 篇
   - blog-xxx.md (XXXX 字) — 标题
   - zhihu-xxx.md (XXXX 字) — 标题
```

## 快速触发

用户说以下任何一种，触发此 skill：
- "处理这个视频"
- "视频全链路"
- "直播回放处理"
- "把这个视频变成内容"
- "video pipeline"

默认执行 `all`（全部产出），除非用户指定只要某个阶段。

## 注意事项

- Stage 1 转写**必须用 nohup 后台**，否则超时
- 文件名含中文时建议建英文 symlink，并在转写和切片阶段复用同一个输入路径
- 切片依赖 `transcript.json` 的 `segments` / `word_segments`，不是 `transcript.txt`
- 当前 `video-to-text` 不内置说话人分离；`speaker` 可能为 `null`
- 文章生成依赖 insights.md，不能跳过 Stage 2 直接到 Stage 4
- 所有产出存 `workspace/pipeline/<project-name>/`，不用 /tmp/
- 用完浏览器后必须 `browser stop`
