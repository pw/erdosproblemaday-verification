#!/usr/bin/env python3
"""Independent finite audit for the integrated Problem 708 c_11 proof.

This program imports none of the candidate checkers.  In particular it
discovers the inherited critical graph classes from labelled graphs, searches
for aligned certificates using frozenset set systems, exhausts the abstract
tight-set contraction used in the singleton Hall repair, and independently
constructs the n=11 private-prime padding example.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import gcd


Edge = tuple[int, int]
Vertex = tuple[str, int]
Block = frozenset[Edge]


def vertices(edges: frozenset[Edge] | set[Edge]) -> frozenset[Vertex]:
    return frozenset({("L", i) for i, _ in edges} | {("R", j) for _, j in edges})


def endpoints(edge: Edge) -> frozenset[Vertex]:
    return frozenset((('L', edge[0]), ('R', edge[1])))


def powerset(items):
    ordered = tuple(items)
    for mask in range(1 << len(ordered)):
        yield frozenset(ordered[i] for i in range(len(ordered)) if mask >> i & 1)


def direct_minimal_core(edges: frozenset[Edge], q: int) -> bool:
    """Check every proper edge subset, not just induced subgraphs."""
    ordered = tuple(edges)
    if len(edges) - len(vertices(edges)) != q:
        return False
    degrees = Counter(vertex for edge in edges for vertex in endpoints(edge))
    if min(degrees.values(), default=0) < 2:
        return False
    for mask in range(1, (1 << len(ordered)) - 1):
        subset = frozenset(ordered[i] for i in range(len(ordered)) if mask >> i & 1)
        if len(subset) - len(vertices(subset)) >= q:
            return False
    return True


def relabel(edges: frozenset[Edge], row_perm, col_perm) -> frozenset[Edge]:
    return frozenset((row_perm[i], col_perm[j]) for i, j in edges)


def graph_code(edges: frozenset[Edge], left: int, right: int) -> str:
    return "/".join(
        "".join("1" if (i, j) in edges else "0" for j in range(right))
        for i in range(left)
    )


def canonical_graph(edges: frozenset[Edge], left: int, right: int) -> tuple[str, frozenset[Edge]]:
    candidates = []
    orientations = ((edges, left, right),)
    if left == right:
        orientations += ((frozenset((j, i) for i, j in edges), left, right),)
    for oriented, rows, cols in orientations:
        for rp in permutations(range(rows)):
            for cp in permutations(range(cols)):
                moved = relabel(oriented, rp, cp)
                candidates.append((graph_code(moved, rows, cols), moved))
    return min(candidates, key=lambda pair: pair[0])


def discover_critical_classes():
    shapes = (
        (2, 8, 2, 4),
        (2, 8, 3, 3),
        (2, 9, 3, 4),
        (2, 10, 3, 5),
        (2, 10, 4, 4),
        (3, 9, 3, 3),
        (3, 10, 2, 5),
        (3, 10, 3, 4),
    )
    classes = {}
    labelled_counts = {}
    direct_subset_checks = 0
    for q, edge_count, left, right in shapes:
        complete = tuple((i, j) for i in range(left) for j in range(right))
        found = {}
        labelled = 0
        for chosen in combinations(complete, edge_count):
            edges = frozenset(chosen)
            if len(vertices(edges)) != left + right:
                continue
            if not direct_minimal_core(edges, q):
                continue
            labelled += 1
            code, representative = canonical_graph(edges, left, right)
            found[code] = representative
        for representative in found.values():
            direct_subset_checks += (1 << len(representative)) - 2
        key = (q, edge_count, left, right)
        classes[key] = tuple(found[code] for code in sorted(found))
        labelled_counts[key] = labelled

    expected_classes = {
        (2, 8, 2, 4): 1,
        (2, 8, 3, 3): 1,
        (2, 9, 3, 4): 2,
        (2, 10, 3, 5): 3,
        (2, 10, 4, 4): 7,
        (3, 9, 3, 3): 1,
        (3, 10, 2, 5): 1,
        (3, 10, 3, 4): 2,
    }
    assert {key: len(value) for key, value in classes.items()} == expected_classes
    assert labelled_counts[(2, 10, 3, 5)] == 210
    assert labelled_counts[(2, 10, 4, 4)] == 2040
    assert labelled_counts[(3, 10, 2, 5)] == 1
    assert labelled_counts[(3, 10, 3, 4)] == 54
    return classes, labelled_counts, direct_subset_checks


def endpoint_levels(edges: frozenset[Edge], left: int, right: int):
    all_vertices = tuple(("L", i) for i in range(left)) + tuple(("R", j) for j in range(right))
    for selected in powerset(all_vertices):
        induced = frozenset(edge for edge in edges if endpoints(edge) <= selected)
        yield selected, induced


def layer_requirements(edges: frozenset[Edge], left: int, right: int, exceptional: Block):
    requirements = set()
    for selected, induced in endpoint_levels(edges, left, right):
        deletable = exceptional & induced
        for deleted in powerset(deletable):
            actual = induced - deleted
            demand = max(0, len(actual) - len(selected))
            if demand:
                requirements.add((actual, demand))
    return tuple(sorted(requirements, key=lambda pair: (pair[1], sorted(pair[0]))))


def all_matchings(edges: frozenset[Edge]):
    ordered = tuple(sorted(edges))
    answers = []
    for size in range(min(len({i for i, _ in edges}), len({j for _, j in edges})) + 1):
        for chosen in combinations(ordered, size):
            used = [vertex for edge in chosen for vertex in endpoints(edge)]
            if len(used) == len(set(used)):
                answers.append(frozenset(chosen))
    return tuple(answers)


def block_pool(edges: frozenset[Edge], size: int) -> tuple[Block, ...]:
    return tuple(frozenset(chosen) for chosen in combinations(sorted(edges), size))


def covers(blocks: tuple[Block, ...], requirements) -> bool:
    return all(sum(block <= actual for block in blocks) >= demand for actual, demand in requirements)


def generic_support_tuples(edges: frozenset[Edge], left: int, right: int, q: int, sizes):
    requirements = layer_requirements(edges, left, right, frozenset())
    pools = tuple(block_pool(edges, size) for size in sizes)
    answers = []
    if q == 2:
        iterator = product(pools[0], pools[1]) if sizes[0] != sizes[1] else combinations(pools[0], 2)
        for first, second in iterator:
            blocks = (first, second)
            if len(first | second) < 6:
                continue
            if covers(blocks, requirements):
                answers.append(blocks)
    else:
        for blocks in combinations(pools[0], 3):
            if any(len(a | b) < 6 for a, b in combinations(blocks, 2)):
                continue
            if len(frozenset().union(*blocks)) < 9:
                continue
            if covers(blocks, requirements):
                answers.append(blocks)
    assert answers
    return tuple(answers)


def endpoint_safe(edges: frozenset[Edge], block: Block, exceptional: Block, left: int, right: int) -> bool:
    all_vertices = tuple(("L", i) for i in range(left)) + tuple(("R", j) for j in range(right))
    for omitted in all_vertices:
        induced_exact = frozenset(
            edge for edge in edges - exceptional if omitted not in endpoints(edge)
        )
        if len(block | induced_exact) < 5:
            return False
    return True


def audit_aligned_fixed_blocks(classes):
    summaries = []
    total_matchings = 0
    robust_layer_requirements = 0
    for (q, edge_count, left, right), representatives in sorted(classes.items()):
        if q == 3 and (left, right) == (2, 5):
            continue
        sizes = (4, 5) if q == 2 and edge_count == 9 else ((4, 4) if q == 2 else (4, 4, 4))
        for class_index, edges in enumerate(representatives):
            tuples = generic_support_tuples(edges, left, right, q, sizes)
            matchings = all_matchings(edges)
            for exceptional in matchings:
                requirements = layer_requirements(edges, left, right, exceptional)
                robust_layer_requirements += len(requirements)
                witness = next(
                    (
                        blocks
                        for blocks in tuples
                        if all(endpoint_safe(edges, block, exceptional, left, right) for block in blocks)
                        and covers(blocks, requirements)
                    ),
                    None,
                )
                assert witness is not None, (q, edge_count, left, right, class_index, exceptional)
            total_matchings += len(matchings)
            summaries.append(
                {
                    "key": (q, edge_count, left, right, class_index),
                    "generic_tuples": len(tuples),
                    "matchings": len(matchings),
                }
            )
    assert len(summaries) == 17  # 14 q=2 and 3 fixed-block q=3 classes.
    return summaries, total_matchings, robust_layer_requirements


def hall(neighborhoods) -> bool:
    count = len(neighborhoods)
    for mask in range(1, 1 << count):
        union = set()
        members = 0
        for index, neighborhood in enumerate(neighborhoods):
            if mask >> index & 1:
                union.update(neighborhood)
                members += 1
        if len(union) < members:
            return False
    return True


def audit_tight_set_contraction():
    """Exhaust small abstract set systems satisfying the written hypotheses."""
    checked = 0
    failing = 0
    bad_sets = 0
    configurations = ((3, 2, 3), (4, 2, 2))  # universe, edge items, repairs
    for universe_size, edge_count, repair_count in configurations:
        universe = frozenset(range(universe_size))
        options = tuple(frozenset(item) for item in powerset(universe) if item)
        for neighborhoods in product(options, repeat=edge_count + repair_count):
            edges = neighborhoods[:edge_count]
            repairs = neighborhoods[edge_count:]
            if not hall(edges):
                continue
            multi_ok = True
            for mask in range(1, 1 << (edge_count + repair_count)):
                chosen_repairs = sum(mask >> (edge_count + i) & 1 for i in range(repair_count))
                if chosen_repairs < 2:
                    continue
                selected = tuple(neighborhoods[i] for i in range(len(neighborhoods)) if mask >> i & 1)
                if len(frozenset().union(*selected)) < len(selected):
                    multi_ok = False
                    break
            if not multi_ok:
                continue
            checked += 1
            if hall(neighborhoods):
                continue
            failing += 1

            deficient_by_repair = defaultdict(list)
            for repair_index in range(repair_count):
                d_index = edge_count + repair_index
                for edge_mask in range(1 << edge_count):
                    selected_indices = [i for i in range(edge_count) if edge_mask >> i & 1] + [d_index]
                    union = frozenset().union(*(neighborhoods[i] for i in selected_indices))
                    if len(union) < len(selected_indices):
                        deficient_by_repair[repair_index].append((edge_mask, union))
            assert len(deficient_by_repair) == 1
            repair_index, witnesses = next(iter(deficient_by_repair.items()))
            without_bad = neighborhoods[: edge_count + repair_index] + neighborhoods[edge_count + repair_index + 1 :]
            assert hall(without_bad)

            for edge_mask, union in witnesses:
                r_indices = tuple(i for i in range(edge_count) if edge_mask >> i & 1)
                n_r = frozenset().union(*(edges[i] for i in r_indices)) if r_indices else frozenset()
                assert len(n_r) == len(r_indices)
                assert union == n_r
                assert repairs[repair_index] <= n_r

                other_items = [
                    neighborhoods[i]
                    for i in range(edge_count + repair_count)
                    if i != edge_count + repair_index and i not in r_indices
                ]
                contracted = tuple(neighborhood - n_r for neighborhood in other_items)
                assert hall(contracted)
                bad_sets += 1
    assert checked and failing and bad_sets
    return checked, failing, bad_sets


def rational_grid(denominator: int) -> frozenset[Fraction]:
    return frozenset(Fraction(k, denominator) for k in range(1, denominator))


def audit_k25():
    profile_checks = 0
    for t in range(3):
        minimum_uncovered = 3 + t
        for count in range(minimum_uncovered, 6):
            for denominators in combinations_with_replacement(range(1, t + 3), count):
                capture_ok = all(
                    sum(m0 % m == 0 for m in denominators) <= 2
                    for m0 in set(denominators)
                )
                grid_size = len(
                    frozenset().union(*(rational_grid(m) for m in denominators))
                )
                assert not (capture_ok and grid_size <= t + 1), (t, denominators)
                profile_checks += 1

    edges = frozenset((i, j) for i in range(2) for j in range(5))
    layer_checks = 0
    for selected, induced in endpoint_levels(edges, 2, 5):
        for deleted in all_matchings(induced):
            actual = induced - deleted
            demand = max(0, len(actual) - len(selected))
            complete_columns = sum((0, j) in actual and (1, j) in actual for j in range(5))
            assert demand <= max(0, complete_columns - 2)
            if len([v for v in selected if v[0] == "L"]) == 2:
                assert demand == max(0, complete_columns - 2)
            layer_checks += 1

    order_statistic_vectors = 0
    for values in product(range(5), repeat=5):
        three_smallest = sum(sorted(values)[:3])
        by_levels = sum(max(0, sum(value >= level for value in values) - 2) for level in range(1, 5))
        assert three_smallest == by_levels
        order_statistic_vectors += 1
    return profile_checks, layer_checks, order_statistic_vectors


def audit_q4_layer_interface():
    rows, cols = range(3), range(4)
    edges = frozenset((i, j) for i in rows for j in cols if (i, j) != (0, 0))
    blocks = tuple(
        ((i, k, j), frozenset(((i, j), (k, j))))
        for i, k in combinations(rows, 2)
        for j in cols
        if (i, j) in edges and (k, j) in edges
    )
    requirements = layer_requirements(edges, 3, 4, frozenset())
    valid = []
    for chosen in combinations(blocks, 4):
        supports = tuple(item[1] for item in chosen)
        if covers(supports, requirements):
            valid.append(frozenset(item[0] for item in chosen))
    expected = set()
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c, d in combinations(range(4), 2):
                if not (a == b and a in (c, d)):
                    expected.add(frozenset(((0, 1, a), (0, 2, b), (1, 2, c), (1, 2, d))))
    assert set(valid) == expected and len(valid) == 45
    return len(requirements), len(valid)


def exact_open_multiples(start: Fraction, maximum: int, divisor: int) -> frozenset[int]:
    low = start.numerator // start.denominator - 2
    high_value = start + 2 * maximum
    high = high_value.numerator // high_value.denominator + 2
    return frozenset(value for value in range(low, high + 1) if start < value < high_value and value % divisor == 0)


def audit_progression_thresholds(limit: int = 180):
    ten_checks = 0
    nine_checks = 0
    phases = (Fraction(0), Fraction(1, 2), Fraction(1, 3), Fraction(-2, 3))
    for maximum in range(4, limit + 1):
        for phase in phases:
            sets = {
                divisor: exact_open_multiples(phase, maximum, divisor)
                for divisor in range(1, maximum // 4 + 1)
            }
            candidates = [d for d, points in sets.items() if len(points) >= 7]
            for first, second in combinations(candidates, 2):
                union = len(sets[first] | sets[second])
                assert union > 10
                ten_checks += 1
                assert union > 9
                nine_checks += 1
    return ten_checks, nine_checks


def egcd(a: int, b: int):
    if not b:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def crt(residues, moduli) -> int:
    modulus = 1
    value = 0
    for residue, next_modulus in zip(residues, moduli):
        g, inverse, _ = egcd(modulus, next_modulus)
        assert g == 1
        step = ((residue - value) * inverse) % next_modulus
        value += modulus * step
        modulus *= next_modulus
        value %= modulus
    return value


def valuation(value: int, prime: int, cap: int) -> int:
    answer = 0
    while answer < cap and value % prime == 0:
        value //= prime
        answer += 1
    return answer


def minimum_cover(types: Counter, target: tuple[int, ...]) -> int | None:
    zero = (0,) * len(target)
    dp = {zero: 0}
    for vector, multiplicity in types.items():
        if not any(vector):
            continue
        max_use = min(
            multiplicity,
            max((target[i] + vector[i] - 1) // vector[i] for i in range(len(target)) if vector[i]),
        )
        old = tuple(dp.items())
        updated = dict(dp)
        for state, cost in old:
            current = state
            for copies in range(1, max_use + 1):
                current = tuple(min(target[i], current[i] + vector[i]) for i in range(len(target)))
                updated[current] = min(updated.get(current, 10**9), cost + copies)
        dp = updated
    return dp.get(target)


def audit_padding_n11():
    u, v, w = 101, 103, 107
    qs = (10427, 10429, 10433, 10453, 10457, 10459, 10463)
    r = len(qs)
    assert u > r and all(u * v + r < q < v * w for q in qs)
    moduli = (u * w, v * v) + qs
    residues = (
        1,
        ((v + 1) * pow(u * w, -1, v * v)) % (v * v),
    ) + tuple((j * pow(u * v * w, -1, q)) % q for j, q in enumerate(qs, 1))
    t = crt(residues, moduli)
    x = t * u * v * w
    low, high = x - u * v, x + u * v
    points = tuple(range(low + 1, high))
    primes = (u, v, w) + qs
    target = (2, 4, 2) + (1,) * r
    types = Counter(
        tuple(valuation(point, prime, target[i]) for i, prime in enumerate(primes))
        for point in points
    )

    for j, q in enumerate(qs, 1):
        q_multiples = [point for point in points if point % q == 0]
        assert q_multiples == [x - j]
        assert all((x - j) % prime for prime in (u, v, w))
    assert [point for point in points if point % (v * v) == 0] == [x - v]
    assert valuation(x - v, v, 4) == 2
    for pair_product in (u * v, u * w, v * w):
        assert [point for point in points if point % pair_product == 0] == [x]
    assert tuple(valuation(x, prime, 5) for prime in (u, v, w)) == (1, 1, 1)

    optimum = minimum_cover(types, target)
    assert optimum == 12
    return {
        "integer_points": len(points),
        "valuation_types": len(types),
        "minimum_cover": optimum,
        "required_points": 11,
        "metric_ratio": Fraction(2 * u, w),
        "q_primes": qs,
    }


def main():
    classes, labelled, subset_checks = discover_critical_classes()
    robust, matching_count, robust_requirements = audit_aligned_fixed_blocks(classes)
    contraction = audit_tight_set_contraction()
    k25 = audit_k25()
    q4 = audit_q4_layer_interface()
    progressions = audit_progression_thresholds()
    padding = audit_padding_n11()

    print("C11_INTEGRATED_COLD_AUDIT=PASS")
    print("critical_class_counts=", {key: len(value) for key, value in classes.items()})
    print("critical_labelled_counts=", labelled)
    print("direct_proper_edge_subset_checks=", subset_checks)
    print("aligned_robust_classes=", len(robust))
    print("aligned_exceptional_matchings=", matching_count)
    print("aligned_robust_requirements=", robust_requirements)
    for summary in robust:
        print("ROBUST", summary)
    print("tight_set_contraction=", contraction)
    print("k25=", k25)
    print("q4_layer_interface=", q4)
    print("progression_smoke=", progressions)
    print("padding_n11=", padding)


if __name__ == "__main__":
    main()
