#!/bin/bash
# Family 25 (#304/#148/#293) after drive.py's BUILD END: comparator modules, probes, statement match. leanchecker --fresh launched separately.
set -u
L=/tmp/oaimath/025/lean-build; SRC=/tmp/oaimath/024/repo/lean; OUT=$L/out
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
grep -q '^build 0 ' $L/steps.tsv || { log "build not clean — stopping"; exit 1; }
mkdir -p $OUT/ComparatorChallenges
for C in ShortEgyptianFractions EgyptianFractions; do
  step cmpmod_$C bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/$C.lean -o $OUT/ComparatorChallenges/$C.olean -i $OUT/ComparatorChallenges/$C.ilean > $L/logs/cmpmod_$C.log 2>&1"
done
cd $L/probe
step cmpSE bash -c "nice -n 19 lean -DautoImplicit=false CmpSE.lean > $L/logs/cmpSE.log 2>&1"
step cmpEF bash -c "nice -n 19 lean -DautoImplicit=false CmpEF.lean > $L/logs/cmpEF.log 2>&1"
step axSE bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false AxSE.lean > $L/logs/axSE.log 2>&1"
step axEF bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false AxEF.lean > $L/logs/axEF.log 2>&1"
step neg bash -c "nice -n 19 lean -DautoImplicit=false Neg.lean > $L/logs/neg.log 2>&1"
step typectl bash -c "nice -n 19 lean -DautoImplicit=false TypeCtl.lean > $L/logs/typectl.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 ); echo "statement_match $? 0" >> $L/steps.tsv
log "statement_match: $(tr '\n' ' ' < $L/statement_match.txt)"
touch $L/PROBES_DONE
