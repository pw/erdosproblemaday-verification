#!/bin/bash
# Stop the July-engine triangle n=8 run (pid from ps; 15.5 GB RSS at ~2 h 17 min and still growing; cannot finish on this box).
P=333479
if [ "$(tr '\0' ' ' < /proc/$P/cmdline 2>/dev/null | grep -c 'run_old_n8.py triangle 8')" = "1" ]; then
  grep VmHWM /proc/$P/status; kill -TERM $P; sleep 3; kill -0 $P 2>/dev/null && kill -KILL $P; echo "stopped $P at $(date -u +%FT%TZ)"
else echo "pid $P is not the July triangle run — nothing done"; fi
