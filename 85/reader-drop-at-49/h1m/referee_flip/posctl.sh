#!/bin/bash
# campaign formula minus C4 (all four flags + transposition SB): must be SAT with a clean recheck. One process at a time.
cd ~/MathDyad/erdos85/h1m
python3 -c "
import random
rows=[l.split('\t')[:2] for l in open('classes_all.tsv')]
for j,M in random.Random(777).sample(rows,150): print(j,M)
" > referee_flip/posctl_cells.txt
while read j M; do
  out=$(bash -c "ulimit -v 4000000; exec nice -n 19 ~/.venv/bin/python h1mcell.py 7 $j 300 kissat --pairsb --slots --ph --edgeswap --drop-c4 --M $M" 2>&1 | tail -1)
  echo "$j $M | $out"
done < referee_flip/posctl_cells.txt
echo ALLDONE
