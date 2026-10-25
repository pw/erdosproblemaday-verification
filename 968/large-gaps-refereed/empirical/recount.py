# independent recount (numpy, different algorithm/language from gaps.c) at N = 10^6 and 10^7
import numpy as np, sys
LIM = 179424700  # p_{10^7} = 179424673, p_{10^7+1} = 179424691
s = np.ones(LIM + 1, dtype=bool); s[:2] = False
for i in range(2, int(LIM**0.5) + 1):
    if s[i]: s[i*i::i] = False
P = np.flatnonzero(s).astype(np.int64)          # P[0] = p_1 = 2
for N in (10**6, 10**7):
    n = np.arange(1, N + 1, dtype=np.int64)       # n = 1..N
    pn, pn1 = P[:N], P[1:N + 1]
    # p_n/n < p_{n+1}/(n+1)  <=>  (n+1) p_n < n p_{n+1}   (int64 safe here: 1e7 * 2e8 = 2e15)
    inc = int(np.count_nonzero((n + 1) * pn < n * pn1))
    g = (pn1 - pn).astype(np.float64); lp = np.log(pn.astype(np.float64))
    gt = {C: int(np.count_nonzero(g > C * lp)) for C in (1.0, 2.0, 3.0)}
    print(f"N={N} p_N={int(pn[-1])} inc={inc} gt1.0={gt[1.0]} gt2.0={gt[2.0]} gt3.0={gt[3.0]}")
