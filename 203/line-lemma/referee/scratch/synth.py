import json, sys, random, itertools
from math import gcd
from fractions import Fraction as F
from ortools.sat.python import cp_model
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
T=12
rng=random.Random(7)
# candidate characters: (e,u,v) with e|12, gcd(u,v,e)=1, distinct lattices
chars=[]
for e in (2,3,4,6,12):
    for u in range(e):
        for v in range(e):
            if gcd(gcd(u,v),e)==1: chars.append((e,u,v))
def lattice(e,u,v): return frozenset((k,l) for k in range(T) for l in range(T) if (u*k+v*l)%e==0)
seen={}; uniq=[]
for c in chars:
    L=lattice(*c)
    if L not in seen: seen[L]=c; uniq.append(c)
def find_cover(fam):
    m=cp_model.CpModel(); x=[]
    for (e,u,v) in fam:
        xs=[m.NewBoolVar('') for _ in range(e)]; m.AddExactlyOne(xs); x.append(xs)
    for k in range(T):
        for l in range(T):
            m.AddBoolOr([x[j][(u*k+v*l)%e] for j,(e,u,v) in enumerate(fam)])
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=20; s.parameters.num_workers=2
    st=s.Solve(m)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return [next(c for c in range(e) if s.Value(x[j][c])) for j,(e,u,v) in enumerate(fam)]
    return None
# want a family with mixed characters, NOT all from one 1-D character; greedy random until a cover exists
for trial in range(200):
    fam=rng.sample(uniq, 9)
    # require at least 3 pairwise non-proportional characters with e>=3
    cov=find_cover(fam)
    if cov is not None and len({(u*pow(v,-1,e)%e if gcd(v,e)==1 else ('v',v,e)) for e,u,v in fam})>=4:
        break
print('family', fam, 'cover classes', cov, 'density', sum(F(1,e) for e,_,_ in fam))
# verify cover literally
for k in range(T):
    for l in range(T):
        assert any((u*k+v*l)%e==c for (e,u,v),c in zip(fam,cov))
pool=[{'p':'s%d'%j,'e':e,'u':u,'v':v} for j,(e,u,v) in enumerate(fam)]
json.dump({'N':12,'pool':pool},open('/tmp/ref203lines/synth_cover.json','w'))
dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3),(5,-7)]
bad=0
for d in dirs:
    E,lum,M,ev=LL.instance(pool,d,None)
    name,V,bd,t,wt=LL.cpsat(E,lum,M,30,2)
    print(' dir',d,'lumpy',len(lum),'i',[i for _,i,_ in lum],'E',E,'->',name,'V',V, 'bound',bd)
    if V<1 or bd<1: bad+=1
print('synthetic 2-D cover: directions with V<1 (false exclusions):',bad)
