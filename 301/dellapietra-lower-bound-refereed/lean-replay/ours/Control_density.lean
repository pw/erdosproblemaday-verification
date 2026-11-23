import Erdos301

/-!
# Our own statement bridge for Erdős #301 (erdosproblemaday.com audit, 2026-11-23)

`OursFree` is written from scratch in our own words. It does not mention the
author's `Relation`, `Relation.Inside`, `Admissible`, `upto` or `reciprocal`.
`ours_lower` is stated with Mathlib primitives only, so a reader can check its
meaning without reading the author's definitions; it is then *derived* from the
author's theorem `Erdos301.Analytic.erdos301Conclusion_unconditional`.
-/

namespace EPAD301

/-- `A` is #301-free: there is no `a ∈ A` and no set `B ⊆ A` with `a ∉ B`,
`|B| ≥ 2` and `1/a = Σ_{b ∈ B} 1/b`, computed in exact rationals. (A finset
`B` has pairwise distinct elements; `a ∉ B` makes `a` distinct from all of them.) -/
def OursFree (A : Finset ℕ) : Prop :=
  ∀ (a : ℕ) (B : Finset ℕ), a ∈ A → B ⊆ A → a ∉ B → 2 ≤ B.card →
    (1 : ℚ) / a ≠ ∑ b ∈ B, (1 : ℚ) / b

/-- The author's admissibility implies ours, for sets of positive integers. -/
theorem oursFree_of_admissible {A : Finset ℕ} (hpos : ∀ n ∈ A, 1 ≤ n)
    (hA : Erdos301.Admissible A) : OursFree A := by
  intro a B ha hB haB hcard heq
  have hsum : ∑ i : Fin B.card, (((B.equivFin.symm i : B) : ℕ) : ℚ)⁻¹
      = ∑ b ∈ B, (1 : ℚ) / b := by
    calc ∑ i : Fin B.card, (((B.equivFin.symm i : B) : ℕ) : ℚ)⁻¹
        = ∑ b : B, ((b : ℕ) : ℚ)⁻¹ :=
          Equiv.sum_comp B.equivFin.symm (fun b : B => ((b : ℕ) : ℚ)⁻¹)
      _ = ∑ b ∈ B, ((b : ℕ) : ℚ)⁻¹ :=
          Finset.sum_coe_sort B (fun b : ℕ => ((b : ℕ) : ℚ)⁻¹)
      _ = ∑ b ∈ B, (1 : ℚ) / b := by simp only [one_div]
  let r : Erdos301.Relation B.card :=
    { head := a
      tail := fun i => ((B.equivFin.symm i : B) : ℕ)
      head_pos := hpos a ha
      tail_pos := fun i => hpos _ (hB (B.equivFin.symm i).2)
      head_ne_tail := fun i h => haB (by rw [h]; exact (B.equivFin.symm i).2)
      tail_injective := fun i j h => B.equivFin.symm.injective (Subtype.ext h)
      at_least_two := hcard
      equation := by
        show ((a : ℚ))⁻¹ = ∑ i : Fin B.card, (((B.equivFin.symm i : B) : ℕ) : ℚ)⁻¹
        rw [hsum, ← heq, one_div] }
  exact hA B.card r ⟨ha, fun i => hB (B.equivFin.symm i).2⟩

/-- CONTROL (must NOT compile): density `1 + ε` instead of `1/2 + ε`. False, since `|A| ≤ N`. -/
theorem ctrl_density :
    ∃ ε : ℝ, 0 < ε ∧ ∃ N₀ : ℕ, ∀ N ≥ N₀, ∃ A : Finset ℕ,
      A ⊆ Finset.Icc 1 N ∧ OursFree A ∧ ((1 : ℝ) + ε) * (N : ℝ) ≤ (A.card : ℝ) := by
  obtain ⟨ε, hε, N₀, h⟩ := Erdos301.Analytic.erdos301Conclusion_unconditional
  refine ⟨ε, hε, N₀, fun N hN => ?_⟩
  obtain ⟨A, hsub, hadm, hcard⟩ := h N hN
  have hsub' : A ⊆ Finset.Icc 1 N := hsub
  refine ⟨A, hsub', oursFree_of_admissible
    (fun n hn => (Finset.mem_Icc.mp (hsub' hn)).1) hadm, ?_⟩
  exact hcard

end EPAD301
