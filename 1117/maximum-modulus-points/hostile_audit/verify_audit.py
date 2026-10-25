#!/usr/bin/env python3
"""Independent deterministic checks for the Problem 1117 hostile audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tarfile
from pathlib import Path


DEFAULT_AUTHOR = Path(
    "/home/exedev/erdos_scratch/fresh12_erdos1117_maxmod_points_20260811"
)
AUTHOR = Path(os.environ.get("AUTHOR_BUNDLE", DEFAULT_AUTHOR))
EXPECTED_AUTHOR_MANIFEST = (
    "4332c124aa51e217254c7071fb346bf666f6bc610fa95dcb72d8d0c69a06ff73"
)
NUMBER = 1117


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_author_manifest() -> int:
    manifest = AUTHOR / "MANIFEST.sha256"
    require(manifest.is_file(), f"missing author manifest: {manifest}")
    require(sha256(manifest) == EXPECTED_AUTHOR_MANIFEST, "author manifest identity changed")

    checked = 0
    for line in manifest.read_text().splitlines():
        expected, relative = line.split("  ", 1)
        relative = relative.removeprefix("./")
        require(relative and not Path(relative).is_absolute(), f"unsafe manifest path: {relative}")
        require(".." not in Path(relative).parts, f"unsafe manifest path: {relative}")
        target = AUTHOR / relative
        require(target.is_file(), f"missing author file: {relative}")
        require(sha256(target) == expected, f"author hash mismatch: {relative}")
        checked += 1
    require(checked >= 15, "unexpectedly short author manifest")
    return checked


def read_tex(archive_name: str, member_suffix: str) -> str:
    archive = AUTHOR / "sources" / archive_name
    with tarfile.open(archive) as tf:
        names = [name for name in tf.getnames() if name.endswith(member_suffix)]
        require(len(names) == 1, f"expected one {member_suffix}: {names}")
        handle = tf.extractfile(names[0])
        require(handle is not None, f"could not extract {names[0]}")
        return handle.read().decode("utf-8", errors="strict")


def verify_gate_and_sources() -> None:
    source_dir = AUTHOR / "sources"
    index = (source_dir / "site_index_20260811.js").read_text()
    ledger = (source_dir / "site_ledger_data_20260811.js").read_text()

    exact_patterns = (
        rf"\bproblemNum\s*:\s*{NUMBER}\b",
        rf"\{{n\s*:\s*{NUMBER}\b",
    )
    for pattern in exact_patterns:
        require(not re.search(pattern, index), f"number collision in index: {pattern}")
        require(not re.search(pattern, ledger), f"number collision in ledger: {pattern}")

    combined = (index + "\n" + ledger).lower()
    for phrase in (
        "maximum modulus point",
        "maximum-modulus point",
        "maximum modulus set",
        "maximum-modulus set",
        "maximum curve",
    ):
        require(phrase not in combined, f"framework collision: {phrase}")

    live = json.loads((source_dir / "live_1117_20260811.json").read_text())
    pages = {page["requested_url"]: page["body_text"] for page in live["pages"]}
    main = pages["https://www.erdosproblems.com/1117"]
    claims = pages["https://www.erdosproblems.com/forum/thread/1117/proof-claims"]
    for phrase in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Currently working on this problem\tNone",
        "Interested in collaborating\tNone",
        "The second question is still open",
    ):
        require(phrase in main, f"live snapshot missing: {phrase}")
    require("No proof claims have been submitted yet." in claims, "proof claim exists")

    current = read_tex("arxiv_2607.09462v1_source.tar", "Erdos_finite_order_v8_arxiv.tex")
    required_current = (
        r"v_f(r)\defeq \#(\M(f)\cap\{|z|=r\})",
        r"There is an entire function \(f\in\B\), of finite order",
        r"\limsup_{r\to\infty} v_f(r)=\infty",
        r"The second part remains open",
        r"no useful control of \(v_f(r)\) away from the prescribed radii",
        r"v_f(e^{x_n})\ge 2n+1",
        r"Since \(x_n\to+\infty\)",
    )
    for phrase in required_current:
        require(phrase in current, f"2026 source quantifier missing: {phrase}")

    distinct_moduli = current.find("no two points have the same modulus")
    prescribed_point = current.find(r"\(z_n\in\M(f)\)", distinct_moduli)
    require(
        distinct_moduli >= 0 and prescribed_point >= distinct_moduli,
        "Theorem 1.2 distinct-moduli scope missing",
    )

    approximate = read_tex("arxiv_2208.11154v2_source.tar", "maxmod_revision3.tex")
    for phrase in (
        "it is theoretically possible",
        "is uniformly bounded",
        "unable to conclude",
    ):
        require(phrase in approximate, f"2024 non-solution disclaimer missing: {phrase}")


# A Gaussian integer is represented as (real, imaginary).
GI = tuple[int, int]


def gi_add(a: GI, b: GI) -> GI:
    return a[0] + b[0], a[1] + b[1]


def gi_mul(a: GI, b: GI) -> GI:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gi_conj(a: GI) -> GI:
    return a[0], -a[1]


def gi_scale(a: GI, scalar: int) -> GI:
    return a[0] * scalar, a[1] * scalar


def verify_endpoint_harmonic() -> int:
    """Exercise the endpoint identity with genuinely complex coefficients."""
    checked = 0
    endpoint_pairs = (((1, 2), (-2, 1)), ((-3, -1), (2, -2)), ((1, -1), (3, 2)))
    for m in range(5):
        for span in range(1, 8):
            d = m + span
            for left, right in endpoint_pairs:
                coefficients: dict[int, GI] = {m: left, d: right}
                for j in range(m + 1, d):
                    value = ((2 * j + span) % 5 - 2, (3 * j + m) % 5 - 2)
                    if value != (0, 0) and (j + span) % 3:
                        coefficients[j] = value
                for radius in (1, 2, 4):
                    fourier: dict[int, GI] = {}
                    for j, aj in coefficients.items():
                        for k, ak in coefficients.items():
                            term = gi_scale(gi_mul(aj, gi_conj(ak)), radius ** (j + k))
                            fourier[j - k] = gi_add(fourier.get(j - k, (0, 0)), term)
                    expected = gi_scale(gi_mul(right, gi_conj(left)), radius ** (d + m))
                    require(fourier[span] == expected, "endpoint Fourier coefficient failed")
                    require(expected != (0, 0), "endpoint Fourier coefficient vanished")
                    require(max(abs(freq) for freq, value in fourier.items() if value != (0, 0)) == span,
                            "Fourier degree differs from support span")
                    # Differentiating multiplies the top coefficient by i*span, so it stays nonzero.
                    derivative_top = (-span * expected[1], span * expected[0])
                    require(derivative_top != (0, 0), "derivative lost the top harmonic")
                    checked += 1
    return checked


def verify_complex_binomial_phases() -> int:
    """Count equality phases for arbitrary root-of-unity arguments of A and B."""
    checked = 0
    for span in range(1, 31):
        for phase_modulus in (5, 7, 11):
            grid = span * phase_modulus
            for phase_a in range(phase_modulus):
                for phase_b in range(phase_modulus):
                    solutions = [
                        k
                        for k in range(grid)
                        if (phase_b + k - phase_a) % phase_modulus == 0
                    ]
                    require(len(solutions) == span, "complex binomial phase count failed")
                    checked += 1
    return checked


def main() -> None:
    files = verify_author_manifest()
    verify_gate_and_sources()
    harmonic_checks = verify_endpoint_harmonic()
    phase_checks = verify_complex_binomial_phases()
    print(f"PASS author manifest: {files} files")
    print("PASS frozen exact-number/framework/live gates")
    print("PASS primary quantifiers: selected-radius limsup only; liminf open")
    print(f"PASS complex endpoint-harmonic identities: {harmonic_checks}")
    print(f"PASS complex binomial phase counts: {phase_checks}")
    print("NOTE cyclic critical-point proof, including q=1, is in AUDIT_REPORT.md")
    print("PASS hostile audit: narrow claims only")


if __name__ == "__main__":
    main()
