#!/usr/bin/env python3
"""Exact finite values for #757 from explicit scale-separated blocks.

Only the Python standard library is used.  The constructions are checked
literally against the live |B-B| predicate on every quadruple.  Their exact
Sidon numbers are certified by a blockwise upper bound plus a directly
checked matching Sidon witness.
"""

from collections import Counter
from itertools import combinations


A3 = (0, 97, 194)
A12 = (0, 97, 161, 194, 227, 322, 374, 454, 521, 534, 547, 720)
A14 = (0, 136, 200, 243, 246, 249, 272,
       286, 298, 323, 400, 528, 596, 1056)


def is_sidon(values):
    seen = set()
    for i, x in enumerate(values):
        for y in values[i:]:
            total = x + y
            if total in seen:
                return False
            seen.add(total)
    return True


def max_sidon(values):
    for size in range(len(values), -1, -1):
        for subset in combinations(values, size):
            if is_sidon(subset):
                return size, subset
    raise AssertionError


def combine(left, right, scale=1000):
    """A concrete separated union satisfying the elementary lemma below."""
    assert left[0] == right[0] == 0
    left_span = left[-1]
    right_span = right[-1]
    right_gap = min(y - x for x, y in zip(right, right[1:]))
    assert scale * right_gap > left_span
    translate = left_span + scale * right_span + 1
    shifted = tuple(translate + scale * y for y in right)
    assert left[-1] < shifted[0]
    return left + shifted, shifted, scale, translate


def signed_difference_histogram(values):
    hist = Counter()
    for quad in combinations(values, 4):
        hist[len({x - y for x in quad for y in quad})] += 1
    return dict(sorted(hist.items()))


def weak_sidon(values):
    sums = [x + y for x, y in combinations(values, 2)]
    return len(sums) == len(set(sums))


def ap_edges(values):
    return tuple(t for t in combinations(values, 3)
                 if t[0] + t[2] == 2*t[1])


def audit_case(name, left, right, expected_n, expected_h):
    values, shifted, scale, translate = combine(left, right)
    assert len(values) == expected_n

    # Direct live predicate on every quadruple.
    histogram = signed_difference_histogram(values)
    assert sum(histogram.values()) == sum(1 for _ in combinations(values, 4))
    assert min(histogram) >= 11

    # Structural diagnostics independently verify the scale-separation proof.
    assert weak_sidon(values)
    left_edges = set(ap_edges(left))
    shifted_edges = {
        tuple(translate + scale*x for x in edge) for edge in ap_edges(right)
    }
    edges = set(ap_edges(values))
    assert edges == left_edges | shifted_edges
    assert all(len(set(e) & set(f)) <= 1 for e, f in combinations(edges, 2))

    # Exhaust each component.  Any Sidon subset of the union intersects each
    # component in a Sidon subset, so h(union) <= h(left)+h(right).  The union
    # of the displayed component witnesses is checked directly and matches.
    h_left, witness_left = max_sidon(left)
    h_right, witness_right = max_sidon(right)
    witness = witness_left + tuple(translate + scale*x for x in witness_right)
    assert is_sidon(witness)
    exact_h = h_left + h_right
    assert len(witness) == exact_h == expected_h

    # Named-theorem lower-bound arithmetic from the wave-7k report.
    lower = expected_n - (8*expected_n - 6)//17
    assert lower == exact_h

    result = {
        "name": name,
        "n": expected_n,
        "h": exact_h,
        "lower": lower,
        "scale": scale,
        "translate": translate,
        "values": values,
        "quadruples": sum(histogram.values()),
        "difference_histogram": histogram,
        "weak_pair_sums": expected_n*(expected_n-1)//2,
        "ap_edges": tuple(sorted(edges)),
        "witness": witness,
        "component_h": (h_left, h_right),
    }
    return result


def main():
    cases = (
        ("A14+A3", A14, A3, 17, 10),
        ("A12+A12", A12, A12, 24, 14),
        ("A14+A12", A14, A12, 26, 15),
        ("A14+A14", A14, A14, 28, 16),
    )
    for args in cases:
        result = audit_case(*args)
        print("CASE", result["name"])
        print("  A =", result["values"])
        print("  n / exact h / named lower =",
              result["n"], result["h"], result["lower"])
        print("  scale / translate =", result["scale"], result["translate"])
        print("  quadruples / |B-B| histogram =",
              result["quadruples"], result["difference_histogram"])
        print("  distinct-element pair sums =", result["weak_pair_sums"])
        print("  AP edges =", result["ap_edges"])
        print("  component h =", result["component_h"])
        print("  Sidon witness =", result["witness"])
    print("VERIFIED: f(17)=10, f(24)=14, f(26)=15, f(28)=16")


if __name__ == "__main__":
    main()
