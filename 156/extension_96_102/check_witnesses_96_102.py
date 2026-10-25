#!/usr/bin/env python3
"""Direct certificates for the new A382397 values 96 through 102."""

from hashlib import sha256


RULER = (0, 24, 27, 35, 39, 41, 75)
WITNESSES = {
    96: (13, 37, 40, 48, 52, 54, 88),
    97: (14, 38, 41, 49, 53, 55, 89),
    98: (15, 39, 42, 50, 54, 56, 90),
    99: (16, 40, 43, 51, 55, 57, 91),
    100: (17, 41, 44, 52, 56, 58, 92),
    101: (18, 42, 45, 53, 57, 59, 93),
    102: (10, 33, 38, 42, 59, 69, 71, 89),
}


def sidon(values: tuple[int, ...]) -> bool:
    sums: set[int] = set()
    for i, left in enumerate(values):
        for right in values[i:]:
            total = left + right
            if total in sums:
                return False
            sums.add(total)
    return True


def blocked(values: tuple[int, ...], candidate: int) -> bool:
    return not sidon(tuple(sorted(values + (candidate,))))


def main() -> None:
    assert sidon(RULER)
    assert all(blocked(RULER, x) for x in range(-17, 84) if x not in RULER)
    assert not blocked(RULER, -18)
    assert not blocked(RULER, 84)

    transcript: list[str] = []
    for n, values in WITNESSES.items():
        assert len(values) == (7 if n <= 101 else 8)
        assert len(set(values)) == len(values)
        assert min(values) >= 1 and max(values) <= n
        assert sidon(values)
        outside = 0
        for candidate in range(1, n + 1):
            if candidate in values:
                continue
            assert blocked(values, candidate)
            outside += 1
        if n <= 101:
            assert values == tuple(x + n - 83 for x in RULER)
        record = f"n={n} k={len(values)} outside={outside} witness={values}"
        transcript.append(record)
        print(record)

    digest = sha256(("\n".join(transcript) + "\n").encode()).hexdigest()
    print(f"transcript_sha256={digest}")
    print("WITNESS_CHECK=PASS")


if __name__ == "__main__":
    main()
