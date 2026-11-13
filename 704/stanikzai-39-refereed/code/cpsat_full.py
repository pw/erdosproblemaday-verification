"""Gate ground truth with no decomposition: CP-SAT maximum independent set of J(n,5,3) (no symmetry breaking)."""
import sys
from itertools import combinations
from ortools.sat.python import cp_model
n = int(sys.argv[1])
V = list(combinations(range(n), 5))
m = cp_model.CpModel()
x = [m.NewBoolVar(f'x{i}') for i in range(len(V))]
S = [set(a) for a in V]
for i in range(len(V)):
    for j in range(i + 1, len(V)):
        if len(S[i] & S[j]) == 3: m.AddBoolOr([x[i].Not(), x[j].Not()])
m.Add(x[0] == 1)   # vertex-transitivity: WLOG {0,1,2,3,4} is in
m.Maximize(sum(x))
sv = cp_model.CpSolver(); sv.parameters.num_workers = 4; sv.parameters.max_time_in_seconds = float(sys.argv[2])
st = sv.Solve(m)
sol = [V[i] for i in range(len(V)) if sv.Value(x[i])]
ok = all(len(set(a) & set(b)) != 3 for a, b in combinations(sol, 2))
print(n, sv.StatusName(st), 'obj', sv.ObjectiveValue(), 'bound', sv.BestObjectiveBound(), 'witness_ok', ok, 'wall', round(sv.WallTime(), 1))
