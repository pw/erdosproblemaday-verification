"""Seat A: brute numeric check of every inequality chain in Sec 4.3 (odd p) with exact rationals.
For each case, the printed cost bound must be < T(N) (strict, since N >= 9 in all these cases) for every N
allowed by the printed clique lower bound (checked on a window of N above the threshold; the cost bounds are
linear in N or constant while T doubles every two steps, so the window is ample).
Negative control: the same check with the clique lower bound weakened (threshold minus a few) must FAIL
somewhere, proving the check can go red."""
from fractions import Fraction as F
import sys
sys.path.insert(0, "/home/exedev/MathDyad/subs-1116/117/seatA")
from analyze import T

def Cp(p, k): return (p**k - 1) // (p - 1)
WIN = 120
fails = []

def check(name, thr, cost, params, weaken=0):
    bad = []
    for N in range(max(3, thr - weaken), thr + WIN):
        c = cost(N)
        if not (c < T(N)):
            bad.append(N)
    if bad and weaken == 0:
        fails.append((name, params, bad[:3]))
    return bad

def run(weaken=0):
    nbad = 0
    for p in (3, 5, 7, 11, 13):
        for j in range(1, 9):
            sigma = p * j + 1
            # A: abelian noncentral, j >= 2: a <= 1 + C_p(2j) N / sigma, N >= p^2 j + 1
            if j >= 2:
                nbad += bool(check("A", p*p*j + 1, lambda N: 1 + F(Cp(p, 2*j) * N, sigma), (p, j), weaken))
            # B: central, one component, j >= 2: a = p^j + 1, N >= p j + 1 (p >= 5); p=3,j=2 is the 10/7 case
            if j >= 2 and p >= 5:
                nbad += bool(check("B", p*j + 1, lambda N: p**j + 1, (p, j), weaken))
            if p == 3 and j >= 3:
                u, v = divmod(j, 3)
                nbad += bool(check("C", 12*u + 3*v + 1, lambda N: 3**j + 1, (p, j), weaken))
            # D: central, several components: j=2: p^2+1 ; j>=3: C_p(2j); N >= p^2 (j-1) + 1
            if j == 2:
                nbad += bool(check("D2", p*p + 1, lambda N: p*p + 1, (p, j), weaken))
            if j >= 3:
                nbad += bool(check("D", p*p*(j-1) + 1, lambda N: Cp(p, 2*j), (p, j), weaken))
            # E: nonabelian radical, m >= 2
            for m in range(2, 31):
                M = max(p + 1, m + 1)
                b1 = lambda N: Cp(p, m) + F(p**(m-1) * Cp(p, 2*j) * N, sigma)
                # Z(R) != Z(P): N >= max(sigma M, sigma(m+1)+1)
                nbad += bool(check("E1", max(sigma*M, sigma*(m+1)+1), b1, (p, j, m), weaken))
                # Z(R) == Z(P): z = p^(2j+m), cyclic lifts C_p(2j+m) also available; N >= sigma M
                nbad += bool(check("E2", sigma*M, lambda N: min(b1(N), Cp(p, 2*j + m)), (p, j, m), weaken))
    return nbad

n0 = run(0)
print("printed thresholds: failing parameter sets =", n0, fails[:10])
nneg = run(weaken=6)
print("negative control (thresholds weakened by 6): failing parameter sets =", nneg, "(must be > 0)")
assert n0 == 0 and nneg > 0
print("OK")
