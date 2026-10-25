import OAI.Geometry.HeilbronnTriangle.Main

/-!
# Every sufficiently large `n` (erdos cron seat, 2026-10-22, 15:00Z)

OpenAI's formalization (`OAI.Problem355.heilbronn_power_lower_bound`) proves the Heilbronn power lower bound along an
UNBOUNDED SEQUENCE of sizes `n`, with exponent `1/(100000·k)`; its scope note says "the paper's statement for every
sufficiently large n is broader". This file proves the paper's Theorem 1.1 as stated — every sufficiently large `n` —
with the paper's own exponent `η = 2/(45435k+16)` (§8, display (8.6)), from OpenAI's per-prime construction.

Route = the paper's §8 interpolation. OpenAI's `PrimeParameterData` keeps BOTH sides of its two Bertrand windows
(`100k²r³⁰ < B ≤ 200k²r³⁰`, `h¹⁰⁰ < q ≤ 2h¹⁰⁰`), so `a_r = r·√(N³/τ)` satisfies `r^α ≤ a_r ≤ √U·r^α` with
`α = 45435k + 16`. For large `n`, take the least `m` with `n ≤ m^α` and a Bertrand prime `r ∈ (m, 2m]`; OpenAI's
construction at `r` gives `⌊a_r⌋ ≥ n` points with every triangle `≥ τ/(16N³) = r²/(16a_r²)`; keep any `n` of them.

The mathematics is OpenAI's; the extraction of the per-prime statement from `Main.lean`'s proof, the two-sided growth
bounds and the interpolation are ours.
-/

namespace OAI

noncomputable section

attribute [local irreducible] Problem355.heilbronnT Problem355.heilbronnM

namespace Problem355.EveryN

open Parameters

/-- OpenAI's construction at a single large prime, extracted from the proof of
`OAI.Problem355.heilbronn_power_lower_bound` in `Main.lean` (same point law, same constants `8` and `Ct`). -/
theorem configuration_at_large_prime :
    ∃ r0 : ℕ, ∀ r : ℕ, r0 ≤ r → r.Prime → ∀ D : PrimeParameterData heilbronnK r,
      ∃ P : Finset Point, P.card = D.sampleCard ∧ pointsInUnitSquare P ∧
        triangleAreasAtLeast P (D.tau / (16 * (D.N : ℝ) ^ 3)) := by
  let Ct : ℝ := (128 / 7 : ℝ) * UniformFixedFiberCount.countConstant
  have hCt : 0 ≤ Ct :=
    mul_nonneg (by norm_num) UniformFixedFiberCount.countConstant_nonneg
  obtain ⟨r1, hr1⟩ := exists_nat_gt
    (4 * 8 + 24 * Ct * (31620 * (heilbronnK : ℝ) + 1) ^ 2)
  refine ⟨r1, fun r hr hp D => ?_⟩
  let : Fact r.Prime := ⟨hp⟩
  let : Fact D.q.Prime := ⟨D.auxiliary_prime⟩
  refine ParameterSampling.configuration_of_law D (ActualPointLaw.pointLaw D)
    (Cp := 8) (Ct := Ct) (by norm_num) hCt ?_ (ActualPointLaw.pairProbability_le D) ?_
  · exact hr1.trans_le (by exact_mod_cast hr)
  · exact ActualPointLaw.tripleProbability_le_of_count D
      UniformFixedFiberCount.countConstant_nonneg
      (fun A => ActualPointLaw.weightedFiberBound_of_matrix_count
        UniformFixedFiberCount.countConstant
        @UniformFixedFiberCount.matrix_fiber_le D A)


end Problem355.EveryN
end
end OAI
