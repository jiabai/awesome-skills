#!/bin/bash
# clip.sh — 视频切片 + 静音压缩（音画同步版）
# 用法:
#   clip.sh --input video.mp4 --clips clips.txt --output ./clips/
#   clip.sh --input video.mp4 --start 30:16 --end 31:58 --name "01-胆子够大" --output ./clips/
#
# clips.txt 格式（每行一条）:
#   30:16|31:58|01-胆子够大
#   1:50:08|1:52:20|02-AI后背发凉
#
# 静音压缩原理: silencedetect → 逐段切出非静音片段 → concat 拼接
# 每段都是从原始素材直接裁的，音画天然对齐

set -euo pipefail

# === 参数解析 ===
INPUT=""
CLIPS_FILE=""
OUTDIR="./clips"
SINGLE_START=""
SINGLE_END=""
SINGLE_NAME=""
SILENCE_NOISE="-30dB"
SILENCE_DUR="0.5"
NO_DESILENCE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --input)     INPUT="$2"; shift 2 ;;
    --clips)     CLIPS_FILE="$2"; shift 2 ;;
    --output)    OUTDIR="$2"; shift 2 ;;
    --start)     SINGLE_START="$2"; shift 2 ;;
    --end)       SINGLE_END="$2"; shift 2 ;;
    --name)      SINGLE_NAME="$2"; shift 2 ;;
    --noise)     SILENCE_NOISE="$2"; shift 2 ;;
    --silence-dur) SILENCE_DUR="$2"; shift 2 ;;
    --no-desilence) NO_DESILENCE=true; shift ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

if [ -z "$INPUT" ]; then
  echo "Error: --input required"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: Input file not found: $INPUT"
  exit 1
fi

mkdir -p "$OUTDIR"
TMPDIR="$OUTDIR/.tmp-segments"
mkdir -p "$TMPDIR"

# === 工具函数 ===

# MM:SS → H:MM:SS
to_hms() {
  local t="$1"
  if [[ "$t" == *:*:* ]]; then echo "$t"; return; fi
  local mm="${t%%:*}" ss="${t##*:}"
  printf "%d:%02d:%s" $((mm/60)) $((mm%60)) "$ss"
}

float_sub() {
  awk -v a="$1" -v b="$2" 'BEGIN { printf "%.6f", a - b }'
}

float_gt() {
  awk -v a="$1" -v b="$2" 'BEGIN { exit !(a > b) }'
}

abs_path() {
  local path="$1" dir base
  dir=$(dirname "$path")
  base=$(basename "$path")
  printf "%s/%s" "$(cd "$dir" && pwd -P)" "$base"
}

ffmpeg_concat_path() {
  local path="$1" abs
  abs=$(abs_path "$path")
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -am "$abs"
  else
    printf "%s" "$abs"
  fi
}

# 处理单条切片
process_clip() {
  local start="$1" end="$2" name="$3"
  local hms_start hms_end
  hms_start=$(to_hms "$start")
  hms_end=$(to_hms "$end")
  
  echo "  Cutting: $name ($hms_start → $hms_end)"
  
  # Step 1: 粗切
  local RAW="$TMPDIR/raw-${name}.mp4"
  ffmpeg -ss "$hms_start" -to "$hms_end" -i "$INPUT" \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 128k \
    -y "$RAW" 2>/dev/null
  
  if [ ! -f "$RAW" ] || [ ! -s "$RAW" ]; then
    echo "  ❌ Cut failed!"
    rm -f "$RAW"
    return 1
  fi
  
  if $NO_DESILENCE; then
    mv "$RAW" "$OUTDIR/${name}.mp4"
    local sz dur
    sz=$(du -h "$OUTDIR/${name}.mp4" | cut -f1)
    dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUTDIR/${name}.mp4" 2>/dev/null | cut -d. -f1)
    echo "  ✅ ${sz}, ${dur}s (原始，未压缩静音)"
    return 0
  fi
  
  # Step 2: 静音检测
  local SL="$TMPDIR/sl-${name}.txt"
  ffmpeg -i "$RAW" -af "silencedetect=noise=${SILENCE_NOISE}:d=${SILENCE_DUR}" -f null - 2>"$SL"
  
  local S_STARTS=() S_ENDS=()
  while IFS= read -r line; do
    S_STARTS+=("$line")
  done < <(grep "silence_start:" "$SL" | sed 's/.*silence_start: //' | cut -d' ' -f1)
  while IFS= read -r line; do
    S_ENDS+=("$line")
  done < <(grep "silence_end:" "$SL" | sed 's/.*silence_end: //' | cut -d' ' -f1)
  local NS=${#S_STARTS[@]}
  
  if [ "$NS" -eq 0 ]; then
    mv "$RAW" "$OUTDIR/${name}.mp4"
    rm -f "$SL"
    local sz dur
    sz=$(du -h "$OUTDIR/${name}.mp4" | cut -f1)
    dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUTDIR/${name}.mp4" 2>/dev/null | cut -d. -f1)
    echo "  ✅ ${sz}, ${dur}s (无停顿)"
    return 0
  fi
  
  # Step 3: 计算非静音段
  local DUR
  DUR=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$RAW" 2>/dev/null)
  
  local SEGS=() PREV="0"
  for i in $(seq 0 $((NS-1))); do
    local ss="${S_STARTS[$i]}" se="${S_ENDS[$i]:-$DUR}"
    local dur_seg
    dur_seg=$(float_sub "$ss" "$PREV")
    if [ -n "$dur_seg" ] && float_gt "$dur_seg" "0.05"; then
      SEGS+=("$PREV|$ss")
    fi
    PREV="$se"
  done
  local dur_seg
  dur_seg=$(float_sub "$DUR" "$PREV")
  if [ -n "$dur_seg" ] && float_gt "$dur_seg" "0.05"; then
    SEGS+=("$PREV|$DUR")
  fi
  
  local NSEG=${#SEGS[@]}
  
  if [ "$NSEG" -eq 0 ]; then
    mv "$RAW" "$OUTDIR/${name}.mp4"
    rm -f "$SL"
    echo "  ⚠️ 全是静音，直接输出"
    return 0
  fi
  
  # Step 4: 逐段切出 + concat
  local CONCAT_LIST="$TMPDIR/concat-${name}.txt"
  > "$CONCAT_LIST"
  
  for j in $(seq 0 $((NSEG-1))); do
    IFS='|' read -r seg_s seg_e <<< "${SEGS[$j]}"
    local SEG_FILE="$TMPDIR/seg-${name}-$(printf '%03d' $j).mp4"
    ffmpeg -i "$RAW" -ss "$seg_s" -to "$seg_e" \
      -c:v libx264 -preset fast -crf 23 \
      -c:a aac -b:a 128k \
      -y "$SEG_FILE" 2>/dev/null
    if [ -f "$SEG_FILE" ] && [ -s "$SEG_FILE" ]; then
      local ABS_SEG_FILE ESC_SEG_FILE
      ABS_SEG_FILE=$(ffmpeg_concat_path "$SEG_FILE")
      ESC_SEG_FILE=$(printf "%s" "$ABS_SEG_FILE" | sed "s/'/'\\\\''/g")
      echo "file '${ESC_SEG_FILE}'" >> "$CONCAT_LIST"
    fi
  done
  
  if ! ffmpeg -f concat -safe 0 -i "$CONCAT_LIST" \
    -c:v libx264 -preset fast -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart \
    -y "$OUTDIR/${name}.mp4" 2>/dev/null; then
    echo "  ⚠️ Concat 失败，用原始切片"
    cp "$RAW" "$OUTDIR/${name}.mp4"
  fi
  
  # 清理
  rm -f "$RAW" "$SL" "$CONCAT_LIST" "$TMPDIR"/seg-${name}-*.mp4
  
  if [ -f "$OUTDIR/${name}.mp4" ]; then
    local sz dur
    sz=$(du -h "$OUTDIR/${name}.mp4" | cut -f1)
    dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUTDIR/${name}.mp4" 2>/dev/null | cut -d. -f1)
    echo "  ✅ ${sz}, ${dur}s (静音段: $NS, 拼接段: $NSEG)"
  fi
}

# === 主逻辑 ===

if [ -n "$SINGLE_START" ] && [ -n "$SINGLE_END" ]; then
  # 单条模式
  name="${SINGLE_NAME:-clip}"
  process_clip "$SINGLE_START" "$SINGLE_END" "$name"
elif [ -n "$CLIPS_FILE" ]; then
  # 批量模式
  total=$(grep -c . "$CLIPS_FILE" 2>/dev/null || echo 0)
  count=0
  while IFS='|' read -r start end name; do
    # 跳过空行和注释
    [[ -z "$start" || "$start" == \#* ]] && continue
    count=$((count + 1))
    echo "[$count/$total] Processing..."
    process_clip "$start" "$end" "$name"
  done < "$CLIPS_FILE"
else
  echo "Error: Need --clips <file> or --start/--end/--name"
  exit 1
fi

rm -rf "$TMPDIR"

echo ""
echo "=== Done ==="
for f in "$OUTDIR"/*.mp4; do
  [ -f "$f" ] || continue
  sz=$(du -h "$f" | cut -f1)
  dur=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$f" 2>/dev/null | cut -d. -f1)
  min=$((dur/60)); sec=$((dur%60))
  printf "  %-35s %5s  %d:%02d\n" "$(basename "$f")" "$sz" "$min" "$sec"
done
echo "Total: $(ls "$OUTDIR"/*.mp4 2>/dev/null | wc -l | tr -d ' ') clips"
