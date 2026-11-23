#!/bin/bash
# rsscap.sh LIMIT_KB TIMEOUT_S cmd... : run cmd, kill it (by PID) if its RSS exceeds LIMIT_KB or it outlives TIMEOUT_S.
LIM=$1; TO=$2; shift 2
"$@" & P=$!
peak=0; t0=$SECONDS
while kill -0 $P 2>/dev/null; do
  r=$(awk '/VmRSS/{print $2}' /proc/$P/status 2>/dev/null); r=${r:-0}
  [ "$r" -gt "$peak" ] && peak=$r
  if [ "$r" -gt "$LIM" ]; then kill $P; echo "RSSCAP KILLED pid=$P rss_kb=$r after $((SECONDS-t0))s"; wait $P; exit 137; fi
  if [ $((SECONDS-t0)) -gt "$TO" ]; then kill $P; echo "RSSCAP TIMEOUT pid=$P after $TO s peak_kb=$peak"; wait $P; exit 124; fi
  sleep 0.5
done
wait $P; rc=$?; echo "RSSCAP done rc=$rc peak_kb=$peak wall=$((SECONDS-t0))s"; exit $rc
