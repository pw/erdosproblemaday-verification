#!/usr/bin/env python3
"""Splice the #802 entry + OAI_CLAIMS/LEAN_LABEL/CLOSED_BY_LITERATURE/HEADLINES into src/index.js. Each anchor asserted exactly once.
Usage: apply802.py <worktree> <values.json> [--dry-run]  (adapted from apply551.py)"""
import sys, json, re
wt, vals = sys.argv[1], json.load(open(sys.argv[2])); dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/184/entry/entry_draft.js').read()
for _ in range(3):
    for k, v in vals.items(): e = e.replace('@@' + k + '@@', v)
left = re.findall(r'@@\w+@@', e); assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "802-openai-aeks' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  802:  { fam: 184, claim: "α ≫ n·log d / d for K_r-free graphs (Ajtai–Erdős–Komlós–Szemerédi)", lean: "yes" },',
     '  802:  { fam: 184, claim: "α ≫ n·log d / d for K_r-free graphs (Ajtai–Erdős–Komlós–Szemerédi) — refereed here 21 Oct, see /day/802-openai-aeks-independence-refereed", lean: "own802", refereed: true },')
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own802: ' + json.dumps(vals['LEANLABEL'], ensure_ascii=False) + ', ')
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n  802,  // Ajtai–Erdős–Komlós–Szemerédi 1981: α ≥ c_r·n·log d/d for K_r-free graphs of average degree d (Shearer 1995 had n log d/(d log log d)): OpenAI\'s 25 Sept 2026 proof (21 pp) — its Lean (31 modules) kernel-replayed on our box 2026-10-21, standard axioms, statement matched; read line by line + hostile seats, no gap; bridge to a verbatim copy of FC\'s erdos_802 (every r, every average degree; still research open there). /day/802-openai-aeks-independence-refereed\n')
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + vals['HEADLINE'])
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
