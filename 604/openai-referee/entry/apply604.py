#!/usr/bin/env python3
"""Insert the #604 entry at the top of `entries`, update OAI_CLAIMS[604], add a HEADLINES card, CLOSED_BY_LITERATURE (if --closed).
Usage: apply604.py <index.js> [--closed] [--dry-run]. Idempotent: refuses if the slug is already present.
Inputs: /tmp/oaimath/604/entry/entry604.js (the entry object with {{BODY}}), body604.html (no backticks)."""
import sys, argparse, re
ap=argparse.ArgumentParser(); ap.add_argument('index'); ap.add_argument('--closed',action='store_true'); ap.add_argument('--dry-run',action='store_true')
a=ap.parse_args()
src=open(a.index,encoding='utf-8').read()
slug='604-openai-weak-pinned-distances-refereed'
assert slug not in src, "entry already present — refusing (edit in place instead)"
body=open('/tmp/oaimath/604/entry/body604.html',encoding='utf-8').read().strip()
ent=open('/tmp/oaimath/604/entry/entry604.js',encoding='utf-8').read()
assert '`' not in body, "backtick in body would terminate the template literal"
assert '${' not in body
for ph in ("{{","[[","REPLACE_ME","TODO","still running"): assert ph not in body, ph
assert body.count("updated when it lands")<=1, "more than one pending anchor"
ent=ent.replace('{{BODY}}',body)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
# OAI_CLAIMS[604]
old2='604:  { fam: 167, claim: "the weak pinned distinct-distances conjecture", lean: "yes" },'
assert src.count(old2)==1, src.count(old2)
new2=open('/tmp/oaimath/604/entry/oai_claim_line.txt',encoding='utf-8').read().strip()
src=src.replace(old2,new2,1)
# LEAN_LABEL key own604 before own1150
lab='own1150: "OpenAI\'s own Lean proves Theorem 1.1'
assert src.count(lab)==1, src.count(lab)
src=src.replace(lab, 'own604: "OpenAI\'s own Lean proves Theorem 1.1 (large repeated distance fibers are rare) and, in Pins.lean, the problem page\'s first question (nonzero distances, in its ∀ε form) — exists_pin_eventually: for every ε > 0 every large n-point planar set has a point with ≥ n^(1−ε) distinct distances — kernel-replayed on our machine on 14 Oct 2026 (48 modules, standard axioms, statement byte-identical to the challenge, the page\'s question compiled as a probe, wrong-shape control fails); eight hostile seats read the paper and its sources — see our /day entry",\n' + lab, 1)
# HEADLINES card at the top (after the opening of the array)
hanchor='const HEADLINES = [\n'; assert src.count(hanchor)==1
card=open('/tmp/oaimath/604/entry/headline_card.js',encoding='utf-8').read()
src=src.replace(hanchor, hanchor+card, 1)
if a.closed:
    c='const CLOSED_BY_LITERATURE = new Set([\n'; assert src.count(c)==1
    src=src.replace(c, c+'  604,  // '+open('/tmp/oaimath/604/entry/closed_comment.txt',encoding='utf-8').read().strip()+'\n',1)
if a.dry_run: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(a.index,'w',encoding='utf-8').write(src); print("applied; entry chars", len(ent))
