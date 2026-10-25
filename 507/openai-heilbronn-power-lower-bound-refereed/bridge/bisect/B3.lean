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


/-- `r^α ≤ 4^α · n` when `r ≤ 2m`, `2 ≤ m` and `(m-1)^α ≤ n`. -/
lemma pow_le_four_pow_mul {α m r n : ℕ} (hm : 2 ≤ m) (hr : r ≤ 2 * m) (hn : (m - 1) ^ α ≤ n) :
    r ^ α ≤ 4 ^ α * n := by
  have h1 : m ≤ 2 * (m - 1) := by omega
  calc r ^ α ≤ (2 * m) ^ α := Nat.pow_le_pow_left hr α
    _ ≤ (2 * (2 * (m - 1))) ^ α := Nat.pow_le_pow_left (by omega) α
    _ = 4 ^ α * (m - 1) ^ α := by rw [← mul_pow]; ring_nf
    _ ≤ 4 ^ α * n := Nat.mul_le_mul_left _ hn

/-- The interpolation step for a general `k ≥ 2`: from OpenAI-style configurations at every large prime, every
sufficiently large `n` gets `n` points with all triangles `≥ c·n^(-2+2/α)`, `α = 45435k+16`. -/
theorem every_large_n_of {k : ℕ} (hk : 2 ≤ k)
    (hcfg : ∃ r0 : ℕ, ∀ r : ℕ, r0 ≤ r → r.Prime → ∀ D : PrimeParameterData k r,
      ∃ P : Finset Point, P.card = D.sampleCard ∧ pointsInUnitSquare P ∧
        triangleAreasAtLeast P (D.tau / (16 * (D.N : ℝ) ^ 3))) :
    ∃ c : ℝ, 0 < c ∧ ∃ n0 : ℕ, 3 ≤ n0 ∧ ∀ n : ℕ, n0 ≤ n →
      ∃ P : Finset Point, P.card = n ∧ pointsInUnitSquare P ∧
        triangleAreasAtLeast P
          (c * Real.rpow (n : ℝ) (-2 + 2 / (alphaOf k : ℝ))) := by
  classical
  obtain ⟨r0, hcfg⟩ := hcfg
  have hα : 0 < alphaOf k := alphaOf_pos k
  have hU : 0 < Real.sqrt (upperConst k) :=
    Real.sqrt_pos.2 (by exact_mod_cast upperConst_pos (by omega))
  have hlow : ∀ r (D : PrimeParameterData k r), r ^ alphaOf k ≤ D.sampleCard :=
    fun r D => pow_alpha_le_sampleCard D
  have hup : ∀ r (D : PrimeParameterData k r),
      aReal D ≤ Real.sqrt (upperConst k) * (r : ℝ) ^ alphaOf k := fun r D => aReal_le D
  have hlowR : ∀ r (D : PrimeParameterData k r), (r : ℝ) ^ alphaOf k ≤ aReal D :=
    fun r D => rpow_alpha_le_aReal D
  generalize alphaOf k = α at hα hlow hup hlowR ⊢
  generalize Real.sqrt (upperConst k) = U at hU hup
  obtain ⟨R0, hR0⟩ : ∃ R0 : ℕ, R0 = max r0 (400 * k ^ 2) + 2 := ⟨_, rfl⟩
  have hR0two : 2 ≤ R0 := by omega
  have hR0pow : R0 ≤ R0 ^ α := Nat.le_self_pow (by omega) R0
  refine ⟨1 / (16 * (U * 4 ^ α) ^ 2), by positivity, R0 ^ α + 1, by omega, ?_⟩
  intro n hn
  have hn1 : 1 ≤ n := by omega
  have hex : ∃ m, n ≤ m ^ α := ⟨n, Nat.le_self_pow (by omega) n⟩
  obtain ⟨m, hmdef⟩ : ∃ m, m = Nat.find hex := ⟨_, rfl⟩
  have hm : n ≤ m ^ α := hmdef ▸ Nat.find_spec hex
  have hmR : R0 < m := by
    by_contra h
    push_neg at h
    have : m ^ α ≤ R0 ^ α := Nat.pow_le_pow_left h α
    omega
  have hm_min : (m - 1) ^ α ≤ n := by
    have := Nat.find_min hex (show m - 1 < Nat.find hex by omega)
    push_neg at this
    exact this.le
  obtain ⟨r, hrp, hmr, hr2m⟩ := Nat.exists_prime_lt_and_le_two_mul m (by omega)
  have hr400 : 400 * k ^ 2 ≤ r := by omega
  have hr0 : r0 ≤ r := by omega
  let D : PrimeParameterData k r := Classical.choice (exists_primeParameterData hk hr400)
  obtain ⟨P, hcard, hsq, harea⟩ := hcfg r hr0 hrp D
  have hS : n ≤ P.card := by
    rw [hcard]
    calc n ≤ m ^ α := hm
      _ ≤ r ^ α := Nat.pow_le_pow_left hmr.le α
      _ ≤ D.sampleCard := hlow r D
  obtain ⟨Q, hQP, hQcard⟩ := Finset.exists_subset_card_eq hS
  refine ⟨Q, hQcard, fun p hp => hsq p (hQP hp), ?_⟩
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn1
  have hrR : (0 : ℝ) < r := by exact_mod_cast D.r_pos
  have ha_pos : 0 < aReal D := lt_of_lt_of_le (by positivity) (hlowR r D)
  have hr4 : ((r : ℝ) ^ α) ≤ (4 : ℝ) ^ α * n := by
    exact_mod_cast pow_le_four_pow_mul (by omega) hr2m hm_min
  have ha_le : aReal D ≤ U * 4 ^ α * n := by
    calc aReal D ≤ U * (r : ℝ) ^ α := hup r D
      _ ≤ U * ((4 : ℝ) ^ α * n) := by gcongr
      _ = U * 4 ^ α * n := by ring
  have hnr : (n : ℝ) ≤ (r : ℝ) ^ α := by
    exact_mod_cast hm.trans (Nat.pow_le_pow_left hmr.le α)
  have hαR : (0 : ℝ) < α := by exact_mod_cast hα
  have hpow : Real.rpow (n : ℝ) (2 / (α : ℝ)) ≤ (r : ℝ) ^ 2 := by
    have h1 : Real.rpow (n : ℝ) (2 / (α : ℝ)) ≤ Real.rpow ((r : ℝ) ^ α) (2 / (α : ℝ)) :=
      Real.rpow_le_rpow hnR.le hnr (by positivity)
    have h2 : Real.rpow ((r : ℝ) ^ α) (2 / (α : ℝ)) = (r : ℝ) ^ 2 := by
      rw [Real.rpow_eq_pow, ← Real.rpow_natCast, ← Real.rpow_mul hrR.le,
        mul_div_cancel₀ _ hαR.ne']
      norm_num
    exact h1.trans h2.le
  have hsplit : Real.rpow (n : ℝ) (-2 + 2 / (α : ℝ)) =
      Real.rpow (n : ℝ) (2 / (α : ℝ)) / (n : ℝ) ^ 2 := by
    rw [Real.rpow_eq_pow, Real.rpow_eq_pow, Real.rpow_add hnR, Real.rpow_neg hnR.le]
    norm_num
    ring
  have key : 1 / (16 * (U * 4 ^ α) ^ 2) * Real.rpow (n : ℝ) (-2 + 2 / (α : ℝ)) ≤
      (D.tau : ℝ) / (16 * (D.N : ℝ) ^ 3) := by
    rw [area_eq D, hsplit]
    have hsq' : aReal D ^ 2 ≤ (U * 4 ^ α * n) ^ 2 := by gcongr
    have hden : 16 * aReal D ^ 2 ≤ 16 * ((U * 4 ^ α) ^ 2 * (n : ℝ) ^ 2) := by
      nlinarith [hsq']
    calc 1 / (16 * (U * 4 ^ α) ^ 2) * (Real.rpow (n : ℝ) (2 / (α : ℝ)) / (n : ℝ) ^ 2)
        = Real.rpow (n : ℝ) (2 / (α : ℝ)) / (16 * ((U * 4 ^ α) ^ 2 * (n : ℝ) ^ 2)) := by
          field_simp
      _ ≤ (r : ℝ) ^ 2 / (16 * aReal D ^ 2) :=
          div_le_div₀ (by positivity) hpow (by positivity) hden
  intro p hp q hq s hs hpq hps hqs
  exact key.trans (harea p (hQP hp) q (hQP hq) s (hQP hs) hpq hps hqs)


end Problem355.EveryN
end
end OAI
