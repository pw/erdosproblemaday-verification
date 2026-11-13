"""Second leaf instrument: OR-tools CP-SAT (CP/SAT/LP hybrid, unrelated to any branch-and-bound clique code)
decides each leaf of <out>/leaves.txt. Model: x_w in {0,1} per residual vertex; x_a + x_b <= 1 for every pair
adjacent in J (i.e. non-adjacent in Gbar); sum x >= tau. J adjacency recomputed here from the 5-sets.
Usage: cpsat_leaves.py out workers cap_s [ids_file]"""
import sys, json, os, time
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
out, P, cap = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
man = json.load(open(out + '/manifest.json'))
n, s = man['n'], man['s']
V = [frozenset(c) for c in combinations(range(n), 5)]
lines = open(out + '/leaves.txt').read().splitlines()
if len(sys.argv) > 4:
    want = set(open(sys.argv[4]).read().split()); lines = [l for l in lines if l.split()[0] in want]
def solve(line):
    from ortools.sat.python import cp_model
    t = list(map(int, line.split())); lid, tau, vs = t[0], t[1], [x - 1 for x in t[3:]]
    m = cp_model.CpModel()
    x = {w: m.NewBoolVar(str(w)) for w in vs}
    for a, b in combinations(vs, 2):
        if len(V[a] & V[b]) == 3: m.AddBoolOr([x[a].Not(), x[b].Not()])
    m.Add(sum(x.values()) >= tau)
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 1; sv.parameters.max_time_in_seconds = cap
    t0 = time.time(); st = sv.Solve(m)
    name = sv.StatusName(st)
    wit = [w for w in vs if name in ('OPTIMAL', 'FEASIBLE') and sv.Value(x[w])]
    return dict(id=lid, tau=tau, size=len(vs), status=name, wall=round(time.time() - t0, 2), witness=wit)
res = []
with ProcessPoolExecutor(P) as ex:
    for r in ex.map(solve, lines, chunksize=1):
        res.append(r)
F = {L['id']: L['F'] for L in man['leaves']}
bad = 0
for r in res:
    if r['witness']:
        fam = [V[w] for w in r['witness'] + F[r['id']] + [man['v'], man['u']]]
        r['witness_ok'] = len(fam) >= s + 1 and all(len(a & b) != 3 for a, b in combinations(fam, 2))
        bad += not r['witness_ok']
from collections import Counter
c = Counter(r['status'] for r in res)
json.dump(res, open(out + f'/results_cpsat{"_subset" if len(sys.argv) > 4 else ""}.json', 'w'))
print('cpsat', dict(c), 'bad_witness', bad, 'sum_wall', round(sum(r['wall'] for r in res), 1), 'max_wall', max(r['wall'] for r in res))
