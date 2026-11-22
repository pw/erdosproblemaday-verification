import sys, time, threading
sys.path.insert(0, '/tmp/e1122/seatO')
from enc import Enc
from check import check
from pysat.solvers import Solver

def frame(n, k, o, i, fixB):
    e = Enc(n, k)
    P = range(1, 1 + o); Q = range(1 + o, 1 + o + i); I = list(range(1 + o + i, n))
    for p in P: e.fix_arc(0, p)
    for q in Q: e.fix_arc(q, 0)
    for r in I: e.fix_nonadj(0, r)
    if fixB:
        arcs = {(x, (x + 1) % 8) for x in range(8)} | {(x, (x - 2) % 8) for x in range(8)}
        for a in range(8):
            for b in range(8):
                if a < b:
                    if (a, b) in arcs: e.fix_arc(I[a], I[b])
                    elif (b, a) in arcs: e.fix_arc(I[b], I[a])
                    else: e.fix_nonadj(I[a], I[b])
    return e

def run(e, label, sname, limit):
    t = time.time()
    with Solver(name=sname, bootstrap_with=e.cnf.clauses) as s:
        tm = threading.Timer(limit, s.interrupt); tm.start()
        r = s.solve_limited(expect_interrupt=True)
        tm.cancel()
        m = s.get_model() if r else None
    dt = time.time() - t
    out = {True: 'SAT', False: 'UNSAT', None: f'TIMEOUT>{limit}s'}[r]
    line = f"{label:58s} {sname:11s} vars={e.pool.top} clauses={len(e.cnf.clauses)} -> {out} ({dt:.1f}s)"
    if r:
        arcs = e.arcs_from_model(m); c = check(e.n, arcs, e.k)
        line += f" check: tt={c['tt']} indep={c['indep']} 2cyc={c['two_cycles']} deg={c['deg']}"
    print(line, flush=True)

limit = float(sys.argv[1]) if len(sys.argv) > 1 else 600
which = sys.argv[2] if len(sys.argv) > 2 else 'all'
if which in ('all', 'dimacs'):
    for (o, i) in [(3, 2), (2, 3)]:
        for fixB in (1, 0):
            e = frame(14, 4, o, i, fixB)
            fn = f"/tmp/e1122/seatO/cnf/lemmaB_{o}{i}_{'B8fixed' if fixB else 'Ifree'}.cnf"
            e.cnf.to_file(fn)
    e = frame(13, 4, 2, 2, 0); e.cnf.to_file("/tmp/e1122/seatO/cnf/control_n13_22_Ifree.cnf")
    print("dimacs written")
if which in ('all', 'solve'):
    run(frame(13, 4, 2, 2, 0), "CONTROL n=13 (2,2) I(0) free, expect SAT", 'cadical195', limit)
    run(frame(13, 4, 2, 2, 1), "CONTROL n=13 (2,2) I(0)=B8, expect SAT", 'cadical195', limit)
    for (o, i) in [(3, 2), (2, 3)]:
        for fixB in (1, 0):
            for sname in ('cadical195', 'glucose4'):
                run(frame(14, 4, o, i, fixB), f"LEMMA B n=14 ({o},{i}) I(0)={'B8 fixed' if fixB else 'free'}, claim UNSAT", sname, limit)
