#!/bin/bash
# kill leanchecker (by PID) if its RSS exceeds 30 GB; exit when it is gone
while true; do
  P=$(pgrep -x leanchecker | head -1)
  [ -z "$P" ] && { sleep 30; P=$(pgrep -x leanchecker | head -1); [ -z "$P" ] && { echo "$(date -u +%T) no leanchecker, exit"; exit 0; }; }
  R=$(awk '/VmRSS/{print $2}' /proc/$P/status 2>/dev/null); echo "$(date -u +%T) pid=$P rss_kb=$R" >> rss.log
  if [ -n "$R" ] && [ "$R" -gt 31457280 ]; then echo "$(date -u +%T) KILL pid=$P rss_kb=$R" >> rss.log; kill $P; fi
  sleep 60
done
