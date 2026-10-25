#!/usr/bin/env -S python3 -I -P
"""Fail-closed, closed-world integrity verifier for this release."""

import sys


def fail(message):
    print(f"MANIFEST_CLOSURE=FAIL reason={message}", file=sys.stderr)
    raise SystemExit(1)


if sys.flags.optimize != 0:
    fail("optimized Python is forbidden")
if not sys.flags.isolated or not sys.flags.safe_path:
    fail("isolated safe-path Python is required; use python3 -I -P")


import os


if "PYTHONOPTIMIZE" in os.environ:
    fail("PYTHONOPTIMIZE must be unset")


import hashlib
from pathlib import Path
import re
import stat


class ManifestFailure(RuntimeError):
    """A release-integrity invariant failed."""


ROOT = Path(__file__).absolute().parent
MANIFEST_NAME = "MANIFEST.sha256"
PIN_NAME = "MANIFEST.sha256.pin"
LINE_PATTERN = re.compile(r"^([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9_.-]*)$")
PIN_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def require(condition, message):
    if not bool(condition):
        raise ManifestFailure(message)


def is_regular_unsymlinked(path):
    try:
        metadata = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode)


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_pin(path):
    require(is_regular_unsymlinked(path), f"{PIN_NAME} is missing or non-regular")
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "pin must be one newline-terminated line")
    try:
        value = raw[:-1].decode("ascii")
    except UnicodeDecodeError as error:
        raise ManifestFailure("pin is not ASCII") from error
    require(PIN_PATTERN.fullmatch(value) is not None, "pin is not a lowercase SHA-256")
    return value


def read_manifest(path):
    require(is_regular_unsymlinked(path), f"{MANIFEST_NAME} is missing or non-regular")
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), "manifest must end with one newline")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ManifestFailure("manifest is not ASCII") from error
    require(bool(lines), "manifest is empty")

    entries = {}
    order = []
    for number, line in enumerate(lines, start=1):
        match = LINE_PATTERN.fullmatch(line)
        require(match is not None, f"invalid manifest line {number}")
        expected, name = match.groups()
        require(name not in {MANIFEST_NAME, PIN_NAME}, f"reserved member listed: {name}")
        require(name not in entries, f"duplicate member: {name}")
        entries[name] = expected
        order.append(name)
    require(order == sorted(order), "manifest members are not in canonical order")
    return entries


def main():
    require(ROOT.is_dir() and not ROOT.is_symlink(), "bundle root is not a real directory")
    manifest = ROOT / MANIFEST_NAME
    pin = ROOT / PIN_NAME
    require(is_regular_unsymlinked(manifest), f"{MANIFEST_NAME} is missing or non-regular")
    expected_manifest_digest = read_pin(pin)
    require(digest(manifest) == expected_manifest_digest, "manifest digest differs from pin")
    entries = read_manifest(manifest)

    actual = {member.name for member in ROOT.iterdir()}
    expected = set(entries) | {MANIFEST_NAME, PIN_NAME}
    require(
        actual == expected,
        f"closure mismatch missing={sorted(expected - actual)} extra={sorted(actual - expected)}",
    )

    for name in sorted(expected):
        require(is_regular_unsymlinked(ROOT / name), f"non-regular or symlinked member: {name}")
    for name, expected_digest in entries.items():
        require(digest(ROOT / name) == expected_digest, f"digest mismatch: {name}")

    print(f"MANIFEST_CLOSURE=PASS members={len(expected)}")


if __name__ == "__main__":
    try:
        main()
    except (ManifestFailure, OSError) as error:
        fail(str(error))
