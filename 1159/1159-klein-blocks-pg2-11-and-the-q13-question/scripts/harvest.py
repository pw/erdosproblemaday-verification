#!/usr/bin/env python3
"""harvest.py q C cadical.log [name] -> parses s/v lines, writes runs/witness_q{q}_c{C}_{name}.json, checks it two ways
(model1159.check for prime q / plane_gf for prime powers), prints spectrum; for prime q also stabilizer order via equiv1159 logic."""
import sys, json, collections, itertools
q,C,log=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]; name=sys.argv[4] if len(sys.argv)>4 else 'w'
status=None; lits=[]
for line in open(log):
    if line.startswith('s '): status=line.split()[1]
    if line.startswith('v '): lits+=[int(t) for t in line.split()[1:]]
print(f"q={q} C={C} {log}: status={status}")
if status!='SATISFIABLE': sys.exit(0)
def is_prime(n): return n>1 and all(n%k for k in range(2,int(n**0.5)+1))
if is_prime(q):
    sys.path.insert(0,'.'); from model1159 import plane, check
    pts,idx,lines=plane(q,check=False)
else:
    from plane_gf import plane_gf
    pts,lines=plane_gf(q); idx={p:i for i,p in enumerate(pts)}
    def check(q,C,S):
        Sset=set(idx[tuple(p)] for p in S); hist=collections.Counter(len(Sset.intersection(L)) for L in lines)
        return all(1<=m<=C for m in hist), dict(sorted(hist.items())), len(Sset)
v=len(pts)
S=[list(pts[l-1]) for l in lits if 0<l<=v]
ok,hist,n=check(q,C,S)
print(f"  |S|={n} blocking&<=C: {ok} spectrum={hist}")
out=f"runs/witness_q{q}_c{C}_{name}.json"; json.dump(S,open(out,'w')); print("  wrote",out)
assert ok
