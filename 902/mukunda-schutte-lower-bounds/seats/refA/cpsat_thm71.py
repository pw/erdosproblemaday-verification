"""CP-SAT version of the local model of Theorem 7.1 (see ilp_thm71.py docstring).
Usage: cpsat_thm71.py j0,j1,...  [time_limit]
j-vector is fixed (WLOG sorted non-increasing by relabelling R); J = sum j.
Prints FEASIBLE witness (re-verified from scratch) or INFEASIBLE / UNKNOWN.
"""
import sys, itertools, time
from ortools.sat.python import cp_model

jvec = ([int(t) for t in sys.argv[1].split(',')] + [0] * 11)[:11]
tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
n = 11
m = cp_model.CpModel()
x = {}
for u, v in itertools.combinations(range(n), 2):
    x[(u, v)] = m.NewBoolVar(f"x{u}_{v}")


def beat(w, u):  # literal "w -> u"
    return x[(w, u)] if w < u else x[(u, w)].Not()


for u in range(n):
    m.Add(sum(beat(u, v) for v in range(n) if v != u) == 5)
subsets = [S for k in range(5, n + 1) for S in itertools.combinations(range(n), k)]
ns = [m.NewIntVar(0, 38, f"n{i}") for i in range(len(subsets))]
m.Add(sum(ns) == 38)
for r in range(n):
    m.Add(sum(ns[i] for i, S in enumerate(subsets) if r not in S) == 20 + jvec[r])
triples = list(itertools.combinations(range(n), 3))
allb = []
for U in triples:
    bs = []
    for w in range(n):
        if w in U:
            continue
        b = m.NewBoolVar(f"b{w}_{U}")
        lits = [beat(w, u) for u in U]
        for l in lits:
            m.AddImplication(b, l)
        m.AddBoolOr([l.Not() for l in lits] + [b])
        bs.append(b)
        allb.append(b)
    out = [ns[i] for i, S in enumerate(subsets) if not (set(S) & set(U))]
    m.Add(sum(bs) + sum(out) >= 5)
m.Add(sum(allb) == 110)  # redundant: each w dominates C(5,3)=10 triples of R
# symmetry breaking compatible with fixed sorted j: nothing further (keep it simple)
s = cp_model.CpSolver()
s.parameters.max_time_in_seconds = tl
s.parameters.num_workers = 1
t0 = time.time()
st = s.Solve(m)
name = s.StatusName(st)
print(f"j={jvec} J={sum(jvec)}: {name} in {time.time()-t0:.1f}s", flush=True)
if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    import numpy as np
    A = np.zeros((n, n), int)
    for (u, v), var in x.items():
        if s.Value(var):
            A[u, v] = 1
        else:
            A[v, u] = 1
    Q = [(subsets[i], s.Value(ns[i])) for i in range(len(subsets)) if s.Value(ns[i])]
    j = [sum(c for S, c in Q if r not in S) - 20 for r in range(n)]
    mind = min(sum(1 for w in range(n) if w not in U and all(A[w, u] for u in U)) +
               sum(c for S, c in Q if not set(S) & set(U)) for U in triples)
    print("  witness re-check: regular", all(A[u].sum() == 5 for u in range(n)), "j =", j,
          "min triple dominators", mind, "q-sizes", sorted(len(S) for S, c in Q for _ in range(c)))
