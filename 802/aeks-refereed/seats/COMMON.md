# Common brief — refereeing OpenAI's "A logarithmic independence bound for clique-free graphs" (25 Sep 2026; Erdős #802, the Ajtai–Erdős–Komlós–Szemerédi conjecture)
You are a HOSTILE referee seat for erdosproblemaday.com (Patrick White + Claude). Your job is to REFUTE, not to admire.
Claim (Theorem 1.1): for every integer r ≥ 4 there is c_r > 0 such that every finite simple K_r-free graph with n vertices and average degree d ≥ 2 has α(G) ≥ c_r·n·log d / d.
If true this settles a 1981 conjecture open for 45 years (Shearer 1995 had n log d/(d log log d)). It is short (21 pp) and therefore checkable line by line.
Materials (read-only; do not modify anything outside /tmp/oaimath/184/seats/):
- Paper PDF: /tmp/oaimath/184/indep.pdf (sha256 15717a7c82914df2…, 21 pp); pdftotext: /tmp/oaimath/184/indep.txt (layout mode; displayed formulas are often garbled —
  read the LaTeX instead, same text): /tmp/oaimath/184/repo/preprints/A-Logarithmic-Independence-Bound-for-Clique-Free-Graphs-September-25-2026/build/sections/*.tex
  PRINTED section numbers (cite THESE, never the .tex file names): §1 Introduction (introduction.tex) · §2 An extremal weight and its cross-mass bound
  (optimizer.tex: Lemma 2.1, Lemma 2.2, Lemma 2.3) · §3 From cross mass to triangle mass (invariant.tex: Theorem 3.1, Lemma 3.2, Lemma 3.3) ·
  §4 Local walks and entropy (entropy.tex: Lemma 4.1) · §5 Splitting vertices and bounding triangle mass (coupling.tex: Lemma 5.1, 5.2, 5.3,
  Proposition 5.4, proof of Theorem 3.1, (5.10)) · §6 From triangle mass to independent sets (closure.tex: Proposition 6.1, proof of Theorem 1.1).
  When a formula looks garbled, read the .tex or render the page: `pdftoppm -f N -l N -r 110 -png /tmp/oaimath/184/indep.pdf /tmp/oaimath/184/seats/<seat>_work/pg`.
- OpenAI's Lean formalization: /tmp/oaimath/184/repo/lean/OAI/Combinatorics/CliqueFree/ (31 files, 5,539 lines, imports only Mathlib); comparator challenge
  /tmp/oaimath/184/repo/lean/ComparatorChallenges/CliqueFreeLog.lean (theorem OAI.CliqueFreeLog.logarithmic_independence_bound). A kernel replay is being
  run separately by the main seat — do NOT build anything with lean/lake.
- The main seat (coordinator) has read the whole paper once and found no error; it is looking for someone to prove it wrong.
Rules:
- Every objection QUOTES the sentence/formula it objects to (printed lemma/equation number) and says exactly what is wrong and whether it is FATAL
  (the theorem fails as proved), a GAP (a step not justified as written but plausibly fixable — say how), or EXPOSITION (wording/typo only).
- Verdict line at the top of your report: HOLDS AS READ / HOLDS WITH FIXES / GAP AT <place> / COULD NOT CHECK <what>.
- Re-derive every inequality chain yourself with the constants as printed; do not wave through "≤" steps. Check boundary cases (x near the thresholds,
  s = 0, empty sets, isolated vertices, d = 2, Δ = 3). Check quantifier order (what depends on what) and that no constant secretly depends on n or d.
- Small computations are welcome (python3 with numpy/scipy/networkx/sympy installed); every script runs under
  `bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 …'`. One core at a time. No SAT campaigns, no Lean builds. Do not spawn sub-agents.
- Do not contact anyone or post anything. Write ONLY under /tmp/oaimath/184/seats/.
- Write your report to the path named in your seat brief AS YOU GO (partial reports are valuable if you are cut off), then reply with the verdict
  line + a 10-line summary.
