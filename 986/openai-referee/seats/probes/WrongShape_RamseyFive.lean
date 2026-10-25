/- DRAFT probe — MUST FAIL TO ELABORATE at the EXPECTED ERROR line. Asserted statement genuinely FALSE
   (AKS: r(5,t) ≤ C t^4/(log t)^3 < t^4/(log t)^2 once log t > C; RightShape_RamseyFive.refute_exponent_two). -/
import Mathlib
import OAI.Combinatorics.RamseyFive.Main

namespace ProbeWrongShapeFive
open Filter

theorem wrongShape_exponent_two :
    ∀ᶠ k : ℕ in atTop,
      (k : ℝ) ^ 4 / (Real.log k) ^ 2 ≤ (OAI.SharpRamseyFive.ramsey 5 k : ℝ) := by
  obtain ⟨_C, _hC, hb⟩ := OAI.SharpRamseyFive.main.1
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  filter_upwards [eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  exact h1   -- EXPECTED ERROR: type mismatch (exponent 3 + 1 : ℝ vs 2 : ℕ)

end ProbeWrongShapeFive
