#!/bin/bash
# Outside replay of Quana Labs' Lean proof of erdos_1186.variants.prs_conjecture (erdosproblemaday.com, 2026-11-19).
set -u
Q=$HOME/MathDyad/erdos1186/quana; L=$Q/logs; cd $Q/src/lean
export PATH="$HOME/.elan/bin:$PATH"; export LEAN_NUM_THREADS=2
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
# watchdog: any lean/lake/leanchecker under this tree above 11 GB RSS, or MemAvailable < 10 GB -> kill the build
( while true; do
    avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    for p in $(pgrep -x lean; pgrep -x leanchecker); do
      cwd=$(readlink /proc/$p/cwd 2>/dev/null); case "$cwd" in $Q/*) ;; *) continue;; esac
      r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); r=${r:-0}
      if [ "$r" -gt 20971520 ] || [ "$avail" -lt 10485760 ]; then echo "$(date -u +%FT%TZ) WATCHDOG kill $p rss_kb=$r avail_kb=$avail" >> $L/watchdog.log; kill $p; fi
    done; sleep 2; done ) & WD=$!
trap "kill $WD 2>/dev/null" EXIT
stamp resume_start
# cache already fetched
lean --version > $L/env.txt; lake --version >> $L/env.txt; git -C .lake/packages/mathlib rev-parse HEAD >> $L/env.txt
# resume: no clean (first attempt in logs/build.log)
( time nice -n 10 lake build Erdos1186 ) > $L/build_resume.log 2>&1; rc=$?; stamp "build exit=$rc"
[ $rc -ne 0 ] && exit $rc
( time lake env lean ../verification/Headline.lean ) > $L/headline.log 2>&1; stamp "headline exit=$?"
( time lake env lean $Q/ours/axioms_ours.lean ) > $L/axioms_ours.log 2>&1; stamp "axioms_ours exit=$?"
( time nice -n 10 lake env leanchecker --fresh Erdos.Proofs.P1186ExFinal ) > $L/leanchecker_fresh.log 2>&1; stamp "leanchecker_fresh exit=$?"
stamp done
