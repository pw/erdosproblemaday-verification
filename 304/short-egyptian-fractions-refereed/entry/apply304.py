#!/usr/bin/env python3
"""Splice the #304 entry + OAI_CLAIMS(148,293,304)/LEAN_LABEL/CLOSED_BY_LITERATURE/HEADLINES into src/index.js. Each anchor asserted exactly once.
Usage: apply304.py <worktree> <values.json> [--dry-run]  (adapted from apply416.py). Refuses any leftover @@PLACEHOLDER@@."""
import sys, json, re
wt, vals = sys.argv[1], json.load(open(sys.argv[2])); dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read(); s0 = s
e = open('/tmp/oaimath/025/entry/entry_draft.js').read()
for _ in range(3):
    for k, v in vals.items(): e = e.replace('@@' + k + '@@', v)
left = re.findall(r'@@\w+@@', e); assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "304-openai-short' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  148:  { fam: 25,  claim: "log log F(k) ≍ k", lean: "yaml" },',
     '  148:  { fam: 25,  claim: "log log F(k) ≍ k — refereed here 21 Oct with #304, see /day/304-openai-short-egyptian-fractions-refereed", lean: "own304", refereed: true },')
once('  293:  { fam: 25,  claim: "log log v(k) ≍ k", lean: "yaml" },',
     '  293:  { fam: 25,  claim: "log log v(k) ≍ k — refereed here 21 Oct with #304, see /day/304-openai-short-egyptian-fractions-refereed", lean: "own304", refereed: true },')
once('  304:  { fam: 25,  claim: "every a/b is a sum of O(log log b) distinct unit fractions", lean: "yaml" },',
     '  304:  { fam: 25,  claim: "every a/b is a sum of O(log log b) distinct unit fractions (Erdős 1950) — refereed here 21 Oct, see /day/304-openai-short-egyptian-fractions-refereed", lean: "own304", refereed: true },')
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own304: ' + json.dumps(vals['LEANLABEL'], ensure_ascii=False) + ', ')
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n  304,  // Is N(b) ≪ log log b? Yes: OpenAI\'s 25 Sep 2026 proof (33 pp; Lean, two independent developments, 348 modules kernel-replayed on our box 2026-10-21, standard axioms, statements matched; bridge to verbatim copies of FC\'s Erdos304.upper_bound + lower_1950) and Bloom–van Doorn\'s 14 Oct exposition. #148 and #293 (estimate questions) get log log F(k) ≍ k and log log v(k) ≍ k from the same paper; not added here — FC keeps 148 open, 293 has no FC file. /day/304-openai-short-egyptian-fractions-refereed\n')
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + vals['HEADLINE'])
new_at = s.count('@@') - s0.count('@@')
assert new_at == 0, ('placeholder @@ left in spliced index.js', new_at)
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
