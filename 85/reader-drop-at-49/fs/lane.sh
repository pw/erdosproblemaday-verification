#!/bin/bash
# lane.sh <cap> <cell>...   cell = h:repsfile:t:k   (repsfile '-' for h=1,3,5)
CAP=$1; shift
for c in "$@"; do IFS=: read h r t k <<< "$c"
  bash -c "ulimit -v 6000000; exec nice -n 10 python3 $HOME/MathDyad/erdos85/fs/fsrun.py $h $r $t $k /tmp/erdos85-fs/cells $CAP kissat" >> /tmp/erdos85-fs/cells.tsv 2>&1
done
echo "LANE DONE $*" >> /tmp/erdos85-fs/cells.tsv
