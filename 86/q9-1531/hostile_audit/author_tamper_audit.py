#!/usr/bin/env python3
"""Adversarial controls for the frozen author's Q9 verifier."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
import tempfile
from itertools import combinations
from pathlib import Path


class TamperAuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TamperAuditFailure(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--author-root",
        type=Path,
        default=Path(__file__).resolve().parent / "author_bundle",
    )
    args = parser.parse_args()
    root = args.author_root.resolve()

    spec = importlib.util.spec_from_file_location("frozen_author_q9", root / "verify_q9_witness.py")
    require(spec is not None and spec.loader is not None, "cannot load author verifier")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)

    source_path = root / "q9_edges_1531.json"
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)

    def expect_rejection(callback, label: str) -> None:
        try:
            callback()
        except verifier.VerificationError:
            return
        raise TamperAuditFailure(f"author verifier accepted substantive tamper: {label}")

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "tampered.json"

        duplicate = copy.deepcopy(source)
        duplicate["edges"][0] = duplicate["edges"][1]
        path.write_text(json.dumps(duplicate), encoding="utf-8")
        expect_rejection(lambda: verifier.load_edges(path, 1531), "same-count duplicate")

        nonedge = copy.deepcopy(source)
        nonedge["edges"][0] = [0, 3]
        path.write_text(json.dumps(nonedge), encoding="utf-8")
        expect_rejection(lambda: verifier.load_edges(path, 1531), "non-Q9 edge")

        boolean = copy.deepcopy(source)
        boolean_row = next(
            index for index, edge in enumerate(boolean["edges"]) if 1 in edge
        )
        boolean["edges"][boolean_row] = [
            True if endpoint == 1 else endpoint
            for endpoint in boolean["edges"][boolean_row]
        ]
        path.write_text(json.dumps(boolean), encoding="utf-8")
        boolean_edges = verifier.load_edges(path, 1531)
        require(len(boolean_edges) == 1531, "unexpected boolean-control result")

        require(source_bytes.startswith(b"{"), "unexpected source prefix")
        duplicate_key_bytes = b'{"n":123,' + source_bytes[1:]
        path.write_bytes(duplicate_key_bytes)
        duplicate_key_edges = verifier.load_edges(path, 1531)
        require(len(duplicate_key_edges) == 1531, "unexpected duplicate-key result")

    edges = {tuple(sorted(edge)) for edge in source["edges"]}
    bad_edges = None
    for first, second in combinations(range(9), 2):
        first_mask = 1 << first
        second_mask = 1 << second
        for base in range(512):
            if base & (first_mask | second_mask):
                continue
            a = base
            b = base | first_mask
            c = base | second_mask
            d = base | first_mask | second_mask
            face = {(a, b), (a, c), (b, d), (c, d)}
            if len(face.intersection(edges)) != 3:
                continue
            missing = next(iter(face.difference(edges)))
            removable = next(iter(edges.difference(face)))
            bad_edges = (edges - {removable}) | {missing}
            break
        if bad_edges is not None:
            break
    require(bad_edges is not None and len(bad_edges) == 1531, "cannot make C4 tamper")
    expect_rejection(lambda: verifier.verify_faces(bad_edges), "complete coordinate face")
    expect_rejection(
        lambda: verifier.verify_common_neighbours(tuple(bad_edges)),
        "repeated common-neighbour pair",
    )

    print(
        "AUTHOR_TAMPER_RESULTS substantive_rejected=4 "
        "same_count_duplicate=reject non_q9_edge=reject complete_face=reject "
        "repeated_common_neighbours=reject"
    )
    print(
        "AUTHOR_SCHEMA_LENIENCY boolean_endpoint=accept duplicate_json_key=accept "
        "impact=non_load_bearing_actual_files_strictly_valid"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, TamperAuditFailure) as exc:
        print(f"AUTHOR_TAMPER_AUDIT_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
