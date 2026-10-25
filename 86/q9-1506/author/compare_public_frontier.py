#!/usr/bin/env python3
"""Exact set comparison against the frozen public Q9=1505 certificate."""

import hashlib
import json
from pathlib import Path


NEW_SHA = "883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c"
OLD_SHA = "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338"


def load(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = [tuple(sorted(map(int, edge))) for edge in data["edges"]]
    if len(rows) != len(set(rows)):
        raise SystemExit(f"duplicate row in {path}")
    return set(rows)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    new_path = root / "q9_edges_1506.json"
    old_path = root / "q9_upstream" / "q9_edges_repair_from1503_iter2.json"
    if digest(new_path) != NEW_SHA or digest(old_path) != OLD_SHA:
        raise SystemExit("frozen certificate hash mismatch")
    new, old = load(new_path), load(old_path)
    added, removed = new - old, old - new
    assert len(new) == 1506 and len(old) == 1505
    assert len(added) == 193 and len(removed) == 192
    print("PASS public-frontier comparison")
    print(f"new_edges={len(new)} old_edges={len(old)} improvement={len(new)-len(old)}")
    print(f"added={len(added)} removed={len(removed)} symmetric_difference={len(new ^ old)}")
    print(f"new_sha256={NEW_SHA}")
    print(f"old_sha256={OLD_SHA}")


if __name__ == "__main__":
    main()
