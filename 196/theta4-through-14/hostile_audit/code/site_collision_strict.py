#!/usr/bin/env python3
"""Stricter Problem 196 collision check, including the site's problemNum field."""

from hashlib import sha256
from pathlib import Path
import re
import sys


AUTHOR = Path("/home/exedev/erdos_scratch/fresh9_erdos196_20260811/bundle_ro")
DEFAULTS = [
    AUTHOR / "provenance/site_index_20260811.js",
    AUTHOR / "provenance/site_ledger_data_20260811.js",
]
PATTERNS = {
    "problemNum": re.compile(r"\bproblemNum\s*:\s*196\b"),
    "n": re.compile(r"\bn\s*:\s*196\b"),
    "problem": re.compile(r"\bproblem\s*:\s*[\"']?196\b", re.IGNORECASE),
    "erdos_url": re.compile(r"erdosproblems(?:\\)?\.com/196\b", re.IGNORECASE),
    "title_or_prose": re.compile(r"(?:#|problem\s*)196\b", re.IGNORECASE),
    "theta4": re.compile(r"theta[ _-]?4\b", re.IGNORECASE),
    "monotone4": re.compile(
        r"monotone.{0,30}(?:4|four).{0,30}(?:ap|arithmetic)", re.IGNORECASE
    ),
}


def main():
    paths = [Path(value) for value in sys.argv[1:]] or DEFAULTS
    total = 0
    for path in paths:
        data = path.read_bytes()
        text = data.decode("utf-8")
        print(f"path={path} sha256={sha256(data).hexdigest()} bytes={len(data)}")
        for label, pattern in PATTERNS.items():
            count = len(pattern.findall(text))
            total += count
            print(f"pattern={label} count={count}")
    print(f"collision_total={total}")
    raise SystemExit(total != 0)


if __name__ == "__main__":
    main()
