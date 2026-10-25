#!/usr/bin/env python3
"""Check 5 mutation (i), sharpened: the hypothesis R >= h in Lemma 7.3 is load-bearing.
Random P,Q conjugates (check5_moment.py) happen to keep the ratio bounded for R < h; the unconjugated
diagonal C = diag(1, B^b, B^e) puts the lattice {x : g(x) large} along coordinate planes, and then
sum g^3/(R^3 I) ~ h/R for R < h.  For R >= h the same C stays bounded (positive side)."""
import numpy as np
from check5_moment import shell, gvals, det_divisors
for (B, k) in ((2, 5), (3, 3)):
    h = B ** k
    for (b, e) in ((k, k), (0, k), (1, k)):
        C = np.diag([1, B ** b % h, B ** e % h]).astype(np.int64)
        Dv, Ev, _ = det_divisors(C[None], h); I = int(Dv[0] * Ev[0])
        row = []
        for R in (1, 2, 4, 8, h, 2 * h):
            X = shell(R); g = gvals(C, X, h)
            row.append((R, round(float((g.astype(np.float64) ** 3).sum()) / (R ** 3 * I), 2)))
        print(f"h={h} C=diag(1,{B}^{b},{B}^{e}) I={I}: (R, sum g^3/(R^3 I)) = {row}")
