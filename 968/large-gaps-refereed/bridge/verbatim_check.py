#!/usr/bin/env python3
"""#968 bridge: assert Set.partialDensity, Set.lowerDensity, Erdos968.u and the statement of erdos_968 in Bridge968.lean are VERBATIM
copies of FC @ 90d18f66 (whitespace-normalised, docstrings excluded). Exit 0 all MATCH; 1 any MISMATCH; 2 an item not found.
Negative control: --mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc968 = open('FC_968.lean').read(); fcd = open('FC_Density.lean').read(); ours = open('Bridge968.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard', '((S ∩ A) ∩ Iic b).ncard / (A ∩ Iio b).ncard', 1)
items = [('Set.partialDensity', fcd, 'noncomputable abbrev partialDensity', '(A ∩ Iio b).ncard'),
         ('Set.lowerDensity', fcd, 'noncomputable def lowerDensity', 'S.partialDensity A b'),
         ('Erdos968.u', fc968, 'noncomputable def u (n : ℕ) : ℝ :=', '/ (n + 1)'),
         ('Erdos968.erdos_968 (statement)', fc968, 'theorem erdos_968 :', ':= by')]
ok, missing = True, False
for name, src, a, b in items:
    x, y = grab(src, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH', len(x or ''), len(y or ''))
# the @[inline] attribute on partialDensity is kept; FC's @[category ...] attribute on erdos_968 is FC-only and dropped
sys.exit(2 if missing else (0 if ok else 1))
