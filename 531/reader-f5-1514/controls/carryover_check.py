#!/usr/bin/env python3
"""30 Oct 2026: recompute the submitter's carry-over figure and his three named flip controls.
Usage: python3 -I carryover_check.py  (run from this directory)"""
import csv
a = open('../submitted/k5_w1513.txt').read().strip()
b = ''.join(c for c in open('../../reader-f4-397/submitted/w396.txt').read() if c in '01')
assert len(a) == 1513 and len(b) == 396
agree = sum(a[i] == b[i] for i in range(396))
print(f'k5_w1513 vs w396 on [1,396]: agree {agree}/396, opposite orientation {396-agree}/396')
flips = {int(r[0]): (int(r[1]), int(r[2])) for r in csv.reader(open('flips.tsv'), delimiter='\t')}
named = {1: 4, 757: 9, 1513: 1}   # README at ed77fae (commit 59b62e2)
for p, want in named.items():
    got = flips[p]
    print(f'flip pos {p}: submitter {want}, ours {got[0]}/{got[1]}', 'OK' if got == (want, want) else 'MISMATCH')
