import Mathlib
import OAI.NumberTheory.GaussianMoat.Main

/-!
# Bridge: OpenAI's Lean ⟹ Formal Conjectures' `Erdos952.erdos_952` (erdos cron seat, 2026-10-22)

The statement of `erdos_952` below is a verbatim copy of `FormalConjectures/ErdosProblems/952.lean` at
google-deepmind/formal-conjectures@3b7c94ec (FC attributes and docstring removed; `verbatim_check.py` asserts the copy,
whitespace-normalised). FC tags it "research solved" and links OpenAI's Lean, but its proof body is `sorry`. The proof
below derives FC's statement from OpenAI's `OAI.GaussianMoat.fullMain` (first conjunct, `MainEndpoint`) with step bound
`D = √C`. The proof is ours; the mathematics is OpenAI's.
-/

namespace Erdos952Mut

/-- The Euclidean distance between the images of two Gaussian integers in `ℂ` is the square root of the norm of
their difference. -/
theorem dist_toComplex_eq_sqrt_norm (a b : GaussianInt) :
    dist (a : ℂ) (b : ℂ) = Real.sqrt ((a - b).norm : ℝ) := by
  rw [Complex.dist_eq, ← GaussianInt.toComplex_sub, Complex.norm_def, GaussianInt.intCast_real_norm]

theorem erdos_952 :
  ¬ ∃ (x : ℕ → GaussianInt) (C : ℤ),
    Function.Injective x ∧
      ∀ n, Prime (x n) ∧ (x (n + 1) - x n).norm < C + (x n).norm := by
  rintro ⟨x, C, hinj, h⟩
  refine OAI.GaussianMoat.fullMain.1 (Real.sqrt (C : ℝ)) x (fun t => (h t).1.irreducible) hinj ?_
  intro t
  rw [dist_toComplex_eq_sqrt_norm]
  exact Real.sqrt_le_sqrt (by exact_mod_cast (h t).2.le)

/-- The uniform form in FC's vocabulary: for every integer bound `C` there is `B` such that every injective sequence
of Gaussian primes `x 0, …, x (n-1)` (`Prime`, not `Irreducible`) whose consecutive differences have norm `< C` has
`n ≤ B`. Derived from the second conjunct of `fullMain` (`UniformEndpoint`). -/
theorem erdos_952_uniform (C : ℤ) : ∃ B : ℕ, ∀ (n : ℕ) (x : Fin n → GaussianInt),
    Function.Injective x → (∀ i, Prime (x i)) →
    (∀ i j : Fin n, j.val = i.val + 1 → (x j - x i).norm < C) → n ≤ B := by
  obtain ⟨B, -, hB⟩ := OAI.GaussianMoat.fullMain.2 (Real.sqrt (C : ℝ))
  refine ⟨B, fun n x hinj hp hstep => hB n x (fun i => (hp i).irreducible) hinj fun i j hij => ?_⟩
  rw [dist_toComplex_eq_sqrt_norm]
  exact Real.sqrt_le_sqrt (by exact_mod_cast (hstep i j hij).le)

end Erdos952Mut
