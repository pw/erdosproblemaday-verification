#!/bin/bash
# n=15, t=7 mixed-sign pattern k -> logs/n15_k<k>_z3_prune.log ; verdict lines appended to results.log
k=$1; cd /home/exedev/MathDyad/erdos792
timeout 43200 nice -n 19 /home/exedev/.venv/bin/python mixed792.py $k --n 15 --t 7 > logs/n15_k${k}_z3_prune.log 2>&1; rc=$?
{ grep -h "RESULT\|WITNESS" logs/n15_k${k}_z3_prune.log; [ $rc -eq 124 ] && echo "TIMEOUT n=15 k=$k engine=z3 prune after 43200s"; [ $rc -ne 10 ] && [ $rc -ne 20 ] && [ $rc -ne 124 ] && echo "ERROR n=15 k=$k rc=$rc"; } >> results.log
