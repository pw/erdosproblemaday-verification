#!/bin/bash
# Kernel re-check of Quana's proof from scratch: lean4checker v4.27.0 (built 2026-11-20 from leanprover/lean4checker tag v4.27.0,
# because the v4.27.0 toolchain ships no leanchecker binary; the 11-19 run's leanchecker step exited 1 on that).
set -u
Q=$HOME/MathDyad/erdos1186/quana; L=$Q/logs; cd $Q/src/lean
export PATH="$HOME/.elan/bin:$PATH"
CHK=$HOME/MathDyad/tools/lean4checker-v4.27.0/.lake/build/bin/lean4checker
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
( while true; do
    avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    for p in $(pgrep -x lean4checker); do
      r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); r=${r:-0}
      if [ "$r" -gt 20971520 ] || [ "$avail" -lt 10485760 ]; then echo "$(date -u +%FT%TZ) WATCHDOG kill $p rss_kb=$r avail_kb=$avail" >> $L/watchdog.log; kill $p; fi
    done; sleep 5; done ) & WD=$!
trap "kill $WD 2>/dev/null" EXIT
git -C $HOME/MathDyad/tools/lean4checker-v4.27.0 rev-parse HEAD > $L/lean4checker_version.txt
stamp "lean4checker_control_start (Init.Prelude, positive control)"
( time nice -n 10 lake env $CHK --fresh Init.Prelude ) > $L/lean4checker_control.log 2>&1; stamp "lean4checker_control exit=$?"
stamp "lean4checker_fresh_start (v4.27.0 build, module Erdos.Proofs.P1186ExFinal)"
( time nice -n 10 lake env $CHK --fresh Erdos.Proofs.P1186ExFinal ) > $L/lean4checker_fresh.log 2>&1; stamp "lean4checker_fresh exit=$?"
stamp checker_done
