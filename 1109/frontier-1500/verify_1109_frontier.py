#!/usr/bin/env python3
"""Arbitrary-width Python verifier for the published Problem 1109 frontier."""

from argparse import ArgumentParser
from hashlib import sha256
from math import isqrt

PUBLISHED_TRANSITIONS = (
    1, 5, 19, 23, 37, 41, 59, 87, 101, 105, 113, 131, 151, 159,
    167, 195, 203, 239, 259, 303, 307, 403, 451, 499, 517, 553,
    573, 609, 645, 701, 719, 787, 807, 827, 889, 1003, 1055, 1067,
    1103,
)


def squarefree_table(limit):
    squarefree = bytearray([1]) * (limit + 1)
    squarefree[0] = 0
    for divisor in range(2, isqrt(limit) + 1):
        square = divisor * divisor
        for multiple in range(square, limit + 1, square):
            squarefree[multiple] = 0
    return squarefree


def clique_at_least(adjacency, candidates, target):
    """Decide whether candidates induce a clique of size target."""
    nodes = 0
    witness = None

    def search(pool, chosen):
        nonlocal nodes, witness
        nodes += 1
        chosen_size = len(chosen)
        if chosen_size == target:
            witness = chosen[:]
            return True
        if chosen_size + pool.bit_count() < target:
            return False

        # Greedily partition pool into independent color classes. A clique
        # uses at most one vertex from each class. Prefix color numbers are
        # therefore rigorous upper bounds during the reverse branch scan.
        remaining = pool
        order = []
        color_bound = []
        color = 0
        while remaining:
            color += 1
            available = remaining
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                order.append(vertex)
                color_bound.append(color)
                remaining ^= bit
                available ^= bit
                available &= ~adjacency[vertex]

        for position in range(len(order) - 1, -1, -1):
            if chosen_size + color_bound[position] < target:
                return False
            vertex = order[position]
            bit = 1 << vertex
            if pool & bit:
                if search(pool & adjacency[vertex], chosen + [vertex]):
                    return True
                pool ^= bit
        return False

    exists = search(candidates, [])
    return exists, witness, nodes


def check_witness(values, squarefree):
    assert values == sorted(values)
    assert len(values) == len(set(values))
    for i, left in enumerate(values):
        for right in values[i:]:
            assert squarefree[left + right], (left, right, left + right)


def main():
    parser = ArgumentParser()
    parser.add_argument("max_n", nargs="?", type=int, default=1000)
    args = parser.parse_args()
    max_n = args.max_n
    assert max_n >= PUBLISHED_TRANSITIONS[-1]

    squarefree = squarefree_table(2 * max_n)
    values = []
    adjacency = []
    optimum = 0
    transitions = []
    total_nodes = 0
    decision_records = []

    for n in range(1, max_n + 1):
        if not squarefree[2 * n]:
            continue

        new_index = len(values)
        old_neighbors = 0
        for old_index, old_value in enumerate(values):
            if squarefree[n + old_value]:
                old_neighbors |= 1 << old_index
                adjacency[old_index] |= 1 << new_index
        adjacency.append(old_neighbors)
        values.append(n)

        if optimum == 0:
            optimum = 1
            transitions.append((n, [n], 0))
            continue

        old_optimum = optimum
        exists, indices, nodes = clique_at_least(adjacency, old_neighbors, old_optimum)
        total_nodes += nodes
        decision_records.append(f"{n}:{old_optimum}:{int(exists)}:{nodes}\n")
        if exists:
            optimum += 1
            witness = sorted(values[index] for index in indices) + [n]
            witness.sort()
            check_witness(witness, squarefree)
            transitions.append((n, witness, nodes))

    transition_points = tuple(point for point, _, _ in transitions)
    assert transition_points[:len(PUBLISHED_TRANSITIONS)] == PUBLISHED_TRANSITIONS

    print("Erdos Problem 1109 exact frontier verifier")
    print(f"MAX_N={max_n} eligible_vertices={len(values)} final_f={optimum}")
    print(f"decision_nodes={total_nodes}")
    print("decision_sha256=" + sha256("".join(decision_records).encode("ascii")).hexdigest())
    print("transitions:")
    for size, (point, witness, nodes) in enumerate(transitions, start=1):
        print(
            f"  f={size} first_N={point} decision_nodes={nodes} "
            f"witness={{{','.join(map(str, witness))}}}"
        )
    print("constant_intervals:")
    for index, (point, _, _) in enumerate(transitions):
        end = transitions[index + 1][0] - 1 if index + 1 < optimum else max_n
        print(f"  {point}..{end}: f(N)={index + 1}")
    print(f"CONCLUSION exact f(N) certified for 1<=N<={max_n}")


if __name__ == "__main__":
    main()
