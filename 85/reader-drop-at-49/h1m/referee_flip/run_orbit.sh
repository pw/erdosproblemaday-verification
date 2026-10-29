#!/bin/bash
# sequential: one process at a time; each run nice 19, ulimit -v 4 GB, timeout 1500 s
cd ~/MathDyad/erdos85/h1m/referee_flip
while read j M st; do
  echo "=== j=$j stab=$st M=$M"
  timeout 1500 bash -c "ulimit -v 4000000; exec nice -n 19 ~/.venv/bin/python orbit_cell.py $j $M 5 7" 2>&1 | grep -E 'RESULT|model|Error|assert'
done < orbit_cells.txt
echo ALLDONE
