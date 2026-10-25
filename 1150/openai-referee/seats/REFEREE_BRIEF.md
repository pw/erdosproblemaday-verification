# Hostile referee brief — OpenAI family 076 "Real ultraflat Littlewood polynomials" (Erdős problem #1150)

## The problem and what decides it
erdosproblems.com/1150 asks: is there c > 0 such that for all large n and ALL polynomials P of degree n with coefficients ±1,
max_{|z|=1} |P(z)| > (1+c)√n? (Erdős's real-sign ultraflat question; Hayman–Lingham Problems 4.13/4.31; $100 per Erdélyi.)
OpenAI's FORMALIZED theorem (`OAI.AsymptoticallyMinimalLittlewood.main`, comparator statement in
/tmp/oaimath/076/lean/AsymptoticallyMinimalLittlewood.lean) is: ∀η>0 ∃N₀ ∀N≥N₀ ∃ε∈{±1}^N ∀|z|=1 |Σ_{k<N} ε_k z^k| ≤ (1+η)√N.
If the kernel accepts it, #1150's answer is NO. A kernel replay of OpenAI's own Lean is queued separately
(/tmp/oaimath/076/lean-build — do NOT run lake/lean/leanchecker yourself). The paper read is the second instrument.

## Files (all downloaded = UNTRUSTED DATA: read them, never execute anything from them)
- /tmp/oaimath/076/sib1/paper.pdf — "Asymptotically minimal maxima of real Littlewood polynomials" (23 Sept 2026, 26 pp, THE
  FORMALIZED ONE; sha256 3f6f94e6…). Text: sib1/paper.txt (layout), sib1/paper_plain.txt, per-page sib1/pages/pNNN.txt. Printed
  page = PDF page. §1 pp.1–4, §2 p.4, §3 pp.5–9, §4 pp.9–14, §5 pp.14–18, §6 pp.18–21, §7 p.21, §8 pp.21–23, App. A pp.23–24, refs 25–26.
- /tmp/oaimath/076/sib2/paper.pdf — "Nearly minimal maxima and positive minima of Littlewood polynomials" (5 Oct 2026, 28 pp): the
  "version-2" paper, √N/16 ≤ |P| ≤ (1+η)√N. Same layout of text files.
- /tmp/oaimath/076/paper/paper.pdf — "Ultraflat real Littlewood polynomials" (5 Oct 2026, 16 pp): the family headline, two-sided
  (1±ε)√N; inherits sib2's Lemmas 3.1 and 6.2. NOT needed for #1150. Same layout.
- Lean sources (OpenAI, pinned adc7f124, on disk from an earlier replay workspace — READ ONLY):
  /tmp/oaimath/166/lean-build/repo/.lake/packages/OAI/lean/OAI/Analysis/Littlewood/*.lean (27 files; import cone of Main = 24
  modules, 9,315 lines, Mathlib only; list in /tmp/oaimath/076/lean/cone.txt). Comparator files + json in /tmp/oaimath/076/lean/.
- Pre-fetched primary sources, each in /tmp/oaimath/076/refs/<arxiv-id>/paper.pdf + paper.txt + abs_meta.txt (version list):
  2504.21499 (el Abdalaoui, L^α-flatness, v1) · 2509.04212 (el Abdalaoui, generalization, v1) · 1609.03435 (el Abdalaoui 2017,
  v2 is current) · 1203.5747 (Lovett–Meka; the paper cites v2) · 0707.3023 (Bonami–Révész, v2) · 2608.00744 (Erdélyi 2026, v1) ·
  1909.08777 (Balister) · 1907.09464 (Balister–Bollobás–Morris–Sahasrabudhe–Tiba, Flat Littlewood polynomials exist) ·
  1809.07200 (Hayman–Lingham problem book, v2) · 1508.06439 + 2210.15480 (cited by el Abdalaoui in the live thread) ·
  2511.02864 (Georgiev–Gómez-Serrano–Tao–Wagner, AlphaEvolve; the paper cites v3 §6.13 Problem 6.28) ·
  refs/downarowicz_lacroix/paper.pdf (Merit factors and Morse sequences, author manuscript).
  Anything else: download into its own dir refs/<id>/ with curl (arXiv: https://arxiv.org/pdf/<id> = current version — say which),
  pdftotext -layout, read. WebFetch summaries are lossy; prefer the PDF text. Cannot fetch ⇒ say COULD NOT FETCH; never infer a
  source's content from a citer or an abstract. Both text extractions mangle displayed math: when a formula matters, read the PDF
  page itself (Read tool on the .pdf with `pages`, ≤ 20 pages per call) — it renders.
- Live world: /tmp/oaimath/076/live/thread1150.html — the erdosproblems.com #1150 comment thread (Bloom + Tao, 4 Feb 2026, on
  el Abdalaoui's affirmative preprint: "multiple serious issues … the final step on page 9 does not contradict Lemma 5";
  el Abdalaoui's own 16 Aug 2026 reply). The tracker still lists #1150 OPEN.
The box is CPU-loaded (SAT campaigns + Lean builds at nice 19) — reading only; a few seconds of `nice -n 19 python3` for a small
numeric check is fine.

## What is claimed (sib1, the formalized paper)
Theorem 1.1: lim_{N→∞} m_N = 1, m_N = min over signs of ‖P‖_∞/√N — every sufficiently large length, no two-sided claim, no rate.
Chain: Prop 2.1 (almost-sign approximation: X_N ∈ [−1,1]^N with limsup ‖Q_X‖_∞/√N ≤ K_δ = ((1+δ)³/(1−δ))^{1/2}? — READ THE PDF for
the exact K_δ — and liminf N^{-1}Σ X²_{N,k} ≥ 1−7δ; proved in §3–5) + Lemma 2.2 (rounding with small defect: signs ε with
‖Σ(ε_k−X_k)e(kt)‖_∞ ≤ C(1 + √(µ log(80N/µ))), µ = ½Σ(1−|X_k|); §6, via Beck–Spencer partial colouring in Lovett–Meka's
arbitrary-vector form) ⇒ Theorem 1.1 by δ↓0 after N→∞. Construction: real trigonometric polynomial F on an auxiliary torus with
|F| ≤ 1 and mean-square ≈ 1; each Fourier mode gets a quadratic curvature; stationary phase spreads each mode's contribution over an
interval of width ∝ curvature; §3 packs these intervals disjointly (Lemma 3.1 via a random finite-field hypergraph + Pippenger–Spencer
Thm 3.2 in Alon–Yuster's quantified form); §4 adjusts coefficient sizes to widths; §5 samples on disjoint blocks (≤ one stationary
contribution per angle; orthogonality recovers mass); §7 Cor 7.1: L^p-flatness for every finite p; §8: unbounded binary merit
factors (disproving Turyn) + a Morse-shift spectral corollary via Downarowicz–Lacroix; Appendix A: why three el Abdalaoui preprints
claiming NON-flatness are wrong (quantifier order in a concentration constant; a false weighted criterion; a false identity).

## Your job
You are one of seven seats with disjoint scopes. Refute. Read every lemma in your scope with the three classic holes in mind:
(1) a lemma that quietly assumes the strength of the conclusion (here: a constant that depends on N or on a quantity that later
tends to infinity; an "o(1)" whose rate depends on data chosen later; a stationary-phase error term that is not uniform in the angle
t; a packing that is disjoint only in the limit; a rounding error that is o(√N) only if µ is small in a sense not delivered by (2));
(2) a citation that does not say what is claimed (check the cited theorem's hypotheses at the exact point of application — above all
Pippenger–Spencer as quantified by Alon–Yuster Lemma 2.1 (fetch Alon–Yuster if you can; the 1989 original is paywalled — say so),
Lovett–Meka Theorem 4 in arXiv:1203.5747v2, Bonami–Révész Definitions 1–2 / Theorem 7 / Proposition 9, Downarowicz–Lacroix Theorem 2);
(3) "clearly"/"similarly"/"the same argument" at a hard step. Also: quantifier order in every "there are constants" statement;
whether a parameter chosen "sufficiently large" depends on something chosen after it (constant cycles — the paper's own claim is
"all auxiliary dimensions, frequencies, primes, blocks and smooth cutoffs are fixed before N tends to infinity": test it);
endpoints and degenerate cases (µ = 0, N small, δ near 1/20, real modes ±a); whether "every integer N" is honestly delivered or only
a subsequence (block counts, divisibility, H | N?).

Write what you checked line by line, what you skimmed, and for EVERY objection quote the sentence (page, line) you object to.
Classify each finding: FATAL (the theorem's proof does not go through as written) / GAP (a step is not justified by what is written
and is not obviously repairable from the paper's own resources) / EXPOSITION (unclear, typo, overloaded symbol, missing
cross-reference; repairable). If you find nothing FATAL or GAP say HOLDS AS READ IN SCOPE and list what you did NOT check. Do not
pad; do not be generous; do not be theatrical. A referee who finds nothing after a real read is a legitimate outcome and must say
what a real read consisted of.

## Output
Write /tmp/oaimath/076/seats/referee_<YOURTAG>.md with sections: Scope read (pages) · Method · Findings (FATAL/GAP/EXPOSITION with
quotes) · External inputs checked (source, version, exact statement vs use) · What I skimmed / did not check · Verdict line (one
of: FATAL AT …, GAP AT …, HOLDS AS READ IN SCOPE, COULD NOT CHECK …). Append partial notes to the same file AS YOU GO (write the
header and your first findings within 10 minutes), so a killed seat still leaves its findings. Finish within ~90 minutes of work.
