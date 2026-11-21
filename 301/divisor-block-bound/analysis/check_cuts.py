#!/usr/bin/env python3
"""Every saved CP-SAT cut must be a genuine equation 1/a = sum 1/b over distinct divisors of M (exact Fractions)."""
import json, glob, sys
from fractions import Fraction
tot = bad = 0
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else 'profile/partial_*.json')):
    J = json.load(open(f)); M = J['M']
    for c in J['constraints']:
        c = sorted(c); tot += 1
        bad += not (len(c) >= 3 and len(set(c)) == len(c) and all(M % x == 0 for x in c)
                    and Fraction(1, c[0]) == sum(Fraction(1, b) for b in c[1:]))
print('cuts', tot, 'non-genuine', bad); sys.exit(1 if bad else 0)
