#!/bin/bash
cd /tmp/e1125/787work
done_n=103094
while true; do
  fin=0; grep -q "ALL TASKS\|NON-UNSAT\|Traceback" k6run/k6_all_waves.log && fin=1
  pgrep -f "solve_k6_pos.py all_waves" > /dev/null || fin=1
  cp /tmp/e1125/dl787/repo/code/learned_cores_m22.txt snap_loop.txt
  n=$(wc -l < snap_loop.txt)
  if [ $n -gt $done_n ]; then
    tail -n +$((done_n+1)) snap_loop.txt | head -n $((n-done_n)) > chunk_$done_n.txt
    timeout 3000 python3 -P audit_cores.py chunk_$done_n.txt 22 > chunk_$done_n.audit 2>&1
    echo "audited lines $((done_n+1))..$n: $(tail -1 chunk_$done_n.audit)" >> audit_loop.log
    done_n=$n
  fi
  [ $fin = 1 ] && [ $n -le $done_n ] && { echo "FINAL total=$done_n" >> audit_loop.log; break; }
  sleep 60
done
