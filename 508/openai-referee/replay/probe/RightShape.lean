import OAI.Geometry.PlaneColoring.Five
-- must COMPILE: erdosproblems.com/508's lower-bound statement written from scratch, no OAI definitions:
-- every colouring of the plane with five colours has two points at distance exactly 1 of the same colour.
-- (a) in ℂ with its Euclidean metric
example : ∀ c : ℂ → Fin 5, ∃ x y : ℂ, dist x y = 1 ∧ c x = c y := by
  intro c
  by_contra h
  push_neg at h
  exact OAI.EuclideanFiveColor.no_proper_five_coloring
    ⟨c, fun x y hxy => h x y (by rwa [dist_eq_norm])⟩
-- (b) in EuclideanSpace ℝ (Fin 2), transported along the linear isometry ℂ ≃ₗᵢ[ℝ] ℝ² (so dist is the ℓ² distance)
example : ∀ c : EuclideanSpace ℝ (Fin 2) → Fin 5,
    ∃ x y : EuclideanSpace ℝ (Fin 2), dist x y = 1 ∧ c x = c y := by
  intro c
  by_contra h
  push_neg at h
  let e : ℂ ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 2) := Complex.orthonormalBasisOneI.repr
  refine OAI.EuclideanFiveColor.no_proper_five_coloring ⟨fun z => c (e z), fun x y hxy => h (e x) (e y) ?_⟩
  rw [e.dist_map, dist_eq_norm]
  exact hxy
-- (c) the chromatic-number phrasing: no 5-colouring, so any proper colouring with k colours has k ≥ 6
example (k : ℕ) (c : ℂ → Fin k) (hc : ∀ x y : ℂ, dist x y = 1 → c x ≠ c y) : 6 ≤ k := by
  by_contra hk
  push_neg at hk
  have hle : k ≤ 5 := by omega
  let f : Fin k → Fin 5 := fun i => ⟨i.val, lt_of_lt_of_le i.isLt hle⟩
  have hf : Function.Injective f := fun i j hij => Fin.ext (Fin.mk.inj hij)
  exact OAI.EuclideanFiveColor.no_proper_five_coloring
    ⟨fun z => f (c z), fun x y hxy hxy' => hc x y (by rwa [dist_eq_norm]) (hf hxy')⟩
