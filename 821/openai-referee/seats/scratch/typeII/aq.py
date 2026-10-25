# Toy check of a_Q(v) <= tau(v) in (6.4): bands of primes, r0 slots per band,
# one fixed slot (band jss, position 0) holds a W-rough integer in [lo,hi].
import itertools, random, math
from sympy import primerange, divisors, factorint
random.seed(2)
bands=[list(primerange(400,800)),list(primerange(100,200)),list(primerange(31,61))]
r0=3; jss=1; W=30; lo,hi=31,4000
def rough(n): return n>1 and min(factorint(n))>W
exc=[n for n in range(lo,hi+1) if rough(n)]
bandof={p:j for j,b in enumerate(bands) for p in b}
def count_lists(v):
  c=0
  for p in divisors(v):
    if not (lo<=p<=hi and rough(p)): continue
    w=v//p
    f=factorint(w)
    if any(q not in bandof for q in f): continue
    ok=True; ways=1
    for j in range(len(bands)):
      mult=[f[q] for q in f if bandof[q]==j]
      need=r0-1 if j==jss else r0
      if sum(mult)!=need: ok=False;break
      ways*=math.factorial(need)//math.prod(math.factorial(m) for m in mult)
    if ok: c+=ways
  return c
worst=0
for t in range(3000):
  lst=[[random.choice(bands[j]) for _ in range(r0)] for j in range(len(bands))]
  lst[jss][0]=random.choice(exc)
  v=math.prod(math.prod(b) for b in lst)
  a=count_lists(v)/math.factorial(r0)**len(bands)
  worst=max(worst,a/len(divisors(v)))
print("max a_Q(v)/tau(v) over samples:",worst)
