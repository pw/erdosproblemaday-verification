import OAI.Combinatorics.SharpRamsey.Main
/-! Probe (ours, 12:00Z erdos seat 2026-10-20): OpenAI's family-170 library proves its prime construction for EVERY d ≥ 3
(`LowerTransfer.actual_prime_construction (i) : PrimeConstruction (i+3)`), while both papers state d ≥ 5 / s ≥ 6 (and s = 5 separately).
`main_of_primeConstruction` asks 6 ≤ s but its proof only uses 3 ≤ s and 1 ≤ s−1. Here: the same proof, verbatim, with 4 ≤ s,
fed by `actual_prime_construction` — giving MainBounds s ∧ MainLimit s for every s ≥ 4, in OpenAI's own definitions, unchanged. -/
namespace Probe986
open OAI.SharpLogRamsey

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

/-- r(4,t) = t³/(log t)^(2+o(1)): the s = 4 case, which neither family-170 paper states. -/
theorem main4 : MainBounds 4 ∧ MainLimit 4 := main_ge4 4 le_rfl
/-- s = 5 from the s ≥ 6 paper's library (Paper A's theorem, in Paper B's definitions). -/
theorem main5 : MainBounds 5 ∧ MainLimit 5 := main_ge4 5 (by norm_num)

end Probe986
set_option pp.all true
#check @Probe986.main4
#print axioms Probe986.main_ge4
#print axioms Probe986.main4
#print axioms Probe986.main5
#print axioms OAI.SharpLogRamsey.LowerTransfer.actual_prime_construction
