---
name: video-to-text
description: 视频/音频转文字稿。从视频文件中提取音频，用 whisperX 进行语音识别、时间戳对齐和说话人分离，输出带时间戳和说话人标签的文字稿。适用于：直播回放转写、会议录音转文字、播客转录、任何视频/音频转文稿的场景。
---

# Video to Text — 视频/音频转文字稿

## 依赖

- **ffmpeg**: 从视频中提取音频（系统已安装）
- **whisperX**: 语音识别 + 对齐 + 说话人分离（`pip install whisperx`）
- **HF_TOKEN**: 说话人分离需要 HuggingFace token（环境变量 `HF_TOKEN`）

## 快速执行

对于简单的转写任务，直接运行脚本：

**Linux / macOS（nohup 后台执行）：**
```bash
nohup python3 {skillDir}/scripts/transcribe.py /path/to/video.mp4 \
  --output-dir /path/to/output \
  --output-name transcript \
  --diarize \
  > /tmp/transcribe.log 2>&1 &
```

**Windows（cmd / PowerShell 后台执行）：**
```batch
REM cmd.exe — 用 start /B 实现后台运行
start /B python {skillDir}\scripts\transcribe.py D:\path\to\video.mp4 ^
  --output-dir D:\path\to\output ^
  --output-name transcript ^
  --diarize ^
  > transcript.log 2>&1
```

```powershell
# PowerShell 7+ — 用 & 后台操作符
python {skillDir}\scripts\transcribe.py D:\path\to\video.mp4 `
  --output-dir D:\path\to\output `
  --output-name transcript `
  --diarize *> transcript.log &
```

**必须后台执行**——长音频（>30 min）转写时间可达数十分钟到数小时，exec session 会超时。Linux/macOS 用 `nohup`，Windows cmd 用 `start /B`，PowerShell 7+ 用 `&` 后台操作符。

## 完整流程

### Step 1: 预处理

1. 确认输入文件存在，获取时长（`ffprobe` 跨平台通用）：`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>`
2. 若文件名含 CJK 字符，创建 symlink 避免编码问题：
   - **Linux/macOS**：`ln -sf "<原路径>" /tmp/input-video.mp4`
   - **Windows cmd（管理员）**：`mklink C:\tmp\input-video.mp4 "<原路径>"`
   - **Windows PowerShell（管理员）**：`New-Item -ItemType SymbolicLink -Path C:\tmp\input-video.mp4 -Target "<原路径>"`
3. 脚本会自动判断：音频文件直接转写，视频文件先提取音频为 16kHz mono WAV

### Step 2: 转写

运行 `scripts/transcribe.py`，关键参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model` | large-v3 | Whisper 模型，large-v3 最准但最慢 |
| `--language` | zh | 语言代码 |
| `--diarize` | off | 启用说话人分离（需 HF_TOKEN） |
| `--device` | cpu | cpu 或 cuda |
| `--batch-size` | 8 | 批次大小，内存不够可降低 |

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
- **`<name>.txt`**: 人类可读文稿，按说话人分段，带 `[MM:SS]` 时间戳
- **`<name>.json`**: 完整 whisperX 输出，含 word-level 时间戳

### 存档

转写完成后，将 `.txt` 文件复制到 `workspace/transcripts/` 目录：
- 命名约定：`<原始文件名>.txt`（如 `直播回放-02月26日.txt`）

## 性能参考

| 音频时长 | 模型 | 设备 | 预计耗时 |
|----------|------|------|----------|
| 30 min | large-v3 | CPU (M-series) | ~15 min |
| 1 hour | large-v3 | CPU (M-series) | ~30 min |
| 2 hours | large-v3 | CPU (M-series) | ~60 min |

## 注意事项

- CJK 文件名在 shell 中容易乱码，始终用 symlink（或 Windows 上的 mklink）改用纯英文路径
  - Linux/macOS：`ln -sf "<中文路径>" /tmp/input-video.mp4`
  - Windows（管理员 cmd）：`mklink C:\tmp\input-video.mp4 "<中文路径>"`
  - Windows PowerShell 中也要注意代码页（`chcp 65001` 设为 UTF-8）
- CPU 转写时 CPU 占用 300-400%，避免同时跑其他重负载任务
- whisperX 的 diarization 依赖 pyannote，首次运行需要下载模型（~1GB）
- 如果本地有 Whisper HTTP server（端口 9876），该 skill 不使用它——直接调用 whisperX Python API 更灵活
