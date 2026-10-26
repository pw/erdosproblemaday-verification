import SeatD003.NoLSStatement
import SeatD003.DepAudit
import OAI.NumberTheory.Jacobsthal.Siegel.DirichletRealZeroBound
/-! Seat D bridge. `SeatD003.NoLandauSiegel` was elaborated and compiled in a Mathlib-only environment
(its .olean is fixed before this file runs); here the kernel checks OpenAI's proof term against it. -/

theorem SeatD003.bridge : SeatD003.NoLandauSiegel :=
  OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound

-- meaning-preserving variant (≥): must also be accepted
theorem SeatD003.bridge_ge : SeatD003.NoLandauSiegel_ge :=
  OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound

#print axioms SeatD003.bridge
#print axioms SeatD003.bridge_ge
#print axioms OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound

-- the statement's constant closure, re-audited in the MIXED environment
#seatD_audit SeatD003.NoLandauSiegel
-- (the same audit of OpenAI's theorem's TYPE was run in run 1, logs/Bridge.run1_with_type_audit.log: its only
--  non-Mathlib-family constant is the theorem itself; moved out so this file can produce an .olean)

-- the 10-23 loophole, tested directly: the same statement TEXT elaborated in the mixed environment
#seatD_same SeatD003.NoLandauSiegel (∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q)

-- what the proof actually uses: foreign modules reached and every PNT+ constant
#seatD_deps SeatD003.bridge

set_option pp.fullNames true in
#check @OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound
