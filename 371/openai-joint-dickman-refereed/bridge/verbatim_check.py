#!/usr/bin/env python3
"""#371 bridge: assert Set.partialDensity, Set.HasDensity and the statement of Erdos371.erdos_371 in Bridge371.lean are VERBATIM
copies of Formal Conjectures @ 3b7c94ec (whitespace-normalised). Exit 0 all MATCH; 1 any MISMATCH; 2 an item not found.
Negative controls: --mutate N flips one token in OUR copy of item N first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc = open('FC_371.lean').read(); fcd = open('FC_Density.lean').read(); ours = open('Bridge371.lean').read()
items = [('Set.partialDensity', fcd, '@[inline]\nnoncomputable abbrev partialDensity', '(A ∩ Iio b).ncard'),
         ('Set.HasDensity', fcd, 'def HasDensity', 'atTop (𝓝 α)'),
         ('Erdos371.erdos_371 (statement)', fc, 'theorem erdos_371 :', ':= by')]
muts = {'1': ('((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard', '((S ∩ A) ∩ Iic b).ncard / (A ∩ Iio b).ncard'),
        '2': ('Tendsto (fun (b : β) => S.partialDensity A b) atTop (𝓝 α)', 'Tendsto (fun (b : β) => S.partialDensity A (b + b)) atTop (𝓝 α)'),
        '3': ('Nat.maxPrimeFac (n + 1) > Nat.maxPrimeFac n }.HasDensity (1/2)', 'Nat.maxPrimeFac (n + 1) ≥ Nat.maxPrimeFac n }.HasDensity (1/2)')}
if '--mutate' in sys.argv:
    k = sys.argv[sys.argv.index('--mutate') + 1]; a, b = muts[k]
    anchor = {'1': 'noncomputable abbrev partialDensity', '2': 'def HasDensity', '3': 'theorem erdos_371 :'}[k]
    i = ours.index(anchor); assert a in ours[i:]   # mutate the occurrence INSIDE the checked item, not an earlier copy
    ours = ours[:i] + ours[i:].replace(a, b, 1)
ok, missing = True, False
for name, src, a, b in items:
    x, y = grab(src, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH', len(x or ''), len(y or ''))
# FC's @[category research solved, AMS 11, formal_proof ...] attribute on erdos_371 is FC-only and dropped; docstrings kept.
sys.exit(2 if missing else (0 if ok else 1))
