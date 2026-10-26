#!/bin/bash
W=/tmp/oaimath/003/seats/C_work; cd $W
for spec in "-1 4 3" "5 4 3" "-7 4 5" "13 4 2" "-3 4 4" "-1 4 6"; do
  set -- $spec
  bash -c "ulimit -v 8000000; exec timeout 1800 nice -n 19 ~/.venv/bin/python3 $W/lemma7.py $1 $2 $3 paper lex 1 $W/runs/N4_paper_d$1_H$3_lex.json" > $W/runs/N4_paper_d$1_H$3_lex.log 2>&1 || echo "FAILED $spec"
done
echo BATCH3 DONE
