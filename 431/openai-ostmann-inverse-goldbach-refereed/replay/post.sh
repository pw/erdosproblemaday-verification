#!/bin/bash
# Family 013 (#431) after drive.py's BUILD END: probes (comparator modules are in the closure, already built), statement match,
# matcher mutation control. Then bridge.sh.
set -u
L=/tmp/oaimath/013/lean-build; OUT=$L/out
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $L/post.log; }
step(){ local name="$1"; shift; log "BEGIN $name"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc ${SECONDS}s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
while ! grep -q '^build ' $L/steps.tsv; do sleep 30; done
grep -q '^build 0 ' $L/steps.tsv || { log "build not clean — stopping"; exit 1; }
cd $L/probe
for C in OstmannComplete OstmannPrimes; do
  step cmp_$C bash -c "nice -n 19 lean -DautoImplicit=false Cmp_$C.lean > $L/logs/cmp_$C.log 2>&1"
  step ax_$C bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false Ax_$C.lean > $L/logs/ax_$C.log 2>&1"
done
step neg bash -c "nice -n 19 lean -DautoImplicit=false Neg.lean > $L/logs/neg.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 ); echo "statement_match $? 0" >> $L/steps.tsv
# matcher mutation control: flip one token in a copy of the comparator log; the matcher must exit 1 on it
mkdir -p $L/mutlogs; cp $L/logs/*.log $L/mutlogs/
sed -i '0,/Nat.Prime/s//Nat.Coprime/' $L/mutlogs/cmp_OstmannPrimes.log
( cd $L && python3 statement_match.py mutlogs > $L/logs/statement_match_mut.log 2>&1 ); echo "statement_match_mutant $? 0" >> $L/steps.tsv
log "statement_match: $(tr '\n' ' ' < $L/statement_match.txt)"
touch $L/PROBES_DONE
