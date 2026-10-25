# Seat L report: Lean ↔ paper ↔ problem

Paper: "Short Egyptian fractions" (OpenAI, 25 Sep 2026). Lean: `/tmp/oaimath/024/repo/lean` (HEAD `1581d4cb`; Lean v4.34.1, Mathlib `d13f23b7`).
I read the source only. I compiled nothing; the kernel replay runs separately. Working files: `/tmp/oaimath/025/seats/L_work/`
(`closure.py`, closure lists, `enum.py`).

## 0. Summary of findings

| # | Finding | Class |
|---|---|---|
| L1 | Both comparator files state Thm 1.1, Cor 1.2 and Cor 1.3 faithfully. Erdős #304, #148 and #293 are stated under the right conventions: #304 has n_1 ≥ 2, #148 has n_1 ≥ 1, #293 counts m ≥ 2. I checked every junk-value trap (sInf, `Finset.sup`/`if`, `ncard`, `liminf`/`limsup`, `log log` of small arguments). Each one is either excluded by a proved conjunct or can only make the statement false, never vacuous. | no objection |
| L2 | The two developments are independent. `ShortEgyptian` (58 files) and `EgyptianFractions` (290-file import closure) have no cross-imports and use different namespaces and data representations. Both follow the paper's route: dense family (Prop 2.1), then descent (§§3–5), then two-numerator split (§2). | no objection |
| L3 | The Lean does not contain a complete quantitative three-prime theorem. The minor arcs are proved unconditionally (Vaughan). The major-arc main term is left as an explicit hypothesis. None of this is used by the comparator theorems. `quantitative_marked_length` (Prop 8.1) is proved by a different "cube-free composite" supply construction that avoids Vinogradov entirely. So the formal certificate covers Prop 8.1 and Cor 1.3, but it does not machine-check the paper's own proof of Lemma 8.2, (8.2) (§8.1). | EXPOSITION (scope of verification) |
| L4 | Places where the Lean is weaker than, stronger than, or different from the paper. None affects any stated result. Details in §3. | — |
| L5 | Formal Conjectures. FC_304 `upper_bound` needs a routine bridge, sketched below. FC already annotates it with OpenAI's `ShortEgyptian/Main.lean#L33`, but the statements are not syntactically the same. FC_148 `erdos_148` (Θ of F itself) is not settled by the result; I propose an honest variant. FC has no 293 file; a draft is below. | EXPOSITION (FC) |

Forbidden-construct sweep: I grepped every file of both import closures (58 + 290) for `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `@[extern`, `opaque`, `unsafe`, `partial def`, `decide := true`, `maxRecDepth`, `csimp`, `ofReduceBool`, `trustCompiler`, `elab`, `macro`, `syntax`/`notation`, `run_cmd`, `#eval`, `import Lean`, and every `set_option`.

- Zero hits outside docstrings. The two hits are prose: `RationalSupplyReduction.lean:96` and `RationalDivisorSupplyAlgebra.lean:97`, both saying "not an axiom". There are no `set_option`s at all.
- Local instances are Decidable only:
  - `scaleFinDecidableEq := Classical.decEq _` (ShortEgyptian/ScaleBounds.lean:7)
  - `local instance : DecidablePred BadModulus := Classical.decPred _` (CompositeBadDensity*.lean)
  - `Classical.propDecidable`
  - an `InBand` decidability instance via `infer_instance` (DyadicBands.lean:13)
  - Decidable instances carry proofs and cannot assert anything false.
- `@[irreducible] def dimM` and `@[instance_reducible]` are elaboration attributes with no soundness effect.
- Comparator JSONs:
  - permitted axioms are `propext`, `Quot.sound`, `Classical.choice`
  - `definition_names: []`
  - `enable_nanoda: false`, so there is no second kernel.
- `OAI/NumberTheory/EgyptianFractions/Defs.lean` is textually identical to the definitions in `ComparatorChallenges/EgyptianFractions.lean`. `ShortEgyptian/Model.lean` is textually identical to the definitions in `ComparatorChallenges/ShortEgyptianFractions.lean`.

## 1. Statements vs paper vs problems; junk-value traps

### 1a. `ComparatorChallenges/ShortEgyptianFractions.lean` (`OAI.ShortEgyptian.main`)

- `IsExpansion a b ns := ns.Pairwise (·<·) ∧ (∀ n ∈ ns, 2 ≤ n) ∧ (ns.map (1/·)).sum = a/b` (in ℚ).
  - Pairwise `<` means strictly increasing, hence distinct.
  - `2 ≤ n` is #304's "1 < n_1".
  - The ℚ equality means a/b need not be reduced, matching the paper's §1 sentence "The fractions a/b need not be in lowest terms".
- `minLength a b := sInf {k | ∃ ns, IsExpansion a b ns ∧ ns.length = k}`. Junk trap: sInf ∅ = 0. This is closed by the first conjunct of `main`, `∀ a b, 1 ≤ a → a < b → ∃ ns, IsExpansion a b ns`, so `minLength` is a genuine minimum.
  - Without that conjunct, the upper bound could hold vacuously with junk 0.
  - The lower bound never could, since junk only makes it harder.
- `maxMinLength b := (Finset.Ico 1 b).sup minLength` is exactly N(b) = max_{1≤a<b} N(a,b).
- `∃ c₁ c₂ > 0, ∃ b₀ ≥ 2, ∀ b ≥ b₀, c₁ log log b ≤ N(b) ≤ c₂ log log b` is Theorem 1.1 verbatim. b₀ is existential, so small-b behaviour of `Real.log (Real.log b)` is irrelevant. For large b the inequalities are genuine.

### 1b. `ComparatorChallenges/EgyptianFractions.lean` (9 theorems, `OAI.Problem337.*`)

Note: `Problem337` is OpenAI's internal label. It is unrelated to Erdős #337 (FC_337 is about additive bases). This is only a naming hazard.

**`IsEgyptianExpansion`, `egyptianLength`, `maxEgyptianLength`.**
- `IsEgyptianExpansion` uses `2 ≤ n i ∧ StrictMono n ∧ ∑ 1/n i = x`.
- `egyptianLength := sInf`. Its nonemptiness and minimality are given separately by `egyptian_length_is_minimum`, so it is not junk.
- `maxEgyptianLength b := (range b).sup (fun a => if 1 ≤ a then egyptianLength a b else 0)` is the max over 1 ≤ a < b. The `a = 0` term contributes 0, which is harmless.
- `main_double_log_order` is Theorem 1.1. Its b₀ has no `2 ≤ b₀` clause, which doesn't matter because b₀ is existential.

**`IsOneExpansion` and `F`.**
- `IsOneExpansion` uses `1 ≤ n i`, which is #148's 1 ≤ n_1.
- `F k := (OneExpansions k).ncard`. Junk trap: ncard of an infinite set is 0. This is closed by `one_expansions_finite_and_bounded` (`Set.Finite (OneExpansions k)` for all k).
- Independently, the lower half of `counting_double_log_order` (c k ≤ log log F k) forces F k ≥ exp(exp(ck)), so junk could never satisfy it. Only the upper half would be vacuous on junk, and finiteness rules that out.
- `counting_double_log_order` is Corollary 1.2.

**`one_expansions_finite_and_bounded`.**
- It states `F k ≤ k^(2^k − 1)` and `n i ≤ k^(2^i.val)`, with i 0-based.
- This is exactly the paper's §6 bound "n_i ≤ k^{2^{i−1}}" (1-based) and "F(k) ≤ ∏ k^{2^{i−1}} = k^{2^k−1}".
- ℕ subtraction `2^k − 1` is never truncated.

**`D`, `missingDenominators`, `v`, `missing_denominator_semantics`.**
- `D k := {m | 2 ≤ m ∧ ∃ n, IsOneExpansion n ∧ ∃ i, n i = m}` and `v k := sInf ({m | 2 ≤ m} \ D k)` match the paper's D_k and v(k) = min({2,3,…} \ D_k).
- They also match #293 under the reading the site adopted (Woett, 8 Dec 2025: "the smallest integer larger than 1 that does not appear"). Note that 1 occurs only for k = 1, so counting m ≥ 1 would make v(k) = 1 for all k ≥ 2.
- Junk trap: sInf ∅ = 0. This is closed by `missing_denominator_semantics`, which proves:
  - `D k` is finite;
  - the complement is nonempty;
  - `2 ≤ v k`;
  - `v k ∉ D k`;
  - every `2 ≤ m < v k` lies in `D k`;
  - `v k ≤ 1 + k^(2^(k−1))` for k ≥ 1.
- The page notes the original ErGr80 source is ambiguous about what is asked. The Lean, like the paper, takes the site's m ≥ 2 reading.

**`prescribed_denominator_corollary` (Cor 1.3), all three displays.**
1. `∃ k0, ∀ k ≥ k0, exp(exp(k/600)) ≤ v k ∧ v k ≤ 1 + k^(2^(k−1))`.
2. `log 2/257 ≤ liminf ∧ liminf ≤ limsup ∧ limsup ≤ log 2` for `prescribedSlope k = log log v(k) / k` (k = 0 gives /0 = 0, which is harmless).
3. `∀ c < log 2/257, eventually exp(exp(ck)) ≤ v k`.

Liminf/limsup junk question. In Mathlib, `liminf u = sSup {a | ∀ᶠ n, a ≤ u n}` and `limsup u = sInf {a | ∀ᶠ n, u n ≤ a}`. In ℝ, sSup or sInf of an empty or unbounded set is 0. Conjunct 1, which is proved in the same theorem, makes the sequence eventually bounded on both sides:
- Lower: v ≥ exp(exp(k/600)) gives log log v ≥ k/600, so the slope is ≥ 1/600.
- Upper: v ≤ 1 + k^{2^{k−1}} gives log log v ≤ k log 2 + log log k, so the slope is ≤ log 2 + o(1) ≤ log 2 + 1.

So the sequence is bounded and cobounded in both directions, and both liminf and limsup are genuine. The proof itself builds `IsBoundedUnder (· ≤ ·) atTop prescribedSlope` (`PrescribedCorollary.lean`, `hbounded`) and feeds it to `liminf_slope_lower_of_double_exp`. Even setting that aside:
- `log 2/257 ≤ liminf` can never hold by junk, since junk is 0 and 0 < log 2/257.
- The content is carried independently by conjunct 3 (lower slope) and conjunct 1 (upper slope).
- Only `liminf ≤ limsup` and `limsup ≤ log 2` could be junk-true for an unbounded sequence, and that case is excluded.

**`quantitative_marked_length`, `exact_marker_padding`, `every_exact_marker_occurs`.**
- `quantitative_marked_length` is Proposition 8.1 verbatim. It gives a `(257/log 2 + ε) log log m` length bound for m ≥ m_ε, with `2 ≤ m_ε`.
- `exact_marker_padding` (r ≥ 3, any marker kept, length r → r + 1) is Lemma 7.2.
- `every_exact_marker_occurs` is §7's "the same construction also supplies the finite exceptional values of m".

### 1c. Small-case numerical check

`L_work/enum.py` exhaustively enumerates k ≤ 6:

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F(k) | 1 | 0 | 1 | 6 | 72 | 2320 |
| v(k) | 2 | 2 | 4 | 11 | 17 | 103 |

- F matches OEIS A006585 and FC_148 `F_first_values`. v matches the #293 forum values (4, 11, 17, 103).
- `n_i ≤ k^(2^i)` (0-based), `F(k) ≤ k^(2^k−1)` and `v(k) ≤ 1 + k^(2^(k−1))` hold for all k ≤ 6. The largest denominator for k = 6 is 3263442.

### 1d. Versus the problems

- **#304.** The page asks "Is it true that N(b) ≪ log log b?". The answer is yes, together with the classical lower bound, and both are stated.
- **#148.** The page says "Find good estimates". The Lean gives log log F(k) ≍ k (two-sided, explicit-exponent form, plus the elementary F(k) ≤ k^{2^k−1}).
- **#293.** The page says "Estimate the growth of v(k)". The Lean gives log log v(k) ≍ k, with log 2/257 ≤ liminf ≤ limsup ≤ log 2 and the explicit eventual bound exp(exp(k/600)) ≤ v(k).

## 2. The two developments: independence, route, section map

### Independence

- Import closure of `OAI.NumberTheory.ShortEgyptian.Main`: 58 modules, all in `ShortEgyptian/`. Its only external import is `Mathlib`.
- Import closure of `OAI.NumberTheory.EgyptianFractions.Main`: 290 modules, all in `EgyptianFractions/`. External imports are `Mathlib`, `Mathlib.Basic.Complex.Basic`, `Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt` and `Mathlib.NumberTheory.Chebyshev`.
- Neither directory references the other (`grep ShortEgyptian EgyptianFractions/` is empty).
- `main_double_log_order` is therefore a second, independent formalization of the upper bound. It uses its own definitions (`Fin k → ℕ` with `StrictMono` rather than `List`), its own lemmas and its own constants.

### Actual proof dependency inside EgyptianFractions

Main's proof bodies reference these names:
- `egyptianLength_attained_of_exists`, `egyptianLength_le_of_expansion` (LengthBasic)
- `exists_strict_unit_fraction_sum` (EgyptianExistence)
- `exists_raw_density_supply` (RawDensityExistence)
- `main_upper_of_raw_density_supply` (RawDensityUpper)
- `main_double_log_lower_bound` (MainLowerVerified)
- `finite_ncard_le_egyptian_box` (FiniteBox)
- `one_expansion_denominator_bound` (DenominatorBound)
- `exact_marker_padding_proof` (ExactPadding)
- `every_exact_marker_occurs_proof` (MarkerOccurrence)
- `missing_denominator_semantics_of_bound` (MissingSemantics)
- `prescribed_denominator_corollary_of_inputs` (PrescribedCorollary)
- `counting_order_of_main_upper` (CountingFromMain)
- `CompositeSupply.quantitative_marked_length` (CompositeSupplyFinal)

The union of the import closures of those defining modules is 234 modules (`L_work/used_closure.txt`). It contains no ThreePrime*, Vaughan*, MinorArc*, MajorArc* or Mangoldt* file. The other 56 modules of the 290 are imported by Main (via `MarkedThreePrimeReduction`, `MangoldtMajorArcReduction` and `CountingFromMarkers`) but cannot be referenced by the comparator theorems. The directory also has a further 76 files (`GoldbachSieve*`, `Selberg*`, `ThreePrimeMinorArc`, `PeriodicMajorArcs`, …) that Main does not import at all.

This is a textual import-graph argument. A constant can only be referenced from a module that transitively imports its definition. A constant-dependency dump from the replay (for example `CollectAxioms`-style traversal of constants) would confirm it mechanically.

### Route

Both developments follow the paper's route:
- Prop 2.1 dense family plus §2 split.
- Lemma 3.1 uniform divisor moment.
- Lemma 4.1 residue lists: deterministic products T0 at high levels, random products T1 at middle levels, R = 1000 independent lists at terminal levels, then a binary range.
- §5 Hölder recurrence over the descent.

Constants are the paper's (4.2):
- `RawDensityParameters.lean`: DM = 204204 = (2·1000+2)(100+2), D0 = 10^5, η = 10^−4, c* = 1/1000, K_d = 3(DM+2)/η, moment order r = 8K_d. The paper's §5 requires "r ∈ N, r ≥ max{2, 8K_d}", and the Lean takes exactly the minimum.
- ShortEgyptian `ScaleGeometry.lean`: `dimM = (2*1000+2)*(100+2)`, `dimX = dimM+2`, `dimC = 4*dimX`.

The EgyptianFractions Prop 2.1 object `DenseEgyptianFamily DM L S C` (MainUpperReduction.lean:15) is Prop 2.1 verbatim:
- e^S < M ≤ e^{DM S};
- |{1..⌊X⌋} \ G| ≤ X/8 with X = e^{(DM+2)S};
- each u ∈ G has u/(MC) as a list of at most L log S unit fractions with denominators ≥ 2 (repetitions allowed);
- C ranges over [e^{4(DM+2)S}, e^{8(DM+2)S}].

ShortEgyptian's `DenseData` (Density.lean:20) is the same object.

### `exists_raw_density_supply` (the "Supply/Interface" check)

`RawDensitySupply` is a `def … : Prop` packaging a `DensityResidueFamily` with size conditions. Main obtains it from `exists_raw_density_supply` (RawDensityExistence.lean, end of file). That lemma instantiates `RawDensityParameters.*` with `eventually_raw_density_supply`, which is proved by `filter_upwards` over these lemmas:
- `eventually_common_residue_lists` (via `eventually_sampled_denominator_certificate`);
- `eventually_geometric_high_residue_lists` (via `deterministic_high_residue_distribution`, the §4.2 deterministic list);
- `eventually_common_geometric_random_fractional_residues` (§4.3 random lists);
- `eventually_residue_level_moment` (Lemma 3.1 feeding §5);
- `eventually_raw_density_supply_of_residue_data`.

All of these lie inside the closure, carry no hypotheses, and are sorry-free. `main_upper_of_raw_density_supply` composes this with `eventually_dense_family_of_raw_supply` (§5) and `main_upper_of_dense_family` (§2). So the supply is unconditional. The same holds in ShortEgyptian: `eventually_density`, `exists_residueSystem`, `eventually_ListScale` and `eventually_MomentScale`. Every hypothesis-carrying structure (`ResidueSystem`, `ListScale`, `MomentScale`, `DenseData`) is discharged by an `eventually_*` lemma.

### Section map: ShortEgyptian (58 files, about 8.1k lines, 383 KB)

| Printed section | Files |
|---|---|
| §1 definitions, identity (4.1)/(4.5) | Model, Basic (`residue_identity`, `predecessor_dvd`) |
| §2 (Lemma 2.2, Lemma 2.3, proof of Thm 1.1, lower bound) | Distinctness (`remove_repetitions`, Takenouchi swaps), GreedyPreparation (`prepare_denominator`), GreedyExistence, DenseSplit, UpperAssembly (`dense_remainder` = the gAM split, `upper_at_scale`), LowerBound (`main_lower`), Main |
| §3 Lemma 3.1 | TruncatedDivisors, PrimeSplitting, DivisorWeights, DivisorMoments, SmoothBounds, PrimeReciprocals, MomentDecay, MomentAsymptotics (`uniform_divisor_moment`, natural r) |
| §4.1 Lemma 4.1, (4.2)–(4.7) | ScaleGeometry, ScaleBounds, PrimeLists, ListConstruction, ResidueAssembly, ResidueSystem (`structure ResidueSystem` = items 1–3 of Lemma 4.1 with c* = 1/1000 and η = 10^−4, `exists_residueSystem`) |
| §4.2 Lemmas 4.2–4.4 | FiniteFourier, FourierDiscrepancy, WindowSpectrum, WindowDiscrepancy, ResidueDiscrepancy (Lemma 4.2), FirstDerivative, SecondDerivative, IntervalDifferencing, IteratedDifferencing, ReciprocalDifferences, ReciprocalEstimates, ParameterBounds (Lemma 4.3), DeterministicMean, DeterministicLists (Lemma 4.4) |
| §4.3 Lemma 4.5 | PrimeProducts, BilinearProducts, ProductCorrelations, HammingDistance, SamplePartitions, RandomMoments, RandomBounds, EmpiricalDiscrepancy, ListSelection |
| §4.4 common choice | LevelSelection (`choose_random_lists`), ListSelection (`simultaneous_finite_selection`) |
| §5 | DescentSets, DoubleCount, DivisorCover, Holder, MomentRecurrence, RecurrenceUnrolling, DensityBounds, TerminalExpansion, TerminalScale, SelectionBounds, Density |

ShortEgyptian formalizes only Thm 1.1 (§§2–5). It does not touch §§6–8.

### Section map: EgyptianFractions (234 used modules)

| Printed section | Files |
|---|---|
| §2 | EgyptianExistence, LengthBasic, GreedyStep, GreedyPreparation, GreedyBudget, RepeatedSquaring (Lemma 2.3), RemoveRepetitions, Distinctize, FixedSumFinite (Lemma 2.2), DensePairing, DenseExpansion, MainUpperReduction, MainLowerAppend, MainLowerVerified |
| §3 | TruncatedDivisors, UniformDivisorMoment (Lemma 3.1, real r ≥ 0), Divisor* (BandDecay, Classes, ClassAssembly, Counting, Density, EnergyNesting, FactorBound, LocalFactor, MomentAbsorption, MomentFinalBudget, PointwiseUniform, PrefixCounting), Rankin*, SmoothRankin*, SmallPrime*, Rough*, LargePrime*, Harmonic*, IntermediateBand*, *PrefixClass, SubcriticalPowerSum, PrimeReciprocal* |
| §4.1 | ResidueLevels, DensityParameters, RawDensityParameters, PrimePool*, ResidueDenominator*, SampledResidueDenominator, SampledDenominatorCertificate, ResidueWideDenominator |
| §4.2 | Cyclic* (Lemma 4.2), Fejer*, DeterministicMean*, DeterministicPhaseWindow, DeterministicReciprocal, ReciprocalPhase*, ReciprocalDerivatives, ReciprocalDifferencingBudget, VanDerCorput, SecondDerivativeTest, SecondDerivativeBudget, Discrete{First,Second}Derivative, IteratedDifferencing, ForwardDifference, SecondDifference, HighResidueDistribution, DeterministicResidueSupply |
| §4.3 | Random*, Geometric{RandomRanges,RandomResidues,CharacterBound,RawDensity}, HammingException, PrimeHits, PrimeGcdHits, HitCount, *Exposure*, Fourier{CommonRealization,FailureBounds,SecondMoment,FrequencyGap}, IndependentBlockSelection, SimultaneousSelection, SampleWordTransfer, FiniteResidueIndices |
| §4.4 | ResidueRegimeSplice, RawDensityExistence |
| §5 | BadPredecessorCount, GoodNumeratorSets, DescentHolder, DescentRecurrence, DescentDecay, DescentDepth, DensityLoss, DensityMoment*, DensityAssembly, Terminal*, BinaryExpansion, BackwardExpansions, CeilResidue, ResidueStep, LeastResidueBridge, RawDensityUpper |
| §6 | DenominatorBound, FiniteBox, CountingUpper, MarkedCleanup (Lemma 6.1 analogue), OddPrimorial, DivisorSplit, SplitArithmetic, DivisorCounting, CountingFromMain ((6.1) branching), CountingPadding ((6.2) injection), CountingTransfer |
| §7 | MarkedGreedy (Lemma 7.1), ExactPadding (Lemma 7.2), MarkerOccurrence, MarkerCoverage, MissingSemantics, PrescribedInversion, PrescribedAnalysis, UpperSlope, PrescribedCorollary |
| §8.2–8.3 | MarkedGreedyDensity (Lemma 8.3: `divisorDense`), MarkedGrouping, MarkedGroupingFin, MarkedGroupingUnits (Lemma 8.4), MarkedBudget, MarkedEndgame (257 = 1 + 16·16), MarkedConstruction, MarkedReduction, MarkedQuantitative, MarkedPrefixBridge, CompositeMarkedReduction |
| §8.1 Lemma 8.2 (different route, see below) | CompositeSupplySize, CompositeBadModuli, CompositeBadDensity*, CompositeConductorBudget, CompositeSpectral, CompositeUnitMixing, CompositeRationalSupply, CompositeSupplyFinal, CubeFree*, EightProduct*, RationalDivisor*, RationalSupplyScaling, ThinSupplyBase, SparseBadDivisorTail, CollisionCounting, ReducedCollisionFourier, ReducedCharacter, BilinearFourier, FiveProducts, PrimeObstruction, PrimeProduct*, PrimeFactorPrefix, PrimePrefixSize, PrimeTripleAsymptotics (elementary), SupplySize |

### Three-prime material (question 2, last part) — finding L3

What is proved unconditionally:
- `MinorArc.eventually_vonMangoldt_minor_arc_bound D` (MinorArcVaughan.lean:13). For every D, for all large N, for every θ ∈ [0,1] outside `majorArcUnion ⌊(log N)^{2(D+6)}⌋ (2(log N)^{2(D+6)}/N)`, we have ‖∑_{n≤N} Λ(n) e(θn)‖ ≤ N/(log N)^D. This is Vaughan's identity plus Dirichlet geometry, all proved in Vaughan*.lean and MinorArc*.lean.
- From that, `eventually_mangoldt_minor_integral_le`: the minor-arc part of ∫_0^1 S(x)^3 e(−Nx) dx has norm ≤ N^2/log N. Its little-o form is `mangoldt_minor_integral_isLittleO`.
- `threePrimeSingularSeries` and its uniform positivity for odd u (`threePrimeSingularSeries_one_le`), prime-power removal, and unweighting.
- The exact major/minor decomposition `mangoldt_coefficient_eq_major_add_minor`.

What is not proved anywhere in the repository is the major-arc main term, which needs Siegel–Walfisz or PNT in progressions for moduli up to (log N)^{18}. It appears only as a hypothesis:
- `quantitativeThreePrimeLowerBound_of_major_lower (hmajor : ∃ c>0, ∀ᶠ N, Odd N → c N² ≤ (majorIntegral N).re)`
- `ternaryMangoldtAsymptotic_of_major_asymptotic (hmajor : …)` (MangoldtMajorArcReduction.lean:55, :75)
- `quantitativeThreePrimeLowerBound_of_singular_error (herror : …)`, whose docstring says "The asymptotic estimate remains a hypothesis; no Vinogradov theorem is asserted."
- `eventual_marked_list_supply_of_three_primes (hthree : QuantitativeThreePrimeLowerBound)` and `quantitative_marked_length_of_three_prime_lower_bound (hthree : …)` (MarkedThreePrimeReduction.lean). This is the paper's own §8.1 route (`markedSupplyMultiplier m = P(⌈16 log m/log 2⌉)^2 · ⌊log log m⌋!`, exactly K_m). It is formalized only conditionally on `QuantitativeThreePrimeLowerBound` (∃c>0, eventually for odd u, #prime triples summing to u ≥ c u^2/log^3 u).

The theorem Main actually uses is `CompositeSupply.quantitative_marked_length` (CompositeSupplyFinal.lean:74). Its docstring reads "proved by the composite cube-free route without any prime-triple distribution premise". The route, briefly:
- Multiplier K = base(m^4)^4, where base(u) is the product of the first ⌈2 log u/log 2⌉ primes. For u = m^4 that is 8 log m/log 2 primes, so log K ≤ (32/log 2 + ε) log m log log m (`eventually_log_multiplier_le`). This is the paper's (8.1) constant.
- Let G be the set of cube-free q ≤ m^4 having no "bad" divisor d ≥ log Y. Here d is bad when the divisors of base(d) collide too often mod d (`BadModulus`). G has density > 2/3 (`card_good_sdiff_gt_two_thirds`, `eventually_badMultiples_card_le`, a Gallagher-type collision count).
- Every s ≤ m^4 is (g·s)/g split as a sum of two members of G. This is the §2 dense-split trick again.
- Each good q is written as ≤ 8 rationals e/t with e | base^2, via an eight-product collision and Fourier argument over all divisors of a composite modulus (`rational_divisor_sum_eight_of_divisor_collision`), after stripping the base-smooth part.
- This gives `HasRationalDivisorSupply m K 16`. That is the paper's (8.2) with h ≤ 16, so 257 = 1 + 16·16 is unchanged.

Consequence. The comparator certificate does establish Prop 8.1 and Cor 1.3 unconditionally. It does not certify the paper's §8.1 argument. The paper's proof relies on:
- the quantitative three-prime theorem, cited as "[15, (1)–(2)] and the exposition in [16, Theorem 1 and Section 3.1]";
- the exceptional-prime count (8.3);
- the five-product Fourier step.

All three are unformalized as used. The cited statement itself is standard and correct as used: r_3(u) ≫ 𝔖(u) u^2/log^3 u with 𝔖(u) ≥ 2∏_{p>2}(1 − (p−1)^{−2}) > 0 for odd u, an absolute constant and an absolute threshold. A reader of the paper should know that the machine check of Cor 1.3's numerical slope rests on a different proof of Lemma 8.2's (8.2).

## 3. Weaker / stronger / different (question 3)

1. **Lower constant c₁ = 1/2** (both developments: `main_lower`, `main_double_log_lower_bound`).
   - The Lean proves log log b ≤ 2·N(b−1,b) (`loglog_le_twice_length`).
   - The paper's §2 proves "log log b ≤ k log 2 + log log(k+1) ≤ (1 + log 2)k", which gives c₁ = 1/(1+log 2) ≈ 0.5906 asymptotically.
   - The Lean is weaker in the constant. Theorem 1.1 only asserts existence, so this does not matter.
2. **Upper constant.**
   - ShortEgyptian's c₂ is the explicit `upperConstant = greedyConstant + 2·densityConstant`, with `densityConstant = terminalConstant + 3·dimX·10^4` (about 6×10^9 or more).
   - EgyptianFractions uses c₂ = 2/log 2 + 2 + 2L + 2.
   - The paper leaves c₂ unspecified ("without quantifying the constant c₂", §1).
3. **Lemma 3.1.** EgyptianFractions proves it for every real r ≥ 0 (`eventually_uniform_divisor_moment`, with exactly the paper's hypotheses S/(2 log S) ≤ log X ≤ DS, √X ≤ Y ≤ X, N ≤ e^{DS}). That is stronger than the paper's r ≥ 1. ShortEgyptian proves it for natural r, which is enough because the descent uses natural r.
4. **Lemma 4.2.** Both Lean developments replace the cited Erdős–Turán inequality (4.8) ([9]) with a self-contained finite-cyclic discrepancy lemma:
   - ShortEgyptian: `finite_residue_discrepancy`.
   - EgyptianFractions: `cyclic_small_interval_of_fourier_automatic`.
   - The shared statement: if the Fourier coefficients satisfy |·| ≤ δ^3 for frequencies 1 ≤ ℓ ≤ ⌊δ^{−4}⌋, then at least δ/2 of the mass has residue < δq.
   - With δ = e^{−ηw} this is exactly Lemma 4.2's e^{−3ηw}/e^{4ηw} parameters. The paper's citation is therefore not load-bearing for the formal proof.
5. **Prime number theorem.** The paper cites the PNT ([19]) for |P| ≥ S^{K−1} and for log P(v) = (1+o(1))ℓ log ℓ.
   - ShortEgyptian uses a central-binomial Chebyshev bound (`PrimeLists.dyadic_prime_count_lower`).
   - EgyptianFractions uses Mathlib's Chebyshev file.
   - An elementary bound suffices even for the sharp 32/log 2, since log P(ℓ) ≤ ℓ log p_ℓ = ℓ(log ℓ + O(log log ℓ)).
6. **Lemma 6.1.** The Lean `marked_cleanup_exact_length` is stronger and slightly different.
   - It keeps the exact length, rather than the paper's "at most t". It does this by taking a lex-minimal tuple and using a length-preserving duplicate replacement 2/m = 1/u + 1/v with u < m for all m ≥ 3, which preserves every odd divisor.
   - The paper instead lets the even replacement shorten the list.
   - Both serve §6 equally.
7. **Lemma 8.2.** Same conclusion (8.1) and (8.2) with h ≤ 16, by a different proof (see L3). The Lean multiplier is P(Y)^4 with 8 log m/log 2 primes, not P(Y)^2⌊L⌋! with 16 log m/log 2 primes. log K has the same leading constant 32/log 2.
8. **Bounds identical to the paper.**
   - `n i ≤ k^(2^i)` (0-based) is the paper's n_i ≤ k^{2^{i−1}}.
   - `F k ≤ k^(2^k−1)` is the paper's F(k) ≤ k^{2^k−1}.
   - `v k ≤ 1 + k^(2^(k−1))` is the paper's upper bound in Cor 1.3. The paper itself notes this is "convenient rather than best known"; Tang's forum remark gives v(k) ≤ s_k, the Sylvester number.
9. **Cor 1.3's lower bound** e^{e^{k/600}} is the same as the paper's, and the slope statement matches. `docs/025.md` mentions only the liminf. The comparator also has limsup ≤ log 2.

## 4. Formal Conjectures

### 4a. FC_304

FC's definitions:
- `unitFractionExpressible a b = {k | ∃ s : Finset ℕ, s.card = k ∧ (∀ n ∈ s, n > 1) ∧ (a/b : ℚ) = ∑ n ∈ s, (n:ℚ)⁻¹}`
- `smallestCollection a b = sInf (unitFractionExpressible a b)`
- `smallestCollectionTo b = sSup {smallestCollection a b | a ∈ Finset.Ico 1 b}`
- `Erdos304.upper_bound : (fun b : ℕ => (smallestCollectionTo b : ℝ)) =O[atTop] (fun b => log (log b))`

FC already tags this with `formal_proof … ShortEgyptian/Main.lean#L33` at commit `adc7f124`. That commit exists in the local repo, and `git diff adc7f124 HEAD` is empty on both developments and both comparator files. But FC's statement is not OpenAI's, and the bridge is not in FC. It needs the following:

- **(B1) Representation.** For all a b, `unitFractionExpressible a b = {k | ∃ ns, IsExpansion a b ns ∧ ns.length = k}`.
  - Forward (⊆): take `ns := s.sort (· ≤ ·)`. Use `Finset.sort_sorted_lt` (Pairwise `<`), `Finset.length_sort` (length = card) and `Finset.mem_sort` (`n > 1` ↔ `2 ≤ n` by omega).
  - For the sum, `(s.sort _).map f` sums to `∑ n ∈ s, f n`, either via `Finset.sort_toFinset` + `List.sum_toFinset` (nodup) or via `List.Perm.sum_eq` with `Finset.sort_perm_toList`.
  - Casting: `1/(n:ℚ) = (n:ℚ)⁻¹` is `one_div`. FC's `(a / b : ℚ)` elaborates leaf-wise to `(↑a / ↑b : ℚ)`, the same as `(a:ℚ)/(b:ℚ)`; FC's `smallestCollection_two_fifteen` confirms this.
  - Backward (⊇): from `Pairwise (·<·)` get `Nodup` (`List.Sorted.nodup`). Take `s := ns.toFinset`, with `List.toFinset_card_of_nodup`, `List.mem_toFinset` and `List.sum_toFinset`.
- **(B2)** `smallestCollection a b = minLength a b` for all a b, by `congrArg sInf (B1)`. No hypothesis is needed, since both sides are junk-equal when the set is empty.
- **(B3)** `smallestCollectionTo b = maxMinLength b`.
  - The set-builder `{f a | a ∈ Finset.Ico 1 b}` is `f '' ↑(Finset.Ico 1 b)` (`Set.ext` + `Finset.mem_coe`).
  - In ℕ, for b ≥ 2 the Finset is nonempty, and `Finset.sup'_eq_csSup_image` plus `Finset.sup'_eq_sup` turns the sSup of the image into `Finset.sup`.
  - For b ≤ 1 both sides are 0 (`csSup_empty`/`Nat.sSup_empty`, `Finset.sup_empty`). Only eventual b matters anyway.
- **(B4) Asymptotics.** From `OAI.ShortEgyptian.main.2` obtain c₂, b₀. Apply `Asymptotics.IsBigO.of_bound c₂`, using `eventually_atTop` with threshold max b₀ 3. There, ‖(N(b):ℝ)‖ = N(b) by `Nat.cast_nonneg`, and ‖log log b‖ = log log b because log b ≥ log 3 > 1. The ℕ-to-ℝ cast is pushed through (B3) with `congrArg`.
- **By-products.**
  - `erdos_304.variants.lower_1950` follows by the same B1–B3 plus `IsBigO.of_bound (1/c₁)`.
  - `upper_1950` and `upper_1985` follow by transitivity: log log b = O(log b/log log b) and O(√log b).
- Formally OpenAI's statement is strictly stronger. FC's `upper_bound` alone is junk-satisfiable if some `unitFractionExpressible` were empty, since FC's own comment says nonemptiness is "not proved for now". OpenAI's conjunct 1 supplies that nonemptiness.

Estimated size: about 60–100 lines.

### 4b. FC_148

`erdos_148 : (fun k ↦ (F k : ℝ)) =Θ[atTop] erdos_148.answer`, where `answer` is a sorried definition and the theorem is tagged `research open, question value`. The OpenAI result does not settle it. log log F(k) ≍ k leaves F(k) undetermined up to bounded factors, and even up to factors exp(o(log F)). (Also, with `answer := F` the Θ statement is trivially true; the "question value" format depends on a human judging the answer's form.)

Honest records in FC language:

```lean
/-- [OAI26a, Corollary 1.2]: $\log\log F(k) \asymp k$. This determines the double-logarithmic
order of `F k`; it does not determine `erdos_148.answer`. -/
@[category research solved, AMS 11, formal_proof using lean4 at
  "https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/NumberTheory/EgyptianFractions/Main.lean"]
theorem erdos_148.variants.loglog_order :
    (fun k : ℕ => Real.log (Real.log (F k : ℝ))) =Θ[atTop] (fun k : ℕ => (k : ℝ)) := by
  sorry

/-- Every denominator of a `k`-term representation is at most `k ^ 2 ^ (k - 1)`
(and `n_i ≤ k ^ 2 ^ (i - 1)` in increasing order); hence the solution set is finite and
`F k ≤ k ^ (2 ^ k - 1)`. -/
@[category research solved, AMS 11]
theorem erdos_148.variants.finite_and_box (k : ℕ) :
    {S : Finset ℕ | S.card = k ∧ 0 ∉ S ∧ ∑ n ∈ S, (1 : ℚ) / n = 1}.Finite ∧
      F k ≤ k ^ (2 ^ k - 1) := by
  sorry
```

Notes on these statements:
- The Θ lower half is junk-proof: F = 0 makes log log F = 0. The upper half is junk-vulnerable without finiteness, hence the second theorem.
- The bridge is `F_FC k = F_OAI k`. Use `Set.ncard_congr` (or `Set.ncard_image_of_injective`) with n ↦ `Finset.univ.image n` and inverse S ↦ `S.orderEmbOfFin h`. The ingredients are `Finset.card_image_of_injective` (StrictMono ⇒ injective), `Finset.image_orderEmbOfFin_univ` / `Finset.orderEmbOfFin_unique`, `Finset.sum_image`, and 0 ∉ S ↔ ∀ i, 1 ≤ n i.
- FC's `erdos_148.variants.lower_bound` (Konyagin's form) follows from the OpenAI lower bound with o := 0, since (log 2 log 3/3)·k/log k ≤ ck eventually and exp∘exp is monotone.
- FC's `upper_bound` (Elsholtz–Planitzer, c₀^{(1/5+o(1))2^k}) is not implied; OpenAI's upper bound k^{2^k−1} is weaker.

### 4c. Draft FC file for #293 (FC has none; `FC_293.lean` is a 404)

```lean
module

public import FormalConjecturesUtil

/-!
# Erdős Problem 293

*References:*
- [erdosproblems.com/293](https://www.erdosproblems.com/293)
- [ErGr80] Erdős, P. and Graham, R., *Old and new problems and results in combinatorial number
  theory*. Monographies de L'Enseignement Mathématique (1980), p. 35.
- [vDTa25b] van Doorn, W. and Tang, Q., arXiv:2512.22083.
- [OAI26a] OpenAI, *Short Egyptian fractions*. OpenAI Math Release preprint (2026).
-/

@[expose] public section

open Filter Real Asymptotics

namespace Erdos293

/-- `D k` is the set of integers `m ≥ 2` occurring as some `n_i` in a solution of
$1 = \frac{1}{n_1} + \cdots + \frac{1}{n_k}$ with $1 \le n_1 < \cdots < n_k$, a solution being
encoded as a `k`-element set of positive integers. -/
def D (k : ℕ) : Set ℕ :=
  {m | 2 ≤ m ∧ ∃ S : Finset ℕ, S.card = k ∧ 0 ∉ S ∧ m ∈ S ∧ ∑ n ∈ S, (1 : ℚ) / n = 1}

/-- `v k` is the least integer `m ≥ 2` not in `D k`. The integer `1` is excluded (it occurs only
for `k = 1`); this is the reading adopted on erdosproblems.com, where the original source is
noted to be ambiguous. Since `D k` is finite (`D_finite`), `sInf` is a genuine minimum. -/
noncomputable def v (k : ℕ) : ℕ := sInf ({m | 2 ≤ m} \ D k)

@[category API, AMS 11]
theorem D_finite (k : ℕ) : (D k).Finite := by
  sorry

@[category API, AMS 11]
theorem v_spec (k : ℕ) :
    2 ≤ v k ∧ v k ∉ D k ∧ ∀ m : ℕ, 2 ≤ m → m < v k → m ∈ D k := by
  sorry

/-- $v(1), \ldots, v(6) = 2, 2, 4, 11, 17, 103$ (forum values $v(7)=733$, $v(8)=27539$,
$v(9)=13856993$ are computer results). -/
@[category test, AMS 11]
theorem v_first_values :
    v 1 = 2 ∧ v 2 = 2 ∧ v 3 = 4 ∧ v 4 = 11 ∧ v 5 = 17 ∧ v 6 = 103 := by
  sorry

/--
Let $k\geq 1$ and let $v(k)$ be the minimal integer which does not appear as some $n_i$ in a
solution to $1=\frac{1}{n_1}+\cdots+\frac{1}{n_k}$ with $1\leq n_1<\cdots <n_k$.
Estimate the growth of $v(k)$.

$\log\log v(k) \asymp k$ [OAI26a, Corollary 1.3]: $v(k)$ grows doubly exponentially in $k$.
-/
@[category research solved, AMS 11, formal_proof using lean4 at
  "https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/NumberTheory/EgyptianFractions/Main.lean"]
theorem erdos_293 :
    (fun k : ℕ => log (log (v k : ℝ))) =Θ[atTop] (fun k : ℕ => (k : ℝ)) := by
  sorry

/-- Explicit slopes [OAI26a, Corollary 1.3], stated without `liminf`/`limsup` so that no
boundedness side condition is needed. -/
@[category research solved, AMS 11]
theorem erdos_293.variants.slopes :
    (∀ c : ℝ, c < log 2 / 257 → ∀ᶠ k : ℕ in atTop, exp (exp (c * k)) ≤ (v k : ℝ)) ∧
    (∀ C : ℝ, log 2 < C → ∀ᶠ k : ℕ in atTop, (v k : ℝ) ≤ exp (exp (C * k))) := by
  sorry

/-- van Doorn and Tang [vDTa25b, Theorem 1.1]. -/
@[category research solved, AMS 11]
theorem erdos_293.variants.van_doorn_tang :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ k : ℕ in atTop, exp (c * (k : ℝ) ^ 2) ≤ (v k : ℝ) := by
  sorry

/-- Elementary upper bound (every denominator is at most `k ^ 2 ^ (k - 1)`). -/
@[category research solved, AMS 11]
theorem erdos_293.variants.elementary_upper (k : ℕ) (hk : 1 ≤ k) :
    v k ≤ 1 + k ^ 2 ^ (k - 1) := by
  sorry

end Erdos293
```

Notes on the draft:
- **Junk audit.** The hard (lower) directions of `erdos_293` and `slopes` fail on junk v = 0 or v = 1, so they are junk-proof. The upper directions are true anyway, and `D_finite`/`v_spec` record that `sInf` is honest.
- **Bridge from OAI.** `D_FC k = OAI.Problem337.D k` via the same Finset ↔ StrictMono bijection as 4b, using `Finset.mem_image` for m ∈ S ↔ ∃ i, n i = m. Hence `v` agrees.
  - `erdos_293` follows from conjunct 1 of `prescribed_denominator_corollary` (k/600 ≤ log log v) together with `missing_denominator_semantics`' bound (log log v ≤ k log 2 + log log k ≤ 2k).
  - `slopes` is conjunct 3 together with the same upper bound.
- **Verified small values.** `v_first_values` is exactly what `enum.py` computed (§1c).

## 5. Verdict

No objection to the paper's statements as formalized. The Lean statements say what Theorem 1.1, Corollary 1.2, Corollary 1.3 and Proposition 8.1 say, and what #304, #148 and #293 ask, with no vacuous conjuncts. Both upper-bound developments are complete, independent, unconditional and sorry/axiom-free at source level. Two pending items:
- The kernel replay (coordinator) must confirm compilation and axioms.
- Caveat L3: the paper's own §8.1 proof (three primes) is not what the Lean checks; Prop 8.1 is certified by a different proof.

VERDICT: HOLDS AS READ
