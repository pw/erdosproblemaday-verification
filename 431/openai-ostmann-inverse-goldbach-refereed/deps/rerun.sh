#!/bin/bash
set -u
D=/tmp/oaimath/013/deps; source /tmp/oaimath/013/bridge/lean_env.sh; export LEAN_PATH=$D/out:$LEAN_PATH
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $D/run.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> $D/steps.tsv; return 0; }
gate(){ while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 20 ]; do sleep 30; done; }
cd $D
step depprobe_compile_fixed bash -c "nice -n 19 lean DepProbe.lean -o out/DepProbe.olean -i out/DepProbe.ilean > DepProbe.log 2>&1"
gate; step probeM bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' lean ProbeM.lean > ProbeM.log 2>&1"
gate; step probeC bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' lean ProbeC.lean > ProbeC.log 2>&1"
touch $D/RERUN_DONE
