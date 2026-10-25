-- the comparator file verbatim (it carries `sorry`), then pp.all prints of the SAME names for a statement match
import Mathlib

namespace OAI

noncomputable section

namespace Problem310

def dyadicPoint (n : ℕ) : ℝ :=
  (2 : ℝ)⁻¹ ^ n

theorem dyadic_affine_avoidance :
    ∀ η : ℝ, 0 < η → η < 1 → ∃ E : Set ℝ,
      E ⊆ Set.Icc (0 : ℝ) 1 ∧ IsCompact E ∧
      MeasureTheory.volume E > ENNReal.ofReal (1 - η) ∧
      ∀ x s : ℝ, s ≠ 0 → ∃ n : ℕ, 1 ≤ n ∧
        x + s * dyadicPoint n ∉ E := by
  sorry

end Problem310

end

end OAI
set_option pp.all true
#print axioms OAI.Problem310.dyadic_affine_avoidance
#check @OAI.Problem310.dyadic_affine_avoidance
#print OAI.Problem310.dyadicPoint
