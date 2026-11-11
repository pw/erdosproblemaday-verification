#!/bin/bash
# usage: run_targets.sh R E tag
export OMP_NUM_THREADS=6
R=$1; E=$2; tag=$3
run(){ name=$1; shift; bash -c "ulimit -v 12000000; exec timeout 3000 nice -n 10 ./e488c $*" > log_target_${tag}_${name}.txt 2>&1; }
run 509_1e16 509 $R $E 10000000000000000
run 1021_1e15_3e14 1021 $R $E 1000000000000000 300000000000000
run 2039_1e15_2e14 2039 $R $E 1000000000000000 200000000000000
