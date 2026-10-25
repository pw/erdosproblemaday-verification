#!/bin/bash
# After run_cake_all.sh finishes: cake_lpr on t1r0 with the LAST hint of the final empty clause dropped (must FAIL).
cd "$(dirname "$0")"
until grep -q '^DONE' cake13.tsv 2>/dev/null; do sleep 15; done
C=$HOME/MathDyad/tools/cake_lpr/cake_lpr; D=/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/strata-lrat
s=$(date +%s)
r=$( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat2 $D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 --mutate-last-empty 2> cake_droplast.unpack.err ) | ( ulimit -v 24000000; nice -n 19 $C --CML_HEAP_SIZE=16000 --CML_STACK_SIZE=4000 h7_t1_rep0.cnf /dev/stdin 2>&1 ) | tr '\n' ' ')
echo -e "t1r0_droplast_empty\t$(( $(date +%s) - s ))s\t$(grep MUTATION cake_droplast.unpack.err)\t$r" > cake_droplast.tsv
