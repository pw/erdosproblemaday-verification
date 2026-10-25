#!/bin/bash
# feasibility model (CP-SAT + HiGHS) on every direction left undecided by the 60 s max-min cap
cd ~/MathDyad/erdos203
while read N d; do
  echo "== feas-undecided N=$N dir=$d $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --dirs "$d" --feas --milp --time 300 --milp-time 300 --workers 3 --maxM 400000 >> lines/feas_${N}_undecided.jsonl 2>> lines/feas_${N}_undecided.err
  tail -1 lines/feas_${N}_undecided.jsonl | python3 -c "import sys,json; o=json.loads(sys.stdin.readline()); f=o['feas']; print('  ',o['dir'],'CP-SAT',f['cpsat_status'],'%.0fs'%f['wall'],'| HiGHS',f.get('milp_status'),'|',o['verdict'])"
done < lines/undecided_now.txt
echo "FEAS-UNDECIDED DONE $(date -u +%T)"
