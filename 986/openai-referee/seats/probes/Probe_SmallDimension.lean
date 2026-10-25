/- DRAFT probe — compile in the OAI repo after the SharpRamsey closure is built. HIGH PRIORITY.

Observation (formal seat, text reading): the s ≥ 6 tree proves the prime construction UNIFORMLY in the
projective dimension d = i + 3, i.e. for every d ≥ 3:
  SharpRamsey/Construction/PrimeConstruction.lean:14
    theorem actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)
and the paper-facing wrapper's hypothesis `hd : 5 ≤ d` (l.27) is used ONLY to rewrite `d-3+3 = d` (l.28),
which needs 3 ≤ d. Every theorem on the path (Marking.eventually_graph_witness, eventually_iterated_context,
eventually_tracked_step, eventually_no_small_context, InitialExperiment.eventually_source_sizes, classCount,
stepPrefactor) is stated for arbitrary `i : ℕ`; no `≤ i` hypothesis occurs anywhere in the s≥6 tree
(grep). If the kernel accepts the tree, then the theorems below are theorems:
  * PrimeConstruction 3  ⇒ r(4,t) ≥ t^3/(log t)^(2+ε) eventually, for every ε > 0 — the SHARP log exponent
    for r(4,t), which NEITHER paper claims (best published lower bound: Mattheus–Verstraëte t^3/(log t)^4);
  * PrimeConstruction 4  ⇒ an independent second formal proof of the s = 5 lower bound (the r5 tree is a
    separate 482-module development with dimension hard-wired `finrank K V = 5`).
EXPECTED: compiles. If it does, family 170's Lean proves strictly more than its papers state; report
both the stronger statement and the fact that the papers' restriction to s ≥ 5 (resp. d ≥ 5 in the s≥6
paper, `00-introduction.tex` l.115, `01-foundations.tex` l.4, `06-conclusion.tex` l.16) is not used.
If it FAILS, record the exact error — that would locate a hidden dimension dependence. -/
import Mathlib
import OAI.Combinatorics.SharpRamsey.Construction.PrimeConstruction
import OAI.Combinatorics.SharpRamsey.Bounds.FromConstruction

namespace ProbeSmallDimension
open OAI.SharpLogRamsey

theorem primeConstruction_three : LowerTransfer.PrimeConstruction 3 :=
  LowerTransfer.actual_prime_construction 0

theorem primeConstruction_four : LowerTransfer.PrimeConstruction 4 :=
  LowerTransfer.actual_prime_construction 1

/-- r(4,t) = t^3/(log t)^{2+o(1)}: the same 10-line assembly as `main_of_primeConstruction`
(FromConstruction.lean:62-74), whose `6 ≤ s` is only used for `omega` side conditions. -/
theorem mainBounds_four : MainBounds 4 := by
  obtain ⟨C, hC, t₀, ht₀⟩ := Upper.ramsey_upper (by norm_num : 3 ≤ 4)
  refine ⟨C, hC, fun ε hε => ?_⟩
  have hl := LowerTransfer.all_epsilon_lower 3 (by norm_num) primeConstruction_three ε hε
  obtain ⟨t₁, ht₁⟩ := Filter.eventually_atTop.mp hl
  -- defeq: 4-1 ≡ 3, 3+1 ≡ 4, (3-1:ℕ) ≡ (4-2:ℕ); if `exact` balks, insert `norm_num at hl ⊢` first.
  exact ⟨max t₀ t₁, fun t ht => ⟨ht₁ t ((le_max_right _ _).trans ht),
    ht₀ t ((le_max_left _ _).trans ht)⟩⟩

theorem main_four : MainBounds 4 ∧ MainLimit 4 :=
  ⟨mainBounds_four, mainLimit_of_mainBounds 4 mainBounds_four⟩

/-- Cross-check for s = 5 through the s ≥ 6 tree (independent of the r5 tree). -/
theorem mainBounds_five_via_general : MainBounds 5 := by
  obtain ⟨C, hC, t₀, ht₀⟩ := Upper.ramsey_upper (by norm_num : 3 ≤ 5)
  refine ⟨C, hC, fun ε hε => ?_⟩
  have hl := LowerTransfer.all_epsilon_lower 4 (by norm_num) primeConstruction_four ε hε
  obtain ⟨t₁, ht₁⟩ := Filter.eventually_atTop.mp hl
  exact ⟨max t₀ t₁, fun t ht => ⟨ht₁ t ((le_max_right _ _).trans ht),
    ht₀ t ((le_max_left _ _).trans ht)⟩⟩

#print axioms primeConstruction_three
#print axioms main_four
#print axioms mainBounds_five_via_general

end ProbeSmallDimension
