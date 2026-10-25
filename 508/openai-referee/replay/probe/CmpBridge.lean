import OAI.Geometry.PlaneColoring.Five
-- STATEMENT MATCH BY THE KERNEL: the comparator's definition and theorem statement, copied VERBATIM (binder names included)
-- from ComparatorChallenges/EuclideanFiveColor.lean into a fresh namespace, with the theorem PROVED BY the solution's theorem.
-- This compiles iff the comparator's ProperColoring and the solution's are definitionally the same and the statements agree.
namespace Cmp
def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
  ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 → coloring point ≠ coloring otherPoint
theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring :=
  OAI.EuclideanFiveColor.no_proper_five_coloring
end Cmp
#print axioms Cmp.no_proper_five_coloring
