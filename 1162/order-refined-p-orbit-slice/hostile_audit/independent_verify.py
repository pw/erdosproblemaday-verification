#!/usr/bin/env python3
"""Independent finite audit for the proposed Problem 1162 result.

This program deliberately does not import or execute any code from the author
bundle.  It uses three finite models:

1. additive-closure enumeration of every subspace of small F_p^m;
2. generation of the complete subgroup lattice of S_5 from permutations; and
3. direct construction of the permutation groups arising from every orbit
   framework in selected cases in S_8 and S_9.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, permutations, product
from math import e, factorial, log2


def gaussian(m: int, r: int, p: int) -> int:
    if r < 0 or r > m:
        return 0
    r = min(r, m - r)
    numerator = 1
    denominator = 1
    for i in range(r):
        numerator *= p ** (m - i) - 1
        denominator *= p ** (r - i) - 1
    assert numerator % denominator == 0
    return numerator // denominator


def full_support_formula(m: int, r: int, p: int) -> int:
    return sum(
        (-1) ** j * combinations_count(m, j) * gaussian(m - j, r, p)
        for j in range(m + 1)
    )


def combinations_count(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))


def framework_count(n: int, m: int, p: int) -> int:
    q = n - p * m
    assert q >= 0
    denominator = factorial(q) * factorial(m) * (p * (p - 1)) ** m
    assert factorial(n) % denominator == 0
    return factorial(n) // denominator


def theorem_count(n: int, m: int, r: int, p: int) -> int:
    return framework_count(n, m, p) * full_support_formula(m, r, p)


def vector_rank_from_size(size: int, p: int) -> int:
    rank = 0
    while size > 1:
        assert size % p == 0
        size //= p
        rank += 1
    return rank


@lru_cache(maxsize=None)
def all_subspaces(p: int, m: int) -> tuple[frozenset[tuple[int, ...]], ...]:
    """Enumerate subspaces by additive closure, with no row-reduction code."""
    vectors = tuple(product(range(p), repeat=m))
    zero = (0,) * m
    initial = frozenset((zero,))
    found = {initial}
    queue = deque((initial,))
    while queue:
        space = queue.popleft()
        for vector in vectors:
            if vector in space:
                continue
            extension = frozenset(
                tuple((w[i] + a * vector[i]) % p for i in range(m))
                for w in space
                for a in range(p)
            )
            if extension not in found:
                found.add(extension)
                queue.append(extension)
    return tuple(found)


def has_full_support(space: frozenset[tuple[int, ...]], m: int) -> bool:
    return all(any(vector[i] != 0 for vector in space) for i in range(m))


def check_additive_subspace_model() -> None:
    for p, m in ((2, 6), (3, 4), (5, 3)):
        spaces = all_subspaces(p, m)
        rank_counts = Counter(vector_rank_from_size(len(space), p) for space in spaces)
        expected_all = {r: gaussian(m, r, p) for r in range(m + 1)}
        assert dict(sorted(rank_counts.items())) == expected_all

        full_counts = Counter(
            vector_rank_from_size(len(space), p)
            for space in spaces
            if has_full_support(space, m)
        )
        expected_full = {
            r: full_support_formula(m, r, p)
            for r in range(m + 1)
            if full_support_formula(m, r, p)
        }
        assert dict(sorted(full_counts.items())) == expected_full
        print(
            f"additive subspaces F_{p}^{m}: total={len(spaces)}, "
            f"full_by_rank={dict(sorted(full_counts.items()))}"
        )


Permutation = tuple[int, ...]


def identity(n: int) -> Permutation:
    return tuple(range(n))


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(perm: Permutation) -> Permutation:
    result = [0] * len(perm)
    for i, image in enumerate(perm):
        result[image] = i
    return tuple(result)


def perm_power(perm: Permutation, exponent: int) -> Permutation:
    result = identity(len(perm))
    for _ in range(exponent):
        result = compose(result, perm)
    return result


def generated_group(n: int, generators: tuple[Permutation, ...]) -> frozenset[Permutation]:
    generators = tuple(dict.fromkeys(generators + tuple(inverse(g) for g in generators)))
    unit = identity(n)
    found = {unit}
    queue = deque((unit,))
    while queue:
        element = queue.popleft()
        for generator in generators:
            new_element = compose(element, generator)
            if new_element not in found:
                found.add(new_element)
                queue.append(new_element)
    return frozenset(found)


def subgroup_lattice_s5() -> tuple[frozenset[Permutation], ...]:
    n = 5
    symmetric_group = tuple(permutations(range(n)))
    trivial = frozenset((identity(n),))
    generators_for = {trivial: ()}
    queue = deque((trivial,))
    while queue:
        subgroup = queue.popleft()
        old_generators = generators_for[subgroup]
        for element in symmetric_group:
            if element in subgroup:
                continue
            extension = generated_group(n, old_generators + (element,))
            if extension not in generators_for:
                generators_for[extension] = old_generators + (element,)
                queue.append(extension)
    return tuple(generators_for)


def prime_power_rank(order: int, p: int) -> int | None:
    rank = 0
    while order % p == 0:
        order //= p
        rank += 1
    return rank if order == 1 else None


def point_orbits(group: frozenset[Permutation], n: int) -> tuple[tuple[int, ...], ...]:
    unseen = set(range(n))
    orbits = []
    while unseen:
        point = min(unseen)
        orbit = tuple(sorted({element[point] for element in group}))
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return tuple(sorted(orbits))


def check_complete_s5_lattice() -> None:
    subgroups = subgroup_lattice_s5()
    assert len(subgroups) == 156
    for p in (2, 3, 5):
        observed = Counter()
        for subgroup in subgroups:
            rank = prime_power_rank(len(subgroup), p)
            if rank is None or rank == 0:
                continue
            orbits = point_orbits(subgroup, 5)
            if all(len(orbit) in (1, p) for orbit in orbits):
                m = sum(len(orbit) == p for orbit in orbits)
                if m:
                    observed[m, rank] += 1
        expected = Counter()
        for m in range(1, 5 // p + 1):
            for rank in range(1, m + 1):
                count = theorem_count(5, m, rank, p)
                if count:
                    expected[m, rank] = count
        assert observed == expected
        print(f"complete S_5 lattice p={p}: slice_counts={dict(sorted(observed.items()))}")


def equal_block_partitions(items: tuple[int, ...], p: int):
    if not items:
        yield ()
        return
    first = items[0]
    for companions in combinations(items[1:], p - 1):
        block = (first,) + companions
        remainder = tuple(x for x in items if x not in block)
        for tail in equal_block_partitions(remainder, p):
            yield (block,) + tail


def cycle_permutation(n: int, cycle: tuple[int, ...]) -> Permutation:
    result = list(range(n))
    for i, point in enumerate(cycle):
        result[point] = cycle[(i + 1) % len(cycle)]
    return tuple(result)


def regular_cyclic_generators(n: int, block: tuple[int, ...]) -> tuple[Permutation, ...]:
    first = block[0]
    cyclic_groups = {}
    for tail in permutations(block[1:]):
        generator = cycle_permutation(n, (first,) + tail)
        group = frozenset(perm_power(generator, exponent) for exponent in range(len(block)))
        cyclic_groups.setdefault(group, min(group - {identity(n)}))
    return tuple(cyclic_groups.values())


def check_framework_collisions(n: int, p: int) -> None:
    assert n % p == 0
    m = n // p
    spaces = tuple(
        space for space in all_subspaces(p, m) if has_full_support(space, m)
    )
    groups_seen: set[frozenset[Permutation]] = set()
    frameworks = 0
    observed_ranks = Counter()

    for blocks in equal_block_partitions(tuple(range(n)), p):
        generator_options = tuple(regular_cyclic_generators(n, block) for block in blocks)
        for generators in product(*generator_options):
            frameworks += 1
            for space in spaces:
                permutation_group = frozenset(
                    compose_many(
                        tuple(perm_power(generators[i], vector[i]) for i in range(m)), n
                    )
                    for vector in space
                )
                assert len(permutation_group) == len(space)
                assert point_orbits(permutation_group, n) == tuple(sorted(blocks))
                for block, generator in zip(blocks, generators):
                    recovered_projection = frozenset(
                        tuple(element[point] for point in block)
                        for element in permutation_group
                    )
                    expected_projection = frozenset(
                        tuple(perm_power(generator, exponent)[point] for point in block)
                        for exponent in range(p)
                    )
                    assert recovered_projection == expected_projection
                assert permutation_group not in groups_seen
                groups_seen.add(permutation_group)
                observed_ranks[vector_rank_from_size(len(space), p)] += 1

    assert frameworks == framework_count(n, m, p)
    expected_ranks = Counter(
        {
            rank: frameworks * full_support_formula(m, rank, p)
            for rank in range(1, m + 1)
            if full_support_formula(m, rank, p)
        }
    )
    assert observed_ranks == expected_ranks
    assert len(groups_seen) == sum(expected_ranks.values())
    print(
        f"collision audit S_{n}, p={p}: frameworks={frameworks}, "
        f"groups_by_rank={dict(sorted(observed_ranks.items()))}"
    )


def compose_many(perms: tuple[Permutation, ...], n: int) -> Permutation:
    result = identity(n)
    for perm in perms:
        result = compose(result, perm)
    return result


def check_arithmetic_and_limits() -> None:
    for p in (2, 3, 5, 7, 11):
        for m in range(1, 13):
            n = p * m + (p - 1)
            for rank in range(m + 1):
                count = theorem_count(n, m, rank, p)
                assert isinstance(count, int) and count >= 0

    n = 20
    exact = theorem_count(n, n // 2, n // 4, 2)
    assert exact == 52_502_131_339_708_050
    print(f"exact p=2 middle slice at n=20: {exact}")

    for p in (2, 3, 5):
        residuals = []
        for m in (40, 41, 80, 81):
            n = p * m
            rank = m // 2
            exact_log = log2(theorem_count(n, m, rank, p))
            displayed = (
                log2(p) * n * n / (4 * p * p)
                + (1 - 1 / p) * n * log2(n)
                - ((1 - 1 / p) * log2(e) + log2(p - 1) / p) * n
            )
            residuals.append(exact_log - displayed)
        assert max(abs(value) for value in residuals) < 4
        assert abs(residuals[2] - residuals[0]) < 0.01
        assert abs(residuals[3] - residuals[1]) < 0.01
        print(f"bounded equation-(2) residuals p={p}: " + ", ".join(f"{x:.9f}" for x in residuals))

    for p, m in ((2, 40), (2, 41), (3, 30), (3, 31)):
        s = m // 2
        central = full_support_formula(m, s, p)
        errors = []
        for k in range(-3, 4):
            rank = s + k
            observed_ratio = full_support_formula(m, rank, p) / central
            exponent = -k * k if m % 2 == 0 else -k * (k - 1)
            predicted_ratio = p**exponent
            errors.append(abs(observed_ratio - predicted_ratio))
        assert max(errors) < 0.001
        print(f"theta-ratio audit p={p}, m={m}: max_error={max(errors):.12g}")


def main() -> None:
    check_additive_subspace_model()
    check_complete_s5_lattice()
    check_framework_collisions(8, 2)
    check_framework_collisions(9, 3)
    check_arithmetic_and_limits()
    print("INDEPENDENT PROBLEM 1162 FINITE AUDIT PASSED")


if __name__ == "__main__":
    main()
