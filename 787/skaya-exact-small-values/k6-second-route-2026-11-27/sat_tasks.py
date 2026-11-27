"""Part (b), task-level version of sat_close.py: same formula (OUR encoding + archive cores certified by OUR checker
+ our own CEGAR cores), but each of the 21 cases is solved as their (u_low, u_high) tasks, passed as ASSUMPTIONS to
one incremental CaDiCaL 1.9.5 (learned clauses are consequences of the formula, so they carry across tasks soundly).

Task literals (same as their _encode_subcase / k6_pos_solver.cpp, in OUR variables s(i,j,l) <=> x_i + x_j = x_l):
  case j_elim:  None -> NOT s(i,20,21) for i=0..19;   j -> s(j,20,21)
  p3, t_low, t_high = (18, 19, 20) if j_elim == 19 else (19, 20, 21)
  u_low:  None -> NOT s(i,p3,t_low) for i < p3, i != j_elim;  u -> s(u,p3,t_low)        (u_high likewise with t_high)
  tasks: u_low, u_high in {None} + [i < p3, i != j_elim], skipping u_low >= u_high when both given.
Exhaustiveness of the task split inside each case is CHECKED MECHANICALLY (not by hand): the s-constraints
(AMO + ORDER2) + the case literals + one clause NOT(task) per task must be UNSAT  -> 'split_exhaustive'.

Resumable: per-task results appended to tasks.jsonl, extra cores to extra_cores.jsonl (shared with sat_close.py).
Usage: sat_tasks.py CASE [CASE ...] | all      (CASE = None or 0..19)"""
import sys, os, time, json, itertools
REDUCED = os.environ.get('REDUCED', '0') == '1'
D = '/home/exedev/MathDyad/subs-1126/787/check'
sys.path.insert(0, D)
from cegar_pos import farkas
from check_certs import certify
from controls_certify import exact_point
from sat_close import TRIP, s, base_clauses, load_cores, case_assumptions, RISK, m
from pysat.solvers import Solver

def tasks_for_case(j):
    p3, tl, th = (m - 4, m - 3, m - 2) if j == m - 3 else (m - 3, m - 2, m - 1)
    avail = [i for i in range(p3) if i != j]
    def lits(u, t):
        return [-s(i, p3, t) for i in range(p3) if i != j] if u is None else [s(u, p3, t)]
    out = []
    for ul in [None] + avail:
        for uh in [None] + avail:
            if ul is not None and uh is not None and ul >= uh: continue
            out.append(((ul, uh), lits(ul, tl) + lits(uh, th)))
    return out

def split_exhaustive(j, tasks, sconstr):
    S = Solver(name='cadical195', bootstrap_with=sconstr)
    for a in case_assumptions(j): S.add_clause([a])
    for _, A in tasks: S.add_clause([-a for a in A])      # NOT(conjunction of the task's literals)
    r = S.solve(); S.delete(); return not r

def main():
    args = sys.argv[1:]
    cases = RISK if args == ['all'] else [None if a == 'None' else int(a) for a in args]
    tp = os.path.join(D, os.environ.get('TASKS_FILE', 'tasks.jsonl')); done = set()
    if os.path.exists(tp):
        for line in open(tp):
            r = json.loads(line)
            if r['status'] == 'UNSAT': done.add((str(r['case']), str(r['task'])))
    t0 = time.time()
    base, nb, no = base_clauses()
    sconstr = base[:nb + no]                               # AMO + ORDER2 only (for the exhaustiveness check)
    if REDUCED:
        # keep only the 7-subset clauses containing {19,20,21} or {18,20,21} (a SUBSET of our clauses: weaker, still sound);
        # under each task's assumptions these propagate to exactly their (k-2)-subset-of-R clauses.
        from sat_close import EDGE
        tops = [(19, 20, 21), (18, 20, 21)]; keep = set()
        for top in tops:
            rest = [x for x in range(m) if x not in top]
            for S4 in itertools.combinations(rest, 4):
                keep.add(tuple(sorted(top + S4)))
        base = base[:nb + no + len(EDGE)] + [[EDGE[(a, b)] for a, b in itertools.combinations(sub, 2)] for sub in sorted(keep)]
        print(f"REDUCED formula: {len(keep)} of the 7-subset clauses kept", flush=True)
    cores, extra = load_cores()
    if os.environ.get('ORDER_ATOMS', '0') == '1':
        # OUR order atoms g(i,j,l) <=> x_i + x_j > x_l (i<j<l), variables NV+1+tid.  All clauses true under that reading:
        #   NOT(s and g);  (s or g)(i,j,l) -> g(i,j,l-1) [l-1 > j];  (s or g)(i,j,l) -> g(i+1,j,l) [i+1 < j];
        #   (s or g)(i,j,l) -> g(i,j+1,l) [j+1 < l].   (x_i+x_j >= x_l implies a strictly larger sum exceeds x_l.)
        from sat_close import NV, TID
        def g(i, j, l): return NV + 1 + TID[(i, j, l)]
        oc = []
        for (i, j, l) in TRIP:
            oc.append([-s(i, j, l), -g(i, j, l)])
            succ = []
            if l - 1 > j: succ.append((i, j, l - 1))
            if i + 1 < j: succ.append((i + 1, j, l))
            if j + 1 < l: succ.append((i, j + 1, l))
            for t2 in succ:
                oc.append([-s(i, j, l), g(*t2)]); oc.append([-g(i, j, l), g(*t2)])
        base = base + oc
        print(f"ORDER_ATOMS: +{len(TRIP)} vars, +{len(oc)} clauses", flush=True)
    S = Solver(name='cadical195')
    S.append_formula(base); S.append_formula(cores); S.append_formula(extra)
    if os.environ.get('PHASES', '1') == '1':
        # search heuristic only (no effect on soundness): equalities default FALSE, edges default TRUE, as in their solver
        from sat_close import EDGE
        S.set_phases([-s(*t) for t in TRIP] + list(EDGE.values()))
    print(f"loaded base {len(base)} + archive cores {len(cores)} + extra {len(extra)} in {time.time()-t0:.1f}s", flush=True)
    for c in cases:
        tasks = tasks_for_case(c)
        ex = split_exhaustive(c, tasks, sconstr)
        tc = time.time(); n_extra = 0; n_new = 0
        for (ul, uh), TA in tasks:
            if (str(c), str((ul, uh))) in done: continue
            A = case_assumptions(c) + TA; tt = time.time(); ext = 0
            while True:
                if not S.solve(assumptions=A):
                    rec = {'case': c, 'task': str((ul, uh)), 'status': 'UNSAT', 'formula': 'reduced' if REDUCED else 'full', 'extra_cores': ext, 'wall_s': round(time.time() - tt, 2)}
                    with open(tp, 'a') as f: f.write(json.dumps(rec) + '\n')
                    break
                model = S.get_model()
                E = [t for t in TRIP if model[s(*t) - 1] > 0]
                y = farkas(m, E)
                if y is None:
                    pt = exact_point(m, E)
                    rec = {'case': c, 'task': str((ul, uh)), 'status': 'FEASIBLE_CANDIDATE' if pt else 'UNDECIDED_LP',
                           'E': E, 'point': [str(v) for v in pt] if pt else None}
                    print(json.dumps(rec), flush=True)
                    with open(tp, 'a') as f: f.write(json.dumps(rec) + '\n')
                    return 3
                T = [E[q] for q in range(len(E)) if y[q] != 0]; w = [y[q] for q in range(len(E)) if y[q] != 0]
                assert certify(m, T, w) != 0
                with open(os.path.join(D, 'extra_cores.jsonl'), 'a') as f:
                    f.write(json.dumps({'m': m, 'case': c, 'task': str((ul, uh)), 'triples': T, 'weights': w}) + '\n')
                S.add_clause([-s(*t) for t in T]); ext += 1
            n_extra += ext; n_new += 1
            if n_new % 20 == 0:
                print(f"  case {c}: {n_new} tasks closed this run, extra cores {n_extra}, {time.time()-tc:.0f}s", flush=True)
        ndone = sum(1 for (ul, uh), _ in tasks if (str(c), str((ul, uh))) in done) + n_new
        rec = {'case': c, 'tasks': len(tasks), 'tasks_unsat': ndone, 'split_exhaustive': ex, 'extra_cores_this_run': n_extra,
               'wall_s_this_run': round(time.time() - tc, 1)}
        print(json.dumps(rec), flush=True)
        with open(os.path.join(D, os.environ.get('TASKS_FILE', 'tasks.jsonl').replace('tasks', 'cases_tasks')), 'a') as f: f.write(json.dumps(rec) + '\n')
    print(f"done, total {time.time()-t0:.1f}s", flush=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
