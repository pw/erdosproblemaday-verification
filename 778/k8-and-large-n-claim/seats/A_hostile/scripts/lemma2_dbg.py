import math, mpmath as mp
from fractions import Fraction as F
mp.mp.dps = 60
def R_exact(m, l):
    k = 0
    while 5**(k+1) * (2*l + 3) <= 3**(k+1) * (2*m + 3): k += 1
    return 1 + k
for l in range(1, 80):
    for m in range(l, 4000):
        R = R_exact(m, l)
        mi = m; seq=[m]
        for i in range(R):
            if mi < l: print("RECURSION FAIL", l, m, R, seq); break
            mi = math.ceil(F(3, 5) * (mi - 1)); seq.append(mi)
        Rf = 1 + int(mp.floor(mp.log((m + mp.mpf(3)/2)/(l + mp.mpf(3)/2))/mp.log(mp.mpf(5)/3)))
        if Rf != R: print("RFORMULA MISMATCH", l, m, R, Rf, F(2*m+3, 2*l+3))
