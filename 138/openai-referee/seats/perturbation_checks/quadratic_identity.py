#!/usr/bin/env python3
"""Exact check of the identity in Lemma perturb:signatures:
  f(n_j) = q^2 ||A + jB||^2 = theta0 + theta1 j + theta2 j^2,
  theta0 = q^2||A||^2, theta1 = 2 q^2 <A,B>, theta2 = q^2 ||B||^2,
and that the signs of (theta0+theta1 j+theta2 j^2 - b), b = 0..B_*, recover
floor(f(n_j)) whenever 0 <= f <= D q^2/4 (B_* = floor(D q^2/4) + 1).
Usage: quadratic_identity.py MODE TRIALS SEED   (MODE = paper | control_no2 | control_scale)"""
import sys, random
from fractions import Fraction as F
from math import floor
mode, TRIALS, rng = sys.argv[1], int(sys.argv[2]), random.Random(int(sys.argv[3]))
bad = 0; floor_bad = 0; checked = 0
for _ in range(TRIALS):
    D = rng.randint(1, 6); q = rng.randint(2, 40); k = rng.randint(2, 30)
    # random affine data with every coordinate of A + jB inside [-1/2, 1/2)
    A = [F(rng.randint(-499, 499), 1000) for _ in range(D)]
    B = [F(rng.randint(-999, 999), 10**6 * k) for _ in range(D)]
    if any(not (-F(1, 2) <= a + j * b < F(1, 2)) for a, b in zip(A, B) for j in range(k)):
        continue
    nA = sum(a * a for a in A); nB = sum(b * b for b in B); AB = sum(a * b for a, b in zip(A, B))
    th0, th1, th2 = q * q * nA, 2 * q * q * AB, q * q * nB
    if mode == "control_no2": th1 = q * q * AB          # deliberately wrong: drop the 2
    if mode == "control_scale": th2 = q * nB            # deliberately wrong: q not q^2
    Bstar = floor(F(D * q * q, 4)) + 1
    for j in range(k):
        f = q * q * sum((a + j * b) ** 2 for a, b in zip(A, B))
        checked += 1
        assert 0 <= f <= F(D * q * q, 4)
        g = th0 + th1 * j + th2 * j * j
        if f != g: bad += 1
        # signs against b = 0..B_* ; floor recovered as (#b with g >= b) - 1
        signs = [(g > b) - (g < b) for b in range(Bstar + 1)]
        rec = sum(1 for sgn in signs if sgn >= 0) - 1
        if rec != floor(f): floor_bad += 1
print(f"mode={mode}: {checked} (j, data) instances, identity mismatches={bad}, floor-recovery mismatches={floor_bad}")
sys.exit(0 if bad == 0 and floor_bad == 0 else 1)
