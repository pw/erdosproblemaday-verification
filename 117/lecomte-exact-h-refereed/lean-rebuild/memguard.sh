#!/bin/bash
# If MemAvailable drops below 12 GB, kill (by PID) lean processes whose cwd is this build dir. Exit when no lake build runs.
D=$(readlink -f ~/MathDyad/subs-1116/117/lean-build)
while pgrep -f "lake build" >/dev/null 2>&1 || pgrep -x lake >/dev/null; do
  A=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
  echo "$(date -u +%T) avail_gb=$A" >> mem.log
  if [ "$A" -lt 12 ]; then
    for P in $(pgrep -x lean); do [ "$(readlink -f /proc/$P/cwd)" = "$D" ] && { echo "$(date -u +%T) KILL lean $P" >> mem.log; kill $P; }; done
  fi
  sleep 15
done
