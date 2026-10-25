import OAI.Geometry.PinnedDistances.Pins
open Filter Topology
-- must FAIL (type mismatch): exponent 1 + ε is NOT what exists_pin_eventually proves — control that RightShape can fail
example : ∀ ε : ℝ, 0 < ε → ∀ᶠ n : ℕ in atTop, ∀ P : Finset (EuclideanSpace ℝ (Fin 2)), P.card = n →
    ∃ x ∈ P, (P.card : ℝ) ^ (1 + ε) ≤ ((OAI.WeakPinned.distances P x).card : ℝ) :=
  OAI.WeakPinned.exists_pin_eventually
