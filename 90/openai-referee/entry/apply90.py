#!/usr/bin/env python3
"""Insert the #90 entry into src/index.js (worktree ~/ErdosProblemADay-1014-0600) + a HEADLINES card.
Reads entry_body.html (placeholders already resolved), title.txt, summary.txt, headline.json; refuses if the slug exists."""
import json, re, sys, pathlib
WT=pathlib.Path('/home/exedev/ErdosProblemADay-1014-0600'); SRC=WT/'src/index.js'
E=pathlib.Path('/tmp/oaimath/167/entry')
slug="90-openai-unit-distance-power-saving-refereed"
s=SRC.read_text(encoding='utf-8')
assert ("slug: \"" + slug + "\"") not in s, "slug already present"
body=(E/'entry_body.html').read_text(encoding='utf-8').strip()
for ph in ("[[SEATS]]","[[WORLD]]","[[LABELS]]"): assert ph not in body, ph+" unresolved"
title=(E/'title.txt').read_text(encoding='utf-8').strip()
summary=(E/'summary.txt').read_text(encoding='utf-8').strip()
hl=json.loads((E/'headline.json').read_text(encoding='utf-8'))
status=(E/'status.txt').read_text(encoding='utf-8').strip()
assert status in ("proof_claimed","in_progress","posted","partial","refuted","declined")
links=[
 ("OpenAI, \"A power saving for planar unit distances\" (23 Sept 2026, 53 pp — the claim under review; paper only, no Lean)", "https://github.com/openai/math/blob/main/preprints/A-power-saving-for-planar-unit-distances-September-23-2026/paper.pdf"),
 ("OpenAI's scope note for family 167 — lean/docs/167.md (formalises the weak pinned theorem only; \"the separate unit-distance power-saving theorem is not included\")", "https://github.com/openai/math/blob/main/lean/docs/167.md"),
 ("OpenAI, \"Planar point sets with many unit distances\" (20 May 2026 — the disproof of the n^{1+o(1)} conjecture, n^{1+c})", "https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf"),
 ("Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood — Remarks on the disproof of the unit distance conjecture (arXiv:2605.20695)", "https://arxiv.org/abs/2605.20695"),
 ("Sawin, An explicit lower bound for the unit distance problem (arXiv:2605.20579)", "https://arxiv.org/abs/2605.20579"),
 ("Guth, survey on the unit distance problem (arXiv:2609.10791, Sept 2026 — the newest item on the problem's forum)", "https://arxiv.org/abs/2609.10791"),
 ("Székely, Crossing numbers and hard Erdős problems in discrete geometry (CPC 1997) — the incidence theorem the paper starts from", "https://doi.org/10.1017/S0963548397002976"),
 ("Katz–Tardos, A new entropy inequality for the Erdős distance problem (2004) — the fibre-resampling idea behind the prediction device", "https://www.ams.org/books/conm/342/"),
 ("The problem's forum thread (47 comments: the disproof's Lean formalisations, the lower-bound exponent record, Bloom's number-field conjecture)", "https://www.erdosproblems.com/forum/thread/90"),
 ("Our audit bundle — brief, nine referee reports, our checks with controls, world captures", "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/90/openai-referee"),
 ("erdosproblems.com/90", "https://www.erdosproblems.com/90"),
]
def js(x): return json.dumps(x, ensure_ascii=False)
entry="""  {
    slug: %s,
    problemNum: 90,
    title: %s,
    date: "2026-10-14",
    status: %s,
    originatedByUs: false,
    summary:
      %s,
    body: `
%s
`,
    links: [
%s
    ],
  },
""" % (js(slug), js(title), js(status), js(summary), body.replace('`','&#96;').replace('${','$​{'),
       "\n".join("      { label: %s, url: %s },"%(js(a),js(b)) for a,b in links))
anchor='const entries = [\n'
assert s.count(anchor)==1
s=s.replace(anchor, anchor+entry, 1)
# HEADLINES card at the top of the array
h_anchor='const HEADLINES = [\n'
assert s.count(h_anchor)==1
card="""  {
    n: 90, kind: %s, tag: %s,
    title: %s,
    line: %s,
    href: "/day/%s",
  },
""" % (js(hl["kind"]), js(hl["tag"]), js(hl["title"]), js(hl["line"]), slug)
s=s.replace(h_anchor, h_anchor+card, 1)
SRC.write_text(s, encoding='utf-8')
print("inserted entry + headline; body chars", len(body))
