#!/bin/bash
# wait for my own audit loop (PID 4017087) to finish, then run CP-SAT cases one at a time
while kill -0 4017087 2>/dev/null; do sleep 20; done
cd /home/exedev/MathDyad/subs-1126/902/refA
for spec in "1,1,1,1,1,1,1,1 300" "1,1,1,1 600" "2 600" "1,1 600" "1 600" "0 600" "3 400" "2,1 400"; do
  set -- $spec
  bash -c "ulimit -v 8000000; exec timeout 900 nice -n 19 ~/.venv/bin/python -I cpsat_thm71.py $1 $2" 2>&1
done
echo CHAIN-DONE
