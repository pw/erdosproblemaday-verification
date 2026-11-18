#!/bin/bash
cd $HOME/MathDyad/erdos112/kirtchakov/work
while kill -0 1953521 2>/dev/null; do sleep 10; done
# remove a possibly half-written last file (the killed run may have stopped mid-write), then regenerate idempotently
last=$(ls -t ../allcnf/*.cnf | head -1); rm -f "$last"
bash ../bin/regen_all.sh > ../allcnf/regen_summary.txt 2>&1
nice -n 19 python3 ../bin/indep_batch.py ../allcnf > ../allcnf/indep.txt 2>&1
echo DONE >> ../allcnf/indep.txt
