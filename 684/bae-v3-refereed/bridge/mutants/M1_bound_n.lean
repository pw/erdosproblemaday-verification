import Erdos684Lean
/-!
# Bridge from Bae's erdos684-lean (v3-arxiv) to Formal Conjectures' Erdős 684 vocabulary
erdos cron seat, 2026-10-31. Ours. `smallPrimePart` and `FCUpperBound` are copied verbatim from
FormalConjectures/ErdosProblems/684.lean (commit d9f6ffa8); `check_verbatim.py` diffs them.
-/
open Filter Real

namespace Bridge684

/-- Formal Conjectures' definition, verbatim. -/
def smallPrimePart (n k : ℕ) : ℕ :=
  ∏ p ∈ Nat.primesLE k, p ^ ((n.choose k).factorization p)

/-- Formal Conjectures' `erdos_684.upper_bound` statement (APSSV, constant 514), verbatim, as a Prop. -/
def FCUpperBound : Prop :=
  ∀ᶠ n : ℕ in atTop, ∃ k ≤ n,
      (k : ℝ) ≤ 514 * (log (n : ℝ)) ^ 2 ∧ n ^ 2 < smallPrimePart n k

theorem smallPrimePart_eq_uPart : smallPrimePart = Erdos684.uPart := rfl

/-- Bae's theorem in FC's vocabulary, unconditional, with no `f` and hence no `⊤`:
for every `C`, infinitely many `n` have `u(n,k) ≤ n²` for every `1 ≤ k ≤ min(n, C log n)`. -/
theorem erdos_684_unbounded_fc (C : ℝ) :
    ∃ᶠ n : ℕ in atTop, ∀ k : ℕ, 1 ≤ k → k ≤ n → (k : ℝ) ≤ C * log (n : ℝ) →
      smallPrimePart n k ≤ n := by
  refine (Erdos684.unbounded_unconditional C).mono fun n hn k hk1 hkn hkC => ?_
  exact (Erdos684.lt_fThr_iff.mp (hn k hkC)) k hk1 le_rfl hkn

/-- The same with Bae's rate `(1/2 − ε) log n · log log n / log log log n`. -/
theorem erdos_684_rate_fc (ε : ℝ) (hε : 0 < ε) :
    ∃ᶠ n : ℕ in atTop, ∀ k : ℕ, 1 ≤ k → k ≤ n →
      (k : ℝ) ≤ (1 / 2 - ε) * log n * log (log n) / log (log (log n)) →
      smallPrimePart n k ≤ n ^ 2 := by
  refine (Erdos684.main_theorem_unconditional ε hε).mono fun n hn k hk1 hkn hkC => ?_
  exact (Erdos684.lt_fThr_iff.mp (hn k hkC)) k hk1 le_rfl hkn

/-- Under FC's upper bound, `f(n)` is eventually finite. -/
theorem fThr_ne_top_eventually (h : FCUpperBound) :
    ∀ᶠ n : ℕ in atTop, Erdos684.fThr n ≠ ⊤ := by
  filter_upwards [h, eventually_ge_atTop 1] with n hn hn1
  obtain ⟨k, hkn, -, hk⟩ := hn
  rw [Ne, Erdos684.fThr_eq_top_iff]
  intro hall
  rcases Nat.eq_zero_or_pos k with rfl | hk1
  · have h1 : 1 ≤ n ^ 2 := Nat.one_le_pow _ _ hn1
    have h0 : smallPrimePart n 0 = 1 := by simp [smallPrimePart]
    omega
  · exact absurd (hall k hk1 hkn) (not_le.mpr hk)

/-- Finite-valued unboundedness: given FC's (APSSV) upper bound, for every `C` infinitely many `n`
have `f(n)` FINITE and `> C log n`. -/
theorem unbounded_finite (h : FCUpperBound) (C : ℝ) :
    ∃ᶠ n : ℕ in atTop, Erdos684.fThr n ≠ ⊤ ∧
      ∀ k : ℕ, (k : ℝ) ≤ C * log (n : ℝ) → (k : ℕ∞) < Erdos684.fThr n :=
  ((Erdos684.unbounded_unconditional C).and_eventually (fThr_ne_top_eventually h)).mono
    fun _ ⟨h1, h2⟩ => ⟨h2, h1⟩

end Bridge684

#print axioms Bridge684.erdos_684_unbounded_fc
#print axioms Bridge684.erdos_684_rate_fc
#print axioms Bridge684.fThr_ne_top_eventually
#print axioms Bridge684.unbounded_finite
#print axioms Bridge684.smallPrimePart_eq_uPart
