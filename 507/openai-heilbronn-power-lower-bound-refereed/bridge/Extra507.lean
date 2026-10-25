import Mathlib
import Bridge507

/-!
# Two more targets from the every-n theorem (erdos cron seat, 2026-10-22, 15:00Z)

1. Formal Conjectures' `Green77.green_77` (Ben Green's open problem 77, `research open` in FC at 3bf943f1):
   "∃ o → 0 with α ≪ n^(-2+o(n))" — the almost-n⁻² upper bound for FC's `Erdos507.α`. We prove its NEGATION,
   statement copied verbatim between the markers.
2. Big O Speedrun's trusted statement `BigOSpeedrun.HeilbronnTriangle.Bound η` (bigospeedrun/verifier @0efdd614,
   `challenges/heilbronn-triangle/Statement.lean`, copied verbatim between the markers) at OpenAI's exponent
   `η = 2/(45435k+16)`, `k = heilbronnK` — the board's "OpenAI baseline".
-/

open Filter Topology Asymptotics
open scoped EuclideanGeometry

-- VERBATIM BEGIN green77-open
open Erdos507 Filter Topology

namespace Green77
-- VERBATIM END green77-open

/-- The NEGATION of Formal Conjectures' `Green77.green_77`; the proposition inside `¬ ( … )` is FC's statement verbatim. -/
theorem green_77_negated : ¬ (
-- VERBATIM BEGIN green77-statement
    ∃ (o : ℕ → ℝ), Tendsto o atTop (𝓝 0) ∧
      α ≪ fun n ↦ n ^ (-2 + o n)
-- VERBATIM END green77-statement
    ) := by
  rintro ⟨o, ho, hbig⟩
  obtain ⟨c, hc, hlow⟩ := Erdos507Bridge.eventually_alpha_ge
  set e : ℝ := 2 / (OAI.Problem355.EveryN.alphaOf OAI.Problem355.heilbronnK : ℝ) with he
  have hepos : 0 < e := Erdos507Bridge.alphaExp_pos
  obtain ⟨C, hC⟩ := hbig.bound
  -- o n < e/2 eventually
  have ho' : ∀ᶠ n in atTop, o n < e / 2 := ho.eventually (gt_mem_nhds (by linarith))
  -- n^(e/2) → ∞
  have hgrow : Tendsto (fun n : ℕ => (n : ℝ) ^ (e / 2)) atTop atTop :=
    (tendsto_rpow_atTop (by linarith)).comp tendsto_natCast_atTop_atTop
  have hbigN : ∀ᶠ n : ℕ in atTop, (|C| + 1) / c < (n : ℝ) ^ (e / 2) :=
    hgrow.eventually (eventually_gt_atTop _)
  obtain ⟨n, hn1, hn2, hn3, hn4, hn5⟩ :=
    (hlow.and (hC.and (ho'.and (hbigN.and (eventually_gt_atTop 0))))).exists
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn5
  have hn1' : (1 : ℝ) ≤ n := by exact_mod_cast hn5
  -- unfold the answer
  have hans : Erdos507.erdos_507.lower.answer n = (n : ℝ) ^ (-2 + e) := rfl
  rw [hans] at hn1
  have hpos1 : 0 < (n : ℝ) ^ (-2 + o n) := Real.rpow_pos_of_pos hnR _
  have hαnn : 0 ≤ α n := le_trans (by positivity) hn1
  rw [Real.norm_of_nonneg hαnn, Real.norm_of_nonneg hpos1.le] at hn2
  -- n^(-2+o n) ≤ n^(-2+e/2)
  have hmono : (n : ℝ) ^ (-2 + o n) ≤ (n : ℝ) ^ (-2 + e / 2) :=
    Real.rpow_le_rpow_of_exponent_le hn1' (by linarith)
  have hsplit : (n : ℝ) ^ (-2 + e) = (n : ℝ) ^ (-2 + e / 2) * (n : ℝ) ^ (e / 2) := by
    rw [← Real.rpow_add hnR]; ring_nf
  have hq : 0 < (n : ℝ) ^ (-2 + e / 2) := Real.rpow_pos_of_pos hnR _
  -- c·n^(-2+e/2)·n^(e/2) ≤ α n ≤ C·n^(-2+o n) ≤ |C|·n^(-2+e/2)
  have key : c * ((n : ℝ) ^ (-2 + e / 2) * (n : ℝ) ^ (e / 2)) ≤ |C| * (n : ℝ) ^ (-2 + e / 2) := by
    calc c * ((n : ℝ) ^ (-2 + e / 2) * (n : ℝ) ^ (e / 2)) = c * (n : ℝ) ^ (-2 + e) := by rw [hsplit]
      _ ≤ α n := hn1
      _ ≤ C * (n : ℝ) ^ (-2 + o n) := hn2
      _ ≤ |C| * (n : ℝ) ^ (-2 + o n) := by gcongr; exact le_abs_self C
      _ ≤ |C| * (n : ℝ) ^ (-2 + e / 2) := by gcongr
  have key2 : c * (n : ℝ) ^ (e / 2) ≤ |C| := by
    have := key
    rw [show c * ((n : ℝ) ^ (-2 + e / 2) * (n : ℝ) ^ (e / 2)) =
        (c * (n : ℝ) ^ (e / 2)) * (n : ℝ) ^ (-2 + e / 2) by ring] at this
    exact le_of_mul_le_mul_right this hq
  have key3 : (|C| + 1) < c * (n : ℝ) ^ (e / 2) := by
    rw [div_lt_iff₀ hc] at hn4; linarith
  linarith

/-- Non-vacuity control for the negation above: with the exponent `+2` in place of `-2`, the SAME proposition shape
(same `α`, same `≪`, same `o`) is PROVABLE (take `o = 0`; `0 ≤ α n ≤ 4`). So FC's statement is not false for a
trivial reason of form; it is false because `α` is large. -/
theorem green_77_shape_control :
    ∃ (o : ℕ → ℝ), Tendsto o atTop (𝓝 0) ∧
      α ≪ fun n ↦ n ^ (2 + o n) := by
  refine ⟨fun _ => 0, tendsto_const_nhds, ?_⟩
  have hmin0 : ∀ S : Finset ℝ², 0 ≤ minTriangleArea S := by
    intro S
    unfold minTriangleArea
    apply Real.sInf_nonneg
    rintro _ ⟨p, _, _, rfl⟩
    exact abs_nonneg _
  have hα0 : ∀ n, 0 ≤ α n := by
    intro n; unfold α
    apply Real.sSup_nonneg
    rintro _ ⟨S, _, rfl⟩
    exact hmin0 S
  have hα4 : ∀ n, α n ≤ 4 := by
    intro n; unfold α
    apply Real.sSup_le _ (by norm_num)
    rintro _ ⟨S, hS, rfl⟩
    exact Erdos507Bridge.minTriangleArea_le_four hS.2.1
  refine Asymptotics.IsBigO.of_bound 4 ?_
  filter_upwards [eventually_gt_atTop 0] with n hn
  have hn1 : (1 : ℝ) ≤ n := by exact_mod_cast hn
  rw [Real.norm_of_nonneg (hα0 n), add_zero, Real.norm_of_nonneg (by positivity)]
  have : (1 : ℝ) ≤ (n : ℝ) ^ (2 : ℝ) := Real.one_le_rpow hn1 (by norm_num)
  nlinarith [hα4 n]

end Green77

-- VERBATIM BEGIN bos
namespace BigOSpeedrun.HeilbronnTriangle

open OAI.Problem355

def Bound (η : ℚ) : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∃ N : ℕ, ∀ n : ℕ, N ≤ n →
    ∃ P : Finset Point, P.card = n ∧ pointsInUnitSquare P ∧
      triangleAreasAtLeast P (c * Real.rpow (n : ℝ) (-2 + (η : ℝ)))

end BigOSpeedrun.HeilbronnTriangle
-- VERBATIM END bos

namespace Extra507

/-- The rational exponent's cast, for an abstract `K` (so no tactic touches the concrete `heilbronnK`). -/
lemma cast_eta (K : ℕ) :
    (((2 : ℚ) / (45435 * (K : ℚ) + 16) : ℚ) : ℝ) = 2 / (OAI.Problem355.EveryN.alphaOf K : ℝ) := by
  unfold OAI.Problem355.EveryN.alphaOf
  push_cast
  ring

/-- **The Big O Speedrun Heilbronn board's statement at OpenAI's baseline exponent `2/(45435k+16)`.** -/
theorem bound_openai_baseline :
    BigOSpeedrun.HeilbronnTriangle.Bound ((2 : ℚ) / (45435 * (OAI.Problem355.heilbronnK : ℚ) + 16)) := by
  obtain ⟨c, hc, n0, -, h⟩ := OAI.Problem355.EveryN.every_large_n
  refine ⟨c, hc, n0, fun n hn => ?_⟩
  rw [cast_eta]
  exact h n hn

end Extra507
