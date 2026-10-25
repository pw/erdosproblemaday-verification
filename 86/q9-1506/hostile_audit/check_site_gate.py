#!/usr/bin/env python3
"""Read-only collision audit for problem 86 in the two site data sources."""

from pathlib import Path
import re


ROOT = Path("/home/exedev/ErdosProblemADay")
paths = [ROOT / "src/index.js", ROOT / "src/ledger_data.js"]
patterns = {
    "ledger_record_86": re.compile(r"\{n:86,"),
    "problem_token_86": re.compile(r"#86(?:\D|$)"),
    "live_url_86": re.compile(r"erdosproblems\.com/(?:86|forum/thread/86)(?:\D|$)"),
    "oeis_A245762": re.compile(r"A245762", re.I),
    "same_framework": re.compile(
        r"(?:C.?4.?free.{0,120}hypercube|hypercube.{0,120}C.?4.?free|"
        r"subgraph.{0,80}hypercube|hypercube.{0,80}subgraph)",
        re.I | re.S,
    ),
}

for path in paths:
    text = path.read_text(encoding="utf-8")
    counts = {name: len(pattern.findall(text)) for name, pattern in patterns.items()}
    print(path)
    print(" ".join(f"{name}={count}" for name, count in counts.items()))
    assert not any(counts.values())

print("SITE_GATE_PASS problem86_and_same_framework_absent=yes")
