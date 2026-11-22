#!/usr/bin/env python3
"""Second instrument for Tresmontant's #700(b) theorem (submission yzwb6a), written from scratch.
(1) brute force: f(n) = min over 1<k<=n/2 of gcd(n,C(n,k)) for n=pqr, via LEGENDRE valuations over ALL k (numpy);
(2) exhaustive reduced check (Lucas digits, k = s*t*j) over every hypothesis triple with p <= PMAX.
Exit 0 iff every check comes out as the theorem predicts and every control behaves."""
import sys, math, numpy as np
from sympy import primerange, isprime

def f_brute(p,q,r):
    n=p*q*r; k=np.arange(2, n//2+1, dtype=np.int64); g=np.ones_like(k)
    for s in (p,q,r):
        v=np.zeros_like(k); m=s
        while m<=n:
            v += n//m - k//m - (n-k)//m; m*=s
        g *= np.where(v>0, s, 1)
    return int(g.min())

def digits(x,b):
    d=[]
    while x: d.append(x%b); x//=b
    return d
def dom(a,b,base):          # a <=_base b digitwise
    da,db=digits(a,base),digits(b,base)
    if len(da)>len(db): return False
    return all(x<=y for x,y in zip(da,db))
def ndigits_le(a, b, base):
    """vectorised: for arrays a (any) and scalar b, True where a <=_base b digitwise."""
    a=a.copy(); ok=np.ones(a.shape,bool); bb=b
    while True:
        da=a%base; db=bb%base
        ok &= da<=db
        a//=base; bb//=base
        if bb==0:
            ok &= a==0; break
    return ok
def small_gcd_exists(p,q,r):
    """True iff some 1<k<=n/2 has two of p,q,r not dividing C(n,k) (valid when r<pq)."""
    for (s,t,u) in ((p,q,r),(p,r,q),(q,r,p)):
        j=np.arange(1, u//2+1, dtype=np.int64)
        if np.any(ndigits_le(t*j, t*u, s) & ndigits_le(s*j, s*u, t)): return True
    return False

ok=True
# --- (1) brute force on hypothesis triples (independent of Lucas) ---
def hyp(p,q,r): d,h,e=q-p,r-q,r-p; return h>d and 2*e*e<p
tests=[(101,103,107),(107,109,113),(191,193,197),(227,229,233),(269,271,277),(311,313,317),(347,349,353)]
for (p,q,r) in tests:
    n=p*q*r; f=f_brute(p,q,r); pred = f*f>n
    print(f"brute n={p}*{q}*{r}={n} hyp={hyp(p,q,r)} f={f} f^2>n={pred} f==pq:{f==p*q}")
    ok &= (hyp(p,q,r) and pred) or not hyp(p,q,r)
# control: violates 2e^2<p -> expect f<sqrt n
for (p,q,r),want in [((103,107,113),False),((13,17,23),None)]:
    n=p*q*r; f=f_brute(p,q,r); print(f"control (hyp false) n={n} hyp={hyp(p,q,r)} f={f} f^2>n={f*f>n} (submission says 103*107*113 has f<sqrt n; 13*17*23 just reported)")
    if want is not None: ok &= ((f*f>n)==want)
# control: decreasing gaps h<=d with p large -> expect f=p (< sqrt n)
for (p,q,r) in [(457,461,463)]:
    f=f_brute(p,q,r); print(f"control (h<=d) n={p*q*r} f={f} f^2>n={f*f>p*q*r}"); ok &= f*f<p*q*r
# brute vs reduced agreement on every triple of primes with r<140 (whatever the hypothesis)
P=list(primerange(3,140)); agree=0; dis=0
for i in range(len(P)):
    for j in range(i+1,len(P)):
        for k2 in range(j+1,len(P)):
            p,q,r=P[i],P[j],P[k2]
            if p*q*r>3_000_000 or r>=p*q: continue   # Step 1's reduction needs r<pq
            fb=f_brute(p,q,r); n=p*q*r
            if (fb*fb<=n)==small_gcd_exists(p,q,r): agree+=1
            else: dis+=1; print("DISAGREE",p,q,r,fb)
print(f"brute vs reduced (all triples of odd primes below 140 with r<pq, n<=3e6): agree={agree} disagree={dis}"); ok &= dis==0 and agree>100
# --- (2) exhaustive reduced check over hypothesis triples ---
PMAX=int(sys.argv[1]) if len(sys.argv)>1 else 6000
ps=list(primerange(3, PMAX+400)); cnt=0; bad=0
for a,p in enumerate(ps):
    if p>PMAX: break
    emax=int(math.isqrt((p-1)//2))           # 2e^2<p
    for b in range(a+1,len(ps)):
        q=ps[b]
        if q-p>=emax: break
        for c in range(b+1,len(ps)):
            r=ps[c]
            if r-p>emax or 2*(r-p)**2>=p: break
            if r-q<=q-p: continue
            cnt+=1
            if small_gcd_exists(p,q,r): bad+=1; print("COUNTEREXAMPLE",p,q,r)
print(f"hypothesis triples with p<={PMAX}: {cnt}, with f(n)<=sqrt(n): {bad}"); ok &= bad==0 and cnt>0
print("ALL AS PREDICTED" if ok else "SOMETHING UNEXPECTED"); sys.exit(0 if ok else 1)
