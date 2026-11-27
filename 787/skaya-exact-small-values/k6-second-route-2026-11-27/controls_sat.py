"""Controls for the SAT side (part b).  Each control can go red.
C1  No certified core excludes a REAL 22-element configuration.  Formula = AMO + ORDER2 + all archive cores
    (+ our extra cores), assumptions = the exact s-assignment (every true x_i + x_j = x_l) of a real set:
    {1..22}; P+{100} (P = positive part of their 43-element witness); smallest / largest 22 of P59 (positive part
    of their 59-element witness); 60 random 22-subsets of [1,40]; 60 random 22-subsets of P59.  Must all be SAT.
    Mutation (must fire): the same with every archive core id shifted by +1 (wrong triple mapping).
C2  The full encoding with k = 7 (every 8-subset contains an edge) + all cores, assumptions = s-assignment of P+{100}
    (alpha = alpha(P) + 1 = 7, computed below): must be SAT; with k = 6 (the real formula) the same assumptions must be
    UNSAT (P+{100} has an independent 7-set)."""
import sys, itertools, random, time
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/787/check')
from sat_close import TRIP, s, EDGE, NV, load_cores, m
from pysat.solvers import Solver
from write_cnf import order_atoms
import subprocess
KISSAT = '/home/exedev/MathDyad/tools/kissat/build/kissat'

P = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,20,22,24,26,42]
P59 = list(range(1, 17)) + list(range(18, 29, 2)) + list(range(32, 53, 4)) + [84]
assert len(P) == 21 and len(P59) == 29

def assign(vals):
    v = sorted(vals); assert len(v) == m and len(set(v)) == m and v[0] > 0
    pos = set((i, j, l) for (i, j, l) in TRIP if v[i] + v[j] == v[l])
    return [s(*t) if t in pos else -s(*t) for t in TRIP], len(pos)

def alpha(vals):
    S = set(vals); v = sorted(vals); n = len(v)
    adj = [[(v[a] + v[b] in S) for b in range(n)] for a in range(n)]
    best = 0
    def grow(cur, start):
        nonlocal best
        best = max(best, len(cur))
        for x in range(start, n):
            if all(not adj[x][y] for y in cur): grow(cur + [x], x + 1)
    grow([], 0); return best

def amo_order():
    cl = []
    def amo(lits):
        for a, b in itertools.combinations(lits, 2): cl.append([-a, -b])
    for i in range(m):
        for j in range(i + 1, m): amo([s(i, j, l) for l in range(j + 1, m)])
    for l in range(m):
        for a in range(l): amo([s(min(a, b), max(a, b), l) for b in range(l) if b != a])
    for (a, b, l) in TRIP:
        for (c, d, l2) in TRIP:
            if (a, b) != (c, d) and a <= c and b <= d and l >= l2: cl.append([-s(a, b, l), -s(c, d, l2)])
    return cl

def main():
    t0 = time.time(); rng = random.Random(1126); fails = 0
    configs = [('1..22', list(range(1, 23))), ('P+{100}', P + [100]), ('P59 smallest 22', P59[:22]), ('P59 largest 22', P59[-22:])]
    configs += [(f'rand[1,40] #{r}', rng.sample(range(1, 41), 22)) for r in range(60)]
    configs += [(f'rand P59 #{r}', rng.sample(P59, 22)) for r in range(60)]
    cores, extra = load_cores()
    from sat_close import base_clauses
    _b, _nb, _no = base_clauses(); sconstr = _b[:_nb + _no]
    assert sorted(map(tuple, sconstr)) == sorted(map(tuple, amo_order())), 'amo_order() != the s-constraints sat_hybrid ran'
    base = sconstr + order_atoms()          # exactly the s-part sat_hybrid.py ran (base[:nb+no]) + our order atoms (27 Nov: was amo_order(), a re-implementation)
    for label, shift in (('C1 real cores', 0), ('C1 MUTATION ids+1', 1)):
        S = Solver(name='cadical195'); S.append_formula(base)
        if shift == 0:
            S.append_formula(cores); S.append_formula(extra)
        else:
            nt = len(TRIP)
            S.append_formula([[-((-x - 1 + 1) % nt + 1) for x in c] for c in cores])
        sat = unsat = 0; dens = []
        for name, vals in configs:
            A, ne = assign(vals); dens.append(ne)
            if S.solve(assumptions=A): sat += 1
            else:
                unsat += 1
                if shift == 0: print('  ERROR: real configuration blocked:', name, sorted(vals))
        print(f"{label}: {len(configs)} real configurations ({min(dens)}..{max(dens)} true equalities each): SAT {sat}, UNSAT {unsat}", flush=True)
        if shift == 0: fails += unsat
        else: fails += (unsat == 0)
        S.delete()
    aP = alpha(P); aN = alpha(P + [100])
    print(f"alpha(P) = {aP}, alpha(P+{{100}}) = {aN}")
    A, _ = assign(P + [100])
    for kk, expect in ((7, True), (6, False)):
        S = Solver(name='cadical195'); S.append_formula(base)
        for (i, j), e in EDGE.items(): S.add_clause([-e] + [s(i, j, l) for l in range(j + 1, m)])
        for sub in itertools.combinations(range(m), kk + 1): S.add_clause([EDGE[(a, b)] for a, b in itertools.combinations(sub, 2)])
        S.append_formula(cores); S.append_formula(extra)
        r = S.solve(assumptions=A)
        print(f"C2 k={kk}: full encoding + all cores, assumptions = P+{{100}}: {'SAT' if r else 'UNSAT'} (expected {'SAT' if expect else 'UNSAT'})", flush=True)
        fails += (r != expect); S.delete()
        # C3: the kissat path (clauses streamed on stdin, as in sat_hybrid.py) on the same formula + the planted units
        cls = list(base)
        for (i, j), e in EDGE.items(): cls.append([-e] + [s(i, j, l) for l in range(j + 1, m)])
        for sub in itertools.combinations(range(m), kk + 1): cls.append([EDGE[(a, b)] for a, b in itertools.combinations(sub, 2)])
        cls += cores + extra + [[a] for a in A]
        data = (f"p cnf {NV + len(TRIP)} {len(cls)}\n" + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)).encode()
        p = subprocess.run(['nice', '-n', '19', KISSAT, '--quiet'], input=data, capture_output=True, timeout=1800)
        rk = {10: True, 20: False}.get(p.returncode)
        ok = (rk == expect)
        if rk:   # check kissat's model really sets the planted s-literals
            mod = set(int(x) for ln in p.stdout.decode().splitlines() if ln.startswith('v') for x in ln[1:].split())
            ok = ok and all(a in mod for a in A)
        print(f"C3 k={kk}: kissat on the same clauses + planted units: exit {p.returncode} (expected {'10 SAT' if expect else '20 UNSAT'}) {'ok' if ok else 'FAIL'}", flush=True)
        fails += (not ok); del data, cls
    print(f"CONTROLS_SAT {'PASS' if fails == 0 else 'FAIL'} ({time.time()-t0:.0f}s)")
    return 0 if fails == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
