#!/usr/bin/env python3
"""Independent hostile verifier for the proposed Q9=1506 C4-free graph."""

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / "candidate_q9_1506.json"
PUBLIC = ROOT / "public_q9_1505.json"
REPRODUCED = ROOT / "reproduced_q9_1506_seed1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(path: Path, expected_edges: int) -> tuple[int, set[tuple[int, int]]]:
    document = json.loads(path.read_text())
    assert document["n"] == 9
    assert document["num_edges"] == expected_edges
    assert isinstance(document["edges"], list)
    assert len(document["edges"]) == expected_edges

    edges = set()
    for index, row in enumerate(document["edges"]):
        assert isinstance(row, list) and len(row) == 2, (index, row)
        u, v = row
        assert type(u) is type(v) is int, (index, row)
        assert 0 <= u < v < 512, (index, row)
        assert (u ^ v).bit_count() == 1, (index, row)
        assert (u, v) not in edges, (index, row)
        edges.add((u, v))
    assert len(edges) == expected_edges
    return document["n"], edges


def audit_graph(label: str, n: int, edges: set[tuple[int, int]]) -> dict[str, object]:
    adjacency = [set() for _ in range(1 << n)]
    direction_counts = Counter()
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        direction_counts[(u ^ v).bit_length() - 1] += 1

    degrees = [len(neighbours) for neighbours in adjacency]
    assert sum(degrees) == 2 * len(edges)
    assert max(degrees) <= n

    # Route 1: enumerate each coordinate square once, using the vertex with
    # both selected coordinate bits cleared as its canonical base.
    square_occupancy = Counter()
    complete_squares = []
    square_count = 0
    for i in range(n):
        bit_i = 1 << i
        for j in range(i + 1, n):
            bit_j = 1 << j
            for base in range(1 << n):
                if base & (bit_i | bit_j):
                    continue
                a = base
                b = base | bit_i
                c = base | bit_j
                d = base | bit_i | bit_j
                boundary = ((a, b), (a, c), (b, d), (c, d))
                occupied = sum(tuple(sorted(edge)) in edges for edge in boundary)
                square_occupancy[occupied] += 1
                square_count += 1
                if occupied == 4:
                    complete_squares.append((a, b, c, d))
    assert square_count == (1 << (n - 2)) * n * (n - 1) // 2 == 4608
    assert not complete_squares

    # Route 2: in any simple graph a 4-cycle exists exactly when some two
    # vertices have at least two distinct common neighbours.  Count each
    # length-two path by its unordered endpoint pair and reject repetition.
    endpoint_pair_center = {}
    cherries = 0
    for center, neighbours in enumerate(adjacency):
        for endpoints in combinations(sorted(neighbours), 2):
            cherries += 1
            if endpoints in endpoint_pair_center:
                previous = endpoint_pair_center[endpoints]
                raise AssertionError(
                    f"{label}: C4 through endpoints={endpoints}, "
                    f"centers={previous},{center}"
                )
            endpoint_pair_center[endpoints] = center
    assert cherries == len(endpoint_pair_center)

    degree_histogram = Counter(degrees)
    print(
        f"GRAPH_PASS label={label} n={n} edges={len(edges)} vertices={1 << n} "
        f"degree_min={min(degrees)} degree_max={max(degrees)} "
        f"degree_sum={sum(degrees)} squares={square_count} complete_squares=0 "
        f"cherries={cherries} repeated_endpoint_pairs=0"
    )
    print(
        f"DIAGNOSTICS label={label} directions="
        + ",".join(f"{i}:{direction_counts[i]}" for i in range(n))
        + " degree_histogram="
        + ",".join(f"{degree}:{degree_histogram[degree]}"
                   for degree in sorted(degree_histogram))
        + " square_occupancy="
        + ",".join(f"{occupied}:{square_occupancy[occupied]}"
                   for occupied in range(5))
    )
    return {
        "adjacency": adjacency,
        "degrees": degrees,
        "directions": direction_counts,
        "square_occupancy": square_occupancy,
        "cherries": cherries,
    }


assert sha256(CANDIDATE) == "883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c"
assert sha256(PUBLIC) == "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338"
assert sha256(REPRODUCED) == "f6995bca4340fd43f343f69bf799d0531028a53a374083876303d9245d41d65d"

candidate_n, candidate_edges = parse(CANDIDATE, 1506)
public_n, public_edges = parse(PUBLIC, 1505)
reproduced_n, reproduced_edges = parse(REPRODUCED, 1506)
candidate_diagnostics = audit_graph("candidate1506", candidate_n, candidate_edges)
public_diagnostics = audit_graph("public1505", public_n, public_edges)
reproduced_diagnostics = audit_graph("reproduced1506", reproduced_n, reproduced_edges)

added = candidate_edges - public_edges
removed = public_edges - candidate_edges
intersection = candidate_edges & public_edges
assert len(candidate_edges) == len(public_edges) + 1
assert len(added) - len(removed) == 1
print(
    f"COMPARISON_PASS public_edges={len(public_edges)} candidate_edges={len(candidate_edges)} "
    f"intersection={len(intersection)} added={len(added)} removed={len(removed)} "
    f"improvement={len(candidate_edges) - len(public_edges)}"
)
assert candidate_edges != reproduced_edges
assert len(candidate_edges & reproduced_edges) == 1325
print(
    "REPRODUCTION_PASS generator_produced_distinct_valid_1506=yes "
    f"candidate_reproduced_intersection={len(candidate_edges & reproduced_edges)}"
)
print("INDEPENDENT_Q9_AUDIT_PASS lower_bound=1506 exactness_claimed=no")
