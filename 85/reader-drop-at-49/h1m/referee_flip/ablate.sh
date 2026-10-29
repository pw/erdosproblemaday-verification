#!/bin/bash
# Bare-cell ablation: no --pairsb/--slots/--ph/--edgeswap, and --no-sb (no within-block transposition SB either).
cd ~/MathDyad/erdos85/h1m
for jm in "4 0,0,0,0,0,4,0,0,0,3,1,0,0,1,3,0,4,0,0,0,0,0,0,0" "2 0,1,0,0,3,0,4,0,0,0,0,0,0,0,0,0,3,0,0,0,1,0,0,2"; do
  set -- $jm
  s=$(date +%s)
  r=$(bash -c "ulimit -v 4000000; exec nice -n 19 ~/.venv/bin/python h1mcell.py 7 $1 1500 kissat --no-sb --M $2" 2>&1 | tail -2 | tr '\n' ' ')
  echo "j=$1 M=$2 BARE (no flags, --no-sb): $r [$(( $(date +%s) - s )) s]"
done
echo ALLDONE
