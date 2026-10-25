#!/usr/bin/env python3
"""Check the cold combined scan and its overlap-count identity."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "full_scan_0_200b_width73456789.out"


fields = {}
gaps = []
for line in OUTPUT.read_text().splitlines():
    parts = line.split()
    if len(parts) == 2 and parts[1].isdigit():
        fields[parts[0]] = int(parts[1])
    elif len(parts) == 4 and parts[0] == "GAP":
        gaps.append(tuple(map(int, parts[1:])))

expected = {
    "CHUNK_WIDTH": 73_456_789,
    "CHUNKS": 2723,
    "REPRESENTED_COUNT": 30_700_929_089,
    "FIRST": 0,
    "LAST": 200_000_000_000,
    "MAX_GAP": 112,
    "MAX_GAP_LEFT": 133_858_454_292,
    "MAX_GAP_RIGHT": 133_858_454_404,
    "NONREPRESENTED_RUN": 111,
    "REPORTED_GAP_AT_LEAST": 108,
    "REPORTED_GAP_COUNT": 2,
}
for key, value in expected.items():
    assert fields[key] == value, (key, fields[key], value)

assert gaps == [
    (112, 133_858_454_292, 133_858_454_404),
    (108, 190_766_104_961, 190_766_105_069),
]

# The author's two overlapping scans share only the represented endpoints of
# the old 107-gap, so their counts must combine to the cold full-range count.
assert 15_563_133_098 + 15_137_795_993 - 2 == fields["REPRESENTED_COUNT"]
print("COLD_FULL_SCAN_PASS range=0..200000000000 chunks=2723 width=73456789")
print("represented=30700929089 max_gap=112 endpoints=133858454292,133858454404")
print("reported_ge_108=2 overlap_count_identity=PASS")
