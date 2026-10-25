# Referee report — seat `lean` (family 076, the formal object `OAI.AsymptoticallyMinimalLittlewood.main`)

Scope (verbatim from seats/PROMPTS.md): comparator lean/AsymptoticallyMinimalLittlewood.lean (+ .json); solution tree
/tmp/oaimath/166/lean-build/repo/.lake/packages/OAI/lean/OAI/Analysis/Littlewood/ (Model.lean, Main.lean, the 24 modules of
lean/cone.txt). Questions (1) statement identity, (2) correspondence to erdosproblems #1150, (3) route/module map vs sib1 §3–§6,
(4) vacuity/mis-statement, (5) Formal Conjectures erdos_1150 + openai/math issues. NO lake/lean run (source reading only).

Status: DONE (verdict at bottom).

## Running notes

### (1) Statement identity — first pass (09:2x)
- Model.lean (22 lines) vs comparator: `diff` of the def block shows ONLY (a) a docstring line
  `/-- Real signs in every consecutive degree 0,...,N-1. -/` before `IsRealSigning` (and `/-- The Littlewood polynomial of length N,
  evaluated at z. -/` before `littlewoodValue`) and (b) comparator has `theorem main : MainStatement := by sorry` where Model has none.
  `littlewoodValue`, `IsRealSigning`, `MainStatement` bodies are character-identical. Docstrings do not change the kernel term.
- Main.lean ends with `theorem main : MainStatement := by ...` inside `namespace OAI` / `namespace AsymptoticallyMinimalLittlewood`,
  i.e. the constant is `OAI.AsymptoticallyMinimalLittlewood.main` = the json's `theorem_names` entry. Main.lean imports only
  `OAI.Analysis.Littlewood.AlmostSign`; `MainStatement` must therefore reach it transitively from Model (checking next).

### (1) cont. — provenance and name resolution (checked)
- The comparator file + json on disk are byte-identical (`diff`) to `lean/ComparatorChallenges/AsymptoticallyMinimalLittlewood.{lean,json}`
  inside the pinned OAI checkout (git HEAD adc7f1241b42e322a6451854ab7e4b4c146bf78a, "Initial commit" 2026-10-06; `git status
  --short` = 0 lines, i.e. working tree = commit). `formalization.yaml:934–936` registers exactly this pair:
  comparator_config ComparatorChallenges/AsymptoticallyMinimalLittlewood.json · declaration OAI.AsymptoticallyMinimalLittlewood.main ·
  file OAI/Analysis/Littlewood/Main.lean.
- Import graph of the cone is a single LINEAR chain (each module imports exactly one predecessor; only Model imports Mathlib):
  Model → Gaussian → Rounding → BinaryPacket → Curvature → Cutoff → QuadraticTail → Spreading → ProductProbability → Nibble →
  Matching → Averages → FiniteRank → Chunks → DependentMoments → SlotGraph → SlotParameters → IntervalPacking → SamplingTail →
  SamplingEnergy → ModeSampling → BlockSampling → AlmostSign → Main. = 24 modules = cone.txt. 9,315 lines (wc).
- `def MainStatement` / `def littlewoodValue` / `def IsRealSigning` each occur exactly ONCE in the cone (Model.lean:8,12,15). The
  other `littlewoodValue`/`IsRealSigning` defs in the directory (FlatnessModel.lean:12,16) are in namespace
  `AsymptoticallyMinimalLittlewoodFiniteFlatness`, not in Main's cone. So `theorem main : MainStatement` (Main.lean:187) in
  `namespace OAI.AsymptoticallyMinimalLittlewood` can only resolve to Model's constant. `defect_rounding` (Rounding.lean:1225) and
  `round_sample_once` (Main.lean) state their conclusions with the SAME Model constants `IsRealSigning`, `littlewoodValue`.
- Forbidden-construct scan over the 24 cone files (source text, my grep): sorry 0 · admit 0 · native_decide 0 · implemented_by 0 ·
  extern 0 · unsafe 0 · opaque 0 · macro/syntax/elab/notation/infix 0 · set_option 0 · run_cmd/#eval/initialize 0 · `axiom` 1 hit =
  a COMMENT (Averages.lean:157 "so no conditional-probability axiom is used"). `partial` 3 hits = docstring words. Instances:
  3 `local instance` (BinaryPacket.lean:12–15: MeasureSpace UnitAddCircle := haarAddCircle, IsAddHaar, IsProbability — local, and
  declared AFTER Model so cannot touch the statement), 1 local Decidable instance (DependentMoments:251), 4 `attribute [local
  instance] Classical.propDecidable`, 1 GLOBAL `attribute [instance] FinitePacket.fintypeI/J/nonemptyI` (Spreading.lean:474) — on
  a structure defined in the cone, irrelevant to `MainStatement` (already elaborated in Model, which imports nothing but Mathlib).
- Dependency packages: OAI/lean/patches/*.patch patch OTHER packages (AINTLIB, StrongPNT, carleson, …), none patches Mathlib; the
  Littlewood cone imports none of those packages.

### (1) cont. — the pin is still current (checked 2026-10-12 via GitHub API/raw)
- openai/math main HEAD = fd4aeeb2ee4f (2026-10-08, merge of PR #1 "Update manuscripts and Lean formalizations", 1,185 files;
  its body says "Lean builds were not run for this synchronization"). I fetched every file of lean/OAI/Analysis/Littlewood/ (27,
  directory listing at main also = 27, same names) and both comparator files at fd4aeeb2ee4f: ALL byte-identical (`cmp`) to the
  adc7f124 copies on disk. lean-toolchain v4.34.1 and Mathlib pin d13f23b723 identical. So PR #1 did not touch this formal object.

### (2) Correspondence with erdosproblems.com/1150 (and Formal Conjectures `Erdos1150.erdos_1150`)
#1150 (live page, saved thread1150.html): "Does there exist a constant c>0 such that, for all large n and all polynomials P of
degree n with coefficients ±1, max_{|z|=1}|P(z)| > (1+c)√n?" Negation (= answer NO): ∀c>0, for infinitely many n there is a
degree-n ±1 polynomial with max_{|z|=1}|P| ≤ (1+c)√n.
Comparator `MainStatement`: ∀η>0 ∃N₀≥1 ∀N≥N₀ ∃ε:Fin N→ℝ, (∀k, ε k=−1 ∨ ε k=1) ∧ ∀z:ℂ, ‖z‖=1 → ‖Σ_{k:Fin N} (ε k:ℂ) z^(k:ℕ)‖ ≤ (1+η)√N.
- length vs degree: ε has N entries, all ±1 (never 0), so P_ε = Σ_{k<N} ε_k z^k has EXACT degree n = N−1 (leading coeff ±1). Every
  coefficient of index ≤ n is ±1 — matches "polynomials of degree n with coefficients ±1" (and FC's `∀ i ≤ natDegree, coeff i = ±1`
  ∧ `natDegree = n`).
- √N vs √n: Lean bounds by (1+η)√(n+1). Given c>0 take η=c/2; (1+c/2)√(n+1) ≤ (1+c)√n ⇔ (1+c/2)²(n+1) ≤ (1+c)²n, true for all
  n ≥ (1+c/2)²/((1+c)²−(1+c/2)²) — a finite threshold. So MainStatement ⇒ for every c>0 and every sufficiently large n a
  counterexample exists: strictly STRONGER than the negation of #1150 (which needs only infinitely many n). The √N normalisation is
  the natural Parseval one (‖P‖₂ = √N), so Lean is if anything the harder side of the off-by-one.
- `1 ≤ N₀`: harmless strengthening (excludes the vacuous N=0 polynomial; any N₀ can be raised). Not needed for #1150.
- `‖z‖ = 1` over ℂ: the unit circle; `‖·‖` on ℂ is the modulus. `Real.sqrt N` = `Real.sqrt (↑N : ℝ)`, argument ≥ 0, no negative-sqrt
  issue. `(ε k : ℂ)` is the real-to-complex coercion; `z ^ (k : ℕ)` uses `Fin.val`. Max over the circle is expressed as a ∀z bound —
  equivalent to the sup bound (circle compact, nonempty).
- Formal Conjectures (fetched FormalConjectures/ErdosProblems/1150.lean at main, 2026-10-12; refs/fc_1150/): `erdos_1150 :
  answer(False) ↔ ∃ c > 0, ∀ᶠ n in atTop, ∀ P : ℂ[X], (∀ i ≤ P.natDegree, P.coeff i = -1 ∨ P.coeff i = 1) → P.natDegree = n →
  ⨆ z : Metric.sphere (0:ℂ) 1, ‖P.eval z‖ > (1+c) * Real.sqrt n`, `@[category research solved, … formal_proof using lean4 at
  ".../openai/math/blob/adc7f124…/lean/OAI/Analysis/Littlewood/Main.lean#L187"]` — L187 of our Main.lean is exactly
  `theorem main : MainStatement := by`. Body is still `sorry` (FC records a link, not a bridge proof). History: added 2026-02-06
  (#2012) with `answer(sorry)` and `research open`; flipped to `answer(False)` / `research solved` by commit 3dfd999dfe (PR #6898,
  mo271, merged 2026-10-11T08:10:50Z, "mark problems solved in the OpenAI math release"); `diff` of pre/post shows ONLY the
  answer/category/docstring/reference changed — the predicate is the original Feb-2026 one, i.e. not retro-fitted to OpenAI's.
- Bridge FC ⇐ comparator (paper argument, I did NOT write/run Lean): given c>0 suppose ∀ᶠ n the FC predicate holds; take η=c/2,
  n ≥ max(N₀−1, threshold above, FC's eventual bound); build P := Σ_{k<n+1} ε_k X^k ∈ ℂ[X]; natDegree P = n, coeffs ±1;
  ⨆_{sphere}‖P.eval z‖ ≤ (1+η)√(n+1) ≤ (1+c)√n (ciSup_le, sphere nonempty) contradicting ">". So comparator ⇒ ¬FC-RHS ⇒ answer
  False is consistent. The ⨆ in ℝ has the junk value 0 only for unbounded families; P is bounded on the sphere, no junk issue.
  Verdict on (2): the Lean statement says what #1150 negates, in a slightly stronger (all large lengths) form. No mis-statement.

### (3) Route of the Lean proof — module ↔ paper map (read: statements of every top-level theorem; full text of Model, Main,
AlmostSign, the key statements in Rounding/Nibble/Matching/IntervalPacking/BlockSampling/Spreading/Gaussian/SamplingTail)
Lines: Model 22 · §2 344 · §3 packing 2,355 + Pippenger–Spencer replacement 1,748 · §4 2,366 · §5 1,113 · §6 1,367 = 9,315.
- §2 (Thm 1.1 from Prop 2.1 + Lemma 2.2): Main.lean. `small_delta_budget` picks δ∈(0,1/20) with
  √((1+δ)³/(1−δ)) + 393216·√(δ log(20/δ)) < 1+η/2 by continuity of x↦x log x at 0 (393216 = 2·196608 = the paper's 2C).
  Quantifier order is explicit and correct: η → δ(η) → all auxiliary data (δ) → N₀ → N. The paper's "lim sup then δ↓0" becomes a
  single fixed δ per η, which is the honest form. `entropy_small_defect` proves μ log(80N/μ) ≤ 4δN log(20/δ) for 0≤μ≤4δN DIRECTLY
  (log x ≤ x−1 split), i.e. it does not use the paper's monotonicity sentence "u ↦ u log(80N/u) is increasing on 0<u≤N/2"
  (sib1 p.5 l.3 of the proof) — so that sentence is not load-bearing for the formal object. µ=0 is handled separately in
  `defect_rounding` (returns ε := X). `defect_from_energy` = "1−|x| ≤ 1−x²".
- Prop 2.1: AlmostSign.lean `almost_sign_sampler` — note it is STRONGER than the printed Prop 2.1: the energy ratio has a LIMIT L
  (Tendsto) with L ≥ 1−7δ, and the sup bound is NON-asymptotic: ‖Q_X‖∞/√N ≤ K_δ + C/N for EVERY N≥1, C = C(δ) fixed. K_δ =
  √((1+δ)³/(1−δ)) exactly as printed in (1).
- §4 Prop 4.1: BinaryPacket (the recursive pⱼ of (19), `energy_increment` = (20): Mⱼ₊₁ ≥ Mⱼ + (1−Mⱼ)²/8), Curvature
  (`exists_generic` = γ off the hyperplanes s^⊥; `determinant_tuning` = (21)), Cutoff, QuadraticTail (chirp coefficients,
  nonstationary decay by repeated integration by parts, finite Fourier truncation), Spreading (`exists_auxiliary_packet`, whose
  `RawData` fields are exactly Prop 4.1's: nonzero, pairwise nonparallel, ‖F‖∞≤1 for F = 2Re Σcᵢe(aᵢ·y), (1−3δ)² ≤ 2Σ|cᵢ|²,
  λᵢ≠0, 2Σ|λᵢ|<1, |cᵢ|² ≤ K_δ²|λᵢ|). Lemma 4.2 = Gaussian.lean `uniform_quadratic_integration`: same formula as (17) with the
  explicit error π/(T|β|)·∫ξ²|ǧ(ξ)|dξ, uniform in u — proved from Mathlib's `fourier_gaussian_pi'` + `integrable_cexp_quadratic`
  + Schwartz Fourier inversion, extended to the purely imaginary (undamped) case by an in-house boundary argument.
- §3 Lemma 3.1: Chunks/FiniteRank/DependentMoments/SlotGraph/SlotParameters build the same random-slot finite-field hypergraph
  (odd slot lengths, chunks of ~R sites, oriented centers, prime q large enough that pairs of rows have rank 2), compute degrees
  and codegrees via fibers of linear forms over F_q, second-moment control; IntervalPacking `signed_interval_packing` is Lemma 3.1
  verbatim (closed arcs of length wᵢ/H centred at σaᵢ·θ_h, all 2rH pairwise disjoint), H := |matching|, θ_h := y_h/q;
  `signed_interval_packing_general` handles r=1 by padding with a fresh zero-coefficient frequency.
  **Theorem 3.2 (Pippenger–Spencer) is NOT used and is NOT in Mathlib** (grep of the pinned Mathlib d13f23b7: 0 hits for
  Pippenger / nibble / Rödl / Lovett / stationary phase). Instead Nibble.lean (1,077 l.) + ProductProbability (371) + Matching (71)
  + Averages (229) prove from scratch a Rödl-nibble ALMOST-PERFECT MATCHING (`almost_perfect_matching`): degrees within e·D of D,
  codegree ≤ C ≤ e·D, AND |U|·C ≤ K₀·D ⇒ a matching covering ≥ (1−η)|U| vertices. The extra hypothesis |U|·C ≤ K₀·D (codegree
  O(D/|U|)) is much stronger than Pippenger–Spencer's codegree o(D), and it is exactly what the finite-field construction gives
  (codegree ≤ q^{m−2} = degree·O(1/q), |U| = Θ(q); see `random_slot_matching` hypotheses). Only ONE large matching is needed (not a
  full edge colouring), so the formal route uses a weaker, cheaper, self-contained combinatorial input. This sidesteps the brief's
  question about Alon–Yuster's quantified form entirely for the formal object.
- §5: SamplingTail (Poisson summation for the sampled chirp via Mathlib `SchwartzMap.tsum_eq_tsum_fourier`, summable lattice tails),
  SamplingEnergy (off-diagonal averages incl. equal curvature → mean-square recovery), ModeSampling (`mode_energy`,
  `mode_maximum`: at most one stationary term per angle ⇒ bound K), BlockSampling (`block_cutoffs`, `stationary_unique`,
  `sample_packed`). Uniformity in t is built into the statements (∀ t ∈ [0,1], bound K + C/N with C independent of t and N).
- §6 Lemma 2.2: Rounding.lean `defect_rounding`, constant C = 196608, log(80N/µ) as printed (rows 2M = 40N, M = 20N).
  **Lemma 6.1 is NOT proved via Lovett–Meka.** The formal Lemma 6.1 analogue (`matrix_signing`: ξ∈{±1}^s, ‖Bξ‖∞ ≤
  8192·√(s log(2R/s)) for s ≤ R) is proved by the classical Beck/Spencer ENTROPY (pigeonhole) method: MGF/quantisation-code
  counting + Hamming-ball counting give two far-apart signings with identical rounded row sums (`exists_signings_same_round`),
  half their difference is a zero-start partial colouring fixing ≥ s/16 coordinates (`exists_partial_coloring`), iterated
  (`matrix_signing_raw`). The paper's arbitrary-start-point need is avoided because §6.2's dyadic scheme only ever colours the
  odd coordinates from zero (`dyadic_round_step`, sign reversal for non-increasing mass = `matrix_signing_nonpos`), exactly the
  paper's §6.2. Grid→circle: NOT the paper's maximum-principle/Cauchy/Bernstein argument but an oversampled cross-Dirichlet
  reproducing identity (`polynomial_grid_bound`: deg<N, M ≥ 2N ⇒ sup ≤ 2·grid max; proof = `Finset.sum_mul_sq_le_sq_mul_sq` on the grid mean squares of D_{2N}, D_N — my own bookkeeping gives √2, so 2 is safe).
  So the paper's citation of Lovett–Meka [19, Thm 4] is not load-bearing for the formal object either.
- Net: the formal proof follows the paper's §2–§6 architecture step for step, but replaces all three heavy external inputs
  (Pippenger–Spencer, Lovett–Meka, and the analytic grid lemma) by self-contained elementary proofs; the analytic inputs taken
  from Mathlib are standard (Gaussian Fourier transform, Fourier inversion on 𝓢, Poisson summation on 𝓢, torus Parseval /
  mFourier, ContDiffBump). Nothing heavy is axiomatised (0 `axiom` declarations in source).

### (4) Vacuity / mis-statement hunt (all negative)
- `MainStatement` is not trivially true: at N=2 the best signing has max 2 = √2·√2, so for η < √2−1 the bound fails at N=2 and
  N₀ is forced up; for small η the statement is equivalent to lim m_N = 1 (sib1 Thm 1.1 "Equivalently…", p.2), the open
  real-sign question. Nor is it trivially false (Parseval gives only ≥ √N).
- `IsRealSigning` is `∀ k, ε k = -1 ∨ ε k = 1` — excludes 0 and all other reals; coefficients are genuine signs.
- `littlewoodValue` sums ALL consecutive degrees 0..N−1 (`Fin N`, `z ^ (k:ℕ)`), no gaps, no reindexing; same constant used in
  `defect_rounding` and `round_sample_once` (only one definition in the cone).
- `Real.sqrt N` takes `(↑N : ℝ) ≥ 0`; no negative-argument junk. `‖z‖ = 1` is the full unit circle; `unitCircle_parameter`
  (Main.lean) maps every such z to t∈[0,1] with z = exp(2πit), and the sampler bound is quantified over all t∈[0,1].
- No subsequence: Lean's X N k = Re Σ_h χ_h(k/N)·F(kθ_h + (N/2)v(k/N − x*_h)²) (BlockSampling `sample_packed`) is defined for EVERY
  N ≥ 1 with H fixed and no divisibility condition; `main` produces ε for every N ≥ N₀.
- Quantifier order: η ⇒ δ (`small_delta_budget`) ⇒ packet/packing/blocks/cutoffs (`almost_sign_sampler hδ hδ20`, which takes only
  δ) ⇒ constants L, C ⇒ N₀ (eventually_atTop) ⇒ N. Nothing chosen later feeds back into an earlier choice; the constant C in
  K_δ + C/N is produced before N is introduced (the `∃ X L C, … ∀ N` shape forces this syntactically).
- json: `definition_names: []` (solver may not supply its own bodies for challenge defs — all three are fully given in the
  challenge), `permitted_axioms` = propext/Quot.sound/Classical.choice, `enable_nanoda: false` (OpenAI's config runs no second
  kernel; our queued replay adds leanchecker --fresh).
- Docstrings in Model.lean (absent in the comparator) are not part of the kernel declarations.

### (5) Formal Conjectures + openai/math issues
- FC: see (2) — `Erdos1150.erdos_1150` exists, predicate unchanged since Feb 2026, answer(False) + research solved + proof link to
  Main.lean#L187 since PR #6898 (merged 2026-10-11T08:10:50Z). The FC→comparator bridge is NOT formalised by anyone (FC body
  `sorry`); the bridge is elementary (my sketch in (2)). FC also proves `erdos_1150.variants.parseval_lower_bound` (≥ √(n+1)),
  consistent with Lean's √N normalisation.
- openai/math: repository has Issues DISABLED (`has_issues: false`, `open_issues_count: 0` via API 2026-10-12); the issues
  endpoint returns exactly one item, PR #1 (dr-openai, 2026-10-08, merged; body: "Lean builds were not run for this
  synchronization"). GitHub search `repo:openai/math littlewood` → 0. So "no reaction found" on family 076 there — and none is
  possible via issues. PR #1 did not modify any Littlewood or comparator file (byte-compare in (1)).

## Scope read
- Comparator lean/AsymptoticallyMinimalLittlewood.lean + .json: whole. Model.lean (22 l.), Main.lean (232 l.), AlmostSign.lean
  (112 l.): whole, line by line. Statements (not proof bodies) of every top-level theorem/lemma/def/structure in the other 21 cone
  modules (grep of `theorem|lemma|def|structure` + docstrings), and in full the statements of: Rounding `defect_rounding`,
  `defectMass`, `matrix_defect_rounding`, `dyadic_round(_step)`, `matrix_signing(_raw)`, `exists_partial_coloring`,
  `polynomial_grid_bound`; Nibble `almost_perfect_matching` (+ its parameter wiring); Matching `matching_after_pruning`;
  SlotGraph `random_slot_matching`; IntervalPacking `integer_slot_matching`, `signed_interval_packing(_fintype/_general)` (+ the
  tail of the proof turning a matching into θ_h); Spreading `RawData`, `FinitePacket`, `exists_auxiliary_packet` (head);
  Gaussian `integral_schwartz_mul_gaussian`, `integral_schwartz_quadratic_exact`, `uniform_quadratic_error`,
  `uniform_quadratic_integration`; SamplingTail `poisson_chirp`, `poisson_tail_bound`; BlockSampling `block_cutoffs`,
  `sample_packed` (+ the definition of X).
- Paper (sib1) for the correspondence only: pp.2–5 (§1 Thm 1.1, §1.3, §2 Prop 2.1/Lemma 2.2/proof of Thm 1.1), p.5–6 (Lemma 3.1,
  Thm 3.2 statement), pp.9–12 (Prop 4.1, Lemma 4.2, start of the proof incl. (19)–(21)), pp.18–21 (§6 in full). Text layer only.
- erdosproblems #1150 statement (live/thread1150.html). Formal Conjectures 1150.lean (main + pre-solved revision 6fbb54f24c) and
  PR #6898. openai/math: repo metadata, issues/PR list, PR #1, main HEAD file listing, 30 files byte-compared.

## Method
Source reading + grep + `diff`/`cmp` + GitHub API/raw fetches into refs/fc_1150, refs/gh_openai_math, refs/openai_math_main (data
only, nothing executed). No lake/lean/leanchecker run. A small amount of arithmetic by hand (N=2 counterexample to small η; the
√(n+1)→√n threshold; constant bookkeeping 393216 = 2·196608, 196608 = 8·24576, 40N rows ⇒ log(80N/µ)).

## Findings
No FATAL. No GAP in scope.
- EXPOSITION E1 (cross-seat; the important one). The formal proof does NOT go through the paper's three external inputs:
  (a) Pippenger–Spencer/Alon–Yuster (sib1 p.4 §1.3: "It uses a randomly constructed finite-field hypergraph and the
  Pippenger–Spencer coloring theorem"; p.6 Thm 3.2) — replaced by an in-house Rödl-nibble almost-perfect-matching theorem under the
  stronger codegree hypothesis |U|·C ≤ K₀·D, which the finite-field hypergraph supplies; (b) Lovett–Meka (p.4: "in the
  arbitrary-vector form verified through Lovett–Meka's theorem [19]"; p.18: "we derive it from the arbitrary-vector partial-coloring
  theorem of Lovett and Meka [19, Theorem 4 in the cited preprint version]") — replaced by the classical entropy/pigeonhole
  zero-start partial colouring (fixes ≥ s/16 coords) iterated, which suffices because §6.2 only colours odd dyadic coordinates
  from zero; (c) the maximum-principle/Cauchy grid-to-circle passage (pp.20–21) — replaced by a Cauchy–Schwarz cross-Dirichlet
  reproducing identity (M ≥ 2N ⇒ sup ≤ 2·grid max). Consequence for the panel: a kernel PASS certifies Theorem 1.1 itself but
  NOT the paper's citations at Thm 3.2 / Lemma 6.1; conversely, any hypothesis mismatch the construct/round seats find in those
  citations is repairable from the formal route and would not touch #1150.
- EXPOSITION E2. The printed Prop 2.1 (p.4, "lim sup_{N→∞} ‖Q_X‖∞/√N ≤ K_δ", "lim inf … ≥ 1−7δ") undersells what is formalised:
  `almost_sign_sampler` proves ∀N≥1, ‖Q_X‖∞/√N ≤ K_δ + C(δ)/N and that the energy ratio CONVERGES to some L ≥ 1−7δ. Not a defect.
- EXPOSITION E3. The proof of Thm 1.1 (p.5 l.7–8: "The function u ↦ u log(80N/u) is increasing on 0 < u ≤ N/2") is true (the
  derivative log(80N/u)−1 > 0 for u < 80N/e) but not used by the formal proof, which proves µ log(80N/µ) ≤ 4δN log(20/δ) directly.
- EXPOSITION E4 (world). No formal bridge exists from the comparator to FC's `erdos_1150` (FC body is `sorry`, it only links
  Main.lean#L187). The bridge is elementary (sketch in (2)); the comparator statement is the stronger one.
- Not a finding but recorded: openai/math has Issues disabled; the FiniteFlatness comparator (Cor 7.1) is a separate theorem with
  its own namespace and 3 extra modules — not in this cone, not checked.

## External inputs checked
- Formal Conjectures FormalConjectures/ErdosProblems/1150.lean @ main (3dfd999dfe, 2026-10-11) and @ 6fbb54f24c (pre-solve):
  predicate identical in both (diff = answer/category/docstring/reference only). Statement vs use: degree-n / √n / ±1 coefficients
  / sup over Metric.sphere — implied by the comparator (see (2)).
- openai/math @ fd4aeeb2ee4f (current main) vs pinned adc7f124: Littlewood dir (27 files) + 3 comparator files byte-identical;
  toolchain v4.34.1 and Mathlib d13f23b723 identical.
- Mathlib d13f23b7 (on disk): no Pippenger–Spencer, Rödl nibble, Lovett–Meka, Spencer discrepancy or stationary-phase theorem
  (grep 0 hits). Used from Mathlib: `fourier_gaussian_pi'`, `integrable_cexp_quadratic`, Schwartz Fourier inversion,
  `SchwartzMap.tsum_eq_tsum_fourier` (Poisson), `hasSum_sq_fourierCoeff`/mFourier (torus Parseval), `ContDiffBump`, Haar on
  UnitAddCircle. I did not re-verify these Mathlib statements (trusted library).

## What I skimmed / did not check
- Proof BODIES of 21 modules (Nibble, ProductProbability, Averages, FiniteRank, Chunks, DependentMoments, SlotGraph,
  SlotParameters, IntervalPacking except its tail, BinaryPacket, Curvature, Cutoff, QuadraticTail, Spreading, Gaussian except
  statements, SamplingTail/Energy, ModeSampling, BlockSampling except X, Rounding except the statements listed) — their
  correctness is the kernel's job (replay queued in /tmp/oaimath/076/lean-build; not run by me).
- Elaborated identity of Model vs comparator constants: I established TEXTUAL identity (bodies character-identical, same imports
  = Mathlib only, same package options); the pp.all comparison in ChallengeStatement.lean/Axioms1150.lean is the instrument for
  elaborated identity and has not run yet.
- `#print axioms`: I report source greps only (0 sorry/admit/axiom-decl/native_decide/implemented_by/extern/unsafe/opaque/
  macro/elab/notation/set_option in the 24 files; the single "axiom" string is a comment). The kernel replay must confirm.
- The FiniteFlatness theorem and its 4 extra modules; the paper's §7–§8 and Appendix A; the PDF-rendered math (text layer only).

## Verdict
HOLDS AS READ IN SCOPE — `main` in Main.lean proves the constant `OAI.AsymptoticallyMinimalLittlewood.MainStatement` defined in
Model.lean, textually identical to the comparator; the statement is non-vacuous and implies a strictly stronger (all-large-n)
negation of erdosproblems #1150 / FC `erdos_1150`; the formal route follows sib1 §2–§6 but replaces Pippenger–Spencer,
Lovett–Meka and the grid lemma by self-contained proofs. Final word on the theorem itself rests on the queued kernel replay.

Status: DONE.
