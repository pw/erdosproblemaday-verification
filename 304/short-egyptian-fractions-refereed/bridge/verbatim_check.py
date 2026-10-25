#!/usr/bin/env python3
"""Family 25 bridges: assert that the FC definitions and statements copied into Bridge304.lean / Bridge148_293.lean are VERBATIM
copies of FC @ 2a315101 (FC_304.lean, FC_148.lean; whitespace-normalised, docstrings excluded). Exit 0 all MATCH; 1 any MISMATCH;
2 an item not found. Negative control: --mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
f304 = open('FC_304.lean').read(); f148 = open('FC_148.lean').read()
b304 = open('Bridge304.lean').read(); b148 = open('Bridge148_293.lean').read(); b148lb = open('Bridge148LB.lean').read()
if '--mutate' in sys.argv: b304 = b304.replace('(∀ n ∈ s, n > 1)', '(∀ n ∈ s, n > 0)', 1)
if '--mutate148' in sys.argv: b148 = b148.replace('S.card = k ∧ 0 ∉ S', 'S.card = k ∧ 1 ∉ S', 1)
if '--mutateLB' in sys.argv: b148lb = b148lb.replace('log 2 * log 3 / 3', 'log 2 * log 3 / 2', 1)
items = [(f304, b304, 'Erdos304.unitFractionExpressible', 'def unitFractionExpressible (a b : ℕ) : Set ℕ :=', '(n : ℚ)⁻¹}'),
         (f304, b304, 'Erdos304.smallestCollection', 'noncomputable def smallestCollection (a b : ℕ) : ℕ :=', 'sInf (unitFractionExpressible a b)'),
         (f304, b304, 'Erdos304.smallestCollectionTo', 'noncomputable def smallestCollectionTo (b : ℕ) : ℕ :=', 'a ∈ Finset.Ico 1 b}'),
         (f304, b304, 'Erdos304.upper_bound (statement)', 'theorem upper_bound :', ':= by'),
         (f304, b304, 'Erdos304.erdos_304.variants.lower_1950 (statement)', 'theorem erdos_304.variants.lower_1950 :', ':= by'),
         (f148, b148, 'Erdos148.F', 'noncomputable def F (k : ℕ) : ℕ :=', '= 1}.ncard'),
         (f148, b148lb, 'Erdos148.erdos_148.variants.lower_bound (statement)', 'theorem erdos_148.variants.lower_bound :', ':= by')]
ok, missing = True, False
for fc, ours, name, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH', len(x or ''), len(y or ''))
for fc, ours, o in ((f304, b304, 'open Asymptotics Filter'), (f148, b148, 'open Filter Real'), (f148, b148lb, 'open Filter Real')):
    r = o in norm(fc) and o in norm(ours); ok &= r; print('open line', repr(o), 'MATCH' if r else 'MISMATCH')
sys.exit(2 if missing else (0 if ok else 1))
