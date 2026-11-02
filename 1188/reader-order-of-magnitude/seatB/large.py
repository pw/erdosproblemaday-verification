#!/usr/bin/env python3
"""Large instances of the split construction whose period is far too big for an exhaustive check.

mode prop47 X : the exact parameters of Section 4.1 (I = primes in (X^{1/5}, X^{1/4}], G = primes in
                (2X^{2/5}, P), P = largest prime <= sqrt(X/2)), depth-one trees, random paddings.
mode tree   X K : deep trees built by the algorithm in the proof of Lemma 4.10 (a_e, b_e, L_e),
                with relaxed (non-asymptotic) windows, I = {11,13,17,19}, paddings s*r, s <= 12 {2,3,5,7}-smooth,
                r prime >= 23, D_p = I-numbers d with 2X/p^2 < d and X/(pd) >= 40.

Checks (all exact, z represented by its residues modulo r^{E_r} for every prime r <= P):
  * moduli pairwise distinct, all in [2, X]; every padding divides M_F(q) and is coprime to j(q)
  * the explicit private integer of the proof of Prop 4.3 lies in its own class and in no other
  * covering, by sampling: every split fibre x 30 random points, every fibre x 1 point,
    200 multiples of M_F(P), 20000 uniform points of Z/L
  * the count prod_{p,d} L_p(d)! and the Lemma 4.10 bookkeeping (identity N_1 = sum_e L_e/e, N_1 <= p-1,
    |P_{p,d}| - l(d) < L_p(d) <= |P_{p,d}|).
A NEGATIVE control is run at the end: one leaf class is deleted, and the sampler must find an
uncovered point in that fibre; one padding is duplicated, and the distinctness check must fail.
"""
import sys, random, math, time, itertools
from fractions import Fraction
from math import gcd, prod, log, lgamma
import numpy as np
from cover import primes_upto, crt

def spf_sieve(n):
    spf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == 0:
            blk = spf[i * i::i]
            blk[blk == 0] = i
            spf[i * i::i] = blk
    idx = np.nonzero(spf == 0)[0]
    spf[idx] = idx
    return spf

class Inst:
    def __init__(s, X, P, I, seed):
        s.X, s.P, s.I = X, P, sorted(I)
        s.Iset = set(I)
        s.rng = random.Random(seed)
        s.primes = primes_upto(P)
        s.spf = spf_sieve(X)
        s.E = {r: max(e for e in range(1, 64) if r ** e < P) for r in s.primes if r < P}
        s.E[P] = 1
        # F-prime-powers < P
        s.QF = []
        for r in s.primes:
            if r >= P or r in s.Iset: continue
            q = r
            while q < P:
                s.QF.append(q); q *= r
        s.QF.sort()
        s.trees = {}   # (q,u) -> list of leaves (path tuple of (c,v)) ; [()] if unsplit
        s.pad = {}     # (q,u,path) -> sigma
        s.iota, s.tau = {}, [None] * P

    def fac(s, n):
        f = {}
        while n > 1:
            r = int(s.spf[n]); f[r] = f.get(r, 0) + 1; n //= r
        return f

    def jq(s, q): return int(s.spf[q])

    def divides_MF(s, sigma, q):
        """sigma | M_F(q)  <=>  sigma is I-free and every component of sigma is < q."""
        for r, e in s.fac(sigma).items():
            if r in s.Iset or r ** e >= q: return False
        return True

    def unsplit_pool(s, q, need):
        """first `need` integers sigma <= X/q with sigma | M_F(q) and gcd(sigma, j)=1 (Lemma 4.6(a)/4.9(a))."""
        j = s.jq(q); out = []; sig = 1; lim = s.X // q
        while len(out) < need:
            if sig > lim: raise RuntimeError(f"unsplit pool too small at q={q}")
            if sig % j and s.divides_MF(sig, q): out.append(sig)
            sig += 1
        return out

    def finish(s):
        """unsplit fibres everywhere not yet assigned, then iota and tau (Lemma 4.6(b)/4.9(b))."""
        for q in s.QF:
            j = s.jq(q)
            free_u = [u for u in range(1, j) if (q, u) not in s.trees]
            used = {sig for (qq, u, path), sig in s.pad.items() if qq == q and not path}
            pool = [z for z in s.unsplit_pool(q, j - 1 + len(used)) if z not in used]
            for u, sig in zip(free_u, pool):
                s.trees[(q, u)] = [()]; s.pad[(q, u, ())] = sig
        ts = s.rng.sample(range(1, s.P), len(s.QF))
        s.iota = dict(zip(s.QF, ts))
        s.tau[0] = 1
        for q in s.QF: s.tau[s.iota[q]] = q
        taken = set(v for v in s.tau if v is not None)
        cand = []; v = 2; lim = s.X // s.P
        while len(cand) < s.P:
            if v > lim: raise RuntimeError("tau pool too small")
            if v not in taken and s.divides_MF(v, s.P): cand.append(v)
            v += 1
        it = iter(cand)
        for t in range(s.P):
            if s.tau[t] is None: s.tau[t] = next(it)

    def build(s):
        s.cls = []   # (a, n, tag)
        for (q, u), leaves in s.trees.items():
            j = s.jq(q); qo = q // j
            for path in leaves:
                e = prod(c for c, v in path) if path else 1
                r = crt([(v, c) for c, v in path])[0] if path else 0
                sig = s.pad[(q, u, path)]
                a, n = crt([(qo * u, q), (r, e), (0, sig)])
                s.cls.append((a, n, ('A', q, u, path)))
        for t in range(s.P):
            a, n = crt([(t, s.P), (0, s.tau[t])])
            s.cls.append((a, n, ('B', t)))

    # ---------------- checks ----------------
    def check_basic(s):
        mods = [n for a, n, _ in s.cls]
        assert all(2 <= n <= s.X for n in mods), "modulus out of range"
        distinct = len(set(mods)) == len(mods)
        hyp = True
        for (q, u, path), sig in s.pad.items():
            if not (s.divides_MF(sig, q) and sig % s.jq(q)): hyp = False
        for q in s.QF:
            for path in s.trees[(q, 1)] if (q, 1) in s.trees else []:
                pass
        return distinct, hyp

    def zvec_cols(s):
        s.basis = [r for r in s.primes if r <= s.P]
        s.col = {r: i for i, r in enumerate(s.basis)}
        s.mod = np.array([r ** s.E[r] if r not in s.Iset else r for r in s.basis], dtype=np.int64)
        # check every modulus component fits
        for a, n, _ in s.cls:
            for r, e in s.fac(n).items():
                assert r in s.col and (r ** e) <= s.mod[s.col[r]] and s.mod[s.col[r]] % (r ** e) == 0, (n, r, e)

    def class_comps(s, a, n):
        return [(s.col[r], r ** e, a % (r ** e)) for r, e in s.fac(n).items()]

    def private_vectors(s):
        Z = np.zeros((len(s.cls), len(s.basis)), dtype=np.int64)
        Ip = [r for r in s.basis if r in s.Iset]
        for i, (a, n, tag) in enumerate(s.cls):
            row = Z[i]
            for r in Ip: row[s.col[r]] = s.rng.randrange(r)
            if tag[0] == 'A':
                _, q, u, path = tag
                j = s.jq(q); qo = q // j
                row[s.col[j]] = qo * u                     # z = q°u mod j^{E_j}
                for c, v in path: row[s.col[c]] = crt([(vv, cc) for cc, vv in path])[0] % c
                row[s.col[s.P]] = s.iota[q]               # z = iota(q) mod P
                # other primes r not in I, r != j : z = 0 mod r^{E_r}  (already 0)
            else:
                row[s.col[s.P]] = tag[1]                   # M_F(P) | z, z = t mod P
        return Z

    def membership_counts(s, Z, want_owner=False):
        """count, for each row z of Z, the classes containing z (exact, via a key index)."""
        cnt = np.zeros(len(Z), dtype=np.int32)
        owner = np.full(len(Z), -1, dtype=np.int64)
        keycache = {}
        for ci, (a, n, tag) in enumerate(s.cls):
            comps = s.class_comps(a, n)
            # key = the level component (q for A classes, P for B classes): the I-free top
            if tag[0] == 'A':
                kr = s.jq(tag[1]); kc = next(c for c in comps if s.basis[c[0]] == kr)
            else:
                kc = next(c for c in comps if s.basis[c[0]] == s.P)
            col, m, res = kc
            if (col, m) not in keycache:
                k = Z[:, col] % m; order = np.argsort(k, kind='stable'); keycache[(col, m)] = (k[order], order)
            sk, order = keycache[(col, m)]
            lo, hi = np.searchsorted(sk, res, 'left'), np.searchsorted(sk, res, 'right')
            cand = order[lo:hi]
            for col2, m2, res2 in comps:
                if (col2, m2) == (col, m) or len(cand) == 0: continue
                cand = cand[(Z[cand, col2] % m2) == res2]
            cnt[cand] += 1
            if want_owner: owner[cand] = ci
        return cnt, owner

    def fibre_row(s, q, u, hard):
        """random point of the fibre (q,u). hard=True: z = iota(q) mod P (no B_t can contain it, B_{iota(q)} needs q|z)
        AND z = 0 mod r^{E_r} for every other F-prime r (no class of another level can contain it), i.e. the
        neighbourhood of the paper's private integers: only the leaves of T_{q,u} can cover such a point.
        hard=False: higher digits random (such points are mostly covered redundantly by other classes)."""
        row = np.array([s.rng.randrange(int(m)) for m in s.mod], dtype=np.int64)
        j = s.jq(q); qo = q // j
        for r in s.basis:
            if r in s.Iset or r == s.P: continue
            M = int(s.mod[s.col[r]])
            if r == j:
                row[s.col[r]] = (qo * u + q * s.rng.randrange(M)) % M
            elif hard:
                row[s.col[r]] = 0                         # v_r(z) >= E_r: no class of another level can contain z
            else:
                e = 0
                while r ** (e + 1) < q: e += 1          # r^e || M_F(q); higher digits random
                row[s.col[r]] = (r ** e * s.rng.randrange(M)) % M
        if hard: row[s.col[s.P]] = s.iota[q]          # and no class B_t can contain z
        return row

    def exhaustive_fibre_rows(s, q, u):
        """hard-mode points of fibre (q,u), one for EVERY residue combination of the splitters labelling its tree
        (coverage of a fibre by its leaves depends only on these coordinates, so this is exact for the fibre)."""
        labs = sorted({c for path in s.trees[(q, u)] for c, v in path})
        rows = []
        for combo in itertools.product(*[range(c) for c in labs]):
            row = s.fibre_row(q, u, True)
            for c, v in zip(labs, combo): row[s.col[c]] = v
            rows.append(row)
        return rows

    def sample_points(s):
        rows = []
        split_fibres = [(q, u) for (q, u), lv in s.trees.items() if lv != [()]]
        fibres = list(s.trees.keys())
        nex = 0
        for (q, u) in split_fibres:
            ex = s.exhaustive_fibre_rows(q, u); rows += ex; nex += len(ex)
            rows += [s.fibre_row(q, u, False) for _ in range(10)]
        for (q, u) in fibres:
            rows.append(s.fibre_row(q, u, True)); rows.append(s.fibre_row(q, u, False))
        for _ in range(200):
            row = np.array([s.rng.randrange(int(m)) for m in s.mod], dtype=np.int64)
            for r in s.basis:
                if r not in s.Iset and r != s.P: row[s.col[r]] = 0
            rows.append(row)
        for _ in range(20000):
            rows.append(np.array([s.rng.randrange(int(m)) for m in s.mod], dtype=np.int64))
        return np.array(rows, dtype=np.int64), len(split_fibres), len(fibres), nex

    def report(s, label):
        t0 = time.time()
        distinct, hyp = s.check_basic()
        s.zvec_cols()
        Z = s.private_vectors()
        cnt, owner = s.membership_counts(Z, want_owner=True)
        own_ok = bool((cnt == 1).all() and (owner == np.arange(len(Z))).all())
        S, nsf, nf, nex = s.sample_points()
        scnt, _ = s.membership_counts(S)
        nsplitcls = sum(1 for _, _, t in s.cls if t[0] == 'A' and t[3])
        print(f"[{label}] X={s.X} P={s.P} |I|={len(s.I)} classes={len(s.cls)} split classes={nsplitcls} "
              f"max modulus={max(n for _, n, _ in s.cls)}")
        print(f"[{label}] distinct moduli: {distinct}; paddings divide M_F(q) & coprime to j: {hyp}")
        print(f"[{label}] private integers: each in exactly its own class: {own_ok} "
              f"(count histogram {np.bincount(cnt).tolist()[:5]})")
        print(f"[{label}] covering samples: {len(S)} points ({nsf} split fibres EXHAUSTIVE over their splitter residues "
              f"in the hard set = {nex} pts, +10 soft pts each; {nf} fibres x2 (one hard, one soft); 200 M_F(P)-multiples; "
              f"20000 uniform); uncovered: {int((scnt == 0).sum())}   ({time.time()-t0:.0f}s)")
        return distinct and hyp and own_ok and int((scnt == 0).sum()) == 0

# ------------------------------------------------------------------------------------------------
def prop47(X, seed=47):
    P = max(r for r in primes_upto(int(math.isqrt(X // 2)) + 1) if r * r <= X / 2)
    I = [c for c in primes_upto(int(X ** 0.25) + 2) if X ** 0.2 < c <= X ** 0.25]
    G = [p for p in primes_upto(P) if 2 * X ** 0.4 < p < P]
    s = Inst(X, P, I, seed)
    logF = 0.0; ksum = 0
    for p in G:
        pools = {}; fsum = 0
        for c in I:
            Y = X // (p * c)
            pool = [v for v in range(1, Y + 1) if all(v % cc for cc in I)]
            assert all(v < p for v in pool)
            f = len(pool) // c; pools[c] = (pool, f); fsum += f
        assert fsum < p - 1, ("capacity", p, fsum)
        us = s.rng.sample(range(1, p), fsum); it = iter(us)
        for c in I:
            pool, f = pools[c]
            N = c * f
            chosen = s.rng.sample(pool, N); k = 0
            for _ in range(f):
                u = next(it)
                s.trees[(p, u)] = [((c, v),) for v in range(c)]
                for v in range(c):
                    s.pad[(p, u, ((c, v),))] = chosen[k]; k += 1
            if N: logF += lgamma(N + 1); ksum += N
    s.finish(); s.build()
    print(f"[prop47] X={X}: I={I}, |G|={len(G)} (G={G[:3]}..{G[-2:]}), sum N_pc={ksum}, log prod N_pc! = {logF:.1f}")
    return s.report("prop47"), s

# ------------------------------------------------------------------------------------------------
def lemma410(s, p, Dp, poolsize):
    """the a_e / b_e / L_e bookkeeping of the proof of Lemma 4.10. Returns (a, L, N, N1)."""
    def primes_of(e): return sorted(s.fac(e).keys())
    N = set()
    for d in Dp:
        ps = sorted(s.fac(d).keys(), reverse=True)
        for i in range(1, len(ps) + 1): N.add(prod(ps[:i]))
    ell = {e: min(s.fac(e)) for e in N}
    succ = {e: [e2 for e2 in N if e2 % e == 0 and e2 // e in s.Iset and e2 // e < ell[e]] for e in N}
    a, L = {}, {}
    for e in sorted(N, reverse=True):
        b = sum(a[e2] for e2 in succ[e])
        if e in Dp: a[e] = (poolsize(e) + b) // ell[e]
        else: a[e] = -(-b // ell[e])
        L[e] = ell[e] * a[e] - b
        assert 0 <= L[e] <= poolsize(e)
        if e in Dp: assert poolsize(e) - ell[e] < L[e] <= poolsize(e)
        else: assert L[e] < ell[e]
    N1 = sum(a[e] for e in N if e in s.Iset)
    assert Fraction(N1) == sum(Fraction(L[e], e) for e in N), "identity N_1 = sum L_e/e fails"
    return a, L, N, succ, N1

def tree_instance(X, K, seed=410):
    I = [11, 13, 17, 19]
    P = max(r for r in primes_upto(int(math.isqrt(X // K)) + 1) if r * r <= X / K)
    s = Inst(X, P, I, seed)
    S3 = [v for v in range(1, 13) if v != 11]          # {2,3,5,7}-smooth s <= 12 (primes below the splitters)
    primes_r = [r for r in primes_upto(P) if r >= 23]   # r larger than every splitter
    def pool(p, e):
        Y = min(p - 1, X // (p * e))
        return sorted(sv * r for sv in S3 for r in primes_r if sv * r <= Y)
    Inums = sorted({prod(c) for k in range(1, 5) for c in __import__('itertools').combinations(I, k)})
    logF = 0.0; ksum = 0; levels = 0; maxdepth = 0; logF_bound = 0.0
    for p in primes_upto(P):
        if p >= P or p <= max(I): continue
        Dp = {d for d in Inums if d > 2 * X / p ** 2 and X // (p * d) >= 40}
        if not Dp: continue
        cache = {}
        def ps(e, p=p):
            if e not in cache: cache[e] = len(pool(p, e))
            return cache[e]
        if any(ps(e) <= max(s.fac(e)) for e in Dp): continue
        a, L, N, succ, N1 = lemma410(s, p, Dp, ps)
        if N1 > p - 1:
            print(f"  level {p}: N_1={N1} > p-1, skipped"); continue
        levels += 1
        us = s.rng.sample(range(1, p), N1)
        nodes = {}  # e -> list of (u, path) nodes with I-part e
        it = iter(us)
        for c in sorted(e for e in N if e in s.Iset):
            for _ in range(a[c]):
                u = next(it); nodes.setdefault(c, []).extend((u, ((c, v),)) for v in range(c))
        leaves_by_e = {}
        for e in sorted(N, key=lambda e: (len(s.fac(e)), e)):
            lst = nodes.get(e, [])
            assert len(lst) == len(s.fac(e)) and False or len(lst) == min(s.fac(e)) * a[e], (e, len(lst))
            k = 0
            for e2 in sorted(succ[e], reverse=True):
                c = e2 // e
                for _ in range(a[e2]):
                    u, path = lst[k]; k += 1
                    nodes.setdefault(e2, []).extend((u, path + ((c, v),)) for v in range(c))
            leaves_by_e[e] = lst[k:]
            assert len(leaves_by_e[e]) == L[e]
        for e, lv in leaves_by_e.items():
            pl = pool(p, e); chosen = s.rng.sample(pl, len(lv))
            for (u, path), sig in zip(lv, chosen):
                s.trees.setdefault((p, u), []).append(path)
                s.pad[(p, u, path)] = sig
                maxdepth = max(maxdepth, len(path))
            if e in Dp and lv:
                logF += lgamma(len(lv) + 1); ksum += len(lv)
        # labels decrease along every path & each tree's leaves partition its fibre (sum 1/e = 1)
        for u in set(us):
            lv = s.trees[(p, u)]
            assert all(all(path[i][0] > path[i + 1][0] for i in range(len(path) - 1)) for path in lv)
            assert sum(Fraction(1, prod(c for c, v in path)) for path in lv) == 1
    s.finish(); s.build()
    print(f"[tree] X={X} K={K}: split levels={levels}, max depth={maxdepth}, sum_d L_p(d) over D_p = {ksum}, "
          f"log prod L_p(d)! = {logF:.1f}")
    return s

def negative_controls(s):
    print("[neg] NEGATIVE controls on this instance (each must FAIL):")
    # (a) delete one split leaf of the deepest available kind
    idx = max((i for i, (_, _, t) in enumerate(s.cls) if t[0] == 'A' and t[3]), key=lambda i: len(s.cls[i][2][3]))
    a, n, tag = s.cls[idx]
    _, q, u, path = tag
    saved = s.cls
    Z = s.private_vectors()
    s.cls = saved[:idx] + saved[idx + 1:]
    cnt, _ = s.membership_counts(Z)
    rows = np.array(s.exhaustive_fibre_rows(q, u))
    c2, _ = s.membership_counts(rows)
    e = prod(c for c, v in path)
    labs = sorted({c for p_ in s.trees[(q, u)] for c, v in p_})
    expect = prod(labs) // e
    soft = np.array([s.fibre_row(q, u, False) for _ in range(4000)])
    c3, _ = s.membership_counts(soft)
    print(f"[neg]  (a) delete leaf {tag[1:]} (modulus {n}):")
    print(f"[neg]      its private integer now lies in {int(cnt[idx])} classes (must be 0); private-integer rows with count 0: {int((cnt==0).sum())}")
    print(f"[neg]      exhaustive hard-mode rows of fibre {(q,u)}: uncovered {int((c2==0).sum())} of {len(rows)} (expected {expect} = prod(labels)/e)")
    print(f"[neg]      4000 random fibre points with RANDOM residue mod P: uncovered {int((c3==0).sum())}  "
          f"(weak test: B_t and classes of other levels cover almost every such point; this is why the hard mode is used)")
    s.cls = saved
    # (b) duplicate a padding inside one (q,e) group -> moduli not distinct
    keys = [k for k in s.pad if len(k[2]) >= 1]
    for k1 in keys:
        e1 = prod(c for c, v in k1[2])
        k2 = next((k for k in keys if k != k1 and k[0] == k1[0] and prod(c for c, v in k[2]) == e1), None)
        if k2: break
    old = s.pad[k2]; s.pad[k2] = s.pad[k1]; s.build()
    d, _ = s.check_basic()
    print(f"[neg]  (b) duplicate padding in group (q={k1[0]}, e={e1}): distinct moduli = {d}")
    s.pad[k2] = old; s.build()

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "prop47":
        ok, s = prop47(int(float(sys.argv[2])))
        print("PROP47 RESULT:", "PASS" if ok else "FAIL")
        negative_controls(s)
    elif mode == "tree":
        s = tree_instance(int(float(sys.argv[2])), int(sys.argv[3]))
        ok = s.report("tree")
        print("TREE RESULT:", "PASS" if ok else "FAIL")
        negative_controls(s)
