import OAI.Geometry.UnitDistances.Main
-- must FAIL (type mismatch): exponent β/2 is NOT what Main proves — control that the right-shape probe can fail
example : ∃ C β : ℝ, 0 < C ∧ 1 ≤ β ∧ β < (4 : ℝ) / 3 ∧
    ∀ n : ℕ, (OAI.PlanarUnitDistances.u n : ℝ) ≤ C * (n : ℝ) ^ (β / 2) := OAI.PlanarUnitDistances.main
