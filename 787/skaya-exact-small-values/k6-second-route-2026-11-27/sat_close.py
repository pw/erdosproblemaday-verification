"""Part (b): close the propositional side of n+(6) <= 21 (no 22 positive reals with alpha <= 6) with OUR encoding.

Encoding = scripts/cegar_pos.py (ours, written 25 Nov, before their v1.1.1): variables s(i,j,l) <=> x_i + x_j = x_l
(i<j<l), AMO per pair over l, AMO per (a,l) over b, ORDER2 order clauses, edge e(i,j) -> OR_l s(i,j,l), and every
7-subset of the 22 indices contains an edge.  Added: one blocking clause OR_t NOT s(t) per certificate of their archive
that OUR checker (check_certs.py) certified (file cores_ourids.txt), plus any core WE find and certify here.

Case split = their 21 cases on j_elim (the unique j with x_j + x_20 = x_21, or none), passed as assumptions:
  None: NOT s(i,20,21) for i = 0..19;   j: s(j,20,21).   Propositionally exhaustive (either some s(i,20,21) is true or none).
Their inner split on (u_low, u_high) (4,010 tasks) is NOT used: the SAT solver covers each whole case.

If a case is SAT: take the model's true s-literals E, find an exact integer Farkas certificate with OUR routine
(cegar_pos.farkas: HiGHS hint -> rational -> exact integer check -> deletion filter), re-check it with check_certs.certify,
add the blocking clause, continue.  If E is LP-feasible: build an exact rational point and stop (counterexample candidate).
Resumable: per-case results in cases.jsonl, our extra cores in extra_cores.jsonl (both re-read on start).
Usage: sat_close.py CASE [CASE ...]   (CASE = None or 0..19; 'all' = all 21 in risk order)"""
import sys, os, time, json, itertools
D = '/home/exedev/MathDyad/subs-1126/787/check'
sys.path.insert(0, D)
from cegar_pos import farkas
from check_certs import certify, TID
from controls_certify import exact_point
from pysat.solvers import Solver

m, k = 22, 6
TRIP = sorted(TID, key=TID.get)
def s(i, j, l): return TID[(i, j, l)] + 1
EDGE = {}
for i in range(m):
    for j in range(i + 1, m):
        EDGE[(i, j)] = len(TRIP) + 1 + len(EDGE)
NV = len(TRIP) + len(EDGE)
RISK = [17, 15, 14, 19, 13, 16, 12, 0, None, 11, 10, 6, 7, 5, 4, 3, 2, 1, 9, 8, 18]

def base_clauses():
    cl = []
    def amo(lits):
        for a, b in itertools.combinations(lits, 2): cl.append([-a, -b])
    for i in range(m):
        for j in range(i + 1, m):
            amo([s(i, j, l) for l in range(j + 1, m)])
    for l in range(m):
        for a in range(l):
            amo([s(min(a, b), max(a, b), l) for b in range(l) if b != a])
    nb = len(cl)
    for (a, b, l) in TRIP:                       # ORDER2 (sound: (a,b) <= (c,d) componentwise, distinct => x_a+x_b < x_c+x_d)
        for (c, d, l2) in TRIP:
            if (a, b) != (c, d) and a <= c and b <= d and l >= l2:
                cl.append([-s(a, b, l), -s(c, d, l2)])
    no = len(cl) - nb
    for (i, j), e in EDGE.items():
        cl.append([-e] + [s(i, j, l) for l in range(j + 1, m)])
    for sub in itertools.combinations(range(m), k + 1):
        cl.append([EDGE[(a, b)] for a, b in itertools.combinations(sub, 2)])
    return cl, nb, no

def case_assumptions(c):
    if c is None: return [-s(i, m - 2, m - 1) for i in range(m - 2)]
    return [s(c, m - 2, m - 1)]

def load_cores():
    cores = []
    with open(os.path.join(D, 'cores_ourids.txt')) as f:
        for line in f:
            cores.append([-(int(x) + 1) for x in line.split()])
    extra = []
    p = os.path.join(D, 'extra_cores.jsonl')
    if os.path.exists(p):
        for line in open(p):
            rec = json.loads(line); T = [tuple(t) for t in rec['triples']]
            assert certify(m, T, rec['weights']) != 0
            extra.append([-s(*t) for t in T])
    return cores, extra

def main():
    args = sys.argv[1:]
    cases = RISK if args == ['all'] else [None if a == 'None' else int(a) for a in args]
    done = {}
    rp = os.path.join(D, 'cases.jsonl')
    if os.path.exists(rp):
        for line in open(rp):
            r = json.loads(line)
            if r['status'] == 'UNSAT': done[str(r['case'])] = r
    t0 = time.time()
    base, nb, no = base_clauses()
    cores, extra = load_cores()
    print(f"vars={NV} base clauses={len(base)} (AMO {nb}, ORDER2 {no}); archive cores={len(cores)}; our extra cores so far={len(extra)}; "
          f"build {time.time()-t0:.1f}s", flush=True)
    S = Solver(name='cadical195')
    S.append_formula(base); S.append_formula(cores); S.append_formula(extra)
    print(f"loaded into cadical195 in {time.time()-t0:.1f}s", flush=True)
    for c in cases:
        if str(c) in done:
            print(f"case {c}: already UNSAT in cases.jsonl, skipped", flush=True); continue
        tc = time.time(); n_extra = 0; sizes = []
        A = case_assumptions(c)
        while True:
            ts = time.time()
            r = S.solve(assumptions=A)
            if not r:
                rec = {'case': c, 'status': 'UNSAT', 'extra_cores': n_extra, 'extra_core_sizes': sizes,
                       'wall_s': round(time.time() - tc, 1), 'last_solve_s': round(time.time() - ts, 1),
                       'archive_cores_loaded': len(cores), 'stats': S.accum_stats()}
                print(json.dumps(rec), flush=True)
                with open(rp, 'a') as f: f.write(json.dumps(rec) + '\n')
                break
            model = S.get_model()
            E = [t for t in TRIP if model[s(*t) - 1] > 0]
            y = farkas(m, E)
            if y is None:
                pt = exact_point(m, E)
                rec = {'case': c, 'status': 'FEASIBLE_CANDIDATE' if pt else 'UNDECIDED_LP', 'E': E,
                       'point': [str(v) for v in pt] if pt else None}
                print(json.dumps(rec), flush=True)
                with open(rp, 'a') as f: f.write(json.dumps(rec) + '\n')
                return 3
            T = [E[q] for q in range(len(E)) if y[q] != 0]; w = [y[q] for q in range(len(E)) if y[q] != 0]
            assert certify(m, T, w) != 0
            with open(os.path.join(D, 'extra_cores.jsonl'), 'a') as f:
                f.write(json.dumps({'m': m, 'case': c, 'triples': T, 'weights': w}) + '\n')
            S.add_clause([-s(*t) for t in T]); n_extra += 1; sizes.append(len(T))
            if n_extra % 25 == 0:
                print(f"  case {c}: {n_extra} extra cores, last |E|={len(E)} core={len(T)}, {time.time()-tc:.0f}s", flush=True)
    print(f"done, total {time.time()-t0:.1f}s", flush=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
