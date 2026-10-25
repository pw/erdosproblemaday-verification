#!/usr/bin/env python3
"""#416 bridge: assert Erdos416.V and the statements of erdos_416.parts.i / erdos_416.variants.regularly_varying in Bridge416.lean
are VERBATIM copies of FC @ 32ac619d (whitespace-normalised, docstrings excluded). Exit 0 all MATCH; 1 any MISMATCH; 2 an item not found.
Negative control: --mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc = open('FC_416.lean').read(); ours = open('Bridge416.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('Finset.Icc 1 ⌊x⌋₊', 'Finset.Icc 0 ⌊x⌋₊', 1)
items = [('Erdos416.V', 'noncomputable abbrev V (x : ℝ) : ℝ :=', 'm.totient = n)).card'),
         ('erdos_416.parts.i (statement)', 'theorem erdos_416.parts.i :', ':= by'),
         ('erdos_416.variants.regularly_varying (statement)', 'theorem erdos_416.variants.regularly_varying', ':= by'),
         ]
ok, missing = True, False
for name, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH', len(x or ''), len(y or ''))
o = 'open Filter open scoped Topology Real'
r = o in norm(fc) and o in norm(ours); ok &= r; print('open lines', 'MATCH' if r else 'MISMATCH')
sys.exit(2 if missing else (0 if ok else 1))
