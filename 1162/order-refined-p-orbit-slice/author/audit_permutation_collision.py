#!/usr/bin/env python3
"""Small independent permutation-level audit for verify_order_slice.py.

This constructs the actual subgroups as sets of permutations.  It checks that
different p-block frameworks and full-support vector subspaces never collide,
which is the non-arithmetic step behind the exact multiplier in the theorem.
"""

from __future__ import annotations

import itertools
import math


Permutation = tuple[int, ...]


def identity(n: int) -> Permutation:
    return tuple(range(n))


def compose(first: Permutation, second: Permutation) -> Permutation:
    return tuple(second[first[i]] for i in range(len(first)))


def power(g: Permutation, exponent: int) -> Permutation:
    result = identity(len(g))
    for _ in range(exponent):
        result = compose(result, g)
    return result


def cycle_on_block(n: int, order: tuple[int, ...]) -> Permutation:
    image = list(range(n))
    for a, b in zip(order, order[1:] + order[:1]):
        image[a] = b
    return tuple(image)


def cyclic_p_groups(n: int, block: tuple[int, ...]) -> tuple[tuple[Permutation, ...], ...]:
    anchor = min(block)
    rest = tuple(x for x in block if x != anchor)
    groups: dict[frozenset[Permutation], tuple[Permutation, ...]] = {}
    for tail in itertools.permutations(rest):
        generator = cycle_on_block(n, (anchor,) + tail)
        elements = tuple(power(generator, exponent) for exponent in range(len(block)))
        groups[frozenset(elements)] = elements
    answer = tuple(groups.values())
    assert len(answer) == math.factorial(len(block) - 2)
    return answer


def block_partitions(items: tuple[int, ...], p: int):
    if not items:
        yield ()
        return
    first = items[0]
    for partners in itertools.combinations(items[1:], p - 1):
        block = (first,) + partners
        chosen = set(block)
        remaining = tuple(x for x in items if x not in chosen)
        for suffix in block_partitions(remaining, p):
            yield (block,) + suffix


def frameworks(n: int, p: int, m: int):
    q = n - p * m
    points = tuple(range(n))
    for fixed in itertools.combinations(points, q):
        fixed_set = set(fixed)
        moving = tuple(x for x in points if x not in fixed_set)
        for blocks in block_partitions(moving, p):
            choices = [cyclic_p_groups(n, block) for block in blocks]
            for factors in itertools.product(*choices):
                yield tuple(factor[1] for factor in factors)


def span_vectors(basis: tuple[tuple[int, ...], ...], m: int, p: int):
    for coeffs in itertools.product(range(p), repeat=len(basis)):
        yield tuple(
            sum(coeffs[row] * basis[row][col] for row in range(len(basis))) % p
            for col in range(m)
        )


def brute_subspaces(m: int, p: int) -> dict[int, tuple[frozenset[tuple[int, ...]], ...]]:
    """Enumerate spans of vector subsets; no Gaussian formula or RREF is used."""
    zero = (0,) * m
    nonzero = tuple(v for v in itertools.product(range(p), repeat=m) if v != zero)
    answer: dict[int, set[frozenset[tuple[int, ...]]]] = {
        r: set() for r in range(1, m + 1)
    }
    for r in range(1, m + 1):
        for generators in itertools.combinations(nonzero, r):
            space = frozenset(span_vectors(generators, m, p))
            if len(space) != p**r:
                continue
            if all(any(vector[col] for vector in space) for col in range(m)):
                answer[r].add(space)
    return {r: tuple(spaces) for r, spaces in answer.items()}


def subgroup_from_space(
    generators: tuple[Permutation, ...],
    space: frozenset[tuple[int, ...]],
    p: int,
) -> frozenset[Permutation]:
    n = len(generators[0])
    elements = []
    for vector in space:
        g = identity(n)
        for generator, exponent in zip(generators, vector):
            g = compose(g, power(generator, exponent))
        elements.append(g)
    return frozenset(elements)


def audit_case(n: int, p: int, m: int) -> tuple[int, dict[int, int]]:
    spaces_by_rank = brute_subspaces(m, p)
    groups_by_rank = {r: set() for r in spaces_by_rank}
    framework_total = 0
    for generators in frameworks(n, p, m):
        framework_total += 1
        for r, rank_spaces in spaces_by_rank.items():
            for space in rank_spaces:
                group = subgroup_from_space(generators, space, p)
                assert len(group) == p**r
                groups_by_rank[r].add(group)

    for r, groups in groups_by_rank.items():
        expected = framework_total * len(spaces_by_rank[r])
        assert len(groups) == expected, (n, p, m, r, len(groups), expected)
    counts = {r: len(groups) for r, groups in groups_by_rank.items() if groups}
    print(f"S_{n}, p={p}, m={m}: frameworks={framework_total}, rank_counts={counts}")
    return framework_total, counts


def main() -> None:
    expected = {
        (7, 2, 3): (105, {1: 105, 2: 420, 3: 105}),
        (8, 2, 4): (105, {1: 105, 2: 1365, 3: 1155, 4: 105}),
        (8, 3, 2): (280, {1: 560, 2: 280}),
        (9, 3, 3): (280, {1: 1120, 2: 2800, 3: 280}),
    }
    for case in ((7, 2, 3), (8, 2, 4), (8, 3, 2), (9, 3, 3)):
        assert audit_case(*case) == expected[case]
    print("PERMUTATION-LEVEL COLLISION AUDIT PASSED")


if __name__ == "__main__":
    main()
