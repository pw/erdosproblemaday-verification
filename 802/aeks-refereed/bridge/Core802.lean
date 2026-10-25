import OAI.Combinatorics.CliqueFree.Main

/-! Core of the #802 bridge (erdosproblemaday.com, 2026-10-21): OpenAI's theorem holds with NO lower bound on the
average degree and for EVERY r (r ≤ 3 by monotonicity of clique-freeness; 0 < d < 2 by OpenAI's own max-degree lemma
with Δ = 4 on the vertices of degree ≤ 2d; d = 0 trivially). Stated with OpenAI's `averageDegree`. -/

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

end Bridge802

#print axioms Bridge802.core
