#!/bin/bash
# Family 013 (#431): after PROBES_DONE — verbatim check, compile the two FC bridges (route C, route M), axiom probes
# (--trust=0), mutants (planted sorry must surface; two FALSE statements must fail to compile); a both-routes import probe;
# then ONE leanchecker --fresh (over BothProbe if both routes coexist, else over each bridge) + a missing-module control.
B=/tmp/oaimath/013/bridge; source $B/lean_env.sh
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
while [ ! -f $L/PROBES_DONE ]; do sleep 20; done
grep -q '^build 0 ' $L/steps.tsv || { log "bridge: build not clean — stopping"; exit 1; }
cd $B
step verbatim bash -c "python3 verbatim_check.py > verbatim.log 2>&1"
step verbatim_mut bash -c "python3 verbatim_check.py --mutate > verbatim_mut.log 2>&1"
for R in C M; do
  step bridge${R}_compile bash -c "nice -n 19 lean Bridge431$R.lean -o out/Bridge431$R.olean -i out/Bridge431$R.ilean > Bridge431$R.log 2>&1"
  step bridge${R}_axioms bash -c "nice -n 19 lean --trust=0 Ax431$R.lean > Ax431$R.log 2>&1"
  step mut${R}_sorry_compile bash -c "nice -n 19 lean Bridge431${R}MutSorry.lean -o out/Bridge431${R}MutSorry.olean -i out/Bridge431${R}MutSorry.ilean > Bridge431${R}MutSorry.log 2>&1"
  step mut${R}_sorry_axioms bash -c "nice -n 19 lean Ax431${R}MutSorry.lean > Ax431${R}MutSorry.log 2>&1"
  step mut${R}_nonempty bash -c "nice -n 19 lean Bridge431${R}MutNonempty.lean > Bridge431${R}MutNonempty.log 2>&1"
done
step mutC_dropB bash -c "nice -n 19 lean Bridge431CMutDropB.lean > Bridge431CMutDropB.log 2>&1"
step both_probe bash -c "nice -n 19 lean BothProbe.lean -o out/BothProbe.olean -i out/BothProbe.ilean > BothProbe.log 2>&1"
touch $L/BRIDGE_DONE
while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 20 ]; do sleep 30; done
if grep -q '^both_probe 0 ' $L/steps.tsv; then TARGETS="BothProbe"; else TARGETS="Bridge431C Bridge431M"; fi
log "leanchecker targets: $TARGETS"
for T in $TARGETS; do
  step leanchecker_fresh_$T bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh $T > $L/logs/leanchecker_fresh_$T.log 2>&1"
done
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.NumberTheory.Ostmann.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "LEANCHECKER DONE"; touch $L/LC_DONE
