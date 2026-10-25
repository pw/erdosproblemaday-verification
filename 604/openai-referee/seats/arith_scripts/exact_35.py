# Exact check of Lemma 3.2, identity (3.5): d(x,y) = M + L(x,y) - S(x) - S(y), on explicit hierarchies (Fractions / ints).
# Hierarchy given by a sharing-depth function d on unordered pairs; Pi(r) = classes of {d >= r}.
# Giant = the cell of size > n/2; C(r) = Pi(r) with the giant replaced by its complement, AS A MULTISET (paper p.10).
# Controls: (C1) multiset -> set (drop a duplicated complement); (C2) sign of S flipped.
from fractions import Fraction as F
import itertools, random, math

def classes(P, d, r):
    # classes of the relation {d >= r} (assumed an equivalence relation; verified)
    cls = []
    for x in P:
        for c in cls:
            if d[frozenset((x, c[0]))] >= r:
                c.append(x); break
        else:
            cls.append([x])
    # verify it IS an equivalence relation (transitivity)
    for c in cls:
        for a, b in itertools.combinations(c, 2):
            assert d[frozenset((a, b))] >= r, "not transitive"
    for c1, c2 in itertools.combinations(cls, 2):
        for a in c1:
            for b in c2:
                assert d[frozenset((a, b))] < r
    return [frozenset(c) for c in cls]

def hier_quantities(P, d, multiset=True):
    n = len(P)
    vals = sorted(set(d.values()))
    # intervals (v_{i}, v_{i+1}] on which Pi(r) = classes(d >= v_{i+1}); (-inf, v_1] -> {P}; (v_k, inf) -> singletons
    M = vals[0]           # giant (=P) exists on (-inf, v_1]
    S = {x: F(0) for x in P}
    L = {frozenset(p): F(0) for p in itertools.combinations(P, 2)}
    giant_ray_ok = True; seen_no_giant = False
    for lo, hi in zip(vals[:-1], vals[1:]):
        length = F(hi) - F(lo)
        Pi = classes(P, d, hi)
        G = [c for c in Pi if 2 * len(c) > n]
        assert len(G) <= 1
        if G:
            if seen_no_giant: giant_ray_ok = False
            G = G[0]; M = hi
            comp = frozenset(P) - G
            Cs = [c for c in Pi if c != G]
            if multiset or comp not in Cs:
                Cs = Cs + [comp]
            for x in P:
                if x not in G: S[x] += length
        else:
            seen_no_giant = True
            Cs = Pi
        for pr in L:
            a, b = tuple(pr)
            L[pr] += length * sum(1 for c in Cs if a in c and b in c)
    return M, S, L, giant_ray_ok

def check(P, d, multiset=True, sign=+1):
    M, S, L, ray = hier_quantities(P, d, multiset)
    bad = []
    for pr in L:
        a, b = tuple(pr)
        rhs = M + L[pr] - sign * (S[a] + S[b])
        if F(d[pr]) != rhs: bad.append((tuple(sorted(pr)), d[pr], rhs))
    return bad, ray

def ultrametric_from_dendrogram(P, rng, tie=False):
    # random agglomeration: start singletons; merge two clusters at strictly decreasing (or tied) depth
    clusters = [[x] for x in P]; d = {}
    h = F(rng.randint(30, 60), rng.randint(1, 4))
    while len(clusters) > 1:
        i, j = rng.sample(range(len(clusters)), 2)
        for a in clusters[i]:
            for b in clusters[j]:
                d[frozenset((a, b))] = h
        clusters[i] = clusters[i] + clusters[j]; clusters.pop(j)
        if not (tie and rng.random() < 0.4):
            h -= F(rng.randint(1, 9), rng.randint(1, 5))
    return d

if __name__ == '__main__':
    # (a) Figure 1: n=8, Pi = {1..5},{6,7,8} on (1,2]
    P = list(range(1, 9)); d = {}
    for a, b in itertools.combinations(P, 2):
        if a <= 5 and b <= 5: d[frozenset((a, b))] = F(3)
        elif a >= 6 and b >= 6: d[frozenset((a, b))] = F(2)
        else: d[frozenset((a, b))] = F(1)
    M, S, L, ray = hier_quantities(P, d)
    print("Figure 1: M =", M, " S(6) =", S[6], " S(1) =", S[1], " L(6,7) =", L[frozenset((6, 7))], " L(1,2) =", L[frozenset((1, 2))])
    print("  paper identity failures:", check(P, d)[0])
    print("  CONTROL C1 (set, not multiset) failures:", check(P, d, multiset=False)[0])
    print("  CONTROL C2 (sign of S flipped) failures (first 3):", check(P, d, sign=-1)[0][:3])
    # (b) random ultrametrics, with and without ties
    rng = random.Random(604)
    tot = fails = c1 = c2 = rayfail = 0; dup_events = 0
    for trial in range(3000):
        n = rng.randint(2, 11)
        P = list(range(n))
        d = ultrametric_from_dendrogram(P, rng, tie=(trial % 2 == 1))
        bad, ray = check(P, d); tot += 1; fails += bool(bad); rayfail += (not ray)
        c1 += bool(check(P, d, multiset=False)[0]); c2 += bool(check(P, d, sign=-1)[0])
    print(f"random ultrametrics: {tot} hierarchies, identity failures = {fails}, non-initial-ray giant sets = {rayfail}")
    print(f"  CONTROL C1 (set) caught {c1}/{tot}; CONTROL C2 (sign) caught {c2}/{tot}")
