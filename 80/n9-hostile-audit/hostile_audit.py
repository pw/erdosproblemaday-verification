#!/usr/bin/env python3
"""Independent hostile audit for the frozen Problem 80 order-nine bundle.

This deliberately does not import the producer, its NetworkX audit, or its
C++ scanner.  It regenerates nauty's complete order-nine stream and evaluates
the graph property with a small independent graph6/bit-mask implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


EXPECTED_MANIFEST_SHA256 = (
    "81bb81f74221296c626f613fb023f7e4cea050dad3293a08e37f865713f3ac74"
)
EXPECTED_G6_SHA256 = (
    "ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9"
)
EXPECTED_CLAIMS_SHA256 = (
    "da127236a4419ec178b4c6d72334d6335a8e352ba63b37d0224afc232ae943b5"
)
EXPECTED_FRONTIER = [0, 18, 21, 27, 28, 30, 32, 36]
EXPECTED_EXACT = [1, 14, 1387, 13466, 25335, 18227, 5775, 1044]
EXPECTED_CONNECTED_EXACT = [0, 6, 1143, 12543, 24224, 17707, 5619, 1044]
EXPECTED_RECORDS = 274_668
EXPECTED_ADMISSIBLE = 65_249
EXPECTED_CONNECTED = 62_286


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_manifest(source: Path) -> None:
    manifest = source / "SHA256SUMS"
    assert sha256(manifest) == EXPECTED_MANIFEST_SHA256
    listed: set[Path] = set()
    for raw in manifest.read_text().splitlines():
        expected, relative = raw.split("  ", 1)
        assert relative.startswith("./")
        path = (source / relative[2:]).resolve()
        path.relative_to(source.resolve())
        assert path.is_file()
        assert sha256(path) == expected
        listed.add(path)
    actual = {p.resolve() for p in source.rglob("*") if p.is_file() and p != manifest}
    assert listed == actual
    print(f"manifest_sha256={EXPECTED_MANIFEST_SHA256} files={len(listed)}: PASS")


def decode_graph6(line: bytes) -> list[int]:
    # A short graph6 record for n=9 consists of H plus 36 adjacency bits.
    assert len(line) == 7 and line[0] - 63 == 9
    assert all(63 <= value <= 126 for value in line)
    adjacency = [0] * 9
    bit_index = 0
    for v in range(1, 9):
        for u in range(v):
            value = line[1 + bit_index // 6] - 63
            present = (value >> (5 - bit_index % 6)) & 1
            if present:
                adjacency[u] |= 1 << v
                adjacency[v] |= 1 << u
            bit_index += 1
    assert bit_index == 36
    return adjacency


def connected(adjacency: list[int]) -> bool:
    seen = 1
    stack = 1
    while stack:
        lowbit = stack & -stack
        stack ^= lowbit
        vertex = lowbit.bit_length() - 1
        new = adjacency[vertex] & ~seen
        seen |= new
        stack |= new
    return seen == (1 << 9) - 1


def graph_stats(adjacency: list[int]) -> tuple[int, int, int] | None:
    edges = sum(mask.bit_count() for mask in adjacency) // 2
    least = 8
    book = 0
    for u in range(9):
        later = adjacency[u] & ~((1 << (u + 1)) - 1)
        while later:
            lowbit = later & -later
            later ^= lowbit
            v = lowbit.bit_length() - 1
            codegree = (adjacency[u] & adjacency[v]).bit_count()
            if codegree == 0:
                return None
            least = min(least, codegree)
            book = max(book, codegree)
    if edges == 0:
        least = 0
    return edges, least, book


def read_oeis_histogram(source: Path) -> dict[int, int]:
    histogram: dict[int, int] = {}
    lines = (source / "sources/A396149_N9_Edge_Count.txt").read_text().splitlines()
    assert lines[0] == "--- Edge_Count ---"
    for line in lines[1:]:
        edges, frequency = map(int, line.split())
        histogram[edges] = frequency
    return histogram


def scan(stream: Path, oeis_histogram: dict[int, int]) -> None:
    frontier = [-1] * 8
    exact = [0] * 8
    connected_exact = [0] * 8
    connected_histogram: Counter[int] = Counter()
    records = admissible = connected_count = 0

    with stream.open("rb") as handle:
        for raw in handle:
            line = raw.rstrip(b"\r\n")
            assert line
            records += 1
            adjacency = decode_graph6(line)
            stats = graph_stats(adjacency)
            if stats is None:
                continue
            edges, _least, book = stats
            admissible += 1
            exact[book] += 1
            for cap in range(book, 8):
                frontier[cap] = max(frontier[cap], edges)
            if connected(adjacency):
                connected_count += 1
                connected_exact[book] += 1
                connected_histogram[edges] += 1

    assert records == EXPECTED_RECORDS
    assert admissible == EXPECTED_ADMISSIBLE
    assert frontier == EXPECTED_FRONTIER
    assert exact == EXPECTED_EXACT
    assert connected_count == EXPECTED_CONNECTED
    assert connected_exact == EXPECTED_CONNECTED_EXACT
    assert dict(connected_histogram) == oeis_histogram
    print(f"fresh_nauty_records={records} admissible={admissible}: PASS")
    print("frontier=" + ",".join(map(str, frontier)))
    print("exact_book_counts=" + ",".join(map(str, exact)))
    print(f"connected={connected_count} OEIS_edge_histogram: PASS")


def adjacency_from_edges(edges: list[list[int]] | list[tuple[int, int]]) -> list[int]:
    adjacency = [0] * 9
    for u, v in edges:
        assert 0 <= u < v < 9
        assert not (adjacency[u] >> v) & 1
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return adjacency


def complement_edges(missing: set[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        (u, v)
        for v in range(1, 9)
        for u in range(v)
        if (u, v) not in missing
    ]


def cycle_edges(vertices: list[int]) -> set[tuple[int, int]]:
    result = set()
    for i, u in enumerate(vertices):
        v = vertices[(i + 1) % len(vertices)]
        result.add(tuple(sorted((u, v))))
    return result


def audit_producer_and_witnesses(source: Path) -> None:
    rows = [
        json.loads(line)
        for line in (source / "producer.out").read_text().splitlines()
        if line.startswith("{")
    ]
    assert [(row["k"], row["target"], row["sat"]) for row in rows] == [
        (1, 18, True),
        (1, 19, False),
        (2, 21, True),
        (2, 22, False),
    ]
    claims = [
        {
            key: row[key]
            for key in (
                "n",
                "k",
                "target",
                "sat",
                "edges",
                "edge_count",
                "booksize",
                "codegrees",
            )
        }
        for row in rows
    ]
    payload = json.dumps(claims, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_CLAIMS_SHA256

    # Directly verify both frozen SAT witnesses from edge lists.
    for row in rows:
        if not row["sat"]:
            continue
        stats = graph_stats(adjacency_from_edges(row["edges"]))
        assert stats is not None
        edges, least, book = stats
        assert edges == row["target"] == row["edge_count"]
        assert 1 <= least <= book <= row["k"]

    rook = [
        (3 * r + c, 3 * rr + cc)
        for r in range(3)
        for c in range(3)
        for rr in range(3)
        for cc in range(3)
        if 3 * r + c < 3 * rr + cc and (r == rr or c == cc)
    ]
    tripartite = [
        (u, v)
        for v in range(1, 9)
        for u in range(v)
        if u // 3 != v // 3
    ]
    h4 = {(0, 1)} | cycle_edges([2, 3, 4, 5, 6, 7, 8])
    h5 = cycle_edges([0, 1, 2]) | {(3, 4), (5, 6), (7, 8)}
    h6 = {(0, 1), (2, 3), (4, 5), (6, 7)}
    complete = [(u, v) for v in range(1, 9) for u in range(v)]
    constructions = [
        (1, 18, rook),
        (2, 21, next(row["edges"] for row in rows if row["k"] == 2 and row["sat"])),
        (3, 27, tripartite),
        (4, 28, complement_edges(h4)),
        (5, 30, complement_edges(h5)),
        (6, 32, complement_edges(h6)),
        (7, 36, complete),
    ]
    for cap, target, edges in constructions:
        stats = graph_stats(adjacency_from_edges(edges))
        assert stats is not None and stats[0] == target and stats[2] <= cap
    print(f"claims_sha256={EXPECTED_CLAIMS_SHA256}: PASS")
    print("seven_nonempty_constructions: PASS")


def euler_transform_at_nine(connected_counts: list[int]) -> int:
    all_counts = [0] * 10
    all_counts[0] = 1
    for n in range(1, 10):
        total = 0
        for k in range(1, n + 1):
            divisor_sum = sum(
                d * connected_counts[d] for d in range(1, k + 1) if k % d == 0
            )
            total += divisor_sum * all_counts[n - k]
        assert total % n == 0
        all_counts[n] = total // n
    return all_counts[9]


def audit_sources(source: Path) -> None:
    page = (source / "sources/live_page_20260812.txt").read_text()
    for marker in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Interested in collaborating\tNone",
        "Currently working on this problem\tNone",
        "I am working on formalising the results on this problem\tNone",
        "Formalised statement? Yes",
    ):
        assert marker in page

    oeis = json.loads((source / "sources/OEIS_A396149.json").read_text())[0]
    assert oeis["number"] == 396149
    assert oeis["name"] == (
        "Number of connected graphs on n vertices where every edge is part of at least one triangle."
    )
    values = list(map(int, oeis["data"].split(",")))
    assert values[9] == EXPECTED_CONNECTED
    assert euler_transform_at_nine(values[:10]) == EXPECTED_ADMISSIBLE
    for name in (
        "OEIS_search_booksize.json",
        "OEIS_search_locally_linear.json",
        "OEIS_search_old_frontier.json",
    ):
        assert json.loads((source / "sources" / name).read_text()) is None
    broad = json.loads((source / "sources/OEIS_search_every_edge_triangle.json").read_text())
    assert {396149, 396364} <= {row["number"] for row in broad}
    print("live_gate_capture=OPEN/0/no-worker/no-collaborator/no-formaliser: PASS")
    print("OEIS_A396149_and_Euler_transform: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_bundle", type=Path)
    args = parser.parse_args()
    source = args.source_bundle.resolve()
    audit_manifest(source)
    audit_sources(source)
    audit_producer_and_witnesses(source)
    oeis_histogram = read_oeis_histogram(source)

    with tempfile.TemporaryDirectory(prefix="erdos80-hostile-") as directory:
        fresh = Path(directory) / "all_n9.g6"
        with fresh.open("wb") as output:
            subprocess.run(["nauty-geng", "-q", "9"], check=True, stdout=output)
        assert sha256(fresh) == EXPECTED_G6_SHA256
        assert fresh.read_bytes() == (source / "all_n9.g6").read_bytes()
        scan(fresh, oeis_histogram)

    print("HOSTILE AUDIT: PUBLISH")


if __name__ == "__main__":
    main()
