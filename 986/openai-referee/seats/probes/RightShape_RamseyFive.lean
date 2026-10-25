/- DRAFT probe — compile in the OAI repo after the closure is built. Expected: COMPILES. -/
import Mathlib
import OAI.Combinatorics.RamseyFive.Main

namespace ProbeRightShapeFive
open Filter

/-- Page shape (Erdős #986 form) for s = 5: c = 4. -/
theorem rightShape_986_five :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ k : ℕ in atTop,
      (k : ℝ) ^ 4 / (Real.log k) ^ c ≤ (OAI.SharpRamseyFive.ramsey 5 k : ℝ) := by
  obtain ⟨_C, _hC, hb⟩ := OAI.SharpRamseyFive.main.1
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  refine ⟨3 + 1, by norm_num, ?_⟩
  filter_upwards [eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  exact h1

/-- The false strengthening t^4/(log t)^2 ≤ r(5,t) is REFUTED by the theorem's own upper bound. -/
theorem refute_exponent_two :
    ¬ ∃ t₀ : ℕ, ∀ t : ℕ, t₀ ≤ t →
      (t : ℝ) ^ 4 / (Real.log t) ^ 2 ≤ (OAI.SharpRamseyFive.ramsey 5 t : ℝ) := by
  rintro ⟨t₀, ht₀⟩
  obtain ⟨C, _hC, hb⟩ := OAI.SharpRamseyFive.main.1
  obtain ⟨t₁, ht₁⟩ := hb 1 one_pos
  obtain ⟨t, htC, ht0, ht1, ht2⟩ :=
    (((Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_gt_atTop C).and
      ((eventually_ge_atTop t₀).and ((eventually_ge_atTop t₁).and (eventually_ge_atTop 2)))).exists
  have htC' : C < Real.log (t : ℝ) := htC
  have hlow := ht₀ t ht0
  have hup := (ht₁ t ht1).2
  have htpos : (0 : ℝ) < t := by exact_mod_cast (show 0 < t by omega)
  have hlog : 0 < Real.log (t : ℝ) := Real.log_pos (by exact_mod_cast (show 1 < t by omega))
  have key := hlow.trans hup
  have hsplit : Real.log (t : ℝ) ^ 3 = Real.log (t : ℝ) ^ 2 * Real.log (t : ℝ) := by ring
  rw [hsplit] at key
  have hP : 0 < (t : ℝ) ^ 4 := pow_pos htpos _
  have hL : 0 < Real.log (t : ℝ) ^ 2 := pow_pos hlog _
  rw [div_le_div_iff₀ hL (mul_pos hL hlog)] at key
  have hPL : 0 < (t : ℝ) ^ 4 * Real.log (t : ℝ) ^ 2 := mul_pos hP hL
  nlinarith [mul_lt_mul_of_pos_left htC' hPL]

#print axioms rightShape_986_five
#print axioms refute_exponent_two

end ProbeRightShapeFive
