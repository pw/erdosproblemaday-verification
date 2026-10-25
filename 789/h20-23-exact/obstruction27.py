#!/usr/bin/env python3
"""Exact check: A = {0} ∪ ±P, P = {1,2,3,4,5,6,8,9,10,12,14,15,17} (27 integers): an admissible 5-subset exists and
none of the 296,010 six-subsets is admissible (literal definition) => H(A) = 5 => h(27) <= 5."""
import itertools, sys
from hcheck import admissible
P = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 17]
A = sorted(set(P + [-x for x in P] + [0])); assert len(A) == 27
five = next(S for S in itertools.combinations(A, 5) if admissible(S))
total = 0; six = 0
for S in itertools.combinations(A, 6):
    total += 1
    if admissible(S): six += 1
print("A =", A); print("an admissible 5-subset:", five); print("admissible 6-subsets among", total, ":", six)
print("H(A) = 5  =>  h(27) <= 5" if six == 0 else "FAILED"); sys.exit(0 if six == 0 else 1)
