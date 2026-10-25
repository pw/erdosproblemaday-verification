# Seat C: Itabe #160 Lean source audit and statement match (hostile referee)

Repo: `/tmp/erdos160/itabe/repo` at tag `v0.2.1-review-candidate`, commit `fd426c9`. Lean v4.30.0. Mathlib is pinned to `c5ea00351c28e24afc9f0f84379aa41082b1188f`. `git ls-remote` shows that this commit is the official `leanprover-community/mathlib4` tag `v4.30.0`.
Scope: I read the sources and checked the statements only. I did not run lake or lean. The kernel replay belongs to the driver in `/tmp/erdos160/itabe/lean-build/`; its status is noted only for context at the end.
Date: 2026-10-13.

## VERDICT: STATEMENT MATCHES

Both endpoints are stated purely in terms of `siteH`, real `rpow` and `Filter.atTop` on ℕ. Their only hypotheses are `(ε : ℝ) (hε : 0 < ε)`. `siteH` is the erdosproblems.com/160 quantity h(N). It is pointwise equal to Formal Conjectures' `erdos_160.h`: the two definitions are textually identical except for the AP predicate, and the two AP predicates are logically equivalent on `Set ℕ` (§B).

I found:
- no FATAL finding;
- no GAP that touches the claimed theorem;
- no undischarged hypothesis or assumed instance;
- no `sorry`, `axiom`, `native_decide`, `set_option`, notation, macros or custom instances, apart from one instance built from a proof.

The findings below are expository. One of them (E1) is the only link between the Lean theorem and the page's h(N) that the kernel does not check, namely the equivalence of the two AP predicates. I checked it by hand (§B). It is a one-screen lemma that the author could add.

---

## A. Findings

**E1 (EXPOSITION — the one link the kernel does not check).** The repo never states or proves `siteH n = Erdos160.erdos_160.h n`, because it does not depend on formal-conjectures. The identification therefore rests on the hand argument in §B.

My verdict: the two definitions agree for every `n`, including n = 0..3, and no value of h(N) changes. Recommendation: the author could add a bridge lemma. It needs `IsFourTermAP s ↔ s.IsAPOfLength 4` (≈20 lines, using the repo's own `isFourTermAP_ncard`).

**E2 (EXPOSITION).** The two texts use different conventions.
- Manuscript Def. 1.1 colours `[N]_0 = {0..N-1}` with "the least *positive* integer q".
- Lean `siteH` colours `Finset.Icc 1 N` and takes `sInf` over all of ℕ.

The repo bridges these only in the direction the result needs. `directSourceGoodPalette_of_bounded_notAtMostTwo` (DirectSiteHBridge.lean) maps x ∈ [1,N] to `colour (x.val - 1)`, re-indexed through `Fintype.equivFin C`.

I checked the translation. An IsFourTermAP set `{a, a+d, a+2d, a+3d} ⊆ [1,N]` with d > 0 has a ≥ 1. It maps to `n_i = a + i·d − 1 < N` with `n1 ≠ n0`, i.e. a `BoundedIntFourAP4 N` tuple. `hcolour` gives `¬AtMostTwo4`. This is lifted to `3 ≤ ncard` of the image through `directAtMostTwo4_of_fourSet_ncard_le` together with `ncard_le_ncard`. The image lives in `Fin (card C)`, so `ncard` is honest (finite).

For N ≥ 1 the two definitions coincide: `Fin 0` admits no map from a nonempty domain, so 0 is not good.

**E3 (EXPOSITION; checked for vacuity).** `siteH 0 = 0` is a junk value at the empty horizon and is irrelevant to asymptotics.

For every N the `sInf` is a genuine minimum. `sourceGoodPalette_succ N` shows the identity colouring into `Fin (N+1)` is good, and `Nat.sInf_mem` then applies. The upper-bound step `siteH_le_of_sourceGoodPalette` is `Nat.sInf_le` on a member, so it does not depend on nonemptiness.

The real risk for an *upper* bound is a goodness predicate that is too weak (a sub-family of APs), which would make the bound trivial. That risk is excluded:
- `IsFourTermAP` is the full family of nonconstant 4-APs (§B).
- The repo has a positive control: `three_le_siteH` (siteH N ≥ 3 for N ≥ 4).

**E4 (EXPOSITION).** The manuscript defines h_E(N) = max{k : **2 ≤ k** ≤ N ∧ …}. Lean's `sourceSurjectiveOriginalH` uses `sSup {k | k ≤ N ∧ …}` with no lower bound.
- This is harmless. k = 0 and k = 1 are vacuously or trivially "bad", and 2 is in the set for N ≥ 4, so the supremum is the same.
- The `k ≤ N` restriction is necessary and correct: no surjection exists for k > N, so without it the set would be unbounded and `sSup` would return junk.

**E5 (EXPOSITION).** The coefficient-one "eventually" endpoint has no explicit threshold in Lean. It absorbs C^{1/3} into N^δ via `tendsto_rpow_atTop`. The natural-power theorem does have an explicit threshold: `siteH_oneThirdPlusSubpower_unified_displayed`, with N > max{2^{(76k)^2}, 2^{(40k)^4}}. Effective in principle: N ≥ max(that, C^{1/(3δ)}). This matches the manuscript's (1.6) and (8.4).

**E6 (EXPOSITION).** All palette counts are *available-codomain* cardinalities (`Fintype.card` of the product type), not attained images.
- S_N = 24^L((L+1)P²+1)
- D_N = (log₂B+1)^L((L+1)B²+1)
- U_N = 9p

The manuscript says the same in (4.3), (5.7) and (7.10). This is conservative and the direction is correct, because siteH ≤ |codomain|.

**E7 (EXPOSITION).** In the text extraction, (8.5) reads "227 < 320". That is a pdftotext artifact for 22^7 < 3^20 (2,494,357,888 < 3,486,784,401). Lean proves `(22:ℝ)^7 < 3^20 ⇒ 7/20 < log 3 / log 22` (`sevenTwentieth_lt_logThree_div_logTwentyTwo_unified`).

**I1 (info: hygiene scan, all clean).**
- No `sorry`, `admit`, `axiom`, `opaque`, `unsafe`, `partial`, `implemented_by`, `extern`, `native_decide`, `decide`, `set_option` (including `maxHeartbeats`), `macro`, `syntax`, `notation` or `attribute` in any of the 20 E160 files.
- Imports are only Mathlib (`import Mathlib`, `Mathlib.NumberTheory.Bertrand`, `Mathlib.FieldTheory.Finite.GaloisField`, two matrix/polynomial modules).
- `lakefile.toml` sets only linter and pp options plus `maxSynthPendingDepth = 3` (an elaboration option, not a soundness knob).

**I2 (info: choice is used only to construct).** `Classical.choose` appears in two places:
1. `cubicPrime N := Classical.choose (exists_cubicPrime N)`.
2. `Module.finBasisOfFinrankEq` for the F_p-basis of `GaloisField p 3` (`galoisFieldThreeVectorEquiv`).

Both pick witnesses for a colouring that only needs to exist. This matches the manuscript's "after finite choices of a prime and a field basis". The single global instance is `noncomputable instance cubicPrimeFact (N) : Fact (cubicPrime N).Prime := ⟨cubicPrime_prime N⟩`. It is built from Bertrand's postulate, not assumed, and there is no inconsistent instance anywhere.

**I3 (info: constants match the manuscript, §6–§8).**
- `explicitUnifiedOneThirdThreshold k = max (2^(dtzABABSubpowerThreshold 8 11 0 (2k))^2) (2^((20·(2k))^4))`. For k ≥ 1, `dtzABABSubpowerThreshold 8 11 0 (2k) = max (max 0 1) (2·19·2k) = 76k`.
  - This gives max{2^{(76k)²}, 2^{(40k)⁴}}.
  - The equality is proved in `explicitUnifiedOneThirdThreshold_eq_displayed`.
  - It matches (1.3), (6.7) and (6.9). Both use strict `<` (the manuscript writes N > …).
- `cubicPaletteCubeConstant = 2_985_984 = 729·4096 = 9³·2¹²`. Its derivation matches (7.13)–(7.14):
  - `horizonCubicPalette_cube_lt`: (9p)³ = 729·p³ < 729·4096·N, from `cubicPrime_cube_lt_4096_mul`.
  - p ≤ 2y and y³ < 512N follow from `cubicScale_cube_lt_512_mul`, using 3·e ≤ q+8 with e = ⌊(q+2)/3⌋+2.
- Final combination:
  - S^{2k} < N and D^{2k} < N give (SD)^k < N (`pairProduct_pow_lt_of_two_mul_powers_lt`).
  - Hence H^{3k} ≤ (SD)^{3k}(9p)^{3k} < N³(CN)^k = C^k N^{k+3}.
  - This is identical to (8.3), and (k+3)/(3k) = 1/3 + 1/k.

**I4 (info: cubic factor hypotheses, §7).** `natCubicColour_abba_free (p) [Fact p.Prime] (hp : 3 < p) (a d) (hd : 0 < d) (hbound : a + 3*d < p^3)`. This matches §7: p > 3 prime, with three base-p digits on [0,p³). `a + 3d < p³` is exactly "all four terms lie in [0,p³)" for the increasing orientation, so the horizon is right.

At the call site (`horizonCubicColour_abba_free_of_lt`, CubicHorizon.lean):
- `[Fact]` comes from `cubicPrimeFact`.
- `3 < p` comes from `three_lt_cubicPrime`.
- `hbound` comes from `n3 < N ≤ cubicPrime N ^ 3` (`cubicPrime_cube_covers`).
- The decreasing orientation is handled by reversal.

The prime comes from `Nat.exists_prime_lt_and_le_two_mul (cubicScale N)`, Mathlib's Bertrand's postulate: y < p ≤ 2y with y = 2^e ≥ 4 > 3 (e ≥ 2), so N ≤ y³ < p³. Its digit extraction `Digits3.ofNat` uses an un-reduced top digit `n / (p*p)`, which is valid exactly when n < p³ (`valid_ofNat`). The cubic-line expansion of the norm is derived from `det(X·A + B)` with leading coefficient `det A = norm h`, and 6 ≠ 0 in ZMod p comes from p > 3.

**I5 (info: endpoint statements vs the README).** The README says "for every real ε > 0, eventually H(N) ≤ N^{1/3+ε}". This is literally `siteH_le_rpow_oneThird_add_epsilon_eventually`, with coefficient one and `∀ᶠ N : ℕ in atTop`. "H(N) = O_ε(N^{1/3+ε})" is literally `siteH_oneThirdPlusEpsilon_unified_isBigO` (IsBigO on ℕ with Real.norm; the existential constant is C^{1/3}). "N^{1/3+o(1)}" is the standard reading of the ε-family. I found no gap between the prose and the formal statements. The pp.all elaboration in the driver's `axioms.log` confirms there are no hidden binders or instances: `Real.instPow` (rpow), `Nat.cast`, `Filter.atTop` on `Nat.instPreorder`.

**I6 (info: source convention, item 3).** Erdős 1989 (excerpt, p.143): "Let h(n) be the largest integer for which if we decompose the integers 1, 2, ..., n into h(n) disjoint sets [then two of them have a union containing a 4-AP]".

`sourceSurjectiveOriginalH N = sSup {k | k ≤ N ∧ ∀ surjective c : Icc 1 N → Fin k, ∃ 4-AP whose image has ncard ≤ 2}`. This is the faithful reading:
- surjective = nonempty parts;
- ≤ 2 colours = "two parts whose union contains it" (one-colour case: pair the part with any other part).

The literal two-*distinct*-parts form is proved equivalent for k ≥ 2 (`sourceEverySurjectivePartitionBadDistinctTwo_iff`). The labelled (possibly empty parts) reading is proved to give the same supremum (`sourceSurjectiveOriginalH_eq_sourceOriginalH`). "Largest h such that partitions into h parts are bad" agrees with "for every m ≤ h" because the bad set is proved to be the initial segment {k < siteH N}.

The proof of H(N) = h_E(N)+1 for N ≥ 4 is sound: compression to the used labels, refinement by splitting a fibre, and siteH ≥ 3 via {1,2,3,4}. This bridge is extra; the headline claim concerns the page quantity directly.

---

## B. Definitional relationship: `siteH` vs `erdos_160.h` vs the page's h(N)

**Problem page.** I read the Wayback copy, accessed 2026-10-08, because erdosproblems.com itself is behind Cloudflare: "Let h(N) be the smallest k such that {1,…,N} can be coloured with k colours so that every four-term arithmetic progression must contain at least three distinct colours." Constant progressions must be excluded, otherwise h would be undefined.

**Formal Conjectures** (`FormalConjectures/ErdosProblems/160.lean` and `FormalConjecturesForMathlib/Combinatorics/AP/Basic.lean`, fetched today):
```
Set.IsAPOfLengthWith s l a d := ENat.card s = l ∧ s = {a + n • d | (n : ℕ) (_ : n < l)}
Set.IsAPOfLength s l := ∃ a d, s.IsAPOfLengthWith l a d
erdos_160.h n := sInf {k | ∃ colouring : Finset.Icc 1 n → Fin k, ∀ progression : Set ℕ,
    (progression ⊆ Finset.Icc 1 n ∧ progression.IsAPOfLength 4) →
    3 ≤ (colouring '' {k | (k : ℕ) ∈ progression}).ncard}
```

**Itabe** (`Problem.lean`):
```
IsFourTermAP s := ∃ a d : ℕ, 0 < d ∧ s = {x | ∃ i : ℕ, i < 4 ∧ x = a + i * d}
siteH n := sInf {k | ∃ colouring : Finset.Icc 1 n → Fin k, ∀ progression : Set ℕ,
    (progression ⊆ Finset.Icc 1 n ∧ IsFourTermAP progression) →
    3 ≤ (colouring '' {x | (x : ℕ) ∈ progression}).ncard}
```

The two `sInf` bodies are token-for-token identical, up to bound-variable names, except for the AP predicate.

**Claim:** for every `s : Set ℕ`, `IsFourTermAP s ↔ s.IsAPOfLength 4`.

**(→)** Take the same a and d. On ℕ, `n • d = n * d` (`smul_eq_mul`), and `(n : ℕ∞) < 4 ↔ n < 4`, so the sets coincide. Since d > 0, the four values a, a+d, a+2d, a+3d are distinct, so `ENat.card s = 4`. The repo's `isFourTermAP_ncard` proves the `ncard` version.

**(←)** From `s = {a + n•d | n < 4}` and `ENat.card s = 4`:
- If d = 0, then s = {a} and `ENat.card s = 1 ≠ 4`, so d > 0.
- Then the same (a, d) witnesses `IsFourTermAP`.

**Answers to the specific questions:**
- **d = 0:** `IsAPOfLength 4` does *not* admit it. The `ENat.card s = 4` conjunct excludes singletons; this is exactly Itabe's `0 < d`.
- **Decreasing d:** d ranges over ℕ in both definitions, so there is no negative step syntactically. Both predicates describe *sets*, and the decreasing AP (a+3d, a+2d, a+d, a) is the same set, so nothing is lost on either side.
- **Effect on h(n):** none. The predicates are equivalent, so the defining sets are equal and `siteH n = erdos_160.h n` for **every** n ∈ ℕ, including the junk values: n = 0 gives 0 (empty domain, `Fin 0` colouring), and n = 1, 2, 3 give 1.
- **Status of the equality:** it holds propositionally (`funext` + set-ext + the iff above). It is not syntactic (different constants), and it is not proved in the repo (see E1).
- **Problem page:** both coincide with the page's h(N) for N ≥ 1, reading "four-term AP" as nonconstant. Nonconstancy is the only coherent reading, and the manuscript's abstract states it explicitly ("every nonconstant four-term arithmetic progression").
- **Erdős's 1989 h_E:** h_E(N) = H(N) − 1 for N ≥ 4. This is proved in Lean (`siteH_eq_sourceSurjectiveOriginalH_add_one`), so asymptotics transfer unchanged.

**Consequence for FC.** Carried over through this equivalence, Itabe's endpoint implies FC's `erdos_160.known_upper` (n^{2/3}), since 1/3 + ε ≤ 2/3. It would also witness the `answer(sorry)` slot of FC's `erdos_160.better_upper`, e.g. with upper_bound = n^{1/2}. Hunter's recorded bound already fills that slot; FC's docstrings lag the page (2/3 upper, 1/12 lower, versus the page's log3/log22 and 1/9).

---

## C. Hypotheses carried by the two endpoints (exact)

- `siteH_le_rpow_oneThird_add_epsilon_eventually (ε : ℝ) (hε : 0 < ε) : ∀ᶠ N : ℕ in atTop, (siteH N : ℝ) ≤ (N : ℝ) ^ ((1 : ℝ) / 3 + ε)`
- `siteH_oneThirdPlusEpsilon_unified_isBigO (ε : ℝ) (hε : 0 < ε) : (fun n ↦ (siteH n : ℝ)) =O[atTop] (fun n ↦ (n : ℝ) ^ ((1 : ℝ) / 3 + ε))`

Neither endpoint has any other explicit, implicit or instance argument. Driver pp.all: both depend on axioms `[propext, Classical.choice, Quot.sound]` only.

## D. Dependency chain with every lemma's hypotheses (all discharged internally)

| Lemma | Hypotheses | Discharged by |
|---|---|---|
| `siteH_oneThirdPlusInv_unified_real_bound N k` | `0<k`, `explicitUnifiedOneThirdThreshold k < N` | endpoints choose k with 1/k < ε (`Real.exists_nat_pos_inv_lt`); threshold via `eventually_gt_atTop` |
| `siteH_oneThirdPlusSubpower_unified_explicit_rational` / `_eventually` | same | — |
| `siteH_oneThirdPlusSubpower_unified_explicit N k` | `0<k`, `2^(T(2k))^2 < N`, `2^((40k))^4 < N` | `le_max_left/right` of the threshold |
| `siteH_oneThirdPlusSubpower_of_unified_factors` | `[Fintype C]`, `hgood`, `card C^(2k) < N`, `card D^(2k) < N`, `1 < N` | `explicitUnifiedOneThirdColour_notAtMostTwo N`; `horizonNoThreeMod24Palette_card_pow_lt`; `horizonDyadicSquarePalette_card_pow_lt`; threshold ≥ 1 |
| `explicitUnifiedOneThirdColour_notAtMostTwo N` | none | 4 horizon lemmas below + `properABBAFilter_product_not_atMostTwo` + `atMostTwo_noThree_aabb_abab_properABBA` |
| `horizonNoThreeMod24Colour_isNoThreeEqualColouring N` | none | `explicitDTZ_horizon_cover N` (N ≤ (24·2^m+1)^m) |
| `horizonABABMod24Colour_isABABFreeColouring N` | none | same cover; `horizonNoThree_eq_horizonABAB` (rfl) shares the label |
| `horizonDyadicSquareColour_isAABBFreeColouring N` | none | `aabb_horizon_cover N` (N ≤ 2^{m²} = B^{L+1}) |
| `horizonCubicColour_abba_free N` | none | `natCubicColour_abba_free` with instance `cubicPrimeFact`, `three_lt_cubicPrime`, `cubicPrime_cube_covers` |
| `horizonCubicPalette_cube_lt N` | `1 < N` | threshold |
| `directSiteH_le_card_of_bounded_notAtMostTwo N colour` | `[Fintype C]`, `hcolour` on `BoundedIntFourAP4 N` | `hgood` |
| `natCubicColour_abba_free p` | `[Fact p.Prime]`, `3<p`, `0<d`, `a+3d<p^3` | see I4 |
| `explicitDTZPaletteBound_pow_lt`, `dtzABABPalette_card_pow_lt`, `horizonDyadicSquarePalette_card_pow_lt` | `0<k`, threshold | pure arithmetic |

`IntFourAP4` (signed equal differences) together with `n1 ≠ n0` is the correct nontrivial-AP predicate. The ordering covers both orientations. The pattern logic (`AtMostTwo4`, `NoThreeEqual4` with all four triples, `AABBFree4`, `ABABFree4`, `IsProperABBAFilter`) is defined as stated in manuscript §2.

## E. Independent decorrelated check (Python brute force; does not use the Lean code)

Script: `/tmp/erdos160/seats/c_itabe_check/brute.py`. Log: `brute.log`. It re-implements the manuscript's labels from the text, at small parameters. Every check is paired with a negative control.

1. **ν_p = (thirds shield, F_{p³} norm via a 3×3 multiplication-matrix determinant):** 0 ABBA patterns on [0,p³) for p = 5, 7, 11, 13. Palette used ≤ 9p.
   - Controls fire: norm without shield → 436; shield without norm → 245; shield × *quadratic* form → 49 / 648.
2. **λ (mod-24 carry labels + square norm, P = 24s+1):** THREE = 0 and ABAB = 0 on [0,P³) for s = 1, 2 (N = 15,625 and 117,649).
   - Controls fire: norm only → THREE 576 / ABAB 793; mod-2 label with P = 26 → THREE 16.
3. **μ (dyadic buckets + square norm):** AABB = 0 for (B,L) = (4,3), (8,3), (16,2).
   - Control fires: norm only → 1287.
4. **Composition (§2):** exhaustive over equality patterns, 15³ partition triples. 1521 admissible triples, 0 with ≤ 2 product classes.
   - Control fires: allowing ABAB in λ → 1 violation.

A first end-to-end product test on [0,15625) was **uninformative**: its drop-one-factor negative controls also returned 0, because the labels are near-injective at that scale. I replaced it with check 4 rather than report it as a pass. Small-parameter brute force cannot exercise the regime where the 1/3 exponent bites. That regime is covered only by the kernel.

## F. Kernel replay (context only; not run by this seat; read from the driver's logs at ~18:21Z)

The driver's first `lake build ErdosProblems -j2` failed instantly (Lake 5 has no `-j`). The audits in that pass ran on an unbuilt tree ("unknown module prefix"). In the retry, all four steps passed (`check_release.sh` rc = 0, then `build2`, `their_audit2`, `our_audit2` and `negcontrol2` all rc = 0):
- All 21 modules built ("Build completed successfully (8496 jobs)").
- `check_release.sh`: "All checks passed."
- `--trust=0 #print axioms` on all 9 author endpoints plus the driver's 5 probes: only `propext`, `Classical.choice`, `Quot.sound` (the threshold-equality lemma does not even use Choice).
- Negative control: a `sorry`'d theorem reports `sorryAx`, so the audit can see a hole.
- The `leanchecker --fresh` step had not yet run when this file was written.
