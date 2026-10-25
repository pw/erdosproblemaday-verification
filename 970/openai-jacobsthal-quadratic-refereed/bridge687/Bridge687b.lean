import Bridge687

/-!
# The quantitative variant proposed in formal-conjectures draft PR #7442 (AItoBit, 18 Oct 2026)

`erdos_687.variants.quadratic_log` (statement verbatim from the PR's diff at its head commit) follows from our
`Erdos687.Y_isBigO`, which is stronger by a factor (log log x)²: x²/(log x · log log x)² ≤ (x/log x)² once log log x ≥ 1.
-/

open Filter Asymptotics

namespace Erdos687

theorem erdos_687.variants.quadratic_log :
    (fun x : ℕ ↦ (Y x : ℝ)) =O[atTop]
      (fun x : ℕ ↦ ((x : ℝ) / Real.log (x : ℝ)) ^ 2) := by
  refine Y_isBigO.trans (IsBigO.of_bound 1 ?_)
  have hcast : Tendsto (fun x : ℕ => (x : ℝ)) atTop atTop := tendsto_natCast_atTop_atTop
  have hll := hcast.eventually
    ((Real.tendsto_log_atTop.comp Real.tendsto_log_atTop).eventually_ge_atTop (1 : ℝ))
  have hge := hcast.eventually (eventually_ge_atTop (3 : ℝ))
  filter_upwards [hll, hge] with x hx1 hx2
  simp only [Function.comp_apply] at hx1 hx2
  have hL : 0 < Real.log (x : ℝ) := Real.log_pos (by linarith)
  have hLL : (1 : ℝ) ≤ Real.log (Real.log (x : ℝ)) := hx1
  have e : (x : ℝ) ^ 2 / (Real.log x * Real.log (Real.log x)) ^ 2
      = ((x : ℝ) / Real.log x) ^ 2 / (Real.log (Real.log x)) ^ 2 := by
    rw [mul_pow, div_pow]; field_simp
  rw [e, Real.norm_of_nonneg (by positivity), Real.norm_of_nonneg (by positivity), one_mul]
  apply div_le_self (by positivity)
  nlinarith

end Erdos687
