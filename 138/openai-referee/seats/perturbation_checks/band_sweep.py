#!/usr/bin/env python3
"""Deterministic adversarial sweep (1-D reduction of perturb:multiplicity).
Points t = delta + j*g (j integer), band m <= t^2 + C' < m+1, exact rationals.
g = separation (paper: 1). Report the largest band population.
Usage: band_sweep.py G"""
import sys
from fractions import Fraction as F
from math import floor
g = F(sys.argv[1]); worst = 0; arg = None
for di in range(0, 200):                     # delta in [0, g)
    delta = g * F(di, 200)
    for ci in range(0, 401):                 # C' in [0, 8] step 1/50, plus integer +- tiny
        for Cp in (F(ci, 50), F(ci, 50) + F(1, 10**9)):
            pop = {}
            for j in range(-12, 13):
                t = delta + j * g
                m = floor(t * t + Cp)
                pop[m] = pop.get(m, 0) + 1
            b = max(pop.values())
            if b > worst: worst, arg = b, (delta, Cp)
print(f"g={g}: largest band population {worst} at (delta, C')={arg}")
sys.exit(0 if worst <= 4 else 1)
