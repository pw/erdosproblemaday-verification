#!/usr/bin/env python3
"""Independent difference-based replay of the frozen n=66..95 witnesses."""

from hashlib import sha256
from pathlib import Path
from runpy import run_path


BUNDLE_ROOT = Path(__file__).resolve().parent.parent
WITNESSES = run_path(BUNDLE_ROOT / "check_156_witnesses_66_95.py")["WITNESSES"]


def positive_differences(values):
    return [
        values[right] - values[left]
        for right in range(1, len(values))
        for left in range(right)
    ]


def main():
    assert tuple(WITNESSES) == tuple(range(66, 96))
    witness_pairs = 0
    insertion_tests = 0
    enlarged_pairs = 0
    transcript = []

    for n, witness in WITNESSES.items():
        assert tuple(sorted(witness)) == witness
        assert len(witness) == (6 if n <= 67 else 7)
        assert witness[0] >= 1 and witness[-1] <= n

        differences = positive_differences(witness)
        assert len(differences) == len(set(differences))
        witness_pairs += len(differences)

        for x in range(1, n + 1):
            if x in witness:
                continue
            enlarged = tuple(sorted(witness + (x,)))
            enlarged_differences = positive_differences(enlarged)
            distinct = len(set(enlarged_differences))
            assert distinct < len(enlarged_differences), (n, witness, x)
            insertion_tests += 1
            enlarged_pairs += len(enlarged_differences)
            transcript.append(f"{n}:{x}:{len(enlarged_differences) - distinct}")

    digest = sha256("\n".join(transcript).encode("ascii")).hexdigest()
    print(
        f"witnesses={len(WITNESSES)} base_difference_pairs={witness_pairs} "
        f"forbidden_insertions={insertion_tests} enlarged_difference_pairs={enlarged_pairs}"
    )
    print(f"independent_difference_transcript_sha256={digest}")
    print("DIRECT_WITNESS_REPLAY=PASS")


if __name__ == "__main__":
    main()
