#!/usr/bin/env python3
"""Insert the #341 Queneau entry + HEADLINES card + a see-also link on Li's entry into <worktree>/src/index.js.
usage: apply.py <worktree> [--dry-run]   (idempotent: refuses if the slug is already present)"""
import sys, pathlib, json, re
WT=pathlib.Path(sys.argv[1]); SRC=WT/'src/index.js'; dry='--dry-run' in sys.argv
E=pathlib.Path(__file__).parent
slug="341-queneau-variant-not-periodic-either"
title=(E/'title.txt').read_text().strip(); summary=(E/'summary.txt').read_text().strip(); body=(E/'body.html').read_text().strip()
for ph in ("REFEREE_SENTENCE","GREEDY_SENTENCE","[[","TODO","REPLACE_ME","XXX"): assert ph not in body, "placeholder left: "+ph
assert '`' not in body and '${' not in body, "backtick/${ in body"
s=SRC.read_text(encoding='utf-8')
assert s.count('slug: "'+slug+'"')==0, "slug already present"
def js(x): return json.dumps(x, ensure_ascii=False)
entry=('  {\n    slug: %s,\n    problemNum: 341,\n    title: %s,\n    date: "2026-10-14",\n    status: "partial",\n    originatedByUs: true,\n    summary:\n      %s,\n    body: `\n%s\n`,\n    links: [\n'
       '      { label: "Verification bundle — PROOF.md (the full argument incl. the rule-D calculation), the dynamics and FFT scripts, both greedy runs to 10⁷, the 27-seed census, referee reports", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/341/queneau-variant-56-for-77" },\n'
       '      { label: "Our 13 October referee entry on Li\'s disproof of #341 (the shield and the framing lemmas reused here)", url: "/day/341-li-disproof-refereed" },\n'
       '      { label: "Li, Counterexamples to Erdős Problem 341 (paper + Lean, GitHub)", url: "https://github.com/LiAlreadyExists/Erdos-341" },\n'
       '      { label: "Green, 100 open problems — Problem 7 (the Dickson and Queneau variants, both marked open)", url: "https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf" },\n'
       '      { label: "van Berkel–Bosma, On t-sumfree sequences (arXiv 2609.16843) — the strict rule from t-term starts; their conjectures are untouched here", url: "https://arxiv.org/abs/2609.16843" },\n'
       '      { label: "Our July working report for #341 (the finite periodicity certificate used to show Li\'s seed is periodic under rule Q)", url: "/report/341" },\n'
       '      { label: "erdosproblems.com/341", url: "https://www.erdosproblems.com/341" },\n'
       '    ],\n  },\n') % (js(slug), js(title), js(summary), body)
i=s.index('const entries = [\n')+len('const entries = [\n'); s=s[:i]+entry+s[i:]
h=json.load(open(E/'headline.json'))
card=('  {\n    n: %d, kind: %s, tag: %s,\n    title: %s,\n    line: %s,\n    href: %s,\n  },\n')%(h['n'],js(h['kind']),js(h['tag']),js(h['title']),js(h['line']),js(h['href']))
j=s.index('const HEADLINES = [\n')+len('const HEADLINES = [\n'); s=s[:j]+card+s[j:]
# see-also link on Li's entry: first links array after its slug
k=s.index('slug: "341-li-disproof-refereed"'); l=s.index('    links: [\n',k)+len('    links: [\n')
see='      { label: "Follow-up, 14 October: Queneau\'s i<j variant is not always periodic either — Li\'s seed with 77 → 56 (ours)", url: "/day/'+slug+'" },\n'
s=s[:l]+see+s[l:]
print(f"entry {len(entry)} chars, card {len(card)} chars, see-also link added; dry={dry}")
if not dry: SRC.write_text(s,encoding='utf-8'); print("written", SRC)
