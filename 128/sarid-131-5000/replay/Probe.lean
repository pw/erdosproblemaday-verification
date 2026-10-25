import Erdos128

/-! Host seat probes (erdos cron 2026-10-12 18:00Z). Printed statements + a syntactic match of the
Formal Conjectures shape. Every `#print axioms` line must list exactly propext/Classical.choice/Quot.sound. -/

set_option pp.all true in
#check @Erdos128.ModuloBCL.sparse_half_131_5000

set_option pp.all true in
#check @Erdos128.ModuloBCL.formalConjectures_131_5000

#print Erdos128.ModuloBCL.BCLEventual
#print Erdos128.BCLCutCertificate
#print Erdos128.HasSparseHalf
#print Erdos128.edgeCountOn
#print Erdos128.FormalConjecturesStatement
#print Erdos128.C4FlagCertificate
#print Erdos128.c4Hom

/-- The 131/5000 Formal-Conjectures shape is the upstream FC body with (1,50) → (131,5000), by `Iff.rfl`. -/
theorem host_fc_shape_131_5000 :
    Erdos128.FormalConjecturesStatement131_5000 ↔
    (∀ (V : Type) [Fintype V] (G : SimpleGraph V),
      (∀ V' : Set V, 2 * V'.ncard + 1 ≥ Fintype.card V →
        5000 * (G.induce V').edgeSet.ncard > 131 * Fintype.card V ^ 2) → ¬ G.CliqueFree 3) :=
  Iff.rfl

/-- The (1,50) instance is the upstream FC body up to `1 * n^2 = n^2`. -/
theorem host_fc_shape_1_50 :
    Erdos128.FormalConjecturesStatement 1 50 ↔
    (∀ (V : Type) [Fintype V] (G : SimpleGraph V),
      (∀ V' : Set V, 2 * V'.ncard + 1 ≥ Fintype.card V →
        50 * (G.induce V').edgeSet.ncard > Fintype.card V ^ 2) → ¬ G.CliqueFree 3) := by
  unfold Erdos128.FormalConjecturesStatement
  simp only [Nat.one_mul]

#print axioms host_fc_shape_131_5000
#print axioms host_fc_shape_1_50
#print axioms Erdos128.ModuloBCL.provider_of_eventual
#print axioms Erdos128.ModuloBCL.sparse_half_131_5000
#print axioms Erdos128.ModuloBCL.formalConjectures_131_5000
#print axioms Erdos128.C4Certificate.checkedC4FlagCertificateProvider
#print axioms Erdos128.C4Certificate.certificate_all_triangleFree_masks
