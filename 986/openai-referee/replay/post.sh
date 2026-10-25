#!/bin/bash
# After drive.py's BUILD END: comparator modules, probes, statement match, leanchecker --fresh ×2 + missing-module control.
set -u
L=/tmp/oaimath/170/lean-build; SRC=/tmp/oaimath/170/repo/lean; OUT=$L/out
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
waitmem(){ while [ "$(memavail_gb)" -lt "$1" ]; do log "waiting mem ≥ $1G (have $(memavail_gb))"; sleep 60; done; }
until grep -q '^build ' $L/steps.tsv; do sleep 30; done
grep -q '^build 0 ' $L/steps.tsv || { log "build not clean — stopping"; exit 1; }
mkdir -p $OUT/ComparatorChallenges
for c in SharpLogRamsey RamseyFive; do
  step cmpmod_$c bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/$c.lean -o $OUT/ComparatorChallenges/$c.olean -i $OUT/ComparatorChallenges/$c.ilean > $L/logs/cmpmod_$c.log 2>&1"
done
cd $L/probe
step smoke bash -c "nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
for t in SL R5; do
  step cmp$t bash -c "nice -n 19 lean -DautoImplicit=false Cmp$t.lean > $L/logs/cmp$t.log 2>&1"
  step ax$t bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false Ax$t.lean > $L/logs/ax$t.log 2>&1"
done
step negSL bash -c "nice -n 19 lean -DautoImplicit=false NegSL.lean > $L/logs/negSL.log 2>&1"
step typeSL bash -c "nice -n 19 lean -DautoImplicit=false TypeSL.lean > $L/logs/typeSL.log 2>&1"
for f in $L/probe/Extra_*.lean; do [ -e "$f" ] || continue; b=$(basename $f .lean); step $b bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false $f > $L/logs/$b.log 2>&1"; done
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 )
log "statement_match: $(tr '\n' ' ' < $L/statement_match.txt)"
touch $L/PROBES_DONE
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 26
step leanchecker_fresh_SL bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.SharpRamsey.Main > $L/logs/leanchecker_fresh_SL.log 2>&1"
waitmem 26
step leanchecker_fresh_R5 bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.RamseyFive.Main > $L/logs/leanchecker_fresh_R5.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.Combinatorics.SharpRamsey.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE"; touch $L/ALL_DONE
