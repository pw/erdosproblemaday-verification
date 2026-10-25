import Bridge986
-- must FAIL: a mutated FC definition (K_{k+1} instead of K_k) is not OpenAI's ramsey.
noncomputable def mutRamsey (k l : ℕ) : ℕ := Bridge986.FC.graphRamsey (SimpleGraph.completeGraph (Fin (k+1))) (SimpleGraph.completeGraph (Fin l))
example (s k : ℕ) : mutRamsey s k = OAI.SharpLogRamsey.ramsey s k := by
  unfold mutRamsey Bridge986.FC.graphRamsey OAI.SharpLogRamsey.ramsey
  congr 1
  ext n
  simp only [Set.mem_setOf_eq, OAI.SharpLogRamsey.RamseyProperty]
  refine forall_congr' fun C => or_congr ?_ ?_
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    simp [SimpleGraph.CliqueFree]
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    simp [SimpleGraph.CliqueFree]
