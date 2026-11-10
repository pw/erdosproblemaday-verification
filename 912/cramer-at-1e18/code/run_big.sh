#!/bin/bash
# exact h(n) at 10^15..10^18 with nonempty-k bitsets (for the model comparison)
cd ~/MathDyad/erdos912
export OMP_NUM_THREADS=8
for e in 15 16 17 18; do
  n=$(python3 -c "print(10**$e)")
  /usr/bin/time -v bash -c "ulimit -v 6000000; exec nice -n 10 ./hfast $n 0 bits_1e$e.bin" > hfast_1e$e.out 2> hfast_1e$e.err
done
echo DONE > run_big.done
