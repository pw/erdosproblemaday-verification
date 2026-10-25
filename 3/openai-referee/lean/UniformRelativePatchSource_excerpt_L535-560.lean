    (hlifting : ∀ τ : ℝ, 0 < τ → τ ≤ 1 / 2 →
      ∃ E : ℕ, 2 ≤ E ∧ RelativePatchPowerInductionRule (k - 2) n₀ (k - 2) τ E) :
    QuantitativeDensityBound k := by
  obtain ⟨κ, H₀, K, B, D, pmin, hκ, hgain, hK, hB, hD, hsource⟩ :=
    exists_subquadratic_patch_source_of_uniform_relative_lifting (k - 2) n₀ (by omega) hlifting
  have hresult := quantitative_density_of_patch_source (by omega : 0 < (k - 2) + 2)
    hκ hgain hK (by norm_num : (1 : ℝ) ≤ 1) (by norm_num : (1 : ℝ) < 2)
    (by norm_num : (0 : ℝ) < 1) hB hD hsource
  simpa only [Nat.sub_add_cancel (by omega : 2 ≤ k)] using hresult

theorem manuscript_targets_of_uniform_relative_lifting
    (hlifting : ∀ k : ℕ, 3 ≤ k → ∃ n₀ : ℕ, 0 < n₀ ∧
      ∀ τ : ℝ, 0 < τ → τ ≤ 1 / 2 →
        ∃ E : ℕ, 2 ≤ E ∧ RelativePatchPowerInductionRule (k - 2) n₀ (k - 2) τ E) :
    QuantitativeDensityTheorem ∧ ReciprocalProgressionTheorem := by
  have hquant : QuantitativeDensityTheorem := by
    intro k hk
    obtain ⟨n₀, hn₀, hrelative⟩ := hlifting k hk
    let : NeZero n₀ := ⟨Nat.ne_of_gt hn₀⟩
    exact quantitative_density_bound_of_uniform_relative_lifting k n₀ hk hrelative
  exact ⟨hquant, reciprocalProgressionTheorem_of_quantitativeDensityTheorem hquant⟩

end Erdos3

end

