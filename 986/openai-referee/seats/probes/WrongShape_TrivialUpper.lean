/- DRAFT probe — MUST FAIL TO ELABORATE at the EXPECTED ERROR line. Asserted statement genuinely FALSE:
   Erdős–Szekeres gives r(s,t) ≤ C(s+t-2, s-1) ≤ t^{s-1} < t^s (Lean: `Foundation.ramsey_le_pow`).
   Guards against an encoding in which `ramsey` could be junk-large (it cannot: sInf over ℕ of a
   nonempty set). Attempt: push the main lower bound through `linarith` with no upper information. -/
import Mathlib
import OAI.Combinatorics.SharpRamsey.Main

namespace ProbeWrongShapeTrivial
open Filter

theorem wrongShape_power_s (s : ℕ) (hs : 6 ≤ s) :
    ∀ᶠ k : ℕ in atTop, (k : ℝ) ^ s ≤ (OAI.SharpLogRamsey.ramsey s k : ℝ) := by
  obtain ⟨_C, _hC, hb⟩ := (OAI.SharpLogRamsey.main s hs).1
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  filter_upwards [eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  linarith   -- EXPECTED ERROR: linarith failed

end ProbeWrongShapeTrivial
