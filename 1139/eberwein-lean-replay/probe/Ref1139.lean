import Mathlib
-- The Formal Conjectures statement of erdos_1139, verbatim (FC main, FormalConjectures/ErdosProblems/1139.lean),
-- elaborated in an environment that imports Mathlib ONLY (none of the submitted modules).
open Nat Filter
open scoped ArithmeticFunction.Omega
open scoped Topology

namespace Ref1139

theorem erdos_1139 :
    letI u := Nat.nth (fun n ↦ 0 < n ∧ Ω n ≤ 2)
    atTop.limsup (fun k : ℕ ↦ (((u (k + 1) : ℝ) - (u k : ℝ)) / Real.log (↑k + 1) : EReal)) = ⊤ := by
  sorry

end Ref1139
