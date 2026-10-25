#!/usr/bin/env python3
"""Numerical check of Lemma 3.1 / Cor 3.2 / Cor 3.3 of the OpenAI unit-distance preprint (Sec. 3).
Seat `prediction`.  Everything finite and exact except where marked MC (Monte Carlo over tests).
Run: nice -n 19 python3 -I prediction_sim.py
"""
import numpy as np, math, itertools, sys
rng = np.random.default_rng(20261014)

# ---------------------------------------------------------------- the law
def law_from_adj(adj):
    adj = adj[adj.sum(1) > 0][:, adj.sum(0) > 0]          # "delete atoms of zero marginal mass"
    E = adj.sum()
    omega = adj / E                                       # uniform edge law
    mu = omega.sum(1); kappa = omega.sum(0)
    w_p_given_q = omega / kappa                           # columns sum to 1
    # wedge law (3.1): pi(p,r) = sum_q kappa(q) w(p|q) w(r|q)
    pi = (w_p_given_q * kappa) @ w_p_given_q.T
    ref = np.outer(mu, mu)
    m = pi > 0
    D = float((pi[m] * np.log(pi[m] / ref[m])).sum())
    return dict(adj=adj, omega=omega, mu=mu, kappa=kappa, wpq=w_p_given_q, pi=pi, D=D)

def random_unbalanced(nP=30, nQ=200, dlo=2, dhi=8):
    adj = np.zeros((nP, nQ))
    for q in range(nQ):
        d = rng.integers(dlo, dhi + 1)
        adj[rng.choice(nP, d, replace=False), q] = 1
    return adj

# ---------------------------------------------------------------- tests
# a test = (c : P->[M] int array, F : M x d feature matrix, G : Q x d coefficient matrix)
def random_test(law, M, d, B, Bp, aligned=True):
    nP = law['mu'].size
    c = rng.integers(0, M, nP)
    F = rng.normal(size=(M, d)); F *= B / np.maximum(np.linalg.norm(F, axis=1, keepdims=True), 1e-12)
    if aligned:   # adversarial-but-legal: g(q) aligned with E_{p|q} f(c(p)) - E_mu f(c(p))
        fc = F[c]
        v = law['wpq'].T @ fc - law['mu'] @ fc
        nv = np.linalg.norm(v, axis=1).max()
        G = Bp * v / nv if nv > 0 else np.zeros_like(v)
    else:
        G = rng.normal(size=(law['kappa'].size, d)); G *= Bp / np.linalg.norm(G, axis=1, keepdims=True)
    return (c, F, G)

def refine(labels, c):
    """history partition after appending code c: returns new integer labels"""
    key = labels * (c.max() + 1) + c
    _, new = np.unique(key, return_inverse=True)
    return new

def residual(law, labels, test, cond=True):
    """U(x) = f(c(x)) - m_{T,H(x)} with m_{T,h} = sum_x mu_h(x) f(c(x))   (cond=False: wrong, uses mu)"""
    c, F, G = test
    mu = law['mu']; fc = F[c]
    if not cond:
        return fc - mu @ fc
    U = np.empty_like(fc)
    for h in np.unique(labels):
        idx = labels == h
        muh = mu[idx] / mu[idx].sum()
        U[idx] = fc[idx] - muh @ fc[idx]
    return U

def phi(law, U, G):
    """|E_{(p,q)~omega} <U(p), g(q)>|"""
    return abs(float((law['omega'] * (U @ G.T)).sum()))

def frozen_sequence_stats(law, tests, cond=True, check_chain=False, wrong_ref=False):
    K = len(tests); nP = law['mu'].size
    labels = np.zeros(nP, dtype=np.int64)
    phis, Xs, inner, chain = [], [], [], 0.0
    for j, t in enumerate(tests):
        c, F, G = t
        U = residual(law, labels, t, cond)
        phis.append(phi(law, U, G))
        EU = law['wpq'].T @ U                          # E_{p~w(.|q)} U(p), shape Q x d
        X = float((law['kappa'] * (EU ** 2).sum(1)).sum())
        I = float((law['pi'] * (U @ U.T)).sum())
        Xs.append(X); inner.append(I)
        if check_chain:
            chain += chain_term(law, labels, c, wrong_ref)
        labels = refine(labels, c)
    return np.array(phis), np.array(Xs), np.array(inner), chain, labels

def chain_term(law, labels, c, wrong_ref=False):
    """E_{(p,r)~pi} KL(a_{j,H(p),H(r)} || b_{j,H(p),H(r)})  with b = (c)_*mu_h (x) (c)_*mu_h'.
    wrong_ref=True uses the WRONG reference (c)_*mu_h (x) (c)_*mu_h (first endpoint's history twice)."""
    pi, mu = law['pi'], law['mu']; M = c.max() + 1
    tot = 0.0
    H = np.unique(labels)
    push = {h: np.bincount(c[labels == h], weights=mu[labels == h], minlength=M) / mu[labels == h].sum() for h in H}
    for h in H:
        for hp in H:
            blk = pi[np.ix_(labels == h, labels == hp)]
            w = blk.sum()
            if w <= 0: continue
            a = np.zeros((M, M))
            np.add.at(a, (c[labels == h][:, None].repeat(blk.shape[1], 1), c[labels == hp][None, :].repeat(blk.shape[0], 0)), blk)
            a /= w
            b = np.outer(push[h], push[h] if wrong_ref else push[hp])
            m = a > 0
            if np.any(b[m] == 0):
                return math.inf
            tot += w * float((a[m] * np.log(a[m] / b[m])).sum())
    return tot

def transcript_KL(law, labels):
    """KL of the image of pi under (tau(p),tau(r)) vs image of mu x mu   (data processing: <= D)"""
    pi, mu = law['pi'], law['mu']
    H = np.unique(labels)
    A = np.array([[pi[np.ix_(labels == h, labels == g)].sum() for g in H] for h in H])
    m = np.array([mu[labels == h].sum() for h in H]); Bm = np.outer(m, m)
    k = A > 0
    return float((A[k] * np.log(A[k] / Bm[k])).sum())

def bound(B, Bp, D, K):  return 4 * B * Bp * (D / K) ** 0.25
def sharp(B, Bp, D, K):  return 2 ** 1.25 * B * Bp * (D / K) ** 0.25

out = print
# =============================================================== Experiment A: random unbalanced graph
out("=== A. random unbalanced bipartite graph, |P|=30, |Q|=200, center degrees uniform in {2..8}")
law = law_from_adj(random_unbalanced())
out(f"|P|={law['mu'].size} |Q|={law['kappa'].size} |E|={int(law['adj'].sum())}  D=KL(pi||mu x mu)={law['D']:.6f} nats")
out(f"marginal check: pi rows sum to mu: {np.allclose(law['pi'].sum(1), law['mu'])}, cols: {np.allclose(law['pi'].sum(0), law['mu'])}")
M, d, B, Bp = 3, 2, 1.0, 1.0
out(f"tests: c uniform random P->[{M}], f random on sphere radius B={B} in R^{d}, g aligned with neighbourhood mean, |g|<=B'={Bp}")
worst_ratio = 0.0
for K in [1, 2, 4, 8, 16, 32, 64]:
    seq_avgs = []; viol = 0; chain_ok = True; id_err = 0.0; c310_ok = True
    for rep in range(200):
        tests = [random_test(law, M, d, B, Bp) for _ in range(K)]
        ph, Xs, inner, chain, labels = frozen_sequence_stats(law, tests, check_chain=(rep < 20))
        id_err = max(id_err, float(np.max(np.abs(Xs - inner))))          # (3.11) exact identity
        if (inner < -1e-12).any(): c310_ok = False
        if inner.mean() > 8 * B * B * math.sqrt(law['D'] / (2 * K)) + 1e-12: c310_ok = False   # (3.10)
        if rep < 20:
            tk = transcript_KL(law, labels)
            if not (abs(chain - tk) < 1e-9 and tk <= law['D'] + 1e-12): chain_ok = False      # (3.8) chain rule + DP
        a = ph.mean(); seq_avgs.append(a)
        if a > sharp(B, Bp, law['D'], K) + 1e-12: viol += 1
        worst_ratio = max(worst_ratio, a / bound(B, Bp, law['D'], K))
    # direct fresh-test MC of (3.7): J uniform, prefix T_1..T_{J-1}, independent fresh T
    fresh = []
    for s in range(3000):
        J = rng.integers(1, K + 1)
        labels = np.zeros(law['mu'].size, dtype=np.int64)
        for _ in range(J - 1):
            labels = refine(labels, random_test(law, M, d, B, Bp)[0])
        T = random_test(law, M, d, B, Bp)
        fresh.append(phi(law, residual(law, labels, T), T[2]))
    fresh = np.array(fresh)
    out(f"K={K:3d}: per-frozen-sequence max avg_j Phi_j={max(seq_avgs):.4f}  mean={np.mean(seq_avgs):.4f} | fresh-test MC (3.7) LHS={fresh.mean():.4f}+-{fresh.std()/math.sqrt(len(fresh)):.4f} | "
        f"2^(5/4)BB'(D/K)^(1/4)={sharp(B,Bp,law['D'],K):.4f}  4BB'(D/K)^(1/4)={bound(B,Bp,law['D'],K):.4f} | seq>sharp: {viol}/200 | "
        f"(3.8)chain==transcriptKL<=D: {chain_ok} | (3.11) max|diff|={id_err:.1e} | (3.10)&nonneg: {c310_ok}")
out(f"worst observed (per-sequence average)/(4BB'(D/K)^(1/4)) over all K: {worst_ratio:.4f}")

# ---------------------------------------------------------------- Cor 3.2 on the same law
out("\n=== A'. Cor 3.2 acceptance (A_T(q) = codes of actual neighbours of q, so s0 = 0), M=3")
def acc_test(law, M):
    c = rng.integers(0, M, law['mu'].size)
    A = np.zeros((law['kappa'].size, M), bool)
    pp, qq = np.nonzero(law['adj']); A[qq, c[pp]] = True
    F = np.eye(M); G = A.astype(float)                       # f = e_c (|f|=1), g = indicator vector (|g|<=sqrt M)
    return (c, F, G), A
def s_pred(law, labels, c, A):
    fail = 0.0
    for h in np.unique(labels):
        idx = labels == h; muh = law['mu'][idx] / law['mu'][idx].sum()
        fail += float((law['omega'][idx].sum(0) * ((~A[:, c[idx]]) @ muh)).sum())
    return fail
for K in [4, 16, 64]:
    per_seq = []; ident = 0.0; coll = []
    for rep in range(200):
        labels = np.zeros(law['mu'].size, dtype=np.int64); vals = []
        for j in range(K):
            t, A = acc_test(law, M)
            sp = s_pred(law, labels, t[0], A)
            U = residual(law, labels, t)
            # identity: E<f(c(p)) - m, g(q)> = (1 - s_act) - (1 - s_pred) = s_pred - s_act, s_act = 0
            ident = max(ident, abs(float((law['omega'] * (U @ t[2].T)).sum()) - sp))
            vals.append(sp); labels = refine(labels, t[0])
        per_seq.append(np.mean(vals))
    b = 2 ** 1.25 * math.sqrt(M) * (law['D'] / K) ** 0.25
    out(f"K={K:3d}: per-sequence avg_j s_pred,j : max={max(per_seq):.4f} mean={np.mean(per_seq):.4f}  <= 2^(5/4) sqrt(M)(D/K)^(1/4)={b:.4f} [paper 4 sqrt(M)(D/K)^(1/4)={4*math.sqrt(M)*(law['D']/K)**0.25:.4f}] : {max(per_seq) <= b}; "
        f"identity <f-m,g> == s_pred - s_act : max err {ident:.1e}")
# a fixed history for the exact (3.13)/(3.14) checks: prefix of 3 acceptance tests
labels = np.zeros(law['mu'].size, dtype=np.int64)
for _ in range(3): labels = refine(labels, acc_test(law, M)[0][0])
best = (None, labels, 4)
# (3.13)/(3.14) exact checks for this fixed history
labels = best[1]; mu = law['mu']
joint = np.zeros((mu.size, mu.size))
for p in range(mu.size):
    idx = labels == labels[p]; joint[p, idx] = mu[p] * mu[idx] / mu[idx].sum()
out(f"(3.13) marginals: p-marginal==mu {np.allclose(joint.sum(1), mu)}, phat-marginal==mu {np.allclose(joint.sum(0), mu)}; "
    f"(3.14) P(p=phat)={np.trace(joint):.4f} <= |H(P)| max mu = {len(np.unique(labels))*mu.max():.4f}")
eq = np.zeros_like(joint)
for h in np.unique(labels):
    idx = labels == h; muh = mu[idx] / mu[idx].sum()
    eq[np.ix_(idx, idx)] += mu[idx].sum() * np.outer(muh, muh)
out(f"'equivalent way to draw the pair' (h~mu(H=h), then two iid from mu_h) equals (3.13) pair law: {np.allclose(eq, joint)}")

# =============================================================== Experiment B: planted two-block law, D = log 2; FAIL controls
out("\n=== B. planted two-block law (D = log 2 exactly) and FAIL controls")
nP, nQ = 30, 200
adj = np.zeros((nP, nQ)); adj[:15, :100] = 1; adj[15:, 100:] = 1
lawB = law_from_adj(adj)
out(f"D = {lawB['D']:.6f}, log 2 = {math.log(2):.6f}")
blk = (np.arange(nP) >= 15).astype(int)
half = (blk, np.array([[1.0], [-1.0]]), np.where(np.arange(nQ) >= 100, -1.0, 1.0)[:, None])   # B = B' = 1, d = 1
trivial = (np.zeros(nP, dtype=int), np.array([[1.0]]), np.zeros((nQ, 1)))
K = 10000
bB = bound(1, 1, lawB['D'], K)
ph, _, _, _, _ = frozen_sequence_stats(lawB, [half] * K)
out(f"K={K}: correct conditioning  avg_j Phi_j = {ph.mean():.6f}  (expect 1/K = {1/K})  <= 4BB'(D/K)^(1/4) = {bB:.4f}: {ph.mean() <= bB}")
ph, _, _, _, _ = frozen_sequence_stats(lawB, [half] * K, cond=False)
out(f"FAIL control 1 (prediction from mu, history ignored): avg Phi = {ph.mean():.4f} > bound {bB:.4f}: VIOLATES = {ph.mean() > bB}")
ph, _, _, _, _ = frozen_sequence_stats(lawB, [trivial] * (K - 1) + [half])
out(f"FAIL control 2 (fresh test NOT identically distributed with the prefix tests: prefix trivial, fresh = half test): Phi at the fresh test = {ph[-1]:.4f} > bound {bB:.4f}: VIOLATES = {ph[-1] > bB}")
# FAIL control 3: wrong reference law in (3.8)
tests = [random_test(law, M, d, B, Bp) for _ in range(8)]
_, _, _, ch_ok, labels = frozen_sequence_stats(law, tests, check_chain=True)
_, _, _, ch_bad, _ = frozen_sequence_stats(law, tests, check_chain=True, wrong_ref=True)
out(f"FAIL control 3 (law A, K=8): chain sum with correct b = {ch_ok:.6f} (== transcript KL {transcript_KL(law, labels):.6f} <= D={law['D']:.6f}); "
    f"with WRONG reference b=(c)_*mu_h x (c)_*mu_h : {ch_bad:.6f} -> exceeds D: {ch_bad > law['D']}")

# =============================================================== Experiment C: Cor 3.3 pieces
out("\n=== C. Cor 3.3: feature/coefficient inner product == hashed strict-cross indicator (exhaustive)")
def ip(a, b, aq, bq, L, coef=-2.0):
    f = np.concatenate([np.eye(L)[a], np.eye(L)[b], np.eye(L * L)[a * L + b]])
    g = np.concatenate([np.eye(L)[aq], np.eye(L)[bq], coef * np.eye(L * L)[aq * L + bq]])
    return float(f @ g), float(np.linalg.norm(f)), float(np.linalg.norm(g))
for coef, tag in [(-2.0, 'paper (-2)'), (-1.0, 'FAIL control 4 (coef -1)')]:
    bad = 0; norms = set()
    for L in [2, 3, 4]:
        for a, b, aq, bq in itertools.product(range(L), repeat=4):
            v, nf, ng = ip(a, b, aq, bq, L, coef); norms.add((round(nf, 6), round(ng, 6)))
            sc = float((a == aq) != (b == bq))
            if abs(v - sc) > 1e-12: bad += 1
    out(f"{tag}: mismatches over all L in {{2,3,4}} = {bad}; norms (|f|,|g|) = {sorted(norms)} (paper: sqrt3={math.sqrt(3):.6f}, sqrt6={math.sqrt(6):.6f})")

out("\n=== C'. hashing: P(true strict cross != hashed strict cross) <= 2/L for any two fixed true states (exact enumeration)")
def sc(y, z): return (y[0] == z[0]) != (y[1] == z[1])
for L in [2, 3]:
    labsA = range(3); labsB = range(3)
    worst = 0.0; worst_bad = 0.0
    states = list(itertools.product(labsA, labsB))
    hashes = list(itertools.product(range(L), repeat=3))
    # biased hash for the control: all labels mapped to 0 w.p. 1/2, else uniform
    for y in states:
        for z in states:
            cnt = 0
            for hA in hashes:
                for hB in hashes:
                    if sc(y, z) != sc((hA[y[0]], hB[y[1]]), (hA[z[0]], hB[z[1]])): cnt += 1
            worst = max(worst, cnt / len(hashes) ** 2)
            # non-uniform hash (FAIL control 5): each label hashed to value 0 with prob 1/2, else uniform on [L]
            pv = np.full(L, 0.5 / L); pv[0] += 0.5
            P = 0.0
            for hA in hashes:
                for hB in hashes:
                    w = np.prod([pv[x] for x in hA]) * np.prod([pv[x] for x in hB])
                    if sc(y, z) != sc((hA[y[0]], hB[y[1]]), (hA[z[0]], hB[z[1]])): P += w
            worst_bad = max(worst_bad, P)
    cu = 1 / L; cb = 0.25 * (1 + 1 / L) ** 2 + (L - 1) / (4 * L * L)
    fu = max(2 * cu * (1 - cu), cu); fb = max(2 * cb * (1 - cb), cb)
    out(f"L={L}: uniform independent hash worst flip prob (enumeration) = {worst:.4f}, formula max(2c(1-c),c) = {fu:.4f}, <= 2/L = {2/L:.4f}: {worst <= 2/L + 1e-12};  "
        f"non-uniform hash: enumeration {worst_bad:.4f}, formula {fb:.4f}")
for L in [8, 16]:
    cu = 1 / L; cb = 0.25 * (1 + 1 / L) ** 2 + (L - 1) / (4 * L * L)
    fu = max(2 * cu * (1 - cu), cu); fb = max(2 * cb * (1 - cb), cb)
    out(f"L={L}: uniform hash worst flip = {fu:.4f} <= 2/L={2/L:.4f}: {fu <= 2/L};  FAIL control 5 (hash value 0 w.p. 1/2+1/(2L)): worst flip = {fb:.4f} > 2/L: {fb > 2/L}")

out("\n=== C''. 'predicted point sampled using no current hash' is load-bearing (MC)")
# law: 200 points in 100 groups of 2; 300 centres, each adjacent to both points of one group.
# states: A_p = group(p), B_p = p (distinct); A_q = group of its neighbours, B_q = -1.  Every edge is a TRUE strict cross (s0 = 0).
nG = 100; nPc = 2 * nG; nQc = 300
adjc = np.zeros((nPc, nQc)); gq = np.concatenate([np.arange(nG), rng.integers(0, nG, nQc - nG)])  # every group has a centre
for q in range(nQc): adjc[2 * gq[q], q] = adjc[2 * gq[q] + 1, q] = 1
lawC = law_from_adj(adjc)
Ap = np.arange(nPc) // 2; Bpl = np.arange(nPc); Aq = gq; Bq = np.full(nQc, -1)
pp, qq = np.nonzero(lawC['adj'])
def flip_rate(cheat, Lh, reps):
    tot = 0.0
    for _ in range(reps):
        hA = rng.integers(0, Lh, nG); hB = rng.integers(0, Lh, nPc + 1)    # hB[-1] is the hash of label -1
        hp = hA[Ap] * Lh + hB[Bpl]
        diff = 0.0
        for p, q in zip(pp, qq):
            if cheat: xs = np.nonzero(hp == hp[p])[0]
            else:     xs = np.arange(nPc)
            muh = lawC['mu'][xs] / lawC['mu'][xs].sum()
            tru = ((Ap[xs] == Aq[q]) != (Bpl[xs] == Bq[q])).astype(float)
            hsh = ((hA[Ap[xs]] == hA[Aq[q]]) != (hB[Bpl[xs]] == hB[-1])).astype(float)
            diff += lawC['omega'][p, q] * float(muh @ np.abs(tru - hsh))
        tot += diff
    return tot / reps
for Lh in [4, 8]:
    r_ok = flip_rate(False, Lh, 40); r_ch = flip_rate(True, Lh, 40)
    out(f"L={Lh}: predicted-pair E|true - hashed|: hash-free prediction (mu) {r_ok:.4f} <= 2/L={2/Lh}: {r_ok <= 2/Lh};  "
        f"FAIL control 6 (prediction drawn from p's CURRENT hashed fibre): {r_ch:.4f} > 2/L: {r_ch > 2/Lh}")
