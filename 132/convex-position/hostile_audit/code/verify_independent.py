#!/usr/bin/env python3
"""Independent exact checks for the second hostile audit of Problem 132."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from math import comb
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT.parent
BUNDLE = RUN / "bundle_ro"
PRIVATE_FISHBURN = RUN / "private_source_cache" / "fishburn1995_vor.pdf"

INPUT_MANIFEST_SHA256 = (
    "4e2716c6aec0c0a50d1ffc64286559cccef3cdbc28c33e409a08a71d5965d4b7"
)
INPUT_ARCHIVE_SHA256 = (
    "a738c216386c79d09ab3fb77bb7feb69168d9ceca6a8a853c99d79e90f8736a1"
)
FISHBURN_SHA256 = (
    "b63a4ff8d00e4b2fcc7acc68924c0975ffc9d4a640ce7c1962f2781525053935"
)
EXPECTED_CLAIM = (
    "For every set A of n >= 5 distinct points in the Euclidean plane such "
    "that every point of A is a vertex of conv(A), there is a distance d "
    "strictly smaller than the diameter of A for which between 1 and n "
    "unordered pairs of points of A are at distance d.\n\n"
    "No assertion is made here for arbitrary planar point sets, for the "
    "number of qualifying distances as n tends to infinity, or for any "
    "unaudited claim in the live discussion thread.  Full unrestricted "
    "Erdos Problem 132 remains OPEN/GAP."
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def check_input_integrity() -> None:
    manifest = BUNDLE / "MANIFEST.sha256"
    assert digest(manifest) == INPUT_MANIFEST_SHA256
    entries = []
    for line in manifest.read_text(encoding="ascii").splitlines():
        expected, raw_name = line.split("  ", 1)
        name = raw_name.removeprefix("./")
        relative = Path(name)
        assert not relative.is_absolute() and ".." not in relative.parts
        path = BUNDLE / relative
        assert path.is_file(), relative
        assert digest(path) == expected, relative
        entries.append(relative)
    assert len(entries) == 45
    assert digest(RUN / "bundle_ro.tar.gz") == INPUT_ARCHIVE_SHA256


def check_private_fishburn() -> None:
    assert PRIVATE_FISHBURN.stat().st_size == 1_798_795
    assert PRIVATE_FISHBURN.read_bytes().startswith(b"%PDF-")
    assert digest(PRIVATE_FISHBURN) == FISHBURN_SHA256


def check_primary_statements() -> None:
    tex = (BUNDLE / "sources/cdliu_v5_main.tex").read_text(encoding="utf-8")
    for needle in (
        r"Let $n\geq5$. For any convex point set $X\subseteq\mathbb{R}^2$",
        r"$X$ determines at least $\lfloor n/2 \rfloor$ distinct distances",
        r"for $n=6$, there exist exactly two possibilities, $a(X)=(6,6,3)$, or $a(X)=(5,5,5)$",
        r"for $n \geq 8$, either $X =R_n$ or $X=R_{n+1}^-$",
        r"\left\lfloor \frac{n}{2} \right\rfloor (n+1) + 1 > {n \choose 2}",
    ):
        assert needle in tex, needle

    published = (BUNDLE / "sources/cdliu_published.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "Theorem 1.2. Let n >= 5." not in published  # source uses a Unicode >= sign
    assert "Theorem 1.2. Let n \u2265 5. For any convex point set" in published
    assert "Proof of Theorem 1.2." in published

    altman = (BUNDLE / "sources/altman1972.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "THEOREM 3. In every plane strictly convex n-sided polygon" in altman


def polynomial_subtract(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        - (right[i] if i < len(right) else 0)
        for i in range(width)
    )


def check_counting_branch() -> None:
    # Coefficients are in increasing powers of k.  These identities prove the
    # gap formulas symbolically rather than extrapolating from a finite loop.
    even_forced = (1, 1, 2)  # k(2k+1)+1
    even_pairs = (0, -1, 2)  # C(2k,2)
    odd_forced = (1, 2, 2)  # k(2k+2)+1
    odd_pairs = (0, 1, 2)  # C(2k+1,2)
    assert polynomial_subtract(even_forced, even_pairs) == (1, 2, 0)
    assert polynomial_subtract(odd_forced, odd_pairs) == (1, 1, 0)

    for n in range(5, 10_001):
        forced = (n // 2) * (n + 1) + 1
        gap = forced - comb(n, 2)
        expected = n + 1 if n % 2 == 0 else (n + 1) // 2
        assert gap == expected > 0


def cyclic_step_counts(order: int, deleted: int | None = None) -> Counter[int]:
    vertices = [vertex for vertex in range(order) if vertex != deleted]
    counts: Counter[int] = Counter()
    for index, left in enumerate(vertices):
        for right in vertices[index + 1 :]:
            delta = (right - left) % order
            counts[min(delta, order - delta)] += 1
    return counts


def check_models_and_boundary_cases() -> None:
    pentagon = cyclic_step_counts(5)
    assert pentagon == Counter({1: 5, 2: 5})
    assert pentagon[1] == 5  # step 1 is non-diametral; step 2 is maximal

    for vector in ((6, 6, 3), (5, 5, 5)):
        assert len(vector) == 3 and sum(vector) == comb(6, 2)
        # The vector is frequency-sorted, not distance-sorted.  This assertion
        # checks the conclusion for every possible position of the diameter.
        for diameter_index in range(3):
            non_diameter = [
                value for index, value in enumerate(vector) if index != diameter_index
            ]
            assert non_diameter and min(non_diameter) <= 6

    for n in range(5, 201):
        counts = cyclic_step_counts(n)
        assert sum(counts.values()) == comb(n, 2)
        if n % 2:
            maximum_step = (n - 1) // 2
            assert counts == Counter({step: n for step in range(1, maximum_step + 1)})
            assert any(counts[step] <= n for step in range(1, maximum_step))
        else:
            maximum_step = n // 2
            expected = {step: n for step in range(1, maximum_step)}
            expected[maximum_step] = n // 2
            assert counts == Counter(expected)
            assert any(counts[step] <= n for step in range(1, maximum_step))

    for n in range(8, 102, 2):
        order = n + 1
        maximum_step = n // 2
        for deleted in range(order):
            counts = cyclic_step_counts(order, deleted)
            assert sum(counts.values()) == comb(n, 2)
            assert counts == Counter(
                {step: n - 1 for step in range(1, maximum_step + 1)}
            )
            assert any(counts[step] <= n for step in range(1, maximum_step))


def object_numbers(text: str) -> set[int]:
    numbers = {int(value) for value in re.findall(r"\bproblemNum\s*:\s*(\d+)", text)}
    numbers.update(int(value) for value in re.findall(r"\{\s*n\s*:\s*(\d+)", text))
    return numbers


def check_claim_boundary() -> None:
    claim = (ROOT / "CLAIM.txt").read_text(encoding="ascii").strip()
    assert claim == EXPECTED_CLAIM


def check_frozen_scope() -> None:

    for relative in ("site_snapshot/index.js", "site_snapshot/ledger_data.js"):
        text = (BUNDLE / relative).read_text(encoding="utf-8")
        assert 132 not in object_numbers(text)
        lowered = text.lower()
        for needle in (
            "2505.04283",
            "10.1007/s10474-025-01562-y",
            "on multiplicities of interpoint",
            "all distances except the diameter",
            "other than the diameter",
        ):
            assert needle not in lowered, (relative, needle)

    live = (BUNDLE / "provenance/problem132_live_recheck.md").read_text(
        encoding="utf-8"
    )
    claims = (BUNDLE / "provenance/problem132_claims_recheck.md").read_text(
        encoding="utf-8"
    )
    assert "OPEN  This is open" in live
    assert "No proof claims have been submitted yet." in claims

    yaml = (BUNDLE / "site_snapshot/problems.yaml").read_text(encoding="utf-8")
    match = re.search(r'^- number: "132"\n.*?(?=^- number: ")', yaml, re.M | re.S)
    assert match
    assert re.search(r"status:\n\s+state: \"open\"", match.group(0))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-input",
        action="store_true",
        help="fail unless the restricted sibling input bundle is available",
    )
    parser.add_argument(
        "--require-private",
        action="store_true",
        help="fail unless the private Fishburn VOR is available",
    )
    return parser.parse_args()


def main() -> None:
    if not __debug__:
        raise RuntimeError("Python assertions must remain enabled")
    args = parse_args()

    check_claim_boundary()
    print("exact approved claim and OPEN/GAP boundary: PASS")

    if BUNDLE.is_dir():
        check_input_integrity()
        print("input manifest (45 entries) and archive hashes: PASS")
        check_primary_statements()
        print("frozen primary theorem/classification statements: PASS")
        check_frozen_scope()
        print("frozen OPEN and site-collision scope: PASS")
    elif args.require_input:
        raise FileNotFoundError(f"required frozen input bundle is absent: {BUNDLE}")
    else:
        print("restricted sibling input bundle absent: SKIP source/snapshot checks")

    if PRIVATE_FISHBURN.is_file():
        check_private_fishburn()
        print("private Fishburn VOR hash: PASS")
    elif args.require_private:
        raise FileNotFoundError(
            f"required private Fishburn VOR is absent: {PRIVATE_FISHBURN}"
        )
    else:
        print("private Fishburn VOR absent: SKIP private-source hash check")

    check_counting_branch()
    print("all-n parity identities and 5 <= n <= 10000 diagnostics: PASS")
    check_models_and_boundary_cases()
    print("n=5, n=6, regular, and every deleted-vertex model diagnostic: PASS")
    print("ALL INDEPENDENT HOSTILE-AUDIT CHECKS PASSED")


if __name__ == "__main__":
    main()
