import OAI.Geometry.PlaneColoring.Five
-- CONTROL (must FAIL): the comparator's definition with the distance changed to 2 — the solution's theorem must NOT prove it.
namespace CmpWrong
def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
  ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 2 → coloring point ≠ coloring otherPoint
theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring :=
  OAI.EuclideanFiveColor.no_proper_five_coloring
end CmpWrong
