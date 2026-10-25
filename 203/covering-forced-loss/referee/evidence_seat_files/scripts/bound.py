import sys, json
from fractions import Fraction
sys.path.insert(0, "/tmp/evidence203/scripts")
from pool import pool
B4 = {5: 4, 7: 6, 11: 10, 13: 12}; M4 = Fraction(353, 720)
B5 = {**B4, 17: 16};          M5 = Fraction(1529, 2880)
def bounds(N):
    g, rows = pool(N)
    S = sum(Fraction(1, e) for *_, e in rows)
    ps = {p for p, *_ in rows}
    out = {"pool": S}
    for name, B, M in (("B4", B4, M4), ("B5", B5, M5)):
        if not set(B) <= ps:  # block prime absent: bound is still valid but use B4 instead
            out[name] = None; continue
        out[name] = S - sum(Fraction(1, e) for e in B.values()) + M
    return len(rows), out
for N in [int(x) for x in sys.argv[1:]]:
    n, o = bounds(N)
    print(f"N={N:6d} #pool={n:3d}  pool={o['pool']} (~{float(o['pool']):.6f})  "
          f"B4-bound={o['B4']} (~{float(o['B4']):.6f})  B5-bound={o['B5']} (~{float(o['B5']) if o['B5'] is not None else float('nan'):.6f})  "
          f"=> {'NO COVERING' if min(x for x in o.values() if x is not None)<1 else 'not settled'}")
