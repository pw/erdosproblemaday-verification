#!/usr/bin/env python3
"""Splice the #507 entry + OAI_CLAIMS[507] / LEAN_LABEL own507 / HEADLINES card / BLOOM_8OCT banner fix into src/index.js.
#507 is NOT added to CLOSED_BY_LITERATURE: the problem (estimate α(n)) stays open. Each anchor asserted exactly once.
Usage: apply507.py <worktree> [--dry-run] [--allow-pending]. Refuses leftover placeholders unless --allow-pending."""
import sys, json
wt = sys.argv[1]; dry = '--dry-run' in sys.argv
p = f"{wt}/src/index.js"; s = open(p).read()
E = '/tmp/oaimath/191/entry/'
e = open(E + 'entry507.js').read()
left = [k for k in ('READING_PARAGRAPH', 'WORLD_PARAGRAPH', 'WORLD_REPLAYS_PARAGRAPH', 'LEANCHECKER_SENTENCE', 'BLIND_SENTENCE', 'C_ITEMS', 'C_VERDICT') if k in e]
assert not left or '--allow-pending' in sys.argv, left
assert e.count('`') == 2, 'backtick count in entry must be 2'
assert '${' not in e, 'template interpolation in entry'
def once(old, new):
    global s
    assert s.count(old) == 1, (old[:90], s.count(old)); s = s.replace(old, new, 1)
assert 'slug: "507-openai' not in s
once("const entries = [\n", "const entries = [\n" + e)
once('  507:  { fam: 191, claim: "Heilbronn: α(n) ≥ n^(−2+η), improving Komlós–Pintz–Szemerédi", lean: "linked" },',
     '  507:  { fam: 191, claim: "Heilbronn: for every large n, some n points in the unit square have every triangle of area ≥ c·n^(−2+η), η = 2/(45435k+16) ≈ 3·10⁻²³⁶ — the first power gain over Komlós–Pintz–Szemerédi\'s (log n)/n² (1982); the estimate of α(n) stays open — read by AI referee seats here 22 Oct, see /day/507-openai-heilbronn-power-lower-bound-refereed", lean: "own507", refereed: true },')
LL = open(E + 'lean_label.txt').read().strip()
once('const LEAN_LABEL = { ', 'const LEAN_LABEL = { own507: ' + json.dumps(LL, ensure_ascii=False) + ', ')
HL = open(E + 'headline.js').read()
once('const HEADLINES = [\n', 'const HEADLINES = [\n' + HL)
# Bloom's 8 Oct list (erdosproblems.com/forum/thread/blog:10) has 25 problems; four of our OAI_CLAIMS keys are not on it.
once('function oaiNotice(n) {\n',
     '// Bloom\'s 8 Oct 2026 post "Erdős problems in the OpenAI proofs" lists these 25 (re-read 22 Oct); #142, #505, #507 and #978\n'
     '// are OpenAI families we matched ourselves, so "Bloom calls these claims" must not be said of them.\n'
     'const BLOOM_8OCT = new Set([3, 90, 120, 138, 148, 172, 174, 181, 184, 293, 304, 371, 416, 431, 508, 551, 604, 802, 821, 952, 968, 970, 986, 1083, 1150]);\n\n'
     'function oaiNotice(n) {\n')
once('. Bloom calls these claims, not endorsements${c.refereed ? "" : "; anything on this page that says the question is open was written before that release and has not re-checked it"}.</div>`;',
     '. ${BLOOM_8OCT.has(Number(n)) ? "Bloom calls these claims, not endorsements" : "This problem is not among the 25 on Bloom\'s 8 Oct list of the release\'s Erdős claims; the match to family " + c.fam + " is our own reading, not Bloom\'s"}${c.refereed ? "" : "; anything on this page that says the question is open was written before that release and has not re-checked it"}.</div>`;')
if dry: print('dry run OK; entry chars', len(e)); sys.exit(0)
open(p, 'w').write(s); print('applied; entry chars', len(e))
