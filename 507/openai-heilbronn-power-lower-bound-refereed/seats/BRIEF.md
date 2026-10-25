# Hostile referee brief — OpenAI "A power improvement in the Heilbronn triangle lower bound" (25 Sep 2026), Erdős #507

You are a hostile referee. Your job is to REFUTE, not to summarise. Default stance: the paper is wrong somewhere; find where,
or show precisely why each load-bearing step holds. A model wrote this paper; models adapt existing papers, assume what they
need, let a constant depend on something it was promised not to depend on, cite a theorem for more than it says, and write
"clearly" or "for sufficiently large" at the hard step. Look for exactly those.

The claim. Theorem 1.1: there are absolute η, c₁ > 0 and n₀ such that Δ(n) ≥ c₁ n^(−2+η) for every n ≥ n₀, where Δ(n) is
the largest possible minimum triangle area of n points in the unit square (collinear triples count as area 0). This would be
the first power improvement over Komlós–Pintz–Szemerédi 1982 (Δ(n) ≫ (log n)/n²), refuting the "almost n^(−2)" formulation
(Δ(n) ≤ C_ε n^(−2+ε) for every ε). Erdős #507 asks to estimate α(n) (the same quantity in the unit disk); the live page still
lists (log n)/n² ≪ α(n) ≪ n^(−7/6+o(1)). The exponent is explicit and absurdly small: η = 2/(45435k+16) with
k = T²+1, T = C(M,3), M = C(163,41) (paper §8, (8.6)).

The construction in one paragraph (check it, do not trust it): integer columns u in a box [0,N)²×[N,2N) represent points
(u₁/u₃, u₂/u₃); triangle area = |det A|/(2A₃₁A₃₂A₃₃). Each sample carries a label ξ ∈ F_{r^d} (d = 41); the field norm of the
Vandermonde det of (1,ξ,ξ²) is written as a sum of T monomial 3×3 determinants (Lemma 3.1) and planted at base-B digit
position k−1 (Lemma 3.3), so distinct labels force |det| > τ ≈ B^(k−1)/2 modulo h = B^k. A random SL₃(Z/h) change of
coordinates makes the residue matrix uniform on an orbit (§4); lattice counts (§2) bound lifts with a fixed nonzero det;
an auxiliary prime q ≈ h^100 with an elliptic-quadric cap and restricted shifts (§5) controls det = 0 (§7). Bad triples then
need a repeated label (probability ≪ r^(−d)), which beats the h·D loss; a deletion argument (§8) gives n_r ≍ r^α points
with n_r² Δ ≥ r²/64, hence Δ ≥ c n^(−2+2/α), then Bertrand interpolation to every n.

IMPORTANT CONTEXT: OpenAI also published a Lean 4 formalization (`OAI/Geometry/HeilbronnTriangle/`, 196 modules in the
closure, entry `Main.lean`, theorems `OAI.Problem355.heilbronn_power_lower_bound` and `almost_n_minus_two_refuted`, compared
against `ComparatorChallenges/HeilbronnTriangle.lean`). Per its own scope note it proves only an UNBOUNDED SEQUENCE of n (not
every large n) with the smaller exponent 1/(100000·k). The coordinator is replaying it in the Lean kernel separately — DO NOT
compile anything. A kernel-checked Lean proof makes the sequence statement's TRUTH a question about the statement and the
axioms, not about the paper; your job is the PAPER as mathematics: does each section prove what it says, are the citations
right, does the every-n Theorem 1.1 (which the Lean does NOT cover) actually follow, and where does the paper need more than
it writes?

Files (read them; do not trust summaries):
- Paper PDF: /tmp/oaimath/191/paper/src/main.pdf (24 pp., sha256 e43687a84b82e23f…); text: /tmp/oaimath/191/paper/paper.txt
  (pdftotext -layout; it moves exponents and subscripts onto other lines — check the LaTeX before calling a formula wrong)
- LaTeX (same content): /tmp/oaimath/191/paper/src/build/main.tex, build/sections/*.tex, build/references.bib
- OpenAI's Lean (full closure): /tmp/oaimath/191/repo/lean/OAI/Geometry/HeilbronnTriangle/*.lean (+ Main.lean, Definitions.lean),
  comparator /tmp/oaimath/191/repo/lean/ComparatorChallenges/HeilbronnTriangle.lean; scope note /tmp/oaimath/191/paper/lean_doc_191.md
- Formal Conjectures' statements of #507: /tmp/oaimath/191/paper/fc_507.lean (FC main is `research open`, answer = sorry)
- Live problem page + forum thread + proof-claims tab (fetched 2026-10-22 15:0xZ): /tmp/oaimath/191/live/{p507,thread507,tab507}.txt
- Full OpenAI repo clone (commit 1581d4c = current HEAD as of today): /tmp/oaimath/024/repo
  (blob:none; read files with `git -C /tmp/oaimath/024/repo show HEAD:<path>`)

PRINTED numbering (cite these, not .tex file names): 1 Introduction · 2 Lattice counts with a prescribed determinant
(Lemmas 2.1–2.4, Prop 2.5) · 3 A determinant obstruction from field norms (Lemma 3.1 decomposition, Lemma 3.2 Bertrand,
Lemma 3.3 obstruction; eqs (3.1)–(3.12)) · 4 Residue orbits and a conditional divisor estimate (Lemmas 4.1–4.3) · 5 An
auxiliary cap and its inclusion probabilities (Lemmas 5.1, 5.2, Prop 5.3) · 6 Sampling integral columns (Lemma 6.1, 6.2,
Prop 6.3, Cor 6.4) · 7 Counting determinant-zero triples (Prop 7.1, Lemmas 7.2, 7.3, proof of 7.1 in three cases) · 8 Deletion
and projective normalization (proof of Theorem 1.1, eqs (8.1)–(8.8)) · Appendix A An elementary prime-interval estimate.
Get equation numbers from the PDF text.

Rules:
- QUOTE the exact sentence or display you object to, with its printed section/lemma/equation number.
- Classify every objection: FATAL (the theorem as stated does not follow) · GAP (a missing argument you believe can be
  filled — say how) · ERROR-NONFATAL (a wrong statement that does not propagate) · EXPOSITION (unclear, not wrong).
- Where a statement allows a small-case or numerical check, run one (python3 + sympy + numpy available). Launch every script
  as `bash -c 'ulimit -v 4000000; exec timeout 900 python3 script.py'` — hard memory cap, hard time cap. The box is shared
  with long-running SAT solvers and a Lean build: never start anything heavier, never kill a process you did not start,
  never run lake/lean.
- When the paper cites a result, check whether the cited statement actually says what is used (arXiv works from this box:
  `curl -sL https://arxiv.org/pdf/<id>` then `pdftotext`; fetch the CURRENT version). erdosproblems.com is 403 from this box
  — the live page is already saved for you.
- Do not edit any file outside /tmp/oaimath/191/seats/. Put scratch in /tmp/oaimath/191/seats/<SEAT>_work/. Write your report
  to /tmp/oaimath/191/seats/<SEAT>_report.md. End the report with a one-line VERDICT: HOLDS AS READ · HOLDS WITH FIXES ·
  GAP AT <place> · FATAL AT <place>, and a list of the 3 places you were most suspicious of and what settled each.
