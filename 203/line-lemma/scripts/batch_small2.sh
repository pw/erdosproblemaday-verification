#!/bin/bash
cd ~/MathDyad/erdos203
for N in "$@"; do
  echo "== N=$N $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --time 60 --workers 3 --maxM 400000 > lines/ll_$N.jsonl 2> lines/ll_$N.err
  python3 - $N <<'PY'
import json,sys
from fractions import Fraction as F
N=sys.argv[1]; rows=[json.loads(l) for l in open(f'lines/ll_{N}.jsonl')]
d=[r for r in rows if 'cpsat' in r]; ex=[r for r in d if F(r['cpsat']['bound'])<1]
print('  dirs %d excluded %d maxbound %.4f minV %.4f'%(len(d),len(ex),max(F(r['cpsat']['bound']) for r in d),min(F(r['cpsat']['V']) for r in d)))
PY
done
echo "BATCH small2 DONE $(date -u +%T)"
