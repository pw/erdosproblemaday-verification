# Direct enumeration of the line instance and the coarsening rule, using only 2^k 3^l mod p (never u,v).
import json, sys, random
from math import gcd
from fractions import Fraction as F
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines')
import linelemma as LL
D='/home/exedev/MathDyad/erdos203'
def lcm(a,b): return a*b//gcd(a,b)
def phi(p,k,l): return pow(2,k,p)*pow(3,l,p)%p
def egcd(a,b):
    if b==0: return a,1,0
    g,x,y=egcd(b,a%b); return g,y,x-(a//b)*y
def check(q, d, Ms, rng):
    p,e=q['p'],q['e']; a,b=d
    # pick a random coset C = {x : phi(x) = target}; target = phi(x0) for random x0
    x0=(rng.randrange(e*3),rng.randrange(e*3)); target=phi(p,*x0)
    tau0=b*x0[0]-a*x0[1]
    # (k1,l1) with b*k1 - a*l1 = 1
    g,s,t=egcd(b,-a) if b!=0 or a!=0 else None
    # b*s + (-a)*t = g = ±1
    k1,l1=s*g, t*g   # now b*k1 - a*l1 = 1
    assert b*k1-a*l1==1
    # line tau: points (k1*tau + a*t, l1*tau + b*t), t in range(e) suffices (period divides e)
    dens={}
    for tau in range(e):   # i_p | e so tau mod e covers everything
        hit=sum(1 for tt in range(e) if phi(p,k1*tau+a*tt,l1*tau+b*tt)==target)
        dens[tau]=F(hit,e)
    met=[tau for tau in range(e) if dens[tau]>0]
    vals=set(dens[tau] for tau in met)
    # code's prediction
    E,lum,M,ev=LL.instance([q],d,None)
    if lum: _,i,w=lum[0]
    else: i,w=1,ev[0][1]
    pred_met=[tau for tau in range(e) if (tau-tau0)%i==0]
    ok = (met==pred_met) and vals=={w} and w==F(1,LL_ord(p,a,b))
    # coarsening: average over tau ≡ c (mod Mc) equals [c ≡ tau0 mod gcd(i,Mc)] * gcd(i,Mc)/e
    cok=True
    for Mc in Ms:
        L=lcm(Mc,e)
        Ec,lumc,_,evc=LL.instance([q],d,Mc)
        ic,wc=(lumc[0][1],lumc[0][2]) if lumc else (1,evc[0][1])
        for c in range(Mc):
            avg=sum(dens[(c+j*Mc)%e] for j in range(L//Mc))/(L//Mc)
            predc = wc if (c-tau0)%ic==0 else F(0)
            if avg!=predc: cok=False
        # 2-D version: density of C inside the rank-2 cell {x: tau(x) ≡ c mod Mc}, counted on the torus (Z/T)^2, T=lcm(e,Mc)
        T=lcm(e,Mc)
        cnt={}; tot={}
        for k in range(T):
            for l in range(T):
                c=(b*k-a*l)%Mc
                tot[c]=tot.get(c,0)+1
                if phi(p,k,l)==target: cnt[c]=cnt.get(c,0)+1
        for c in range(Mc):
            predc = wc if (c-tau0)%ic==0 else F(0)
            if F(cnt.get(c,0),tot[c])!=predc: cok=False
    return ok, cok, i, w
def LL_ord(p,a,b):
    g=phi(p,a,b); o=1; x=g
    while x!=1: x=x*g%p; o+=1
    return o
rng=random.Random(20261014)
pools={N:json.load(open(f'{D}/pool_{N}.json'))['pool'] for N in (720,5040,7920)}
dirs=[(2,-1),(3,-2),(1,1),(1,-3),(2,3),(1,0),(0,1),(5,-7)]
nfail=0; ntest=0; nonaxis_nontriv=[]
for N,pool in pools.items():
    for q in pool:
        if q['e']>240: continue
        for d in dirs:
            ok,cok,i,w=check(q,d,[6,10,12,8],rng); ntest+=1
            if not(ok and cok): nfail+=1; print('FAIL',N,q['p'],q['e'],d,ok,cok,i,w)
            if d==(2,-1) and 1<i<q['e']: nonaxis_nontriv.append((q['p'],q['e'],i,str(w)))
print('tests',ntest,'failures',nfail)
print('direction (2,-1), primes with 1<i_p<e_p (nontrivial lumps):',sorted(set(nonaxis_nontriv))[:12])
