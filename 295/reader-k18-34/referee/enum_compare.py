import math, random, sys, time
sys.path.insert(0,'/tmp/erdos295-referee')
from ref_search import S
import ref_search
sys.setrecursionlimit(10000)
def enum(N,t,a,b,prime,quad,d=None,primes=frozenset()):
    s=S(prime=prime,quad=quad,enum_all=True)
    s.dfs(N if d is None else d,t,a,b,primes,())
    return s
# (1) small N, full problem, all solutions
rows=[]
for N,t in [(2,3),(2,4),(2,5),(2,6),(3,5),(3,6),(3,7),(4,8),(4,9),(5,10),(5,11),(6,11),(6,12),(7,13),(7,14),(8,15),(9,17),(10,19)]:
    t0=time.time()
    P=enum(N,t,1,1,True,True); U=enum(N,t,1,1,False,False)
    sp=set(P.sols); su=set(U.sols)
    rows.append((N,t,len(su),len(sp),sp==su,P.c['pprunes'],P.c['two_prunes'],round(time.time()-t0,1)))
    print(f"N={N} t={t}: plain solutions={len(su)} pruned solutions={len(sp)} identical={sp==su} "
          f"(pruned run used {P.c['pprunes']} prime prunes, {P.c['two_prunes']} quadratic prunes) {round(time.time()-t0,1)}s", flush=True)
# (2) random residual states with solutions
random.seed(2026)
mismatch=0; tot=0; withsol=0; pp=0; qp=0
t0=time.time()
while tot<3000 and time.time()-t0<600:
    t=random.choice([2,3,3,4])
    d=random.randint(2,40)
    # build residual as sum of t random distinct denominators >= d (guarantees >=1 solution) or random
    if random.random()<0.7:
        xs=sorted(random.sample(range(d, d+random.choice([10,30,80])), t))
        if random.random()<0.5: xs[-1]=xs[-1]*random.randint(1,50)+random.randint(0,3)
        xs=sorted(set(xs))
        if len(xs)<t: continue
        n_,m_=0,1
        for x in xs: n_,m_=n_*x+m_,m_*x
    else:
        m_=random.randint(2,5000); n_=random.randint(1,m_-1)
    g=math.gcd(n_,m_); a,b=n_//g,m_//g
    if a>=b*t: continue
    primes=frozenset(ref_search.small_primes(b)) if b>1 else frozenset()
    P=S(prime=True,quad=True,enum_all=True); P.dfs(d,t,a,b,primes,())
    U=S(prime=False,quad=False,enum_all=True); U.dfs(d,t,a,b,primes,())
    tot+=1
    if set(P.sols)!=set(U.sols): mismatch+=1; print("MISMATCH", d,t,a,b, len(P.sols), len(U.sols))
    if U.sols: withsol+=1
    pp+=P.c['pprunes']; qp+=P.c['two_prunes']
print(f"random residual states: {tot} compared, {withsol} with >=1 solution, mismatches={mismatch}, "
      f"prime prunes exercised={pp}, quadratic prunes exercised={qp}")
