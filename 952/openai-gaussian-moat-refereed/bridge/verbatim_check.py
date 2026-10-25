#!/usr/bin/env python3
"""Assert that the FC statement copied into Bridge952.lean is VERBATIM FC @ 3b7c94ec (FC_952.lean; whitespace-normalised,
docstring and attributes excluded). Exit 0 MATCH; 1 MISMATCH; 2 not found. --mutate flips one token in our copy first
and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc = open('FC_952.lean').read(); ours = open('Bridge952.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('Function.Injective x ∧\n      ∀ n, Prime', 'Function.Injective x ∧\n      ∀ n, Irreducible', 1)
items = [('erdos_952 (statement)', 'theorem erdos_952 :', '.norm < C := by')]
ok, missing = True, False
for name, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
sys.exit(2 if missing else (0 if ok else 1))
