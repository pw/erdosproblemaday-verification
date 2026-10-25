#!/usr/bin/env python3
"""Referee (h1m): INDEPENDENT enumeration of the H1 miss matrices, different algorithm from menum.py / mcount.c.

Algorithm: the 24 free entries are grouped into the 6 pair-of-pairs 2x2 blocks
    B(P,Q) = [[M[2P][2Q], M[2P][2Q+1]], [M[2P+1][2Q], M[2P+1][2Q+1]]]   (P < Q pairs)
M4 (Lemma D) lives INSIDE one block: for X in P, Y in Q it reads M[X'][Y] + M[X][Y'] <= 5, i.e. the two
anti-diagonal-type sums of B: B[1][0]+B[0][1] <= 5 (X=2P,Y=2Q) and B[0][0]+B[1][1] <= 5 (X=2P,Y=2Q+1).
(Derived here from the definition, not copied: X'=X^1.)
Matrices are built block by block (recursion over the 6 blocks, each block chosen from a precomputed list of
2x2 non-negative integer matrices), with row-sum feasibility; also COUNTED by a separate dictionary DP over row-sum
states (no enumeration) as a cross-check.
Orbits: Burnside, #orbits = (1/|G|) sum_g Fix(g), Fix computed by numpy over the enumerated list.
Group: ALL permutations of the 8 blocks commuting with X -> X^1 and preserving the case's e-pattern (brute force over
S8), compared as a set with menum.group(j).
Also validates classes_all.tsv: every rep is an admissible matrix, reps are pairwise non-equivalent (own canonical form
= min over the group of the integer code, computed by numpy), the orbit sizes / stabiliser orders are correct, and
the reps hit every orbit exactly once.
"""
import itertools, sys, collections, functools
print = functools.partial(print, flush=True)
import numpy as np

H1M = "/home/exedev/MathDyad/erdos85/h1m"
PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]
IDX = {p: i for i, p in enumerate(PAIRS)}

def E_of(j):          # our case convention: pairs 0..j-1 are (2,2); the rest (2,1) with the first block e=2
    return [2 if (p < j or s == 0) else 1 for p in range(4) for s in (0, 1)]

def group_bruteforce(E):
    G = []
    for g in itertools.permutations(range(8)):
        if all(g[X ^ 1] == g[X] ^ 1 for X in range(8)) and all(E[g[X]] == E[X] for X in range(8)):
            G.append(g)
    return G

BLOCKS = list(itertools.combinations(range(4), 2))   # 6 pair-of-pairs

def enumerate_matrices(E, use_m4):
    """vectorised block join: partial tables = numpy rows of (6 blocks x 4 entries); add one 2x2 block at a time
    (cross product with the block-candidate list), filter row sums <= R, and require EXACT row sums for the two
    rows of every pair whose last block has been placed."""
    R = np.array([2 * e for e in E], dtype=np.int16)
    cands = np.array([b for b in itertools.product(range(5), repeat=4)
                      if not (use_m4 and (b[2] + b[1] > 5 or b[0] + b[3] > 5))], dtype=np.int16)
    last = {p: max(i for i, bb in enumerate(BLOCKS) if p in bb) for p in range(4)}
    tab = np.zeros((1, 0), dtype=np.int16)
    rs = np.zeros((1, 8), dtype=np.int16)
    for i, (P, Q) in enumerate(BLOCKS):
        contrib = np.zeros((len(cands), 8), dtype=np.int16)
        contrib[:, 2*P] = cands[:, 0] + cands[:, 1]; contrib[:, 2*P+1] = cands[:, 2] + cands[:, 3]
        contrib[:, 2*Q] = cands[:, 0] + cands[:, 2]; contrib[:, 2*Q+1] = cands[:, 1] + cands[:, 3]
        exact = [2*p + s for p in (P, Q) if last[p] == i for s in (0, 1)]
        ntabs, nrs = [], []
        CH = max(1, 2_000_000 // len(cands))
        for c0 in range(0, len(tab), CH):
            t, r = tab[c0:c0+CH], rs[c0:c0+CH]
            newrs = r[:, None, :] + contrib[None, :, :]                 # (chunk, ncand, 8)
            ok = (newrs <= R).all(axis=2)
            if exact:
                ok &= (newrs[:, :, exact] == R[exact]).all(axis=2)
            ii, cc = np.nonzero(ok)
            ntabs.append(np.concatenate([t[ii], cands[cc]], axis=1)); nrs.append(newrs[ii, cc])
        tab = np.concatenate(ntabs); rs = np.concatenate(nrs)
    assert (rs == R).all()
    res = np.zeros((len(tab), 24), dtype=np.int8)
    for bi, (P, Q) in enumerate(BLOCKS):
        a00, a01, a10, a11 = (tab[:, 4*bi + t] for t in range(4))
        res[:, IDX[(2*P, 2*Q)]] = a00; res[:, IDX[(2*P, 2*Q+1)]] = a01
        res[:, IDX[(2*P+1, 2*Q)]] = a10; res[:, IDX[(2*P+1, 2*Q+1)]] = a11
    return res

def count_dp(E, use_m4):
    """pure counting: dictionary DP over row-sum states, no enumeration."""
    R = tuple(2 * e for e in E)
    cands = [b for b in itertools.product(range(5), repeat=4)
             if not (use_m4 and (b[2] + b[1] > 5 or b[0] + b[3] > 5))]
    st = collections.Counter({(0,)*8: 1})
    for (P, Q) in BLOCKS:
        nst = collections.Counter()
        for s, c in st.items():
            for a00, a01, a10, a11 in cands:
                t = list(s)
                t[2*P] += a00 + a01; t[2*P+1] += a10 + a11; t[2*Q] += a00 + a10; t[2*Q+1] += a01 + a11
                if all(t[X] <= R[X] for X in range(8)):
                    nst[tuple(t)] += c
        st = nst
    return st[R]

def perm_index(g):
    """index map: new flat vector N with N[g X][g Y] = M[X][Y]  ->  N = M[:, src] with src[IDX[(gX,gY)]] = IDX[(X,Y)]"""
    src = [None] * 24
    for (X, Y), i in IDX.items():
        a, b = g[X], g[Y]
        src[IDX[(min(a, b), max(a, b))]] = i
    assert sorted(src) == list(range(24))
    return np.array(src)

def burnside(mats, G):
    tot = 0
    for g in G:
        src = perm_index(g)
        tot += int((mats[:, src] == mats).all(axis=1).sum())
    assert tot % len(G) == 0
    return tot // len(G)

def codes(mats):
    w = (5 ** np.arange(24, dtype=np.int64))[::-1]
    return mats.astype(np.int64) @ w

def canon(mats, G):
    best = None
    for g in G:
        c = codes(mats[:, perm_index(g)])
        best = c if best is None else np.minimum(best, c)
    return best

if __name__ == "__main__":
    sys.path.insert(0, H1M)
    import menum
    cls = collections.defaultdict(list)
    for line in open(f"{H1M}/classes_all.tsv"):
        jj, flat, o, s = line.rstrip("\n").split("\t")
        cls[int(jj)].append((tuple(int(t) for t in flat.split(",")), int(o), int(s)))
    grand = {True: 0, False: 0}
    for j in range(5):
        E = E_of(j)
        assert E == menum.case_E(j)
        G = group_bruteforce(E)
        Gm = set(menum.group(j))
        print(f"case j={j} E={E}: |G| brute force {len(G)}, menum group {len(Gm)}, equal as sets {set(G) == Gm}")
        for use in (False, True):
            mats = enumerate_matrices(E, use)
            dp = count_dp(E, use)
            # validity of every enumerated matrix (re-check from scratch)
            full = np.zeros((len(mats), 8, 8), dtype=np.int64)
            for (X, Y), i in IDX.items():
                full[:, X, Y] = mats[:, i]; full[:, Y, X] = mats[:, i]
            assert (full.sum(axis=2) == np.array([2 * e for e in E])).all()
            if use:
                for X, Y in PAIRS:
                    assert (full[:, X ^ 1, Y] + full[:, X, Y ^ 1] <= 5).all()
            assert len(set(map(bytes, mats))) == len(mats)
            orb = burnside(mats, G)
            grand[use] += orb
            print(f"   {'with' if use else 'w/o '} M4: matrices enum {len(mats)} dp {dp}  orbits (Burnside) {orb}")
            if use:
                # validate classes_all.tsv against this independent enumeration
                rows = cls[j]
                reps = np.array([r for r, _, _ in rows], dtype=np.int8)
                mcode = set(codes(mats).tolist())
                inset = all(c in mcode for c in codes(reps).tolist())
                cr = canon(reps, G)
                distinct = len(set(cr.tolist())) == len(rows)
                cm = canon(mats, G)
                hit = set(cr.tolist()) == set(cm.tolist())
                # orbit size / stabiliser
                okos = True
                for (r, o, s) in rows:
                    v = np.array([r], dtype=np.int8)
                    st = sum(1 for g in G if (v[:, perm_index(g)] == v).all())
                    if st != s or o * s != len(G):
                        okos = False
                orbsizes = sum(o for _, o, _ in rows)
                print(f"   classes_all.tsv j={j}: rows {len(rows)} all-admissible {inset} pairwise-inequivalent {distinct} "
                      f"cover-every-orbit {hit} stab/orbit-size correct {okos} sum orbit sizes {orbsizes} (= matrices {len(mats)}: {orbsizes == len(mats)})")
    print(f"TOTAL orbits without M4 {grand[False]}, with M4 {grand[True]}, removed {grand[False] - grand[True]}")
