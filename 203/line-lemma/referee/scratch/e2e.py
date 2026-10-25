# End-to-end: exact max over coset choices of min over lines, computed from 2-D point counts of phi_p on (Z/T)^2.
import json, sys, itertools
from math import gcd
from fractions import Fraction as F
import numpy as np
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
D='/home/exedev/MathDyad/erdos203'
T=60
pool=[q for q in json.load(open(f'{D}/pool_5040.json'))['pool'] if T%q['e']==0]
print('primes with e|60:',[(q['p'],q['e']) for q in pool], 'density', float(sum(F(1,q['e']) for q in pool)))
dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3),(5,-7)]
K,Lg=np.meshgrid(np.arange(T),np.arange(T),indexing='ij')
def phi_grid(p):
    a=np.array([pow(2,int(k),p) for k in range(T)],dtype=object); b=np.array([pow(3,int(l),p) for l in range(T)],dtype=object)
    return np.array([[a[k]*b[l]%p for l in range(T)] for k in range(T)],dtype=np.int64)
grids={q['p']:phi_grid(q['p']) for q in pool}
def run(sub, d):
    a,b=d; tau=(b*K-a*Lg)%T
    S=1
    vecs=[]
    for q in sub:
        g=grids[q['p']]; H=sorted(set(g.flatten().tolist()))
        assert len(H)==q['e']
        vs=[]
        for h in H:
            v=[F(int(((tau==t)&(g==h)).sum()), int((tau==t).sum())) for t in range(T)]
            vs.append(v)
        vecs.append(vs)
    den=1
    for vs in vecs:
        for v in vs:
            for x in v: den=den*x.denominator//gcd(den,x.denominator)
    iv=[[np.array([int(x*den) for x in v],dtype=np.int64) for v in vs] for vs in vecs]
    best=-1
    # translation symmetry NOT used here (pure brute force)
    for choice in itertools.product(*[range(len(v)) for v in iv]):
        W=sum(iv[j][c] for j,c in enumerate(choice))
        m=int(W.min())
        if m>best: best=m
    return F(best,den)
import time
for sub_n in (5,6):
    sub=pool[:sub_n]
    prod=1
    for q in sub: prod*=q['e']
    print('subpool',[q['p'] for q in sub],'choices',prod)
    nd=0
    for d in dirs:
        t0=time.time(); Vb=run(sub,d)
        E,lum,M,ev=LL.instance(sub,d,None)
        name,V,bd,t,wt=LL.cpsat(E,lum,M,60,2)
        ok=(V==Vb and name=='OPTIMAL'); nd+= (not ok)
        print(f'  dir {d}: 2-D brute {Vb} | linelemma CP-SAT {name} {V} {"OK" if ok else "MISMATCH"} ({time.time()-t0:.1f}s)', flush=True)
    print('  mismatches',nd)
    if prod>3e5: break
