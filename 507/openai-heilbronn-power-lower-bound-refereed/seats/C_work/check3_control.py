#!/usr/bin/env python3
"""Instrument control for check3: exact counter vs independent Monte Carlo on prescriptions where the
probability is NONZERO (the first control in check3_tail.py happened to hit a zero-probability case)."""
import numpy as np
from check3_tail import exact_prob, mc_prob
rng = np.random.default_rng(99)
for (B, r, L, name, res) in ((5, 2, 4, "P1 all-0", [[0, 0] for _ in range(9)]),
                             (7, 3, 6, "P2 all-2", [[2, 2] for _ in range(9)]),
                             (3, 2, 4, "ML all-1", [[1, 1] for _ in range(9)])):
    for j in (1, 2):
        pe, c, tot = exact_prob(res, j, B, r, L)
        pm = mc_prob(res, j, B, r, L, 3000000, rng)
        se = (pe * (1 - pe) / 3000000) ** 0.5
        print(f"{name} B={B} r={r} L={L} j={j}: exact {pe:.6f} ({c}/{tot}) vs MC {pm:.6f}  |diff|/se = {abs(pe-pm)/max(se,1e-12):.2f}")
