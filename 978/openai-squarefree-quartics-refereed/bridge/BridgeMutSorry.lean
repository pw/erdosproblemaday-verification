import Mathlib
import OAI.NumberTheory.PowerFree.Main

/-!
# Bridge: OpenAI's Lean ⟹ Formal Conjectures' `Erdos978.erdos_978.parts.ii`, `parts.iii`, `variants.sub_two`
(erdos cron seat, 2026-10-22)

The three statements in `namespace Erdos978` below are verbatim copies of `FormalConjectures/ErdosProblems/978.lean` at
google-deepmind/formal-conjectures@a7b87c8d (FC attributes and docstrings removed; `verbatim_check.py` asserts the copies,
whitespace-normalised). `Powerfree` is a verbatim copy of FC's definition in
`FormalConjecturesForMathlib/Algebra/Powerfree.lean` (same commit). FC tags `parts.ii` and `parts.iii` "research solved" and
links OpenAI's Lean, but their proof bodies are `sorry`. The proofs below derive all three from OpenAI's
`OAI.QuarticPowerFree.allDegrees` (positive density of `(d-2)`-power-free values, every `d ≥ 4`). The proofs are ours; the
mathematics is OpenAI's.
-/

open Polynomial Set

section FCPowerfree
variable {M : Type*}

/-- Verbatim copy of Formal Conjectures' `Powerfree` (FormalConjecturesForMathlib/Algebra/Powerfree.lean). -/
def Powerfree [Monoid M] (k : ℕ) (m : M) : Prop :=
  ∀ ⦃x : M⦄, x ^ k ∣ m → IsUnit x

end FCPowerfree

namespace Erdos978Bridge

open OAI.QuarticPowerFree

/-- OpenAI's `PowerFree k a` (no prime `k`-th power divides `a`) implies FC's `Powerfree k a` (every `x` with `x^k ∣ a` is
a unit), for every `k` and every integer `a` (including `a = 0`, where both are false). -/
theorem powerfree_of_PowerFree {k : ℕ} {a : ℤ} (h : PowerFree k a) : Powerfree k a := by
  intro x hx
  by_contra hu
  rw [Int.isUnit_iff_natAbs_eq] at hu
  obtain ⟨p, hp, hpx⟩ := Nat.exists_prime_and_dvd hu
  exact h p hp ((pow_dvd_pow_of_dvd (Int.natCast_dvd.mpr hpx) k).trans hx)

/-- The converse: FC's `Powerfree` implies OpenAI's `PowerFree` (a prime is not a unit). So the two sets coincide. -/
theorem PowerFree_of_powerfree {k : ℕ} {a : ℤ} (h : Powerfree k a) : PowerFree k a := by
  intro p hp hdvd
  have hu := h hdvd
  rw [Int.isUnit_iff_natAbs_eq, Int.natAbs_natCast] at hu
  exact hp.one_lt.ne' hu

/-- FC's local condition (for every prime `p` some `n ≥ 0` has `p^k ∤ f(n)`) implies OpenAI's `LocallyAdmissible f k`
(`ρ_f(p^k) < p^k`): the residue `n mod p^k` is a non-root, so the root set is a proper subset of `range (p^k)`. -/
theorem locallyAdmissible_of_exists (f : ℤ[X]) (k : ℕ)
    (h : ∀ p : ℕ, p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ k ∣ f.eval (n : ℤ)) : LocallyAdmissible f k := by
  intro p hp
  obtain ⟨n, hn⟩ := h p hp
  have hq : 0 < p ^ k := pow_pos hp.pos k
  unfold rho
  calc _ < (Finset.range (p ^ k)).card := by
          apply Finset.card_lt_card
          rw [Finset.filter_ssubset]
          refine ⟨n % p ^ k, Finset.mem_range.mpr (Nat.mod_lt _ hq), ?_⟩
          intro hdiv
          apply hn
          have h1 : ((p ^ k : ℕ) : ℤ) ∣ (n : ℤ) - ((n % p ^ k : ℕ) : ℤ) := by
            rw [Int.natCast_mod]
            exact (Int.mod_modEq (n : ℤ) ((p ^ k : ℕ) : ℤ)).dvd
          have h2 := h1.trans (Polynomial.sub_dvd_eval_sub (n : ℤ) ((n % p ^ k : ℕ) : ℤ) f)
          have h3 : ((p ^ k : ℕ) : ℤ) ∣ f.eval (n : ℤ) := by
            have := dvd_add h2 hdiv
            rwa [sub_add_cancel] at this
          simpa [Nat.cast_pow] using h3
    _ = p ^ k := Finset.card_range _

/-- Gauss: an irreducible integer polynomial of positive degree stays irreducible over `ℚ`. -/
theorem irreducible_map_of_irreducible {f : ℤ[X]} (hi : Irreducible f) (hd : f.natDegree ≠ 0) :
    Irreducible (f.map (Int.castRingHom ℚ)) :=
  (Polynomial.IsPrimitive.Int.irreducible_iff_irreducible_map_cast (hi.isPrimitive hd)).mp hi

/-- A density statement with positive constant forces infinitely many inputs `n ≥ 1` with `f(n)` power-free. -/
theorem infinite_of_densityStatement (f : ℤ[X]) (k : ℕ) (h : DensityStatement f k) :
    {n : ℕ | PowerFree k (f.eval (n : ℤ))}.Infinite := by
  sorry

end Erdos978Bridge

namespace Erdos978Bridge
open OAI.QuarticPowerFree

/-- `X⁴ + 2` is irreducible over `ℚ` (Eisenstein at 2, then Gauss). -/
theorem irreducible_X4_add_2 : Irreducible ((X ^ 4 + C 2 : ℤ[X]).map (Int.castRingHom ℚ)) := by
  have hP : (Ideal.span {(2 : ℤ)}).IsPrime := (Ideal.span_singleton_prime (by norm_num)).mpr Int.prime_two
  have hdeg : (X ^ 4 + C 2 : ℤ[X]).degree = 4 := degree_X_pow_add_C (by norm_num) _
  have hirr : Irreducible (X ^ 4 + C 2 : ℤ[X]) := by
    apply irreducible_of_eisenstein_criterion hP
    · rw [leadingCoeff_X_pow_add_C (by norm_num), Ideal.mem_span_singleton]; norm_num
    · intro n hn
      rw [hdeg] at hn
      have hn4 : n < 4 := by exact_mod_cast hn
      rw [Ideal.mem_span_singleton]
      interval_cases n <;> simp [coeff_X_pow]
    · rw [hdeg]; norm_num
    · rw [Ideal.span_singleton_pow, Ideal.mem_span_singleton]; simp [coeff_X_pow]
    · exact (monic_X_pow_add_C (2 : ℤ) (by norm_num : (4 : ℕ) ≠ 0)).isPrimitive
  exact irreducible_map_of_irreducible hirr (by rw [natDegree_X_pow_add_C]; norm_num)

end Erdos978Bridge

namespace Erdos978

open Erdos978Bridge OAI.QuarticPowerFree

theorem erdos_978.variants.sub_two {f : ℤ[X]} (hi : Irreducible f) (hd : 9 ≤ f.natDegree)
    (hp : ∀ (p : ℕ), p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ (f.natDegree - 2) ∣ f.eval (n : ℤ)) :
    {n : ℕ | Powerfree (f.natDegree - 2) (f.eval (n : ℤ))}.Infinite := by
  have hD := allDegrees f (irreducible_map_of_irreducible hi (by omega)) (by omega)
    (locallyAdmissible_of_exists f _ hp)
  exact (infinite_of_densityStatement f _ hD).mono (fun n hn => powerfree_of_PowerFree hn)

theorem erdos_978.parts.ii :
    ∀ {f : ℤ[X]}, Irreducible f → f.natDegree > 3 →
    (¬ ∃ l : ℕ, f.natDegree = 2 ^ l) → 0 < f.leadingCoeff →
    (∀ (p : ℕ), p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ (f.natDegree - 2) ∣ f.eval (n : ℤ)) →
    {n : ℕ | Powerfree (f.natDegree - 2) (f.eval (n : ℤ))}.Infinite := by
  intro f hi hd _ _ hp
  have hD := allDegrees f (irreducible_map_of_irreducible hi (by omega)) (by omega)
    (locallyAdmissible_of_exists f _ hp)
  exact (infinite_of_densityStatement f _ hD).mono (fun n hn => powerfree_of_PowerFree hn)

theorem erdos_978.parts.iii : {n : ℕ | Squarefree (n ^ 4 + 2)}.Infinite := by
  set f : ℤ[X] := X ^ 4 + C 2 with hf
  have hdeg : f.natDegree = 4 := natDegree_X_pow_add_C
  have hloc : LocallyAdmissible f (f.natDegree - 2) := by
    rw [hdeg]
    refine locallyAdmissible_of_exists f 2 (fun p hp => ⟨0, ?_⟩)
    intro hdvd
    have h2 : (((p ^ 2 : ℕ)) : ℤ) ∣ ((2 : ℕ) : ℤ) := by simpa [hf] using hdvd
    have h3 := Nat.le_of_dvd (by norm_num) (Int.natCast_dvd_natCast.mp h2)
    have h4 := hp.two_le
    nlinarith
  have hD := allDegrees f irreducible_X4_add_2 (by omega) hloc
  rw [hdeg] at hD
  refine (infinite_of_densityStatement f 2 hD).mono (fun n hn => ?_)
  simp only [Set.mem_ofPred_eq] at hn ⊢
  rw [Nat.squarefree_iff_prime_squarefree]
  intro x hx hxx
  apply hn x hx
  have h1 : ((x * x : ℕ) : ℤ) ∣ ((n ^ 4 + 2 : ℕ) : ℤ) := Int.natCast_dvd_natCast.mpr hxx
  simpa [hf, sq] using h1

end Erdos978

/-! Strengthening (ours, same proof): FC's `parts.ii` without the two hypotheses `k ≠ 2^l` and `0 < leadingCoeff`, which
the OpenAI theorem does not need. -/
namespace Erdos978Bridge
open OAI.QuarticPowerFree

theorem parts_ii_without_extra_hypotheses {f : ℤ[X]} (hi : Irreducible f) (hd : 3 < f.natDegree)
    (hp : ∀ (p : ℕ), p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ (f.natDegree - 2) ∣ f.eval (n : ℤ)) :
    {n : ℕ | Powerfree (f.natDegree - 2) (f.eval (n : ℤ))}.Infinite := by
  have hD := allDegrees f (irreducible_map_of_irreducible hi (by omega)) (by omega)
    (locallyAdmissible_of_exists f _ hp)
  exact (infinite_of_densityStatement f _ hD).mono (fun n hn => powerfree_of_PowerFree hn)

end Erdos978Bridge

/-! ## Positive density in FC's own vocabulary (ours)

`Set.partialDensity`, `Set.HasDensity`, `Set.HasPosDensity` below are verbatim copies of FC's definitions in
`FormalConjecturesForMathlib/Data/Set/Density.lean` @ a7b87c8d (docstrings shortened). FC states the `(k-2)` question only as
"infinitely many"; FC's `parts.i` (Hooley's `(k-1)` case) already uses `HasPosDensity`. We prove the `(k-2)` analogue with
the exact density: the Euler product `densityConstant f (d-2)` of OpenAI's statement. -/

open Filter
open scoped Topology

namespace Set

/-- FC: the proportion of elements of `{x ∈ A | x < b}` that lie in `S ∩ A`. -/
@[inline]
noncomputable abbrev partialDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (A : Set β := Set.univ) (b : β) : ℝ :=
  ((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard

/-- FC: `S` has density `α` relative to `A`. -/
def HasDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (α : ℝ) (A : Set β := Set.univ) : Prop :=
  Tendsto (fun (b : β) => S.partialDensity A b) atTop (𝓝 α)

/-- FC: `S` has positive density relative to `A`. -/
def HasPosDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (A : Set β := Set.univ) : Prop :=
  ∃ α > 0, S.HasDensity α A

end Set

namespace Erdos978Bridge
open OAI.QuarticPowerFree

/-- The two notions of power-free agree on `ℤ`, so the two sets coincide. -/
theorem setOf_powerfree_eq (f : ℤ[X]) (k : ℕ) :
    {n : ℕ | Powerfree k (f.eval (n : ℤ))} = {n : ℕ | PowerFree k (f.eval (n : ℤ))} := by
  ext n; exact ⟨PowerFree_of_powerfree, powerfree_of_PowerFree⟩

/-- OpenAI's density statement (inputs `1 ≤ n ≤ X`, real `X`) gives FC's natural density (inputs `0 ≤ n < b`, `b ∈ ℕ`),
with the same constant. -/
theorem hasDensity_of_densityStatement (f : ℤ[X]) (k : ℕ) (h : DensityStatement f k) :
    Set.HasDensity {n : ℕ | Powerfree k (f.eval (n : ℤ))} (densityConstant f k) := by
  classical
  obtain ⟨-, -, ho⟩ := h
  set c := densityConstant f k
  rw [setOf_powerfree_eq]
  set P : ℕ → Prop := fun n => PowerFree k (f.eval (n : ℤ)) with hP
  -- the FC numerator is the filter over `range b`; OpenAI's count is the filter over `Icc 1 b`
  have hnum : ∀ b : ℕ, (({n : ℕ | P n} ∩ Set.univ) ∩ Set.Iio b).ncard = ((Finset.range b).filter P).card := by
    intro b
    rw [← Set.ncard_coe_finset]
    congr 1
    ext n
    simp [Finset.mem_range, and_comm]
  have hden : ∀ b : ℕ, (Set.univ ∩ Set.Iio b).ncard = b := by
    intro b
    have : (Set.univ ∩ Set.Iio b : Set ℕ) = ↑(Finset.range b) := by ext n; simp
    rw [this, Set.ncard_coe_finset, Finset.card_range]
  have hcount : ∀ b : ℕ, count f k (b : ℝ) = ((Finset.Icc 1 b).filter P).card := by
    intro b
    unfold count
    rw [Nat.floor_natCast]
  have hup : ∀ b : ℕ, ((Finset.range b).filter P).card ≤ ((Finset.Icc 1 b).filter P).card + 1 := by
    intro b
    calc ((Finset.range b).filter P).card ≤ ((insert 0 (Finset.Icc 1 b)).filter P).card := by
          apply Finset.card_le_card
          apply Finset.filter_subset_filter
          intro n hn
          rw [Finset.mem_range] at hn
          rw [Finset.mem_insert, Finset.mem_Icc]
          omega
      _ ≤ ((Finset.Icc 1 b).filter P).card + 1 := by
          rw [Finset.filter_insert]
          split_ifs
          · exact Finset.card_insert_le _ _
          · exact Nat.le_succ _
  have hlo : ∀ b : ℕ, ((Finset.Icc 1 b).filter P).card ≤ ((Finset.range b).filter P).card + 1 := by
    intro b
    calc ((Finset.Icc 1 b).filter P).card ≤ ((insert b (Finset.range b)).filter P).card := by
          apply Finset.card_le_card
          apply Finset.filter_subset_filter
          intro n hn
          rw [Finset.mem_Icc] at hn
          rw [Finset.mem_insert, Finset.mem_range]
          omega
      _ ≤ ((Finset.range b).filter P).card + 1 := by
          rw [Finset.filter_insert]
          split_ifs
          · exact Finset.card_insert_le _ _
          · exact Nat.le_succ _
  -- OpenAI's o(X) along the naturals
  have ho' : (fun b : ℕ => (count f k (b : ℝ) : ℝ) - c * (b : ℝ)) =o[atTop] (fun b : ℕ => (b : ℝ)) :=
    ho.comp_tendsto tendsto_natCast_atTop_atTop
  have hdiff : (fun b : ℕ => (((Finset.range b).filter P).card : ℝ) - (count f k (b : ℝ) : ℝ))
      =o[atTop] (fun b : ℕ => (b : ℝ)) := by
    have h1 : (fun _ : ℕ => (1 : ℝ)) =o[atTop] (fun b : ℕ => (b : ℝ)) := by
      rw [Asymptotics.isLittleO_one_left_iff]
      simpa using tendsto_natCast_atTop_atTop
    refine Asymptotics.IsBigO.trans_isLittleO ?_ h1
    refine Asymptotics.IsBigO.of_bound 1 (Filter.Eventually.of_forall fun b => ?_)
    rw [hcount b, Real.norm_eq_abs, Real.norm_eq_abs, abs_one, mul_one, abs_le]
    have := hup b; have := hlo b
    constructor
    · have : (((Finset.Icc 1 b).filter P).card : ℝ) ≤ ((Finset.range b).filter P).card + 1 := by exact_mod_cast hlo b
      linarith
    · have : (((Finset.range b).filter P).card : ℝ) ≤ ((Finset.Icc 1 b).filter P).card + 1 := by exact_mod_cast hup b
      linarith
  have hsum := (hdiff.add ho').tendsto_div_nhds_zero
  have hlim : Tendsto (fun b : ℕ => (((Finset.range b).filter P).card : ℝ) / (b : ℝ)) atTop (𝓝 c) := by
    have h2 := hsum.add_const c
    rw [zero_add] at h2
    refine h2.congr' ?_
    filter_upwards [Filter.eventually_gt_atTop 0] with b hb
    have hb' : (b : ℝ) ≠ 0 := by exact_mod_cast hb.ne'
    field_simp
    ring
  unfold Set.HasDensity
  refine hlim.congr' (Filter.Eventually.of_forall fun b => ?_)
  simp only [Set.partialDensity]
  rw [hnum b, hden b]

end Erdos978Bridge

namespace Erdos978

open Erdos978Bridge OAI.QuarticPowerFree

/-- (ours) The `(k-2)`-power-free values of an irreducible integer polynomial of degree `k ≥ 4` with no fixed prime
`(k-2)`-th power divisor have positive natural density in FC's sense — with density equal to OpenAI's Euler product. FC
states the `(k-2)` question only as `parts.ii` ("infinitely many"); this is the density form, in the vocabulary of FC's
`parts.i`. No `k ≠ 2^l` and no sign condition. -/
theorem erdos_978.parts.ii_density {f : ℤ[X]} (hi : Irreducible f) (hd : 3 < f.natDegree)
    (hp : ∀ (p : ℕ), p.Prime → ∃ n : ℕ, ¬ (p : ℤ) ^ (f.natDegree - 2) ∣ f.eval (n : ℤ)) :
    Set.HasDensity {n : ℕ | Powerfree (f.natDegree - 2) (f.eval (n : ℤ))}
        (densityConstant f (f.natDegree - 2)) ∧
      Set.HasPosDensity {n : ℕ | Powerfree (f.natDegree - 2) (f.eval (n : ℤ))} := by
  have hD := allDegrees f (irreducible_map_of_irreducible hi (by omega)) (by omega)
    (locallyAdmissible_of_exists f _ hp)
  have hpos := hD.2.1
  have h := hasDensity_of_densityStatement f _ hD
  exact ⟨h, ⟨_, hpos, h⟩⟩

end Erdos978
