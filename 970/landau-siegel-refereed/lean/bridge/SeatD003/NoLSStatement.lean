import Mathlib

/-!
Seat D, erdos cron 2026-10-26 09Z. Mathlib-ONLY statement of Theorem 1 of OpenAI,
"Uniform exclusion of Landau--Siegel zeros" (preprint 1 Oct 2026), p.1, display (1.1):

  "There is an absolute constant c>0 such that every real zero β∈(0,1) of every primitive
   nonprincipal real Dirichlet L-function of conductor q≥3 satisfies (1−β) log q ≥ c."

Clause map: "primitive ... of conductor q" = χ : DirichletCharacter ℂ q with χ.IsPrimitive
(Mathlib: conductor χ = q, so the modulus IS the conductor); "nonprincipal" = χ ≠ 1;
"real" = every value has zero imaginary part; "real zero β∈(0,1)" = 0<β<1 and
χ.LFunction β = 0 (Mathlib's analytic continuation, not the junk-valued LSeries);
"log" = Real.log (natural log).  This module imports only Mathlib and is compiled to an
.olean with nothing of OpenAI's on LEAN_PATH.
-/

namespace SeatD003

def NoLandauSiegel : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

/-- Meaning-preserving variant (≥ instead of ≤, conjunction written as nested ∧ the same way):
must be ACCEPTED (it is definitionally the same proposition: `GE.ge a b` unfolds to `LE.le b a`). -/
def NoLandauSiegel_ge : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → (1 - β) * Real.log q ≥ c

/-! Mutants (each must be REJECTED when OpenAI's term is offered for it). -/

/-- (i) β < 1 weakened to β ≤ 2 (bounds more β). -/
def Mut_beta_le_two : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β ≤ 2 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

/-- (ii) drop the log: c ≤ 1 - β (a far stronger, open claim). -/
def Mut_no_log : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β)

/-- (iii) drop χ ≠ 1 (mathematically equivalent for primitive χ with q ≥ 3, syntactically different). -/
def Mut_drop_ne_one : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

/-- (iv) "real" replaced by "purely imaginary" (.re = 0). -/
def Mut_re_not_im : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).re = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

/-- (v) the junk-value trap: LFunction replaced by the naive LSeries (which is 0 off its
domain of absolute convergence, so this version is FALSE: every β ∈ (0,1) would be a "zero"). -/
def Mut_LSeries : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ LSeries (fun n => χ n) (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

/-- (vi) drop primitivity (then q is only a modulus, not the conductor). -/
def Mut_drop_primitive : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q,
    χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ,
      (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q

end SeatD003
