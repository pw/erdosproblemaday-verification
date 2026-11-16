"""probe.py -- alternating bilinear maps beta: F_p^d x F_p^d -> F_p^e (class-2 groups G = F_p^d x F_p^e,
(v,c)(w,c') = (v+w, c+c'+B(v,w)) with B - B^T = beta; [g,h] = beta(v,w), so G/Z = V/rad(beta)).

usage: python3 probe.py p d e family count seed0 out.jsonl
families:
  random      e independent uniformly random alternating matrices
  formplusdeg beta_1 = standard nondegenerate symplectic (d even) / max rank, beta_2..e = random of rank 2
  sum2        beta_1 = random form, beta_2 = beta_1 + (random rank-2 form)   [pencil containing two close forms]
  tracesub    d = 2r, V = F_q^2 (q = p^r), beta_j = Tr(c_j * det) for a random e-dim F_p-subspace <c_j> of F_q
  directsum   V = V1 + V2 (d1 = d//2 even part), beta_1 = symplectic on V1, beta_2 = symplectic on V2 (needs e>=2)

For each map: twin classes by identical commutation rows (same centraliser), z, omega lower bound
(heuristic + exact MCQ with time limit, proven flag), a upper bound from a verified proper colouring
(DSATUR, then tabucol / SAT at K = T(omega_lb) if needed), alpha (exact w/ time limit) for a lower bound
max(omega, ceil(k/alpha)).  Certifies a <= T(omega) via a_ub <= T(omega_lb) (T nondecreasing) and
z <= (T(omega)-1)^2 via z <= (T(omega_lb)-1)^2.
"""
import sys, json, time, random
import numpy as np
from graphlib import (T, check_clique, check_colouring, c_clique, c_heurclique, c_dsatur, c_tabu,
                      colour_sat)


def all_vectors(p, d):
    X = np.zeros((p ** d, d), dtype=np.int64)
    for idx in range(p ** d):
        t = idx
        for i in range(d):
            X[idx, i] = t % p
            t //= p
    return X


def rand_alt(p, d, rnd):
    M = np.zeros((d, d), dtype=np.int64)
    for i in range(d):
        for j in range(i + 1, d):
            x = rnd.randrange(p)
            M[i, j] = x
            M[j, i] = (-x) % p
    return M


def std_symp(p, d):
    M = np.zeros((d, d), dtype=np.int64)
    for i in range(0, d - 1, 2):
        M[i, i + 1] = 1
        M[i + 1, i] = p - 1
    return M


def rank2_alt(p, d, rnd):
    # u ^ w : (u w^T - w u^T)
    while True:
        u = np.array([rnd.randrange(p) for _ in range(d)], dtype=np.int64)
        w = np.array([rnd.randrange(p) for _ in range(d)], dtype=np.int64)
        M = (np.outer(u, w) - np.outer(w, u)) % p
        if M.any():
            return M


# ---- finite field F_q, q = p^r, via a monic irreducible polynomial ----
def find_irred(p, r, rnd):
    import itertools
    def polymulmod(a, b, f):
        res = [0] * (2 * r)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                res[i + j] = (res[i + j] + x * y) % p
        for k in range(2 * r - 1, r - 1, -1):
            c = res[k]
            if c:
                for t in range(r + 1):
                    res[k - r + t] = (res[k - r + t] - c * f[t]) % p
        return res[:r]
    # test irreducibility by checking that x generates a field: brute force: no root in any proper subfield
    # simple approach: enumerate monic polys, check no factor of degree <= r/2 by trial division
    def divides(g, f):
        f = list(f)
        dg = len(g) - 1
        for k in range(len(f) - 1, dg - 1, -1):
            c = f[k] * pow(g[-1], p - 2, p) % p
            if c:
                for t in range(dg + 1):
                    f[k - dg + t] = (f[k - dg + t] - c * g[t]) % p
        return not any(f[:dg])
    for coeffs in itertools.product(range(p), repeat=r):
        f = list(coeffs) + [1]
        if f[0] == 0:
            continue
        ok = True
        for dg in range(1, r // 2 + 1):
            for gc in itertools.product(range(p), repeat=dg):
                g = list(gc) + [1]
                if divides(g, f):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return f, (lambda a, b: polymulmod(a, b, f))
    raise ValueError


def trace_forms(p, r, e, rnd):
    """beta_j(x,y) = Tr(c_j (x1 y2 - x2 y1)), x = (x1,x2) in F_q^2, coordinates = poly basis."""
    f, mul = find_irred(p, r, rnd)
    q = p ** r
    def el(i):  # int -> coefficient list
        return [(i // p ** k) % p for k in range(r)]
    def add(a, b):
        return [(x + y) % p for x, y in zip(a, b)]
    def neg(a):
        return [(-x) % p for x in a]
    # trace of basis elements: Tr(a) = sum a^{p^k}
    def power(a, n):
        res = [1] + [0] * (r - 1)
        b = a
        while n:
            if n & 1:
                res = mul(res, b)
            b = mul(b, b)
            n >>= 1
        return res
    def tr(a):
        s = [0] * r
        b = a
        for k in range(r):
            s = add(s, b)
            b = power(b, p)
        assert all(x == 0 for x in s[1:]), 'trace not in prime field'
        return s[0]
    # choose e linearly independent c_j (as F_p-vectors) at random
    while True:
        cs = [el(rnd.randrange(1, q)) for _ in range(e)]
        A = np.array(cs, dtype=np.int64)
        if rank_mod(A, p) == e:
            break
    d = 2 * r
    basis = []
    for i in range(d):
        v = [0] * d
        v[i] = 1
        basis.append(v)
    Ms = []
    for c in cs:
        M = np.zeros((d, d), dtype=np.int64)
        for i in range(d):
            for j in range(d):
                x1, x2 = basis[i][:r], basis[i][r:]
                y1, y2 = basis[j][:r], basis[j][r:]
                det = add(mul(x1, y2), neg(mul(x2, y1)))
                M[i, j] = tr(mul(c, det))
        Ms.append(M)
    return Ms, {'irred': f, 'c': cs}


def rank_mod(A, p):
    A = A.copy() % p
    rk = 0
    rows, cols = A.shape
    for c in range(cols):
        piv = None
        for r_ in range(rk, rows):
            if A[r_, c] % p:
                piv = r_
                break
        if piv is None:
            continue
        A[[rk, piv]] = A[[piv, rk]]
        inv = pow(int(A[rk, c]), p - 2, p)
        A[rk] = (A[rk] * inv) % p
        for r_ in range(rows):
            if r_ != rk and A[r_, c]:
                A[r_] = (A[r_] - A[r_, c] * A[rk]) % p
        rk += 1
    return rk


def make_map(p, d, e, family, seed):
    rnd = random.Random(seed * 1000003 + p * 101 + d * 11 + e)
    info = {}
    if family == 'random':
        Ms = [rand_alt(p, d, rnd) for _ in range(e)]
    elif family == 'formplusdeg':
        Ms = [std_symp(p, d)] + [rank2_alt(p, d, rnd) for _ in range(e - 1)]
    elif family == 'sum2':
        A = rand_alt(p, d, rnd)
        Ms = [A, (A + rank2_alt(p, d, rnd)) % p] + [rand_alt(p, d, rnd) for _ in range(e - 2)]
    elif family == 'tracesub':
        assert d % 2 == 0
        Ms, info = trace_forms(p, d // 2, e, rnd)
    elif family == 'directsum':
        d1 = (d // 2) // 2 * 2
        M1 = np.zeros((d, d), dtype=np.int64)
        M1[:d1, :d1] = std_symp(p, d1)
        M2 = np.zeros((d, d), dtype=np.int64)
        M2[d1:, d1:] = std_symp(p, d - d1)
        Ms = [M1, M2] + [rand_alt(p, d, rnd) for _ in range(e - 2)]
    else:
        raise ValueError(family)
    for M in Ms:
        assert (M.diagonal() % p == 0).all() and ((M + M.T) % p == 0).all(), 'not alternating'
    return Ms, info


def build_graph(p, d, Ms):
    X = all_vectors(p, d)
    N = X.shape[0]
    nonc = np.zeros((N, N), dtype=bool)
    for M in Ms:
        B = (X @ M @ X.T) % p
        nonc |= (B != 0)
    assert (nonc == nonc.T).all() and not nonc.diagonal().any()
    rad = ~nonc.any(axis=1)
    z = N // int(rad.sum())
    classes = {}
    for v in range(N):
        if rad[v]:
            continue
        key = np.packbits(nonc[v]).tobytes()
        classes.setdefault(key, []).append(v)
    reps = [vs[0] for vs in classes.values()]
    k = len(reps)
    sub = nonc[np.ix_(reps, reps)]
    adj = [0] * k
    for i in range(k):
        row = sub[i]
        b = 0
        for j in np.nonzero(row)[0]:
            b |= 1 << int(j)
        adj[i] = b
    return z, k, adj, reps


def analyse_map(p, d, e, family, seed, clique_t=3.0, hard_t=60.0):
    """cheap certificate first (heuristic clique + DSATUR); exact/expensive steps only when the
    certificate is tight (a_ub >= T(omega_lb)) or fails."""
    t0 = time.time()
    Ms, info = make_map(p, d, e, family, seed)
    z, k, adj, reps = build_graph(p, d, Ms)
    rec = {'p': p, 'd': d, 'e': e, 'family': family, 'seed': seed, 'z': z, 'k': k}
    if k == 0:
        rec.update({'omega_lb': 1, 'omega_proven': True, 'a_ub': 1, 'a_lb': 1, 'cert_a': True, 'cert_z': True, 'T': 1,
                    'ratio_ub': 1.0, 'tight': False})
        return rec, Ms
    iters = 300 if k <= 255 else 60
    C = c_heurclique(k, adj, iters, seed + 1)
    w = len(C)
    col = c_dsatur(k, adj)
    a_ub = max(col) + 1
    how = 'dsatur'
    tight = a_ub >= T(w) or (w >= 3 and z > (T(w) - 1) ** 2)
    Cx, pr = c_clique(k, adj, hard_t if tight else clique_t, w + 1)
    if Cx is not None:
        C, w = Cx, len(Cx)
    omega_proven = pr
    assert check_clique(adj, C)
    t = T(w)
    if a_ub > t:
        for s in range(1, 4):
            it = max(20000, min(2000000, int(4e8 // (k * max(t, 1)))))
            c2 = c_tabu(k, adj, t, it, s)
            if c2 is not None:
                col, a_ub, how = c2, max(c2) + 1, 'tabu'
                break
    if a_ub > t and len(Ms) == 1:
        c4 = spread_colouring(p, d, Ms[0], reps)
        if check_colouring(k, adj, c4) and max(c4) + 1 < a_ub:
            col, a_ub, how = c4, max(c4) + 1, 'spread(isometry to F_q trace model)'
    if a_ub > t and k <= 400:
        c3 = colour_sat(k, adj, t, C)
        if c3 is not None:
            col, a_ub, how = c3, max(c3) + 1, 'sat'
        else:
            how = 'sat-UNSAT-at-T(omega_lb)'
    assert check_colouring(k, adj, col)
    alpha, pra = None, False
    a_lb = w
    if a_ub >= t:   # potential equality/violation: get a counting lower bound
        full = (1 << k) - 1
        cadj = [(~adj[v]) & full & ~(1 << v) for v in range(k)]
        I, pra = c_clique(k, cadj, hard_t, 0)
        alpha = len(I)
        if pra:
            a_lb = max(w, -(-k // alpha))
    rec.update({'omega_lb': w, 'omega_proven': omega_proven, 'clique': [int(reps[c]) for c in C], 'T': t,
                'a_ub': a_ub, 'a_ub_method': how, 'alpha': alpha, 'alpha_proven': pra, 'a_lb': a_lb,
                'cert_a': a_ub <= t, 'cert_z': z <= (t - 1) ** 2 if w >= 3 else True,
                'ratio_ub': a_ub / t, 'tight': tight, 'secs': round(time.time() - t0, 2)})
    if info:
        rec['info'] = {kk: (vv if not isinstance(vv, np.ndarray) else vv.tolist()) for kk, vv in info.items()}
    return rec, Ms


def main():
    p, d, e = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    family, count, seed0, out = sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    with open(out, 'a') as f:
        for s in range(seed0, seed0 + count):
            rec, Ms = analyse_map(p, d, e, family, s)
            flag = (not rec['cert_a']) or (not rec['cert_z']) or (rec['a_lb'] >= rec['T'] and rec['omega_lb'] >= 9)
            if flag:
                rec['matrices'] = [M.tolist() for M in Ms]
            f.write(json.dumps(rec) + '\n')
            f.flush()
            print('%s p=%d d=%d e=%d seed=%d z=%d k=%d omega>=%d%s a<=%d (%s) a>=%d T=%d certA=%s certZ=%s %.1fs%s' % (
                family, p, d, e, s, rec['z'], rec['k'], rec['omega_lb'], '(exact)' if rec['omega_proven'] else '',
                rec['a_ub'], rec.get('a_ub_method', '-'), rec['a_lb'], rec['T'], rec['cert_a'], rec['cert_z'],
                rec.get('secs', 0), '  <<< FLAG' if flag else ''))
            sys.stdout.flush()



# ---------------- U3: explicit spread colouring for a single form (e = 1) ----------------
def gf_ops(p, r):
    f, mul = find_irred(p, r, None)
    def power(a, n):
        res = [1] + [0] * (r - 1)
        b = a
        while n:
            if n & 1:
                res = mul(res, b)
            b = mul(b, b)
            n >>= 1
        return res
    inv = lambda a: power(a, p ** r - 2)
    return mul, inv


def symplectic_pairs(p, d, form):
    """symplectic Gram-Schmidt over F_p. form(u,v) -> int. Returns (pairs [(u,w)], radical basis)."""
    S = [np.eye(d, dtype=np.int64)[i] for i in range(d)]
    pairs = []
    while True:
        found = None
        for i in range(len(S)):
            for j in range(len(S)):
                if form(S[i], S[j]) % p:
                    found = (i, j)
                    break
            if found:
                break
        if not found:
            break
        i, j = found
        u, w = S[i], S[j]
        w = (w * pow(int(form(u, w)) % p, p - 2, p)) % p   # beta(u,w) = 1
        rest = [S[t] for t in range(len(S)) if t not in (i, j)]
        S = [(s - form(s, w) * u + form(s, u) * w) % p for s in rest]
        pairs.append((u, w))
    rad = [s for s in S if s.any()]
    return pairs, rad


def spread_colouring(p, d, M, reps):
    """colour each twin-class representative (a vector index) by the F_q-line of its image in the
    trace model F_q^2 (q = p^r, 2r = rank M) under an isometry V/rad -> F_q^2.  Returns colours."""
    form = lambda u, v: int(u @ M @ v) % p
    pairs, rad = symplectic_pairs(p, d, form)
    r = len(pairs)
    Ms0, info = trace_forms(p, r, 1, random.Random(0))
    # force c = 1 for the model: recompute with c = 1
    mul, inv = gf_ops(p, r)
    B0 = Ms0[0]
    # rebuild B0 with c = 1 explicitly
    f, _ = find_irred(p, r, None)
    def tr1(a):
        # trace via Gram: use info-free recomputation
        s = [0] * r
        b = list(a)
        for _ in range(r):
            s = [(x + y) % p for x, y in zip(s, b)]
            # b <- b^p
            res = [1] + [0] * (r - 1)
            for _k in range(p):
                res = mul(res, b)
            b = res
        return s[0]
    dd = 2 * r
    B0 = np.zeros((dd, dd), dtype=np.int64)
    E = np.eye(dd, dtype=np.int64)
    for i in range(dd):
        for j in range(dd):
            x1, x2, y1, y2 = list(E[i][:r]), list(E[i][r:]), list(E[j][:r]), list(E[j][r:])
            det = [(a - b) % p for a, b in zip(mul(x1, y2), mul(x2, y1))]
            B0[i, j] = tr1(det)
    form0 = lambda u, v: int(u @ B0 @ v) % p
    pairs0, rad0 = symplectic_pairs(p, dd, form0)
    assert len(pairs0) == r and not rad0, 'trace model not nondegenerate'
    # basis matrix P (columns u_1,w_1,...,u_r,w_r, rad...) and its inverse mod p
    cols = []
    for u, w in pairs:
        cols += [u, w]
    cols += rad
    P = np.array(cols, dtype=np.int64).T % p
    Pinv = inv_mod(P, p)
    imgs = []
    for u, w in pairs0:
        imgs += [u, w]
    Q = np.array(imgs, dtype=np.int64).T % p   # dd x 2r
    X = all_vectors(p, d)
    colours = []
    keys = {}
    for v in reps:
        c = (Pinv @ X[v]) % p
        y = (Q @ c[:2 * r]) % p
        x1, x2 = list(y[:r]), list(y[r:])
        if any(x1):
            key = (1,) + tuple(mul(inv(x1), x2))
        else:
            key = (0,) + tuple(x1)  # (0, 1) line
            key = (0,)
        colours.append(keys.setdefault(key, len(keys)))
    # check isometry on basis
    phi = lambda x: (Q @ ((Pinv @ x) % p)[:2 * r]) % p
    for i in range(d):
        for j in range(d):
            ei, ej = np.eye(d, dtype=np.int64)[i], np.eye(d, dtype=np.int64)[j]
            assert form(ei, ej) == form0(phi(ei), phi(ej)), 'isometry check failed'
    return colours


def inv_mod(A, p):
    n = A.shape[0]
    Aug = np.concatenate([A % p, np.eye(n, dtype=np.int64)], axis=1)
    r_ = 0
    for c in range(n):
        piv = next(i for i in range(r_, n) if Aug[i, c] % p)
        Aug[[r_, piv]] = Aug[[piv, r_]]
        Aug[r_] = (Aug[r_] * pow(int(Aug[r_, c]), p - 2, p)) % p
        for i in range(n):
            if i != r_ and Aug[i, c]:
                Aug[i] = (Aug[i] - Aug[i, c] * Aug[r_]) % p
        r_ += 1
    return Aug[:, n:]


if __name__ == '__main__':
    main()
