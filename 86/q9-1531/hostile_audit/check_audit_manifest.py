#!/usr/bin/env python3
"""Strictly verify the hostile-audit bundle and its content manifest."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys


ROOT = Path(__file__).resolve().parent
MANIFEST_NAME = "MANIFEST.sha256"
LINE_RE = re.compile(r"([0-9a-f]{64})  ([A-Za-z0-9_.\-/]+)")


def fail(message: str) -> None:
    print(f"AUDIT_MANIFEST_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def regular_files_and_check_metadata() -> set[str]:
    root_info = ROOT.lstat()
    if not stat.S_ISDIR(root_info.st_mode) or root_info.st_mode & 0o222:
        fail("audit root is not a read-only directory")
    regular: set[str] = set()
    for directory, dirnames, filenames in os.walk(ROOT, followlinks=False):
        base = Path(directory)
        for name in [*dirnames, *filenames]:
            path = base / name
            info = path.lstat()
            relative = path.relative_to(ROOT).as_posix()
            if info.st_mode & 0o222:
                fail(f"writable filesystem entry: {relative}")
            if stat.S_ISLNK(info.st_mode):
                fail(f"symlink: {relative}")
            if stat.S_ISDIR(info.st_mode):
                continue
            if not stat.S_ISREG(info.st_mode):
                fail(f"special filesystem entry: {relative}")
            if info.st_nlink != 1:
                fail(f"hardlinked regular file: {relative}")
            regular.add(relative)
    return regular


def parse_manifest() -> list[tuple[str, str]]:
    path = ROOT / MANIFEST_NAME
    try:
        raw = path.read_bytes()
        text = raw.decode("ascii")
    except (OSError, UnicodeDecodeError) as error:
        fail(f"cannot read strict ASCII manifest: {error}")
    if not text or not text.endswith("\n"):
        fail("manifest must be nonempty and newline-terminated")

    records: list[tuple[str, str]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = LINE_RE.fullmatch(line)
        if match is None:
            fail(f"malformed line {line_number}")
        digest, name = match.groups()
        pure = PurePosixPath(name)
        if pure.is_absolute() or name != pure.as_posix() or ".." in pure.parts:
            fail(f"unsafe or noncanonical path on line {line_number}: {name}")
        if name == MANIFEST_NAME:
            fail("manifest must not list itself")
        records.append((name, digest))

    names = [name for name, _ in records]
    if names != sorted(names):
        fail("paths are not sorted")
    if len(names) != len(set(names)):
        fail("duplicate manifest path")
    return records


def main() -> None:
    actual_files = regular_files_and_check_metadata()
    records = parse_manifest()
    listed_files = {name for name, _ in records}
    expected_files = actual_files - {MANIFEST_NAME}
    if listed_files != expected_files:
        missing = sorted(expected_files - listed_files)
        extra = sorted(listed_files - expected_files)
        fail(f"coverage mismatch: unlisted={missing} nonexistent={extra}")

    for name, expected in records:
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != expected:
            fail(f"SHA-256 mismatch: {name}")

    print(
        "AUDIT_MANIFEST_PASS "
        f"listed_files={len(records)} total_regular_files={len(actual_files)} "
        "writable_entries=0 links=0 special_files=0"
    )


if __name__ == "__main__":
    main()
