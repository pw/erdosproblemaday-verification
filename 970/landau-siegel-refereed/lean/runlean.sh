#!/bin/bash
# runlean.sh ENVFILE LOG SRC [OLEAN_BASE]: guarded single lean run (memory gate, RSS watchdog 12 GB, 40 min)
source "$1"; LOG=$(readlink -f $2); SRC=$3; OB=$4
while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 28 ]; do echo "memgate wait $(date -u +%T)" >> $LOG.gate; sleep 20; done
cd /tmp/oaimath/003/seats/D_work/bridge
echo "[$(date -u +%FT%TZ)] lean $SRC ${OB:+-o $OB.olean} LEAN_PATH=$LEAN_PATH" > $LOG
if [ -n "$OB" ]; then mkdir -p $(dirname $OB); ARGS="-o $OB.olean -i $OB.ilean"; fi
/tmp/oaimath/003/seats/D_work/rsscap.sh 12000000 2400 nice -n 19 lean -DautoImplicit=false $SRC $ARGS >> $LOG 2>&1
rc=$?; echo "[$(date -u +%FT%TZ)] rc=$rc" >> $LOG; exit $rc
