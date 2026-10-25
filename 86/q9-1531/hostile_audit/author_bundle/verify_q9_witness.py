#!/usr/bin/env python3
"""Definition-level verifier for a C4-free subgraph certificate of Q9."""

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def load_edges(path, expected):
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("n") == 9, "metadata n is not 9")
    require(data.get("num_edges") == expected, "metadata edge count mismatch")
    rows = data.get("edges")
    require(isinstance(rows, list) and len(rows) == expected, "wrong edge-row count")

    edges = []
    for position, row in enumerate(rows):
        require(
            isinstance(row, list)
            and len(row) == 2
            and all(isinstance(value, int) for value in row),
            f"malformed edge row {position}",
        )
        u, v = row
        require(0 <= u < 512 and 0 <= v < 512, f"endpoint out of range at row {position}")
        require(u != v, f"loop at row {position}")
        require((u ^ v).bit_count() == 1, f"non-Q9 edge at row {position}")
        edges.append((min(u, v), max(u, v)))
    require(len(set(edges)) == expected, "duplicate edge")
    return tuple(edges)


def verify_faces(edge_set):
    faces = 0
    for first, second in combinations(range(9), 2):
        first_mask = 1 << first
        second_mask = 1 << second
        for base in range(512):
            if base & (first_mask | second_mask):
                continue
            a = base
            b = base | first_mask
            c = base | second_mask
            d = base | first_mask | second_mask
            face = ((a, b), (a, c), (b, d), (c, d))
            require(not all(edge in edge_set for edge in face), f"complete square face {(a,b,d,c)}")
            faces += 1
    require(faces == 4608, f"enumerated {faces} faces")
    return faces


def verify_common_neighbours(edges):
    adjacency = [set() for _ in range(512)]
    degrees_by_direction = Counter()
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        degrees_by_direction[(u ^ v).bit_length() - 1] += 1

    cherries = Counter()
    for center in range(512):
        for u, v in combinations(sorted(adjacency[center]), 2):
            cherries[(u, v)] += 1
    repeated = [pair for pair, count in cherries.items() if count > 1]
    require(not repeated, f"pair has two common neighbours: {repeated[0] if repeated else None}")

    degrees = [len(neighbours) for neighbours in adjacency]
    require(sum(degrees) == 2 * len(edges), "handshake identity failed")
    require(sum(degrees_by_direction.values()) == len(edges), "direction count failed")
    return Counter(degrees), tuple(degrees_by_direction[i] for i in range(9)), len(cherries)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("expected", type=int)
    args = parser.parse_args()

    edges = load_edges(args.file, args.expected)
    edge_set = set(edges)
    faces = verify_faces(edge_set)
    degree_histogram, directions, cherries = verify_common_neighbours(edges)
    digest = hashlib.sha256(args.file.read_bytes()).hexdigest()
    print(
        "Q9_WITNESS=PASS "
        f"edges={len(edges)} vertices=512 faces={faces} c4=0 "
        f"cherries={cherries} repeated_pairs=0"
    )
    print(f"degree_histogram={dict(sorted(degree_histogram.items()))}")
    print(f"direction_counts={directions}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
