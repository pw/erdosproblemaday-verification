#!/usr/bin/env python3
"""Splice the #968 entry + OAI_CLAIMS/LEAN_LABEL/CLOSED_BY_LITERATURE/HEADLINES into src/index.js. Each anchor asserted exactly once.
Usage: apply968.py <worktree> <values.json> [--dry-run]  (adapted from apply802.py)"""
import sys, json, re
wt, vals = sys.argv[1], json.load(open(sys.argv[2])); dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/026/entry/entry_draft.js').read()
for _ in range(3):
    for k, v in vals.items(): e = e.replace('@@' + k + '@@', v)
left = re.findall(r'@@\w+@@', e); assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "968-openai-large-prime-gaps' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  968:  { fam: 26,  claim: "a positive proportion of prime gaps exceed C·log p, for every C", lean: "yes" },',
     '  968:  { fam: 26,  claim: "a positive proportion of prime gaps exceed C·log p, for every C, so p_n/n increases on a set of positive lower density (the Erdős–Prachar question) — refereed here 21 Oct, see /day/968-openai-large-prime-gaps-positive-proportion-refereed", lean: "own968", refereed: true },')
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own968: ' + json.dumps(vals['LEANLABEL'], ensure_ascii=False) + ', ')
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n  968,  // Erdős–Prachar (1961–62): does p_n/n increase on a set of positive (lower) density? OpenAI\'s 25 Sept 2026 proof (19 pp): for every C a positive proportion of gaps exceed C·log p — its Lean (56 modules, incl. Siegel–Walfisz and Bombieri–Vinogradov) kernel-replayed on our box 2026-10-21, standard axioms, statement matched; read line by line + hostile seats; bridge to a verbatim copy of FC\'s erdos_968. /day/968-openai-large-prime-gaps-positive-proportion-refereed\n')
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + vals['HEADLINE'])
new_at = s.count('@@') - open(p).read().count('@@')
assert new_at == 0, ('placeholder @@ left in spliced index.js', new_at)
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
