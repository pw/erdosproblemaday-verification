#!/usr/bin/env python3
# Heuristic (c): share of steps n -> n+1 at which h moves. By the jump rule, h moves only if n+1 = kQ (Q prime > sqrt(n+1))
# AND exactly one of {class k is empty, class k-1 holds no prime besides Q}. Cramér/Poisson: P(n+1 = kQ) ~ (1/k)(1/log(n/k)),
# p0(k) = exp(-(n/(k(k+1)))/log(n/k)).  density(n) ~ sum_k (1/k)(1/log(n/k)) [p0(k)(1-p0(k-1)) + (1-p0(k))p0(k-1)].
# Limit: (2/log n) * integral_0^inf (e^-u - e^-2u)/u du = 2 log 2 / log n  (Frullani).   Chunked; run under ulimit.
import numpy as np, math
for e in range(5, 19):
    n = 10.0 ** e; K = math.isqrt(int(n)); tot = 0.0; CH = 5_000_000; k0 = 2
    while k0 <= K:
        k = np.arange(k0, min(K, k0 + CH - 1) + 1, dtype=float)
        lam = lambda kk: (n / (kk * (kk + 1))) / np.log(n / kk)
        p0k = np.exp(-lam(k)); p0km = np.exp(-lam(k - 1))
        tot += float(np.sum((p0k * (1 - p0km) + (1 - p0k) * p0km) / (k * np.log(n / k)))); k0 += CH
    print(f"1e{e}: Cramér finite-n move density {tot:.4f}   limit form 2log2/log n = {2*math.log(2)/math.log(n):.4f}", flush=True)
