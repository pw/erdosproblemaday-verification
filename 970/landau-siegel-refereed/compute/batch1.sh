#!/bin/bash
# Lemma 7, paper variant, grid over d, N, H, tiebreak
for d in -1 -3 5 -7 13 3 -5; do
 for N in 2 3; do
  for H in 1 2 3 5 8; do
   for tb in lex rev; do
    ~/.venv/bin/python3 lemma7.py $d $N $H paper $tb 1 runs/paper_d${d}_N${N}_H${H}_${tb}.json > runs/paper_d${d}_N${N}_H${H}_${tb}.log 2>&1 || echo "FAILED $d $N $H $tb"
   done
  done
 done
done
echo BATCH1 DONE
