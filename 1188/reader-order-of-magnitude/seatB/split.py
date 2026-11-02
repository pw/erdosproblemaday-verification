#!/usr/bin/env python3
"""Construction 4.2 (split construction with splitting trees), implemented from the paper's text,
and exhaustive checks of Proposition 4.3 on small instances + Examples 4.4 and 4.5.
"""
import itertools, random, sys, time
from math import gcd, prod
from cover import check, ok, lcmlist, crt, primes_upto, factor

def is_prime_power(q):
    f = factor(q)
    return len(f) == 1, (next(iter(f)) if len(f) == 1 else None)

def Fpp_list(P, I):
    """F-prime-powers < P (prime powers j^k with j not in I)."""
    out = []
    for q in range(2, P):
        pp, j = is_prime_power(q)
        if pp and j not in I:
            out.append(q)
    return out

def M_F(m, I):
    return lcmlist([q for q in Fpp_list(m, I)]) if m > 2 else 1

def jq(q): return next(iter(factor(q)))

def divisors(n):
    ds = [1]
    for p, e in factor(n).items():
        ds = [d * p**k for d in ds for k in range(e + 1)]
    return sorted(ds)

def leaves(tree, path=()):
    """tree: None (leaf) or (c, [child_0,...,child_{c-1}])."""
    if tree is None:
        yield path
    else:
        c, ch = tree
        assert len(ch) == c
        for v in range(c):
            yield from leaves(ch[v], path + ((c, v),))

def leaf_e_r(path):
    e = prod(c for c, v in path) if path else 1
    r, _ = crt([(v, c) for c, v in path]) if path else (0, 1)
    return e, r

def build(P, I, trees, pad, iota, tau):
    """Returns list of classes (a, n, tag)."""
    QF = Fpp_list(P, I)
    cls = []
    for q in QF:
        j = jq(q); qo = q // j
        for u in range(1, j):
            for path in leaves(trees[(q, u)]):
                e, r = leaf_e_r(path)
                s = pad[(q, u, path)]
                a, n = crt([(qo * u, q), (r, e), (0, s)])
                cls.append((a, n, ('A', q, u, path, s)))
    for t in range(P):
        a, n = crt([(t, P), (0, tau[t])])
        cls.append((a, n, ('B', t)))
    return cls

def check_hyp(P, I, trees, pad, iota, tau):
    """Check (T1)-(T3) and the label-distinctness condition of a splitting tree."""
    QF = Fpp_list(P, I)
    for q in QF:
        j = jq(q); MF = M_F(q, I)
        seen = {}
        for u in range(1, j):
            for path in leaves(trees[(q, u)]):
                labs = [c for c, v in path]
                if len(set(labs)) != len(labs) or any(c not in I for c in labs): return "labels"
                s = pad[(q, u, path)]
                if MF % s or gcd(s, j) != 1: return f"padding {s} at q={q}"
                e, _ = leaf_e_r(path)
                if (e, s) in seen: return f"T1 distinctness q={q} e={e} s={s}"
                seen[(e, s)] = 1
    vals = set(iota.values())
    if len(vals) != len(QF) or not all(1 <= t <= P - 1 for t in vals): return "T2"
    MFP = M_F(P, I)
    if len(set(tau)) != P or any(MFP % v for v in tau) or tau[0] != 1: return "T3"
    if any(tau[iota[q]] != q for q in QF): return "T3 iota"
    return None

def system_set(cls): return frozenset((a % n, n) for a, n, _ in cls)

# ---------------------------------------------------------------------------------------------
def example_44():
    P, I, x = 13, {5}, 600
    QF = Fpp_list(P, I); assert QF == [2, 3, 4, 7, 8, 9, 11], QF
    assert M_F(11, I) == 504
    trees, pad = {}, {}
    for q in QF:
        j = jq(q); MF = M_F(q, I)
        avail = [d for d in divisors(MF) if d <= x / q and gcd(d, j) == 1]
        for u in range(1, j):
            trees[(q, u)] = None
            pad[(q, u, ())] = avail[u - 1]
    trees[(11, 1)] = (5, [None] * 5)
    del pad[(11, 1, ())]
    for v, s in enumerate([1, 2, 3, 4, 6]):
        pad[(11, 1, ((5, v),))] = s
    iota = {q: i + 1 for i, q in enumerate(QF)}
    tau = [1, 2, 3, 4, 7, 8, 9, 11, 6, 12, 14, 18, 21]
    return P, I, x, trees, pad, iota, tau

def example_45():
    P, I, x = 13, {5, 7}, 2310
    QF = Fpp_list(P, I); assert QF == [2, 3, 4, 8, 9, 11], QF
    assert M_F(11, I) == 72
    trees, pad = {}, {}
    for q in QF:
        j = jq(q); MF = M_F(q, I)
        avail = [d for d in divisors(MF) if d <= x / q and gcd(d, j) == 1]
        for u in range(1, j):
            trees[(q, u)] = None
            pad[(q, u, ())] = avail[u - 1]
    child0 = (5, [None] * 5)
    trees[(11, 1)] = (7, [child0] + [None] * 6)
    del pad[(11, 1, ())]
    for v, s in zip(range(1, 7), [1, 2, 3, 4, 6, 8]):
        pad[(11, 1, ((7, v),))] = s
    for w, s in zip(range(5), [1, 2, 3, 4, 6]):
        pad[(11, 1, ((7, 0), (5, w)))] = s
    iota = {q: i + 1 for i, q in enumerate(QF)}
    tau = [1, 2, 3, 4, 8, 9, 11, 6, 12, 18, 22, 24, 33]
    return P, I, x, trees, pad, iota, tau

def run_examples(full45=False):
    # ---- Example 4.4
    P, I, x, trees, pad, iota, tau = example_44()
    assert check_hyp(P, I, trees, pad, iota, tau) is None
    cls = build(P, I, trees, pad, iota, tau)
    res = check([(a, n) for a, n, _ in cls])
    split = sorted([(a, n) for a, n, t in cls if t[0] == 'A' and t[3]], key=lambda z: z[1])
    print("Ex 4.4:", {k: res[k] for k in ('covering', 'minimal', 'distinct', 'L', 'k', 'maxmod')}, "split classes:", split)
    assert split == [(45, 55), (56, 110), (12, 165), (188, 220), (144, 330)], split
    # all 6720 ordered choices of 5 paddings from {1,2,3,4,6,7,8,9}
    pool = [1, 2, 3, 4, 6, 7, 8, 9]
    seen = set(); nok = 0; t0 = time.time()
    for choice in itertools.permutations(pool, 5):
        for v, s in enumerate(choice):
            pad[(11, 1, ((5, v),))] = s
        cls = build(P, I, trees, pad, iota, tau)
        r = check([(a, n) for a, n, _ in cls])
        nok += ok(r) and r['maxmod'] <= x
        seen.add(system_set(cls))
    print(f"Ex 4.4: {nok} of 6720 padding choices give minimal distinct coverings with moduli <= {x}; "
          f"{len(seen)} pairwise distinct systems  ({time.time()-t0:.0f}s)")
    # ---- Example 4.5
    P, I, x, trees, pad, iota, tau = example_45()
    assert check_hyp(P, I, trees, pad, iota, tau) is None
    cls = build(P, I, trees, pad, iota, tau)
    res = check([(a, n) for a, n, _ in cls])
    split = [(a, n) for a, n, t in cls if t[0] == 'A' and t[3]]
    print("Ex 4.5:", {k: res[k] for k in ('covering', 'minimal', 'distinct', 'L', 'k', 'maxmod')})
    print("        split classes:", sorted(split, key=lambda z: z[1]))
    listed = [(1, 77), (100, 154), (45, 231), (144, 308), (12, 462), (496, 616), (210, 385), (56, 770),
              (672, 1155), (1288, 1540), (1134, 2310)]
    assert sorted(split) == sorted(listed), "Example 4.5 split classes differ from the paper's list"
    pool7 = [d for d in divisors(72) if d <= 30]; assert len(pool7) == 10
    pool35 = [1, 2, 3, 4, 6]
    seen = set(); nok = 0; ntot = 0
    for ch35 in itertools.permutations(pool35):
        for w, s in enumerate(ch35): pad[(11, 1, ((7, 0), (5, w)))] = s
        cls = build(P, I, trees, pad, iota, tau); r = check([(a, n) for a, n, _ in cls])
        nok += ok(r) and r['maxmod'] <= x; ntot += 1; seen.add(system_set(cls))
    print(f"Ex 4.5: all 120 orderings of the I-part-35 paddings: {nok}/{ntot} ok, {len(seen)} distinct")
    for w, s in zip(range(5), pool35): pad[(11, 1, ((7, 0), (5, w)))] = s
    rng = random.Random(45)
    choices = list(itertools.permutations(pool7, 6))
    if not full45:
        choices = rng.sample(choices, 3000)
    seen = set(); nok = 0; t0 = time.time()
    for ch7 in choices:
        for v, s in zip(range(1, 7), ch7): pad[(11, 1, ((7, v),))] = s
        cls = build(P, I, trees, pad, iota, tau); r = check([(a, n) for a, n, _ in cls])
        nok += ok(r) and r['maxmod'] <= x; seen.add(system_set(cls))
    print(f"Ex 4.5: {len(choices)} choices of the I-part-7 paddings: {nok} ok, {len(seen)} distinct ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    run_examples(full45=('--full' in sys.argv))
