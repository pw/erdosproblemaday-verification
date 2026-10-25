#!/usr/bin/env python3
"""Exact check: A = {0} ∪ ±P with P = {1,3,4,5,6,8,9,10,12,14,15,17} (25 integers) has H(A) = 5:
an admissible 5-subset exists, and none of the 177,100 six-subsets is admissible (literal definition)."""
import itertools, sys
from hcheck import admissible
P = [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 17]
A = sorted(set(P + [-x for x in P] + [0])); assert len(A) == 25
five = next(S for S in itertools.combinations(A, 5) if admissible(S))
six = sum(1 for S in itertools.combinations(A, 6) if admissible(S))
print("A =", A); print("an admissible 5-subset:", five); print("admissible 6-subsets among", sum(1 for _ in itertools.combinations(A, 6)), ":", six)
print("H(A) = 5  =>  h(25) <= 5" if six == 0 else "FAILED")
sys.exit(0 if six == 0 else 1)
