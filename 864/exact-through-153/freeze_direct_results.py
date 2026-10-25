#!/usr/bin/env python3
"""Emit one canonical RESULT line for every sliced direct-search center."""

from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PATTERN = re.compile(
    r"RESULT cap=151 core=(14|15|16) t_range=(\d+)\.\.(\d+) found=0 "
    r"orbit_nodes=\d+ complete_cores=\d+ valid_cores=\d+ "
    r"extension_nodes=\d+ seconds=[0-9.eE+-]+"
)
rows = defaultdict(dict)
reproduction_paths = sorted(ROOT.glob("direct_core14_t*.log")) \
    + sorted(ROOT.glob("direct_core15_t*.log")) \
    + sorted(ROOT.glob("direct_core16_t*.log"))
if len(reproduction_paths) == 239:
    paths = reproduction_paths
else:
    paths = (
        sorted(ROOT.glob("slice_*.log"))
        + sorted(ROOT.glob("omit_*.log"))
        + sorted(ROOT.glob("redo_core*.log"))
        + [ROOT / "direct_core15_t056.log"]
    )
for path in paths:
    for line in path.read_text().splitlines():
        match = PATTERN.fullmatch(line)
        if not match:
            continue
        core, lo, hi = map(int, match.groups())
        assert lo == hi
        assert lo not in rows[core], (core, lo, "duplicate")
        rows[core][lo] = line

expected = {
    16: list(range(64, 152)),
    15: list(range(56, 151, 2)),
    14: list(range(49, 152)),
}
for core in (16, 15, 14):
    assert sorted(rows[core]) == expected[core], (core, "coverage mismatch")
    for center in expected[core]:
        print(rows[core][center])
