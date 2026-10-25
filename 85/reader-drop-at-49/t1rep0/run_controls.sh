#!/bin/bash
# Negative controls on the full-size t1_rep0 check: (a) one hint dropped deep in the proof; (b) one CNF unit clause negated.
cd "$(dirname "$0")"
D=/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/strata-lrat
L=$HOME/.local/bin/lrat-check
awk 'NR==2{ if ($1 ~ /^-/) {sub(/^-/,"",$1)} else {$1="-"$1} } {print}' h7_t1_rep0.cnf > h7_t1_rep0_cnfmut.cnf
( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat $D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 --mutate 4000000 2> ctl_mut_unpack.err ) | ( ulimit -v 24000000; nice -n 19 $L h7_t1_rep0.cnf > ctl_mut.out 2>&1 ); echo "mut pipestatus ${PIPESTATUS[*]}" >> controls.rc ) &
( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat $D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 2> ctl_cnf_unpack.err ) | ( ulimit -v 24000000; nice -n 19 $L h7_t1_rep0_cnfmut.cnf > ctl_cnf.out 2>&1 ); echo "cnfmut pipestatus ${PIPESTATUS[*]}" >> controls.rc ) &
wait
date -u +%FT%TZ > controls.end
