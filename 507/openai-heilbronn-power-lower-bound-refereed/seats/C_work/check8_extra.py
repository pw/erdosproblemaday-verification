#!/usr/bin/env python3
"""Extra checks (beyond the brief's list), same discipline.

(a) Proposition 2.5 (the I^2 saving that Corollary 6.4 trades against the orbit size h^8/(D^3E^2)):
    #{3x3 matrices, rows in Lambda_C, row lengths <= X, det = t}  <=  C (log 2X)^2 X^6 / I^2,
    for Lambda_C = {v : v mod h in rowspan C} of index I = DE, lambda_3 <= E <= X.
    Exact counts over toy lattices (h = 4, 8, 9; every (D,E) class); report count * I^2 / (X^6 log^2 2X),
    which must stay bounded uniformly in I.
    Mutation: an over-strong saving I^3 (count <= C X^6/I^3) is rejected if count*I^3/X^6 grows with I.
(b) Lemma 6.1: ordered proportional pairs in the box [0,N)^2 x [N,2N) number << N^3 (exact for N <= 160).
    Mutation: the full box [0,2N)^3 including the origin side is not the claim; instead we show the
    count is NOT o(N^3) (ratio stabilises), i.e. N^3 is the right order (a claimed N^2.5 is rejected).
"""
import itertools, math, random, time
import numpy as np

# --- local instruments (independent of check2_orbits.py) ---
def _det(g):
    return (g[0][0] * (g[1][1] * g[2][2] - g[1][2] * g[2][1]) - g[0][1] * (g[1][0] * g[2][2] - g[1][2] * g[2][0])
            + g[0][2] * (g[1][0] * g[2][1] - g[1][1] * g[2][0]))

def random_gl(h, rng):
    while True:
        g = [[rng.randrange(h) for _ in range(3)] for _ in range(3)]
        if math.gcd(_det(g) % h, h) == 1: return np.array(g, dtype=np.int64)

def span_set(C, h):
    """row span of C mod h as a set of encoded vectors, built by closure under adding rows (BFS)"""
    rows = [tuple(int(x) % h for x in C[i]) for i in range(3)]
    seen = {(0, 0, 0)}; frontier = [(0, 0, 0)]
    while frontier:
        nxt = []
        for v in frontier:
            for r in rows:
                w = tuple((a + b) % h for a, b in zip(v, r))
                if w not in seen: seen.add(w); nxt.append(w)
        frontier = nxt
    return {a * h * h + b * h + c for (a, b, c) in seen}

def DE_of(C, h):
    span = span_set(C, h)
    I = h ** 3 // len(span)
    D = h
    for (i1, i2) in ((0, 1), (0, 2), (1, 2)):
        for (j1, j2) in ((0, 1), (0, 2), (1, 2)):
            D = math.gcd(D, int(C[i1, j1] * C[i2, j2] - C[i1, j2] * C[i2, j1]))
    return D, I // D, span

def ball(R):
    m = int(math.floor(R))
    ax = np.arange(-m, m + 1, dtype=np.int64)
    X = np.array(np.meshgrid(ax, ax, ax, indexing='ij')).reshape(3, -1).T
    return X[(X * X).sum(axis=1) <= R * R]

def lattice_points(C, h, X, span):
    P = ball(X)
    m = P % h
    code = m[:, 0] * h * h + m[:, 1] * h + m[:, 2]
    keep = np.array([c in span for c in code.tolist()])
    return P[keep]

def count_det(Lp, ts):
    u2 = np.repeat(Lp, len(Lp), axis=0); u3 = np.tile(Lp, (len(Lp), 1))
    n = np.cross(u2, u3)
    un, cnt = np.unique(n, axis=0, return_counts=True)
    out = {t: 0 for t in ts}
    CH = 4000
    for s in range(0, len(un), CH):
        dots = Lp @ un[s:s + CH].T
        c = cnt[s:s + CH]
        for t in ts:
            out[t] += int(((dots == t).sum(axis=0) * c).sum())
    return out

def part_a(rng):
    print("=== (a) Proposition 2.5: count * I^2 / (X^6 log^2 2X) uniformly bounded in I ===")
    rows = []
    for h, B, k in ((4, 2, 2), (8, 2, 3), (9, 3, 2)):
        for b in range(k + 1):
            for e in range(b, k + 1):
                P = random_gl(h, rng); Q = random_gl(h, rng)
                C = (P @ np.diag([1, B ** b % h, B ** e % h]) @ Q) % h
                D_, E_, span = DE_of(C, h); I = D_ * E_
                for X in ((6, 8) if I <= 2 else ((10, 14) if I <= 16 else (14, 18))):
                    if E_ > X: continue
                    Lp = lattice_points(C, h, X, span)
                    if len(Lp) ** 2 > 9e6: continue
                    ts = [I * m for m in (1, 2, 3, 6)]
                    c = count_det(Lp, ts)
                    norm = X ** 6 * math.log(2 * X) ** 2
                    best = max(c[t] for t in ts)
                    rows.append((h, D_, E_, I, X, best, best * I ** 2 / norm, best * I ** 3 / norm, len(Lp)))
    for r in rows:
        print(f"  h={r[0]} D={r[1]} E={r[2]} I={r[3]} X={r[4]}: |Lambda cap ball|={r[8]}, max_t count={r[5]}, "
              f"count*I^2/(X^6 log^2) = {r[6]:.4f}   [MUTATION I^3: {r[7]:.4f}]")
    by = {}
    for r in rows:
        by.setdefault(r[3], []).append(r[6])
    print("  POSITIVE: max normalised (I^2) ratio by I:", {I: round(max(v), 3) for I, v in sorted(by.items())})
    byM = {}
    for r in rows:
        byM.setdefault(r[3], []).append(r[7])
    print("  MUTATION (I^3): max ratio by I:", {I: round(max(v), 3) for I, v in sorted(byM.items())})

def part_b():
    print("\n=== (b) Lemma 6.1: ordered proportional pairs in [0,N)^2 x [N,2N) << N^3 ===")
    for N in (10, 20, 40, 80, 160):
        a = np.arange(N, dtype=np.int64); c3 = np.arange(N, 2 * N, dtype=np.int64)
        U = np.array(np.meshgrid(a, a, c3, indexing='ij')).reshape(3, -1).T
        g = np.gcd(np.gcd(U[:, 0], U[:, 1]), U[:, 2])
        Z = U // g[:, None]
        _, cnt = np.unique(Z, axis=0, return_counts=True)
        pairs = int((cnt.astype(np.int64) ** 2).sum())
        print(f"  N={N}: ordered proportional pairs (incl. equal) = {pairs}; /N^3 = {pairs / N**3:.4f}; "
              f"MUTATION /N^2.5 = {pairs / N**2.5:.3f}")

def main():
    rng = random.Random(808)
    t0 = time.time()
    part_a(rng)
    print(f"[{time.time()-t0:.0f}s]")
    part_b()
    print(f"[{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    main()
