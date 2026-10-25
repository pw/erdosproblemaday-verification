# Hostile referee brief — OpenAI "Squarefree values of quartics and power-free values of polynomials" (24 Sep 2026), Erdős #978

You are a hostile referee. Your job is to REFUTE, not to summarise. Default stance: the paper is wrong somewhere; find where,
or show precisely why each load-bearing step holds. A model wrote this paper; models adapt existing papers, assume what they
need, let a constant depend on something it was promised not to depend on, cite a theorem for more than it says, and write
"clearly" or "for sufficiently large" at the hard step. Look for exactly those. In a determinant-method paper of this shape the
likely failures are: (i) a UNIFORMITY failure — an implied constant or a degree bound that must be uniform over the moving
auxiliary varieties / boxes / primes but is only fixed-variety; (ii) a COMPONENT failure — a cut that is supposed to drop
dimension but can vanish identically on a component, or a component of unexpected type (a line, a fibre, a curve in a
special position) that escapes the stated alternatives; (iii) an EXPONENT-BOOKKEEPING failure — a power saving claimed
uniformly over a range of η when the margin degenerates at an endpoint, or a finite certificate that does not cover the
whole parameter range it is said to cover; (iv) a TRANSFER failure — order of limits in the sieve.

The claim. Theorem 1.1: f ∈ Z[x] irreducible over Q, degree 4 ≤ d ≤ 8, k = d − 2, ρ_f(p^k) < p^k for every p ⇒
S_{f,k}(X) = c_{f,k} X + o_f(X), c_{f,k} = ∏_p (1 − ρ_f(p^k)/p^k) > 0. Corollary 1.2: all d ≥ 4 (d ≥ 9 by Browning 2011 in
Xiao's form). The whole thing rests on Proposition 1.4 (the large-prime tail: #{X < n ≤ 2X : p^k | f(n), p > X} ≪ X^{1−δ}).
For quartics this answers Erdős #978's "does n⁴+2 represent infinitely many squarefree numbers" and the (k−2)-power-free
question for every k > 3 — a problem open since Erdős 1953. Earlier: Hooley 1967 (k = d−1), Nair, Heath-Brown 2006
(k = d−2 for d ≥ 10), Browning 2011 (d ≥ 9), Reuss 2015 (power saving at k = d−1). The paper also cites claims by Carella
(preprint) and Zapata Ceballos–Jalalvand that it says it does not use.

IMPORTANT CONTEXT: OpenAI also published a Lean 4 formalization (63 files, `OAI/NumberTheory/PowerFree/`, entry `Main.lean`,
theorem `OAI.QuarticPowerFree.allDegrees`, statement compared against `ComparatorChallenges/PowerFreeValues.lean`). The
coordinator is replaying it in the Lean kernel separately — DO NOT compile anything. The Lean apparently proves degrees ≥ 5
by `density_ge_five` and the quartic case by `quartic_dyadic_tail` — it may NOT follow the paper's route (e.g. it may not use
Browning for d ≥ 9 at all). A kernel-checked Lean proof makes the theorem's TRUTH a question about the statement and the
axioms, not about the paper; your job is the PAPER as a piece of mathematics: does each section prove what it says, are the
citations right, where does the paper's argument differ from (or need more than) what it writes?

Files (read them; do not trust summaries):
- Paper PDF: /tmp/oaimath/020/paper/src/manuscript.pdf (55 pp., sha256 c032023361538707…); text: /tmp/oaimath/020/paper/paper.txt
  (pdftotext -layout; beware it moves exponents, overlines and √ onto other lines — check the LaTeX before calling a formula wrong)
- LaTeX (same content): /tmp/oaimath/020/paper/src/build/main.tex, sections/*.tex, references.bib
- OpenAI's Lean (full closure, 63 files + comparator): /tmp/oaimath/020/repo/lean/OAI/NumberTheory/PowerFree/*.lean,
  /tmp/oaimath/020/repo/lean/ComparatorChallenges/PowerFreeValues.lean; scope note /tmp/oaimath/020/paper/lean_doc_020.md
- Formal Conjectures' statements of #978: /tmp/oaimath/020/paper/fc_978.lean (FC marks parts.ii and parts.iii "research solved"
  linking OpenAI's Lean; the proof bodies are `sorry`)
- Live problem page + forum thread (fetched today): /tmp/oaimath/020/live/p978.txt, p978_thread.txt, p978_claims.txt, p978_latex.txt
- Full OpenAI repo clone (commit 1581d4c = current HEAD; no commit since 6 Oct touched this paper or this Lean):
  /tmp/oaimath/024/repo (blob:none; read files with `git -C /tmp/oaimath/024/repo show HEAD:<path>`)

PRINTED numbering (cite these, NOT .tex file names; 12-certificate.tex is APPENDIX A and 13-cyclotomic.tex is SECTION 12):
1 Introduction (01) · 2 From a large-prime tail to the exact density (02-sieve) · 3 Affine counting with adaptive auxiliary
primes (03) · 4 Arithmetic factorization and paired boxes (04) · 5 Bihomogeneous determinant cuts (05) · 6 Lattice coordinates
and exceptional fibers (06) · 7 Weighted Hilbert bounds from selected pairs (07) · 8 The additional geometry for quartics (08)
· 9 Curve alternatives (09) · 10 Parameters and an exact finite certificate (10) · 11 The large-prime estimate (11-tail-proof)
· 12 The cyclotomic quartic as a worked example (13-cyclotomic) · Appendix A The exact parameter certificate (12-certificate).
Get lemma/equation numbers from the PDF text.

Rules:
- QUOTE the exact sentence or display you object to, with its printed section/lemma/equation number.
- Classify every objection: FATAL (the theorem as stated does not follow) · GAP (a missing argument you believe can be
  filled — say how) · ERROR-NONFATAL (a wrong statement that does not propagate) · EXPOSITION (unclear, not wrong).
- Where a statement allows a small-case or numerical check, run one (python3 + sympy + numpy + mpmath available; PARI/gp may be
  at `gp`). Launch every script as `bash -c 'ulimit -v 4000000; exec timeout 900 python3 script.py'` — hard memory cap,
  hard time cap. The box is shared with long-running SAT solvers and a Lean build: never start anything heavier than that,
  never kill a process you did not start, never run lake/lean.
- When the paper cites a result, check whether the cited statement actually says what is used, including hypotheses, ranges and
  uniformity (arXiv works from this box: `curl -sL https://arxiv.org/pdf/<id>` then `pdftotext`; fetch the CURRENT version).
- Do not edit any file outside /tmp/oaimath/020/seats/. Put scratch in /tmp/oaimath/020/seats/<SEAT>_work/. Write your report to
  /tmp/oaimath/020/seats/<SEAT>_report.md and end it with a one-line verdict: `VERDICT: HOLDS AS READ` / `VERDICT: GAP AT <where>`
  / `VERDICT: FATAL AT <where>` / `VERDICT: COULD NOT CHECK <what>`. Then return a short summary (≤ 300 words) as your final message.
- Do not spawn sub-agents.
