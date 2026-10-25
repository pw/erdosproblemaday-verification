# (g) Lemma 2.1 circle row "a circle contains at most 2M points", M = 1 + |Delta(P)|; and the line row 2M.
# Exact arithmetic: points with exact squared distances via sympy for polygons; integer points for Pythagorean circles.
import itertools, math
from sympy import cos, pi, Rational, nsimplify, simplify, sqrt, S as SS, minimal_polynomial, Symbol
from fractions import Fraction
x = Symbol('x')
def chord_sq(n, k):   # squared chord between vertices k apart on unit circle: 2-2cos(2 pi k/n)
    return simplify(2 - 2*cos(2*pi*Rational(k, n)))
print("== regular n-gon (all vertices on the circle): |Delta| = #distinct chords, M = 1+|Delta|; claim n <= 2M (proof gives n <= 2M-1) ==")
for n in range(3, 25):
    chords = set()
    for k in range(1, n//2+1):
        chords.add(minimal_polynomial(chord_sq(n, k), x))   # exact distinctness via minimal polynomials + numeric
    numvals = sorted(set(round(float(chord_sq(n, k)), 12) for k in range(1, n//2+1)))
    D = len(numvals); M = 1 + D
    print(f"  n={n:2d}: |Delta|={D}, M={M}, 2M={2*M}, n<=2M: {n<=2*M}, n<=2M-1: {n<=2*M-1}{'  <-- equality n=2M-1' if n==2*M-1 else ''}")
print("== regular 2k-gon + centre (centre is off the circle, so the circle still carries 2k points; M can only grow) ==")
for k in range(2, 9):
    n = 2*k
    vals = set(round(float(chord_sq(n, j)), 12) for j in range(1, k+1)); vals.add(1.0)   # radius 1
    M = 1 + len(vals)
    print(f"  2k={n:2d}+centre: |Delta|={len(vals)}, M={M}, circle points {n} <= 2M={2*M}: {n<=2*M}")
print("== exhaustive: every subset (|S|>=2) of vertices of the regular 12-gon and 13-gon; max over subsets of |S| - (2M-1) ==")
for n in (12, 13):
    pts = list(range(n)); best = None
    sqd = {k: round(float(chord_sq(n, k)), 12) for k in range(0, n)}
    for r in range(2, n+1):
        for sub in itertools.combinations(pts, r):
            ds = set(sqd[(b-a) % n] for a, b in itertools.combinations(sub, 2))
            M = 1 + len(ds); excess = r - (2*M - 1)
            if best is None or excess > best[0]: best = (excess, r, M, sub)
    print(f"  n={n}: max (|S| - (2M-1)) = {best[0]} attained e.g. by |S|={best[1]}, M={best[2]}, S={best[3]}")
print("== exhaustive subsets of the 12 integer points on x^2+y^2=25 and the 16 on x^2+y^2=65 (exact integer squared distances) ==")
for R2 in (25, 65):
    P = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if a*a+b*b == R2]
    best = None
    for r in range(2, min(len(P), 12)+1):
        for sub in itertools.combinations(P, r):
            ds = set((a[0]-b[0])**2+(a[1]-b[1])**2 for a, b in itertools.combinations(sub, 2))
            M = 1 + len(ds); excess = r - (2*M-1)
            if best is None or excess > best[0]: best = (excess, r, M, sub)
    print(f"  R^2={R2}: {len(P)} lattice points; max (|S|-(2M-1)) over subsets of size<=12 = {best[0]} (|S|={best[1]}, M={best[2]})")
print("== line row: n collinear points, from an endpoint all distances distinct => n <= M (paper states 2M) ==")
for n in range(2, 12):
    D = len(set(range(1, n))); M = 1 + D
    print(f"  arithmetic progression n={n}: M={M}, n<=M: {n<=M}, n<=2M: {n<=2*M}")
