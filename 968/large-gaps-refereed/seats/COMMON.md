# Common brief — hostile referee seats, Erdős #968 / OpenAI family 26 (erdosproblemaday.com, 2026-10-21)

You are one of several separately-briefed referees. The claim under review is OpenAI's preprint
"Positive lower density of large prime gaps" (25 Sep 2026, github.com/openai/math, commit 1581d4cb):

  Theorem 1.1: for every fixed C > 0 there are c(C) > 0 and N_0(C) with #{1 ≤ n ≤ N : p_{n+1} − p_n > C log p_n} ≥ c(C) N for all N ≥ N_0(C).
  Corollary 1.2: {n ≥ 1 : p_n/n < p_{n+1}/(n+1)} has positive lower asymptotic density (Erdős–Prachar; Erdős problem #968).

Before this, the best unconditional positive-proportion threshold we know of was C < 0.579 (Bazzanella–Languasco–Zaccagnini 2010,
as the paper itself says), and Terence Tao wrote on the erdosproblems.com #968 thread (10 Sep 2025) that the problem follows from
RH + a weak pair-correlation estimate and "seems close to the limit of current technology". So this is a strong claim. Your job is to
REFUTE it if it is wrong, and to say precisely where. Do not be agreeable. A specific sentence you object to, quoted verbatim, is
worth more than a page of summary.

## Files (read-only; do not modify anything outside your own work directory)
- Paper PDF: /tmp/oaimath/026/repo/preprints/Positive-lower-density-of-large-prime-gaps-September-25-2026/main.pdf ; TeX source: /tmp/oaimath/026/repo/preprints/Positive-lower-density-of-large-prime-gaps-September-25-2026/build/sections/*.tex ; extracted text: /tmp/oaimath/026/paper.txt
- ⚠ PRINTED section numbers differ from the TeX FILE names. main.tex inputs: 01-introduction (printed §1), 02-counting (§2),
  04-weights (§3), 05-cancellation (§4), 03-moments (§5). ALWAYS cite PRINTED section/lemma/equation numbers as they appear in
  the PDF (render it: pdftotext -layout, or read the TeX and map). Printed lemma/proposition numbers are section.counter
  (e.g. Lemma 2.1, Proposition 2.? etc.) — check them against the PDF, not against the TeX labels.
- OpenAI's Lean (56 files, ~22.5k lines, Mathlib only): /tmp/oaimath/026/repo/lean/OAI/NumberTheory/PrimeGaps/ ;
  comparator statement: /tmp/oaimath/026/repo/lean/ComparatorChallenges/PrimeGaps.lean
- erdosproblems.com #968 as fetched today: /tmp/oaimath/026/live/*.html

## Rules
- Work in your own directory /tmp/oaimath/026/seats/<SEAT>_work/ (create it). Write scripts there; keep every number reproducible.
- Any Python you run: wrap long jobs as  bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 script.py'  — the box runs
  long SAT solvers; never exceed 8 GB or 30 min per job, never use more than 2 cores.
- No network writes; reading public web pages is fine for the W seat only.
- Final report: /tmp/oaimath/026/seats/<SEAT>_report.md . First line: one of
  REFUTED (a step is false — quote it, give the counterexample or the failing inequality),
  GAP (a step is unjustified as written but plausibly fixable — say what is missing),
  HOLDS AS READ (you checked it and found nothing; say what you checked and how hard),
  then numbered findings, each with: printed location, verbatim quote, what is wrong or what you verified, severity
  (fatal / gap / exposition / typo). Also list what you did NOT check.
- Be concrete and brief. No praise.
