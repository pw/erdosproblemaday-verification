#!/bin/bash
# perfect-power variant, all 26 periods ≤ 65,520 with density ≥ 1 + the open pools; waits for the pure batch to finish first
cd ~/MathDyad/erdos203
W=$1; W2=$2; shift 2
while kill -0 $W 2>/dev/null || kill -0 $W2 2>/dev/null; do sleep 20; done
for N in "$@"; do
  echo "== pp N=$N $(date -u +%T)"
  python3 lines/linelemma.py pool_$N.json --pp 1 --time 60 --workers 3 --maxM 400000 --order-by-E > lines/pp_$N.jsonl 2> lines/pp_$N.err
  python3 - $N <<'PY'
import json,sys
from fractions import Fraction as F
N=sys.argv[1]; rows=[json.loads(l) for l in open(f'lines/pp_{N}.jsonl')]
d=[r for r in rows if 'cpsat' in r and r['cpsat'].get('bound')]; ex=[r for r in d if F(r['cpsat']['bound'])<1]
print('  dirs %d excluded %d maxbound %.4f minbound %.4f'%(len(d),len(ex),max(F(r['cpsat']['bound']) for r in d),min(F(r['cpsat']['bound']) for r in d)))
PY
done
echo "BATCH pp DONE $(date -u +%T)"
