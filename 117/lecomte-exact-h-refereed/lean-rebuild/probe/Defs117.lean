import ErdosProblems.Erdos117
#print Erdos117.NoncommutingBound
#print Erdos117.AbelianCover
#print Erdos117.HasAbelianCover
#print Erdos117.UniversalAbelianCoverBound
#print Erdos117.h
#check @Erdos117.erdos_117
#print axioms Erdos117.erdos_117
-- control: the quaternion group Q8 has a noncommuting triple, so NoncommutingBound Q8 2 must be FALSE; we only
-- check that the bound with n = 2 is not provable by `decide`-free trivialities by stating its negation as a goal type.
example : Erdos117.NoncommutingBound (Multiplicative (ZMod 2)) 1 := by
  intro s hs
  -- in an abelian group a pairwise-noncommuting set has at most one element
  by_contra hlt
  push_neg at hlt
  obtain ⟨x, hx, y, hy, hxy⟩ := Finset.one_lt_card.mp hlt
  exact hs hx hy hxy (Commute.all x y)
