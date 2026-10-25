#!/bin/bash
# Tsaturian control: origin red, (5,0) blue [WLOG], rotations about base-lattice points by theta_sqrt3, theta_3
cd ~/MathDyad/erdos188
P=~/.venv/bin/python
for cr in 2 3 4; do
  f=runs/ts_c${cr}_k5
  $P config188.py --R 12 --k 5 --ds sqrt3,3 --centers $cr --origin-red --blue 5,0 --out $f > $f.build 2>&1
  /usr/bin/time -f "%es %MKB" timeout 1800 nice -n 19 cadical -q $f.cnf > $f.sol 2> $f.time
  echo "$f $(cat $f.build) :: $(grep '^s ' $f.sol) $(tr '\n' ' ' < $f.time)" >> runs/ladder2.log
  if grep -q UNSAT $f.sol; then echo "UNSAT at cr=$cr" >> runs/ladder2.log; break; fi
done
echo DONE >> runs/ladder2.log
