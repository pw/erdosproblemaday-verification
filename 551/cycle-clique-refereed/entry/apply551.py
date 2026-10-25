#!/usr/bin/env python3
"""Splice the #551 entry + OAI_CLAIMS/LEAN_LABEL/CLOSED_BY_LITERATURE/HEADLINES into src/index.js. Each anchor asserted exactly once.
Usage: apply551.py <worktree> <values.json> [--dry-run]  (adapted from apply505.py)"""
import sys, json, re
wt, vals = sys.argv[1], json.load(open(sys.argv[2])); dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/189/entry/entry_draft.js').read()
for _ in range(3):
    for k, v in vals.items(): e = e.replace('@@' + k + '@@', v)
left = re.findall(r'@@\w+@@', e); assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "551-openai-cycle-clique' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  551:  { fam: 189, claim: "R(C_m, K_n) = (m−1)(n−1)+1 for all m ≥ n ≥ 3 except (3,3)", lean: "yes" },',
     '  551:  { fam: 189, claim: "R(C_m, K_n) = (m−1)(n−1)+1 for all m ≥ n ≥ 3 except (3,3) — refereed here 20 Oct, see /day/551-openai-cycle-clique-ramsey-refereed", lean: "own551", refereed: true },')
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own551: ' + json.dumps(vals['LEANLABEL'], ensure_ascii=False) + ', ')
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n  551,  // Erdős–Faudree–Rousseau–Schelp cycle–clique conjecture R(C_m,K_n) = (m−1)(n−1)+1, m ≥ n ≥ 3, (m,n) ≠ (3,3): Keevash–Long–Skokan 2021 for large n; OpenAI\'s 25 Sept 2026 proof of the whole range (41 pp, 3,099 finite patterns) — its Lean (comparator closure, 182 modules) kernel-replayed on our box 2026-10-20, standard axioms, statement matched; read line by line + three hostile seats, no gap; bridge to a verbatim copy of FC\'s erdos_551 (still research open there). /day/551-openai-cycle-clique-ramsey-refereed\n')
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + vals['HEADLINE'])
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
