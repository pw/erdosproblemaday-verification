#!/bin/bash
# t1r0 negative controls on the referee's strict RUP checker (binary LRAT via our re-encoder; re-encoding verified
# byte-identical to the referee's own zstd decode on t7r0). Each must FAIL; the unmutated run must pass.
cd "$(dirname "$0")"
D=/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/strata-lrat; R=referee/src/rupcheck
P="$D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 --binary"
: > t1_strict_controls.out
run() { tag=$1; cnf=$2; shift 2; s=$(date +%s)
  r=$( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat2 $P "$@" 2> t1ctl_$tag.unpack.err ) | ( ulimit -v 12000000; nice -n 19 $R $cnf 2>&1 ) | tail -1 )
  echo -e "$tag\t$(( $(date +%s) - s ))s\t$(grep MUTATION t1ctl_$tag.unpack.err | head -1)\t$r" >> t1_strict_controls.out; }
run orig h7_t1_rep0.cnf
run droplast_empty h7_t1_rep0.cnf --mutate-last-empty
run mutate4M h7_t1_rep0.cnf --mutate 4000000
run cnfmut2 h7_t1_rep0_cnfmut2.cnf
echo DONE >> t1_strict_controls.out
