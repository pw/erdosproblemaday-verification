#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def edge_set(path):
    return {tuple(sorted(edge)) for edge in json.loads(path.read_text())["edges"]}


canonical = edge_set(ROOT / "q9_edges_1531.json")
raw = edge_set(ROOT / "provenance/q9_edges_1531_raw.json")
if canonical != raw or len(canonical) != 1531:
    raise SystemExit("canonical/raw edge-set mismatch")
print("CANONICAL_IDENTITY=PASS edges=1531")
