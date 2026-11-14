import sys, itertools, numpy as np
from fractions import Fraction
sys.path.insert(0,'/home/exedev/MathDyad/erdos704/q51')
from wstruct import WA
N=13
V=[frozenset(c) for c in itertools.combinations(range(N),5)]
idx={s:i for i,s in enumerate(V)}
v=np.zeros(len(V)); 
for s in WA: v[idx[s]]=1
prev=0.0; comps=[]
for j in range(0,6):
    J=[frozenset(c) for c in itertools.combinations(range(N),j)]
    M=np.array([[1.0 if t<=s else 0.0 for t in J] for s in V])
    x,res,rk,sv=np.linalg.lstsq(M,v,rcond=None)
    p=M@x; L=float(p@p); comps.append(L-prev); prev=L
fr=[Fraction(c).limit_denominator(5000) for c in comps]
print('squared lengths:', [str(f) for f in fr], 'float:', [round(c,9) for c in comps])
print('claimed:', ['11/13','32/715','389/77','472/35','347/35','128/35'])
print('sum =', sum(fr))
print('dims', [1,12,65,208,429,572])
def primes(n):
    out=[];d=2
    while d*d<=n:
        while n%d==0: out.append(d); n//=d
        d+=1
    if n>1: out.append(n)
    return out
print('numerator prime factors:', [(f.numerator, primes(f.numerator)) for f in fr])
