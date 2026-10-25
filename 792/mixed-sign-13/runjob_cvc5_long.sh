#!/bin/bash
k=$1; cd /home/exedev/MathDyad/erdos792
timeout 43200 nice -n 19 /home/exedev/.venv/bin/python mixed792.py $k --t 6 --engine cvc5 > logs/k${k}_cvc5_prune_long.log 2>&1; rc=$?
{ grep -h "RESULT\|WITNESS" logs/k${k}_cvc5_prune_long.log; [ $rc -eq 124 ] && echo "TIMEOUT k=$k engine=cvc5 long after 43200s"; [ $rc -ne 10 ] && [ $rc -ne 20 ] && [ $rc -ne 124 ] && echo "ERROR k=$k cvc5 long rc=$rc"; } >> results_cvc5_long.log
