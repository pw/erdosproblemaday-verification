-- MUTANT (must FAIL to compile): F with 1 ∉ S instead of 0 ∉ S
import Mathlib
import OAI.NumberTheory.EgyptianFractions.Main

/-!
# Bridges: OpenAI's `OAI.Problem337` theorems ⟹ Erdős #148 and #293 in Formal Conjectures' language

* `Erdos148.F` is a verbatim copy of `F` in `FormalConjectures/ErdosProblems/148.lean` at
  google-deepmind/formal-conjectures@2a315101 (21 Oct 2026). FC's `erdos_148` is a `research open` value question
  (`=Θ[atTop] erdos_148.answer`, answer sorried); `erdos_148.variants.double_log_order` below is OUR statement of what
  OpenAI's Corollary 1.2 settles: `log log F(k) ≍ k`.
* Formal Conjectures has no file for #293 (erdosproblems.com/293: "Formalised statement? No"). `Erdos293.v` and the
  two theorems about it are OUR proposed formalisation in FC's style (denominators as a `Finset ℕ` with `0 ∉ S`, as in
  FC's #148), proved from OpenAI's Corollary 1.3.
The proofs are ours (erdos cron seat, 2026-10-21); the mathematics is OpenAI's, used as a black box.
-/

open Filter Real

namespace EgyptianBridge

/-- A strictly increasing `n : Fin k → ℕ` with positive values and reciprocal sum `1`, read as a finite set. -/
theorem image_of_oneExpansion {k : ℕ} (n : Fin k → ℕ) (hn : OAI.Problem337.IsOneExpansion n) :
    (Finset.univ.image n).card = k ∧ 0 ∉ Finset.univ.image n ∧
      ∑ x ∈ Finset.univ.image n, (1 : ℚ) / x = 1 := by
  obtain ⟨h1, hmono, hsum⟩ := hn
  refine ⟨?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hmono.injective, Finset.card_univ, Fintype.card_fin]
  · intro h0
    obtain ⟨i, -, hi⟩ := Finset.mem_image.mp h0
    have := h1 i
    omega
  · rw [Finset.sum_image (fun x _ y _ hxy => hmono.injective hxy)]
    exact hsum

/-- Conversely a finite set of positive integers with reciprocal sum `1`, enumerated increasingly. -/
theorem oneExpansion_of_finset {k : ℕ} (S : Finset ℕ) (hcard : S.card = k) (h0 : 0 ∉ S)
    (hsum : ∑ x ∈ S, (1 : ℚ) / x = 1) : OAI.Problem337.IsOneExpansion (S.orderEmbOfFin hcard) := by
  refine ⟨?_, (S.orderEmbOfFin hcard).strictMono, ?_⟩
  · intro i
    have hmem := Finset.orderEmbOfFin_mem S hcard i
    rcases Nat.eq_zero_or_pos (S.orderEmbOfFin hcard i) with h | h
    · rw [h] at hmem
      exact absurd hmem h0
    · exact h
  · have himg := Finset.image_orderEmbOfFin_univ S hcard
    rw [← himg, Finset.sum_image (fun x _ y _ hxy => (S.orderEmbOfFin hcard).injective hxy)] at hsum
    exact hsum

end EgyptianBridge

namespace Erdos148

noncomputable def F (k : ℕ) : ℕ :=
  {S : Finset ℕ | S.card = k ∧ 1 ∉ S ∧ ∑ n ∈ S, (1 : ℚ) / n = 1}.ncard

/-- FC's `F` (sets) is OpenAI's `F` (strictly increasing tuples). -/
theorem F_eq_oai (k : ℕ) : F k = OAI.Problem337.F k := by
  unfold F OAI.Problem337.F OAI.Problem337.OneExpansions
  symm
  refine Set.ncard_congr (fun n _ => Finset.univ.image n) ?_ ?_ ?_
  · intro n hn
    exact EgyptianBridge.image_of_oneExpansion n hn
  · intro n m hn hm heq
    have hc : (Finset.univ.image m).card = k := (EgyptianBridge.image_of_oneExpansion m hm).1
    have e1 : n = (Finset.univ.image m).orderEmbOfFin hc :=
      Finset.orderEmbOfFin_unique hc
        (fun x => by
          have hx : n x ∈ Finset.univ.image n := Finset.mem_image_of_mem n (Finset.mem_univ x)
          rw [heq] at hx
          exact hx) hn.2.1
    have e2 : m = (Finset.univ.image m).orderEmbOfFin hc :=
      Finset.orderEmbOfFin_unique hc (fun x => Finset.mem_image_of_mem m (Finset.mem_univ x)) hm.2.1
    exact e1.trans e2.symm
  · rintro S ⟨hcard, h0, hsum⟩
    exact ⟨S.orderEmbOfFin hcard, EgyptianBridge.oneExpansion_of_finset S hcard h0 hsum,
      Finset.image_orderEmbOfFin_univ S hcard⟩

/-- Erdős Problem 148 (our variant statement): the number `F k` of `k`-term distinct Egyptian-fraction
representations of `1` satisfies `log log F(k) ≍ k` (OpenAI, *Short Egyptian fractions*, Corollary 1.2). -/
theorem erdos_148.variants.double_log_order :
    (fun k : ℕ => Real.log (Real.log (F k : ℝ))) =Θ[atTop] (fun k : ℕ => (k : ℝ)) := by
  obtain ⟨c, C, hc, hC, k0, h⟩ := OAI.Problem337.counting_double_log_order
  simp only [F_eq_oai]
  refine ⟨Asymptotics.IsBigO.of_bound C ?_, Asymptotics.IsBigO.of_bound (1 / c) ?_⟩
  · filter_upwards [eventually_ge_atTop k0] with k hk
    obtain ⟨h1, h2⟩ := h k hk
    have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
    have hLL : 0 ≤ Real.log (Real.log (OAI.Problem337.F k : ℝ)) := le_trans (by positivity) h1
    rw [Real.norm_of_nonneg hLL, Real.norm_of_nonneg hk0]
    exact h2
  · filter_upwards [eventually_ge_atTop k0] with k hk
    obtain ⟨h1, h2⟩ := h k hk
    have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
    have hLL : 0 ≤ Real.log (Real.log (OAI.Problem337.F k : ℝ)) := le_trans (by positivity) h1
    rw [Real.norm_of_nonneg hLL, Real.norm_of_nonneg hk0, one_div, ← div_eq_inv_mul, le_div_iff₀ hc]
    linarith

end Erdos148

namespace Erdos293

/-- `v k` is the least integer `m ≥ 2` that is not a denominator in any representation
`1 = 1/n_1 + ⋯ + 1/n_k` with `1 ≤ n_1 < ⋯ < n_k` (erdosproblems.com/293, [ErGr80, p. 35]). -/
noncomputable def v (k : ℕ) : ℕ :=
  sInf {m : ℕ | 2 ≤ m ∧ ∀ S : Finset ℕ, S.card = k → 0 ∉ S → ∑ n ∈ S, (1 : ℚ) / n = 1 → m ∉ S}

theorem v_eq_oai (k : ℕ) : v k = OAI.Problem337.v k := by
  unfold v OAI.Problem337.v
  congr 1
  ext m
  simp only [OAI.Problem337.missingDenominators, OAI.Problem337.D, Set.mem_ofPred_eq, Set.mem_sdiff]
  constructor
  · rintro ⟨hm, hS⟩
    refine ⟨hm, ?_⟩
    rintro ⟨-, n, hn, i, rfl⟩
    obtain ⟨hc, h0, hs⟩ := EgyptianBridge.image_of_oneExpansion n hn
    exact hS _ hc h0 hs (Finset.mem_image_of_mem n (Finset.mem_univ i))
  · rintro ⟨hm, hnot⟩
    refine ⟨hm, fun S hcard h0 hsum hmS => hnot ⟨hm, S.orderEmbOfFin hcard,
      EgyptianBridge.oneExpansion_of_finset S hcard h0 hsum, ?_⟩⟩
    have hr : m ∈ Set.range (S.orderEmbOfFin hcard) := by
      rw [Finset.range_orderEmbOfFin]
      exact hmS
    obtain ⟨i, hi⟩ := hr
    exact ⟨i, hi⟩

/-- Erdős Problem 293 (our statement), explicit form: for all large `k`,
`exp (exp (k / 600)) ≤ v k ≤ 1 + k ^ (2 ^ (k - 1))` (OpenAI, Corollary 1.3). -/
theorem erdos_293.variants.explicit_bounds :
    ∀ᶠ k : ℕ in atTop, Real.exp (Real.exp ((k : ℝ) / 600)) ≤ (v k : ℝ) ∧ v k ≤ 1 + k ^ (2 ^ (k - 1)) := by
  obtain ⟨⟨k0, h⟩, -, -⟩ := OAI.Problem337.prescribed_denominator_corollary
  filter_upwards [eventually_ge_atTop k0] with k hk
  rw [v_eq_oai]
  exact h k hk

/-- Erdős Problem 293 (our statement): `log log v(k) ≍ k`, i.e. `v(k)` grows doubly exponentially in `k`. -/
theorem erdos_293.variants.double_log_order :
    (fun k : ℕ => Real.log (Real.log (v k : ℝ))) =Θ[atTop] (fun k : ℕ => (k : ℝ)) := by
  obtain ⟨⟨k0, h⟩, -, -⟩ := OAI.Problem337.prescribed_denominator_corollary
  simp only [v_eq_oai]
  -- lower: log log v ≥ k / 600 eventually
  have hlow : ∀ k : ℕ, k0 ≤ k → (k : ℝ) / 600 ≤ Real.log (Real.log (OAI.Problem337.v k : ℝ)) := by
    intro k hk
    have h1 := (h k hk).1
    have hpos : 0 < Real.exp (Real.exp ((k : ℝ) / 600)) := Real.exp_pos _
    have e1 : Real.exp ((k : ℝ) / 600) ≤ Real.log (OAI.Problem337.v k : ℝ) := by
      have := Real.log_le_log hpos h1
      rwa [Real.log_exp] at this
    have e2 := Real.log_le_log (Real.exp_pos _) e1
    rwa [Real.log_exp] at e2
  -- upper: v ≤ 2 ^ (4 ^ k) for k ≥ 1, so log log v ≤ k log 4 + log log 2 ≤ 2 k
  have hnat : ∀ k : ℕ, 1 ≤ k → 1 + k ^ (2 ^ (k - 1)) ≤ 2 ^ (4 ^ k) := by
    intro k hk1
    have hk2 : k ≤ 2 ^ k := (Nat.lt_two_pow_self).le
    have a1 : k ^ (2 ^ (k - 1)) ≤ 2 ^ (k * 2 ^ (k - 1)) := by
      rw [pow_mul]
      exact Nat.pow_le_pow_left hk2 _
    have a2 : 1 + 2 ^ (k * 2 ^ (k - 1)) ≤ 2 ^ (k * 2 ^ (k - 1) + 1) := by
      rw [pow_succ]
      have : 1 ≤ 2 ^ (k * 2 ^ (k - 1)) := Nat.one_le_two_pow
      omega
    have a3 : k * 2 ^ (k - 1) + 1 ≤ 4 ^ k := by
      have e : 2 ^ k = 2 * 2 ^ (k - 1) := by
        rw [← pow_succ']
        congr 1
        omega
      have h4 : (4 : ℕ) ^ k = 2 ^ k * 2 ^ k := by
        rw [← mul_pow]
        norm_num
      have hp : 1 ≤ 2 ^ (k - 1) := Nat.one_le_two_pow
      rw [h4]
      nlinarith
    calc 1 + k ^ (2 ^ (k - 1)) ≤ 1 + 2 ^ (k * 2 ^ (k - 1)) := by omega
      _ ≤ 2 ^ (k * 2 ^ (k - 1) + 1) := a2
      _ ≤ 2 ^ (4 ^ k) := Nat.pow_le_pow_right (by norm_num) a3
  have hup : ∀ k : ℕ, max k0 1 ≤ k → Real.log (Real.log (OAI.Problem337.v k : ℝ)) ≤ 2 * (k : ℝ) := by
    intro k hk
    have hk0 : k0 ≤ k := le_trans (le_max_left _ _) hk
    have hk1 : 1 ≤ k := le_trans (le_max_right _ _) hk
    have hv2 : 2 ≤ OAI.Problem337.v k := (OAI.Problem337.missing_denominator_semantics k).2.2.1
    have hvle : OAI.Problem337.v k ≤ 2 ^ (4 ^ k) := le_trans (h k hk0).2 (hnat k hk1)
    have hvR : (OAI.Problem337.v k : ℝ) ≤ (2 : ℝ) ^ (4 ^ k) := by exact_mod_cast hvle
    have hv2R : (2 : ℝ) ≤ (OAI.Problem337.v k : ℝ) := by exact_mod_cast hv2
    have hlogv_pos : 0 < Real.log (OAI.Problem337.v k : ℝ) := Real.log_pos (by linarith)
    have l1 : Real.log (OAI.Problem337.v k : ℝ) ≤ (4 : ℝ) ^ k := by
      have := Real.log_le_log (by linarith) hvR
      rw [Real.log_pow] at this
      have hl2 : Real.log 2 < 1 := by
        have := Real.log_two_lt_d9
        linarith
      have h4pos : (0 : ℝ) < ((4 ^ k : ℕ) : ℝ) := by positivity
      calc Real.log (OAI.Problem337.v k : ℝ) ≤ ((4 ^ k : ℕ) : ℝ) * Real.log 2 := this
        _ ≤ ((4 ^ k : ℕ) : ℝ) * 1 := by gcongr
        _ = (4 : ℝ) ^ k := by push_cast; ring
    have l2 := Real.log_le_log hlogv_pos l1
    rw [Real.log_pow] at l2
    have hl4 : Real.log 4 < 2 := by
      have : Real.log 4 = 2 * Real.log 2 := by
        rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
        norm_num
      rw [this]
      have := Real.log_two_lt_d9
      linarith
    have hk0R : (0 : ℝ) ≤ k := Nat.cast_nonneg k
    nlinarith
  refine ⟨Asymptotics.IsBigO.of_bound 2 ?_, Asymptotics.IsBigO.of_bound 600 ?_⟩
  · filter_upwards [eventually_ge_atTop (max k0 1)] with k hk
    have hk0 : k0 ≤ k := le_trans (le_max_left _ _) hk
    have hLL : 0 ≤ Real.log (Real.log (OAI.Problem337.v k : ℝ)) :=
      le_trans (by positivity) (hlow k hk0)
    rw [Real.norm_of_nonneg hLL, Real.norm_of_nonneg (Nat.cast_nonneg k)]
    exact hup k hk
  · filter_upwards [eventually_ge_atTop k0] with k hk
    have hLL : 0 ≤ Real.log (Real.log (OAI.Problem337.v k : ℝ)) := le_trans (by positivity) (hlow k hk)
    rw [Real.norm_of_nonneg hLL, Real.norm_of_nonneg (Nat.cast_nonneg k)]
    have := hlow k hk
    linarith

end Erdos293
