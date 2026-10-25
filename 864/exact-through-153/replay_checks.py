#!/usr/bin/env python3
"""Fast integrity and semantic replay checks for the frozen bundle."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent


def text(name):
    return (ROOT / name).read_text()


gate = text("live_gate.txt")
for required in (
    "OPEN",
    "0 claimed proofs for this problem",
    "Interested in collaborating\tNone",
    "Currently working on this problem\tNone",
):
    assert required in gate, required

source = text("golomb_ruler_source.html")
assert "0 1 6 10 23 26 34 41 53 55" in source

audit = text("audit_output.txt")
assert "CASE REDUCTION core sizes 14,15,16,17,18,19,20 PASS" in audit
assert audit.rstrip().endswith(
    "EXHAUSTED: no valid 20-set has diameter <= 151"
)

positive = text("positive_control.log")
assert "cap=152 core=20" in positive and "found=1" in positive
assert "WITNESS 0 1 3 8 14 26 30 47 62 71 81 90 105 122 126 138 144 149 151 152" in positive

sanitizer = text("sanitizer_output.txt")
assert "exit=2" in sanitizer
for bad in ("AddressSanitizer:", "runtime error:", "UndefinedBehaviorSanitizer"):
    assert bad not in sanitizer, bad

report = text("REPORT.md")
assert "PENDING" not in report
assert "F(135) = F(136) = ... = F(152) = 19" in report
assert "F(153) = 20" in report

for command in (
    ["python3", "verify_witness.py"],
    ["python3", "scan_construction.py"],
    ["python3", "verify_direct_logs.py"],
    ["python3", "compare_counts.py"],
):
    completed = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, check=True
    )
    print(completed.stdout.rstrip())

print("ALL REPLAY CHECKS PASSED")
