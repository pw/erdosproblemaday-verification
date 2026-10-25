# Seat L — Lean vs paper (Erdős #174, OpenAI "A classification of finite Euclidean Ramsey configurations")

Read-only seat. I did not compile anything; the kernel replay belongs to the coordinator. Everything below comes from reading
`/tmp/oaimath/024/repo/lean/{ComparatorChallenges,OAI/Combinatorics/EuclideanRamsey,OAI/Combinatorics/SphericalRamsey}`,
the paper source `/tmp/oaimath/172/src/build/sections/*.tex` (cited by printed numbers), and the live #174 page text.
One symbolic check was run (sympy, capped): `/tmp/oaimath/172/seats/L_scratch/check12.py`.

Bottom line: all seven comparator statements say what the paper says, and none is weaker than the paper or Erdős in a way
that matters. The source tree has no `sorry`, axiom, `native_decide`, extern, unsafe or notation tricks, and no instance on any
type that appears in a statement. The Lean proves Theorem 1.1 by the paper's route, stage by stage. Four sub-lemmas use
different internal proofs, so the paper's own proofs of those lemmas are not what the kernel checks. The twelve-point
development does not use the classification at all: it proves a stronger, direct 50-colour result.

---

## 1. Statement faithfulness (7 comparator files)

### Shared definitions (identical in all seven comparators and in `EuclideanRamsey/Model.lean`; diffed)
- `Congruent a b := ∀ i j, dist (b i) (b j) = dist (a i) (a j)` checks distances only. **Injectivity of the copy is forced**
  whenever `a` is injective: for i ≠ j, `dist (b i) (b j) = dist (a i) (a j) > 0`. Every comparator theorem either assumes
  `Function.Injective a` (classification, Circle, Quadratic, Spherical, Transitive) or proves it (Nine). Under injectivity
  the labelled tuple b is an isometric image of A. Copies extend to affine isometries: `Congruence.congruent_linearIsometry`,
  the polarization step of Prop 2.4. So "congruent copy at scale one" is captured exactly.
- `Ramsey a := ∀ r ≥ 2, ∃ D ≥ 1, ∀ c : Space D → Fin r, ∃ b, Congruent a b ∧ ∃ k, ∀ i, c (b i) = k` has arbitrary
  functions as colourings (no measurability). This matches §1, paragraph 1 of the paper word for word.
  - **vs Erdős** ("for any k ≥ 1 there is d = d(A,k) such that any k-colouring of ℝ^d has a monochromatic copy"):
    - k = 1 is implied by k = 2: compose a 1-colouring with `Fin 1 ↪ Fin 2`.
    - Requiring D ≥ 1 loses nothing. d = 0 can only work when A is a singleton, and singletons are Lean-Ramsey
      (`Congruence.singleton_ramsey`).
    - The two definitions are therefore **equivalent**. EGMRSS's "copy" means a congruent copy. No weakening.
- `coordinateField a := IntermediateField.adjoin ℚ (range of all coordinates)`, so the paper's F = ℚ((a_i)_α) as a subfield
  of ℝ. Its type coercion `Coeff a` carries the standard ℚ-algebra structure.
  - `TensorRing a := Coeff a ⊗[ℚ] Coeff a` is the paper's B = F ⊗_ℚ F.
  - `multiply := Algebra.TensorProduct.lmul' ℚ` is m_F (x⊗y ↦ xy).
  - `augmented a i : Option (Fin d) → F`, with `none ↦ 1` and `some j ↦ (a_i)_j`, is p_i = (1, a_i), index 0 = `none`.
  - All correct.

### (a) `EuclideanRamsey.lean` — `classification` ↔ Theorem 1.1
- Hypotheses `2 ≤ s`, `Function.Injective a` and `affineSpan ℝ (range a) = ⊤` are the paper's "at least two points with
  affine span ℝ^d", with sets represented as injective tuples.
  - `1 ≤ d` is redundant (two distinct points span at least a line) and harmless.
- `FieldCriterion` condition (1) is `∀ i, Σ_α Σ_β (aug_iα ⊗ 1) · P_αβ · (1 ⊗ aug_iβ) = 0`. This is the componentwise
  expansion of (p_i⊗1)^T P (1⊗p_i), summed over all of `Option (Fin d)`, constant index included.
- Condition (2), `∀ α β : Fin d, m(P (some α) (some β)) = δ_αβ`, applies to the **spatial block only**. As in the paper,
  there is no condition on the constant row or column.
- **Faithful.** Neither side is degenerate:
  - The same module tree proves Ramsey instances (Circle, Transitive).
  - It also proves non-Ramsey instances (Nine), so `Ramsey ↔ FieldCriterion` cannot be "trivial ↔ trivial".
  - B is a nonzero ring, and m_F is surjective.
- Main.lean also has a statement that is **not comparator-checked**: `classification_nonempty`, covering any nonempty
  injective configuration in any ambient dimension via a full-span representative. It is the "choose a congruent
  representative" sentence of §1.1, made formal.

### (b) `GrahamSpherical.lean` — `full_main` ↔ Prop 7.7
- **Parameter.** `parameter = ∑' m:ℕ, 1/10^((m+1)!)` equals Σ_{k≥1} 10^{-k!}. This is the paper's t: the (m+1)! indexed
  from m = 0 is the paper's m! indexed from m = 1, and the first partial sums agree exactly (checked).
  - Mathlib's `liouvilleNumber 10` includes the i = 0 term 10^{-0!} = 1/10.
  - Lean proves `parameter = liouvilleNumber 10 − 1/10`, transcendence via Mathlib's Liouville theorem, and
    `0.11 < parameter < 0.12` (Parameter.lean).
  - So the `tsum` is not its junk value 0. Independently, `ncard = 12` would fail at 0, because then u = 1, v = 0 and the
    three squares coincide, giving 4 points.
- **Points.** u, v and `squareCoordinate` (Q_0 = {(1,0), (−1,0), (0,1), (0,−1)}) are literally as in the paper.
  - Label (0,q) gives (u q0 − v q1, v q0 + u q1) = R_+ q.
  - Label (1,q) gives (u q0 + v q1, −v q0 + u q1) = R_− q.
  - Label (2,q) gives q.
- **Literal match with Prop 7.7.**
  - `witness.ncard = 12` and `witness ⊆ Metric.sphere 0 1` (L2) say "X is a twelve-point subset of the unit circle".
  - `¬ EuclideanRamsey witness` says "not Ramsey".
- **This file's own Ramsey definition** is set-based: `0 < r`, `∃ n > 0`, copies are `f : X → Point n` with `Isometry f`
  on the subtype. For a 12-point X, isometric maps from X are exactly congruent labelled tuples.
  - The r = 1 clause holds for every n ≥ 2, so including r = 1 neither weakens nor trivialises the definition.
  - Hence `¬EuclideanRamsey witness ⇔ ¬Ramsey (vertex)` in the other namespace.
  - It is **not vacuous**. The negation cannot be witnessed cheaply: n = 1 is free (no copy exists in ℝ¹), but the
    statement needs every n > 0, including n ≥ 2 where copies exist.
- **Extra conjunct.** `∀ n > 0, ∃ color : Point n → Fin 50, AvoidsCopy witness color` is **stronger than the paper**, which
  claims no colour count. The paper's route (Prop 2.4) would give (2s+1)^s = 25^12.

### (c) `EuclideanRamseyCircle.lean` ↔ Cor 7.4
- `a : Fin s → Space 2`, `0 < s ≤ 5`, injective, `∃ c r, ∀ i, dist (a i) c = r` implies `Ramsey a`. Faithful.
- **EXPOSITION:** the statement is planar only. The paper's "points on a circle" may sit in any ℝ^n. The general case follows
  in one line from `ramsey_congruent_iff`, since a circle lies in a 2-plane, but that step is not a comparator statement.
- Degenerate cases (r = 0, s = 1) are handled (`zero_radius_ramsey`, `singleton_ramsey`).

### (d) `EuclideanRamseyNine.lean` ↔ Prop 7.6
- `literalCircleConfig t i = ((1−t_i²)/(1+t_i²), 2t_i/(1+t_i²))` with `AlgebraicIndependent ℚ t` (t : Fin 9 → ℝ) implies
  injective, on the unit circle, and `¬ Ramsey`. Literal match.

### (e) `EuclideanRamseyQuadratic.lean` ↔ Prop 7.3
- Hypotheses: injective, full affine span, cospherical, and
  `LinearIndependent (Coeff a) (i ↦ ((α,β) ↦ aug_iα · aug_iβ))`. These are the paper's "s row vectors
  (p_iα p_iβ)_{0≤α,β≤d} linearly independent over F", over all ordered pairs as in the paper. Faithful.

### (f) `EuclideanRamseySpherical.lean` ↔ Cor 7.1
- Injective + `Ramsey a` implies `EuclideanGeometry.Cospherical (range a)` (Mathlib: ∃ centre, radius). There is no span
  hypothesis, matching "every finite Euclidean Ramsey set is spherical". Faithful.

### (g) `EuclideanRamseyTransitive.lean` ↔ Cor 7.2
- `a`, `y` live in the same `Space D`; `range a ⊆ range y`; y is transitive under distance-preserving permutations of its
  index set. For a finite set these are its isometries.
- **EXPOSITION:** the comparator covers literal subsets. The paper's "isometric subset" (subtransitive) version is the
  non-comparator `TransitiveConsequence.isometric_subconfiguration_ramsey` (takes an index map `e` with `Congruent a (y∘e)`).
  It also follows from the comparator statement plus `ramsey_congruent_iff`.
- `_hy` (y injective) is unused, which is harmless. Faithful.

**Comparator defs vs solution defs.** `EuclideanRamsey/Model.lean` is identical to the definitions in the challenge files
(diffed). `SphericalRamsey/Model.lean` differs from `GrahamSpherical.lean` only by docstrings and an extra `weight` def that
the statement does not use. Instances declared in solution files cannot reach the challenge statements: those are
elaborated in files importing only Mathlib.

---

## 2. Proof audit (source level)

Closure = 47 files / 8,620 lines (EuclideanRamsey) + 19 files / 982 lines (SphericalRamsey).
- The brief says 18 SphericalRamsey files; there are 19, the extra being `Result.lean`, a 13-line alias.
- No file in either directory imports anything outside these two directories, Mathlib, and `Lean.Elab.Tactic.Omega`
  (the `omega` tactic).
- The `patches/` directory touches only third-party dependencies outside this closure. No patch targets any `Mathlib/`
  path, and Mathlib is pinned at d13f23b unpatched.

| token | count | note |
|---|---|---|
| `sorry` | 0 | (each comparator challenge file has exactly 1, as intended) |
| `admit` | 0 | 1 grep hit is the docstring word "admits" (BasisDerivation.lean:90) |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` / `unsafe` | 0 / 0 / 0 / 0 | the only `unsafe` in the repo is in `lakefile.lean` build config (dependency patching), not in any proof |
| `@[csimp]` / `decide := true` | 0 / 0 | |
| `set_option` (incl. `debug.*`, `maxHeartbeats`) | 0 | |
| `Lean.ofReduceBool` / `ofReduceNat` / `trustCompiler` | 0 | |
| `macro` / `macro_rules` / `syntax` / `elab` / `notation` | 0 | the 2 "elab" grep hits are `section Relabel`/`end Relabel` |
| `run_cmd` / `#eval` | 0 | |
| `by decide` | 6 | small Nat/Fin facts (e.g. `2 ≤ 50`, `Fin` inequalities); kernel `Decidable` |
| `instance` (incl. local) | 21 | see below |

**Instances: none on ℝ, `EuclideanSpace`, `Matrix`, `TensorProduct` or `IntermediateField`, the types appearing in
statements.**
- Instances on fresh types:
  - `FiniteEuclidean := ℕ →₀ ℝ` (a `def`, own inner-product structure);
  - `Corner p` (Mul/Semigroup, and a `Group` built from proven axioms);
  - Nine's `ParameterField`/`TargetField` algebras (proven equal to canonical).
- Prop-valued instances: `.Normal` for subgroups (`derived_normal`, `pairLeft_normal`, `singleFractions_normal`,
  `AugKernel`); `IsNoetherianRing (LatticeRing k)` from Mathlib's `Algebra.FiniteType`; `FiniteDimensional F F⟮x⟯`
  from integrality.
- `local instance tensorRing : CommRing (F ⊗[ℚ] F) := inferInstance` is the global instance itself.
- `attribute [local instance] Ultrafilter.mul Ultrafilter.semigroup` uses Mathlib's (Hindman) ultrafilter semigroup.
- There is no `local notation` and no `open private`.

Comparator JSON: permitted axioms `propext, Quot.sound, Classical.choice` for all seven. The `#print axioms` check is the
coordinator's replay; nothing in the source suggests it should fail.

---

## 3. Route audit

### Theorem 1.1, necessity (Ramsey ⇒ criterion) — paper's route (Prop 2.4 + Prop 2.1)
- `Congruence.congruent_linearIsometry`: copy = t + Q a (polarization).
- `TensorNecessity.lean`:
  - `separate_arrayMap` gives a ℚ-functional separating (0, I) from the image (Prop 2.4's ℓ).
  - `exists_separated_functions` gives h_i and L (eqs. (5)–(6)).
  - `separated_copy_sum`: Σ H_i(b_i) = −1 (eq. (7)).
  - `floor_coloring_obstruction` with K = 2s+1, and `ramsey_realCriterion`.
  - Colours = `Fin s → ZMod (2s+1)`, i.e. **(2s+1)^s, exactly the paper's K^s**.
- `TensorDescent.realCriterion_fieldCriterion` descends from ℝ⊗_ℚℝ to F⊗_ℚF; then `ramsey_fieldCriterion`.
  - **Different proof of Prop 2.1:** an F-basis b of ℝ plus an F-linear φ : ℝ → F with φ(1) = 1, mapping
    (x b_λ) ⊗ (y b_μ) ↦ (x⊗y)(φ(b_λ b_μ) ⊗ 1).
  - The paper instead row-reduces for coefficients c_{λμ}. Lean's c_{λμ} = φ(r_λ r_μ) is one explicit solution of the
    paper's system, so this is equivalent and simpler.
  - Lean never passes through symmetric tensors 𝒯(W) on this side; it works with unsymmetrised arrays.

### Theorem 1.1, sufficiency (criterion ⇒ Ramsey) — paper's route
Lattice identity → two-scale permutation pairs → free-group paths → ultrafilter realisation → Hales–Jewett:
1. `TensorDescent.fieldCriterion_realCriterion`: include F⊗F into ℝ⊗ℝ.
2. `TensorPresentation.exists_symmetric_tensor_presentation`, `realCriterion_lattice`: the §3 setup (rational symmetric
   C, rows w_j, U C Uᵀ = I, quotient tensors vanish).
   - Lean uses a spanning family rather than a basis; harmless.
3. `LatticeMoments` (`FiniteLatticeIdentity`, moments, jet ideals), then `AdicLifting.finite_lattice_identity` = **Lemma 3.1**.
   - **Different proof:** truncated nilpotent exp/log in R/I^N, plus Artin–Rees
     (`Ideal.exists_pow_inf_eq_pow_smul`, via `adic_intersection_lifting`).
   - The paper uses the m-adic completion and its flatness (Stacks 00MB). Same mathematical content at finite order.
4. `SmoothingKernel.exists_radial_smoothing`, `Hessian`, `DifferentialSplitting.exists_split_smoothing`,
   `SmoothingMatrix.compact_smoothing` = **Lemma 4.2**.
   - The statement `CompactSmoothing` matches (4.2): smooth, compact support, b ≥ 0, ∫b > 0,
     ∫(D_C b)_− ‖Ux‖² < η∫b.
   - **Different proof:** a radial-power bump ((1/4 + |x|²)^p − 1)_+ with p = 1/4 − d/2, smoothed by exp(−1/t), on
     H = im Uᵀ, times a vertically rescaled factor on V = ker U. The paper averages Gaussians over covariances S + tC.
   - `SmoothingMatrix.exists_small_covariance` builds the paper's S but is **never used** (dead code).
5. `Discretization.lattice_riemann`, `RationalConvolution.lattice_riemann_perturb`,
   `StencilConvolution.exists_discrete_smoothing`, `rational_smoothing` = **Lemma 4.3** (convolution, then rationalise in
   an open neighbourhood). Same route.
6. `SignedRows.normalized_signed_rows`, `GramCompletion.complete_gram_pair`, `two_scale_of_signed_rows`,
   `realCriterion_two_scale` = **Lemma 4.1**.
   - Same statement: q = η/(1+η) and g_i = f_i ∘ σ_i.
   - Lean does not need the affine-span hypothesis here.
7. `FiniteEuclidean` (ℰ = ℕ →₀ ℝ) and `PathWords` (`LetterGroup = FreeGroup ℰ`, inductive `Path`, which is exactly the
   paper's diagonal/copy factors with weights).
8. `UltrafilterStrings.simultaneously_realize` = Lemma 5.5.
9. `PathSynchronization.synchronize_paths` = Lemma 5.3.
10. `CornerGroup.exists_group_corner` = Lemma 5.4. Zorn on closed left ideals plus Mathlib's Ellis–Nakamura
    `exists_idempotent_in_compact_subsemigroup`.
11. `ColoringCompactness.paths_monochromatic` = Prop 5.1. Mathlib's Hales–Jewett
    `Combinatorics.Line.exists_mono_in_high_dimension`; colour words by ultrafilter colour; weights 1/t per variable
    position.
12. `finite_coloring_compactness` = **Lemma 5.2**. **Different proof:** ultrafilter limit over D rather than Tychonoff.
13. `PathFractions`: `RightFraction`, `singleFractions` = L_i, `singleCost` = c_i (Lemma 6.2).
14. `DerivedFractions.derived_subset_single` = eq. (37), N^{(s−2)} ⊂ L_i, with N = `AugKernel`.
15. `PathWords.unit_pair_inverse`/`pairGroup` = Lemma 6.1. The pair is extended to a copy by a Householder reflection
    rather than a frame.
16. `NormalCost`, `OrbitAveraging.finite_group_averaging` = Lemma 6.3.
17. `CorrectionPaths.averaged_equal_endpoints`, `permutation_equal_endpoints` = Prop 6.4.
    - H = Perm(Fin ℓ) acts on the labelled set H × Fin s rather than on the orbit set Z ⊂ ℰ; equivalent.
18. `Main.fieldCriterion_ramsey` with η = 1/(4n), δ = 1/(4ns), so the weight ratio is < 1/(2n) < 1/n.
    `classification` is necessity plus sufficiency.

**Verdict on route.** Same route as the paper, stage for stage.
- Lemma statements match. Four internal proofs differ: Prop 2.1 descent, Lemma 3.1, Lemma 4.2, Lemma 5.2.
- Consequence for the other seats: a defect in the paper's proofs of Lemma 3.1 (completion and flatness) or Lemma 4.2
  (Gaussian averaging, Schur-complement choice of S, cutoff estimates) is **not** what the kernel checks. The kernel checks
  different proofs of the same statements. Those two paper proofs need their own human check if the paper is to stand on
  its own text.

### Twelve points (Prop 7.7): no classification
SphericalRamsey imports nothing from EuclideanRamsey; it proves non-Ramseyness **directly with a derivation colouring**.
- `RealTranscendenceBasis` + `BasisDerivation` + `AlgebraicExtension` (Mathlib `FieldTheory.Differential`) +
  `RealDerivation.exists_real_derivation` give a ℤ-derivation D : ℝ → ℝ with D(t) = (1+t²)/2. Hence D u = −v and D v = u.
- `MonochromaticObstruction.derivationEnergy` is e(y) = Σ_j D(y_j)².
- `AffineCopy.affine_copy`: every isometric copy is y_i = z + x_{i1}A + x_{i2}B with |A| = |B| = 1.
- `EnergyIdentity.weighted_affine_derivation_energy` and `CopyInvariant.weighted_copy_derivation_energy` give
  Σ_i β_i e(y_i) = 8, with β = 1 on the rotated squares and −2 on Q_0.
- **Sympy-verified:** Lean's `weighted_coordinate_square` identity
  Σβ_i(p + a x_{i0} + b x_{i1} + c Dx_{i0} + d Dx_{i1})² = 4(u²+v²)(c²+d²) + 4(u²+v²−1)(a²+b²) holds identically.
  The paper's three moment identities (31) also check: 0, 0, diag(0, 4, 4).
- **Where 50 comes from:** colour = ⌊3e(y)⌋ mod 50 (`energyColor`). `Coloring.rounding_obstruction`:
  - Σβ_i = 0, so a monochromatic copy forces S = Σβ_i⌊3e_i⌋ ≡ 0 (mod 50).
  - The floors put S strictly inside (16, 32), which holds no multiple of 50.
  - 50 is an arbitrary admissible modulus. The same rounding argument already works mod 16, and mod any m ≥ 32.
  - It has nothing to do with the paper's 25^12 from Prop 2.4.

### Coverage gaps (paper items not in the Lean)
- **Cor 7.5** (kites, and the refutation of LRW Conjecture A necessity):
  - Covered: "K_a is Ramsey" (four circle points, via Circle).
  - Not covered: "K_a is not subtransitive" is cited from LRW Cor. 2 and not formalised. So the disproof of Conjecture A
    is only half machine-checked.
  - Refuting a conjecture of the form "these kites are not Ramsey" (Conjecture 3 as the paper describes it) needs only the
    Ramsey half.
  - I did not check LRW's text.
- **Remark 2.2** (Noetherian ring, finitely generated kernel; the criterion as an exact finite computation): not formalised.
  Nothing formal says the criterion is decidable or effective. Whether the existential criterion "characterises" Ramsey
  sets in Erdős's sense is a judgment call, not a formal fact (EXPOSITION).
- **Remark 2.3** (direct congruence invariance of the tensor criterion, even across coordinate fields): no Lean lemma about
  `FieldCriterion` under congruence. It follows only indirectly: classification plus `ramsey_congruent_iff`, for full-span
  representatives.
- **Prop 2.1** in its symmetric-tensor form ((3) in 𝒯(W)): not stated as such. Lean uses unsymmetrised arrays; the
  symmetrisation is inside `TensorPresentation`. Equivalent.
- **Prop 7.7's proof as written** (derivation ∂ on ℚ(t), "coordinate field = ℚ(t)", contradiction via Theorem 1.1): not what
  Lean does. Lean proves the statement, and more, by the direct route above.
- **Prop 7.6's determinant claim:** covered.
  - `NineGridDeterminant.det_E_ne_zero` uses the denominator-cleared rows (1+t², 1−t², 2t), giving det C' = 8 and
    det(C'⊗C') = 8⁶.
  - The paper's uncleared C has det 2 and det(C⊗C) = 2⁶ = 64. The two are consistent.
  - Injectivity of F⊗F into the rational function field is `IndependentTensor.tensorEmbedding_injective`.
- Intro and literature claims (EGMRSS Thm 13, Kříž, Cantwell, Pálvölgyi's Theorem A.3) are not formalised and need not be.

### Lean beyond the paper
- The 50-colour bound for the twelve points, valid in every dimension with a single derivation.
- A classification-free proof of the twelve-point result.
- `classification_nonempty` (arbitrary nonempty configurations).
- `isometric_subconfiguration_ramsey`.
- Sufficiency (`fieldCriterion_ramsey`) without the affine-span hypothesis.
- Ramsey ⇒ cospherical with no span or representative assumptions.
- Unused remnant: `exists_small_covariance`.

---

## 4. "Every spherical configuration with algebraic coordinates is Ramsey"?

**No such statement exists in the Lean, and none in the paper.**
- Grep of both directories and all seven comparators: `IsAlgebraic` appears only in Parameter.lean (proving `parameter` is
  transcendental).
- `Algebra.IsAlgebraic` appears only in `SphericalRamsey/AlgebraicExtension.lean` and `RealDerivation.lean`. There it
  extends a derivation from ℚ(transcendence basis) up to ℝ, which is the obstruction direction.
- `FormallyUnramified` and `KaehlerDifferential`: zero hits in the closure. They occur only in unrelated
  `OAI/NumberTheory/{PiExponent,SiegelZeros}` files.

**Observation for the coordinator (not a defect).** The statement is a few-line consequence of Theorem 1.1 that neither
document draws.
- If F is a number field, F⊗_ℚF is étale. There is a separability idempotent e with m_F(e) = 1 and e(x⊗1) = e(1⊗x).
- Take the sphere equation H ∈ Mat_{d+1}(F) with spatial block I_d (exists over F, as in the proof of Prop 7.3), and set
  P_αβ = e·(H_αβ ⊗ 1).
- Then (p_i⊗1)ᵀP(1⊗p_i) = e·((p_iᵀHp_i) ⊗ 1) = 0 and m_F(P_αβ) = H_αβ.
- So Theorem 1.1 makes **every spherical set with algebraic coordinates** (equivalently, algebraic squared distances)
  Ramsey, i.e. Graham's conjecture for all algebraic spherical sets.
- That is a very strong, unadvertised corollary and a natural falsification target: any known non-Ramsey spherical set with
  algebraic coordinates would refute Theorem 1.1.
- Pálvölgyi's heptagon requires transcendental r (palv_v1 Theorem 1), so it is consistent. In Lean it would follow from
  `classification` once e is built (Mathlib separability API). It is not formalised.

---

## Objections, classified
- **EXPOSITION (L1):** Circle comparator is planar only, and the Transitive comparator covers literal subsets only. The
  general forms follow by `ramsey_congruent_iff`; `isometric_subconfiguration_ramsey` exists but is not comparator-checked.
- **EXPOSITION (L2):** Cor 7.5 depends on the cited, unformalised LRW Cor. 2, so the formal record checks only the "Ramsey"
  half of the Conjecture A disproof. The paper is explicit that this half is a citation, so the formal record shows fewer
  checked claims than the abstract implies.
- **EXPOSITION (L3):** Remarks 2.2 and 2.3 are not formalised. Representative-independence of `FieldCriterion` and the
  effectiveness of the criterion are informal only.
- **EXPOSITION (L4):** the Lean proves Lemmas 3.1, 4.2, 5.2 and Prop 2.1 by different arguments. The kernel certificate
  therefore does not certify the paper's own proofs of those lemmas, only their statements. Dead code:
  `exists_small_covariance`.
- **EXPOSITION (L5):** the twelve-point Lean result bypasses the classification entirely and is strictly stronger
  (50 colours). The paper's Prop 7.7 proof, via Theorem 1.1, is not the one checked, though both are sound routes.
- No FATAL, GAP or ERROR-NONFATAL objection from this seat. The statements match, and the source audit is clean.

Conditional on the coordinator's kernel replay accepting the seven `theorem_names` with only
`propext/Quot.sound/Classical.choice`:

VERDICT: HOLDS AS READ
