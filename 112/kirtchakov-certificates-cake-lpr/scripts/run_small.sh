#!/bin/bash
cd $HOME/MathDyad/erdos112/kirtchakov/work
echo "=== START small $(date -u +%FT%TZ) P=${1:-2}"
xargs -P ${1:-2} -L 1 nice -n 19 bash ../bin/one2.sh < order_small.txt
echo "=== END small $(date -u +%FT%TZ)"
