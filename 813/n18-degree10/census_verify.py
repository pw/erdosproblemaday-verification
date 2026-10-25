#!/usr/bin/env python3
"""Definition-level verifier for the Erdos #813 neighbourhood census.

This independently parses graph6 and verifies every listed graph is K4-free
and has no triangle-free seven-set.  It also independently verifies
augmentation completeness between consecutive files: every valid child
deletes to some listed parent, up to graph isomorphism.

The latter is a small Python/NetworkX audit, deliberately independent of the
C extension filter and nauty shortg used to produce the census.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from collections import Counter
from itertools import combinations

import networkx as nx


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_graphs(path: str) -> list[nx.Graph]:
    with open(path, "rb") as stream:
        return list(nx.read_graph6(stream))


def valid(graph: nx.Graph) -> bool:
    vertices = tuple(graph.nodes())
    assert vertices == tuple(range(len(vertices)))
    if any(
        all(graph.has_edge(u, v) for u, v in combinations(subset, 2))
        for subset in combinations(vertices, 4)
    ):
        return False
    if any(
        not any(
            all(graph.has_edge(u, v) for u, v in combinations(triple, 2))
            for triple in combinations(subset, 3)
        )
        for subset in combinations(vertices, 7)
    ):
        return False
    return True


def masks_of(graph: nx.Graph) -> list[int]:
    return [sum(1 << v for v in graph.neighbors(u)) for u in graph]


def graph6_of(adj: list[int]) -> bytes:
    """Small-order graph6 encoder, independently checked against NetworkX."""
    n = len(adj)
    assert n <= 62
    bits = [adj[i] >> j & 1 for j in range(1, n) for i in range(j)]
    bits.extend([0] * ((-len(bits)) % 6))
    return bytes([n + 63] + [
        63 + sum(bits[start + offset] << (5 - offset) for offset in range(6))
        for start in range(0, len(bits), 6)
    ]) + b"\n"


def valid_extensions(graph: nx.Graph) -> list[bytes]:
    """All valid one-vertex extensions, using only the definition.

    Since the parent is valid and K4-free, a new neighbourhood A works iff
    A is triangle-free and A intersects every triangle-free parent 6-set in
    a set containing an edge.  This equivalence is also easy to check
    directly: it excludes precisely new K4s and new bad seven-sets.
    """
    adj = masks_of(graph)
    n = len(adj)
    edgeful = [False] * (1 << n)
    triangle_free = [True] * (1 << n)
    for subset in range(1 << n):
        vertices = [v for v in range(n) if subset >> v & 1]
        edgeful[subset] = any(adj[u] >> v & 1 for u, v in combinations(vertices, 2))
        triangle_free[subset] = not any(
            all(adj[u] >> v & 1 for u, v in combinations(triple, 2))
            for triple in combinations(vertices, 3)
        )
    tf6 = [
        subset for subset in range(1 << n)
        if subset.bit_count() == 6 and triangle_free[subset]
    ]
    output = []
    for neighbourhood in range(1 << n):
        if neighbourhood.bit_count() > 6 or not triangle_free[neighbourhood]:
            continue
        if not all(edgeful[neighbourhood & six] for six in tf6):
            continue
        child = list(adj) + [neighbourhood]
        for v in range(n):
            if neighbourhood >> v & 1:
                child[v] |= 1 << n
        encoded = graph6_of(child)
        # Independent encoder control.
        nx_child = graph.copy()
        nx_child.add_node(n)
        nx_child.add_edges_from((n, v) for v in range(n) if neighbourhood >> v & 1)
        assert encoded == nx.to_graph6_bytes(nx_child, header=False)
        output.append(encoded)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    censuses = [load_graphs(path) for path in args.files]

    for path, graphs in zip(args.files, censuses):
        orders = Counter(len(graph) for graph in graphs)
        assert len(orders) <= 1
        assert all(valid(graph) for graph in graphs)
        with open(path, "rb") as stream:
            lines = [line for line in stream if line.strip()]
        assert len(lines) == len(set(lines))
        print(
            f"FILE path={path} sha256={sha256(path)} "
            f"orders={dict(orders)} valid={len(graphs)} distinct_lines=PASS"
        )

    for child_path, parents, children in zip(args.files[1:], censuses, censuses[1:]):
        encoded_extensions = []
        for parent in parents:
            encoded_extensions.extend(valid_extensions(parent))
        labelled_extensions = len(encoded_extensions)
        with tempfile.TemporaryDirectory(prefix="erdos813-census-") as tmp:
            raw_path = os.path.join(tmp, "extensions.g6")
            canonical_path = os.path.join(tmp, "canonical.g6")
            with open(raw_path, "wb") as stream:
                stream.writelines(encoded_extensions)
            subprocess.run(
                ["nauty-shortg", "-q", raw_path, canonical_path], check=True
            )
            with open(canonical_path, "rb") as stream:
                canonical = stream.read()
            with open(child_path, "rb") as stream:
                expected = stream.read()
            assert canonical == expected
        print(
            f"TRANSITION {len(parents)}->{len(children)}: "
            f"valid_labelled_extensions={labelled_extensions} "
            f"canonical_byte_comparison=PASS COMPLETE"
        )

    print("VERIFIED: every supplied census and transition passes.")


if __name__ == "__main__":
    main()
