import OAI.Geometry.Borsuk.Main
-- must FAIL: main_theorem's non-cover clause is about ten sets; it cannot be re-typed as eleven
def HasElevenSmallCover : Prop :=
  ∃ C : Fin 11 → Set OAI.BorsukNine.Matrix4,
    (∀ i, C i ⊆ OAI.BorsukNine.projectorSet) ∧ OAI.BorsukNine.projectorSet ⊆ ⋃ i, C i ∧
    ∀ i, Metric.diam (C i) < Real.sqrt 2
theorem wrongK : ¬ HasElevenSmallCover := OAI.BorsukNine.main_theorem.2.2.2
