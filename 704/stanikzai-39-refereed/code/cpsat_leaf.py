"""Second instrument: OR-tools CP-SAT decides 'clique of size tau?' on a DIMACS leaf. Prints SAT <labels> | UNSAT."""
import sys
from ortools.sat.python import cp_model
path, tau = sys.argv[1], int(sys.argv[2])
n = 0; E = set()
for line in open(path):
    if line[0] == 'p': n = int(line.split()[2])
    elif line[0] == 'e':
        a, b = map(int, line.split()[1:3]); E.add((min(a, b), max(a, b)))
m = cp_model.CpModel()
x = [m.NewBoolVar(f'x{i}') for i in range(n + 1)]
for a in range(1, n + 1):
    for b in range(a + 1, n + 1):
        if (a, b) not in E: m.AddBoolOr([x[a].Not(), x[b].Not()])   # non-adjacent pair: not both
m.Add(sum(x[1:]) >= tau)
sv = cp_model.CpSolver()
sv.parameters.num_workers = 1
sv.parameters.max_time_in_seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 900.0
st = sv.Solve(m)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print('SAT', ' '.join(str(i) for i in range(1, n + 1) if sv.Value(x[i])))
elif st == cp_model.INFEASIBLE: print('UNSAT')
else: print('UNKNOWN', sv.StatusName(st))
