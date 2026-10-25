#!/bin/bash
# cake_lpr (CakeML-verified LRAT checker, github.com/tanyongkiam/cake_lpr @ a36874a, the commit the authors' kit pins)
# on all 13 H7 t>=1 certificates (our decoder -> text LRAT on a pipe) + the cited-clause CNF control on t1r0.
cd "$(dirname "$0")"
C=$HOME/MathDyad/tools/cake_lpr/cake_lpr
D=/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/strata-lrat
P=/tmp/erdos85-1019/repo/proofs/Proofs
: > cake13.tsv
for c in "1 0" "2 0" "2 1" "3 0" "3 1" "3 2" "4 0" "4 1" "4 2" "5 0" "5 1" "6 0" "7 0"; do set -- $c
  f=$P/Erdos85OrderFortyNineSevenHighT$1Rep$2Certificate.lean
  read fb bb < <(grep -A1 'parsePackedLz4OrderFortyNineLratProof sevenHigh' $f | tail -1)
  s=$(date +%s)
  r=$( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat $D/h7_t$1_rep$2.packed.lz4p7 $fb $bb 2>/dev/null ) | ( ulimit -v 24000000; nice -n 19 /usr/bin/time -f "MAXRSS_KB=%M" $C --CML_HEAP_SIZE=16000 --CML_STACK_SIZE=4000 h7_t$1_rep$2.cnf /dev/stdin 2>&1 ) | tr '\n' ' ')
  echo -e "t$1r$2\t$(( $(date +%s) - s ))s\t$r" >> cake13.tsv
done
s=$(date +%s)
r=$( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat $D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 2>/dev/null ) | ( ulimit -v 24000000; nice -n 19 $C --CML_HEAP_SIZE=16000 --CML_STACK_SIZE=4000 h7_t1_rep0_cnfmut2.cnf /dev/stdin 2>&1 ) | tr '\n' ' ')
echo -e "t1r0_cnfmut2(clause 1302103 flipped, cited by the first lemma)\t$(( $(date +%s) - s ))s\t$r" >> cake13.tsv
echo DONE >> cake13.tsv
