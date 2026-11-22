import sys, time, threading
sys.path.insert(0, '/tmp/e1122/seatO')
from enc import Enc
from check import check
from pysat.solvers import Solver

def irw14():
    A = set()
    for x in range(14):
        A.add((x, (x + 1) % 14)); A.add((x, (x - 2) % 14))
        A.add((x, (x + 4) % 14) if x % 2 == 0 else (x, (x - 6) % 14))
    return A

def irw22():
    return {(x, (x + s) % 22) for x in range(22) for s in (1, 4, -5, 10)}

def frame(n, k, o, i, fixI=None, fixfull=False, inner_deg=None):
    e = Enc(n, k)
    P = range(1, 1 + o); Q = range(1 + o, 1 + o + i); I = list(range(1 + o + i, n))
    for p in P: e.fix_arc(0, p)
    for q in Q: e.fix_arc(q, 0)
    for r in I: e.fix_nonadj(0, r)
    if fixI is not None:
        h = len(I)
        for a in range(h):
            for b in range(a + 1, h):
                if (a, b) in fixI: e.fix_arc(I[a], I[b])
                elif (b, a) in fixI: e.fix_arc(I[b], I[a])
                else: e.fix_nonadj(I[a], I[b])
    if inner_deg is not None:
        for v in I:
            lits = [e.a(v, w) for w in I if w != v] + [e.a(w, v) for w in I if w != v]
            e.card(lits, inner_deg, 'equals')
    return e

def _child(clauses, sname, q):
    with Solver(name=sname, bootstrap_with=clauses) as s:
        r = s.solve()
        q.put((r, s.get_model() if r else None))

def run(e, label, sname, limit):
    import multiprocessing as mp
    t = time.time(); q = mp.Queue()
    pr = mp.Process(target=_child, args=(e.cnf.clauses, sname, q)); pr.start()
    try:
        r, m = q.get(timeout=limit)
    except Exception:
        r, m = None, None
    pr.terminate(); pr.join()
    dt = time.time() - t
    out = {True: 'SAT', False: 'UNSAT', None: f'TIMEOUT>{limit:.0f}s'}[r]
    line = f"{label:66s} {sname:10s} vars={e.pool.top} cl={len(e.cnf.clauses)} -> {out} ({dt:.1f}s)"
    if r:
        c = check(e.n, e.arcs_from_model(m), e.k); line += f" check: tt={c['tt']} indep={c['indep']} 2cyc={c['two_cycles']} deg={c['deg']}"
    print(line, flush=True)

limit = float(sys.argv[1]); which = sys.argv[2]
B8 = {(x, (x + 1) % 8) for x in range(8)} | {(x, (x - 2) % 8) for x in range(8)}
if which == 'graphs':
    print("IRW14:", check(14, irw14(), 4)); print("IRW22 k=5:", check(22, irw22(), 5)); print("IRW22 k=4 (expect indep>0):", {k: v for k, v in check(22, irw22(), 4).items() if k in ('indep', 'first_indep')})
if which == 'r15':
    run(frame(15, 4, 3, 3, B8), "r(I4,L3)=15: n=15 v0 (3,3) I(0)=B8 fixed, expect UNSAT", 'cadical195', limit)
    run(frame(15, 4, 3, 3), "r(I4,L3)=15: n=15 v0 (3,3) I(0) free, expect UNSAT", 'cadical195', limit)
    run(Enc(15, 4), "r(I4,L3)=15: n=15 plain (no frame), expect UNSAT", 'cadical195', limit)
if which == 'A':
    I14 = irw14()
    run(frame(21, 6, 3, 3, I14), "MUTATION n=21 k=6 (I6-free) v0 (3,3) I(0)=IRW14, expect SAT", 'cadical195', limit)
    run(frame(20, 5, 3, 2, I14), "near-miss n=20 k=5 v0 (3,2) I(0)=IRW14, unknown", 'cadical195', limit)
    for (o, i) in [(3, 3), (4, 2)]:
        run(frame(21, 5, o, i, I14), f"LEMMA A x-check n=21 k=5 v0 ({o},{i}) I(0)=IRW14, claim UNSAT", 'cadical195', limit)
    for (o, i) in [(3, 3), (4, 2)]:
        run(frame(21, 5, o, i, None, inner_deg=6), f"LEMMA A x-check n=21 ({o},{i}) I(0) free + 6-reg, claim UNSAT", 'cadical195', limit)
