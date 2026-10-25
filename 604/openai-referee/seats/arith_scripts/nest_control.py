# Control for the nesting assertion used in endtoend_36.py: replace the paper's nested-shift rule
# (s_{m+1} = s_m + B*l_m) by INDEPENDENT uniform shifts at each scale. The nesting check must now fire,
# and the "first sharing scale" must stop being an ultrametric (classes() transitivity assert).
import numpy as np, math, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from exact_35 import hier_quantities
PTS = [complex(u, b) for u, b in [(0, 0), (1, 0), (0, 1), (2, 1), (3, 3), (5, 2), (1, 4)]]
n = len(PTS); PAIRS = list(itertools.combinations(range(n), 2))
def run(nested, rng):
    th = rng.uniform(0, 2*math.pi); xi = rng.uniform(0, math.log(2)); l0 = math.exp(xi)
    c, s = math.cos(th), math.sin(th)
    X = np.array([[z.real*c + z.imag*s, -z.real*s + z.imag*c] for z in PTS])
    s0 = rng.uniform(0, 1, 2) * l0; sm = s0.copy(); prev = None; first = {}; nest_ok = True
    for m in range(-6, 40):
        l = l0 * 2.0**m
        if not nested: sh = rng.uniform(0, 1, 2) * l
        elif m <= 0: sh = np.mod(s0, l)
        else: sm = sm + rng.integers(0, 2, 2) * (l0 * 2.0**(m-1)); sh = sm
        cells = [tuple(np.floor((X[k] - sh) / l).astype(np.int64)) for k in range(n)]
        if prev is not None:
            for a, b in PAIRS:
                if prev[a] == prev[b] and cells[a] != cells[b]: nest_ok = False
        for pr in PAIRS:
            if pr not in first and cells[pr[0]] == cells[pr[1]]: first[pr] = m
        prev = cells
        if len(first) == len(PAIRS) and m > 12: break
    ultra_ok = True
    try:
        hier_quantities(list(range(n)), {frozenset(pr): F(-first[pr]) for pr in PAIRS})
    except AssertionError:
        ultra_ok = False
    return nest_ok, ultra_ok
rng = np.random.default_rng(7)
for nested in (True, False):
    res = [run(nested, rng) for _ in range(2000)]
    print(f"nested={nested}: nesting violated in {sum(not a for a,_ in res)}/2000 grids; "
          f"first-share depth not an ultrametric in {sum(not b for _,b in res)}/2000")
