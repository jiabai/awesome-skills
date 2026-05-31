---
name: video-clipper
description: 从长视频（直播回放、会议录像、播客）中批量生成短视频切片。基于转写文稿和观点摘要定位片段边界，使用仓库内置 clip.sh 按时间段切片，并用 ffmpeg silencedetect 删除较长静音停顿，输出音画同步的短视频。适用于：直播切片、会议精华提取、短视频二创、播客精彩片段。
---

# Video Clipper — 长视频切片

## 依赖

- **ffmpeg / ffprobe**: 视频切片、静音检测、片段拼接
- **bash + awk**: 运行 `scripts/clip.sh` 并计算浮点时间段（Linux/macOS/Git Bash 均可）
- **转写 JSON**: 推荐使用 `video-to-text` 输出的 `transcript.json` 定位片段边界
- **脚本**: 本 skill 只依赖仓库内置的 `scripts/clip.sh`

## 能力边界

`scripts/clip.sh` 当前支持：
- 单条切片：按 `--start` / `--end` / `--name` 输出一个 mp4
- 批量切片：读取 `clips.txt`，每行一条 `start|end|name`
- 删除较长静音停顿：用 `silencedetect` 找出停顿，再拼接非静音片段
- 保持音画同步：每段从原始素材或粗切片中独立裁剪，再用 concat 拼接

本 skill 不承诺额外后处理；如果用户需要更精细的剪辑质量，请先产出这些基础切片，再交给人工剪辑或其他专门工具处理。

## 参考资料

定位片段边界前，先读取 `references/clipping-guide.md`。它解释了如何判断观点完整性、如何向前后扩展确认，以及为什么用分段裁剪后拼接来保持音画同步。

## 工作流程

```
Phase 1: 素材准备
Phase 2: 切片点定位（观点边界）
Phase 3: 生成 clips.txt
Phase 4: 运行 scripts/clip.sh
Phase 5: 最终检查
```

---

### Phase 1: 素材准备

1. 确认输入视频存在，获取总时长：
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /path/to/video.mp4
   ```
2. 如果文件名含 CJK 字符，建议建一个英文路径 symlink，方便后台命令和 shell 脚本稳定运行：
   ```bash
   ln -sf "/path/to/直播回放.mp4" /tmp/livestream-input.mp4
   ```
3. 确认 `transcript.json` 存在。优先使用 `segments` 定位句子边界；需要更细粒度时参考 `word_segments`。

---

### Phase 2: 切片点定位

切片质量主要取决于边界是否准确。不要凭直觉猜时间戳，先用转写文字校准。

#### 2.1 候选片段来源

- 优先用 `insight-extractor` 输出中的金句、争议点、行动项
- 或使用用户指定的话题名，在 `transcript.json` 中搜索相关文本
- 每条短视频只保留一个清晰主题

#### 2.2 用 `transcript.json` 校准边界

```python
import json

START = 600
END = 780

with open("transcript.json", encoding="utf-8") as f:
    data = json.load(f)

for seg in data["segments"]:
    if START <= seg["start"] <= END:
        m, s = divmod(int(seg["start"]), 60)
        h, m = divmod(m, 60)
        ts = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        print(f"[{ts}] {seg['text'].strip()}")
```

#### 2.3 边界原则

1. **观点完整**：从引入或铺垫开始，到结论或反应结束
2. **前不带冗余**：切掉寒暄、闲聊、无关过渡
3. **后不拖尾**：观点讲完就停，不带下一个话题开头
4. **扩展确认**：向前后各扩 2-3 分钟查看文字，确认没有漏掉关键铺垫或结论

#### 2.4 时间戳格式

- < 60 分钟：`MM:SS`，如 `41:40`
- >= 60 分钟：`H:MM:SS`，如 `1:50:08`

`clip.sh` 会把 `MM:SS` 自动转换为 `H:MM:SS`。

---

### Phase 3: 生成 `clips.txt`

在项目目录中创建切片列表：

```text
30:16|31:58|01-胆子够大
1:50:08|1:52:20|02-AI后背发凉
```

格式说明：
- 第 1 列：开始时间
- 第 2 列：结束时间
- 第 3 列：输出文件名，不需要 `.mp4`

建议输出到项目目录，例如：
- `workspace/pipeline/<project-name>/clips.txt`
- `workspace/pipeline/<project-name>/clips/`

---

### Phase 4: 运行 `clip.sh`

#### 批量模式

```bash
nohup bash {video-clipper-skillDir}/scripts/clip.sh \
  --input {input-video-path-or-symlink} \
  --clips workspace/pipeline/<project-name>/clips.txt \
  --output workspace/pipeline/<project-name>/clips \
  > /tmp/video-clipper.log 2>&1 &
```

#### 单条模式

```bash
bash {video-clipper-skillDir}/scripts/clip.sh \
  --input {input-video-path-or-symlink} \
  --start 30:16 \
  --end 31:58 \
  --name "01-胆子够大" \
  --output workspace/pipeline/<project-name>/clips
```

#### 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--noise` | `-30dB` | 静音检测阈值；背景噪声大时可调到 `-25dB` |
| `--silence-dur` | `0.5` | 多长的停顿会被删除，单位秒 |
| `--no-desilence` | false | 只粗切，不删除静音停顿 |

批量任务建议后台运行，并用日志观察进度：

```bash
tail -f /tmp/video-clipper.log
```

---

### Phase 5: 最终检查

```bash
for f in workspace/pipeline/<project-name>/clips/*.mp4; do
  [ -f "$f" ] || continue
  sz=$(du -h "$f" | cut -f1)
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
  min=$((dur/60)); sec=$((dur%60))
  printf "%-35s %5s  %d:%02d\n" "$(basename "$f")" "$sz" "$min" "$sec"
done
```

检查重点：
- 输出文件是否存在且非空
- 时长是否接近预期
- 文件名是否按编号排序
- 需要抽查播放，确认开头和结尾没有截断观点

---

## 输出规格

- **位置**：`workspace/pipeline/<project-name>/clips/`
- **命名**：`01-主题.mp4`、`02-主题.mp4`
- **编码**：H.264 CRF23 + AAC 128kbps + faststart
- **大小**：取决于片段时长和画面复杂度
- **内容**：按时间段切出的短视频，默认删除较长静音停顿

---

## 与其他 Skill 的衔接

```
video-to-text       →  transcript.json（定位时间戳）
    ↓
insight-extractor   →  insights.md（候选主题和金句）
    ↓
video-clipper       →  clips.txt + clips/*.mp4
    ↓
人工 / 剪辑工具      →  字幕、封面、竖屏适配、发布
```

---

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| 音画不同步 | 对长视频直接做复杂过滤容易产生时间基问题 | 使用独立片段裁剪后 concat 拼接 |
| 时间戳不认 | `109:30` 格式超过 59:59 | 改为 `H:MM:SS`（`1:49:30`） |
| macOS zsh 报错 | 某些 shell 特性不可用 | 用 bash 运行脚本 |
| Windows `bash` 提示未安装 Linux | 系统自带 `bash.exe` 是 WSL 启动器 | 使用 Git Bash 的 `bash.exe`，或安装 WSL 发行版 |
| 中文文件名乱码 | 后台命令和 CJK 路径组合不稳定 | 建英文 symlink |
| exec session 超时 | 批量视频任务耗时较久 | 用 `nohup` 后台运行 |
| 停顿删得太多 | 静音阈值或时长过于激进 | 调低 `--noise` 或调大 `--silence-dur` |

---

## 性能参考

| 切片数 | 总原始时长 | 预计耗时 |
|--------|-----------|----------|
| 6 条 | ~15 min | ~5-10 min |
| 14 条 | ~35 min | ~15-25 min |
| 20 条 | ~50 min | ~25-35 min |
