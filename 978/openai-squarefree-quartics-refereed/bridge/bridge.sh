#!/bin/bash
# Family 20 (#978): after the replay's PROBES_DONE — compile the FC bridge, axiom probe (--trust=0), mutants; then
# leanchecker --fresh over Bridge978 (OpenAI's 63-module closure + Mathlib + the bridge) and a missing-module control.
B=/tmp/oaimath/020/bridge; source $B/lean_env.sh
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
while [ ! -f $L/PROBES_DONE ]; do sleep 20; done
grep -q '^build 0 ' $L/steps.tsv || { log "bridge: build not clean — stopping"; exit 1; }
cd $B
step bridge_compile bash -c "nice -n 19 lean Bridge978.lean -o out/Bridge978.olean -i out/Bridge978.ilean > Bridge978.log 2>&1"
step bridge_axioms bash -c "nice -n 19 lean --trust=0 AxBridge.lean > AxBridge.log 2>&1"
step mut_sorry_compile bash -c "nice -n 19 lean BridgeMutSorry.lean -o out/BridgeMutSorry.olean -i out/BridgeMutSorry.ilean > BridgeMutSorry.log 2>&1"
step mut_sorry_axioms bash -c "nice -n 19 lean AxMutSorry.lean > AxMutSorry.log 2>&1"
step mut_exp bash -c "nice -n 19 lean BridgeMutExp.lean > BridgeMutExp.log 2>&1"
step mut_nolocal bash -c "nice -n 19 lean BridgeMutNoLocal.lean > BridgeMutNoLocal.log 2>&1"
touch $L/BRIDGE_DONE
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Bridge978 > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.NumberTheory.PowerFree.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
