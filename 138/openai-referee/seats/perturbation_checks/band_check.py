#!/usr/bin/env python3
"""Exact check of the line/norm-band geometry in Lemma perturb:multiplicity.

Claim checked (06-perturbation.tex): points on an affine line, pairwise
Euclidean distance >= SEP (paper: SEP = 1), lying in one half-open band
m <= ||z||^2 < m+1, number at most two on each closed half-line from the
nearest point z_0, hence at most four in total.  We also record the
SHARPER count (at most one per half-open half-line, two in total), which is
what the Lean file KeyMultiplicity.lean actually proves
(affine_norm_band_card_le_two), and the band-interval containment
u <= t^2 <= v with u = max(0, m - C'), v = m + 1 - C'.

Everything is exact rational arithmetic: lines are A + t*B with B = s*e,
e a rational unit vector (inverse stereographic projection), so ||B|| = |s|
is rational and no square root is ever taken.

Usage: band_check.py SEP TRIALS SEED
"""
import sys, random
from fractions import Fraction as F
from math import floor

def rat_unit(D, rng):
    # inverse stereographic projection of a rational point of Q^{D-1}
    x = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(D - 1)]
    nx = F(0) + sum(v * v for v in x)
    e = [2 * v / (nx + 1) for v in x] + [(nx - 1) / (nx + 1)]
    assert sum(v * v for v in e) == 1
    return e

def dot(a, b): return sum(x * y for x, y in zip(a, b))

def trial(D, SEP, rng):
    e = rat_unit(D, rng)
    s = F(rng.randint(1, 40), rng.randint(1, 40))          # ||B|| = s
    B = [s * v for v in e]
    # nearest point z0 orthogonal to e, chosen so that C' = ||z0||^2 is often
    # an integer, or an integer +- a tiny epsilon (adversarial band placement)
    if D >= 2:
        w = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(D)]
        w = [wi - dot(w, e) * ei for wi, ei in zip(w, e)]   # project off e
        nw = dot(w, w)
        target = F(rng.choice([0, 1, 2, 3, 5, 10, 50])) + rng.choice(
            [F(0), F(1, 10**6), -F(1, 10**6), F(rng.randint(0, 99), 100)])
        if nw == 0 or target <= 0:
            z0 = [F(0)] * D
        else:
            # scale w by a rational r with r^2*nw close to target (exact when possible)
            r2 = target / nw
            r = F(round(float(r2) ** 0.5 * 10**6), 10**6)
            z0 = [r * wi for wi in w]
    else:
        z0 = [F(0)]
    # parameter t along B; point = z0 + t*B; separation |t-t'|*s >= SEP
    gap = SEP / s
    t0 = F(rng.randint(-50, 50), rng.randint(1, 50)) * gap     # random offset
    pts = []
    t = t0 - 20 * gap
    for _ in range(41):
        pts.append(t)
        t += gap * rng.choice([1, 1, 1, 1, F(101, 100), F(3, 2), 2])
    # nearest-point parameter is t* = 0 here because z0 is orthogonal to B
    return z0, B, s, pts

def main():
    SEP = F(sys.argv[1]); TRIALS = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    worst_total = worst_half_closed = worst_half_open = 0
    contain_fail = 0
    for it in range(TRIALS):
        D = rng.choice([1, 2, 3, 4])
        z0, B, s, ts = trial(D, SEP, rng)
        Cp = dot(z0, z0)
        bands = {}
        for t in ts:
            P = [a + t * b for a, b in zip(z0, B)]
            f = dot(P, P)
            # identity ||z0 + t B||^2 = (t s)^2 + C'  (z0 orthogonal to B)
            assert f == (t * s) ** 2 + Cp
            bands.setdefault(floor(f), []).append(t * s)   # arclength param
        for m, T in bands.items():
            u = max(F(0), m - Cp); v = m + 1 - Cp
            assert v > 0
            for tt in T:                                  # containment, exact
                if not (u <= tt * tt <= v):
                    contain_fail += 1
            pos = [tt for tt in T if tt >= 0]; neg = [tt for tt in T if tt <= 0]
            worst_total = max(worst_total, len(T))
            worst_half_closed = max(worst_half_closed, len(pos), len(neg))
            worst_half_open = max(worst_half_open, len([tt for tt in T if tt > 0]),
                                  len([tt for tt in T if tt < 0]))
    print(f"SEP={SEP} trials={TRIALS}: max per band={worst_total}, "
          f"max per closed half-line={worst_half_closed}, max per open half-line={worst_half_open}, "
          f"containment failures={contain_fail}")
    ok_paper = worst_total <= 4 and worst_half_closed <= 2 and contain_fail == 0
    ok_sharp = worst_total <= 2
    print("paper claim (<=2 per half, <=4 per band):", "HOLDS" if ok_paper else "REJECTED")
    print("sharp claim (<=2 per band, Lean affine_norm_band_card_le_two):", "HOLDS" if ok_sharp else "REJECTED")
    sys.exit(0 if ok_paper else 1)

main()
