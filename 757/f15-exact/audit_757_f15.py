#!/usr/bin/env python3
"""Second, deliberately independent audit of the A15 witness for #757.

Unlike verify_a15.py, this script proves h(A15)=9 by checking just the
critical layers: every C(15,10)=3,003 ten-subset fails the Sidon definition,
and one displayed nine-subset passes it.  It evaluates the live |B-B|
predicate literally for every C(15,4)=1,365 quadruple.
"""

from collections import Counter
from itertools import combinations
from math import comb


A = (0, 136, 200, 243, 246, 249, 272, 286,
     298, 323, 400, 528, 596, 1056, 1057)

WITNESS = (0, 136, 200, 243, 246, 298, 323, 528, 1057)


def live_difference_count(block):
    """Literal cardinality of B-B, including zero and both signs."""
    return len({x - y for x in block for y in block})


def sidon_by_sums(block):
    """All unordered sums x+y (allowing x=y) occur once."""
    totals = [block[i] + block[j]
              for i in range(len(block)) for j in range(i, len(block))]
    return len(totals) == len(set(totals))


def sidon_by_distances(block):
    """Equivalent Golomb-ruler formulation, implemented independently."""
    distances = [y - x for x, y in combinations(block, 2)]
    return len(distances) == len(set(distances))


def main():
    assert len(A) == 15 and len(set(A)) == 15 and tuple(sorted(A)) == A

    live_hist = Counter(live_difference_count(b) for b in combinations(A, 4))
    assert sum(live_hist.values()) == comb(15, 4) == 1365
    assert min(live_hist) >= 11
    assert live_hist == {11: 144, 13: 1221}

    # Check all 3,003 critical ten-subsets via two separate Sidon predicates.
    ten_count = sum_sidon = distance_sidon = disagreements = 0
    first_sum_collision = None
    for block in combinations(A, 10):
        ten_count += 1
        by_sums = sidon_by_sums(block)
        by_distances = sidon_by_distances(block)
        sum_sidon += by_sums
        distance_sidon += by_distances
        disagreements += by_sums != by_distances
        if first_sum_collision is None and not by_sums:
            first_sum_collision = block
    assert ten_count == comb(15, 10) == 3003
    assert sum_sidon == distance_sidon == disagreements == 0

    # One explicit lower witness, checked in both formulations.
    assert len(WITNESS) == 9 and set(WITNESS) <= set(A)
    assert sidon_by_sums(WITNESS)
    assert sidon_by_distances(WITNESS)

    # Structural diagnostics, calculated afresh.
    distinct_pair_sums = [x + y for x, y in combinations(A, 2)]
    assert len(distinct_pair_sums) == len(set(distinct_pair_sums)) == 105
    aps = tuple(t for t in combinations(A, 3) if t[0] + t[2] == 2*t[1])
    assert len(aps) == 12
    assert all(1057 not in t for t in aps)
    assert all(len(set(e) & set(f)) <= 1 for e, f in combinations(aps, 2))

    print("live |B-B| histogram:", dict(sorted(live_hist.items())))
    print("quadruples:", comb(15, 4))
    print("ten-subsets checked:", ten_count)
    print("Sidon ten-subsets (sum/distance):", sum_sidon, distance_sidon)
    print("predicate disagreements:", disagreements)
    print("explicit Sidon nine-set:", WITNESS)
    print("distinct-element pair sums:", len(set(distinct_pair_sums)))
    print("AP triples:", aps)
    print("INDEPENDENT AUDIT PASSED: h(A)=9 and A satisfies live (4,5) predicate")


if __name__ == "__main__":
    main()
