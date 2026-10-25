-- The Comparator challenge module verbatim (statement with `sorry`), followed by pp.all prints of its definitions,
-- to diff against the same prints from the solution's Model (Erdos3Axioms.lean). Mathlib-only import.
import Mathlib

namespace OAI

namespace Erdos3

def HasAP (A : Set ℕ) (k : ℕ) : Prop :=
  ∃ a d : ℕ, 0 < d ∧ ∀ i < k, a + i * d ∈ A

end Erdos3

open scoped BigOperators

namespace Erdos3

noncomputable def reciprocalTerm (A : Set ℕ) (n : ℕ) : ℝ := by
  classical
  exact if n ∈ A then (n : ℝ)⁻¹ else 0

end Erdos3

namespace Erdos3

def ReciprocalProgressionTheorem : Prop :=
  ∀ A : Set ℕ, ¬ Summable (reciprocalTerm A) → ∀ k : ℕ, HasAP A k

end Erdos3

namespace Erdos3

theorem manuscriptReciprocalProgressionTheorem : ReciprocalProgressionTheorem := by
  sorry

end Erdos3

end OAI
set_option pp.all true in
#print OAI.Erdos3.ReciprocalProgressionTheorem
set_option pp.all true in
#print OAI.Erdos3.HasAP
set_option pp.all true in
#print OAI.Erdos3.reciprocalTerm
#print axioms OAI.Erdos3.manuscriptReciprocalProgressionTheorem
