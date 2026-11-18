#!/bin/bash
cd $HOME/MathDyad/erdos112/kirtchakov/work
echo "=== START $(date -u +%FT%TZ) P=${1:-6}"
xargs -P ${1:-6} -L 1 nice -n 19 bash ../bin/one.sh < order.txt
echo "=== END $(date -u +%FT%TZ)"; ls res/*.json | wc -l
