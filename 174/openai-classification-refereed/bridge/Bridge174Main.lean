import Bridge174FC
import OAI.Combinatorics.EuclideanRamsey.Main

/-!
# Formal Conjectures' `erdos_174` in FC's own terms, from OpenAI's classification (ours, 2026-10-21)

FC states `erdos_174 (n) : {A | IsRamsey A} = erdos_174.answer n` with `answer := sorry`. We cannot fill FC's `sorry`
in place; instead `erdos_174_criterion` proves the same set equality with an explicit right-hand side `criterionAnswer`:
the finite sets that are subsingletons or are congruent, through an explicit labelling, to a configuration with full
affine span satisfying OpenAI's `FieldCriterion` (Theorem 1.1 of OpenAI family 172). The mathematics is OpenAI's
`classification_nonempty`; ours is the transport between FC's set-based copies and OpenAI's indexed ones.
-/

namespace Erdos174

/-- Our explicit answer for FC's `erdos_174`. -/
def criterionAnswer (n : ℕ) : Set (Set (EuclideanSpace ℝ (Fin n))) :=
  {A | A.Finite ∧ (A.Subsingleton ∨ ∃ (s d : ℕ) (b : Fin s → OAI.EuclideanRamsey.Space d) (f : Fin s ≃ A),
      1 ≤ d ∧ Function.Injective b ∧ affineSpan ℝ (Set.range b) = ⊤ ∧ OAI.EuclideanRamsey.FieldCriterion b ∧
      ∀ i j, dist (b i) (b j) = dist ((f i : EuclideanSpace ℝ (Fin n))) (f j))}

theorem isRamsey_of_subsingleton {n : ℕ} {A : Set (EuclideanSpace ℝ (Fin n))} (hA : A.Subsingleton) :
    IsRamsey A := by
  refine ⟨hA.finite, fun k hk => ⟨0, fun c => ⟨fun _ => 0, ?_, c 0, fun _ => rfl⟩⟩⟩
  intro x y
  have : (x : EuclideanSpace ℝ (Fin n)) = y := hA x.2 y.2
  simp [this]

/-- FC's `IsRamsey` ⇔ OpenAI's `Ramsey` of any enumeration, for a set with two distinct points. -/
theorem isRamsey_iff_oai {n s : ℕ} {A : Set (EuclideanSpace ℝ (Fin n))} (hfin : A.Finite) (e : Fin s ≃ A)
    {x y : EuclideanSpace ℝ (Fin n)} (hx : x ∈ A) (hy : y ∈ A) (hxy : x ≠ y) :
    IsRamsey A ↔ OAI.EuclideanRamsey.Ramsey (fun i => (e i : EuclideanSpace ℝ (Fin n))) := by
  constructor
  · intro hA r hr
    obtain ⟨d, hd⟩ := hA.2 r (by omega)
    obtain ⟨p0, hp0, -⟩ := hd (fun _ => ⟨0, by omega⟩)
    refine ⟨d, dim_pos_of_congruent hx hy hxy hp0, fun c => ?_⟩
    obtain ⟨p, hp, k, hk⟩ := hd c
    refine ⟨fun i => p (e i), fun i j => ?_, k, fun i => hk (e i)⟩
    have := hp (e i) (e j)
    simp only [dist_edist] at this ⊢
    rw [this]
  · intro hR
    refine ⟨hfin, fun k hk => ?_⟩
    rcases Nat.lt_or_ge k 2 with hk1 | hk2
    · obtain rfl : k = 1 := by omega
      exact ⟨n, fun c => ⟨fun a => (a : EuclideanSpace ℝ (Fin n)), fun _ _ => rfl, 0,
        fun _ => Subsingleton.elim _ _⟩⟩
    · obtain ⟨D, -, hD⟩ := hR k hk2
      refine ⟨D, fun c => ?_⟩
      obtain ⟨b, hb, j, hj⟩ := hD c
      refine ⟨fun a => b (e.symm a), fun a a' => ?_, j, fun a => hj _⟩
      have := hb (e.symm a) (e.symm a')
      simp only [Equiv.apply_symm_apply] at this
      simp only [edist_dist, this]

theorem erdos_174_criterion (n : ℕ) :
    {A : Set (EuclideanSpace ℝ (Fin n)) | IsRamsey A} = criterionAnswer n := by
  classical
  ext A
  constructor
  · intro hA
    refine ⟨hA.1, ?_⟩
    by_cases hsub : A.Subsingleton
    · exact Or.inl hsub
    · right
      obtain ⟨x, hx, y, hy, hxy⟩ : ∃ x ∈ A, ∃ y ∈ A, x ≠ y := by simpa [Set.Subsingleton] using hsub
      have := hA.1.to_subtype
      let e : Fin (Nat.card A) ≃ A := (Finite.equivFin A).symm
      have ha : Function.Injective (fun i => (e i : EuclideanSpace ℝ (Fin n))) :=
        fun i j hij => e.injective (Subtype.ext hij)
      have hpos : 0 < Nat.card A := Nat.card_pos_iff.mpr ⟨⟨⟨x, hx⟩⟩, inferInstance⟩
      rcases (OAI.EuclideanRamsey.classification_nonempty _ hpos ha).mp
          ((isRamsey_iff_oai hA.1 e hx hy hxy).mp hA) with h1 | ⟨d, hd, b, hb, hc, hspan, hcrit⟩
      · exfalso
        have hu := (Nat.card_eq_one_iff_unique.mp h1).1
        have : (⟨x, hx⟩ : A) = ⟨y, hy⟩ := hu.elim _ _
        exact hxy (congrArg Subtype.val this)
      · exact ⟨Nat.card A, d, b, e, hd, hb, hspan, hcrit, fun i j => hc i j⟩
  · rintro ⟨hfin, hsub | ⟨s, d, b, f, hd, hb, hspan, hcrit, hdist⟩⟩
    · exact isRamsey_of_subsingleton hsub
    · by_cases hsub : A.Subsingleton
      · exact isRamsey_of_subsingleton hsub
      obtain ⟨x, hx, y, hy, hxy⟩ : ∃ x ∈ A, ∃ y ∈ A, x ≠ y := by simpa [Set.Subsingleton] using hsub
      have ha : Function.Injective (fun i => (f i : EuclideanSpace ℝ (Fin n))) :=
        fun i j hij => f.injective (Subtype.ext hij)
      have hpos : 0 < s := by
        rcases Nat.eq_zero_or_pos s with rfl | h
        · exact (f.symm ⟨x, hx⟩).elim0
        · exact h
      refine (isRamsey_iff_oai hfin f hx hy hxy).mpr ?_
      exact (OAI.EuclideanRamsey.classification_nonempty _ hpos ha).mpr
        (Or.inr ⟨d, hd, b, hb, fun i j => hdist i j, hspan, hcrit⟩)

/-- Non-vacuity: OpenAI's twelve-point witness is not in the answer set. -/
theorem witness_not_mem_criterionAnswer : OAI.GrahamSpherical.witness ∉ criterionAnswer 2 := by
  intro h
  rw [← erdos_174_criterion] at h
  exact OAI.GrahamSpherical.full_main.2.2.2 (isRamsey_witness_oai h)

end Erdos174
