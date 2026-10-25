#!/bin/bash
cd /home/exedev/MathDyad/erdos789
# controls: [-11,11] whole interval has H=5 (bundle) -> max m should be 23 at N=11; [-12,12] has H=6 -> max m < 25 at N=12
nice -n 19 /home/exedev/.venv/bin/python signedsearch789.py 11 6 20
nice -n 19 /home/exedev/.venv/bin/python signedsearch789.py 12 6 22
for N in 14 17 20 23 26; do nice -n 19 /home/exedev/.venv/bin/python signedsearch789.py $N 6 27; done
echo "SIGNEDSWEEP DONE"
