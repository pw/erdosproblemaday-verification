import OAI.Geometry.Borsuk.Main
-- CONTROL, must FAIL: FC def mutated (< → ≤); the bridge must break at the strict-inequality step (h1).

/-!
# Bridge (erdosproblemaday.com, 2026-10-20): Formal Conjectures' `Borsuk.borsuk_conjecture.not_nine`
# (and `erdos_505`) from OpenAI's `OAI.BorsukNine.euclidean_nine_counterexample`.

The two definitions below are copied VERBATIM (text and binder names) from
google-deepmind/formal-conjectures @ 14c308135590c8706ce83e40af88a65c4f8e197b,
`FormalConjectures/Wikipedia/BorsukConjecture.lean` (namespace `Borsuk`), together with the notation
`scoped[EuclideanGeometry] notation "ℝ^" n:65 => EuclideanSpace ℝ (Fin n)` from
`FormalConjecturesForMathlib/Geometry/Euclidean.lean`. Only the enclosing namespace differs (`Bridge505.Borsuk`).
FC's statement differs from OpenAI's in three ways this file has to cross: `ediam` instead of `Metric.diam`,
"smaller than the set's own diameter" instead of "< √2", and cover sets not required to lie inside the set.
-/

scoped[EuclideanGeometry] notation "ℝ^" n:65 => EuclideanSpace ℝ (Fin n)

namespace Bridge505

open Metric Bornology

open scoped EuclideanGeometry

namespace Borsuk

variable {E : Type*} [PseudoEMetricSpace E]

def HasBorsukCover (k : ℕ) (s : Set E) : Prop :=
  ∃ c : Fin k → Set E, s ⊆ ⋃ i, c i ∧ ∀ i, ediam (c i) ≤ ediam s

def BorsukConjecture (n : ℕ) : Prop :=
  ∀ s : Set (ℝ^n), IsBounded s → s.Nontrivial → HasBorsukCover (n + 1) s

/-- FC's `borsuk_conjecture.not_nine`, from OpenAI's nine-dimensional counterexample. -/
theorem borsuk_conjecture.not_nine : ¬ BorsukConjecture 9 := by
  obtain ⟨X, hXc, hXd, hno⟩ := OAI.BorsukNine.euclidean_nine_counterexample
  intro h
  have hb : IsBounded X := hXc.isBounded
  have hnt : X.Nontrivial := by
    by_contra hns
    rw [Set.not_nontrivial_iff] at hns
    have h0 := Metric.diam_subsingleton hns
    rw [hXd] at h0
    have : (0 : ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
    linarith
  obtain ⟨c, hcov, hsmall⟩ := h X hb hnt
  apply hno
  refine ⟨fun i => c i ∩ X, fun i => Set.inter_subset_right, ?_, ?_⟩
  · intro x hx
    obtain ⟨i, hi⟩ := Set.mem_iUnion.mp (hcov hx)
    exact Set.mem_iUnion.mpr ⟨i, hi, hx⟩
  · intro i
    have h1 : ediam (c i ∩ X) < ediam X :=
      lt_of_le_of_lt (ediam_mono Set.inter_subset_left) (hsmall i)
    have hXfin : ediam X ≠ ⊤ := isBounded_iff_ediam_ne_top.mp hb
    have h2 : diam (c i ∩ X) < diam X :=
      (ENNReal.toReal_lt_toReal (ne_top_of_lt h1) hXfin).mpr h1
    rw [hXd] at h2
    exact h2

/-- FC's `borsuk_conjecture.not_forall` (= the type of FC's `Erdos505.erdos_505`). -/
theorem borsuk_conjecture.not_forall : ¬ ∀ n, BorsukConjecture n :=
  fun h => borsuk_conjecture.not_nine (h 9)

/-- FC's `borsuk_conjecture` (fails somewhere in the formerly open range 4 ≤ n ≤ 62). -/
theorem borsuk_conjecture : ¬ ∀ n, 4 ≤ n → n ≤ 62 → BorsukConjecture n :=
  fun h => borsuk_conjecture.not_nine (h 9 (by norm_num) (by norm_num))

end Borsuk

end Bridge505

#print axioms Bridge505.Borsuk.borsuk_conjecture.not_nine
#print axioms Bridge505.Borsuk.borsuk_conjecture.not_forall
#print axioms Bridge505.Borsuk.borsuk_conjecture
