import SeatD003.NoLSStatement
import SeatD003.DepAudit
-- Mathlib-only environment: the statement text re-elaborated must be SAME (positive control of #seatD_same)
#seatD_same SeatD003.NoLandauSiegel (∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q)
