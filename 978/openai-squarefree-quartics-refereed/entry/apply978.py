#!/usr/bin/env python3
"""Splice the #978 entry + OAI_CLAIMS[978] / LEAN_LABEL own978 / CLOSED_BY_LITERATURE / HEADLINES into src/index.js.
Each anchor asserted exactly once. Usage: apply978.py <worktree> [--dry-run]. Refuses any leftover placeholder."""
import sys, json, os
wt = sys.argv[1]; dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/020/entry/entry978.js').read()
left = [k for k in ('READING_PARAGRAPH', 'NUMBERS_PARAGRAPH', 'SEAT_VERDICTS', 'READING_M2', 'LEANCHECKER_SENTENCE') if k in e]; assert not left or '--allow-pending' in sys.argv, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "978-openai' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  978:  { fam: 20,  claim: "n⁴+2 is squarefree with positive density; (d−2)-power-free values for d ≥ 4", lean: "yaml" },',
     '  978:  { fam: 20,  claim: "n⁴+2 is squarefree with positive density; (d−2)-power-free values with the Euler-product density for every d ≥ 4 — read by four AI referee seats here 22 Oct, see /day/978-openai-squarefree-quartics-refereed", lean: "own978", refereed: true },')
LL = open('/tmp/oaimath/020/entry/lean_label.txt').read().strip()
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own978: ' + json.dumps(LL, ensure_ascii=False) + ', ')
CB = open('/tmp/oaimath/020/entry/closed_by.txt').read().rstrip('\n') + '\n'
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n' + CB)
HL = open('/tmp/oaimath/020/entry/headline.js').read()
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + HL)
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
