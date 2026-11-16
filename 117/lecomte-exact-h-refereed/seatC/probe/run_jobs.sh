#!/bin/bash
# usage: run_jobs.sh JOBFILE OUT.jsonl LOG
# runs each job line sequentially in ONE process chain (memory + time capped, nice 19)
cd /home/exedev/MathDyad/subs-1116/117/seatC
while read -r p d e fam cnt s0; do
  [ -z "$p" ] && continue
  bash -c "ulimit -v 8000000; exec nice -n 19 timeout 3600 python3 -u probe.py $p $d $e $fam $cnt $s0 $2" >> "$3" 2>&1
  echo "JOBDONE $p $d $e $fam $cnt $s0 rc=$?" >> "$3"
done < "$1"
echo ALLDONE >> "$3"
