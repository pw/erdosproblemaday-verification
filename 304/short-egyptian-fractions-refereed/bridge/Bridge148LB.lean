import Bridge148_293

/-!
# Bridge (added after `Bridge148_293`, same seat, 2026-10-21): Formal Conjectures' `Erdos148.erdos_148.variants.lower_bound`
The statement is a verbatim copy of FC's (google-deepmind/formal-conjectures@2a315101, `FormalConjectures/ErdosProblems/148.lean`,
tagged research solved, `sorry` there), about the verbatim `Erdos148.F` of `Bridge148_293`. Kept in its own file so that the
`leanchecker --fresh` pass already running over `Bridge148_293` is not disturbed.
-/

open Filter Real

namespace Erdos148

/-- Konyagin's lower bound as Formal Conjectures states it, `Erdos148.erdos_148.variants.lower_bound` (verbatim; research solved,
`sorry` in FC), from OpenAI's Corollary 1.2 with `o := 0`: `log 2 · log 3 / 3 · k / log k` is eventually below `c·k`. -/
theorem erdos_148.variants.lower_bound :
    ∃ o : ℕ → ℝ, o =o[atTop] (1 : ℕ → ℝ) ∧ ∀ᶠ k : ℕ in atTop,
      exp (exp ((log 2 * log 3 / 3 + o k) * ((k : ℝ) / log k))) ≤ F k := by
  obtain ⟨c, C, hc, hC, k0, h⟩ := OAI.Problem337.counting_double_log_order
  refine ⟨0, Asymptotics.isLittleO_zero _ _, ?_⟩
  have hev : ∀ᶠ k : ℕ in atTop, Real.log 2 * Real.log 3 / 3 / c ≤ Real.log (k : ℝ) :=
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually_ge_atTop _
  filter_upwards [eventually_ge_atTop k0, hev, eventually_ge_atTop 3] with k hk hlog hk3
  have h1 := (h k hk).1
  rw [F_eq_oai]
  simp only [Pi.zero_apply, add_zero]
  have hk3R : (3 : ℝ) ≤ k := by exact_mod_cast hk3
  have hlogk : 0 < Real.log (k : ℝ) := Real.log_pos (by linarith)
  have hA : Real.log 2 * Real.log 3 / 3 / Real.log k ≤ c := by
    rw [div_le_iff₀ hlogk]
    have := (div_le_iff₀ hc).mp hlog
    linarith
  have hle : Real.log 2 * Real.log 3 / 3 * ((k : ℝ) / Real.log k) ≤ c * k := by
    have e : Real.log 2 * Real.log 3 / 3 * ((k : ℝ) / Real.log k) =
        Real.log 2 * Real.log 3 / 3 / Real.log k * k := by ring
    rw [e]
    exact mul_le_mul_of_nonneg_right hA (by linarith)
  have hkpos : (0 : ℝ) < k := by linarith
  have hck : 0 < c * (k : ℝ) := mul_pos hc hkpos
  have hLL : 0 < Real.log (Real.log (OAI.Problem337.F k : ℝ)) := lt_of_lt_of_le hck h1
  have hF2 : 2 ≤ OAI.Problem337.F k := by
    by_contra hlt
    have hlt' : OAI.Problem337.F k < 2 := by omega
    clear hlt
    set n := OAI.Problem337.F k with hn
    interval_cases n <;> simp at hLL
  have hlogF : 0 < Real.log (OAI.Problem337.F k : ℝ) :=
    Real.log_pos (by exact_mod_cast (show 1 < OAI.Problem337.F k by omega))
  calc Real.exp (Real.exp (Real.log 2 * Real.log 3 / 3 * ((k : ℝ) / Real.log k)))
      ≤ Real.exp (Real.exp (c * k)) := by gcongr
    _ ≤ Real.exp (Real.exp (Real.log (Real.log (OAI.Problem337.F k : ℝ)))) := by gcongr
    _ = (OAI.Problem337.F k : ℝ) := by
      rw [Real.exp_log hlogF, Real.exp_log (by positivity)]

end Erdos148
