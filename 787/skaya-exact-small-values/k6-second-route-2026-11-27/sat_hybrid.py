"""Part (b), throughput driver (same mathematics as sat_tasks.py with ORDER_ATOMS=1):
formula = OUR encoding (s-variables, AMO, ORDER2, edges, every 7-subset has an edge) + OUR order atoms
+ every archive core certified by OUR checker + our own CEGAR cores; each case split into their (u_low, u_high) tasks
(passed as assumptions / unit clauses), the split's exhaustiveness checked mechanically per case.
Engine per task: incremental CaDiCaL 1.9.5 (pysat) with a conflict budget; if the budget runs out, the task goes to the
kissat binary (fresh run, the same clauses streamed on stdin + the task's unit clauses).
SAT answers from either engine go through the CEGAR step (exact Farkas certificate by OUR routine, re-checked; or an
exact rational point = counterexample candidate, stop).
Resumable: results appended to tasks_hybrid.jsonl; tasks already UNSAT in tasks_oa.jsonl / tasks_hybrid.jsonl skipped.
Usage: sat_hybrid.py BUDGET_CONFLICTS CASE [CASE ...] | BUDGET_CONFLICTS all"""
import sys, os, time, json, threading, subprocess
D = '/home/exedev/MathDyad/subs-1126/787/check'
sys.path.insert(0, D)
from cegar_pos import farkas
from check_certs import certify
from controls_certify import exact_point
from sat_close import TRIP, s, base_clauses, load_cores, case_assumptions, RISK, NV, m
from sat_tasks import tasks_for_case, split_exhaustive
from write_cnf import order_atoms
from pysat.solvers import Solver
KISSAT = '/home/exedev/MathDyad/tools/kissat/build/kissat'

def main():
    budget = float(sys.argv[1]); args = sys.argv[2:]
    cases = RISK if args == ['all'] else [None if a == 'None' else int(a) for a in args]
    out = os.path.join(D, 'tasks_hybrid.jsonl'); done = set()
    for fn in ('tasks_oa.jsonl', 'tasks_hybrid.jsonl'):
        p = os.path.join(D, fn)
        if os.path.exists(p):
            for line in open(p):
                r = json.loads(line)
                if r['status'] == 'UNSAT': done.add((str(r['case']), str(r['task'])))
    t0 = time.time()
    base, nb, no = base_clauses(); sconstr = base[:nb + no]
    base = base + order_atoms(); nvars = NV + len(TRIP)
    cores, extra = load_cores()
    body = ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in base + cores).encode()
    nbody = len(base) + len(cores)
    S = Solver(name='cadical195'); S.append_formula(base); S.append_formula(cores); S.append_formula(extra)
    extra_cls = list(extra)
    print(f"loaded {nbody} clauses (+{len(extra)} extra) in {time.time()-t0:.1f}s; body {len(body)/1e6:.0f} MB", flush=True)

    def kissat(units):
        cls = extra_cls + [[u] for u in units]
        hdr = f"p cnf {nvars} {nbody + len(cls)}\n".encode()
        tail = ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in cls).encode()
        p = subprocess.run(['nice', '-n', '19', KISSAT, '--quiet'], input=hdr + body + tail, capture_output=True, timeout=3600)
        if p.returncode == 20: return False, None
        if p.returncode == 10:
            lits = [int(x) for ln in p.stdout.decode().splitlines() if ln.startswith('v') for x in ln[1:].split()]
            mod = [0] * (nvars + 1)
            for x in lits:
                if x != 0: mod[abs(x)] = x
            return True, [mod[v] for v in range(1, nvars + 1)]
        raise RuntimeError(f"kissat exit {p.returncode}: {p.stderr[-500:]}")

    def cegar_step(model, c, key):
        E = [t for t in TRIP if model[s(*t) - 1] > 0]
        y = farkas(m, E)
        if y is None:
            pt = exact_point(m, E)
            rec = {'case': c, 'task': key, 'status': 'FEASIBLE_CANDIDATE' if pt else 'UNDECIDED_LP', 'E': E,
                   'point': [str(v) for v in pt] if pt else None}
            print(json.dumps(rec), flush=True)
            with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
            sys.exit(3)
        T = [E[q] for q in range(len(E)) if y[q] != 0]; w = [y[q] for q in range(len(E)) if y[q] != 0]
        assert certify(m, T, w) != 0
        with open(os.path.join(D, 'extra_cores.jsonl'), 'a') as f:
            f.write(json.dumps({'m': m, 'case': c, 'task': key, 'triples': T, 'weights': w}) + '\n')
        cl = [-s(*t) for t in T]; S.add_clause(cl); extra_cls.append(cl)

    for c in cases:
        tasks = tasks_for_case(c)
        ex = split_exhaustive(c, tasks, sconstr)
        tc = time.time(); nk = 0; nnew = 0; ext0 = len(extra_cls)
        for (ul, uh), TA in tasks:
            key = str((ul, uh))
            if (str(c), key) in done: continue
            A = case_assumptions(c) + TA; tt = time.time()
            st0 = S.accum_stats().get('conflicts', 0)
            pr_ok = True                               # (pysat propagate() measured at ~1-2 s per call here: not used)
            if not pr_ok:
                rec = {'case': c, 'task': key, 'status': 'UNSAT', 'formula': 'full+order_atoms', 'engine': 'propagation',
                       'wall_s': round(time.time() - tt, 2)}
                with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
                nnew += 1; continue
            while True:
                S.conf_budget(int(budget))                 # BUDGET = conflicts (pysat's CaDiCaL has no interrupt)
                r = S.solve_limited(assumptions=A)
                engine = 'cadical195'; t_cad = round(time.time() - tt, 2)
                if r is None:
                    engine = 'kissat'; tk = time.time(); r, model = kissat(A); t_kis = round(time.time() - tk, 2)
                else:
                    model = S.get_model() if r else None
                if not r:
                    rec = {'case': c, 'task': key, 'status': 'UNSAT', 'formula': 'full+order_atoms', 'engine': engine,
                           'cadical_conflicts': S.accum_stats().get('conflicts', 0) - st0, 'cadical_s': t_cad,
                           'kissat_s': t_kis if engine == 'kissat' else 0, 'wall_s': round(time.time() - tt, 2)}
                    with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
                    nk += engine == 'kissat'; break
                cegar_step(model, c, key)
            nnew += 1
            if nnew % 25 == 0:
                print(f"  case {c}: {nnew} tasks closed this run ({nk} by kissat), extra cores {len(extra_cls)-ext0}, {time.time()-tc:.0f}s", flush=True)
        ndone = sum(1 for k2, _ in tasks if (str(c), str(k2)) in done) + nnew
        rec = {'case': c, 'tasks': len(tasks), 'tasks_unsat': ndone, 'split_exhaustive': ex, 'kissat_tasks_this_run': nk,
               'extra_cores_this_run': len(extra_cls) - ext0, 'wall_s_this_run': round(time.time() - tc, 1)}
        print(json.dumps(rec), flush=True)
        with open(os.path.join(D, 'cases_hybrid.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
    print(f"done, total {time.time()-t0:.1f}s", flush=True)

if __name__ == '__main__':
    main()
