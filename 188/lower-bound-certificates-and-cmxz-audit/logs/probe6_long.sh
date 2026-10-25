#!/bin/bash
# Relaunch (01:12Z) of the two l_6 probes that timed out at 1200 s, with 3-hour caps; results append to runs/probe6.log.
# (l6_c4_b5 is the informative one: its l_5 twin ts3_c4_k5_b5 is UNSAT in 0.28 s. l6_c3_b6's twin is SAT.)
cd ~/MathDyad/erdos188
for f in l6_c4_b5 l6_c3_b6; do
  nohup sh -c "/usr/bin/time -f '%es %MKB' timeout 10800 nice -n 19 cadical -q runs/$f.cnf > runs/${f}_long.sol 2> runs/${f}_long.time; \
    echo \"runs/$f LONG :: \$(grep '^s ' runs/${f}_long.sol || echo TIMEOUT-10800) \$(tr '\n' ' ' < runs/${f}_long.time)\" >> runs/probe6.log" > /dev/null 2>&1 &
done
# ladder3.sh (3600 s caps) continues on its own: l6_c6_b6 (running since ~00:36Z), then l6_c6_b5 (the twin of the 69-point l_5 instance), then c8.
