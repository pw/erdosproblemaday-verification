#!/usr/bin/env python3
"""Independent finite audit for the c11 K3,4-e placement candidate.

The infinite steps remain the written open-interval count, Konig's theorem,
and Rado's theorem.  This script independently checks every finite pattern
used in the confined-grid argument, the layer certificate, and two literal
exact-difference kernels (including the known empty-q12-column example).
"""

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import gcd


ROWS = range(3)
COLS = range(4)
MISSING = (0, 0)
EDGES = tuple(
    (i, j) for i in ROWS for j in COLS if (i, j) != MISSING
)


def grid(m):
    return frozenset(Fraction(k, m) for k in range(1, m))


def capture_ok(ms):
    """The proved C_m0 <= 2 condition for every occurring denominator."""
    return all(sum(m0 % m == 0 for m in ms) <= 2 for m0 in set(ms))


def audit_confined_grids():
    # t=1: no three occurrences fit in the third row plus one outside point.
    feasible_t1 = []
    for ms in combinations_with_replacement(range(1, 4), 3):
        union = frozenset().union(*(grid(m) for m in ms))
        if capture_ok(ms) and len(union) <= 2:
            feasible_t1.append(ms)
    assert feasible_t1 == []

    # t=2,3: every feasible multiset of at least three occurrences contains
    # denominators 2 and 3, and hence the midpoint/trisection grid.
    summaries = {}
    target = grid(2) | grid(3)
    for t in (2, 3):
        cases = []
        for size in (3, 4):
            for ms in combinations_with_replacement(range(1, t + 3), size):
                union = frozenset().union(*(grid(m) for m in ms))
                if capture_ok(ms) and len(union) <= t + 1:
                    assert 2 in ms and 3 in ms
                    assert target <= union
                    cases.append(ms)
        summaries[t] = tuple(cases)
        assert cases

    # Four t=2 occurrences have exactly the multiplicities used in the hard
    # r(C)>=3 equality case.
    t2_size4 = [ms for ms in summaries[2] if len(ms) == 4]
    assert t2_size4 == [(2, 2, 3, 3)]

    # t=4 with the third row outside: internal grids have only the four T
    # positions.  Three or four occurrences again force denominators 2,3.
    adjacent_t4 = []
    for size in (3, 4):
        for ms in combinations_with_replacement(range(1, 7), size):
            union = frozenset().union(*(grid(m) for m in ms))
            if capture_ok(ms) and len(union) <= 4:
                assert 2 in ms and 3 in ms
                assert target <= union
                adjacent_t4.append(ms)
    assert adjacent_t4

    # The only apparent t=0 two-block patterns reach C=2.  The written proof
    # excludes them by the exact equality |Z(q)|=|F|=7, not by grid geometry.
    t0_pairs = []
    for ms in combinations_with_replacement(range(1, 3), 2):
        if capture_ok(ms):
            assert any(sum(m0 % m == 0 for m in ms) == 2 for m0 in set(ms))
            t0_pairs.append(ms)
    assert t0_pairs == [(1, 1), (1, 2), (2, 2)]

    return {
        "t1_forbidden_triples": 10,
        "t2_t3_feasible_profiles": sum(map(len, summaries.values())),
        "t4_adjacent_profiles": len(adjacent_t4),
        "t0_equality_profiles": len(t0_pairs),
    }


def audit_geometry():
    s = grid(2) | grid(3)
    ratios = {}
    for small in s:
        for large in s:
            ratio = large / small
            if ratio > 1:
                ratios.setdefault(ratio, []).append((small, large))
    assert set(ratios) == {Fraction(3, 2), Fraction(2), Fraction(4, 3)}
    assert all(len(pairs) == 1 for pairs in ratios.values())

    # A broad exact-rational smoke test of the uniform two-pair inequality.
    checked = 0
    minimum = 99
    for denominator in range(1, 81):
        for numerator in range(-240, 241):
            z = Fraction(numerator, denominator)
            if z in (0, 1):
                continue
            rows = (Fraction(0), Fraction(1), z)
            union = set()
            for i, k, omitted in ((0, 1, 2), (0, 2, 1)):
                points = {
                    rows[i] + ratio * (rows[k] - rows[i]) for ratio in s
                }
                points.discard(rows[omitted])
                union.update(points)
            minimum = min(minimum, len(union))
            assert len(union) >= 4
            checked += 1
    assert minimum == 4
    return checked, minimum


def cover_profiles(sizes, budget):
    for t in range(budget + 1):
        max_h = budget - t
        for hs in product(*(range(size + 1) for size in sizes)):
            if sum(hs) <= max_h:
                yield t, hs, tuple(size - h for size, h in zip(sizes, hs))


def impossible_profile(name, t, remaining):
    """Encode exactly the contradictions invoked in the written rank proof."""
    if t == 0:
        return any(count > 1 for count in remaining)
    if t == 1:
        return any(count > 2 for count in remaining)
    if name == "C":
        # Its only budget-two t=2 profile is the full four-block family,
        # excluded by the five-divisible-vertices equality argument.
        return t == 2 and remaining == (4,)
    if name in ("AC", "BC"):
        if t == 2:
            return remaining[1] == 4 or all(count >= 3 for count in remaining)
        if t == 3:
            return all(count >= 3 for count in remaining)
    if name == "ABC":
        if t == 2:
            if remaining[2] == 4:
                return True
            return sum(count >= 3 for count in remaining) >= 2
        if t == 3:
            return sum(count >= 3 for count in remaining) >= 2
        if t == 4:
            return remaining == (3, 3, 4)
    return False


def audit_rank_case_split():
    claims = {
        "A": ((3,), 0),
        "B": ((3,), 0),
        "C": ((4,), 2),
        "AB": ((3, 3), 1),
        "AC": ((3, 4), 3),
        "BC": ((3, 4), 3),
        "ABC": ((3, 3, 4), 4),
    }
    checked = 0
    for name, (sizes, alleged_rank) in claims.items():
        for t, hs, remaining in cover_profiles(sizes, alleged_rank):
            if name in ("A", "B", "AB"):
                bad = (t == 0 and any(n > 1 for n in remaining)) or (
                    t == 1 and any(n > 2 for n in remaining)
                )
            else:
                bad = impossible_profile(name, t, remaining)
            assert bad, (name, t, hs, remaining)
            checked += 1
    return checked


def induced_levels():
    levels = []
    for row_mask in range(1 << 3):
        for col_mask in range(1 << 4):
            level = frozenset(
                (i, j)
                for i, j in EDGES
                if row_mask >> i & 1 and col_mask >> j & 1
            )
            excess = max(0, len(level) - row_mask.bit_count() - col_mask.bit_count())
            if excess:
                levels.append((level, excess))
    return tuple(levels)


def block_records():
    records = []
    for j in COLS:
        for i, k in combinations(ROWS, 2):
            support = frozenset(((i, j), (k, j)))
            if support <= frozenset(EDGES):
                records.append(((i, k, j), support))
    return tuple(records)


def audit_layer_certificate():
    levels = induced_levels()
    blocks = block_records()
    admissible = []
    for chosen in combinations(range(len(blocks)), 4):
        if all(
            sum(blocks[index][1] <= level for index in chosen) >= excess
            for level, excess in levels
        ):
            admissible.append(chosen)
    assert len(levels) == 17
    assert len(blocks) == 10
    assert len(admissible) == 45

    named = {name: index for index, (name, _) in enumerate(blocks)}
    expected = set()
    for a in range(1, 4):
        for b in range(1, 4):
            for c, d in combinations(range(4), 2):
                if not (a == b and a in (c, d)):
                    expected.add(
                        tuple(
                            sorted(
                                (
                                    named[0, 1, a],
                                    named[0, 2, b],
                                    named[1, 2, c],
                                    named[1, 2, d],
                                )
                            )
                        )
                    )
    assert set(admissible) == expected

    vectors = 0
    for values in product(range(4), repeat=7):
        row_values, col_values = values[:3], values[3:]
        edge_values = {
            edge: min(row_values[edge[0]], col_values[edge[1]])
            for edge in EDGES
        }
        block_values = [
            min(edge_values[edge] for edge in support) for _, support in blocks
        ]
        repair = min(
            sum(block_values[index] for index in chosen) for chosen in admissible
        )
        assert sum(edge_values.values()) <= sum(values) + repair
        vectors += 1
    return len(levels), len(admissible), vectors


def maximum_matching(neighborhoods):
    owner = {}

    def augment(left, seen):
        for point in neighborhoods[left]:
            if point in seen:
                continue
            seen.add(point)
            if point not in owner or augment(owner[point], seen):
                owner[point] = left
                return True
        return False

    return sum(augment(left, set()) for left in range(len(neighborhoods)))


def literal_kernel(maximum, start, left, right):
    labels = {(i, j): right[j] - left[i] for i, j in EDGES}
    assert min(labels.values()) > 0
    assert max(labels.values()) == maximum
    assert len(set(labels.values())) == 11
    assert all(
        left[i] % label == 0 and right[j] % label == 0
        for (i, j), label in labels.items()
    )
    forbidden = set(left + right)
    blocks = {}
    for i, k, columns in (
        (0, 1, range(1, 4)),
        (0, 2, range(1, 4)),
        (1, 2, range(4)),
    ):
        for j in columns:
            q = gcd(labels[i, j], labels[k, j])
            blocks[i, k, j] = tuple(
                point
                for point in range(start + 1, start + 2 * maximum)
                if point % q == 0 and point not in forbidden
            )

    families = (
        tuple(blocks[0, 1, j] for j in range(1, 4)),
        tuple(blocks[0, 2, j] for j in range(1, 4)),
        tuple(blocks[1, 2, j] for j in range(4)),
    )
    unions = (
        families[0],
        families[1],
        families[2],
        families[0] + families[1],
        families[0] + families[2],
        families[1] + families[2],
        families[0] + families[1] + families[2],
    )
    ranks = tuple(maximum_matching(group) for group in unions)
    required = (1, 1, 3, 2, 4, 4, 5)
    assert all(actual >= lower for actual, lower in zip(ranks, required))

    five_witnesses = 0
    four_witnesses = 0
    for a in range(3):
        for b in range(3):
            for cs in combinations(range(4), 3):
                chosen = [families[0][a], families[1][b]] + [families[2][c] for c in cs]
                if maximum_matching(chosen) < 5:
                    continue
                five_witnesses += 1
                keep_options = [pair for pair in combinations(cs, 2) if not (a == b and a + 1 in pair)]
                assert keep_options
                assert any(
                    maximum_matching(
                        [families[0][a], families[1][b]]
                        + [families[2][c] for c in pair]
                    )
                    == 4
                    for pair in keep_options
                )
                four_witnesses += 1
    assert five_witnesses > 0
    return labels, blocks, ranks, five_witnesses, four_witnesses


def audit_literal_kernels():
    first = literal_kernel(24, 107, [130, 120, 126], [144, 132, 135, 140])
    empty_column = literal_kernel(70, 805, [864, 840, 875], [910, 880, 882, 900])
    assert empty_column[1][1, 2, 0] == ()
    return first[2:], empty_column[2:]


def main():
    grids = audit_confined_grids()
    geometry = audit_geometry()
    covers = audit_rank_case_split()
    layers = audit_layer_certificate()
    literals = audit_literal_kernels()
    print(
        "C11_PLACEMENT_AUDIT=PASS",
        f"grids={grids}",
        f"geometry={geometry}",
        f"cover_profiles={covers}",
        f"layers={layers}",
        f"literals={literals}",
    )
    print("STATUS=PLACEMENT_COMPONENT full_c11_integration=SEPARATE_CANDIDATE")


if __name__ == "__main__":
    main()
