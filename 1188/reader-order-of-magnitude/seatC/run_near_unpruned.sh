#!/bin/bash
# Route B (C port) on M_x = [2..x] minus the primes p > x/2 (primes with a single multiple <= x).
# Each x bounded at 1800 s. Primes 5, 7, 11 and all their multiples <= x stay in.
cd "$(dirname "$0")"
for x in 14 15 16 18 20 21 22 24; do
  m=$(seq 2 $x | grep -vxE '13|17|19|23' | tr '\n' ' ')
  /usr/bin/time -f "x=$x time %es mem %MKB" nice -n 19 bash -c "ulimit -v 8000000; exec timeout 1800 ./routeBc 0 $m" > Bc_near_x$x.out 2> Bc_near_x$x.err
  echo "x=$x $(grep -h 'TOTAL\|nodes' Bc_near_x$x.out | tr '\n' ' ') $(tail -1 Bc_near_x$x.err)"
done
echo ALLDONE
