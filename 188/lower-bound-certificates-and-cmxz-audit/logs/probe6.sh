#!/bin/bash
cd ~/MathDyad/erdos188
P=~/.venv/bin/python
run() { # name k ds centers rotr blueflag R timeout
  f=runs/$1
  $P config188.py --R $7 --k $2 --ds $3 --centers $4 --rot-radius $5 --origin-red $6 --out $f > $f.build 2>&1
  /usr/bin/time -f "%es %MKB" timeout $8 nice -n 19 cadical -q $f.cnf > $f.sol 2> $f.time
  echo "$f $(cat $f.build) :: $(grep '^s ' $f.sol || echo TIMEOUT) $(tr '\n' ' ' < $f.time)" >> runs/probe6.log
}
run l6_c4_b6 6 sqrt3,3 4 4 "--blue 6,0" 12 1200 &
run l6_c4_b5 6 sqrt3,3 4 4 "--blue 5,0" 12 1200 &
run l6_c4_b0 6 sqrt3,3 4 4 "" 12 1200 &
run l6_c3_b6 6 sqrt3,3 3 4 "--blue 6,0" 12 1200 &
wait
echo DONE >> runs/probe6.log
