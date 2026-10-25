import OAI.Geometry.PinnedDistances.Pins
open Filter Topology
-- must COMPILE: erdosproblems.com/604's first question, written from scratch (no OAI definitions in the statement):
-- for every ε > 0, every sufficiently large n-point planar set has a point determining ≥ n^(1−ε) distinct distances.
example : ∀ ε : ℝ, 0 < ε → ∀ᶠ n : ℕ in atTop, ∀ P : Finset (EuclideanSpace ℝ (Fin 2)), P.card = n →
    ∃ x ∈ P, (n : ℝ) ^ (1 - ε) ≤ (((P.erase x).image (fun y => dist y x)).card : ℝ) := by
  intro ε hε
  filter_upwards [OAI.WeakPinned.exists_pin_eventually ε hε] with n h P hP
  obtain ⟨x, hx, hle⟩ := h P hP
  subst hP
  exact ⟨x, hx, hle⟩
-- and Theorem 1.1 exactly as the comparator states it
example (s : ℝ) (hs : 0 < s) : Tendsto (fun n : ℕ => OAI.WeakPinned.F n s) atTop (𝓝 0) :=
  OAI.WeakPinned.main s hs
