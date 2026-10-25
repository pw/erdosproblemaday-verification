# Sanity checks of the Prop 2.2 deletion-process arithmetic (PDF p.7) and of the finite mechanics it relies on.
# Part A: exact identities used in the edge count, for all N up to 3000, with Fractions.  Control: off-by-one sum.
# Part B: the "excess" inequality as an algebraic implication, checked on random exact rational instances.
#         Control: drop the 1/log N term from t_N (then eta_N can be 0 and strict positivity fails).
# Part C: run the actual process on concrete planar point sets (exact integer squared distances) and assert
#         every invariant the proof uses.  Control: a mutated process that skips the post-deletion fiber cleanup.
import math, random
from fractions import Fraction as Fr
fails = []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: fails.append(name)

# ---------- Part A ----------
okA = True; okA_ctrl_rejected = True
for N in range(2, 3001):
    m0 = -(-N // 2); A = N*(N-1); B = m0*(m0-1)
    S = sum(2*(m-1) for m in range(m0+1, N+1))
    if S != A - B: okA = False
    S_bad = sum(2*(m-1) for m in range(m0, N+1))      # control: sum starting at m0
    if S_bad == A - B and N > 1 and m0 > 1: okA_ctrl_rejected = okA_ctrl_rejected and False
check("A: sum_{m=m0+1}^N 2(m-1) == A_N - B_N for 2<=N<=3000", okA)
check("A control: sum from m0 is NOT A_N-B_N (control rejected)", okA_ctrl_rejected)
# B_N/A_N -> 1/4 and the first N with 1 - B/A - eta > 0 for small eta (illustrative)
for N in [10, 100, 1000, 10**6]:
    m0 = -(-N//2); print(f"   N={N}: B_N/A_N = {m0*(m0-1)/(N*(N-1)):.6f}")

# ---------- Part B ----------
# Claim: with t = b + |F-th| + ell (ell = 1/log N > 0), eta = sqrt(t), and 0 <= B <= A, b >= 0,
#   F*A - (th-eta)(A-B) - ell*A - (th+b)*B  >=  eta*(A-B) - t*A  = eta*A*(1 - B/A - eta).
rng = random.Random(2)
viol = 0; ctrl_viol = 0
for _ in range(200000):
    A = Fr(rng.randint(2, 10**6)); B = Fr(rng.randint(0, int(A)))
    th = Fr(rng.randint(1, 1000), 1000); F = Fr(rng.randint(0, 1000), 1000)
    b = Fr(rng.randint(0, 50), 1000); ell = Fr(rng.randint(1, 50), 1000)
    t = b + abs(F-th) + ell
    # exact eta not needed for the identity: the inequality LHS-RHS = (F-th+|F-th|)A + b(A-B) + ... >= 0 ;
    # test it with eta = any number (take a rational eta and set t = eta^2 consistently)
    eta = Fr(rng.randint(0, 1000), 1000)
    lhs = F*A - (th-eta)*(A-B) - ell*A - (th+b)*B
    rhs = eta*(A-B) - t*A
    if lhs < rhs: viol += 1
    if not (eta*(A-B) - eta*eta*A == eta*A*(1 - B/A - eta)): viol += 1
check("B: excess >= eta(A-B) - t*A on 200000 exact random instances (and the factorisation identity)", viol == 0)
# Control: t WITHOUT the 1/log N term (fiber cost -A/log N still subtracted in the edge count).
# Then the claimed "excess >= eta(A-B) - t*A" must FAIL on some instance (F_N(s)=theta, b_N=0).
A, B = Fr(100*99), Fr(50*49); F = th = Fr(1, 3); b = Fr(0); ell = Fr(1, 5)
eta = Fr(1, 10); t_bad = b + abs(F-th)                      # missing ell
lhs = F*A - (th-eta)*(A-B) - ell*A - (th+b)*B
check("B control: with 1/log N dropped from t_N the excess inequality is FALSE (lhs < eta(A-B)-t*A)",
      lhs < eta*(A-B) - t_bad*A)

# ---------- Part C ----------
def run_process(P, s_thr, K, a, mutate_skip_cleanup=False):
    """P: list of integer points.  Initial edges: all (x,y), x!=y, with k_P(x,y) >= s_thr (exact).
       Fibers keyed by (source, squared distance). Discard fibers with < K edges; delete a vertex whose
       in+out degree < 2a(m-1); clean fibers after each deletion.  Returns trace for invariant checks."""
    N = len(P)
    d2 = lambda x, y: (x[0]-y[0])**2 + (x[1]-y[1])**2
    cls = {}
    for x in P:
        for y in P:
            if y != x: cls.setdefault((x, d2(x, y)), set()).add(y)
    fibers = {key: set(T) for key, T in cls.items() if len(T) >= s_thr}      # initial fibers = whole classes
    n_initial_fibers = len(fibers); E0 = sum(len(T) for T in fibers.values())
    V = set(P); fiber_cost = 0; vertex_cost = 0; deletion_log = []
    discarded = set(); ok_split = True; ok_once = True; snap = None
    def cleanup():
        nonlocal fiber_cost, ok_once
        for key in list(fibers):
            if 0 < len(fibers[key]) < K:
                if key in discarded: ok_once = False
                fiber_cost += len(fibers[key]); discarded.add(key); fibers[key] = set()
                if len(fibers[key]) >= K: pass
    cleanup()
    while True:
        m = len(V)
        deg = {v: 0 for v in V}
        for (x, r), T in fibers.items():
            for y in T: deg[x] += 1; deg[y] += 1
        low = [v for v in V if deg[v] < 2*a*(m-1)]
        if not low: break
        v = min(low)                       # any order; the argument is order-free
        cost = deg[v]; vertex_cost += cost; deletion_log.append((m, cost, 2*a*(m-1)))
        V.discard(v)
        for key in list(fibers):
            if key[0] == v: fibers[key] = set()
            else: fibers[key].discard(v)
        if not mutate_skip_cleanup: cleanup()
        if len(V) == -(-N//2) and snap is None:
            Es = sum(len(T) for T in fibers.values())
            kmin = min([sum(1 for z in V if z != x and d2(x, z) == r) for (x, r), T in fibers.items() if T], default=10**9)
            snap = dict(E=Es, fiber_cost=fiber_cost, kmin=kmin)
    # invariants
    E = [(x, y) for (x, r), T in fibers.items() for y in T]
    # (i) no fiber split: every surviving fiber equals the FULL class of its source in the final set
    for (x, r), T in fibers.items():
        if T and T != {y for y in V if y != x and d2(x, y) == r}: ok_split = False
    return dict(N=N, n=len(V), V=V, E=E, fibers=fibers, E0=E0, nfib0=n_initial_fibers, fiber_cost=fiber_cost,
                vertex_cost=vertex_cost, log=deletion_log, ok_split=ok_split, ok_once=ok_once, d2=d2, snap=snap)

def invariants(R, K, a, s_thr, label):
    N, n, E = R['N'], R['n'], R['E']; d2 = R['d2']; V = R['V']
    oks = []
    oks.append(("initial fibers <= E0/s_thr", R['nfib0'] <= R['E0']/s_thr))
    oks.append(("fiber cleanup cost <= (#initial fibers)*K", R['fiber_cost'] <= R['nfib0']*K))
    oks.append(("each deletion at count m costs < 2a(m-1)", all(c < bnd for (m, c, bnd) in R['log'])))
    m0 = -(-N//2)
    # edge accounting at the end: E_final >= E0 - a*(A - n(n-1)) - fiber_cost  (paper's count with m0 replaced by n)
    oks.append(("|E_final| >= E0 - a(N(N-1)-n(n-1)) - fiber_cost",
                len(E) >= R['E0'] - a*(N*(N-1) - n*(n-1)) - R['fiber_cost'] - 1e-9))
    oks.append(("no fiber split (surviving fiber == full class in final set)", R['ok_split']))
    oks.append(("each initial fiber discarded at most once", R['ok_once']))
    if R['snap'] is not None:
        S = R['snap']; A = N*(N-1); B = m0*(m0-1)
        oks.append(("at count m0: |E| >= E0 - a(A_N-B_N) - fiber_cost (paper's count)", S['E'] >= R['E0'] - a*(A-B) - S['fiber_cost'] - 1e-9))
        oks.append(("at count m0: every edge has k_{P'} >= K (so |E| <= B_N * ratio_{P'}(K))", S['kmin'] >= K))
        print(f"     [{label}] m0-snapshot (first time vertex count = m0, after cleanup): |E|={S['E']} >= E0 - a(A-B) - cost = {R['E0'] - a*(A-B) - S['fiber_cost']:.1f}")
    sizes = [len(T) for T in R['fibers'].values() if T]
    oks.append(("all surviving fibers have >= K edges", all(z >= K for z in sizes)))
    if n >= 2 and E:
        dn = len(E)/(n*(n-1))
        deg = {v: 0 for v in V}; indeg = {v: 0 for v in V}
        for x, y in E: deg[x] += 1; deg[y] += 1; indeg[y] += 1
        oks.append(("degree lower bounds hold at stop", all(deg[v] >= 2*a*(n-1) for v in V)))
        oks.append(("d_n >= a  (left half of (2.5))", dn >= a - 1e-12))
        # every edge has k_final(x,y) >= K, so d_n <= R_final(K)  (right half of (2.5) with F replaced by the actual ratio)
        kf = lambda x, y: sum(1 for z in V if z != x and d2(x, z) == d2(x, y))
        oks.append(("every final edge has k_P'(x,y) >= K", all(kf(x, y) >= K for x, y in E)))
        # (2.2): (qX+qY)/2 >= (a/d_n) alpha ; q <= pi/d_n is an identity
        oks.append(("(qX+qY)/2 >= (a/d_n) alpha pointwise", all(deg[v]/(2*len(E)) >= (a/dn)/n - 1e-15 for v in V)))
        gam = 0.5
        mass = sum(indeg[v] for v in V if indeg[v] < n**gam)/len(E)
        oks.append(("(2.3) finite form: qY{d^- < n^g} <= n*n^g/|E|", mass <= n*n**gam/len(E) + 1e-15))
        # (2.4) finite form: |E| * E_e 1_C(x_e) p_e 1{p_e>=lam} == #{(x_e,y) in C^2 : |F_e∩C| >= lam k_e}, and each
        # counted pair has k_C(x_e,y) >= |F_e ∩ C| >= lam*K
        lam = 0.3; rng = random.Random(7); ok24 = True
        Vl = sorted(V)
        for _ in range(60):
            C = set(rng.sample(Vl, rng.randint(2, len(Vl))))
            lhs = sum((len(T)/len(E)) * (1 if x in C else 0) * (len(T & C)/len(T)) * (1 if len(T & C)/len(T) >= lam else 0)
                      for (x, r), T in R['fibers'].items() if T)
            cnt = 0
            for (x, r), T in R['fibers'].items():
                if T and x in C and len(T & C) >= lam*len(T):
                    for y in T & C:
                        cnt += 1
                        kC = sum(1 for z in C if z != x and d2(x, z) == r)
                        if not (kC >= len(T & C) >= lam*K): ok24 = False
            if abs(lhs*len(E) - cnt) > 1e-9: ok24 = False
        oks.append(("(2.4) counting identity + k_C >= |F_e∩C| >= lam*K on 60 random subsets", ok24))
    allok = all(o for _, o in oks)
    print(f"  [{label}] N={N} stop n={n} (m0={m0}) E0={R['E0']} |E|={len(E)} deletions={len(R['log'])} "
          f"fiber_cost={R['fiber_cost']} vertex_cost={R['vertex_cost']}: {'all invariants hold' if allok else 'VIOLATIONS: '+str([nm for nm, o in oks if not o])}")
    return allok

rng = random.Random(604)
grid = [(i, j) for i in range(12) for j in range(12)]
noise = set()
while len(noise) < 56:
    p = (rng.randint(100, 10**6), rng.randint(100, 10**6))
    noise.add(p)
P1 = grid + sorted(noise)                                            # N = 200
P2 = [(i, j) for i in range(14) for j in range(14)]                  # N = 196
P3 = [(i, j) for i in range(10) for j in range(10)] + [(i, j) for i in range(30, 36) for j in range(30, 36)]  # two grids, N=136
okC = True
for P, s_thr, K, a, lab in [(P1, 4, 3, 0.25, "grid12+56 random"), (P1, 4, 4, 0.20, "grid12+56 random b"),
                           (P2, 8, 6, 0.05, "grid14 hi"), (P2, 4, 6, 0.12, "grid14 collapsing"),
                           (P3, 3, 5, 0.08, "two grids collapsing")]:
    R = run_process(P, s_thr, K, a)
    okC &= invariants(R, K, a, s_thr, lab)
check("C: all invariants on 5 concrete runs", okC)
# Control: skip the cleanup after vertex deletions -> some surviving fiber drops below K (the check must see it)
R = run_process(P2, 8, 6, 0.05, mutate_skip_cleanup=True)
ctrl = invariants(R, 6, 0.05, 8, "CONTROL skip-cleanup")
check("C control: skip-cleanup run is REJECTED by the invariant checker", not ctrl)
print("OVERALL:", "ALL CHECKS PASS, ALL CONTROLS FAIL" if not fails else f"PROBLEMS: {fails}")
