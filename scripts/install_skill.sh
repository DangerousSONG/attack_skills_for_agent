#!/usr/bin/env bash
# install_skill.sh — 把 attack-skill-router 装进 Claude Code 的用户级 skill 目录。
#
# 为什么需要: Claude Code 从 ~/.claude/skills/<name>/SKILL.md 发现 skill, 而本库的 SKILL.md 在
# 仓库里。历史上这里是"复制"安装, 结果副本停在旧版(不含 CLI 章节)、Claude 根本用不上路由 CLI。
# 本脚本改为"目录真实存在 + 目录内文件软链回仓库": 仓库即唯一真源, 改完立刻生效, 不会再漂移。
# (不软链整个目录: 部分实现用 readdir(withFileTypes).isDirectory() 过滤, 会跳过符号链接目录。)
#
# 用法: bash scripts/install_skill.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/.." && pwd)"
SRC="$ROOT/attack-skill-router"
DST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/attack-skill-router"
FILES=(SKILL.md reference.md MERGES.md)

# ---- 1. 定住解释器: 找一个真能 import 依赖的 python, 写进 .python-path 供 scripts/search_skills 用
if [ -n "${SKILL_PYTHON:-}" ]; then
  CANDIDATES=("$SKILL_PYTHON")
else
  CANDIDATES=("$ROOT/../PentestAgent/venv/bin/python"
              "$HOME/safe-range/PentestAgent/venv/bin/python"
              python3 python)
fi
PY=""
for c in "${CANDIDATES[@]}"; do
  case "$c" in */*) [ -x "$c" ] || continue ;; *) command -v "$c" >/dev/null 2>&1 || continue ;; esac
  if "$c" -c 'import torch, sentence_transformers, sklearn, scipy' 2>/dev/null; then
    # 只做目录层面的路径规整(去掉 /../), 绝不 readlink -f 解释器本身:
    # venv 的 bin/python 通常是符号链接, 解析掉就变成系统解释器、丢失 site-packages。
    PY="$(cd "$(dirname "$c")" && printf '%s/%s' "$(pwd -P)" "$(basename "$c")")"
    break
  fi
  echo "  跳过 $c (缺 torch/sentence_transformers/sklearn/scipy)"
done
[ -n "$PY" ] || { echo "未找到满足依赖的解释器; 请 export SKILL_PYTHON=<path> 后重跑" >&2; exit 3; }
# 复核: 规整后的路径必须与刚通过校验的解释器等价, 否则宁可失败也不要写入错的路径
"$PY" -c 'import torch, sentence_transformers, sklearn, scipy' 2>/dev/null \
  || { echo "内部错误: 规整后的解释器 $PY 反而不满足依赖" >&2; exit 3; }
echo "$PY" > "$ROOT/.python-path"
echo "[1/3] 解释器已记录: $PY -> .python-path"

# ---- 2. 建目录并软链文件(已存在的真实文件先备份, 不静默覆盖)
# SKILL.md 是唯一的硬需求(Claude Code 靠它发现 skill); 其余是配套文档, 本 SKILL.md 内已用绝对路径
# 引用它们, 所以被沙箱/权限拦下也不影响使用 —— 分级处理, 不因次要文件失败而整体退出。
mkdir -p "$DST"
link_one() {  # $1=文件名  返回 0=成功/已就绪  1=被拒
  local f="$1"
  [ -f "$SRC/$f" ] || { echo "  跳过 $f (仓库内不存在)"; return 0; }
  if [ -L "$DST/$f" ] && [ "$(readlink -f "$DST/$f")" = "$(readlink -f "$SRC/$f")" ]; then
    echo "  $f 已是正确软链"; return 0
  fi
  if [ -e "$DST/$f" ]; then
    mv "$DST/$f" "$DST/$f.bak.$(date +%Y%m%d-%H%M%S)" 2>/dev/null || { echo "  !! 无法备份 $f (权限)"; return 1; }
    echo "  已备份旧的真实文件 $f"
  fi
  ln -sfn "$SRC/$f" "$DST/$f" 2>/dev/null || { echo "  !! 无法软链 $f (权限)"; return 1; }
  echo "  已软链 $f"
}
FAILED=()
for f in "${FILES[@]}"; do link_one "$f" || FAILED+=("$f"); done
if [ -L "$DST/SKILL.md" ]; then
  echo "[2/3] SKILL.md 软链就绪 -> $DST"
  [ ${#FAILED[@]} -eq 0 ] || echo "      以下配套文件未能软链(不影响使用, SKILL.md 内已写绝对路径): ${FAILED[*]}"
else
  echo "[2/3] 失败: SKILL.md 未能软链进 $DST" >&2
  echo "      Claude Code 将无法发现本 skill。请手动执行:" >&2
  echo "        ln -sfn $SRC/SKILL.md $DST/SKILL.md" >&2
  exit 5
fi

# ---- 3. 自检: 从任意 cwd 跑一次 CLI, 证明包装脚本能自定位
chmod +x "$ROOT/scripts/search_skills"
ERR="$(mktemp)"; RC=0
OUT="$(cd /tmp && "$ROOT/scripts/search_skills" "SQL injection in login form" --top-k 1 --desc-chars 40 2>"$ERR")" || RC=$?
if [ "$RC" -ne 0 ] || ! printf '%s' "$OUT" | grep -q '"slug"'; then
  echo "自检失败 (exit=$RC)" >&2
  echo '--- stderr ---' >&2; cat "$ERR" >&2
  echo '--- stdout ---' >&2; printf '%s\n' "$OUT" >&2
  rm -f "$ERR"; exit 4
fi
rm -f "$ERR"
echo "[3/3] 自检通过(cwd=/tmp): $(printf '%s' "$OUT" | grep -o '"slug": "[^"]*"' | head -1)"
echo
echo "安装完成。在 Claude Code 里用 /attack-skill-router <任务描述>, 或直接描述渗透任务让它自动触发。"
