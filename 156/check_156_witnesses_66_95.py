#!/usr/bin/env python3
"""Direct finite certificates for the upper bounds A382397(66)..A382397(95)."""

from hashlib import sha256

WITNESSES = {
    66: (21, 25, 31, 40, 43, 60),
    67: (16, 23, 35, 38, 44, 55),
    68: (16, 23, 35, 38, 44, 55, 68),
    69: (13, 24, 30, 33, 45, 52, 68),
    70: (6, 32, 34, 37, 38, 47, 54),
    71: (14, 16, 30, 38, 43, 47, 53),
    72: (18, 30, 32, 33, 40, 49, 53),
    73: (5, 30, 41, 42, 60, 64, 69),
    74: (9, 12, 23, 35, 40, 42, 62),
    75: (9, 12, 28, 30, 39, 40, 63),
    76: (4, 12, 30, 31, 33, 47, 53),
    77: (19, 27, 31, 34, 52, 63, 65),
    78: (15, 25, 36, 37, 40, 42, 72),
    79: (15, 26, 33, 45, 49, 55, 58),
    80: (30, 35, 38, 44, 45, 69, 71),
    81: (22, 30, 31, 37, 51, 53, 56),
    82: (22, 34, 38, 39, 41, 64, 75),
    83: (20, 29, 35, 46, 48, 60, 64),
    84: (7, 29, 39, 53, 56, 60, 62),
    85: (25, 28, 30, 48, 49, 55, 63),
    86: (12, 34, 42, 45, 47, 63, 73),
    87: (18, 42, 43, 45, 49, 59, 81),
    88: (22, 24, 35, 42, 45, 59, 64),
    89: (27, 35, 38, 52, 56, 58, 82),
    90: (29, 32, 34, 51, 55, 64, 84),
    91: (11, 27, 30, 34, 48, 58, 59),
    92: (11, 35, 43, 45, 49, 54, 80),
    93: (18, 39, 42, 50, 54, 56, 87),
    94: (12, 37, 45, 47, 51, 58, 81),
    95: (30, 31, 33, 48, 55, 59, 93),
}


def old_pair_sums(a):
    result = {}
    for i, left in enumerate(a):
        for right in a[i:]:
            value = left + right
            if value in result:
                raise AssertionError(f"repeated old sum {value}: {result[value]} and {(left, right)}")
            result[value] = (left, right)
    return result


def insertion_collision(a, sums, x):
    for mark in a:
        if x + mark in sums:
            left, right = sums[x + mark]
            return f"{x}+{mark}={left}+{right}"
    if 2 * x in sums:
        left, right = sums[2 * x]
        return f"{x}+{x}={left}+{right}"
    return None


def check(n, a):
    expected_size = 6 if n <= 67 else 7
    assert len(a) == expected_size
    assert tuple(sorted(a)) == a and len(set(a)) == len(a)
    assert 1 <= a[0] and a[-1] <= n
    sums = old_pair_sums(a)
    assert len(sums) == len(a) * (len(a) + 1) // 2
    collisions = []
    for x in range(1, n + 1):
        if x in a:
            continue
        collision = insertion_collision(a, sums, x)
        assert collision is not None, f"{n=} {a=} addable {x=}"
        collisions.append(f"x={x}:{collision}")
    digest = sha256("\n".join(collisions).encode("ascii")).hexdigest()
    print(f"n={n} size={len(a)} witness={a} collision_sha256={digest}")


if __name__ == "__main__":
    assert tuple(WITNESSES) == tuple(range(66, 96))
    for domain_size, witness in WITNESSES.items():
        check(domain_size, witness)
    print("CONCLUSION all upper-bound witnesses for n=66..95 pass direct pair-sum checks")
