#!/usr/bin/env python3
"""Does a Li-type shield exist in Z/M with three rails P = {m, 2m, 4m} (M = 7m)?  Unknowns: B, D subsets of Z/M \ P.
Li's Lemma 3.1 conditions (Q = P u B):
 (cover) every r not in Q lies in (B+B) u (P+B) u (D+B);
 (avoid) no r in Q lies in (B+B) u (P+B) u (D+B) u (D+P) [+ D+D, strict variant];
 (PP)    the mixed rail sums 3m, 5m, 6m are not in Q (so only diagonal rail pairs reach Q).
Positive control: M = 49, m = 7 must be SAT and must admit Li's own (B, D).  Negative control: forbid B entirely -> UNSAT."""
import sys, itertools
from pysat.solvers import Cadical195
from pysat.formula import IDPool
def build(M,m,strictDD=True,forceLi=None,noB=False):
    P={m%M,(2*m)%M,(4*m)%M}; pool=IDPool(); cl=[]
    b=lambda r: pool.id(('b',r%M)); d=lambda r: pool.id(('d',r%M))
    R=[r for r in range(M) if r not in P]
    for r in P: cl.append([-b(r)]); cl.append([-d(r)])
    for r in R: cl.append([-b(r),-d(r)])
    for r in [(3*m)%M,(5*m)%M,(6*m)%M]: cl.append([-b(r)])
    if noB:
        for r in R: cl.append([-b(r)])
    # pair literals: y(u,v,type) <-> conjunction
    def pair(u,v,kind):
        u%=M; v%=M
        if kind=='BB': lits=[b(u),b(v)]
        elif kind=='PB': lits=[b(v)] if u in P else None
        elif kind=='DB': lits=[d(u),b(v)]
        elif kind=='DP': lits=[d(u)] if v in P else None
        elif kind=='DD': lits=[d(u),d(v)]
        if lits is None: return None
        y=pool.id(('y',u,v,kind))
        if ('def',y) not in pool.obj2id:
            pool.id(('def',y))
            for l in lits: cl.append([-y,l])
            cl.append([y]+[-l for l in lits])
        return y
    for r in range(M):
        reps=[]
        for u in range(M):
            v=(r-u)%M
            for kind in ('BB','PB','DB'):
                y=pair(u,v,kind)
                if y is not None: reps.append(y)
        avoid=list(reps)
        for u in range(M):
            v=(r-u)%M
            y=pair(u,v,'DP')
            if y is not None: avoid.append(y)
            if strictDD:
                y=pair(u,v,'DD')
                if y is not None: avoid.append(y)
        if r in P:
            for y in avoid: cl.append([-y])          # rails: nothing but diagonal rail pairs (handled by the controller)
        else:
            cl.append([b(r)]+reps)                    # cover if not in B
            for y in avoid: cl.append([-b(r),-y])     # avoid if in B
    cl.append([b(r) for r in R])                      # B nonempty
    if forceLi:
        B,D=forceLi
        for r in R:
            cl.append([b(r)] if r in B else [-b(r)]); cl.append([d(r)] if r in D else [-d(r)])
    return cl,pool,P
def solve(M,m,**kw):
    cl,pool,P=build(M,m,**kw)
    with Cadical195(bootstrap_with=cl) as s:
        ok=s.solve()
        if not ok: return None
        mod=set(l for l in s.get_model() if l>0)
        B=sorted(r for r in range(M) if r not in P and pool.id(('b',r)) in mod)
        D=sorted(r for r in range(M) if r not in P and pool.id(('d',r)) in mod)
        return B,D
print("positive control M=49, m=7 with Li's B,D forced:", solve(49,7,strictDD=False,forceLi=({3,22,32,40,48},{1,2,5,13,27,36,47})))
print("positive control M=49 free (non-strict DD):", solve(49,7,strictDD=False))
print("negative control M=49 with B forbidden:", solve(49,7,strictDD=False,noB=True))
for m in range(1,8):
    M=7*m
    for strict in (True,False):
        r=solve(M,m,strictDD=strict)
        print(f"M={M} m={m} strictDD={strict}: {'UNSAT' if r is None else r}")
