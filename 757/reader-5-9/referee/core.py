# Independent reconstruction. Exact rationals; no import from the submission dir.
from fractions import Fraction as F
O=(0,49,75,83,98,101,117,119,121,159,269)
r=F(18,269)
def phi(x): return 101+r*x
def copies(K):
    cs=[]; cur=[F(x) for x in O]
    for j in range(K+1):
        cs.append(frozenset(cur)); cur=[phi(x) for x in cur]
    return cs
def SK(K):
    return sorted(set().union(*copies(K)))
