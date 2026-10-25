#!/usr/bin/env python3
"""Independent hostile audit for the proposed c_9=2 proof.

This intentionally does not import either supplied checker.  Graphs and repair
partitions are represented as integer bit masks and all useful partitions are
found by brute force rather than by the classifications in the proof.
"""

from collections import Counter
from itertools import combinations, product
from math import gcd


def pop(x):
    return x.bit_count()


def edge_data(left, right):
    pairs = [(i, j) for i in range(left) for j in range(right)]
    return pairs, {pair: k for k, pair in enumerate(pairs)}


def active_count(mask, pairs):
    ls = 0
    rs = 0
    for k, (i, j) in enumerate(pairs):
        if mask >> k & 1:
            ls |= 1 << i
            rs |= 1 << j
    return pop(ls) + pop(rs)


def induced_mask(graph, chosen_left, chosen_right, pairs):
    ans = 0
    for k, (i, j) in enumerate(pairs):
        if graph >> k & 1 and chosen_left >> i & 1 and chosen_right >> j & 1:
            ans |= 1 << k
    return ans


def has_six_vertex_eight_core(graph, pairs):
    for k in range(len(pairs)):
        if graph >> k & 1:
            core = graph ^ (1 << k)
            if active_count(core, pairs) == 6:
                return True
    return False


def useful_partitions(graph, left, right, pairs):
    """Find every 4+5 partition that pays every induced-level excess."""
    edges = [k for k in range(len(pairs)) if graph >> k & 1]
    answers = []
    for chosen in combinations(edges, 4):
        p4 = sum(1 << k for k in chosen)
        p5 = graph ^ p4
        good = True
        for lm in range(1 << left):
            for rm in range(1 << right):
                level = induced_mask(graph, lm, rm, pairs)
                deficit = max(0, pop(level) - active_count(level, pairs))
                paid = int(level & p4 == p4) + int(level & p5 == p5)
                if paid < deficit:
                    good = False
                    break
            if not good:
                break
        if good:
            answers.append((p4, p5))
    return answers


def audit_seven_vertex_graphs():
    counts = Counter()
    certificates = {}
    for left, right in ((2, 5), (3, 4)):
        pairs, _ = edge_data(left, right)
        for chosen in combinations(range(len(pairs)), 9):
            graph = sum(1 << k for k in chosen)
            if active_count(graph, pairs) != 7:
                continue
            if has_six_vertex_eight_core(graph, pairs):
                counts[left, right, "core"] += 1
                continue
            partitions = useful_partitions(graph, left, right, pairs)
            assert partitions, (left, right, graph)
            counts[left, right, "repairable"] += 1
            counts["certificate_count", len(partitions)] += 1
            certificates[left, right, graph] = (pairs, partitions[0])
    assert counts[2, 5, "core"] == 10
    assert counts[2, 5, "repairable"] == 0
    assert counts[3, 4, "core"] == 120
    assert counts[3, 4, "repairable"] == 96
    return counts, certificates


def audit_repairs_directly(certificates, cap=4):
    """Numerically test every endpoint valuation vector for every no-core graph."""
    checked = 0
    for (left, right, graph), (pairs, (p4, p5)) in certificates.items():
        for vals in product(range(cap), repeat=left + right):
            edge_vals = []
            for i, j in pairs:
                edge_vals.append(min(vals[i], vals[left + j]))
            target = sum(edge_vals[k] for k in range(len(pairs)) if graph >> k & 1)
            repairs = [0, 0]
            for level_no in range(1, cap):
                level = 0
                for k in range(len(pairs)):
                    if graph >> k & 1 and edge_vals[k] >= level_no:
                        level |= 1 << k
                deficit = max(0, pop(level) - active_count(level, pairs))
                containing = [q for q, part in enumerate((p4, p5)) if level & part == part]
                assert len(containing) >= deficit
                for q in containing[:deficit]:
                    repairs[q] += 1
            assert target <= sum(vals) + sum(repairs)
            assert repairs[0] <= min(edge_vals[k] for k in range(len(pairs)) if p4 >> k & 1)
            assert repairs[1] <= min(edge_vals[k] for k in range(len(pairs)) if p5 >> k & 1)
            checked += 1
    return checked


def audit_k33(cap=7):
    pairs, index = edge_data(3, 3)
    blocks = []
    for missing in range(3):
        block = 0
        for i, j in pairs:
            if i != missing and j != missing:
                block |= 1 << index[i, j]
        blocks.append(block)
    checked = 0
    for vals in product(range(cap), repeat=6):
        weights = [min(vals[i], vals[3 + j]) for i, j in pairs]
        repairs = [0, 0, 0]
        for level_no in range(1, cap):
            lm = sum(1 << i for i in range(3) if vals[i] >= level_no)
            rm = sum(1 << j for j in range(3) if vals[3 + j] >= level_no)
            level = induced_mask((1 << 9) - 1, lm, rm, pairs)
            deficit = max(0, pop(level) - active_count(level, pairs))
            containing = [q for q, block in enumerate(blocks) if level & block == block]
            assert len(containing) >= deficit
            for q in containing[:deficit]:
                repairs[q] += 1
        assert sum(weights) <= sum(vals) + sum(repairs)
        for q, block in enumerate(blocks):
            assert repairs[q] <= min(weights[k] for k in range(9) if block >> k & 1)
        checked += 1
    return checked


def prime_factors(n):
    ans = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            ans[p] = ans.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        ans[n] = ans.get(n, 0) + 1
    return ans


def minimum_cover(inputs, points):
    factorization = prime_factors(1)
    target_map = {}
    for a in inputs:
        for p, e in prime_factors(a).items():
            target_map[p] = target_map.get(p, 0) + e
    primes = sorted(target_map)
    target = tuple(target_map[p] for p in primes)
    vectors = Counter()
    for y in points:
        vec = []
        for p, cap in zip(primes, target):
            e = 0
            z = y
            while z % p == 0:
                z //= p
                e += 1
            vec.append(min(e, cap))
        vec = tuple(vec)
        if any(vec):
            vectors[vec] += 1
    states = {tuple(0 for _ in target): 0}
    for vec, multiplicity in vectors.items():
        old = dict(states)
        limit = min(multiplicity, sum(target))
        for state, cost in old.items():
            cur = state
            for take in range(1, limit + 1):
                cur = tuple(min(t, x + v) for t, x, v in zip(target, cur, vec))
                new_cost = cost + take
                if new_cost < states.get(cur, 10**9):
                    states[cur] = new_cost
    return states[target]


def build_lower_instance():
    # Frozen candidate's concrete r=5 parameters and CRT solution.
    u, v, w = 101, 103, 107
    qs = [10427, 10429, 10433, 10453, 10457]
    mods = [u * w, v * v] + qs
    residues = [1, (v + 1) * pow(u * w, -1, v * v) % (v * v)]
    residues += [(j + 1) * pow(u * v * w, -1, q) % q for j, q in enumerate(qs)]
    modulus = 1
    t = 0
    for m, r in zip(mods, residues):
        # Pairwise-coprime incremental CRT.
        k = ((r - t) * pow(modulus, -1, m)) % m
        t += modulus * k
        modulus *= m
    x = t * u * v * w
    points = range(x - u * v + 1, x + u * v)
    inputs = [u * v, v * v, u * w, v * w] + qs
    for j, q in enumerate(qs, 1):
        hits = [y for y in points if y % q == 0]
        assert hits == [x - j]
        assert all((x - j) % p for p in (u, v, w))
    return minimum_cover(inputs, points), inputs, len(points)


def scan_small_arithmetic():
    """Exhaust M=9 and M=10 over all A and all interval phases."""
    tested = 0
    worst = 0
    for M in (9, 10):
        for inputs in combinations(range(1, M + 1), 9):
            period = 1
            for a in inputs:
                period = period * a // gcd(period, a)
            for t in range(period):
                # Integer left endpoint: the sparse open-interval phase.
                points = range(t + 1, t + 2 * M)
                mc = minimum_cover(inputs, points)
                assert mc <= 9, (M, inputs, t, mc)
                worst = max(worst, mc)
                tested += 1
                # A nonintegral phase has one extra point and cannot be worse.
    return tested, worst


def main():
    counts, certificates = audit_seven_vertex_graphs()
    direct = audit_repairs_directly(certificates)
    k33 = audit_k33()
    lower, inputs, point_count = build_lower_instance()
    small_count, small_worst = scan_small_arithmetic()
    print("seven-vertex graph counts:", dict(counts))
    print("direct 7-vertex valuation vectors:", direct)
    print("K3,3 valuation vectors:", k33)
    print("n=9 lower instance:", inputs, "points", point_count, "minimum", lower)
    print("small arithmetic intervals:", small_count, "worst minimum", small_worst)
    assert lower == 10
    print("INDEPENDENT AUDIT PASSED")


if __name__ == "__main__":
    main()
