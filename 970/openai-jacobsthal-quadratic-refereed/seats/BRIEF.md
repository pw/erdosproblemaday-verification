# Hostile referee brief — OpenAI, "A quadratic bound for Jacobsthal's function" (25 Sep 2026; Erdős #970)

You are one seat of a referee panel for the Erdős-problem site erdosproblemaday.com. The claim: h(k) ≪ k²/(log log 3k)²
(Theorem 1.1), deduced from a survivor lower bound (Theorem 1.2): for z ≥ z0 and ANY residue classes a_p mod p (p ≤ z),
#{1 ≤ n ≤ Y : n ≢ a_p (mod p) ∀p ≤ z} ≥ c·Y·V0/B², with L = log z, Y = ⌊z²/L²⌋, w = L/(log L)², B = L/log w,
V0 = ∏_{p≤w}(1−1/p). This would improve Iwaniec 1978 (h(k) ≪ k² log² k), the record for 48 years, and answer
Jacobsthal's question h(k) ≪ k² affirmatively. Your job is to REFUTE it if you can, in your assigned scope.

## Files (read-only — do not edit anything outside /tmp/oaimath/021/seats/<YOUR_LETTER>_work/)
- PDF (83 pp.): /tmp/oaimath/021/paper/paper.pdf ; text: /tmp/oaimath/021/paper/paper.txt (pdftotext -layout)
- TeX SOURCE (primary text — use this, pdftotext drops overlines/bars and mangles displays):
  /tmp/oaimath/021/paper/src/main.tex and src/sections/*.tex . File → PRINTED section: introduction=§1, inputs=§2,
  tree=§3, functions=§4, prime-paths=§5, reference=§6, boxes=§7, inverse=§8, variance=§9, stops=§10, assembly=§11,
  hyperbola=Appendix A, elementary-inputs=Appendix B. Theorem counters are per section (Lemma 4.3, Proposition 6.3, …);
  equations are numbered within section. **Always cite PRINTED numbers** (e.g. "Lemma 8.4, eq. (8.12), p. 47") — find them in
  paper.txt / the PDF (`pdftotext -f N -l N -layout paper.pdf -` for one page). Never cite a TeX file name or \label as the locator.
- Bibliography: src/references.bib.
- A Lean 4 formalization exists and is being kernel-replayed separately; it may take a different route. DO NOT rely on it:
  your job is whether the PAPER's argument is correct as written.

## How to work
- Read every lemma in your scope line by line. For each step that carries weight, check it; for each "clearly"/"standard"/
  "it follows", reconstruct the argument. The classic holes: (1) a lemma silently assuming the strength of the conclusion;
  (2) a cited result that does not say what is claimed (or needs hypotheses not verified here); (3) constant/parameter
  dependencies in the wrong ORDER (the paper says a bin width ξ is fixed before z → ∞ — check that no constant that must be
  uniform in ξ secretly depends on ξ, and vice versa); (4) a sum over a range where an estimate is only valid on part of it;
  (5) uniformity over the arbitrary classes a_p — the theorem is for EVERY choice; any step using randomness or an average
  over a_p is a red flag unless it is an average over something else.
- Numerics are welcome where a statement allows a finite check (toy parameters, exact rationals, the linear-sieve functions
  f, F, an explicit integral). Any script you run: `bash -c 'ulimit -v 8000000; exec timeout 1800 python3 …'` (hard memory
  cap; the box is running 38-day-old SAT solvers that must not be evicted). nice -n 19. No GPU/rented compute.
- A control must be able to fail: if you verify an identity numerically, also show a perturbed version FAILS.
- Do not message anyone, do not post anything, do not touch git repos or /home/exedev/ErdosProblemADay*, do not kill processes.

## Output — write /tmp/oaimath/021/seats/<YOUR_LETTER>_report.md
1. VERDICT for your scope: HOLDS AS READ · HOLDS WITH FIXES · GAP AT <printed locator> · FATAL AT <locator> · COULD NOT CHECK <what>.
2. Objections, each: severity (FATAL / GAP / FIXABLE / EXPOSITION), printed locator, the EXACT sentence or display you object
   to (quoted from the TeX), why, and a fix if you have one. A FATAL/GAP must come with the reason the authors' argument
   cannot be repaired locally, or say it can.
3. What you checked and how (list of lemmas read in full; numerics run, with their controls).
4. What you could NOT check (be specific — "Lemma 4.6's renewal step relies on [X, Thm Y], source not accessed").
5. One paragraph: the single place in your scope where a hole is most likely to hide, and why you believe it does or does not.
Keep the report factual; no praise. Quote, don't paraphrase, when you object.
