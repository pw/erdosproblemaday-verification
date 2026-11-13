"""Question 5.1 of the submission: is χ(J(13,5,3)) = 39?  Search for a 39-colouring invariant under the cyclic shift
x -> x+1 (mod 13). Such a colouring = 3 independent sets I_1..I_3 of size 33, each a transversal of 33 of the 99
Z_13-orbits of 5-sets, the three groups partitioning the orbits; the 13 shifts of each I_j are the colour classes."""
import sys, json
from itertools import combinations
from ortools.sat.python import cp_model
n, k, t, NC = 13, 5, 3, int(sys.argv[1]) if len(sys.argv) > 1 else 3
V = [frozenset(c) for c in combinations(range(n), k)]
shift = lambda s, c: frozenset((x + c) % n for x in s)
orbits, seen = [], set()
for s in V:
    if s in seen: continue
    o = [shift(s, c) for c in range(n)]
    assert len(set(o)) == n
    seen |= set(o); orbits.append(o)
O = len(orbits); print('orbits', O)
m = cp_model.CpModel()
y = {(a, j, c): m.NewBoolVar(f'y{a}_{j}_{c}') for a in range(O) for j in range(NC) for c in range(n)}
for a in range(O):
    m.AddExactlyOne([y[a, j, c] for j in range(NC) for c in range(n)])
for j in range(NC):
    m.Add(sum(y[a, j, c] for a in range(O) for c in range(n)) == O // NC)
# symmetry: orbit 0 goes to group 0 with representative index 0
m.Add(y[0, 0, 0] == 1)
for a in range(O):
    for b in range(a + 1, O):
        for c in range(n):
            A = orbits[a][c]
            for d in range(n):
                if len(A & orbits[b][d]) == t:
                    for j in range(NC):
                        m.AddBoolOr([y[a, j, c].Not(), y[b, j, d].Not()])
sv = cp_model.CpSolver(); sv.parameters.num_workers = 6; sv.parameters.max_time_in_seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
st = sv.Solve(m); print('status', sv.StatusName(st), 'wall', round(sv.WallTime(), 1))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    base = [[sorted(orbits[a][c]) for a in range(O) for c in range(n) if sv.Value(y[a, j, c])] for j in range(NC)]
    classes = [[sorted(shift(frozenset(s), c)) for s in B] for B in base for c in range(n)]
    allv = [tuple(s) for C in classes for s in C]
    ok = len(classes) == 39 and len(allv) == 1287 and len(set(allv)) == 1287 and all(
        len(set(a) & set(b)) != t for C in classes for a, b in combinations(C, 2))
    print('colouring_ok', ok)
    json.dump(dict(base=base, classes=classes), open('cyc39_solution.json', 'w'))
