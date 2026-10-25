#!/usr/bin/env python3
"""Splice the #952 entry + OAI_CLAIMS[952] / LEAN_LABEL own952 / CLOSED_BY_LITERATURE / HEADLINES into src/index.js.
Each anchor asserted exactly once. Usage: apply952.py <worktree> [--dry-run]. Refuses any leftover placeholder."""
import sys, json, os
wt = sys.argv[1]; dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/028/entry/entry952.js').read()
left = [k for k in ('SEATS_SUMMARY', 'LEANCHECKER_SENTENCE', 'READING_PARAGRAPH', 'WORLD_PARAGRAPH', 'EXTRA_LINKS', 'BFS_PENDING', 'NC_SENTENCE', 'NC_RESULT') if k in e]; assert not left or '--allow-pending' in sys.argv, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "952-openai' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  952:  { fam: 28,  claim: "Gaussian moat: no bounded-step infinite walk", lean: "yaml" },',
     '  952:  { fam: 28,  claim: "Gaussian moat: no bounded-step infinite walk — refereed here 22 Oct, see /day/952-openai-gaussian-moat-refereed", lean: "own952", refereed: true },')
LL = open('/tmp/oaimath/028/entry/lean_label.txt').read().strip()
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own952: ' + json.dumps(LL, ensure_ascii=False) + ', ')
CB = open('/tmp/oaimath/028/entry/closed_by.txt').read().rstrip('\n') + '\n'
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n' + CB)
HL = open('/tmp/oaimath/028/entry/headline.js').read()
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + HL)
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
