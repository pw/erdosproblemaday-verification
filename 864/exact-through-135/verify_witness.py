#!/usr/bin/env python3
"""Direct pair-count check for the new 19-point witness."""

from collections import Counter


WITNESS = (
    0, 4, 5, 7, 17, 33, 44, 52, 58, 67,
    76, 82, 90, 101, 117, 127, 129, 130, 134,
)


def main() -> None:
    assert len(WITNESS) == 19
    assert len(set(WITNESS)) == 19
    assert WITNESS[0] == 0 and WITNESS[-1] == 134
    counts = Counter(
        WITNESS[i] + WITNESS[j]
        for i in range(len(WITNESS))
        for j in range(i, len(WITNESS))
    )
    repeated = {s: c for s, c in sorted(counts.items()) if c > 1}
    assert repeated == {134: 10}
    print("WITNESS", *WITNESS)
    print("size=19 diameter=134 repeated_sums={134: 10} PASS")


if __name__ == "__main__":
    main()
