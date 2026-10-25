# Seat L — the Lean against the paper (#371 / OpenAI 012, "The joint Dickman law for consecutive integers")

Scope: the OAI Lean closure at /tmp/oaimath/012/src/oai (+ patched PrimeNumberTheoremAnd / StrongPNT, Architect), read against
the printed paper (paper.txt). I did not compile anything. Every "proved" below means "a closed Lean term exists in the source
tree with no hypothesis of that type". That this term actually checks (axioms = propext / Classical.choice / Quot.sound, and the
comparator accepts it) is the separate kernel replay, and my verdict depends on it.
Work files: /tmp/oaimath/012/seats/L_work/ (scan.py, importers.py, rho_check.py).

---------------------------------------------------------------------------------------------------------------------------

## 1. Does the unconditional proof avoid Matomäki–Radziwiłł and MRT? How is the §2 short average obtained?

**As hypotheses, yes, entirely.** `RealShortIntervalInput` (MR 2016 Thm 1), `ComplexShortIntervalInput` (MRT Thm A.1),
`MultiplicativeExponentialInput` (Montgomery–Vaughan), `CharacterDistanceInput` (KMT Lemma 7.8) and TwoPointCorrelations'
`MRTShortExponentialInput` / `MRTLiouvilleShortInput` are proved by no theorem anywhere in the tree (grep for any theorem whose
type is one of these: zero hits). `UnconditionalMain.rationalFixedScaleLaw_unconditional` is a closed term whose arguments are
eight theorems, none of them MR or MRT. So the hMR/hMRT route (ConditionalMain, DischargedMain `main_results_after_*`) is dead
code with respect to `PaperMain.joint_law`.

**As mathematics, no.** The Lean does not swap in some cheaper idea. It **formalizes the Matomäki–Radziwiłł method itself**,
specialised to the bin labels. The general MR machinery lives in `OAI/NumberTheory/TwoPointCorrelations/MRT*.lean`: prime bands
`[P_j,Q_j]`, "typical" integers with a prime in every band (MRT Lemma 2.2, `MRTTypicalDensity`), the corrected Ramaré
decomposition (`MRTBandSeparation`), large values at separated heights (`MRTLargeValues`), and the first-small-band energy
(`MRTGeneralSmallEnergy`). Halász's theorem is formalized next to it (`HalaszGeneralMean`, `HalaszLocalWindow`).

Chain (file : theorem), top down:

- `UnconditionalMain` : `rationalFixedScaleLaw_unconditional`
- → `Amplification/RationalThresholdsDischarge` : `rationalFixedScaleLaw_of_distance_divergence_proved`. Rational c, d are put
  over a common denominator J.
- → `Arithmetic/RationalBinSmoothDischarge` : `fixedDensity_common_denominator_proved`
- → `Amplification/BinJointEventsDischarge` : `bin_joint_event_limit_proved`. Finite Fourier on `BinCountState J =
  Fin(J-1)→Fin(J+1)`.
- → `Analysis/CanonicalCharacterPairsDischarge` → `Analysis/BinCharacterPairsDischarge` : `bin_character_pair_limit_proved`
- → `Amplification/BinDecorrelationDischarge` : `centeredBinCorrelation_tendsto_proved`. This is Prop 2.2, proved by
  "every subsequence has a sub-subsequence with limit 0".
- → `Amplification/BinCorrelationLimitDischarge` : `bin_correlation_limit_zero_proved`. This is the contradiction step. It
  combines `Counting/SubsequencePositiveBlocks.nonzero_binLabel_correlation_along_forces_blocks` (positive block energy, §4–5)
  with `Counting/ArithmeticBlockMeanDischarge.arithmetic_block_centered_mean_proved` (the block energy vanishes, §5–10).
- → `Counting/FiniteCountingMeanDischarge` → `CountingPrefixMean/ModelMean/PeriodicEnergy/ForwardEnergy/CoarseCountingRows/
  CoarseCountingConvolution/CoarseResidueSmoothing/CoarseBinShort … Discharge` → `Analysis/LaplaceShortDischarge` :
  `unit_laplace_short_with_center_proved`. **This is the Lean form of Lemma 2.3**: weights are combinations of
  `primeLaplaceFeature` = G_{B,v}, the class is a unit class mod q, and the bound has the shape ∀ε ∀ᶠB ∀ᶠx, i.e.
  lim_B limsup_x.
- → `Counting/PrescribedShortDischarge` : `all_characters_short_with_center_proved`. This splits by Dirichlet character
  exactly as in §2.5.
  - **Principal character.** `Counting/PrincipalBinShortDischarge.finitePrimeWeight_short_with_center_proved` ←
    `Amplification/CenteredBinSpectral.centered_bin_spectral` + `Counting/ShortAffineLimit.shortAverage_iterated_affine`. The
    second piece is a Gallagher/Parseval step: if ∫_{-T}^{T}|Σ_{N<n≤2N}F(n)n^{-1-it}|² ≤ base(H) + slope·T/N for all T ≥ 1,
    then the short averages are small.
  - **Nonprincipal character.** `Counting/NonprincipalShortDischarge.nonprincipal_weightedBinAverage_short_proved` (its
    `_hKMT` and `_hM` arguments are unused) ← `Counting/TwistedInterpolantShort.twisted_interpolant_short` ←
    `Amplification/TwistedBinSpectral`.

`centered_bin_spectral` splits the frequency axis into three parts:

1. **Low frequencies, |t| ≤ U.** Handled by `BinDyadicLowFrequency`, using `hmean`: long-interval means of the centered label
   tend to 0. Those means come from the proved finite-bin distribution, i.e. Lemma 2.1.
2. **Frequencies where some MR band polynomial is small.** Handled by `Counting/CanonicalAffineEnergy.canonical_affine_energy`.
   This is MR's Ramaré/typical-integer bound, valid for *every* 1-bounded multiplicative F.
3. **The MR exceptional set**, where every band polynomial is large (`mrtNoSmallBand`). Handled by
   `Counting/BinExceptionalEnergy.bin_exceptional_energy`. It uses an auxiliary band of primes in [N^α, N^β] with β <
   min(1/12, 1/J), the large-values count, and a sup bound on the cofactor polynomial,
   `Amplification/BinCofactorBound.bin_cofactor_away_zero`.

The cofactor bound has two ranges:

- Low range, |t| ≤ 3(log m)^8: `finite_weight_count_window_logarithmic`.
- High range, (log m)^8 ≤ |t| ≤ m²: `Counting/HighCofactorWindow.high_frequency_count_window`. This is Halász
  (`TwoPointCorrelations.halasz_local_count_window`) plus a lower bound on the distance from f to n^{it}, taken from
  `Arithmetic/PrimeAgreementPolynomial`. That lower bound rests on `PrimePhasePolynomial.prime_cosine_defect_polynomial`
  (Σ_{p≤X}(1−cos(t log p))/p ≥ R for 1 ≤ |t| ≤ X^A), which comes from `Analysis/ZetaLogarithmicBound.zeta_logarithmic_bound`
  (|ζ(σ+it)| ≤ (1/B)·log|t| + C for 1 < σ ≤ 2, any B). That in turn is proved from an approximate functional equation plus
  `Analysis/CharacterMiddleSum.character_middle_sum_bound`: a power saving N^{-δ} for Σ_{N<n≤2^K N} χ(n)n^{-σ-it} when
  (2^K N)^{1/2} ≤ |t|/2π ≤ N^B. That is Weyl/van der Corput differencing, from EgyptianFractions' IteratedDifferencing /
  SecondDerivativeTest.

The twisted case runs the same scheme. Its distance input comes from `Analysis/CharacterPolynomialDistance` /
`CharacterUniformSublog`: L(1+δ+it, χ) ≤ η log X for |t| ≤ X.

**Why the bin labels make this easier (plain terms).** f_x(p) = 1 for *every* prime p ≤ x^{1/J}, or χ(p) after a twist.
Three consequences:

- **(a) The bands do not depend on f.** All of MR's bands live far below x^{1/J}, since they depend only on H. So the band
  polynomials there are just Σ p^{-1-it} (resp. Σ χ(p)p^{-1-it}), the same for every label. The part of MR that works for an
  arbitrary multiplicative function (step 2) is used verbatim.
- **(b) The only possible conspiracy is at t ≈ 0.** The hard step in MR/MRT is a function that "pretends" to be n^{it}. A
  bin label agrees with 1 on all small primes, so it can only pretend to be n^{it} where 1 itself does, on primes up to a
  fixed power of x. That happens only for |t| = O(1). It is excluded for 1 ≤ |t| ≤ X^A as soon as ζ(1+it) = o(log t), and
  for a fixed nonprincipal χ for all |t| ≤ X as soon as L(1+it, χ) = o(log t) (L has no pole). So no realness assumption (MR
  Thm 1) and no exceptional twist t₀ (MRT A.1) is needed. Halász gives cancellation at every large frequency uniformly, and
  the t ≈ 0 range is controlled by the known long-mean distribution (Lemma 2.1).
- **(c) No Vinogradov–Korobov needed.** The zeta input is only Littlewood-strength (o(log t), from Weyl sums). The paper's
  Lemma 2.6 instead uses "The Vinogradov–Korobov bound, … |ζ(σ+iu)| ≪ (log(|u|+3))^{3/4}" (2.17, citing Ford). That is more
  than the argument needs.

A side effect: in the principal case the Lean treats the *complex* centered label directly (`centeredWeightedBinCoefficient`).
It does not use the paper's interpolation by real nonnegative multiplicative functions (2.18), which exists only to fit MR's
real-valued hypothesis.

So the paper's sentence (§1.2) is accurate as a description of the reduction but over-specifies the input: "The rest of the
proof must reduce the mixed correlation to this particular cancellation statement." The cancellation statement is needed; the
two cited theorems are not. **EXPOSITION** (route remark, not an error).

## 2. The eight inputs used unconditionally

Proof sketches below were spot-read; the full proofs total ~177k lines of OAI Lean. None of the inputs carries an
unsatisfiable hypothesis or a `False` trick, and none is trivial because of a weak definition. Because the final theorem is
closed, a too-weak input could not make it false anyway; I checked each for strength regardless.

| Input | Proved at | Statement vs cited theorem | Non-vacuous? |
|---|---|---|---|
| CharacterDistanceDivergence | `Analysis/CharacterDistanceDivergence.lean : characterDistanceDivergence` (via `character_LFunction_uniform_sublog` + `characterDistance_ge_log_sub_L`) | Qualitative: for each nonprincipal χ, ∀R ∀ᶠX ∀\|t\|≤X, D(χ,n^{it};X)² ≥ R. **Weaker than KMT Lemma 7.8** ((1/4)loglog X − C). Downstream needs only divergence (the paper's (2.16) and MRT's (1+M)e^{-M} also need only M→∞). In the unconditional chain it is threaded through but dead at the leaves (`_hKMT` unused). | yes |
| FordUpperSieveInput | `Arithmetic/BrunUpperSieve.lean : fordUpperSieveInput` | Finite-population upper sieve: S ≤ C(κ,A)·M·∏(1−g(p)) + Σ_{d\|P, d≤z}\|r_d\| under the dimension condition (Ω). Proved by a Brun-type even inclusion–exclusion truncation on disjoint logarithmic prime blocks, with explicit C = exp(exp(4(κlog2+A/log2)) + κlog8 + A/log2). Same shape as Ford 2023 Thm 2.4. | yes (C independent of population; LHS ≤ M + \|r_∅\| does not make it trivial since ∏(1−g) can be tiny) |
| SquarefreeSelbergDelangeInput | `Arithmetic/SquarefreeSelbergDelange.lean : squarefreeSelbergDelangeInput` | Σ_{n≤Y} μ²(n)z^{ω(n)} = Y Σ_{j≤H} c_j (log Y)^{z−1−j} + O_H(Y(log Y)^{z−2−H}) for all H and real Y ≥ 3, with c_0 = ∏_p(1+z/p)(1−1/p)^z/Γ(z) > 0, for z ∈ {1/4, 1/2}. Proved by Perron + zero-free region + Riesz/finite-difference unsmoothing. Faithful (restricted to the two exponents used). | yes |
| SquarefreeCharacterEstimateInput | `Analysis/SquarefreeCharacterDischarge.lean : squarefreeCharacterEstimateInput` | Siegel–Walfisz form: for q ≤ (log Y)^C and χ ≠ 1, the twisted sum is ≤ K(z,C,D)·Y(log Y)^{−D}. Uses a formalized Siegel bound (`PrimeGaps/SiegelBounds.quadratic_siegel`, `CharacterZeroFreeStrip`), so K is ineffective. The file's docstring still says "an explicit conditional input, not a proof", which is stale (see O2). | yes |
| PrimeReciprocalMertensInput | `Arithmetic/MertensDischarge.lean : primeReciprocalMertensInput` ← PNT+ `Erdos970.Mertens.E₂p.abs_le` | \|Σ_{p≤x}1/p − loglog x − M\| ≤ C/log x. M is existential, but the C/log x bound pins it to Mertens' constant, so this is not weakened. | yes |
| PrimeProductMertensInput | same file : `primeProductMertensInput` ← `E₃.bound'`, `prod_one_minus_div_prime_eq` | log x·∏_{p≤x}(1−1/p) → e^{−γ}, the exact constant. | yes |
| FiniteMcDiarmidInput | `Probability/FiniteMcDiarmidDischarge.lean : finiteMcDiarmidInput` | P(f − Ef > a) ≤ exp(−2a²/(n c²)) under Hamming-Lipschitz \|f x − f y\| ≤ c·d_H(x,y). That condition is equivalent to equal bounded differences c_i = c, and the constant matches McDiarmid (6.7). Proved by Chernoff + a Hoeffding-lemma MGF bound (`finite_product_mgf`). The degenerate case nc² = 0 is handled correctly by the bound ≤ 1. | yes |
| FiniteBinDistributionInput | `Arithmetic/FiniteBinDistributionDischarge.lean : finiteBinDistributionInput` (`finiteBinStateDistribution`, `highBinGenerating_eq_dickman`) | Gives a probability vector ν on capped count vectors such that, for every A > 0, the frequency among n ≤ Ax with bins at x tends to ν(r), with ν independent of A. The "no factor in bins ≥ k" marginal is ρ(J/k). Faithful to Lemma 2.1 without residues; residues and weights are handled downstream. The docstring cites Tenenbaum 2000's *rate* theorem, but only the qualitative limit is stated and proved. | yes |

## 3. Statement faithfulness (comparator vs Theorem 1.1 / Corollary 1.2)

I checked the comparator `ComparatorChallenges/JointDickman.lean` against `PaperMain.lean` and the paper.

- **Definitions are textually identical** in the comparator and the solution: `OAI.Erdos970.NumberTheoryLean.DelayConstruction.
  {kernel, stepApprox, delay}` and `…Dickman.rho` (in `Jacobsthal/Renewal/DickmanFiniteDecay.lean`), `OAI.JointDickman.
  empiricalCount` (Basic.lean) and `realDensity` (MainStatements.lean). The three theorem statements are character-identical.
- **ρ is the Dickman function.** The delay construction gives ρ = 1 on (−∞,1] and ρ(u) = 1 − ∫_1^u ρ(t−1)/t dt, which is
  uρ′ = −ρ(u−1). Numerical check (L_work/rho_check.py): this construction gives ρ(1.5) = 0.594534891 (vs 1−ln1.5), ρ(2) =
  0.306852819 (vs 1−ln 2) and ρ(3) = 0.048608387 (known value 0.0486083883).
- **Largest prime factor.** `Nat.maxPrimeFac` (Mathlib, `getLastD` of `primeFactorsList`) is P⁺ for n ≥ 2, with maxPrimeFac 1
  = 1 = P⁺(1). Irrelevant anyway, since n ≥ 2 and n+1 ≥ 3.
- **Counting and normalisation.** Counting over `Finset.Icc 2 ⌊X⌋₊` matches 2 ≤ n ≤ X. Dividing by real X with `atTop` on ℝ
  matches "all real X, ordinary unweighted counting".
- **Thresholds.** `(n:ℝ)^a` and `(n:ℝ)^b` are real powers, and **both are based at n** (P⁺(n+1) ≤ n^b), exactly as printed.
  The ranges 0<a<1 and 0<b<1 match.
- **Corollary 1.2.** Strict P⁺(n) < P⁺(n+1) over 2 ≤ n ≤ X tends to 1/2, matching the paper. The reverse ordering is likewise
  1/2.
- **No mismatch found.**
- Aside (not my seat): FC's `erdos_371` uses `Set.HasDensity` on all of ℕ, including n = 0, 1. That is a finite change, and the
  real-X statement implies the integer one. The bridge is the coordinator's.

## 4. Route comparison (Lean vs printed sections)

The §2–3 rows are traced. The §4–§10 rows rest on module names plus spot reads of the discharge chain; I did not read them
line by line.

| § | Paper | Lean |
|---|---|---|
| 2.1 | Lemma 2.1 by factorial moments | Same content (`BinGeneratingDickman`, `DistinctBinGenerating`); stated for ν on capped vectors, every A. **Follows.** |
| 2.2–2.5 | Lemma 2.3 from MR Thm 1 (real interpolants) + MRT A.1 + Lemma 2.6 (VK) | **Different route**: in-house MR method + Halász + ζ/L(1+it) = o(log t) via Weyl sums; complex centered labels directly in the principal case (§1 above). |
| 2.6 | Profile W on (0,∞)×Ẑ, Haar measure, Radon–Nikodym | **Different, more elementary**: a compatible family of finite residue profiles V_q(a), extracted by Tychonoff compactness along the bad subsequence (`SubsequenceAmplifiedProfile.empiricalResidueCoefficient_subsequence_along`, `ResidueHilbert`: "Their compatible refinements replace an explicit construction of Haar measure on the profinite integers"). |
| 3 | Selberg–Delange, character estimates, Ford sieve, Mertens (cited) | All proved: Perron/contour + Siegel + a Brun-block sieve instead of citing Ford Thm 2.4 + PNT+ Mertens. **Follows, inputs internalised.** |
| 4 | Amplifier D_B, fair-coin model, first/second moments, Cauchy–Schwarz, off-diagonal pairs | `Amplification/*Amplification*`, `Probability/Amplification{FairKernel,FirstMoment,SecondMoment}`, `Counting/SubsequencePositive*`. **Follows.** |
| 5 | Coupling to independent model sets, endpoint kernel in cut norm | `Probability/{ArithmeticGraphKernel,CandidateSiteKernel,…}`, `Counting/BlockSiteComparison`. **Follows.** |
| 6 | Second moment for latent rows | `Amplification/Latent{Row,Edge}Square*`, `Probability/ArithmeticSecondMoment`. **Follows.** |
| 7 | Fair-split channels | `Probability/{FairSplitChannel,FiniteChannels,ResidueAttenuation,CoarseChannel}`. **Follows.** |
| 8 | Endpoint features, Fourier detection of a−b = jc, singular series; MV minor arcs | `Amplification/{SingularSeries*,MajorArc*,MinorArc*,Endpoint*}`. Minor arcs via `Arithmetic/SquarefreeMinorArc` + `DischargedSmoothMinorArc`, **not** the Montgomery–Vaughan input (which is never discharged and never used). **Follows, MV replaced.** |
| 9 | Cut-norm sampling + McDiarmid | `Counting/{SamplingTransfer,SamplingConcentration,BlockCutNorm}` + proved McDiarmid. **Follows.** |
| 10 | Main energy → products of Lemma 2.3 averages | `Counting/*Discharge` chain ending at `LaplaceShortDischarge`. **Follows.** |
| 11 | Fixed-threshold law → moving thresholds; ordering by continuity | Rational common denominator J, then monotone rational sandwich (`MovingLimit.jointDickmanLaw_of_rational_fixedScale`); ordering via a Dickman-quantile grid (`Ordering`). **Follows.** |

Paper steps the Lean never needs: MR 2016 Thm 1, MRT Thm A.1, the real nonnegative interpolation (2.18) in the principal case,
Vinogradov–Korobov / Ford's zeta bound (2.17), KMT Lemma 7.8's quantitative rate, Montgomery–Vaughan Cor. 1, profinite Haar
measure / Radon–Nikodym, and Tenenbaum's rate theorem.

**Order of limits (the brief's main worry), as the Lean enforces it.** The combined quantifier order is:

1. **Positive side** (`nonzero_binLabel_correlation_along_forces_blocks`): ∃ subsequence s, ∃ e > 0, ∃ A, ∀ L τ (τ ≤
   samplingTau), ∃ C₀, ∀ C ≥ C₀, ∀ᶠ B, ∀ᶠ N along s: e ≤ block average.
2. **Vanishing side** (`arithmetic_block_centered_mean_proved`, which is quantified over every A > 0 and L ≥ 10000): ∃ τ, ∀ ε,
   ∃ C_min, ∀ C ≥ C_min, ∀ᶠ B, ∀ᶠ N over all N.
3. **Combination** (`bin_correlation_limit_zero_proved`): τ depends on A, A on the subsequence, and C = max(C₀, C₁). This is
   legitimate only because the vanishing lemma holds for every A, and the kernel checks exactly this.

So within the Lean there is no x-before-B inversion; every object chosen after the subsequence is fed into a lemma that is
uniform in it.

## 5. Patched dependencies and forbidden-construct scan

**What the patches are.**

- **PrimeNumberTheoremAnd @c39a751 + `PrimeNumberTheoremAnd.Erdos970.*`.** Namespaced ports to the newer Mathlib of
  EulerMaclaurin, Auxiliary, Sobolev, Fourier, Rectangle, ResidueCalcOnRectangles, MellinCalculus, ZetaBounds, ZetaConj and
  SmoothExistence, plus `Erdos970/MertensClassical.lean`. That file (1,982 lines) is a port of upstream `IEANTN/Mertens.lean`
  (2,454 lines, no `sorry`; 622 differing diff lines). It proves Mertens' second and third theorems with explicit O(1/log x),
  and the closure uses it (Mertens inputs).
- **StrongPNT @2f5835c + `StrongPNT.Erdos970.*`** (PNT1_ComplexAnalysis, PNT2_LogDerivative, PNT3_RiemannZeta,
  PNT4_ZeroFreeRegion, Z0, ZetaZeroFree, PNT5_Strong). Diffs against the upstream copies in the same tree are namespace and
  import renames, Mathlib API fixes and deleted blueprint comments. The originals contain no `sorry` and the patch does not
  fill any. The headline theorem is `Strong_PNT : ∃ c > 0, (ψ − id) =O[atTop] x·exp(−c·(log x)^{1/2})`, built on the de la
  Vallée Poussin zero-free region.
- **How StrongPNT reaches the joint-law closure** (import trace, L_work/importers.py): via
  `Jacobsthal/Primes/HighPrimeRemoval` (`psi_strong`, `theta_strong`) and `TwoPointCorrelations/ModFive{HighZeros,
  LogDerivative}`. Both feed `TwoPointCorrelations.Halasz*` → `JointDickman/Amplification/HalaszArithmetic`. Constant-level use
  is not checked statically; the replay's dependency dump would show it.
- **Unpatched PNT modules in the closure:** Auxiliary, Fourier, Rectangle, ResidueCalcOnRectangles, EulerMaclaurin,
  ZetaBounds, Asymptotics.Uniformly, Wiener, PerronFormula and Tactic.AdditiveCombination. Some of them import LeanArchitect
  (@468e8f5).

**Scan** (L_work/scan.py) over 1,837 files: the 1,796 in oai_files.txt + 41 pnt/strongpnt/Architect modules from
all_order.txt, with comments stripped. The OAI files total about 177k lines.

| construct | count | where |
|---|---|---|
| `sorry` | 3 | all in `ComparatorChallenges/JointDickman.lean` (the challenge, by design; not imported by the solution) |
| `admit` | 1 | Architect/Tactic.lean: `g.admit` inside the *definition* of the `sorry_using` tactic. `sorry_using`/`blueprint_using` are used nowhere in OAI, Erdos970 or StrongPNT files. |
| `axiom` | 2 | pnt `Tactic/AdditiveCombination.lean` l.172–173 (`axiom qc`, `axiom hqc`). These sit inside a `/-- … -/` docstring example (l.120–178); my regex stripper missed it because of a nested `/- -/`. Not code. |
| `unsafe`, `debug.skipKernelTC` | 1 each | Architect/Load.lean `runEnvOfImports`, an IO blueprint-export runner. It does not run during elaboration of the proof modules and cannot affect the kernel replay. |
| `native_decide`, `implemented_by`, `extern`, `@[csimp]`, `opaque`, `ofReduceBool`, `trustCompiler`, `run_cmd`/`#eval`, `set_option debug.*`, `maxRecDepth` | 0 | — |
| `macro`/`elab`/`syntax`/`initialize`/`partial def` | Architect and the AdditiveCombination tactic only | **0** in any OAI file (no metaprogramming at all in OAI) |
| `maxHeartbeats` | 1 | Architect only (0 in OAI) |

---------------------------------------------------------------------------------------------------------------------------

## Objections

- **O1 (EXPOSITION).** Paper §1.2: "the real short-interval theorem of Matomäki and Radziwiłł [16, Theorem 1] … The complex
  theorem of Matomäki, Radziwiłł and Tao [17, Theorem A.1, corrected version] controls the nonprincipal twists. The rest of
  the proof must reduce the mixed correlation to this particular cancellation statement." The formal proof shows that neither
  black box is needed for these labels, nor is VK ((2.17) in Lemma 2.6). A specialised MR argument + Halász + ζ/L(1+it) =
  o(log t) suffices (§1 above). The paper is not wrong; it cites more than it uses. Worth saying in the paper, because a reader
  auditing "unconditional" otherwise has to trust MRT's *corrected* Prop A.3.
- **O2 (EXPOSITION, Lean docs stale).** Two docstrings describe things as conditional when they are discharged:
  - `Amplification/PublishedInputs.lean` header: "These definitions are *propositions to be supplied as hypotheses*. They are
    not axioms or proofs of the cited analytic theorems."
  - `Analysis/CharacterInputs.lean`: "This is an explicit conditional input, not a proof of that analytic result."

  True of the Props, misleading about the unconditional theorem. Also, `CharacterDistanceDivergence` is threaded through the
  whole unconditional chain but unused at the leaves (`_hKMT` in `nonprincipal_weightedBinAverage_short_proved`). The scope
  note `docs/012.md` does not say that MR/MRT/MV/KMT are not used.
- **O3 (EXPOSITION).** `BinMarginalInput.lean` cites Tenenbaum 2000's rate theorem, but `FiniteBinDistributionInput` states and
  proves only the qualitative finite-bin limit. Harmless.
- **No FATAL, GAP or ERROR-NONFATAL objection against the Lean-vs-paper correspondence.** The statement is faithful, the
  route is followable, every input is discharged by a proof that I sampled and found genuine, and the scan is clean.

**Caveats.** (i) The verdict is conditional on the separate kernel replay: `#print axioms PaperMain.joint_law / increasing_order
/ decreasing_order` ⊆ {propext, Classical.choice, Quot.sound}, and comparator acceptance. (ii) §4–§10 were mapped by module
name and discharge-chain spot reads, not line by line. (iii) The ~177k lines were not read in full; the kernel, not this
reader, certifies the intermediate steps.

VERDICT: HOLDS AS READ
