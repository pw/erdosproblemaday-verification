#!/usr/bin/env python3
"""Re-run the local-source portion of the problem-1162 candidate gate."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


FILES = (
    Path("/home/exedev/ErdosProblemADay/src/index.js"),
    Path("/home/exedev/ErdosProblemADay/src/ledger_data.js"),
)
PHRASES = (
    "number of subgroups",
    "subgroups of s_n",
    "subgroups of the symmetric group",
    "roney-dougal",
    "gareth tracey",
)


def main() -> None:
    failed = False
    for path in FILES:
        data = path.read_bytes()
        text = data.decode("utf-8")
        number_hits = len(re.findall(r"(?<!\d)1162(?!\d)", text))
        print(f"{path}")
        print(f"  sha256={hashlib.sha256(data).hexdigest()}")
        print(f"  standalone_1162_hits={number_hits}")
        failed |= number_hits != 0
        folded = text.casefold()
        for phrase in PHRASES:
            hits = folded.count(phrase)
            print(f"  phrase[{phrase!r}]={hits}")
            failed |= hits != 0
    if failed:
        raise SystemExit("SITE GATE FAILED")
    print("LOCAL SITE GATE PASSED")


if __name__ == "__main__":
    main()
