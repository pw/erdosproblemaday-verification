#!/bin/bash
# Independent replay of jidodat/erdos684-lean @ v3-arxiv (49ee38c), erdos cron seat 2026-10-31.
# Every step logged to steps.tsv with rc + elapsed; each step gated on the previous rc.
set -u
REPO=/tmp/e684/lean/repo
OUT=$HOME/MathDyad/erdos684/replay
TC=$HOME/.elan/toolchains/leanprover--lean4---v4.32.2/bin
STEPS=$OUT/steps.tsv
mkdir -p $OUT/home $OUT/logs
echo 1000 > /proc/self/oom_score_adj 2>/dev/null   # any OOM victim is ours, never the cadicals
echo $$ > $OUT/driver.pid
run() { # name, cmd...
  local name=$1; shift; local t0=$(date +%s)
  ( cd $REPO && env -i PATH=$TC:/usr/bin:/bin HOME=$OUT/home MATHLIB_CACHE_DIR=/home/exedev/.cache/mathlib LANG=C.UTF-8 LEAN_NUM_THREADS=4 \
      nice -n 19 ionice -c2 -n7 "$@" ) > $OUT/logs/$name.log 2>&1
  local rc=$?; printf '%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$name" "$rc" "$(( $(date +%s)-t0 ))" >> $STEPS
  return $rc
}
run cache_get lake exe cache get || exit 1
run build lake build || exit 2
run audit lake env lean $OUT/Audit.lean || exit 3
run eval lake env lean $OUT/Eval.lean
echo done >> $STEPS
