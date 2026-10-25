import OAI.Combinatorics.ProgressionColoring.Main
open Filter
open OAI.QuantitativeVanDerWaerden
-- must COMPILE: erdosproblems.com/138's question — the two-colour van der Waerden number has W(k)^(1/k) → ∞
example : Tendsto (fun k : ℕ => (W 2 k : ℝ) ^ (1 / (k : ℝ))) atTop atTop :=
  kthRoot_tendsto (by norm_num)
-- the explicit two-colour bound: W(k) > k^(k/100000) for all large k (Nat.log 2 2 = 1)
example : ∃ K : ℕ, ∀ k ≥ K, (k : ℝ) ^ ((1 / 100000 : ℝ) * k) < (W 2 k : ℝ) := by
  obtain ⟨K, hK⟩ := uniform_lower_bound
  refine ⟨K, fun k hk => ?_⟩
  have h := hK k hk 2 le_rfl
  have h2 : Nat.log 2 2 = 1 := by decide
  simpa [h2] using h
-- the bound is not vacuous: W 2 k is a positive natural (sInf of an empty set would be 0 and the inequality would fail)
example : ∃ K : ℕ, ∀ k ≥ K, 0 < W 2 k := by
  obtain ⟨K, hK⟩ := uniform_lower_bound
  refine ⟨K, fun k hk => ?_⟩
  have h := hK k hk 2 le_rfl
  have h0 : (0 : ℝ) ≤ (k : ℝ) ^ ((1 / 100000 : ℝ) * k * (Nat.log 2 2 : ℝ)) := by positivity
  exact_mod_cast lt_of_le_of_lt h0 h
-- Theorem 1.1 exactly as the comparator states it
example : ∃ K : ℕ, ∀ k ≥ K, ∀ r ≥ 2,
    (k : ℝ) ^ ((1 / 100000 : ℝ) * k * (Nat.log 2 r : ℝ)) < (W r k : ℝ) :=
  uniform_lower_bound
