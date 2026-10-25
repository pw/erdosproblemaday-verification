# Toy check of Lemma 2.7 (wedge law, (2.16)-(2.18)) on explicit bipartite graphs.
# Wedge law (2.11): P(p,q,r) = 1/(|E| d(q)) for (p,q),(r,q) in E.
# Lemma's finite content (codegree <= 2 hypothesis: two distinct points share <= 2 centres):
#   (2.16) every off-diagonal atom pi(p,r) <= M := 2/(|E| d_min)
#   (2.17) P(p=r) = |Q|/|E|   (exact)
#   H(p,r) >= (1-P(p=r)) log(1/M);  H(p) <= log|P|
#   => D = KL(pi || mu x mu) = H(p)+H(r)-H(p,r) <= B := 2 log|P| - (1-|Q|/|E|) log(|E| d_min / 2)
import sys, math, random
import numpy as np, scipy.sparse as sps

def random_codeg2_graph(NP, NQ, d, seed):
    rng = random.Random(seed)
    cover = {}
    rows, cols = [], []
    q = 0; tries = 0
    while q < NQ:
        tries += 1
        if tries > 50 * NQ: raise RuntimeError("could not place centres")
        nb = rng.sample(range(NP), d)
        pairs = [(min(x,y), max(x,y)) for i,x in enumerate(nb) for y in nb[i+1:]]
        if any(cover.get(pr, 0) >= 2 for pr in pairs): continue
        for pr in pairs: cover[pr] = cover.get(pr, 0) + 1
        rows += [q]*d; cols += nb; q += 1
    A = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NQ, NP))
    return A

def analyse(A, label, eps_small=None):
    NQ, NP = A.shape
    dq = np.asarray(A.sum(axis=1)).ravel(); dp = np.asarray(A.sum(axis=0)).ravel()
    keepq = dq > 0; keepp = dp > 0
    A = A[keepq][:, keepp]; dq = dq[keepq]; dp = dp[keepp]
    NQ, NP = A.shape
    E = A.sum()
    W = sps.diags(1.0 / (E * dq))
    pi = (A.T @ W @ A).toarray()          # NP x NP wedge point-pair law
    mu = dp / E
    assert abs(pi.sum() - 1) < 1e-9
    assert np.allclose(pi.sum(axis=0), mu) and np.allclose(pi.sum(axis=1), mu)
    codeg = (A.T @ A).toarray(); np.fill_diagonal(codeg, 0)
    maxcodeg = codeg.max()
    dmin = dq.min()
    M = 2.0 / (E * dmin)
    off = pi.copy(); np.fill_diagonal(off, 0)
    diag = np.trace(pi)
    nz = pi[pi > 0]
    Hpr = -(nz * np.log(nz)).sum()
    Hp = -(mu * np.log(mu)).sum()
    D_direct = (pi[pi > 0] * np.log(pi[pi > 0] / np.outer(mu, mu)[pi > 0])).sum()
    D_ent = 2 * Hp - Hpr
    B = 2 * math.log(NP) - (1 - NQ / E) * math.log(E * dmin / 2)
    res = {
      '|P|': NP, '|Q|': NQ, '|E|': int(E), 'd_min,Q': int(dmin), 'max codeg': int(maxcodeg),
      '(2.16) max offdiag <= M': bool(off.max() <= M * (1 + 1e-12)),
      '(2.17) P(p=r) == |Q|/|E|': bool(abs(diag - NQ / E) < 1e-12),
      'H(p,r) >= (1-P(p=r))log(1/M)': bool(Hpr >= (1 - diag) * math.log(1 / M) - 1e-12),
      'D_direct == H(p)+H(r)-H(p,r)': bool(abs(D_direct - D_ent) < 1e-9),
      'D <= B': bool(D_direct <= B + 1e-12),
    }
    print(f"== {label}")
    for k, v in res.items(): print(f"   {k}: {v}")
    print(f"   D = {D_direct:.4f}   B = {B:.4f}   D/log|P| = {D_direct/math.log(NP):.3f}   B/log|P| = {B/math.log(NP):.3f}   P(p=r) = {diag:.4f}")
    return res, D_direct, B

if __name__ == "__main__":
    ok = True
    # (1) unbalanced toy at the paper's exponents: |P|=t^{1+2a}, |Q|=t^{2+a}, d(q)=t^a
    for (t, a, seed) in [(60, 0.40, 1), (100, 0.35, 2), (150, 0.30, 3)]:
        d = max(2, round(t ** a)); NP = round(t ** (1 + 2 * a)); NQ = round(t ** (2 + a))
        A = random_codeg2_graph(NP, NQ, d, seed)
        res, D, B = analyse(A, f"UNBALANCED t={t}, a={a}: |P|=t^(1+2a)={NP}, |Q|=t^(2+a)={NQ}, d(q)=t^a~{d}")
        L = math.log(t)
        print(f"   D/log t = {D/L:.3f};  paper's leading form a + (2+3a) t^-a = {a + (2+3*a)*t**(-a):.3f};  exact finite B/log t = {B/L:.3f}")
        ok &= all(res.values())
    # (2) balanced toy: |P|=|Q|=N, d(q) ~ N^{1/3} (SST shape)
    for (N, seed) in [(1000, 4), (2400, 5)]:
        d = round(N ** (1/3)); A = random_codeg2_graph(N, N, d, seed)
        res, D, B = analyse(A, f"BALANCED (SST shape) N={N}, d={d}")
        ok &= all(res.values())
        print(f"   balanced: B/log N = {B/math.log(N):.3f} (~1/3 + diag term, does NOT tend to 0)")
    print("ALL LEMMA-2.7 CHECKS PASS ON VALID GRAPHS:", ok)

    print("\n===== CONTROL (hypothesis violated, must FAIL) =====")
    # blocks of 2 points sharing m = B^2 centres: codegree m >> 2
    Bk = 30; m = Bk * Bk
    rows, cols = [], []
    q = 0
    for blk in range(Bk):
        for j in range(m):
            rows += [q, q]; cols += [2 * blk, 2 * blk + 1]; q += 1
    A = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(q, 2 * Bk))
    res, D, B = analyse(A, f"CODEGREE-VIOLATING control: {Bk} blocks K(2,{m})")
    print("   control rejected (some check False):", not all(res.values()))
    print(f"   exact D = log B = {math.log(Bk):.4f}")
