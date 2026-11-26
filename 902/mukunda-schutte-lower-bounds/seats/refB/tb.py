"""Referee-B tournament toolkit (written from the paper's definitions only).

Tournament = list out[v] of Python-int bitmasks: bit u of out[v] set iff v -> u.
inm[v] = bitmask of in-neighbours of v.  D(X) = AND_{x in X} inm[x]  (excludes X automatically).
"""
from itertools import combinations
from math import comb


def qr_tournament(p):
    assert p % 4 == 3
    sq = {(x * x) % p for x in range(1, p)}
    out = []
    for i in range(p):
        m = 0
        for j in range(p):
            if j != i and ((j - i) % p) in sq:
                m |= 1 << j
        out.append(m)
    return out


def load_outlists(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('#'):
                continue
            rows.append([int(t) for t in line.split()] if line else [])
    out = []
    for v, r in enumerate(rows):
        m = 0
        for u in r:
            m |= 1 << u
        out.append(m)
    return out


def check_tournament(out):
    N = len(out)
    full = (1 << N) - 1
    for v in range(N):
        assert not (out[v] >> v) & 1, 'loop'
        assert out[v] & ~full == 0
    for u in range(N):
        for v in range(u + 1, N):
            a = (out[u] >> v) & 1
            b = (out[v] >> u) & 1
            assert a + b == 1, (u, v, a, b)
    return True


def in_masks(out):
    N = len(out)
    inm = [0] * N
    for v in range(N):
        m = out[v]
        while m:
            low = m & -m
            u = low.bit_length() - 1
            inm[u] |= 1 << v
            m ^= low
    return inm


def D(inm, X, N):
    m = (1 << N) - 1
    for x in X:
        m &= inm[x]
    return m


def nu_all(inm, N, kmax, fixed=None):
    """nu_k for k=0..kmax by exhaustive DFS. If fixed is a tuple of vertices,
    only k-sets containing `fixed` (for k>=len(fixed)) are enumerated -- valid
    when an automorphism group maps every k-set to one containing `fixed`."""
    full = (1 << N) - 1
    best = [None] * (kmax + 1)
    best[0] = N
    cnt = [0] * (kmax + 1)
    if fixed:
        base = full
        for x in fixed:
            base &= inm[x]
        f = len(fixed)
        # sets of size < f containing a prefix of fixed: handled separately by caller
        best_f = bin(base).count('1')
        best[f] = best_f
        cnt[f] = 1
        rest = [v for v in range(N) if v not in fixed]
        def rec(start, depth, mask):
            for idx in range(start, len(rest)):
                mm = mask & inm[rest[idx]]
                c = mm.bit_count()
                d = depth + 1
                cnt[d] += 1
                if best[d] is None or c < best[d]:
                    best[d] = c
                if d < kmax:
                    rec(idx + 1, d, mm)
        if f < kmax:
            rec(0, f, base)
        return best, cnt

    def rec(start, depth, mask):
        for v in range(start, N):
            mm = mask & inm[v]
            c = mm.bit_count()
            d = depth + 1
            cnt[d] += 1
            if best[d] is None or c < best[d]:
                best[d] = c
            if d < kmax:
                rec(v + 1, d, mm)
    rec(0, 0, full)
    return best, cnt


def bits(m):
    r = []
    while m:
        low = m & -m
        r.append(low.bit_length() - 1)
        m ^= low
    return r
