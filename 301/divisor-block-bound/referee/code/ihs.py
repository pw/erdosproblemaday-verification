#!/usr/bin/env python3
"""Independent referee program for Erdos #301 block profiles.

F_M(t) = max |A|, A subset of D(M) cap [1,t], with no 1/a = sum 1/b_i (a, b_i distinct in A).
Method: implicit hitting set. Master = exact MaxSAT (pysat RC2): minimise #removed elements
subject to "every known violation {a} u B loses at least one element".  Separation = exact
subset-sum test in x-space (x = L/d, L = lcm of candidates) with Python big-int bitsets.
Optimum of master (subset of constraints) is a LOWER bound on h; the returned set is verified
violation-free by the separator, so when the loop stops h is exact.
Usage: ihs.py M Tmax      (block profile over divisors of M up to Tmax)
       ihs.py interval n  (F on {1..n}, n=1..N)
env BUG=1/2 inserts a deliberate one-line bug (negative control).
"""
import sys, os, json, time
from math import gcd
from fractions import Fraction
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

BUG = os.environ.get('BUG', '0')
MASTER = os.environ.get('MASTER', 'scip')
TAG = os.environ.get('TAG', '')
NWIT = int(os.environ.get('NWIT', '4'))
import random
RNG = random.Random(1)

def lcm(a, b): return a // gcd(a, b) * b

def violations(ds):
    """ds: candidate set (labels d). Return list of cuts (frozensets of d) = {a} u B with
    1/a = sum_{b in B} 1/b, a not in B.  Empty list <=> ds is solution-free."""
    L = 1
    for d in ds: L = lcm(L, d)
    xs = sorted(L // d for d in ds)          # ascending x = descending d; distinct
    maxx = xs[-1]
    mask = (1 << (maxx + 1)) - 1
    if BUG == '2': mask = (1 << maxx) - 1     # BUG 2: off-by-one mask
    reach, snaps, cuts = 1, [], []
    for j, x in enumerate(xs):
        snaps.append(reach)                   # sums of distinct elements xs[0..j-1]
        if (reach >> x) & 1:
            for prefer_take in (True, False) + (None,) * NWIT:  # several witnesses per violated target
                s, w = x, []
                for i in range(j - 1, -1, -1):
                    pt = prefer_take if prefer_take is not None else (RNG.random() < 0.5)
                    if pt and s >= xs[i] and (snaps[i] >> (s - xs[i])) & 1:
                        w.append(xs[i]); s -= xs[i]
                    elif (snaps[i] >> s) & 1:
                        continue
                    else:
                        w.append(xs[i]); s -= xs[i]
                assert s == 0 and len(w) >= 2 and sum(w) == x
                cuts.append(frozenset([L // x] + [L // y for y in w]))
        if BUG == '1':
            reach = (reach | (1 << x)) & mask   # BUG 1: forgets multi-term sums
        else:
            reach = (reach | (reach << x)) & mask
    return cuts

def check_solution_free_fraction(A):
    """Slow independent check (Fractions, set DP) used on small sets only."""
    A = sorted(A)
    for a in A:
        bs = [b for b in A if b > a]
        sums = {Fraction(0)}
        for b in bs:
            sums |= {s + Fraction(1, b) for s in sums if s + Fraction(1, b) <= Fraction(1, a)}
        if Fraction(1, a) in sums: return False
    return True

def scip_cover(cands, cuts):
    from pyscipopt import Model, quicksum
    m = Model(); m.hideOutput(); m.setParam('lp/threads', 1)
    m.setParam('parallel/maxnthreads', 1)
    r = {d: m.addVar(vtype='B', name='r%d' % d) for d in cands}
    for c in cuts: m.addCons(quicksum(r[d] for d in c) >= 1)
    m.setObjective(quicksum(r.values()), 'minimize')
    m.optimize()
    assert m.getStatus() == 'optimal', m.getStatus()
    removed = [d for d in cands if m.getVal(r[d]) > 0.5]
    cost = int(round(m.getObjVal()))
    assert cost == len(removed)
    return removed, cost

class Profile:
    def __init__(self):
        self.cuts = set()
        self.prevF = 0
        self.prevkept = []
    def solve(self, cands):
        if MASTER == 'scip2':
            r = self.solve_scip2(cands)
            self.prevF = r[0]; self.prevkept = r[2]
            return r
        if MASTER == 'sat':
            r = self.solve_sat(cands)
            self.prevF = r[0]
            return r
        return self.solve_opt(cands)
    def solve_sat(self, cands):
        # F(t) in {F(prev), F(prev)+1}; a set of size F(prev)+1 must contain the new (largest) element.
        from pysat.solvers import Minicard
        n = len(cands); k = self.prevF + 1
        idx = {d: i + 1 for i, d in enumerate(cands)}
        if k > n: raise RuntimeError
        S = Minicard()
        for c in self.cuts:
            if all(d in idx for d in c): S.add_clause([-idx[d] for d in c])
        S.add_clause([idx[cands[-1]]])
        S.add_atmost([-idx[d] for d in cands], n - k)       # keep >= k
        it = 0
        while True:
            it += 1
            if not S.solve():
                S.delete()
                # cert: UNSAT => F(t) = F(prev); previous optimum (without new element) still valid
                kept = self.prevkept
                return len(kept), n - len(kept), kept, [d for d in cands if d not in kept], it
            model = S.get_model()
            kept = [d for d in cands if model[idx[d] - 1] > 0]
            new = violations(kept)
            if not new:
                S.delete()
                if len(kept) > k: kept = kept  # still valid (cannot exceed k by monotonicity) 
                assert len(kept) == k, (len(kept), k)
                self.prevkept = kept
                return len(kept), n - len(kept), kept, [d for d in cands if d not in kept], it
            for c in new:
                if c not in self.cuts:
                    self.cuts.add(c); S.add_clause([-idx[d] for d in c])
    def solve_scip2(self, cands):
        from pyscipopt import Model, quicksum
        m = Model(); m.hideOutput(); m.setParam('lp/threads', 1); m.setParam('parallel/maxnthreads', 1)
        r = {d: m.addVar(vtype='B', name='r%d' % d) for d in cands}
        m.setObjective(quicksum(r.values()), 'minimize')
        idx = set(cands)
        for c in self.cuts:
            if c <= idx: m.addCons(quicksum(r[d] for d in c) >= 1)
        # valid bound: h(t) >= h(prev) ; and r[new] = 0 WLOG is NOT valid for optimisation, so not used
        m.addCons(quicksum(r.values()) >= len(cands) - 1 - self.prevF)
        it = 0
        while True:
            it += 1
            m.optimize()
            assert m.getStatus() == 'optimal', m.getStatus()
            removed = [d for d in cands if m.getVal(r[d]) > 0.5]
            cost = int(round(m.getObjVal())); assert cost == len(removed)
            kept = [d for d in cands if d not in set(removed)]
            new = [c for c in violations(kept) if c not in self.cuts]
            if not violations(kept):
                return len(kept), cost, kept, removed, it
            m.freeTransform()
            for c in new:
                self.cuts.add(c); m.addCons(quicksum(r[d] for d in c) >= 1)
    def solve_opt(self, cands):
        idx = {d: i + 1 for i, d in enumerate(cands)}
        it = 0
        while True:
            it += 1
            active = [c for c in self.cuts if all(d in idx for d in c)]
            if MASTER == 'rc2':
                w = WCNF()
                for c in active: w.append([idx[d] for d in c])   # hard: remove >=1 of the cut
                for d in cands: w.append([-idx[d]], weight=1)    # soft: keep d
                with RC2(w) as rc2:
                    model = rc2.compute()
                    cost = rc2.cost
                removed = [d for d in cands if model[idx[d] - 1] > 0]
            else:
                removed, cost = scip_cover(cands, active)
            kept = [d for d in cands if d not in set(removed)]
            new = violations(kept)
            if not new:
                return len(kept), cost, kept, removed, it
            self.cuts.update(new)

def verify_int_sets(A):
    """Second, independent separator: plain set-of-ints DP per target (no bitsets)."""
    L = 1
    for d in A: L = lcm(L, d)
    for a in A:
        tgt = L // a
        sums = {0}
        for b in A:
            if b <= a: continue
            y = L // b
            sums |= {s + y for s in sums if s + y <= tgt}
        if tgt in sums: return False
    return True

def divisors(M):
    return sorted(d for d in range(1, M + 1) if M % d == 0)

def main():
    mode = sys.argv[1]
    P = Profile()
    out = []
    t0 = time.time()
    if mode == 'interval':
        N = int(sys.argv[2])
        for n in range(1, N + 1):
            F, h, kept, rem, it = P.solve(list(range(1, n + 1)))
            assert len(kept) == F and n - F == h
            print(n, F, 'removed', rem, 'iters', it, 'cuts', len(P.cuts), '%.1fs' % (time.time() - t0), flush=True)
            out.append(F)
        print('SEQ', ','.join(map(str, out)))
        return
    M = int(mode); T = int(sys.argv[2])
    D = [d for d in divisors(M) if d <= T]
    if os.environ.get('SEED') == '1':      # pre-seed every k=2 and k=3 solution (pure strengthening)
        import itertools
        for a in D:
            bs = [b for b in D if b > a]
            for b, c in itertools.combinations(bs, 2):
                if b * c == a * (b + c): P.cuts.add(frozenset((a, b, c)))
            for b, c, e in itertools.combinations(bs, 3):
                if b * c * e == a * (c * e + b * e + b * c): P.cuts.add(frozenset((a, b, c, e)))
        print('seeded', len(P.cuts), flush=True)
    res = []
    k0 = 1
    if os.environ.get('RESUME') == '1':    # resume from own saved profile + cuts
        res = json.load(open(os.environ.get('RESUME_PROF', '/tmp/ref301/prof_%d.json' % M)))
        P.cuts.update(frozenset(c) for c in json.load(open(os.environ.get('RESUME_CUTS', '/tmp/ref301/cuts_%d.json' % M))))
        assert [r['t'] for r in res] == D[:len(res)]
        P.prevF = res[-1]['F']; P.prevkept = res[-1]['kept']; k0 = len(res) + 1
        assert verify_int_sets(P.prevkept) and len(P.prevkept) == P.prevF
        print('resumed at n=%d with %d cuts' % (k0, len(P.cuts)), flush=True)
    for k in range(k0, len(D) + 1):
        cands = D[:k]
        F, h, kept, rem, it = P.solve(cands)
        assert verify_int_sets(kept), ('VERIFY FAILED', kept)
        res.append({'t': D[k - 1], 'n': k, 'F': F, 'h': h, 'kept': kept})
        print('t=%d n=%d F=%d h=%d iters=%d cuts=%d %.1fs removed=%s' % (D[k-1], k, F, h, it, len(P.cuts), time.time() - t0, rem), flush=True)
        json.dump(res, open('/tmp/ref301/prof_%d%s.json' % (M, TAG), 'w'))
        json.dump(sorted(sorted(c) for c in P.cuts), open('/tmp/ref301/cuts_%d%s.json' % (M, TAG), 'w'))

if __name__ == '__main__':
    main()
