"""Cross-check: SAT enumeration count vs own backtracker count on the 13-vertex B8-glue frames."""
import sys, time
sys.path.insert(0, '/tmp/e1122/seatO')
from enc import Enc
def frame(n, k, o, i, fixB):
    e = Enc(n, k)
    P = range(1, 1 + o); Q = range(1 + o, 1 + o + i); I = list(range(1 + o + i, n))
    for p in P: e.fix_arc(0, p)
    for q in Q: e.fix_arc(q, 0)
    for r in I: e.fix_nonadj(0, r)
    if fixB:
        arcs = {(x, (x + 1) % 8) for x in range(8)} | {(x, (x - 2) % 8) for x in range(8)}
        for a in range(8):
            for b in range(8):
                if a < b:
                    if (a, b) in arcs: e.fix_arc(I[a], I[b])
                    elif (b, a) in arcs: e.fix_arc(I[b], I[a])
                    else: e.fix_nonadj(I[a], I[b])
    return e

from pysat.solvers import Solver
for (o, i) in [(2, 2), (3, 1), (1, 3)]:
    e = frame(13, 4, o, i, 1)
    av = [e.a(a, b) for a in range(13) for b in range(13) if a != b]
    t = time.time(); cnt = 0
    with Solver(name='cadical195', bootstrap_with=e.cnf.clauses) as s:
        while s.solve():
            m = set(l for l in s.get_model() if l > 0)
            s.add_clause([-v if v in m else v for v in av]); cnt += 1
    print(f"n=13 glue ({o},{i}) I(0)=B8: SAT enumeration count = {cnt} ({time.time()-t:.1f}s)", flush=True)
