#!/bin/bash
set -u
D=/tmp/oaimath/013/deps; L=/tmp/oaimath/013/lean-build; source /tmp/oaimath/013/bridge/lean_env.sh
export LEAN_PATH=$D/out:$LEAN_PATH
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $D/run.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> $D/steps.tsv; return 0; }
gate(){ while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 20 ]; do sleep 30; done; }
while ! grep -q '^build970 ' $L/steps970.tsv 2>/dev/null; do sleep 30; done
while [ ! -f $D/NOW_DONE ]; do sleep 20; done
log "build970: $(grep '^build970 ' $L/steps970.tsv | cut -c1-80)"
cd $D
gate; step probe970 bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' lean Probe970.lean > Probe970.log 2>&1"
log "DONE"; touch $D/DEPS_DONE
