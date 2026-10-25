# Finite checks for §10 arithmetic, Lemma 10.4, Lemma A.1 (toy brute force), Lemma B.1.
import math, random, itertools
G=0.5772156649015329
print("== §10 numeric constants ==")
f=lambda s: 2*math.exp(G)*math.log(s-1)/s
print("f(2.18)=%.5f  bound 2(1.95)(.166)/2.18=%.5f  e^g=%.5f  H6-log6=%.5f  e^.66=%.5f  log1.18=%.6f  cubic=%.6f"%(
  f(2.18),2*1.95*.166/2.18,math.exp(G),sum(1/j for j in range(1,7))-math.log(6),math.exp(.66),math.log(1.18),.18-.18**2/2+.18**3/3))
print(".94/2.22=%.5f  .95*.94/2.22=%.5f"%(.94/2.22,.95*.94/2.22))
print("f is increasing on [2,4]:", all(f(2+i/1000)<f(2+(i+1)/1000) for i in range(1,2000)))
# Lemma 10.4: sum_{d0<=P^.95, supp in E} W_E(d0)/d0 >= e^-g(.94-o(1))
def primes_upto(n):
    s=bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
def lemma104(P, E, expo=.95):
    E=sorted(E); X=int(P**expo)
    # total product over E of (1-1/(t-1)); zero factor for t=2 handled by requiring 2|d0
    base=1.0; has2=(2 in E)
    for t in E:
        if t>2: base*=(1-1/(t-1))
    # enumerate d0 <= X with all prime factors in E: DFS
    tot=0.0
    Es=[t for t in E if t<=X]
    def dfs(i, d, corr, used2):
        nonlocal tot
        # corr = product over t|d0, t>2 of 1/(1-1/(t-1))
        if (not has2) or used2: tot += base*corr/d
        for j in range(i,len(Es)):
            t=Es[j]
            if d*t> X: break
            dd=d*t; c=corr/(1-1/(t-1)) if t>2 else corr
            while dd<=X:
                dfs(j+1, dd, c, used2 or t==2)
                dd*=t
    dfs(0,1,1.0,False)
    return tot
target=math.exp(-G)*.94
for P in [10**4, 10**5]:
    pr=primes_upto(P-1)
    cases={'all':pr,'odd':[t for t in pr if t>2],'none':[],'only2':[2],'big half':[t for t in pr if t>P**.5],
           'small':[t for t in pr if t<100],'random1/2':[t for t in pr if random.Random(1).random()<.5]}
    for name,E in cases.items():
        v=lemma104(P,E)
        print(f"P={P} E={name:9s} sum={v:.4f}  target e^-g*.94={target:.4f}  {'OK' if v>=target else 'BELOW'}")
    # control: exponent .5 instead of .95 for E=all should fall below the .94 target (~.5 e^-g)
    print(f"P={P} CONTROL exponent .50, E=all: {lemma104(P,pr,.5):.4f} (expect ~ e^-g*.5={math.exp(-G)*.5:.4f} < target)")
# Lemma A.1 brute force: C_l vs main term, small moduli
print("\n== Lemma A.1 toy brute force ==")
from math import gcd
def phi(n):
    r=n; m=n; p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0: m//=p
            r-=r//p
        p+=1
    if m>1: r-=r//m
    return r
def tau(n): return sum(1 for d in range(1,n+1) if n%d==0)
rng=random.Random(7); worst=0; worst_ctrl=0
for trial in range(60):
    H=rng.choice([6,10,12,15,18,20,30,36]); 
    Hp=[p for p in [2,3,5,7] if H%p==0]
    T0=1
    for p in Hp:
        if rng.random()<.5: T0*=p
    T1=rng.choice([1,7,11,13,77]) 
    if gcd(T1,H*T0)!=1: T1=1
    N=H*T0
    C0=rng.choice([c for c in range(1,H) if gcd(c,H)==1]); k0=rng.randrange(T0)
    p0=rng.choice([u for u in range(T0) if gcd(u,T0)==1]) if T0>1 else 0
    p1=rng.choice([u for u in range(T1) if gcd(u,T1)==1]) if T1>1 else 0
    m1=rng.randrange(T1)
    l=rng.choice([1]+[q for q in [1,7,11,13,17,19] if gcd(q,H*T1)==1])
    a=rng.uniform(-500,500); X=rng.uniform(0,3000); b=rng.uniform(-500,500); Y2=rng.uniform(0,3000)
    c=(C0+H*k0)%N
    cnt=0
    for p in range(math.ceil(a), math.floor(a+X)+1):
        if p%l or (p-p0)%T0 or (p-p1)%T1: continue
        for m in range(math.ceil(b), math.floor(b+Y2)+1):
            if (m-m1)%T1==0 and (p*m-c)%N==0: cnt+=1
    main=X*Y2*phi(N)/(l*T1**2*N**2*phi(T0))
    bound=tau(N)**2*math.log(2*N)**2*math.sqrt(N*T0)*(1+X/(l*N)+Y2/N)
    ctrl=X*Y2*phi(N)/(l*T1**2*N**2)   # control: drop the 1/phi(T0) factor
    worst=max(worst,abs(cnt-main)/bound); 
    if T0>2: worst_ctrl=max(worst_ctrl,abs(cnt-ctrl)/max(1,main))
print("max |C_l - main|/explicit-error-shape over 60 random toy instances = %.4f (bounded => consistent)"%worst)
print("CONTROL: max |C_l - main_without_1/phi(T0)| / main (T0>2 cases) = %.3f (should be O(1) large => control fails as it must)"%worst_ctrl)
# Large-X instance to see main term dominate
H,T0,T1,N=12,6,5,72; C0,k0,p0,p1,m1,l=5,2,1,2,3,1
c=(C0+H*k0)%N; X=Y2=20000.0; cnt=0
for p in range(0,20001):
    if (p-p0)%T0 or (p-p1)%T1: continue
    for m in range(0,20001):
        pass
# faster: for each p count m via arithmetic
cnt=0
for p in range(0,20001):
    if (p-p0)%T0 or (p-p1)%T1: continue
    # m mod N determined: p unit mod N?
    if gcd(p,N)!=1: continue
    inv=pow(p,-1,N); r=(c*inv)%N
    # m ≡ r mod N and m ≡ m1 mod T1 -> class mod N*T1
    for mm in range(T1):
        m=r+N*mm
        if (m-m1)%T1==0: break
    M=N*T1
    cnt+= (20000-m)//M+1 if m<=20000 else 0
main=X*Y2*phi(N)/(T1**2*N**2*phi(T0))
print(f"large instance H=12,T0=6,T1=5: C={cnt}, main={main:.1f}, rel.err={(cnt-main)/main:+.5f}")
# Lemma B.1: Buchstab omega -> e^-gamma
print("\n== Lemma B.1: Buchstab omega(u) via delay equation ==")
h=1e-4; n1=int(1/h)
om=[1/(1+i*h) for i in range(n1+1)]   # u in [1,2]
u=2.0; i=n1
# (u w)' = w(u-1): integrate u*w with trapezoid
uw=2*om[-1]
while u<12-1e-12:
    # w(u-1) at index i-n1 and next
    a=om[i-n1]; bb=om[i+1-n1]
    uw+=h*(a+bb)/2; u+=h; i+=1
    om.append(uw/u)
for U in [3,4,6,8,10,12]:
    idx=int(round((U-1)/h)); print(f"omega({U})={om[idx]:.6f}", end="  ")
print(f"\n e^-gamma={math.exp(-G):.6f}; CONTROL e^-gamma*1.01={1.01*math.exp(-G):.6f} differs from omega(12) by {abs(om[-1]-1.01*math.exp(-G)):.2e}")
