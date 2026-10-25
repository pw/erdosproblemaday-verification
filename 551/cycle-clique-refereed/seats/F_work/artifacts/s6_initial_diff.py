#!/usr/bin/env python3
"""Regenerates seat F's S6 figure: over all 3,099 patterns, how many initial forbidden-parameter matrices change when the
degree-<=1 test of Lemma 9.4 is deleted (mut/S6_no_degree_test.py) vs the unmodified original checker (orig_lib.py)."""
import importlib.util, sys
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
D = '/tmp/oaimath/189/seats/F_work/'
O = load('orig', D + 'orig_lib.py'); S = load('s6', D + 'mut/S6_no_degree_test.py')
tot = diff = 0
for k in range(5, 18):
    for t in range(max(3, k // 2), min(8, k) + 1):
        for P in O.forests(t, k - t):
            tot += 1
            a = O.initial(k, t, P); b = S.initial(k, t, P)
            if repr(a) != repr(b): diff += 1
print(f'patterns {tot}; initial matrices that differ (S6 vs original) {diff}')
sys.exit(0 if tot == 3099 else 2)
