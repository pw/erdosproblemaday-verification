import Erdos1139Official
open Nat Filter
open scoped ArithmeticFunction.Omega
-- Negative controls: each must FAIL to typecheck.
-- (1) Ω n ≤ 3 instead of ≤ 2
theorem neg1 : letI u := Nat.nth (fun n ↦ 0 < n ∧ Ω n ≤ 3)
    atTop.limsup (fun k : ℕ ↦ (((u (k + 1) : ℝ) - (u k : ℝ)) / Real.log (↑k + 1) : EReal)) = ⊤ := Erdos1139.erdos_1139
-- (2) limsup replaced by liminf
theorem neg2 : letI u := Nat.nth (fun n ↦ 0 < n ∧ Ω n ≤ 2)
    atTop.liminf (fun k : ℕ ↦ (((u (k + 1) : ℝ) - (u k : ℝ)) / Real.log (↑k + 1) : EReal)) = ⊤ := Erdos1139.erdos_1139
-- (3) log k replaced by log (k+2)
theorem neg3 : letI u := Nat.nth (fun n ↦ 0 < n ∧ Ω n ≤ 2)
    atTop.limsup (fun k : ℕ ↦ (((u (k + 1) : ℝ) - (u k : ℝ)) / Real.log (↑k + 2) : EReal)) = ⊤ := Erdos1139.erdos_1139
