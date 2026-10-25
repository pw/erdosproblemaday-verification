#!/usr/bin/env python3
"""Exact least preimages of Euler's phi for EVERY y-smooth a with exponent vector <= X (componentwise).
Every preimage n of a y-smooth a is a product of prime powers q^f with q^(f-1)(q-1) | a, so q-1 is y-smooth and
f >= 2 only for q <= y. Hence l(a) = min over exact covers of the exponent vector of a by
  - "free primes" q > y with q-1 y-smooth (each used at most once):  vector v(q-1), cost log(q/(q-1))
  - for each p <= y, at most ONE power p^f (f>=1; p=2 needs f>=2):   vector v(p-1) + (f-1)e_p, cost log(p/(p-1))
R(a) = l(a)/a = exp(min cost). Dynamic programme over the whole lattice at once (0/1 for free primes, group for powers).
Primality of d+1: sympy.isprime (BPSW above 2^64; BPSW never rejects a prime, so no true preimage is missed;
a BPSW pseudoprime could only ADD a fake cheaper cover, i.e. make R look smaller - conservative for a seed claim).
Usage: smoothdp.py "2,3,5" "30,20,12" [--top N]
"""
import sys, math, itertools, numpy as np
from sympy import isprime, primerange
P = [int(t) for t in sys.argv[1].split(',')]
X = [int(t) for t in sys.argv[2].split(',')]
TOP = int(sys.argv[sys.argv.index('--top')+1]) if '--top' in sys.argv else 15
k = len(P); shape = tuple(x+1 for x in X)
def vec(n):
    v=[0]*k
    for j,p in enumerate(P):
        while n%p==0: n//=p; v[j]+=1
    return v, n
INF = 1e300
cost = np.full(shape, INF); cost[(0,)*k] = 0.0
choice_items = []   # (vector, cost, label)
# free primes q > y, q-1 y-smooth with v(q-1) <= X
nfree=0
for e in itertools.product(*[range(x+1) for x in X]):
    d = 1
    for p,ex in zip(P,e): d *= p**ex
    if d % 2: continue
    q = d+1
    if q <= P[-1]: continue
    if isprime(q):
        choice_items.append((e, math.log(q/(q-1)), q)); nfree+=1
def shifted(arr, v):
    # out[x] = arr[x - v] (INF where x - v < 0)
    out = np.full(arr.shape, INF)
    src = tuple(slice(0, s - vi) for s,vi in zip(arr.shape, v))
    dst = tuple(slice(vi, s) for s,vi in zip(arr.shape, v))
    if all(s - vi > 0 for s,vi in zip(arr.shape, v)):
        out[dst] = arr[src]
    return out
for (e, c, q) in choice_items:
    cost = np.minimum(cost, shifted(cost, e) + c)
    cost = np.minimum(cost, shifted(cost, e) + c)
# groups: powers of each p <= y
for j,p in enumerate(P):
    base, rest = vec(p-1); assert rest == 1, "p-1 must be y-smooth for p in the base (true for consecutive small primes)"
    old = cost.copy(); new = cost.copy()
    for f in range(1, X[j]+2):
        if p == 2 and f == 1: continue   # 2*odd is never least
        v = list(base); v[j] += f-1
        if any(vi > xi for vi,xi in zip(v, X)): break
        new = np.minimum(new, shifted(old, v) + math.log(p/(p-1)))
    cost = new
R = np.exp(np.where(cost < 1e299, cost, np.nan))
fin = ~np.isnan(R)
print(f"base {P} bounds {X}: lattice {cost.size}, free primes {nfree}, totients in lattice {int(fin.sum())}")
flat = [(R[idx], idx) for idx in zip(*np.nonzero(fin))]
flat.sort(reverse=True)
if '--odd' in sys.argv: flat=[t for t in flat if any(int(u)>0 for u in t[1][1:])]
for thr in (2.0,2.01,2.05,2.1,2.5,3.0): print(f'  #points with R > {thr}: {sum(1 for t in flat if t[0]>thr)}')
for r, idx in flat[:TOP]:
    a = 1
    for p,ex in zip(P, idx): a *= p**int(ex)
    print(f"  R={r:.9f}  exps={tuple(int(t) for t in idx)}  a={a}  log10(a)={math.log10(a):.1f}")
if '--save' in sys.argv: np.save(sys.argv[sys.argv.index('--save')+1], R)
