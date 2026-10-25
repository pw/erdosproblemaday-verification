import Mathlib
import EveryN507

/-!
# Bridge: OpenAI's Lean (+ our every-n step) ⟹ Formal Conjectures' `Erdos507` lower-bound statements
(erdos cron seat, 2026-10-22, 15:00Z)

Everything between the `VERBATIM` markers is copied from google-deepmind/formal-conjectures@3bf943f1
(`FormalConjecturesForMathlib/Geometry/2d.lean`, `FormalConjecturesForMathlib/Analysis/Asymptotics/Basic.lean`,
`FormalConjectures/ErdosProblems/507.lean`), with FC attributes and docstrings removed and `module`/`public` syntax
dropped; `verbatim_check.py` asserts the copies whitespace-normalised. The ONE change is the body of
`erdos_507.lower.answer`, which FC leaves as `sorry` (a "question value" problem): we supply `n ^ (-2 + 2/α)`.

Proved below, all from `OAI.Problem355.EveryN.every_large_n` (OpenAI's construction + our interpolation):
* `Erdos507.erdos_507.lower` — FC's statement verbatim (FC: `research open`), with the answer supplied;
* `Erdos507.erdos_507.variants.lower_kps82` and `Erdos507.erdos_507.variants.lower_erdos` — FC's statements verbatim
  (FC: `research solved`, proof bodies `sorry`).
FC's unit disk vs OpenAI's unit square: translate by `(-1/2, -1/2)`; areas are unchanged and the square lands in the
disk of radius `1/√2`.
-/

-- VERBATIM BEGIN 2d
scoped[EuclideanGeometry] notation "ℝ²" => EuclideanSpace ℝ (Fin 2)

open scoped EuclideanGeometry Finset

noncomputable instance Module.orientedEuclideanSpaceFinTwo : Module.Oriented ℝ ℝ² (Fin 2) :=
  ⟨Basis.orientation <| PiLp.basisFun 2 _ _⟩

instance fact_finrank_euclideanSpace_fin_two : Fact (Module.finrank ℝ ℝ² = 2) :=
  ⟨finrank_euclideanSpace_fin⟩

namespace EuclideanGeometry

variable {V P : Type*} {n : ℕ}

variable [NormedAddCommGroup V] [InnerProductSpace ℝ V] [MetricSpace P] [NormedAddTorsor V P]

variable [Module.Oriented ℝ V (Fin 2)] [Fact (Module.finrank ℝ V = 2)] {p : Fin n → P}

noncomputable def triangle_area (a b c : P) : ℝ :=
  positiveOrientation.areaForm (a -ᵥ c) (b -ᵥ c) / 2

lemma triangle_area_eq_det (a b c : ℝ²) :
    triangle_area a b c =
    Matrix.det !![a 0, b 0, c 0;
                  a 1, b 1, c 1;
                  1,   1,   1] / 2 := by
  rw [triangle_area, Orientation.areaForm_to_volumeForm,
    positiveOrientation.volumeForm_robust (EuclideanSpace.basisFun (Fin 2) ℝ) rfl, Module.Basis.det_apply]
  suffices (a 0 - c 0) * (b 1 - c 1) - (b 0 - c 0) * (a 1 - c 1) =
      a 0 * b 1 - a 0 * c 1 - b 0 * a 1 + b 0 * c 1 + c 0 * a 1 - c 0 * b 1 by
    simp [Matrix.det_fin_two, Matrix.det_fin_three, Module.Basis.toMatrix, this]
  ring

end EuclideanGeometry
-- VERBATIM END 2d

-- VERBATIM BEGIN asymptotics
notation f " ≫ " g => Asymptotics.IsBigO Filter.atTop (g : ℕ → ℝ) (f : ℕ → ℝ)
notation g " ≪ " f => Asymptotics.IsBigO Filter.atTop (g : ℕ → ℝ) (f : ℕ → ℝ)
-- VERBATIM END asymptotics

-- VERBATIM BEGIN 507-defs
open Asymptotics Filter Topology
open scoped EuclideanGeometry

namespace Erdos507

noncomputable def minTriangleArea (S : Finset ℝ²) : ℝ :=
  sInf {abs (EuclideanGeometry.triangle_area (p 0) (p 1) (p 2)) |
    (p : Fin 3 → ℝ²) (_ : Function.Injective p) (_ : ∀ i, p i ∈ S)}

noncomputable def α (n : ℕ) : ℝ :=
  sSup (minTriangleArea '' { S : Finset ℝ² |
    S.card = n ∧ ↑S ⊆ Metric.closedBall (0 : ℝ²) 1 ∧ ¬ Collinear ℝ (S : Set ℝ²) })

noncomputable def lowerBest (n : ℕ) : ℝ := Real.log n / (n : ℝ) ^ 2
-- VERBATIM END 507-defs

/-- FC leaves this `sorry`; the answer supplied here is `n ^ (-2 + 2/α)`, `α = 45435k + 16`. -/
noncomputable def erdos_507.lower.answer : ℕ → ℝ :=
  fun n => (n : ℝ) ^ (-2 + 4 / (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ))

end Erdos507

namespace Erdos507Bridge

open Erdos507 EuclideanGeometry

/-- OpenAI's points, translated by `(-1/2, -1/2)` into FC's plane. -/
noncomputable def φ (p : OAI.Problem355.Point) : ℝ² := !₂[p.1 - 1 / 2, p.2 - 1 / 2]

@[simp] lemma φ_zero (p : OAI.Problem355.Point) : φ p 0 = p.1 - 1 / 2 := by simp [φ]
@[simp] lemma φ_one (p : OAI.Problem355.Point) : φ p 1 = p.2 - 1 / 2 := by simp [φ]

lemma φ_injective : Function.Injective φ := by
  intro p q h
  have h0 := congrArg (fun x : ℝ² => x 0) h
  have h1 := congrArg (fun x : ℝ² => x 1) h
  simp only [φ_zero, φ_one] at h0 h1
  exact Prod.ext (by linarith) (by linarith)

/-- FC's signed area in coordinates. -/
lemma triangle_area_coords (a b c : ℝ²) :
    triangle_area a b c = ((a 0 - c 0) * (b 1 - c 1) - (b 0 - c 0) * (a 1 - c 1)) / 2 := by
  rw [triangle_area_eq_det]
  simp [Matrix.det_fin_three]
  ring

/-- FC's unsigned area of the translated triangle is OpenAI's `triangleArea`. -/
lemma abs_area_φ (p q s : OAI.Problem355.Point) :
    |triangle_area (φ p) (φ q) (φ s)| = OAI.Problem355.triangleArea p q s := by
  rw [triangle_area_coords, OAI.Problem355.triangleArea, abs_div, abs_two]
  simp only [φ_zero, φ_one]
  congr 2
  ring

/-- Points of the unit square land in FC's closed unit disk. -/
lemma φ_mem_ball {p : OAI.Problem355.Point} (hp : OAI.Problem355.pointInUnitSquare p) :
    φ p ∈ Metric.closedBall (0 : ℝ²) 1 := by
  obtain ⟨h1, h2, h3, h4⟩ := hp
  rw [mem_closedBall_zero_iff, EuclideanSpace.norm_eq, Fin.sum_univ_two, φ_zero, φ_one]
  rw [Real.sqrt_le_one]
  simp only [Real.norm_eq_abs, sq_abs]
  nlinarith

/-- Collinear points have FC area zero. -/
lemma triangle_area_eq_zero_of_collinear {a b c : ℝ²} (h : Collinear ℝ ({a, b, c} : Set ℝ²)) :
    triangle_area a b c = 0 := by
  obtain ⟨v, hv⟩ := (collinear_iff_of_mem (p₀ := c) (by simp)).1 h
  obtain ⟨ra, ha⟩ := hv a (by simp)
  obtain ⟨rb, hb⟩ := hv b (by simp)
  rw [triangle_area, ha, hb, vadd_vsub, vadd_vsub, map_smul, map_smul, LinearMap.smul_apply,
    Orientation.areaForm_apply_self]
  simp

/-- Coordinates of a point in the closed unit disk are at most 1 in absolute value. -/
lemma abs_coord_le {x : ℝ²} (hx : x ∈ Metric.closedBall (0 : ℝ²) 1) (i : Fin 2) : |x i| ≤ 1 := by
  rw [mem_closedBall_zero_iff] at hx
  have := PiLp.norm_apply_le x i
  rw [Real.norm_eq_abs] at this
  linarith

/-- Every triangle in the closed unit disk has `|area| ≤ 4`. -/
lemma abs_area_le_four {a b c : ℝ²} (ha : a ∈ Metric.closedBall (0 : ℝ²) 1)
    (hb : b ∈ Metric.closedBall (0 : ℝ²) 1) (hc : c ∈ Metric.closedBall (0 : ℝ²) 1) :
    |triangle_area a b c| ≤ 4 := by
  rw [triangle_area_coords, abs_div, abs_two]
  have e : ∀ x y : ℝ², x ∈ Metric.closedBall (0 : ℝ²) 1 → y ∈ Metric.closedBall (0 : ℝ²) 1 →
      ∀ i, |x i - y i| ≤ 2 := by
    intro x y hx hy i
    calc |x i - y i| ≤ |x i| + |y i| := abs_sub _ _
      _ ≤ 1 + 1 := add_le_add (abs_coord_le hx i) (abs_coord_le hy i)
      _ = 2 := by norm_num
  have key : |(a 0 - c 0) * (b 1 - c 1) - (b 0 - c 0) * (a 1 - c 1)| ≤ 8 := by
    calc |(a 0 - c 0) * (b 1 - c 1) - (b 0 - c 0) * (a 1 - c 1)|
        ≤ |(a 0 - c 0) * (b 1 - c 1)| + |(b 0 - c 0) * (a 1 - c 1)| := abs_sub _ _
      _ = |a 0 - c 0| * |b 1 - c 1| + |b 0 - c 0| * |a 1 - c 1| := by rw [abs_mul, abs_mul]
      _ ≤ 2 * 2 + 2 * 2 := by
          gcongr
          · exact e a c ha hc 0
          · exact e b c hb hc 1
          · exact e b c hb hc 0
          · exact e a c ha hc 1
      _ = 8 := by norm_num
  linarith

lemma minTriangleArea_le_four {S : Finset ℝ²} (hS : (S : Set ℝ²) ⊆ Metric.closedBall (0 : ℝ²) 1) :
    minTriangleArea S ≤ 4 := by
  unfold minTriangleArea
  by_cases hne : ∃ p : Fin 3 → ℝ², Function.Injective p ∧ ∀ i, p i ∈ S
  · obtain ⟨p, hp, hpS⟩ := hne
    calc _ ≤ |triangle_area (p 0) (p 1) (p 2)| := by
          refine csInf_le ?_ ?_
          · refine ⟨0, ?_⟩
            rintro _ ⟨q, _, _, rfl⟩
            exact abs_nonneg _
          · exact ⟨p, hp, hpS, rfl⟩
      _ ≤ 4 := abs_area_le_four (hS (hpS 0)) (hS (hpS 1)) (hS (hpS 2))
  · have : {x | ∃ (p : Fin 3 → ℝ²) (_ : Function.Injective p) (_ : ∀ i, p i ∈ S),
        |triangle_area (p 0) (p 1) (p 2)| = x} = ∅ := by
      ext x
      simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
      rintro ⟨p, hp, hpS, -⟩
      exact hne ⟨p, hp, hpS⟩
    simp only [this, Real.sInf_empty]
    norm_num

/-- The analytic core: for every large `n`, FC's `α n ≥ c · n^(-2+2/α)`. -/
theorem eventually_alpha_ge :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ n : ℕ in atTop, c * erdos_507.lower.answer n ≤ α n := by
  obtain ⟨c, hc, n0, hn0, h⟩ := OAI.Problem355.EveryN.every_large_n
  refine ⟨c, hc, Filter.eventually_atTop.2 ⟨n0, fun n hn => ?_⟩⟩
  obtain ⟨P, hcard, hsq, harea⟩ := h n hn
  set η : ℝ := -2 + 2 / (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ)
  have hn3 : 3 ≤ n := hn0.trans hn
  have hnpos : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hbpos : 0 < c * Real.rpow (n : ℝ) η := mul_pos hc (Real.rpow_pos_of_pos hnpos _)
  classical
  let S : Finset ℝ² := P.image φ
  have hScard : S.card = n := by rw [Finset.card_image_of_injective _ φ_injective, hcard]
  have hSball : (S : Set ℝ²) ⊆ Metric.closedBall (0 : ℝ²) 1 := by
    intro x hx
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.1 (Finset.mem_coe.1 hx)
    exact φ_mem_ball (hsq p hp)
  -- every injective triple of S has |area| ≥ c n^η
  have hall : ∀ p : Fin 3 → ℝ², Function.Injective p → (∀ i, p i ∈ S) →
      c * Real.rpow (n : ℝ) η ≤ |triangle_area (p 0) (p 1) (p 2)| := by
    intro p hp hpS
    choose x hx hxp using fun i => Finset.mem_image.1 (hpS i)
    have hne : ∀ i j, i ≠ j → x i ≠ x j := by
      intro i j hij hx'
      exact hij (hp (by rw [← hxp i, ← hxp j, hx']))
    rw [← hxp 0, ← hxp 1, ← hxp 2, abs_area_φ]
    exact harea (x 0) (hx 0) (x 1) (hx 1) (x 2) (hx 2)
      (hne 0 1 (by decide)) (hne 0 2 (by decide)) (hne 1 2 (by decide))
  -- S has an injective triple
  obtain ⟨a, ha, b, hb, d, hd, hab, had, hbd⟩ := Finset.two_lt_card.1 (by omega : 2 < S.card)
  let t : Fin 3 → ℝ² := ![a, b, d]
  have ht : Function.Injective t := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all [t]
  have htS : ∀ i, t i ∈ S := by
    intro i; fin_cases i <;> simp [t, ha, hb, hd]
  -- not collinear
  have hncol : ¬ Collinear ℝ (S : Set ℝ²) := by
    intro hcol
    have hsub : ({t 0, t 1, t 2} : Set ℝ²) ⊆ S := by
      intro x hx
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
      rcases hx with h | h | h <;> rw [h] <;> exact Finset.mem_coe.2 (htS _)
    have h0 := triangle_area_eq_zero_of_collinear (hcol.subset hsub)
    have := hall t ht htS
    rw [h0, abs_zero] at this
    linarith
  -- min area ≥ bound
  have hmin : c * Real.rpow (n : ℝ) η ≤ minTriangleArea S := by
    unfold minTriangleArea
    refine le_csInf ?_ ?_
    · exact ⟨_, t, ht, htS, rfl⟩
    · rintro _ ⟨p, hp, hpS, rfl⟩
      exact hall p hp hpS
  -- α n ≥ min area
  have hα : minTriangleArea S ≤ α n := by
    unfold α
    apply le_csSup
    · refine ⟨4, ?_⟩
      rintro _ ⟨T, hT, rfl⟩
      exact minTriangleArea_le_four hT.2.1
    · exact ⟨S, ⟨hScard, hSball, hncol⟩, rfl⟩
  have : erdos_507.lower.answer n = Real.rpow (n : ℝ) η := by
    simp only [erdos_507.lower.answer, η, Real.rpow_eq_pow]
  rw [this]
  exact hmin.trans hα

lemma answer_pos {n : ℕ} (hn : 0 < n) : 0 < erdos_507.lower.answer n := by
  unfold erdos_507.lower.answer
  exact Real.rpow_pos_of_pos (by exact_mod_cast hn) _

lemma answer_isBigO_alpha : erdos_507.lower.answer ≪ α := by
  obtain ⟨c, hc, h⟩ := eventually_alpha_ge
  refine Asymptotics.IsBigO.of_bound (1 / c) ?_
  filter_upwards [h, Filter.eventually_gt_atTop 0] with n hn hn0
  have hpos := answer_pos hn0
  have hαpos : 0 ≤ α n := le_trans (by positivity) hn
  rw [Real.norm_of_nonneg hpos.le, Real.norm_of_nonneg hαpos]
  rw [div_mul_eq_mul_div, one_mul, le_div_iff₀ hc]
  linarith

lemma alphaExp_pos : (0 : ℝ) < 2 / (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ) := by
  have : (0 : ℝ) < (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ) := by
    exact_mod_cast OAI.Problem355.EveryN.alphaOf_pos _
  positivity

lemma lowerBest_isLittleO_answer : lowerBest =o[atTop] erdos_507.lower.answer := by
  set e : ℝ := 2 / (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ) with he
  have hpos : 0 < e := alphaExp_pos
  have h1 : (fun n : ℕ => Real.log n) =o[atTop] (fun n : ℕ => (n : ℝ) ^ e) :=
    (isLittleO_log_rpow_atTop hpos).comp_tendsto tendsto_natCast_atTop_atTop
  have h2 : (fun n : ℕ => Real.log n * (n : ℝ) ^ (-2 : ℝ)) =o[atTop]
      (fun n : ℕ => (n : ℝ) ^ e * (n : ℝ) ^ (-2 : ℝ)) :=
    h1.mul_isBigO (Asymptotics.isBigO_refl _ _)
  refine h2.congr' ?_ ?_
  · filter_upwards [Filter.eventually_gt_atTop 0] with n hn
    have hnR : (0 : ℝ) < n := by exact_mod_cast hn
    simp only [lowerBest, Real.rpow_neg hnR.le, div_eq_mul_inv]
    norm_num
  · filter_upwards [Filter.eventually_gt_atTop 0] with n hn
    have hnR : (0 : ℝ) < n := by exact_mod_cast hn
    simp only [erdos_507.lower.answer]
    rw [← Real.rpow_add hnR, ← he]
    ring_nf

end Erdos507Bridge

namespace Erdos507

open Erdos507Bridge

-- VERBATIM BEGIN 507-lower
theorem erdos_507.lower:
    (lowerBest =o[atTop] erdos_507.lower.answer) ∧ (erdos_507.lower.answer ≪ α) := by
-- VERBATIM END 507-lower
  exact ⟨lowerBest_isLittleO_answer, answer_isBigO_alpha⟩

-- VERBATIM BEGIN 507-kps82
theorem erdos_507.variants.lower_kps82 : lowerBest ≪ α := by
-- VERBATIM END 507-kps82
  exact lowerBest_isLittleO_answer.isBigO.trans answer_isBigO_alpha

-- VERBATIM BEGIN 507-erdos
theorem erdos_507.variants.lower_erdos : α ≫ (fun n ↦ 1 / (n : ℝ) ^ 2) := by
-- VERBATIM END 507-erdos
  refine Asymptotics.IsBigO.trans ?_ answer_isBigO_alpha
  refine Asymptotics.IsBigO.of_bound 1 ?_
  filter_upwards [Filter.eventually_gt_atTop 0] with n hn
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (0 : ℝ) < n := by linarith
  have hans := answer_pos hn
  rw [Real.norm_of_nonneg (by positivity), Real.norm_of_nonneg hans.le, one_mul]
  unfold erdos_507.lower.answer
  have : 1 / (n : ℝ) ^ 2 = (n : ℝ) ^ (-2 : ℝ) := by
    rw [Real.rpow_neg hn0.le]; norm_num
  rw [this]
  apply Real.rpow_le_rpow_of_exponent_le hnR
  linarith [alphaExp_pos]

end Erdos507
