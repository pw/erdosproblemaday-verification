#!/bin/bash
# second instrument for claim (i): feasibility model (CP-SAT + HiGHS) on every direction of every period ≤ 65,520 with density ≥ 1
cd ~/MathDyad/erdos203
for N in "$@"; do
  echo "== feas N=$N $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --feas --milp --time 120 --milp-time 120 --workers 2 --maxM 400000 > lines/feas_$N.jsonl 2> lines/feas_$N.err
  python3 -c "
import json
rows=[json.loads(l) for l in open('lines/feas_$N.jsonl')]; f=[r for r in rows if 'feas' in r]
cp=sum(1 for r in f if r['feas']['cpsat_status']=='INFEASIBLE'); mi=sum(1 for r in f if r['feas'].get('milp_status')==2)
wit=sum(1 for r in f if r['feas'].get('t') is not None)
print('  dirs %d  CP-SAT INFEASIBLE %d  HiGHS INFEASIBLE %d  witnesses(≥1) %d  undecided %d'%(len(f),cp,mi,wit,len(f)-cp-wit))"
done
echo "BATCH feas-small DONE $(date -u +%T)"
