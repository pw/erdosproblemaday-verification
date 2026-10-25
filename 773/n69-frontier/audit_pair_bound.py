#!/usr/bin/env python3
"""Independent semantic audit of the DFS pair-conflict upper bound."""

from __future__ import annotations

import hashlib
import itertools
import random
from collections import defaultdict
from pathlib import Path


N = 69
BFILE = Path("oeis_A390813_b390813.txt")
BFILE_SHA256 = "dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916"


def collision_supports() -> list[frozenset[int]]:
    representations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for first in range(1, N + 1):
        for second in range(first, N + 1):
            representations[first * first + second * second].append((first, second))
    supports: set[frozenset[int]] = set()
    for pairs in representations.values():
        for first, second in itertools.combinations(pairs, 2):
            supports.add(frozenset((*first, *second)))
    return sorted(supports, key=lambda edge: (len(edge), sorted(edge)))


def is_sidon(vertices: set[int]) -> bool:
    sums: set[int] = set()
    ordered = sorted(vertices)
    for position, first in enumerate(ordered):
        for second in ordered[position:]:
            value = first * first + second * second
            if value in sums:
                return False
            sums.add(value)
    return True


def greedy_clique_cover(vertices: set[int], neighbors: dict[int, set[int]]) -> list[set[int]]:
    remaining = set(vertices)
    cover: list[set[int]] = []
    while remaining:
        seed = max(remaining, key=lambda vertex: (len(neighbors[vertex] & remaining), -vertex))
        remaining.remove(seed)
        clique = {seed}
        candidates = remaining & neighbors[seed]
        while candidates:
            vertex = max(
                candidates,
                key=lambda item: (len(neighbors[item] & candidates), -item),
            )
            remaining.remove(vertex)
            clique.add(vertex)
            candidates.remove(vertex)
            candidates.intersection_update(neighbors[vertex])
        cover.append(clique)
    return cover


def exact_independence_number(vertices: list[int], neighbors: dict[int, set[int]]) -> int:
    neighbor_masks = []
    for vertex in vertices:
        mask = 0
        for index, other in enumerate(vertices):
            if other in neighbors[vertex]:
                mask |= 1 << index
        neighbor_masks.append(mask)
    memo: dict[int, int] = {0: 0}

    def solve(mask: int) -> int:
        if mask in memo:
            return memo[mask]
        index = mask.bit_length() - 1
        without_vertex = mask & ~(1 << index)
        result = max(
            solve(without_vertex),
            1 + solve(without_vertex & ~neighbor_masks[index]),
        )
        memo[mask] = result
        return result

    return solve((1 << len(vertices)) - 1)


def main() -> None:
    digest = hashlib.sha256(BFILE.read_bytes()).hexdigest()
    assert digest == BFILE_SHA256, digest
    supports = collision_supports()
    assert len(supports) == 712
    assert sum(len(edge) == 3 for edge in supports) == 21
    assert sum(len(edge) == 4 for edge in supports) == 691

    rng = random.Random(773_069)
    audited_states = 0
    exact_graphs = 0
    for state_index in range(200):
        k = rng.randrange(12, 66)
        selected = {N}
        for vertex in range(N - 1, k, -1):
            if rng.random() < 0.48 and is_sidon(selected | {vertex}):
                selected.add(vertex)
        excluded = set(range(k + 1, N + 1)) - selected

        blocked: set[int] = set()
        neighbors = {vertex: set() for vertex in range(1, k + 1)}
        for edge in supports:
            if edge & excluded:
                continue
            remaining = edge - selected
            if len(remaining) == 1:
                (vertex,) = remaining
                if vertex <= k:
                    blocked.add(vertex)
            elif len(remaining) == 2:
                first, second = remaining
                if first <= k and second <= k:
                    neighbors[first].add(second)
                    neighbors[second].add(first)

        viable = set(range(1, k + 1)) - blocked
        for vertex in range(1, k + 1):
            assert (not is_sidon(selected | {vertex})) == (vertex in blocked)
        for first, second in itertools.combinations(sorted(viable), 2):
            direct_conflict = not is_sidon(selected | {first, second})
            graph_conflict = second in neighbors[first]
            assert direct_conflict == graph_conflict, (
                k,
                sorted(selected),
                first,
                second,
                direct_conflict,
                graph_conflict,
            )

        cover = greedy_clique_cover(viable, neighbors)
        assert set().union(*cover) == viable if cover else not viable
        assert sum(map(len, cover)) == len(viable)
        for clique in cover:
            assert all(second in neighbors[first] for first, second in itertools.combinations(clique, 2))

        if state_index < 60:
            if len(viable) >= 16:
                sample = sorted(rng.sample(sorted(viable), 16))
            else:
                sample = sorted(viable)
            sample_cover = greedy_clique_cover(set(sample), neighbors)
            alpha = exact_independence_number(sample, neighbors)
            assert alpha <= len(sample_cover)
            exact_graphs += 1
        audited_states += 1

    print(f"PASS bfile_sha256={digest}")
    print(f"PASS supports={len(supports)} triples=21 quadruples=691")
    print(f"PASS random_states={audited_states} direct_pair_graph_equivalence")
    print(f"PASS exact_independence_graphs={exact_graphs} clique_cover_upper_bound")


if __name__ == "__main__":
    main()
