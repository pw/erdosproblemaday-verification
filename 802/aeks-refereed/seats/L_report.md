# Seat L report — OpenAI Lean formalization of "A logarithmic independence bound for clique-free graphs" vs the paper

VERDICT: HOLDS AS READ — the comparator statement is exactly Theorem 1.1 (r ≥ 4, c chosen before V and G, real
average degree 2|E|/n, Mathlib independence number, natural log); no soundness-weakening construct anywhere in the
31 modules; every load-bearing paper step has a Lean counterpart. Several steps take a different (valid) route — listed
in §5 so the entry does not say "the Lean follows the paper line by line". Two EXPOSITION items (§6). No FATAL, no GAP.

Scope: read-only source audit of /tmp/oaimath/184/repo/lean/OAI/Combinatorics/CliqueFree/ (31 files, 5,539 lines),
ComparatorChallenges/CliqueFreeLog.{lean,json}, lakefile.lean, patches/. Nothing built. Lean v4.34.1; Mathlib pin
d13f23b723b8… (= the local checkout /tmp/erdos0300/lean/mathlib4, same commit, used to read the Mathlib definitions).

## 1. The comparator statement vs Theorem 1.1

Challenge (ComparatorChallenges/CliqueFreeLog.lean) and solution (OAI/Combinatorics/CliqueFree/Main.lean):

    noncomputable def averageDegree {V : Type*} [Fintype V] (G : SimpleGraph V) : ℝ := by
      classical
      exact 2 * (G.edgeFinset.card : ℝ) / (Fintype.card V : ℝ)

    theorem logarithmic_independence_bound (r : ℕ) (hr : 4 ≤ r) :
        ∃ c : ℝ, 0 < c ∧
          ∀ {V : Type} [Fintype V] (G : SimpleGraph V),
            G.CliqueFree r → 2 ≤ averageDegree G →
            c * (Fintype.card V : ℝ) * Real.log (averageDegree G) / averageDegree G ≤ (G.indepNum : ℝ)

- Text identity: the `averageDegree` def (challenge vs Model.lean) and the theorem header (challenge vs Main.lean) are
  byte-identical (diffed). CliqueFreeLog.json: definition_names = [] (no definition holes — so comparator requires the
  solution's `OAI.CliqueFreeLog.averageDegree` to be the same declaration, which it is), permitted_axioms =
  propext/Quot.sound/Classical.choice, enable_nanoda false. Empty definition_names is the norm in this repo (393 of the 403
  challenges that define anything); it means "no definition holes", not "unchecked" — comparator requires every constant
  used by the challenge statement to be the same declaration in the solution environment (our own comparator notes,
  /tmp/oaimath/181/coffey/repo/formal/comparator/README.md, "Why the bridge is split").
- averageDegree = 2|E|/|V| as a real. |V| = 0 gives 2·0/0 = 0 (Lean x/0 = 0), so `2 ≤ averageDegree G` is false and
  the empty graph is excluded — consistent with the paper, which defines d only for n > 0 (§1, "If G has n>0
  vertices"). Main.lean derives `Fintype.card V ≠ 0` from exactly this. The Fintype instance on edgeSet comes from
  `classical`; card is instance-independent, so the value is the true edge count.
- `G.indepNum` (Mathlib Clique.lean:1048) = sSup {n | ∃ s, G.IsNIndepSet n s}; IsNIndepSet = IsIndepSet ∧ card = n.
  For finite V the set is bounded and nonempty (n = 0), so this is the maximum size of an independent set
  (`exists_isNIndepSet_indepNum`, `IsIndepSet.card_le_indepNum`). The ℕ-sSup junk value (0 for an unbounded set) could
  only make the statement HARDER, and cannot arise for Fintype V.
- `G.CliqueFree r` (Clique.lean:379) = ∀ t : Finset V, ¬ G.IsNClique r t; IsNClique = IsClique ∧ card = r. Exactly
  "no r pairwise adjacent vertices". SimpleGraph = loopless undirected simple graph.
- Quantifier order: ∃ c, 0 < c ∧ ∀ {V} [Fintype V] G, … — c depends only on r (and hr); it is chosen before V, G, n, d.
  Matches "c_r depends only on r". The proof's c is 1/(16·D) with D = 3+3B/2, B from `exists_optimizer_triangle_bound
  (r-2)` — no dependence on n or d possible by the binder order.
- `Real.log` = natural log (paper: "All logarithms are natural"). With d ≥ 2, log d > 0; no log-of-nonpositive junk.
- Parse: c*n*log d/d = ((c·n)·log d)/d; d ≥ 2 > 0, so no division junk.
- Universe: `{V : Type}` (universe 0 only). Not a mathematical weakening: every finite simple graph is isomorphic to
  one on `Fin n : Type`, and α, |E|, n, K_r-freeness are isomorphism invariants. Formally it is the less general
  statement; the internal library is universe-polymorphic (`universe u` throughout) and Main instantiates `.{0}` only
  because the challenge fixes `Type` — replacing `.{0}` by `.{u}` in Main should give the polymorphic version verbatim (not compiled).
  EXPOSITION at most.
- Hypotheses r ≥ 4 and d ≥ 2: identical to the paper. (The Lean proof only uses r ≥ 2 — `Nat.sub_add_cancel` on
  r-2+2 — so the same proof covers r = 3; see §5.12.)
- Vacuity: not vacuous (e.g. C₅ is K₄-free with d = 2). Not weaker than the paper in any respect.

## 2. Paper item → Lean declaration (all in namespace OAI.CliqueFreeIndependence.WeightedGraph unless noted)

Import chain (31 modules, all reached from Main; only Model.lean imports anything outside the folder, and that is
`import Mathlib`): Model → Numerical → WeightedGraph → Optimizer → OptimizerBounds; Lottery → MultiplierLaw →
Deletion; FiniteEntropy → EdgeState; Packing → SparseMultipliers → VariationalCross → DisjointCross → CrossBound;
TriangleState → Projection → Splitting; Reach; FiniteKernel → LocalWalk → WalkEntropy → WalkCoupling; FiniteCoupling;
SplittingLoss → VertexSplitting; Peeling → TriangleBound → IndependentSet → MaxDegree → Main.

| Paper (printed numbering) | Lean file : declaration | Notes |
|---|---|---|
| §2 definitions M_G, w(S), e_w(S,D), F_G, F*_G | WeightedGraph: `mass`, `crossMass`, `edgeMass` (=crossMass univ univ/2), `neighbors`, `commonMass`; Optimizer: `vertexPotential` (t(1−log t), Mathlib log 0 = 0 gives 0·log 0 = 0), `potential`, `IsOptimizer` (w ≥ 0 and potential q ≤ potential w ∀ q ≥ 0) | faithful |
| Lemma 2.1 (existence, positivity, (2.1) stationarity, w_v ≤ 1, (2.2) divergence identity) | Optimizer: `exists_optimizer`, `optimizer_stationary` (0 < w_v ∧ log(1/w_v) = w(N(v)) ∧ w_v ≤ 1), `optimizer_divergence` | different route (§5.1); no "nonempty" hypothesis needed |
| Lemma 2.2 (sparse multipliers, b_r(ε) = 2^{r(r−2)} ε^{−(r−2)}) | SparseMultipliers: `sparse_multipliers_on` (k = r−2; `multiplierBound k ε = 2^{(k+2)k}/ε^k`); Packing: `neighborhood_packing`; MultiplierLaw: `normalize_subprob`, `BoundedOn`, `expectedEdges`; Lottery: finite laws as `List (ℝ × α)` | different multiplier construction (§5.2); conclusion slightly stronger |
| (2.4) g_x | WeightedGraph: `growth x s = s*(x + max 0 (log (1/s)))` (s = 0 ↦ 0); EdgeState: `growth_mono`, `growth_le_twice` | faithful |
| Lemma 2.3 (cross mass, C_r = 16r²) | CrossBound: `optimizer_cross_bound k G hw hfree : CrossBound G w (16*((k:ℝ)+2)^2)`; DisjointCross: `optimizer_cross_disjoint`, `optimizer_cross_disjoint_moderate`, `log_multiplier_le`, `cross_error_le`; VariationalCross: `variational_cross_lottery` | same q-vector; different constant bookkeeping and exact averaging over colourings (§5.3) |
| (3.1) cross-mass property | WeightedGraph: `CrossBound G w C` (∀ x ≥ 1, ∀ A B Finsets, mass A ≤ eˣ → mass B ≤ eˣ → crossMass A B ≤ C·growth x (mass A)) | faithful, sets may overlap |
| Theorem 3.1 | TriangleBound: `weighted_triangles (hC : 1 ≤ C) : ∃ B > 0, ∀ V G w, (∀ v, 0 < w v) → CrossBound G w C → triangleMass G w ≤ B * edgeMass G w`, B = 2(1+e^X/3) | same constant as paper's C_△; different iteration (§5.6) |
| Lemma 3.2 (preservation under splitting) | Projection: structure `EdgeProjection H G π` (map_adj; inj = injective on directed edges); `EdgeProjection.crossBound`, `.edgeMass_le`, `.neighborMass_le`, `.edgeMap_injective`; TriangleBound: `EdgeProjection.of_le` (edge deletion) | the T_H ≤ T_G clause and the general "finite composition" clause have NO Lean counterpart — not needed (§5.5) |
| Lemma 3.3: (3.3) normalisations | WeightedGraph: `triangleMass` is DEFINED as (Σ_u w_u h_u)/6 with `triangleAt` = h_u; TriangleState: `sum_weight` (Σ over ordered triangles = 6T), `marginal` | second identity is definitional in Lean |
| Lemma 3.3: (3.4) T ≤ (L/3)M | WeightedGraph: `triangleMass_le_of_neighborMass` | faithful |
| Lemma 3.3: peeling (3.5), s_u ≥ τ, h_u ≥ τ s_u, cross-mass inherited | Peeling: `peeling` (∃ H ≤ G, ∀ edges c_uv ≥ τ, T_G − τM_G ≤ T_H); WeightedGraph: `neighborMass_ge_of_commonMass`, `triangleAt_ge_of_commonMass` | different route (§5.4) |
| §4 setup: P_u, Q_u, K_u^j, π_u, μ, ordered triangle law (4.3), H_w, TV | LocalWalk: `transition` (one kernel on oriented edges EdgeState G, block-diagonal by source), `law` (= μ), `normalizer` (= 6T, `normalizer_eq`), `vertexWeight`; FiniteKernel: `lazy`, `smoothed P j = P * lazy P ^ j`, `avgEntropy`; FiniteEntropy: `entropy`, `divergence`, `tv` | kernels on the disjoint union of the neighbourhoods instead of one per centre (§5.7) |
| Lemma 4.1 (constants E_C = 42C²+2C, A_C = 10+E_C, B_C = 2√(A_C+1), R = ⌈x⌉) | WalkEntropy: `LocalWalk.exists_smooth_index` (x ≥ 32, has an edge, c_uv ≥ 1/x, s_u ≤ eˣ ⇒ ∃ j < ⌈x⌉₊, H_j ≤ A_C log x ∧ rowDistance j ≤ B_C √(log x/x)); Reach: `exceptionalConstant`, `entropyConstant`, `smoothingConstant` | constants identical |
| reversibility, (4.4) density | LocalWalk: `transition_reversible`, `smoothed_density`; FiniteKernel: `reversible_smoothed`, `smoothed_density` | faithful |
| (4.5) −log x ≤ H_0 ≤ … ≤ H_R ≤ A_C log x | WalkEntropy: `avg_entropy_lower`, `avg_entropy_upper`; FiniteKernel: `smoothed_entropy_mono` | faithful |
| S_i(v), w(S_R) ≤ e^{20x²}, leakage (4.6) | Reach: `enlarge`, `reach`, `reach_mass_exp` (threshold = 1/(eˣx⁶) = x^{−6}/L, `Numerical.threshold`); WalkEntropy: `reach_leakage`, `incoming_good_le` | faithful |
| B_v, w(B_v) ≤ 21C x^{−6} s_v, (4.7) P(u ∈ B_v ∣ v) ≤ E_C x^{−4} | Reach: `badSet`, `reach_bad_mass`, `conditional_bad_bound`, `reach_bad_cross`; WalkEntropy: `law_bad_sum`, `law_bad_le` | faithful |
| (4.8) H_w ≤ log m, H_R bound | FiniteEntropy: `entropy_supported_le_log`, `entropy_supported_concentration`; WalkEntropy: `entropy_good_row`, `averaged_entropy_bound` | faithful |
| (4.9) entropy increment, Pinsker-type TV ≤ √D, corner triangle inequality, (4.2) | FiniteKernel: `entropy_increment`, `entropy_increment_nonneg`, `entropy_increment_tv`, `lazy_triangle_tv`, `smoothed_row_distance_sq`, `exists_smoothed_row_distance`; FiniteEntropy: `hellinger_le_divergence`, `tv_sq_le_hellinger` | faithful |
| Lemma 5.1 (shared rejection, 2d/(1+d)) | FiniteCoupling: `shared_rejection` (+ `exists_threshold_law`, `joint_of_trials`, `sharp_bound_le`) | finite construction, all rows coupled jointly (§5.8) |
| Lemma 5.2 (δ_x = (A_C+1) log x/(√x + log x)) | FiniteKernel: `reversed_entropy_tail` (+ FiniteEntropy `entropy_tail`); applied in VertexSplitting `weighted_splitting` (hδ) with a = √x | inadmissible ⟺ K(y,e) < w_v e^{−√x}, as in (5.2) |
| (5.3) group weight ≤ e^{√x}; the split graph H′ | Splitting: `Splitting.graph`, `Splitting.projection`, `Splitting.neighborMass_le` | copies indexed by ALL oriented edges (u,y), empty groups kept as isolated vertices (harmless) |
| Lemma 5.3 (a_C = 6(B_C+A_C+1)) | VertexSplitting: `splittingConstant`, `weighted_splitting`, `splitting_error_le`; SplittingLoss: `Splitting.exists_graph`, `expected_loss_le`, `bad_mass_le`; Splitting: `Survives`, `triangleMass_surviving_le`; WalkCoupling: `triangle_pair_sum`, `triangle_edge_sum`; TriangleState: `corner_sum`, `sum_edge_permutations` | same a_C; the "conditions are also necessary"/"at most one triangle over each old triangle" converse is not formalised (not needed — only ≥ is used) |
| (5.4) X(C) | Numerical: `exists_iteration_threshold` (X ≥ 32 ∧ a·log X/√X ≤ 1/4), `lossRatio` | identical condition |
| Proposition 5.4 | TriangleBound: `neighborhood_reduction` | hypothesis "x ≥ 32 and a_C log x/√x ≤ 1" instead of "x > X(C)" (more general) |
| proof of Theorem 3.1, (5.5) summable losses | TriangleBound: `triangle_bound_scale`, `weighted_triangles`; Numerical: `scale`, `lossRatio_square`, `lossRatio_scale`, `inv_scale`, `recurrence_bound` | different iteration (§5.6) |
| (5.10) T ≤ B_r M for optimisers, B_r = C_△(16r²) | IndependentSet: `exists_optimizer_triangle_bound (k : ℕ) : ∃ B > 0, ∀ V G w, IsOptimizer G w → G.CliqueFree (k+2) → triangleMass G w ≤ B * edgeMass G w` | faithful (B = C_△(16(k+2)²)) |
| (6.1) D_r = 3 + 3B_r/2 | literal `3+3*B/2` in IndependentSet, MaxDegree, Main | faithful |
| (6.2) closed-neighbourhood deletion cost | Deletion: `optimizer_deletion_cost`, `mass_closedNeighbors`, `edgeMass_closedNeighbors`, `potential_induce` | faithful |
| (6.3) averaged cost ≤ D_r log Δ | IndependentSet: `exists_cheap_vertex` | faithful (same w_v² ≤ w_v estimates) |
| (6.4) W ≥ n/Δ, (6.5) 2M/W ≤ log Δ | OptimizerBounds: `optimizer_total_weight`, `optimizer_edge_bound` (Δ ≥ 3, uses e < 3) | faithful |
| Proposition 6.1, first inequality | IndependentSet: `maximum_degree_potential_bound` (∃ independent I with potential q ≤ D log Δ·|I| for all q ≥ 0; strong induction on |V|) | phrased with an explicit I; takes the triangle bound as a hypothesis `htri` |
| Proposition 6.1, second inequality | MaxDegree: `maximum_degree_independence`, `potential_const_lower`, `log_le_one_add_quarter`, `edgeMass_const_le` | constant n log Δ/(4·(3+3B/2)·Δ) exactly as printed; conditional on `htri` (§4) |
| proof of Theorem 1.1 | Main: `OAI.CliqueFreeLog.logarithmic_independence_bound`; MaxDegree: `degree_cutoff_card`, `indepNum_induce_le`; IndependentSet: `degree_induce_le`, `indepSet_image_induce` | c = 1/(16D), as printed |

Paper steps with NO Lean counterpart (none load-bearing): Lemma 3.2's T_H ≤ T_G clause and its general composition
clause; Lemma 5.3's converse (survival conditions are necessary; ≤ 1 triangle above each old triangle); Lemma 5.1's
"rows stop a.s." (no infinite trials in Lean); §1's sharpness/history remarks. Lean steps with no paper counterpart: the
clamp lemma `potential_clamp` (existence of the maximiser), `normalize_subprob` (zero-padding of the lottery),
`recurrence_bound`, `Numerical.scale`, `exists_threshold_law`/`joint_of_trials` (finite rejection sampling).

## 3. Audit for anything that could make the kernel check weaker than it looks

Counts over the 31 files (grep, word-bounded where meaningful):
axiom 0 · sorry 0 · admit 0 · native_decide 0 · `decide := true` 0 · `by decide`/`decide` 0 · implemented_by 0 ·
extern 0 · unsafe 0 · opaque 0 · set_option 0 (so no maxHeartbeats 0, no debug.skipKernelTC) · macro 0 · elab 0 ·
syntax 0 · @[csimp] 0 · #eval 0 · #exit 0 · run_cmd/run_tac 0 · `open Lean`/`Lean.` 0 · meta 0 · partial def 0 ·
termination_by/decreasing_by 0 · Inhabited/default 0 · Classical.ofNonempty 0 · private 0 · irreducible_def 0 ·
Lean.ofReduceBool/trustCompiler 0. Confirms the main seat's grep.
Present and benign:
- `attribute [local instance] Classical.propDecidable` (in 30 of 31 files; not Model.lean) and `Classical.decEq` local instances
  (CrossBound; FiniteCoupling ×3; FiniteKernel ×1; `edgeStateDecEq := Classical.decEq _` declared once in EdgeState and
  re-enabled with priority 10000 in 10 files). Decidability instances only choose terms; the kernel checks the proofs.
  None appears in the main statement (its only instance argument is the bound `[Fintype V]`).
- One `Classical.choice (inferInstance : Nonempty J)` (FiniteCoupling.lean:150) — picks a default label; uses a
  permitted axiom.
- Two non-local `noncomputable instance`s: `edgeStateFintype` and `triangleStateFintype` (= `Subtype.fintype _`).
- 69 `noncomputable` — irrelevant to soundness.
Junk values that could reach the statement: none. averageDegree's x/0 = 0 at n = 0 only falsifies the hypothesis;
Real.log is applied to d ≥ 2; indepNum's ℕ-sSup junk cannot occur for Fintype V. Internally `divergence` uses Lean's
log 0 = 0 instead of the paper's +∞, but every use carries the support hypothesis (`divergence_nonneg … mix_support`),
and in any case internal junk cannot affect a kernel-checked final statement that does not mention it.
Build configuration: lakefile.lean sets only `autoImplicit false`; its `run_cmd`/`post_update` code (the one
`unsafe env.evalConstCheck`) is Lake-configuration code that git-applies compatibility patches to 23 third-party
packages — none of them is Mathlib or Lean core (checked every `+++` path), and none is in the import closure of the
CliqueFree modules (Mathlib only). Mathlib is the official leanprover-community repo at the pinned commit.
Residual (not checkable by reading): that the replayed environment's `#print axioms` for the theorem is exactly
{propext, Classical.choice, Quot.sound} — that is the main seat's kernel replay / comparator run.

## 4. Exported max-degree version (Proposition 6.1) and the Formal Conjectures `Erdos802.erdos_802`

### 4.1 What is exported
There is NO unconditional max-degree theorem in the library. The max-degree bound is exported in CONDITIONAL form
(MaxDegree.lean, namespace OAI.CliqueFreeIndependence.WeightedGraph, universe-polymorphic `{V : Type u} [Fintype V]`):

    lemma maximum_degree_independence (k : ℕ) {B Δ : ℝ} (hB : 0 ≤ B) (hΔ : 3 ≤ Δ)
        (htri : ∀ {U : Type u} [Fintype U] (H : SimpleGraph U) (w : U → ℝ),
          IsOptimizer H w → H.CliqueFree (k+2) → triangleMass H w ≤ B * edgeMass H w)
        (G : SimpleGraph V) (hf : G.CliqueFree (k+2)) (hdeg : ∀ v, (G.degree v : ℝ) ≤ Δ) :
        (Fintype.card V : ℝ)*Real.log Δ/(4*(3+3*B/2)*Δ) ≤ (G.indepNum : ℝ)

and the hypothesis is discharged by (IndependentSet.lean)

    lemma exists_optimizer_triangle_bound (k : ℕ) :
        ∃ B : ℝ, 0 < B ∧ ∀ {V : Type u} [Fintype V] (G : SimpleGraph V) (w : V → ℝ),
          IsOptimizer G w → G.CliqueFree (k+2) → triangleMass G w ≤ B * edgeMass G w

So the paper's Proposition 6.1 (second inequality, with r = k+2, D_r = 3+3B/2, real Δ ≥ 3) is the two-line
composition (UNCOMPILED sketch — no building was allowed):

    open OAI.CliqueFreeIndependence.WeightedGraph in
    open scoped Classical in
    theorem maxDegreeBound (k : ℕ) : ∃ B : ℝ, 0 < B ∧ ∀ {V : Type} [Fintype V] (G : SimpleGraph V) {Δ : ℝ},
        3 ≤ Δ → G.CliqueFree (k+2) → (∀ v, (G.degree v : ℝ) ≤ Δ) →
        (Fintype.card V : ℝ) * Real.log Δ / (4*(3+3*B/2)*Δ) ≤ (G.indepNum : ℝ) := by
      obtain ⟨B, hB, htri⟩ := exists_optimizer_triangle_bound.{0} k
      exact ⟨B, hB, fun G hΔ hf hdeg => maximum_degree_independence k hB.le hΔ htri G hf hdeg⟩

Caveat: `G.degree v` inside MaxDegree.lean is elaborated with the file's `Classical.propDecidable` local instance; a
caller's `Fintype (G.neighborSet v)` instance may not be syntactically the same term → may need `convert`/`simp`
(degree is instance-independent). Also useful and public: `degree_cutoff_card` (|{v : deg v ≤ 2d}| ≥ n/2 given
Σ deg = n·d, d > 0), `degree_induce_le`, `indepNum_induce_le` (MaxDegree/IndependentSet).

### 4.2 Averages: FC vs OpenAI
FC's `SimpleGraph.averageDegree` is NOT in Mathlib (absent at both d13f23b and in the local Mathlib copies) — it is
FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Degrees.lean (fetched read-only from GitHub at FC commit
90d18f666e…, the commit of the local FC cache; copy in L_work/fc/Degrees.lean):

    variable {α : Type*} [Fintype α] [DecidableEq α]
    noncomputable def averageDegree (G : SimpleGraph α) [DecidableRel G.Adj] : ℚ :=
      (∑ v, (G.degree v : ℚ)) / (Fintype.card α : ℚ)

It is ℚ-valued (cast to ℝ inside `log` and the inequality in 802.lean, under `open scoped Classical`). Provably
((G.averageDegree : ℚ) : ℝ) = OAI.CliqueFreeLog.averageDegree G: push_cast + `SimpleGraph.sum_degrees_eq_twice_card_edges`
(Mathlib DegreeSum.lean:102) + instance-congruence for edgeFinset.card; both are 0 at n = 0. Equal as numbers, not
definitionally.

### 4.3 Deriving FC's `erdos_802` (∀ r, ∃ c > 0, ∀ n, ∀ G : SimpleGraph (Fin n), G.CliqueFree r →
c * (log d / d) * n ≤ G.indepNum — no d ≥ 2 hypothesis, all r)
Feasible from this library, using only public declarations (sketch, uncompiled):
- r' := max r 4; `hf.mono (le_max_left r 4)` (Mathlib `CliqueFree.mono`, Clique.lean:441) gives K_{r'}-freeness.
  So r = 0..3 need nothing extra (r = 0: CliqueFree 0 is False since ∅ is a 0-clique; r = 1: n = 0; r = 2: d = 0).
- c₁ from `logarithmic_independence_bound r' _`; B from `exists_optimizer_triangle_bound.{0} (r'-2)`, D := 3+3B/2;
  c := min c₁ (Real.log 3 / (24*D)) > 0. (The theorem's own c is hidden behind ∃, so the small-degree constant must be
  rebuilt from B; with the paper's constants c₁ = 1/(16D) would already suffice.)
- d ≥ 2: the OAI theorem (rewrite c*n*log d/d = c*(log d/d)*n).
- d ≤ 1: log d / d ≤ 0 (d = 0 gives log 0/0 = 0; 0 < d ≤ 1 gives log d ≤ 0), so LHS ≤ 0 ≤ indepNum.
- 1 < d < 2 (the "usable small-degree bound"): A := {v : deg v ≤ 2d}; |A| ≥ n/2 by `degree_cutoff_card`; every
  degree in G[A] is a natural number ≤ 2d < 4, hence ≤ 3; apply `maximum_degree_independence` with Δ := 3 to G[A]
  (K_{r'}-free via `cliqueFree_induce_iff`), then `indepNum_induce_le`: α(G) ≥ (n/2)·log 3/(4·D·3) = n log 3/(24D)
  ≥ c·n ≥ c·(log d/d)·n, since 0 ≤ log d/d < 1 for d > 1.
- The same pieces give FC's variants r_eq_three (mono to 4), aeks (log log(d+1) ≤ log d for d ≥ e−1, else LHS ≤ 0),
  shearer (shrink c by log log 3), alon (neighbourhoods (r−2)-colourable ⇒ K_r-free for r ≥ 3; r ≤ 2 ⇒ edgeless).
Practical obstacle (not mathematical): FC pins Lean v4.33.1 + Mathlib tag v4.33.1 (manifest rev 0df444a360…), OAI pins
Lean v4.34.1 + Mathlib d13f23b7. A formal bridge needs one environment: either port the 31 Mathlib-only OAI files to
FC's older pin (risk = Mathlib renames), or restate FC's 802 + its 2-line averageDegree inside the OAI environment
(faithful-statement check, but not FC's own file; a comparator run would need FC's challenge file compiled in the same
environment). FC files also use the Lean module system (`module`, `public import`, `@[expose] public section`) while the
OAI files are plain `import` files — check interop before planning a direct import.

## 5. Where the Lean takes a different route from the paper (do not say "follows the paper line by line")
5.1 Lemma 2.1. Existence: Lean maximises over the compact cube [0,1]^V and shows clamping coordinates to ≤ 1 never
    decreases F (`potential_clamp`, using t(1−log t) ≤ 1), instead of the paper's coercivity argument. Stationarity:
    Lean compares w with the single-coordinate update w_v ↦ e^{−w(N(v))} and uses log y < y−1 for y ≠ 1
    (`optimizer_stationary`), instead of first-derivative conditions. Same conclusions.
5.2 Lemma 2.2. Lean (`neighborhood_packing`) gives each removed neighbourhood probability p_i = s_i/(2s) with
    s = w(S) the TOTAL weight (paper: s_i/(2b), b = Σ s_i), keeps the R-branch (prob 1/2, multiplier 2) always (paper:
    "if no V_i were removed, take m_v = 1"), and pads the missing probability 1/2 − b/(2s) with the all-zero multiplier
    (`normalize_subprob`). Means stay 1, p_i > η/2 still holds, the bound b_{k+2}(ε) is identical, and the edge bound
    comes out as (ε/2)s² (paper: (3/4)εs²) — a slightly stronger conclusion via a different construction.
5.3 Lemma 2.3. Same test vector q. Constant bookkeeping differs: Lean bounds log(1+k·b) ≤ (5+10k+k²)x with k := r−2
    (it applies log 2 ≤ 1 ≤ x) and the disjoint-case coefficient as 8+10k+k² ≤ 4(k+2)², where the paper writes
    A_r = 4+8(r−2)+(1+r(r−2))log 2 and A_r+3 ≤ r²+6r−8 ≤ 4r². Same final C_r = 16r². Overlapping sets: Lean sums
    exactly over all 2^|V| colourings f : V → Bool (`sum_colored_cross`) — the paper's random colouring, written as an
    average.
5.4 Lemma 3.3 (peeling). Lean takes H := argmax over subgraphs H ≤ G of T_H − τM_H (`peeling`); maximality forces
    c_uv ≥ τ on every remaining edge (deleting one would raise the objective), and T_G − τM_G ≤ T_H − τM_H ≤ T_H.
    Paper: greedy deletion + telescoping. Same statement.
5.5 Lemma 3.2. `EdgeProjection` proves cross-mass, edge-mass and neighbourhood-mass preservation; T_H ≤ T_G and the
    general composition clause are not formalised — the Lean iteration never needs them (each step's projection is
    used once, in `neighborhood_reduction`, composed by hand with the peeling inclusion).
5.6 Proof of Theorem 3.1 (largest route change). Paper: from an arbitrary x₀ iterate x_{i+1} = √x_i while x_i > X,
    then bound Π(1−ε_i) ≥ 1−Σε_i and Σ1/x_i via f(t²)/f(t) = 2/√t and monotonicity of f = log t/√t on [X,∞).
    Lean: works on the fixed ladder X^{2^n} (`Numerical.scale`), picks n ≥ total weight so that every neighbourhood
    weight ≤ e^{X^{2^n}}, and proves by induction on n that T ≤ (1+e^X/3)(2−2^{−n})M (`triangle_bound_scale`) via the
    one-step `recurrence_bound` with q = 2^{−(n+1)}, ε ≤ q/4 (`lossRatio_scale`, from f(x²) ≤ f(x)/2 for x ≥ 16) and
    1/x ≤ q/2 (`inv_scale`). It never uses monotonicity of f. Final constant 2(1+e^X/3) = the paper's C_△(C), with the
    same threshold condition a_C·log X/√X ≤ 1/4 (≡ (5.4)).
5.7 §4. One kernel `LocalWalk.transition` on the oriented-edge type EdgeState G (block-diagonal by source vertex)
    replaces the family (P_u)_u; `law` on EdgeState G is μ; entropies/rows are indexed by oriented edges. Same
    objects, packaged as a single finite Markov kernel.
5.8 Lemma 5.1. Lean builds the coupling finitely: per-label threshold laws from Lebesgue measure on [0,1]
    (`exists_threshold_law`) and a recursion on the finite set of unfinished rows (`joint_of_trials`), instead of an
    infinite i.i.d. trial sequence; and it couples ALL rows of the global kernel at once rather than independently per
    centre u. Since the triangle-loss estimate is a union bound (no independence used — the paper says so), this is
    harmless. Same sharp bound 2d/(1+d).
5.9 Lemma 5.3. Copies are indexed by all oriented edges (u,y) (vertex type EdgeState G), so empty groups appear as
    isolated copies; the paper creates only nonempty groups. Hypothesis is "has an edge" (`Nonempty (EdgeState G)`)
    rather than T_H > 0.
5.10 Proposition 5.4: Lean hypothesis is "x ≥ 32 and a_C log x/√x ≤ 1" (paper: x > X(C)) — more general.
5.11 Proposition 6.1: Lean is stated for every k ≥ 0 (r = k+2 ≥ 2, paper: r ≥ 4) and takes the optimiser triangle
    bound as a hypothesis; the first inequality is phrased as ∃ independent I with F_G(q) ≤ D log Δ·|I| for all q ≥ 0.
5.12 Theorem 1.1: the Lean proof uses only r ≥ 2 (`Nat.sub_add_cancel`), so the same proof also yields the r = 3
    (Ajtai–Komlós–Szemerédi) case; the statement keeps the paper's r ≥ 4.

## 6. Objections / exposition
- EXPOSITION (repo doc, not the paper): lean/docs/184.md (= /tmp/oaimath/184/lean_doc_184.md) is headed
  "# Correspondence coloring with a fixed forbidden subgraph" — the wrong title (the body correctly describes the
  clique-free independence bound and links the right paper/comparator file). Fix: retitle "A logarithmic independence
  bound for clique-free graphs".
- EXPOSITION (formal statement): `{V : Type}` restricts to universe 0. Harmless (finite graphs ↔ Fin n) and the library
  is polymorphic; worth one sentence if the entry says "formalised verbatim".
- No FATAL and no GAP found on the Lean side: the final statement is Theorem 1.1, the import closure is Mathlib-only,
  and there is no construct that could make a successful kernel replay weaker than it looks. The only remaining
  trust items are external to the source: (i) the replay's `#print axioms` = {propext, Classical.choice, Quot.sound},
  (ii) the replayed statement is the challenge statement (comparator, or a `#check`-level type equality).
