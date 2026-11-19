#!/bin/bash
cd ~/MathDyad/erdos1186/numerics
export OMP_NUM_THREADS=1
ulimit -v 8000000
nice -n 15 timeout 900 python3 dsearch.py 300 60 40 > dsearch_n300.log 2>&1
nice -n 15 timeout 900 python3 dsearch.py 600 40 30 > dsearch_n600.log 2>&1
nice -n 15 timeout 1200 python3 dsearch.py 1096 24 16 > dsearch_n1096.log 2>&1
echo ALLDONE >> dsearch_n1096.log
