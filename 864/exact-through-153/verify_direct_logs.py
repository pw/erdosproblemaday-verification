#!/usr/bin/env python3
"""Verify exact center coverage and aggregate direct-search logs."""

from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PATTERN = re.compile(
    r"RESULT cap=(\d+) core=(\d+) t_range=(\d+)\.\.(\d+) found=(\d+) "
    r"orbit_nodes=(\d+) complete_cores=(\d+) valid_cores=(\d+) "
    r"extension_nodes=(\d+) seconds=([0-9.eE+-]+)"
)

expected = {
    16: set(range(64, 152)),
    15: set(range(56, 151, 2)),
    14: set(range(49, 152)),
}
seen = defaultdict(list)
totals = defaultdict(lambda: defaultdict(int))

canonical = ROOT / "direct_sliced_results.txt"
if canonical.exists():
    paths = [canonical]
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
        cap, core, lo, hi, found, orbit, complete, valid, extension, _ = match.groups()
        cap, core, lo, hi, found = map(int, (cap, core, lo, hi, found))
        assert cap == 151 and core in expected
        assert lo == hi and found == 0
        seen[core].append(lo)
        totals[core]["orbit_nodes"] += int(orbit)
        totals[core]["complete_cores"] += int(complete)
        totals[core]["valid_cores"] += int(valid)
        totals[core]["extension_nodes"] += int(extension)

for core in (16, 15, 14):
    centers = seen[core]
    assert len(centers) == len(set(centers)), (core, "duplicate center")
    assert set(centers) == expected[core], (
        core,
        "missing",
        sorted(expected[core] - set(centers)),
        "extra",
        sorted(set(centers) - expected[core]),
    )
    values = totals[core]
    print(
        f"CASE {core} centers={len(centers)} found=0 "
        f"orbit_nodes={values['orbit_nodes']} "
        f"complete_cores={values['complete_cores']} "
        f"valid_cores={values['valid_cores']} "
        f"extension_nodes={values['extension_nodes']}"
    )

whole = (ROOT / "direct_whole_results.txt").read_text()
whole_rows = [PATTERN.fullmatch(line) for line in whole.splitlines()]
whole_rows = [m for m in whole_rows if m]
assert len(whole_rows) == 4
expected_ranges = {20: (100, 151), 19: (90, 151), 18: (81, 151), 17: (72, 151)}
for match in whole_rows:
    cap, core, lo, hi, found = map(int, match.groups()[:5])
    assert cap == 151 and found == 0
    assert (lo, hi) == expected_ranges[core]
print("CASE 17..20 whole-log coverage PASS")
print("DIRECT LOG COVERAGE PASSED")
