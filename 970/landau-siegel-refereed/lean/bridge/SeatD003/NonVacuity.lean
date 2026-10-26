import Mathlib
import SeatD003.NoLSStatement
/-! Seat D: non-vacuity of the hypotheses and the meaning of `DirichletCharacter.LFunction`
(Mathlib-only, kernel-checked). -/

namespace SeatD003
open DirichletCharacter

/-- the quadratic (Legendre) character mod 3, as a Dirichlet character with values in ℂ -/
noncomputable def chi3 : DirichletCharacter ℂ 3 :=
  (quadraticChar (ZMod 3)).ringHomComp (Int.castRingHom ℂ)

lemma chi3_apply (a : ZMod 3) : chi3 a = ((quadraticChar (ZMod 3) a : ℤ) : ℂ) := rfl

lemma chi3_two : chi3 2 = -1 := by
  have h : quadraticChar (ZMod 3) 2 = -1 :=
    quadraticChar_neg_one_iff_not_isSquare.mpr (by decide)
  rw [chi3_apply, h]; simp

lemma chi3_ne_one : chi3 ≠ 1 := by
  intro h
  have h2 := chi3_two
  have hu : IsUnit (2 : ZMod 3) := by decide
  rw [h, MulChar.one_apply hu] at h2
  norm_num at h2

lemma chi3_isPrimitive : chi3.IsPrimitive := by
  rw [isPrimitive_def]
  rcases (Nat.dvd_prime Nat.prime_three).mp (conductor_dvd_level chi3) with h | h
  · exact absurd (eq_one_iff_conductor_eq_one.mpr h) chi3_ne_one
  · exact h

lemma chi3_real (a : ZMod 3) : (chi3 a).im = 0 := by
  rw [chi3_apply]; exact Complex.intCast_im _

/-- (4a) The hypotheses of Theorem 1 on (q, χ) are satisfiable. -/
theorem hypotheses_satisfiable :
    ∃ (q : ℕ) (_ : NeZero q) (χ : DirichletCharacter ℂ q),
      3 ≤ q ∧ χ.IsPrimitive ∧ χ ≠ 1 ∧ ∀ a : ZMod q, (χ a).im = 0 :=
  ⟨3, inferInstance, chi3, le_rfl, chi3_isPrimitive, chi3_ne_one, chi3_real⟩

/-- control: the trivial character mod 3 is NOT primitive (so `IsPrimitive` is not vacuous-true). -/
theorem one_mod3_not_primitive : ¬ (1 : DirichletCharacter ℂ 3).IsPrimitive := by
  rw [isPrimitive_def, conductor_one]; decide

/-- (4b) uniqueness: any entire function agreeing with the Dirichlet series ∑ χ(n) n^{-s} on
Re s > 1 IS `χ.LFunction` everywhere (identity theorem on the connected set ℂ). So the value of
`χ.LFunction` at β ∈ (0,1) is the analytic continuation of the series, not a junk value. -/
theorem LFunction_unique {N : ℕ} [NeZero N] (χ : DirichletCharacter ℂ N) (hχ : χ ≠ 1)
    (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (hagree : ∀ s : ℂ, 1 < s.re → f s = LSeries (fun n => χ n) s) :
    f = χ.LFunction := by
  have h1 : AnalyticOnNhd ℂ f Set.univ := hf.differentiableOn.analyticOnNhd isOpen_univ
  have h2 : AnalyticOnNhd ℂ χ.LFunction Set.univ :=
    (differentiable_LFunction hχ).differentiableOn.analyticOnNhd isOpen_univ
  have hev : f =ᶠ[nhds (2 : ℂ)] χ.LFunction := by
    have hopen : {z : ℂ | 1 < z.re} ∈ nhds (2 : ℂ) :=
      (isOpen_lt continuous_const Complex.continuous_re).mem_nhds (by norm_num)
    filter_upwards [hopen] with z hz
    rw [hagree z hz, LFunction_eq_LSeries χ hz]
  have := h1.eqOn_of_preconnected_of_eventuallyEq h2 isPreconnected_univ (Set.mem_univ _) hev
  funext s; exact this (Set.mem_univ s)


/-- Control for the junk-value trap: the mutant that reads "zero" off Mathlib's naive `LSeries`
(which is 0 wherever the series is not absolutely summable, i.e. on all of 0 < β < 1) is FALSE.
So the bridge's use of `LFunction` is load-bearing, and mutant (v)'s rejection is semantic. -/
theorem not_Mut_LSeries : ¬ Mut_LSeries := by
  rintro ⟨c, hc, h⟩
  have hl : 0 < Real.log 3 := Real.log_pos (by norm_num)
  obtain ⟨t, ht0, ht1, ht2⟩ : ∃ t : ℝ, 0 < t ∧ t ≤ 1/2 ∧ t * Real.log 3 ≤ c / 2 := by
    refine ⟨min (1/2 : ℝ) (c / (2 * Real.log 3)), lt_min (by norm_num) (by positivity),
      min_le_left _ _, ?_⟩
    calc min (1/2 : ℝ) (c / (2 * Real.log 3)) * Real.log 3
        ≤ c / (2 * Real.log 3) * Real.log 3 := by gcongr; exact min_le_right _ _
      _ = c / 2 := by field_simp
  have hz : LSeries (fun n => chi3 n) (((1 - t : ℝ)) : ℂ) = 0 := by
    apply LSeries.eq_zero_of_not_LSeriesSummable
    rw [DirichletCharacter.LSeriesSummable_iff (by norm_num) chi3, Complex.ofReal_re]
    linarith
  have key := h 3 le_rfl chi3 chi3_isPrimitive chi3_ne_one chi3_real (1 - t)
    ⟨by linarith, by linarith, hz⟩
  have h3 : ((3 : ℕ) : ℝ) = 3 := by norm_num
  rw [h3] at key
  nlinarith

end SeatD003

#check @DirichletCharacter.LFunction_eq_LSeries
#check @DirichletCharacter.differentiable_LFunction
#check @DirichletCharacter.differentiableAt_LFunction
#check @DirichletCharacter.LFunction_apply_one_ne_zero
#print DirichletCharacter.LFunction
#print DirichletCharacter.IsPrimitive
#print DirichletCharacter
#print axioms SeatD003.hypotheses_satisfiable
#print axioms SeatD003.LFunction_unique
#print axioms SeatD003.one_mod3_not_primitive
#print axioms SeatD003.not_Mut_LSeries
