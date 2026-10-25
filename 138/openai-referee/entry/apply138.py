#!/usr/bin/env python3
"""Insert the #138 entry at the top of `entries`, update OAI_CLAIMS[138], add LEAN_LABEL own138, a HEADLINES card, CLOSED_BY_LITERATURE (if --closed).
Usage: apply138.py <index.js> [--closed] [--dry-run]. Idempotent: refuses if the slug is already present.
Inputs in /tmp/oaimath/160/entry/: entry138.js (with {{BODY}} {{TITLE}} {{STATUS}} {{SUMMARY}}), body138.html, title.txt, status.txt, summary.txt, oai_claim_line.txt, lean_label.txt, headline_card.js, closed_comment.txt."""
import sys, argparse, re
E='/tmp/oaimath/160/entry/'
ap=argparse.ArgumentParser(); ap.add_argument('index'); ap.add_argument('--closed',action='store_true'); ap.add_argument('--dry-run',action='store_true')
a=ap.parse_args()
src=open(a.index,encoding='utf-8').read()
slug='138-openai-superexponential-van-der-waerden-refereed'
assert slug not in src, "entry already present — refusing (edit in place instead)"
rd=lambda f: open(E+f,encoding='utf-8').read()
body=rd('body138.html').strip(); title=rd('title.txt').strip(); status=rd('status.txt').strip(); summary=rd('summary.txt').strip()
assert status in ('proof_claimed','in_progress','posted','partial','refuted','declined'), status
for s,name in ((body,'body'),(title,'title'),(summary,'summary')):
    assert '`' not in s, name+": backtick"; assert '${' not in s, name+": ${"
    for ph in ("{{","[[","REPLACE_ME","TODO","PLACEHOLDER","XXX"): assert ph not in s, (name,ph)
assert '"' not in title and '"' not in summary, "double quote in a JS string field"
ent=rd('entry138.js').replace('{{BODY}}',body).replace('{{TITLE}}',title).replace('{{STATUS}}',status).replace('{{SUMMARY}}',summary)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
old2='  138:  { fam: 160, claim: "W_r(k) > k^(ck·log r): superexponential van der Waerden numbers", lean: "yes" },\n'
assert src.count(old2)==1, src.count(old2)
new2=rd('oai_claim_line.txt'); assert '{{' not in new2
src=src.replace(old2,new2,1)
lab='own1150: "OpenAI\'s own Lean proves Theorem 1.1'
assert src.count(lab)==1, src.count(lab)
ll=rd('lean_label.txt').strip(); assert '{{' not in ll and ll.startswith('own138:')
src=src.replace(lab, ll+'\n'+lab, 1)
hanchor='const HEADLINES = [\n'; assert src.count(hanchor)==1
card=rd('headline_card.js'); assert '{{' not in card
src=src.replace(hanchor, hanchor+card, 1)
if a.closed:
    c='const CLOSED_BY_LITERATURE = new Set([\n'; assert src.count(c)==1
    cc=rd('closed_comment.txt').strip(); assert '{{' not in cc
    src=src.replace(c, c+'  '+cc+'\n',1)
if a.dry_run: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(a.index,'w',encoding='utf-8').write(src); print("applied; entry chars", len(ent))
