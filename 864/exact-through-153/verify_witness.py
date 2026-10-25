#!/usr/bin/env python3
"""Definition-level checks for the 20-point Problem #864 witness."""

from collections import Counter
from itertools import combinations


B = (0, 1, 6, 10, 23, 26, 34, 41, 53, 55)
W = tuple(sorted(B + tuple(152 - b for b in B)))
EXPECTED = (
    0, 1, 6, 10, 23, 26, 34, 41, 53, 55,
    97, 99, 111, 118, 126, 129, 142, 146, 151, 152,
)
W19 = (
    0, 4, 5, 7, 17, 33, 44, 52, 58, 67,
    76, 82, 90, 101, 117, 127, 129, 130, 134,
)
DIRECT_CONTROL = (
    0, 1, 3, 8, 14, 26, 30, 47, 62, 71,
    81, 90, 105, 122, 126, 138, 144, 149, 151, 152,
)


def unordered_sum_counts(points):
    return Counter(
        points[i] + points[j]
        for i in range(len(points))
        for j in range(i, len(points))
    )


assert W == EXPECTED
assert len(W) == len(set(W)) == 20
assert W[0] == 0 and W[-1] == 152

# Independently check that the source 10-mark set is a Golomb ruler.
differences = [b - a for a, b in combinations(B, 2)]
assert len(differences) == 45
assert len(set(differences)) == 45
assert min(differences) == 1 and max(differences) == 55

counts = unordered_sum_counts(W)
repeated = {s: c for s, c in counts.items() if c > 1}
assert sum(counts.values()) == 210
assert repeated == {152: 10}
representations = [
    (W[i], W[j])
    for i in range(20)
    for j in range(i, 20)
    if W[i] + W[j] == 152
]
assert representations == [
    (0, 152), (1, 151), (6, 146), (10, 142), (23, 129),
    (26, 126), (34, 118), (41, 111), (53, 99), (55, 97),
]

translated = tuple(x + 1 for x in W)
translated_counts = unordered_sum_counts(translated)
assert {s: c for s, c in translated_counts.items() if c > 1} == {154: 10}
assert translated[0] == 1 and translated[-1] == 153

counts19 = unordered_sum_counts(W19)
assert sum(counts19.values()) == 190
assert {s: c for s, c in counts19.items() if c > 1} == {134: 10}

control_counts = unordered_sum_counts(DIRECT_CONTROL)
assert sum(control_counts.values()) == 210
assert {s: c for s, c in control_counts.items() if c > 1} == {152: 10}

print("source Golomb ruler: 10 marks, 45 distinct positive differences, PASS")
print("normalized witness:", " ".join(map(str, W)))
print("unordered pairs with diagonal: 210")
print("only repeated sum: 152, representations: 10")
print("translated witness lies in [1,153], only repeated sum: 154")
print("prior 19-point witness: diameter 134, only repeated sum 134 (10 reps), PASS")
print("direct-search positive control at diameter 152: sole repeat 152 (10 reps), PASS")
print("ALL WITNESS CHECKS PASSED")
