#!/usr/bin/env python3
"""Scan reflection centers for the posted 10-mark Golomb ruler."""

from collections import Counter

B = (0, 1, 6, 10, 23, 26, 34, 41, 53, 55)

for center in range(111, 1001):
    points = tuple(sorted(B + tuple(center - b for b in B)))
    if len(set(points)) != 20:
        continue
    counts = Counter(
        points[i] + points[j]
        for i in range(20)
        for j in range(i, 20)
    )
    repeated = {s: c for s, c in counts.items() if c > 1}
    if len(repeated) <= 1:
        print(f"first center={center}")
        print("witness=" + " ".join(map(str, points)))
        print("repeated=" + repr(repeated))
        break
else:
    raise SystemExit("no center found through 1000")
