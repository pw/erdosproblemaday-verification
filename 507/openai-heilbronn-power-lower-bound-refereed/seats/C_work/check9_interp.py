#!/usr/bin/env python3
"""Extra: (a) Appendix A threshold: the final inequality (n/3)log4 > sqrt(2n)log(2n) + log(2n+1) and the
Bertrand conclusion checked numerically; (b) Section 8 interpolation n <= n_r <= C_k n with C_k = max(1, 4^a D/A)
on toy (alpha, A_k, D_k) using actual primes r in (m, 2m] and the EXTREME admissible n_r (both ends).
Mutation: C_k' = 2^alpha D/A (one factor 2^alpha short) must be violated for some n."""
import math
from sympy import nextprime, primerange
# (a)
f = lambda n: (n / 3) * math.log(4) - math.sqrt(2 * n) * math.log(2 * n) - math.log(2 * n + 1)
last_bad = max(n for n in range(1, 200000) if f(n) <= 0)
print(f"(a) Appendix A inequality (n/3)log4 > sqrt(2n)log(2n)+log(2n+1) fails last at n = {last_bad}; holds for all 1..200000 beyond it")
ok = all(nextprime(n) <= 2 * n for n in range(1, 200001))
print(f"    Bertrand (prime in (n,2n]) verified directly for n = 1..200000: {ok}")
# (b)
viol = 0; mviol = 0; tested = 0
for alpha in (3, 5, 7):
    for (A, D) in ((0.5, 2.0), (0.01, 50.0), (1.0, 1.0)):
        Ck = max(1.0, 4 ** alpha * D / A); Ckm = max(1.0, 2 ** alpha * D / A)
        for n in list(range(int(A) + 1, 3000)) + [10**6, 10**9, 10**12]:
            if (n / A) ** (1 / alpha) < 1: continue
            m = math.ceil((n / A) ** (1 / alpha))
            r = nextprime(m)
            assert m < r <= 2 * m
            for nr in (math.ceil(A * r ** alpha), math.floor(D * r ** alpha)):
                if nr < A * r ** alpha or nr > D * r ** alpha: continue
                tested += 1
                if not (n <= nr <= Ck * n): viol += 1
                if not (n <= nr <= Ckm * n): mviol += 1
print(f"(b) interpolation: {tested} (alpha, A, D, n, extreme n_r) cases; violations of n <= n_r <= C_k n: {viol}; "
      f"MUTATION C_k'=2^alpha D/A violations: {mviol}")
