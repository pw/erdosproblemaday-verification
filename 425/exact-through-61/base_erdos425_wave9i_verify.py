#!/usr/bin/env python3
"""
From-scratch verifier for the finite computation in erdos425_wave9i.md.

For A subseteq [n], the Erdős #425 (strict-pair) condition is that a*b is
different for every two-element subset {a,b} of A.  Two different pairs
with the same product cannot share an endpoint, so every obstruction is a
four-element set.  Thus F(n) is the independence number of a 4-uniform
hypergraph, or equivalently n minus its minimum vertex-cover number.

This script:
  1. constructs the obstruction hypergraph on [50] in two independent ways;
  2. proves all upper bounds by a deterministic exhaustive vertex-cover
     search written below (no solver/library dependency);
  3. constructs and directly checks a matching lower-bound witness at the
     beginning of every constant plateau of F(n).

Expected runtime on the exe.dev VM is roughly tens of seconds.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from time import perf_counter
from typing import Iterable


N_MAX = 50

# Claimed exact values, indexed by n-1.
EXPECTED_F = (
    1, 2, 3, 4, 5, 5, 6, 6, 7, 7,
    8, 9, 10, 10, 10, 11, 12, 12, 13, 13,
    13, 14, 15, 15, 16, 16, 16, 16, 17, 17,
    18, 19, 19, 19, 20, 20, 21, 21, 21, 21,
    22, 23, 24, 24, 24, 24, 25, 25, 26, 26,
)


def edges_by_equal_product_pairs(n: int) -> tuple[tuple[int, int, int, int], ...]:
    """Generate obstructions by grouping all strict pairs by their product."""
    representations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            representations[a * b].append((a, b))

    edges: set[tuple[int, int, int, int]] = set()
    for pairs in representations.values():
        for (a, b), (c, d) in combinations(pairs, 2):
            # Cancellation proves this must hold for distinct strict pairs.
            assert len({a, b, c, d}) == 4
            edge = tuple(sorted((a, b, c, d)))
            assert len(edge) == 4
            edges.add(edge)
    return tuple(sorted(edges))


def edges_by_four_subsets(n: int) -> tuple[tuple[int, int, int, int], ...]:
    """
    Independent generator: inspect every four-subset and its three pairings.

    This does not use a product-to-pairs dictionary and therefore catches
    mistakes in the primary generator's grouping/combinations logic.
    """
    edges: list[tuple[int, int, int, int]] = []
    for a, b, c, d in combinations(range(1, n + 1), 4):
        if a * b == c * d or a * c == b * d or a * d == b * c:
            edges.append((a, b, c, d))
    return tuple(edges)


def has_distinct_strict_pair_products(a_set: Iterable[int]) -> bool:
    """Direct witness check, deliberately independent of the hypergraph."""
    seen: set[int] = set()
    values = sorted(a_set)
    for i, a in enumerate(values):
        for b in values[i + 1 :]:
            product = a * b
            if product in seen:
                return False
            seen.add(product)
    return True


def direct_combination_crosscheck(n: int, optimum: int) -> tuple[int, ...]:
    """
    Independent exhaustive check at one manageable point.

    It inspects ordinary combinations and their pair products directly; it
    does not call the hypergraph generator or CoverSearch.
    """
    witness: tuple[int, ...] | None = None
    for candidate in combinations(range(1, n + 1), optimum):
        if has_distinct_strict_pair_products(candidate):
            witness = candidate
            break
    assert witness is not None

    for candidate in combinations(range(1, n + 1), optimum + 1):
        assert not has_distinct_strict_pair_products(candidate)
    return witness


@dataclass(frozen=True)
class SearchStats:
    nodes: int
    memo_states: int
    seconds: float


class CoverSearch:
    """
    Exact decision search for a vertex cover of size at most `budget`.

    State:
      uncovered: bitset of hyperedges not hit by a chosen cover vertex;
      available: vertices neither chosen nor excluded by canonical branching.

    For a selected uncovered edge with ordered available vertices v_1,...,v_t,
    branch i chooses v_i and excludes v_1,...,v_{i-1}.  Every possible cover
    belongs to exactly the branch of its first chosen vertex in that edge.
    Singleton candidate edges are forced.

    Two safe lower bounds prune:
      * ceil(number of uncovered edges / maximum current vertex degree);
      * a greedy family of edges with pairwise disjoint candidate-vertex sets.
    """

    def __init__(
        self,
        n: int,
        edges: tuple[tuple[int, int, int, int], ...],
    ) -> None:
        self.n = n
        self.edges = tuple(edge for edge in edges if edge[-1] <= n)
        self.edge_vertex_masks = tuple(
            sum(1 << (vertex - 1) for vertex in edge) for edge in self.edges
        )
        incidence = [0] * n
        for edge_index, edge in enumerate(self.edges):
            edge_bit = 1 << edge_index
            for vertex in edge:
                incidence[vertex - 1] |= edge_bit
        self.incidence = tuple(incidence)
        self.nodes = 0
        self.memo: dict[tuple[int, int], int] = {}
        self.solution: tuple[int, ...] | None = None

    def run(self, budget: int) -> tuple[tuple[int, ...] | None, SearchStats]:
        start = perf_counter()
        if budget < 0:
            return None, SearchStats(0, 0, perf_counter() - start)
        all_edges = (1 << len(self.edges)) - 1
        all_vertices = (1 << self.n) - 1
        found = self._search(all_edges, all_vertices, budget, ())
        elapsed = perf_counter() - start
        answer = self.solution if found else None
        return answer, SearchStats(self.nodes, len(self.memo), elapsed)

    def _search(
        self,
        uncovered: int,
        available: int,
        budget: int,
        path: tuple[int, ...],
    ) -> bool:
        self.nodes += 1

        # Exhaust all forced singleton candidate edges.
        while uncovered:
            forced_vertices = 0
            work = uncovered
            while work:
                edge_bit = work & -work
                edge_index = edge_bit.bit_length() - 1
                candidates = self.edge_vertex_masks[edge_index] & available
                if candidates == 0:
                    return False
                if candidates & (candidates - 1) == 0:
                    forced_vertices |= candidates
                work -= edge_bit

            if forced_vertices == 0:
                break
            needed = forced_vertices.bit_count()
            if needed > budget:
                return False
            budget -= needed
            work = forced_vertices
            while work:
                vertex_bit = work & -work
                vertex_zero_indexed = vertex_bit.bit_length() - 1
                uncovered &= ~self.incidence[vertex_zero_indexed]
                path += (vertex_zero_indexed + 1,)
                work -= vertex_bit
            available &= ~forced_vertices

        if uncovered == 0:
            self.solution = path
            return True
        if budget <= 0:
            return False

        # Gather current edges/candidate masks once for bounds and branching.
        current: list[tuple[int, int, int]] = []
        max_degree = 0
        work = available
        while work:
            vertex_bit = work & -work
            vertex_zero_indexed = vertex_bit.bit_length() - 1
            max_degree = max(
                max_degree,
                (uncovered & self.incidence[vertex_zero_indexed]).bit_count(),
            )
            work -= vertex_bit

        work = uncovered
        while work:
            edge_bit = work & -work
            edge_index = edge_bit.bit_length() - 1
            candidate_mask = self.edge_vertex_masks[edge_index] & available
            # Zero candidates were already rejected during unit propagation.
            current.append((candidate_mask.bit_count(), edge_index, candidate_mask))
            work -= edge_bit

        degree_bound = (
            uncovered.bit_count() + max_degree - 1
        ) // max_degree

        used_candidates = 0
        disjoint_edge_bound = 0
        for _, _, candidate_mask in sorted(current):
            if candidate_mask & used_candidates == 0:
                disjoint_edge_bound += 1
                used_candidates |= candidate_mask
        if max(degree_bound, disjoint_edge_bound) > budget:
            return False

        key = (uncovered, available)
        if self.memo.get(key, -1) >= budget:
            return False
        # Descendants strictly reduce `uncovered`, so there is no cyclic
        # self-use of this provisional memo entry.
        self.memo[key] = budget

        # Prefer a shortest candidate edge, breaking ties by current degrees.
        best_score: tuple[int, int, int, int, int] | None = None
        best_candidates = 0
        for candidate_count, edge_index, candidate_mask in current:
            degrees: list[int] = []
            work = candidate_mask
            while work:
                vertex_bit = work & -work
                vertex_zero_indexed = vertex_bit.bit_length() - 1
                degrees.append(
                    (
                        uncovered
                        & self.incidence[vertex_zero_indexed]
                    ).bit_count()
                )
                work -= vertex_bit
            score = (
                -candidate_count,
                min(degrees),
                sum(degrees),
                max(degrees),
                -edge_index,
            )
            if best_score is None or score > best_score:
                best_score = score
                best_candidates = candidate_mask

        ordered_candidates: list[tuple[int, int, int]] = []
        work = best_candidates
        while work:
            vertex_bit = work & -work
            vertex_zero_indexed = vertex_bit.bit_length() - 1
            degree = (
                uncovered & self.incidence[vertex_zero_indexed]
            ).bit_count()
            ordered_candidates.append(
                (degree, vertex_zero_indexed, vertex_bit)
            )
            work -= vertex_bit
        ordered_candidates.sort(reverse=True)

        earlier_candidates = 0
        for _, vertex_zero_indexed, vertex_bit in ordered_candidates:
            if self._search(
                uncovered & ~self.incidence[vertex_zero_indexed],
                available & ~(earlier_candidates | vertex_bit),
                budget - 1,
                path + (vertex_zero_indexed + 1,),
            ):
                return True
            earlier_candidates |= vertex_bit
        return False


def plateaus(values: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    """Return inclusive (first_n, last_n, value) constant runs."""
    answer: list[tuple[int, int, int]] = []
    first = 1
    value = values[0]
    for n, next_value in enumerate(values[1:], start=2):
        if next_value != value:
            answer.append((first, n - 1, value))
            first = n
            value = next_value
    answer.append((first, len(values), value))
    return tuple(answer)


def main() -> None:
    start = perf_counter()
    assert len(EXPECTED_F) == N_MAX

    pair_edges = edges_by_equal_product_pairs(N_MAX)
    quadruple_edges = edges_by_four_subsets(N_MAX)
    assert pair_edges == quadruple_edges
    print(
        f"independent edge generators agree: "
        f"|E(H_{N_MAX})|={len(pair_edges)}"
    )
    direct_witness_20 = direct_combination_crosscheck(20, EXPECTED_F[19])
    print(
        "independent direct-combination check: "
        f"F(20)={EXPECTED_F[19]}, witness={direct_witness_20}"
    )

    total_nodes = 0
    lower_witnesses: dict[int, tuple[int, ...]] = {}

    for first_n, last_n, value in plateaus(EXPECTED_F):
        # Lower bound at the start of the plateau: find a cover of size
        # first_n-value and independently check its complement's products.
        lower_search = CoverSearch(first_n, pair_edges)
        cover, lower_stats = lower_search.run(first_n - value)
        assert cover is not None
        assert len(set(cover)) == len(cover) <= first_n - value
        witness = tuple(
            vertex
            for vertex in range(1, first_n + 1)
            if vertex not in set(cover)
        )
        assert len(witness) >= value
        witness = witness[:value]
        assert has_distinct_strict_pair_products(witness)
        lower_witnesses[first_n] = witness

        # Upper bound at the end of the plateau: exhaustively prove there is
        # no cover one smaller than last_n-value.
        upper_budget = last_n - value - 1
        upper_search = CoverSearch(last_n, pair_edges)
        too_small_cover, upper_stats = upper_search.run(upper_budget)
        assert too_small_cover is None
        total_nodes += lower_stats.nodes + upper_stats.nodes

        print(
            f"F(n)={value:2d} for {first_n:2d}<=n<={last_n:2d}: "
            f"witness@{first_n}={witness}; "
            f"upper search@{last_n} budget={upper_budget}, "
            f"nodes={upper_stats.nodes}, "
            f"time={upper_stats.seconds:.3f}s"
        )

    # Expand the plateau proof and verify it reproduces every table entry.
    reconstructed = [None] * N_MAX
    for first_n, last_n, value in plateaus(EXPECTED_F):
        for n in range(first_n, last_n + 1):
            reconstructed[n - 1] = value
    assert tuple(reconstructed) == EXPECTED_F

    # Display and directly validate a convenient terminal witness.
    terminal_witness = lower_witnesses[49]
    # The final plateau starts at n=49 and remains valid at n=50.
    assert len(terminal_witness) == EXPECTED_F[-1]
    assert max(terminal_witness) <= 49 < 50
    assert has_distinct_strict_pair_products(terminal_witness)

    print("F(1..50) =", " ".join(map(str, EXPECTED_F)))
    print(f"terminal size-26 witness in [50]: {terminal_witness}")
    print(f"total recursive nodes (all searches): {total_nodes}")
    print(f"wall time: {perf_counter() - start:.3f}s")
    print("VERIFIED")


if __name__ == "__main__":
    main()
