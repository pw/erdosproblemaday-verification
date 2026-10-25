#!/usr/bin/env python3
"""Check 2: Lemmas 4.1 (diagonal form, row lattice) and 4.2 (special-linear orbit bound) over Z/h,
h = B^k in {4, 8, 9, 25, 27}.

Independent instruments (none uses the paper's elimination or stabilizer estimate):
  * D, E from DETERMINANTAL DIVISORS of the integer matrix [C~ ; hI] (6x3): D = Delta2/Delta1, E = Delta3/Delta2.
  * index [Z^3 : Lambda_C] by brute force = h^3 / |row span mod h| (row span enumerated as all x.C).
  * E Z^3 in Lambda_C by brute-force membership of E e_i in the row span.
  * orbit sizes |O_C|:
      h = 4  : EXACT orbit partition of all 4^9 matrices under the generators E_ij(1) of SL_3(Z/4)
               (union-find); positive control: orbit of I == brute-force count of det == 1.
      h >= 8 : |SL_3(Z/h)| / |Stab_SL(C)|, Stab counted by brute force over (Ann_left C)^3 where
               Ann_left is found by brute force over (Z/h)^3; cross-checked against the h = 4 partition.
               For the few classes with |Ann|^3 too large (h = 25, 27, D*E >= ~h^1.7) we count
               Stab_SL(diag(1,D,E)) via det(I+Y) = (1+a2)(1+b3) - a3 b2 (exact enumeration; valid by
               conjugation), and this route is itself cross-checked against brute force where both run.
  * the paper's own elimination (proof of Lemma 4.1) is implemented and checked: C == P diag(1,B^b,B^e) Q,
    P, Q invertible, and (b, e) agree with the determinantal divisors.
Claims checked: (4.1) index = DE and E Z^3 <= Lambda_C; 'b >= j iff all 2x2 minors vanish mod B^j';
(4.2) |O_C| >= (21/64) h^8 / (D^3 E^2)  -> report worst ratio.
Mutations (must be REJECTED): (i) D^3E^2 -> D^2E^2;  (ii) det-image factor dropped:
|O_C| >= (21/64) h^9/(D^3E^3).
"""
import itertools, math, random, sys, time
import numpy as np

def vg(v, h):
    """B-adic: return gcd(v, h) for integer arrays."""
    return np.gcd(np.asarray(v, dtype=np.int64) % h, h)

def det3(M):  # M (...,3,3) int64
    return (M[..., 0, 0] * (M[..., 1, 1] * M[..., 2, 2] - M[..., 1, 2] * M[..., 2, 1])
            - M[..., 0, 1] * (M[..., 1, 0] * M[..., 2, 2] - M[..., 1, 2] * M[..., 2, 0])
            + M[..., 0, 2] * (M[..., 1, 0] * M[..., 2, 1] - M[..., 1, 1] * M[..., 2, 0]))

def minors2(M):
    out = []
    for (i1, i2) in ((0, 1), (0, 2), (1, 2)):
        for (j1, j2) in ((0, 1), (0, 2), (1, 2)):
            out.append(M[..., i1, j1] * M[..., i2, j2] - M[..., i1, j2] * M[..., i2, j1])
    return np.stack(out, axis=-1)

def det_divisors(M, h):
    """M (...,3,3) entries in [0,h). Return (D, E, unit) via determinantal divisors of [M; hI]."""
    m1 = np.gcd.reduce(np.concatenate([M.reshape(M.shape[:-2] + (9,)), np.full(M.shape[:-2] + (1,), h)], axis=-1), axis=-1)
    unit = (m1 == 1)
    mn = minors2(M)
    m2 = np.gcd.reduce(mn, axis=-1)           # gcd of integer 2x2 minors (may be 0)
    D2 = np.gcd(np.gcd(m2, h * m1), h * h)    # Delta2 = gcd(2x2 minors of [M;hI])
    dt = det3(M)
    D3 = np.gcd(np.gcd(np.gcd(dt, h * m2), h * h * m1), h ** 3)
    D1 = m1
    Dv = D2 // D1
    Ev = D3 // D2
    return Dv, Ev, unit

def rowspan_size(Mlist, h):
    """brute force |{x.C mod h}| for each C in Mlist (n,3,3)"""
    X = np.array(list(itertools.product(range(h), repeat=3)), dtype=np.int64)  # h^3 x 3
    sizes = []; spans = []
    for C in Mlist:
        rows = (X @ C) % h
        enc = rows[:, 0] * h * h + rows[:, 1] * h + rows[:, 2]
        u = np.unique(enc)
        sizes.append(len(u)); spans.append(set(u.tolist()))
    return sizes, spans

def inv_mod(a, h):
    return pow(int(a), -1, h)

def paper_diagonalize(C, B, k):
    """Literal implementation of the elimination in the proof of Lemma 4.1 over Z/h.
    Returns (b, e, P, Q) with C == P diag(1,B^b,B^e) Q (mod h)."""
    h = B ** k
    A = [[int(x) % h for x in row] for row in C]
    P = [[int(i == j) for j in range(3)] for i in range(3)]   # we track A = Pinv C Qinv; keep P, Q with C = P A Q
    Q = [[int(i == j) for j in range(3)] for i in range(3)]
    def val(x):
        x %= h
        if x == 0: return k
        v = 0
        while x % B == 0: x //= B; v += 1
        return v
    def swap_rows(i, j):
        A[i], A[j] = A[j], A[i]
        for row in P: row[i], row[j] = row[j], row[i]           # C = P A Q, A' = S A -> P' = P S^{-1} = P S
    def swap_cols(i, j):
        for row in A: row[i], row[j] = row[j], row[i]
        Q[i], Q[j] = Q[j], Q[i]
    def add_row(dst, src, c):   # A[dst] += c*A[src]; P' = P E^{-1}: col_src(P) -= c*col_dst(P)
        A[dst] = [(x + c * y) % h for x, y in zip(A[dst], A[src])]
        for row in P: row[src] = (row[src] - c * row[dst]) % h
    def add_col(dst, src, c):   # col dst += c * col src ; Q' = E^{-1} Q: row_src(Q) -= c*row_dst(Q)
        for row in A: row[dst] = (row[dst] + c * row[src]) % h
        Q[src] = [(x - c * y) % h for x, y in zip(Q[src], Q[dst])]
    def scale_row(i, u):        # A[i] *= u (unit) ; P' col_i *= u^{-1}
        ui = inv_mod(u, h)
        A[i] = [(x * u) % h for x in A[i]]
        for row in P: row[i] = (row[i] * ui) % h
    # step 1: unit entry to (0,0)
    pos = next((i, j) for i in range(3) for j in range(3) if math.gcd(A[i][j], h) == 1)
    swap_rows(0, pos[0]); swap_cols(0, pos[1])
    scale_row(0, inv_mod(A[0][0], h))
    for i in (1, 2): add_row(i, 0, -A[i][0])
    for j in (1, 2): add_col(j, 0, -A[0][j])
    # step 2: 2x2 block
    blk = [(i, j) for i in (1, 2) for j in (1, 2)]
    if all(A[i][j] % h == 0 for i, j in blk):
        b = e = k
    else:
        i0, j0 = min(blk, key=lambda ij: val(A[ij[0]][ij[1]]))
        b = val(A[i0][j0])
        swap_rows(1, i0); swap_cols(1, j0)
        u = (A[1][1] // B ** b) % h
        scale_row(1, inv_mod(u, h))     # A[1][1] = B^b
        assert A[1][1] == B ** b % h
        # clear: A[2][1] divisible by B^b; A[2][1] = c B^b
        c = (A[2][1] // B ** b); add_row(2, 1, -c)
        c = (A[1][2] // B ** b); add_col(2, 1, -c)
        x = A[2][2] % h
        e = val(x)
        if e < k:
            u = (x // B ** e) % h
            scale_row(2, inv_mod(u, h))
        assert e >= b
    Dg = [[1, 0, 0], [0, B ** b % h, 0], [0, 0, B ** e % h]]
    for i in range(3):
        for j in range(3):
            assert A[i][j] % h == Dg[i][j] % h, (A, b, e)
    return b, e, np.array(P, dtype=np.int64), np.array(Q, dtype=np.int64)

def is_unit_matrix(M, h):
    return math.gcd(int(round(det3(np.array(M, dtype=np.int64)))) % h, h) == 1

def sl_order_bruteforce(h):
    """count det == 1 mod h over all h^9 matrices, chunked by first row"""
    vals = np.array(list(itertools.product(range(h), repeat=3)), dtype=np.int64)  # h^3 rows
    r2 = vals[:, None, :]; r3 = vals[None, :, :]
    # cross product of rows 2 and 3 for all pairs: (h^3, h^3, 3)
    cx = np.stack([r2[..., 1] * r3[..., 2] - r2[..., 2] * r3[..., 1],
                   r2[..., 2] * r3[..., 0] - r2[..., 0] * r3[..., 2],
                   r2[..., 0] * r3[..., 1] - r2[..., 1] * r3[..., 0]], axis=-1) % h
    cx = cx.reshape(-1, 3)
    cnt = 0; cntgl = 0
    for row1 in vals:
        d = (cx @ row1) % h
        cnt += int((d == 1).sum())
        cntgl += int((np.gcd(d, h) == 1).sum())
    return cnt, cntgl

def ann_left(C, h, X):
    rows = (X @ C) % h
    return X[(rows == 0).all(axis=1)]

def stab_sl_bruteforce(C, h, X):
    A = ann_left(C, h, X)
    n = len(A)
    cnt = 0
    I = np.eye(3, dtype=np.int64)
    # pairs (y2,y3)
    y2 = np.repeat(A, n, axis=0); y3 = np.tile(A, (n, 1))
    for y1 in A:
        M = np.empty((n * n, 3, 3), dtype=np.int64)
        M[:, 0, :] = I[0] + y1; M[:, 1, :] = I[1] + y2; M[:, 2, :] = I[2] + y3
        cnt += int((det3(M) % h == 1).sum())
    return cnt, n

def stab_sl_diag(D, E, h):
    annD = np.arange(0, h, h // D, dtype=np.int64) if D <= h else None   # {x: D x = 0} = (h/D) Z/h
    annE = np.arange(0, h, h // E, dtype=np.int64)
    a2, a3 = np.meshgrid(annD, annD, indexing='ij'); a2 = a2.ravel(); a3 = a3.ravel()
    b2, b3 = np.meshgrid(annE, annE, indexing='ij'); b2 = b2.ravel(); b3 = b3.ravel()
    cnt = 0
    for i in range(len(a2)):
        dd = ((1 + a2[i]) * (1 + b3) - a3[i] * b2) % h
        cnt += int((dd == 1).sum())
    return cnt * len(annD) * len(annE)

def bound_ratio(orbit, D, E, h):
    return orbit * D ** 3 * E ** 2 / h ** 8

# ------------------------------------------------------------------ h = 4 exhaustive
def exhaustive_h4():
    h = 4; B = 2; k = 2
    n = h ** 9
    idx = np.arange(n, dtype=np.int64)
    ent = np.stack([(idx // h ** p) % h for p in range(9)], axis=1).reshape(n, 3, 3)
    def enc(M):
        flat = M.reshape(-1, 9)
        return (flat * (h ** np.arange(9))).sum(axis=1)
    gens = []
    for i in range(3):
        for j in range(3):
            if i == j: continue
            M = ent.copy(); M[:, i, :] = (M[:, i, :] + M[:, j, :]) % h
            gens.append(enc(M))
    lab = idx.copy()
    it = 0
    while True:
        it += 1
        old = lab.copy()
        for g in gens:
            m = np.minimum(lab, lab[g])
            lab2 = m.copy()
            lab2[g] = np.minimum(m[g], m)
            lab = lab2
        lab = lab[lab]; lab = lab[lab]
        if (lab == old).all(): break
    sizes = np.bincount(lab, minlength=n)
    orbit = sizes[lab]
    dets = det3(ent) % h
    sl_bf = int((dets == 1).sum())
    I_idx = int(enc(np.eye(3, dtype=np.int64)[None])[0])
    print(f"h=4: union-find converged in {it} rounds; |orbit(I)| = {orbit[I_idx]}, brute-force #det==1: {sl_bf}  "
          f"(positive control {'PASS' if orbit[I_idx]==sl_bf else 'FAIL'})")
    Dv, Ev, unit = det_divisors(ent, h)
    sel = np.nonzero(unit)[0]
    print(f"h=4: {len(sel)} matrices with a unit entry (of {n})")
    # index brute force for all unit-entry matrices
    X = np.array(list(itertools.product(range(h), repeat=3)), dtype=np.int64)
    pres = np.zeros((len(sel), 64), dtype=bool)
    for st in range(0, len(sel), 16384):
        chunk = sel[st:st + 16384]
        rows = np.einsum('xi,nij->nxj', X, ent[chunk]) % h            # (chunk, 64, 3)
        code = rows[..., 0] * 16 + rows[..., 1] * 4 + rows[..., 2]
        sub = np.zeros((len(chunk), 64), dtype=bool)
        np.put_along_axis(sub, code, True, axis=1)
        pres[st:st + len(chunk)] = sub
    spansize = pres.sum(axis=1)
    index = h ** 3 // spansize
    idx_ok = (index == Dv[sel] * Ev[sel]).all()
    # E e_i in span
    Esel = Ev[sel]
    ok_E = True
    for i in range(3):
        v = np.zeros((len(sel), 3), dtype=np.int64); v[:, i] = Esel % h
        c = v[:, 0] * 16 + v[:, 1] * 4 + v[:, 2]
        ok_E &= bool(pres[np.arange(len(sel)), c].all())
    # b characterization via minors: b >= j iff all minors == 0 mod B^j
    mn = minors2(ent[sel]) % h
    bch_ok = True
    bvals = np.round(np.log2(Dv[sel])).astype(int)
    for j in range(1, k + 1):
        allzero = (mn % (B ** j) == 0).all(axis=1)
        bch_ok &= bool((allzero == (bvals >= j)).all())
    ratios = bound_ratio(orbit[sel].astype(np.float64), Dv[sel].astype(np.float64), Ev[sel].astype(np.float64), h)
    worst = ratios.min()
    w = sel[ratios.argmin()]
    # mutations
    mut1 = orbit[sel] * Dv[sel] ** 2 * Ev[sel] ** 2 / h ** 8
    mut2 = orbit[sel] * Dv[sel] ** 3 * Ev[sel] ** 3 / h ** 9
    print(f"h=4: index==DE for all: {idx_ok}; E Z^3 in Lambda for all: {ok_E}; b-minor characterization: {bch_ok}")
    print(f"h=4: worst |O|D^3E^2/h^8 = {worst:.6f} (claim >= 21/64 = {21/64:.6f}) at C={ent[w].tolist()} D={Dv[w]} E={Ev[w]} |O|={orbit[w]}")
    print(f"h=4: MUTATION D^2E^2: violations {int((mut1 < 21/64).sum())} of {len(sel)}; worst ratio {mut1.min():.6f}")
    print(f"h=4: MUTATION no det-image (h^9/(D^3E^3)): violations {int((mut2 < 21/64).sum())} of {len(sel)}; worst ratio {mut2.min():.6f}")
    # paper's elimination on a sample
    rng = random.Random(4)
    bad = 0
    for t in rng.sample(list(sel), 3000):
        b, e, P, Q = paper_diagonalize(ent[t], B, k)
        Dg = np.diag([1, B ** b % h, B ** e % h])
        okm = ((P @ Dg @ Q) % h == ent[t] % h).all()
        okinv = math.gcd(int(det3(P)) % h, h) == 1 and math.gcd(int(det3(Q)) % h, h) == 1
        okbe = (B ** b == Dv[t]) and (B ** e == Ev[t])
        bad += not (okm and okinv and okbe)
    print(f"h=4: paper elimination on 3000 samples: failures {bad}")
    # per (b,e) class worst ratio
    classes = {}
    for D_, E_, rt in zip(Dv[sel].tolist(), Ev[sel].tolist(), ratios.tolist()):
        classes[(D_, E_)] = min(classes.get((D_, E_), 9e9), rt)
    print("h=4: worst ratio per (D,E):", {kk: round(v, 4) for kk, v in sorted(classes.items())})
    return ent, orbit, sel, Dv, Ev

def random_unit_entry(h, rng):
    while True:
        C = np.array([[rng.randrange(h) for _ in range(3)] for _ in range(3)], dtype=np.int64)
        if math.gcd(int(np.gcd.reduce(C.ravel())), h) == 1 and any(math.gcd(int(x), h) == 1 for x in C.ravel()):
            return C

def random_gl(h, rng):
    while True:
        M = np.array([[rng.randrange(h) for _ in range(3)] for _ in range(3)], dtype=np.int64)
        if math.gcd(int(det3(M)) % h, h) == 1: return M

def sampled(h, B, k, slorder, rng, nrand, nper_class, cross_ent=None):
    X = np.array(list(itertools.product(range(h), repeat=3)), dtype=np.int64)
    mats = [random_unit_entry(h, rng) for _ in range(nrand)]
    for b in range(k + 1):
        for e in range(b, k + 1):
            for _ in range(nper_class):
                P = random_gl(h, rng); Q = random_gl(h, rng)
                Dg = np.diag([1, B ** b % h, B ** e % h]).astype(np.int64)
                mats.append((P @ Dg @ Q) % h)
    worst = (9e9, None); fails = dict(index=0, Ez=0, bchar=0, elim=0, bound=0, route_mismatch=0)
    mut1v = 0; mut2v = 0; per_class = {}; nbrute = 0; ndiag = 0
    Ms = np.array(mats)
    Dv, Ev, unit = det_divisors(Ms, h)
    sizes, spans = rowspan_size(Ms, h)
    for t, C in enumerate(mats):
        D_, E_ = int(Dv[t]), int(Ev[t])
        assert unit[t]
        if h ** 3 // sizes[t] != D_ * E_: fails['index'] += 1
        for i in range(3):
            v = [0, 0, 0]; v[i] = E_ % h
            if v[0] * h * h + v[1] * h + v[2] not in spans[t]: fails['Ez'] += 1
        mn = minors2(C) % h
        bb = round(math.log(D_, B))
        for j in range(1, k + 1):
            if ((mn % B ** j == 0).all()) != (bb >= j): fails['bchar'] += 1
        b, e, P, Q = paper_diagonalize(C, B, k)
        Dg = np.diag([1, B ** b % h, B ** e % h])
        if not (((P @ Dg @ Q) % h == C % h).all() and B ** b == D_ and B ** e == E_): fails['elim'] += 1
        annsz = D_ * E_
        if annsz ** 3 <= 2.5e7:
            st, n = stab_sl_bruteforce(C, h, X); nbrute += 1
            if n != annsz: fails['index'] += 1000
            if annsz ** 3 <= 2e6:   # cross-check the diag route
                if stab_sl_diag(D_, E_, h) != st: fails['route_mismatch'] += 1
        else:
            st = stab_sl_diag(D_, E_, h); ndiag += 1
        orb = slorder // st
        assert slorder % st == 0
        if cross_ent is not None:
            pass
        rt = bound_ratio(orb, D_, E_, h)
        if rt < 21 / 64: fails['bound'] += 1
        if rt < worst[0]: worst = (rt, C.tolist(), D_, E_, orb)
        per_class[(D_, E_)] = min(per_class.get((D_, E_), 9e9), rt)
        if orb * D_ ** 2 * E_ ** 2 / h ** 8 < 21 / 64: mut1v += 1
        if orb * D_ ** 3 * E_ ** 3 / h ** 9 < 21 / 64: mut2v += 1
    print(f"h={h}: {len(mats)} matrices ({nrand} random unit-entry + {nper_class}/class reps); stab brute={nbrute}, via diag={ndiag}")
    print(f"   failures: {fails}")
    print(f"   worst |O|D^3E^2/h^8 = {worst[0]:.6f} (claim >= {21/64:.6f}) at D={worst[2]} E={worst[3]} |O|={worst[4]}")
    print(f"   per-class worst: {{ {', '.join(f'{kk}: {v:.4f}' for kk, v in sorted(per_class.items()))} }}")
    print(f"   MUTATION D^2E^2 violations: {mut1v}/{len(mats)};  MUTATION no det-image violations: {mut2v}/{len(mats)}")

def main():
    t0 = time.time()
    ent, orbit, sel, Dv, Ev = exhaustive_h4()
    # cross-validate stabilizer route against exact h=4 partition on a sample
    h = 4; X = np.array(list(itertools.product(range(h), repeat=3)), dtype=np.int64)
    sl4 = int(orbit[0 * 0 + int((np.eye(3, dtype=np.int64).ravel() * (4 ** np.arange(9))).sum())])
    rng = random.Random(44)
    mism = 0
    for t in rng.sample(list(sel), 400):
        st, n = stab_sl_bruteforce(ent[t], h, X)
        if sl4 // st != orbit[t]: mism += 1
    print(f"h=4: stabilizer-route orbit sizes vs exact partition on 400 samples: mismatches {mism}  (cross-validation)")
    print(f"[{time.time()-t0:.0f}s]")
    # SL orders
    sl = {}
    for hh in (8, 9):
        c, cg = sl_order_bruteforce(hh)
        sl[hh] = c
        print(f"|SL_3(Z/{hh})| brute force = {c}; |GL| = {cg}; formula h^9(1-1/B)(1-1/B^2)(1-1/B^3)/phi(h) = "
              f"{hh**9*(1-1/(2 if hh==8 else 3))*(1-1/(2 if hh==8 else 3)**2)*(1-1/(2 if hh==8 else 3)**3)/((1-1/(2 if hh==8 else 3))*hh):.1f}")
        print(f"[{time.time()-t0:.0f}s]", flush=True)
    for p, kk in ((5, 2), (3, 3)):
        c, cg = sl_order_bruteforce(p)
        sl[p ** kk] = c * p ** (8 * (kk - 1))
        print(f"|SL_3(F_{p})| brute force = {c} -> |SL_3(Z/{p**kk})| = {sl[p**kk]} (kernel of reduction has p^(8(k-1)) elements)")
    rng = random.Random(2026)
    for hh, B, k, nr, npc in ((8, 2, 3, 600, 4), (9, 3, 2, 600, 4), (25, 5, 2, 250, 2), (27, 3, 3, 150, 2)):
        sampled(hh, B, k, sl[hh], rng, nr, npc)
        print(f"[{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    main()
