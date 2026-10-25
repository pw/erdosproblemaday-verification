#!/bin/bash
cd ~/MathDyad/erdos188
P=~/.venv/bin/python
run() { # name k ds centers rotr blue R
  f=runs/$1
  $P config188.py --R $7 --k $2 --ds $3 --centers $4 --rot-radius $5 --origin-red --blue $6 --out $f > $f.build 2>&1
  /usr/bin/time -f "%es %MKB" timeout 3600 nice -n 19 cadical -q $f.cnf > $f.sol 2> $f.time
  echo "$f $(cat $f.build) :: $(grep '^s ' $f.sol) $(tr '\n' ' ' < $f.time)" >> runs/ladder3.log
}
for cr in 6 8 10; do run ts3_c${cr}_k5 5 sqrt3,3 $cr 4 5,0 12; if grep -q UNSAT runs/ts3_c${cr}_k5.sol; then echo "k5 UNSAT at cr=$cr" >> runs/ladder3.log; break; fi; done
for cr in 6 8; do run l6_c${cr}_b6 6 sqrt3,3 $cr 4 6,0 12; run l6_c${cr}_b5 6 sqrt3,3 $cr 4 5,0 12; done
echo DONE >> runs/ladder3.log
