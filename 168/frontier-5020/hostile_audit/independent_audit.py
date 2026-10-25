#!/usr/bin/env python3
"""Independent, solver-free audit of the frozen Erdos Problem 168 artifacts.

This deliberately does not import or execute code from the bundle.  Smooth
numbers are enumerated from a bounded exponent rectangle and forbidden triples
are recovered by integer multiplication, not by the bundle's heap/corner code.
The SCIP transcript checks only establish what the floating MIP run reported;
they are not exact proof certificates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


EXPECTED_SOURCE_HASHES = {
    "a004059.py.txt": "1e38d564f8e42ea7c26843186ca76c4077e797ebcac402a3de00b3f8df7e2529",
    "a386439.py.txt": "92b08a0c6647f55851356f6f3f6f7c8435a19446d5237c0ab0a53a9357aaa25d",
    "b004059.txt": "bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea",
    "veselinov_2604.15515.pdf": "68e3b58de8d2bf8f4e5fb48560f2c43e489d7979e7e0f8c44ed2ddf1c7adbb14",
}
CURRENT_SOURCE_NAMES = {
    "a004059.py.txt": "a004059.current.py.txt",
    "a386439.py.txt": "a386439.current.py.txt",
    "b004059.txt": "b004059.current.txt",
    "veselinov_2604.15515.pdf": "veselinov_2604.15515.current.pdf",
}
EXPECTED_FLAT_ROWS = [5000, 5001, 5004, 5006, 5009, 5011, 5013, 5016, 5020]
EXPECTED_EXTENSION = [
    (3336, 5002),
    (3337, 5003),
    (3338, 5005),
    (3339, 5007),
    (3340, 5008),
    (3341, 5010),
    (3342, 5012),
    (3343, 5014),
    (3344, 5015),
    (3345, 5017),
    (3346, 5018),
    (3347, 5019),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def smooth_rectangle(count: int) -> list[tuple[int, int, int]]:
    """Return (value,a,b) using a finite rectangle proven large enough."""
    a_limit, b_limit = 256, 192
    triples = [
        (pow(2, a) * pow(3, b), a, b)
        for a in range(a_limit)
        for b in range(b_limit)
    ]
    triples.sort()
    prefix = triples[:count]
    assert len(prefix) == count
    assert len({value for value, _, _ in prefix}) == count
    last = prefix[-1][0]
    # Any exponent pair outside the rectangle is larger than the last result.
    assert pow(2, a_limit) > last and pow(3, b_limit) > last
    return prefix


def multiplicative_edges(
    triples: list[tuple[int, int, int]], count: int
) -> list[tuple[int, int, int]]:
    values = [value for value, _, _ in triples[:count]]
    position = {value: i for i, value in enumerate(values)}
    answer = []
    for i, value in enumerate(values):
        east = position.get(2 * value)
        north = position.get(3 * value)
        if east is not None and north is not None:
            answer.append((i, east, north))
    return answer


def parse_bfile(path: Path) -> list[tuple[int, int]]:
    lines = path.read_text(encoding="ascii").splitlines()
    assert lines and lines[0] == "# A004059"
    rows = []
    for line in lines[1:]:
        assert line and not line.startswith("#")
        fields = line.split()
        assert len(fields) == 2
        rows.append(tuple(map(int, fields)))
    assert [n for n, _ in rows] == list(range(1, len(rows) + 1))
    positions = [k for _, k in rows]
    assert positions == sorted(set(positions))
    return rows


def verify_manifest(bundle: Path) -> int:
    manifest = bundle / "SHA256SUMS"
    entries: dict[str, str] = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  \./([^\s]+)", line)
        assert match, f"malformed manifest line: {line!r}"
        expected, relative = match.groups()
        assert relative not in entries and ".." not in Path(relative).parts
        entries[relative] = expected
    actual = {
        str(path.relative_to(bundle))
        for path in bundle.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    assert set(entries) == actual, (
        f"manifest mismatch missing={sorted(actual - set(entries))} "
        f"extra={sorted(set(entries) - actual)}"
    )
    for relative, expected in entries.items():
        assert digest(bundle / relative) == expected, relative
    return len(entries)


def parse_witness(path: Path, prefix: list[tuple[int, int, int]]) -> set[int]:
    by_pair = {(a, b): i for i, (_, a, b) in enumerate(prefix)}
    selected: set[int] = set()
    lines = path.read_text(encoding="ascii").splitlines()
    for line in lines:
        fields = line.split()
        assert len(fields) == 2, (path, line)
        pair = tuple(map(int, fields))
        assert pair in by_pair, (path, pair)
        selected.add(by_pair[pair])
    assert len(selected) == len(lines), f"duplicate point in {path}"
    return selected


def exact_log_number(text: str, label: str) -> Decimal:
    matches = re.findall(
        rf"^{re.escape(label)}\s*:\s*([+\-0-9.eE]+)", text, flags=re.MULTILINE
    )
    assert len(matches) == 1, (label, matches)
    return Decimal(matches[0])


def verify_scip_report(bundle: Path, row: dict[str, object], cover: int) -> None:
    solver = row["solver"]
    assert isinstance(solver, dict)
    assert solver["status"] == "optimal"
    assert solver["objective"] == cover
    assert Decimal(str(solver["dual_bound"])) == cover
    assert Decimal(str(solver["gap"])) == 0
    path = bundle / "frontier" / str(solver["log"])
    text = path.read_text(encoding="ascii")
    assert "SCIP Status        : problem is solved [optimal solution found]" in text
    assert exact_log_number(text, "Primal Bound") == cover
    assert exact_log_number(text, "Dual Bound") == cover
    assert exact_log_number(text, "Gap") == 0
    nodes = int(exact_log_number(text, "Solving Nodes"))
    assert nodes == solver["nodes"]
    assert "transformed objective value is always integral (scale: 1)" in text


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def directed_decimal(value: Fraction, places: int, upward: bool) -> str:
    scale = 10**places
    numerator = value.numerator * scale
    quotient, remainder = divmod(numerator, value.denominator)
    if upward and remainder:
        quotient += 1
    raw = str(quotient).rjust(places + 1, "0")
    return raw[:-places] + "." + raw[-places:]


def parse_fraction(text: str) -> Fraction:
    numerator, denominator = map(int, text.split("/"))
    return Fraction(numerator, denominator)


def verify_density(
    bundle: Path,
    triples: list[tuple[int, int, int]],
    published_rows: list[tuple[int, int]],
    frontier_rows: list[dict[str, object]],
) -> dict[str, object]:
    values = [value for value, _, _ in triples]
    published_positions = {k for _, k in published_rows}
    extended_positions = set(published_positions)
    extended_positions.update(
        int(row["k"])
        for row in frontier_rows
        if int(row["k"]) > 5000 and row["increment"] == 1
    )

    def bounds(positions: set[int], through: int) -> tuple[Fraction, Fraction, Fraction]:
        lower = sum(
            (Fraction(1, 3 * values[k - 1]) for k in positions if k <= through),
            Fraction(),
        )
        # The full reciprocal mass is exactly
        # (sum 2^-a)(sum 3^-b) = 2 * 3/2 = 3.
        width = Fraction(1) - sum(
            (Fraction(1, 3 * value) for value in values[:through]), Fraction()
        )
        assert width > 0
        return lower, lower + width, width

    published = bounds(published_positions, 5000)
    extended = bounds(extended_positions, 5020)
    frozen = json.loads(
        (bundle / "frontier" / "density_interval.json").read_text(encoding="ascii")
    )

    for name, expected, through, count in (
        ("published_5000_corrected", published, 5000, 3335),
        ("extended", extended, 5020, 3347),
    ):
        obj = frozen[name]
        lower, upper, width = expected
        assert obj["through"] == through
        assert obj["last_smooth"] == str(values[through - 1])
        assert obj["known_increments"] == count
        assert parse_fraction(obj["lower_fraction"]) == lower
        assert parse_fraction(obj["upper_fraction"]) == upper
        assert parse_fraction(obj["width_fraction"]) == width
        assert obj["lower_outward"] == directed_decimal(lower, 60, False)
        assert obj["upper_outward"] == directed_decimal(upper, 60, True)
        assert obj["width_upper"] == directed_decimal(width, 60, True)

    published_lower, published_upper, _ = published
    d5001 = values[5000]
    omitted = Fraction(1, 3 * d5001)
    buggy_upper = published_lower + Fraction(1) - sum(
        (Fraction(1, 3 * value) for value in values[:5001]), Fraction()
    )
    assert buggy_upper + omitted == published_upper
    bug = frozen["a386439_source_bug"]
    assert bug["d_5001"] == str(d5001)
    assert parse_fraction(bug["omitted_tail_term_fraction"]) == omitted
    assert bug["omitted_tail_term_upper"] == directed_decimal(omitted, 60, True)
    assert bug["source_bug_upper_outward"] == directed_decimal(buggy_upper, 60, True)
    assert bug["correct_upper_outward"] == directed_decimal(published_upper, 60, True)

    fixed_places = 0
    for places in range(1, 100):
        scale = 10**places
        if (extended[0].numerator * scale // extended[0].denominator) != (
            extended[1].numerator * scale // extended[1].denominator
        ):
            break
        fixed_places = places
    assert fixed_places == 35
    return {
        "lower": directed_decimal(extended[0], 60, False),
        "upper": directed_decimal(extended[1], 60, True),
        "width": fraction_text(extended[2]),
        "common_decimal_places": fixed_places,
        "d5001": d5001,
        "omitted_term": fraction_text(omitted),
    }


def verify_boundary_exchange(triples: list[tuple[int, int, int]]) -> None:
    prefix = triples[:5000]
    values = {value for value, _, _ in prefix}
    pairs = {(a, b) for _, a, b in prefix}
    counts = [sum((a + 2 * b) % 3 == color for _, a, b in prefix) for color in range(3)]
    assert counts == [1667, 1667, 1666]
    selected = {(a, b) for _, a, b in prefix if (a + 2 * b) % 3 != 2}
    selected.difference_update({(121, 1), (123, 0)})
    selected.update({(121, 2), (122, 0), (123, 1)})
    assert selected <= pairs and len(selected) == 3335
    for value, a, b in prefix:
        if 2 * value in values and 3 * value in values:
            assert not {(a, b), (a + 1, b), (a, b + 1)} <= selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--online-sources", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    online = args.online_sources.resolve()

    manifest_count = verify_manifest(bundle)
    for frozen_name, expected in EXPECTED_SOURCE_HASHES.items():
        frozen_path = bundle / "sources" / frozen_name
        assert digest(frozen_path) == expected
        current_name = CURRENT_SOURCE_NAMES[frozen_name]
        current_path = online / current_name
        assert current_path.exists(), current_path
        assert digest(current_path) == expected, current_path

    published_rows = parse_bfile(online / "b004059.current.txt")
    assert len(published_rows) == 3335 and published_rows[-1] == (3335, 5000)
    a057561 = [
        int(line.split()[1])
        for line in (online / "b057561.current.txt").read_text(encoding="ascii").splitlines()
        if line and not line.startswith("#")
    ]
    reconstructed_a057561 = [
        max(n for n, first_k in published_rows if first_k <= k) for k in range(1, 70)
    ]
    assert a057561 == reconstructed_a057561
    a386439 = "".join(
        line.split()[1]
        for line in (online / "b386439.current.txt").read_text(encoding="ascii").splitlines()
        if line and not line.startswith("#")
    )
    assert a386439 == "80096575500655898909042032638808241"

    data = json.loads((bundle / "frontier" / "results.json").read_text(encoding="ascii"))
    rows = data["rows"]
    assert [row["k"] for row in rows] == list(range(5000, 5021))
    assert data["problem"]["published_endpoint"] == {"k": 5000, "f": 3335}
    assert data["problem"]["oeis_bfile_sha256"] == EXPECTED_SOURCE_HASHES["b004059.txt"]

    triples = smooth_rectangle(5021)
    all_values = [value for value, _, _ in triples]
    all_pairs = [(a, b) for _, a, b in triples]
    solver_rows: list[int] = []
    exact_values: dict[int, int] = {}
    corner_checks = 0
    previous_f: int | None = None
    previous_edges: set[tuple[int, int, int]] = set()

    # Verify the one-new-corner statement over the entire reconstructed range.
    for k in range(1, 5021):
        current_edges = set(multiplicative_edges(triples, k))
        new_edges = current_edges - previous_edges
        _, a, b = triples[k - 1]
        if b == 0:
            assert not new_edges, (k, a, b, new_edges)
        else:
            assert len(new_edges) == 1, (k, a, b, new_edges)
            edge = next(iter(new_edges))
            assert set(edge) == {
                all_values[:k].index(pow(2, a) * pow(3, b - 1)),
                all_values[:k].index(pow(2, a + 1) * pow(3, b - 1)),
                k - 1,
            }
        previous_edges = current_edges

    for row in rows:
        k = int(row["k"])
        f = int(row["f"])
        prefix = triples[:k]
        edges = multiplicative_edges(triples, k)
        assert row["smooth_value"] == str(prefix[-1][0])
        assert row["exponents"] == list(prefix[-1][1:])
        assert row["corners"] == len(edges)

        # Multiplicative triples and exponent corners must be identical.
        for anchor, east, north in edges:
            a, b = all_pairs[anchor]
            assert all_pairs[east] == (a + 1, b)
            assert all_pairs[north] == (a, b + 1)

        witness_name = f"independent_k{k}.txt"
        assert row["witness"] == witness_name
        chosen = parse_witness(bundle / "frontier" / witness_name, prefix)
        assert len(chosen) == f
        for edge in edges:
            assert not set(edge) <= chosen, (k, edge)
        corner_checks += len(edges)

        if previous_f is None:
            assert k == 5000 and f == 3335 and row["increment"] is None
        else:
            increment = f - previous_f
            assert increment in (0, 1)
            assert row["increment"] == increment
            if increment == 1:
                assert row["solver"] is None
                assert row["method"] == "witness plus f(k)<=f(k-1)+1"
            else:
                assert row["method"] == "SCIP optimal minimum vertex cover"

        if row["solver"] is not None:
            solver_rows.append(k)
            verify_scip_report(bundle, row, k - f)
        exact_values[k] = f
        previous_f = f

    assert solver_rows == EXPECTED_FLAT_ROWS == data["solved_prefixes"]
    assert [exact_values[k] for k in range(5000, 5021)] == [
        3335, 3335, 3336, 3337, 3337, 3338, 3338,
        3339, 3340, 3340, 3341, 3341, 3342, 3342,
        3343, 3344, 3344, 3345, 3346, 3347, 3347,
    ]

    extension_lines = [
        line
        for line in (bundle / "b004059_extension.txt").read_text(encoding="ascii").splitlines()
        if line and not line.startswith("#")
    ]
    extension = [tuple(map(int, line.split())) for line in extension_lines]
    assert extension == EXPECTED_EXTENSION
    derived_extension = [
        (int(row["f"]), int(row["k"]))
        for row in rows[1:]
        if row["increment"] == 1
    ]
    assert derived_extension == EXPECTED_EXTENSION

    verify_boundary_exchange(triples)
    density = verify_density(bundle, triples, published_rows, rows)
    summary = {
        "status": "PASS_WITH_SOLVER_EVIDENCE_GAP",
        "manifested_files": manifest_count,
        "online_source_hashes_match": True,
        "oeis_a057561_terms_crosschecked": len(a057561),
        "oeis_a386439_digits_crosschecked": len(a386439),
        "published_frontier": {"f": 3335, "k": 5000},
        "verified_range": [5000, 5020],
        "final_f": exact_values[5020],
        "flat_scip_rows": solver_rows,
        "witnesses": len(rows),
        "corner_checks": corner_checks,
        "density": density,
        "limitations": [
            "SCIP transcripts are floating-MIP evidence, not checkable exact certificates",
            "the historical b-file computation itself is not proof-carrying",
        ],
    }
    rendered = json.dumps(summary, indent=2) + "\n"
    if args.summary:
        args.summary.write_text(rendered, encoding="ascii")
    print(rendered, end="")


if __name__ == "__main__":
    main()
