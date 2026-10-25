# Numerical tests of Lemma 4.3 (S_x >= 4 mu^3 at some x) and Lemma 4.4 (endpoint profile saving),
# with a mutation control.  seat MATH.
import numpy as np, sys
sys.path.insert(0, '/tmp/erdos1800/seats/math')
from graphs import *
rng = np.random.default_rng(20261012)

def stats(A, w):
    mu = 0.5 * w @ A @ w
    d = A @ w
    e = A @ (w*d)
    S = d*(e - mu*d)
    return mu, d, e, S

def L(al):
    ah = min(al, 1-al); return min(4*ah*ah, ah*(1-ah))

# ---------- build the test population
pop = []   # (name, A, w, regular_uniform_flag)
def add(name, A, w, reg=False): pop.append((name, A, w, reg))
base = [('C5',cycle(5)), ('Petersen',petersen()), ('Clebsch',clebsch()), ('Andrasfai3',andrasfai(3)),
        ('Andrasfai4',andrasfai(4)), ('C7',cycle(7)), ('MobiusKantor',mobius_kantor())]
for name, A in base:
    assert is_tf(A)
    n = len(A)
    add(name+'/uniform', A, np.full(n, 1/n), True)
# 200 random weighted graphs
gs = {k: geng(k) for k in range(2, 9)}
while len(pop) < 207:
    kind = rng.integers(0, 4)
    if kind == 0:
        n = int(rng.integers(3, 13)); A = random_bipartite(rng, n); name='bip'
    elif kind == 1:
        nm, B = base[int(rng.integers(0, 3))]
        sizes = rng.integers(1, 4, size=len(B))
        A = blowup(B, sizes, rng, pdel=rng.uniform(0, 0.4)); name='blowup-'+nm
    elif kind == 2:
        k = int(rng.integers(2, 9)); A = gs[k][int(rng.integers(0, len(gs[k])))]; name=f'geng{k}'
    else:
        n = int(rng.integers(5, 14)); A = random_tf(rng, n, rng.uniform(0.2, 1)); name='randtf'
    if A.sum() == 0: continue
    assert is_tf(A)
    n = len(A)
    w = rng.dirichlet(np.full(n, rng.choice([0.3, 1.0, 5.0])))
    w = np.maximum(w, 1e-6); w /= w.sum()
    add(name, A, w)

# ---------- Lemma 4.3
def l43(const):
    worst = (np.inf, None)
    worst_rel = np.inf
    for name, A, w, reg in pop:
        mu, d, e, S = stats(A, w)
        if mu <= 0: continue
        m = np.max(S[d > 0]) - const*mu**3
        rel = np.max(S[d>0])/(4*mu**3)
        if m < worst[0]: worst = (m, name)
        worst_rel = min(worst_rel, rel)
    return worst, worst_rel
w4, r4 = l43(4.0)
print(f"Lemma 4.3 over {len(pop)} weighted graphs: min_G (max_x S_x - 4 mu^3) = {w4[0]:.3e} (at {w4[1]}); min ratio max S/(4mu^3) = {r4:.12f}")
for name, A, w, reg in pop[:7]:
    mu, d, e, S = stats(A, w)
    print(f"   {name:24s} max S_x - 4mu^3 = {np.max(S)-4*mu**3:+.3e}")
w401, _ = l43(4.01)
print(f"MUTATION 4.01 mu^3: min_G (max_x S_x - 4.01 mu^3) = {w401[0]:.3e} at {w401[1]}  -> {'FAILS (as it must)' if w401[0] < 0 else 'still passes: CONTROL BROKEN'}")
# non-triangle-free sanity (lemma does not use triangle-freeness)
bad = 0
for _ in range(300):
    n = int(rng.integers(3, 12)); A = (np.triu(rng.random((n,n)) < rng.uniform(0.2,0.9), 1)).astype(float); A = A + A.T
    if A.sum()==0: continue
    w = rng.dirichlet(np.ones(n)); mu, d, e, S = stats(A, w)
    if np.max(S[d>0]) < 4*mu**3 - 1e-15: bad += 1
print("Lemma 4.3 on 300 random NON-triangle-free weighted graphs: violations =", bad)

# ---------- Lemma 4.4
def A_of(A, w, psi, pi): return 0.5 * (w*pi) @ A @ (w*pi) + np.sum(w*psi*pi)
worst_slack = np.inf; worst_info=None; n_tests=0; feas_viol=0; mean_viol=0; ident_err=0; prod_viol=0; case_err=0
for name, A, w, reg in pop:
    mu, d, e, S = stats(A, w)
    if mu <= 0: continue
    good = np.where((d > 0) & (S >= 4*mu**3*(1-1e-12)))[0]
    for trial in range(10):
        al = rng.uniform(0, 1) if trial < 8 else rng.choice([rng.uniform(0,0.02), rng.uniform(0.98,1)])
        psi = rng.normal(0, rng.choice([0.01, 1, 100]), size=len(A))
        for x in good:   # every admissible x, not just one
            dd = d[x]; z = 1-dd
            assert 0 < dd < 1 and 0 < z < 1
            phi = A[x].copy() - dd
            tp = min((1-al)/z, al/dd); tm = min(al/z, (1-al)/dd)
            # three-case product check
            ah = min(al, 1-al)
            if dd <= ah: pc = ah*(1-ah)/z**2
            elif dd <= 1-ah: pc = ah*ah/(dd*z)
            else: pc = ah*(1-ah)/dd**2
            case_err = max(case_err, abs(pc - tp*tm)/max(pc,1e-300))
            if tp*tm < L(al)*(1-1e-12): prod_viol += 1
            lp, lm = tm/(tp+tm), tp/(tp+tm)
            pip, pim = al + tp*phi, al - tm*phi
            Aal = A_of(A, w, psi, np.full(len(A), al))
            avg = lp*A_of(A,w,psi,pip) + lm*A_of(A,w,psi,pim)
            ident_err = max(ident_err, abs(avg - (Aal - tp*tm*S[x]))/(1+abs(Aal)))
            best = min((A_of(A,w,psi,pip), pip), (A_of(A,w,psi,pim), pim), key=lambda u: u[0])
            pi = best[1]
            if pi.min() < -1e-12 or pi.max() > 1+1e-12: feas_viol += 1
            if abs(w@pi - al) > 1e-12: mean_viol += 1
            slack = (Aal - 4*L(al)*mu**3) - best[0]
            scale = 1 + abs(Aal)
            if slack/scale < worst_slack: worst_slack = slack/scale; worst_info=(name, al, x, slack)
            n_tests += 1
print(f"Lemma 4.4: {n_tests} (graph, alpha, psi, admissible x) tests; worst relative slack of (9) = {worst_slack:.3e} at {worst_info[:3]}")
print(f"   feasibility violations={feas_viol}  mean violations={mean_viol}  max |avg identity err|={ident_err:.2e}  t+t-<L(alpha): {prod_viol}  3-case formula max rel err={case_err:.2e}")
# mutation: replace L(alpha) by 1.01*L(alpha)/... saving 4*1.01*L*mu^3 must fail on a regular uniform graph with d in middle case
name, A, w, reg = pop[0]   # C5 uniform
mu, d, e, S = stats(A, w); x = 0; dd=d[x]; z=1-dd
al = 0.5; tp = min((1-al)/z, al/dd); tm=min(al/z,(1-al)/dd)
print(f"C5 uniform, alpha=1/2: t+t- = {tp*tm:.6f}, L = {L(al)}, S_x/(4mu^3) = {S[x]/(4*mu**3):.6f} -> the lemma's saving 4L mu^3 = {4*L(al)*mu**3:.6e}, achieved = {tp*tm*S[x]:.6e}")
