import Mathlib
/-! Probe: the only pp.all differences between Formal Conjectures' `SimpleGraph.IsDecomposition` (elaborated under Mathlib 0df444a3)
and our verbatim copy `Bridge184.IsDecomposition` (elaborated under Mathlib d13f23b7) are the instance paths to `PartialOrder` and
`OrderBot` on `Set (Sym2 V)`. Here both paths are written out explicitly, in one environment, and the two `PairwiseDisjoint`
propositions are shown definitionally equal (`Iff.rfl`, kernel-checked). -/
universe u
variable {V : Type u} {ι : Type u} (s : Set ι) (f : ι → Set (Sym2 V))

theorem neg_control_complement :
    (@Set.PairwiseDisjoint (Set (Sym2 V)) ι
      (@CompleteSemilatticeInf.toPartialOrder (Set (Sym2 V)) (@CompleteLattice.toCompleteSemilatticeInf (Set (Sym2 V))
        (@CompleteBooleanAlgebra.toCompleteLattice (Set (Sym2 V)) (@CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra (Set (Sym2 V))
          (@Set.instCompleteAtomicBooleanAlgebra (Sym2 V))))))
      (@HeytingAlgebra.toOrderBot (Set (Sym2 V)) (@Order.Frame.toHeytingAlgebra (Set (Sym2 V)) (@CompleteDistribLattice.toFrame (Set (Sym2 V))
        (@CompleteBooleanAlgebra.toCompleteDistribLattice (Set (Sym2 V)) (@CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra (Set (Sym2 V))
          (@Set.instCompleteAtomicBooleanAlgebra (Sym2 V)))))))
      s f) ↔
    (@Set.PairwiseDisjoint (Set (Sym2 V)) ι
      (@CompletePartialOrder.toPartialOrder (Set (Sym2 V)) (@CompleteLattice.toCompletePartialOrder (Set (Sym2 V))
        (@CompleteBooleanAlgebra.toCompleteLattice (Set (Sym2 V)) (@CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra (Set (Sym2 V))
          (@Set.instCompleteAtomicBooleanAlgebra (Sym2 V))))))
      (@CompletePartialOrder.toOrderBot (Set (Sym2 V)) (@CompleteLattice.toCompletePartialOrder (Set (Sym2 V))
        (@CompleteBooleanAlgebra.toCompleteLattice (Set (Sym2 V)) (@CompleteAtomicBooleanAlgebra.toCompleteBooleanAlgebra (Set (Sym2 V))
          (@Set.instCompleteAtomicBooleanAlgebra (Sym2 V))))))
      s (fun j => (f j)ᶜ)) := Iff.rfl

#print axioms neg_control_complement
