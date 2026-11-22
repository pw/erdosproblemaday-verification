"""Enumerate all labelled {I3,L3}-free oriented graphs on 8 vertices with own SAT encoding,
then compare with the S8-orbit of Bermond's Z8 graph (x->x+1, x->x-2)."""
import sys, time, itertools
sys.path.insert(0, '/tmp/e1122/seatO')
from enc import Enc
from check import check
from pysat.solvers import Solver

def enumerate_all(n, k, sname):
    e = Enc(n, k)
    arcvars = [(i, j, e.a(i, j)) for i in range(n) for j in range(n) if i != j]
    sols = set()
    t = time.time()
    with Solver(name=sname, bootstrap_with=e.cnf.clauses) as s:
        while s.solve():
            m = set(l for l in s.get_model() if l > 0)
            arcs = frozenset((i, j) for i, j, v in arcvars if v in m)
            sols.add(arcs)
            s.add_clause([-v if v in m else v for _, _, v in arcvars])
    return sols, time.time() - t

for sname in ('cadical195', 'glucose4'):
    sols, dt = enumerate_all(8, 3, sname)
    bad = [a for a in sols if (lambda c: c['tt'] or c['indep'] or c['two_cycles'])(check(8, a, 3))]
    print(f"n=8 k=3 {sname}: {len(sols)} labelled solutions in {dt:.1f}s; failing brute check: {len(bad)}")

B = {(x, (x + 1) % 8) for x in range(8)} | {(x, (x - 2) % 8) for x in range(8)}
c = check(8, B, 3)
print("Bermond Z8 graph:", c)
orbit = set()
aut = 0
for p in itertools.permutations(range(8)):
    img = frozenset((p[a], p[b]) for a, b in B)
    orbit.add(img)
    aut += (img == frozenset(B))
print(f"orbit size {len(orbit)}, |Aut| = {aut}, 8!/|Aut| = {40320 // aut}")
print("enumerated set == orbit of Bermond:", sols == orbit)
for n, k in [(3, 2), (4, 2), (9, 3)]:
    s, dt = enumerate_all(n, k, 'cadical195')
    print(f"control count n={n} k={k}: {len(s)} labelled ({dt:.2f}s)")
