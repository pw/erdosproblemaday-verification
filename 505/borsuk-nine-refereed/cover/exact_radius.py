#!/usr/bin/env python3
"""Exact covering radius of n lines (rational unit centres): cos^2(rho) = 1/(2M), M = max |v|^2 over vertices of
P = {x : <x,c_i>^2 <= 1/2} (same enumeration as verify_cover.py; the vertex set does not depend on the 1/2, only the scale).
Prints M as an exact fraction and rho in degrees. Used for the 10-line upper bracket."""
import json, sys, math
from verify_cover import rational_unit, certify
d = json.load(open(sys.argv[1])); C = [rational_unit(v) for v in d['centres']]
M, arg, nf = certify(C)
print(f"n={len(C)} M={float(M):.15f} exact_den_digits={len(str(M.denominator))} cos^2(rho)=1/(2M)={float(1/(2*M)):.15f} rho={math.degrees(math.acos(math.sqrt(float(1/(2*M))))):.6f} deg")
json.dump({'centres_rational': [[str(a) for a in c] for c in C], 'M': str(M)}, open(sys.argv[1].replace('.json', '.exact.json'), 'w'))
