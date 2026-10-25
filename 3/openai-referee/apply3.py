#!/usr/bin/env python3
"""Insert the #3 entry at the top of `entries`, add LEAN_LABEL key own3, flip OAI_CLAIMS[3].lean + claim text, add a HEADLINES card.
Usage: apply3.py <index.js> [--dry-run]. Reads body3.html + entry3.js + card3.js from this directory. Idempotent: refuses if the slug is present."""
import sys, re, os
here=os.path.dirname(os.path.abspath(__file__))
idx=sys.argv[1]; dry='--dry-run' in sys.argv
src=open(idx).read()
SLUG='3-openai-reciprocal-sum-conjecture-refereed'
assert SLUG not in src, "entry already present — refusing (edit in place instead)"
body=open(os.path.join(here,'body3.html')).read()
ent=open(os.path.join(here,'entry3.js')).read()
card=open(os.path.join(here,'card3.js')).read()
assert '`' not in body, "backtick in body would terminate the template literal"
assert '${' not in body, "${ in body would interpolate"
left=re.findall(r'\{\{[A-Z_]+\}\}',body); assert not left, left
ent=ent.replace('{{BODY}}',body)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
old='third181: "no Lean in the release'
assert src.count(old)==1
src=src.replace(old, 'own3: "OpenAI\'s own Lean proves the reciprocal-sum statement — Erdős #3 exactly as asked — via a weaker bound r_k(N) ≤ C·N·exp(−c(log log N)^(1+η)) (itself new past the summability threshold); the quasipolynomial headline is paper-only; our kernel replay is queued — see our /day entry", '+old, 1)
old2='3:    { fam: 159, claim: "r_k(N) ≤ N·exp(−c(log N)^ε), implying the reciprocal-sum conjecture (Lean proves a weaker bound that still implies it)", lean: "partial" },'
assert src.count(old2)==1, "OAI_CLAIMS[3] line not found verbatim"
src=src.replace(old2, '3:    { fam: 159, claim: "r_k(N) ≤ C_k·N·exp(−c_k(log N)^ε_k) for every k ≥ 3 (quasipolynomial Szemerédi), hence the reciprocal-sum conjecture", lean: "own3" },',1)
hanchor='  {\n    n: 1199, kind: "solved", tag: "SOLVED · NOT BY US",'
assert src.count(hanchor)==1
src=src.replace(hanchor, card+hanchor, 1)
if dry: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(idx,'w').write(src); print("applied; entry chars", len(ent))
