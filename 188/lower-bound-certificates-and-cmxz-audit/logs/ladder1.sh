#!/bin/bash
cd ~/MathDyad/erdos188
P=~/.venv/bin/python
for cr in 1 2 3; do for k in 5 6; do
  f=runs/c${cr}_k${k}
  $P config188.py --R 10 --k $k --ds sqrt3,3,5 --centers $cr --origin-red --out $f > $f.build 2>&1
  /usr/bin/time -f "%es %MKB" timeout 1800 nice -n 19 cadical -q $f.cnf > $f.sol 2> $f.time
  echo "$f $(cat $f.build) :: $(grep '^s ' $f.sol) $(tr '\n' ' ' < $f.time)" >> runs/ladder1.log
done; done
echo DONE >> runs/ladder1.log
