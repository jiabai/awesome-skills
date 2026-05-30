---
name: video-to-text
description: 视频/音频转文字稿。从视频文件中提取音频，用 SenseVoiceSmall 进行语音识别，再用 ct-punc 恢复标点符号，输出带时间戳的文字稿。适用于：直播回放转写、会议录音转文字、播客转录、任何视频/音频转文稿的场景。
---

# Video to Text — 视频/音频转文字稿

## 依赖

- **ffmpeg**: 从视频中提取音频

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
3. 脚本会自动判断：音频文件直接转写，视频文件先提取音频为 16kHz mono WAV

### Step 2: 转写

运行 `scripts/transcribe.py`，关键参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--language` | zh | 语言代码：zh、en、yue、ja、ko、auto |
| `--device` | cpu | cpu 或 cuda |

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

脚本生成一个文件：
- **`<name>.txt`**: 带标点的纯文本

### 存档

转写完成后，将 `.txt` 文件复制到 `workspace/transcripts/` 目录：
- 命名约定：`<原始文件名>.txt`（如 `直播回放-02月26日.txt`）

## 性能参考

| 音频时长 | 模型 | 设备 | 预计耗时 |
|----------|------|------|----------|
| 30 min | SenseVoiceSmall | CPU (M-series) | ~3 min |
| 1 hour | SenseVoiceSmall | CPU (M-series) | ~6 min |
| 2 hours | SenseVoiceSmall | CPU (M-series) | ~12 min |

> SenseVoiceSmall 基于 ONNX 推理，处理 10 秒音频仅需约 70ms，比 whisperX 快 5-10 倍。

## 注意事项

- CJK 文件名在 shell 中容易乱码，始终用 symlink（或 Windows 上的 mklink）改用纯英文路径
  - Linux/macOS：`ln -sf "<中文路径>" /tmp/input-video.mp4`
  - Windows（管理员 cmd）：`mklink C:\tmp\input-video.mp4 "<中文路径>"`
  - Windows PowerShell 中也要注意代码页（`chcp 65001` 设为 UTF-8）
- SenseVoiceSmall 首次运行会自动下载模型（~400MB），确保网络畅通
- ct-punc 首次运行会自动下载模型（~50MB），与 ASR 模型分开下载
- SenseVoice 内置 ffmpeg 后端处理视频文件，视频无需手动提取音频
- 如需说话人分离，可额外使用 pyannote-audio 等工具对结果 JSON 做后处理
