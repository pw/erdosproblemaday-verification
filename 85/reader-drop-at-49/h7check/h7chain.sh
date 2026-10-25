#!/bin/bash
L=/tmp/erdos85-1019/build/orchestrate.log
echo "$(date -u +%FT%TZ) H7: relaunched by hand (cube splitter strips lean --run's stdout prefix)" >> $L
for ph in cubes covers leaves; do
  bash -c "ulimit -v 30000000; exec python3 /home/exedev/MathDyad/erdos85/h7_check.py /tmp/erdos85-1019/h7check $ph 2 7200" >> /tmp/erdos85-1019/h7check.out 2>&1
  rc=$?; echo "$(date -u +%FT%TZ) H7: phase $ph rc=$rc" >> $L
  [ $rc -ne 0 ] && { echo "$(date -u +%FT%TZ) H7: stopping after $ph" >> $L; break; }
done
