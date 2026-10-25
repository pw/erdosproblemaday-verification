import OAI.Combinatorics.SharpRamsey.Main
-- must FAIL: the solution requires 6 ≤ s; it cannot be applied at s = 5 (type-level control)
theorem wrongHyp (s : ℕ) (hs : 5 ≤ s) : OAI.SharpLogRamsey.MainBounds s ∧ OAI.SharpLogRamsey.MainLimit s :=
  OAI.SharpLogRamsey.main s hs
