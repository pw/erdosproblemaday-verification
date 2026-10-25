#!/bin/bash
set -u
B=/tmp/oaimath/170/bridge; L=/tmp/oaimath/170/lean-build
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$B/out:$(cat $L/lean_path.txt)
cd $B
step(){ local n=$1; shift; local t0=$SECONDS; "$@"; local rc=$?; echo "$n $rc $((SECONDS-t0))" >> $B/steps.tsv; }
step Bridge986 bash -c "nice -n 19 lean -DautoImplicit=false Bridge986.lean -o out/Bridge986.olean -i out/Bridge986.ilean > logs_Bridge986.log 2>&1"
step Bridge986Main bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false Bridge986Main.lean -o out/Bridge986Main.olean -i out/Bridge986Main.ilean > logs_Bridge986Main.log 2>&1"
for n in Neg_s3 Neg_defmut Neg_sorry; do step $n bash -c "nice -n 19 lean -DautoImplicit=false $n.lean > logs_$n.log 2>&1"; done
echo DONE >> $B/steps.tsv
