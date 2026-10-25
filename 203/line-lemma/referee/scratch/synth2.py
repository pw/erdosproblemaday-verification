import json, sys, random
from math import gcd
from fractions import Fraction as F
from ortools.sat.python import cp_model
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
T=12
rng=random.Random(11)
chars=[(e,u,v) for e in (2,3,4,6,12) for u in range(e) for v in range(e) if gcd(gcd(u,v),e)==1]
def key(e,u,v): return frozenset((k,l) for k in range(T) for l in range(T) if (u*k+v*l)%e==0)
uniq={};
for c in chars: uniq.setdefault(key(*c),c)
uniq=list(uniq.values())
bye={}
for c in uniq: bye.setdefault(c[0],[]).append(c)
def exact_cover(fam):
    m=cp_model.CpModel(); x=[]
    for (e,u,v) in fam:
        xs=[m.NewBoolVar('') for _ in range(e)]; m.AddExactlyOne(xs); x.append(xs)
    for k in range(T):
        for l in range(T):
            m.Add(sum(x[j][(u*k+v*l)%e] for j,(e,u,v) in enumerate(fam))==1)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=5; s.parameters.num_workers=2
    st=s.Solve(m)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return [next(c for c in range(e) if s.Value(x[j][c])) for j,(e,u,v) in enumerate(fam)]
    return None
shapes=[(2,4,6,12),(2,4,8)[:0] or (2,6,6,6),(3,4,4,6),(2,4,6,12),(4,4,4,6,12),(3,4,6,6,12)]
found=[]
for trial in range(400):
    sh=rng.choice([(2,4,6,12),(3,4,4,6),(2,6,6,6),(4,4,4,6,12),(3,4,6,6,12),(2,4,12,12,12)])
    fam=[rng.choice(bye[e]) for e in sh]
    if len({key(*c) for c in fam})<len(fam): continue
    # demand genuinely 2-D: characters not all multiples of one (u,v) direction
    cov=exact_cover(fam)
    if cov is None: continue
    dirsets={(u*pow(v,-1,e))%e if gcd(v,e)==1 else None for e,u,v in fam}
    if len(dirsets)>=3:
        found.append((fam,cov)); 
        if len(found)>=3: break
dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3),(5,-7)]
tot_bad=0
for fam,cov in found:
    for k in range(T):
        for l in range(T):
            assert sum((u*k+v*l)%e==c for (e,u,v),c in zip(fam,cov))==1
    pool=[{'p':'s%d'%j,'e':e,'u':u,'v':v} for j,(e,u,v) in enumerate(fam)]
    print('EXACT 2-D PARTITION', fam, 'classes', cov, 'density', sum(F(1,e) for e,_,_ in fam))
    for d in dirs:
        E,lum,M,ev=LL.instance(pool,d,None)
        name,V,bd,t,wt=LL.cpsat(E,lum,M,30,2)
        br=LL.brute(E,lum,M)
        ok = (V==1 and bd==1 and br[0]==1)
        tot_bad += not ok
        print('   dir',d,'i',[i for _,i,_ in lum],'E',E,'V',V,'bound',bd,'brute',br[0], '' if ok else '<-- WRONG')
print('exact-partition controls: wrong rows', tot_bad)
