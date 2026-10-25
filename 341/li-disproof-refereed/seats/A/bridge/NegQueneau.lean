import LeanProject.Erdos341

/-! Referee A: machine-checked bridge from Li's `erdos_341_negative` to the
Formal Conjectures statement `erdos_341` (answer(False) elaborates to `False`).
The statement below is copied verbatim from fc341.lean with `answer(False)` replaced by `False`. -/

open Nat Set Filter

theorem fc_erdos_341_refA :
    False ↔
      ∀ (a : ℕ → ℤ),
        (∀ᶠ n in atTop,
          IsLeast { x | a n < x ∧ x ∉ { a i + a j | (i < j) (j ≤ n) } } (a (n + 1))) →
        let d := fun i ↦ a (i + 1) - a i
        ∃ p > 0, ∀ᶠ m in atTop, d (m + p) = d m := by
  constructor
  · intro h; exact h.elim
  · intro H
    obtain ⟨i0, _, hstep⟩ := Erdos341.least_next_rule_after_fixed_seed
    set e := Erdos341.enumeration with he
    have hmono : StrictMono e := Erdos341.enumeration_strictMono
    have hyp : ∀ᶠ n in atTop,
        IsLeast { x : ℤ | (e n : ℤ) < x ∧ x ∉ { (e i : ℤ) + (e j : ℤ) | (i ≤ n) (j ≤ n) } }
          ((e (n + 1) : ℕ) : ℤ) := by
      rw [Filter.eventually_atTop]
      refine ⟨i0, fun n hn => ?_⟩
      obtain ⟨hlt, hnot, hall⟩ := hstep n hn
      refine ⟨⟨by exact_mod_cast hlt, ?_⟩, ?_⟩
      · rintro ⟨i, hi, j, hj, hij⟩
        apply hnot
        exact ⟨i, hi, j, hj, by exact_mod_cast hij⟩
      · rintro y ⟨hy1, hy2⟩
        by_contra hcon
        push_neg at hcon
        have hy0 : (0 : ℤ) ≤ y := le_trans (by positivity) hy1.le
        obtain ⟨t, rfl⟩ := Int.eq_ofNat_of_zero_le hy0
        have ht1 : e n < t := by exact_mod_cast hy1
        have ht2 : t < e (n + 1) := by exact_mod_cast hcon
        obtain ⟨i, hi, j, hj, hij⟩ := hall t ht1 ht2
        exact hy2 ⟨i, hi, j, hj, by exact_mod_cast hij⟩
    have hP := H (fun n => (e n : ℤ)) hyp
    simp only at hP
    obtain ⟨p, hp, hev⟩ := hP
    rw [Filter.eventually_atTop] at hev
    obtain ⟨N, hN⟩ := hev
    apply Erdos341.gap_not_eventuallyPeriodic
    refine ⟨N, p, hp, fun m hm => ?_⟩
    have h1 := hN m hm
    have hle1 : e (m + p) ≤ e (m + p + 1) := (hmono (by omega)).le
    have hle2 : e m ≤ e (m + 1) := (hmono (by omega)).le
    simp only [Erdos341.gap, Erdos341.gapOf, Erdos341.enumOf] at *
    rw [← he] at *
    have : ((e (m + p + 1) - e (m + p) : ℕ) : ℤ) = ((e (m + 1) - e m : ℕ) : ℤ) := by
      push_cast [hle1, hle2]
      simpa [Nat.add_right_comm] using h1
    exact_mod_cast this

#print axioms fc_erdos_341_refA
