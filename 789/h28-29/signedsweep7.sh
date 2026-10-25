#!/bin/bash
cd /home/exedev/MathDyad/erdos789
for N in 14 17 20 23; do nice -n 19 /home/exedev/.venv/bin/python signedsearch789.py $N 7 29; done
echo "SIGNEDSWEEP7 DONE"
