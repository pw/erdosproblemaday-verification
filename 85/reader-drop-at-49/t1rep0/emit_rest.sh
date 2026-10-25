#!/bin/bash
cd "$(dirname "$0")"
B=/tmp/erdos85-1019/build; P=/tmp/erdos85-1019/repo/proofs; T=$HOME/.elan/toolchains/leanprover--lean4---v4.31.0/bin
LP=$B/lean:$(ls -d $P/.lake/packages/*/.lake/build/lib/lean | paste -sd:)
D=$P/Proofs/Certificates/strata-lrat; L=$HOME/.local/bin/lrat-check
for c in "2 0" "2 1" "3 0" "3 1" "3 2" "4 0" "4 1" "4 2"; do set -- $c
  ( ulimit -v 40000000; PATH=$T:/usr/bin:/bin LEAN_PATH=$LP nice -n 19 lean -j1 --run EmitT1Rep0.lean $1 $2 $PWD/h7_t$1_rep$2.cnf ) > emit_t$1r$2.log 2>&1
  M=$(echo $1 | sed 's/^/T/')Rep$2
  f=$P/Proofs/Erdos85OrderFortyNineSevenHigh${M}Certificate.lean
  read fb bb < <(grep -A1 'parsePackedLz4OrderFortyNineLratProof sevenHigh' $f | tail -1)
  r=$( ( ulimit -v 8000000; nice -n 19 ./unpack_lrat $D/h7_t$1_rep$2.packed.lz4p7 $fb $bb 2> unpack_t$1r$2.err ) | nice -n 19 $L h7_t$1_rep$2.cnf 2>&1 | grep -E "VERIFIED|FAILED" | head -1)
  echo "t$1 rep$2 $(tail -1 emit_t$1r$2.log) | $r | $(tail -1 unpack_t$1r$2.err) | header_actions=$(grep -o 'lrat_actions=[0-9]*' $f)" >> all13.tsv
done
echo DONE >> all13.tsv
