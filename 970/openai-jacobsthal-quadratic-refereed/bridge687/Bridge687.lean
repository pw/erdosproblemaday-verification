import Mathlib
import OAI.NumberTheory.Jacobsthal.Main

/-!
# OpenAI's Jacobsthal bound ⟹ Erdős 687: `Y(x) ≪ x² / (log x · log log x)²`
(erdos cron seat, erdosproblemaday.com, 2026-10-23)

`Green46.IsCoveredByResidues` and `Erdos687.Y` are verbatim copies of formal-conjectures
`GreensOpenProblems/46.lean` and `ErdosProblems/687.lean` at google-deepmind/formal-conjectures@c83a94d7
(docstrings and attributes removed; `verbatim_check.py` asserts the copies, and the two FC statements below).

* `lt_of_covered` — the Chinese remainder step: a cover of `[1, y]` by one class at each prime `p ≤ x`
  gives `y` consecutive integers none coprime to `x#`; so `y < m` for every admissible `m` of OpenAI's
  `IsJacobsthalBound k m` with `k ≥ π(x)`.
* `Y_isBigO` — `Y(x) ≪ x² / (log x · log log x)²`, from OpenAI's comparator-checked
  `erdos_970_iterated_log` applied at `k = ⌈2x / log x⌉ ≥ π(x)` (Mathlib's Chebyshev bound).
* FC's `erdos_687.parts.ii` (`Y(x) = o(x²)`, tagged research solved; formal proof by 30k30, from OpenAI's
  quadratic route) and `erdos_687.variants.iwaniec` (`Y(x) ≪ x²`, Iwaniec 1978) as corollaries.

The proofs here are ours; the mathematics they rest on is OpenAI's (Theorem 1.1 of
"A quadratic bound for Jacobsthal's function", 25 Sep 2026).
-/

open Filter Asymptotics

namespace Green46

/-- Verbatim from formal-conjectures `GreensOpenProblems/46.lean` (c83a94d7). -/

def IsCoveredByResidues (x y : ℕ) : Prop :=
  ∃ a : ℕ → ℕ, ∀ m ∈ Finset.Icc 1 y, ∃ p ≤ x, p.Prime ∧ m ≡ a p [MOD p]

end Green46

namespace Erdos687

/-- Verbatim from formal-conjectures `ErdosProblems/687.lean` (c83a94d7). -/
noncomputable def Y (x : ℕ) : ℕ :=
  sSup {y : ℕ | Green46.IsCoveredByResidues x y}

open OAI.Erdos970.NumberTheoryLean.Targets

/-- The Chinese remainder step: a cover of `[1, y]` by one class for each prime `p ≤ x` gives `y`
consecutive integers none coprime to `x#`; `x#` has `π x` prime factors, so any admissible
interval length `m` for some `k ≥ π x` exceeds `y`. -/
theorem lt_of_covered {x y k m : ℕ} (hc : Green46.IsCoveredByResidues x y)
    (hk : Nat.primeCounting x ≤ k) (hm : IsJacobsthalBound k m) : y < m := by
  obtain ⟨a, ha⟩ := hc
  by_contra! hmy
  have hs : ∀ p ∈ Nat.primesLE x, (fun p : ℕ => p) p ≠ 0 :=
    fun p hp => (Nat.prime_of_mem_primesLE hp).ne_zero
  have pp : ((Nat.primesLE x : Finset ℕ) : Set ℕ).Pairwise (Function.onFun Nat.Coprime fun p : ℕ => p) :=
    fun p hp q hq hpq =>
      (Nat.coprime_primes (Nat.prime_of_mem_primesLE hp) (Nat.prime_of_mem_primesLE hq)).2 hpq
  let c := Nat.chineseRemainderOfFinset (fun p => p + 1 - a p % p) (fun p => p) (Nat.primesLE x) hs pp
  have hcard : (primorial x).primeFactors.card ≤ k := by
    rw [primeFactors_primorial, Nat.primesLE_card_eq_primeCounting]; exact hk
  obtain ⟨i, him, hcop⟩ := hm (primorial x) (primorial_pos x) hcard ((c : ℕ) : ℤ)
  obtain ⟨p, hpx, hp, hpm⟩ := ha (i + 1) (Finset.mem_Icc.2 ⟨by omega, by omega⟩)
  have hpt : p ∈ Nat.primesLE x := Nat.mem_primesLE.2 ⟨hpx, hp⟩
  have hcp : (c : ℕ) ≡ p + 1 - a p % p [MOD p] := c.2 p hpt
  have hr : a p % p < p := Nat.mod_lt _ hp.pos
  have h1 : i + 1 ≡ a p % p [MOD p] := hpm.trans (Nat.mod_modEq _ _).symm
  have h2 : (c : ℕ) + i ≡ (p + 1 - a p % p) + i [MOD p] := hcp.add_right i
  have h3 : (p + 1 - a p % p) + i = (p - a p % p) + (i + 1) := by omega
  have h4 : (p - a p % p) + (i + 1) ≡ (p - a p % p) + a p % p [MOD p] := h1.add_left _
  have h5 : (p - a p % p) + a p % p = p := by omega
  have h6 : (c : ℕ) + i ≡ 0 [MOD p] := by
    have := h2.trans (h3 ▸ h4)
    rw [h5] at this
    exact this.trans (Nat.modEq_zero_iff_dvd.2 dvd_rfl)
  have hdiv : p ∣ (c : ℕ) + i := Nat.modEq_zero_iff_dvd.1 h6
  have hnat : (((c : ℕ) : ℤ) + (i : ℤ)).natAbs = (c : ℕ) + i := by
    rw [← Nat.cast_add, Int.natAbs_natCast]
  rw [hnat] at hcop
  have hpP : p ∣ primorial x := by
    apply Nat.dvd_of_mem_primeFactors
    rw [primeFactors_primorial]; exact hpt
  have hg : p ∣ Nat.gcd ((c : ℕ) + i) (primorial x) := Nat.dvd_gcd hdiv hpP
  rw [hcop.gcd_eq_one] at hg
  exact hp.not_dvd_one hg

theorem Y_le {x k m : ℕ} (hk : Nat.primeCounting x ≤ k) (hm : IsJacobsthalBound k m) : Y x ≤ m := by
  have h0 : (0 : ℕ) ∈ {y : ℕ | Green46.IsCoveredByResidues x y} :=
    ⟨fun _ => 0, fun m hm => absurd (Finset.mem_Icc.1 hm) (by omega)⟩
  exact csSup_le ⟨0, h0⟩ fun y hy => (lt_of_covered hy hk hm).le


/-- The sharpest bound for Erdős 687 that OpenAI's Theorem 1.1 gives through `π(x) ≪ x/log x`:
`Y(x) ≪ x² / (log x · log log x)²`. OpenAI's theorem is applied at `k = ⌈2x/log x⌉ ≥ π(x)`
(Chebyshev's upper bound, in Mathlib), so no lower bound for `π(x)` is needed. -/
theorem Y_isBigO :
    (fun x : ℕ => (Y x : ℝ)) =O[atTop]
      (fun x : ℕ => (x : ℝ) ^ 2 / (Real.log x * Real.log (Real.log x)) ^ 2) := by
  obtain ⟨C, hC, hJ⟩ := OAI.Erdos970.Erdos970Final.erdos_970_iterated_log
  have hcast : Tendsto (fun x : ℕ => (x : ℝ)) atTop atTop := tendsto_natCast_atTop_atTop
  have hcheb := hcast.eventually (Chebyshev.eventually_primeCounting_le (ε := 1/2) (by norm_num))
  have hsqrt := hcast.eventually
    ((isLittleO_log_rpow_atTop (by norm_num : (0:ℝ) < 1/2)).bound (by norm_num : (0:ℝ) < 1))
  have hll := hcast.eventually
    ((Real.tendsto_log_atTop.comp Real.tendsto_log_atTop).eventually_ge_atTop (2 * Real.log 2))
  have hge2 := hcast.eventually (eventually_ge_atTop (2:ℝ))
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hlog4 : Real.log 4 + 1/2 ≤ 2 := by
    have e : Real.log 4 = 2 * Real.log 2 := by
      rw [show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num
    have := Real.log_two_lt_d9
    rw [e]; norm_num at this; linarith
  refine IsBigO.of_bound (36 * C) ?_
  filter_upwards [hcheb, hsqrt, hll, hge2] with x hx1 hx2 hx3 hx4
  simp only [Function.comp_apply] at hx1 hx2 hx3 hx4
  set t : ℝ := (x : ℝ) with ht
  have htpos : 0 < t := by linarith
  have hlogpos : 0 < Real.log t := Real.log_pos (by linarith)
  set a : ℝ := 2 * t / Real.log t with ha
  have ha_pos : 0 < a := by positivity
  set K : ℕ := ⌈a⌉₊ with hKdef
  have hKa : a ≤ (K : ℝ) := Nat.le_ceil a
  have hpi : Nat.primeCounting x ≤ K := by
    have h : (Nat.primeCounting x : ℝ) ≤ a := by
      have h0 := hx1
      rw [Nat.floor_natCast] at h0
      have htl : 0 ≤ t / Real.log t := by positivity
      calc (Nat.primeCounting x : ℝ) ≤ (Real.log 4 + 1/2) * t / Real.log t := h0
        _ = (Real.log 4 + 1/2) * (t / Real.log t) := by ring
        _ ≤ 2 * (t / Real.log t) := by gcongr
        _ = a := by rw [ha]; ring
    exact_mod_cast h.trans hKa
  have hKpos : 0 < K := Nat.ceil_pos.2 ha_pos
  obtain ⟨m, hm, hmb⟩ := hJ K hKpos
  have hY : (Y x : ℝ) ≤ m := by exact_mod_cast Y_le hpi hm
  have hsq : Real.log t ≤ Real.sqrt t := by
    have h := hx2
    rw [Real.norm_of_nonneg hlogpos.le, Real.norm_of_nonneg (by positivity), one_mul,
      ← Real.sqrt_eq_rpow] at h
    exact h
  have hsqrt_pos : 0 < Real.sqrt t := Real.sqrt_pos.2 htpos
  have ha_ge : Real.sqrt t ≤ a := by
    rw [ha, le_div_iff₀ hlogpos]
    calc Real.sqrt t * Real.log t ≤ Real.sqrt t * Real.sqrt t := by gcongr
      _ = t := Real.mul_self_sqrt htpos.le
      _ ≤ 2 * t := by linarith
  have hK0 : (0 : ℝ) ≤ K := Nat.cast_nonneg K
  have h3K : Real.sqrt t ≤ 3 * (K : ℝ) := by linarith
  have hlog3K : (1/2) * Real.log t ≤ Real.log (3 * K) := by
    have e : Real.log (Real.sqrt t) = (1/2) * Real.log t := by
      rw [Real.log_sqrt htpos.le]; ring
    rw [← e]
    exact Real.log_le_log hsqrt_pos h3K
  have hLL : 0 < Real.log (Real.log t) := by linarith
  have hd_pos : 0 < (1/2) * Real.log (Real.log t) := by positivity
  have hD : (1/2) * Real.log (Real.log t) ≤ Real.log (Real.log (3 * K)) := by
    have h1 : Real.log ((1/2) * Real.log t) = Real.log (1/2) + Real.log (Real.log t) :=
      Real.log_mul (by norm_num) hlogpos.ne'
    have h2 : Real.log (1/2 : ℝ) = - Real.log 2 := by rw [one_div, Real.log_inv]
    have h3 : Real.log ((1/2) * Real.log t) ≤ Real.log (Real.log (3 * K)) :=
      Real.log_le_log (by positivity) hlog3K
    linarith
  have hK_le : (K : ℝ) ≤ 3 * t / Real.log t := by
    have h1 : (K : ℝ) < a + 1 := Nat.ceil_lt_add_one ha_pos.le
    have h2 : 1 ≤ t / Real.log t := by
      rw [le_div_iff₀ hlogpos, one_mul]
      linarith [Real.log_le_sub_one_of_pos htpos]
    have e1 : a = 2 * (t / Real.log t) := by rw [ha]; ring
    have e2 : 3 * t / Real.log t = 3 * (t / Real.log t) := by ring
    rw [e2]; rw [e1] at h1; linarith
  have hY0 : (0 : ℝ) ≤ (Y x : ℝ) := Nat.cast_nonneg _
  have hg0 : 0 ≤ t ^ 2 / (Real.log t * Real.log (Real.log t)) ^ 2 := by positivity
  rw [Real.norm_of_nonneg hY0, Real.norm_of_nonneg hg0]
  calc (Y x : ℝ) ≤ m := hY
    _ ≤ C * (K : ℝ) ^ 2 / (Real.log (Real.log (3 * (K : ℝ)))) ^ 2 := hmb
    _ ≤ C * (3 * t / Real.log t) ^ 2 / ((1/2) * Real.log (Real.log t)) ^ 2 := by
        apply div_le_div₀ (by positivity)
        · exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hK0 hK_le 2) hC.le
        · exact pow_pos hd_pos 2
        · exact pow_le_pow_left₀ hd_pos.le hD 2
    _ = 36 * C * (t ^ 2 / (Real.log t * Real.log (Real.log t)) ^ 2) := by
        field_simp
        ring

theorem isLittleO_aux :
    (fun x : ℕ => (x : ℝ) ^ 2 / (Real.log x * Real.log (Real.log x)) ^ 2) =o[atTop]
      (fun x : ℕ => (x : ℝ) ^ 2) := by
  have hcast : Tendsto (fun x : ℕ => (x : ℝ)) atTop atTop := tendsto_natCast_atTop_atTop
  have hL : Tendsto (fun x : ℕ => Real.log x * Real.log (Real.log x)) atTop atTop :=
    (Real.tendsto_log_atTop.comp hcast).atTop_mul_atTop₀
      ((Real.tendsto_log_atTop.comp Real.tendsto_log_atTop).comp hcast)
  have hL2 : Tendsto (fun x : ℕ => (Real.log x * Real.log (Real.log x)) ^ 2) atTop atTop :=
    (tendsto_pow_atTop (by norm_num : (2:ℕ) ≠ 0)).comp hL
  rw [isLittleO_iff_tendsto']
  · refine hL2.inv_tendsto_atTop.congr' ?_
    filter_upwards [eventually_ge_atTop 1] with x hx
    have hx0 : (x : ℝ) ^ 2 ≠ 0 := by positivity
    simp only [Pi.inv_apply]
    field_simp
  · filter_upwards [eventually_ge_atTop 1] with x hx h
    exfalso
    have : (x : ℝ) ^ 2 ≠ 0 := by positivity
    exact this h

/-- Formal Conjectures `Erdos687.erdos_687.parts.ii` (statement verbatim, c83a94d7). -/
theorem erdos_687.parts.ii :
    (fun x : ℕ ↦ (Y x : ℝ)) =o[atTop] (fun x : ℕ ↦ (x : ℝ) ^ 2) := by
  exact Y_isBigO.trans_isLittleO isLittleO_aux

/-- Formal Conjectures `Erdos687.erdos_687.variants.iwaniec` (statement verbatim, c83a94d7). -/
theorem erdos_687.variants.iwaniec :
    (fun x : ℕ ↦ (Y x : ℝ)) =O[atTop] (fun x : ℕ ↦ (x : ℝ) ^ 2) := by
  exact erdos_687.parts.ii.isBigO

end Erdos687
