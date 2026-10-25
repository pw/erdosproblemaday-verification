"""Exact check of Lemma dichotomy:affinity (05-dichotomy.tex, printed Lemma 5.1).
z_j = a + j b on T^e (rational a,b), J = indices whose representative lies in a half-open box of side W.
Claim: if W <= 2H and 2kH < 1 (the proof only uses W*(j3-j1) <= W*(k-1) < 1), the in-box
representatives are affine in j on J.  Control: W = 1.5/(k-1) must produce non-affine J's."""
import random, sys
from fractions import Fraction as F

def rep_in_box(z, c, W):          # unique real rep of z (mod 1) in [c, c+W) if any (W<1)
    r = (z - c) % 1
    return c + r if r < W else None

def affine_on(J, Z):
    if len(J) <= 2: return True
    j0, j1 = J[0], J[-1]
    return all((Z[j] - Z[j0]) * (j1 - j0) == (Z[j1] - Z[j0]) * (j - j0) for j in J)

def trial(k, e, W, rng, den):
    a = [F(rng.randrange(den), den) for _ in range(e)]
    # step close to a rational with small denominator so that the box is revisited often
    b = []
    for _ in range(e):
        if rng.random() < 0.5:   # near a rational with small denominator: many revisits
            hh = rng.randint(1, 6); t = rng.randrange(hh)
            b.append(F(t, hh) + F(rng.randint(-den//(50*k), den//(50*k)), den))
        else:                    # generic step: revisits come from different laps
            b.append(F(rng.randrange(den), den))
    c = [F(rng.randrange(den), den) - F(1, 2) for _ in range(e)]
    Zs = {}
    for j in range(k):
        reps = [rep_in_box(a[i] + j*b[i], c[i], W) for i in range(e)]
        if all(r is not None for r in reps): Zs[j] = reps
    J = sorted(Zs)
    ok = all(affine_on(J, {j: Zs[j][i] for j in J}) for i in range(e))
    return len(J), ok

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for k in [12, 40, 100]:
    H = F(1, k*k)
    for label, W in [("paper: W=2H, 2kH<1", 2*H), ("edge: W=(1-1/k^3)/(k-1)", (1 - F(1, k**3)) / (k - 1)),
                     ("CONTROL: W=1.5/(k-1)", F(3, 2*(k-1)))]:
        n = bad = big = 0
        for _ in range(4000):
            m, ok = trial(k, 1, W, rng, 10**9)
            if m >= 3:
                n += 1; bad += (not ok)
        print(f"k={k:4d} {label:28s} trials with |J|>=3: {n:5d}   non-affine: {bad}")
