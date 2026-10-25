#!/usr/bin/env python3
"""Offline, optimization-safe audit for the public Problem 174 package."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from fractions import Fraction
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
PDF_MAGIC = bytes((37, 80, 68, 70, 45))


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check_manifest() -> int:
    manifest = ROOT / "MANIFEST.sha256"
    require(manifest.is_file() and not manifest.is_symlink(), "invalid root manifest")
    lines = [line for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    listed: list[str] = []
    for number, line in enumerate(lines, 1):
        match = re.fullmatch(r"([0-9a-f]{64})  (\./.+)", line)
        require(match is not None, f"malformed manifest line {number}")
        expected, relative = match.groups()
        require(relative != "./MANIFEST.sha256", "manifest lists itself")
        require(relative not in listed, f"duplicate manifest path: {relative}")
        logical = PurePosixPath(relative[2:])
        require(
            not logical.is_absolute()
            and logical.parts
            and all(part not in ("", ".", "..") for part in logical.parts)
            and f"./{logical.as_posix()}" == relative,
            f"non-canonical manifest path: {relative}",
        )
        path = ROOT.joinpath(*logical.parts)
        require(path.resolve().is_relative_to(ROOT), f"manifest path escapes root: {relative}")
        require(path.is_file() and not path.is_symlink(), f"missing or linked file: {relative}")
        require(sha256(path) == expected, f"hash mismatch: {relative}")
        listed.append(relative)

    regular_files = [path for path in ROOT.rglob("*") if path.is_file()]
    actual = sorted(
        f"./{path.relative_to(ROOT).as_posix()}"
        for path in regular_files
        if path != manifest
    )
    require(sorted(listed) == actual, "manifest is not exact filesystem closure")
    for path in regular_files:
        require(path.suffix.lower() != ".pdf", f"PDF extension shipped: {path.name}")
        with path.open("rb") as handle:
            require(PDF_MAGIC not in handle.read(1024), f"PDF payload shipped: {path.name}")
    return len(lines)


def check_text_metadata() -> int:
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    report = (ROOT / "REPORT.md").read_text(encoding="utf-8")
    live = (ROOT / "LIVE_GATE.txt").read_text(encoding="utf-8")

    source_markers = (
        "https://arxiv.org/abs/2608.09649",
        "Kenneth Moore",
        "Theorem 1.2",
        "2a1f866a06e5a8452f8b8425e6e244706a23eb039bb427eac5a51ade028fd45e",
        "https://creativecommons.org/licenses/by/4.0/",
        "https://arxiv.org/abs/2606.13472",
        "Maria-Romina Ivan",
        "Corollary 4 on p. 6 and Conjecture 8 on p. 9",
        "9e7a0da78ec6094bde530cf789c9ef58a680810ef2ac52feac49114c4c884f0e",
        "https://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "f0ee8b166026281c106562102657a71a7be8a85db964e0b370244ddc4764fbfd",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        "10.1016/0097-3165(73)90011-3",
        "Proposition 4 on journal p. 343",
        "on journal p. 357 supplies product closure",
        "ac59b75ae71753073a99d689e60a8d52caa7a47216dd21d7d57026b8d281682a",
        "10.1090/S0894-0347-1990-1020148-2",
        "Theorem 5.1 on journal p. 5",
        "e82f0e24babe4751e695fd90da2f46363e127544f53598ea9a2ae805a6eaba72",
        "contains no third-party PDF",
    )
    report_markers = (
        "Status: **PARTIAL, independently audited**",
        "Corollary 4 already proves the conclusion for a",
        "Moore removes that structural assumption",
        "no peer-reviewed version",
        "B = empty",
        "general characterization remains open",
        "`LIVE_GATE.txt` preserves",
    )
    live_markers = (
        "OPEN",
        "0 claimed proofs for this problem",
        "Currently working on this problem: None",
    )
    for marker in source_markers:
        require(marker in sources, f"missing source marker: {marker}")
    for marker in report_markers:
        require(marker in report, f"missing report marker: {marker}")
    for marker in live_markers:
        require(marker in live, f"missing live marker: {marker}")
    require("Barnabas Ivan" not in sources, "incorrect ILW author attribution")
    require("live/live_gate.txt" not in report, "stale private live-gate path")
    return len(source_markers) + len(report_markers) + len(live_markers)


Vector = tuple[Fraction, ...]


def vector(values: list[str]) -> Vector:
    require(all(isinstance(item, str) for item in values), "non-string rational fixture")
    return tuple(Fraction(item) for item in values)


def subtract(left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "vector dimension mismatch")
    return tuple(x - y for x, y in zip(left, right))


def squared_distance(left: Vector, right: Vector) -> Fraction:
    require(len(left) == len(right), "distance dimension mismatch")
    return sum((x - y) ** 2 for x, y in zip(left, right))


def rank(rows: list[Vector]) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [list(row) for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                x - scale * y for x, y in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def affine_rank(points: list[Vector]) -> int:
    require(bool(points), "empty affine-rank input")
    return rank([subtract(point, points[0]) for point in points[1:]])


def check_case(case: dict[str, object]) -> int:
    require(set(case) == {"base", "u", "h", "c_points"}, "wrong fixture keys")
    base = [vector(row) for row in case["base"]]
    u = vector(case["u"])
    h = Fraction(case["h"])
    c_points = [vector(row) for row in case["c_points"]]
    require(bool(base) and bool(c_points) and h > 0, "invalid nonempty fixture")
    d1, d2, count = len(u), len(c_points[0]), len(c_points)
    require(all(len(point) == d1 for point in base), "base dimension mismatch")
    require(all(len(point) == d2 for point in c_points), "C dimension mismatch")

    basis = [
        tuple(Fraction(int(i == j)) for j in range(count))
        for i in range(count)
    ]
    simplex = [
        c_points[i] + tuple(h * coordinate for coordinate in basis[i])
        for i in range(count)
    ]
    require(affine_rank(simplex) == count - 1, "simplex is affinely dependent")

    zero_block = tuple(Fraction(0) for _ in range(count))
    apices = [u + c_points[i] + zero_block for i in range(count)]
    fibres = [[point + simplex[i] for point in base] for i in range(count)]
    target_apex = u + (h,)
    target_base = [point + (Fraction(0),) for point in base]
    checks = 0

    for i, j in itertools.combinations(range(count), 2):
        require(
            squared_distance(apices[i], apices[j])
            == squared_distance(c_points[i], c_points[j]),
            "apex/C distance mismatch",
        )
        checks += 1
    for i in range(count):
        for j, k in itertools.combinations(range(len(base)), 2):
            require(
                squared_distance(fibres[i][j], fibres[i][k])
                == squared_distance(base[j], base[k]),
                "fibre/base distance mismatch",
            )
            checks += 1
        for j in range(len(base)):
            require(
                squared_distance(fibres[i][j], apices[i])
                == squared_distance(target_base[j], target_apex),
                "pyramid apex distance mismatch",
            )
            checks += 1

    product_points = [
        (j, i, base[j] + simplex[i])
        for j in range(len(base))
        for i in range(count)
    ]
    for left, right in itertools.combinations(product_points, 2):
        j, i, point = left
        k, ell, other = right
        expected = squared_distance(base[j], base[k]) + squared_distance(
            simplex[i], simplex[ell]
        )
        require(squared_distance(point, other) == expected, "product metric mismatch")
        checks += 1
    return checks


def check_geometric_fixtures() -> tuple[int, int]:
    data = json.loads((ROOT / "fixtures/geometric_cases.json").read_text(encoding="utf-8"))
    require(set(data) == {"cases"}, "wrong fixture document keys")
    cases = data["cases"]
    require(isinstance(cases, list) and len(cases) == 3, "wrong fixture case count")
    return len(cases), sum(check_case(case) for case in cases)


def check_colour_dichotomy() -> int:
    checked = 0
    for colours in itertools.product(range(3), repeat=3):
        red_apex = any(colour == 0 for colour in colours)
        other_pair = any(
            colours[i] == colours[j] != 0
            for i, j in itertools.combinations(range(3), 2)
        )
        require(red_apex or other_pair, "colour dichotomy failed")
        checked += 1
    return checked


def main() -> None:
    manifest_files = check_manifest()
    text_markers = check_text_metadata()
    fixture_cases, equalities = check_geometric_fixtures()
    colourings = check_colour_dichotomy()
    print(
        "PUBLIC_BUNDLE=PASS "
        f"manifest_files={manifest_files} pdfs=0 text_markers={text_markers} "
        f"fixture_cases={fixture_cases} geometric_equalities={equalities} "
        f"abstract_colourings={colourings}"
    )


if __name__ == "__main__":
    main()
