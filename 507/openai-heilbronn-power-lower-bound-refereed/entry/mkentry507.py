#!/usr/bin/env python3
# Assemble entry507.js from body.html + reading.html + world.html + world_replays.html (+ leanchecker_sentence.txt with --final).
# Refuses backticks / ${ in any piece. Pending placeholders survive only without --final.
import json, sys, os
E = '/tmp/oaimath/191/entry/'
body = open(E + 'body.html').read()
def piece(name, ph):
    global body
    f = E + name
    if os.path.exists(f):
        txt = open(f).read().strip()
        assert body.count(ph) == 1, ph
        body = body.replace(ph, txt)
piece('reading.html', 'READING_PARAGRAPH')
piece('world.html', 'WORLD_PARAGRAPH')
piece('world_replays.html', 'WORLD_REPLAYS_PARAGRAPH')
if '--final' in sys.argv:
    lc = open(E + 'leanchecker_sentence.txt').read().strip()
    assert body.count('LEANCHECKER_SENTENCE') == 1
    body = body.replace('LEANCHECKER_SENTENCE', lc)
body = body.replace('<p>\n</p>', '').replace('<p></p>', '')
assert '`' not in body and '${' not in body
title = ("#507: Heilbronn's triangle problem — OpenAI's claimed first power improvement over Komlós–Pintz–Szemerédi (every triangle ≥ c·n^(−2+η), "
         "η ≈ 3·10⁻²³⁶), its Lean replayed here and extended by us from a sequence of n to every large n; Formal Conjectures' open "
         "#507 lower-bound question and Green's problem 77 answered in Lean from it")
summary = open(E + 'summary.txt').read().strip()
links = json.load(open(E + 'links.json'))
assert '`' not in title + summary and '${' not in title + summary
out = []
out.append('  {')
out.append('    slug: "507-openai-heilbronn-power-lower-bound-refereed",')
out.append('    problemNum: 507,')
out.append('    title: ' + json.dumps(title, ensure_ascii=False) + ',')
out.append('    date: "2026-10-22",')
out.append('    status: "in_progress",')
out.append('    originatedByUs: false,')
out.append('    summary:\n      ' + json.dumps(summary, ensure_ascii=False) + ',')
out.append('    body: `\n' + body.rstrip() + '\n`,')
out.append('    links: [')
for t, u in links:
    out.append('      { label: ' + json.dumps(t, ensure_ascii=False) + ', url: ' + json.dumps(u, ensure_ascii=False) + ' },')
out.append('    ],')
out.append('  },')
open(E + 'entry507.js', 'w').write('\n'.join(out) + '\n')
print('entry507.js', len('\n'.join(out)), 'chars; pending:', [k for k in ('READING_PARAGRAPH', 'WORLD_PARAGRAPH', 'WORLD_REPLAYS_PARAGRAPH', 'LEANCHECKER_SENTENCE', 'BLIND_SENTENCE') if k in body])
