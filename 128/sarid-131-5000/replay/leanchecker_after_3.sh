#!/bin/bash
# Re-runs the #128 leanchecker --fresh after the #3 replay's build step lands (second `build` row in its steps.tsv),
# so the two Mathlib-cone jobs never share the box's 62 GB at once (earlyoom killed both on 2026-10-12 19:50Z).
W=/tmp/erdos1800/lean-build; S3=/tmp/oaimath/159/lean-build/steps.tsv
while [ "$(grep -c '^build ' "$S3")" -lt 2 ]; do sleep 120; done
echo "[$(date -u +%FT%TZ)] #3 build row #2 present ($(grep '^build ' "$S3" | tail -1)); starting leanchecker --fresh Erdos128" >> "$W/leanchecker_after_3.log"
cd "$W/erdos128" || exit 10
export PATH=$HOME/.elan/toolchains/leanprover--lean4---v4.30.0/bin:$PATH
t0=$(date +%s)
setsid nice -n 19 taskset -c 8-15 lake env leanchecker --fresh Erdos128 > "$W/leanchecker_fresh.log" 2>&1
rc=$?
printf 'leanchecker_fresh\t%s\t%s\t%ss\n' "$(date -u +%FT%TZ)" "$rc" "$(( $(date +%s) - t0 ))" >> "$W/steps.tsv"
echo "[$(date -u +%FT%TZ)] leanchecker rc=$rc" >> "$W/leanchecker_after_3.log"
