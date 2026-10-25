/- DRAFT probe — MUST FAIL TO ELABORATE, at the line marked EXPECTED ERROR (type mismatch / rewrite /
   exact failure). A parse error or unknown identifier ANYWHERE makes the probe vacuous: fix and rerun.
   The asserted statement is genuinely FALSE: AKS (1980) gives r(s,t) ≤ C_s t^{s-1}/(log t)^{s-2}, which is
   < t^{s-1}/(log t)^{s-3} as soon as log t > C_s. (RightShape_SharpLog.refute_s_minus_three proves its
   negation from `main`.) -/
import Mathlib
import OAI.Combinatorics.SharpRamsey.Main

namespace ProbeWrongShapeSharpLog
open Filter

theorem wrongShape_s_minus_three (s : ℕ) (hs : 6 ≤ s) :
    ∀ᶠ k : ℕ in atTop,
      (k : ℝ) ^ (s - 1) / (Real.log k) ^ (s - 3) ≤ (OAI.SharpLogRamsey.ramsey s k : ℝ) := by
  obtain ⟨_C, _hC, hb⟩ := (OAI.SharpLogRamsey.main s hs).1
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  filter_upwards [eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  exact h1   -- EXPECTED ERROR: type mismatch, `Real.log ↑k ^ (↑(s - 2) + 1)` (rpow) vs `Real.log ↑k ^ (s - 3)` (npow)

end ProbeWrongShapeSharpLog
