#!/bin/bash
cd /home/exedev/MathDyad/subs-1116/117/seatC
while read -r p nb ns e cnt s0; do
  [ -z "$p" ] && continue
  bash -c "ulimit -v 8000000; exec nice -n 19 timeout 3600 python3 -u probe_zpk.py $p $nb $ns $e $cnt $s0 probe/zpk.jsonl" >> logs/probe_zpk.log 2>&1
  echo "JOBDONE $p $nb $ns $e $cnt $s0 rc=$?" >> logs/probe_zpk.log
done < probe/jobs_zpk.txt
echo ALLDONE >> logs/probe_zpk.log
