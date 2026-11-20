#!/bin/bash
cd ~/MathDyad/erdos488/core
for a in "557 2818382931264" "523 3548133892336" "607 3162277660168" "887 1318256738556" "709 2238721138568" "1009 1096478196143"; do
  set -- $a; ( time OMP_NUM_THREADS=8 nice -n 15 ./core $1 $2 ) > core_y$1_T$2.txt 2>&1
done
echo done > run_cores.done
