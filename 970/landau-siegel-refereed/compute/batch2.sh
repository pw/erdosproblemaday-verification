#!/bin/bash
# broken / relabelled variants (controls) for Lemma 7
for d in -1 -3 5 -7 13 3 -5; do
 for N in 2 3; do
  for H in 1 2 3 5; do
   for v in tau permslot2 swap wrong2; do
    ~/.venv/bin/python3 lemma7.py $d $N $H $v lex 1 runs/${v}_d${d}_N${N}_H${H}_lex.json > runs/${v}_d${d}_N${N}_H${H}_lex.log 2>&1 || echo "FAILED $v $d $N $H"
   done
  done
 done
done
echo BATCH2 DONE
