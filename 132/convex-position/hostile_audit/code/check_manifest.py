#!/usr/bin/env python3
"""Check exact file and directory closure for this hostile-audit bundle."""

from hashlib import sha256
from pathlib import Path
import os
import re


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
ALLOWED_DIRECTORIES = {"code", "logs"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="ascii").splitlines():
        digest, separator, relative = line.partition("  ")
        require(separator == "  ", f"bad manifest line: {line!r}")
        require(bool(re.fullmatch(r"[0-9a-f]{64}", digest)), "bad digest")
        require(relative and relative not in entries, f"duplicate path: {relative}")
        entries[relative] = digest

    actual_files: set[str] = set()
    actual_directories: set[str] = set()
    for directory, names, files in os.walk(ROOT, followlinks=False):
        base = Path(directory)
        for name in names:
            path = base / name
            require(not path.is_symlink(), f"symlink directory: {path}")
            actual_directories.add(path.relative_to(ROOT).as_posix())
        for name in files:
            path = base / name
            require(not path.is_symlink(), f"symlink file: {path}")
            relative = path.relative_to(ROOT).as_posix()
            if relative == MANIFEST.name:
                continue
            require(path.is_file(), f"non-regular file: {relative}")
            actual_files.add(relative)

    require(actual_directories == ALLOWED_DIRECTORIES,
            f"directory mismatch: {sorted(actual_directories)}")
    require(actual_files == set(entries),
            f"file coverage mismatch: {sorted(actual_files ^ set(entries))}")
    for relative, expected in entries.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, f"hash mismatch: {relative}")
    print(f"AUDIT_MANIFEST_PASS files={len(entries)} dirs=2")


if __name__ == "__main__":
    main()
