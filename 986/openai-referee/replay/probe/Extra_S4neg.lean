import OAI.Combinatorics.SharpRamsey.Main
/-! Negative control for Extra_S4 (must FAIL to elaborate): the construction is NOT available at d = 2 through this route —
`actual_prime_construction (i)` only reaches d = i+3 ≥ 3, so asking for s = 3 (PrimeConstruction 2) must not typecheck. -/
open OAI.SharpLogRamsey
example : LowerTransfer.PrimeConstruction 2 := LowerTransfer.actual_prime_construction 0
