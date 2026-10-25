# End-to-end numerical tests of Lemma 2.1, Lemma 2.2, Lemma 3.2 (identities (4),(5)), and the Section 4.2
# construction (13)/(14), on actual triangle-free graphs.  Exact Fractions where an identity is claimed.  seat MATH.
import numpy as np, sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/erdos1800/seats/math')
from graphs import *
rng = np.random.default_rng(128)

def cost(A, f):   # n^-2 * sum over edges f_x f_y
    n = len(A); return 0.5 * f @ A @ f / n**2

def all_bipartitions(n):
    # rows = indicator of side X for all 2^(n-1) partitions (vertex n-1 fixed in Y)
    k = np.arange(2**(n-1))[:,None]
    return ((k >> np.arange(n-1)[None,:]) & 1).astype(np.int8)

def internal(A, M):
    # internal edge count for each partition row of M (vertex n-1 in Y)
    n = len(A)
    Xs = np.concatenate([M, np.zeros((len(M),1),np.int8)], axis=1).astype(float)
    Ys = 1 - Xs
    return 0.5*np.einsum('ij,jk,ik->i', Xs, A, Xs) + 0.5*np.einsum('ij,jk,ik->i', Ys, A, Ys), Xs

def D2(A):
    n = len(A)
    if n == 1: return 0
    v, _ = internal(A, all_bipartitions(n)); return int(round(v.min()))

# ---------- Corollary 4.2 consistency on all small triangle-free graphs (blow-up invariant => any small
# counterexample would refute BCL Thm 2(a) itself)
best = (0, None)
for n in range(2, 11):
    for A in geng(n):
        r = D2(A)/n**2
        if r > best[0]: best = (r, n)
print(f"max D2(G)/n^2 over ALL triangle-free graphs on <=10 vertices = {best[0]:.6f} (n={best[1]}); 2/47 = {2/47:.6f}; 1/25 = {1/25}")

# ---------- Lemma 2.2: D2(G(2)) = 4 D2(G), hom(C4) and e scale
bad = 0; cnt = 0
for n in range(2, 8):
    for A in geng(n)[::3]:
        B = blowup(A, [2]*n)
        if D2(B) != 4*D2(A): bad += 1
        if abs(np.trace(np.linalg.matrix_power(B,4)) - 16*np.trace(np.linalg.matrix_power(A,4))) > 1e-6: bad += 1
        if B.sum() != 4*A.sum(): bad += 1
        assert is_tf(B)
        cnt += 1
print(f"Lemma 2.2 on {cnt} graphs (k=2): violations of D2/hom/e scaling or triangle-freeness = {bad}")
# k=3 for small ones
bad=0; cnt=0
for n in range(2, 6):
    for A in geng(n):
        B = blowup(A, [3]*n)
        if D2(B) != 9*D2(A): bad += 1
        cnt += 1
print(f"Lemma 2.2 k=3 on {cnt} graphs: D2 violations = {bad}")

# ---------- Lemma 2.1: pair-shift rounding never increases cost and ends at floor(n/2) set
def round_half(A, f):
    f = f.copy(); n = len(A)
    while True:
        frac = [i for i in range(n) if 1e-12 < f[i] < 1-1e-12]
        if len(frac) <= 1: break
        x, y = frac[0], frac[1]
        lo = max(-f[x], f[y]-1); hi = min(1-f[x], f[y])
        cands = []
        for t in (lo, hi):
            g = f.copy(); g[x] += t; g[y] -= t; g = np.clip(g,0,1); cands.append((cost(A,g), g))
        c0 = cost(A, f)
        cb, gb = min(cands, key=lambda u: u[0])
        assert cb <= c0 + 1e-13, (cb, c0)
        f = gb
    return f
viol = 0; tot = 0
for _ in range(400):
    n = int(rng.integers(1, 14)); A = random_tf(rng, n, rng.uniform(0.2,1))
    f = rng.random(n); 
    # project to mass n/2 within [0,1]
    for _ in range(200):
        f = np.clip(f + (n/2 - f.sum())/n, 0, 1)
    if abs(f.sum() - n/2) > 1e-9: continue
    g = round_half(A, f)
    S = [i for i in range(n) if g[i] > 1-1e-9]
    eS = 0.5*A[np.ix_(S,S)].sum()
    if len(S) != n//2 or eS/n**2 > cost(A, f) + 1e-12: viol += 1
    tot += 1
print(f"Lemma 2.1 rounding on {tot} random (graph, fractional half): violations = {viol}")

# ---------- Lemma 3.2: identities (4) and (5) exactly, and the averaged bound
def lemma32(A):
    n = len(A); E = [(i,j) for i in range(n) for j in range(i+1,n) if A[i,j]]
    deg = A.sum(1)
    assert deg.max() < n/2
    rho = Fr(2*len(E), n*n)
    hom = int(round(np.trace(np.linalg.matrix_power(A.astype(np.int64),4))))
    s5 = 0; worst_edge = None
    for (u,v) in E:
        Nu = set(np.nonzero(A[u])[0]); Nv = set(np.nonzero(A[v])[0]); B = set(range(n)) - Nu - Nv
        du, dv = Fr(len(Nu), n), Fr(len(Nv), n); z = 1-du-dv
        p = (Fr(1,2)-du)/z
        assert 0 <= p <= 1
        fu = [Fr(1) if i in Nu else (p if i in B else Fr(0)) for i in range(n)]
        fv = [Fr(1) if i in Nv else (1-p if i in B else Fr(0)) for i in range(n)]
        assert sum(fu) == Fr(n,2) and sum(fv) == Fr(n,2)
        Qu = sum(fu[i]*fu[j] for (i,j) in E)/n**2; Qv = sum(fv[i]*fv[j] for (i,j) in E)/n**2
        eNN = sum(1 for (i,j) in E if (i in Nu and j in Nv) or (i in Nv and j in Nu))
        lhs = (1-p)*Qu + p*Qv; rhs = p*(1-p)*(rho/2 - Fr(eNN, n*n))
        if lhs != rhs: return ('(4) FAILS', u, v, lhs, rhs)
        s5 += eNN
        m = min(Qu, Qv)
        worst_edge = m if worst_edge is None else min(worst_edge, m)
    if 2*s5 != hom: return ('(5) FAILS', 2*s5, hom)
    t = Fr(hom, n**4)
    bound = rho/8 - t/(4*rho)
    return ('ok', worst_edge <= bound, float(worst_edge), float(bound))
res = {'ok':0, 'bad':0, 'boundfail':0}; ntest=0
for _ in range(600):
    kind = rng.integers(0,3)
    if kind == 0: A = random_tf(rng, int(rng.integers(4,15)), rng.uniform(0.2,1))
    elif kind == 1:
        nm, B0 = [('C5',cycle(5)),('P',petersen()),('Cl',clebsch())][int(rng.integers(0,3))]
        A = blowup(B0, rng.integers(1,3,size=len(B0)), rng, rng.uniform(0,0.3))
    else: A = random_bipartite(rng, int(rng.integers(4,15)))
    if A.sum()==0 or A.sum(1).max() >= len(A)/2: continue
    r = lemma32(A); ntest += 1
    if r[0] != 'ok': res['bad'] += 1; print(r)
    else:
        res['ok'] += 1
        if not r[1]: res['boundfail'] += 1
print(f"Lemma 3.2 on {ntest} graphs (Delta<n/2): identity failures = {res['bad']}, averaged-bound failures = {res['boundfail']}")

# ---------- Section 4.2: (13) exactly, then Lemma 4.4 inside Y and (14) per baseline, on actual graphs
def L(al):
    ah = min(al,1-al); return min(4*ah*ah, ah*(1-ah))
def sec42(A, Xmask):
    n = len(A); X = [i for i in range(n) if Xmask[i]]; Y = [i for i in range(n) if not Xmask[i]]
    if len(X) > len(Y): X, Y = Y, X
    nx_, ny = len(X), len(Y)
    eX = int(A[np.ix_(X,X)].sum()//2); eY = int(A[np.ix_(Y,Y)].sum()//2); e = int(A.sum()//2)
    rho = Fr(2*e, n*n); I = Fr(eX+eY, n*n); IY = Fr(eY, n*n)
    s = Fr(ny - nx_, n); a = s/(1+s); c = 1-a
    mu = 4*c*c*IY
    assert Fr(ny, n) == 1/(2*c)
    f1 = np.zeros(n); f1[X] = 1; f1[Y] = float(a)
    f2 = np.zeros(n); f2[Y] = float(c)
    B1 = a*rho/2 + c*I - (1+a)/(4*c)*mu; B2 = mu/4
    fa = [Fr(1) if i in X else a for i in range(n)]; fb = [Fr(0) if i in X else c for i in range(n)]
    Es = [(i,j) for i in range(n) for j in range(i+1,n) if A[i,j]]
    c1 = sum(fa[i]*fa[j] for i,j in Es)/n**2; c2 = sum(fb[i]*fb[j] for i,j in Es)/n**2
    assert c1 == B1 and c2 == B2, ('(13) fails', c1, B1, c2, B2)
    assert sum(fa) == Fr(n,2) and sum(fb) == Fr(n,2)
    out = []
    H = A[np.ix_(Y,Y)]; w = np.full(ny, 1/ny)
    muH = 0.5*w@H@w
    assert abs(muH - float(mu)) < 1e-12
    if muH == 0:
        return [(float(c1), float(B1)), (float(c2), float(B2))], 0
    d = H@w; ee = H@(w*d); S = d*(ee - muH*d)
    xs = np.where((d>0) & (S >= 4*muH**3*(1-1e-12)))[0]
    assert len(xs) > 0
    worst = np.inf
    for base, al, f in ((B1, float(a), f1), (B2, float(c), f2)):
        for x in xs:
            dd = d[x]; z = 1-dd; phi = H[x] - dd
            tp = min((1-al)/z, al/dd) if 0<al<1 else 0.0; tm = min(al/z, (1-al)/dd) if 0<al<1 else 0.0
            cands = []
            for tt in (tp, -tm):
                g = f.copy(); g[Y] = al + tt*phi
                cands.append((cost(A, g), g))
            cb, g = min(cands, key=lambda u: u[0])
            if g.min() < -1e-12 or g.max() > 1+1e-12 or abs(g.sum()-n/2) > 1e-9: return 'INFEASIBLE', None
            target = float(base) - L(float(a))*float(mu)**3/float(c)**2
            worst = min(worst, target - cb)
    return worst, (float(a), float(mu), float(rho), float(I))
worst = np.inf; nt = 0; Fcheck_bad = 0
def Fval(a, mu, r0=7/22, I0=2/47):
    c = 1-a; P = a*r0/2 + c*I0
    return min(P - (1+a)/(4*c)*mu, mu/4) - L(a)/c**2*mu**3
for _ in range(500):
    kind = rng.integers(0,3)
    if kind == 0: A = random_tf(rng, int(rng.integers(5,15)), rng.uniform(0.3,1))
    elif kind == 1:
        nm, B0 = [('C5',cycle(5)),('P',petersen())][int(rng.integers(0,2))]
        sizes = rng.integers(1,3,size=len(B0))
        if sizes.sum() > 15: continue
        A = blowup(B0, sizes, rng, rng.uniform(0,0.3))
    else: A = random_bipartite(rng, int(rng.integers(5,15)))
    n = len(A)
    if A.sum() == 0: continue
    M = all_bipartitions(n); vals, Xs = internal(A, M)
    choice = int(np.argmin(vals)) if rng.random() < 0.6 else int(rng.integers(0, len(M)))   # optimal or arbitrary cut
    r, info = sec42(A, Xs[choice].astype(bool))
    if r == 'INFEASIBLE': print('INFEASIBLE profile'); continue
    if isinstance(r, list): continue
    worst = min(worst, r); nt += 1
    a, mu, rho, I = info
    if rho <= 7/22 and I <= 2/47:
        true_bound = None
print(f"Section 4.2 construction on {nt} (graph, bipartition) pairs: (13) exact every time; "
      f"min over pairs of [ (B_i - L mu^3/c^2) - cost(perturbed half) ] = {worst:.3e} (must be >= 0)")
# mutation control for Lemma 4.4/(14): K_{m,m} uniform, alpha<=1/5, psi=0 is an equality case for (9)
m = 6; A = np.zeros((2*m,2*m)); A[:m,m:] = 1; A[m:,:m] = 1
w = np.full(2*m, 1/(2*m)); muH = 0.5*w@A@w; d = A@w; ee = A@(w*d); S = d*(ee-muH*d)
al = 0.15; x = 0; dd=d[x]; z=1-dd; phi=A[x]-dd
tp = min((1-al)/z, al/dd); tm=min(al/z,(1-al)/dd)
Aq = lambda pi: 0.5*(w*pi)@A@(w*pi)
best = min(Aq(al+tp*phi), Aq(al-tm*phi))
print(f"K_6,6 uniform, alpha=0.15: A(alpha)-best = {Aq(np.full(2*m,al))-best:.10e}; 4L mu^3 = {4*L(al)*muH**3:.10e};"
      f" with 1.01*L the claimed saving {4*1.01*L(al)*muH**3:.10e} would {'FAIL' if Aq(np.full(2*m,al))-best < 4*1.01*L(al)*muH**3 else 'hold'}")
