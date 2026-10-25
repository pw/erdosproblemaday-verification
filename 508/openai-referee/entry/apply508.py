#!/usr/bin/env python3
"""Insert the #508 entry at the top of `entries`, update OAI_CLAIMS[508], add the LEAN_LABEL own508 text, add a HEADLINES card.
Usage: apply508.py <index.js> [--dry-run]. Idempotent: refuses if the slug is already present.
Inputs (this dir): entry508.js ({{TITLE}}/{{SUMMARY}}/{{BODY}}/{{EXTRA_LINKS}}), title.txt, summary.txt, body508.html (no backticks),
extra_links.js, oai_claim_line.txt, lean_label.txt, headline_card.js."""
import sys, argparse, re, os
ap=argparse.ArgumentParser(); ap.add_argument('index'); ap.add_argument('--dry-run',action='store_true'); a=ap.parse_args()
D=os.path.dirname(os.path.abspath(__file__)); rd=lambda n: open(os.path.join(D,n),encoding='utf-8').read()
src=open(a.index,encoding='utf-8').read()
slug='508-openai-plane-not-five-colorable-refereed'
assert slug not in src, "entry already present — refusing (edit in place instead)"
body=rd('body508.html').strip(); title=rd('title.txt').strip(); summary=rd('summary.txt').strip(); extra=rd('extra_links.js').rstrip('\n')
for t in (body,title,summary,extra):
    assert '`' not in t, "backtick would terminate the template literal"; assert '${' not in t
for ph in ("{{","[[","REPLACE_ME","TODO","still running","XXX"): assert ph not in body and ph not in summary, ph
assert '"' not in title and '"' not in summary, "double quote inside a JS double-quoted string"
assert body.count("updated when it lands")<=1, "more than one pending anchor"
ent=rd('entry508.js').replace('{{BODY}}',body).replace('{{TITLE}}',title).replace('{{SUMMARY}}',summary).replace('{{EXTRA_LINKS}}',extra)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
old2='  508:  { fam: 158, claim: "the plane is not 5-colourable (χ ≥ 6)", lean: "yaml" },'
assert src.count(old2)==1, src.count(old2)
src=src.replace(old2, rd('oai_claim_line.txt').rstrip('\n'), 1)
lab='own1150: "OpenAI\'s own Lean proves Theorem 1.1'; assert src.count(lab)==1, src.count(lab)
ll=rd('lean_label.txt').strip(); assert ll.startswith('own508: "') and ll.endswith('",')
src=src.replace(lab, ll+'\n' + lab, 1)
hanchor='const HEADLINES = [\n'; assert src.count(hanchor)==1
src=src.replace(hanchor, hanchor+rd('headline_card.js'), 1)
if a.dry_run: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(a.index,'w',encoding='utf-8').write(src); print("applied; entry chars", len(ent))
