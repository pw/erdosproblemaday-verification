#!/usr/bin/env python3
"""Li-type shield in Z/M with an L-rail doubling cycle P = {x*2^i mod M : i < L} (needs (2^L-1)x = 0 mod M, x != 0).
Unknowns B, D in Z/M minus P. Conditions (Li Lemma 3.1 shape):
 (cover) r not in Q=P u B  =>  r in (B+B) u (P+B) u (D+B)
 (avoid) r in Q            =>  r not in (B+B) u (P+B) u (D+B) u (D+P) [u (D+D) if strict]
 (PP)    mixed rail sums x2^i + x2^j (i != j) are not in Q.
usage: shield_sat_L.py M x L [strict]"""
import sys
from pysat.solvers import Cadical195
from pysat.formula import IDPool
M,x,L=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); strict=len(sys.argv)>4 and sys.argv[4]=='strict'
P=[(x*2**i)%M for i in range(L)]
assert len(set(P))==L and ((2**L-1)*x)%M==0, (P,"not an L-cycle")
pool=IDPool(); cl=[]
b=lambda r: pool.id(('b',r%M)); d=lambda r: pool.id(('d',r%M))
Pset=set(P); R=[r for r in range(M) if r not in Pset]
for r in P: cl+= [[-b(r)],[-d(r)]]
for r in R: cl.append([-b(r),-d(r)])
mixed={(P[i]+P[j])%M for i in range(L) for j in range(L) if i!=j}
bad=[r for r in mixed if r in Pset]
if bad:
    print(f"M={M} x={x} L={L} P={P} strict={strict}: UNSAT (PP) — mixed rail sums {sorted(bad)} land on rails, so Li's diagonal-only gate structure cannot hold"); sys.exit(0)
for r in mixed: cl.append([-b(r)])
defined=set()
def pair(u,v,kind):
    u%=M; v%=M
    lits={'BB':[b(u),b(v)],'PB':([b(v)] if u in Pset else None),'DB':[d(u),b(v)],'DP':([d(u)] if v in Pset else None),'DD':[d(u),d(v)]}[kind]
    if lits is None: return None
    y=pool.id(('y',u,v,kind))
    if y not in defined:
        defined.add(y)
        for l in lits: cl.append([-y,l])
        cl.append([y]+[-l for l in lits])
    return y
for r in range(M):
    reps=[]; avoid=[]
    for u in range(M):
        v=(r-u)%M
        for kind in ('BB','PB','DB'):
            y=pair(u,v,kind)
            if y is not None: reps.append(y); avoid.append(y)
        y=pair(u,v,'DP')
        if y is not None: avoid.append(y)
        if strict:
            y=pair(u,v,'DD')
            if y is not None: avoid.append(y)
    if r in Pset:
        for y in avoid: cl.append([-y])
    else:
        cl.append([b(r)]+reps)
        for y in avoid: cl.append([-b(r),-y])
cl.append([b(r) for r in R])
with Cadical195(bootstrap_with=cl) as s:
    ok=s.solve()
    if not ok: print(f"M={M} x={x} L={L} P={P} strict={strict}: UNSAT")
    else:
        mod=set(l for l in s.get_model() if l>0)
        B=sorted(r for r in R if pool.id(('b',r)) in mod); D=sorted(r for r in R if pool.id(('d',r)) in mod)
        print(f"M={M} x={x} L={L} P={P} strict={strict}: SAT  B={B} D={D}")
