#!/bin/bash
cd /tmp/oaimath/021/b687; source lean_env.sh
while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 20 ]; do sleep 30; done
echo "[$(date -u +%FT%TZ)] BEGIN leanchecker_fresh Bridge687" >> lc.log
nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Bridge687 > lc_fresh.log 2>&1; echo "leanchecker_fresh rc=$?" >> lc.log
nice -n 19 leanchecker --fresh Erdos687DoesNotExist > lc_missing.log 2>&1; echo "leanchecker_missing_control rc=$?" >> lc.log
echo "[$(date -u +%FT%TZ)] END" >> lc.log; touch LC_DONE
