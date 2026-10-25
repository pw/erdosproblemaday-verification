#!/usr/bin/env python3
"""How local is the finite contradiction? Core = pure + pair_count + nonempty (+ down), with pair_count imposed only for tetrahedra
S whose overlap with S0 = {0,1,2,3} lies in a given set of sizes. UNSAT with a small set = a proof that only needs those designs."""
import itertools as it, sys
from pysat.solvers import Cadical153
from tensystem_cnf import S4, S3, q, t, L
S0 = frozenset({0,1,2,3})
def cnf(sizes, down=True):
    cl = []
    if down:
        for s in S4:
            for u in it.combinations(sorted(s), 3): cl.append([-q(s), t(u)])
    for u in S3: cl.append([-t(u)] + [q(u | {v}) for v in L if v not in u])
    for s in S4:
        if len(s & S0) not in sizes: continue
        C = [v for v in L if v not in s]
        for p in it.combinations(C, 2):
            xs = [t(set(p) | {w}) for w in C if w not in p]
            for a in it.combinations(xs, 3): cl.append([-q(s)] + [-x for x in a]); cl.append([-q(s)] + list(a))
    cl.append([q(S0)])
    return cl
for down in (True, False):
    for sizes in [(4,), (4,3), (4,2), (4,3,2), (4,3,2,1), (4,3,2,1,0), (4,3,1), (4,2,1), (4,3,0)]:
        with Cadical153(bootstrap_with=cnf(set(sizes), down)) as s:
            print(f"down={down!s:5} designs imposed for |S∩S0| in {sizes}: {'SAT' if s.solve() else 'UNSAT'}")
