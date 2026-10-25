# Hostile referee brief — OpenAI "The joint Dickman law for consecutive integers" (24 Sep 2026), Erdős #371 (+ #928)

You are a hostile referee. Your job is to REFUTE, not to summarise. Default stance: the paper is wrong somewhere; find where,
or show precisely why each load-bearing step holds. A model wrote this paper; models adapt existing papers, assume what they
need, let a constant depend on something it was promised not to depend on, cite a theorem for more than it says, and write
"clearly" or "for sufficiently large" at the hard step. Look for exactly those. The most likely failure in a paper of this
shape is an ORDER-OF-LIMITS error: the paper says "the original scale x tends to infinity before the auxiliary scale B; bin
data, feature degrees, residue moduli and divisor multipliers are fixed in that inner limit" and that "the contradiction
applies to a subsequence of every possible bad sequence of original scales". Check every place where something chosen
after x (or depending on the subsequence, on W, on the optimizing cut, on φ) is later treated as fixed, and every place a
uniformity in B is silently needed.

The claim. Theorem 1.1: for every fixed a, b ∈ (0,1), (1/X)·#{2 ≤ n ≤ X : P+(n) ≤ n^a, P+(n+1) ≤ n^b} → ρ(1/a)ρ(1/b)
(ordinary natural density, all real X). Corollary 1.2: P+(n) < P+(n+1) has natural density 1/2 (Erdős–Pomerance 1978;
Erdős #371). Prior art per the paper: Teräväinen 2018 (logarithmic density), Tao–Teräväinen 2019 and 2026 (ordinary
averages outside an exceptional set of scales), Wang 2021 (conditional on Elliott–Halberstam for friable integers).
The new content is "the unconditional ordinary limit at every sufficiently large scale". External inputs named in §1.2:
Matomäki–Radziwiłł 2016 Theorem 1 (real short intervals), Matomäki–Radziwiłł–Tao 2015 Theorem A.1 "corrected version"
(complex, non-principal twists), Selberg–Delange / Granville–Koukoulopoulos / Koukoulopoulos / Ford sieve & zeta bounds,
Montgomery–Vaughan 1977 (minor arcs), McDiarmid 1989, Frieze–Kannan / Alon et al. / Borgs et al. (cut-norm sampling).

Files (read them; do not trust summaries):
- Paper PDF: /tmp/oaimath/012/paper/paper.pdf (84 pp., sha256 e66b4e8a1fe197d3…); pdftotext -layout: /tmp/oaimath/012/paper/paper.txt
- LaTeX source (same content): /tmp/oaimath/012/paper/build/main.tex and build/sections/{introduction,labels,arithmetic,
  amplification,graph,moments,channels,kernel,sampling,conclusion,distribution}.tex, bibliography build/references.bib
- OpenAI's Lean (closure copy, 1,793 OAI files + patched PrimeNumberTheoremAnd/StrongPNT): /tmp/oaimath/012/src/oai/OAI/
  NumberTheory/JointDickman/ (entry PaperMain.lean → UnconditionalMain.lean → DischargedMain.lean; statements in
  MainStatements.lean; "published inputs" as Prop hypotheses in Amplification/PublishedInputs.lean and
  TwoPointCorrelations/PublishedInputs.lean); comparator /tmp/oaimath/012/src/oai/ComparatorChallenges/JointDickman.lean;
  scope note /tmp/oaimath/024/repo/lean/docs/012.md. A kernel replay is being run separately by the coordinator; do not compile.
- Live problem pages (text): /tmp/oaimath/012/live/p371.txt, p371_claims.txt, p371_thread.txt, p928 page in p928.html, p372.html
- Formal Conjectures' statement of #371: /tmp/oaimath/012/paper/fc_371.lean (FC marks it "research solved", linking OpenAI's Lean)

PRINTED numbering (cite these, NOT .tex file names; the TeX files are NOT in printed order by name): 1 Introduction (Thm 1.1,
Cor 1.2; §1.1 previous work, §1.2 method) · 2 Large-prime labels and their short averages (labels.tex) · 3 Arithmetic
preliminaries at an auxiliary log scale (arithmetic.tex) · 4 Amplifying a mixed correlation (amplification.tex) · 5 From
mixed amplification to an independent-site kernel (graph.tex) · 6 A second moment for the latent rows (moments.tex) ·
7 Smoothing channels on logarithmic and residue space (channels.tex) · 8 Integral approximation by endpoint features
(kernel.tex) · 9 Sampling the integral cut comparison (sampling.tex) · 10 Vanishing of the main energy (conclusion.tex) ·
11 Marginals, the joint law, and the ordering corollary (distribution.tex). Get lemma/equation numbers from the PDF text.

Rules:
- QUOTE the exact sentence or display you object to, with its printed section/lemma/equation number.
- Classify every objection: FATAL (the theorem as stated does not follow) · GAP (a missing argument you believe can be
  filled — say how) · ERROR-NONFATAL (a wrong statement that does not propagate) · EXPOSITION (unclear, not wrong).
- Where a statement allows a small-case or numerical check, run one (python3 + sympy + numpy available; launch any script as
  `bash -c 'ulimit -v 4000000; exec timeout 900 python3 script.py'` — hard memory cap, hard time cap). The box is shared
  with long-running solvers and a Lean build: never start anything heavier than that, never kill a process you did not start.
- When the paper cites a result, check whether the cited statement (fetch the arXiv source/PDF of the CURRENT version where
  you can: `curl -sL https://arxiv.org/pdf/<id>` then `pdftotext`; arxiv.org works from this box) actually says what is
  used, including hypotheses, ranges and uniformity.
- Do not edit any file outside /tmp/oaimath/012/seats/. Write your report to /tmp/oaimath/012/seats/<SEAT>_report.md and
  end it with a one-line verdict: `VERDICT: HOLDS AS READ` / `VERDICT: GAP AT <where>` / `VERDICT: FATAL AT <where>` /
  `VERDICT: COULD NOT CHECK <what>`. Then return a short summary (≤ 300 words) as your final message.
- Do not spawn sub-agents.
