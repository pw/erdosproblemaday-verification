#!/bin/bash
# matched l5 controls for the l6 probes (same R, centres, rot radius, ds, WLOG)
cd ~/MathDyad/erdos188; P=~/.venv/bin/python
run() { f=runs/$1; $P config188.py --R 12 --k 5 --ds sqrt3,3 --centers $2 --rot-radius 4 --origin-red $3 --out $f > $f.build 2>&1
  /usr/bin/time -f "%es" timeout 600 nice -n 19 cadical -q $f.cnf > $f.sol 2> $f.time
  echo "$f $(cat $f.build) :: $(grep '^s ' $f.sol || echo TIMEOUT) $(tr '\n' ' ' < $f.time)" >> runs/controls5.log; }
run ts3_c4_k5_b0 4 "" & run ts3_c4_k5_b6 4 "--blue 6,0" & run ts3_c4_k5_b5 4 "--blue 5,0" & run ts3_c3_k5_b6 3 "--blue 6,0" & run ts3_c6_k5_b6 6 "--blue 6,0" &
wait; echo DONE >> runs/controls5.log
