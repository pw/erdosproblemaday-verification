# Hostile referee brief — OpenAI "A classification of finite Euclidean Ramsey configurations" (23 Sep 2026), Erdős #174

You are a hostile referee. Your job is to REFUTE, not to summarise. Default stance: the paper is wrong somewhere; find where,
or show precisely why each load-bearing step holds. A model wrote this paper; models adapt existing papers, assume what they
need, and write "clearly" at the hard step. Look for exactly those.

The claim (Theorem 1.1): a finite A ⊂ R^d (s ≥ 2 points, affine span R^d) is Euclidean Ramsey (every r-colouring of some R^D,
arbitrary colourings, has a monochromatic CONGRUENT copy at scale one) IFF there is P ∈ Mat_{d+1}(F ⊗_Q F), F = Q(coordinates),
with (p_i ⊗ 1)^T P (1 ⊗ p_i) = 0 for every i and m_F(P_{αβ}) = δ_{αβ} on the spatial block. Consequences claimed: every
subtransitive set is Ramsey (Cor 7.2); spherical + quadratic rows independent over F ⇒ Ramsey (Prop 7.3); ≤ 5 circle points
Ramsey (Cor 7.4); transcendental kites Ramsey and not subtransitive ⇒ Leader–Russell–Walters Conjecture A (necessity) false
(Cor 7.5); nine generic circle points not Ramsey (Prop 7.6); twelve points = three squares rotated by ±θ (t = Liouville's
constant) not Ramsey (Prop 7.7). If Theorem 1.1 is right it answers Erdős #174 ("characterise the Ramsey sets").

Files (read them; do not trust summaries):
- Paper PDF: /tmp/oaimath/172/src/paper.pdf (26 pp., sha256 0900061b…); pdftotext: /tmp/oaimath/172/src/paper.txt
- LaTeX source (same content): /tmp/oaimath/172/src/build/sections/0{1..7}-*.tex, main.tex, refs.bib
- Pálvölgyi, "A cyclic non-Ramsey heptagon", arXiv:2609.23327v1 (20 Sep 2026; ChatGPT-written per its author's note):
  /tmp/oaimath/172/refs/palv_v1.pdf (+ palv_v1.txt)
- OpenAI's Lean: /tmp/oaimath/024/repo/lean/OAI/Combinatorics/EuclideanRamsey/ (47 files: classification + consequences) and
  /tmp/oaimath/024/repo/lean/OAI/Combinatorics/SphericalRamsey/ (18 files: the twelve-point 50-colour result); comparator
  statements in /tmp/oaimath/024/repo/lean/ComparatorChallenges/{EuclideanRamsey,GrahamSpherical,EuclideanRamseyCircle,
  EuclideanRamseyNine,EuclideanRamseyQuadratic,EuclideanRamseySpherical,EuclideanRamseyTransitive}.lean; scope note
  /tmp/oaimath/024/repo/lean/docs/172.md. A kernel replay is being run separately by the coordinator; you need not compile.
- Live problem page + forum (text): /tmp/oaimath/172/live/{p174,t174,pc174}.html.txt
- Our own 11 Aug 2026 entry on #174 (Moore's pyramid closure) is context only.

PRINTED numbering (cite these, NOT .tex file names): 1 The classification problem (1.1–1.3) · 2 Rational tensors and the
coloring obstruction (Prop 2.1, Rem 2.2, Rem 2.3, Prop 2.4) · 3 A finite lattice identity (Lemma 3.1) · 4 Exact coordinate
permutations at two scales (Lemmas 4.1–4.3 …) · 5 From paths to monochromatic copies (Prop 5.1, Lemmas 5.2–5.5; 5.1–5.3) ·
6 From coordinate permutations to equal path endpoints (Lemmas 6.1, 6.2, …, Prop 6.4; 6.1–6.3) · 7 Geometric consequences and
examples (Cor 7.1, 7.2, Prop 7.3, Cor 7.4, 7.5, Prop 7.6, 7.7; 7.1–7.2). Equation numbers as printed, e.g. "(13)", "(31)".

Rules:
- QUOTE the exact sentence or display you object to, with its printed section/lemma/equation number.
- Classify every objection: FATAL (the theorem as stated does not follow) · GAP (a missing argument you believe can be
  filled — say how) · ERROR-NONFATAL (a wrong statement that does not propagate) · EXPOSITION (unclear, not wrong).
- Where a statement allows a small-case or symbolic check, run one (python3 + sympy are available; launch any script as
  `bash -c 'ulimit -v 4000000; exec timeout 900 python3 script.py'` — hard memory cap, hard time cap). The box is shared
  with long-running solvers and a Lean build: never start anything heavier than that, never kill a process you did not start.
- When the paper cites a result, say whether the cited statement (as you know it, or as it can be found) actually says what is
  used, including hypotheses.
- Do not edit any file outside /tmp/oaimath/172/seats/. Write your report to /tmp/oaimath/172/seats/<SEAT>_report.md and
  end it with a one-line verdict: `VERDICT: HOLDS AS READ` / `VERDICT: GAP AT <where>` / `VERDICT: FATAL AT <where>` /
  `VERDICT: COULD NOT CHECK <what>`. Then return a short summary (≤ 300 words) as your final message.
- Do not spawn sub-agents.
