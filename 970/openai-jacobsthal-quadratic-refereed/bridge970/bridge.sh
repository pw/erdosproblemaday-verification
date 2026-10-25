#!/bin/bash
# Family 21 (#970): after the replay's PROBES_DONE — verbatim check, compile the FC bridge, axiom probe (--trust=0), mutants;
# then leanchecker --fresh over Bridge970 (OpenAI's 850-module closure + Mathlib + the bridge) and a missing-module control.
B=/tmp/oaimath/021/bridge; source $B/lean_env.sh
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
while [ ! -f $L/PROBES_DONE ]; do sleep 20; done
grep -q '^build 0 ' $L/steps.tsv || { log "bridge: build not clean — stopping"; exit 1; }
cd $B
step verbatim bash -c "python3 verbatim_check.py > verbatim.log 2>&1"
step verbatim_mut bash -c "python3 verbatim_check.py --mutate > verbatim_mut.log 2>&1"
step bridge_compile bash -c "nice -n 19 lean Bridge970.lean -o out/Bridge970.olean -i out/Bridge970.ilean > Bridge970.log 2>&1"
step bridge_axioms bash -c "nice -n 19 lean --trust=0 AxBridge.lean > AxBridge.log 2>&1"
step mut_sorry_compile bash -c "nice -n 19 lean BridgeMutSorry.lean -o out/BridgeMutSorry.olean -i out/BridgeMutSorry.ilean > BridgeMutSorry.log 2>&1"
step mut_sorry_axioms bash -c "nice -n 19 lean AxMutSorry.lean > AxMutSorry.log 2>&1"
step mut_exp bash -c "nice -n 19 lean BridgeMutExp.lean > BridgeMutExp.log 2>&1"
step mut_k0 bash -c "nice -n 19 lean BridgeMutK0.lean > BridgeMutK0.log 2>&1"
touch $L/BRIDGE_DONE
while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 20 ]; do sleep 30; done
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Bridge970 > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.NumberTheory.Jacobsthal.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
