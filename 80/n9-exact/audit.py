#!/usr/bin/env python3
"""Cold audit of the frozen Problem 80 n=9 computation.

This uses NetworkX's graph6 decoder and direct common-neighbour sets, rather
than the producer's CNF model or the C++ scan's graph6/bitset code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
EXPECTED_FRONTIER = [0, 18, 21, 27, 28, 30, 32, 36]
EXPECTED_G6_SHA256 = "ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9"
EXPECTED_RECORDS = 274668


def stats_from_edges(n, edges):
    edges = {tuple(sorted(e)) for e in edges}
    qs = []
    for u, v in edges:
        qs.append(sum(
            tuple(sorted((u, w))) in edges and tuple(sorted((v, w))) in edges
            for w in range(n) if w not in (u, v)
        ))
    return len(edges), min(qs, default=0), max(qs, default=0)


def check_sat_witness(k, target, producer_output):
    rows = [
        json.loads(line) for line in producer_output.read_text().splitlines()
        if line.startswith("{")
    ]
    row = next(row for row in rows if row["k"] == k and row["target"] == target)
    assert row["sat"] and row["k"] == k and row["target"] == target
    count, least, book = stats_from_edges(9, row["edges"])
    assert count == target and least >= 1 and book <= k
    print(f"SAT witness k={k}: edges={count}, codegree range={least}..{book}: PASS")


def complement_edges(parts):
    h = set()
    for part in parts:
        for i, u in enumerate(part):
            v = part[(i + 1) % len(part)]
            if len(part) == 2 and i == 1:
                continue
            h.add(tuple(sorted((u, v))))
    complete = {tuple(e) for e in __import__("itertools").combinations(range(9), 2)}
    return complete - h


def check_structural_witnesses():
    # k=3: K_{3,3,3}.
    classes = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}]
    e3 = [
        (u, v) for u in range(9) for v in range(u + 1, 9)
        if not any(u in c and v in c for c in classes)
    ]
    # k=4: complement of K2 disjoint union C7.
    e4 = complement_edges([[0, 1], [2, 3, 4, 5, 6, 7, 8]])
    # k=5: complement of K3 disjoint union three K2s.
    e5 = complement_edges([[0, 1, 2], [3, 4], [5, 6], [7, 8]])
    # k=6: complement of four K2s plus one isolated vertex.
    e6 = complement_edges([[0, 1], [2, 3], [4, 5], [6, 7], [8]])
    # The singleton in the helper adds a loop, harmless because the complete
    # simple-edge set contains no loop.
    e7 = list(__import__("itertools").combinations(range(9), 2))
    for k, target, edges in [(3, 27, e3), (4, 28, e4), (5, 30, e5), (6, 32, e6), (7, 36, e7)]:
        count, least, book = stats_from_edges(9, edges)
        assert (count, book) == (target, k)
        assert least >= 1
        print(f"structural witness k={k}: edges={count}, codegree range={least}..{book}: PASS")


def scan_with_networkx(graph6_path):
    raw = graph6_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_G6_SHA256
    lines = raw.splitlines()
    assert len(lines) == EXPECTED_RECORDS
    best = [-1] * 8
    exact = [0] * 8
    admissible = 0
    connected = 0
    connected_best = [-1] * 8
    connected_exact = [0] * 8
    connected_edge_hist = {}
    for line in lines:
        graph = nx.from_graph6_bytes(line)
        assert len(graph) == 9
        if graph.number_of_edges() == 0:
            book = 0
        else:
            q = [len(set(graph[u]) & set(graph[v])) for u, v in graph.edges]
            if min(q) == 0:
                continue
            book = max(q)
        admissible += 1
        exact[book] += 1
        for cap in range(book, 8):
            best[cap] = max(best[cap], graph.number_of_edges())
        if nx.is_connected(graph):
            connected += 1
            connected_exact[book] += 1
            connected_edge_hist[graph.number_of_edges()] = (
                connected_edge_hist.get(graph.number_of_edges(), 0) + 1
            )
            for cap in range(book, 8):
                connected_best[cap] = max(
                    connected_best[cap], graph.number_of_edges()
                )
    assert best == EXPECTED_FRONTIER
    assert exact == [1, 14, 1387, 13466, 25335, 18227, 5775, 1044]
    assert admissible == 65249
    # OEIS A396149 counts the connected members.  Its author's linked N=9
    # edge-count table is a useful independent aggregate cross-check, but it
    # does not tabulate booksize/codegree and hence does not contain M_k(9).
    oeis_hist = {}
    for line in (HERE / "sources/A396149_N9_Edge_Count.txt").read_text().splitlines()[1:]:
        edge_count, frequency = map(int, line.split())
        oeis_hist[edge_count] = frequency
    assert connected == 62286
    assert connected_edge_hist == oeis_hist
    assert connected_best == [-1] + EXPECTED_FRONTIER[1:]
    print(f"NetworkX full scan: records={len(lines)}, admissible={admissible}: PASS")
    print(f"connected={connected}, OEIS_A396149_N9_edge_histogram: PASS")
    print("frontier=" + ",".join(map(str, best)))
    print("exact_book_counts=" + ",".join(map(str, exact)))
    print("connected_exact_book_counts=" + ",".join(map(str, connected_exact)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, default=HERE / "all_n9.g6")
    parser.add_argument("--producer-output", type=Path, default=HERE / "producer.out")
    args = parser.parse_args()
    check_sat_witness(1, 18, args.producer_output)
    check_sat_witness(2, 21, args.producer_output)
    check_structural_witnesses()
    scan_with_networkx(args.graph6)
    print("FINAL AUDIT: PASS")


if __name__ == "__main__":
    main()
