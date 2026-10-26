# W_factcheck — hostile fact-check of /tmp/oaimath/003/entry/update970.html and update431.html
Checked 2026-10-26 ~10:05Z against: W_work/ primary sources (Tao posts, arXiv/Hexagon PDFs, GitHub records, live pages fetched 10:02Z in W_work/live/), and the seat reports R0_main_seat_read.md, R1_report.md, C_report.md, D_report.md, W_report.md, plus R1_BRIEF.md / C_BRIEF.md and the paper TeX.
Severity: A = false or misattributed statement of fact; B = overstatement / misleading; C = precision or cosmetic. LEANCHECKER_RESULT ignored as instructed.

Checked and CLEAN (no objection): Theorem 1 wording; Banks 11 Oct 2610.15483 and Kerr 15 Oct 2610.21099 (dates, ids, "explicit constants", "direct proof"); Green 17 Oct; the Tao quote "the Siegel zero problem has been solved in a number of ways" (verbatim substring of his 19 Oct post, which begins "Recently, ..."); atimics/math2 on 8 Oct (created 8 Oct 01:15Z, last push 8 Oct 19:02Z); c = (log 3)/8; D's facts (Lean 4.34.1, Mathlib d13f23b, 67 modules, 0 errors, axioms propext/Classical.choice/Quot.sound, 46/5,316/0-foreign constants, 6 mutants, LSeries-version false, mod-3 witness, no axiom/sorry/macro/global notation/relevant global instance, 37 modules used only for the multiplicity estimate, 105 files, 0 hits for nearest-point/Lagrange); C's numbers 7 fields and their list, 188 cases, 91 equalities, 84/93, 56/84, 75 of 81; R1's three exposition notes; the quotes "open in the published literature" (970 live page: "that is open in the published literature"; 431 live page: "It is open in the published literature") and "a result of this size wants specialists before anyone leans on it" (431 live page, verbatim); the slug /day/970-openai-jacobsthal-quadratic-refereed exists live; "#687 bridge" is real (Bridge687.lean on the live 970 page); 431's "Nothing in route C ... changes" matches the live 431 page ("route C's closure contains no module from that directory").

## Objections

### 1. (B) "refereed" in the headline — update970 first sentence; update431 first sentence
Draft: "we have now refereed the no-Siegel-zero proof, and the world was well ahead of us." / "the no-Siegel-zero proof is now refereed here".
Wrong: no human referee and no journal; the same drafts end "No journal has refereed any of this yet", and the live 970 page labels exactly this kind of result "(d) ... unrefereed by any human" and the paper's argument "(c) as a written proof ... read here by AI seats". A number theorist will read "refereed" as formal refereeing. Source: live 970 page (labels paragraph), R1/R0 are AI-seat reads.
Correct: "we have now read the no-Siegel-zero proof with AI referee seats, and the world was well ahead of us." / "the no-Siegel-zero proof has now been read and checked here by AI referee seats".

### 2. (A) Wrong first name — update970 last bullet
Draft: "Seat W found that Jacob Reilly (jmreilly1113) had already formalized ..."
Wrong: the author is Joseph M. Reilly (repo jmreilly1113/siegel-zeros-audit, README licence line "Copyright 2026 Joseph M. Reilly"). Source: W_work/reilly/README.md l.39.
Correct: "Seat W found that Joseph M. Reilly (jmreilly1113) had already formalized the paper's own Lemma 3 (8–9 October) and rerouted OpenAI's Lean proof through it, replacing its Corollary 4 by +2/−1 lines; the official comparator with Lean's kernel and nanoda accepts that version."

### 3. (A) "unprompted" — update970 sanity bullet
Draft: "Three seats, separately and unprompted, asked what the determinant argument proves when there is no Siegel zero."
Wrong: R1's brief required it ("SANITY TEST (do at least one): an argument that excludes Siegel zeros must not also 'prove' something false ... compare with what Chebotarev/PNT says"). C's brief did not ask; the main seat's read (R0) and C's §3(d) did it on their own. Source: R1_BRIEF.md l.23; C_BRIEF.md (no such task); R0; C_report §3(d).
Correct: "Three seats, working separately (R1 because its brief required it, the main seat and seat C on their own), asked what the determinant argument proves when there is no Siegel zero."

### 4. (A) N = 4 "for one field" — update970 "Exact computation" bullet
Draft: "(matrices up to 81 × 81, and 256 × 256 at N = 4 for one field)"
Wrong: N = 4 (256 × 256) was run six times on five fields: d = −1 (H = 3, 6), −3 (H = 4), −7 (H = 5), 13 (H = 2), 5 (H = 3). Source: C_report §2a (N=4 list), C_report §1.
Correct: "(matrices up to 81 × 81 for N = 2, 3 across all seven fields, and 256 × 256 at N = 4 in six runs on five of them)". Also state that H took the values 1, 2, 3, 5, 8 (N ≤ 3) and 2–6 (N = 4), rather than "from 1 to 8".

### 5. (A) The quoted paragraph does not end there — update970 first paragraph
Draft: "The paragraph above ends "Nobody here has refereed it.""
Wrong: on the live 970 page the sentence is mid-paragraph; it is followed by "What this changes: ... What it does not change: the paper, which the seats below read, does not need the larger claim." Source: W_work/live/day_970-...txt l.45.
Correct: "The paragraph above says "Nobody here has refereed it.""

### 6. (B) "proves nothing false" — update970 sanity bullet
Draft: "So for a fixed field the method sits exactly on the truth, with nothing to spare, and proves nothing false."
Wrong/overstated: the test is leading-order and heuristic. R1: "the method proves nothing false that I could find", and its own note that the remaining O(S) terms were "a rough heuristic estimate ... not a computation"; C: "does not prove a falsehood unconditionally at leading order"; R0: "no slack to spare (as H, γ → ∞)". Source: R1 sanity section; C §3(d); R0.
Correct: "So for a fixed field the method sits, at leading order, exactly on the truth, with nothing to spare; none of our three tests made it contradict Chebotarev."

### 7. (A/B) The identity class is our extension, not the paper's — update970 sanity bullet
Draft: "The divisibility step works for every prime whose Frobenius is one of the three conjugations used as variables (the identity, σ or στ)"
Problem: Lemma 7 in the paper covers only p > H with χ(p) = −1, i.e. σ and στ. Identity-class primes are the main seat's extension (R0: argued), C tested it (46 cases, 0 failures), R1 extended Lemma 7 to all classes. As written the page attributes it to the paper. Source: paper Lemma 7; R0 sanity; C §3(d)(i); R1 sanity.
Correct: "The paper's Lemma 7 treats primes with Frobenius σ or στ. The same replacement trick also works for the identity class (our extension, checked by seat C in 46 cases), so the argument bounds the share of primes with Frobenius in {identity, σ, στ} ..."

### 8. (B, mathematics) "almost all primes" — update970 "How the proof goes", sentence 1
Draft: "forces almost all primes up to a fixed power of q to have χ(p) = −1 (Lemma 2 ...)"
Misleading: the primes with χ(p) = −1 have density 1/2. Lemma 2 says Σ_{χ(p)=1} log p/p ≪ ℓ + δ(log X)²/ℓ, i.e. almost all of the weight Σ log p/p (up to X = q^C, C large, δ small) sits on χ(p) = −1. A number theorist will object to "almost all primes". Source: paper §2 eq. (2.1)–(2.2); R0 ("almost all log-mass of primes").
Correct: "forces almost all of the logarithmic weight Σ log p/p over primes up to q^C (C a large fixed constant) onto primes with χ(p) = −1".

### 9. (C, mathematics) "every such p" — update970, Lemma 7 sentence
Draft: "so Δ is divisible by a large power of every such p (Lemma 7)."
Imprecise: Lemma 7 needs p > H, p ∤ 2q, χ(p) = −1, and the power is E_p = Σ⌊α₁/p⌋ (large only for p ≤ U). C showed it fails for p ≤ H (56 of 84 cases, N ≤ 3). Source: paper Lemma 7; C §3(b).
Correct: "so Δ is divisible by p^{E_p}, a large power, for every prime p > H with χ(p) = −1 and p ∤ 2q (Lemma 7)."

### 10. (B) "Six altered statements are rejected" — update970 Lean bullet
Draft: "Six altered statements are rejected."
Misleading by omission: D states that three of the six (β ≤ 2, drop χ ≠ 1, drop primitivity) are mathematically implied by or equivalent to the theorem; their rejection shows the check is definitional, not that they are false. Only the LSeries mutant is provably false; the no-log mutant is far stronger. Source: D_report Task 3, "Mutants" note.
Correct: "Six altered statements are rejected by the kernel at the term (three of them are true or equivalent statements, so that shows the match is definitional; the semantic discriminators are the 'c ≤ 1 − β' mutant and the LSeries one)."

### 11. (A) "three sentences ... behind the record" — update431 first sentence
Draft: "three sentences above were behind the record. We wrote that ... 'is open in the published literature', that 'nobody on our side has refereed' the proof, and that 'a result of this size wants specialists ...'"
Wrong: the middle sentence ("Nobody on our side has refereed ...") was true on 23 Oct; it is superseded by this update, not behind the record. The 970 draft correctly says "Both". Source: live 431 page l.66, 69; update970 last paragraph.
Correct: "two sentences above were behind the record, and a third is now out of date."
Also quote form: the live text is "Nobody on our side has refereed the 105 modules or the preprint behind them"; the draft's lower-case "nobody ... refereed" is a fragment, fine if marked as such.

### 12. (A/B) Who did what — both drafts, "the main seat and four AI seats read OpenAI's nine-page preprint and audited the Lean"
Overstates: line-by-line reading of the paper was done by the main seat (R0) and R1; seat C recomputed its lemmas exactly (and re-derived Lemma 3's proof; Lemma 2/§6 only re-read); seat D audited the Lean and read the paper only to map it (no mathematics refereeing); seat W surveyed the public record and checked the bibliography, and did not referee the paper. Source: R0, R1, C §6, D scope, W_report §3.1.
Correct: "the main seat and seat R1 read the nine-page preprint line by line, seat C recomputed its lemmas exactly on small cases, seat D audited the Lean behind dirichlet_real_zero_bound, and seat W surveyed the public record."

### 13. (A, unsourced) "Patrick asked us to" — update970 first paragraph
No seat file, brief or live page records this request (grep of all briefs and the live pages: no "Patrick"). Either confirm with the coordinator or drop. Correct (if unconfirmed): delete "Patrick asked us to, and".

### 14. (B) Absence claims — update970 last paragraph; update431
Draft: "No journal has refereed any of this yet, and nobody has reported a gap." / "None of it is refereed in a journal yet, and nobody has reported a gap."
W searched web, GitHub, arXiv, Hexagon, Tao's posts/comments, HN, and found no report of a gap; but X, Zulip, MathOverflow, Reddit were not searchable, and I did not check journals. An absence claim must be stated as one. Source: W_report "Searched and found nothing" and "could NOT check".
Correct: "None of it has appeared in a journal that we know of, and we found no public report of a gap (we could not search X, Zulip or MathOverflow)."

### 15. (C) Dates for the replays — update970 last paragraph
Draft: "From 9 October, third parties had replayed ... with Lean's kernel and the independent nanoda kernel (jmreilly1113, carlostoledo1891/cert-machine, nealmcb)."
Precision: Reilly's comparator + nanoda run is dated 8 Oct (posted 9 Oct); cert-machine run 10 Oct (both kernels); nealmcb's comparator run 11 Oct used Lean's kernel only (nanoda on SiegelZeros's export in a separate paired sweep, 15 Oct). Source: W_report §2.1 (results/2026-10-08-lean-comparator-nanoda-netblock.txt; cert-machine run 38019899278; nealmcb configs.csv, kernel-pair-sweep.jsonl).
Correct: "From 8–9 October, third parties had replayed OpenAI's comparator challenge SiegelZeros: Reilly (8–9 Oct) and cert-machine (10 Oct) with Lean's kernel and nanoda together, nealmcb (11 Oct) with Lean's kernel and, in a separate sweep (15 Oct), nanoda."

### 16. (C) The quasi-RH route — update970 last paragraph
Draft: "The same statement also follows from the family's quasi-Riemann-hypothesis theorem (no zeros with Re s > 7/8) ... so the Lean has a second route through different mathematics."
Precision: it is the Dirichlet-L version (DirichletSevenEighths, all q and all characters), not the zeta-only statement, that implies it. A number theorist should also be told that specialists have studied the 11/12 paper and set the 199-page 7/8 paper aside (Quanta 19 Oct), so this is redundancy at the Lean level, not a second human-checked proof. Source: atimics/math2 README and Fidelity/Checks.lean; Quanta 19 Oct (W_work/press2/quanta.txt).
Correct: "The same statement also follows, with c = (log 3)/8, from the family's theorem that no Dirichlet L-function has a zero with Re s > 7/8 (atimics/math2, 8 October), so the Lean has a second route through different mathematics, though specialists have studied the 11/12 paper rather than the 7/8 one."

### 17. (B) Unsourced process claim — update970 last paragraph
Draft: "...because that day's search covered GitHub code and not the mathematics."
The only record is /tmp/oaimath/013/world/gh_search_siegel.txt (code searches by the 09:00Z seat and B2); no 003 seat report states what was not searched. Keep only if the coordinator can confirm.
Correct: "...because our search that day was of GitHub code, not of the mathematical literature."

### 18. (C) Quote capitalisation — update970 bullet 1
Draft: 'The §6 sentence "analyticity therefore prevents zeros from accumulating at 1" is terse.'
Paper §6: "Analyticity therefore prevents zeros from accumulating at $1$." (paper.tex l.673).
Correct: 'The §6 sentence "Analyticity therefore prevents zeros from accumulating at 1" is terse.'

### 19. (C) Symbols — update970 bullet 1
Draft: "The letter H is both the weight and the hyperplane, and K is both the field and the dilated polytope."
The hyperplane and the polytope are calligraphic (\mathcal H, \mathcal K, paper.tex l.374; R1 E2). Correct: "H is the weight and calligraphic ℋ the hyperplane; K is the field and calligraphic 𝒦 the dilated polytope."

### 20. (C) Small precision items — update970
(a) "84 of 93" and "56 of 84" are N ≤ 3 subtotals (with N = 4: 95 of 105 and 58 of 89); add "(N ≤ 3)". Source: C §3(a),(b).
(b) "with the same constants (H ≥ 86,713,344)": the paper prints c₀ = (4·97²)⁻¹, C₀ = 192 and requires (C₀/c₀)/H ≤ 1/12; 86,713,344 = 12·C₀/c₀ is the number the Lean uses. Correct: "(H ≥ 12·C₀/c₀ = 86,713,344 in the Lean)". Source: paper l.549, l.694; D Task 5.
(c) "a different and much longer zero estimate": D did not measure relative length (it did not read the ≈15k lines); write "a different and long multiplicity estimate".
(d) "so that hypothesis is doing real work": C also found the paper's own ℚ-dependent cases (d = 2, 4, 8) did NOT lose rank at N = 2, 3, so the hypothesis is sufficient, not shown necessary; add "(sufficient; not shown necessary at these sizes)". Source: C §4(iii).

## Overstated "our seats" check
Items 1, 3, 6, 7, 12 are the places where the drafts claim more than the seats did. No claim of priority or novelty for our seats appears in either draft apart from these; the closing paragraph ("our read is one of many, and late") is accurate.

VERDICT: 20 objections (A: 2, 3, 4, 5, 11, 12 (partly), 13; B: 1, 6, 7, 8, 10, 14, 17; C: 9, 15, 16, 18, 19, 20) — fix 1–8, 10–14 before publishing.
