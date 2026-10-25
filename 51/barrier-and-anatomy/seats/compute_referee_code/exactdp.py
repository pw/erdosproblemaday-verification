#!/usr/bin/env python3
"""Referee's decorrelated exact DP: least preimage n (exact Python int, no logs/floats) for every a = prod P^x, x <= X.
Primality of free primes q = d+1 by a Lucas (Pocklington-Lehmer) CERTIFICATE using the known factorization of q-1
(no BPSW). Composite test by Miller-Rabin witness (a composite never gets a certificate, so certificate = proof).
Covers: items (vector, multiplier n-factor); each prime used once; base primes p: one power p^f (p=2: f>=2)."""
import sys, itertools, random
P=[int(t) for t in sys.argv[1].split(',')]; X=[int(t) for t in sys.argv[2].split(',')]
k=len(P)
def lucas_cert(q, fac):
    # q prime iff exists g with g^(q-1)=1 and g^((q-1)/p) != 1 for all p | q-1
    if q<4: return q in (2,3)
    # quick composite filter
    if pow(2,q-1,q)!=1: return False
    for g in range(2, 2000):
        if pow(g,q-1,q)!=1: return False
        if all(pow(g,(q-1)//p,q)!=1 for p in fac): return True
    raise RuntimeError("no witness found for %d"%q)
items=[]
for e in itertools.product(*[range(x+1) for x in X]):
    d=1
    for p,ex in zip(P,e): d*=p**ex
    q=d+1
    if q in P or d==1: continue
    if lucas_cert(q,[p for p,ex in zip(P,e) if ex>0]):
        items.append(('free',[e],[q]))
# base groups
for j,p in enumerate(P):
    # vector of p-1
    m=p-1; v=[0]*k
    for i,r in enumerate(P):
        while m%r==0: m//=r; v[i]+=1
    assert m==1
    opts=[]; 
    for f in range(1,200):
        if p==2 and f==1: continue
        w=list(v); w[j]+=f-1
        if any(a>b for a,b in zip(w,X)): break
        opts.append((tuple(w), p**f))
    items.append(('group',opts,None))
INF=None
shape=[x+1 for x in X]
cells=list(itertools.product(*[range(x+1) for x in X]))
best={c:None for c in cells}; best[(0,)*k]=1
def sub(c,v): 
    r=tuple(a-b for a,b in zip(c,v)); return r if min(r)>=0 else None
nfree=0
for kind,vs,qs in items:
    old=dict(best)
    if kind=='free':
        opts=[(tuple(vs[0]),qs[0])]; nfree+=1
    else: opts=vs
    for v,mult in opts:
        for s in itertools.product(*[range(x-vi+1) for x,vi in zip(X,v)]):
            o=old[s]
            if o is None: continue
            c=tuple(a+b for a,b in zip(s,v)); cand=o*mult; bc=best[c]
            if bc is None or cand<bc: best[c]=cand
import pickle
pickle.dump(best,open('exact_%s_%s.pkl'%('-'.join(map(str,P)),'-'.join(map(str,X))),'wb'))
print('free primes (Lucas-certified):',nfree,' totient cells:',sum(1 for c in cells if best[c] is not None))
