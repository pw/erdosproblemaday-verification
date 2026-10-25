import OAI.Combinatorics.CycleDecomposition.Main
-- must FAIL to elaborate: a constant bound (k ≤ C) is false (a matching on n/2 edges needs n/2 parts)
theorem wrong : ∃ C : ℝ, 0 < C ∧ ∀ (n : ℕ) (G : SimpleGraph (Fin n)),
    ∃ k : ℕ, OAI.ErdosGallai.EdgeDecomposition G k ∧ (k : ℝ) ≤ C := OAI.ErdosGallai.erdos_gallai
