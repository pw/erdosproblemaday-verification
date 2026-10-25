import OAI.Combinatorics.CliqueFree.Main

/-!
# Bridge (erdosproblemaday.com, 2026-10-21): Formal Conjectures' `Erdos802.erdos_802` from OpenAI's
# `OAI.CliqueFreeLog.logarithmic_independence_bound` (family 184, `OAI.Combinatorics.CliqueFree.Main` closure).

The definition `SimpleGraph.averageDegree` and the theorem statements in `namespace Erdos802` below are copied VERBATIM
(text and binder names) from google-deepmind/formal-conjectures @ 90d18f666eb98adec4eee4d12f1d37e30b4eb204
(2026-10-20T20:20:35Z): `FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Degrees.lean` (namespace `SimpleGraph`)
and `FormalConjectures/ErdosProblems/802.lean` (namespace `Erdos802`; `erdos_802` is tagged `research open`, the variants
`research solved`). The definition keeps FC's full name `SimpleGraph.averageDegree` (OpenAI's Mathlib d13f23b7 has no constant of that name), so the
statements' dot notation `G.averageDegree` resolves exactly as in FC; only the theorems' enclosing namespace differs (`Bridge802`). This proves a verbatim copy of FC's statement in
OpenAI's environment (Lean v4.34.1, Mathlib d13f23b7), not FC's own constant.

FC's statement differs from OpenAI's comparator theorem in three ways, all handled here:
(1) it quantifies over EVERY r : ℕ (OpenAI: 4 ≤ r) — r ≤ 3 by monotonicity of `CliqueFree`;
(2) it has NO lower bound on the average degree t (OpenAI: 2 ≤ t) — for 0 < t < 2 we use OpenAI's own maximum-degree
    lemma `maximum_degree_independence` with Δ = 4 on the vertices of degree ≤ 2t (at least half of them), and t = 0 is
    trivial (Real.log 0 = 0, x / 0 = 0);
(3) its average degree is FC's ℚ-valued (∑ deg)/|V|, cast to ℝ; OpenAI's is the real 2|E|/|V| — equal by the handshake lemma.
-/

namespace SimpleGraph

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- The average degree of `G`. -/
noncomputable def averageDegree (G : SimpleGraph α) [DecidableRel G.Adj] : ℚ  :=
  (∑ v, (G.degree v : ℚ)) / (Fintype.card α : ℚ)

end SimpleGraph

namespace Bridge802

open Finset OAI.CliqueFreeIndependence.WeightedGraph

theorem core (r : ℕ) : ∃ c > (0:ℝ), ∀ {V : Type} [Fintype V] (G : SimpleGraph V),
    G.CliqueFree r →
      c * (Real.log (OAI.CliqueFreeLog.averageDegree G) / OAI.CliqueFreeLog.averageDegree G) *
        (Fintype.card V : ℝ) ≤ (G.indepNum : ℝ) := by
  classical
  obtain ⟨c1, hc1, h1⟩ := OAI.CliqueFreeLog.logarithmic_independence_bound (max r 4 - 2 + 2) (by omega)
  obtain ⟨B, hB, htri⟩ := exists_optimizer_triangle_bound.{0} (max r 4 - 2)
  let D : ℝ := 3 + 3*B/2
  have hD : 0 < D := by dsimp [D]; positivity
  have hl4 : 0 < Real.log 4 := Real.log_pos (by norm_num)
  have hc2 : 0 < Real.log 4 / (32*D) := by positivity
  refine ⟨min c1 (Real.log 4 / (32*D)), lt_min hc1 hc2, ?_⟩
  intro V _ G hf
  have hf' : G.CliqueFree (max r 4 - 2 + 2) := hf.mono (by omega)
  have hc0 : 0 ≤ min c1 (Real.log 4 / (32*D)) := (lt_min hc1 hc2).le
  have hn0 : (0:ℝ) ≤ Fintype.card V := Nat.cast_nonneg _
  have hα0 : (0:ℝ) ≤ G.indepNum := Nat.cast_nonneg _
  have hd0 : 0 ≤ OAI.CliqueFreeLog.averageDegree G := by
    simp only [OAI.CliqueFreeLog.averageDegree]; positivity
  rcases le_or_gt 2 (OAI.CliqueFreeLog.averageDegree G) with h2 | h2
  · -- d ≥ 2: OpenAI's theorem
    have hmain := h1 G hf' h2
    have hlog : 0 ≤ Real.log (OAI.CliqueFreeLog.averageDegree G) := Real.log_nonneg (by linarith)
    have hq : 0 ≤ Real.log (OAI.CliqueFreeLog.averageDegree G) / OAI.CliqueFreeLog.averageDegree G :=
      div_nonneg hlog (by linarith)
    calc min c1 (Real.log 4 / (32*D)) * (Real.log (OAI.CliqueFreeLog.averageDegree G) /
            OAI.CliqueFreeLog.averageDegree G) * (Fintype.card V : ℝ)
        ≤ c1 * (Real.log (OAI.CliqueFreeLog.averageDegree G) / OAI.CliqueFreeLog.averageDegree G) *
            (Fintype.card V : ℝ) := by
          apply mul_le_mul_of_nonneg_right _ hn0
          exact mul_le_mul_of_nonneg_right (min_le_left _ _) hq
      _ = c1 * (Fintype.card V : ℝ) * Real.log (OAI.CliqueFreeLog.averageDegree G) /
            OAI.CliqueFreeLog.averageDegree G := by ring
      _ ≤ G.indepNum := hmain
  · rcases eq_or_lt_of_le hd0 with h0 | hpos
    · -- d = 0: the left side is 0
      rw [← h0]; simp
    · -- 0 < d < 2: vertices of degree ≤ 2d < 4, OpenAI's maximum-degree bound with Δ = 4
      set d := OAI.CliqueFreeLog.averageDegree G with hd
      have hn : (Fintype.card V : ℝ) ≠ 0 := by
        intro hn
        have hz : OAI.CliqueFreeLog.averageDegree G = 0 := by simp [OAI.CliqueFreeLog.averageDegree, hn]
        rw [← hd] at hz; linarith
      have hsum : (∑ v, (G.degree v : ℝ)) = (Fintype.card V : ℝ)*d := by
        rw [OAI.CliqueFreeLog.sum_degrees_real]
        simp only [hd, OAI.CliqueFreeLog.averageDegree]
        field_simp
      let A : Finset V := univ.filter fun v ↦ (G.degree v : ℝ) ≤ 2*d
      have hAcard : (Fintype.card V : ℝ)/2 ≤ (Fintype.card (A : Set V) : ℝ) := by
        have he : Fintype.card (A : Set V) = A.card := Fintype.card_coe A
        rw [he]
        exact degree_cutoff_card G hpos hsum
      have hfree : (G.induce (A : Set V)).CliqueFree (max r 4 - 2 + 2) :=
        (G.cliqueFree_induce_iff _ _).2 hf'.cliqueFreeOn
      have hdeg (v : (A : Set V)) : ((G.induce (A : Set V)).degree v : ℝ) ≤ 4 := by
        have hv : (G.degree v : ℝ) ≤ 2*d := (mem_filter.1 v.property).2
        have h4 : (G.degree v : ℝ) ≤ 4 := le_trans hv (by linarith)
        exact (Nat.cast_le.2 (degree_induce_le G A v)).trans h4
      have hmax := maximum_degree_independence (max r 4 - 2) hB.le (by norm_num : (3:ℝ) ≤ 4)
        htri (G.induce (A : Set V)) hfree hdeg
      have hi : ((G.induce (A : Set V)).indepNum : ℝ) ≤ G.indepNum :=
        Nat.cast_le.2 (indepNum_induce_le G A)
      have hratio : Real.log d / d ≤ 1 := by
        rw [div_le_one hpos]
        have := Real.log_le_sub_one_of_pos hpos
        linarith
      have hstep1 : min c1 (Real.log 4 / (32*D)) * (Real.log d / d) * (Fintype.card V : ℝ) ≤
          (Real.log 4 / (32*D)) * (Fintype.card V : ℝ) := by
        apply mul_le_mul_of_nonneg_right _ hn0
        calc min c1 (Real.log 4 / (32*D)) * (Real.log d / d) ≤ min c1 (Real.log 4 / (32*D)) * 1 :=
              mul_le_mul_of_nonneg_left hratio hc0
          _ ≤ Real.log 4 / (32*D) := by rw [mul_one]; exact min_le_right _ _
      have hstep2 : (Real.log 4 / (32*D)) * (Fintype.card V : ℝ) ≤
          (Fintype.card (A : Set V) : ℝ) * Real.log 4 / (4*(3+3*B/2)*4) := by
        have hDD : (4*(3+3*B/2)*4 : ℝ) = 16*D := by dsimp [D]; ring
        rw [hDD]
        have h16 : 0 < 16*D := by positivity
        rw [le_div_iff₀ h16]
        have heq : (Real.log 4 / (32*D)) * (Fintype.card V : ℝ) * (16*D) =
            ((Fintype.card V : ℝ)/2) * Real.log 4 := by field_simp; ring
        rw [heq]
        exact mul_le_mul_of_nonneg_right hAcard hl4.le
      exact hstep1.trans (hstep2.trans (hmax.trans hi))


/-- FC's ℚ-valued average degree, cast to ℝ, is OpenAI's real average degree. -/
lemma averageDegree_cast {V : Type} [Fintype V] [DecidableEq V] (G : _root_.SimpleGraph V) [DecidableRel G.Adj] :
    ((G.averageDegree : ℚ) : ℝ) = OAI.CliqueFreeLog.averageDegree G := by
  classical
  simp only [_root_.SimpleGraph.averageDegree, OAI.CliqueFreeLog.averageDegree]
  push_cast
  congr 1
  convert OAI.CliqueFreeLog.sum_degrees_real G

open Real

namespace Erdos802

open scoped Classical in
/--
Is it true that any $K_r$-free graph on $n$ vertices with average degree $t$ contains an
independent set on
$$\gg_r \frac{\log t}{t}n$$
many vertices?

A conjecture of Ajtai, Erdős, Komlós, and Szemerédi [AEKS81].
-/
theorem erdos_802 : ∀ r : ℕ, ∃ c > (0 : ℝ), ∀ n : ℕ, ∀ G : SimpleGraph (Fin n),
    G.CliqueFree r →
      c * (log G.averageDegree / G.averageDegree) * n ≤ G.indepNum := by
  intro r
  obtain ⟨c, hc, h⟩ := core r
  refine ⟨c, hc, fun n G hG => ?_⟩
  have e := averageDegree_cast G
  have := h G hG
  simp only [Fintype.card_fin] at this
  rw [e]
  exact this

open scoped Classical in
/--
Ajtai, Erdős, Komlós, and Szemerédi [AEKS81] proved that any $K_r$-free graph on $n$ vertices
with average degree $t$ contains an independent set on
$$\gg_r \frac{\log\log(t+1)}{t}n$$
many vertices.
-/
theorem erdos_802.variants.aeks : ∀ r : ℕ, ∃ c > (0 : ℝ), ∀ n : ℕ, ∀ G : SimpleGraph (Fin n),
    G.CliqueFree r →
      c * (log (log (G.averageDegree + 1)) / G.averageDegree) * n ≤ G.indepNum := by
  intro r
  obtain ⟨c, hc, h⟩ := erdos_802 r
  refine ⟨c, hc, fun n G hG => ?_⟩
  refine le_trans ?_ (h n G hG)
  have ht : (0 : ℝ) ≤ (G.averageDegree : ℝ) := by
    simp only [_root_.SimpleGraph.averageDegree]; push_cast; positivity
  rcases eq_or_lt_of_le ht with h0 | hpos
  · rw [← h0]; simp
  · apply mul_le_mul_of_nonneg_right _ (Nat.cast_nonneg _)
    apply mul_le_mul_of_nonneg_left _ hc.le
    apply div_le_div_of_nonneg_right _ hpos.le
    have h1 : 0 < log ((G.averageDegree : ℝ) + 1) := Real.log_pos (by linarith)
    apply Real.log_le_log h1
    have := Real.log_le_sub_one_of_pos (by linarith : (0:ℝ) < (G.averageDegree : ℝ) + 1)
    linarith

open scoped Classical in
/--
Ajtai, Komlós, and Szemerédi [AKS80] proved the conjectured bound when $r = 3$: any
triangle-free graph on $n$ vertices with average degree $t$ contains an independent set on
$$\gg \frac{\log t}{t}n$$
many vertices.
-/
theorem erdos_802.variants.r_eq_three : ∃ c > (0 : ℝ), ∀ n : ℕ, ∀ G : SimpleGraph (Fin n),
    G.CliqueFree 3 →
      c * (log G.averageDegree / G.averageDegree) * n ≤ G.indepNum :=
  erdos_802 3

end Erdos802

end Bridge802

#print axioms Bridge802.core
#print axioms Bridge802.Erdos802.erdos_802
#print axioms Bridge802.Erdos802.erdos_802.variants.aeks
#print axioms Bridge802.Erdos802.erdos_802.variants.r_eq_three
