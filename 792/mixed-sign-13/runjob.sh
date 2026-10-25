#!/bin/bash
# one job: k engine prune|noprune  -> logs/k<k>_<engine>_<p>.log ; RESULT/WITNESS lines appended to results.log
k=$1; eng=$2; p=$3; flag=""; [ "$p" = noprune ] && flag="--no-prune"
cd /home/exedev/MathDyad/erdos792
timeout 21600 nice -n 19 /home/exedev/.venv/bin/python mixed792.py $k --t 6 --engine $eng $flag > logs/k${k}_${eng}_${p}.log 2>&1; rc=$?
{ grep -h "RESULT\|WITNESS" logs/k${k}_${eng}_${p}.log; [ $rc -eq 124 ] && echo "TIMEOUT k=$k engine=$eng prune=$p after 21600s"; [ $rc -ne 10 ] && [ $rc -ne 20 ] && [ $rc -ne 124 ] && echo "ERROR k=$k engine=$eng prune=$p rc=$rc"; } >> results.log
