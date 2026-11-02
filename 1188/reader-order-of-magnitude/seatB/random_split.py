#!/usr/bin/env python3
"""Random instances of Construction 4.2 with deep splitting trees (labels in ANY order, not only
decreasing -- Proposition 4.3 only assumes distinct labels on each path), checked exhaustively.
Also: negative controls that violate one hypothesis each, to show the checker can fail, and an
injectivity test (all permutations of one (q,e) padding group give distinct valid systems)."""
import itertools, random, sys, time
from math import gcd, prod
from cover import check, ok, lcmlist
from split import Fpp_list, M_F, jq, divisors, leaves, leaf_e_r, build, check_hyp, system_set

def rand_instance(rng, P, I, maxdepth=3, pdepth=(0.5, 0.4, 0.3, 0.2)):
    """Greedy random data for Construction 4.2: trees grown node by node; a node with I-part e is split
    by c only if the pool for I-part e*c still has >= c unused paddings; a leaf takes a random unused
    padding of its I-part (labels in arbitrary order, distinct along each path)."""
    QF = Fpp_list(P, I)
    MFP = M_F(P, I)
    if len(divisors(MFP)) < P: raise RuntimeError("M_F(P) has fewer than P divisors: (T3) impossible")
    for attempt in range(500):
        trees, pad = {}, {}
        try:
            for q in QF:
                j = jq(q); MF = M_F(q, I)
                avail = [d for d in divisors(MF) if gcd(d, j) == 1]
                rem = {}
                def R(e):
                    if e not in rem: rem[e] = list(avail)
                    return rem[e]
                def grow(e, used, dep, path, u):
                    opts = [c for c in sorted(I) if c not in used and len(R(e * c)) >= c]
                    must = len(R(e)) == 0
                    if opts and dep < maxdepth and (must or rng.random() < pdepth[dep]):
                        c = rng.choice(opts)
                        return (c, [grow(e * c, used | {c}, dep + 1, path + ((c, v),), u) for v in range(c)])
                    if must: raise ValueError
                    s_ = R(e).pop(rng.randrange(len(R(e))))
                    pad[(q, u, path)] = s_
                    return None
                for u in range(1, j):
                    trees[(q, u)] = grow(1, frozenset(), 0, (), u)
            break
        except ValueError:
            continue
    else:
        raise RuntimeError("could not place paddings")
    iv = rng.sample(range(1, P), len(QF))
    iota = dict(zip(QF, iv))
    tau = [None] * P; tau[0] = 1
    for q in QF: tau[iota[q]] = q
    rest = [d for d in divisors(MFP) if d not in set(tau)]
    free = [t for t in range(P) if tau[t] is None]
    for t, d in zip(free, rng.sample(rest, len(free))): tau[t] = d
    return trees, pad, iota, tau

def depth(tree): return 0 if tree is None else 1 + max(depth(ch) for ch in tree[1])

def main():
    rng = random.Random(1188)
    configs = [(11, {3}), (11, {5}), (11, {5, 7}), (13, {5}), (13, {5, 7}), (13, {7}),
               (13, {5, 11}), (13, {5, 7, 11}), (17, {5, 7}), (17, {5}), (17, {5, 7, 11}),
               (17, {5, 11, 13}), (17, {7, 11, 13}), (17, {5, 7, 11, 13})]
    tot = good = 0; maxd = 0; maxk = 0
    for P, I in configs:
        for rep in range(4):
            try:
                trees, pad, iota, tau = rand_instance(rng, P, I)
            except RuntimeError as ex:
                print(f"P={P} I={sorted(I)}: skipped ({ex})"); continue
            h = check_hyp(P, I, trees, pad, iota, tau); assert h is None, h
            cls = build(P, I, trees, pad, iota, tau)
            res = check([(a, n) for a, n, _ in cls])
            d = max(depth(t) for t in trees.values())
            nsplit = sum(1 for _, _, t in cls if t[0] == 'A' and t[3])
            tot += 1; good += ok(res); maxd = max(maxd, d); maxk = max(maxk, res['k'])
            print(f"P={P:2d} I={sorted(I)} rep={rep}: k={res['k']:4d} split={nsplit:4d} maxdepth={d} L={res['L']:>9d} "
                  f"covering={res['covering']} minimal={res['minimal']} distinct={res['distinct']}", flush=True)
    print(f"RANDOM INSTANCES: {good}/{tot} minimal distinct covering systems; max tree depth {maxd}; max classes {maxk}")

    # ---------------- negative controls: violate one hypothesis at a time -------------------
    print("\nNEGATIVE CONTROLS (each must FAIL)")
    P, I = 13, {5, 7}
    trees, pad, iota, tau = rand_instance(random.Random(7), P, I, pdepth=(0.9, 0.7, 0.3, 0.2))
    base = build(P, I, trees, pad, iota, tau)
    assert ok(check([(a, n) for a, n, _ in base]))
    # (i) drop one leaf class of a split fibre -> not covering
    idx = next(i for i, (_, _, t) in enumerate(base) if t[0] == 'A' and t[3])
    cls = base[:idx] + base[idx + 1:]
    print(" (i) drop one split leaf      :", {k: v for k, v in check([(a, n) for a, n, _ in cls]).items() if k in ('covering','minimal','distinct','uncovered')})
    # (ii) duplicate padding inside one (q,e) group -> repeated modulus
    key = next(k for k in pad if k[2])  # a split leaf
    q, u, path = key; e, _ = leaf_e_r(path)
    other = next(k for k in pad if k != key and k[0] == q and leaf_e_r(k[2])[0] == e)
    pad2 = dict(pad); pad2[other] = pad[key]
    cls = build(P, I, trees, pad2, iota, tau)
    print(" (ii) T1 distinctness broken  :", check_hyp(P, I, trees, pad2, iota, tau), {k: v for k, v in check([(a, n) for a, n, _ in cls]).items() if k in ('covering','minimal','distinct')})
    # (iii) padding with a component >= q (does not divide M_F(q)) -> fibre not covered
    pad3 = dict(pad); q0 = 11; key3 = next(k for k in pad if k[0] == q0)
    pad3[key3] = 13 * 2  # 13 does not divide M_F(11)
    cls = build(P, I, trees, pad3, iota, tau)
    print(" (iii) padding not | M_F(q)    :", check_hyp(P, I, trees, pad3, iota, tau), {k: v for k, v in check([(a, n) for a, n, _ in cls]).items() if k in ('covering','minimal','distinct','uncovered')})
    # (iv) tau(iota(q)) != q for one level q -> some A-class loses its private integer?
    QF = Fpp_list(P, I)
    tau4 = list(tau); qq = 4; t4 = iota[qq]
    swap = next(t for t in range(1, P) if tau4[t] not in QF and t != t4)
    tau4[t4], tau4[swap] = tau4[swap], tau4[t4]
    cls = build(P, I, trees, pad, iota, tau4)
    r4 = check([(a, n) for a, n, _ in cls])
    print(" (iv) tau(iota(4)) != 4        :", check_hyp(P, I, trees, pad, iota, tau4), {k: v for k, v in r4.items() if k in ('covering','minimal','distinct')}, "no-private classes:", r4['no_private'][:4])

    # ---------------- injectivity: permute one (q,e) group fully -----------------------------
    print("\nINJECTIVITY")
    groups = {}
    for (q, u, path) in pad:
        if path: groups.setdefault((q, leaf_e_r(path)[0]), []).append((q, u, path))
    (q, e), ls = max(groups.items(), key=lambda kv: len(kv[1]) if len(kv[1]) <= 6 else 0)
    vals = [pad[k] for k in ls]
    seen = set(); nok = 0; n = 0
    for perm in itertools.permutations(vals):
        p2 = dict(pad)
        for k, s in zip(ls, perm): p2[k] = s
        cls = build(P, I, trees, p2, iota, tau)
        nok += ok(check([(a, n_) for a, n_, _ in cls])); n += 1; seen.add(system_set(cls))
    print(f" level q={q}, I-part e={e}: {len(ls)} leaves; {n} permutations -> {nok} valid, {len(seen)} distinct systems")

if __name__ == "__main__":
    main()
