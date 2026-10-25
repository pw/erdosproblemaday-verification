#!/bin/bash
B=/tmp/oaimath/170/bridge; L=/tmp/oaimath/170/lean-build
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$B/out:$(cat $L/lean_path.txt)
cd $B
for m in Bridge986 Bridge986Main; do t0=$SECONDS; nice -n 19 leanchecker $m > logs_leanchecker_$m.log 2>&1; echo "leanchecker_$m $? $((SECONDS-t0))" >> steps.tsv; done
t0=$SECONDS; nice -n 19 leanchecker Bridge986DoesNotExist > logs_leanchecker_missing.log 2>&1; echo "leanchecker_missing_control $? $((SECONDS-t0))" >> steps.tsv
echo LCDONE >> steps.tsv
