import OAI.NumberTheory.PrimeGaps.RatioCorollary

/-!
# Bridge (erdosproblemaday.com, 2026-10-21): Formal Conjectures' `Erdos968.erdos_968` from OpenAI's
# `OAI.Problem344.large_gaps_and_ratio_density` (family 26, `OAI.NumberTheory.PrimeGaps.RatioCorollary` closure).

`Set.partialDensity`, `Set.lowerDensity`, `Erdos968.u` and the statement of `Erdos968.erdos_968` below are copied VERBATIM
(text and binder names) from google-deepmind/formal-conjectures @ 90d18f666eb98adec4eee4d12f1d37e30b4eb204:
`FormalConjecturesForMathlib/Data/Set/Density.lean` (namespace `Set`; FC's docstrings and the `@[inline]` attribute kept)
and `FormalConjectures/ErdosProblems/968.lean` (namespace `Erdos968`; the `@[category research solved, ...]` attribute is
FC-only and dropped). OpenAI's Mathlib d13f23b7 has no constants of these names, so the dot notation `.lowerDensity`
resolves exactly as in FC. This proves a verbatim copy of FC's statement in OpenAI's environment (Lean v4.34.1, Mathlib
d13f23b7), not FC's own constant.

FC's statement differs from OpenAI's comparator theorem in two ways, both handled here:
(1) indexing: FC's `u n = p_{n+1}/(n+1)` is 0-based via `Nat.nth Nat.Prime n`; OpenAI's `primeAt n = Nat.nth Nat.Prime (n-1)`
    is 1-based and its set is `{n | 1 ≤ n ∧ p_n/n < p_{n+1}/(n+1)}`. So `n ∈ FC's set ↔ n+1 ∈ OpenAI's set` (`mem_iff`),
    and FC's count below `b` equals OpenAI's `initialCount` up to `b` (`count_eq`).
(2) density: FC's `lowerDensity` is the liminf of `|S ∩ [0,b)| / b`; OpenAI's `lowerAsymptoticDensity` is the sSup of the
    `d` with `d ≤ count/N` eventually. Positivity of the latter gives a `d > 0` eventually below FC's partial densities.
-/

open Filter

open scoped Topology

namespace Set

/--
Given a set `S` and an element `b` in an order `β`, where all intervals bounded above are finite,
we define the partial density of `S` (relative to a set `A`) to be the proportion of elements in
`{x ∈ A | x < b}` that lie in `S ∩ A`.

This definition was inspired from https://github.com/b-mehta/unit-fractions
-/
@[inline]
noncomputable abbrev partialDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (A : Set β := Set.univ) (b : β) : ℝ :=
  ((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard

/--
Given a set `S` in an order `β`, where all intervals bounded above are finite, we define the lower
density of `S` (relative to a set `A`) to be the liminf of the partial densities of `S`
(relative to `A`) for `b → ∞`.
-/
noncomputable def lowerDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (A : Set β := Set.univ) : ℝ :=
  atTop.liminf fun (b : β) ↦ S.partialDensity A b

end Set

open Filter Real
open scoped BigOperators

namespace Erdos968

/--
`u n` is the normalized `n`th prime, defined as `pₙ / (n+1)` where `pₙ` is the `n`th prime
(with `0.nth Nat.Prime = 2`).

This corresponds to the classical sequence `(p₁/1, p₂/2, p₃/3, ...)` while using `Nat.nth Prime`'s
`0`-based indexing; in particular, the denominator is always positive.
-/
noncomputable def u (n : ℕ) : ℝ :=
  (n.nth Nat.Prime : ℝ) / (n + 1)

/-- The index shift between FC's 0-based set and OpenAI's 1-based `ratioIncreaseIndices`. -/
theorem mem_iff (n : ℕ) :
    n ∈ {n : ℕ | u n < u (n + 1)} ↔ n + 1 ∈ OAI.Problem344.ratioIncreaseIndices := by
  simp only [Set.mem_ofPred_eq, u, OAI.Problem344.ratioIncreaseIndices, OAI.Problem344.primeAt,
    Nat.add_sub_cancel, le_add_iff_nonneg_left, zero_le, true_and]
  push_cast
  rfl

/-- FC's count of the set below `b` is OpenAI's `initialCount` of its set up to `b`. -/
theorem count_eq (b : ℕ) :
    (({n : ℕ | u n < u (n + 1)} ∩ Set.univ) ∩ Set.Iio b).ncard =
      OAI.Problem344.initialCount OAI.Problem344.ratioIncreaseIndices b := by
  classical
  have hset : (({n : ℕ | u n < u (n + 1)} ∩ Set.univ) ∩ Set.Iio b) =
      (((Finset.range b).filter (fun n => n + 1 ∈ OAI.Problem344.ratioIncreaseIndices) : Finset ℕ) : Set ℕ) := by
    ext n
    simp only [Set.inter_univ, Set.mem_inter_iff, Set.mem_Iio, Finset.coe_filter, Finset.mem_range,
      Set.mem_ofPred_eq]
    have h := mem_iff n
    simp only [Set.mem_ofPred_eq] at h
    rw [h, and_comm]
  rw [hset, Set.ncard_coe_finset]
  unfold OAI.Problem344.initialCount
  apply Finset.card_nbij' (fun n => n + 1) (fun m => m - 1)
  · intro n hn
    simp only [Finset.coe_filter, Finset.mem_range, Set.mem_ofPred_eq] at hn
    simp only [Finset.coe_filter, Finset.mem_Icc, Set.mem_ofPred_eq]
    exact ⟨⟨by omega, by omega⟩, hn.2⟩
  · intro m hm
    simp only [Finset.coe_filter, Finset.mem_Icc, Set.mem_ofPred_eq] at hm
    simp only [Finset.coe_filter, Finset.mem_range, Set.mem_ofPred_eq]
    refine ⟨by omega, ?_⟩
    have : m - 1 + 1 = m := by omega
    rw [this]; exact hm.2
  · intro n _; simp
  · intro m hm
    simp only [Finset.coe_filter, Finset.mem_Icc, Set.mem_ofPred_eq] at hm
    simp only; omega

theorem univ_count (b : ℕ) : ((Set.univ : Set ℕ) ∩ Set.Iio b).ncard = b := by
  rw [Set.univ_inter, ← Finset.coe_range, Set.ncard_coe_finset, Finset.card_range]

/--
Does the set `{n | u n < u (n+1)}` have positive lower density?

Yes. This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked
Lean proof.
-/
theorem erdos_968 : 0 < {n : ℕ | u n < u (n + 1)}.lowerDensity := by
  have hpos := (OAI.Problem344.large_gaps_and_ratio_density).2
  unfold OAI.Problem344.lowerAsymptoticDensity at hpos
  have hne : ({d : ℝ | ∃ N0 : ℕ, ∀ N : ℕ, N0 ≤ N →
      d ≤ (OAI.Problem344.initialCount OAI.Problem344.ratioIncreaseIndices N : ℝ) / (N : ℝ)}).Nonempty :=
    ⟨0, 0, fun N _ => by positivity⟩
  obtain ⟨d, ⟨N0, hN0⟩, hd⟩ := exists_lt_of_lt_csSup hne hpos
  unfold Set.lowerDensity
  refine lt_of_lt_of_le hd (le_liminf_of_le ?_ ?_)
  · refine isCoboundedUnder_ge_of_le atTop (x := (1 : ℝ)) (fun b => ?_)
    apply div_le_one_of_le₀ _ (Nat.cast_nonneg _)
    exact_mod_cast Set.ncard_le_ncard (Set.inter_subset_inter_left _ Set.inter_subset_right)
  · filter_upwards [eventually_ge_atTop N0] with b hb
    rw [Set.partialDensity, count_eq, univ_count]
    exact hN0 b hb

end Erdos968
