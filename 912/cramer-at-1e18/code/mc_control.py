#!/usr/bin/env python3
# Monte Carlo control for model.c: simulate the Cramér model and the z=5 sieve model at n = 10^6,
# J = #{k : some selected l in (s, n] has n//l = k}; compare the sample mean with model.c's E[J].
import numpy as np, math, sys
n = 10**6; s = math.isqrt(n)
l = np.arange(s + 1, n + 1, dtype=np.int64)
k = n // l
q = 1.0 / np.log(l.astype(float))
cop = (l % 2 != 0) & (l % 3 != 0) & (l % 5 != 0)
theta5 = 2 * 1.5 * 1.25
rng = np.random.default_rng(912)
T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
for name, prob in (("cramer", q), ("z=5", np.where(cop, theta5 * q, 0.0))):
    Js = []
    for _ in range(T):
        sel = rng.random(l.size) < prob
        Js.append(np.unique(k[sel]).size)
    Js = np.array(Js, float)
    print(f"{name}: mean J = {Js.mean():.2f}  sd = {Js.std(ddof=1):.2f}  se(mean) = {Js.std(ddof=1)/math.sqrt(T):.2f}  T={T}")
