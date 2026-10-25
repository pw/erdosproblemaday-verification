#!/bin/bash
# #551 after drive.py's BUILD END: comparator module, probes, statement match, bridge + controls, leanchecker --fresh + missing control.
set -u
L=/tmp/oaimath/189/lean-build; SRC=/tmp/oaimath/189/repo/lean; OUT=$L/out; B=/tmp/oaimath/189/bridge
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
waitmem(){ while [ "$(memavail_gb)" -lt "$1" ]; do log "waiting mem ≥ $1G (have $(memavail_gb))"; sleep 60; done; }
until grep -q '^build ' $L/steps.tsv 2>/dev/null; do sleep 30; done
grep -q '^build 0 ' $L/steps.tsv || { log "build not clean — stopping"; exit 1; }
mkdir -p $OUT/ComparatorChallenges
step cmpmod bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/CycleCliqueRamsey.lean -o $OUT/ComparatorChallenges/CycleCliqueRamsey.olean -i $OUT/ComparatorChallenges/CycleCliqueRamsey.ilean > $L/logs/cmpmod.log 2>&1"
cd $L/probe
step smoke bash -c "nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
step cmp bash -c "nice -n 19 lean -DautoImplicit=false Cmp.lean > $L/logs/cmp.log 2>&1"
step ax bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false Ax.lean > $L/logs/ax.log 2>&1"
step neg bash -c "nice -n 19 lean -DautoImplicit=false Neg.lean > $L/logs/neg.log 2>&1"
step typectl bash -c "nice -n 19 lean -DautoImplicit=false TypeCtl.lean > $L/logs/typectl.log 2>&1"
step pos44 bash -c "nice -n 19 lean -DautoImplicit=false Pos44.lean > $L/logs/pos44.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 )
log "statement_match: $(tr '\n' ' ' < $L/statement_match.txt)"
cd $B
step bridge bash -c "nice -n 19 lean -DautoImplicit=false Bridge551.lean -o $B/Bridge551.olean > $B/bridge.log 2>&1"
step bridge_wrongshape bash -c "nice -n 19 lean -DautoImplicit=false BridgeWrongShape.lean > $B/bridge_wrongshape.log 2>&1"
step bridge_mut bash -c "nice -n 19 lean -DautoImplicit=false BridgeMut.lean > $B/bridge_mut.log 2>&1"
touch $L/PROBES_DONE
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 26
cd $L
step leanchecker_fresh bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.Ramsey.CycleClique.MainTheorem > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.Ramsey.CycleClique.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE"; touch $L/ALL_DONE
