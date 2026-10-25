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

/-- The growth exponent of the sample size, `α = 45435k + 16` (paper (8.5)). -/
def alphaOf (k : ℕ) : ℕ := 45435 * k + 16

/-- The constant in the upper growth bound: `3·2³⁰·(200k²)^(3029k+1)`. -/
def upperConst (k : ℕ) : ℕ := 3 * 2 ^ 30 * (200 * k ^ 2) ^ (3029 * k + 1)

lemma alphaOf_pos (k : ℕ) : 0 < alphaOf k := by unfold alphaOf; omega

lemma upperConst_pos {k : ℕ} (hk : 0 < k) : 0 < upperConst k := by
  unfold upperConst; positivity

variable {k r : ℕ} (D : PrimeParameterData k r)

lemma k_pos (D : PrimeParameterData k r) : 0 < k := by have := D.two_le_k; omega

/-- `h¹⁰¹ ≤ M` (from `h¹⁰⁰ < q`). -/
lemma pow101_le_M : D.h ^ 101 ≤ D.M := by
  have hq : D.h ^ 100 ≤ D.q := le_of_lt D.auxiliary_lower
  calc D.h ^ 101 = D.h * D.h ^ 100 := by ring
    _ ≤ D.h * D.q := Nat.mul_le_mul_left _ hq
    _ = D.M := rfl

/-- `M ≤ 2·h¹⁰¹` (from `q ≤ 2h¹⁰⁰`). -/
lemma M_le_two_pow101 : D.M ≤ 2 * D.h ^ 101 := by
  have hq : D.q ≤ 2 * D.h ^ 100 := D.auxiliary_upper
  calc D.M = D.h * D.q := rfl
    _ ≤ D.h * (2 * D.h ^ 100) := Nat.mul_le_mul_left _ hq
    _ = 2 * D.h ^ 101 := by ring

lemma r30_le_B : r ^ 30 ≤ D.B := by
  have h := D.base_lower
  have hk : 1 ≤ k ^ 2 := Nat.one_le_pow _ _ (k_pos D)
  have : r ^ 30 ≤ 100 * k ^ 2 * r ^ 30 := by
    calc r ^ 30 = 1 * 1 * r ^ 30 := by ring
      _ ≤ 100 * k ^ 2 * r ^ 30 := by gcongr; norm_num
  omega

lemma h_pow_eq : D.h ^ 3030 = D.B ^ (k - 1) * D.B ^ (3029 * k + 1) := by
  have hk := k_pos D
  unfold PrimeParameterData.h
  rw [← pow_mul, ← pow_add]
  congr 1
  omega

lemma two_alpha : 2 * alphaOf k = 2 + 30 * (3029 * k + 1) := by unfold alphaOf; ring

/-- Lower growth, integer form: `τ · r^(2α) ≤ r² · M³⁰`. -/
lemma lower_nat : D.tau * r ^ (2 * alphaOf k) ≤ r ^ 2 * D.M ^ 30 := by
  have hτ : D.tau ≤ D.B ^ (k - 1) := by
    unfold PrimeParameterData.tau threshold; exact Nat.div_le_self _ _
  have hrB : r ^ (30 * (3029 * k + 1)) ≤ D.B ^ (3029 * k + 1) := by
    rw [pow_mul]; exact Nat.pow_le_pow_left (r30_le_B D) _
  have hM : D.h ^ 3030 ≤ D.M ^ 30 := by
    calc D.h ^ 3030 = (D.h ^ 101) ^ 30 := by rw [← pow_mul]
      _ ≤ D.M ^ 30 := Nat.pow_le_pow_left (pow101_le_M D) _
  calc D.tau * r ^ (2 * alphaOf k)
      = r ^ 2 * (D.tau * r ^ (30 * (3029 * k + 1))) := by rw [two_alpha, pow_add]; ring
    _ ≤ r ^ 2 * (D.B ^ (k - 1) * D.B ^ (3029 * k + 1)) := by gcongr
    _ = r ^ 2 * D.h ^ 3030 := by rw [h_pow_eq D]
    _ ≤ r ^ 2 * D.M ^ 30 := by gcongr

/-- Upper growth, integer form: `r² · M³⁰ ≤ U · τ · r^(2α)`, `U = 3·2³⁰·(200k²)^(3029k+1)`. -/
lemma upper_nat : r ^ 2 * D.M ^ 30 ≤ upperConst k * D.tau * r ^ (2 * alphaOf k) := by
  have hB3 : 3 ≤ D.B := D.base_ge_three
  have h3τ : D.B ^ (k - 1) ≤ 3 * D.tau := by
    unfold PrimeParameterData.tau; exact previous_power_le_three_threshold hB3 D.two_le_k
  have hBup : D.B ^ (3029 * k + 1) ≤
      (200 * k ^ 2) ^ (3029 * k + 1) * r ^ (30 * (3029 * k + 1)) := by
    rw [pow_mul, ← mul_pow]; exact Nat.pow_le_pow_left D.base_upper _
  have hM : D.M ^ 30 ≤ 2 ^ 30 * D.h ^ 3030 := by
    calc D.M ^ 30 ≤ (2 * D.h ^ 101) ^ 30 := Nat.pow_le_pow_left (M_le_two_pow101 D) _
      _ = 2 ^ 30 * D.h ^ 3030 := by rw [mul_pow, ← pow_mul]
  calc r ^ 2 * D.M ^ 30
      ≤ r ^ 2 * (2 ^ 30 * D.h ^ 3030) := by gcongr
    _ = r ^ 2 * (2 ^ 30 * (D.B ^ (k - 1) * D.B ^ (3029 * k + 1))) := by rw [h_pow_eq D]
    _ ≤ r ^ 2 * (2 ^ 30 * ((3 * D.tau) *
          ((200 * k ^ 2) ^ (3029 * k + 1) * r ^ (30 * (3029 * k + 1))))) := by gcongr
    _ = upperConst k * D.tau * r ^ (2 * alphaOf k) := by
        unfold upperConst; rw [two_alpha, pow_add]; ring

/-- The real number whose floor is `sampleCard`. -/
def aReal : ℝ := (r : ℝ) * Real.sqrt ((D.N : ℝ) ^ 3 / (D.tau : ℝ))

lemma aReal_nonneg : 0 ≤ aReal D := by unfold aReal; positivity

lemma aReal_sq : aReal D ^ 2 = (r : ℝ) ^ 2 * (D.M : ℝ) ^ 30 / (D.tau : ℝ) := by
  have hτ : (0 : ℝ) < D.tau := by exact_mod_cast D.tau_pos
  unfold aReal
  rw [mul_pow, Real.sq_sqrt (by positivity)]
  unfold PrimeParameterData.N
  push_cast
  ring

lemma tau_real_pos : (0 : ℝ) < D.tau := by exact_mod_cast D.tau_pos

/-- Lower growth: `r^α ≤ a`. -/
lemma rpow_alpha_le_aReal : (r : ℝ) ^ alphaOf k ≤ aReal D := by
  have hτ := tau_real_pos D
  have hsq : ((r : ℝ) ^ alphaOf k) ^ 2 ≤ aReal D ^ 2 := by
    rw [aReal_sq, le_div_iff₀ hτ, ← pow_mul, mul_comm (alphaOf k) 2, mul_comm]
    exact_mod_cast lower_nat D
  exact (pow_le_pow_iff_left₀ (by positivity) (aReal_nonneg D) two_ne_zero).1 hsq

/-- Upper growth: `a ≤ √U · r^α`. -/
lemma aReal_le : aReal D ≤ Real.sqrt (upperConst k) * (r : ℝ) ^ alphaOf k := by
  have hτ := tau_real_pos D
  have hsq : aReal D ^ 2 ≤ (Real.sqrt (upperConst k) * (r : ℝ) ^ alphaOf k) ^ 2 := by
    rw [aReal_sq, div_le_iff₀ hτ, mul_pow, Real.sq_sqrt (by positivity), ← pow_mul,
      mul_comm (alphaOf k) 2]
    have := upper_nat D
    calc (r : ℝ) ^ 2 * (D.M : ℝ) ^ 30 ≤ (upperConst k : ℝ) * D.tau * (r : ℝ) ^ (2 * alphaOf k) := by
          exact_mod_cast this
      _ = (upperConst k : ℝ) * (r : ℝ) ^ (2 * alphaOf k) * D.tau := by ring
  exact (pow_le_pow_iff_left₀ (aReal_nonneg D) (by positivity) two_ne_zero).1 hsq

/-- `sampleCard ≥ r^α`. -/
lemma pow_alpha_le_sampleCard : r ^ alphaOf k ≤ D.sampleCard := by
  unfold PrimeParameterData.sampleCard
  apply Nat.le_floor
  push_cast
  exact rpow_alpha_le_aReal D

/-- The minimum-area bound of the construction, rewritten: `τ/(16N³) = r²/(16a²)`. -/
lemma area_eq : (D.tau : ℝ) / (16 * (D.N : ℝ) ^ 3) = (r : ℝ) ^ 2 / (16 * aReal D ^ 2) := by
  have hτ := tau_real_pos D
  have hN : (0 : ℝ) < D.N := by exact_mod_cast D.N_pos
  have hr : (0 : ℝ) < r := by exact_mod_cast D.r_pos
  rw [aReal_sq]
  unfold PrimeParameterData.N
  push_cast
  have hM : (0 : ℝ) < D.M := by exact_mod_cast D.M_pos
  field_simp
  ring



end Problem355.EveryN
end
end OAI
