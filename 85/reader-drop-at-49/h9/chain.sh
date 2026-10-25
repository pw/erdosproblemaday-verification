#!/bin/bash
cd /home/exedev/MathDyad/erdos85/h9
until [ -f /tmp/erdos85-1019/h9/results.json ]; do sleep 15; done
for f in /tmp/erdos85-1019/h9gen/*.cnf; do b=$(basename $f); cmp -s $f /tmp/erdos85-1019/h9/$b && echo "same $b" || echo "DIFF $b"; done > gen_vs_h9run.cmp
bash -c 'ulimit -v 8000000; exec ./drat_h9.sh' > drat_h9.log 2>&1
bash -c 'ulimit -v 8000000; exec nice -n 19 /home/exedev/.venv/bin/python hrun.py 7 reps7.json 1 7 /tmp/erdos85-1019/h7t 2400 kissat' > h7t.out 2>&1
echo "$(date -u +%FT%TZ) chain done" >> h7t.out
