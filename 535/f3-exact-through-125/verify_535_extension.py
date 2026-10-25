#!/usr/bin/env python3
"""Dependency-free exact verifier for Problem 535, N=101..125, r=3."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent

# (first N, last N, exact f_3(N), lower witness contained at first N,
#  expected forbidden triples at last N, expected deterministic DFS nodes)
PLATEAUS = [
    (
        101,
        107,
        14,
        (10, 12, 13, 15, 18, 20, 24, 40, 48, 54, 75, 80, 91, 96),
        71799,
        4225121,
    ),
    (
        108,
        124,
        15,
        (11, 14, 20, 24, 30, 33, 36, 40, 48, 80, 90, 96, 98, 99, 108),
        109838,
        11638943,
    ),
    (
        125,
        125,
        16,
        (14, 20, 21, 24, 25, 30, 36, 40, 48, 63, 80, 90, 96, 98, 108, 125),
        113132,
        8579402,
    ),
]

EXPECTED_TABLE_DIGEST = "c4663eebc814f6a00fd78b590cea0aab34e5542f822759ddd339ddf0733df968"


def bad_triple(a: int, b: int, c: int) -> bool:
    return math.gcd(a, b) == math.gcd(a, c) == math.gcd(b, c)


def is_independent(values: tuple[int, ...]) -> bool:
    return not any(bad_triple(*triple) for triple in itertools.combinations(values, 3))


def make_pair_masks(n: int) -> tuple[list[int], list[list[int]], int]:
    triples: list[tuple[int, int, int]] = []
    degree = [0] * n
    for a, b, c in itertools.combinations(range(n), 3):
        if bad_triple(a + 1, b + 1, c + 1):
            triples.append((a, b, c))
            degree[a] += 1
            degree[b] += 1
            degree[c] += 1

    # A static degree order affects speed only, never which subsets exist.
    order = sorted(range(n), key=lambda vertex: (-degree[vertex], vertex))
    position = [0] * n
    for ordered_position, vertex in enumerate(order):
        position[vertex] = ordered_position

    masks = [[0] * n for _ in range(n)]
    for a, b, c in triples:
        i, j, k = position[a], position[b], position[c]
        masks[i][j] |= 1 << k
        masks[j][i] |= 1 << k
        masks[i][k] |= 1 << j
        masks[k][i] |= 1 << j
        masks[j][k] |= 1 << i
        masks[k][j] |= 1 << i
    return order, masks, len(triples)


def find_independent_set(n: int, target: int) -> tuple[tuple[int, ...] | None, int, int]:
    """Exhaustively decide whether an independent target-set exists."""
    order, pair_masks, edge_count = make_pair_masks(n)
    nodes = 0

    def search(
        chosen_positions: tuple[int, ...], candidates: int, still_needed: int
    ) -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        if still_needed == 0:
            return chosen_positions

        # Every subset has one unique increasing sequence in this fixed order.
        # The only prunes are insufficient cardinality and completed bad triples.
        while candidates.bit_count() >= still_needed:
            lowest_bit = candidates & -candidates
            vertex = lowest_bit.bit_length() - 1
            candidates ^= lowest_bit
            next_candidates = candidates
            for old_vertex in chosen_positions:
                next_candidates &= ~pair_masks[old_vertex][vertex]
            answer = search(
                chosen_positions + (vertex,), next_candidates, still_needed - 1
            )
            if answer is not None:
                return answer
        return None

    positions = search((), (1 << n) - 1, target)
    if positions is None:
        return None, nodes, edge_count
    witness = tuple(sorted(order[position] + 1 for position in positions))
    assert len(witness) == target and is_independent(witness)
    return witness, nodes, edge_count


def verify_live_gate() -> None:
    problem = (ROOT / "LIVE_PROBLEM.txt").read_text(encoding="utf-8")
    discussion = (ROOT / "LIVE_DISCUSSION.txt").read_text(encoding="utf-8")
    for marker in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Interested in collaborating\tNone",
        "Currently working on this problem\tNone",
        "I am working on formalising the results on this problem\tNone",
        "Related OEIS sequences: Possible",
        "9 comments on this problem",
    ):
        assert marker in problem, f"live gate marker missing: {marker!r}"
    assert "All comments are the responsibility of the user." in discussion
    assert "0 claimed proofs for this problem" in discussion
    print("live gate: OPEN; zero claims; no worker/collaborator/formalizer")
    print("records gate: live page assigns no OEIS sequence ('Possible')")


def main() -> None:
    verify_live_gate()

    expanded: list[int] = []
    print("range value upper-target edges DFS-nodes result")
    for first, last, value, witness, expected_edges, expected_nodes in PLATEAUS:
        assert len(witness) == value
        assert len(set(witness)) == value
        assert min(witness) >= 1 and max(witness) <= first
        assert is_independent(witness)
        found, nodes, edges = find_independent_set(last, value + 1)
        assert found is None
        assert edges == expected_edges
        assert nodes == expected_nodes
        print(
            f"{first}-{last} {value} {value + 1} {edges} {nodes} UNSAT; "
            f"witness={witness}"
        )
        expanded.extend([value] * (last - first + 1))

    assert len(expanded) == 25
    digest = hashlib.sha256(
        json.dumps(expanded, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    assert digest == EXPECTED_TABLE_DIGEST
    print(f"f3(101..125)={expanded}")
    print(f"sha256(compact JSON table)={digest}")
    print("VERIFIED: exact f_3(N) for every 101 <= N <= 125")


if __name__ == "__main__":
    main()
