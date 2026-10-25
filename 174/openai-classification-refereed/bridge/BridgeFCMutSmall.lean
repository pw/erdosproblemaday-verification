import Mathlib
import OAI.Combinatorics.SphericalRamsey.Main
import OAI.Combinatorics.EuclideanRamsey.Spherical

/-!
# Bridges: OpenAI's Lean ⟹ Formal Conjectures' `Erdos174` (erdos cron seat, 2026-10-21)

`IsRamsey` and the statements of `erdos_174.variants.graham` and `erdos_174.variants.spherical` below are verbatim
copies of `FormalConjectures/ErdosProblems/174.lean` at google-deepmind/formal-conjectures@2a315101 (merged
2026-10-20 in PR #7469), FC attributes and docstrings removed (`verbatim_check.py` asserts the copies,
whitespace-normalised). FC tags `graham` "research open"; it is false, and `graham_false` below derives the
negation of FC's statement from OpenAI's `OAI.GrahamSpherical.full_main` (the twelve-point set). FC tags
`spherical` "research solved" with a `sorry`; `erdos_174.variants.spherical` below proves FC's statement from
OpenAI's `OAI.EuclideanRamsey.ramsey_cospherical`. The proofs are ours; the mathematics is OpenAI's.
-/

namespace Erdos174

def IsRamsey {n : ℕ} (A : Set (EuclideanSpace ℝ (Fin n))) : Prop :=
  A.Finite ∧ ∀ k : ℕ, 1 ≤ k → ∃ d : ℕ, ∀ c : EuclideanSpace ℝ (Fin d) → Fin k,
    ∃ p : A → EuclideanSpace ℝ (Fin d),
      Congruent (fun a : A ↦ (a : EuclideanSpace ℝ (Fin n))) p ∧ ∃ i, ∀ a, c (p a) = i

/-- A copy of a set with two distinct points cannot live in `ℝ⁰`. -/
theorem dim_pos_of_congruent {n d : ℕ} {A : Set (EuclideanSpace ℝ (Fin n))}
    {x y : EuclideanSpace ℝ (Fin n)} (hx : x ∈ A) (hy : y ∈ A) (hxy : x ≠ y)
    {p : A → EuclideanSpace ℝ (Fin d)}
    (hp : Congruent (fun a : A ↦ (a : EuclideanSpace ℝ (Fin n))) p) : 0 < d := by
  rcases Nat.eq_zero_or_pos d with rfl | h
  · exfalso
    have h1 := hp ⟨x, hx⟩ ⟨y, hy⟩
    have h2 : p ⟨x, hx⟩ = p ⟨y, hy⟩ := Subsingleton.elim _ _
    rw [h2, edist_self] at h1
    exact hxy (edist_eq_zero.mp h1)
  · exact h

/-- FC's `IsRamsey` for the twelve-point witness gives OpenAI's set-based `EuclideanRamsey`. -/
theorem isRamsey_witness_oai (h : IsRamsey OAI.GrahamSpherical.witness) :
    OAI.GrahamSpherical.EuclideanRamsey OAI.GrahamSpherical.witness := by
  have hcard := OAI.GrahamSpherical.full_main.1
  have hfin : OAI.GrahamSpherical.witness.Finite := h.1
  obtain ⟨x, y, hx, hy, hxy⟩ := (Set.one_lt_ncard_iff hfin).mp (by rw [hcard]; norm_num)
  intro r hr
  obtain ⟨d, hd⟩ := h.2 r hr
  obtain ⟨p0, hp0, -⟩ := hd (fun _ => ⟨0, hr⟩)
  refine ⟨d, dim_pos_of_congruent hx hy hxy hp0, fun color => ?_⟩
  obtain ⟨p, hp, i, hi⟩ := hd color
  exact ⟨p, fun a b => (hp a b).symm, i, hi⟩

/-- The negation of FC's `erdos_174.variants.graham` (statement verbatim inside the `¬`). -/
theorem graham_false :
    ¬ (∀ {n : ℕ} (A : Set (EuclideanSpace ℝ (Fin n))) (hA : A.Finite)
        (hs : EuclideanGeometry.Cospherical A) (h5 : A.ncard ≤ 5), IsRamsey A) := by
  intro h
  obtain ⟨hcard, hsph, -, hnot⟩ := OAI.GrahamSpherical.full_main
  have hfin : OAI.GrahamSpherical.witness.Finite := Set.finite_of_ncard_ne_zero (by rw [hcard]; norm_num)
  have hcos : EuclideanGeometry.Cospherical OAI.GrahamSpherical.witness :=
    ⟨0, 1, fun p hp => by simpa using hsph hp⟩
  exact hnot (isRamsey_witness_oai (h OAI.GrahamSpherical.witness hfin hcos))

/-- FC's `erdos_174.variants.spherical` (statement verbatim), from OpenAI's `ramsey_cospherical`. -/
theorem erdos_174.variants.spherical {n : ℕ} (A : Set (EuclideanSpace ℝ (Fin n)))
    (hA : IsRamsey A) : EuclideanGeometry.Cospherical A := by
  classical
  have hfin : A.Finite := hA.1
  by_cases hsub : A.Subsingleton
  · rcases hsub.eq_empty_or_singleton with rfl | ⟨x, rfl⟩
    · exact EuclideanGeometry.cospherical_empty
    · exact EuclideanGeometry.cospherical_singleton x
  · obtain ⟨x, hx, y, hy, hxy⟩ : ∃ x ∈ A, ∃ y ∈ A, x ≠ y := by
      simpa [Set.Subsingleton] using hsub
    have : Finite A := hfin.to_subtype
    let e : Fin (Nat.card A) ≃ A := (Finite.equivFin A).symm
    let a : Fin (Nat.card A) → OAI.EuclideanRamsey.Space n := fun i => (e i : EuclideanSpace ℝ (Fin n))
    have ha : Function.Injective a := fun i j hij => e.injective (Subtype.ext hij)
    have hrange : Set.range a = A := by
      ext z; constructor
      · rintro ⟨i, rfl⟩; exact (e i).2
      · intro hz; exact ⟨e.symm ⟨z, hz⟩, by simp only [a, Equiv.apply_symm_apply]⟩
    have hR : OAI.EuclideanRamsey.Ramsey a := by
      intro r hr
      obtain ⟨d, hd⟩ := hA.2 r (by omega)
      obtain ⟨p0, hp0, -⟩ := hd (fun _ => ⟨0, by omega⟩)
      refine ⟨d, dim_pos_of_congruent hx hy hxy hp0, fun c => ?_⟩
      obtain ⟨p, hp, k, hk⟩ := hd c
      refine ⟨fun i => p (e i), fun i j => ?_, k, fun i => hk (e i)⟩
      have := hp (e i) (e j)
      simp only [dist_edist, a] at this ⊢
      rw [this]
    have := OAI.EuclideanRamsey.ramsey_cospherical a ha hR
    rwa [hrange] at this

end Erdos174
