#!/usr/bin/env python3
"""Cross-check every k=8 census orbit (kernel dim 1 over Frac) with the minor-limit instrument; print agreement."""
import re
from fractions import Fraction as Fr
from minor_check import limit_vector
agree = dis = 0
for line in open('census_k8.log'):
    m = re.match(r"k=8 \(([\d, ]+)\): .*kernel_dim_over_Frac=(\d+) .*criterion=(\w+)", line)
    if not m: continue
    S = tuple(int(x) for x in m.group(1).split(',')); kd = int(m.group(2)); v1 = m.group(3)
    if kd != 1: print(S, 'kernel dim', kd, 'skipped'); continue
    vs = []
    for x0 in (Fr(2, 7), Fr(-5, 3)):
        mm, L = limit_vector(S, x0)
        a11, a12, a21, a22 = L[4], L[5], L[7], L[8]
        vs.append('HOLDS' if (a12 == 0 and a21 == 0 and a11 == a22 and a11 != 0) else 'FAILS')
    ok = all(v == v1 for v in vs); agree += ok; dis += (not ok)
    print(S, 'census', v1, 'minors', vs, 'AGREE' if ok else 'DISAGREE', flush=True)
print(f"SUMMARY agree {agree} disagree {dis}")
