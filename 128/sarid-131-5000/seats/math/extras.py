# Small extra checks: 417/241 ratio, high-precision balancing rho, term count, intro extremal claims (beta by brute force).
import sys, json, itertools, numpy as np
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, '/tmp/erdos1800/seats/math')
from graphs import *
a = Fr(88,417); s = a/(1-a); print("|Y|/|X| at a* =", (1+s)/(1-s), " (claimed 417/241)")
# balancing rho assuming the max sits at a*(rho0) with mu = cap (structure confirmed numerically in lemma45.log)
mp.mp.dps = 30
I0 = mp.mpf(2)/47; g = mp.mpf(3)/64 + mp.mpf(1)/50000000000
def low(r):
    a = I0/(r/2+I0); c = 1-a
    return I0*c**2 - 64*I0**3*a*c**5
high = lambda r: r/8 - r**2/4 + g/4
rb = mp.findroot(lambda r: high(r)-low(r), 0.3183)
print("balancing rho =", mp.nstr(rb, 12), " value =", mp.nstr(high(rb), 12))
print("L-branch check at a*(rb):", mp.nstr(I0/(rb/2+I0),8), "> 1/5")
d = json.load(open('/tmp/erdos1800/claim/erdos-128-sparse-halves/clebsch_tangent_certificate.json'))
print("certificate terms:", len(d['terms']), " all weights > 0:", all(Fr(t['weight'])>0 for t in d['terms']))
# intro: beta of balanced blow-ups of C5 and Petersen, brute force over floor(n/2)-subsets
def beta(A):
    n = len(A); h = n//2; best = None
    for S in itertools.combinations(range(n), h):
        e = A[np.ix_(S,S)].sum()/2
        if best is None or e < best: best = e
    return Fr(int(best), n*n)
for k in (1,2,3,4):
    print(f"C5({k}): n={5*k}, beta = {beta(blowup(cycle(5),[k]*5))}  (1/50 = {Fr(1,50)})")
for k in (1,2):
    print(f"Petersen({k}): n={10*k}, beta = {beta(blowup(petersen(),[k]*10))}")
