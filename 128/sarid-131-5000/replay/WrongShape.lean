import Erdos128
/-- Second negative control: a deliberately WRONG shape (130 in place of 131) must FAIL to type-check by `Iff.rfl`. -/
theorem host_wrong_shape :
    Erdos128.FormalConjecturesStatement131_5000 ↔
    (∀ (V : Type) [Fintype V] (G : SimpleGraph V),
      (∀ V' : Set V, 2 * V'.ncard + 1 ≥ Fintype.card V →
        5000 * (G.induce V').edgeSet.ncard > 130 * Fintype.card V ^ 2) → ¬ G.CliqueFree 3) :=
  Iff.rfl
