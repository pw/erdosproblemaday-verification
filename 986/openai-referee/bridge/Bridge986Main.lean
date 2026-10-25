/-
Unconditional bridge (15:00Z erdos seat, 2026-10-20). Imports both OpenAI `Main` modules (family 170) and the conditional
bridge `Bridge986` (drafted by the 12:00Z formal seat, compiled unchanged). Adds the s = 4 case through OpenAI's own
`LowerTransfer.actual_prime_construction` (the 12:00Z seat's probe `Extra_S4`, copied verbatim below), so that the
Formal Conjectures statement `erdos_986` (verbatim copy, `FC.Erdos986Statement`) reduces EXACTLY to its s = 3 instance.
-/
import Bridge986
import OAI.Combinatorics.SharpRamsey.Main
import OAI.Combinatorics.RamseyFive.Main

namespace Bridge986
open OAI.SharpLogRamsey

/-- Verbatim from probe `Extra_S4` (12:00Z seat): OpenAI's assembly `main_of_primeConstruction`, with `4 ≤ s`. -/
theorem main_of_primeConstruction4 (s : ℕ) (hs : 4 ≤ s)
    (hprime : LowerTransfer.PrimeConstruction (s-1)) : MainBounds s ∧ MainLimit s := by
  have hb : MainBounds s := by
    obtain ⟨C,hC,t₀,ht₀⟩ := Upper.ramsey_upper (by omega : 3 ≤ s)
    refine ⟨C,hC,fun ε hε => ?_⟩
    have hl := LowerTransfer.all_epsilon_lower (s-1) (by omega) hprime ε hε
    have he : s-1+1=s := by omega
    have he' : s-1-1=s-2 := by omega
    rw [he,he'] at hl
    obtain ⟨t₁,ht₁⟩ := Filter.eventually_atTop.mp hl
    exact ⟨max t₀ t₁,fun t ht => ⟨ht₁ t ((le_max_right _ _).trans ht),
      ht₀ t ((le_max_left _ _).trans ht)⟩⟩
  exact ⟨hb,mainLimit_of_mainBounds s hb⟩

theorem main_ge4 (s : ℕ) (hs : 4 ≤ s) : MainBounds s ∧ MainLimit s := by
  have h := LowerTransfer.actual_prime_construction (s-4)
  rw [show s-4+3 = s-1 by omega] at h
  exact main_of_primeConstruction4 s hs h

/-- r(4,t) = t³/(log t)^(2+o(1)), in OpenAI's s ≥ 6 definitions. -/
theorem main4 : MainBounds 4 ∧ MainLimit 4 := main_ge4 4 le_rfl

/-- Family 170 implies FC `erdos_986` for every s ≥ 5 (c = s − 1, C = 1) — via the two papers' own theorems. -/
theorem erdos986At_ge_five_unconditional : ∀ s, 5 ≤ s → FC.Erdos986At s :=
  erdos986At_ge_five OAI.SharpRamseyFive.main.1 (fun s hs => (OAI.SharpLogRamsey.main s hs).1)

/-- …and for s = 4 (c = 3, C = 1) through `actual_prime_construction 1`, which neither paper states. -/
theorem erdos986At_four : FC.Erdos986At 4 := erdos986At_of_mainBounds 4 main4.1

/-- Every s ≥ 4 from the s ≥ 6 library alone (the s = 5 paper not used). -/
theorem erdos986At_ge_four_sharpLogOnly : ∀ s, 4 ≤ s → FC.Erdos986At s :=
  fun s hs => erdos986At_of_mainBounds s (main_ge4 s hs).1

/-- The exact remaining gap: FC `erdos_986` ⇔ its s = 3 instance (classical: Erdős 1961, Kim 1995). -/
theorem erdos986_iff_three : FC.Erdos986Statement ↔ FC.Erdos986At 3 := by
  rw [statement_iff_three_four OAI.SharpRamseyFive.main.1 (fun s hs => (OAI.SharpLogRamsey.main s hs).1)]
  exact ⟨fun h => h.1, fun h => ⟨h, erdos986At_four⟩⟩

end Bridge986

set_option pp.all true
#check @Bridge986.erdos986_iff_three
#check @Bridge986.erdos986At_ge_four_sharpLogOnly
#print axioms Bridge986.erdos986At_ge_five_unconditional
#print axioms Bridge986.erdos986At_four
#print axioms Bridge986.erdos986At_ge_four_sharpLogOnly
#print axioms Bridge986.erdos986_iff_three
#print axioms Bridge986.classicalRamsey_eq_sharpLog
#print axioms Bridge986.classicalRamsey_eq_five
