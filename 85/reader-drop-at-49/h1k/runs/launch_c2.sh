#!/bin/bash
# launch one h1cube2 case: launch_c2.sh j cap
cd ~/MathDyad/erdos85/h1k
j=$1; cap=$2
ulimit -v 6000000
s=$(date +%s)
timeout $((cap+300)) ~/.venv/bin/python h1cube2.py 7 $j $cap kissat --pairsb --emit runs/c2_case$j.cnf
echo "  case $j wall $(( $(date +%s)-s )) s"
