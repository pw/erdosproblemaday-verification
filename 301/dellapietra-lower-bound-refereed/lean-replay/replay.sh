#!/bin/bash
# Outside replay of Della Pietra's Lean proof of Erdos301Conclusion (erdosproblemaday.com, 2026-11-23).
set -u
Q=$HOME/MathDyad/erdos301/dellapietra; L=$Q/logs; cd $Q/build
export PATH="$HOME/.elan/bin:$PATH"; export LEAN_NUM_THREADS=4
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
( while true; do
    avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    for p in $(pgrep -x lean; pgrep -x leanchecker; pgrep -x lean4checker); do
      cwd=$(readlink /proc/$p/cwd 2>/dev/null); case "$cwd" in $Q/*) ;; *) continue;; esac
      r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); r=${r:-0}
      if [ "$r" -gt 11534336 ] || [ "$avail" -lt 10485760 ]; then echo "$(date -u +%FT%TZ) WATCHDOG kill $p rss_kb=$r avail_kb=$avail" >> $L/watchdog.log; kill $p; fi
    done; sleep 2; done ) & WD=$!
trap "kill $WD 2>/dev/null" EXIT
stamp start
( time lake exe cache get ) > $L/cache_get.log 2>&1; stamp "cache_get exit=$?"
lean --version > $L/env.txt; lake --version >> $L/env.txt; git -C .lake/packages/mathlib rev-parse HEAD >> $L/env.txt; git -C .lake/packages/erdos327 rev-parse HEAD >> $L/env.txt
( time nice -n 10 lake build Erdos301 ) > $L/build.log 2>&1; rc=$?; stamp "build exit=$rc"
[ $rc -ne 0 ] && exit $rc
( time lake env lean Erdos301/Axioms.lean ) > $L/axioms_theirs.log 2>&1; stamp "axioms_theirs exit=$?"
stamp done
