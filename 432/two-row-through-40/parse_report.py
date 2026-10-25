#!/usr/bin/env python3
"""Check that REPORT.md's table agrees exactly with both audit sources."""

from __future__ import annotations

import ast
import importlib.util
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parent


def cpp_rows() -> dict[int, tuple[int, int, list[int]]]:
    text = (ROOT / "audit_clique.cpp").read_text()
    block = text.split("static const vector<Row> rows = {", 1)[1].split("};", 1)[0]
    rows: dict[int, tuple[int, int, list[int]]] = {}
    for n, threshold, gap, starts in re.findall(
        r"\{(\d+),\s*(\d+),\s*(\d+),\s*\{([^}]*)\}\}", block
    ):
        rows[int(n)] = (
            int(threshold),
            int(gap),
            [int(value) for value in starts.split(",")],
        )
    return rows


def report_rows() -> dict[int, tuple[int, int, list[int]]]:
    rows: dict[int, tuple[int, int, list[int]]] = {}
    for line in (ROOT / "REPORT.md").read_text().splitlines():
        match = re.fullmatch(r"\| (\d+) \| (\d+) \| (\d+) \| ([0-9,]+) \|", line)
        if match:
            n, threshold, gap, starts = match.groups()
            rows[int(n)] = (
                int(threshold),
                int(gap),
                [int(value) for value in starts.split(",")],
            )
    return rows


def python_rows() -> dict[int, tuple[int, int, list[int]]]:
    tree = ast.parse((ROOT / "audit_cpsat.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "ROWS"
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("ROWS not found")


def main() -> None:
    report = report_rows()
    cpp = cpp_rows()
    python = python_rows()
    assert sorted(report) == list(range(11, 41))
    assert report == cpp == python
    print("PASS: report, C++ audit, and CP-SAT audit contain identical L_11..L_40 tables")


if __name__ == "__main__":
    main()
