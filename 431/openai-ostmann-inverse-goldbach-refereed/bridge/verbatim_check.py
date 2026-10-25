#!/usr/bin/env python3
"""Assert the FC text copied into Bridge431{C,M}.lean is VERBATIM FC (FormalConjectures/ErdosProblems/431.lean, commit in
FC_SHA.txt), whitespace-normalised, docstrings/attributes excluded: theorems erdos_431, erdos_431.variants.ostmann, and the
two `open scoped` lines. Exit 0 all MATCH; 1 a MISMATCH; 2 a block not found. --mutate flips one token in our copy first
and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def grab(src, start, end):
    src, start, end = norm(src), norm(start), norm(end)
    i = src.find(start)
    if i < 0: return None
    j = src.find(end, i + len(start))
    return None if j < 0 else norm(src[i:j + len(end)])
fc = open('FC_431.lean').read()
items = [('erdos_431', 'theorem erdos_431 :', ':= by'),
         ('erdos_431.variants.ostmann', 'theorem erdos_431.variants.ostmann', ':= by'),
         ]
OPENS = ['open scoped Pointwise', 'open scoped symmDiff']
ok, missing = True, False
for f in ('Bridge431C.lean', 'Bridge431M.lean'):
    ours = open(f).read()
    if '--mutate' in sys.argv:
        ours = ours.replace('{n | n.Prime}).Infinite', '{n | n.Prime}).Finite', 1)
    for name, a, b in items:
        x, y = grab(fc, a, b), grab(ours, a, b)
        if x is None or y is None: missing = True
        r = x is not None and x == y; ok &= r
        print(f, name, 'MATCH' if r else 'MISMATCH'); print('   FC  :', x); print('   ours:', y)
for f in ('Bridge431C.lean', 'Bridge431M.lean'):
    for o in OPENS:
        r = (o in open(f).read()) and (o in fc); ok &= r
        print(f, repr(o), 'PRESENT IN BOTH' if r else 'MISSING')
thms = re.findall(r'(?m)^theorem\s+(\S+)', fc); print('FC theorems:', thms)
if sorted(thms) != ['erdos_431', 'erdos_431.variants.ostmann']: missing = True
sys.exit(2 if missing else (0 if ok else 1))
