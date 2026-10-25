import OAI.MeasureTheory.DyadicAvoidance.Main
-- POSITIVE CONTROL for the control: the comparator's statement, re-typed by hand, is inhabited by Main's theorem. MUST compile.
example : (∀ η : ℝ, 0 < η → η < 1 → ∃ E : Set ℝ, E ⊆ Set.Icc (0:ℝ) 1 ∧ IsCompact E ∧ MeasureTheory.volume E > ENNReal.ofReal (1 - η) ∧ ∀ x s : ℝ, s ≠ 0 → ∃ n : ℕ, 1 ≤ n ∧ x + s * OAI.Problem310.dyadicPoint n ∉ E) := OAI.Problem310.dyadic_affine_avoidance
