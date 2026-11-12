#!/bin/bash
# kill the build's process group if MemAvailable < 14 GB (protects day-old solvers from earlyoom)
PG=$1
while kill -0 -- -$PG 2>/dev/null; do
  a=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
  if [ "$a" -lt 14000000 ]; then echo "$(date -u +%FT%TZ) MEMGUARD kill pg=$PG avail_kb=$a" >> /tmp/e708/run/memguard.log; kill -- -$PG; sleep 5; kill -9 -- -$PG 2>/dev/null; exit 0; fi
  sleep 2
done
