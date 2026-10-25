#!/bin/bash
cd /home/exedev/MathDyad/erdos789
while pgrep -f '[s]ignedsweep7.sh' >/dev/null; do sleep 30; done
for N in 26 29; do nice -n 19 /home/exedev/.venv/bin/python signedsearch789.py $N 7 39; done
echo "SIGNEDSWEEP7B DONE"
