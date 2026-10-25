#!/usr/bin/env python3
"""Independent finite stress tests for the candidate proof that c_9 = 2."""

from collections import Counter
from itertools import combinations, product
from math import gcd, isqrt
from random import Random


def active_count(edges):
    return len({i for i, _ in edges}) + len({j for _, j in edges})


def induced(edges, left, right):
    return {e for e in edges if e[0] in left and e[1] in right}


def has_eight_edge_six_vertex_core(edges):
    return any(active_count(set(core)) == 6 for core in combinations(edges, 8))


def partition_repairs_every_induced_level(edges, part4, left_count, right_count):
    part5 = edges - part4
    for left_mask in range(1 << left_count):
        left = {i for i in range(left_count) if left_mask >> i & 1}
        for right_mask in range(1 << right_count):
            right = {j for j in range(right_count) if right_mask >> j & 1}
            level = induced(edges, left, right)
            deficit = max(0, len(level) - active_count(level))
            supported = int(part4 <= level) + int(part5 <= level)
            if supported < deficit:
                return False
    return True


def discover_seven_vertex_repairs():
    counts = Counter()
    valid_partition_counts = []
    for left_count, right_count in ((2, 5), (3, 4)):
        complete = [(i, j) for i in range(left_count) for j in range(right_count)]
        for chosen in combinations(complete, 9):
            edges = set(chosen)
            if active_count(edges) != 7:
                continue
            if has_eight_edge_six_vertex_core(edges):
                counts[left_count, right_count, "core"] += 1
                continue

            assert (left_count, right_count) == (3, 4)
            right_degrees = [sum(j == col for _, j in edges) for col in range(4)]
            assert sorted(right_degrees) == [2, 2, 2, 3]
            full = right_degrees.index(3)
            missing = [
                next(i for i in range(3) if (i, col) not in edges)
                for col in range(4)
                if col != full
            ]
            kind = "balanced" if sorted(Counter(missing).values()) == [1, 1, 1] else "unbalanced"

            repairs = []
            for chosen_part in combinations(edges, 4):
                part4 = set(chosen_part)
                if partition_repairs_every_induced_level(
                    edges, part4, left_count, right_count
                ):
                    repairs.append(part4)
            assert repairs
            counts[left_count, right_count, kind] += 1
            valid_partition_counts.append(len(repairs))

    assert counts == Counter(
        {
            (2, 5, "core"): 10,
            (3, 4, "core"): 120,
            (3, 4, "balanced"): 24,
            (3, 4, "unbalanced"): 72,
        }
    )
    return counts, min(valid_partition_counts), max(valid_partition_counts)


def audit_k33_valuations(cap=6):
    edges = {(i, j) for i in range(3) for j in range(3)}
    blocks = [
        {(i, j) for i in range(3) for j in range(3) if i != slot and j != slot}
        for slot in range(3)
    ]
    checked = 0
    for values in product(range(cap + 1), repeat=6):
        left_values, right_values = values[:3], values[3:]
        edge_values = {(i, j): min(left_values[i], right_values[j]) for i, j in edges}
        repairs = [0, 0, 0]
        for level_number in range(1, cap + 1):
            left = {i for i, value in enumerate(left_values) if value >= level_number}
            right = {j for j, value in enumerate(right_values) if value >= level_number}
            level = induced(edges, left, right)
            deficit = max(0, len(level) - active_count(level))
            if deficit == 3:
                assert len(left) == len(right) == 3
                repairs = [value + 1 for value in repairs]
            elif deficit == 1:
                if len(left) == 2:
                    missing = next(iter({0, 1, 2} - left))
                else:
                    assert len(right) == 2
                    missing = next(iter({0, 1, 2} - right))
                repairs[missing] += 1
            else:
                assert deficit == 0

        edge_demand = sum(edge_values.values())
        endpoint_supply = sum(values)
        assert edge_demand <= endpoint_supply + sum(repairs)
        for slot, block in enumerate(blocks):
            assert repairs[slot] <= min(edge_values[edge] for edge in block)
        checked += 1
    return checked


def prime_factors(n):
    factors = Counter()
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] += 1
            n //= divisor
        divisor += 1
    if n > 1:
        factors[n] += 1
    return factors


def valuation(n, prime, cap):
    answer = 0
    while answer < cap and n % prime == 0:
        answer += 1
        n //= prime
    return answer


def minimum_cover(vectors, target, cutoff=None):
    classes = Counter(vector for vector in vectors if any(vector))
    zero = (0,) * len(target)
    best = {zero: 0}
    maximum_useful = sum(target)
    for vector, multiplicity in classes.items():
        updated = dict(best)
        for state, cost in best.items():
            limit = min(multiplicity, maximum_useful)
            if cutoff is not None:
                limit = min(limit, cutoff - cost)
            current = state
            for take in range(1, limit + 1):
                current = tuple(
                    min(goal, have + take * gain)
                    for goal, have, gain in zip(target, state, vector)
                )
                new_cost = cost + take
                if new_cost < updated.get(current, 10**9):
                    updated[current] = new_cost
        best = updated
    return best.get(tuple(target))


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for divisor in range(3, isqrt(n) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def next_prime(n):
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def chinese_remainder(moduli, residues):
    modulus = 1
    for value in moduli:
        assert gcd(modulus, value) == 1
        modulus *= value
    answer = 0
    for value, residue in zip(moduli, residues):
        complement = modulus // value
        answer += residue * complement * pow(complement, -1, value)
    return answer % modulus


def audit_padded_nine_instance():
    u, v, w, padding = 101, 103, 107, 5
    qs = []
    candidate = u * v + padding
    while len(qs) < padding:
        candidate = next_prime(candidate)
        assert candidate < v * w
        qs.append(candidate)

    moduli = [u * w, v * v] + qs
    residues = [
        1,
        (v + 1) * pow(u * w, -1, v * v) % (v * v),
    ] + [
        (index + 1) * pow(u * v * w, -1, prime) % prime
        for index, prime in enumerate(qs)
    ]
    t = chinese_remainder(moduli, residues)
    x = t * u * v * w
    lo, hi = x - u * v + 1, x + u * v - 1
    points = list(range(lo, hi + 1))

    core_primes = (u, v, w)
    assert [y for y in points if y % (u * v) == 0] == [x]
    assert [y for y in points if y % (u * w) == 0] == [x]
    assert [y for y in points if y % (v * w) == 0] == [x]
    assert [y for y in points if y % (v * v) == 0] == [x - v]
    assert not [y for y in points if y % (v**3) == 0]
    assert all(
        sum(y % prime == 0 for prime in core_primes) <= 1
        for y in points
        if y != x
    )
    for index, prime in enumerate(qs, start=1):
        assert [y for y in points if y % prime == 0] == [x - index]
        assert all((x - index) % core_prime for core_prime in core_primes)

    primes = core_primes + tuple(qs)
    target = (2, 4, 2) + (1,) * padding
    vectors = [
        tuple(valuation(point, prime, goal) for prime, goal in zip(primes, target))
        for point in points
    ]
    full_minimum = minimum_cover(vectors, target)
    core_minimum = minimum_cover([vector[:3] for vector in vectors], target[:3])
    assert core_minimum == 5
    assert full_minimum == 10
    return qs, len(points), v * w, core_minimum, full_minimum


def interval_points(maximum, doubled_left_endpoint):
    return [
        value
        for value in range(1, (doubled_left_endpoint + 4 * maximum) // 2 + 2)
        if doubled_left_endpoint < 2 * value < doubled_left_endpoint + 4 * maximum
    ]


def actual_instance_minimum(moduli, doubled_left_endpoint):
    maximum = max(moduli)
    target_factors = Counter()
    for modulus in moduli:
        target_factors.update(prime_factors(modulus))
    primes = tuple(sorted(target_factors))
    target = tuple(target_factors[prime] for prime in primes)
    points = interval_points(maximum, doubled_left_endpoint)
    vectors = [
        tuple(valuation(point, prime, goal) for prime, goal in zip(primes, target))
        for point in points
    ]
    return minimum_cover(vectors, target, cutoff=9), len(points)


def audit_actual_instances():
    checked = 0
    worst = 0
    for maximum in range(9, 12):
        for prefix in combinations(range(1, maximum), 8):
            moduli = prefix + (maximum,)
            for doubled_left in range(4 * maximum + 1):
                minimum, point_count = actual_instance_minimum(moduli, doubled_left)
                assert point_count >= 9 and minimum is not None and minimum <= 9
                checked += 1
                worst = max(worst, minimum)

    random = Random(70809)
    for _ in range(300):
        maximum = random.randrange(12, 51)
        moduli = tuple(sorted(random.sample(range(1, maximum), 8) + [maximum]))
        doubled_left = random.randrange(8 * maximum + 1)
        minimum, point_count = actual_instance_minimum(moduli, doubled_left)
        assert point_count >= 9 and minimum is not None and minimum <= 9
        checked += 1
        worst = max(worst, minimum)
    return checked, worst


def main():
    graph_counts, minimum_partitions, maximum_partitions = discover_seven_vertex_repairs()
    valuation_vectors = audit_k33_valuations()
    lower = audit_padded_nine_instance()
    actual_count, actual_worst = audit_actual_instances()
    print("seven_vertex_graphs", dict(graph_counts))
    print("discovered_partition_count_range", minimum_partitions, maximum_partitions)
    print("k33_valuation_vectors", valuation_vectors)
    print("n9_padding", lower)
    print("literal_instances", actual_count, "worst_minimum", actual_worst)
    print("COLD C9 AUDIT PASSED")


if __name__ == "__main__":
    main()
