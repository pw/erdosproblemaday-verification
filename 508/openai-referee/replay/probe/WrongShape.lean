import OAI.Geometry.PlaneColoring.Five
-- must FAIL (type mismatch): six colours is NOT what the theorem says — the control that RightShape can fail
example : ¬ ∃ c : ℂ → Fin 6, OAI.EuclideanFiveColor.ProperColoring 6 c :=
  OAI.EuclideanFiveColor.no_proper_five_coloring
