# Blind consistency read — /day/1150 (body1150.html + entry1150.js + card1150.js), 2026-10-12

Page line numbers refer to the de-tagged prose of body1150.html (python strip of tags, `cat -n`); record lines are file:line.
Final (2026-10-12). Reader had no stake in the page; reading only, no lake/lean run.

## Issues

1. **SUBSTANTIVE — no seat read the 28-page paper's own chain, but the page/entry/card say all three papers were read.**
   Page l.193 (Labels): "The two-sided ultraflat theorem (1 ± ε)√N and the √N/16 lower bound: (c) — paper-only, **one seat each on
   their own chains**, no kernel." Entry summary (entry1150.js:8): "seven tool-equipped referee seats … found no gap in **any of the
   family's three papers**." Card (card1150.js:4): "Seven hostile seats **read all three papers** of the family: no gap." Title
   (entry1150.js:4): "seven hostile seats read the three papers: no gap".
   Records: seats/PROMPTS.md:5–83 — the seven scopes are sib1 (reduce/construct/sample/round/lean), the 16-page ultraflat paper
   (ultra), and citations/world (world). No seat has the 28-page "Nearly minimal maxima and positive minima" paper (sib2) or its
   √N/16 theorem in scope. The only sib2 reading anywhere is ultra's inherited-input check (referee_ultra.md:3, 7–9: "sib2: p. 9 (Lemma
   3.1 statement + Theorem 3.2), pp. 10–13 (proof of Lemma 3.1, read at skim-plus level) … pp. 23–25 (Lemma 6.1 statement, Lemma
   6.2 statement + full proof"); referee_ultra.md:163–164 "sib2 Lemma 3.1's PROOF: skimmed … not re-derived". The √N/16 lower-bound
   chain (sib2's own §§4–5/positive-minimum argument) was read by nobody. The page's paragraph on "the seven seats" (l.97–139) itself
   lists no sib2 seat. Fix: say the √N/16 theorem was not refereed (only two of its lemmas, as inputs to the 16-page paper), and drop
   "all three papers" from summary/card/title.

2. **SUBSTANTIVE — the sample seat's uniformity finding is misreported.** Page l.117–119: "Lemma 5.1 line by line … **uniform in the
   block centre because Lemma 4.2's error does not depend on u**". The seat's answer is the opposite on the block centre:
   referee_sample.md:62–67 "Uniform in b ∈ J … head |ℓ|≤L by Lemma 4.2, whose error … is independent of u … **The block centre x* and λ
   are FIXED data of each application, not varying parameters; the paper never needs uniformity in x*** because there are finitely
   many blocks (H fixed). Constants depend on (χ, x*, λ, J) only". What u-independence buys is uniformity in b (i.e. in the angle t),
   not in the block centre (sample brief PROMPTS.md:27 asked about "the block centre, the angle t, and … J" separately). Fix: "uniform
   in the angle (b ∈ J) because Lemma 4.2's error does not depend on u; the block centres are fixed data, finitely many".

3. **SUBSTANTIVE — Bloom's 8 October post DOES list #1150; the page says it does not (and contradicts itself).** Page l.175–176:
   "Nobody on the page has mentioned the OpenAI release; **it is not among the 25 problems in Bloom's 8 October blog post**". Records:
   referee_world.md:167–169 "Bloom, 'Erdős problems in the OpenAI proofs', 8 Oct 2026 … ✔: **lists [1150] 'Ultraflat Littlewood
   polynomial'**: 'This PDF claims a proof of the following …'"; world_work/world_search.md:27–35 ("There are significant claims relevant
   to 25 Erdős problems." (list includes [1150]) + the verbatim 1150 section); world_work/raw/blog10.txt:88, 435–441 ("[1150]",
   "- Ultraflat Littlewood polynomial"); the 25 bracketed problem numbers in blog10.txt include 1150. The page's own next paragraph
   (l.181) then counts "Bloom's post ('not … any kind of endorsement')" as one of the three reactions to 076. Fix: "it is among the 25
   problems in Bloom's 8 October post, as a claim, with his explicit non-endorsement (he summarizes the one-sided bound and links the
   16-page PDF)".

4. **SUBSTANTIVE — "Vaaler's 1999 list 2.36" names the wrong source.** Page l.3–4: "Hayman's 1974 problem list 4.31, **Vaaler's 1999
   list 2.36**". The only record is the citation key: live/thread1150.html (rendered l.27) "#1150: [Ha74,4.31][Va99,2.36]". On
   erdosproblems.com / Formal Conjectures, [Va99] is "Various, Some of Paul's favorite problems. Booklet produced for the conference
   'Paul Erdős and his mathematics', Budapest, July 1999" (~/.cache/erdos-sources/formal-conjectures/FormalConjectures/ErdosProblems/
   README.md and 119.lean reference lists). No record carries "Vaaler". ([Ha74] = Hayman, Research problems in function theory: new
   problems (1974) is right.) Fix: "the 1999 Budapest problem booklet, 2.36".

5. **MINOR — "read … by us" for the merit-factor corollary is not in our own reads.** Page l.193–195 (Labels): "The merit-factor
   corollary that refutes Turyn's conjecture: (b) rigorous modulo Theorem 1.1 — an elementary deduction, read by the round seat **and by
   us**." The page's "Our own reads" paragraph (l.155–164) covers §2, §6.2 and §7 (Corollary 7.1) only; §8 / Corollary 8.1 is not
   listed (README.md:42 "Our own reads (page text): §2, §6.2, §7"). The round seat did read it (referee_round.md:64–67). Either add §8 to
   the own-reads paragraph (it is the same ∫f⁴ ≤ ‖f‖∞²∫f² step) or drop "and by us".

6. **MINOR — module/line/scan bookkeeping in the source-audit sentence.** Page l.48–52: "the import cone of Main is 24 modules and 9,315
   lines **under OAI/Analysis/Littlewood/ (28 modules, 9,712 lines with FiniteFlatness), importing nothing but Mathlib**; **zero
   occurrences of sorry, admit, axiom, …**". (a) The 28-module joint cone is not all under Littlewood/: lean/cone_joint.txt:28 is
   `OAI.MeasureTheory.Integral.BoundedMoments`, and MinimizingFamily imports `Lean.Elab.Tactic.NormCast`/`Lean.Elab.Tactic.Omega`
   (scan.log:2–4; README.md:18–19 says so explicitly). Main's 24-module cone is Mathlib-only (correct). (b) The scan that produced the
   zeros covered the 27 files / 9,601 lines of the Littlewood directory (scan.log:1; scan.sh:4–5), not the 28-module/9,712-line cone —
   BoundedMoments.lean was not scanned (it was compiled in the replay). (c) "zero occurrences of … axiom": scan.sh counts only
   line-start declarations (`^\s*axiom\b`, comment lines excluded); there is one occurrence of the word in a docstring (Averages.lean:157,
   referee_lean.md:37–38). Say "no axiom declarations".

7. **MINOR — "three of the paper's cited inputs" vs "two of the paper's citations".** Page l.57–60: "replaces three of the paper's
   **cited** inputs — Pippenger–Spencer …; Lovett–Meka …; and the grid-to-circle step by a Dirichlet-kernel Cauchy–Schwarz argument
   instead of the maximum principle". The grid-to-circle step is the paper's own uncited argument (sib1/pages/p020.txt–p021.txt: maximum
   principle + Cauchy, no reference), and the page's own Labels (l.191) and l.62 say "two of the paper's citations". referee_lean.md:129–130
   calls it the third "heavy external input", i.e. external to the formal route, not a citation. Fix: "two cited inputs and one in-house
   analytic step".

8. **MINOR — plasma-ai is a self-report, presented as an existing machine check.** Page l.83–84: "Two outside machine checks of the same
   Lean exist (carlostoledo1891/cert-machine …; plasma-ai/erdos, 7 October)". referee_world.md:191–193: plasma-ai "**claims** it built the
   module … (who/what ran it — human or AI — not stated)"; only cert-machine was checked against its published JSON (✔, l.187–190).
   Wording: "one outside machine check with a published log (cert-machine) and one claimed (plasma-ai)".

9. **MINOR — "about twenty exposition notes" undercounts.** Page l.139. Count from the reports: reduce E1–E3 (3), construct E1–E5 (5),
   sample E1–E3 (3), round E1–E4 (4), lean E1–E4 (4), ultra 1–5 (5), world W1+W3 (2) = **26** (referee_*.md "Findings" sections). README.md:41
   repeats "~20". Say "about two dozen" or "26".

10. **MINOR — the world seat's numerics are slightly overstated.** Page l.136–137: "**exact** brute-force mN for N ≤ 20 (**1.146 to
    1.433**) matches Odlyzko's exhaustive Figure 1". (a) referee_world.md:45 "Method (**rigorous up to float rounding**)" — grid +
    refinement, not exact. (b) m_1 = 1.0000 (referee_world.md:51); 1.146–1.433 is the range for 2 ≤ N ≤ 20 (the seat's own l.76 has the
    same slip). (c) Odlyzko's Fig. 1 covers n = 10..50, so only N = 11..20 were compared, "to plot resolution" (referee_world.md:58–61).

11. **MINOR — Appendix A's other two targets misdescribed.** Page l.174–175: "OpenAI's Appendix A names the same quantifier defect, in
    the same place, and **two more in the later preprints**." Of the other two preprints, 1609.03435v2 is EARLIER (2016/Jan 2017), and
    for it Appendix A names no defect at all — it only reconciles the endpoint convention (referee_reduce.md:58–62, 143–145, E3: "Appendix
    A examines no step of the argument"). The two further defects (Theorem 1 false; Corollary 3 identity) are both in ONE later preprint,
    2509.04212 (referee_reduce.md:81–90). Fix: "and two more in the later 2509.04212".

12. **MINOR — "five hours" is an estimate.** Page l.85–86: "which would have held it for five hours". Record: README.md:31 "est. 5 h
    wait"; replay/gated_driver_retired.log shows only 10 minutes of waiting (09:12:34–09:22:35Z). Say "an estimated five hours".

13. **MINOR — the leanchecker --fresh pass is over Main's closure only.** Page l.91–92: "the leanchecker --fresh pass over **the whole
    import closure**, Mathlib included". manual/build.sh:51 and build.log:44 run `leanchecker --fresh OAI.Analysis.Littlewood.Main` —
    FiniteFlatness's four extra modules (FlatnessModel, MinimizingFamily, BoundedMoments, FiniteFlatness) are outside it, though the
    previous sentence covers both theorems. Say "over Main's import closure".

14. **MINOR — "verbatim" / "exactly the negation" overstate.** Page l.41 "— Theorem 1.1 **verbatim**"; l.24 "This alone **is** the
    negation of #1150"; title (entry1150.js:4) "the Lean proves **exactly** the negation of what was asked"; label1150.txt "which is exactly
    the negation of #1150". The comparator is sib1 p.2's "Equivalently" form plus a `1 ≤ N₀` clause (sib1/pages/p002.txt:44–56;
    lean/AsymptoticallyMinimalLittlewood.lean:14), and it is in length-N/√N form, which **implies** the negation only via the bridge; the
    lean seat: "strictly STRONGER than the negation of #1150 (which needs only infinitely many n)" (referee_lean.md:61–62, 80). The page's
    own Labels (l.186–188) correctly treat the bridge as a separate (a) step. Use "implies"/"the 'Equivalently' form".

15. **MINOR — N = 2 remark: "it fails" reads as the theorem failing.** Page l.63: "the statement is not vacuous (at N = 2 the best
    maximum is 2, so **it fails** for η < √2 − 1)". Arithmetic is right (min max of ±1±z is 2 = √2·√2; (1+η)√2 < 2 ⇔ η < √2−1;
    referee_lean.md:135–136; m_2 = 1.4142, referee_world.md:51) but what fails is the N = 2 instance, forcing N₀ ≥ 3 — the theorem is
    claimed for all η. Say "so the bound fails at N = 2 for η < √2 − 1, forcing N₀ > 2".

16. **MINOR — universal about Mathlib axioms.** Page l.75–76: "the axioms **every** Mathlib theorem carries and nothing else". Many Mathlib
    theorems depend on a subset or none of propext/Classical.choice/Quot.sound; the records show only that these are the json's
    `permitted_axioms` (lean/AsymptoticallyMinimalLittlewood.json:8–12). Say "the three standard axioms Mathlib uses".

17. **MINOR — Pippenger–Spencer original stated from memory.** Page l.112–113: "(the 1989 Pippenger–Spencer original is paywalled **and
    its extra D ≥ D₀ hypothesis is harmless**)". referee_construct.md:25–27, 124: "the 1989 Pippenger–Spencer original (paywalled, **NOT
    fetched**) carries a D ≥ D₀ hypothesis" — the hypothesis is the seat's recollection, unverified against the source. Say "reportedly
    carries … (not fetched)".

18. **MINOR — GGTW Figure 16 cause stated as fact.** Page l.148–150: "… against a true 1.2808 — **a mesh defect** in that paper".
    referee_world.md:66–68: the low points are "**consistent with** their stated evaluator (max over a mesh … misprinted 'K = 6, 7')" — an
    inference. Also l.148 "≈ 1.10 at degree 11 against a true 1.2808": degree 11 = N = 12, m_12 = 1.2808 ✓.

19. **MINOR — sample seat's "at most one stationary contribution" reason truncated.** Page l.119–120: "at most one stationary contribution
    per angle because a nonzero term forces a strict inequality and the packed intervals are shorter than one". referee_sample.md:68–72:
    strict inequality ⇒ −t in the interior of I_{a,h}; **Lemma 3.1's pairwise disjointness of all 2rH closed intervals** ⇒ at most one
    (a,h); length < 1 ⇒ at most one ℓ. "Shorter than one" alone gives only the ℓ-uniqueness. Add "disjoint and".

20. **MINOR — "the kernel-checked object is the headline statement" vs the page's own "family's headline".** Page l.151: "here, unlike
    #3, the kernel-checked object is **the headline statement**"; page l.30 calls the two-sided (3) "**the family's headline**", and
    referee_world.md:184–186: CONTENTS.md's 076 headline is two-sided and "the two-sided headline is NOT what is formalised". Say "the
    statement #1150 turns on".

21. **MINOR — "seven … seats … found no mathematical gap" in sib1 overcounts.** Page l.189–190 (Labels, "The paper as written" = the
    26-page paper): "seven tool-equipped machine seats with disjoint scopes … found no mathematical gap". The ultra seat's scope is a
    different paper (referee_ultra.md:1–3) and the world seat checked citations/numerics only, "Did not read §§3–6, 8 of sib1 for
    mathematics" (referee_world.md:235). Five seats (reduce, construct, sample, round, lean) read sib1's mathematics. (Companion to #1.)

22. **MINOR — BBMST "at every degree".** Page l.10–11: "proved two-sided flatness with fixed constants **at every degree**". BBMST Thm 1.1
    is "for all n ⩾ 2" (referee_world.md:113–114; referee_ultra.md:158–159) — degree 1 (1 ± z, which vanishes on the circle) is excluded.
    Say "at every degree n ≥ 2".

## Checked and found consistent (no issue)
- Problem statement, [Ha74,4.31], "last edited 23 January 2026", 5 comments / 0 proof claims, $100 prize via Erdélyi [Er06] (Alfaiz),
  DanielChin's Problem-22 remark, Bloom (04 Feb, verbatim with ellipsis), Tao (04 Feb, verbatim with ellipsis), el Abdalaoui 16 Aug 2026 —
  live/thread1150.html.
- teorth: open, last_update 2026-01-23, formalized yes (2026-02-06), no prize — ~/.cache/erdos-sources/teorth problems.yaml:18988–19000;
  TRACKER_AT 2026-10-12.
- Formal Conjectures (fetched live 2026-10-12, identical to world_work/raw/fc_1150.lean): answer(False), research solved, formal_proof link
  Main.lean#L187, body `sorry`, predicate unchanged; PR #6898 merged 2026-10-11 (world_search.md:45).
- Paper hashes (3f6f94e6…, 639fe69d…, 89e4fd2b…) = sha256 of the on-disk PDFs; page counts 26/28/16; dates 23 Sept / 5 Oct / 5 Oct; titles;
  sib1 Theorem 1.1 + "Equivalently" (p.2), K_δ = √((1+δ)³/(1−δ)), 1−7δ, Lemma 2.2's C(1+√(µ log(80N/µ))), µ = ½Σ(1−|X_k|), 1−8δ ⇒ µ ≤ 4δN,
  M = 20N grid, πe/20, Corollary 7.1 (every length, 0<p<∞) and its proof, §8 merit factor ⇒ Turyn (abstract + p.3), 23 bibliography
  entries, Odlyzko not cited, "[12, Problem 22]" on p.2, ultra paper's "[8, Problem 26]"; Odlyzko quote (odlyzko/ultraflat.txt:173–174),
  n ≤ 52, skew-symmetric to 104.
- Replay: steps.tsv (build 0 952; gated_driver_retired 09:22:18Z; build_first_attempt_root_rule rc 1), 952 s = 09:23:48→09:39:40Z,
  28/28 rc=0 with empty logs (modules.tsv), Lean 4.34.1 / OAI adc7f124 / Mathlib d13f23b7 (manual/build.log:1–3), LEAN_NUM_THREADS=2 +
  nice 19, -DautoImplicit=false, oleans into our own dir; axioms.log l.1–2 verbatim; challenge.log l.37 and negcontrol.log l.2 verbatim;
  the three pp.all blocks are byte-identical (diff of axioms.log:3–37 vs challenge.log:2–36, not just the whitespace-normalised script
  compare); ChallengeStatement.lean's first 23 lines are byte-identical to the comparator; leanchecker started 09:40:20Z and its log is
  still empty.
- Lean facts: Main.lean:187 is `theorem main : MainStatement := by`; Model.lean defs identical to comparator up to two docstrings; json
  permitted axioms / enable_nanoda false; 24-module cone = 9,315 lines; 27 Littlewood files byte-identical to main HEAD (lean seat).
- Bridge arithmetic: (1+c/2)²(n+1) ≤ (1+c)²n ⇔ n ≥ (1+c/2)²/(c+3c²/4), finite for every c>0; degree exactly N−1 since ε_{N−1} = ±1;
  ‖z‖=1 includes z = ±1. Correct.
- Seat summaries for reduce, construct, round, ultra, lean, world match their reports except as itemised above.

## Verdict
4 SUBSTANTIVE + 18 MINOR
