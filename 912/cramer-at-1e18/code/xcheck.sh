#!/bin/bash
# cross-check: same n, different K0 (moves the sieve/MR boundary), must give identical h
cd ~/MathDyad/erdos912; export OMP_NUM_THREADS=6
for e in 15 16 17 18; do n=$(python3 -c "print(10**$e)"); K=$(grep -o 'K0=[0-9]*' hfast_1e$e.out | cut -d= -f2)
  for f in 2 0.5; do K2=$(python3 -c "print(int($K*$f))"); bash -c "ulimit -v 6000000; exec nice -n 10 ./hfast $n $K2" 2>/dev/null | head -1 | sed "s/^/K0x$f /"; done; done > xcheck.log
echo DONE >> xcheck.log
