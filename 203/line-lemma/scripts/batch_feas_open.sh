#!/bin/bash
# second instrument for the open-pool verdicts: FEASIBILITY model (every line ≥ 1 hard), CP-SAT + HiGHS; INFEASIBLE = proof
cd ~/MathDyad/erdos203
for spec in "166320 1,1 0" "221760 1,1 0" "332640 1,1 0" "720720 1,1 55440" "110880 1,1 0"; do
  set -- $spec; N=$1; d=$2; Mp=$3
  echo "== feas N=$N dir=$d Mp=$Mp $(date -u +%T)"
  if [ "$Mp" = "0" ]; then MPA=""; else MPA="--Mp $Mp"; fi
  python3 lines/linelemma.py pool_$N.json --dirs "$d" $MPA --feas --milp --time 600 --milp-time 900 --workers 4 > lines/feas_$N.jsonl 2> lines/feas_$N.err
  python3 -c "
import json
for l in open('lines/feas_$N.jsonl'):
    o=json.loads(l); f=o['feas']; print('  ',o['dir'],'Mp',o['Mp'],'CP-SAT',f['cpsat_status'],'%.0fs'%f['wall'],'| HiGHS status',f.get('milp_status'),'|',o['verdict'])"
done
echo "BATCH feas-open DONE $(date -u +%T)"
