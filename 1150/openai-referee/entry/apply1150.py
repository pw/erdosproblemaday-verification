#!/usr/bin/env python3
"""Insert the #1150 entry at the top of `entries`, add LEAN_LABEL key own1150, flip OAI_CLAIMS[1150], add a HEADLINES card.
Usage: apply1150.py <index.js> [--dry-run]. Reads body1150.html + entry1150.js + card1150.js from this directory. Idempotent: refuses if the slug is present."""
import sys, re, os
here=os.path.dirname(os.path.abspath(__file__))
idx=sys.argv[1]; dry='--dry-run' in sys.argv
src=open(idx).read()
SLUG='1150-openai-ultraflat-littlewood-refereed'
assert SLUG not in src, "entry already present — refusing (edit in place instead)"
body=open(os.path.join(here,'body1150.html')).read()
ent=open(os.path.join(here,'entry1150.js')).read()
card=open(os.path.join(here,'card1150.js')).read()
assert '`' not in body, "backtick in body would terminate the template literal"
assert '${' not in body, "${ in body would interpolate"
left=re.findall(r'\{\{[A-Z_]+\}\}',body); assert not left, left
ent=ent.replace('{{BODY}}',body)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
old='own3: "OpenAI\'s own Lean proves the reciprocal-sum statement'
assert src.count(old)==1
label=open(os.path.join(here,'label1150.txt')).read().strip()
assert '"' not in label and '`' not in label
src=src.replace(old, 'own1150: "'+label+'", '+old, 1)
old2='1150: { fam: 76,  claim: "ultraflat real Littlewood polynomials exist (disproving the problem as stated)", lean: "partial" },'
assert src.count(old2)==1, "OAI_CLAIMS[1150] line not found verbatim"
src=src.replace(old2, '1150: { fam: 76,  claim: "real Littlewood polynomials with max ≤ (1+η)√N at every large length N (Thm 1.1, formalized) — hence NO to #1150 — and, paper-only, two-sided ultraflat (1±ε)√N", lean: "own1150" },',1)
hanchor='  {\n    n: 1199, kind: "solved", tag: "SOLVED · NOT BY US",'
assert src.count(hanchor)==1
src=src.replace(hanchor, card+hanchor, 1)
cl='  1083, // Erdős distinct distances in ℝ^d, d ≥ 3, with the constant factor'
assert src.count(cl)==1
src=src.replace(cl, '  1150, // Erdős ultraflat question for ±1 polynomials: answer NO — OpenAI\'s 23 Sept 2026 Theorem 1.1 (min max = (1+o(1))√N), OpenAI\'s own Lean, kernel-replayed on our box 2026-10-12 (28 modules, 0 errors, main depends only on propext/Classical.choice/Quot.sound, statement matched to the challenge); seven hostile seats found no gap. /day/1150-openai-ultraflat-littlewood-refereed\n'+cl, 1)
if dry: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(idx,'w').write(src); print("applied; entry chars", len(ent))
