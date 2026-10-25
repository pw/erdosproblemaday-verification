#!/usr/bin/env python3
"""Spectral interlacing filter on M-classes (label (a) argument, numeric check).
A = adjacency of H (40 vertices, 6-regular). A^2 = 5I + J - P - Gamma (P = 8 disjoint K5 on the blocks, Gamma = cross-
block codegree-0 pairs, 5-regular). Q = P + Gamma = 5I + J - A^2 has lambda_min >= -1 - 5 = -6 (Weyl), so every
non-principal eigenvalue theta of A has theta^2 <= 11. Block quotient B = N/5 (N[X][X] = 2e(X), N[X][X'] = 0,
N[X][Y] = 5 - M[X][Y]) is symmetric (equal block sizes) and interlaces A: lambda_2(B) <= sqrt(11), lambda_8(B) >= -sqrt(11)."""
import sys, numpy as np
from menum import PAIRS, case_E
TOL = 1e-9
def B_of(j, flat):
    E = case_E(j)
    N = np.zeros((8, 8))
    for X in range(8):
        N[X][X] = 2 * E[X]
    for (X, Y), v in zip(PAIRS, flat):
        N[X][Y] = N[Y][X] = 5 - v
    return N / 5.0
bad = {}; tot = {}
for line in open(sys.argv[1]):
    j, flat, o, s = line.split("\t"); j = int(j); flat = list(map(int, flat.split(",")))
    ev = np.sort(np.linalg.eigvalsh(B_of(j, flat)))[::-1]
    assert abs(ev[0] - 6) < 1e-9, ev
    tot[j] = tot.get(j, 0) + 1
    if ev[1] > 11 ** 0.5 + TOL or ev[-1] < -(11 ** 0.5) - TOL:
        bad[j] = bad.get(j, 0) + 1
for j in sorted(tot):
    print(f"case {j}: classes {tot[j]}, killed by interlacing {bad.get(j, 0)}")
