#!/bin/bash
cd ~/MathDyad/erdos203
for N in "$@"; do
  echo "== N=$N $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --time 180 --workers 4 --maxM 400000 --order-by-E --stop-at-first > lines/ll_$N.jsonl 2> lines/ll_$N.err
  python3 - $N <<'PY'
import json,sys
N=sys.argv[1]
for line in open(f'lines/ll_{N}.jsonl'):
    o=json.loads(line)
    if 'skipped' in o: print('  skipped',o['dir'],o['M']); continue
    c=o['cpsat']; print('  ',o['dir'],'E=%.4f M=%d'%(o['E_f'],o['M']),c['status'],c['V'],'(%.4f)'%(c['V_f'] or 0),'bound',c['bound'],'%.0fs'%c['wall'],o['verdict'])
PY
done
echo "BATCH open2 DONE $(date -u +%T)"
