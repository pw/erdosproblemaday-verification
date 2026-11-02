"""Seat C: CP-SAT witness finder (OR-tools) for a minimal distinct covering system with moduli in M and
>= k classes. Used ONLY to find witnesses quickly; every witness is re-verified by checker.py.
(Upper bounds come from kenc.py/kissat and dfsK, not from this file.)
usage: python3 cpsat_witness.py --x X --k K [--workers 2] [--time 600]"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checker, kenc
from math import gcd
from ortools.sat.python import cp_model
ap = argparse.ArgumentParser(); ap.add_argument('--x', type=int); ap.add_argument('--moduli', type=int, nargs='*')
ap.add_argument('--k', type=int, required=True); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--time', type=float, default=600); ap.add_argument('--sym', action='store_true'); ap.add_argument('--sym2', action='store_true')
a = ap.parse_args()
M = a.moduli if a.moduli else kenc.smooth_set(a.x)
L = 1
for n in M: L = L // gcd(L, n) * n
m = cp_model.CpModel()
c = {(n, r): m.NewBoolVar('c_%d_%d' % (n, r)) for n in M for r in range(n)}
used = {}
for n in M:
    m.AddAtMostOne([c[n, r] for r in range(n)])
    used[n] = m.NewBoolVar('u%d' % n)
    m.Add(sum(c[n, r] for r in range(n)) == used[n])
u = {}
for z in range(L):
    lits = [c[n, z % n] for n in M]
    m.AddBoolOr(lits)
    u[z] = m.NewBoolVar('p%d' % z)
    m.Add(sum(lits) <= 1).OnlyEnforceIf(u[z])
for n in M:
    for r in range(n):
        m.AddBoolOr([u[z] for z in range(r, L, n)]).OnlyEnforceIf(c[n, r])
m.Add(sum(used.values()) >= a.k)
if a.sym:  # translate so that the class of the LARGEST used modulus is 0 mod it (valid for every system)
    Ms = sorted(M)
    for i, n in enumerate(Ms):
        for r in range(1, n):
            m.AddBoolOr([c[n, r].Not()] + [used[mm] for mm in Ms[i + 1:]])
if a.sym and a.sym2:  # then multiply by a unit u of Z/L (fixes 0 mod the largest modulus): the class of the
    # SECOND largest used modulus n can be taken to have residue 0 or a proper divisor of n
    Ms = sorted(M)
    for i, n in enumerate(Ms):
        allowed = {0} | {d for d in range(1, n) if n % d == 0}
        larger = Ms[i + 1:]
        for r in range(n):
            if r in allowed: continue
            for mm in larger:   # forbid: c[n,r] and mm is the ONLY larger used modulus
                m.AddBoolOr([c[n, r].Not(), used[mm].Not()] + [used[m2] for m2 in larger if m2 != mm])
s = cp_model.CpSolver(); s.parameters.num_workers = a.workers; s.parameters.max_time_in_seconds = a.time
st = s.Solve(m)
print('M', M, 'k>=', a.k, 'status', s.StatusName(st), 'wall %.1fs' % s.WallTime())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sysm = sorted([(r, n) for (n, r), v in c.items() if s.Value(v)], key=lambda t: t[1])
    print('SYSTEM (%d classes):' % len(sysm), ' '.join('%d/%d' % t for t in sysm))
    print('checker.accept =', checker.accept(sysm), ' max modulus', max(n for r, n in sysm))
