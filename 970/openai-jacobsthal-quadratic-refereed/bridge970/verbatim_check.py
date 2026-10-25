#!/usr/bin/env python3
"""Assert that every FC text copied into Bridge970.lean is VERBATIM FC @ FC_SHA.txt (whitespace-normalised; docstrings and
attributes excluded): defs IsJacobsthalBound, jacobsthalFunction; theorems erdos_970, erdos_970.variants.iterated_log.
Exit 0 all MATCH; 1 a MISMATCH; 2 a block not found. --mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
ours = open('Bridge970.lean').read()
if '--mutate' in sys.argv:
    ours = ours.replace('(Real.log (Real.log (3 * k)))', '(Real.log (Real.log (2 * k)))', 1)
fc = open('FC_970.lean').read()
items = [('IsJacobsthalBound', 'def IsJacobsthalBound', '.Coprime n'),
         ('jacobsthalFunction', 'noncomputable def jacobsthalFunction', 'IsJacobsthalBound k m}'),
         ('erdos_970', 'theorem erdos_970 :', ':= by'),
         ('erdos_970.variants.iterated_log', 'theorem erdos_970.variants.iterated_log', ':= by')]
ok, missing = True, False
for name, a, b in items:
    x, y = grab(fc, a, b), grab(ours, a, b)
    if x is None or y is None: missing = True
    r = x is not None and x == y; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
# the FC file must contain exactly these two theorems (no third statement we failed to bridge)
thms = re.findall(r'(?m)^theorem\s+(\S+)', fc); print('FC theorems:', thms)
if sorted(thms) != ['erdos_970', 'erdos_970.variants.iterated_log']: missing = True
sys.exit(2 if missing else (0 if ok else 1))
