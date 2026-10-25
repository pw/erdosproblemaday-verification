#!/usr/bin/env python3
"""Check 4: Lemma 5.1 (elliptic-quadric cap in a box) and Lemma 5.2 (restricted shifts, short relations).

(A) Gamma = {(x, y, x^2 - nu y^2)} with nu a NONSQUARE: no three collinear points, exhaustive, q = 5,7,11,13,17.
    Mutation: nu a square (split quadric) and nu = 0 must produce collinear triples.
(B) Paper constants: H in {1,2,3}, q prime >= 2000 H^2, w = floor(q/(1000H^2)); build S = (b+Gamma) cap box with
    |S| >= w^3/q (search over random shifts), check no three collinear in S; count |A| exactly (A depends on a1
    only) and compare with q^3/2 and with the union bound; pick a in A, G in GL_3(F_q); V = G(a+S):
    |V| = |S|, 0 not in V, no three collinear, and EXHAUSTIVE short-relation check over all x with |x| <= H:
      sum x != 0 -> no (u1,u2,u3) in V^3 (repeats allowed) with x1u1+x2u2+x3u3 = 0;
      sum x == 0 -> none with u1,u2,u3 distinct.
(C) Stress: same logic with a much denser cap (w = floor(q/(80)) for H = 2, i.e. 3Hw < q/2 still) so that
    the relation check bites on ~780 points.  Mutations: shift a = 0 (not in A), and a = -v (0 in V): the
    checker must find a forbidden short relation.  Split quadric: collinear triples in S must appear.
"""
import itertools, random, time
import numpy as np
from sympy import nextprime, isprime

def inv_mod_arr(x, q):
    # x int64 array, q prime < 2^31; Fermat
    res = np.ones_like(x); base = x % q; e = q - 2
    while e:
        if e & 1: res = res * base % q
        base = base * base % q; e >>= 1
    return res

def collinear_lines(P, q):
    """P (n,3) distinct points mod q. Return number of lines containing >= 3 points of P (and max points on a line)."""
    n = len(P)
    if n < 3: return 0, min(n, 2)
    I, J = np.triu_indices(n, 1)
    d = (P[J] - P[I]) % q
    f = np.argmax(d != 0, axis=1)                       # first nonzero coordinate
    lead = d[np.arange(len(d)), f]
    inv = inv_mod_arr(lead, q)
    dn = d * inv[:, None] % q
    pf = P[I][np.arange(len(d)), f]
    p0 = (P[I] - pf[:, None] * dn) % q
    key = np.concatenate([f[:, None], dn, p0], axis=1)
    _, cnt = np.unique(key, axis=0, return_counts=True)
    # a line with m points has m(m-1)/2 pairs
    m = (1 + np.sqrt(1 + 8 * cnt)) / 2
    return int((cnt >= 3).sum()), int(round(m.max()))

def is_square(nu, q):
    return pow(nu % q, (q - 1) // 2, q) == 1 if nu % q else True

def gamma_points(q, nu):
    x, y = np.meshgrid(np.arange(q), np.arange(q), indexing='ij')
    x = x.ravel().astype(np.int64); y = y.ravel().astype(np.int64)
    return np.stack([x, y, (x * x - nu * y * y) % q], axis=1)

def box_slice(q, nu, w, b):
    """S = (b + Gamma) cap {0..w-1}^3 ; returns points (n,3) in box coordinates"""
    xp, yp = np.meshgrid(np.arange(w), np.arange(w), indexing='ij')
    xp = xp.ravel().astype(np.int64); yp = yp.ravel().astype(np.int64)
    x = (xp - b[0]) % q; y = (yp - b[1]) % q
    z = (x * x % q - nu * (y * y % q)) % q
    zp = (z + b[2]) % q
    keep = zp < w
    return np.stack([xp[keep], yp[keep], zp[keep]], axis=1)

def nonsquare(q):
    return next(v for v in range(2, q) if not is_square(v, q))

def short_vectors(H):
    out = []
    R = int(H)
    for x in itertools.product(range(-R, R + 1), repeat=3):
        if x == (0, 0, 0) or sum(t * t for t in x) > H * H: continue
        # keep one of +-x
        if tuple(-t for t in x) in out: continue
        out.append(x)
    return out

def relation_check(V, q, H):
    """Exhaustive: returns list of violations (x, sumx, indices)."""
    n = len(V)
    keyc = np.array([1, q, q * q], dtype=object)
    viol = []
    Vl = [tuple(int(c) for c in v) for v in V]
    for x in short_vectors(H):
        sx = sum(x)
        x1, x2, x3 = x
        # map value of x3*u3 -> list of indices
        d3 = {}
        for k3, v in enumerate(Vl):
            key = tuple((x3 * c) % q for c in v)
            d3.setdefault(key, []).append(k3)
        for k1, v1 in enumerate(Vl):
            a = tuple((x1 * c) % q for c in v1)
            for k2, v2 in enumerate(Vl):
                t = tuple((-(a[i] + x2 * v2[i])) % q for i in range(3))
                if t in d3:
                    for k3 in d3[t]:
                        if sx != 0 or len({k1, k2, k3}) == 3:
                            viol.append((x, sx, (k1, k2, k3)))
                            if len(viol) > 20: return viol
    return viol

def random_gl(q, rng):
    while True:
        g = [[rng.randrange(q) for _ in range(3)] for _ in range(3)]
        d = (g[0][0] * (g[1][1] * g[2][2] - g[1][2] * g[2][1]) - g[0][1] * (g[1][0] * g[2][2] - g[1][2] * g[2][0])
             + g[0][2] * (g[1][0] * g[2][1] - g[1][1] * g[2][0])) % q      # exact Python ints
        if d: return np.array(g, dtype=np.int64)

def norm_q(t, q):
    t %= q
    return np.minimum(t, q - t)

def count_A1(q, H, w):
    a1 = np.arange(q, dtype=np.int64)
    ok = np.ones(q, dtype=bool)
    for m in range(1, 3 * H + 1):
        ok &= norm_q(m * a1, q) > 3 * H * w
    return ok

def part_A():
    print("=== (A) Gamma: no three collinear (exhaustive) ===")
    for q in (5, 7, 11, 13, 17):
        nu = nonsquare(q)
        L, mx = collinear_lines(gamma_points(q, nu), q)
        Ls, mxs = collinear_lines(gamma_points(q, 1), q)
        L0, mx0 = collinear_lines(gamma_points(q, 0), q)
        print(f"  q={q} nu={nu} (nonsquare): lines with >=3 points: {L} (max pts/line {mx})  | "
              f"MUTATION nu=1 (square): {Ls} lines (max {mxs})  | MUTATION nu=0: {L0} lines (max {mx0})")

def build_S(q, nu, w, rng, tries=60):
    target = w ** 3 / q
    best = None
    for t in range(tries):
        b = [rng.randrange(q) for _ in range(3)]
        S = box_slice(q, nu, w, b)
        if best is None or len(S) > len(best[1]): best = (b, S)
        if len(S) >= target: return b, S, t + 1
    return best[0], best[1], tries

def part_B(rng):
    print("\n=== (B) paper constants: q >= 2000H^2, w = floor(q/(1000H^2)) ===")
    for H, q0 in ((1, 1_000_000), (2, 4_000_000), (3, 9_000_000)):
        q = int(nextprime(q0)); assert q >= 2000 * H * H
        w = q // (1000 * H * H)
        nu = nonsquare(q) if q < 10**4 else next(v for v in range(2, 1000) if not is_square(v, q))
        b, S, tries = build_S(q, nu, w, rng)
        Lc, mx = collinear_lines(S, q)
        okA = count_A1(q, H, w)
        frac_bad = 1 - okA.mean()
        ub = 3 * H * (6 * H * w + 1) / q
        a1 = rng.randrange(q)
        while not okA[a1]: a1 = rng.randrange(q)
        a = np.array([a1, rng.randrange(q), rng.randrange(q)], dtype=np.int64)
        G = random_gl(q, rng)
        V = ((S + a) % q) @ G.T % q
        distinct = len({tuple(v) for v in V.tolist()}) == len(S)
        zero_in = any((v == 0).all() for v in V)
        LV, mxV = collinear_lines(V, q)
        viol = relation_check(V, q, H) if len(V) <= 400 else None
        print(f"  H={H} q={q} w={w} nu={nu}: |S|={len(S)} (w^3/q={w**3/q:.1f}, shift found after {tries} tries) "
              f"lines>=3 in S: {Lc}; Pr(a1 not allowed) = {frac_bad:.5f} <= union bound {ub:.5f}: {frac_bad <= ub}; "
              f"|A|/q^3 = {okA.mean():.5f} >= 1/2: {okA.mean() >= 0.5}")
        print(f"      V: |V|==|S|: {distinct}; 0 in V: {zero_in}; lines>=3 in V: {LV}; "
              f"short-relation violations (|x|<=H): {'skipped' if viol is None else len(viol)} "
              f"(#x up to sign = {len(short_vectors(H))})")

def part_C(rng, H, q0, wdiv):
    print(f"\n=== (C) stress H={H}: dense cap, 3Hw < q/2 kept, relation check exhaustive ===")
    q = int(nextprime(q0))
    w = q // wdiv
    assert 3 * H * w < q / 2
    nu = nonsquare(q)
    b, S, tries = build_S(q, nu, w, rng)
    Lc, mx = collinear_lines(S, q)
    okA = count_A1(q, H, w)
    print(f"  H={H} q={q} w={w}: |S|={len(S)} (w^3/q={w**3/q:.1f}); lines>=3 in S: {Lc}; |A|/q^3 = {okA.mean():.4f}")
    a1 = rng.randrange(q)
    while not okA[a1]: a1 = rng.randrange(q)
    a = np.array([a1, rng.randrange(q), rng.randrange(q)], dtype=np.int64)
    G = random_gl(q, rng)
    V = ((S + a) % q) @ G.T % q
    t0 = time.time()
    viol = relation_check(V, q, H)
    print(f"  POSITIVE (a in A): short-relation violations: {len(viol)}  [{time.time()-t0:.0f}s]; 0 in V: {any((v==0).all() for v in V)}; lines>=3 in V: {collinear_lines(V, q)[0]}")
    # mutation 1: a = 0 (not allowed)
    V0 = (S % q) @ G.T % q
    t0 = time.time()
    viol0 = relation_check(V0, q, H)
    print(f"  MUTATION a=0 (not in A): violations found: {len(viol0)}{' (first: x=%s, sum=%d, idx=%s)' % viol0[0] if viol0 else ''} [{time.time()-t0:.0f}s]")
    # mutation 2: a = -v for some v in S (0 in V)
    am = (-S[0]) % q
    Vm = ((S + am) % q) @ G.T % q
    violm = relation_check(Vm, q, H)
    print(f"  MUTATION a=-v (a1={int(am[0])}, allowed? {bool(okA[int(am[0])])}): 0 in V: {any((v==0).all() for v in Vm)}; violations: {len(violm)}")
    # mutation 3: split quadric cap in the same box
    bs, Ss, _ = build_S(q, 1, w, rng)
    Ls, mxs = collinear_lines(Ss, q)
    print(f"  MUTATION split quadric nu=1: |S|={len(Ss)}, lines with >=3 points: {Ls} (max {mxs})")
    # mutation 4: dense box WITHOUT the quadric (random points) -- relation checker must fire
    Rp = np.array(rng.sample([(x, y, z) for x in range(30) for y in range(30) for z in range(30)], 400), dtype=np.int64)
    Vr = ((Rp + a) % q) @ G.T % q
    print(f"  MUTATION random 400 points in a 30^3 box (no cap property): lines>=3: {collinear_lines(Vr, q)[0]}; "
          f"relation violations: {len(relation_check(Vr, q, H))}")

def main():
    rng = random.Random(5150)
    part_A()
    part_B(rng)
    part_C(rng, 2, 20000, 80)
    part_C(rng, 3, 60000, 200)

if __name__ == "__main__":
    main()
