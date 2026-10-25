-- MUTANT (must FAIL to compile): FC def with n > 0 (allows denominator 1)
import Mathlib
import OAI.NumberTheory.ShortEgyptian.Main

/-!
# Bridge: OpenAI's `OAI.ShortEgyptian.main` ⟹ Formal Conjectures' `Erdos304.upper_bound`

The definitions `unitFractionExpressible`, `smallestCollection`, `smallestCollectionTo` and the statements of
`upper_bound` and `erdos_304.variants.lower_1950` below are verbatim copies of
`FormalConjectures/ErdosProblems/304.lean` at google-deepmind/formal-conjectures@2a315101 (21 Oct 2026),
with the FC attributes (`@[category …]`, `formal_proof …`) and docstrings removed (`verbatim_check.py`
asserts the copies, whitespace-normalised). The proofs are ours (erdos cron seat, 2026-10-21); the
mathematics is OpenAI's theorem, used as a black box.
-/

open Asymptotics Filter

namespace Erdos304

def unitFractionExpressible (a b : ℕ) : Set ℕ :=
  {k | ∃ s : Finset ℕ, s.card = k ∧ (∀ n ∈ s, n > 0) ∧ (a / b : ℚ) = ∑ n ∈ s, (n : ℚ)⁻¹}

noncomputable def smallestCollection (a b : ℕ) : ℕ := sInf (unitFractionExpressible a b)

noncomputable def smallestCollectionTo (b : ℕ) : ℕ :=
  sSup {smallestCollection a b | a ∈ Finset.Ico 1 b}

/-- OpenAI's sum `(ns.map (fun n => (1 : ℚ) / (n : ℚ))).sum` (which elaborates through the coercion
`List ℕ → List ℚ`) is FC's finset sum over the list's elements, for a duplicate-free list. -/
theorem oai_sum_eq (ns : List ℕ) (hnd : ns.Nodup) :
    (ns.map (fun n => (1 : ℚ) / (n : ℚ))).sum = ∑ n ∈ ns.toFinset, (n : ℚ)⁻¹ := by
  induction ns with
  | nil => simp
  | cons x xs ih =>
    rw [List.nodup_cons] at hnd
    rw [List.toFinset_cons, Finset.sum_insert (mt List.mem_toFinset.mp hnd.1), ← ih hnd.2]
    simp

/-- FC's finite sets of denominators are OpenAI's strictly increasing lists. -/
theorem unitFractionExpressible_eq_oai (a b : ℕ) :
    unitFractionExpressible a b =
      {k : ℕ | ∃ ns : List ℕ, OAI.ShortEgyptian.IsExpansion a b ns ∧ ns.length = k} := by
  ext k
  constructor
  · rintro ⟨s, rfl, hs, hsum⟩
    refine ⟨s.sort (· ≤ ·), ⟨?_, ?_, ?_⟩, Finset.length_sort _⟩
    · exact ((Finset.pairwise_sort s (· ≤ ·)).and (Finset.sort_nodup s (· ≤ ·))).imp
        (fun h => lt_of_le_of_ne h.1 h.2)
    · intro n hn
      have := hs n ((Finset.mem_sort _).mp hn)
      omega
    · rw [oai_sum_eq _ (Finset.sort_nodup s (· ≤ ·)), Finset.sort_toFinset]
      exact hsum.symm
  · rintro ⟨ns, ⟨hp, h2, hsum⟩, rfl⟩
    have hnd : ns.Nodup := hp.imp (fun h => ne_of_lt h)
    refine ⟨ns.toFinset, List.toFinset_card_of_nodup hnd, ?_, ?_⟩
    · intro n hn
      have := h2 n (List.mem_toFinset.mp hn)
      omega
    · rw [← oai_sum_eq ns hnd]
      exact hsum.symm

theorem smallestCollection_eq_minLength (a b : ℕ) :
    smallestCollection a b = OAI.ShortEgyptian.minLength a b := by
  unfold smallestCollection OAI.ShortEgyptian.minLength
  rw [unitFractionExpressible_eq_oai]

theorem smallestCollectionTo_eq_maxMinLength (b : ℕ) :
    smallestCollectionTo b = OAI.ShortEgyptian.maxMinLength b := by
  have hset : {smallestCollection a b | a ∈ Finset.Ico 1 b} =
      (fun a => OAI.ShortEgyptian.minLength a b) '' (↑(Finset.Ico 1 b) : Set ℕ) := by
    ext x
    simp [smallestCollection_eq_minLength]
  unfold smallestCollectionTo OAI.ShortEgyptian.maxMinLength
  rw [hset]
  rcases (Finset.Ico 1 b).eq_empty_or_nonempty with h | h
  · simp [h]
  · rw [← Finset.sup'_eq_sup h, Finset.sup'_eq_csSup_image]

/-- Erdős Problem 304, `Erdos304.upper_bound` of Formal Conjectures, verbatim: `N(b) ≪ log log b`. -/
theorem upper_bound :
    (fun b : ℕ => (smallestCollectionTo b : ℝ)) =O[atTop] (fun b : ℕ => Real.log (Real.log b)) := by
  obtain ⟨-, c₁, c₂, -, -, b₀, -, h⟩ := OAI.ShortEgyptian.main
  refine Asymptotics.IsBigO.of_bound c₂ ?_
  filter_upwards [eventually_ge_atTop (max b₀ 3)] with b hb
  have hbb : b₀ ≤ b := le_trans (le_max_left _ _) hb
  have h3 : (3 : ℝ) ≤ (b : ℝ) := by exact_mod_cast le_trans (le_max_right _ _) hb
  have hb0 : (0 : ℝ) < (b : ℝ) := by linarith
  have hlog1 : 1 ≤ Real.log (b : ℝ) := by
    rw [Real.le_log_iff_exp_le hb0]
    linarith [Real.exp_one_lt_d9]
  have hll : 0 ≤ Real.log (Real.log (b : ℝ)) := Real.log_nonneg hlog1
  rw [Real.norm_of_nonneg (by positivity), Real.norm_of_nonneg hll, smallestCollectionTo_eq_maxMinLength]
  exact (h b hbb).2

/-- Erdős 1950's lower bound, `Erdos304.erdos_304.variants.lower_1950` of Formal Conjectures, verbatim — also a
consequence of OpenAI's theorem (its lower half, `c₁ = 1/2`). -/
theorem erdos_304.variants.lower_1950 :
    (fun b : ℕ => Real.log (Real.log b)) =O[atTop]
      (fun b => (smallestCollectionTo b : ℝ)) := by
  obtain ⟨-, c₁, c₂, hc₁, -, b₀, -, h⟩ := OAI.ShortEgyptian.main
  refine Asymptotics.IsBigO.of_bound (1 / c₁) ?_
  filter_upwards [eventually_ge_atTop (max b₀ 3)] with b hb
  have hbb : b₀ ≤ b := le_trans (le_max_left _ _) hb
  have h3 : (3 : ℝ) ≤ (b : ℝ) := by exact_mod_cast le_trans (le_max_right _ _) hb
  have hb0 : (0 : ℝ) < (b : ℝ) := by linarith
  have hlog1 : 1 ≤ Real.log (b : ℝ) := by
    rw [Real.le_log_iff_exp_le hb0]
    linarith [Real.exp_one_lt_d9]
  have hll : 0 ≤ Real.log (Real.log (b : ℝ)) := Real.log_nonneg hlog1
  rw [Real.norm_of_nonneg hll, Real.norm_of_nonneg (by positivity), smallestCollectionTo_eq_maxMinLength]
  rw [div_mul_eq_mul_div, one_mul, le_div_iff₀ hc₁]
  linarith [(h b hbb).1]

end Erdos304
