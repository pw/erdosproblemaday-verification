# Hostile referee brief — Erdős #986 / OpenAI family 170: "Sharp logarithmic exponents for off-diagonal Ramsey numbers"

Written by the 2026-10-20 12:00Z erdos cron seat (erdosproblemaday.com). You are one of five separately-briefed seats. Be hostile:
your job is to find where it breaks, not to admire it. Quote the exact sentence/line you object to (TeX file + label, or Lean
file:line). Do NOT run `lean`/`lake`/`leanchecker` (memory guard on this box — our own kernel replay runs separately, already
launched); read Lean sources as text. Python/grep/pdftotext/curl are fine; any python you run must be memory-capped:
`bash -c 'ulimit -v 8000000; exec timeout 1800 python3 …'`. Write your report to the file named in your seat prompt, and WRITE IT
INCREMENTALLY (append findings as you go — a seat that dies at a session limit must leave its partial report on disk).

THE PROBLEM (erdosproblems.com/986, live page saved /tmp/oaimath/170/live/986.html, thread forum_thread_986.html): "For any fixed s ≥ 3,
R(s,k) ≫ k^{s−1}/(log k)^c for some c = c(s) > 0." The page (last edited 21 June 2026) says the problem is RESOLVED by Bradač [Br26]
(arXiv 2605.28793, v3 ~17 June 2026): r(s,k) ≫_s k^{s−1}/(log k)^{2s−4}; "an earlier version of Bradač's work had an exponent of s−2 —
the adjustment to achieve s−1 was observed by an internal model at OpenAI". A forum comment says Bradač's paper has a Lean
formalization (https://www.math.cmu.edu/~wes/trellis.php). Upper bound O_s(k^{s−1}/(log k)^{s−2}) = Ajtai–Komlós–Szemerédi 1980; LRZ 2001.

THE CLAIM (OpenAI, two preprints both dated 24 Sept 2026, released in github.com/openai/math 6 Oct 2026, family 170):
  r(s,t) = t^{s−1}/(log t)^{s−2+o(1)} for every fixed s ≥ 5 — i.e. Bradač's log power 2s−4 improved to the AKS power s−2 (+ε).
  Paper A — "The sharp logarithmic exponent of r(5,t)" (41 pp): PDF /tmp/oaimath/170/papers/r5.pdf (sha256 71adbadd…), pdftotext
    r5.txt (MATH MANGLED — use the TeX): /tmp/oaimath/170/repo/preprints/The-Sharp-Logarithmic-Exponent-of-r-5-t-September-24-2026/build/
    {paper.tex, introduction, upper-bound, flags-entropy, predictor-statement, compression-local, compression-tree, predictor-setup,
    predictor-geometry, predictor-score, predictor-completion, final-conversion}.tex + references.bib.
    Theorem 1.1: ∃ C, ∀ε>0, t ≥ t₀(ε): t⁴/(log t)^{3+ε} ≤ r(5,t) ≤ C t⁴/(log t)³.
  Paper B — "Sharp Logarithmic Exponents for Fixed Off-Diagonal Ramsey Numbers" (53 pp, s ≥ 6): PDF papers/s6.pdf (sha256 20ab597a…);
    TeX /tmp/oaimath/170/repo/preprints/Sharp-Logarithmic-Exponents-for-Fixed-Off-Diagonal-Ramsey-Numbers-September-24-2026/build/
    {main.tex, sections/00-introduction … 06-conclusion.tex, figures/validation.tex, references.bib}.
    Theorem 1.1 (intro:main) for s ≥ 6; Theorem 1.2 (intro:prime-construction): d ≥ 5, 0<η<1/10, large prime q, σ = log q: a graph
    on ⌊q^d σ⌋ vertices, K_{d+1}-free, α < ⌊q σ^{1+η}⌋.
  CONSTRUCTION (both): N i.i.d. uniform incident flags (a_i, b_i) of PG(d,q) (point a, hyperplane b ∋ a); positions i<j adjacent iff
    a_i ⊥ b_j and a_j ⊥̸ b_i (Bradač's ordered incident-flag graph, [Br26 §2.5]). K_{d+1}-free by linear independence. An independent set
    = a "consistent" flag sequence: i<j, a_i ⊥ b_j ⇒ a_j ⊥ b_i.
  PROOF SHAPE: suppose every stream has a consistent sequence of length k = ⌊qσ^{1+η}⌋; select one (law may be heavily biased).
    Entropy LOWER bound H(F) ≥ dσℓ + ηℓ log σ − O(k) for a selected sequence of deterministic length ℓ = Θ(k), surviving O(1)
    conditionings on events of probability bounded below. Entropy UPPER bound dσℓ + O(k) by a compression ("marking" à la Bradač
    Claim 2.13, all but O(q log q) positions marked in known domains of size O(q^d); sparse-pair DESCRIPTION theorem for point sets
    with incidence density ≪ 1/q — samples from public random tables + geometric data, Poisson score, rich-line/plane polynomial
    bounds with characteristic > degrees (Dvir, Guth–Katz, Elekes–Kaplan–Sharir, Ellenberg–Hablicsek); balanced binary tree of
    incidence tests with fresh validation samples; additive potential; bounded number of iterations, decoder restarting from the full
    projective spaces each round). Paper B adds: repeated projection reducing dimension j ≥ 4 to 2 and 3; a two-row high-rank
    description via a rich-subspace bound from Nie–Wang's finite-degree closure inequality; "reciprocal classes" vs high-rank classes.
    Final section: prime parameters → all large t; the AKS-type upper bound.
  LEAN (repo rev 1581d4c): /tmp/oaimath/170/repo/lean/OAI/Combinatorics/{RamseyFive,SharpRamsey}/ — 858 files / 123,565 lines
    (RamseyFive closure 482 modules, SharpRamsey 408, 32 shared), imports Mathlib only. Mains: RamseyFive/Main.lean proves
    `OAI.SharpRamseyFive.main : SharpBounds ∧ SharpExponent`; SharpRamsey/Main.lean proves `OAI.SharpLogRamsey.main (s) (hs : 6 ≤ s) :
    MainBounds s ∧ MainLimit s`. Comparator challenges lean/ComparatorChallenges/{RamseyFive,SharpLogRamsey}.{lean,json} (permitted
    axioms propext/Quot.sound/Classical.choice). Docs lean/docs/170.md. Toolchain v4.34.1, Mathlib d13f23b7. Our source audit
    (12:1xZ): no axiom/sorry/native_decide/metaprogramming/set_option anywhere outside the two challenge files' `sorry`. Our kernel
    replay of all 858 modules is RUNNING (results land in /tmp/oaimath/170/lean-build/{driver.log,modules.tsv,steps.tsv}).

STANDARDS. Three classic holes: a lemma assuming the conclusion's strength; a citation that does not say what is claimed (check each
cited result in ITS source, current version — arXiv PDFs via curl + pdftotext); "clearly"/"standard" at the hard step. For an
entropy-compression proof the specific failure modes are: (1) the lower bound's conditioning — does H(F) ≥ dσℓ + ηℓ log σ − O(k)
really survive the conditionings used later, with the stated O(k)? (2) message-length accounting — does any message cost carry a
hidden σ or log σ factor per position that, summed over Θ(k) positions, exceeds the ηℓ log σ surplus? (3) adaptivity — samples
"fresh" relative to what was selected? public tables fixed BEFORE or AFTER the stream/selection? (4) an iteration whose losses
compound beyond O(1) rounds; (5) the transfer from primes q and the specific N, k to every large t (Bertrand-type gaps,
monotonicity of r, rounding). Count every log σ.
A formal proof makes the THEOREM's truth a question about (i) the kernel (we replay), (ii) statement fidelity, (iii) the trusted base —
so where a Lean proof exists, your most valuable output beyond the maths is: where the PAPER and the LEAN disagree (paper-only claims,
weaker/stronger forms, a lemma the Lean proves differently), and whether the formal statement means what Erdős asked.
Verdict vocabulary for your report header: HOLDS AS READ · HOLDS WITH FIXES (list) · GAP AT <where> · COULD NOT CHECK <what>.
Every objection: severity FATAL / GAP / UNCLEAR / EXPOSITION / COSMETIC, the quoted text, why, and what would fix it.
