#!/usr/bin/env python3
"""Compare valid reflected-core counts in the two exhaustive programs."""

from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DIRECT = re.compile(
    r"RESULT cap=151 core=(\d+) t_range=\d+\.\.\d+ found=0 "
    r"orbit_nodes=\d+ complete_cores=(\d+) valid_cores=(\d+) "
    r"extension_nodes=\d+ seconds=[0-9.eE+-]+"
)
AUDIT = re.compile(
    r"CASE (\d+) outliers=\d+ lower_halves=\d+ core_candidates=\d+ "
    r"valid_cores=(\d+) extension_nodes=\d+ "
    r"digest_xor=[0-9a-f]+ digest_sum=[0-9a-f]+"
)

direct = defaultdict(int)
for name in ("direct_whole_results.txt", "direct_sliced_results.txt"):
    for line in (ROOT / name).read_text().splitlines():
        match = DIRECT.fullmatch(line)
        if not match:
            continue
        core, complete, valid = map(int, match.groups())
        assert complete == valid
        direct[core] += valid

assert set(direct) == set(range(14, 21))

audit = {}
for line in (ROOT / "audit_output.txt").read_text().splitlines():
    match = AUDIT.fullmatch(line)
    if match:
        core, valid = map(int, match.groups())
        assert core not in audit
        audit[core] = valid
assert set(audit) == set(range(14, 21))

for core in range(20, 13, -1):
    assert direct[core] == audit[core], (
        core, direct[core], audit[core], "valid-core mismatch"
    )
    print(f"core={core} direct={direct[core]} audit={audit[core]} MATCH")
print("ALL SEVEN VALID-CORE COUNTS MATCH")
