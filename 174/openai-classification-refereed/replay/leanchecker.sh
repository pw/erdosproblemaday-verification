#!/bin/bash
# Family 172: leanchecker --fresh over LcAll (OpenAI's 65-module closure + Mathlib + Bridge174), then a missing-module control.
L=/tmp/oaimath/172/lean-build; B=/tmp/oaimath/172/bridge; source $B/lean_env.sh
export LEAN_PATH=$B/out:$LEAN_PATH
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
cd $B
step lcall_compile bash -c "nice -n 19 lean LcAll.lean -o out/LcAll.olean -i out/LcAll.ilean > $L/logs/lcall.log 2>&1"
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh LcAll > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.EuclideanRamsey.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
