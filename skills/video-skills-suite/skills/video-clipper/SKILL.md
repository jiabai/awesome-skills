---
name: video-clipper
description: 从长视频（直播回放、会议录像、播客）中批量生成短视频切片。基于转写文稿精确定位观点边界，自动去除静音卡顿和口吃，输出音画同步的短视频。适用于：直播切片、会议精华提取、短视频二创、播客精彩片段。
---

# Video Clipper — 长视频智能切片

## 依赖

- **ffmpeg / ffprobe**: 视频切片、静音检测、trim+concat（系统已安装）
- **whisperx venv**: `scripts/.venv-whisperx/`（用于二次质检）
- **转写 JSON**: 需要 `video-to-text` skill 的带时间戳 JSON 输出（用于精确定位和口吃检测）
- **脚本集**（均在 `workspace/scripts/`）：
  - `batch-clip-v4.sh` — 主批量切片脚本（去静音 + 去口吃 + crossfade）
  - `smart-silence.py` — 智能静音处理（长静音删除 / 短静音压缩）
  - `stutter-detect.py` — 口吃检测（基于原始转写 JSON）
  - `clip-postcheck.py` — WhisperX 二次扫描 + 自动修复残留口吃
  - `batch-postcheck.sh` — 批量二次质检脚本
  - `iterate-until-clean.py` — 单条 clip 反复迭代（转写→检测→修复→再转写）直到零问题

## 完整四阶段流程

```
Phase 1: 素材准备
Phase 2: 切片点定位（观点边界）
Phase 3: 批量切片（去静音 + 去口吃 + crossfade）← batch-clip-v4.sh
Phase 4: 二次质检（WhisperX 重转写 → 残留口吃检测修复）← batch-postcheck.sh
```

---

### Phase 1: 素材准备

1. **确认输入文件**，获取总时长
2. **CJK 文件名处理**：含中文则建英文 symlink，后台 nohup 命令需用英文路径
   ```bash
   ln -sf "/path/to/直播回放.mp4" /tmp/livestream-input.mp4
   ```
3. **确认转写 JSON 存在**：`video-to-text` skill 的输出（含 word_segments 级时间戳）

---

### Phase 2: 切片点定位

**最关键的一步——不能凭直觉猜时间戳，必须基于转写文字精确定位。**

#### 2.1 候选话题来源
- 优先用 `insight-extractor` 输出中的金句和时间戳
- 或人工给出话题名，再用转写 JSON 定位

#### 2.2 用转写 JSON 校准边界

```python
import json

with open("transcript.json") as f:
    data = json.load(f)

for seg in data["segments"]:
    if START <= seg["start"] <= END:
        m, s = divmod(int(seg["start"]), 60)
        h, m = divmod(m, 60)
        ts = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        print(f"  [{ts}] {seg['text'].strip()}")
```

#### 2.3 精确边界原则

1. **观点完整**：从引入/铺垫 → 结论/反应，不截断
2. **前不带冗余**：切掉闲聊、过渡、无关内容
3. **后不拖尾**：观点讲完即切，不带下一话题开头
4. **扩展确认**：向前后各扩 2-3 分钟，确认边界无误

#### 2.4 时间戳格式

- < 60 分钟：`MM:SS`（如 `41:40`）
- ≥ 60 分钟：`H:MM:SS`（如 `1:50:08`）

---

### Phase 3: 批量切片（主流程）

使用 `scripts/batch-clip-v4.sh`。

#### 三层清理管道

1. **精确粗切** (`ffmpeg -ss ... -to ...`)：从原视频按时间段切出原始片段
2. **静音 + 口吃跳切** (`smart-silence.py` + `stutter-detect.py`)：
   - 长静音（≥0.5s）：完全跳过
   - 短静音（0.25-0.5s）：压缩到 0.12s（保留呼吸感）
   - 口吃（重复词/短语）：基于原始转写 JSON 检测，跳过第一次出现
3. **filter_complex trim+concat + crossfade**：
   - 视频：plain concat（避免视觉闪烁）
   - 音频：链式 `acrossfade`（每拼接点 20ms，消除"咔哒"感）

#### ⚠️ 关键约束

- **不能用 `select/aselect`**：长视频音视频时间基不同，会产生漂移
- **必须用 `nohup` 后台运行**：14 条 × 每条约 2-3 分钟，总耗时 ~20-30 分钟
- **macOS zsh 无 `mapfile`**：用 `while IFS= read -r line` 替代
- **时间戳 >59:59 时**：必须用 `H:MM:SS` 格式（`109:30` → `1:49:30`）

#### 运行方式

```bash
# 确认 symlink 存在
ln -sf "/path/to/原始视频.mp4" /tmp/livestream-input.mp4

# 后台运行
nohup bash workspace/scripts/batch-clip-v4.sh > /tmp/batch-clip-v4.log 2>&1 &

# 监控
tail -f /tmp/batch-clip-v4.log
```

#### 修改切片列表

编辑 `batch-clip-v4.sh` 中的 `clips=()` 数组，格式为 `"start|end|name"`：

```bash
clips=(
  "30:16|31:58|01-胆子够大"
  "1:50:08|1:52:20|02-AI后背发凉"
  ...
)
```

---

### Phase 4: 二次质检（WhisperX post-check）

**为什么需要二次质检？**

口吃检测基于原始转写 JSON，但原始转写有时会漏掉某些口吃（没有转写出来）。  
编辑后的 clip 可能仍含残留口吃，需要用 WhisperX **重新转写 clip 本身**，再做检测。

```
原始转写 JSON → stutter-detect.py → 跳切 → clip
                                              ↓
                                   clip-postcheck.py（WhisperX 重转写）
                                              ↓
                                   发现残留 → 自动二次修复
```

#### 运行 post-check

```bash
# 激活 whisperx venv
source scripts/.venv-whisperx/bin/activate

# 单条检测（不修复，只报告）
python3 scripts/clip-postcheck.py clips/02-AI后背发凉.mp4

# 单条检测 + 自动修复（-fixed.mp4 会替换原文件）
python3 scripts/clip-postcheck.py clips/02-AI后背发凉.mp4 --fix

# 批量检测 + 自动修复全部 clips/
bash scripts/batch-postcheck.sh
```

#### clip-postcheck.py 检测项

1. **单字重复**（AA 型）：运运、对对对 → 保留最后一个
2. **短语重复**（ngram 2-4 字）：就是就是、当时的当时 → 保留后一个
3. **低置信度簇**：3 个以上 score<0.05 的连续字，且与后文重叠 → 标记为跳切残留

**有效叠词白名单（不误判）**：试试、看看、谢谢、刚刚、常常、爷爷、妈妈 等 100+ 词

#### 单条反复迭代（最严格模式）

对质量要求极高的 clip，用 `iterate-until-clean.py`：

```bash
source scripts/.venv-whisperx/bin/activate
python3 scripts/iterate-until-clean.py clips/02-AI后背发凉.mp4
```

每轮：WhisperX 转写 → 检测 → 修复 → 替换 → 再转写验证。  
最多 5 轮，通常 1-2 轮收敛。

#### 每条耗时

WhisperX 转写 1 分钟 clip ≈ 60-90 秒（CPU）。  
14 条全部 post-check ≈ 15-20 分钟。**务必后台运行**。

---

### Phase 5: 最终检查

```bash
for f in clips/*.mp4; do
  [ -f "$f" ] || continue
  sz=$(du -h "$f" | cut -f1)
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
  min=$((dur/60)); sec=$((dur%60))
  printf "%-35s %5s  %d:%02d\n" "$(basename "$f")" "$sz" "$min" "$sec"
done
```

---

## 输出规格

- **位置**：`workspace/clips/<编号>-<名称>.mp4`
- **命名**：`01-胆子够大.mp4`、`02-AI后背发凉.mp4`
- **编码**：H.264 CRF23 + AAC 128kbps + faststart
- **大小**：3-25MB/条（取决于时长）
- **压缩率**：比原始切片平均短 20-30%（静音 + 口吃 + crossfade）

---

## 与其他 Skill 的衔接

```
video-to-text       →  转写 JSON（时间戳 + 口吃检测来源）
    ↓
insight-extractor   →  观点摘要（切片候选来源）
    ↓
video-clipper       →  短视频切片（本 skill）
    ├── Phase 3: batch-clip-v4.sh（去静音 + 去口吃 + crossfade）
    └── Phase 4: batch-postcheck.sh（WhisperX 二次质检）
    ↓
（人工 / 剪映加字幕）→  发布短视频平台
```

---

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| 音画不同步 | `select/aselect` 滤镜音视频时间基不同 | 改用 `trim/atrim + concat` |
| 时间戳不认 | `109:30` 格式超过 59:59 | 改为 `H:MM:SS`（`1:49:30`）|
| macOS zsh 报错 | `mapfile` 不存在 | 用 `while IFS= read -r line` |
| 中文文件名乱码 | nohup 后台 + CJK 路径 | 建英文 symlink |
| exec session 超时 | 15-30 分钟任务被 SIGTERM | 所有批量任务必须 `nohup` |
| 残留口吃 | 原始转写漏识别，stutter-detect 抓不到 | Phase 4 WhisperX post-check |
| 跳切"咔哒"声 | trim+concat 拼接点音频突变 | 每拼接点加 20ms `acrossfade` |
| 口吃误判叠词 | 试试/看看/谢谢 被当作重复 | `VALID_REDUP` 白名单过滤 |

---

## 性能参考

| 切片数 | 总原始时长 | Phase 3 耗时 | Phase 4 耗时 |
|--------|-----------|-------------|-------------|
| 6 条 | ~15 min | ~8 min | ~10 min |
| 14 条 | ~35 min | ~20 min | ~20 min |
| 20 条 | ~50 min | ~30 min | ~28 min |
