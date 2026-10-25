#!/usr/bin/env python3
"""Check 1c: Lemma 3.1 (norm polynomial as a sum of T monomial determinants) on the toy d = 3,
K = F_{r^3}, 3d = 9 variables per group, M = C(11,3) = 165 monomials, T = C(165,3) = 735130,
for r = 3, 5, 7.  Exact finite-field arithmetic (tables), coefficient tensor computed in full.

We compute the FULL coefficient tensor c[p,q,s] (165^3 entries, each in K) of
    N = prod_{j<d} sigma^j(D),   D = det(Z(X1), Z(X2), Z(X3)),
by expanding the d trilinear factors (no use of the paper's argument), then check:
  (a) every coefficient lies in F_r                                  [N has coefficients in F_r]
  (b) c[p,q,s] = 0 whenever two of p,q,s coincide                    [proof of Lemma 3.1]
  (c) c is antisymmetric under every transposition                   [alternation, d odd]
  (d) positive control on the tensor itself: sum_{p,q,s} c m_p(U1) m_q(U2) m_s(U3) == Nm(det(Z(U1),Z(U2),Z(U3)))
      at random points U_j in F_r^9 (this validates my coefficient extraction)
  (e) Lemma 3.1 identity: N(U) == sum_{p<q<s} c_pqs det[m_p;m_q;m_s](U1,U2,U3)  (the T-term sum)
      at random points and at random label points X(xi) (xi in K)
  (f) (3.4): N(X(xi1),X(xi2),X(xi3)) = Nm(Vandermonde) != 0 for ALL ordered distinct label triples
Mutations (must be REJECTED):
  Ma  d = 2 (even): N = D*sigma(D) is symmetric, (b)/(c)/(e) must fail
  Mb  one nonzero c_pqs (p<q<s) perturbed by +1: (e) must fail at random points
  Mc  no Frobenius (N' = D^d): (a) must fail
"""
import itertools, sys, time
import numpy as np

def find_irreducible(r, d):
    # monic degree-d polynomial with no roots (enough for d = 2, 3)
    for coeffs in itertools.product(range(r), repeat=d):
        poly = list(coeffs) + [1]   # c0 + c1 x + ... + x^d
        if all(sum(poly[i] * pow(x, i, r) for i in range(d + 1)) % r != 0 for x in range(r)):
            return poly
    raise ValueError

class Field:
    def __init__(self, r, d):
        self.r, self.d, self.q = r, d, r ** d
        self.mod = find_irreducible(r, d)
        q = self.q
        self.vec = [self.to_vec(e) for e in range(q)]
        mul = np.zeros((q, q), dtype=np.int32)
        add = np.zeros((q, q), dtype=np.int32)
        for x in range(q):
            vx = self.vec[x]
            for y in range(q):
                vy = self.vec[y]
                add[x, y] = self.from_vec([(a + b) % r for a, b in zip(vx, vy)])
                mul[x, y] = self.from_vec(self.polymulmod(vx, vy))
        self.mul, self.add = mul, add
        self.neg = np.array([self.from_vec([(-a) % r for a in self.vec[x]]) for x in range(q)], dtype=np.int32)

    def to_vec(self, e):
        v = []
        for _ in range(self.d):
            v.append(e % self.r); e //= self.r
        return v

    def from_vec(self, v):
        e = 0
        for i in reversed(range(self.d)):
            e = e * self.r + v[i]
        return e

    def polymulmod(self, a, b):
        r, d = self.r, self.d
        prod = [0] * (2 * d - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % r
        for deg in range(2 * d - 2, d - 1, -1):
            c = prod[deg]
            if c:
                prod[deg] = 0
                for i in range(d):
                    prod[deg - d + i] = (prod[deg - d + i] - c * self.mod[i]) % r
        return prod[:d]

    def m(self, x, y): return int(self.mul[x, y])
    def a(self, x, y): return int(self.add[x, y])
    def pw(self, x, n):
        res, base = 1, x
        while n:
            if n & 1: res = self.m(res, base)
            base = self.m(base, base); n >>= 1
        return res
    def frob(self, x, j): return self.pw(x, self.r ** j)
    def norm(self, x):
        res = 1
        for j in range(self.d): res = self.m(res, self.frob(x, j))
        return res
    def embed(self, c):  # F_r -> K
        return c % self.r

def levi(i1, i2, i3):
    if len({i1, i2, i3}) < 3: return 0
    perm = [i1, i2, i3]; inv = sum(1 for a in range(3) for b in range(a + 1, 3) if perm[a] > perm[b])
    return -1 if inv % 2 else 1

def build(F, frobenius=True):
    r, d = F.r, F.d
    nv = 3 * d
    beta = [F.pw(F.from_vec([0, 1] + [0] * (d - 2)) if d >= 2 else 1, nu) for nu in range(d)]  # omega^nu
    # t[a,b,c] in K, a = i*d + nu
    t = np.zeros((nv, nv, nv), dtype=np.int32)
    for a in range(nv):
        for b in range(nv):
            for c in range(nv):
                e = levi(a // d, b // d, c // d)
                if e == 0: continue
                val = F.m(F.m(beta[a % d], beta[b % d]), beta[c % d])
                t[a, b, c] = val if e == 1 else int(F.neg[val])
    tl = []
    for l in range(d):
        if frobenius:
            fr = np.array([F.frob(x, l) for x in range(F.q)], dtype=np.int32)
            tl.append(fr[t].reshape(-1))
        else:
            tl.append(t.reshape(-1).copy())
    mons = list(itertools.combinations_with_replacement(range(nv), d))
    Mn = len(mons)
    # orderings, padded to d!
    import math
    nfact = math.factorial(d)
    ords = np.zeros((Mn, nfact, d), dtype=np.int32)
    valid = np.zeros((Mn, nfact), dtype=bool)
    for p, mon in enumerate(mons):
        perms = sorted(set(itertools.permutations(mon)))
        for o in range(nfact):
            ords[p, o] = perms[o % len(perms)]
            valid[p, o] = o < len(perms)
    # coefficient tensor
    cten = np.zeros((Mn, Mn, Mn), dtype=np.int32)
    for o1 in range(nfact):
        for o2 in range(nfact):
            for o3 in range(nfact):
                mask = valid[:, o1][:, None, None] & valid[:, o2][None, :, None] & valid[:, o3][None, None, :]
                if not mask.any(): continue
                term = None
                for l in range(d):
                    A = ords[:, o1, l][:, None, None]; Bq = ords[:, o2, l][None, :, None]; Cs = ords[:, o3, l][None, None, :]
                    flat = A * (nv * nv) + Bq * nv + Cs
                    g = tl[l][flat]
                    term = g if term is None else F.mul[term, g]
                cten = np.where(mask, F.add[cten, term], cten)
    return mons, cten, beta

def mon_values(mons, U, r):
    # U: list of 3d ints mod r -> vector of monomial values mod r
    out = np.ones(len(mons), dtype=np.int64)
    for p, mon in enumerate(mons):
        v = 1
        for a in mon: v = v * U[a] % r
        out[p] = v
    return out

def det_field(F, cols):
    # cols: three column vectors (length 3) of K elements; det = sum eps Z1[i1]Z2[i2]Z3[i3]
    tot = 0
    for i1, i2, i3 in itertools.permutations(range(3)):
        e = levi(i1, i2, i3)
        v = F.m(F.m(cols[0][i1], cols[1][i2]), cols[2][i3])
        tot = F.a(tot, v if e == 1 else int(F.neg[v]))
    return tot

def Z_of(F, U, beta):
    d = F.d
    out = []
    for i in range(3):
        acc = 0
        for nu in range(d):
            acc = F.a(acc, F.m(beta[nu], F.embed(U[i * d + nu])))
        out.append(acc)
    return out

def X_of_label(F, xi):
    # coordinates of (1, xi, xi^2) in the polynomial basis omega^nu (beta)
    vals = [1, xi, F.m(xi, xi)]
    U = []
    for i in range(3):
        U.extend(F.vec[vals[i]])   # polynomial-basis coordinates = base-r digits
    return U

def run_case(r, d, rng, frobenius=True, label=""):
    t0 = time.time()
    F = Field(r, d)
    mons, cten, beta = build(F, frobenius=frobenius)
    Mn = len(mons)
    res = {}
    res['M'] = Mn
    res['a_coeffs_in_Fr'] = bool((cten < r).all())
    cr = cten % r if res['a_coeffs_in_Fr'] else None
    idx = np.arange(Mn)
    rep = np.zeros_like(cten, dtype=bool)
    rep |= (idx[:, None, None] == idx[None, :, None])
    rep |= (idx[None, :, None] == idx[None, None, :])
    rep |= (idx[:, None, None] == idx[None, None, :])
    res['b_zero_on_repeats'] = bool((cten[rep] == 0).all())
    negc = F.neg[cten]
    res['c_antisym'] = bool((np.transpose(cten, (1, 0, 2)) == negc).all() and (np.transpose(cten, (0, 2, 1)) == negc).all())
    P, Q, S = np.nonzero((idx[:, None, None] < idx[None, :, None]) & (idx[None, :, None] < idx[None, None, :]))
    res['T_slots'] = len(P)
    coefs = cten[P, Q, S].astype(np.int64)  # K elements
    res['nonzero_slots'] = int((coefs != 0).sum())
    # evaluation identities
    def lhs(U1, U2, U3):
        cols = [Z_of(F, U, beta) for U in (U1, U2, U3)]
        return F.norm(det_field(F, cols))
    nzc = np.nonzero(cten)
    nzvals = cten[nzc]
    def full_tensor_eval(U1, U2, U3):
        m1, m2, m3 = (mon_values(mons, U, r) for U in (U1, U2, U3))
        mm = (m1[nzc[0]] * m2[nzc[1]] % r) * m3[nzc[2]] % r   # F_r values = K elements 0..r-1
        prodK = F.mul[nzvals, mm]
        # K addition = coordinatewise addition mod r in the polynomial basis
        coords = [int(((prodK // (r ** j)) % r).sum() % r) for j in range(F.d)]
        return F.from_vec(coords)
    def T_sum(U1, U2, U3, coefs_r):
        mv = np.stack([mon_values(mons, U, r) for U in (U1, U2, U3)], axis=1)  # (Mn,3)
        a1, a2, a3 = mv[P, 0], mv[P, 1], mv[P, 2]
        b1, b2, b3 = mv[Q, 0], mv[Q, 1], mv[Q, 2]
        c1, c2, c3 = mv[S, 0], mv[S, 1], mv[S, 2]
        det = (a1 * ((b2 * c3 - b3 * c2) % r) - a2 * ((b1 * c3 - b3 * c1) % r) + a3 * ((b1 * c2 - b2 * c1) % r)) % r
        return int((coefs_r * det).sum() % r)
    npts = 40 if not frobenius or d % 2 == 0 else 120
    ok_d = 0; ok_e = 0; tested = 0
    for it in range(npts):
        Us = [[rng.randrange(r) for _ in range(3 * d)] for _ in range(3)]
        L = lhs(*Us)
        if it < 15:
            ok_d += (full_tensor_eval(*Us) == L)
        if res['a_coeffs_in_Fr']:
            ok_e += (T_sum(*Us, coefs % r) == L)  # L is in F_r iff norm (value < r)
        tested += 1
    res['d_tensor_matches_norm'] = f"{ok_d}/{min(npts,15)}"
    res['e_Tsum_matches_N_random'] = f"{ok_e}/{tested}" if res['a_coeffs_in_Fr'] else "n/a (coeffs not in F_r)"
    # label points
    if res['a_coeffs_in_Fr']:
        okl = 0; nl = 0
        for it in range(60):
            xs = [rng.randrange(F.q) for _ in range(3)]
            Us = [X_of_label(F, x) for x in xs]
            # sanity: Z(X(xi)) = (1, xi, xi^2)
            assert Z_of(F, Us[1], beta) == [1, xs[1], F.m(xs[1], xs[1])]
            okl += (T_sum(*Us, coefs % r) == lhs(*Us)); nl += 1
        res['e_Tsum_matches_N_labels'] = f"{okl}/{nl}"
        # Mb mutation: perturb one nonzero slot
        nzslots = np.nonzero(coefs)[0]
        j = nzslots[rng.randrange(len(nzslots))]
        cm = (coefs % r).copy(); cm[j] = (cm[j] + 1) % r
        bad = 0
        for it in range(40):
            Us = [[rng.randrange(r) for _ in range(3 * d)] for _ in range(3)]
            bad += (T_sum(*Us, cm) != lhs(*Us))
        res['Mb_perturbed_slot_mismatches'] = f"{bad}/40"
    # (f) all ordered distinct label triples: N = Nm(Vandermonde) != 0
    if frobenius and d % 2 == 1:
        q = F.q
        zero_found = 0; formula_mismatch = 0; cnt = 0
        labels = list(range(q))
        sample = itertools.permutations(labels, 3) if q <= 27 else (tuple(rng.sample(labels, 3)) for _ in range(20000))
        for xs in sample:
            cols = [[1, x, F.m(x, x)] for x in xs]
            Dv = det_field(F, cols)
            n = F.norm(Dv)
            # Vandermonde prod_{i<j}(xi_j - xi_i)
            V = 1
            for i in range(3):
                for j in range(i + 1, 3):
                    V = F.m(V, F.a(xs[j], int(F.neg[xs[i]])))
            formula_mismatch += (Dv != V)
            zero_found += (n == 0)
            cnt += 1
        res['f_distinct_label_triples'] = cnt
        res['f_det_equals_vandermonde_mismatch'] = formula_mismatch
        res['f_norm_zero_count'] = zero_found
    res['seconds'] = round(time.time() - t0, 1)
    print(f"{label} r={r} d={d} frobenius={frobenius}: {res}", flush=True)
    return res

def main():
    import random
    rng = random.Random(31337)
    for r in (3, 5, 7):
        run_case(r, 3, rng, label="[POSITIVE d=3]")
    for r in (3, 5, 7):
        run_case(r, 2, rng, label="[MUTATION Ma d=2 even]")
    for r in (3, 5):
        run_case(r, 3, rng, frobenius=False, label="[MUTATION Mc no Frobenius]")

if __name__ == "__main__":
    main()
