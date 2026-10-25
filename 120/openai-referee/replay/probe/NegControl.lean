import OAI.MeasureTheory.DyadicAvoidance.Main
theorem oai_negcontrol_false : False := by sorry
#print axioms oai_negcontrol_false
-- wrong-shape control: the statement with 1 - η replaced by 1 - η/2 must NOT be what Main proves (type mismatch expected)
example : (∀ η : ℝ, 0 < η → η < 1 → ∃ E : Set ℝ, E ⊆ Set.Icc (0:ℝ) 1 ∧ IsCompact E ∧ MeasureTheory.volume E > ENNReal.ofReal (1 - η) ∧ ∀ x s : ℝ, s ≠ 0 → ∃ n : ℕ, 1 ≤ n ∧ x + s * OAI.Problem310.dyadicPoint n ∉ E) := OAI.Problem310.dyadic_affine_avoidance
