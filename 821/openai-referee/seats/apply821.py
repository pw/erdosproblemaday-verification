#!/usr/bin/env python3
"""Insert the #821 entry at the top of `entries`, add the LEAN_LABEL key, flip OAI_CLAIMS[821].lean, add a HEADLINES card.
Usage: apply821.py <index.js> --memory-sentence FILE --ten-seats WORD --seats-of-seats TEXT --rebuilt TEXT --verified-twice TEXT [--dry-run]
Idempotent: refuses if the slug is already present."""
import sys, argparse, re
ap=argparse.ArgumentParser(); ap.add_argument('index'); ap.add_argument('--memory-sentence',required=True); ap.add_argument('--ten-seats',required=True)
ap.add_argument('--seats-of-seats',required=True); ap.add_argument('--rebuilt',required=True); ap.add_argument('--verified-twice',required=True); ap.add_argument('--dry-run',action='store_true')
a=ap.parse_args()
src=open(a.index).read()
assert '821-openai-totient-fibers-refereed' not in src, "entry already present — refusing (edit in place instead)"
body=open('/tmp/oaimath/011/entry/body821.html').read()
ent=open('/tmp/oaimath/011/entry/entry821.js').read()
mem=open(a.memory_sentence).read().strip()
body=body.replace('{{MEMORY_SENTENCE}}',mem).replace('{{SEATS_OF_SEATS}}',a.seats_of_seats).replace('{{VERIFIED_TWICE}}',a.verified_twice).replace('{{TEN_SEATS}}',a.ten_seats).replace('{{REBUILT}}',a.rebuilt)
assert '`' not in body, "backtick in body would terminate the template literal"
ent=ent.replace('{{BODY}}',body).replace('{{TEN_SEATS}}',a.ten_seats).replace('{{SEATS_OF_SEATS}}',a.seats_of_seats)
assert '{{' not in ent, re.findall(r'\{\{[A-Z_]+\}\}',ent)
anchor='const entries = [\n'; assert src.count(anchor)==1
src=src.replace(anchor, anchor+ent, 1)
# LEAN_LABEL key
old='third181: "no Lean in the release'
assert old in src
src=src.replace(old, 'conditional821: "no Lean in the release for the theorem — OpenAI\'s library formalizes only the §8 transfer (smooth shifted primes ⇒ large fibers), which we kernel-checked on 11 Oct 2026; the count itself has no formal proof — see our /day entry", '+old, 1)
# OAI_CLAIMS[821]
old2='821:  { fam: 11,  claim: "φ(m)=n has more than n^(1−ε) solutions infinitely often", lean: "no" },'
assert old2 in src
src=src.replace(old2, old2.replace('lean: "no"','lean: "conditional821"'),1)
# HEADLINES card at slot 3 (after 477 and 112)
hanchor='  {\n    n: 1199, kind: "solved", tag: "SOLVED · NOT BY US",'
assert src.count(hanchor)==1
card=('  {\n    n: 821, kind: "bound", tag: "REFEREED 11 OCT · OPENAI\'S CLAIM · NO GAP FOUND · UNVERIFIED BY HUMANS OR KERNEL",\n'
      '    title: "Erdős\'s totient conjecture: OpenAI claims x^(1−o(1)) primes p with p − 1 smooth to every exponent — we read all 68 pages",\n'
      '    line: "Below smoothness exponent 0.284 nothing of this strength was known; the paper\'s parity-breaking step is a new " +\n'
      '      "transference theorem for weighted dilation graphs. ' + a.ten_seats.capitalize() + ' hostile seats found no mathematical gap; the decisive " +\n'
      '      "identity was rebuilt as an exact computation and made to fail on purpose. No Lean exists for anything but the last page. Not ours; not closed.",\n'
      '    href: "/day/821-openai-totient-fibers-refereed",\n  },\n')
src=src.replace(hanchor, card+hanchor, 1)
if a.dry_run: print("DRY RUN ok; entry chars", len(ent)); sys.exit(0)
open(a.index,'w').write(src); print("applied; entry chars", len(ent))
