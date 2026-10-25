#!/bin/bash
# Family 25: leanchecker --fresh over BridgeAll (imports Bridge304 + Bridge148_293 ⇒ OpenAI's 348-module closure + Mathlib + our bridges), then a missing-module control.
L=/tmp/oaimath/025/lean-build; B=/tmp/oaimath/025/bridge; source $B/lean_env.sh
export LEAN_PATH=$B/out:$LEAN_PATH
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
cd $B
printf 'import Bridge304\nimport Bridge148_293\n' > BridgeAll.lean
step bridgeall bash -c "nice -n 19 lean BridgeAll.lean -o out/BridgeAll.olean -i out/BridgeAll.ilean > $L/logs/bridgeall.log 2>&1"
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh BridgeAll > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.NumberTheory.ShortEgyptian.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
