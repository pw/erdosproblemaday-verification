import Erdos301

/-! POSITIVE CONTROL for the axioms printer (must compile, with a `sorry` warning,
and `#print axioms` must name `sorryAx` and `EPAD301.cheat`). -/
namespace EPAD301
axiom cheat : False
theorem fake_by_sorry : ¬ Erdos301.Erdos301Conclusion := by sorry
theorem fake_by_axiom : ¬ Erdos301.Erdos301Conclusion := cheat.elim
end EPAD301
#print axioms EPAD301.fake_by_sorry
#print axioms EPAD301.fake_by_axiom
