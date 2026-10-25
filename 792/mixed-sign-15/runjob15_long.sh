#!/bin/bash
# n=15, t=7, pattern k, 36 h cap -> logs/n15_k<k>_z3_prune_long.log ; verdicts appended to results_n15_long.log
k=$1; cd /home/exedev/MathDyad/erdos792
timeout 129600 nice -n 19 /home/exedev/.venv/bin/python mixed792.py $k --n 15 --t 7 > logs/n15_k${k}_z3_prune_long.log 2>&1; rc=$?
{ grep -h "RESULT\|WITNESS" logs/n15_k${k}_z3_prune_long.log; [ $rc -eq 124 ] && echo "TIMEOUT n=15 k=$k z3 prune long after 129600s"; [ $rc -ne 10 ] && [ $rc -ne 20 ] && [ $rc -ne 124 ] && echo "ERROR n=15 k=$k long rc=$rc"; } >> results_n15_long.log
