#!/bin/bash
while kill -0 4017087 2>/dev/null; do sleep 20; done
cd /home/exedev/MathDyad/subs-1126/902/refA
for spec in "1,1,1,1,1,1,1,1 120" "2 300" "1,1 300" "1 200" "0 200"; do
  set -- $spec
  bash -c "ulimit -v 8000000; exec timeout 600 nice -n 19 ~/.venv/bin/python -I cpsat_thm71.py $1 $2" 2>&1
done
echo CHAIN-DONE
