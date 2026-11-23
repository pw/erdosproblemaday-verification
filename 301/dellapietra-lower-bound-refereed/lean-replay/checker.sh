#!/bin/bash
Q=$HOME/MathDyad/erdos301/dellapietra; L=$Q/logs; cd $Q/build; export PATH="$HOME/.elan/bin:$PATH"
stamp(){ echo "$(date -u +%FT%TZ) $*" >> $L/steps.tsv; }
( while true; do
    avail=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    for p in $(pgrep -x leanchecker); do
      cwd=$(readlink /proc/$p/cwd 2>/dev/null); case "$cwd" in $Q/build*) ;; *) continue;; esac
      r=$(awk '/VmRSS/{print $2}' /proc/$p/status 2>/dev/null); r=${r:-0}
      if [ "$r" -gt 20971520 ] || [ "$avail" -lt 10485760 ]; then echo "$(date -u +%FT%TZ) WATCHDOG kill $p rss_kb=$r avail_kb=$avail" >> $L/watchdog.log; kill $p; fi
    done; sleep 5; done ) & WD=$!
trap "kill $WD 2>/dev/null" EXIT
stamp "leanchecker_fresh start module=$1"
( time nice -n 10 lake env leanchecker --fresh $1 ) > $L/leanchecker_fresh.log 2>&1; stamp "leanchecker_fresh exit=$?"
