#!/usr/bin/env python3
"""Does the Lean literal certificate (Data.lean) equal the JSON, term by term? And do Lean's blockKeys
equal the coordinate order I derived from first principles?"""
import re, sys, json
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/erdos1800/seats/cert'); import myverify as mv
L = '/tmp/erdos1800/claim/erdos-128-sparse-halves/lean/Erdos128/C4Certificate/'
src = open(L + 'Data.lean').read()
body = src[src.index('def certificateTerms'):src.index('theorem certificateTerms_weight_pos')]
num = r'\(\s*(-?\s*\d+)\s*(?:/\s*(\d+))?\s*:\s*ℚ\s*\)'
def fr(m): return Fr(int(m[0].replace(' ', '')), int(m[1]) if m[1] else 1)
terms = []
# simpler tokenised parse
entries = re.findall(r'⟨(.*?)⟩', body, re.S)
for e in entries:
    head, rest = e.split(',', 1)
    head = head.strip()
    w_m = re.match(r'\s*' + num, rest)
    w = fr(w_m.groups()); rest2 = rest[w_m.end():]
    vec = [fr(x) for x in re.findall(num, rest2[rest2.index('['):rest2.rindex(']')])]
    blk = {'.s0': 's0_root0', '.s2 false': 's2_root0', '.s2 true': 's2_root1'}.get(head)
    if blk is None: blk = 'u4_root' + head.split()[1]
    terms.append((blk, w, vec))
eps, jterms = mv.load_cert()
print('Lean terms parsed:', len(terms), ' JSON terms:', len(jterms))
same = [a == b for a, b in zip(terms, jterms)]
print('term-by-term identical (block, weight, full vector):', sum(same), '/', len(jterms), ' order identical:', all(same) and len(terms) == len(jterms))
# epsilon / gamma in Lean
ext = open('/tmp/erdos1800/claim/erdos-128-sparse-halves/lean/Erdos128/ExternalInputs.lean').read()
print('Lean c4FlagGamma line:', re.search(r'def c4FlagGamma : ℚ :=\s*(.*)', ext).group(1).strip())
# blockKeys
defs = open(L + 'Defs.lean').read()
bk = dict()
for head, ks in re.findall(r'\|\s*(\.s0|\.s2 (?:true|false)|\.u4 \d+)\s*=>\s*\[([\d,\s]*)\]', defs):
    blk = {'.s0': 's0_root0', '.s2 false': 's2_root0', '.s2 true': 's2_root1'}.get(head) or 'u4_root' + head.split()[1]
    bk[blk] = [int(x) for x in ks.replace(' ', '').split(',') if x]
C = mv.coords()
mine = {b: sorted(C[b], key=lambda k: C[b][k]) for b in C}
mine['s0_root0'] = [0, 1, 3]   # my s0 index is edge count 0,1,2 <-> keys 0,1,3 (asserted in coords())
print('Lean blockKeys == my first-principles coordinate keys:', {b: bk.get(b) == mine[b] for b in mine})
