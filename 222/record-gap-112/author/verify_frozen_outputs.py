#!/usr/bin/env python3
"""Check the frozen full-range summaries, OEIS anchor, and endpoint arithmetic."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
FULL_OUTPUTS = (
    "scan_99951600293_200000000000.out",
    "scan_report_99951600293_200000000000.out",
    "independent_scan_99951600293_200000000000.out",
)
EXPECTED = {
    "REPRESENTED_COUNT": 15_137_795_993,
    "FIRST": 99_951_600_293,
    "LAST": 200_000_000_000,
    "MAX_GAP": 112,
    "MAX_GAP_LEFT": 133_858_454_292,
    "MAX_GAP_RIGHT": 133_858_454_404,
    "NONREPRESENTED_RUN": 111,
}
EXPECTED_REPORTED = [
    (112, 133_858_454_292, 133_858_454_404),
    (108, 190_766_104_961, 190_766_105_069),
]
BASELINE_EXPECTED = {
    "REPRESENTED_COUNT": 15_563_133_098,
    "FIRST": 0,
    "LAST": 99_951_600_400,
    "MAX_GAP": 107,
    "MAX_GAP_LEFT": 99_951_600_293,
    "MAX_GAP_RIGHT": 99_951_600_400,
    "NONREPRESENTED_RUN": 106,
}


def read_output(filename: str) -> tuple[dict[str, int], list[tuple[int, int, int]]]:
    fields = {}
    gaps = []
    for line in (ROOT / filename).read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].isdigit():
            fields[parts[0]] = int(parts[1])
        elif len(parts) == 4 and parts[0] == "GAP":
            gaps.append(tuple(map(int, parts[1:])))
    return fields, gaps


baseline_fields, baseline_gaps = read_output("baseline_scan_0_99951600400.out")
for key, value in BASELINE_EXPECTED.items():
    assert baseline_fields[key] == value, (key, baseline_fields[key], value)
assert baseline_fields["REPORTED_GAP_AT_LEAST"] == 107
assert baseline_fields["REPORTED_GAP_COUNT"] == 1
assert baseline_gaps == [(107, 99_951_600_293, 99_951_600_400)]

for filename in FULL_OUTPUTS:
    fields, gaps = read_output(filename)
    for key, value in EXPECTED.items():
        assert fields[key] == value, (filename, key, fields[key], value)
    if fields.get("REPORTED_GAP_AT_LEAST") == 108:
        assert gaps == EXPECTED_REPORTED, (filename, gaps)
        assert fields["REPORTED_GAP_COUNT"] == len(gaps)


def read_bfile(filename: str) -> list[tuple[int, int]]:
    rows = []
    for line in (ROOT / filename).read_text().splitlines():
        if line and not line.startswith("#"):
            index, value = map(int, line.split())
            rows.append((index, value))
    return rows


record_starts = read_bfile("oeis_A297350_bfile_20260811.txt")
record_runs = read_bfile("oeis_A357018_bfile_20260811.txt")
assert len(record_starts) == len(record_runs) == 43
assert record_starts[-1] == (43, 99_951_600_293)
assert record_runs[-1] == (43, 106)

# Published record endpoints and both closed scan endpoints are represented.
assert 107_377**2 + 297_358**2 == 99_951_600_293
assert 77_520**2 + 306_500**2 == 99_951_600_400
assert 49_986**2 + 362_436**2 == 133_858_454_292
assert 35_298**2 + 364_160**2 == 133_858_454_404
assert 200_000**2 + 400_000**2 == 200_000_000_000

print(
    "FROZEN_OUTPUTS_PASS baseline=0..99951600400 post_anchor_scanners=3 "
    "represented=15137795993 max_gap=112 endpoints=133858454292,133858454404 "
    "oeis_anchor_start=99951600293 oeis_anchor_gap=107"
)
