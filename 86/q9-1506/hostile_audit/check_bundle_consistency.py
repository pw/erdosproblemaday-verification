#!/usr/bin/env python3
"""Strict cross-format and public-baseline check for the frozen Q9 bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUTHOR = Path("/home/exedev/erdos_scratch/erdos86_q9_1506_20260811")
EXPECTED_MANIFEST_SHA = "2878fa5ec38e7d52e056883f53dfbeb72c72a200ec6eb133402cbf620d890e3c"
EXPECTED_NEW_SHA = "883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c"
EXPECTED_OLD_SHA = "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_strict(path: Path, expected_count: int) -> list[tuple[int, int]]:
    document = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert document["n"] == 9
    assert document["num_edges"] == expected_count
    assert isinstance(document["edges"], list)
    assert len(document["edges"]) == expected_count

    edges: list[tuple[int, int]] = []
    for index, row in enumerate(document["edges"]):
        assert isinstance(row, list) and len(row) == 2, (index, row)
        u, v = row
        assert type(u) is int and type(v) is int, (index, row)
        assert 0 <= u < v < 512, (index, row)
        assert (u ^ v).bit_count() == 1, (index, row)
        edges.append((u, v))
    assert len(set(edges)) == expected_count
    return edges


manifest = AUTHOR / "SHA256SUMS"
new_json = AUTHOR / "q9_edges_1506.json"
new_text = AUTHOR / "q9_edges_1506.txt"
old_json = AUTHOR / "q9_upstream" / "q9_edges_repair_from1503_iter2.json"

assert digest(manifest) == EXPECTED_MANIFEST_SHA
assert digest(new_json) == EXPECTED_NEW_SHA
assert digest(old_json) == EXPECTED_OLD_SHA

new_edges = load_strict(new_json, 1506)
old_edges = load_strict(old_json, 1505)

text_edges: list[tuple[int, int]] = []
for line_number, raw in enumerate(new_text.read_text(encoding="ascii").splitlines(), 1):
    fields = raw.split()
    assert len(fields) == 2, (line_number, raw)
    text_edges.append(tuple(map(int, fields)))
assert text_edges == new_edges

new_set, old_set = set(new_edges), set(old_edges)
assert len(new_set & old_set) == 1313
assert len(new_set - old_set) == 193
assert len(old_set - new_set) == 192

print("BUNDLE_CONSISTENCY_PASS")
print(f"manifest_sha256={digest(manifest)}")
print(f"new_sha256={digest(new_json)} new_edges={len(new_set)}")
print(f"old_sha256={digest(old_json)} old_edges={len(old_set)}")
print("portable_text_rows=1506 exact_order_match=yes")
print("intersection=1313 added=193 removed=192 net_improvement=1")
