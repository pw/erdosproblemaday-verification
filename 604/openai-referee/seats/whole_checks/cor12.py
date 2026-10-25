# Finite check of Corollary 1.2's counting step (paper p.2) and of the Lean bound (Pins.lean, bad_fraction_bound).
# Exact: integer coordinates, squared distances as Python ints; n^x as floats only in the threshold comparisons.
import itertools, math, random, sys
from collections import Counter

def stats(P, eps):
    n = len(P); s = eps/2
    rich = 0; bad = 0; worst = None
    for x in P:
        cls = Counter((y[0]-x[0])**2 + (y[1]-x[1])**2 for y in P if y != x)
        nd = len(cls)                                   # |D_x(P)| : distinct nonzero distances at pin x
        r_x = sum(c for c in cls.values() if c >= n**s) # targets y with k_P(x,y) >= n^s
        rich += r_x
        if nd < n**(1-eps): bad += 1
    return n, rich, bad

def configs():
    for k in (5, 8, 12, 16):
        yield f"grid{k}x{k}", [(i,j) for i in range(k) for j in range(k)]
    # circle of radius^2 = 5^2*13^2*17^2 lattice points + centre (many lattice points on one circle)
    R2 = (5*13*17)**2
    r = math.isqrt(R2); circ = set()
    for a in range(-r, r+1):
        b = math.isqrt(R2-a*a)
        if a*a+b*b == R2: circ |= {(a,b),(a,-b)}
    circ = sorted(circ); yield f"circle({len(circ)})+centre", circ+[(0,0)]
    yield f"circle+centre+5far", circ+[(0,0)]+[(10**7+3*i*i+i, 7*i+11) for i in range(5)]
    random.seed(1)
    yield "random60", list({(random.randrange(10**6), random.randrange(10**6)) for _ in range(60)})
    yield "grid10+line", [(i,j) for i in range(10) for j in range(10)] + [(i, 100) for i in range(30)]

ok_paper = ok_lean = True; control_fail = False
for name, P in configs():
    for eps in (0.2, 0.4, 0.6, 0.9):
        n, R, b = stats(P, eps)
        # paper: b*(n-1-n^{1-eps/2}) <= R   (when the bracket is positive)
        lhs = b*(n-1-n**(1-eps/2)); paper = (lhs <= R + 1e-9)
        # Lean: b/n <= 2*R/(n(n-1)) + 2*n^{1-eps/2}/n
        lean = (b/n <= 2*R/(n*(n-1)) + 2*n**(1-eps/2)/n + 1e-12)
        # CONTROL (deliberately wrong): drop the light-target term, i.e. claim every bad pin's n-1 targets are rich: b*(n-1) <= R
        ctrl = (b*(n-1) <= R)
        ok_paper &= paper; ok_lean &= lean
        if b > 0 and not ctrl: control_fail = True
        print(f"{name:18s} n={n:4d} eps={eps:.1f} bad={b:4d} richpairs(eps/2)={R:6d} paper_ineq={paper} lean_ineq={lean} WRONG_control_holds={ctrl}")
print("PAPER INEQUALITY HOLDS ON ALL:", ok_paper, "| LEAN INEQUALITY HOLDS ON ALL:", ok_lean, "| wrong control rejected somewhere:", control_fail)
