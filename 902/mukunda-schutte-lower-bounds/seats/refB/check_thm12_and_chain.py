"""Referee B: Theorem 1.2 arithmetic (printed p.4) in exact rationals, the table rows of Table 1,
and a random high-precision test of the integral comparison in the proof of Lemma 4.3 (p.5)."""
from fractions import Fraction as Fr
from math import comb
import random, mpmath as mp
P = lambda n: (2 * n + 5) * 2 ** (n - 2)
Lam = lambda n: Fr((n + 1) * comb(2 * n + 3, n - 1), comb(n + 2, 3))
print('Lambda(5) =', Lam(5), '=', float(Lam(5)), ' P(5) =', P(5), ' Lambda(4) =', Lam(4), float(Lam(4)), ' P(4)=', P(4))
bad = [n for n in range(5, 3001) if not Lam(n) > P(n)]
print('Lambda(n) > P(n) fails for n in [5,3000]:', bad)
ratio_ok = all(Lam(n + 1) / Lam(n) == Fr(2 * (n + 2) ** 2 * (2 * n + 5), (n + 1) * (n + 3) * (n + 5)) for n in range(3, 600))
poly_ok = all(2 * (n + 2) ** 2 * (2 * n + 5) - 3 * (n + 1) * (n + 3) * (n + 5) == n**3 - n**2 - 13 * n - 5 for n in range(-20, 200))
print('ratio formula exact n=3..599:', ratio_ok, ' polynomial identity:', poly_ok, ' value at n=5:', 5**3 - 25 - 65 - 5)
print('Case-1 bound N >= Lambda(n)+n-2 vs P(n)-1, n=5..12:', [(n, float(Lam(n) + n - 2), P(n) - 1) for n in range(5, 13)])
print('Table row (n+2)2^(n-1)-1:', [(n + 2) * 2 ** (n - 1) - 1 for n in range(2, 13)])
print('Table row Thm1.2 (n+5/2)2^(n-1)-1:', [(2 * n + 5) * 2 ** (n - 2) - 1 for n in range(4, 13)])
# integral comparison: G(m,h) = ln C(m,n)/C(m-h,n) >= n*Phi((m+1)/n, h/n), for m-h>=n, h>=1
mp.mp.dps = 40
F = lambda x: mp.mpf(0) if x == 1 else mp.log(x) - (x - 1) * mp.log1p(-1 / x)
Phi = lambda a, b: F(a) - F(a - b)
random.seed(1126)
worst = mp.inf; cnt = 0
for _ in range(4000):
    n = random.choice([random.randint(1, 30), random.randint(30, 3000)])
    h = random.randint(1, 5 * n)
    m = h + n + random.randint(0, 5 * n)
    G = mp.log(mp.binomial(m, n)) - mp.log(mp.binomial(m - h, n))
    r = n * Phi(mp.mpf(m + 1) / n, mp.mpf(h) / n)
    worst = min(worst, G - r); cnt += 1
print(f'integral comparison G - n*Phi >= 0 on {cnt} random (n,m,h), n up to 3000: min slack {mp.nstr(worst, 6)}')
