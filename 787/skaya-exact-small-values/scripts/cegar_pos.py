"""Independent CEGAR: is there a set of m positive reals x_0<...<x_{m-1} with alpha(G)<=k?
G: edge {i,j} iff x_i+x_j = x_l for some l.  Encoding (mine, not theirs):
 s(i,j,l), i<j<l  <=> x_i+x_j=x_l
 AMO over l for each pair (i,j); AMO over j for each (i,l) [x_j=x_l-x_i unique]; AMO over i for (j,l).
 every (k+1)-subset of {0..m-1} contains an edge  (edge(i,j) -> OR_l s(i,j,l)).
Refinement: true s-literals -> LP (x_0>=1, x_{t+1}-x_t>=1, equalities). If infeasible, Farkas
certificate y (integers, verified EXACTLY: w=-A^T y, all suffix sums of w >= 0, not all 0),
block the support. If feasible, try to build an exact rational point -> counterexample."""
import sys, itertools, time, os
ORDER2 = os.environ.get('ORDER2','1')=='1'
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from pysat.solvers import Solver

def run(m, k, log=sys.stdout):
    vid = {}
    def v(key):
        if key not in vid: vid[key] = len(vid) + 1
        return vid[key]
    trip = [(i,j,l) for l in range(m) for j in range(l) for i in range(j)]
    for t in trip: v(('s',)+t)
    S = Solver(name='cadical153')
    def amo(lits):
        for a,b in itertools.combinations(lits,2): S.add_clause([-a,-b])
    for i in range(m):
        for j in range(i+1,m):
            amo([v(('s',i,j,l)) for l in range(j+1,m)])
    for l in range(m):
        for a in range(l):
            # pairs {a,b} with b<l, b!=a, summing to x_l: unique b
            amo([v(('s',min(a,b),max(a,b),l)) for b in range(l) if b!=a])
    if ORDER2:
        # sound order clauses: (a,b) <= (c,d) componentwise, distinct pairs => x_a+x_b < x_c+x_d, so sums x_l, x_l' need l < l'
        for (a,b,l) in trip:
            for (c,d,l2) in trip:
                if (a,b)!=(c,d) and a<=c and b<=d and l>=l2:
                    S.add_clause([-v(('s',a,b,l)), -v(('s',c,d,l2))])
    for i in range(m):
        for j in range(i+1,m):
            S.add_clause([-v(('e',i,j))] + [v(('s',i,j,l)) for l in range(j+1,m)])
    for sub in itertools.combinations(range(m), k+1):
        S.add_clause([v(('e',a,b)) for a,b in itertools.combinations(sub,2)])
    svars = [v(('s',)+t) for t in trip]
    S.set_phases([-x for x in svars])
    it = 0; t0 = time.time(); coresizes = []
    while S.solve():
        it += 1
        mod = S.get_model(); pos = set(x for x in mod if x > 0)
        E = [t for t in trip if v(('s',)+t) in pos]
        y = farkas(m, E)
        if y is None:
            pt = exact_point(m, E)
            print(f"m={m} k={k}: FEASIBLE configuration found after {it} iters: E={E} point={pt}", file=log, flush=True)
            return ('SAT', E, pt, it)
        core = [E[r] for r in range(len(E)) if y[r] != 0]
        coresizes.append(len(core))
        S.add_clause([-v(('s',)+t) for t in core])
        if it % 200 == 0:
            print(f"  iter {it} core={len(core)} |E|={len(E)} {time.time()-t0:.1f}s", file=log, flush=True)
    print(f"m={m} k={k}: UNSAT after {it} refinements (all cores exactly certified), core sizes max={max(coresizes) if coresizes else 0}, {time.time()-t0:.1f}s", file=log, flush=True)
    return ('UNSAT', it, coresizes)

def check_cert(m, E, y):
    w = [0]*m
    for r,(i,j,l) in enumerate(E):
        w[i] -= y[r]; w[j] -= y[r]; w[l] += y[r]
    suf = 0; ok = True; nz = False
    for t in range(m-1,-1,-1):
        suf += w[t]
        if suf < 0: ok = False
        if suf != 0: nz = True
    return ok and nz

def lp_cert(m, E):
    r = len(E)
    if r == 0: return None
    W = np.zeros((m, r))  # w = W y  (w = -A^T y)
    for c,(i,j,l) in enumerate(E):
        W[i,c] -= 1; W[j,c] -= 1; W[l,c] += 1
    Suf = np.triu(np.ones((m,m)))  # suffix sums: Z = Suf @ w? row t sums w_s for s>=t
    Z = Suf @ W
    # Z y >= 0, sum(Z y) = 1, y free (split)
    A_ub = np.hstack([-Z, Z]); b_ub = np.zeros(m)
    A_eq = np.hstack([Z.sum(0), -Z.sum(0)]).reshape(1,-1)
    res = linprog(np.ones(2*r), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=(0,None), method='highs')
    if res.status != 0: return None
    return res.x[:r] - res.x[r:]

def rationalize(yf):
    import math
    fr = [Fraction(float(a)).limit_denominator(10**6) for a in yf]
    L = 1
    for f in fr: L = L*f.denominator//math.gcd(L, f.denominator)
    return [int(f*L) for f in fr]

def farkas(m, E):
    yf = lp_cert(m, E)
    if yf is None: return None
    y = rationalize(yf)
    if not check_cert(m, E, y):
        raise RuntimeError(f"could not certify exactly: E={E}")
    # shrink: deletion filter on support, keeping exact certificates
    sup = [r for r in range(len(E)) if y[r] != 0]
    cur = [E[r] for r in sup]
    pos = 0
    while pos < len(cur):
        trial = cur[:pos] + cur[pos+1:]
        yt = lp_cert(m, trial)
        if yt is not None:
            yi = rationalize(yt)
            if check_cert(m, trial, yi):
                cur = trial; continue
        pos += 1
    yc = rationalize(lp_cert(m, cur)); assert check_cert(m, cur, yc)
    full = [0]*len(E); idx = {t:n for n,t in enumerate(E)}
    for t,val in zip(cur, yc): full[idx[t]] = val
    assert check_cert(m, E, full)
    return full

def exact_point(m, E):
    # LP feasible; build exact rational point via nullspace of equalities
    res = linprog(np.zeros(m), A_ub=np.array([[-1 if c==0 else 0 for c in range(m)]] + [[(1 if c==t else -1 if c==t+1 else 0) for c in range(m)] for t in range(m-1)]),
                  b_ub=-np.ones(m), A_eq=(np.array([[ (1 if c in (i,j) else -1 if c==l else 0) for c in range(m)] for (i,j,l) in E]) if E else None),
                  b_eq=(np.zeros(len(E)) if E else None), bounds=(None,None), method='highs')
    return [round(a,6) for a in res.x] if res.status==0 else None

if __name__ == '__main__':
    m, k = int(sys.argv[1]), int(sys.argv[2])
    out = run(m, k)
    print(out[0])
