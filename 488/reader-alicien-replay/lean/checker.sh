#!/bin/bash
# From-scratch kernel re-check of the whole import closure of Solution (Mathlib included): leanchecker --fresh (v4.35.0-rc2).
set -u
D=$HOME/MathDyad/erdos488/alicien; L=$D/logs; cd $D/src/repo
export PATH="$HOME/.elan/bin:$PATH"
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
( while true; do
    avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    for p in $(pgrep -x leanchecker); do
      cwd=$(readlink /proc/$p/cwd 2>/dev/null); case "$cwd" in $D/*) ;; *) continue;; esac
      r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); r=${r:-0}
      if [ "$r" -gt 16777216 ] || [ "$avail" -lt 10485760 ]; then echo "$(date -u +%FT%TZ) WATCHDOG kill $p rss_kb=$r avail_kb=$avail" >> $L/watchdog.log; kill $p; fi
    done; sleep 5; done ) & WD=$!
trap "kill $WD 2>/dev/null" EXIT
stamp "leanchecker_missing_module_control_start"
( lake env leanchecker --fresh Erdos488.NoSuchModule ) > $L/leanchecker_control_missing.log 2>&1; stamp "leanchecker_missing_module_control exit=$? (want nonzero)"
stamp "leanchecker_fresh_start Solution"
( time nice -n 10 lake env leanchecker --fresh Solution ) > $L/leanchecker_fresh.log 2>&1; stamp "leanchecker_fresh exit=$?"
stamp checker_done
