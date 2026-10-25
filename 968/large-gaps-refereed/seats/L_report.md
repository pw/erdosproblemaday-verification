HOLDS AS READ

Seat L: OpenAI's Lean against the paper. I read source only and built nothing. I cite Lean as file:line under repo/lean/OAI/NumberTheory/PrimeGaps/ unless another path is given. Paper numbering follows the PDF: §1 intro, §2 = 02-counting, §3 = 04-weights, §4 = 05-cancellation, §5 = 03-moments.

Bottom line: the comparator statement says what Theorem 1.1 and Corollary 1.2 say, and I found no degenerate reading. The Lean chain has no open hypotheses. It does not assume Bombieri–Vinogradov (BV). It proves BV from Siegel–Walfisz (SW), and proves SW, including Siegel's theorem, from Mathlib alone. So the Lean is strictly stronger than the paper, which assumes BV (Lemma 5.2). The construction is the paper's, parameter for parameter. Every difference I found is about exposition or about rates; none is a gap.

The coordinator's replay supports this; I did not run it myself (lean-build/driver.log: "BUILD END 0 56 failed []"). lean-build/statement_match.txt reads: MATCH / STD_AXIOMS / CMP_SORRY_SEEN. `main`, `bombieriVinogradov` and `siegelWalfisz` each depend only on [propext, Classical.choice, Quot.sound]. The type and negative controls fired as expected (logs/typectl.log, logs/neg.log).

## Map: paper item → Lean

| Paper (printed) | Lean name | file:line |
|---|---|---|
| Thm 1.1 | `OAI.LargePrimeGaps.main` = `index_density_of_bombieriVinogradov bombieriVinogradov` | Main.lean:161-164; DetectorMoments.lean:288-338 |
| §2 proof of Thm 1.1 (Cauchy–Schwarz twice, X = ⌊p_N/3⌋) | `index_density_from_weight_estimates`, `goodStarts_bound_of_moments`, `index_bound_of_goodStarts`, `indexScale`, `eventually_scale_comparison` | EqualityPatterns.lean:27; Indices.lean:329, 444, 378, 383 |
| Lemma 2.2 (last prime, multiplicity ≤ h) | `goodStarts`, `gapPrimes`, `exists_gapPrime_of_goodStart`, `goodStarts_card_le`, `gapPrimes_card_le_largeGapIndices` | Indices.lean:56, 62, 67, 96, 118 |
| Cor 1.2 | `positive_lower_density_prime_ratio_increases`; conjunction `large_gaps_and_ratio_density` | RatioCorollary.lean:20, 30; RatioDensity.lean:56-70; RatioReduction.lean:8; RatioAlgebra.lean:7; PrimeGrowth.lean:35 |
| Prop 2.1 (weights) | no single statement: its content is the five hypotheses of `index_density_from_weight_estimates`, discharged at | DetectorMoments.lean:319-338 |
| Prop 3.1 (5), E Z² → w | `unorderedWeight_second_limit` (proved, unused by `main`) | ProfileSymmetry.lean:271 |
| Prop 3.1 (5), E Z⁴ = O(1) | `unorderedWeight_fourth_bound` | ProfileSymmetry.lean:282 |
| Prop 3.1 (6), E Z² V_J → λw | `unorderedWeight_external_marked_limit` | MarkedMoments.lean:273 |
| Prop 3.1 (6), E Z² V_I → v | `unorderedWeight_internal_marked_limit` | RestrictedWeights.lean:431 |
| Prop 3.1 (7), detector bound | `unorderedWeight_detector_bound`, `weighted_detector_square_majorant`, `exists_detector_profile` | DetectorMoments.lean:249; Detectors.lean:374, 467 |
| identity (8), prime deletion | `unorderedWeight_prime_delete`, `divisorSum_prime_delete`, `divisorCoefficient_snoc_prime_zero` | RestrictedWeights.lean:63; TensorProfiles.lean:281, 244 |
| Lemma 4.1 | `exists_small_first_moment_profile` (same four conclusions) | Profiles.lean:265 |
| Prop 4.2 | `exists_canceling_families`, `exists_family_small_marked_ratio`, `cancellationFamily_W_tendsto`, `cancellationFamily_V_tendsto`, `cancellationFamily_V_bound` | OrthantIntegrals.lean:149, 184, 103, 122; LevelMoments.lean:332 |
| Prop 5.1 (13) | `unmarked_average_uniform_asymptotic`, `marked_average_uniform_asymptotic` | LaplaceTransform.lean:351, 398 |
| Prop 5.1 (14), constant | `small_fiber_kernelConstant` | LaplaceTransform.lean:252 |
| Lemma 5.2 (16) | `weightedErrorSum` / `weightedErrorSum_log_decay`, `marked_error_sum_log_decay`, `endpoint_sum_log_decay` | MangoldtBounds.lean:426, 453, 356, 205 |
| Lemma 5.3 | `unmarked_arithmetic_error`, `marked_arithmetic_error`, `not_prime_on_nonreduced_class` | DivisorBounds.lean:38, 405; DivisorSums.lean:334 |
| Lemma 5.4 | `singularBoxMean_uniform`, `uniform_singularBoxMean_tendsto` | BoxMeans.lean:365; EqualityPatterns.lean:383 |
| BV (assumed in the paper) | `def BombieriVinogradov`; `bombieriVinogradov_of_siegelWalfisz`; `bombieriVinogradov` | MangoldtBounds.lean:101; LogParameters.lean:284; Main.lean:158 |
| SW | `def SiegelWalfisz`; `primeWeighted_error_bound`; `primeCharacterError_log_bound`; `siegelWalfisz` | ConductorBounds.lean:222; RieszDecay.lean:330; Main.lean:29, 142 |
| Siegel's theorem | `quadratic_siegel_eventual` (ineffective `by_cases hex` at :364); `quadratic_siegel` | SiegelBounds.lean:357, 471; used once at ZeroFreeBounds.lean:327 |
| Large sieve, Pólya–Vinogradov | `additive_large_sieve`, `rational_additive_large_sieve`, `multiplicative_large_sieve`, `bilinear_multiplicative_large_sieve`, `primitive_polya_vinogradov` | AdditiveSieve.lean:359, 425; MultiplicativeSieve.lean:235, 320, 395 |

## Findings

1. **Comparator statement is faithful; no trivial truth.** Verified.
   - Statement: ComparatorChallenges/PrimeGaps.lean:7-11 defines `prime n := Nat.nth Nat.Prime (n - 1)`, so p_1 = 2 and n ∈ Icc 1 N. The gap condition is strict: `C * Real.log (prime n) < prime (n+1) − prime n`. Lines 26-33 define `ratioIncreaseIndices` as `1 ≤ n ∧ p_n/n < p_{n+1}/((n+1:ℕ):ℝ)`. Theorem 1.1 is `c * N ≤ card` for every N ≥ N₀ and every real C > 0. All match the PDF wording ("#{1 ≤ n ≤ N : p_{n+1} − p_n > C log p_n} ≥ c(C)N"; "{n ≥ 1 : p_n/n < p_{n+1}/(n+1)}").
   - `lowerAsymptoticDensity` is the sSup of the eventual lower bounds of count/N. That set is bounded above by 1 and contains 0 (DensityBounds.lean:32-44), so Real.sSup's junk value 0 cannot arise. The set is downward-closed, so "0 < sSup" is the same as liminf count/N > 0.
   - The ratio condition is equivalent to p_{n+1} − p_n > p_n/n (RatioAlgebra.lean:7), as the paper says.
   - The definitions are textually identical to the solution's (Indices.lean:7-12; Density.lean:9-29), and the coordinator's pp.all comparison matched all 6 definitions plus the theorem type.
   - The erdosproblems.com #968 page asks for "positive density" and glosses it as positive lower density. That is what Corollary 1.2 and the comparator assert. The page's add-on question (u_n<u_{n+1}<u_{n+2} infinitely often) is addressed by neither the paper nor the Lean.

2. **The chain is unconditional; nothing is carried in a structure.** Verified.
   - Main.lean:161-164: `main` has no hypotheses. Its BV argument is the proved `bombieriVinogradov` (Main.lean:158), which comes from `siegelWalfisz` (Main.lean:142).
   - The 56 files form a linear import chain rooted at `import Mathlib` (Indices, Density, PrimeGrowth, RatioAlgebra).
   - There are 0 `structure`/`class`/`inductive` declarations, 0 `axiom`/`sorry`/`admit`/`native_decide`/`implemented_by`/`extern`/`unsafe`/`opaque`, and 0 `set_option` (so no maxHeartbeats, maxRecDepth or kernel-skip).
   - The Prop-valued definitions (`HasBudget` DivisorSums.lean:20, `AdmissibleFamily` OrthantIntegrals.lean:143, `SymmetricFunction` LevelMoments.lean:390, `boxDiameterBound` BoxMeans.lean:166, BV, SW) are all discharged before `main`.
   - The 6 `decide` are trivial: `2 ≠ 0` at OrthantIntegrals.lean:37, 101, MultiplicativeSieve.lean:243 and ProfileVariance.lean:318; `(0:Fin 2) ≠ 1` at DetectorMoments.lean:158; a Bool `decide (0≤r j)` inside a filter at AdditiveSieve.lean:297.
   - The 2 `Classical.propDecidable` (PatternMoments.lean:282, TensorProfiles.lean:385) only supply a filter's Decidable instance.
   - The lakefile's dependency patches (lean/patches/*, lakefile.lean ~146) are keyed by package label. None targets mathlib (pinned at d13f23b), and PrimeGaps imports no patched package.

3. **The `BombieriVinogradov` definition is the standard endpoint BV, the form the paper cites as (15).** Verified (MangoldtBounds.lean:87-105).
   - `endpointError x q` is a Finset.sup over c < q with `Nat.Coprime c q` of |Σ_{0<n≤⌊x⌋, n%q=c} Λ(n) − x/φ(q)| (`residuePrefix`, OrthantIntegrals.lean:437-441). That is ψ, not θ. q = 1 is included, since Coprime 0 1.
   - Quantifiers: ∀A>0 ∃b>0, M, x₀, with the sum over q ∈ Icc 1 ⌊x^{1/2}(log x)^{-b}⌋.
   - It has no max over y ≤ x, so it is weaker than the textbook statement and exactly the paper's (15).
   - It is not vacuous. The q = 1 term gives ψ(X) − X ≪ X(log X)^{-A}; `BombieriVinogradov_quantitative_PNT` (ContourIntegrals.lean:186) derives this. That lemma is dead code but works as a non-vacuity witness.
   - The paper needs only moduli q ≤ X^σ with σ = 2τ = 1/4 < 1/2. The Lean uses exactly that: `weightedErrorSum_log_decay` requires `rho < 1/2` (MangoldtBounds.lean:453).

4. **The `SiegelWalfisz` definition is faithful.** Verified (ConductorBounds.lean:222-227; CharacterErrors.lean:27-31).
   - It reads: ∀A,B>0 ∃M, x₀ ∀x≥x₀ ∀d with 0<d≤(log x)^B, ∀ primitive χ mod d, ‖Σ_{0<n≤⌊x⌋} χ(n)Λ(n) − [χ=1]x‖ ≤ M x (log x)^{-A}.
   - A primitive χ equals 1 only when d = 1, so the d = 1 case is the prime number theorem with log-power error. It is non-vacuous.
   - It covers primitive characters only, which is the standard reduction: imprimitive characters differ by O(log² x). `primeCharacterError_le_primitive` handles this inside the BV proof (CharacterErrors.lean ~105-224).
   - BV from SW: SW is invoked with (A', B') = (2A+14, A+11), and the BV level exponent is b = A+10 (LogParameters.lean:284-306). The route is Vaughan's identity (VaughanIdentity/VaughanBounds/DyadicMeans) plus the multiplicative large sieve with constant N + Q²·H_{Q²}. That is one extra log factor over optimal, which is harmless.

5. **Siegel's theorem is proved in its ineffective form, and the SW proof avoids the textbook zero-free-region route.** Severity: exposition, not a defect.
   - Siegel: SiegelBounds.lean:364 splits on whether some primitive real ψ has a zero in [1−ε/240, 1] (`by_cases hex`). The root case uses the biquadratic product ψ·χ·ψχ (`biquadraticCoefficients`, TaylorBounds.lean:491; `biquadratic_residue_lower_of_root`, SiegelBounds.lean:322). The no-root case uses `quadratic_residue_lower_of_no_root` (:282). `quadratic_siegel` (:471) then gives |L(1,χ)| ≥ c(ε)(q+1)^{-ε} for all primitive quadratic χ ≠ 1.
   - SW route: only lower bounds |L(σ+it,χ)| ≥ c((q+2)(|t|+2))^{-ε} on 1 ≤ σ ≤ 2 are proved (ZeroFreeBounds.lean:322, 440; PrincipalGrowth.lean:302). Siegel's bound covers the real-character case near t = 0.
   - These bounds yield derivative bounds for L'/L/(s(s+1)) on the 1-line (RieszBounds.lean:136). A Riesz-mean Mellin inversion on Re s = 1 with repeated integration by parts then gives `primeWeighted_error_bound` (RieszDecay.lean:330): E ≤ D√(q+2)x²(log x)^{-a} + x for every q, which is trivial for large q. Unsmoothing with h = x/(log x)^{A+2} gives SW (Main.lean:29-140).
   - This is a known valid route that differs from the de la Vallée Poussin zero-free region. Correctness rests on the kernel check.

6. **The main construction is the paper's, parameter for parameter.** Verified.
   - τ = 1/8 (DetectorMoments.lean:292).
   - λ = C+1 (:293). Paper: "choose λ > max{C, 1}".
   - ε = λ²/(16D) with D = λ + λ²·(∫g²)² + 1 (:297-299). Paper: ε = λ²/(2K_λ) with K_λ = λ + λ²c_G² and c_G = ∫|G′|² = ∫g², so D = K_λ + 1 and ε is smaller than the paper's.
   - k = (m+1)² and r = m+1 = √k exactly (OrthantIntegrals.lean:54, 172). Paper: "r = ⌊√k⌋ and a = k − r + 1". Active levels are Icc (k−r+1) k (LevelMoments.lean:169-173).
   - `levelFunction` = (−1)^j/(√r√α_j)·∏√k g(k t_i)·χ(S_j), which is the paper's (9) (ProfileVariance.lean:477-480). β = τ/3 and γ = 2τ/3 (OrthantIntegrals.lean:154-155). f_0 = 0 (LevelMoments.lean:208).
   - Z sums over j of subset sums over I = {h+1..2h}: injective tuples with weight 1/j! (`subsetCoefficient`, WeightMoments.lean:133-139; `unorderedBlock`, ProfileSymmetry.lean:222).
   - The weight is W = Z², not normalised by w (harmless).
   - Detector and blocks are defined as in the paper: V_B = (1/log X)Σ_{b∈B} θ(m+b), J = Ioc 0 h, I = Ioc h 2h (Indices.lean:240-249).
   - Support budgets are as tabulated in §5.4: 2τ < 1/2 for the marked moments (DetectorMoments.lean:323, 331), 4τ < 1 (:318), 6τ < 1 (:329).

7. **The Lean is weaker than the paper on displayed rates.** Severity: exposition, not load-bearing.
   - Prop 5.1, verbatim: "= L^{−t}{S(H)C + O(L^{−1/2}(log L)^A)}". The Lean proves only an o(1) error uniform in the shifts (LaplaceTransform.lean:351, 398). Shifts there are in ℕ (nonnegative) with b_i ≤ D and 2D ≤ ⌊(log X)^β⌋ (`densityCutoff`, ContourIntegrals.lean:375; applied with β = 2 at EqualityPatterns.lean:372). That suffices because the application multiplies by (h/L)^t = O(1).
   - Lemma 5.4's "O_{s,K}(1/log log h) + O_s(h^{−1/2}(log log h)^{A_s})" is formalised only as ∀ε ∃h₀ (BoxMeans.lean:365).
   - So the paper's explicit rates are not machine-checked, but nothing downstream needs them.

8. **The Lean replaces the paper's prime number theorem steps with Chebyshev bounds.** Severity: exposition.
   - The proof of Corollary 1.2 says "The prime number theorem gives p_n/n ∼ log p_n. Apply Theorem 1.1 with C = 2". The Lean instead uses C = 2/log 2 and Mathlib's `Chebyshev.pi_ge` (PrimeGrowth.lean:25-59; RatioDensity.lean:64-70).
   - The proof of Theorem 1.1 says "The prime number theorem gives X/log X ∼ N/3". The Lean instead uses N log X ≤ 6(log 4+1)X from `Chebyshev.eventually_primeCounting_le` (Indices.lean:369-407), giving c(C) = δ/(6(log 4+1)(C+1)) (EqualityPatterns.lean:47-50) where the paper has δ/(4λ).
   - Both steps are easier than the paper makes them look.

9. **Prop 2.1 states more than its use requires.** Severity: exposition. Prop 2.1(1) includes "E_X W_X −→ 1". Neither the paper's proof of Theorem 1.1 nor the Lean (`index_density_from_weight_estimates`, EqualityPatterns.lean:27-38) uses it. The Lean proves the corresponding E Z² → w (ProfileSymmetry.lean:271), but `main` never references it.

10. **The Lean has one side condition the paper leaves implicit.** Severity: exposition. `unorderedWeight_prime_delete` needs k ≤ h = blockLength (RestrictedWeights.lean:63-66), i.e. the fixed dimension k is at most |I|. This holds eventually because k is fixed before X → ∞, as the paper stresses ("The parameter order is essential").

11. **docs/026.md understates the scope.** Severity: typo/exposition. It says the formalised supplement "proves that the indices n for which p_n/n<p_{n+1}/(n+1) have positive lower asymptotic density". The comparator (ComparatorChallenges/PrimeGaps.json) checks the conjunction including Theorem 1.1. The namespace `Problem344` does not match #968, presumably an internal ID; this is harmless.

12. **Audit counts and oddities.**
    - Size: 56 files, 22,533 lines, zero comments.
    - Declarations: 1,561 top-level (1,118 `theorem`, 175 `lemma`, 263 `def`, 1 `abbrev` at FourierNormalization.lean:409, 4 `instance`). Three instances are Prop-valued and proved: SigmaFinite/IsFiniteMeasureOnCompacts at CumulativeProfiles.lean:199, 203 and LaplaceTransform.lean:43. The fourth is `Fintype (Setoid ι)` via `Fintype.ofInjective` (EqualityPatterns.lean:126).
    - No unusually long proofs: the longest declaration is 113 lines (Main.lean:29), then ZeroFreeBounds.lean:216 (106) and ConductorBounds.lean:404 (101).
    - About 70 declarations have no textual reference elsewhere, e.g. `BombieriVinogradov_quantitative_PNT` and `unorderedWeight_second_limit` (script: L_work/deadcode.py).
    - Main.lean:7-27 repeats the same `open` line 9 times, a concatenation artifact.
    - "largeGapIndices" exists twice: as a Finset in `OAI.LargePrimeGaps` and as a Set in `OAI.Problem344` (Density.lean:20), bridged by `largeGap_count_eq` (RatioCorollary.lean:8).
    - Scripts: L_work/declstats.py, L_work/deadcode.py; rendered PDF text: L_work/paper_layout.txt.

## What I did NOT check
- I did not read the ~1,290 lemma proofs line by line. Proof correctness rests on the coordinator's build, which runs the kernel per declaration with no `set_option`, and on its axiom printout. I did not run a separate `leanchecker` replay myself.
- I did not check mathematical soundness of the paper's own §5 arguments beyond the statement-level match to the Lean. Seats T/O cover the paper.
- I did not check the comparator tool's own soundness, the Lean toolchain (v4.34.1), or the Mathlib commit beyond the patch question.
- I did not compare against any third-party formalisation of #968, such as the "Formalised statement? Yes" link on erdosproblems.com.
- I did not check whether the BV-from-SW constants (A+10, 2A+14, A+11) are optimal. Only validity matters, and the kernel covers that.
