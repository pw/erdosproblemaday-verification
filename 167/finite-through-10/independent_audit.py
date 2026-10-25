#!/usr/bin/env python3
"""Independent audit for the finite Erdos 167 census.

This deliberately does not parse graph6 or use the constructive algorithm from
verify_167.cpp.  NetworkX parses graph6.  Two memoized definition-level searches
compute the exact triangle-packing number nu and exact triangle edge-cover number
tau for every connected unlabeled graph through the requested order (default 8).
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import subprocess

import networkx as nx


def triangle_hypergraph(g: nx.Graph):
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    edge_id = {e: i for i, e in enumerate(edges)}
    triangles = []
    for a, b, c in itertools.combinations(sorted(g.nodes()), 3):
        if g.has_edge(a, b) and g.has_edge(a, c) and g.has_edge(b, c):
            triangles.append(
                (1 << edge_id[(a, b)])
                | (1 << edge_id[(a, c)])
                | (1 << edge_id[(b, c)])
            )
    return edges, triangles


def exact_values(g: nx.Graph):
    edges, triangles = triangle_hypergraph(g)
    t = len(triangles)
    if not t:
        return 0, 0

    all_triangles = (1 << t) - 1
    incident = [0] * len(edges)
    conflicts = [0] * t
    for i, tri in enumerate(triangles):
        for e in range(len(edges)):
            if tri >> e & 1:
                incident[e] |= 1 << i
    for i, tri in enumerate(triangles):
        for e in range(len(edges)):
            if tri >> e & 1:
                conflicts[i] |= incident[e]

    @functools.cache
    def packing(remaining: int) -> int:
        if not remaining:
            return 0
        # Partition all packings according to their use of a high-incidence edge.
        active_edges = [
            ((remaining & incident[e]).bit_count(), e)
            for e in range(len(edges))
            if remaining & incident[e]
        ]
        _, e = max(active_edges)
        best = packing(remaining & ~incident[e])  # no chosen triangle uses e
        candidates = remaining & incident[e]
        while candidates:
            bit = candidates & -candidates
            i = bit.bit_length() - 1
            best = max(best, 1 + packing(remaining & ~conflicts[i]))
            candidates ^= bit
        return best

    @functools.cache
    def cover(remaining: int) -> int:
        if not remaining:
            return 0
        # Every cover must choose one of the three graph edges in this triangle.
        bit = remaining & -remaining
        i = bit.bit_length() - 1
        opts = []
        tri = triangles[i]
        while tri:
            ebit = tri & -tri
            e = ebit.bit_length() - 1
            opts.append(1 + cover(remaining & ~incident[e]))
            tri ^= ebit
        return min(opts)

    return packing(all_triangles), cover(all_triangles)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=1)
    ap.add_argument("--max-n", type=int, default=8)
    args = ap.parse_args()
    assert 1 <= args.min_n <= args.max_n <= 9, "the independent exact audit is intentionally capped at 9"

    grand = 0
    for n in range(args.min_n, args.max_n + 1):
        proc = subprocess.Popen(
            ["/bin/nauty-geng", "-cq", str(n)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        assert proc.stdout is not None
        count = nontrivial = equality = 0
        digest = hashlib.sha256()
        for raw in proc.stdout:
            raw = raw.strip()
            if not raw:
                continue
            digest.update(raw + b"\n")
            g = nx.from_graph6_bytes(raw)
            assert len(g) == n and nx.is_connected(g)
            nu, tau = exact_values(g)
            assert tau <= 2 * nu, (n, raw.decode(), nu, tau)
            count += 1
            nontrivial += bool(nu)
            equality += bool(nu and tau == 2 * nu)
        assert proc.wait() == 0
        grand += count
        print(
            f"n={n} graphs={count} triangle_graphs={nontrivial} "
            f"exact_tau_eq_2nu={equality} sha256={digest.hexdigest()}"
        )
    print(f"PASS exact independent census through n={args.max_n}; total_connected={grand}")


if __name__ == "__main__":
    main()
