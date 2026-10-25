#!/usr/bin/env python3
"""Assert that the FC text copied into Bridge174FC.lean is VERBATIM FC @ 2a315101 (FC_174.lean; whitespace-normalised,
docstrings and attributes excluded). Exit 0 all MATCH; 1 any MISMATCH; 2 an item not found.
--mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc = open('FC_174.lean').read(); ours = open('Bridge174FC.lean').read() + open('Bridge174Main.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('∀ k : ℕ, 1 ≤ k →', '∀ k : ℕ, 2 ≤ k →', 1)
items = [('Erdos174.IsRamsey', 'def IsRamsey {n : ℕ} (A : Set (EuclideanSpace ℝ (Fin n))) : Prop :=', 'c (p a) = i'),
         ('graham binders+conclusion (ours sits inside ¬ (∀ … , IsRamsey A))',
          '(A : Set (EuclideanSpace ℝ (Fin n))) (hA : A.Finite)', 'IsRamsey A'),
         ('erdos_174 left-hand side (ours: = criterionAnswer n)', '(n : ℕ) : {A : Set', '| IsRamsey A} ='),
         ('erdos_174.variants.spherical (statement)', 'theorem erdos_174.variants.spherical {n : ℕ}', 'EuclideanGeometry.Cospherical A')]
ok, missing = True, False
for name, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if name.startswith('graham'):   # FC: theorem erdos_174.variants.graham {n : ℕ} (A …) (hA …) (hs …) : IsRamsey A
        x = grab(fc[fc.find('theorem erdos_174.variants.graham'):fc.find('theorem erdos_174.variants.leader_russell_walters')], a, b)
        x = None if x is None else x.replace(') : IsRamsey A', '), IsRamsey A')
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
sys.exit(2 if missing else (0 if ok else 1))
