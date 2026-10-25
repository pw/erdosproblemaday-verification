#!/usr/bin/env python3
"""Require all Python optimization modes to reject tracked-file mutations."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODES = ((), ("-O",), ("-OO",))
TRACKED_TARGETS = (
    "REPORT.md",
    "SOURCES.md",
    "fixtures/geometric_cases.json",
)
PDF_MAGIC = bytes((37, 80, 68, 70, 45))


def run(root: Path, mode: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *mode, str(root / "verify_public_bundle.py")],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add_tracked_file(root: Path, relative: str, content: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    manifest = root / "MANIFEST.sha256"
    manifest.chmod(manifest.stat().st_mode | 0o200)
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(f"{digest}  ./{relative}\n")


def add_untracked_file(root: Path) -> None:
    (root / "UNTRACKED.txt").write_text("not in manifest\n", encoding="utf-8")


def add_nested_manifest(root: Path) -> None:
    path = root / "nested" / "MANIFEST.sha256"
    path.parent.mkdir()
    path.write_text("untracked nested manifest\n", encoding="utf-8")


def add_disguised_pdf(root: Path) -> None:
    add_tracked_file(root, "fixtures/disguised.bin", PDF_MAGIC + b"1.7\n")


def add_pdf_extension(root: Path) -> None:
    add_tracked_file(root, "fixtures/disguised.pdf", b"not a PDF payload\n")


def duplicate_manifest_entry(root: Path) -> None:
    manifest = root / "MANIFEST.sha256"
    first = manifest.read_text(encoding="utf-8").splitlines()[0]
    manifest.chmod(manifest.stat().st_mode | 0o200)
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(first + "\n")


STRUCTURAL_MUTATIONS = (
    ("untracked regular file", add_untracked_file),
    ("untracked nested manifest", add_nested_manifest),
    ("tracked disguised PDF payload", add_disguised_pdf),
    ("tracked PDF extension", add_pdf_extension),
    ("duplicate manifest entry", duplicate_manifest_entry),
)


def main() -> None:
    clean_checks = 0
    tracked_mutation_checks = 0
    structural_checks = 0
    for mode in MODES:
        result = run(ROOT, mode)
        require(result.returncode == 0, f"clean run failed for mode {mode}: {result.stderr}")
        require("PUBLIC_BUNDLE=PASS" in result.stdout, f"missing PASS for mode {mode}")
        clean_checks += 1

    with tempfile.TemporaryDirectory() as temporary:
        for target in TRACKED_TARGETS:
            copy = Path(temporary) / target.replace("/", "_")
            shutil.copytree(ROOT, copy)
            changed = copy / target
            changed.chmod(changed.stat().st_mode | 0o200)
            with changed.open("ab") as handle:
                handle.write(b"\nTAMPER\n")
            for mode in MODES:
                result = run(copy, mode)
                require(result.returncode != 0, f"mutation accepted: {target}, mode {mode}")
                tracked_mutation_checks += 1

        for number, (name, mutate) in enumerate(STRUCTURAL_MUTATIONS):
            copy = Path(temporary) / f"structural_{number}"
            shutil.copytree(ROOT, copy)
            mutate(copy)
            for mode in MODES:
                result = run(copy, mode)
                require(result.returncode != 0, f"structure accepted: {name}, mode {mode}")
                structural_checks += 1

    print(
        "TAMPER_MATRIX=PASS "
        f"clean_modes={clean_checks} "
        f"tracked_mutation_rejections={tracked_mutation_checks} "
        f"structural_rejections={structural_checks}"
    )


if __name__ == "__main__":
    main()
