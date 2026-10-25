#!/usr/bin/env python3
"""Audit the frozen local-site snapshots for exact and framework collisions."""

from hashlib import sha256
from pathlib import Path
import re


BASE = Path(__file__).resolve().parent.parent
SNAPSHOTS = {
    BASE / "provenance" / "site_index_20260811.js":
        "b7111451218492db6756cc88dde0a8b98700d4c6f47e476171a02950b6d9af8b",
    BASE / "provenance" / "site_ledger_data_20260811.js":
        "9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052",
}
NUMBER_PATTERN = re.compile(
    r'(?:\bn\s*:|\bproblem\s*:|erdosproblems(?:\\\\)?\.com/)'
    r'\s*["\']?(\d+)',
    re.IGNORECASE,
)
FRAMEWORK_PHRASES = [
    "monotone arithmetic progression",
    "monotone 4-term",
    "monotone 3-term",
    "monotone ap",
    "permutation avoiding",
    "permutations avoiding",
    "4-ap-free permutation",
    "3-ap-free permutation",
    "HasMonotoneAP",
]


def main():
    discrepancies = 0
    exact_196_total = 0
    framework_total = 0

    for path, expected_digest in SNAPSHOTS.items():
        data = path.read_bytes()
        digest = sha256(data).hexdigest()
        digest_match = digest == expected_digest
        discrepancies += not digest_match

        text = data.decode("utf-8")
        numbers = [int(value) for value in NUMBER_PATTERN.findall(text)]
        exact_count = numbers.count(196)
        exact_196_total += exact_count

        print(
            f"snapshot={path.name} sha256={digest} "
            f"digest_match={int(digest_match)} "
            f"distinct_structured_numbers={len(set(numbers))} "
            f"exact_196_count={exact_count}"
        )

        lowered = text.lower()
        for phrase in FRAMEWORK_PHRASES:
            count = lowered.count(phrase.lower())
            framework_total += count
            print(f"snapshot={path.name} phrase={phrase!r} count={count}")

    discrepancies += exact_196_total != 0
    discrepancies += framework_total != 0
    print(f"exact_196_total={exact_196_total}")
    print(f"framework_phrase_total={framework_total}")
    print(f"audit_discrepancies={discrepancies}")
    raise SystemExit(discrepancies != 0)


if __name__ == "__main__":
    main()
