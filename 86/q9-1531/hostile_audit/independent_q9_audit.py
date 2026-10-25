#!/usr/bin/env python3
"""Clean-room hostile verifier for the frozen Q9=1531 certificate bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


EXPECTED_FILE_SHA256 = {
    "q9_edges_1531.json": "4592a484fcfa65ef9883843485a60ff7b8d3856e81b4a667ae9cf14536132a5a",
    "provenance/q9_edges_1531_raw.json": "21c7c0ad8c24f2cd5e337722d41e606e3154e4fb3c43b503d4124dba3290bb61",
    "provenance/q9_edges_1506.json": "883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c",
    "provenance/q9_public_1505.json": "0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338",
}


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def reject_constant(token: str) -> None:
    raise AuditFailure(f"non-JSON numeric constant: {token}")


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AuditFailure(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def strict_json(payload: bytes, label: str) -> object:
    try:
        text = payload.decode("utf-8", errors="strict")
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditFailure(f"{label}: invalid strict JSON: {exc}") from exc


def q9_universe() -> frozenset[tuple[int, int]]:
    universe = {
        (u, u | (1 << coordinate))
        for coordinate in range(9)
        for u in range(512)
        if not u & (1 << coordinate)
    }
    require(len(universe) == 9 * 256 == 2304, "Q9 universe count is not 2304")
    return frozenset(universe)


def parse_certificate_bytes(
    payload: bytes,
    label: str,
    expected_count: int,
    universe: frozenset[tuple[int, int]],
) -> tuple[dict[str, object], frozenset[tuple[int, int]]]:
    document = strict_json(payload, label)
    require(type(document) is dict, f"{label}: root is not an object")
    require(type(document.get("n")) is int, f"{label}: n is not a JSON integer")
    require(document["n"] == 9, f"{label}: n is not 9")
    require(
        type(document.get("num_edges")) is int,
        f"{label}: num_edges is not a JSON integer",
    )
    require(
        document["num_edges"] == expected_count,
        f"{label}: metadata count is not {expected_count}",
    )

    rows = document.get("edges")
    require(type(rows) is list, f"{label}: edges is not an array")
    require(len(rows) == expected_count, f"{label}: wrong edge-row count")

    edges: set[tuple[int, int]] = set()
    reversed_rows = 0
    for position, row in enumerate(rows):
        require(
            type(row) is list and len(row) == 2,
            f"{label}: edge row {position} is not a two-item array",
        )
        u, v = row
        require(
            type(u) is int and type(v) is int,
            f"{label}: edge row {position} endpoints are not JSON integers",
        )
        require(0 <= u < 512 and 0 <= v < 512, f"{label}: endpoint out of range")
        require(u != v, f"{label}: loop at row {position}")
        edge = (min(u, v), max(u, v))
        if u > v:
            reversed_rows += 1
        require(edge in universe, f"{label}: non-Q9 edge at row {position}: {row}")
        require(edge not in edges, f"{label}: duplicate undirected edge at row {position}")
        edges.add(edge)

    require(len(edges) == expected_count, f"{label}: distinct-edge count mismatch")
    require(reversed_rows == 0, f"{label}: {reversed_rows} non-canonical reversed rows")
    return document, frozenset(edges)


def load_certificate(
    path: Path,
    relative: str,
    label: str,
    expected_count: int,
    universe: frozenset[tuple[int, int]],
) -> tuple[dict[str, object], frozenset[tuple[int, int]]]:
    payload = path.read_bytes()
    expected_hash = EXPECTED_FILE_SHA256[relative]
    actual_hash = sha256_bytes(payload)
    require(actual_hash == expected_hash, f"{label}: frozen file hash mismatch")
    return parse_certificate_bytes(payload, label, expected_count, universe)


def edge_set_sha256(edges: frozenset[tuple[int, int]]) -> str:
    # The portable canonical serialization is sorted ASCII lines: "u v\n".
    payload = "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")
    return sha256_bytes(payload)


def face_audit(edges: frozenset[tuple[int, int]]) -> dict[str, object]:
    occupancy = Counter()
    complete: list[tuple[int, int, int, int]] = []
    faces = 0
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
            boundary = ((a, b), (a, c), (b, d), (c, d))
            count = sum(edge in edges for edge in boundary)
            occupancy[count] += 1
            faces += 1
            if count == 4:
                complete.append((a, b, d, c))
    require(faces == 4608, f"coordinate-face enumeration returned {faces}, not 4608")
    require(sum(occupancy.values()) == faces, "face occupancy total mismatch")
    if complete:
        raise AuditFailure(f"complete coordinate face found: {complete[0]}")
    return {"faces": faces, "occupancy": occupancy}


def common_neighbour_audit(edges: frozenset[tuple[int, int]]) -> dict[str, object]:
    adjacency = [set() for _ in range(512)]
    directions = Counter()
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        directions[(u ^ v).bit_length() - 1] += 1

    degrees = [len(neighbours) for neighbours in adjacency]
    require(sum(degrees) == 2 * len(edges), "handshake identity failed")
    require(max(degrees) <= 9, "degree exceeds Q9 degree")
    require(sum(directions.values()) == len(edges), "direction-count identity failed")

    # Route A: enumerate every length-two path by center and endpoint pair.
    cherries_by_pair = Counter()
    cherries = 0
    for center in range(512):
        for endpoints in combinations(sorted(adjacency[center]), 2):
            cherries_by_pair[endpoints] += 1
            cherries += 1
    repeated_cherries = {
        pair: count for pair, count in cherries_by_pair.items() if count > 1
    }
    require(
        not repeated_cherries,
        f"repeated cherry endpoint pair: {next(iter(repeated_cherries.items()), None)}",
    )

    # Route B: independently exhaust all C(512,2)=130816 vertex pairs and
    # intersect their adjacency sets. Each intersection element is one center.
    pair_distribution = Counter()
    vertex_pairs = 0
    maximum_common = 0
    for u in range(512):
        for v in range(u + 1, 512):
            count = len(adjacency[u].intersection(adjacency[v]))
            pair_distribution[count] += 1
            vertex_pairs += 1
            maximum_common = max(maximum_common, count)
            require(
                count == cherries_by_pair.get((u, v), 0),
                f"common-neighbour/cherry disagreement for {(u, v)}",
            )
    require(vertex_pairs == 512 * 511 // 2 == 130816, "vertex-pair count mismatch")
    require(maximum_common <= 1, f"a vertex pair has {maximum_common} common neighbours")
    require(pair_distribution[1] == cherries, "cherry total mismatch")
    require(
        pair_distribution[0] + pair_distribution[1] == vertex_pairs,
        "unexpected common-neighbour distribution",
    )

    return {
        "cherries": cherries,
        "degrees": Counter(degrees),
        "directions": directions,
        "maximum_common": maximum_common,
        "pair_distribution": pair_distribution,
        "vertex_pairs": vertex_pairs,
    }


def audit_graph(label: str, edges: frozenset[tuple[int, int]]) -> dict[str, object]:
    faces = face_audit(edges)
    common = common_neighbour_audit(edges)
    print(
        f"GRAPH_PASS label={label} edges={len(edges)} vertices=512 "
        f"q9_universe=2304 faces={faces['faces']} complete_faces=0 "
        f"vertex_pairs={common['vertex_pairs']} max_common={common['maximum_common']} "
        f"cherries={common['cherries']} repeated_cherries=0"
    )
    print(
        f"DIAGNOSTICS label={label} "
        + "directions="
        + ",".join(f"{i}:{common['directions'][i]}" for i in range(9))
        + " degree_histogram="
        + ",".join(
            f"{degree}:{common['degrees'][degree]}"
            for degree in sorted(common["degrees"])
        )
        + " face_occupancy="
        + ",".join(f"{count}:{faces['occupancy'][count]}" for count in range(5))
        + " common_neighbours="
        + ",".join(
            f"{count}:{common['pair_distribution'][count]}"
            for count in sorted(common["pair_distribution"])
        )
    )
    return {"faces": faces, "common": common}


def expect_failure(callback, label: str) -> None:
    try:
        callback()
    except AuditFailure:
        return
    raise AuditFailure(f"negative control was accepted: {label}")


def self_tests(
    source_document: dict[str, object],
    source_edges: frozenset[tuple[int, int]],
    universe: frozenset[tuple[int, int]],
) -> None:
    def encoded(document: dict[str, object]) -> bytes:
        return json.dumps(document, separators=(",", ":")).encode("utf-8")

    duplicate = copy.deepcopy(source_document)
    duplicate["edges"][0] = duplicate["edges"][1]
    expect_failure(
        lambda: parse_certificate_bytes(encoded(duplicate), "duplicate", 1531, universe),
        "duplicate edge",
    )

    nonedge = copy.deepcopy(source_document)
    nonedge["edges"][0] = [0, 3]
    expect_failure(
        lambda: parse_certificate_bytes(encoded(nonedge), "nonedge", 1531, universe),
        "non-Q9 edge",
    )

    boolean = copy.deepcopy(source_document)
    boolean["edges"][0] = [0, True]
    expect_failure(
        lambda: parse_certificate_bytes(encoded(boolean), "boolean", 1531, universe),
        "boolean endpoint",
    )

    expect_failure(
        lambda: strict_json(b'{"n":9,"n":9,"num_edges":0,"edges":[]}', "dupkey"),
        "duplicate JSON key",
    )
    expect_failure(
        lambda: strict_json(b'{"n":NaN,"num_edges":0,"edges":[]}', "nan"),
        "non-JSON NaN",
    )

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
            present = face.intersection(source_edges)
            if len(present) != 3:
                continue
            missing = next(iter(face.difference(source_edges)))
            removable = next(iter(source_edges.difference(face)))
            bad_edges = frozenset(source_edges.difference({removable}).union({missing}))
            break
        if bad_edges is not None:
            break
    require(bad_edges is not None and len(bad_edges) == 1531, "failed to build C4 mutation")
    expect_failure(lambda: face_audit(bad_edges), "complete coordinate face")
    expect_failure(lambda: common_neighbour_audit(bad_edges), "repeated common neighbours")

    print(
        "NEGATIVE_CONTROLS_PASS duplicate_edge=1 non_q9_edge=1 boolean_endpoint=1 "
        "duplicate_key=1 nan=1 complete_face=1 repeated_common_neighbours=1"
    )


def format_comparison(
    label: str,
    newer: frozenset[tuple[int, int]],
    older: frozenset[tuple[int, int]],
    expected_delta: int,
) -> None:
    common = len(newer.intersection(older))
    added = len(newer.difference(older))
    removed = len(older.difference(newer))
    require(len(newer) - len(older) == expected_delta, f"{label}: size delta mismatch")
    require(added - removed == expected_delta, f"{label}: set delta mismatch")
    print(
        f"SET_COMPARISON_PASS label={label} newer={len(newer)} older={len(older)} "
        f"common={common} newer_only={added} older_only={removed} net={expected_delta}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--author-root",
        type=Path,
        default=Path(__file__).resolve().parent / "author_bundle",
    )
    parser.add_argument("--skip-self-tests", action="store_true")
    args = parser.parse_args()

    root = args.author_root.resolve()
    universe = q9_universe()
    specifications = (
        ("candidate1531", "q9_edges_1531.json", 1531),
        ("raw1531", "provenance/q9_edges_1531_raw.json", 1531),
        ("site1506", "provenance/q9_edges_1506.json", 1506),
        ("public1505", "provenance/q9_public_1505.json", 1505),
    )
    documents: dict[str, dict[str, object]] = {}
    edge_sets: dict[str, frozenset[tuple[int, int]]] = {}
    for label, relative, expected_count in specifications:
        path = root / relative
        document, edges = load_certificate(path, relative, label, expected_count, universe)
        documents[label] = document
        edge_sets[label] = edges
        print(
            f"FILE_PASS label={label} rows={expected_count} unique={len(edges)} "
            f"sha256={sha256_bytes(path.read_bytes())} edge_set_sha256={edge_set_sha256(edges)}"
        )

    require(
        edge_sets["candidate1531"] == edge_sets["raw1531"],
        "canonical and raw 1531 edge sets differ",
    )
    require(
        documents["candidate1531"]["edges"] == documents["raw1531"]["edges"],
        "canonical and raw 1531 edge rows differ in content or order",
    )
    canonical_nonmetadata = {
        key: value
        for key, value in documents["candidate1531"].items()
        if key not in {"construction", "meta"}
    }
    raw_nonmetadata = {
        key: value
        for key, value in documents["raw1531"].items()
        if key not in {"construction", "meta"}
    }
    require(
        canonical_nonmetadata == raw_nonmetadata,
        "canonical/raw differences extend beyond descriptive metadata",
    )
    print(
        "CANONICAL_RAW_IDENTITY_PASS edges=1531 row_order_identity=yes "
        "only_construction_and_meta_differ=yes "
        f"edge_set_sha256={edge_set_sha256(edge_sets['candidate1531'])}"
    )

    for label in ("candidate1531", "site1506", "public1505"):
        audit_graph(label, edge_sets[label])

    format_comparison("candidate_vs_site", edge_sets["candidate1531"], edge_sets["site1506"], 25)
    format_comparison("candidate_vs_public", edge_sets["candidate1531"], edge_sets["public1505"], 26)
    format_comparison("site_vs_public", edge_sets["site1506"], edge_sets["public1505"], 1)

    if not args.skip_self_tests:
        self_tests(documents["candidate1531"], edge_sets["candidate1531"], universe)

    print(
        "INDEPENDENT_Q9_AUDIT_PASS lower_bound=1531 exactness_claimed=no "
        "optimality_claimed=no"
    )


if __name__ == "__main__":
    try:
        main()
    except (AuditFailure, OSError) as exc:
        print(f"INDEPENDENT_Q9_AUDIT_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
