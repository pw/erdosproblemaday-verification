#!/usr/bin/env python3
"""Check the frozen input and literature statements against arXiv source TeX."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: audit_primary_source.py rare.tex heptagon_matrix.json")
    tex = Path(sys.argv[1]).read_text()
    data = json.loads(Path(sys.argv[2]).read_text())

    start = tex.index(r"\label{example_1}")
    stop = tex.index(r"\end{equation}", start)
    rows = []
    for line in tex[start:stop].splitlines():
        values = [int(value) for value in re.findall(r"\d+", line)]
        if len(values) == 7:
            rows.append(values)
    assert rows == data["distance_matrix"]
    assert data["diameter"] == 22270
    assert data["characteristic"] == 2002

    assert r"\dot{d}(2,7)=22270" in tex
    assert "Each non degenerated triangle in a plane integral point set has equal characteristic." in tex
    assert "the characteristic is given by $2002=2\\cdot 7\\cdot 11\\cdot 13$" in tex
    assert "diameter of at most $70000$" in tex
    assert (
        "characteristic being a divisor of "
        "$6469693230=2\\cdot 3\\cdot 5\\cdot 7\\cdot 11\\cdot 13\\cdot 17\\cdot 19\\cdot 23\\cdot 29$"
        in tex
    )
    assert 6469693230 % 2002 == 0

    coordinate_tokens = [
        r"\frac{26127018}{2227},\frac{932064}{2227}\sqrt{2002}",
        r"\frac{245363}{17},\frac{3144}{17}\sqrt{2002}",
        r"\frac{17615968}{2227},\frac{238464}{2227}\sqrt{2002}",
        r"\frac{56068}{17},\frac{3144}{17}\sqrt{2002}",
        r"\frac{19079044}{2227},-\frac{54168}{2227}\sqrt{2002}",
    ]
    assert all(token in tex for token in coordinate_tokens)

    print("matrix_entries_matched=49")
    print("primary_diameter=22270")
    print("primary_characteristic=2002")
    print("primary_restricted_search_bound=70000")
    print("characteristic_divides_search_product=true")
    print("exact_coordinate_rows_matched=5")
    print("PRIMARY_SOURCE_AUDIT_PASS")


if __name__ == "__main__":
    main()
