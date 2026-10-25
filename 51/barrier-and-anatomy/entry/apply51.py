#!/usr/bin/env python3
"""Splice the #51 entry + HEADLINES card into src/index.js and drop the LEDGER_OFFSITE line for 51.
Refuses if any placeholder (ALLCAPS_LINE, @@) survives or if anchors are missing/duplicated."""
import sys, re, json
site = sys.argv[1]
p = site + '/src/index.js'
t = open(p).read()
E = '/home/exedev/MathDyad/erdos51/entry/'
title = open(E+'title.txt').read().strip()
summary = open(E+'summary.txt').read().strip()
body = open(E+'entry_body.html').read()
card = json.load(open(E+'card.json'))
for name, s in [('title',title),('summary',summary),('body',body)] + [('card.'+k, v) for k,v in card.items()]:
    if re.search(r'[A-Z_]{6,}_LINE|@@|TODO', s): sys.exit(f'placeholder survives in {name}')
    if '`' in s or '${' in s: sys.exit(f'backtick or ${{ in {name} — would break the template literal')
slug = "51-a-no-answer-needs-smooth-shifted-primes"
if slug in t: sys.exit('slug already present')
def js(s): return json.dumps(s, ensure_ascii=False)
links = [
 {"label": "Verification bundle — the barrier theorem and its corollaries, the smooth-family dynamic programme and the independent branch-and-bound with their cross-check, exact diagonals, the 10⁹ census split by T and W, the July chain re-checked, referee reports, live-page captures", "url": "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/51/barrier-and-anatomy"},
 {"label": "Our July working report on #51 (the identity ℓ/a = ∏ p/(p−1), the replicator criterion, the safe-marker chain to 2.044975) — copy in the bundle", "url": "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/51/barrier-and-anatomy/july-report"},
 {"label": "OEIS A393265 — record values of ℓ(a)/a (McCranie): no more terms below 1.2·10¹¹", "url": "https://oeis.org/A393265"},
 {"label": "Erdős, Some unconventional problems in number theory, Astérisque 61 (1979) 73–82 — p. 80, the hope m′_X/m_X → 1", "url": "http://www.numdam.org/item/AST_1979__61__73_0/"},
 {"label": "Erdős, Some of my favourite problems in number theory, combinatorics, and geometry, Resenhas IME-USP 2 (1995) — §9, the problem", "url": "https://doi.org/10.11606/resimeusp.v2i2.74798"},
 {"label": "Our referee entry on OpenAI's totient preprint (#416): seeds, Theorem 2.2, Ford's propagation lemma", "url": "/day/416-openai-totient-count-asymptotic-refereed"},
 {"label": "Erdős problem #51 and its forum thread (Tao, 10 Aug 2025; Kovač, 28 Aug 2025)", "url": "https://www.erdosproblems.com/forum/thread/51"},
]
for l in card.get('extra_links', []): links.append(l)
entry = ("  {\n"
 f"    slug: {js(slug)},\n    problemNum: 51,\n    title: {js(title)},\n    date: \"2026-10-21\",\n    status: \"partial\",\n    originatedByUs: true,\n"
 f"    summary:\n      {js(summary)},\n    body: `{body}`,\n    links: [\n" +
 "".join(f"      {{ label: {js(l['label'])}, url: {js(l['url'])} }},\n" for l in links) + "    ],\n  },\n")
anchor = 'const entries = [\n'
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + entry, 1)
h = ("  {\n"
 f"    n: 51, kind: \"bound\", tag: {js(card['tag'])},\n    title: {js(card['title'])},\n    line: {js(card['line'])},\n    href: \"/day/{slug}\",\n  }},\n")
ha = 'const HEADLINES = [\n'
assert t.count(ha) == 1
t = t.replace(ha, ha + h, 1)
off = '  { n: 51, problem: "Least inverse-totient ratios", outcome: "No counterexample — ratio behavior verified computationally. Open.", status: "open", seats: ["CODEX"], date: "2026-07-25" },\n'
assert t.count(off) == 1, 'offsite line not found exactly once'
t = t.replace(off, '', 1)
open(p, 'w').write(t)
print('spliced', slug)
