#!/usr/bin/env python3
"""Definition-level verifier for the 1506-edge Q9 witness.

This checker independently enumerates every square face of Q9.  It is adapted
from Rafal Wrona's MIT-licensed verifier, frozen in provenance/.
"""

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="q9_edges_1506.json")
    args = parser.parse_args()
    path = Path(args.file)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("n") != 9 or data.get("num_edges") != 1506:
        raise SystemExit("FAIL: metadata must say n=9 and num_edges=1506")
    raw_edges = data.get("edges")
    if not isinstance(raw_edges, list) or len(raw_edges) != 1506:
        raise SystemExit("FAIL: certificate must contain exactly 1506 edge rows")

    edges = set()
    for row in raw_edges:
        if not isinstance(row, list) or len(row) != 2:
            raise SystemExit(f"FAIL: malformed edge row {row!r}")
        u, v = map(int, row)
        if not (0 <= u < 512 and 0 <= v < 512):
            raise SystemExit(f"FAIL: endpoint outside Q9 in {(u, v)}")
        if (u ^ v).bit_count() != 1:
            raise SystemExit(f"FAIL: not a Q9 edge: {(u, v)}")
        edge = tuple(sorted((u, v)))
        if edge in edges:
            raise SystemExit(f"FAIL: duplicate edge {edge}")
        edges.add(edge)

    faces = 0
    for d1, d2 in combinations(range(9), 2):
        m1, m2 = 1 << d1, 1 << d2
        for base in range(512):
            if base & (m1 | m2):
                continue
            a, b, c, d = base, base | m1, base | m2, base | m1 | m2
            square = ((a, b), (a, c), (b, d), (c, d))
            faces += 1
            if all(tuple(sorted(edge)) in edges for edge in square):
                raise SystemExit(f"FAIL: C4 on vertices {(a, b, d, c)}")
    if faces != 4608:
        raise SystemExit(f"FAIL: enumerated {faces} faces, expected 4608")

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"PASS faces: edges=1506 valid_Q9_edges=1506 faces={faces} violations=0")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
