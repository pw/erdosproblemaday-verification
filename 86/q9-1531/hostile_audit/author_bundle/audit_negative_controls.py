#!/usr/bin/env python3
"""Mutation controls for the Q9 witness checker."""

import importlib.util
import json
import tempfile
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("q9verify", ROOT / "verify_q9_witness.py")
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def require_rejection(callback, label):
    try:
        callback()
    except verify.VerificationError:
        return
    raise RuntimeError(f"negative control accepted: {label}")


raw = json.loads((ROOT / "q9_edges_1531.json").read_text())

with tempfile.TemporaryDirectory() as directory:
    temp = Path(directory) / "mutated.json"

    duplicate = json.loads(json.dumps(raw))
    duplicate["num_edges"] = 1532
    duplicate["edges"].append(duplicate["edges"][0])
    temp.write_text(json.dumps(duplicate))
    require_rejection(lambda: verify.load_edges(temp, 1532), "duplicate edge")

    nonedge = json.loads(json.dumps(raw))
    nonedge["edges"][0] = [0, 3]
    temp.write_text(json.dumps(nonedge))
    require_rejection(lambda: verify.load_edges(temp, 1531), "non-hypercube edge")

edges = {tuple(sorted(edge)) for edge in raw["edges"]}
bad_edges = None
for first, second in combinations(range(9), 2):
    first_mask, second_mask = 1 << first, 1 << second
    for base in range(512):
        if base & (first_mask | second_mask):
            continue
        a = base
        b = base | first_mask
        c = base | second_mask
        d = base | first_mask | second_mask
        face = {(a, b), (a, c), (b, d), (c, d)}
        present = face & edges
        if len(present) == 3:
            missing = next(iter(face - edges))
            removable = next(edge for edge in edges if edge not in face)
            bad_edges = (edges - {removable}) | {missing}
            break
    if bad_edges is not None:
        break

if bad_edges is None or len(bad_edges) != 1531:
    raise RuntimeError("could not construct complete-face negative control")
require_rejection(lambda: verify.verify_faces(bad_edges), "complete square face")

print("NEGATIVE_CONTROLS=PASS duplicate=1 nonedge=1 complete_face=1")
