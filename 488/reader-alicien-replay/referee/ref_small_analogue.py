# Small analogues of Lemmas 5-6: smoothness bound H=2^h, block n=2^h x, x=2^(h j), A = H-smooth in [x,2x).
# Brute-force B(n), B(m) and compare to the lemma bounds. Referee scratch.
from math import gcd, lcm, prod
from fractions import Fraction
import numpy as np
def primes_upto(N): return [p for p in range(2,N+1) if all(p%d for d in range(2,int(p**.5)+1))]
def smooth(t,P):
    while t>1:
        for p in P:
            if t%p==0: t//=p; break
        else: return False
    return True
def count_B(A, M):
    cov=np.zeros(M+1,dtype=bool)
    for a in A: cov[a::a]=True
    return np.cumsum(cov)  # cum[k]=B(k)
def phi(n): return sum(1 for u in range(1,n+1) if gcd(u,n)==1)
bad=0
for h in (2,3,4):
    H=2**h; P=primes_upto(H); S=[p for p in P if p>2]; Q=prod(S); ph=prod(p-1 for p in S)
    for j in range(1,6):
        x=2**(h*j); n=H*x
        if n>4*10**6: continue
        A=[a for a in range(x,2*x) if smooth(a,P)]
        # primitivity
        prim=all(b%a for a in A for b in A if a<b)
        O=lambda y:[w for w in range(1,y+1,2) if smooth(w,P)]
        Ox=O(x); On=O(n)
        cum=count_B(A,n); Bn=int(cum[n])
        L5 = Bn <= (h+1)*len(On)
        # brute check: every t in B cap [1,n] is smooth in [x, n]
        aw={w: next(2**e*w for e in range(0,h*j+2) if x<=2**e*w<2*x) for w in Ox}
        assert all(v in A for v in aw.values())
        m=1
        for v in aw.values(): m=lcm(m,v*Q)
        if m>3*10**7:
            print(f"h={h} j={j}: x={x} |A|={len(A)} prim={prim} B(n)={Bn} (h+1)|O(n)|={(h+1)*len(On)} L5={L5}; m={m} too big, skip m-side"); bad+= not L5; continue
        cum_m=count_B(A,m); Bm=int(cum_m[m])
        # T_w sets: build explicitly and check disjoint + exact sizes
        seen=set(); tot=0; disj=True; exact=True
        for w,a in aw.items():
            Tw=[a*u for u in range(1,m//a+1) if gcd(u,Q)==1]
            exact &= len(Tw)==(m//(a*Q))*ph
            st=set(Tw); disj &= not (st & seen); seen|=st; tot+=len(Tw)
        within = all(1<=t<=m for t in seen)
        L6 = Fraction(tot) > Fraction(len(Ox)*m*ph, 2*x*Q)
        ratio=Fraction(Bm,m)/Fraction(Bn,n)
        ok = L5 and disj and exact and within and L6 and tot<=Bm
        bad += not ok
        print(f"h={h} j={j}: x={x} |A|={len(A)} prim={prim} |O(x)|={len(Ox)} |O(n)|={len(On)} B(n)={Bn}<= {(h+1)*len(On)}:{L5} | m={m} B(m)={Bm} sumTw={tot} disj={disj} exact={exact} L6={L6} | ratio={float(ratio):.4f}")
print("FAILURES:",bad)
