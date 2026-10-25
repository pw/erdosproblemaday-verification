#!/usr/bin/env python3
"""Dependency-free finite audit of the combinatorial steps in the Delta>=7 proof."""

from itertools import combinations


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


# Any coloring with at most five classes has two classes whose union has at
# least eight vertices. Empty classes cover fewer than five colors without a
# separate case.
five_colorings = list(compositions(18, 5))
assert min(sum(sorted(sizes, reverse=True)[:2]) for sizes in five_colorings) == 8

# Pairwise triangle-free unions in a six-coloring force all class sizes to 3.
balanced = [
    sizes for sizes in compositions(18, 6)
    if all(sizes[i] + sizes[j] <= 6 for i, j in combinations(range(6), 2))
]
assert balanced == [(3, 3, 3, 3, 3, 3)]

# Neighbor counts of z in the other five nonempty classes, under degree <= 6.
neighbor_counts = [
    sizes for degree in (5, 6) for sizes in compositions(degree, 5)
    if all(size >= 1 for size in sizes)
]
expected_counts = {(1, 1, 1, 1, 1)} | {
    tuple(2 if i == doubled else 1 for i in range(5))
    for doubled in range(5)
}
assert set(neighbor_counts) == expected_counts

# Hostile audit of the last graph-theoretic implication.  Enumerate every
# cross-class edge pattern on N(z) that supplies an edge for every class pair;
# each must contain a K4 (and hence gives a K5 together with z).
audited_patterns = 0
for sizes in neighbor_counts:
    classes = []
    for color, size in enumerate(sizes):
        classes.extend([color] * size)
    n = len(classes)
    eligible = [
        (u, v) for u, v in combinations(range(n), 2)
        if classes[u] != classes[v]
    ]
    for mask in range(1 << len(eligible)):
        edges = {
            eligible[i] for i in range(len(eligible)) if mask >> i & 1
        }
        covers_pairs = all(
            any(
                tuple(sorted((u, v))) in edges
                for u in range(n) for v in range(n)
                if classes[u] == a and classes[v] == b
            )
            for a, b in combinations(range(5), 2)
        )
        if not covers_pairs:
            continue
        audited_patterns += 1
        assert any(
            all(tuple(sorted(pair)) in edges for pair in combinations(four, 2))
            for four in combinations(range(n), 4)
        )

assert audited_patterns == 1 + 5 * 81
print("VERIFIED: Delta>=7 finite combinatorial audit passes.")
print(f"five_color_size_vectors={len(five_colorings)} minimum_top_two=8")
print(f"six_color_feasible_vectors={balanced}")
print(f"neighbor_count_vectors={len(neighbor_counts)}")
print(f"cross_class_edge_patterns_audited={audited_patterns} all_contain_K4=YES")
