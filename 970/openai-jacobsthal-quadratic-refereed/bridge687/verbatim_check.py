#!/usr/bin/env python3
"""Assert the FC texts copied into Bridge687.lean are verbatim FC @ c83a94d7 (whitespace-normalised):
def Green46.IsCoveredByResidues, def Erdos687.Y, theorems erdos_687.parts.ii and erdos_687.variants.iwaniec.
Exit 0 all MATCH, 1 a MISMATCH, 2 a block missing. --mutate edits our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
ours = open('Bridge687.lean').read()
if '--mutate' in sys.argv:
    ours = ours.replace('=o[atTop] (fun x : ℕ ↦ (x : ℝ) ^ 2)', '=o[atTop] (fun x : ℕ ↦ (x : ℝ) ^ 3)', 1)
g46 = open('fc/FC_G46_HEAD.lean').read(); e687 = open('fc/FC_687_c83a94d7.lean').read()
items = [('IsCoveredByResidues', g46, 'def IsCoveredByResidues', '[MOD p]'),
         ('Y', e687, 'noncomputable def Y (x : ℕ) : ℕ :=', 'IsCoveredByResidues x y}'),
         ('erdos_687.parts.ii', e687, 'theorem erdos_687.parts.ii :', ':= by'),
         ('erdos_687.variants.iwaniec', e687, 'theorem erdos_687.variants.iwaniec :', ':= by')]
ok, missing = True, False
for name, fc, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
sys.exit(2 if missing else (0 if ok else 1))
