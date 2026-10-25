#!/usr/bin/env python3
"""Independent finite and small-instance audit of the proposed c_10=2 proof.

This intentionally does not import the frozen checker.  Graph criticality is
tested over every edge submask, graph types are canonicalized from scratch,
and placement is tested on concrete open intervals.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd, lcm
from random import Random


def edge_bit(i: int, j: int, right: int) -> int:
    return 1 << (i * right + j)


def active_counts(mask: int, left: int, right: int) -> tuple[int, int]:
    left_mask = 0
    right_mask = 0
    for i in range(left):
        row = (mask >> (i * right)) & ((1 << right) - 1)
        if row:
            left_mask |= 1 << i
            right_mask |= row
    return left_mask.bit_count(), right_mask.bit_count()


def deficit(mask: int, left: int, right: int) -> int:
    a, b = active_counts(mask, left, right)
    return mask.bit_count() - a - b


def critical_over_all_edge_subsets(mask: int, left: int, right: int, q: int) -> bool:
    if deficit(mask, left, right) != q:
        return False
    sub = (mask - 1) & mask
    while sub:
        if deficit(sub, left, right) >= q:
            return False
        sub = (sub - 1) & mask
    return True


def permute_mask(
    mask: int, left: int, right: int, lp: tuple[int, ...], rp: tuple[int, ...]
) -> int:
    answer = 0
    for i in range(left):
        for j in range(right):
            if mask & edge_bit(i, j, right):
                answer |= edge_bit(lp[i], rp[j], right)
    return answer


@lru_cache(maxsize=None)
def all_permutations(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(permutations(range(n)))


def canonical(mask: int, left: int, right: int) -> int:
    return min(
        permute_mask(mask, left, right, lp, rp)
        for lp in all_permutations(left)
        for rp in all_permutations(right)
    )


def induced_level_masks(mask: int, left: int, right: int) -> tuple[tuple[int, int], ...]:
    levels: set[int] = set()
    for lm in range(1 << left):
        for rm in range(1 << right):
            level = 0
            for i in range(left):
                if not (lm >> i) & 1:
                    continue
                for j in range(right):
                    if (rm >> j) & 1 and mask & edge_bit(i, j, right):
                        level |= edge_bit(i, j, right)
            levels.add(level)
    return tuple((level, max(0, deficit(level, left, right))) for level in levels)


def block_condition(levels: tuple[tuple[int, int], ...], blocks: tuple[int, ...]) -> bool:
    return all(sum((block & level) == block for block in blocks) >= d for level, d in levels)


def masks_of_size(mask: int, size: int) -> list[int]:
    bits = [1 << i for i in range(mask.bit_length()) if mask >> i & 1]
    return [sum(chosen) for chosen in combinations(bits, size)]


def find_q2_blocks(mask: int, left: int, right: int, edge_count: int):
    levels = induced_level_masks(mask, left, right)
    first_size, second_size = (4, 5) if edge_count == 9 else (4, 4)
    first = masks_of_size(mask, first_size)
    second = masks_of_size(mask, second_size)
    for a in first:
        for b in second:
            if a >= b and first_size == second_size:
                continue
            if a & b:
                continue
            if block_condition(levels, (a, b)):
                return a, b
    return None


def find_q3_blocks(mask: int, left: int, right: int):
    levels = induced_level_masks(mask, left, right)
    candidates = masks_of_size(mask, 4)
    for ai, a in enumerate(candidates):
        for bi in range(ai + 1, len(candidates)):
            b = candidates[bi]
            if (a | b).bit_count() < 6:
                continue
            for c in candidates[bi + 1 :]:
                if (a | c).bit_count() < 6 or (b | c).bit_count() < 6:
                    continue
                if (a | b | c).bit_count() < 9:
                    continue
                if block_condition(levels, (a, b, c)):
                    return a, b, c
    return None


def matching_masks(mask: int, left: int, right: int) -> tuple[int, ...]:
    answers = []
    sub = mask
    while True:
        degrees_left = [0] * left
        degrees_right = [0] * right
        for i in range(left):
            for j in range(right):
                if sub & edge_bit(i, j, right):
                    degrees_left[i] += 1
                    degrees_right[j] += 1
        if max(degrees_left + degrees_right, default=0) <= 1:
            answers.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return tuple(answers)


def robust_to_exceptional_matching(
    mask: int,
    left: int,
    right: int,
    exceptional: int,
    blocks: tuple[int, ...],
) -> bool:
    """Check every induced endpoint level and every active anomaly subset."""
    for lm in range(1 << left):
        for rm in range(1 << right):
            induced = 0
            for i in range(left):
                for j in range(right):
                    if (
                        (lm >> i) & 1
                        and (rm >> j) & 1
                        and mask & edge_bit(i, j, right)
                    ):
                        induced |= edge_bit(i, j, right)
            supplied_vertices = sum(active_counts(induced, left, right))
            available_exceptional = exceptional & induced
            deleted = available_exceptional
            while True:
                label_level = induced & ~deleted
                missing = max(0, label_level.bit_count() - supplied_vertices)
                if sum((block & label_level) == block for block in blocks) < missing:
                    return False
                if deleted == 0:
                    break
                deleted = (deleted - 1) & available_exceptional
    return True


def audit_repaired_c9_certificates():
    # Every inclusion-minimal nine-edge/two-defect 3x4 graph, with every
    # possible global exceptional matching.
    graph_matching_pairs = 0
    graphs = 0
    for chosen in combinations(range(12), 9):
        mask = sum(1 << bit for bit in chosen)
        if active_counts(mask, 3, 4) != (3, 4):
            continue
        if not critical_over_all_edge_subsets(mask, 3, 4, 2):
            continue
        blocks = find_q2_blocks(mask, 3, 4, 9)
        assert blocks is not None
        graphs += 1
        for exceptional in matching_masks(mask, 3, 4):
            assert robust_to_exceptional_matching(mask, 3, 4, exceptional, blocks)
            graph_matching_pairs += 1
    assert graphs == 96
    assert graph_matching_pairs == 3888

    # K3,3 needs a pairing chosen for the global exceptional matching.
    k33 = (1 << 9) - 1
    k33_matchings = matching_masks(k33, 3, 3)
    assert len(k33_matchings) == 34
    for exceptional in k33_matchings:
        found = False
        for pairing in permutations(range(3)):
            blocks = tuple(
                sum(
                    edge_bit(i, j, 3)
                    for i in range(3)
                    for j in range(3)
                    if i != omitted_row and j != pairing[omitted_row]
                )
                for omitted_row in range(3)
            )
            if robust_to_exceptional_matching(k33, 3, 3, exceptional, blocks):
                found = True
                break
        assert found, exceptional
    return graphs, graph_matching_pairs, len(k33_matchings)


def valuation(value: int, prime: int) -> int:
    answer = 0
    while value % prime == 0:
        answer += 1
        value //= prime
    return answer


def primes_through(limit: int) -> tuple[int, ...]:
    answers = []
    for candidate in range(2, limit + 1):
        if all(candidate % prime for prime in answers if prime * prime <= candidate):
            answers.append(candidate)
    return tuple(answers)


def corrected_vdlt_edge(a: int, maximum: int, multiplier: int):
    x = multiplier * maximum
    midpoint = x + maximum
    u = (midpoint // a) * a
    if midpoint % a:
        return (u, u + a), "T1"
    if 2 * a < maximum and midpoint % (2 * a):
        return (midpoint - 2 * a, midpoint + 2 * a), "T2"
    return (midpoint - a, midpoint + a), "T3"


def audit_corrected_vdlt_layers(maximum_limit: int = 150):
    instances = 0
    exceptional_levels = 0
    for maximum in range(2, maximum_limit + 1):
        for multiplier in range(6):
            x = multiplier * maximum
            midpoint = x + maximum
            records = {
                a: (*corrected_vdlt_edge(a, maximum, multiplier),)
                for a in range(1, maximum)
            }
            edge_pairs = [record[0] for record in records.values()]
            assert len(set(edge_pairs)) == maximum - 1
            assert all(
                x < left < x + 2 * maximum
                and x < right < x + 2 * maximum
                and midpoint not in (left, right)
                and left % a == right % a == 0
                for a, ((left, right), _) in records.items()
            )
            exceptional_edges = {
                edge
                for a, (edge, kind) in records.items()
                if kind == "T3" and ((midpoint // a) & 1)
            }
            assert all(
                gcd(left, right) // a == (2 if edge in exceptional_edges else 1)
                for a, (edge, _) in records.items()
                for left, right in (edge,)
            )
            assert all(
                2 * a > maximum
                for a, (edge, _) in records.items()
                if edge in exceptional_edges
            )
            t3_edges = {records[a][0] for a in records if records[a][1] == "T3"}
            t3_vertices = [vertex for edge in t3_edges for vertex in edge]
            assert len(t3_vertices) == len(set(t3_vertices))

            all_vertices = set(t3_vertices)
            for (left, right), _ in records.values():
                all_vertices.update((left, right))
            for prime in primes_through(x + 2 * maximum):
                largest = max(valuation(vertex, prime) for vertex in all_vertices)
                for level in range(1, largest + 1):
                    induced = {
                        edge
                        for edge, _ in records.values()
                        if all(valuation(vertex, prime) >= level for vertex in edge)
                    }
                    label_level = {
                        edge
                        for a, (edge, _) in records.items()
                        if valuation(a, prime) >= level
                    }
                    assert label_level <= induced
                    extra = induced - label_level
                    if extra:
                        exceptional_levels += 1
                        assert prime == 2
                        assert extra <= exceptional_edges
                        vertices = [vertex for edge in extra for vertex in edge]
                        assert len(vertices) == len(set(vertices))
                        for a, (edge, kind) in records.items():
                            if edge in extra:
                                assert kind == "T3"
                                assert level == valuation(a, 2) + 1
            instances += 1
    return instances, exceptional_levels


def enumerate_critical_graphs():
    summary: Counter[tuple[int, int, int, int]] = Counter()
    classes: dict[tuple[int, int, int, int], dict[int, int]] = {}
    specifications = [
        (2, 8, 6),
        (2, 9, 7),
        (2, 10, 8),
        (3, 9, 6),
        (3, 10, 7),
    ]
    for q, edges, vertices in specifications:
        for left in range(1, vertices // 2 + 1):
            right = vertices - left
            if left * right < edges:
                continue
            key = (q, edges, left, right)
            orbits: dict[int, int] = {}
            complete = range(left * right)
            for chosen in combinations(complete, edges):
                mask = sum(1 << bit for bit in chosen)
                if active_counts(mask, left, right) != (left, right):
                    continue
                if not critical_over_all_edge_subsets(mask, left, right, q):
                    continue
                summary[key] += 1
                form = canonical(mask, left, right)
                orbits.setdefault(form, mask)
            if orbits:
                classes[key] = orbits

    expected = Counter(
        {
            (2, 8, 2, 4): 1,
            (2, 8, 3, 3): 9,
            (2, 9, 3, 4): 96,
            (2, 10, 3, 5): 210,
            (2, 10, 4, 4): 2040,
            (3, 9, 3, 3): 1,
            (3, 10, 2, 5): 1,
            (3, 10, 3, 4): 54,
        }
    )
    assert summary == expected, (summary, expected)

    expected_orbits = {
        (2, 8, 2, 4): 1,
        (2, 8, 3, 3): 1,
        (2, 9, 3, 4): 2,
        (2, 10, 3, 5): 3,
        # Ten when the two bipartition sides stay oriented; these collapse to
        # the candidate's seven classes when transposition is also allowed.
        (2, 10, 4, 4): 10,
        (3, 9, 3, 3): 1,
        (3, 10, 2, 5): 1,
        (3, 10, 3, 4): 2,
    }
    actual_orbits = {key: len(value) for key, value in classes.items()}
    assert actual_orbits == expected_orbits, (actual_orbits, expected_orbits)

    certificates = {}
    for key, representatives in classes.items():
        q, edges, left, right = key
        for form in representatives:
            if q == 2:
                cert = find_q2_blocks(form, left, right, edges)
                assert cert is not None, key
                certificates[(key, form)] = cert
            elif (left, right) != (2, 5):
                cert = find_q3_blocks(form, left, right)
                assert cert is not None, key
                certificates[(key, form)] = cert
    return summary, classes, certificates


def audit_k25_valuations(cap: int = 5):
    checked = 0
    for values in product(range(cap + 1), repeat=7):
        left = values[:2]
        right = values[2:]
        demand = sum(min(left[i], right[j]) for i in range(2) for j in range(5))
        q = sorted(min(left[0], left[1], right[j]) for j in range(5))
        repair = sum(q[:3])
        assert demand <= sum(values) + repair
        layer_repair = 0
        for level in range(1, max(values, default=0) + 1):
            columns = sum(
                left[0] >= level and left[1] >= level and r >= level for r in right
            )
            layer_repair += max(0, columns - 2)
        assert layer_repair == repair
        checked += 1
    return checked


def interval_multiples(d: int, x2: int, maximum: int) -> set[int]:
    lower_k = x2 // (2 * d) + 1
    upper_k = (x2 + 4 * maximum - 1) // (2 * d)
    return {k * d for k in range(lower_k, upper_k + 1)}


def audit_progression_all_residue_phases(maximum_limit: int = 100):
    checks = 0
    for maximum in range(4, maximum_limit + 1):
        for d in range(1, maximum // 4 + 1):
            for e in range(d + 1, maximum // 4 + 1):
                period = lcm(d, e)
                for shift in range(period):
                    for fractional in (0, 1):
                        x2 = 2 * shift + fractional
                        first = interval_multiples(d, x2, maximum)
                        second = interval_multiples(e, x2, maximum)
                        if len(first) >= 7 and len(second) >= 7:
                            assert len(first | second) >= 10, (
                                maximum,
                                d,
                                e,
                                x2,
                                first,
                                second,
                            )
                        checks += 1
    return checks


def maximum_matching_size(neighborhoods: list[set[int]]) -> int:
    best = 0

    def visit(index: int, used: set[int], matched: int):
        nonlocal best
        if matched + len(neighborhoods) - index <= best:
            return
        if index == len(neighborhoods):
            best = max(best, matched)
            return
        visit(index + 1, used, matched)
        for point in neighborhoods[index] - used:
            used.add(point)
            visit(index + 1, used, matched + 1)
            used.remove(point)

    visit(0, set(), 0)
    return best


def row_column_maps(rows: list[int], columns: set[int], maximum: int):
    """Generate exact-difference columns by divisors, not cubic point scans."""
    answer = {}
    for row in rows:
        choices = {}
        for difference in range(1, maximum + 1):
            if row % difference:
                continue
            for column in (row - difference, row + difference):
                if column in columns:
                    choices[column] = difference
        answer[row] = choices
    return answer


def audit_concrete_k25(maximum_limit: int = 55):
    configurations = 0
    row_pairs = 0
    for maximum in range(10, maximum_limit + 1):
        # Exhaust the nearby integer/noninteger phases and add reproducible
        # larger translations, whose endpoint integers have richer divisors.
        rng = Random(1000 + maximum)
        phases = list(range(0, 4 * maximum))
        phases.extend(2 * rng.randrange(2 * maximum, 200 * maximum) + rng.randrange(2) for _ in range(24))
        for x2 in phases:
            points = [
                n
                for n in range(1, (x2 + 4 * maximum) // 2 + 2)
                if x2 < 2 * n < x2 + 4 * maximum
            ]
            low = [n for n in points if 2 * n <= x2 + 2 * maximum]
            high = [n for n in points if 2 * n > x2 + 2 * maximum]
            for rows_side, columns_side in ((low, high), (high, low)):
                column_set = set(columns_side)
                choices_by_row = row_column_maps(rows_side, column_set, maximum)
                for rows in combinations(rows_side, 2):
                    common = choices_by_row[rows[0]].keys() & choices_by_row[rows[1]].keys()
                    candidates = [
                        (
                            column,
                            (choices_by_row[rows[0]][column], choices_by_row[rows[1]][column]),
                        )
                        for column in common
                    ]
                    if len(candidates) < 5:
                        continue
                    row_pairs += 1
                    # Search all five-column choices, but discard repeated labels early.
                    for chosen in combinations(candidates, 5):
                        labels = [label for _, pair in chosen for label in pair]
                        if len(set(labels)) != 10:
                            continue
                        configurations += 1
                        kernel = set(rows) | {column for column, _ in chosen}
                        q_values = [gcd(*pair) for _, pair in chosen]
                        neighborhoods = [
                            interval_multiples(q, x2, maximum) - kernel for q in q_values
                        ]
                        assert maximum_matching_size(neighborhoods) >= 3, (
                            maximum,
                            x2,
                            rows,
                            chosen,
                            q_values,
                            neighborhoods,
                        )
    return row_pairs, configurations


def prime_vector(value: int, primes: tuple[int, ...], caps: tuple[int, ...]):
    result = []
    for prime, cap in zip(primes, caps):
        exponent = 0
        while value % prime == 0 and exponent < cap:
            exponent += 1
            value //= prime
        result.append(exponent)
    return tuple(result)


def factor_target(values: tuple[int, ...]):
    counts: Counter[int] = Counter()
    for value in values:
        divisor = 2
        while divisor * divisor <= value:
            while value % divisor == 0:
                counts[divisor] += 1
                value //= divisor
            divisor += 1
        if value > 1:
            counts[value] += 1
    primes = tuple(sorted(counts))
    return primes, tuple(counts[p] for p in primes)


def product_cover_exists(
    values: tuple[int, ...], points: tuple[int, ...], limit: int
) -> bool:
    primes, target = factor_target(values)
    zero = (0,) * len(primes)
    states = {zero: 0}
    for point in points:
        vector = prime_vector(point, primes, target)
        updated = dict(states)
        for state, count in states.items():
            if count >= limit:
                continue
            next_state = tuple(min(cap, a + b) for cap, a, b in zip(target, state, vector))
            if next_state == target:
                return True
            if count + 1 < updated.get(next_state, 1 << 30):
                updated[next_state] = count + 1
        states = updated
    return target in states and states[target] <= limit


def audit_actual_small_intervals(samples: int = 500):
    rng = Random(70810)
    checked = 0
    # Include every ten-label set for M <= 12, then seeded larger samples.
    cases = []
    for maximum in range(10, 13):
        for tail in combinations(range(1, maximum), 9):
            cases.append(tail + (maximum,))
    while len(cases) < samples:
        maximum = rng.randrange(13, 31)
        cases.append(tuple(sorted(rng.sample(range(1, maximum), 9))) + (maximum,))
    for values in cases[:samples]:
        maximum = values[-1]
        for _ in range(3):
            shift = rng.randrange(0, 5 * maximum + 1)
            x2 = 2 * shift + rng.randrange(2)
            points = tuple(
                n
                for n in range(1, shift + 2 * maximum + 2)
                if x2 < 2 * n < x2 + 4 * maximum
            )
            assert product_cover_exists(values, points, 10), (values, x2, points)
            checked += 1
        # Explicit aligned endpoint tests, including x=0.
        for multiplier in (0, 1, 3):
            shift = multiplier * maximum
            x2 = 2 * shift
            points = tuple(range(shift + 1, shift + 2 * maximum))
            assert product_cover_exists(values, points, 10)
            without_midpoint = tuple(point for point in points if point != shift + maximum)
            assert product_cover_exists(values[:-1], without_midpoint, 9)
            checked += 1
    return checked


def aligned_reuse_counterexample():
    maximum = 10
    smaller = tuple(range(1, 10))
    midpoint = 10
    cover = (1, 2, 3, 4, 6, 7, 9, 10, 12)
    smaller_product = 1
    cover_product = 1
    for value in smaller:
        smaller_product *= value
    for point in cover:
        cover_product *= point
    target = maximum * smaller_product
    assert cover_product % smaller_product == 0
    assert cover_product % maximum == 0
    assert cover_product % target != 0
    assert cover_product // smaller_product == 3
    residual = target // gcd(target, cover_product)
    assert residual == maximum
    interval = tuple(range(1, 2 * maximum))
    assert [point for point in interval if point % residual == 0] == [midpoint]
    assert all((cover_product * point) % target for point in interval if point not in cover)
    return maximum, smaller, cover, residual


def audit_possible_avoidance_repair(maximum_limit: int = 16):
    """Test, but do not assume, the missing b0-avoiding nine-cover lemma."""
    checked = 0
    for maximum in range(10, maximum_limit + 1):
        for smaller in combinations(range(1, maximum), 9):
            for multiplier in range(6):
                shift = multiplier * maximum
                midpoint = shift + maximum
                points = tuple(
                    point
                    for point in range(shift + 1, shift + 2 * maximum)
                    if point != midpoint
                )
                assert product_cover_exists(smaller, points, 9)
                checked += 1
    return checked


def main():
    summary, classes, certificates = enumerate_critical_graphs()
    repaired_certificates = audit_repaired_c9_certificates()
    corrected_layers = audit_corrected_vdlt_layers()
    valuations = audit_k25_valuations()
    progression = audit_progression_all_residue_phases()
    row_pairs, k25 = audit_concrete_k25()
    intervals = audit_actual_small_intervals()
    reuse_gap = aligned_reuse_counterexample()
    avoidance = audit_possible_avoidance_repair()
    print("critical labelled graphs:", dict(sorted(summary.items())))
    print("critical isomorphism classes:", {k: len(v) for k, v in sorted(classes.items())})
    print("independent block certificates:", len(certificates))
    print("aligned repair graph/matching checks:", repaired_certificates)
    print("corrected vDLT instances/exceptional levels:", corrected_layers)
    print("K2,5 valuation vectors:", valuations)
    print("AP full-residue phase checks:", progression)
    print("concrete K2,5 row pairs/configurations:", row_pairs, k25)
    print("actual c10/c9 small interval instances:", intervals)
    print("aligned reuse counterexample:", reuse_gap)
    print("small b0-avoiding repair instances:", avoidance)
    print("INDEPENDENT_FINITE_CHECKS=PASS; FROZEN_CANDIDATE=GAP; ALIGNED_REPAIR=PASS")


if __name__ == "__main__":
    main()
