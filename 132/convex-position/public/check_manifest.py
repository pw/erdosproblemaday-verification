#!/usr/bin/env python3
"""Require exact file coverage and hashes for this public package."""

from hashlib import sha256
from pathlib import Path
import os


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.sha256"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="ascii").splitlines():
        digest, separator, relative = line.partition("  ")
        require(separator == "  ", f"bad manifest line: {line!r}")
        require(len(digest) == 64, f"bad digest for {relative}")
        require(relative and relative not in entries, f"duplicate path: {relative}")
        entries[relative] = digest

    actual: set[str] = set()
    for directory, names, files in os.walk(ROOT, followlinks=False):
        base = Path(directory)
        require(not names, f"unexpected directories: {sorted(names)}")
        for name in files:
            path = base / name
            require(not path.is_symlink(), f"symlink file: {path}")
            relative = path.relative_to(ROOT).as_posix()
            if relative == MANIFEST.name:
                continue
            require(path.is_file(), f"non-regular file: {relative}")
            actual.add(relative)

    require(actual == set(entries),
            f"manifest coverage mismatch missing={sorted(actual-set(entries))} "
            f"extra={sorted(set(entries)-actual)}")
    for relative, expected in entries.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, f"hash mismatch: {relative}")
    print(f"MANIFEST_PASS files={len(entries)}")


if __name__ == "__main__":
    main()
