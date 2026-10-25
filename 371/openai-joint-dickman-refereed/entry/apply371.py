#!/usr/bin/env python3
"""Splice the #371 entry + OAI_CLAIMS[371] / LEAN_LABEL own371 / CLOSED_BY_LITERATURE / HEADLINES into src/index.js.
Each anchor asserted exactly once. Usage: apply371.py <worktree> [--dry-run]. Refuses any leftover placeholder."""
import sys, json, os
wt = sys.argv[1]; dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/012/entry/entry371.js').read()
left = [k for k in ('REPLAY_HEADLINE', 'REPLAY_PARAGRAPH', 'LEAN_ROUTE_PARAGRAPH', 'LEAN_SEAT_SENTENCE', 'BRIDGE_AXIOMS_SENTENCE', 'READING_PARAGRAPH', 'WORLD_PARAGRAPH', 'LINKS_PLACEHOLDER', 'ALPHA_TABLE', 'INDEP_TABLE', 'LEANCHECKER_SENTENCE') if k in e]; assert not left or '--allow-pending' in sys.argv, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "371-openai' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  371:  { fam: 12,  claim: "the density of {n : P(n) < P(n+1)} is 1/2 (Erdős–Pomerance)", lean: "yes" },',
     '  371:  { fam: 12,  claim: "the density of {n : P(n) < P(n+1)} is 1/2 (Erdős–Pomerance), via the joint Dickman law in natural density — refereed here 22 Oct, see /day/371-openai-joint-dickman-law-refereed", lean: "own371", refereed: true },')
LL = open('/tmp/oaimath/012/entry/lean_label.txt').read().strip()
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own371: ' + json.dumps(LL, ensure_ascii=False) + ', ')
CB = open('/tmp/oaimath/012/entry/closed_by.txt').read().rstrip('\n') + '\n'
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n' + CB)
HL = open('/tmp/oaimath/012/entry/headline.js').read()
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + HL)
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
