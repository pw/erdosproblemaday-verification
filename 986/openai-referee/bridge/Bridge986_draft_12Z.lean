/-
DRAFT (formal referee seat, 2026-10-20) — NOT COMPILED BY THIS SEAT. To be compiled by the replay seat
inside the OAI repo (Lean v4.34.1, Mathlib d13f23b7), e.g. placed at `lean/Bridge986.lean` and built
with `lake env lean Bridge986.lean`.

Purpose: show that OpenAI's main theorems (family 170) imply the Formal Conjectures statement
`Erdos986.erdos_986` (google-deepmind/formal-conjectures, FormalConjectures/ErdosProblems/986.lean,
main @ commit 75bdce36b881, 2026-09-19) for every s ≥ 5, and nothing for s = 3, 4.

This file is CONDITIONAL: it imports only the two tiny `Model` files (Mathlib-only) and takes the
OpenAI statements as hypotheses, so it is cheap to compile. The unconditional corollary is in
`Bridge986Main.lean` (same directory), which imports the two `Main` modules.

The FC definitions `graphRamsey`, `classicalRamsey` are copied VERBATIM from
FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Ramsey.lean (main, fetched 2026-10-20), only
re-namespaced under `Bridge986.FC`. The FC theorem statement is copied verbatim as a `Prop`.
-/
import Mathlib
import OAI.Combinatorics.SharpRamsey.Model
import OAI.Combinatorics.RamseyFive.Model

namespace Bridge986

namespace FC

/-- VERBATIM (FC `SimpleGraph.graphRamsey`). -/
noncomputable def graphRamsey {α β : Type*} [Fintype α] [Fintype β]
    (G : SimpleGraph α) (H : SimpleGraph β) : ℕ :=
  sInf { n : ℕ | ∀ (C : SimpleGraph (Fin n)), G.IsContained C ∨ H.IsContained Cᶜ }

/-- VERBATIM (FC `SimpleGraph.classicalRamsey`). -/
noncomputable def classicalRamsey (k l : ℕ) : ℕ :=
  graphRamsey (completeGraph (Fin k)) (completeGraph (Fin l))

open Filter in
/-- VERBATIM statement of FC `Erdos986.erdos_986`, as a Prop. -/
def Erdos986Statement : Prop :=
    ∀ (s : ℕ) (_hs : 3 ≤ s),
      ∃ (c C : ℝ), 0 < c ∧ 0 < C ∧
        ∀ᶠ (k : ℕ) in atTop,
          (classicalRamsey s k : ℝ) ≥
            C * (k : ℝ) ^ (s - 1) / (Real.log k) ^ c

open Filter in
/-- The body of `Erdos986Statement` at a single `s`. -/
def Erdos986At (s : ℕ) : Prop :=
  ∃ (c C : ℝ), 0 < c ∧ 0 < C ∧
    ∀ᶠ (k : ℕ) in atTop,
      (classicalRamsey s k : ℝ) ≥
        C * (k : ℝ) ^ (s - 1) / (Real.log k) ^ c

theorem statement_iff : Erdos986Statement ↔ ∀ s, 3 ≤ s → Erdos986At s := Iff.rfl

end FC

open FC

/-! ### The two encodings of r(s,k) agree with FC's `classicalRamsey`. -/

/-- FC's `classicalRamsey` = OpenAI's s ≥ 6 `ramsey` (clique in `Gᶜ` encoding). -/
theorem classicalRamsey_eq_sharpLog (s k : ℕ) :
    classicalRamsey s k = OAI.SharpLogRamsey.ramsey s k := by
  unfold classicalRamsey graphRamsey OAI.SharpLogRamsey.ramsey
  congr 1
  ext n
  simp only [Set.mem_setOf_eq, OAI.SharpLogRamsey.RamseyProperty]
  refine forall_congr' fun C => or_congr ?_ ?_
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    simp [SimpleGraph.CliqueFree]
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    simp [SimpleGraph.CliqueFree]

/-- FC's `classicalRamsey` = OpenAI's s = 5 `ramsey` (`IsNIndepSet` encoding). -/
theorem classicalRamsey_eq_five (s k : ℕ) :
    classicalRamsey s k = OAI.SharpRamseyFive.ramsey s k := by
  unfold classicalRamsey graphRamsey OAI.SharpRamseyFive.ramsey
  congr 1
  ext n
  simp only [Set.mem_setOf_eq, OAI.SharpRamseyFive.RamseyProperty]
  refine forall_congr' fun C => or_congr ?_ ?_
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    simp [SimpleGraph.CliqueFree]
  · rw [← SimpleGraph.not_cliqueFree_iff_top_isContained]
    -- `Cᶜ.IsNClique l B ↔ C.IsNIndepSet l B` is `SimpleGraph.isNClique_compl` (@[simp], Clique.lean:973)
    simp [SimpleGraph.CliqueFree, SimpleGraph.isNClique_compl]

/-! ### s ≥ 6: `MainBounds s` ⇒ FC body at s, with c = (s-2)+1 = s-1, C = 1. -/

theorem erdos986At_of_mainBounds (s : ℕ) (h : OAI.SharpLogRamsey.MainBounds s) :
    Erdos986At s := by
  obtain ⟨_C₀, _hC₀, hb⟩ := h
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  refine ⟨((s - 2 : ℕ) : ℝ) + 1, 1, by positivity, one_pos, ?_⟩
  filter_upwards [Filter.eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  rw [classicalRamsey_eq_sharpLog, one_mul, ge_iff_le]
  exact h1

/-! ### s = 5: `SharpBounds` ⇒ FC body at 5, with c = 3+1 = 4, C = 1. -/

theorem erdos986At_five_of_sharpBounds (h : OAI.SharpRamseyFive.SharpBounds) :
    Erdos986At 5 := by
  obtain ⟨_C₀, _hC₀, hb⟩ := h
  obtain ⟨t₀, ht₀⟩ := hb 1 one_pos
  refine ⟨3 + 1, 1, by norm_num, one_pos, ?_⟩
  filter_upwards [Filter.eventually_ge_atTop t₀] with k hk
  have h1 := (ht₀ k hk).1
  rw [Real.rpow_eq_pow] at h1
  have e : (k : ℝ) ^ (5 - 1) = (k : ℝ) ^ 4 := rfl
  rw [classicalRamsey_eq_five, one_mul, ge_iff_le, e]
  exact h1

/-! ### Assembly for all s ≥ 5, and the EXACT gap to the FC statement (s = 3, 4). -/

theorem erdos986At_ge_five (h5 : OAI.SharpRamseyFive.SharpBounds)
    (h6 : ∀ s, 6 ≤ s → OAI.SharpLogRamsey.MainBounds s) :
    ∀ s, 5 ≤ s → Erdos986At s := by
  intro s hs
  rcases Nat.lt_or_ge s 6 with hlt | hge
  · obtain rfl : s = 5 := by omega
    exact erdos986At_five_of_sharpBounds h5
  · exact erdos986At_of_mainBounds s (h6 s hge)

/-- The gap, stated exactly: given OpenAI's theorems, FC `erdos_986` is EQUIVALENT to its
s = 3 and s = 4 instances. (Those are known — Kim 1995 / Erdős 1961 / Spencer 1977 for s = 3,
Mattheus–Verstraëte 2024 for s = 4, Bradač 2026 for all s ≥ 3 — but are not supplied by family 170.) -/
theorem statement_iff_three_four (h5 : OAI.SharpRamseyFive.SharpBounds)
    (h6 : ∀ s, 6 ≤ s → OAI.SharpLogRamsey.MainBounds s) :
    Erdos986Statement ↔ (Erdos986At 3 ∧ Erdos986At 4) := by
  rw [statement_iff]
  constructor
  · intro h
    exact ⟨h 3 le_rfl, h 4 (by norm_num)⟩
  · rintro ⟨h3, h4⟩ s hs
    rcases Nat.lt_or_ge s 5 with hlt | hge
    · interval_cases s
      · exact h3
      · exact h4
    · exact erdos986At_ge_five h5 h6 s hge

end Bridge986
