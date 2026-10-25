#!/usr/bin/env python3
"""#802: the constant c_r that OpenAI's printed constants give (paper §§2-6; the paper does not optimise it).
C = C_r = 16 r^2 (Lemma 2.3); E_C = 42C^2 + 2C, A_C = 10 + E_C, B_C = 2 sqrt(A_C + 1) (Lemma 4.1); a_C = 6(B_C + A_C + 1) (Lemma 5.3);
X(C) = least X >= 32 with 2 a_C log X / sqrt X <= 1/2 (5.6); C_tri(C) = 2(1 + e^X/3) (proof of Thm 3.1); B_r = C_tri(16 r^2) (5.10);
D_r = 3 + (3/2) B_r (6.1); c_r = 1/(16 D_r) (proof of Thm 1.1).  log10 c_r = -(X log10 e) - log10(16 * (1 + 3/(e^X)...)) ~ -(X/ln 10) - log10 16."""
from mpmath import mp, mpf, log, sqrt, findroot
mp.dps = 50
for r in [4, 5, 6, 10]:
    C = mpf(16 * r * r); E = 42 * C**2 + 2 * C; A = 10 + E; B = 2 * sqrt(A + 1); a = 6 * (B + A + 1)
    X = findroot(lambda X: 2 * a * log(X) / sqrt(X) - mpf(1) / 2, mpf('1e19'))
    assert 2 * a * log(X * 1.0000001) / sqrt(X * 1.0000001) < mpf(1) / 2 < 2 * a * log(X * 0.9999999) / sqrt(X * 0.9999999)
    print(f"r={r}  C={int(C)}  a_C={float(a):.4e}  X(C)={float(X):.4e}  log10 c_r = {float(-(X / log(10)) - log(16, 10)):.4e}")
