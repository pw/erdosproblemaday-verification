# Hostile referee brief — Erdős #184 (Erdős–Gallai cycle decomposition): TWO AI-generated proofs, both with Lean 4 formalizations

Written by the 2026-10-20 03:00Z erdos cron seat (erdosproblemaday.com). You are one of four separately-briefed seats. Be hostile:
your job is to find where it breaks, not to admire it. Quote the exact sentence/line you object to (TeX label + printed number, or
Lean file:line). Do NOT run `lean`/`lake`/`leanchecker` (memory guard on this box — our own kernel replays run separately, gated);
read Lean sources as text. Python/grep/pdftotext/curl are fine. Write your report to the file named in your seat prompt.

THE PROBLEM (erdosproblems.com/184, live page saved /tmp/oaimath/181/live/p184.txt, proof-claims tab claims184.txt, comments c379.html):
"Any graph on n vertices can be decomposed into O(n) many edge-disjoint cycles and edges." Erdős–Gallai [EGP66 §5] proved O(n log n);
Conlon–Fox–Sudakov O(n log log n); Bucić–Montgomery O(n log* n) (arXiv 2211.07689; journal 2024). Page (edited 16 Oct 2026) now says
"A formal proof of the main conjecture … is available here" linking OpenAI's comparator file. Its proof-claims tab carries ONE claim:
Ryan Coffey (GitHub steelwheel01, "using Claude Opus 5.5"), submitted 2026-10-01 03:29:21, with paper + Lean.

PROOF A — OpenAI, "A linear cycle-and-edge decomposition of every graph", dated September 24, 2026 (released in github.com/openai/math on
6 Oct 2026, family 181), 32 pp. PDF /tmp/oaimath/181/paper.pdf (sha256 4aa44187…); pdftotext /tmp/oaimath/181/paper.txt (math MANGLED);
USE THE TeX: /tmp/oaimath/604/lean-build/repo/preprints/A-linear-cycle-and-edge-decomposition-of-every-graph-September-24-2026/build/
{main.tex, sections/{preliminaries,routing,residue,splitting,folding,induction}.tex, figures/lifting.tex, references.bib}.
Theorem 1.1: absolute C>0, every finite simple graph on n vertices has an edge partition into ≤ Cn parts, each a cycle's edge set or a
single edge. Corollary 1.2 (Eulerian; and a Δ/2+δn version under a large-cut condition via GGKO2021 Prop 6.3).
Architecture (main.tex "Outline of the proof"): scales D_j = n^{0.95^j}; at scale D remove few long cycles, assign the rest to boxes of
order ≤ D^{1.02} (total order ×(1+O(1/log D))); extract vertex-disjoint pieces of cut expansion D^{0.90}; residual average degree ≤ D^{0.95}.
Choose a layer whose total piece order S pays for a prefix; small-residue lemma (lem:small-residue) for expanding pieces; reserve edges
for routing; batch the sparse descendant boxes; pair low-degree vertices inside batch∩piece intersections and IDENTIFY pairs
(lem:pair-folding, lem:batch-resolution); induction on the quotients; lift each quotient cycle through reserved expander paths
(lem:routing) to a simple cycle. Cost O(S + n/log D) outside recursion; quotient orders sum ≤ n − S/3 + O(n/log D); residues ≤ S/100;
strengthened hypothesis C·φ(n)·n with φ(n) = max{1/2, 1 − 1/sqrt(log n)}; quotients have order ≤ D^{0.30}. External inputs: Lovász 1968
path-and-cycle decomposition, Aharoni–Haxell 2000 matching theorem, BM2024 methods. Lean: /tmp/oaimath/604/lean-build/repo/lean/OAI/
Combinatorics/CycleDecomposition/ (34 files, 21,451 lines, Main.lean proves `OAI.ErdosGallai.erdos_gallai`), comparator challenge
lean/ComparatorChallenges/CycleDecomposition.lean (+ .json: permitted axioms propext/Quot.sound/Classical.choice). Repo rev 1581d4c;
content of these paths identical to rev adc7f12 (the rev Formal Conjectures cites). Toolchain v4.34.1, Mathlib d13f23b7.

PROOF B — Ryan Coffey (Yale per README), "A proof of the Erdős–Gallai cycle decomposition conjecture", PDF created 2026-10-01 03:20Z,
152 pp. Repo clone /tmp/oaimath/181/coffey/repo (github.com/steelwheel01/erdos-gallai-lean, HEAD 660ae11). PDF paper/erdos-gallai-proof.pdf;
pdftotext /tmp/oaimath/181/coffey_paper.txt; USE THE TeX: paper/src/{ms,s1..s7,formalization}.tex. Earlier manuscript v6.1 that the Lean
statements quote: proofs/manuscript/{ms.tex,s1..s6.tex,ERRATA_v6.1.md}. Main Theorem (s1:thmMain): f(G) ≤ c_EG·n with galactic,
uncomputed constants (D* of tower type; log2 log2 D* ≥ 2^8). Architecture: keeps BM's round structure; τ-rules inside BM's Lemma 14
(Lemma 14^τ) + cap on guest degrees ⇒ hierarchy HB_tp with negligible hub concentration; standalone parts chained into cycles via junction
paths in lent random colour classes of ancestors ≥ 2 rounds back (TPV, JS-LC); each end of a leftover single edge gets a PRIVATE junction
edge to a junction vertex in a sparse random pool in its ancestor's expander ⇒ simple quotient graphs with a vanishing fraction of n
vertices in total; decompositions of quotients lift back; induction on vertex count. Lean: formal/ (601 .lean files, ~93k lines;
libraries EG, EGTest, EGCheck, Challenge, Solution), proves Formal Conjectures' `Erdos184.erdos_184` taken unchanged at FC commit
2424bb48 (formal/comparator/Challenge.lean claimed byte-identical, sha256 9f36e4e0…). Toolchain v4.33.1, Mathlib v4.33.1 (0df444a3).
README "Known limitations": no human review of maths, Lean or statement fidelity.

FORMAL CONJECTURES (google-deepmind) CURRENT main 184.lean (fetch raw.githubusercontent.com/google-deepmind/formal-conjectures/main/
FormalConjectures/ErdosProblems/184.lean): `erdos_184` now `@[category research solved, … formal_proof using lean4 at "…openai/math/
blob/adc7f124…/lean/OAI/Combinatorics/CycleDecomposition/Main.lean#L207"]` and its docstring credits "an internal OpenAI model in
September 2026". NOTE: OpenAI's Lean proves OpenAI's MainStatement (∃ C>0, ∀ n, ∀ G : SimpleGraph (Fin n), ∃ k, EdgeDecomposition G k ∧
k ≤ C·n, parts : Fin k → Set (Sym2 (Fin n)) each a Walk.IsCycle edgeSet or a singleton of an edge, pairwise disjoint, union = edgeSet) —
NOT FC's `erdos_184` (∃ f =O[atTop] n, ∀ Fintype V, ∃ D : Finset G.Subgraph, ∀ H ∈ D, IsCycleOrEdge H.coe ∧ IsDecomposition G D ∧
D.card ≤ f |V|; IsCycleOrEdge H := (H.Connected ∧ H.IsRegularOfDegree 2) ∨ H.edgeFinset.card = 1). Coffey's Lean proves FC's statement.

STANDARDS. Three classic holes: a lemma assuming the conclusion's strength; a citation that does not say what is claimed (check each
cited result in ITS source, current version — arXiv PDFs via curl, pdftotext); "clearly"/"standard" at the hard step. Count losses: an
O(n) claim dies by an accumulating per-round/per-scale cost. A formal proof makes the THEOREM's truth a question about (i) the kernel
(we replay), (ii) statement fidelity, (iii) the trusted base — so where a Lean proof exists, your most valuable output is: where the
PAPER and the LEAN disagree (paper-only claims, errata, weaker/stronger forms), and whether the formal statement means what Erdős asked.
Verdict vocabulary for your report header: HOLDS AS READ · HOLDS WITH FIXES (list) · GAP AT <where> · COULD NOT CHECK <what>.
Every objection: severity FATAL / GAP / UNCLEAR / EXPOSITION / COSMETIC, the quoted text, why, and what would fix it.

## ADDENDUM (03:3xZ) — PROOF C, found by the world seat: Jaehoon Kim (KAIST), arXiv:2610.07840
"A proof of the Erdős–Gallai cycle decomposition conjecture". v1 submitted Tue 6 Oct 2026 06:42:42 UTC (32 pp), v2 Fri 9 Oct 04:08:00
UTC (22 pp, "simplifies the first version"). Single human author; "Use of AI tools: The author made extensive use of ChatGPT (OpenAI)
and Claude (Anthropic) in developing the arguments and preparing the text and figures … The author has verified all results." No Lean.
Files: /tmp/oaimath/181/refs/kim_v2.pdf, kim_v2.txt (pdftotext -layout), kim_v1.pdf, and the LaTeX SOURCE (use it):
/tmp/oaimath/181/refs/kim_src/erdos_gallai_v2.tex. Architecture (§1.1, §2): no rounds. Potential Φ(G) = Σ_v f(d_G(v)),
f(d) = 1 − 1/√(d+1); f(d) − f(d−2) ≥ d^{−3/2}. Heavy cycle (Def 1.2): ∃ b ≥ 1 with ≥ b^{3/2} vertices of degree ≤ b on it; removing
one drops Φ by ≥ 1 ⇒ ≤ n heavy cycles in total. Procedure: remove heavy cycles; remove edges at vertices of small positive degree as
single edges; else (light, δ ≥ δ0) Theorem 1.3 gives near-closed S (G[S] min degree ≥ |S|^{1/1000}, ≥ |S|/12 vertices of S with ≤ 2
neighbours outside S), Theorem 1.4 (δ ≥ n^ε ⇒ ≤ C_ε n cycles and edges; via BM robust sublinear expanders + BM's cycle decomposition +
CFS sparse result) decomposes G[S], then remove those ≥ |S|/12 vertices with their ≤ 2 remaining edges. Charge to vertices removed.
§3 light graphs + regions, §4 counting lemmas for cycles through small-degree vertices, §5 Theorem 1.3, §6 Theorem 1.4 (6.1 random
subgraphs & routing — deterministic routing Lemma 6.6 in v2; 6.2 short/medium cycles; 6.3 proof). BM cited by arXiv:2211.07689v2
numbering (the paper says so in its reference [2]).
