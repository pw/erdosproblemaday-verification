import math, random, sys, time
sys.path.insert(0,'/tmp/erdos295-referee')
from ref_search import S
import ref_search
class Budget(Exception): pass
class SB(S):
    LIMIT=300000
    def dfs(self,*args):
        if self.c['nodes']>self.LIMIT: raise Budget
        return super().dfs(*args)
    def two(self,d,a,b,prefix):
        if (2*b-1)//a - max(d,b//a+1) > 200000: raise Budget
        return super().two(d,a,b,prefix)
random.seed(2026)
mismatch=0; tot=0; withsol=0; pp=0; qp=0; nsol=0; skipped=0
t0=time.time()
while time.time()-t0<420:
    t=random.choice([2,3,3,4,4,5])
    d=random.randint(2,30)
    width=random.choice([8,15,30])
    xs=sorted(random.sample(range(d, d+width), t))
    if random.random()<0.5: xs[-1]=xs[-1]*random.randint(2,12)+random.randint(0,2)
    if random.random()<0.3 and t>=3: xs[-2]=xs[-2]*random.randint(2,5)
    xs=sorted(set(xs))
    if len(xs)<t or xs[0]<d: continue
    n_,m_=0,1
    for x in xs: n_,m_=n_*x+m_,m_*x
    g=math.gcd(n_,m_); a,b=n_//g,m_//g
    primes=frozenset(ref_search.small_primes(b))
    try:
        U=SB(prime=False,quad=False,enum_all=True); U.dfs(d,t,a,b,primes,())
        P=SB(prime=True,quad=True,enum_all=True); P.dfs(d,t,a,b,primes,())
    except Budget:
        skipped+=1; continue
    tot+=1
    if set(P.sols)!=set(U.sols):
        mismatch+=1; print("MISMATCH",d,t,a,b,len(P.sols),len(U.sols),flush=True)
    if U.sols: withsol+=1
    nsol+=len(U.sols)
    pp+=P.c['pprunes']; qp+=P.c['two_prunes']
print(f"random residual states (each built as a sum of t<=5 distinct unit fractions >= d, so >=1 solution): {tot} states compared "
      f"({skipped} skipped over a 300k-state budget), {withsol} with solutions, {nsol} solutions in the unpruned enumeration, "
      f"solution-set mismatches={mismatch}, prime prunes exercised={pp}, quadratic prunes exercised={qp}", flush=True)
