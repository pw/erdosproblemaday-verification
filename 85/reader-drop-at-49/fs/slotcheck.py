#!/usr/bin/env python3
"""Each H1 slot clause must be IMPLIED by the base anchor formula alone (c4cnf, no SB, no slots): base & not(C) UNSAT."""
import itertools, sys, time
from pathlib import Path
from pysat.solvers import Cadical153
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
n = 49; S = list(range(9))
B = {i: list(range(9 + 5 * (i - 1), 14 + 5 * (i - 1))) for i in range(1, 9)}
fixed = [(0, i) for i in range(1, 9)] + [(1, 2), (3, 4), (5, 6), (7, 8)] + [(i, v) for i in B for v in B[i]]
base, var, F, adjS = c4cnf.build(n, S, fixed, {v: 7 for v in range(9, 49)})
x = lambda a, b: var[(a, b) if a < b else (b, a)]
partner = {1: 2, 2: 1, 3: 4, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7}
ok = bad = unk = 0; t0 = time.time()
with Cadical153(bootstrap_with=base.clauses) as s:
    for i in B:
        for v in B[i]:
            sl = [[x(v, w) for w in B[i] if w != v]] + [[x(v, w) for w in B[j]] for j in B if j not in (i, partner[i])]
            for a_, b_ in itertools.combinations(sl, 2):
                s.conf_budget(20000)
                r = s.solve_limited(assumptions=[-l for l in a_ + b_])
                if r is False: ok += 1
                elif r is True: bad += 1
                else: unk += 1
print(f"slot clauses implied by base: {ok} confirmed UNSAT(base & not C), {bad} SAT (NOT implied!), {unk} undecided; {round(time.time()-t0,1)}s")
# negative control: a clause that is NOT implied (v hits own slot OR one specific part) must come back SAT or undecided, never UNSAT-confirmed
with Cadical153(bootstrap_with=base.clauses) as s:
    v = B[1][0]; s.conf_budget(20000)
    r = s.solve_limited(assumptions=[-l for l in [x(v, w) for w in B[1] if w != v]])
    print("negative control (v misses only its own slot; must NOT be refuted):", {False: "REFUTED (bad)", True: "SAT", None: "undecided"}[r])
