#!/usr/bin/env python3
"""Assert that every FC text copied into Bridge978.lean is VERBATIM FC @ a7b87c8d (whitespace-normalised; docstrings and
attributes excluded): the three #978 statements (FC_978.lean), `Powerfree` (FC_Powerfree.lean), and `partialDensity`,
`HasDensity`, `HasPosDensity` (FC_Density.lean). Exit 0 all MATCH; 1 a MISMATCH; 2 a block not found.
--mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
ours = open('Bridge978.lean').read()
if '--mutate' in sys.argv:
    ours = ours.replace('{n : ℕ | Squarefree (n ^ 4 + 2)}', '{n : ℕ | Squarefree (n ^ 4 + 1)}', 1)
fc = {'978': open('FC_978.lean').read(), 'pf': open('FC_Powerfree.lean').read(), 'den': open('FC_Density.lean').read()}
items = [('978', 'erdos_978.variants.sub_two', 'theorem erdos_978.variants.sub_two', '.Infinite := by'),
         ('978', 'erdos_978.parts.ii', 'theorem erdos_978.parts.ii :', '.Infinite := by'),
         ('978', 'erdos_978.parts.iii', 'theorem erdos_978.parts.iii', '.Infinite := by'),
         ('pf', 'Powerfree (def body)', 'def Powerfree', 'IsUnit x'),
         ('den', 'partialDensity', 'noncomputable abbrev partialDensity', '(A ∩ Iio b).ncard'),
         ('den', 'HasDensity', 'def HasDensity', 'atTop (𝓝 α)'),
         ('den', 'HasPosDensity', 'def HasPosDensity', 'S.HasDensity α A')]
ok, missing = True, False
for src, name, a, b in items:
    x, y = grab(fc[src], a, b), grab(ours, a, b)
    if src == 'pf' and x and y:   # FC's `def Powerfree (k : ℕ) (m : M)` sits under `variable [Monoid M]`; ours carries `[Monoid M]` inline
        x = x.replace('def Powerfree (k : ℕ)', 'def Powerfree [Monoid M] (k : ℕ)', 1)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
sys.exit(2 if missing else (0 if ok else 1))
