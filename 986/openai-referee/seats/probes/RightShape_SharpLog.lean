/- DRAFT probe — compile in the OAI repo after the closure is built. Expected: COMPILES. -/
import Mathlib
import OAI.Combinatorics.SharpRamsey.Main

namespace ProbeRightShapeSharpLog
open Filter

/-- Page shape (Erdős #986 form) from the main theorem, s ≥ 6: c = s - 1. -/
theorem rightShape_986 (s : ℕ) (hs : 6 ≤ s) :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ k : ℕ in atTop,
      (k : ℝ) ^ (s - 1) / (Real.log k) ^ c ≤ (OAI.SharpLogRamsey.ramsey s k : ℝ) := by
  obtain ⟨_C, _hC, hb⟩ := (OAI.SharpLogRamsey.main s hs).1
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  refine ⟨((s - 2 : ℕ) : ℝ) + 1, by positivity, ?_⟩
  filter_upwards [eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  exact h1

/-- The false strengthening (log-exponent s-3 in the lower bound) is REFUTED by the theorem's own
upper bound. -/
theorem refute_s_minus_three (s : ℕ) (hs : 6 ≤ s) :
    ¬ ∃ t₀ : ℕ, ∀ t : ℕ, t₀ ≤ t →
      (t : ℝ) ^ (s - 1) / (Real.log t) ^ (s - 3) ≤ (OAI.SharpLogRamsey.ramsey s t : ℝ) := by
  rintro ⟨t₀, ht₀⟩
  obtain ⟨C, _hC, hb⟩ := (OAI.SharpLogRamsey.main s hs).1
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
  have hsplit : Real.log (t : ℝ) ^ (s - 2) = Real.log (t : ℝ) ^ (s - 3) * Real.log (t : ℝ) := by
    rw [← pow_succ]; congr 1; omega
  rw [hsplit] at key
  have hP : 0 < (t : ℝ) ^ (s - 1) := pow_pos htpos _
  have hL : 0 < Real.log (t : ℝ) ^ (s - 3) := pow_pos hlog _
  rw [div_le_div_iff₀ hL (mul_pos hL hlog)] at key
  have hPL : 0 < (t : ℝ) ^ (s - 1) * Real.log (t : ℝ) ^ (s - 3) := mul_pos hP hL
  nlinarith [mul_lt_mul_of_pos_left htC' hPL]

#print axioms rightShape_986
#print axioms refute_s_minus_three

end ProbeRightShapeSharpLog
