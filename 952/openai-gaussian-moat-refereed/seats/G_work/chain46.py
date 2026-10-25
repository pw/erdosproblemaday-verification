# Exact check of the chain inequality (4.6) and the mixture step f_V(b) >= (f_X(b)+f_Y(b))/2
# on small instances of the Section 4 transition (random tau law over a few start times,
# h uniform on E_t - E_t, fixed deterministic pair rule, V = X or Y by a fair coin).
import math, random, itertools
random.seed(99)
def two_squares(p):
    for a in range(1,int(p**0.5)+1):
        b2=p-a*a; b=int(round(b2**0.5))
        if b*b==b2 and b>0: return a,b
def rmap(p,sign):
    a,b=two_squares(p); iv=(-a*pow(sign*b%p,-1,p))%p
    return lambda z: (z[0]+z[1]*iv)%p
def H(d):
    t=sum(d.values()); return -sum(v/t*math.log(v/t) for v in d.values() if v>0)
def Hcond(joint, f, g):
    # H(f(w) | g(w)) for law 'joint' on outcomes w (dict w->prob)
    a={}; b={}
    for w,pw in joint.items():
        k=(f(w),g(w)); a[k]=a.get(k,0)+pw; kg=g(w); b[kg]=b.get(kg,0)+pw
    return H(a)-H(b)
def saw(n):
    while True:
        pts=[(0,0)]; s={(0,0)}; ok=True
        for _ in range(n):
            x,y=pts[-1]; c=[(x+a,y+b) for a,b in [(1,0),(-1,0),(0,1),(0,-1)] if (x+a,y+b) not in s]
            if not c: ok=False;break
            q=random.choice(c); pts.append(q); s.add(q)
        if ok: return pts
primes=[5,13,17,29,37]
worst46=1e9; worstmix=1e9; cnt=0
for trial in range(30):
    walk=saw(60); n=random.randint(3,12)
    starts=random.sample(range(0,40),random.randint(1,3))
    ptau={t:random.random() for t in starts}; s0=sum(ptau.values()); ptau={t:v/s0 for t,v in ptau.items()}
    # outcomes w = (t, X, Y, coin)
    joint={}
    for t,pt in ptau.items():
        E=walk[t:t+n+1]
        pairs={}
        for x in E:
            for y in E:
                hh=(x[0]-y[0],x[1]-y[1])
                if hh not in pairs: pairs[hh]=(x,y)   # fixed deterministic rule: first found
        for hh,(x,y) in pairs.items():
            for coin in (0,1):
                w=(t,x,y,coin); joint[w]=joint.get(w,0)+pt/len(pairs)/2
    for _ in range(6):
        b=random.randint(1,3)
        idx=random.sample(primes,b+1); S=idx[:b]; j=idx[b]
        sg={p:random.choice([1,-1]) for p in idx}
        mp={p:rmap(p,sg[p]) for p in idx}
        Bx=lambda w: tuple(mp[p](w[1]) for p in S)
        By=lambda w: tuple(mp[p](w[2]) for p in S)
        hj=lambda w: mp[j]((w[1][0]-w[2][0],w[1][1]-w[2][1]))
        hfull=lambda w: (w[1][0]-w[2][0],w[1][1]-w[2][1])
        FX=lambda w: mp[j](w[1]); FY=lambda w: mp[j](w[2])
        lhs=Hcond(joint,hj,lambda w:(Bx(w),By(w)))
        rhs=Hcond(joint,FX,Bx)+Hcond(joint,FY,By)-Hcond(joint,FX,lambda w:(Bx(w),By(w),hfull(w)))
        worst46=min(worst46,rhs-lhs); cnt+=1
        # mixture step for this fixed signed set S
        HV=H({k:v for k,v in _acc(joint,lambda w: tuple(mp[p](w[1] if w[3]==0 else w[2]) for p in S)).items()}) if False else None
        def law(fn):
            d={}
            for w,pw in joint.items():
                k=fn(w); d[k]=d.get(k,0)+pw
            return d
        hv=H(law(lambda w: tuple(mp[p](w[1] if w[3]==0 else w[2]) for p in S)))
        hx=H(law(lambda w: tuple(mp[p](w[1]) for p in S))); hy=H(law(lambda w: tuple(mp[p](w[2]) for p in S)))
        worstmix=min(worstmix, hv-(hx+hy)/2)
print(f"(4.6) checks={cnt}: min(RHS-LHS) = {worst46:.3e} (>=0 required)")
print(f"mixture: min(H(F_S V) - (H(F_S X)+H(F_S Y))/2) = {worstmix:.3e} (>=0 required)")
