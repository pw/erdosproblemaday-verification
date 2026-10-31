#!/bin/bash
# leanchecker --fresh over Erdos684Lean's whole import closure (re-checks the cached Mathlib oleans too).
# Negative control first: a non-existent module must exit non-zero. No wall-time cap (10-26 lesson).
REPO=/tmp/e684/lean/repo; OUT=$HOME/MathDyad/erdos684/replay; TC=$HOME/.elan/toolchains/leanprover--lean4---v4.32.2/bin
echo 1000 > /proc/self/oom_score_adj 2>/dev/null; echo $$ > $OUT/fresh.pid
E() { ( cd $REPO && env -i PATH=$TC:/usr/bin:/bin HOME=$OUT/home LANG=C.UTF-8 nice -n 19 ionice -c2 -n7 "$@" ); }
t0=$(date +%s); E lake env leanchecker --fresh Erdos684Lean.NoSuchModule > $OUT/logs/fresh_negctl.log 2>&1; rc=$?
printf '%s\tfresh_negctl\t%s\t%s\n' "$(date -u +%FT%TZ)" $rc $(( $(date +%s)-t0 )) >> $OUT/steps.tsv
t0=$(date +%s); /usr/bin/time -v bash -c "cd $REPO && env -i PATH=$TC:/usr/bin:/bin HOME=$OUT/home LANG=C.UTF-8 nice -n 19 ionice -c2 -n7 lake env leanchecker --fresh Erdos684Lean" > $OUT/logs/fresh.log 2>&1; rc=$?
printf '%s\tfresh\t%s\t%s\n' "$(date -u +%FT%TZ)" $rc $(( $(date +%s)-t0 )) >> $OUT/steps.tsv
