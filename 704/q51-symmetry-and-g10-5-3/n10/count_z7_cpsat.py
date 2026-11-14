"""Second count of the g-invariant 21-colourings (g = 7-cycle on 0..6): CP-SAT enumeration of all exact covers of the 36 g-orbits by
three class-orbits, one Boolean per class-orbit (not per support). Independent of count_z7.py's hash-join."""
import json
from itertools import combinations
from ortools.sat.python import cp_model
N = 10
V = [frozenset(c) for c in combinations(range(N), 5)]; IDX = {s: i for i, s in enumerate(V)}
shift = lambda s, t: frozenset((x + t) % 7 if x < 7 else x for x in s)
rep = {}                                   # 5-set -> orbit representative (lexicographically least shift)
for s in V: rep[s] = min(tuple(sorted(shift(s, t))) for t in range(7))
oid = {r: i for i, r in enumerate(sorted(set(rep.values())))}; assert len(oid) == 36
classes = {}                               # canonical class-orbit -> support
for F in json.load(open('mis10_all.json')):
    sets = [V[i] for i in F]; sup = frozenset(oid[rep[s]] for s in sets)
    if len(sup) != 12: continue
    key = min(tuple(sorted(tuple(sorted(shift(s, t))) for s in sets)) for t in range(7))
    classes[key] = sup
keys = list(classes); print('class-orbits:', len(keys))
m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(keys))]
for o in range(36): m.AddExactlyOne([x[i] for i, k in enumerate(keys) if o in classes[k]])
class Cnt(cp_model.CpSolverSolutionCallback):
    def __init__(self): super().__init__(); self.n = 0
    def on_solution_callback(self): self.n += 1
sv = cp_model.CpSolver(); sv.parameters.enumerate_all_solutions = True; sv.parameters.num_workers = 1; cb = Cnt()
st = sv.Solve(m, cb); print('status', sv.StatusName(st), '; colourings counted:', cb.n)
