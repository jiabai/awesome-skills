---
name: video-to-text
description: 视频/音频转文字稿。从视频或音频文件中用 SenseVoiceSmall 进行语音识别，再用 ct-punc 恢复标点符号，输出带时间戳的 transcript.txt 和结构化 transcript.json（segments + word_segments）。适用于：直播回放转写、会议录音转文字、播客转录、任何视频/音频转文稿的场景。
---

# Video to Text — 视频/音频转文字稿

## 依赖

- **ffmpeg / ffprobe**: 视频解码、时长探测、音频活动检测

  | 系统 | 安装方式 |
  |------|---------|
  | **macOS** | `brew install ffmpeg` |
  | **Ubuntu/Debian** | `sudo apt install ffmpeg` |
  | **Fedora/CentOS** | `sudo dnf install ffmpeg` |
  | **Arch Linux** | `sudo pacman -S ffmpeg` |
  | **Windows (winget)** | `winget install ffmpeg` |
  | **Windows (手动)** | 从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载 Windows builds，解压后将 `bin\` 目录添加到系统 `PATH` 环境变量 |

  安装后验证：`ffmpeg -version`

- **funasr**（含 SenseVoiceSmall + ct-punc）：语音识别 + 标点恢复

  ```bash
  pip install modelscope funasr
  ```

  - `modelscope`：提供 SenseVoiceSmall ASR pipeline（`iic/SenseVoiceSmall`，首次下载 ~400MB）
  - `funasr`：提供 ct-punc 标点恢复模型（首次下载 ~50MB）
  - SenseVoice 内置 ffmpeg 后端，视频文件无需手动提取音频

## 快速执行

对于简单的转写任务，直接运行脚本：

**Linux / macOS（nohup 后台执行）：**
```bash
nohup python3 {skillDir}/scripts/transcribe.py /path/to/video.mp4 \
  --output-dir /path/to/output \
  --output-name transcript \
  > /tmp/transcribe.log 2>&1 &
```

**Windows（cmd / PowerShell 后台执行）：**
```batch
REM cmd.exe — 用 start /B 实现后台运行
start /B python {skillDir}\scripts\transcribe.py D:\path\to\video.mp4 ^
  --output-dir D:\path\to\output ^
  --output-name transcript ^
  > transcript.log 2>&1
```

```powershell
# PowerShell 7+ — 用 & 后台操作符
python {skillDir}\scripts\transcribe.py D:\path\to\video.mp4 `
  --output-dir D:\path\to\output `
  --output-name transcript `
  *> transcript.log &
```

**必须后台执行**——长音频（>30 min）转写时间可达数十分钟到数小时，exec session 会超时。Linux/macOS 用 `nohup`，Windows cmd 用 `start /B`，PowerShell 7+ 用 `&` 后台操作符。

## 完整流程

### Step 1: 预处理

1. 确认输入文件存在，获取时长（`ffprobe` 跨平台通用）：`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>`
2. 若文件名含 CJK 字符，创建 symlink 避免编码问题：
   - **Linux/macOS**：`ln -sf "<原路径>" /tmp/input-video.mp4`
   - **Windows cmd（管理员）**：`mklink C:\tmp\input-video.mp4 "<原路径>"`
   - **Windows PowerShell（管理员）**：`New-Item -ItemType SymbolicLink -Path C:\tmp\input-video.mp4 -Target "<原路径>"`
3. 脚本直接把输入文件交给 SenseVoice；视频解码由后端 ffmpeg 处理

### Step 2: 转写

运行 `scripts/transcribe.py`，关键参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--language` | zh | 语言代码：zh、en、yue、ja、ko、auto |
| `--device` | cpu | cpu 或 cuda |

脚本会请求 ASR 后端返回句子级时间戳，并兼容以下结果形态：
- SenseVoice 文本中的 `<|start|><|end|>` 时间戳标签
- 结构化 `sentence_info` / `segments` / `sentences`
- 根级 `timestamp` 或 `word_segments`

如果模型只返回句子级时间戳，脚本会按片段时长估算 `word_segments`，并在 JSON 的 `metadata.word_timestamp_source` 标明来源。

如果模型没有返回任何时间戳但 `ffprobe` 能获取媒体时长，脚本会先用 ffmpeg `silencedetect` 建立语音活动区间，再把标点恢复后的文本分配到多个片段中，并将 `metadata.timestamp_source` 标为 `audio_activity_fallback`。如果音频活动检测也无法形成多段，才退回单个 `0 → duration` 粗粒度片段，并标为 `duration_fallback`。

### Step 3: 监控进度

长音频转写用定时任务监控：

**Linux/macOS（cron watcher）：**
```bash
# 创建 watcher 脚本
cat > /tmp/watch-transcribe.sh << 'EOF'
if ! kill -0 <PID> 2>/dev/null; then
  echo "done $(date)" > /tmp/transcribe-status.txt
fi
EOF
```

或通过 OpenClaw cron 每 5 分钟检查进程状态。

**Windows（PowerShell 定时检查）：**
```powershell
# 手动检查指定 PID 是否仍在运行
$pid = <PID>
if (-not (Get-Process -Id $pid -ErrorAction SilentlyContinue)) {
  "done $(Get-Date)" | Out-File C:\tmp\transcribe-status.txt
}
```

将上述脚本保存为 `C:\tmp\watch-transcribe.ps1`，然后用任务计划程序（Task Scheduler）创建每 5 分钟运行一次的触发器任务。或在 PowerShell 中直接用 `Register-ScheduledJob` 注册定时作业。

> Windows 上也可以用 `Start-Job` 在后台持续轮询：`Start-Job -Name WatchTranscribe -ScriptBlock { while (Get-Process -Id <PID> -ErrorAction SilentlyContinue) { Start-Sleep 300 } }`

### Step 4: 输出

脚本生成两个文件：
- **`<name>.txt`**: 带时间戳的文字稿，格式为 `[MM:SS.mmm - MM:SS.mmm] 文本`
- **`<name>.json`**: 结构化转写结果，供 `video-clipper` / `video-pipeline` 使用

JSON 关键字段：
- `text`: 完整文字稿
- `segments`: 句子/片段级时间戳，字段为 `id`, `start`, `end`, `text`, `speaker`
- `word_segments`: 词/字级时间戳；若 ASR 未返回精确词级时间戳，则由片段时间估算
- `metadata.timestamp_source`: 时间戳来源，如 `sensevoice_tags`, `sentence_info`, `audio_activity_fallback`, `duration_fallback`
- `metadata.word_timestamp_source`: 词级时间戳来源，如 `word_segments`, `timestamp`, `estimated_from_segments`, `estimated_from_audio_activity`

### 存档

转写完成后，将 `.txt` 和 `.json` 文件复制到 `workspace/transcripts/` 目录：
- 命名约定：`<原始文件名>.txt` / `<原始文件名>.json`（如 `直播回放-02月26日.txt`）

## 性能参考

| 音频时长 | 模型 | 设备 | 预计耗时 |
|----------|------|------|----------|
| 30 min | SenseVoiceSmall | CPU (M-series) | ~3 min |
| 1 hour | SenseVoiceSmall | CPU (M-series) | ~6 min |
| 2 hours | SenseVoiceSmall | CPU (M-series) | ~12 min |

> SenseVoiceSmall 基于 ONNX 推理，速度较快，适合长音频批量处理。

## 注意事项

- CJK 文件名在 shell 中容易乱码，始终用 symlink（或 Windows 上的 mklink）改用纯英文路径
  - Linux/macOS：`ln -sf "<中文路径>" /tmp/input-video.mp4`
  - Windows（管理员 cmd）：`mklink C:\tmp\input-video.mp4 "<中文路径>"`
  - Windows PowerShell 中也要注意代码页（`chcp 65001` 设为 UTF-8）
- SenseVoiceSmall 首次运行会自动下载模型（~400MB），确保网络畅通
- ct-punc 首次运行会自动下载模型（~50MB），与 ASR 模型分开下载
- SenseVoice 内置 ffmpeg 后端处理视频文件，视频无需手动提取音频
- 当前脚本不内置说话人分离；如需 speaker 标签，可额外使用 pyannote-audio 等工具对结果 JSON 做后处理
