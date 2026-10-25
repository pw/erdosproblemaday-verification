#!/bin/bash
# #968 (family 26) after drive.py's BUILD END: comparator module, probes, statement match. (leanchecker --fresh is launched separately, after the bridge.)
set -u
L=/tmp/oaimath/026/lean-build; SRC=/tmp/oaimath/026/repo/lean; OUT=$L/out
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
grep -q '^build 0 ' $L/steps.tsv || { log "build not clean — stopping"; exit 1; }
mkdir -p $OUT/ComparatorChallenges
step cmpmod bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/PrimeGaps.lean -o $OUT/ComparatorChallenges/PrimeGaps.olean -i $OUT/ComparatorChallenges/PrimeGaps.ilean > $L/logs/cmpmod.log 2>&1"
cd $L/probe
step smoke bash -c "nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
step cmp bash -c "nice -n 19 lean -DautoImplicit=false Cmp.lean > $L/logs/cmp.log 2>&1"
step ax bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false Ax.lean > $L/logs/ax.log 2>&1"
step neg bash -c "nice -n 19 lean -DautoImplicit=false Neg.lean > $L/logs/neg.log 2>&1"
step typectl bash -c "nice -n 19 lean -DautoImplicit=false TypeCtl.lean > $L/logs/typectl.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 )
log "statement_match: $(tr '\n' ' ' < $L/statement_match.txt)"
touch $L/PROBES_DONE
