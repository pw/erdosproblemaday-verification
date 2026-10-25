# Seat F — formalization and statement (Erdős #505, OpenAI "A nine-dimensional counterexample to Borsuk's covering assertion")

**VERDICT: HOLDS AS READ.** The comparator statement is a faithful formalization of Theorem 1.1 (p.2). The ℝ⁹ form (`euclidean_nine_counterexample`) is an honest instance of the negative answer to Erdős #505 for n = 9, after a trivial rescaling. I found no hidden hypothesis, `Fact`, `class`, axiom or vacuous definition.

**COULD NOT CHECK** the kernel replay itself. That is the main seat's job, and I built nothing.

**SCOPE WARNING for the page.** The kernel-checked proof does not follow the paper's route at several points:
- the degree input to Prop 4.1;
- Lemma 4.2;
- both halves of Theorem 4.3;
- all of Lemmas 6.2–6.4 and Theorem 6.5.

So a successful replay certifies **Theorem 1.1**. It does **not** certify these printed arguments:
- Lemma 3.1(2)–(3);
- the smoothness claims of Lemma 3.2;
- the F₂-cycle/"positive even" claim of Theorem 4.3;
- Lemma 4.2;
- the Stiefel–Whitney argument;
- Lemma 5.3;
- Lemmas 6.2–6.4 and Theorem 6.5 as written;
- Corollary 7.1.

Section 2 below says exactly what was checked instead.

Method: I read the source only, with no build. I diffed the challenge against the definitions, read every file on the main chain, and used grep for hidden assumptions. I ran three small python checks (`seats/seatF_scripts/`).

---

## 1. Statement faithfulness

### 1a. The challenge vs the solution (same names, same definitions)
- `diff ComparatorChallenges/BorsukNine.lean OAI/Geometry/Borsuk/Model.lean`: the only difference is the `main_theorem … := by sorry` block (lines 25–31 of the challenge). The definitions `Vector4`, `Matrix4`, `projector`, `projectorSet`, `traceOneSymmetric` and `HasTenSmallCover` are byte-identical, in the same namespace `OAI.BorsukNine`.
- `Counterexample.lean` `main_theorem` has the literal challenge statement, also in namespace `OAI.BorsukNine`:
  `IsCompact projectorSet ∧ projectorSet ⊆ traceOneSymmetric ∧ Metric.diam projectorSet = Real.sqrt 2 ∧ ¬ HasTenSmallCover`.
- `BorsukNine.json`: `theorem_names = [OAI.BorsukNine.main_theorem]`, `definition_names = []` (so all challenge definitions must match exactly), permitted axioms `propext, Quot.sound, Classical.choice`.
- Every one of the 269 modules imports only `Mathlib` plus `OAI.Geometry.Borsuk.*`. The lakefile's `patches/` touch third-party dependencies (iut, carleson, …), **not Mathlib**, so `Metric.diam`, `EuclideanSpace` and friends are the stock Mathlib definitions.

### 1b. Against the paper's Theorem 1.1 (p.2)
Quote: *"The compact set X = {uuᵀ : u ∈ R⁴, ∥u∥ = 1} ⊂ {A ∈ Sym4(R) : tr A = 1}, with the Frobenius metric, has diameter √2 and cannot be covered by ten subsets of diameter strictly less than √2."*

- `projector u = toLp 2 (fun ij => u i * u j)` lives in `EuclideanSpace ℝ (Fin 4 × Fin 4)`. Its L² norm over the 16 entries is the Frobenius norm. `projectorSet` is the image of the unit sphere, so it is exactly X. The semantics are pinned by proved lemmas: `projector_dist_sq` is (2.1), `‖Pu − Pv‖² = 2 − 2⟨u,v⟩²`, and `diam_projectorSet = √2`. A misread coercion would make these unprovable.
- `traceOneSymmetric` means symmetric with trace 1. The containment is part of the statement.
- `HasTenSmallCover` is `∃ C : Fin 10 → Set Matrix4` with `C i ⊆ projectorSet`, a union covering `projectorSet`, and `Metric.diam (C i) < √2`. That is arbitrary subsets, a cover, and a strict inequality.

### 1c. Against Erdős #505 (live page): *"Is every set of diameter 1 in ℝⁿ the union of at most n+1 sets of diameter <1?"*
Lean pitfalls, each checked:

| Pitfall | Status |
|---|---|
| `Metric.diam` of an unbounded set is the junk value 0 | Harmless. `C i ⊆ projectorSet`, which is compact and hence bounded, so every `diam (C i)` is the true supremum. The clause is in fact **necessary**: without it `C 0 = univ` would have `Metric.diam = 0` and the statement would be false. |
| `Metric.diam ∅ = 0` | Allows empty pieces, i.e. "**at most** 10". Faithful. |
| `diam projectorSet = √2` could be junk | No. It is proved via a matching upper bound and an attained pair (`EuclideanSpace.single 0 1`, `single 1 1`), and `IsCompact` is asserted separately. |
| Covers vs partitions | ¬cover implies ¬partition, so the cover form is the stronger negative statement. Erdős's "union of sets" means sets that cover. |
| Pieces arbitrary? | Yes: `Fin 10 → Set Matrix4`, with no measurability or closedness. |
| Strict `<` | Yes, and it matches "diameter < 1". |
| Diameter √2 vs 1 | Scaling by 1/√2 maps it to diameter 1 with pieces of diameter < 1. This is not formalized, but it is trivial (EXPOSITION). |
| Ambient dimension | The **comparator** statement lives in ℝ¹⁶ = `EuclideanSpace ℝ (Fin 4 × Fin 4)` and only asserts `⊆ traceOneSymmetric`. That the trace-one symmetric slice is a 9-dimensional Euclidean space is not part of the checked statement; see 1d. |

### 1d. `Main.lean` `euclidean_nine_counterexample` (the ℝ⁹ form)
Statement:

`∃ X : Set (EuclideanSpace ℝ (Fin 9)), IsCompact X ∧ Metric.diam X = √2 ∧ ¬∃ C : Fin 10 → Set _, (∀ i, C i ⊆ X) ∧ X ⊆ ⋃ C i ∧ ∀ i, diam (C i) < √2`.

This is precisely Borsuk/#505 for n = 9 with d + 1 = 10 pieces, at diameter √2.

How the proof works:
- `X = coordinates9 '' projectorSet`. `coordinates9` is exactly the paper's map (2.2) (Remark 2.2, p.4), with the same nine coordinates in 0-indexed form.
- `coordinates9_norm_sq` shows `‖coordinates9 A‖² = ‖A‖²` for symmetric trace-0 A. I re-verified this identity symbolically: `seatF_scripts/checks.py` prints `True`.
- `coordinates9_dist` / `coordinates9_isometry` apply it to A − B with A, B trace-one symmetric.
- `coordinates9_diam` transports the diameter. `coordinates9_cover_pullback` pulls a ten-piece cover of the image back to a cover of `projectorSet` with the same diameters, using `C i ⊆ image`. Compactness follows from continuity.

Honest. **Caveat (EXPOSITION):** this theorem is **not** in the comparator's `theorem_names`, so the comparator does not certify its statement. It is kernel-checked only by a replay of `OAI.Geometry.Borsuk.Main`; the main seat's plan already includes `#print axioms` on it. I read the statement above and it is the intended one.

**Context for the page:** #505 was already answered "no" by Kahn–Kalai (n > 2014). This result is a dimension record (9, against the 64 the page cites and the 63 the paper cites from Grinsztajn's note), not a new resolution of the problem. Corollary 7.1 (all d ≥ 9, p.17) is **not formalized**.

---

## 2. Architecture map: paper item → Lean, and whether the route matches

All paths are relative to `OAI/Geometry/Borsuk/`.

| Paper (printed) | Lean | Route |
|---|---|---|
| Lemma 2.1 (p.3–4) | `Projectors/Basic.lean`: `projector_inner`, `projector_dist_sq`, `projector_dist_eq_sqrt_two_iff`, `diam_projectorSet`, `isCompact_projectorSet`, `projectorSet_subset_traceOneSymmetric` | Same computation. The homeomorphism P(V) ≅ X_k is never formalized and is not needed (see Def 2.3). |
| Remark 2.2 (p.4) | `Main.lean` `coordinates9*` | Same map. |
| Def 2.3 (p.4) | `Projectors/Basic.lean` `structure Admissible` | Re-encoded on the sphere: f : V → ι → ℝ, `ContDiff ℝ ∞` on all of V, `f (−u) = f u` for all u, nonnegative with sum 1 on ‖u‖ = 1, disjoint positive labels for orthonormal u, v. A smooth function on P(V) is an even smooth function on S^{k−1}. Smoothness on all of V is a stronger demand, but the construction meets it (§4). |
| Lemma 2.4 (p.4–5) | `cover_to_admissible` | Same route: ε = (√2 − diam)/4 neighbourhoods plus a smooth partition of unity. The Lean thickens in the ambient ℝ¹⁶ (`Metric.thickening`) and uses `SmoothPartitionOfUnity` on `Matrix4`, then composes with `projector`; the paper works relatively on X_k and pulls back to P(V). **Extra, not in the paper:** `admissible_to_cover` and `cover_iff_admissible` prove HasTenSmallCover ⇔ ∃ admissible f with 10 labels, so the reduction loses nothing. |
| Support complex (p.5) | `SupportFace` (`Support/SupportIncidence.lean`), `positiveSupport`, `supportComplex` (`Simplicial/Supports.lean`) | Same. |
| Lemma 3.1 (p.5–6) | E_V = `positiveExtension f Q = integralLift f (op (sqrt Q))`, with `integralLift = card ν · ∫ homogeneousLift f (T x) d(sphereProbability)` (`SphereGeometry/IntegralLift.lean`, `HomogeneousLift.lean`, `SphereMeasure.lean`, `MatrixGeometry/MatrixKernel.lean`). Proved: continuity, nonnegativity, sum = tr Q, homogeneity (`positiveExtension_smul_nonneg`), support (3.2) (`positiveExtension_support`), item 1 (`positiveExtension_rankOne`). | Same integral formula (3.1). **Items 2 (subspace identity) and 3 (smoothness) are not formalized.** The Lean never restricts the construction to x^⊥ (the fibre map G_x is just F on matrices killing x) and never differentiates E_V. |
| Lemma 3.2 (p.6–7) | `signedExtension f A = positiveExtension f A⁺ − positiveExtension f A⁻` (`MatrixGeometry/SignedExtension.lean`): `_odd`, `_sum`, `_abs_sum`, `_continuousOn`; (3.5) via `signedExtension_positive_support` / `_range_labels`; nonsingularity via `Support/FullSupport.lean` (`signedExtension_fullSupport`, `_negativeDefinite`); (3.6) via `sphereExtension` / `normalizedSignedExtension` (Euclidean normalization; `traceSphere`/`traceRadial` for the trace-norm sphere) | Same map (3.3). **Smoothness of F is not formalized and not used.** |
| Prop 4.1 (p.8) | `Admissible.label_bound` (m ≥ N_k) and `sphereExtension_surjective` / `signedExtension_ray` (`Simplicial/OddSphereDimensionBoundFintype.lean`); edge assertion `Admissible.all_pairs` (`Support/AllPairs.lean`) | **Different degree input.** The paper cites Hatcher 2B.6/2B.7 and mod-2 degree. Lean proves Borsuk–Ulam itself, combinatorially: `odd_sphere_dimension_bound` → `annular_odd_dimension_bound` (`Simplicial/FineCrossMap.lean`) → `cross_chain_dimension_bound` (`Simplicial/CrossChainDimensionBound.lean`). The boundary of the cross-polytope with its antipodal flip is iteratively barycentrically refined (mesh ((n−1)/n)^r·2). The map is approximated by a Tucker-style label map `sphereLabel` (`MaxIndex.lean`). The result is an F₂ chain map commuting with ∂, augmentation and the norm map x ↦ x + τx; an antipodal "tower" (`antipodal_tower_augmentation_zero`, `SmithTheory/`) forbids n > m. Surjectivity comes from Borsuk–Ulam with one less dimension (reflect, drop a coordinate), not from degree. **Edge assertion: also a different route.** The paper says the positive spectral subspace must be 1-dimensional (by N₂ = 3). Lean takes A with F(A) on the ray of (+1 at i, j; −1 elsewhere) and runs an intermediate-value path inside ran A⁺, where only labels i, j occur (`two_labels_meet`, `Projectors/TenPure.lean`). |
| Lemma 4.2 (p.8) | Replaced by `odd_homotopy_local_models` (`MatrixGeometry/FinitePositiveBound.lean`), built from `additive_approximation_coeff` (`Simplicial/CompactAdditiveLocality.lean`), `normalized_homotopy_chains` and `eventually_odd_sphere_degree` (`Simplicial/EventuallyFineSphereLabel.lean`), `characteristicDegree` / `cross_equivariant_degree_one` (`Simplicial/CharacteristicDegree.lean`). Wrappers: `trace_odd_local_models`, `trace_patch_models`, `sphere_null_patch_models`. | **Different.** There is no singular homology, excision or inverse-function-theorem count. "Degree" is the coefficient of one cross-polytope facet in the simplicial approximation of the fundamental chain. The **characteristic degree** is a Smith-theory cochain tower: φ₀ = augmentation, φ_{i+1} = lift(φ_i)∘∂ through the norm map, a combinatorial stand-in for w₁^i. Odd maps have characteristic degree 1, and degree is homotopy-invariant and locally additive. The local degree at a preimage is computed by an **odd global model map** that agrees with F near that preimage and hits the ray only there, so its degree is 1 because it is odd. No orientation or derivative-degree theory is needed. |
| Theorem 4.3 (p.9–11), "s ≤ k", (4.1) | `Admissible.support_card_four_le` / `support_card_three_le` (`Projectors/Restrict.lean`): restrict to x^⊥ by `comp_isometry` + `restrict_labels`, then `label_bound` | Same route as (4.1). |
| Theorem 4.3, "s ≥ k" (Sard on f_I; sphere bundle M ≅ L × S^{h−1}; (4.7); Stiefel–Whitney (4.8)) | `Admissible.maximal_support_complement_bound` (`Support/Purity.lean`) via `chart_surgery_impossible` (`Projectors/ChartSurgery.lean`), `compact_disjoint_chambers` (`Support/DisjointChambers.lean`), `finite_center_approximations` (`MatrixGeometry/CenterApproximation.lean`), `finite_smooth_slice_misses_general` (`Projectors/FiniteSmoothSliceMisses*.lean`, `NullImage.lean`), `compact_local_homotopy`, `Admissible.traceHomotopy_ray` (`MatrixGeometry/TraceHomotopy.lean`) | **Different, and it uses no Sard on f_I, no regular level set L and no Stiefel–Whitney classes.** Suppose a = \|J\| > h = N_{k−1}. Take the level set {u : f u = f w, ⟨w,u⟩ ≥ 0}; it is compact, and r = f w itself is used, not a regular value. Cover it by finitely many disjoint open "sign chambers": regions where the active vectors keep their signs, a local version of the paper's affine chart. In chamber j, approximate the fibre map Q ↦ (J-coordinates of E(Q)) on c_j^⊥ by a smooth g_j; this map runs from an (h−1)-dimensional trace slice into the (a−1)-dimensional simplex. Because h − 1 < a − 1, a common missed point z exists by "mini-Sard": a smooth image of lower dimension is Lebesgue-null, derived from Mathlib's `addHaar_image_eq_zero_of_det_fderivWithin_eq_zero` composed with a projection. Then homotope F, inside the union of charts, to a map missing the ray through (½r, ½z), keep every intermediate ray-hit in a compact set, and extend globally (`compact_local_homotopy`). This contradicts `traceHomotopy_ray`: anything homotopic to F through nonvanishing maps hits every ray. |
| Theorem 4.3, purity consequences | `maximal_support_card_four` / `_three`, `support_extends_four` / `_three` (`Support/Purity.lean`); `face_extends_four` (`Projectors/TenPure.lean`); `face_extends_three` (`Support/SupportIncidence.lean`) | Same consequence. |
| Theorem 4.3, "Σ facets is a simplicial cycle over F₂ … positive even number of facets" | **Not formalized.** Replaced by `Admissible.no_free_ridge` (`LocalParity/NoFreeRidge.lean`): every (k−1)-subset of a facet lies in a **second** facet (≥ 2). | **Different and weaker, but sufficient** (see §3). Proof: `exists_regular_facet_point` (`LocalParity/RegularBase.lean`) takes a regular value of the **equidimensional** k → k base-coordinate map in a hemisphere chart (`LocalParity/Sard.lean`: equidimensional Sard straight from Mathlib, plus `compact_regular_level_finite` via the inverse function theorem). `regular_facet_level_odd` (`LocalParity/MatrixParity.lean`) shows \|L\| is odd: this is the paper's (4.7)/(4.9), via local block models `localBlockModel` (linearized base part plus the exact signed extension on the fibre) and `trace_patch_models`. `regular_facet_level_even` (`LocalParity/SphereParity.lean`) shows that if the ridge I∖{a₀} were in no other facet, then \|L\| is even, because the sphere map u ↦ (⟨w,u⟩, tail(f u) − z) is homotopic to one that misses the ray. Odd = even gives the contradiction. |
| Def 5.1 (p.12) | No standalone structure; encoded as `TenSystem.complementary` + `pair_count`, and `SixCounting` (`Support/AllPairs.lean`) | — |
| Lemma 5.2 (p.12) | `six_complement_exclusion`, `six_pair_lower`, `six_complementary`, `six_pair_degree`, `six_pair_count` (`Support/SixFaces.lean`) + `SixCounting.triangle_count_upper` / `_eq_ten` / `pair_degree_eq_two` / `complementary_iff` | **Same counting route** (at most 10 by complementary exclusion, at least 10 by ≥ 2 per edge). The inputs are `all_pairs`, `face_extends_three`, and `triangle_no_free_edge` (= `no_free_ridge` with k = 2). |
| Lemma 5.3 (p.12) | Not formalized as such; absorbed into FiniteCases | — |
| Lemma 6.1 (p.13) | `facet_complement_exclusion`, `facet_six_properties`, `restricted_face_image` (`Projectors/Within.lean`) | **Same route.** Restrict to x^⊥ ≅ ℝ³ (`orthogonal_isometry 3`); labels in S vanish there; apply Lemma 5.2. "No additional triangles" uses three witnesses plus a line orthogonal to all three (`exists_label_absent_dim`, n = 3 < 4). The "two tetrahedra cannot be disjoint" corollary is not stated separately. |
| Lemmas 6.2–6.4, Theorem 6.5 (p.13–16) | `TenLabels/Labels.lean` (`TenSystem`, `relabel`, `three_pos`/`three_neg`) + `FiniteCases/Cases001–145.lean`, ending in `no_fixed_ten_system` / `no_ten_system` (Cases145.lean) | **Entirely different.** It is a machine-generated refutation tree: **4,093** case lemmas in **66,297** lines with 13,170 `decide` lines. After WLOG S = {0,1,2,3} (`relabel`), it splits on membership of explicit triples (T) and quadruples (Q) and closes branches with `h.complementary` (997 uses), `three_neg`/`three_pos` (1,022 / 554 uses, wrapping `pair_count`), `h.down` (396), `h.no_boundary` (284) and `h.pure` (97). In effect it is a SAT certificate over the ≤ 330 Boolean variables (120 triples + 210 quadruples), replayed lemma by lemma. It says nothing about whether the paper's blocks/edge-link argument is correct; it certifies the same **conclusion** from the same inputs (§3). |
| Proof of Theorem 1.1 (p.16) | `Counterexample.lean`: `main_theorem`, `no_admissible_ten`, `Admissible.support_ten_system` | Same assembly. |
| Corollary 7.1 (p.17) | **Not formalized.** | — |

**Answer to "Sard used or avoided?"** The paper's two Sard uses (p.9: regular value r of f_I : U_I → Δ̊_I, with dimension k−1 → s−1; p.10: regular value g of G) are both **avoided**.
- The purity step needs no regular value at all. It uses only the null-image ("mini-Sard") fact to choose z.
- The facet-coefficient step needs Sard only in the **equidimensional** case, which Mathlib already has. The point counted is a regular value of base coordinates ℝᵏ → ℝᵏ.
- No Stiefel–Whitney classes, singular homology, or `RP^n` cohomology appear. The degree theory is a self-contained combinatorial F₂/Smith-theory development on a refined cross-polytope sphere, about 4.2k lines in `Simplicial/` and `SmithTheory/`.

---

## 3. The finite hypotheses (`TenSystem`) vs the paper's Section 6

`TenSystem T Q` with T = 3-element support faces and Q = 4-element support faces (`Counterexample.lean`):

| Field | Meaning | Paper source | Established in Lean by | Rests on |
|---|---|---|---|---|
| `tetra_card` | Q S → \|S\| = 4 | (definition) | By definition of Q | — |
| `down` | 3-subsets of a tetrahedron are triangles | K is a complex | `SupportFace.mono` | — |
| `pure` | every triangle lies in some tetrahedron | Thm 4.3 "every facet has k vertices" | `face_extends_four` ← `support_extends_four` ← `maximal_support_card_four` | `support_card_four_le` (label_bound on x^⊥) + `maximal_support_complement_bound` (chart surgery + `traceHomotopy_ray`) |
| `no_boundary` | each triangle of a tetrahedron lies in a **second** tetrahedron (**≥ 2**) | Thm 4.3 "positive even number" | `tetra_no_free_triangle` ← `no_free_ridge` (k = 3) | `regular_facet_level_odd` vs `_even`, equidimensional Sard |
| `complementary` | for a tetrahedron S and U ⊆ Sᶜ with \|U\| = 3: T U ↔ ¬T(Sᶜ∖U) | Lemma 6.1 + Def 5.1(1) | `facet_six_properties.1` | `six_complementary` on x^⊥, `facet_complement_exclusion` |
| `pair_count` | for P ⊆ Sᶜ with \|P\| = 2, exactly two w ∈ Sᶜ∖P make P∪{w} a triangle | Lemma 6.1 + Def 5.1(2) | `facet_six_properties.2` | `six_pair_count` ← `six_pair_lower` (`all_pairs`, `face_extends_three`, `triangle_no_free_edge`) + `SixCounting` |

`no_ten_system` additionally needs ∃ S, Q S. This comes from `face_extends_four` applied to `SupportFace f ∅`, witnessed by `single 0 1`. (With Q = ∅ the system is trivially satisfiable, so this hypothesis does real work.)

**Correspondence.** I went through every step of Section 6 and listed what it consumes:
- Lemma 6.1 uses purity, Def 5.1(1)–(2) and down.
- Lemma 6.2 uses Lemma 5.3(3)–(4) and "positive even" ⇒ ≥ 2.
- Lemma 6.3 uses Lemmas 6.2 and 5.3(3).
- Lemma 6.4 uses Lemmas 6.2, 6.3 and 6.1.
- Theorem 6.5 uses Lemma 6.4, purity, Lemma 5.3(2) and Lemma 6.2.
- Lemma 5.3 is pure combinatorics from Def 5.1.

So the six fields are **exactly** the inputs the paper's Section 6 uses, with "positive even" weakened to "≥ 2". The Lean's finite theorem is therefore the paper's Section 6 conclusion from (marginally) weaker hypotheses.

**EXPOSITION (paper, Theorem 4.3, p.9):**
- Objected sentence: *"is a simplicial cycle over F₂. Consequently every (k − 2)-dimensional face lies in a positive even number of facets."*
- Evenness is never used downstream except to get "≥ 2" from positivity:
  - Lemma 5.2 (p.12): *"each edge belongs to a positive even number of triangles … at least 2·15/3 = 10 triangles"*.
  - Lemma 6.2 (p.14): *"Positive even multiplicity gives exactly two."*, combined with "at most two".
- The Lean proves only "≥ 2" (`no_free_ridge`) and the theorem still closes.
- Consequence for the page: **the F₂-cycle claim and its proof (the "coefficients of the facet cycle" paragraph, p.11, relying on Lemma 4.2) are not load-bearing and are not kernel-checked.** If another seat finds a problem there, Theorem 1.1 is unaffected; the kernel route bypasses it.
- Not an error; at most a remark that the paper proves more than it uses.

Note: `no_boundary` asks only ≥ 2. "At most 2" is derived inside the machine case analysis (the paper's Lemma 6.2, first half), never assumed.

---

## 4. Hidden assumptions and vacuity

- **grep** over all 269 files finds:
  - no `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `opaque` or `unsafe`;
  - no `class` and no `Fact` hypothesis anywhere (the two `let : Fact (finrank … = k+1) := ⟨by simp⟩` are proved locally);
  - only three `instance`s, all proved (`SphereGeometry/SphereMeasure.lean`: NeZero / IsProbabilityMeasure / IsOpenPosMeasure for the normalized sphere measure);
  - only `local instance Classical.propDecidable`.

  The only propositional structures are `Admissible` and `TenSystem`. `TenSystem` appears only as the hypothesis of the finite lemma and is instantiated (proved) by `support_ten_system`.
- **`Admissible` is not vacuous for an irrelevant reason.**
  - `cover_iff_admissible` (Projectors/Basic.lean) proves `HasTenSmallCover ↔ ∃ f : Vector4 → Fin 10 → ℝ, Admissible f`. Unsatisfiability of `Admissible` at 10 labels **is** the theorem, not an artifact of the definition.
  - **With more labels it is satisfiable.** Take Voronoi cells of a line configuration with angular covering radius ρ < 45°. Two lines in one cell are at angle ≤ 2ρ < 90°, so each cell's projector image is compact with diameter < √2. Lemma 2.4's construction, which is generic in the index type, then gives an admissible map.

  `seatF_scripts/checks.py` (sampled covering radii, i.e. lower bounds):

  | k | Configuration | Lines | Covering radius | Admissible? |
  |---|---|---|---|---|
  | 2 | 3 lines | 3 | 30° | Yes: (k, m) = (2, 3) = (k, N_k), so `label_bound` is sharp |
  | 3 | 6 icosahedral lines | 6 | ≈ 37.33° | Yes: (3, 6) = (3, N₃), sharp |
  | 4 | 24-cell alone | 12 | 45° (boundary case, fails) | No |
  | 4 | 24-cell ∪ dual | 24 | ≈ 31.3° | Yes: m = 24 on ℝ⁴ |

  For k = 3, `seatF_scripts/hemi.py` confirms the induced 10 triangles (the hemi-icosahedron) satisfy Def 5.1(1) and (2). Lemma 5.2 therefore applies to real objects.
- **`smooth : ∀ i, ContDiff ℝ ∞ (fun u => f u i)` on all of V, including u = 0.**
  - This is consistent with `cover_to_admissible`: f u i = ρ i (projector u), where ρ is a `SmoothPartitionOfUnity` on all of `Matrix4` (sum = 1 only on the closed set `projectorSet`) and `projector` is a polynomial.
  - Both factors are smooth everywhere. `contMDiff_iff_contDiff` converts the C^∞ partition functions, and with `open scoped ContDiff` `∞` means (⊤ : ℕ∞), i.e. C^∞, not analytic.
  - Evenness holds because `projector (−u) = projector u`.
  - Nonnegativity and sum = 1 are only required on the sphere; f(0) = ρ(0) is irrelevant. Values off the sphere enter only through `homogeneousLift f v = ‖v‖² f(v/‖v‖)`.
  - Positivity f u i > 0 ⇒ `projector u ∈ tsupport (ρ i) ⊆ U i`. Two points of a thickening of radius (√2 − d)/4 are at distance < (√2 + d)/2 < √2 (`dist_lt_of_mem_thickening_small`), so orthogonal unit vectors cannot share a label.
  - This is a genuine admissible map from an **arbitrary** cover, exactly as in Lemma 2.4.

---

## Objections (quote → what → class)

1. Theorem 1.1 / p.2, *"Thus Borsuk's assertion fails in dimension nine."*
   - The comparator-certified statement is set in ℝ¹⁶ with `⊆ traceOneSymmetric`. The ℝ⁹ statement (`euclidean_nine_counterexample`) is proved in the solution module but **not** listed in `theorem_names`, and the √2 → 1 rescaling for #505 is not formalized.
   - **EXPOSITION.** Both bridges are honest and trivial. The page should say "kernel-checked in ℝ⁹ via `euclidean_nine_counterexample`" only once the main seat's replay of `Main.lean` passes.
2. Theorem 4.3, p.9, *"is a simplicial cycle over F₂. Consequently every (k − 2)-dimensional face lies in a positive even number of facets."*
   - Stronger than anything later used (only ≥ 2 is consumed). It is not formalized; Lean proves `no_free_ridge` instead.
   - **EXPOSITION**, non-load-bearing.
3. Lemma 3.1, p.5–6, items 2–3, and Lemma 3.2, p.6, *"The map F is smooth on the open set of nonsingular symmetric operators."*
   - Not formalized and not needed by the kernel route.
   - The paper's own Theorem 4.3 proof does use them. I checked the item-2 measure identity by hand: it is the standard O(W)-invariance argument with mass r/k and is correct.
   - Whether these steps are rigorous as printed is for the topology seat.
   - **Scope note**, not an objection.
4. Section 6, p.13–16.
   - The kernel checks a machine refutation of `TenSystem`, not the printed Lemmas 6.2–6.4 / Theorem 6.5.
   - **Scope note.** Correctness of the printed combinatorial argument must come from the combinatorics seat, not from "Lean checked it".
5. Corollary 7.1, p.17.
   - Not formalized.
   - **Scope note.** The short Gram-matrix proof should be refereed by hand.

No FATAL or GAP findings in my remit.

Files: report `/tmp/oaimath/156/seats/seatF_formal.md`; scripts `/tmp/oaimath/156/seats/seatF_scripts/checks.py`, `hemi.py`.
