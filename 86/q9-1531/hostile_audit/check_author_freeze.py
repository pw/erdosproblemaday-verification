#!/usr/bin/env python3
"""Independently verify the author manifest, archive, and read-only snapshot."""

from __future__ import annotations

import hashlib
import re
import stat
import sys
import tarfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT / "author_bundle"
ARCHIVE = ROOT / "evidence" / "author_bundle_v3.tar.gz"
EXPECTED_MANIFEST_SHA256 = "520b3c6ae7ced58c696dc8ccb7141e141d0e9db95bec56d1be7865353b88806f"
EXPECTED_ARCHIVE_SHA256 = "ea8bb444fb03fd5ea24d43c2b94f9ff2803a3e4d2810fe05f045e56d1f31321b"
ARCHIVE_PREFIX = "erdos86_q9_1531_20260811_v3"
LINE_PATTERN = re.compile(r"^([0-9a-f]{64})  (\./[^\x00\r\n]+)$")


class FreezeFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeFailure(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(text: str) -> str:
    require(text.startswith("./"), f"manifest path lacks ./ prefix: {text!r}")
    relative = text[2:]
    pure = PurePosixPath(relative)
    require(relative != "", "empty manifest path")
    require(not pure.is_absolute(), f"absolute manifest path: {relative!r}")
    require(".." not in pure.parts, f"parent traversal in manifest: {relative!r}")
    require("." not in pure.parts, f"non-canonical manifest path: {relative!r}")
    return pure.as_posix()


def main() -> None:
    manifest_path = AUTHOR / "SHA256SUMS"
    require(sha256(manifest_path) == EXPECTED_MANIFEST_SHA256, "manifest hash mismatch")
    require(sha256(ARCHIVE) == EXPECTED_ARCHIVE_SHA256, "archive hash mismatch")

    manifest: dict[str, str] = {}
    lines = manifest_path.read_text(encoding="ascii").splitlines()
    for position, line in enumerate(lines, 1):
        match = LINE_PATTERN.fullmatch(line)
        require(match is not None, f"malformed manifest line {position}")
        digest, raw_path = match.groups()
        relative = safe_relative(raw_path)
        require(relative not in manifest, f"duplicate manifest path: {relative}")
        manifest[relative] = digest
    require(list(manifest) == sorted(manifest), "manifest paths are not sorted")

    disk_files = {
        path.relative_to(AUTHOR).as_posix()
        for path in AUTHOR.rglob("*")
        if path.is_file()
    }
    require("SHA256SUMS" in disk_files, "manifest file missing from disk")
    require(
        set(manifest) == disk_files - {"SHA256SUMS"},
        "manifest does not cover exactly every other regular file",
    )
    require(len(manifest) == 21, f"manifest has {len(manifest)} entries, not 21")
    for relative, expected in manifest.items():
        path = AUTHOR / relative
        require(not path.is_symlink(), f"manifest target is a symlink: {relative}")
        require(sha256(path) == expected, f"manifest digest mismatch: {relative}")

    disk_entries: dict[str, tuple[str, int, int]] = {}
    for path in [AUTHOR, *sorted(AUTHOR.rglob("*"))]:
        relative = path.relative_to(AUTHOR).as_posix()
        key = ARCHIVE_PREFIX if relative == "." else f"{ARCHIVE_PREFIX}/{relative}"
        mode = stat.S_IMODE(path.stat().st_mode)
        require(mode & 0o222 == 0, f"snapshot entry is writable: {relative}")
        if path.is_dir():
            disk_entries[key] = ("dir", mode, 0)
        elif path.is_file():
            disk_entries[key] = ("file", mode, path.stat().st_size)
        else:
            raise FreezeFailure(f"unsupported snapshot entry: {relative}")

    archive_entries: dict[str, tuple[str, int, int]] = {}
    with tarfile.open(ARCHIVE, mode="r:gz") as archive:
        for member in archive.getmembers():
            name = member.name.rstrip("/")
            pure = PurePosixPath(name)
            require(name != "", "empty archive member name")
            require(not pure.is_absolute(), f"absolute archive member: {name}")
            require(".." not in pure.parts, f"archive traversal member: {name}")
            require(name not in archive_entries, f"duplicate archive member: {name}")
            require(member.uid == 0 and member.gid == 0, f"non-canonical owner: {name}")
            require(member.mtime == 1786406400, f"non-canonical timestamp: {name}")
            if member.isdir():
                archive_entries[name] = ("dir", member.mode, 0)
            elif member.isfile():
                archive_entries[name] = ("file", member.mode, member.size)
                extracted = archive.extractfile(member)
                require(extracted is not None, f"cannot read archive member: {name}")
                relative = name.removeprefix(f"{ARCHIVE_PREFIX}/")
                require(relative != name, f"member outside archive prefix: {name}")
                require(
                    extracted.read() == (AUTHOR / relative).read_bytes(),
                    f"archive/directory byte mismatch: {relative}",
                )
            else:
                raise FreezeFailure(f"link or special archive member: {name}")
    require(archive_entries == disk_entries, "archive and directory entries differ")

    print(
        "AUTHOR_FREEZE_PASS manifest_entries=21 snapshot_files=22 "
        f"manifest_sha256={EXPECTED_MANIFEST_SHA256} "
        f"archive_sha256={EXPECTED_ARCHIVE_SHA256} read_only=yes archive_exact=yes"
    )


if __name__ == "__main__":
    try:
        main()
    except (FreezeFailure, OSError, tarfile.TarError) as exc:
        print(f"AUTHOR_FREEZE_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
