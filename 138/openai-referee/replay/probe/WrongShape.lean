import OAI.Combinatorics.ProgressionColoring.Main
open OAI.QuantitativeVanDerWaerden
-- must FAIL (type mismatch): coefficient 1 instead of 1/100000 is NOT what uniform_lower_bound proves — control that RightShape can fail
example : ∃ K : ℕ, ∀ k ≥ K, ∀ r ≥ 2,
    (k : ℝ) ^ ((1 : ℝ) * k * (Nat.log 2 r : ℝ)) < (W r k : ℝ) :=
  uniform_lower_bound
