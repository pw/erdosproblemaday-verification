#!/usr/bin/env python3
# Assemble entry978.js from body.html + reading.html + m2_items.html + numbers.html. Refuses backticks / ${ in any piece.
import json, sys
E='/tmp/oaimath/020/entry/'
body=open(E+'body.html').read(); reading=open(E+'reading.html').read(); m2=open(E+'m2_items.html').read(); nums=open(E+'numbers.html').read()
verdicts=("M1, M2 and L returned HOLDS AS READ. W returned HOLDS AS READ on the Erdős sourcing, the cited ranges and the priority record, "
          "and one minor GAP, in Corollary 1.3 (below). The blind reader's corrections (among them that ours was not the first replay) are applied on this page.")
reading=reading.replace('SEAT_VERDICTS_SENTENCE', verdicts).replace('READING_M2_ITEMS\n', m2)
reading=reading.rstrip()
assert reading.endswith('</ul>\n<p>') or reading.endswith('<p>'), reading[-40:]
reading=reading[:reading.rfind('<p>')].rstrip()
old='<p><strong>The reading.</strong> READING_PARAGRAPH</p>'
assert body.count(old)==1; body=body.replace(old,'<p><strong>The reading.</strong> '+reading)
old='NUMBERS_PARAGRAPH</p>'
assert body.count(old)==1; body=body.replace(old, nums+'</p>')
lc=open(E+'leanchecker_sentence.txt').read().strip() if '--final' in sys.argv else 'LEANCHECKER_SENTENCE'
body=body.replace('<p>LEANCHECKER_SENTENCE</p>', '<p>'+lc+'</p>')
for piece in (body,):
    assert '`' not in piece and '${' not in piece
title=("#978: n⁴+2 is squarefree infinitely often — OpenAI's proof that every irreducible quartic with no fixed square divisor takes squarefree values "
       "with the predicted density, its Lean replayed here (a shorter route than the paper's) and its paper read by AI seats; Formal Conjectures' "
       "three #978 statements proved in Lean from it")
summary=("Erdős wrote in 1953 that he could not prove n⁴+2 squarefree for infinitely many n, and in 1981 that there was no quartic polynomial about "
  "which anyone could. Hooley had the (d−1)-power-free case in 1967; at d−2 the record for general polynomials stopped at degree 9 (Browning 2011; binomials to degree 6). OpenAI's preprint, dated "
  "24 September and public since 6 October, claims the (d−2)-power-free values have the predicted Euler-product density for every irreducible f of degree "
  "d ≥ 4 with no fixed prime (d−2)-th-power divisor: n⁴+2 is squarefree for about 75.67% of n. We replayed its Lean (63 modules, Mathlib only) in the kernel: "
  "standard axioms, statement and seven definitions matched to the comparator, independently of two earlier third-party replays. The Lean takes a shorter route than the paper "
  "(no archimedean determinant cuts, no quintic deletion) and proves degrees ≥ 9 itself, without Browning. Four AI seats read the paper: HOLDS AS READ on everything "
  "#978 needs, one fillable gap in a side corollary. Ours: Lean proofs of Formal Conjectures' three #978 statements, tagged solved there but still sorry, "
  "counts by two different methods, and a correction to our own July report. The theorem is OpenAI's.")
links=[
 ("erdosproblems.com/978 (read 22 Oct 2026: no proof claims, comments suspended, no mention of OpenAI; last edited 31 Mar 2026)", "https://www.erdosproblems.com/978"),
 ("OpenAI, \"Squarefree values of quartics and power-free values of polynomials\" (family 020, dated 24 Sep 2026, released 6 Oct, 55 pp)", "https://github.com/openai/math/tree/main/preprints/Squarefree-values-of-quartics-and-power-free-values-of-polynomials-September-24-2026"),
 ("OpenAI's Lean — OAI/NumberTheory/PowerFree (63 modules; entry Main.lean, theorem allDegrees at line 144)", "https://github.com/openai/math/tree/main/lean/OAI/NumberTheory/PowerFree"),
 ("OpenAI's comparator challenge ComparatorChallenges/PowerFreeValues.lean (the statement and its seven definitions)", "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/PowerFreeValues.lean"),
 ("Earlier replay: carlostoledo1891/cert-machine — Comparator on PowerFreeValues, Lean's kernel and nanoda accept (run 38019899278, committed 10 Oct 2026)", "https://github.com/carlostoledo1891/cert-machine/blob/main/corpus/openai-math/kernel-runs/38019899278/PowerFreeValues.json"),
 ("Earlier replay: nealmcb/openai-math-lean-tooling — Comparator over all 416 challenges, PowerFreeValues accepted 11 Oct 2026 (results/cmp-all/configs.csv)", "https://github.com/nealmcb/openai-math-lean-tooling"),
 ("Formal Conjectures, Erdős 978 at commit a7b87c8d — the three statements our bridge copies (parts.ii and parts.iii tagged research solved, proofs sorry)", "https://github.com/google-deepmind/formal-conjectures/blob/a7b87c8d0bb60e73782045d614d4a24907b87b8a/FormalConjectures/ErdosProblems/978.lean"),
 ("Formal Conjectures PR #6898 (Moritz Firsching, merged 11 Oct 2026): marks #978 parts ii and iii solved — build, link resolution and a sorry-grep, no kernel replay", "https://github.com/google-deepmind/formal-conjectures/pull/6898"),
 ("Erdős, \"Arithmetical properties of polynomials\", J. London Math. Soc. 28 (1953) — p. 425: n⁴+2", "https://users.renyi.hu/~p_erdos/1953-02.pdf"),
 ("Erdős, \"Some recent advances and current problems in number theory\" (1965) — §6, p. 219: (k−2)-th power-free values", "https://users.renyi.hu/~p_erdos/1965-17.pdf"),
 ("Erdős, \"Some problems and results on additive and multiplicative number theory\" (LNM 899, 1981) — p. 178: \"no quartic polynomial\"", "https://users.renyi.hu/~p_erdos/1981-33.pdf"),
 ("Heath-Brown, \"Powerfree values of polynomials\" (QJM 2013; arXiv 1103.2028) — binomials x^d + c, and the quartic case named as the open question", "https://arxiv.org/abs/1103.2028"),
 ("Reuss, \"Power-free values of polynomials\" (arXiv 1307.2802) — the number-field / approximate-determinant framework the paper follows", "https://arxiv.org/abs/1307.2802"),
 ("Xiao, \"Power-free values of binary forms and the global determinant method\" (IMRN 2017; arXiv 1505.05587) — Theorem 9.1, Browning's d ≥ 9 range as the paper cites it", "https://arxiv.org/abs/1505.05587"),
 ("Booker and Browning, \"Square-free values of reducible polynomials\" (Discrete Analysis 2016:8; arXiv 1511.00601) — Theorem 1.2, the k = 2 case of Corollary 1.3, uncited by the paper", "https://arxiv.org/abs/1511.00601"),
 ("Zapata Ceballos and Jalalvand, \"On the squarefree values of degree-2q polynomials\" (arXiv 2608.10335) — v1 11 Aug 2026 claimed n⁴+1 and n⁴+2; withdrawn 15 Oct 2026 at the large-prime-ideal step", "https://arxiv.org/abs/2608.10335"),
 ("Carella, \"Squarefree values of polynomials\" (arXiv 2310.16952, math.GM, 2023) — an unrefereed claim; our July report found a sign error in its decisive step", "https://arxiv.org/abs/2310.16952"),
 ("arXiv 2610.29911 (21 Oct 2026, random polynomials) — still says the squarefree asymptotic is known only up to degree 3 (Hooley), and does not cite OpenAI", "https://arxiv.org/abs/2610.29911"),
 ("Our July 2026 report on #978 (exact counts to 10⁵, the local factors of n⁴+2, a rigorous enclosure of the density; dated correction of 22 Oct on the open range)", "/report/978"),
 ("Our bundle (repository private at the time of writing; files available on request) — the replay (driver, per-module logs, probes, statement match and its mutation test), the bridge and its controls, the counting programs, referee reports, model receipts, SHA256SUMS", "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/978/openai-squarefree-quartics-refereed"),
]
L='\n'.join('      { label: %s, url: %s },' % (json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)) for a,b in links)
js=('  {\n    slug: "978-openai-squarefree-quartics-refereed",\n    problemNum: 978,\n    title: %s,\n    date: "2026-10-22",\n    status: "proof_claimed",\n'
    '    originatedByUs: false,\n    summary:\n      %s,\n    body: `\n%s`,\n    links: [\n%s\n    ],\n  },\n') % (json.dumps(title, ensure_ascii=False), json.dumps(summary, ensure_ascii=False), body, L)
assert js.count('`')==2 and '${' not in js
open(E+'entry978.js','w').write(js); print('entry978.js', len(js), 'chars; placeholders left:', [k for k in ('LEANCHECKER_SENTENCE','READING_','NUMBERS_','SEAT_VERDICTS') if k in js])
