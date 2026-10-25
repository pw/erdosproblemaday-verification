      div_le_div_of_nonneg_right hm hden.le
    _ = (C / (Real.log 2) ^ B) * ((m : ℝ) ^ B)⁻¹ := by
      field_simp

theorem QuantitativeDensityBound.summable_dyadic {k : ℕ}
    (h : QuantitativeDensityBound k) :
    Summable (fun m : ℕ ↦ (extremalNumber k (2 ^ m) : ℝ) / 2 ^ m) := by
  obtain ⟨C, _hC, htail⟩ := h.eventually_logarithmic 2
  exact summable_dyadic_of_eventually_logarithmic (by norm_num) htail

theorem hasAP_of_eventually_logarithmic_bound {k : ℕ} {C δ : ℝ} (hδ : 0 < δ)
    (hbound : ∀ᶠ N : ℕ in atTop,
      (extremalNumber k N : ℝ) ≤ C * N / (Real.log N) ^ (1 + δ))
    {A : Set ℕ} (hA : ¬ Summable (reciprocalTerm A)) : HasAP A k :=
  hasAP_of_not_summable_reciprocal
    (summable_dyadic_of_eventually_logarithmic (by linarith) hbound) hA

theorem QuantitativeDensityBound.hasAP {k : ℕ} (h : QuantitativeDensityBound k)
    {A : Set ℕ} (hA : ¬ Summable (reciprocalTerm A)) : HasAP A k :=
  hasAP_of_not_summable_reciprocal h.summable_dyadic hA

theorem reciprocalProgressionTheorem_of_quantitativeDensityTheorem
    (h : QuantitativeDensityTheorem) : ReciprocalProgressionTheorem := by
  intro A hA k
  by_cases hk : 3 ≤ k
  · exact (h k hk).hasAP hA
  · exact ((h 3 le_rfl).hasAP hA).of_le (by omega)

end Erdos3

end

section

namespace Erdos3
open Filter
