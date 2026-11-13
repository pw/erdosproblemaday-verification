"""Question 5.1: chi(J(13,5,3)) = 39?  Ansatz: a colouring invariant under the Frobenius group F_39 = {x -> a x + b mod 13 :
a in {1,3,9}}. No element of F_39 other than the identity fixes a 5-set, so F_39 splits the 1287 vertices into exactly
33 orbits of size 39. A 33-set I meeting every orbit once is a colour class whose 39 images partition the vertices; so
an INDEPENDENT transversal I gives a proper 39-colouring."""
import sys, json
from itertools import combinations
from ortools.sat.python import cp_model
n = 13
V = [frozenset(c) for c in combinations(range(n), 5)]
G = [(a, b) for a in (1, 3, 9) for b in range(n)]
img = lambda g, S: frozenset((g[0] * x + g[1]) % n for x in S)
orbits, seen = [], set()
for S in V:
    if S in seen: continue
    o = sorted({img(g, S) for g in G}, key=sorted)
    assert len(o) == 39
    seen |= set(o); orbits.append(o)
print('orbits', len(orbits))
m = cp_model.CpModel()
y = {(i, j): m.NewBoolVar(f'y{i}_{j}') for i in range(len(orbits)) for j in range(39)}
for i in range(len(orbits)): m.AddExactlyOne([y[i, j] for j in range(39)])
m.Add(y[0, 0] == 1)
for i in range(len(orbits)):
    for k in range(i + 1, len(orbits)):
        for j in range(39):
            for l in range(39):
                if len(orbits[i][j] & orbits[k][l]) == 3: m.AddBoolOr([y[i, j].Not(), y[k, l].Not()])
sv = cp_model.CpSolver(); sv.parameters.num_workers = 4; sv.parameters.max_time_in_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
st = sv.Solve(m); print('status', sv.StatusName(st), 'wall', round(sv.WallTime(), 1))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    I = [orbits[i][j] for i in range(len(orbits)) for j in range(39) if sv.Value(y[i, j])]
    classes = [[img(g, S) for S in I] for g in G]
    allv = [S for C in classes for S in C]
    ok = len(I) == 33 and len(set(allv)) == 1287 and all(len(a & b) != 3 for C in classes for a, b in combinations(C, 2))
    print('colouring_ok', ok)
    json.dump(dict(base=[sorted(S) for S in I], group='x -> a x + b mod 13, a in {1,3,9}',
                   classes=[[sorted(S) for S in C] for C in classes]), open('frob39_solution.json', 'w'))
