import sys, time, itertools
sys.path.insert(0, '/tmp/e1122/seatO')
from enc import Enc
from check import check
from pysat.solvers import Solver

def solve(e, name, solvers=('cadical195', 'glucose4')):
    res = []
    for sname in solvers:
        t = time.time()
        with Solver(name=sname, bootstrap_with=e.cnf.clauses) as s:
            ok = s.solve()
            m = s.get_model() if ok else None
        dt = time.time() - t
        line = f"{name:60s} {sname:11s} vars={e.pool.top:6d} clauses={len(e.cnf.clauses):7d} -> {'SAT' if ok else 'UNSAT'} ({dt:.2f}s)"
        if ok:
            arcs = e.arcs_from_model(m)
            c = check(e.n, arcs, e.k)
            line += f"  check: arcs={c['arcs']} loops={c['loops']} 2cyc={c['two_cycles']} tt={c['tt']} indep{e.k}={c['indep']} deg={c['deg']} deg0={sum(1 for x in arcs if 0 in x)}"
        print(line, flush=True)
        res.append(ok)
    return res

def mk(n, k, **kw):
    return Enc(n, k, **kw)

which = sys.argv[1] if len(sys.argv) > 1 else 'all'

if which in ('all', 'small'):
    # negative / positive controls on known values
    solve(mk(3, 2), "n=3 k=2 (I2,L3), expect SAT (directed 3-cycle)")
    solve(mk(4, 2), "n=4 k=2 r(I2,L3)=4, expect UNSAT")
    solve(mk(8, 3), "n=8 k=3 Bermond, expect SAT")
    solve(mk(9, 3), "n=9 k=3 r(I3,L3)=9, expect UNSAT")
    solve(mk(14, 4), "n=14 k=4 no degree constraint, expect SAT (IRW)")
    solve(mk(22, 5), "n=22 k=5 no degree constraint, expect SAT (IRW Z22)")

if which in ('all', 'B'):
    e = mk(14, 4); e.card(e.deg_lits(0), 6, 'equals')
    solve(e, "n=14 k=4 deg(0)==6, expect SAT")
    e = mk(13, 4); e.card(e.deg_lits(0), 5, 'atmost')
    solve(e, "CONTROL n=13 k=4 deg(0)<=5, expect SAT")
    e = mk(13, 4); e.card(e.deg_lits(0), 4, 'atmost')
    solve(e, "near-miss n=13 k=4 deg(0)<=4 (|I(0)|>=8), unknown")
    e = mk(14, 4, tt=False); e.card(e.deg_lits(0), 5, 'atmost')
    solve(e, "MUTATION n=14 k=4 deg(0)<=5 with NO TT clauses, expect SAT")
    e = mk(14, 5); e.card(e.deg_lits(0), 5, 'atmost')
    solve(e, "MUTATION n=14 k=5 (I5-free) deg(0)<=5, expect SAT")
    e = mk(14, 4); e.card(e.deg_lits(0), 7, 'atleast')
    solve(e, "n=14 k=4 deg(0)>=7, expect UNSAT")
    e = mk(14, 4); e.card(e.deg_lits(0), 5, 'atmost')
    solve(e, "LEMMA B n=14 k=4 deg(0)<=5 (no labels fixed), claim UNSAT")
    for (o, i) in [(3, 2), (2, 3)]:
        e = mk(14, 4)
        P = list(range(1, 1 + o)); Q = list(range(1 + o, 1 + o + i)); R = list(range(1 + o + i, 14))
        for p in P: e.fix_arc(0, p)
        for q in Q: e.fix_arc(q, 0)
        for r in R: e.fix_nonadj(0, r)
        solve(e, f"LEMMA B n=14 k=4 vertex 0 fixed (out,in)=({o},{i}), claim UNSAT")
