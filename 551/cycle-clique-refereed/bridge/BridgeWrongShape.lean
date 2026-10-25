import OAI.Combinatorics.Ramsey.CycleClique.MainTheorem
-- NEGATIVE CONTROL: the same proof aimed at a WRONG value ((k-1)(n-1), no +1). Must FAIL to elaborate.
namespace Bridge551W
namespace SimpleGraph
noncomputable def graphRamsey {α β : Type*} [Fintype α] [Fintype β]
    (G : SimpleGraph α) (H : SimpleGraph β) : ℕ :=
  sInf { n : ℕ | ∀ (C : SimpleGraph (Fin n)), G.IsContained C ∨ H.IsContained Cᶜ }
end SimpleGraph
theorem erdos_551_wrong :
    ∀ (k n : ℕ), 3 ≤ n → n ≤ k → ¬(n = 3 ∧ k = 3) →
      SimpleGraph.graphRamsey (SimpleGraph.cycleGraph k)
        (SimpleGraph.completeGraph (Fin n)) = (k - 1) * (n - 1) := by
  intro k n hn hnk hne
  have hne' : (k, n) ≠ (3, 3) := by
    intro h
    exact hne ⟨(Prod.mk.inj h).2, (Prod.mk.inj h).1⟩
  have h := OAI.CycleClique.main k n hnk hn hne'
  rw [← h]
  rfl
end Bridge551W
