#!/usr/bin/env python3
"""Splice the #505 entry + OAI_CLAIMS/LEAN_LABEL/CLOSED_BY_LITERATURE/HEADLINES into src/index.js. Each anchor asserted exactly once.
Usage: apply505.py <worktree> <values.json> [--dry-run]"""
import sys, json, re
wt, vals = sys.argv[1], json.load(open(sys.argv[2])); dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/156/entry/entry_draft.js').read()
for k, v in vals.items(): e = e.replace('@@' + k + '@@', v)
left = re.findall(r'@@\w+@@', e); assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "505-openai-borsuk' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  505:  { fam: 156, claim: "a Borsuk counterexample in dimension 9 (record was 64)", lean: "yaml" },',
     '  505:  { fam: 156, claim: "a Borsuk counterexample in dimension 9 (record was 64, then 63) — refereed here 20 Oct; OpenAI\'s Lean (269 modules) kernel-replayed on our machine, statement matched; eleven pieces do cover its set (our exact certificate), so its Borsuk number is exactly 11 — see /day/505-openai-borsuk-fails-in-dimension-nine-refereed", lean: "own505", refereed: true },')
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own505: ' + json.dumps(vals['LEANLABEL'], ensure_ascii=False) + ', ')
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n  505,  // Borsuk\'s question: answer NO since Kahn–Kalai 1993 (n > 2014); OpenAI\'s 23 Sept 2026 counterexample in dimension 9 (projectors onto lines in ℝ⁴) — its own Lean (269 modules) kernel-replayed on our box 2026-10-20, standard axioms, statement matched; our exact certificate: eleven pieces suffice, b(X) = 11\n')
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + vals['HEADLINE'])
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied')
