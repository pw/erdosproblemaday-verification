#!/usr/bin/env python3
"""Splice the #174 entry + OAI_CLAIMS[174] / LEAN_LABEL own174 / CLOSED_BY_LITERATURE / HEADLINES / a dated pointer on the
11 Aug #174 entry into src/index.js. Each anchor asserted exactly once. Usage: apply174.py <worktree> [--dry-run].
Refuses any leftover placeholder (LEANCHECKER_SENTENCE, LEANCHECKER_FC_SENTENCE, RANDOM_SENTENCE) unless filled via vals.json."""
import sys, json, re, os
wt = sys.argv[1]; dry = '--dry-run' in sys.argv
vals = json.load(open('/tmp/oaimath/172/entry/vals.json')) if os.path.exists('/tmp/oaimath/172/entry/vals.json') else {}
p = f"{wt}/src/index.js"; s = open(p).read()
e = open('/tmp/oaimath/172/entry/entry174.js').read()
for k, v in vals.items(): e = e.replace(k, v)
left = [k for k in ('LEANCHECKER_SENTENCE', 'LEANCHECKER_FC_SENTENCE', 'RANDOM_SENTENCE') if k in e]; assert not left, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "174-openai-euclidean' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  174:  { fam: 172, claim: "a full classification of Euclidean Ramsey sets", lean: "yaml" },',
     '  174:  { fam: 172, claim: "a full classification of Euclidean Ramsey sets — refereed here 21 Oct, see /day/174-openai-euclidean-ramsey-classification-refereed", lean: "own174", refereed: true },')
LL = ("OpenAI's own Lean proves Theorem 1.1 (A is Ramsey iff the tensor criterion over F ⊗_ℚ F holds) and its consequences "
      "(Ramsey sets are cospherical; subsets of finite transitive sets are Ramsey; at most five circle points; quadratic independence; "
      "nine generic circle points are not Ramsey), and, in a separate development that does not use the classification, the twelve-point "
      "set with a 50-colour obstruction in every dimension. Kernel-replayed on our machine on 21 Oct 2026: 65 modules, 0 errors, standard "
      "axioms, all seven statements and their definitions matched to the comparator challenges under pp.all. Kernel-checked bridges of ours "
      "refute Formal Conjectures' erdos_174.variants.graham (tagged open there), prove its variants.spherical, and prove its main erdos_174 set equality against an explicit answer built from OpenAI's criterion — see our /day entry")
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own174: ' + json.dumps(LL, ensure_ascii=False) + ', ')
CB = ("  174,  // Characterise the Euclidean Ramsey sets: OpenAI's 23 Sept 2026 classification — A is Ramsey iff its sphere equation lifts "
      "to F ⊗_ℚ F (Theorem 1.1, an existential algebraic criterion; whether that is the characterisation Erdős wanted is a judgment, said so on "
      "the page). OpenAI's own Lean (65 modules) kernel-replayed on our box 2026-10-21, standard axioms, seven statements matched; four hostile "
      "seats + our line-by-line read, no gap. Graham's conjecture refuted first by Pálvölgyi (20 Sept). Our Lean bridges refute FC's graham "
      "variant (still tagged open), prove its spherical variant and its main set equality against a criterion-built answer. /day/174-openai-euclidean-ramsey-classification-refereed\n")
once('const CLOSED_BY_LITERATURE = new Set([\n', 'const CLOSED_BY_LITERATURE = new Set([\n' + CB)
HL = '''  {
    n: 174, kind: "solved", tag: "21 OCT · OPENAI'S CLAIM — THE THEOREM IS NOT OURS · ERDŐS: CHARACTERISE THE EUCLIDEAN RAMSEY SETS · ANSWER CLAIMED: AN EXACT ALGEBRAIC TEST — A IS RAMSEY IFF ITS SPHERE EQUATION LIFTS FROM F TO F ⊗ F (F = THE FIELD OF ITS COORDINATES); WHETHER THAT IS THE CHARACTERISATION ERDŐS WANTED IS A JUDGMENT · GRAHAM'S CONJECTURE FELL FIRST (PÁLVÖLGYI, 20 SEPT) · LEAN KERNEL-REPLAYED HERE, 65 MODULES, SEVEN STATEMENTS MATCHED · READ BY FOUR HOSTILE AI SEATS: HOLDS AS READ · OURS: LEAN BRIDGES TO FORMAL CONJECTURES — ITS OPEN-TAGGED GRAHAM STATEMENT REFUTED, ITS SPHERICAL STATEMENT AND ITS MAIN SET EQUALITY PROVED; THE SMALLEST NON-RAMSEY SUBSETS OF OPENAI'S TWELVE POINTS HAVE EIGHT POINTS · UNREVIEWED BY HUMANS",
    title: "Which finite point sets are Euclidean Ramsey? An exact algebraic test: OpenAI's classification, its Lean replayed and its proof read by AI seats here",
    line: "Every Ramsey set lies on a sphere. Write its points as p_i = (1, a_i), with coordinates generating a field F: the set is Ramsey exactly when its sphere equation can be lifted from F to the tensor ring F ⊗ F before multiplying out. With algebraic coordinates the lift always exists (a corollary first published in AI-generated repositories), so only transcendental coordinates can break Graham's conjecture: Pálvölgyi's seven points, OpenAI's twelve, and eight inside those twelve, among them a square and a rectangle on one circle. The theorem is OpenAI's.",
    href: "/day/174-openai-euclidean-ramsey-classification-refereed",
  },
'''
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + HL)
# dated pointer on the 11 Aug entry (append a paragraph at the end of its body)
i = s.find('slug: "174-ramsey-pyramid-closure"'); assert i > 0
j = s.find('\n`,\n    links:', i); assert j > 0
upd = ('\n<p><strong>Update, 21 October 2026.</strong> The characterisation this entry called open has since been claimed: '
       'OpenAI\'s exact algebraic criterion of 23 September. We replayed its Lean and refereed it in <a href="/day/174-openai-euclidean-ramsey-classification-refereed">a later entry</a>.</p>')
s = s[:j] + upd + s[j:]
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
