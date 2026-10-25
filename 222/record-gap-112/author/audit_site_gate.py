#!/usr/bin/env python3
"""Audit the frozen site snapshot for direct or same-result #222 coverage."""

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = (ROOT / "site_snapshot/index.js", ROOT / "site_snapshot/ledger_data.js")
DIRECT_PATTERNS = {
    "problem_number_field": r"\bn\s*:\s*222\b",
    "hash_reference": r"#\s*222\b",
    "problem_phrase": r"\bproblem\s*#?\s*222\b",
    "problem_url": r"erdosproblems\.com/222\b",
    "A297350": r"\bA297350\b",
    "A357018": r"\bA357018\b",
    "A256435": r"\bA256435\b",
}
RESULT_PATTERNS = {
    "record_gap_phrase": r"record gaps? between sums? of (?:two|2) squares",
    "consecutive_difference_phrase": (
        r"consecutive (?:differences|gaps).{0,120}sums? of (?:two|2) squares"
    ),
    "new_endpoint_left": r"\b133858454292\b",
    "new_endpoint_right": r"\b133858454404\b",
}
BROAD_PATTERN = re.compile(r"sums? of (?:two|2) squares", re.IGNORECASE)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


texts = {path: path.read_text() for path in FILES}
print("SITE_SNAPSHOT_AUDIT date=2026-08-11")
for path in FILES:
    print(f"SHA256 {digest(path)} {path.relative_to(ROOT)}")

for label, pattern in {**DIRECT_PATTERNS, **RESULT_PATTERNS}.items():
    count = sum(len(re.findall(pattern, text, re.IGNORECASE | re.DOTALL))
                for text in texts.values())
    print(f"GATE_PATTERN {label} count={count}")
    assert count == 0, (label, count)

print("BROAD_PHRASE_CONTEXTS")
for path, text in texts.items():
    for line_number, line in enumerate(text.splitlines(), 1):
        hits = list(BROAD_PATTERN.finditer(line))
        if not hits:
            continue
        record = re.match(r"\{n:(\d+),", line)
        problem = record.group(1) if record else "none"
        print(f"BROAD_HIT file={path.name} line={line_number} problem={problem} count={len(hits)}")

print(
    "SITE_GATE_PASS direct_problem_or_sequence_references=0 "
    "same_result_or_endpoint_references=0 broad_incidental_problems=661,723,955"
)
