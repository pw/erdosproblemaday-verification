#!/bin/bash
# after the runners finish: every (N ≤ 65520, direction) with V < 1 ≤ bound (undecided at the short cap) is rerun at 900 s
cd ~/MathDyad/erdos203
A=$1; B=$2
while kill -0 $A 2>/dev/null || kill -0 $B 2>/dev/null; do sleep 20; done
python3 - <<'PY' > lines/undecided.txt
import json,glob,os
from fractions import Fraction as F
for f in sorted(glob.glob('lines/ll_*.jsonl')):
    N=os.path.basename(f)[3:-6]
    if not N.isdigit() or int(N)>65520: continue
    for l in open(f):
        o=json.loads(l)
        if 'cpsat' in o and o['cpsat'].get('bound') and F(o['cpsat']['V'])<1<=F(o['cpsat']['bound']): print(N, '%d,%d'%tuple(o['dir']))
PY
echo "undecided: $(wc -l < lines/undecided.txt)"; cat lines/undecided.txt
while read N d; do
  echo "== rerun N=$N dir=$d $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --dirs "$d" --time 900 --workers 4 --maxM 400000 >> lines/ll_${N}_rerun.jsonl 2>> lines/ll_${N}_rerun.err
  tail -1 lines/ll_${N}_rerun.jsonl | python3 -c "import sys,json; o=json.loads(sys.stdin.readline()); c=o['cpsat']; print('  ',o['dir'],c['status'],c['V'],'bound',c['bound'],'%.0fs'%c['wall'],o['verdict'])"
done < lines/undecided.txt
echo "RERUN DONE $(date -u +%T)"
