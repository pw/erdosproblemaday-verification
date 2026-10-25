#!/bin/bash
# usage: batch_lines.sh <tag> <workers> N1 N2 ...   → lines/ll_<N>.jsonl per N (all 16 directions, exact where M ≤ 400000)
tag=$1; W=$2; shift 2
cd ~/MathDyad/erdos203
for N in "$@"; do
  echo "== N=$N $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --time 300 --workers $W --maxM 400000 > lines/ll_$N.jsonl 2> lines/ll_$N.err
  python3 - $N <<'PY'
import json,sys
N=sys.argv[1]; best=None
for line in open(f'lines/ll_{N}.jsonl'):
    o=json.loads(line)
    if 'skipped' in o: print('  skipped',o['dir'],o['M']); continue
    c=o['cpsat']; print('  ',o['dir'],'M=%d'%o['M'],c['status'],c['V'],'(%.4f)'%(c['V_f'] or 0),'%.0fs'%c['wall'],o['verdict'])
PY
done
echo "BATCH $tag DONE $(date -u +%T)"
