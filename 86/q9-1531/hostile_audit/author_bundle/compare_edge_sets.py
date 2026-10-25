#!/usr/bin/env python3
"""Compare two Q9 JSON certificates as edge sets, ignoring metadata."""

import argparse
import json
from pathlib import Path


def load(path: Path) -> set[tuple[int, int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("n") != 9:
        raise RuntimeError(f"{path}: n is not 9")
    rows = data.get("edges")
    if not isinstance(rows, list):
        raise RuntimeError(f"{path}: edges is not a list")
    edges = {tuple(sorted(row)) for row in rows}
    if len(edges) != len(rows) or data.get("num_edges") != len(edges):
        raise RuntimeError(f"{path}: duplicate or count mismatch")
    return edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    args = parser.parse_args()

    left = load(args.left)
    right = load(args.right)
    if left != right:
        raise RuntimeError(
            f"edge-set mismatch: left_only={len(left - right)} "
            f"right_only={len(right - left)}"
        )
    print(f"EDGE_SET_IDENTITY=PASS edges={len(left)}")


if __name__ == "__main__":
    main()
