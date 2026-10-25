# Referee report, seat `whole`: the dependency graph, tests (A) and (B) at the level of the whole argument, the formal statement

Paper: "The Euclidean plane is not five-colorable" (OpenAI, 23 Sep 2026, 62 pp.), local copy /tmp/oaimath/158/paper/paper.pdf. Quotes are from the PDF; page numbers are PDF pages, which equal the printed pages.
Lean: /tmp/oai-math/oai-sparse/lean at openai/math 1581d4c, Mathlib d13f23b. I did not run lean or lake myself. Where I cite a kernel or replay result, it comes from the log files in /tmp/oaimath/158/lean-build/ and I say so.
Scripts and outputs: /tmp/oaimath/158/seats/whole_scripts/. Fetched sources: /tmp/oaimath/158/world/whole/.

---------------------------------------------------------------------------------------------------
## 0. Verdict in one paragraph

**Dependency graph.** The architecture holds as read. Theorem 1.1 is derived from the forward half of Theorem 1.3 (Proposition 4.2) plus Theorem 1.4. Every hypothesis of every lemma on that path is supplied where it is needed.
- Ergodicity is assumed only inside the ergodic case of Theorem 2.3, and it is removed explicitly by ergodic decomposition on the last paragraph of §3.5.
- Invariant means are used only through positivity and linearity of the functional I. No limit is ever taken along an invariant mean as if it were a sequence.
- The amenable averaging is sequential: a Følner sequence on a compact metrizable space.

**Test (A) passes.** The transfer genuinely uses properties of F = Q̄∩ℝ that the rational unit circle lacks. The first such use is Lemma 2.7, p. 13: "Each |x_j| < 1 is a sum of two elements of K … The square roots belong to F." Over Q(i), with K_Q the rational unit circle, the rigidity Theorem 2.3 is false; I give explicit counterexamples, checked by exact arithmetic. So the method proves nothing for Payne's rational graph, as it must not.

**Test (B) passes.** Five is used essentially in at least five places in §§5–8. At six labels the first step that breaks is Proposition 5.6, where the complement of a triple is a pair only when k = 5. The hexagonal 7-colouring shows the §5–8 chain must fail at k = 7, and it does fail, at the k-dependent step §8.4.

**Statement.** `no_proper_five_coloring` is Theorem 1.1's first sentence: no 5-colouring of ℂ ≅ ℝ² with the Euclidean modulus is free of monochromatic unit pairs. It is the lower-bound half of the problem page's question, not the whole question. `WeakColoring` is equivalent to Definition 1.2, though not verbatim. Nothing in the 70-module closure weakens the statement or makes it vacuous: there are no axioms or `sorry`s, and the only `Fact` is 0 < 2π.

**A new observation (§5 below).** Proposition 4.2's proof never uses that the forbidden distance is 1. Read verbatim with any set of real-algebraic distances and combined with Furstenberg–Katznelson–Weiss, the method would also settle Soifer's 2ⁿ-distance problem and Kahle's n!-distance problem. Davies–McCarty–Pilipczuk (2023) list both as open. This is not a contradiction: everything it predicts that is already known is true. But the paper's transfer is a much bigger theorem than advertised.

---------------------------------------------------------------------------------------------------
## 1. STATEMENT READING (Lean)

Files read in full: ComparatorChallenges/EuclideanFiveColor.lean and .json, OAI/Geometry/PlaneColoring/{Five,Coloring,Basic,WeakColoring}.lean. Also read: PlaneSpectrum/Basic.lean lines 1–130, BorelTransfer.lean lines 420–450, and the FullApprox and PlanarCover signatures. I grepped all 70 modules in /tmp/oaimath/158/lean-build/order.txt (30,336 lines).

What each declaration says, in plain words:

- **`ProperColoring k c`** (Coloring.lean: `∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y`). The function c : ℂ → Fin k gives different colours to any two complex numbers at Euclidean distance exactly 1. The comparator's version (`∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 → coloring point ≠ coloring otherPoint`) is the same term up to binder names.
  - The norm is Mathlib's `Complex.instNorm` (Mathlib/Analysis/Complex/Norm.lean:28–29: `instance instNorm : Norm ℂ where norm z := √(normSq z)`), i.e. √(re² + im²).
  - The replay's own alpha-normalised comparison of the elaborated `pp.all` terms reports `DEF_ProperColoring(alpha-normalised binders) MATCH` (lean-build/statement_match.txt). Its kernel bridge, probe/CmpBridge.lean, copies the comparator text verbatim and proves it with the solution's theorem; it reports `'Cmp.no_proper_five_coloring' depends on axioms: [propext, Classical.choice, Quot.sound]`. The control with distance 2 fails to typecheck, as it should (logs/cmp_bridge_wrong.log). These are logs, not my runs.
- **`no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c`**. Every function from the plane to a 5-element set has two points at distance exactly 1 with the same value. No measurability is imposed. This is Theorem 1.1's first sentence ("no proper five-coloring, even when arbitrary color classes are allowed"), i.e. χ(ℝ²) ≥ 6.
  - It is **not** the problem page's statement verbatim. The page (live_508.txt) asks "What is the chromatic number of the plane? … the smallest number of colours … such that no two points of the same colour are distance 1 apart". The theorem settles the inequality χ > 5 only.
  - The upper bound χ ≤ 7 is formalised separately, in a different encoding: `OAI.Problem160.properColoring_seven` (ComparatorChallenges/PlaneColoring.json, Seven.lean, on `EuclideanSpace ℝ (Fin 2)` with `dist`).
  - Together the two catalogued declarations give 6 ≤ χ ≤ 7. "(Partial)" is the correct label for #508.
- **`angularMeasure`** = `AddCircle.haarAddCircle` on `AddCircle (2*Real.pi)`. This is the Haar probability measure; Mathlib's Fourier/AddCircle.lean:85 has "Haar measure on the additive circle, normalised to have total measure 1". It equals (2π)⁻¹ times the pushforward of Lebesgue measure on [0, 2π), i.e. normalised arc length in the angle variable.
- **`direction t`** = `AddCircle.toCircle t`. By Mathlib's `toCircle_apply_mk` (`toCircle x = Circle.exp (2 * π / T * x)`) with T = 2π, this is e^{it}. It is a measurable bijection from angles onto S¹, so it carries `angularMeasure` to the normalised arc length σ.
- **`WeakColoring k c`** = `AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure), c p.1 ≠ c (p.1 + direction p.2)`. In words: c is Lebesgue-measurable, and for almost every pair (point x, angle t), x and x + e^{it} get different colours.
  - `volume` on ℂ is Mathlib's inner-product-space Haar measure. `Complex.volume_preserving_equiv_real_prod` identifies it with Lebesgue measure on ℝ×ℝ.
  - Equivalence with Definition 1.2 (p. 2: "Σ_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0 for every R > 0 … The integrals use the completed product measure"). The monochromatic set M = {(x,u): c(x) = c(x+u)} is null for Leb⊗σ if and only if it is null on every B(0,R)×S¹ (σ-finiteness). Pulling back by (x,t) ↦ (x, e^{it}) preserves nullness. Mathlib's `∀ᵐ` is outer-measure nullness, which is the same as nullness for the completion. And AEMeasurable into the discrete Fin k is the same as Lebesgue measurability of each class.
  - So the two are **equivalent, not verbatim**.
  - Basic.lean contains the verbatim transcription, `OAI.Problem160.WeakMeasurableColoring`, built from `weakPairMeasure R` and a sum over i. It is **not in the import closure of Five.lean** (it is absent from order.txt) and is used only by the seven-colour file.
- **`no_measurable_weak_five_coloring {c} (hc : Measurable c) (hw : WeakColoring 5 c) : False`**. No **Borel** 5-colouring of the plane has product-null monochromatic unit pairs. This is formally weaker than Theorem 1.4, which is stated for Lebesgue-measurable c. It is equivalent after modifying c on a null set, and it is exactly what is needed, because the transfer outputs a Borel colouring.
  - The Lean route goes through `fullApprox_exists`: continuous maps from the closed disk of radius 5 into the realisation of K₅, agreeing with the threshold map off small disks. Then `graph_map_small_mesh_impossible` uses `PlanarCover.compact_open_cover_impossible` on `Metric.ball 0 5 ⊆ Q`, and `FullApprox.no_large_positive_sequence` runs the mesh argument of Lemma 7.6 with preconnected sets.
  - So the Lean's planar-cover region is a disk of radius 5. The paper's Lemma 7.5 uses "A closed square of side ten". Both contain a point at distance more than 2 from the boundary, which is all the Brouwer step uses.
- **`proper_to_borel_weak {k} [NeZero k] {c} (hc : ProperColoring k c) : ∃ d, Measurable d ∧ WeakColoring k d`**. For every k ≥ 1, an arbitrary proper k-colouring of the plane yields a Borel colouring with product-null monochromatic unit pairs. This is the forward half of Theorem 1.3. The Lean starts from `ω := ⟨fun x => c x, …⟩ : LabelModel.Space k`, i.e. the restriction of c to E.

Can anything make the formal theorem weaker than Theorem 1.1, trivially true, or vacuous? **No.**
- `grep` over the 70 modules for `axiom|opaque|unsafe|@[extern|implemented_by|sorry|admit|native_decide|macro|elab|run_cmd` finds nothing.
- Every `instance` in the closure either lives on a new type (D, DiscreteE, OrbitSpace, Func, Family, …), is `local` (Borel on `Circle`, `DecidableEq`), or is derived. None touches `Norm ℂ`, `MeasureSpace ℂ` or `Fin`.
- The only `Fact` is `anglePeriodPositive : Fact (0 < 2*Real.pi) := ⟨by positivity⟩`, which is true.
- `ProperColoring` is elaborated in Coloring.lean, which imports only Mathlib, so later instances cannot change its body.
- The internal definitions (`WeakColoring`, `angularMeasure`) do not occur in the comparator statement, so they cannot weaken it. And they are not degenerate: `angularMeasure` is a probability measure, so `WeakColoring` is not trivially satisfiable.
- The replay's axiom logs show `no_proper_five_coloring`, `no_measurable_weak_five_coloring`, `proper_to_borel_weak` and `proper_to_weak` all depend only on [propext, Classical.choice, Quot.sound] (logs/axioms.log). At the time of writing, the replay's `leanchecker --fresh` step was still running.
- Lean's E is `algebraicClosure ℚ ℂ` and K is the algebraic points of `Circle` (PlaneSpectrum/Basic.lean). These are exactly the paper's F(i) and K. The Lean also proves K divisible (`K_pow_surjective`, `instance K_rootable`) and uses it, like the paper's Lemma 2.4 (`fixed_of_finite_orbit`).

---------------------------------------------------------------------------------------------------
## 2. DEPENDENCY GRAPH (what each item needs, and where it is supplied)

Notation: ✓ means the hypothesis is supplied at the place named.

**Theorem 1.1** (p. 2) ← Theorem 1.3 forward (= Proposition 4.2) + Theorem 1.4. ✓ The deduction is one line. The upper bound (hexagons, r = 2/5) is checked numerically in §9.

**Theorem 1.3** (every k, ZFC):
- Forward: Proposition 4.2 ← {Lemma 4.1, Theorem 2.3, amenable averaging}.
- Converse: Lemma 4.3 + "a translate puts any finite configuration in the conull typical set" + product compactness. This uses choice (BPI) on {1..k}^{ℝ²}.

**Theorem 1.4** (k = 5) ← Proposition 7.1 (a label cycle of length 3, 4 or 5 with common exclusion continua) + Propositions 8.2, 8.5, 8.10.

**Corollary 1.5** ← Theorem 1.1 + de Bruijn–Erdős, which uses choice (BPI). (i) also needs left-invariance and finite additivity of μ. (ii) needs only the averaging I re-derive in §6. The citations [12] and [2] are not needed (Objection 6).

Transfer side (§§2–4):

| Item | Needs | Supplied by / where |
|---|---|---|
| Def 2.1 | F = Q̄∩ℝ, E = F(i), K; D = dual of E_disc (compact, metrizable since E countable); C = j(ℝ²) Borel (σ-compact image); "Every nonzero power map u ↦ uⁿ on K is onto" | algebraic closure ✓ |
| Lemma 2.4 | ν wild ⇒ (a) every coset of C is null, (b) the difference law of two independent samples is wild, (c) L_a is null. (a) uses "finite image of the divisible group K is trivial" and E a field (the inverse of u−1). (c) uses K infinite and L_a ∩ L_b ⊂ C | Def 2.1 ✓. Divisibility is not actually needed (Objection 2) |
| §2.2, I | translation-invariant mean on discrete F/ℤ (choice: Hahn–Banach / amenability, [1, Thm G.2.1]); agrees with Lebesgue on C_c | ✓ |
| Lemma 2.5 | ν wild + K-invariant; Lemma 2.4(c); Bochner on ℝ after extending a uniformly continuous positive-definite function; Fourier uniqueness on F̂_disc | ✓ |
| Lemma 2.6 | none (convex coercive objective; measurable selection over ℚ²) | ✓ |
| Lemma 2.7 | **X ergodic**, d equivariant with wild law, a countable tower satisfying (2.6). Base: Lemma 2.4(b). Step: ergodicity makes the coset mass constant; Lemma 2.6 gives the centres b; Z = Y ∨ σ(b) is again ergodic and standard; the induction hypothesis at the earlier factor W, applied in Z to b (the "universal" induction); Lemma 2.5 applied to p(a) = ‖E(ψ_a(b) \| W)‖²; **x_j = k_j + k'_j with k_j ∈ K (square roots in F)** | Lemma 3.1 supplies the tower; Theorem 2.3's proof supplies ergodic X = (D, μ) ✓ |
| Lemma 3.1 | X ergodic (rank constancy; (3.1) boundedness, Σ\|e_i\|² = d); separability for countable termination | ✓ |
| Lemma 3.2 | X ergodic, X ×_Y X ergodic; **power maps u ↦ u^d onto** for d up to 3 (the exponent shift in (3.9): 0,1,2 → 1,2,3) | Lemma 3.1(3); Def 2.1 divisibility ✓ |
| Lemma 3.3 | Lemma 3.2; Y ergodic; **L = √(AB) ∈ F**; **square map onto** in (3.15) and (3.13); radii \|z\| ∈ F | ✓ (F real closed) |
| Lemma 3.4 | N₀ a **number field** (finite degree) ⊂ F; Cayley parametrisation | holds already over ℚ |
| Lemma 3.5 | only w(0) = 0 and (3.12) | field-agnostic ✓ |
| §3.5 | (3.13) ⇒ A₀ syndetic; Lemma 3.4 (needs every q_j to lie in a number field, i.e. **F algebraic**); Lemma 3.5; "**Every t ∈ F∩[−1,1] is the real part of an element of K, namely t + i√(1−t²)**"; contradiction with Lemma 2.5 via positivity of I; then **ergodic decomposition** for a general wild ν (C invariant Borel, so a.e. component is wild) | ✓ |
| Lemma 4.1 | any measure-preserving E-action on a standard space; Koopman operators (for the factor property); Bochner on ℝ²; spectral theorem on E_disc. No ergodicity | ✓ |
| Prop 4.2 | Ω = proper labelings of E (compact metrizable); E⋊K countable and amenable; Følner averages of δ_ω, weak limit (sequential, no ultrafilter); (4.1) from properness; Lemma 4.1; Theorem 2.3 on the normalised spectral measure of b_i (K-invariant by covariance; C-null since b_i ⊥ H_c); K dense in S¹; joint measurable versions; one sample ω via Tonelli (countably many conditions) | ✓ |
| Lemma 4.3 | weak condition + Lebesgue density | ✓ |

On the brief's (E): **Lemma 4.3 IS on the critical path of Theorem 1.4**, even though the converse half of Theorem 1.3 is not. It supplies "typical-point properness":
- p. 26: "By Lemma 4.3, any unit pair of typical points has different colors";
- Lemma 5.2's (5.4): "Lemma 4.3 therefore gives a_i(y_n + r_n e) a_i(y_n + r_n e + v) = 0";
- Lemmas 6.2, 6.3, 6.4, 7.2 and 8.6, and Proposition 8.10 ("typical-point properness gives a proper three-coloring").

The Lean counterpart is `weak_density_proper` in WeakColoring.lean, which is in the closure. I verified Lemma 4.3 line by line (§8).

Obstruction side (§§5–8), all for one fixed Borel weak 5-colouring:
- Lemma 5.2 ← Lemma 4.3 and change of variables. Cor 5.4 ← 5.2(3). Lemma 5.5 ← 5.2(3) and (5.8). **Prop 5.6 ← (5.2), Cor 5.4, Lemma 5.5, compactness of the circle.**
- Def 6.1 is the transition graph. Lemma 6.2 ← circle Fourier decay |σ̂(ξ)| ≤ C(1+|ξ|)^{−1/2} and typical properness. Lemma 6.3 ← 5.2(2). Lemma 6.4 ← 5.2, an irrational rotation, and a unit triangle.
- Theorem 6.5 ← 6.2, 5.6, 5.4 and 5.5 (triangles); 6.3, 6.4, 6.6 (four-cycles); 6.7 (five-cycles).
- Lemma 7.2 ← typical properness. 7.3 ← Def 6.1. 7.4 ← Theorem 6.5 (local finiteness; forests off L) and 7.3. 7.5 ← Brouwer. 7.6 ← 7.2, 7.4, 7.5. 7.7 and 7.8 are topology. Prop 7.1 ← 7.4, 7.6, 7.7, 7.8, 7.2 and Hausdorff compactness.
- Lemma 8.1 ← Prop 7.1. Prop 8.2 ← 8.1, 5.6, 5.4. Props 8.3–8.5 ← 8.1, 6.3, 6.4, 5.4. Lemmas 8.6–8.7 ← 8.1 and 5.4. Lemma 8.8 ← 5.2 and Lemma 8.7. Prop 8.10 ← 8.8, 8.9 and the Moser spindle.

Where things are taken:
- **"almost every"**: always at a fixed centre or for countably many group elements. Remark 5.3 is explicit: "never needs a common exceptional angular set over an uncountable family of centers".
- **limits**: weak-* limits in L∞(S¹), which is sequentially compact because L¹ is separable; Hausdorff limits; Følner limits. None is taken along an invariant mean.
- **compactness**: D, Ω, the weak-* ball, the hyperspace, S¹, and the uncountable product in the converse.
- **choice**: the colouring itself, the invariant mean on F/ℤ, the converse compactness, de Bruijn–Erdős in Corollary 1.5.

---------------------------------------------------------------------------------------------------
## 3. TEST (A): Payne's rational graph, and what the method proves for a general countable field or direction group

### 3.1 Which properties of F(i)/K the proof uses

| Property | Where it is used (verbatim) | Holds for Q(i), K_Q? |
|---|---|---|
| E is a field, so u−1 is invertible | Lemma 2.4, p. 7: "Taking u ≠ 1 and applying the inverse scalar shows d ∈ C" | yes |
| K divisible (u ↦ uⁿ onto) | Lemma 2.4, p. 7: "a finite abelian group cannot be divisible unless it is trivial" (**not essential**, Objection 2). §3.2, p. 16: "the representation u ↦ U_{u^d}, for d ∈ ℤ∖{0}, has the same invariant vectors as U, because the power map u ↦ u^d is onto" (essential for (3.4), (3.13), (3.15)) | **no**: (3+4i)/5 has no square root in K_Q (script check 4) |
| **F Euclidean** (√ of positives in F) | **Lemma 2.7, p. 13: "Each \|x_j\| < 1 is a sum of two elements of K. One explicit choice is k_j = x_j/2 + i√(1 − x_j²/4), k'_j = x_j/2 − i√(1 − x_j²/4). The square roots belong to F"**. Lemma 3.3, p. 19: "put L = √(AB) ∈ F". §3.3, p. 18: "Thus m is radial; its radii lie in F_{≥0}". §3.5, p. 21: "Every t ∈ F ∩ [−1, 1] is the real part of an element of K, namely t + i√(1 − t²)" | **no**: among x = p/q ∈ (0,2) with q ≤ 60, only 16 of 2,203 are sums of two rational units; no t = p/q ∈ (0,1) with q ≤ 400 has t, 2t, 3t all such sums (script check 3) |
| F algebraic (q_j in a number field) | §3.5, p. 21: "Choose a number field N₀ ⊂ F containing the real and imaginary parts of every q_j" | yes |
| number-field general position | Lemma 3.4 | yes: over ℚ, d₀ = 2 and the Cayley points (1+it)/(1−it) are pairwise ℚ-independent unless antipodal |
| Fourier decay of circle measure | Lemma 6.2 only. **Not used in the transfer** | n/a |

### 3.2 The rational analogue of Theorem 2.3 is FALSE (so the proof must break somewhere on the list above)

**(i) Haar on an annihilator.** Let G = span_ℤ(K_Q) ⊂ Q(i). Every rational unit has odd denominator c, and every prime factor of c is ≡ 1 (mod 4); script check 1 finds this for all 3,820 units with c ≤ 3000. Hence G ⊂ ℤ[i][1/p : p ≡ 1 mod 4], and 1/3 ∉ G. So G is a proper K_Q-invariant subgroup.
- H = G^⊥ ⊂ D_Q is a nontrivial compact K_Q-invariant subgroup. It is infinite, since Q(i)/G contains elements 1/3ⁿ of order 3ⁿ.
- H ∩ C = {0}: a continuous character trivial on the dense set G is trivial.
- So m_H is K_Q-invariant and atomless, gives C (that is, {0}) measure 0, i.e. it is wild, and has Fourier coefficient 1 on G. It is not Haar on D_Q.
- Over F(i) this cannot happen. span_ℤ(K) contains u + ū = 2Re u for all u, hence all of F (Euclidean), and it is K-invariant, hence it equals E. A K-invariant subgroup of E is an E-submodule, so it is 0 or E. (Script check 2 shows the exact witness 1/3 = 1 − (u + ū) with u = (1+2√2 i)/3 ∈ K.)

**(ii) The coset S coming from the 2-colouring.** The parity map π((a+bi)/c) = a+b mod 2 (c odd) is a homomorphism Z_(2)[i] → ℤ/2. It is invariant under multiplication by K_Q, and π(u) = 1 for every rational unit (script check 1: 3,820/3,820 units; 20,000/20,000 random additivity and rotation-invariance trials; and among 72 integer relations between small units, none has odd coefficient sum).
- Extend χ = (−1)^π from span(K_Q) to Q(i); this is possible because 𝕋 is divisible.
- Then S = {d ∈ D_Q : d(u) = −1 for all u ∈ K_Q} is nonempty, closed, K_Q-invariant, and disjoint from C. A continuous character equal to −1 on a dense subset of S¹ would equal −1 on all of S¹, which is impossible.
- Any K_Q-invariant probability on S (which exists by Markov–Kakutani) is wild, with f_ν(u) = −1 ≠ 0.
- This S is exactly where the spectral measure of 1_{c=0} − 1_{c=1} lives, for Woodall's/Payne's proper 2-colouring of the K_Q-edge graph on Q(i).
- **Control that FAILS.** Over F(i), S = ∅: 1 + ω + ω² = 0 with ω = e^{2πi/3} ∈ K forces d(0) = (−1)³ = −1 ≠ 1.

**(iii) The transfer itself is false for Q(i).** The rational analogue of Proposition 4.2 would turn that proper 2-colouring of the graph on Q(i) into a weak measurable 2-colouring of ℝ². Proposition 4.2 extends zero correlations from K_Q to all of S¹ "by density", and K_Q is dense. But no weak measurable 2-colouring of ℝ² exists: by Lemma 4.3, density points of a weak colour class contain no unit pair, so a unit equilateral triangle among typical points would be properly 2-coloured. So Q(i) is a genuine counterexample to the transfer, as Payne and p. 1 of the paper say.

**Where exactly the Q(i) version of the proof stops.** Lemmas 2.4 and 2.5 go through over Q(i):
- 2.4(a) via finite-index stabilisers plus the field property;
- 2.4(c) verbatim;
- 2.5 verbatim, with F/ℤ = ℚ/ℤ.

Lemma 3.1 applies too. Take any ergodic component μ of m_H from (i). Such a component exists, and it is atomless (hence wild, since μ(C) = μ({0}) = 0) and not Haar on D_Q (it lives on the Haar-null subgroup H). Atomless: the only finite K_Q-orbit in D_Q is {0}, because a d fixed by a finite-index subgroup satisfies (u−1)d = 0 for some u ≠ 1, so d = 0; and m_H({0}) = 0.

The K_Q-action on H is isometric. The groups (Q(i)/G)[n] ≅ G/nG are finite and K_Q-invariant, and their annihilators form a K_Q-invariant neighbourhood base of 0, i.e. an invariant ultrametric. So (H, μ) is a compact (isometric) system. Lemma 3.1's compact tower therefore runs all the way to X itself. There the conditional difference law is δ₀, which gives C mass 1. So **Lemma 2.7's conclusion is false over Q(i)**.

In Lemma 2.7's inductive step, every sentence before p. 13 is field-agnostic: positive-mass cosets, centres via Lemma 2.6, the phase encoding, the approximations (2.9), the induction hypothesis in Z, and the choice of t from Lemma 2.5. The first sentence that is not is "Each |x_j| < 1 is a sum of two elements of K … The square roots belong to F" (p. 13). The proof would then fail again at §3.2's surjective power maps, at Lemma 3.3's L = √(AB), and at §3.5's t + i√(1−t²).

**Divisibility alone is not the point.** For E = Q(μ_∞) with the divisible dense direction group μ_∞ of roots of unity, span_ℤ(μ_∞) = ℤ[μ_∞] ∌ 1/2. So Haar on its annihilator is again a wild, μ_∞-invariant, non-Haar law. The decisive property is span_ℤ(K) = E with explicit two-term decompositions x = u + ū, which is what Euclidean closure of F buys.

### 3.3 What the method proves, stated for a general countable field (my reconstruction from the hypotheses actually used)

> **Theorem A.** Let F ⊂ ℝ be a subfield such that
> - (H1) every element of F is algebraic over ℚ;
> - (H2) every positive element of F has a square root in F;
> - (H3) on K := {u ∈ F(i) : |u| = 1} the maps u ↦ u² and u ↦ u³ are surjective.
>
> Put E = F(i), D = (E_disc)^, C = j(ℝ²). Then:
> - (i) every K-invariant Borel probability ν on D with ν(C) = 0 is normalised Haar measure;
> - (ii) for every k ≥ 1, if the graph on E joining z, z' with |z − z'| = 1 has a proper k-colouring, then ℝ² has a weak measurable k-colouring (Definition 1.2).
>
> F = Q̄∩ℝ satisfies (H1)–(H3), and it is the only real-closed field satisfying (H1). For F = ℚ, (H2) and (H3) fail, and (i) and (ii) are false (§3.2).

Two remarks on Theorem A:
- (H3)'s cube roots enter only through the shift of exponents {0,1,2} → {1,2,3} in (3.9). Every admissible shift s has max{|s|, |s+2|} ≥ 3. So the Euclidean closure of ℚ, whose K is not 3-divisible, is not covered as written.
- Since a finite unit-distance graph realisable in ℝ² is realisable in F(i) (Tarski transfer), the hypothesis of (ii) is equivalent to "ℝ² has a proper k-colouring".

**Verdict on (A): PASSES.** The transfer uses F-specific properties at named steps, and its rational analogue is provably false.

---------------------------------------------------------------------------------------------------
## 4. TEST (B): where five is used, and what breaks at six

§§2–4 never use k: `proper_to_borel_weak` is stated for every k with `NeZero k`. In §§5–8 the label count enters at the following places:

1. **Proposition 5.6, p. 33–34**: "some fixed triple A ⊂ {1, …, 5} is contained in P_x(e) … the actual coloring on the circle v ↦ x + e + v uses only the complementary pair {1, …, 5} ∖ A almost everywhere." Here 5 − 3 = 2 is what makes x + e *binary*, so that Lemma 5.5 applies.
   - With k labels the argument yields |P| ≤ k − 3. At **k = 6** it gives only |P| ≤ 3: the complement of a triple is a triple, and a 3-label circle is not binary. **This is the first step that breaks at six.**
2. **Theorem 6.5**: "There are only finitely many simple cycles on five labels … separately for each triangle, four-cycle, and five-cycle."
   - The triangle case: "force P_x(e) to intersect the pair of outside labels … binary for that fixed pair". This needs 5 − 3 = 2 outsiders.
   - Four-cycles have one outsider X. Lemma 6.3 needs represented groups whose union is I∖{X}. Lemma 6.4 needs "the two labels outside {X} ∪ D".
   - Five-cycles use the Z/5 diagonals D_i = {i, i+2}.
   - At six there would be three outsiders for a triangle, two for a four-cycle, a new case for five-cycles, and new six-cycles.
3. **Lemma 6.4, p. 37**: "density one at each z_j to the union of the two labels outside {X} ∪ D … unit equilateral triangle would be properly colored with two labels". At six there would be three labels, and the triangle is then 3-colourable.
4. **§7.2**: "Fix 0 < α < 1/5", and G is the 1-skeleton on five vertices. The graph-valuedness itself (≤ 2 positive coordinates) comes from the forests Γ_z, not from the number five. The cover multiplicity 2 is what Lemma 7.5 needs: a plane cover of multiplicity 3 with small mesh exists (hexagons), so multiplicity is the dimension-theoretic heart.
5. **§8**: ℓ ∈ {3,4,5}.
   - Proposition 8.2 uses ℤ/5 arithmetic ("six equal steps do not close modulo five").
   - §8.4 says "write X, Y for the outsiders … There cannot be two outsiders in such a palette, since (5.7) would leave no outsider at Re". That needs **exactly two** outsiders.
   - Lemma 8.8 and Proposition 8.10 need the open region to use **three** labels, because the Moser spindle is not 3-colourable but is 4-colourable (my enumeration: 0 proper 3-colourings, 384 proper 4-colourings).
   - At six, a triangle has three outsiders and the region keeps four labels.

**Hexagonal 7-colouring sanity run.** The hexagonal 7-colouring is a proper, hence weak measurable, 7-colouring, so the §5–8 chain must fail at k = 7. Tracing it:
- palettes have ≤ 2 labels a.e., because unit circles cross hexagon edges transversally;
- the cyclic centres are the triple points, which are locally finite;
- §7 finds a loop around a triple point, a 3-cycle, with continua along the three boundary segments;
- the exclusion Δ(K_j) is consistent with properness;
- and the chain first fails at §8.4's binary-outsider step, since there are 4 outsiders.

So the failure happens exactly at a k-dependent step and not earlier. Nothing in §§5–8 proves something false at k = 7.

**Verdict on (B): PASSES.** Five is used essentially. At six, Proposition 5.6 breaks first; even granting palettes of size ≤ 2, Theorem 6.5's triangle case, Lemma 6.4, §8.4 and Lemma 8.8 break. No bigger k-theorem is left on the table.

---------------------------------------------------------------------------------------------------
## 5. A SECOND PROVE-TOO-MUCH TEST: the distance set. The transfer is far stronger than stated

Proposition 4.2 uses the number 1 in only three places: in Ω (properness on E), in (4.1) ("∫ f_i T_u f_i dμ = 0 (u ∈ K)"), and in the density of K in S¹. Theorem 2.3 does not involve the graph at all.

Replace "unit" by any set Δ ⊂ F_{>0} of real-algebraic distances:
- take labelings of E with no monochromatic pair at a distance in Δ;
- (4.1) then holds for z = d·u with d ∈ Δ, u ∈ K;
- dK is dense in dS¹.

The proof goes through word for word. It gives: **a proper k-colouring of the plane avoiding Δ yields a Lebesgue-measurable k-colouring c with c(x) ≠ c(x + du) for (Leb⊗σ)-a.e. (x,u), for every d ∈ Δ.**

Combine this with Furstenberg–Katznelson–Weiss / Bourgain: a measurable set of positive upper density contains all sufficiently large distances, and their proofs give positive pair measure, which is the weak form. The result is:

> **for every unbounded set Δ of real-algebraic numbers, every finite colouring of ℝ² has a monochromatic pair at a distance in Δ.**

Checked against the literature (fetched; quotes from /tmp/oaimath/158/world/whole/):
- **Consistent with everything known.**
  - Davies 2022 (arXiv 2209.15598): "every finite colouring of the plane contains a monochromatic pair of points at an odd distance". This is Rosenfeld's problem, which is now solved.
  - Davies–McCarty–Pilipczuk 2023 (arXiv 2308.02483): prime distances, and values of integer polynomials.
  - The method would re-derive all of these.
- **Settles listed open problems.** DMP 2023, §5:
  - "Problem 5.4 (Soifer [27]). Is there a ﬁnite colouring of R² containing no monochromatic pair of points whose distance is equal to 2ⁿ for some n ∈ N?"
  - "Problem 5.5 (Kahle [27]). … equal to n! …"
  - "we do not know of a single inﬁnite subset of N for which the plane has a ﬁnite colouring avoiding those distances … we conjecture that both of the problems above should have negative answers".
  - The generalised transfer answers both negatively, in the conjectured direction.
- **No clash with Bukh.** DMP Conjecture 5.6 (Bukh): "Let A ⊂ R>0 be algebraically independent. Then there is a finite colouring of R² containing no monochromatic pair …". Algebraically independent sets consist of transcendental numbers, which E never sees. The method's reach stops exactly where Bukh conjectures it should.

So this is not a refutation. It is a strong "bigger theorem on the table" signal. The novelty, and the risk, of the whole paper sits in Theorem 2.3 (with Lemma 4.1). Theorem 2.3 is equivalent to: every K-invariant positive-definite function on E_disc is a continuous radial positive-definite function restricted to E, plus c·1_{z=0}. That is a discrete, non-measurable analogue of the Crum / Gneiting–Sasvári decomposition the paper cites on p. 6–7. Its ℚ(i) analogue is false (§3.2). The kernel replay is the decisive instrument for it.

I could not fetch Moshchevitin–Raigorodskii, "Colorings of the space ℝⁿ with several forbidden distances", Math. Notes 81 (2007) 656–664 (DOI 10.1134/s0001434607050112; Springer and math-net returned redirect/refused). By its title it concerns finitely many forbidden distances. DMP's 2023 sentence above is the best evidence that no known finite colouring of ℝ² avoids an infinite set of integer distances.

---------------------------------------------------------------------------------------------------
## 6. COROLLARY 1.5 and its half-page proof: VERIFIED (re-derived)

**(i)** Let H be the finite non-5-colourable unit-distance graph from Theorem 1.1 + [4, Thm 1], and m = |E(H)|. For an edge e = {a,b} pick an isometry S_e with S_e0 = a and S_e1 = b. Put M = {T : c(T⁻¹0) = c(T⁻¹1)}. Then S_e M = {T : c(T⁻¹a) = c(T⁻¹b)}.
- For every T, v ↦ c(T⁻¹v) 5-colours H, so it has a monochromatic edge. Hence ∪_e S_e M = E(2).
- Finite subadditivity and left-invariance give m·μ(M) ≥ 1. ✓

**(ii), periodic case.** Let X be uniform on a fundamental domain and R an independent uniform rotation. For each edge, (X + Ra mod Λ, R(b−a)) is distributed as (uniform on the torus) ⊗ σ. Every realisation of v ↦ c(X + Rv) has a monochromatic edge, so Σ_e P_e ≥ 1 with each P_e = P(c(A) = c(A+U)). ✓

**(ii), asymptotic case.** The same coupling on [−R,R]² differs from (A_R, U) by O(diam H / R) in total variation, and conditioning on A_R + U ∈ [−R,R]² costs O(1/R). So the lim inf is at least 1/m. ✓

The proof needs only [4]. The citations "[12, Lemma 2.10 and Theorem 2.11]" and "[2, Theorems 1–2]" are decorative here; the sources seat checks them.

---------------------------------------------------------------------------------------------------
## 7. OBJECTIONS (numbered)

1. **Brief mis-scopes (E); not a paper defect.** The brief says "(E) THE DENSITY-POINT CONVERSE is not needed for Theorem 1.1 (only proper ⇒ weak is used)". The converse *implication* is indeed unused. But **Lemma 4.3 is load-bearing for Theorem 1.4**: p. 26, "By Lemma 4.3, any unit pair of typical points has different colors"; (5.4) on p. 28; and Lemmas 6.2–6.4, 7.2, 8.6 and Proposition 8.10. Severity: N/A for the paper. I verified Lemma 4.3 line by line, and it holds. Fix: the seats' scopes should include Lemma 4.3.
2. **Lemma 2.4, p. 7: COSMETIC.** "The action on this finite orbit gives a finite image of the divisible abelian group K. Such an image is trivial: a finite abelian group cannot be divisible unless it is trivial." Divisibility is overkill. A finite orbit has a stabiliser of finite index, which contains some u ≠ 1; then (u−1)d ∈ C gives d ∈ C because E is a field. The Lean mirrors the overkill (`fixed_of_finite_orbit` with `[RootableBy G ℕ]`). It matters only for test (A): divisibility is *not* what separates F(i) from ℚ(i) at this step.
3. **Exposition gap (UNCLEAR → reconstructed in §3.3).** The paper never states which properties of F and K the transfer needs. (H1) algebraic, (H2) Euclidean and (H3) 2- and 3-divisible are used silently at Lemma 2.7 (p. 13), §3.2 (p. 16), Lemma 3.3 (p. 19), §3.3 (p. 18) and §3.5 (p. 21). Given Payne's graph (cited by the paper itself on p. 1), a referee would require the authors to say where the rational graph fails. The answer: first at Lemma 2.7's k_j decomposition. This is a gap in the EXPOSITION, not the PROOF. Fix: state Theorem A (§3.3) and the ℚ(i) counterexample.
4. **Scope of the transfer (UNCLEAR, not an error).** The transfer works verbatim for any set Δ ⊂ F_{>0} of forbidden distances (§5). With FKW it would answer Soifer's 2ⁿ problem and Kahle's n! problem (DMP 2023, Problems 5.4–5.5) negatively. The paper is silent on this. It is consistent with all known results (Davies 2022; DMP 2023), but it raises the stakes of Theorem 2.3 considerably. Fix: the authors should state the Δ-version, or explain why it fails if it does.
5. **(8.6) wording, p. 57: COSMETIC.** The text reads "The multiplier has norm one because 35² + 12² = 37², so this is a rotation followed by a translation". But the displayed formula is z_g = ((35+12i)/37)(g + (−290+149i)/250), which is a translation followed by a rotation. The formula is the correct one and matches Table 1. Read literally ("rotation followed by a translation" by the displayed vector), the placement puts z₀, z_{uB} and z_{uT} *outside* the region (8.4); my control run shows this (§9).
6. **Corollary 1.5 citations: COSMETIC.** The proof is self-contained given [4]; the citations [12] and [2] can be dropped or reduced to "compare".
7. **The brief's numbering, for the continua seat.** The planar cover obstruction is the paper's **Lemma 7.5** ("A closed square of side ten has no relatively open cover of multiplicity at most two and mesh at most two"), not Lemma 7.2. The Lean version is on a disk of radius 5 (`Metric.ball (0:ℂ) 5 ⊆ Q`), with mesh ≤ 2 and multiplicity ≤ 2 ("any three members through a point have two equal"). The two are mathematically interchangeable for the Brouwer argument.

**No FATAL objection in my scope.** I found no GAP in the PROOF along the dependency path, at the level I could verify (see §8 for what I only skimmed).

---------------------------------------------------------------------------------------------------
## 8. STATUS PER ITEM (my reading, in my scope)

| Item | Status |
|---|---|
| Abstract, §1 intro, Thm 1.1 + its deduction, Def 1.2, Thm 1.3/1.4 statements | VERIFIED LINE BY LINE |
| p. 2–3 hexagon upper bound (r = 2/5; √21 r; \|2−ω\|² = 7) | VERIFIED (numeric check §9) |
| Footnote 1, Reed arc: chord 2 sin(\|t−s\|/2) < 1 on a half-open arc of length π/3 | VERIFIED (arithmetic only; the manuscript itself is the sources seat's) |
| §1.1 overview, Fig. 1 | VERIFIED as an accurate map of §§2–8 |
| Cor 1.5 + proof | VERIFIED (re-derived, §6) |
| Def 2.1 and the following paragraph (divisibility, metrizability, j injective, C Borel, j⁻¹ Borel, action on C) | VERIFIED LINE BY LINE |
| Def 2.2, Thm 2.3 statement | VERIFIED |
| Lemma 2.4 | VERIFIED LINE BY LINE (Objection 2) |
| §2.2 functional I | VERIFIED |
| Lemma 2.5 | VERIFIED LINE BY LINE |
| Lemma 2.6 | VERIFIED |
| §2.4 disintegration preamble | SKIMMED |
| Lemma 2.7 | logic VERIFIED: base case; positive-mass cosets via ergodicity; centres; application of the induction to Z and W; selection of t by positivity of I; k_j step; all numerical constants (Markov 20γ²/τ² < 0.001; Chebyshev 18τ²/s² = 0.0018; \|J\| > 10m²; 0.95² − 0.1 > 1/4). The measure-theoretic infrastructure ((2.9) at limit ordinals, conull equivariance, measurability of the phase encoding) SKIMMED. Rigidity seat |
| Lemma 3.1 | SKIMMED (checked rank constancy, (3.1), strictness, (2.6) from unitary coefficient matrices, countable termination) |
| Lemma 3.2 | SKIMMED (checked where divisibility enters; the vdC induction is standard) |
| Lemma 3.3 | VERIFIED LINE BY LINE (identity (3.14) checked by hand; the ψ-factorisations; (3.13)) |
| Lemma 3.4 | VERIFIED LINE BY LINE (series 1 + 2iha − 2h²a² …; nonvanishing of the norm 1 − it) |
| Lemma 3.5 | VERIFIED LINE BY LINE |
| §3.5 incl. ergodic decomposition | VERIFIED LINE BY LINE |
| Lemma 4.1 | VERIFIED |
| Prop 4.2 | VERIFIED at the argument level (invariant law, rotation-fixedness, K-invariance of the spectral measure, cross terms, extension to S¹, (4.2), sample selection, least-index rule). Joint-measurable construction SKIMMED. Transfer seat |
| Lemma 4.3 | VERIFIED LINE BY LINE |
| Proof of Thm 1.3 (converse) | VERIFIED |
| §5.1, Def 5.1, (5.1) | SKIMMED |
| Lemma 5.2 | SKIMMED |
| Cor 5.4 | VERIFIED (Rf + R⁻¹f = 2cos(π/3) f = f) |
| Lemma 5.5 | SKIMMED (expansions (5.9)–(5.11) read, not recomputed). Palettes seat |
| Prop 5.6 | VERIFIED LINE BY LINE given 5.2, 5.4, 5.5 |
| Def 6.1, Lemma 6.2, Lemma 6.3 | SKIMMED |
| Lemma 6.4 | VERIFIED (cos γ = 5/6; γ/π irrational; \|1−e^{iγ}\| = 1/√3; triangle side 1) |
| Thm 6.5: triangle case | VERIFIED |
| Thm 6.5: four-cycles (Lemma 6.6, transport, accumulation) and five-cycles (Lemma 6.7, accumulation) | SKIMMED |
| Lemma 7.2 | VERIFIED |
| Lemmas 7.3, 7.4 | SKIMMED |
| Lemma 7.5 | VERIFIED LINE BY LINE |
| Lemmas 7.6–7.8, Prop 7.1 | SKIMMED. Continua seat |
| Lemma 8.1 | SKIMMED |
| Prop 8.2 | VERIFIED LINE BY LINE given 8.1, 5.6, 5.4 |
| Lemma 8.3, Lemma 8.4, Prop 8.5, Lemmas 8.6–8.7 | SKIMMED |
| Lemma 8.8 | VERIFIED (sin 3φ = υ(3ξ²−υ²)/r³; sin 3δ = √(1−l/4)(l−1); product formula) |
| Lemma 8.9 / §8.6 | numeric cross-check only (60 digits). The exact rational check belongs to the cycles seat |
| Prop 8.10, proof of Thm 1.4 | VERIFIED given the above |
| References | NOT READ (sources seat), except those cited in §5 |

---------------------------------------------------------------------------------------------------
## 9. FINITE CHECKS (scripts verbatim, outputs, failing controls)

### 9.1 /tmp/oaimath/158/seats/whole_scripts/testA_rational.py
```python
# Test (A): the rational analogue of Theorem 2.3 / Prop 4.2 is FALSE, and the
# F(i)-specific inputs the proof uses fail over Q(i).  Exact arithmetic only.
from fractions import Fraction as Fr
from math import gcd, isqrt
import itertools, random
random.seed(1)

def factor(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p); n//=p
        p+=1
    if n>1: f.append(n)
    return f

# (1) all rational unit vectors (a+bi)/c with c <= N: primitive triples + axes
N=3000
units=set([(Fr(1),Fr(0)),(Fr(-1),Fr(0)),(Fr(0),Fr(1)),(Fr(0),Fr(-1))])
bad_c_even=bad_parity=bad_prime=0
for m in range(2,isqrt(N)+2):
    for n in range(1,m):
        if (m-n)%2==0 or gcd(m,n)!=1: continue
        a,b,c=m*m-n*n,2*m*n,m*m+n*n
        if c>N: continue
        if c%2==0: bad_c_even+=1
        if (a+b)%2==0: bad_parity+=1
        if any(p%4!=1 for p in factor(c)): bad_prime+=1
        for x,y in ((a,b),(b,a)):
            for sx in (1,-1):
                for sy in (1,-1):
                    units.add((Fr(sx*x,c),Fr(sy*y,c)))
for (x,y) in units: assert x*x+y*y==1
print("rational units with denominator <=",N,":",len(units))
print("  even denominators:",bad_c_even,"| a+b even:",bad_parity,"| denominator with a prime !=1 mod 4:",bad_prime)

def odd_den(q): return q.denominator%2==1
def par(z):                      # parity map pi on Z_(2)[i]:  (x+y) mod 2
    x,y=z; s=x+y; assert odd_den(s); return s.numerator%2
assert all(par(u)==1 for u in units)     # chi(u) = (-1)^pi(u) = -1 for EVERY rational unit
print("  pi(u)=1 (chi(u)=-1) for all", len(units), "units: OK")

def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def add(z,w): return (z[0]+w[0], z[1]+w[1])
def rnd():
    d=random.choice([1,3,5,7,9,15,21,25,27,35,45,63,99,125])
    return (Fr(random.randint(-500,500),d),Fr(random.randint(-500,500),d))
U=list(units)
ok_add=ok_rot=0
for _ in range(20000):
    z,w=rnd(),rnd(); u=random.choice(U)
    ok_add += par(add(z,w))==(par(z)+par(w))%2
    ok_rot += par(mul(u,z))==par(z)
print("  homomorphism pi(z+w)=pi(z)+pi(w):",ok_add,"/20000 ; rotation invariance pi(uz)=pi(z):",ok_rot,"/20000")

# (1b) independent sanity check: every integer relation sum n_u u = 0 among a few small
# rational units has EVEN coefficient sum (forced if chi exists)
small=sorted(U,key=lambda z:(max(z[0].denominator,z[1].denominator),z))[:7]
rels=odd=0
for coeffs in itertools.product(range(-2,3),repeat=len(small)):
    if not any(coeffs): continue
    s=(Fr(0),Fr(0))
    for n,u in zip(coeffs,small): s=(s[0]+n*u[0],s[1]+n*u[1])
    if s==(0,0):
        rels+=1; odd += sum(coeffs)%2
print("  relations among 7 smallest units, coeffs in [-2,2]:",rels,"found; with ODD coefficient sum:",odd)

# CONTROL that must FAIL: the same assignment on algebraic units.  Q(sqrt-3) elements as
# a+b*w with w^2=-1-w.  1+w+w^2 = 0 with three unit vectors and coefficient sum 3 (odd):
def emul(p,q):  # (a+bw)(c+dw), w^2 = -1 - w
    a,b=p;c,d=q; return (a*c-b*d, a*d+b*c-b*d)
one=(1,0); w=(0,1); w2=emul(w,w)
tot=(one[0]+w[0]+w2[0], one[1]+w[1]+w2[1])
norm=lambda p: p[0]*p[0]-p[0]*p[1]+p[1]*p[1]          # |a+bw|^2
print("CONTROL (algebraic K): 1+w+w^2 =",tot,"; norms",norm(one),norm(w),norm(w2),
      "; coefficient sum 3 is odd -> a character d with d(u)=-1 on all of K would give d(0)=(-1)^3=-1, but d(0)=1: the set S is EMPTY over F(i)")
assert tot==(0,0) and norm(w)==1 and norm(w2)==1

# (2) Z-span of K: over Q(i) every denominator is a product of primes = 1 mod 4, so 1/3 is
# NOT in span_Z(K_Q) (span is a proper K_Q-invariant subgroup -> Haar on its annihilator is a
# wild, K_Q-invariant, non-Haar law).  Over F(i): u=(1+2*sqrt2 i)/3 is in K and 1/3 = 1-(u+conj u).
print("(2) over F(i): |(1+2sqrt2 i)/3|^2 =", Fr(1,9)+Fr(8,9), "; 1-(u+conj u) =", 1-Fr(2,3))

# (3) Lemma 2.7's k_j step / Sec 3.5's t+i*sqrt(1-t^2): x in Q is a sum of two rational
# units iff 1-x^2/4 is a rational square.
def is_sq(q):
    if q<0: return False
    a,b=q.numerator,q.denominator; return isqrt(a)**2==a and isqrt(b)**2==b
cand=sorted({Fr(p,q) for q in range(1,61) for p in range(1,2*q)})
rep=[x for x in cand if is_sq(1-x*x/4)]
print("(3) x=p/q in (0,2), q<=60:",len(cand),"values; sums of two rational units:",len(rep),
      "e.g.",[str(x) for x in rep[:6]])
trip=[t for t in {Fr(p,q) for q in range(1,401) for p in range(1,q)}
      if all(is_sq(1-(j*t)**2/4) for j in (1,2,3))]
print("    positive control: 6/5 = 2Re((3+4i)/5) detected:", Fr(6,5) in rep, "| negative control 1 (needs sqrt3/2):", Fr(1) in rep)
print("    t=p/q in (0,1), q<=400 with t,2t,3t ALL sums of two rational units:",len(trip))
print("    over F (real algebraic): every |x|<2 qualifies (sqrt(1-x^2/4) in F)")

# (4) square map not onto K_Q: (3+4i)/5 = ((2+i)/sqrt5)^2, and no enumerated rational unit squares to it
target=(Fr(3,5),Fr(4,5))
print("(4) rational units u (den<=%d) with u^2=(3+4i)/5:"%N, sum(mul(u,u)==target for u in U),
      "| CONTROL: u with u^2 = (-7+24i)/25:", sum(mul(u,u)==(Fr(-7,25),Fr(24,25)) for u in U))
# (5) Lemma 3.3's L=sqrt(AB): A=1,B=2 -> sqrt2 not rational
print("(5) is 1*2 a rational square?", is_sq(Fr(2)))
```
Output (wall time 4.8 s, peak RSS 23 MB):
```
rational units with denominator <= 3000 : 3820
  even denominators: 0 | a+b even: 0 | denominator with a prime !=1 mod 4: 0
  pi(u)=1 (chi(u)=-1) for all 3820 units: OK
  homomorphism pi(z+w)=pi(z)+pi(w): 20000 /20000 ; rotation invariance pi(uz)=pi(z): 20000 /20000
  relations among 7 smallest units, coeffs in [-2,2]: 72 found; with ODD coefficient sum: 0
CONTROL (algebraic K): 1+w+w^2 = (0, 0) ; norms 1 1 1 ; coefficient sum 3 is odd -> a character d with d(u)=-1 on all of K would give d(0)=(-1)^3=-1, but d(0)=1: the set S is EMPTY over F(i)
(2) over F(i): |(1+2sqrt2 i)/3|^2 = 1 ; 1-(u+conj u) = 1/3
(3) x=p/q in (0,2), q<=60: 2203 values; sums of two rational units: 16 e.g. ['18/41', '14/25', '24/37', '10/13', '16/17', '56/53']
    positive control: 6/5 = 2Re((3+4i)/5) detected: True | negative control 1 (needs sqrt3/2): False
    t=p/q in (0,1), q<=400 with t,2t,3t ALL sums of two rational units: 0
    over F (real algebraic): every |x|<2 qualifies (sqrt(1-x^2/4) in F)
(4) rational units u (den<=3000) with u^2=(3+4i)/5: 0 | CONTROL: u with u^2 = (-7+24i)/25: 2
(5) is 1*2 a rational square? False
```
Controls that fail, as they should:
- The algebraic-unit relation 1 + ω + ω² = 0 has odd coefficient sum, so the "all units ↦ −1" character does not exist over F(i).
- The detector for "x is a sum of two rational units" accepts 6/5 = 2Re((3+4i)/5) and rejects x = 1, which needs √3/2.
- The square-root search finds the 2 square roots of (−7+24i)/25 = ((3+4i)/5)², but none for (3+4i)/5.

### 9.2 /tmp/oaimath/158/seats/whole_scripts/moser_and_hex.py
This is a cross-check of the last step and of p. 2. The exact version is the cycles seat's (G).
```python
# Cross-check (numeric, 60 digits) of the final step (Lemma 8.8/8.9, eq. (8.4)-(8.6)) and the
# p.2 hexagon upper bound. The exact rational check is the cycles seat's (G); this is a
# whole-paper sanity pass with a control that must FAIL.
from decimal import Decimal as Dm, getcontext
getcontext().prec=60
s3,s11=Dm(3).sqrt(),Dm(11).sqrt()
def C(a,b): return (Dm(a),Dm(b))
def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def add(z,w): return (z[0]+w[0],z[1]+w[1])
def n2(z): return z[0]*z[0]+z[1]*z[1]
A=(s3/2,Dm(1)/2); B=(s3/2,-Dm(1)/2); T=(s3,Dm(0)); u=(Dm(5)/6,s11/6); O=(Dm(0),Dm(0))
G={'0':O,'A':A,'B':B,'T':T,'uA':mul(u,A),'uB':mul(u,B),'uT':mul(u,T)}
E=[('0','A'),('0','B'),('A','B'),('A','T'),('B','T'),('0','uA'),('0','uB'),('uA','uB'),('uA','uT'),('uB','uT'),('T','uT')]
rot=(Dm(35)/37,Dm(12)/37); sh=(Dm(-290)/250,Dm(149)/250)
Z={g:mul(rot,add(p,sh)) for g,p in G.items()}   # (8.6): z_g = rot*(g+shift)
def P(z): x,y=z; return y*y*(3*x*x-y*y)**2
def Pp(z): l=n2(z); return l**3*(1-l/4)*(l-1)**2
def check(Z,label):
    edge_err=max(abs(n2((Z[a][0]-Z[b][0],Z[a][1]-Z[b][1]))-1) for a,b in E)
    ok=True
    for g,z in Z.items():
        l=n2(z); good=(0<l<4) and P(z)<Pp(z); ok&=good
        print(f"  {label} {g:>2}: l={float(l):.6f}  P={float(P(z)):.6g}  P'={float(Pp(z)):.6g}  in-region={good}")
    print(f"  {label}: max |edge^2-1| = {float(edge_err):.2e}; all 7 in region: {ok}")
    return ok, edge_err
ok,err=check(Z,"placement")
assert ok and err<Dm(10)**-50
# CONTROL 1: misread (8.6) as rot*g+shift -> region membership must FAIL somewhere
Zc={g:add(mul(rot,p),sh) for g,p in G.items()}
okc,_=check(Zc,"CONTROL rot*g+shift")
# CONTROL 2: non-unit spindle (u with |u|=1.01) must break an edge
u2=(Dm(5)/6*Dm('1.01'),s11/6*Dm('1.01'))
Zb={**Z,'uT':mul(rot,add(mul(u2,T),sh))}
eb=max(abs(n2((Zb[a][0]-Zb[b][0],Zb[a][1]-Zb[b][1]))-1) for a,b in E)
print("  CONTROL non-unit u: max |edge^2-1| =",float(eb))
# Moser graph not 3-colourable (exhaustive)
import itertools
V=list(G); idx={v:i for i,v in enumerate(V)}
n3=sum(all(c[idx[a]]!=c[idx[b]] for a,b in E) for c in itertools.product(range(3),repeat=7))
n4=sum(all(c[idx[a]]!=c[idx[b]] for a,b in E) for c in itertools.product(range(4),repeat=7))
print("  proper 3-colourings of the 7-vertex graph:",n3,"| CONTROL proper 4-colourings:",n4)
# p.2 hexagon bound
r=Dm(2)/5
print("hexagon: 2r =",2*r,"<1 ;  (sqrt21-2) r =",(Dm(21).sqrt()-2)*r,">1 ; |2-omega|^2 = 4+2+1 =",4+2+1)
```
Output:
```
  placement  0: l=1.700816  P=0.866124  P'=1.38897  in-region=True
  placement  A: l=1.287637  P=0.0895503  P'=0.119773  in-region=True
  placement  B: l=0.095637  P=1.68999e-06  P'=0.00069832  in-region=True
  placement  T: l=0.682458  P=0.0221255  P'=0.0265819  in-region=True
  placement uA: l=2.735008  P=9.72524  P'=19.4763  in-region=True
  placement uB: l=0.459246  P=0.00199268  P'=0.025071  in-region=True
  placement uT: l=2.493438  P=12.5744  P'=13.0226  in-region=True
  placement: max |edge^2-1| = 2.00e-59; all 7 in region: True
  CONTROL rot*g+shift  0: l=1.700816  P=4.81462  P'=1.38897  in-region=False
  CONTROL rot*g+shift  A: l=2.075042  P=2.05972  P'=4.96927  in-region=True
  CONTROL rot*g+shift  B: l=0.195042  P=0.000741416  P'=0.00457321  in-region=True
  CONTROL rot*g+shift  T: l=1.569268  P=0.572776  P'=0.761031  in-region=True
  CONTROL rot*g+shift uA: l=3.579024  P=1.08991  P'=32.0924  in-region=True
  CONTROL rot*g+shift uB: l=1.012948  P=0.597669  P'=0.000130116  in-region=False
  CONTROL rot*g+shift uT: l=3.891156  P=57.4207  P'=13.4006  in-region=False
  CONTROL rot*g+shift: max |edge^2-1| = 1.10e-59; all 7 in region: False
  CONTROL non-unit u: max |edge^2-1| = 0.0303
  proper 3-colourings of the 7-vertex graph: 0 | CONTROL proper 4-colourings: 384
hexagon: 2r = 0.8 <1 ;  (sqrt21-2) r = 1.03303027798233600263521887749120339559378263070718876104290 >1 ; |2-omega|^2 = 4+2+1 = 7
```
The squared radii match the paper's intervals (1.70,1.71), (1.28,1.29), (0.095,0.096), (0.68,0.69), (2.73,2.74), (0.459,0.46), (2.49,2.50).

Controls that fail, as they should:
- Reading (8.6) as "rotation, then translation by (−290+149i)/250" (Objection 5) puts z₀, z_{uB} and z_{uT} outside the region.
- |u| = 1.01 breaks the unit edges (max |edge² − 1| = 0.03).
- The spindle has 0 proper 3-colourings but 384 proper 4-colourings.

---------------------------------------------------------------------------------------------------
## 10. CITATION TABLE (my scope)

| Cited / used | Claimed | Source says (quote) | Verdict |
|---|---|---|---|
| Mathlib `Complex.instNorm` | ‖·‖ on ℂ is Euclidean | Mathlib/Analysis/Complex/Norm.lean:28–29 "instance instNorm : Norm ℂ where norm z := √(normSq z)" | MATCH |
| Mathlib `haarAddCircle` | normalised arc length | Mathlib/Analysis/Fourier/AddCircle.lean:85 "Haar measure on the additive circle, normalised to have total measure 1"; `volume_eq_smul_haarAddCircle : volume = ENNReal.ofReal T • haarAddCircle` | MATCH |
| Mathlib `toCircle` | direction t = e^{it} | Circle.lean:383 "toCircle_apply_mk (x : ℝ) : @toCircle T x = Circle.exp (2 * π / T * x)" | MATCH (T = 2π) |
| Mathlib volume on ℂ | Lebesgue | MeasureTheory/Measure/Lebesgue/Complex.lean: "the Lebesgue measure on ℂ defined as the push-forward of the volume on ℝ² … equal to the measure volume of ℂ coming from its InnerProductSpace structure"; `volume_preserving_equiv_real_prod` | MATCH |
| Davies 2022, arXiv 2209.15598 (used in §5) | odd distances unavoidable | "For every finite colouring of the plane, there is a monochromatic pair of points at an odd distance from each other." | (external; consistent with the generalised transfer) |
| DMP 2023, arXiv 2308.02483 (used in §5) | Problems 5.4–5.5 open; FKW; Bukh | quoted in §5 | (external) |
| [4] de Bruijn–Erdős, [12] Gwyn–Stavrianos, [2] Bourgeat et al. (Cor 1.5) | — | the proof needs only [4] (§6) | deferred to the sources seat |
| Moshchevitin–Raigorodskii 2007 | — | — | COULD NOT FETCH |

---------------------------------------------------------------------------------------------------
## 11. VERDICT FOR MY SCOPE

**HOLDS AS READ** at the level of the dependency graph, the two-part split, Corollary 1.5, and the statement.
- Test (A) passes: the F(i)-specific step is Lemma 2.7, p. 13, and the ℚ(i) analogue is false by explicit counterexample.
- Test (B) passes: k = 5 is essential, and at six Proposition 5.6 breaks first.
- The formal statement is faithful to Theorem 1.1 and is the lower-bound half of #508. `WeakColoring` is equivalent to Definition 1.2. No vacuity.

**COULD NOT CHECK** line by line the measure-theoretic infrastructure of Lemma 2.7, Lemmas 3.1–3.2, and the interiors of §§5–8 listed as SKIMMED above. These are in other seats' scope, and the kernel replay covers them if it completes green.

**New flag:** the transfer, read verbatim, also proves the Δ-distance version (§5). That would settle open problems the authors do not mention. Together with test (A), it marks Theorem 2.3 as the place to concentrate scrutiny.
