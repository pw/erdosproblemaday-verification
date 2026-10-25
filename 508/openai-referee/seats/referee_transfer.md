# Referee report — seat `transfer` (§4 in full; tests (A), (C), (D) against the Lean; Lemma 4.3 only as (E))

Paper: OpenAI, "The Euclidean plane is not five-colorable", 23 Sep 2026, /tmp/oaimath/158/paper/paper.pdf.
§4 occupies PDF pp. 22–26 (read as rendered pages; all quotations below are from the rendered PDF).
Also read for context: pp. 1–10 (introduction, §1.1, Definitions 2.1–2.2, Theorem 2.3, Lemmas 2.4–2.6) and pp. 18–19 (Lemma 3.3), only to answer test (A).

Lean sources read as text (no lean/lake run): `Geometry/PlaneColoring/{Coloring,BorelTransfer,WeakColoring,Five}.lean`,
`Analysis/PlaneSpectrum/{Representations,SpectralMeasure,Ergodicity}.lean` in full, `Basic.lean` (definitions of E, K, D, C, IsWild, Lemma 2.4),
`InvariantMean.lean` (declarations), `RadialEnergy.lean` (the E-specific lemmas), `MeasureTheory/CompactFactors/Stationary.lean` in full,
`ConditionalLimits.lean` (`UniversalGood`). The other closure files (CompactFactors tower, Energy, Selections, NumberFields, Characters, Multipliers,
FourierTests, SmallArcs, Phase*, ConditionalSpectrum) are the proof of Theorem 2.3. They are the rigidity seat's scope, and I did not read them line by line.

Import closure of `BorelTransfer.lean` = the first 32 modules of `lean-build/order.txt` = 15,967 lines. Grep over all 32 for
`sorry|axiom|admit|implemented_by|unsafe|native_decide|extern|opaque`: **zero hits**. I did not build anything. The running replay's
`driver.log` (not mine) reports `built 32/70 OAI.Geometry.PlaneColoring.BorelTransfer (18s)` at 21:22:47Z, with RadialEnergy (28/70), SpectralMeasure (29/70)
and Ergodicity (30/70) built before it. Elaboration therefore succeeded. Whether the final axioms are standard is for the replay's `#print axioms` step to say.

---------------------------------------------------------------------------------------------------------------------------------------

## 1. Verdict for this scope

**§4: HOLDS AS READ, conditional on Theorem 2.3.** Lemma 4.1 and Proposition 4.2 check line by line. I found no FATAL and no GAP in §4. The objections
below are COSMETIC or exposition-level.

**The Lean proves Proposition 4.2, partly by a different route** (§4 below). Its only hypotheses are `ProperColoring k c` and `[NeZero k]`.
**Theorem 2.3 enters at exactly one sentence of the paper and at one lemma of the Lean.**

**Test (A).** §4 contains **no step that uses a property of F(i)/K beyond what Q(i)/K_Q also has, except the single invocation of Theorem 2.3.**
Theorem 2.3 is **false** for (Q(i), K_Q). I give explicit counterexamples, including the very measure that §4's own pipeline produces from the
proper 2-colouring of the rational unit-distance graph (finite checks in §6, with failing controls). So the transfer's correctness rests entirely on
the F(i)-specific inputs to the *proof* of Theorem 2.3.
- Paper: divisibility of K (p. 6, p. 7, p. 19 "surjectivity of the square map") and square roots in F (p. 19 "L = √AB ∈ F"; p. 18 "its radii lie in F≥0").
- Lean: `K_pow_surjective`/`rot_zsmul_surjective`, `sqrtF`, `circle_realPart`, `massReal_difference`.

The counterexample passes Lemmas 2.4 and 2.5 as stated. The divisibility argument written into Lemma 2.4 is therefore *not* what separates the two
cases. The separation must occur in Lemma 2.7/§3. I hand this to the rigidity seat as a negative control.

---------------------------------------------------------------------------------------------------------------------------------------

## 2. Objections (numbered)

**T1. The paper never says which property of E the transfer needs. UNCLEAR (exposition). Not a proof gap.**
- Location: p. 1 and p. 6 (Theorem 2.3); §4 as a whole.
- Quote, p. 1: *"In particular, the graph on all of ℝ² whose edges have rational unit displacement vectors is two-colorable, while every measurable
  coloring requires at least five colors. Thus measurable and unrestricted colorings cannot be identified merely because their distance constraints look the same."*
- What is wrong: the paper raises the obvious challenge itself but never states what in (F(i), K) defeats it. Every sentence of §4 is valid verbatim
  for (Q(i), K_Q) except *"If it is nonzero, normalize it and apply Theorem 2.3."* (p. 24). So the reader must find the answer inside the proof of
  Theorem 2.3, and the answer is not at the place the paper highlights (Lemma 2.4's divisibility; see §5(A)).
- Fix: one remark after Theorem 2.3 giving the Q(i) counterexample of §5(A), and naming the steps of §2–3 that fail for it.

**T2. Lemma 4.1 proves more than Proposition 4.2 uses. COSMETIC.**
- Location: p. 23, Bochner paragraph.
- Quote: *"Bochner's theorem supplies a finite measure on ℝ² representing this extension. Its pushforward under j has the same Fourier coefficients on D as λ_v,
  so Fourier uniqueness identifies the two measures. Thus λ_v(C^c) = 0."*
- What Proposition 4.2 actually uses:
  - the inclusion range P(C) ⊂ H_c (the *easy* direction: dominated convergence), to get "b_i ⊥ H_c ⇒ λ_{b_i}(C) = 0";
  - positivity and sum-one of the projection.
- The Bochner half and the identification H_c = L²(F_c) are correct but unused. The Lean omits both (§4(ii)–(iii) below).
- Nothing to fix.

**T3. Measurability of the exceptional set N is left implicit. COSMETIC.**
- Location: p. 25, "A measurable sample".
- Quote: *"There is a plane-null set N outside which all these representations are correct."*
- N is defined by an L²(µ) condition, and its measurability is not addressed. This is harmless: the construction (summable approximation errors plus an
  a.e.-convergent subsequence) produces a *measurable* conull set of good x, and N may be taken as its complement.
- The Lean avoids N altogether: its version is correct at every x (`exists_measurable_field`).

**T4. Invariance of F_c is not stated. COSMETIC.**
- Location: p. 23.
- Quote: *"Let F_c be the completed factor generated by the bounded members of H_c."*
- The proof never says that F_c is invariant under the action. That is what "factor" means. It is true, because T_z maps bounded members of H_c to bounded
  members of H_c. Conditional expectation onto a sub-σ-algebra does not need it anyway.

**T5. Sign convention between the spectral and Bochner representations. COSMETIC.**
- Location: p. 23.
- The spectral representation ⟨v, T_z v⟩ = ∫ψ_z dλ_v and Bochner's representation may differ by ξ ↦ −ξ. A reflection fixes this. No effect.

**T6. Hedge words in §4, all checked.**
- §4 contains one *"It follows that"* (p. 24, after Theorem 2.3). It is correct: Haar measure has vanishing nonzero Fourier coefficients.
- It contains one *"standard"* (p. 25, "the probability model is standard", used in its technical sense). Correct.
- The p. 3 sentence *"This is a standard amenable averaging construction"* is discharged in full on p. 24 (Følner sequence plus weak-* limit). The citations
  [1, Thm G.2.1, Prop G.2.2(ii), Thm G.5.1] all MATCH (§8).

**No objection rises above COSMETIC/UNCLEAR inside §4.** The brief's classic holes were each checked for this scope:
- **Ergodicity.** Proposition 4.2 never assumes it. The spectral measure of b_i is merely K-invariant, and Theorem 2.3 is stated for every K-invariant wild
  law. The ergodic decomposition is p. 22, end of §3: *"Finally, an arbitrary wild invariant probability has an ergodic decomposition…"*. In the Lean it is
  `wild_fourier`, Ergodicity.lean l.335, via `InvariantDecomposition.fiber_ergodic` l.309.
- **Conditional expectation.** It is applied only after H_c = L²(F_c) is proved.
- **Choice and limits.** The invariant law is a weak-* limit along a *subsequence* of a Følner sequence in a compact metrizable space. That is legitimate.
  No invariant mean is later treated as a sequential limit in §4.
- **Uncountable operations.** None. "Least index with positive field" is a finite operation, and C is a countable union of compacts.

---------------------------------------------------------------------------------------------------------------------------------------

## 3. Line-by-line status

| Item | Status | Notes |
|---|---|---|
| §4 preamble (p. 22) | VERIFIED | |
| Lemma 4.1 — H_c closed | VERIFIED LINE BY LINE | ‖T_z v−v‖ ≤ 2‖v−w‖+‖T_z w−w‖ (T_z unitary) |
| Lemma 4.1 — constants, translation invariance | VERIFIED | ‖T_z T_a v − T_a v‖ = ‖T_z v − v‖ |
| Lemma 4.1 — λ_v(C^c)=0 ⇒ v ∈ H_c | VERIFIED | ∫_C\|ψ_z−1\|² dλ_v = ∫_{ℝ²}\|e^{iξ·z}−1\|² d(j^{-1}_*λ_v) → 0 by DCT; j^{-1} Borel on C (p. 6) |
| Lemma 4.1 — v ∈ H_c ⇒ λ_v(C^c)=0 | VERIFIED | uniform continuity \|F_v(z+h)−F_v(z)\| ≤ ‖v‖‖T_h v−v‖; extension positive definite by approximation; Bochner [1, D.2.2]; Fourier uniqueness on compact D |
| Lemma 4.1 — H_c = range of spectral projection P(C) | VERIFIED | ‖P(C^c)v‖² = λ_v(C^c) |
| Lemma 4.1 — products and Lipschitz images stay in H_c | VERIFIED | T_z(vw) − vw = T_z v·(T_z w − w) + w·(T_z v − v), with ‖T_z v‖_∞ = ‖v‖_∞ (Koopman); Φ(T_z v) = T_z Φ(v) |
| Lemma 4.1 — H_c = L²(F_c) | VERIFIED | unital *-algebra of bounded members; Stone–Weierstrass on a compact range in ℂⁿ; monotone class; closedness gives ⊂; truncations give ⊃ |
| Lemma 4.1 — projection = conditional expectation | VERIFIED | standard once H_c = L²(F_c) |
| Lemma 4.1 — extension to x ∈ ℝ² | VERIFIED | Cauchy via ‖T_{z_n−z_m}v − v‖; group law, unitarity, strong continuity (sup over \|z\| ≤ 2\|x\|); positive cone closed; T_x1 = 1 |
| Lemma 4.1 — rotations | VERIFIED | T_z V_u = V_u T_{u^{-1}z} from V_u T_w V_u^{-1} = T_{uw}; covariance direction re-derived from Koopman formulas and matches the Lean `covariance` (Representations l.95) |
| Prop 4.2 — invariant law | VERIFIED | Ω closed in {1..k}^E (compact metrizable); E ⋊ K amenable [1, G.2.1 + G.2.2(ii)]; Følner [1, G.5.1]; weak-* subsequence; a limit of left-Følner averages of δ_{gω} is invariant |
| Prop 4.2 — f_i, T_z f_i, rotation-fixed, (4.1) | VERIFIED | (V_u f_i)(η) = 1[η(u·0)=i] = f_i(η); 0 and u ∈ K are adjacent |
| Prop 4.2 — p_i = E(f_i\|F_c), 0 ≤ p_i ≤ 1, Σ p_i = 1, p_i and b_i rotation-fixed | VERIFIED | projection commutes with V_u (Lemma 4.1) |
| Prop 4.2 — λ_{b_i} is K-invariant | VERIFIED | ⟨b,T_{uz}b⟩ = ⟨V_u^{-1}b, T_z V_u^{-1}b⟩ = ⟨b,T_z b⟩; Fourier uniqueness |
| Prop 4.2 — λ_{b_i}(C) = 0 | VERIFIED | needs only range P(C) ⊂ H_c |
| Prop 4.2 — apply Theorem 2.3 | VERIFIED *as an application*; Theorem 2.3 itself NOT VERIFIED (rigidity seat) | the hypotheses supplied match Definition 2.2 exactly |
| Prop 4.2 — cross terms vanish ⇒ ⟨p_i, T_u p_i⟩ = 0, u ∈ K | VERIFIED | H_c^⊥ is translation invariant |
| Prop 4.2 — density of K in S¹ ⇒ all u ∈ S¹; (4.2) | VERIFIED | x ↦ ⟨p_i,T_x p_i⟩ is continuous; p_i is real, and so is T_x p_i |
| Prop 4.2 — measurable sample | VERIFIED LINE BY LINE | product-L² Cauchy; a.e.-x identification; Borel version; clamp needs T_x p_i ≤ 1, which follows from T_x(1−p_i) ≥ 0 and T_x1 = 1; Tonelli; countably many ω-conditions; least index; exceptional pairs product-null |
| Lemma 4.3 (test E only) | VERIFIED (quick) | density bound 1/(πh²), support in B(y,2h), \|B(y,2h)\|/(πh²) = 4, absolute continuity of (x',u'); the Lean analogue `weak_density_proper` (WeakColoring.lean l.149) uses a different proof via `weak_all_directions` (continuity in the direction) — SKIMMED |
| Proof of Theorem 1.3, converse (p. 26) | VERIFIED (light) | not needed for Theorem 1.1 |
| Theorem 2.3, Lemmas 2.4–2.7, §3 | NOT VERIFIED (out of scope) | Lemmas 2.4, 2.5, 3.3 read only for test (A) |

---------------------------------------------------------------------------------------------------------------------------------------

## 4. Tests (C) and (D): what the Lean states, in plain words

| Lean name (file:line) | Plain words |
|---|---|
| `PlaneSpectrum.E` (Basic.lean:9) | `algebraicClosure ℚ ℂ` = Q̄ ⊂ ℂ, with the subspace topology from ℂ. This equals F(i) of Definition 2.1. |
| `K` (Basic:11) | Unit-modulus complex numbers that are algebraic. Divisible: `K_pow_surjective` (Basic:17) via `IsAlgClosed.exists_pow_nat_eq`. |
| `D`, `C`, `IsWild` (Basic:48,100,300) | D = Pontryagin dual of E with the discrete topology. C = range of ξ ↦ (z ↦ exp(i⟨ξ,z⟩)). `IsWild ν` = "every u ∈ K preserves ν" ∧ ν(C) = 0, with probability supplied as an instance. This is Definition 2.2 verbatim. |
| `LabelModel.Space k` (Representations:56) | `{ω : E → Fin k // ∀ x y ∈ E, ‖x−y‖ = 1 → ω x ≠ ω y}`: the proper k-labelings of the unit-distance graph on E. Compact (closed in a product of finite sets, `closed_proper`). This is Ω of Proposition 4.2. |
| `trans k a`, `rotate k b` (l.64,69) | (trans a ω)(x) = ω(x+a), for a ∈ E; (rotate b ω)(x) = ω(b·x), for b ∈ K. Both preserve properness. `covariance`: trans a ∘ rotate b = rotate b ∘ trans (b·a). |
| `measure k ω` (l.116; `StationaryMean.measure`, Stationary.lean:85) | A Borel probability on `Space k`. It is the Riesz–Markov measure of the functional f ↦ mean_{b∈K} mean_{a∈E} f(rotate b (trans a ω)) on continuous f. Here `mean` is a translation-invariant mean on the discrete abelian group, an ultrafilter limit of cube averages (InvariantMean.lean:215). **ω is the base point of the averaging**: the restriction c\|_E of the given colouring, set in `proper_to_borel_weak` (BorelTransfer l.436–438). The measure is the invariant average of the orbit of ω; it need not charge ω. |
| `trans_preserving`, `rotate_preserving` (l.118,124) | `measure k ω` is invariant under every translation a ∈ E and every rotation b ∈ K. Proved from shift-invariance of the inner mean, using `covariance`, and of the outer mean. |
| `Hilbert k ω`, `representation k ω`, `rotation k ω b` (l.238,249,241) | L²(ℂ-valued, `measure k ω`). `representation` is the homomorphism E_disc → unitaries, a ↦ the Koopman operator of trans a. `rotation b` is the Koopman operator of rotate b. `rotation_covariance` (l.270): rotation b ∘ T_a = T_{b·a} ∘ rotation b. |
| `ContinuousVectors.space U` (l.182) | {v : a ↦ T_a v tends to v as a → 0 in E's usual topology}. **This is H_c of Lemma 4.1.** `isClosed_space` (l.194) is the first line of the proof of Lemma 4.1. |
| `projection_range` (l.332) | If v takes values in [0,1] a.e., so does its orthogonal projection onto `space U` (real-valued, in [0,1]). Proof: pointwise clamp to [0,1] is a 1-Lipschitz map of L² that fixes v and maps `space U` into itself (`nonlinear_mem`: Koopman operators commute with pointwise Lipschitz maps). `projection_fixed_of_contraction` (l.284): a 1-Lipschitz F with F(S) ⊂ S and F v = v also fixes P_S v. **No factor and no conditional expectation are used.** |
| `projected_sum` (BorelTransfer:91) | Σ_i P f_i = P 1 = 1, because the constant 1 is translation-fixed and hence in `space` (`one_continuous`). |
| `projection_covariance_fixed` (l.366) | If W is unitary, intertwines translations up to a homeomorphism φ of E fixing 0, and fixes v, then W fixes P v. Same contraction argument. |
| `projection_coefficient` (l.380) | If the residual b = v − Pv has ⟨b, T_a b⟩ = 0, then ⟨Pv, T_a Pv⟩ = ⟨v, T_a v⟩. The cross terms vanish because `space` and its orthogonal complement are T-invariant (`op_mem`, `op_orthogonal`). |
| `measure (calculus U) v` (SpectralMeasure:156; Representations:437) | The scalar spectral measure λ_v on D. It is built by Gelfand theory of the commutative C*-algebra generated by the T_a, pulled back to D, followed by Riesz–Markov, so that ∫ψ_a dλ_v = ⟨v, T_a v⟩ (`integral_complex` + `calculus_evaluation`). |
| `measure_ordinary_zero_of_orthogonal` (SpectralMeasure:287) | v ⊥ `space` ⇒ λ_v(C) = 0. The vector "1_C(spectral) v" is shown to be continuous by dominated convergence (`ordinaryVector_continuous`); pairing with v gives λ_v(C) = 0. This is the *easy* half of Lemma 4.1. No Bochner. |
| `residual_fourier` (Ergodicity:403) | **Theorem 2.3 enters here.** Hypotheses: v ⊥ `space U`; v is fixed by all W k; W k ∘ T_z = T_{k·z} ∘ W k. Conclusion: ⟨v, T_z v⟩ = 0 for every z ∈ E∖{0}. Proof: λ_v is wild (`vectorMeasure_invariant` + `measure_ordinary_zero_of_orthogonal`), then `finite_wild_fourier`. |

**Where Theorem 2.3 sits in the Lean chain:**
1. `BorelTransfer.projected_unit_correlation` (l.59–65) calls `residual_fourier` (Ergodicity:403).
2. → `finite_wild_fourier` (:364, normalisation; zero-measure case).
3. → **`wild_fourier` (:335)**: for every probability μ on D with `IsWild μ`, ∫ψ_z dμ = 0 for z ≠ 0. This is Theorem 2.3 in Fourier form; equivalence to μ = m_D is by Fourier uniqueness, which the Lean never states. It works through the ergodic decomposition: invariant-mean `code` map + `condDistrib` + `fiber_ergodic`, Ergodicity:282–320.
4. → `ergodic_wild_fourier` (:52), which uses two inputs:
   - `exists_terminal_factor` (Stationary:126): Lemma 3.1, together with Lemma 2.7 in the form `UniversalGood` (ConditionalLimits:669);
   - `fourier_vanish_of_terminal` → `projectedMass_vanish` → **`massReal_vanish` (RadialEnergy:452)**: §3.3–3.5, with Lemma 2.5 entering as `exists_small_wild_parameter` (FourierTests:200).

**Do the hypotheses BorelTransfer supplies to `residual_fourier` match? Yes, exactly.**
- U = `representation k ω`.
- W = `rotation k ω`.
- hcov = `rotation_covariance k ω`.
- v = `colorVector − projected` ∈ `space`ᗮ, by `sub_starProjection_mem_orthogonal`.
- Fixedness: `color_rotation_fixed` and `projected_rotation_fixed`.
- z = `kCoeff b` ≠ 0, by `kCoeff_ne_zero`.

**Hypotheses stronger than ProperColoring: NONE.**
- `proper_to_borel_weak {k} [NeZero k] {c} (hc : ProperColoring k c)` is the whole interface. `NeZero k` is vacuous in practice: no map ℂ → Fin 0 exists.
- `Space k` uses exactly `‖x − y‖ = 1 → ω x ≠ ω y`, restricted to E.
- No measurability, regularity, or extra set theory is assumed. Choice appears only through Lean's classical logic: ultrafilters for the means, `Nat.find`, `Finset` choice.
- §2–4 never use k = 5, neither the paper nor the Lean (relevant to test B).

**Does the Lean prove Proposition 4.2 as written? Same skeleton, different route at five points:**
- **(i) Invariant law.** Iterated invariant means (inner over E, outer over K) plus Riesz–Markov, instead of Følner averages and a weak-* subsequence on E ⋊ K.
- **(ii) Positivity and sum.** The contraction argument (`projection_range`, `projected_sum`), instead of "H_c = L²(F_c), so projection is conditional expectation". Lemma 4.1's factor statement is never formalised.
- **(iii) Spectral input.** Only "v ⊥ H_c ⇒ λ_v(C) = 0", built from Gelfand theory, instead of the SNAG theorem plus Bochner.
- **(iv) Extension to ℝ².** No operator group on ℂ is built. Only the orbit maps x ↦ "T_x p_i" are extended (`orbitExtension`, by uniform continuity on the dense set E).
  - [0,1]-valuedness (`fieldVector_range`) and Σ = 1 (`fieldVector_sum`) follow by closedness plus density.
  - The correlation identity ⟨T_x p, T_{x+y} p⟩ = ⟨p, T_y p⟩ follows by double density (`orbitExtension_inner`).
  - Extension to every u ∈ S¹ is `circle_closed_induction`: approximate u by z_n ∈ E and use z_n/|z_n| ∈ K (`normalized_algebraic`, which needs |z| algebraic).
- **(v) Measurable sample.** `exists_measurable_field` gives a jointly measurable F with F(t,·) = f(t) µ-a.e. **for every t**, not just a.e. t.
  - Construction: `Nat.find` index into a dense sequence with error < 2^{-n}, summable in L², a.e. convergence, then `limsup` of the real and imaginary parts.
  - The paper's null set N and the product-null argument therefore disappear.
  - `sample_field` gets the exchange of quantifiers from `Measure.ae_ae_comm` (Fubini for a measurable a.e.-set) and picks ω.
  - The output is **Borel** d with ∀ᵐ (x,t) ∂ volume ⊗ Haar(AddCircle 2π): d x ≠ d (x + e^{it}). This is at least what Proposition 4.2 asserts. Whether it matches Definition 1.2 exactly is the "whole" seat's comparison; I note only that "least index" is replaced by "some index with positive field", which is immaterial.

Every route difference is a valid alternative. Points (ii) and (v) are *simpler and stronger* than the paper's text.

---------------------------------------------------------------------------------------------------------------------------------------

## 5. Test (A): Payne's rational graph

### (A1) Every sentence of §4 that mentions E or K, checked against (E, K) → (Q(i), K_Q)

**Lemma 4.1** uses only these properties:
- E is a countable subgroup of ℝ², with its usual topology (density of E is not even used inside the lemma);
- the action is measure-preserving with Koopman operators;
- K acts by multiplications V_u T_z V_u^{-1} = T_{uz} with |u| = 1.

All of these hold for (Q(i), K_Q). Neither divisibility nor algebraicity appears.

**Proposition 4.2** touches E or K in these sentences:
- (a) *"The countable group E ⋊ K acts continuously on Ω … This group is amenable, being an extension of two abelian groups"*: true for Q(i) ⋊ K_Q.
- (b) (4.1): uses only that 0 and u ∈ K are adjacent: true.
- (c) *"The scalar translation spectral measure of b_i is K-invariant … It gives C measure zero"*: generic.
- (d) **"If it is nonzero, normalize it and apply Theorem 2.3."** This is the only E-specific input.
- (e) *"The algebraic unit directions are dense in the usual unit circle, as is seen already from the rational tangent-half-angle parametrization."* Rational units are dense too.
- The measurable sample is generic.

**Conclusion:** §4 proves, verbatim, "Theorem 2.3 for (E, K) ⇒ transfer for (E, K)", for any countable dense subfield E ⊂ ℂ closed under conjugation, with K its unit circle.

In the Lean, BorelTransfer's E-specific uses are:
- `dense_E`: true for Q(i);
- `normalized_algebraic` (z/|z| ∈ K): **false** for Q(i), since (1+i)/√2 ∉ Q(i). It is only used to approximate unit vectors, and Pythagorean density would replace it;
- `residual_fourier`, i.e. Theorem 2.3.

### (A2) Theorem 2.3 is FALSE for (Q(i), K_Q): explicit counterexamples

Let H = ℤ_(2)[i] (Gaussian rationals with odd denominators) and let ρ : H → 𝔽₂ = H/(1+i)H be the residue map, x+iy ↦ num(x)+num(y) mod 2.

- **Every rational unit u = (a+bi)/c lies in H and has ρ(u) = 1.** Primitive Pythagorean c is odd and a+b is odd. Check (1) covers all 2,556 units with c ≤ 2000.
- ρ(uz) = ρ(z) for every z ∈ H (check (3)).
- The subring ℤ[K_Q] is contained in H (check (4)), and E/H is infinite.

**ν_H := Haar measure on the annihilator H^⊥ ⊂ D_{Q(i)}** has these properties:
- It is K_Q-invariant, because uH = H.
- It is wild. A continuous character trivial on the dense subgroup H is trivial, so C ∩ H^⊥ = {0}. H^⊥ is infinite, so its Haar measure has no atoms.
- Its Fourier coefficient is 1_H(z), so it is **not Haar** (the coefficient is 1 at z = 1).

The second counterexample is the very measure §4 manufactures.
- The rational unit graph on Q(i) has the proper 2-colouring c(r+h) = ρ(h), for coset representatives r of Q(i)/H (check (2)).
- Run Proposition 4.2 with k = 2. On the unit-step group G (the additive group generated by K_Q), **every** proper 2-labelling satisfies η(z) = η(0) ⇔ ρ(z) = 0, by path parity, since ρ(sum of n units) = n mod 2. Also µ(η(0) = 1) = ½.
- Hence ⟨f_1, T_z f_1⟩ = ½·1[ρ(z) = 0] on G.
- Both residues occur at points of G arbitrarily close to any point of G (checks (7) and (8): z0 = 3 approached by 3-unit sums with ρ = 0 and by 2-unit differences with ρ = 1, at distance 8.7e-5 / 1.8e-4). So this function is **nowhere continuous on G**.
- If λ_{b_1} were zero or Haar, then ⟨f_1, T_z f_1⟩ = ⟨p_1, T_z p_1⟩ on Q(i)∖{0}, and that function is continuous because p_1 ∈ H_c. Contradiction.
- So the normalised spectral measure of b_1 is K_Q-invariant and C-null (by §4's own E-independent sentences), yet not Haar.

**Therefore Theorem 2.3 fails for Q(i) on exactly the measure that §4 feeds it.** If it held, §4 would output a weak measurable 2-colouring of ℝ²,
which Lemma 4.3 plus one translated unit equilateral triangle refutes.

**What the method proves for the rational graph: nothing.**

### (A3) Where the algebraic case differs

There are three structural differences, each tested:

1. **K is divisible; K_Q is not.** (3+4i)/5 has no square root in Q(i), since x² = 4/5 is not a rational square (check (5)).
   - Paper p. 6: *"Every nonzero power map u ↦ uⁿ on K is onto … Thus K is divisible."*
   - Used on p. 7 (Lemma 2.4: *"a finite abelian group cannot be divisible unless it is trivial"*), and on p. 19 (Lemma 3.3: *"Ergodicity of Y and surjectivity of the square map now give"*; *"Mean ergodicity on Y through the surjective power map u ↦ u^{−2} gives the limit m(r)²."*).
   - Lean: `K_pow_surjective` (Basic:17) → `rot_zsmul_surjective` (Representations:34), used in RadialEnergy l.56 (`projectedMass_pair_mean`), l.97 (`quadratic_mass_inequality`) and l.396 (`radiusFamily_mean`).
2. **F is closed under square roots of nonnegative elements.**
   - Paper p. 19: *"First take A, B > 0 and put L = √AB ∈ F."* Paper p. 18: *"Equal nonzero moduli in E differ by an element of K. Thus m is radial; its radii lie in F≥0."*
   - For Q(i), |1+i| = √2 is not even a rational radius.
   - Lean: `sqrtF` (RadialEnergy:123) in `massReal_difference` (:157) and `circle_realPart` (:259, in `cover_mass_positive` :280); `normF` (Ergodicity:12).
3. **ℤ[K] = E for Q̄, but ℤ[K_Q] ⊂ ℤ_(2)[i] for Q(i).**
   - For Q̄: every real algebraic t ∈ [−2, 2] is u + ū with u = t/2 + i√(1 − t²/4) ∈ K (check (6) shows 1/2 = u + ū with |u|² = 1/16 + 15/16 = 1, impossible in Q(i) because 15/16 is not a square). Hence Q̄ has **no** proper nonzero K-invariant subgroup, and Haar(H^⊥)-type counterexamples cannot exist there.

**Which step catches ν_H? Not Lemma 2.4 or 2.5.**
- Lemma 2.4: cosets of C are ν_H-null, because each meets H^⊥ in at most one point of an atomless Haar measure. The difference law Haar(H^⊥) is C-null. L_1 ∩ H^⊥ = (ℚ + H)^⊥ has infinite index, because ℚ/ℤ_(2) is infinite.
- Lemma 2.5: the coefficient restricted to a line is supported on an infinite-index subgroup of F/ℤ, so the invariant mean is 0.
- So **the divisibility argument written into Lemma 2.4 is not what separates Q̄ from Q(i)**.
- ν_H is not weakly mixing: the K_Q-orbit of the character class ½ + H has exactly 2 elements (check (9); the control (C5) shows the class-counter does separate 15 classes). Its compact factor is therefore nontrivial, and the separation must occur in Lemma 2.7/§3, where divisibility and √ are used again.
- I hand ν_H and the §4-generated measure to the rigidity seat as **negative controls**: any proof of Theorem 2.3, transplanted to Q(i), must fail on them, and the line where it fails is the line that does the real work.

---------------------------------------------------------------------------------------------------------------------------------------

## 6. Finite check (verbatim script, output, controls)

`/tmp/oaimath/158/seats/transfer_checks/payne_rational.py`, run with `python3 -I`: 4.0 s wall, 13 MB RSS.

```python
# Test (A) for the transfer seat: the (Q(i), K_Q) analogue of Section 4.
# Gaussian rationals z = (x, y) with Fraction coordinates.
from fractions import Fraction as Fr
from math import gcd, isqrt
import random, sys

random.seed(158)

def in_H(z):            # H = Z_(2)[i]: both coordinates have odd denominator
    return z[0].denominator % 2 == 1 and z[1].denominator % 2 == 1

def rho(z):             # residue map Z_(2)[i] -> Z_(2)[i]/(1+i) = F_2 ; x+iy -> x+y mod 2
    assert in_H(z), z
    return (z[0].numerator + z[1].numerator) % 2   # odd denominators are 1 mod 2

def add(z, w): return (z[0] + w[0], z[1] + w[1])
def mul(z, w): return (z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0])
def conj(z):   return (z[0], -z[1])
def norm2(z):  return z[0]*z[0] + z[1]*z[1]

def rational_units(cmax):
    U = {(Fr(1), Fr(0)), (Fr(-1), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(-1))}
    m = 2
    while m*m + 1 <= cmax:
        for n in range(1, m):
            if (m - n) % 2 == 1 and gcd(m, n) == 1 and m*m + n*n <= cmax:
                a, b, c = m*m - n*n, 2*m*n, m*m + n*n
                for (p, q) in ((a, b), (b, a)):
                    for s in (1, -1):
                        for t in (1, -1):
                            U.add((Fr(s*p, c), Fr(t*q, c)))
        m += 1
    return sorted(U)

def rand_H(maxden=999, maxnum=2000):
    def r():
        d = random.randrange(1, maxden + 1, 2)            # odd denominator
        return Fr(random.randint(-maxnum, maxnum), d)
    return (r(), r())

def is_rational_square(q):
    q = Fr(q)
    if q < 0: return False
    a, b = q.numerator, q.denominator
    return isqrt(a)**2 == a and isqrt(b)**2 == b

def run(colour, displacements, samples):
    bad = 0
    for _ in range(samples):
        z = rand_H()
        for u in displacements:
            w = add(z, u)
            if not in_H(w) or colour(w) == colour(z):
                bad += 1
    return bad

U = rational_units(2000)
print("rational units with denominator <= 2000:", len(U))
assert all(norm2(u) == 1 for u in U)
# (1) every rational unit lies in H and has residue 1
print("(1) all units in Z_(2)[i]:", all(in_H(u) for u in U), "| all residues 1:", all(rho(u) == 1 for u in U))
# (2) colouring c = rho on H is proper for every rational unit edge
print("(2) improper unit edges, c = rho:", run(rho, U, 300))
# (3) H is K_Q-stable and rho is K_Q-invariant: rho(u z) = rho(z), rho(conj(u) z) = rho(z)
viol = 0
for _ in range(300):
    z = rand_H()
    for u in random.sample(U, 40):
        for v in (u, conj(u)):
            w = mul(v, z)
            if not in_H(w) or rho(w) != rho(z): viol += 1
print("(3) K_Q-invariance violations of (H, rho):", viol)
# (4) subring generated by units stays inside H (random words: sums of products)
ok = True
for _ in range(2000):
    s = (Fr(0), Fr(0))
    for _ in range(random.randint(1, 6)):
        p = (Fr(1), Fr(0))
        for _ in range(random.randint(1, 4)): p = mul(p, random.choice(U))
        s = add(s, p) if random.random() < .5 else add(s, (-p[0], -p[1]))
    ok &= in_H(s)
print("(4) Z[K_Q] sampled words all in Z_(2)[i]:", ok)
# (5) K_Q not divisible: (3+4i)/5 has no square root in Q(i)  (x^2 = 4/5 forced)
print("(5) sqrt((3+4i)/5) rational?  x^2 = 4/5 square?", is_rational_square(Fr(4, 5)))
# (6) Qbar contrast: u = 1/4 + i*sqrt(15)/4 is an algebraic unit (|u|^2 = 1/16 + 15/16 = 1), u + conj(u) = 1/2,
#     so 1/2 lies in Z[K]; in Q(i) no unit has real part 1/4 because 15/16 is not a rational square.
print("(6) |u|^2 =", Fr(1, 16) + Fr(15, 16), "| 15/16 rational square?", is_rational_square(Fr(15, 16)))
# (7) discontinuity of the correlation p*1[rho(z)=0] on H at a point z0 of H \ {0}
z0 = (Fr(3), Fr(0))
seqA = [add(z0, (Fr(1, 2*n + 1), Fr(0))) for n in range(1, 6)]      # rho flips
seqB = [add(z0, (Fr(2, 2*n + 1), Fr(0))) for n in range(1, 6)]      # rho kept
print("(7) rho along z0+1/(2n+1):", [rho(z) for z in seqA], " along z0+2/(2n+1):", [rho(z) for z in seqB],
      " both -> z0 =", z0)

print("--- controls that must FAIL ---")
# (C1) non-unit displacement 2: same residue, the properness check must report failures
print("(C1) improper edges for displacement 2 (non-unit):", run(rho, [(Fr(2), Fr(0))], 300))
# (C2) a different colouring (parity of floor of real part) must be improper for unit edges
print("(C2) improper unit edges, c = floor(Re z) mod 2:", run(lambda z: (z[0].numerator // z[0].denominator) % 2, random.sample(U, 50), 50))
# (C3) multiplier 1+i (not a unit) breaks rho-invariance
viol = sum(rho(mul((Fr(1), Fr(1)), z)) != rho(z) for z in (rand_H() for _ in range(300)))
print("(C3) rho((1+i) z) != rho(z) count:", viol)
# (C4) a point outside H must be rejected by in_H
print("(C4) (1+i)/2 in H?", in_H((Fr(1, 2), Fr(1, 2))))

print("--- (8) discontinuity inside the unit-step group G (sums of rational units only) ---")
from math import tan, pi, hypot
def unit_at(theta, Q):
    t = Fr(round(tan(theta/2)*Q), Q)            # rational tangent half-angle
    d = 1 + t*t
    return ((1 - t*t)/d, 2*t/d)
z0 = add(add((Fr(1), Fr(0)), (Fr(1), Fr(0))), (Fr(1), Fr(0)))   # 3 = 1+1+1, a sum of 3 units
for Q in (10, 100, 1000, 10000):
    a = [unit_at(0.3 + k*2*pi/3, Q) for k in range(3)]
    odd = add(add(a[0], a[1]), a[2])                           # 3 units, small
    u, v = unit_at(0.3, Q), unit_at(0.3 + 1.0/Q, Q*10)
    even = add(u, (-v[0], -v[1]))                              # 2 units, small
    assert all(norm2(w) == 1 for w in a + [u, v])
    print(f"Q={Q:6d}  |odd|={hypot(float(odd[0]), float(odd[1])):.2e} rho(z0+odd)={rho(add(z0, odd))}"
          f"   |even|={hypot(float(even[0]), float(even[1])):.2e} rho(z0+even)={rho(add(z0, even))}")

print("--- (9) K_Q-orbit of the character class 1/2 + H in Q(i)/H (finite orbit => nu_H not weakly mixing) ---")
def v2(q):
    q = Fr(q); n, d, v = q.numerator, q.denominator, 0
    if n == 0: return 10**9
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v
def same_class(z, w):              # z - w in H = Z_(2)[i]  <=>  v_2(N(z-w)) >= 0
    d = add(z, (-w[0], -w[1])); return v2(norm2(d)) >= 0 and in_H(d)
reps = []
for u in U:
    z = mul(u, (Fr(1, 2), Fr(0)))
    if not any(same_class(z, r) for r in reps): reps.append(z)
print("(9) distinct classes {u/2 + H : u in K_Q, denominator <= 2000}:", len(reps), reps)
# control: the orbit of 1/2 + H under multiplication by the NON-unit Gaussian integers 1..6 is larger
reps2 = []
for m in [(Fr(a), Fr(b)) for a in range(0, 4) for b in range(0, 4) if (a, b) != (0, 0)]:
    z = mul(m, (Fr(1, 4), Fr(0)))
    if not any(same_class(z, r) for r in reps2): reps2.append(z)
print("(C5) classes of {m/4 + H : m in Z[i], 0<=a,b<4}:", len(reps2))
```

Output:

```
rational units with denominator <= 2000: 2556
(1) all units in Z_(2)[i]: True | all residues 1: True
(2) improper unit edges, c = rho: 0
(3) K_Q-invariance violations of (H, rho): 0
(4) Z[K_Q] sampled words all in Z_(2)[i]: True
(5) sqrt((3+4i)/5) rational?  x^2 = 4/5 square? False
(6) |u|^2 = 1 | 15/16 rational square? False
(7) rho along z0+1/(2n+1): [0, 0, 0, 0, 0]  along z0+2/(2n+1): [1, 1, 1, 1, 1]  both -> z0 = (Fraction(3, 1), Fraction(0, 1))
--- controls that must FAIL ---
(C1) improper edges for displacement 2 (non-unit): 300
(C2) improper unit edges, c = floor(Re z) mod 2: 866
(C3) rho((1+i) z) != rho(z) count: 159
(C4) (1+i)/2 in H? False
--- (8) discontinuity inside the unit-step group G (sums of rational units only) ---
Q=    10  |odd|=1.16e-01 rho(z0+odd)=0   |even|=0.00e+00 rho(z0+even)=1
Q=   100  |odd|=3.91e-03 rho(z0+odd)=0   |even|=1.17e-02 rho(z0+even)=1
Q=  1000  |odd|=2.49e-04 rho(z0+odd)=0   |even|=1.17e-03 rho(z0+even)=1
Q= 10000  |odd|=8.69e-05 rho(z0+odd)=0   |even|=1.76e-04 rho(z0+even)=1
--- (9) K_Q-orbit of the character class 1/2 + H in Q(i)/H (finite orbit => nu_H not weakly mixing) ---
(9) distinct classes {u/2 + H : u in K_Q, denominator <= 2000}: 2 [(Fraction(-1, 2), Fraction(0, 1)), (Fraction(-992, 1985), Fraction(-63, 3970))]
(C5) classes of {m/4 + H : m in Z[i], 0<=a,b<4}: 15
```

**How to read the controls.**
- (C1) The properness checker reports 300 / 300 failures for a non-unit displacement.
- (C2) It reports 866 failures for a different colouring.
- (C3) The invariance checker reports 159 / 300 for a non-unit multiplier.
- (C4) The membership test rejects (1+i)/2.
- (C5) The class counter reports 15 classes where 15 exist. So "2" in (9) is not an artefact of the counter.

**A control that I first got wrong.** My first version of (C2) used `U[:50]`, the 50 units with real part ≈ −1. Those act like displacement −1, which
always flips floor-parity, so the control printed 0 and could not fail. I replaced it with a random sample of units, and it now fails as it must.

Check (7)'s offsets 1/(2n+1) lie in H but not necessarily in G. Check (8) repeats the discontinuity using only sums of units (elements of G), which is
the case the argument in §5(A2) needs.

---------------------------------------------------------------------------------------------------------------------------------------

## 7. What §4 does NOT establish (for the record)
- The transfer is exactly as strong as Theorem 2.3. Nothing in §4 is a second line of defence.
- If Theorem 2.3 holds, the forward half of Theorem 1.3, plus Falconer's χ_m ≥ 5 argument adapted to weak colourings (Lemma 4.3 supplies the density-point input), would essentially re-prove χ(ℝ²) ≥ 5 with no finite graph. That is a large
  consequence, and it raises the stakes on the rigidity seat's verdict. It is not a contradiction.

---------------------------------------------------------------------------------------------------------------------------------------

## 8. Citation table (this scope)

The source is Bekka–de la Harpe–Valette, "Kazhdan's Property (T)", author manuscript dated 23 Feb 2007 (523 pp.). It was fetched from the paper's own
URL https://ncatlab.org/nlab/files/BekkaHarpeValetteOnKashdanPropertyT.pdf and saved as /tmp/oaimath/158/world/transfer_src/bhv.pdf (pdfinfo CreationDate
2007-02-23, matching the paper's "Theorem locators refer to the author manuscript dated February 23, 2007").

| Cited | Paper's use | Source (quote) | Verdict |
|---|---|---|---|
| [1, Thm D.2.2] | Bochner on ℝ² (Lemma 4.1) | "Theorem D.2.2 (Bochner) Let ϕ be a continuous function of positive type on G. There exists a finite positive Borel measure µ on Ĝ such that µ̂ = ϕ." | MATCH |
| [1, Thm D.3.1] | spectral (SNAG) theorem for E_disc (Lemma 4.1) | "Theorem D.3.1 (SNAG Theorem) (i) Let (π, H) be a unitary representation of the locally compact abelian group G. There exists a unique regular projection valued measure E_π : B(Ĝ) → Proj(H) on Ĝ such that π(x) = ∫_Ĝ x̂(x) dE_π(x̂)…" | MATCH |
| [1, Thm G.2.1] | abelian groups are amenable | "Theorem G.2.1 (Markov-Kakutani) Every abelian topological group G is amenable." | MATCH |
| [1, Prop G.2.2(ii)] | extension of amenable by amenable | "(ii) Let N be a closed normal subgroup of G. If N and G/N are amenable, then G is amenable." | MATCH (N = E, G/N ≅ K) |
| [1, Thm G.5.1] | Følner sets | "(ii) (Følner's Property) for every compact subset Q of G and every ε > 0, there exists a Borel subset U of G with 0 < \|U\| < ∞ such that \|xU △ U\|/\|U\| ≤ ε, for all x ∈ Q" | MATCH (compact = finite in a discrete group) |
| [8] Falconer; [22] Payne, Lemma 1 & Prop. 1 | Lemma 4.3 attribution | not fetched: Lemma 4.3 is outside Theorem 1.1's chain (test E); the sources seat has it | COULD NOT FETCH (not attempted, out of scope) |
| [4, Thm 1] de Bruijn–Erdős | converse in Thm 1.3 | sources seat | not checked here |

---------------------------------------------------------------------------------------------------------------------------------------

## 9. Verdict
- **§4 (Lemma 4.1, Proposition 4.2, the measurable sample, Lemma 4.3 as (E)):** HOLDS AS READ, conditional on Theorem 2.3. Objections T1–T6 are UNCLEAR/COSMETIC.
- **Lean, tests (C) and (D):** `measure k ω` is an E- and K-invariant Borel probability on the compact space of proper k-labelings of Q̄ ⊂ ℂ, averaged from the
  base point c\|_E. There is no hypothesis beyond `ProperColoring` (and `NeZero k`). The Lean proves Proposition 4.2 by a partly different, valid route
  (contraction-positivity, easy-half spectral, every-x measurable version). Theorem 2.3 enters only through `residual_fourier` → `wild_fourier`, and the
  supplied hypotheses match exactly.
- **Test (A):** §4 is generic. The transfer stands or falls with Theorem 2.3, which is false for (Q(i), K_Q) on the measure §4 itself produces. The
  Q̄-specific inputs live in §2.4/§3: divisibility of K, √ in F, and ℤ[K] = E. They do **not** live in §4, and the Q(i) counterexample is **not** caught by
  Lemma 2.4 or Lemma 2.5. **COULD NOT CHECK** Theorem 2.3 itself: out of this seat's scope; it is the rigidity seat's.
