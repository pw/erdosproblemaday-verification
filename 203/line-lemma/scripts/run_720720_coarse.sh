#!/bin/bash
# 720720: exact M is 360360–720720 (too large for a bound in minutes); coarsen to M' | 720720 — still a necessary condition.
cd ~/MathDyad/erdos203
for spec in "1,1 55440" "1,1 27720" "3,-1 55440" "1,-1 55440" "1,3 55440" "3,1 55440" "1,2 55440" "1,-2 55440" "1,-3 55440"; do
  set -- $spec; d=$1; Mp=$2
  echo "== dir=$d Mp=$Mp $(date -u +%T)"
  python3 lines/linelemma.py pool_720720.json --dirs "$d" --Mp $Mp --time 600 --workers 4 >> lines/ll_720720.jsonl 2>> lines/ll_720720.err
  tail -1 lines/ll_720720.jsonl | python3 -c "
import sys,json; o=json.loads(sys.stdin.readline()); c=o['cpsat']
print('  ',o['dir'],'Mp',o['Mp'],'E=%.4f M=%d'%(o['E_f'],o['M']),c['status'],c['V'],'bound',c['bound'],'%.0fs'%c['wall'],o['verdict'])
if o.get('excluded'): sys.exit(3)"
  [ $? -eq 3 ] && { echo "EXCLUDED — stopping"; break; }
done
echo "720720 coarse DONE $(date -u +%T)"
