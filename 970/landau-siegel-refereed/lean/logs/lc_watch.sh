#!/bin/bash
# Main seat, 11:3xZ: replaces seat D's rsscap time cap for leanchecker PID $1 (kept: RSS cap $2 kB; new wall cap $3 s from now).
P=$1; LIM=$2; TO=$3; t0=$SECONDS; peak=0
while kill -0 $P 2>/dev/null; do
  r=$(awk '/VmRSS/{print $2}' /proc/$P/status 2>/dev/null); r=${r:-0}; [ "$r" -gt "$peak" ] && peak=$r
  if [ "$r" -gt "$LIM" ]; then kill $P; echo "LCWATCH RSS-KILLED pid=$P rss_kb=$r $(date -u +%FT%TZ)"; exit 137; fi
  if [ $((SECONDS-t0)) -gt "$TO" ]; then kill $P; echo "LCWATCH TIMEOUT pid=$P after +$TO s peak_kb=$peak $(date -u +%FT%TZ)"; exit 124; fi
  sleep 1
done
echo "LCWATCH pid=$P exited $(date -u +%FT%TZ) peak_kb=$peak"
