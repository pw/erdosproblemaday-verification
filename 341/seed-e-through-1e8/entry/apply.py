#!/usr/bin/env python3
"""Insert the #341 seed-E entry + HEADLINES card + see-also links on the two earlier #341 entries into <worktree>/src/index.js.
usage: apply.py <worktree> [--dry-run]   (idempotent: refuses if the slug is already present; refuses on any placeholder)"""
import sys, pathlib, json, re
WT=pathlib.Path(sys.argv[1]); SRC=WT/'src/index.js'; dry='--dry-run' in sys.argv
E=pathlib.Path(__file__).parent
slug=(E/'slug.txt').read_text().split(':',1)[1].strip()
title=(E/'title.txt').read_text().strip(); summary=(E/'summary.txt').read_text().strip(); body=(E/'body.html').read_text().strip()
h=json.load(open(E/'headline.json'))
for name,txt in (('title',title),('summary',summary),('body',body),('headline',json.dumps(h,ensure_ascii=False))):
    m=re.search(r'⟨[A-Z0-9_]+⟩',txt); assert not m, f"placeholder left in {name}: {m.group(0)}"
    for ph in ("TODO","REPLACE_ME","XXX"): assert ph not in txt, f"{ph} in {name}"
assert '`' not in body and '${' not in body, "backtick/${ in body"
s=SRC.read_text(encoding='utf-8')
assert s.count('slug: "'+slug+'"')==0, "slug already present"
def js(x): return json.dumps(x, ensure_ascii=False)
entry=('  {\n    slug: %s,\n    problemNum: 341,\n    title: %s,\n    date: "2026-10-15",\n    status: "partial",\n    originatedByUs: true,\n    summary:\n      %s,\n    body: `\n%s\n`,\n    links: [\n'
       '      { label: "Verification bundle — both generators and their byte-identical controls, the 10⁸ run and its SHA-256, analyze.py and its logs, the window recurrence checker, the shield SAT and controller censuses, the [13]/[14] seed census, referee report, live-page captures", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/341/seed-e-through-1e8" },\n'
       '      { label: "Our July working report for #341 — the finite periodicity certificate, the 4,094-of-4,095 census of [12], and the original bounded wall for E", url: "/report/341" },\n'
       '      { label: "Our 13 October referee entry on Li\'s disproof (the shield + controller mechanism this entry tests against)", url: "/day/341-li-disproof-refereed" },\n'
       '      { label: "Our 14 October entry: Queneau\'s variant is not always periodic either (the forced-rail census tool reused here)", url: "/day/341-queneau-variant-not-periodic-either" },\n'
       '      { label: "Li, Counterexamples to Erdős Problem 341 (paper + Lean, GitHub) — Lemma 3.1 is the shield the SAT census encodes", url: "https://github.com/LiAlreadyExists/Erdos-341" },\n'
       '      { label: "Calkin, Erdős — On a class of aperiodic sum-free sets (Math. Proc. Camb. Phil. Soc. 1996): \\"there is currently no way to show that these sets are aperiodic\\"", url: "https://www.math.clemson.edu/~calkin/Papers/calkin_erdos.pdf" },\n'
       '      { label: "Finch — Are 0-additive sequences always regular? (Amer. Math. Monthly 99, 1992) and Guy, UPINT C4: the periodicity conjecture", url: "https://www.jstor.org/stable/2324932" },\n'
       '      { label: "Green, 100 open problems — Problem 7 (Dickson\'s and Queneau\'s rules)", url: "https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf" },\n'
       '      { label: "erdosproblems.com/341", url: "https://www.erdosproblems.com/341" },\n'
       '    ],\n  },\n') % (js(slug), js(title), js(summary), body)
i=s.index('const entries = [\n')+len('const entries = [\n'); s=s[:i]+entry+s[i:]
card=('  {\n    n: %d, kind: %s, tag: %s,\n    title: %s,\n    line: %s,\n    href: %s,\n  },\n')%(h['n'],js(h['kind']),js(h['tag']),js(h['title']),js(h['line']),js(h['href']))
j=s.index('const HEADLINES = [\n')+len('const HEADLINES = [\n'); s=s[:j]+card+s[j:]
for prev,label in (('341-queneau-variant-not-periodic-either','Follow-up, 15 October: the last seed in [12] — {1,4,8,10,11,12} has no period through 10⁸ and no shield at all (ours)'),
                   ('341-li-disproof-refereed','Follow-up, 15 October: no Li-type shield exists at any modulus below 49, and the six-element seed {1,4,8,10,11,12} resists every finite test through 10⁸ (ours)')):
    k=s.index('slug: "'+prev+'"'); l=s.index('    links: [\n',k)+len('    links: [\n')
    s=s[:l]+'      { label: '+js(label)+', url: "/day/'+slug+'" },\n'+s[l:]
print(f"entry {len(entry)} chars, card {len(card)} chars, 2 see-also links; dry={dry}")
if not dry: SRC.write_text(s,encoding='utf-8'); print("written", SRC)
