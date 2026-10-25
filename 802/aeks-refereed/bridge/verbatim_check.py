#!/usr/bin/env python3
"""#802 bridge: assert the statements/definition in Bridge802.lean are VERBATIM copies of FC @ 90d18f66 (whitespace-normalised).
Exit 0 all MATCH; 1 any MISMATCH. Negative control: --mutate flips one token in our copy first and must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def thm(src, name):
    m = re.search(r'theorem ' + re.escape(name) + r' :(.*?):= by', src, re.S) or re.search(r'theorem ' + re.escape(name) + r' :(.*?):=\n', src, re.S)
    return None if not m else norm(m.group(1))
def dfn(src):
    m = re.search(r'noncomputable def averageDegree(.*?)\n\n', src, re.S); return None if not m else norm(m.group(1))
fc = open('FC_802.lean').read(); fcd = open('FC_Degrees.lean').read(); ours = open('Bridge802.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('c * (log G.averageDegree / G.averageDegree) * n ≤ G.indepNum := by\n  intro r', 'c * (log G.averageDegree / G.averageDegree) * n < G.indepNum := by\n  intro r', 1)
ok = True
for name in ['erdos_802', 'erdos_802.variants.aeks', 'erdos_802.variants.r_eq_three']:
    a, b = thm(fc, name), thm(ours, name); r = a is not None and a == b; ok &= r
    print(name, 'MATCH' if r else 'MISMATCH', len(a or ''), len(b or ''))
a, b = dfn(fcd), dfn(ours); r = a is not None and a == b; ok &= r; print('def averageDegree', 'MATCH' if r else 'MISMATCH', len(a or ''), len(b or ''))
# the docstring + attribute line above erdos_802 in FC carries `@[category research open ...]`; we drop the attribute (FC-only)
sys.exit(0 if ok else 1)
