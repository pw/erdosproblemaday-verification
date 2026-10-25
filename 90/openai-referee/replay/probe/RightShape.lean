import OAI.Geometry.UnitDistances.Main
-- must COMPILE: the page's statement, written from the comparator, is exactly what Main proves
example : ∃ C β : ℝ, 0 < C ∧ 1 ≤ β ∧ β < (4 : ℝ) / 3 ∧
    ∀ n : ℕ, (OAI.PlanarUnitDistances.u n : ℝ) ≤ C * (n : ℝ) ^ β := OAI.PlanarUnitDistances.main
