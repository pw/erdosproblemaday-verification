import OAI.NumberTheory.JointDickman.PaperMain

/-!
# Bridge core (erdosproblemaday.com, 2026-10-22): Erdős #371 and #928 from OpenAI's joint Dickman law

Everything here is CONDITIONAL on OpenAI's proposition `OAI.JointDickman.JointDickmanLaw` (resp.
`IncreasingOrderLaw`), imported from the low-level module `OAI.NumberTheory.JointDickman.Amplification.Ordering`
(which only defines the statements and proves facts about the Dickman CDF). `Bridge371.lean` instantiates the
hypotheses with OpenAI's unconditional theorems.

`Set.partialDensity` and `Set.HasDensity` below are copied VERBATIM (text, binder names, docstrings, the `@[inline]`
attribute) from google-deepmind/formal-conjectures @ 3b7c94ec, `FormalConjecturesForMathlib/Data/Set/Density.lean`,
so `{n | …}.HasDensity d` means exactly what it means in Formal Conjectures (`|S ∩ [0,b)| / |[0,b)| → d` as `b → ∞`
through ℕ). OpenAI's Mathlib d13f23b7 has no `Set.partialDensity` / `Set.HasDensity`, so dot notation resolves as in FC.

#928 (erdosproblems.com, "Formalised statement? No" as of 2026-10-22) asks, for α, β ∈ (0,1), whether the density of
n with P(n) < n^α and P(n+1) < (n+1)^β exists (and whether it is ρ(1/α)ρ(1/β)). Its thresholds differ from OpenAI's
Theorem 1.1 (strict inequalities; (n+1)^β rather than n^β); `erdos_928_of_jointLaw` closes that gap by a sandwich using
continuity and monotonicity of OpenAI's `dickmanCDF`.
-/

open Filter

open scoped Topology

namespace Set

/--
Given a set `S` and an element `b` in an order `β`, where all intervals bounded above are finite,
we define the partial density of `S` (relative to a set `A`) to be the proportion of elements in
`{x ∈ A | x < b}` that lie in `S ∩ A`.

This definition was inspired from https://github.com/b-mehta/unit-fractions
-/
@[inline]
noncomputable abbrev partialDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (A : Set β := Set.univ) (b : β) : ℝ :=
  ((S ∩ A) ∩ Iio b).ncard / (A ∩ Iio b).ncard

/--
A set `S` in an order `β` where all intervals bounded above are finite is said to have
density `α : ℝ` (relative to a set `A`) if the proportion of `x ∈ S` such that `x < n`
in `A` tends to `α` as `n → ∞`.

When `β = ℕ` this by default defines the natural density of a set
(i.e., relative to all of `ℕ`).
-/
def HasDensity {β : Type*} [Preorder β] [LocallyFiniteOrderBot β]
    (S : Set β) (α : ℝ) (A : Set β := Set.univ) : Prop :=
  Tendsto (fun (b : β) => S.partialDensity A b) atTop (𝓝 α)

end Set

namespace EPAD371

open OAI OAI.JointDickman

/-- FC's partial density of `{n | P n}` at `b` differs from OpenAI's `realDensity P b` by at most `2 / b`:
`[0,b)` and `[2,b]` differ by `{0,1}` on one side and `{b}` on the other. -/
theorem partialDensity_sub_realDensity (P : ℕ → Prop) (b : ℕ) (hb : 1 ≤ b) :
    |({n : ℕ | P n}.partialDensity Set.univ b) - realDensity P (b : ℝ)| ≤ 2 / b := by
  classical
  have hbR : (0 : ℝ) < b := by exact_mod_cast hb
  have hden : ((Set.univ : Set ℕ) ∩ Set.Iio b).ncard = b := by
    rw [Set.univ_inter, ← Finset.coe_range, Set.ncard_coe_finset, Finset.card_range]
  have hnum : (({n : ℕ | P n} ∩ Set.univ) ∩ Set.Iio b).ncard = ((Finset.range b).filter P).card := by
    rw [← Set.ncard_coe_finset]
    congr 1
    ext n
    simp [Finset.mem_range, and_comm]
  have hfl : ⌊(b : ℝ)⌋₊ = b := Nat.floor_natCast b
  set A := ((Finset.range b).filter P).card with hA
  set E := ((Finset.Icc 2 b).filter P).card with hE
  have hE' : empiricalCount P ⌊(b : ℝ)⌋₊ = E := by
    rw [hfl, empiricalCount, hE]
  -- A ≤ E + 2 and E ≤ A + 1
  have h1 : A ≤ E + 2 := by
    have hsub : (Finset.range b).filter P ⊆ ((Finset.Icc 2 b).filter P) ∪ {0, 1} := by
      intro n hn
      simp only [Finset.mem_filter, Finset.mem_range] at hn
      by_cases h2 : 2 ≤ n
      · exact Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨Finset.mem_Icc.mpr ⟨h2, hn.1.le⟩, hn.2⟩)
      · apply Finset.mem_union_right
        interval_cases n <;> simp
    calc A ≤ (((Finset.Icc 2 b).filter P) ∪ {0, 1}).card := Finset.card_le_card hsub
      _ ≤ E + ({0, 1} : Finset ℕ).card := Finset.card_union_le _ _
      _ ≤ E + 2 := by
        have : ({0, 1} : Finset ℕ).card ≤ 2 := Finset.card_le_two
        omega
  have h2 : E ≤ A + 1 := by
    have hsub : (Finset.Icc 2 b).filter P ⊆ ((Finset.range b).filter P) ∪ {b} := by
      intro n hn
      simp only [Finset.mem_filter, Finset.mem_Icc] at hn
      by_cases hlt : n < b
      · exact Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨Finset.mem_range.mpr hlt, hn.2⟩)
      · apply Finset.mem_union_right
        simp only [Finset.mem_singleton]
        omega
    calc E ≤ (((Finset.range b).filter P) ∪ {b}).card := Finset.card_le_card hsub
      _ ≤ A + ({b} : Finset ℕ).card := Finset.card_union_le _ _
      _ = A + 1 := by rw [Finset.card_singleton]
  have hpd : ({n : ℕ | P n}.partialDensity Set.univ b) = (A : ℝ) / b := by
    rw [Set.partialDensity, hnum, hden]
  have hrd : realDensity P (b : ℝ) = (E : ℝ) / b := by
    rw [realDensity, hE']
  rw [hpd, hrd, ← sub_div, abs_div, abs_of_pos hbR]
  apply div_le_div_of_nonneg_right _ hbR.le
  have h1' : (A : ℝ) ≤ E + 2 := by exact_mod_cast h1
  have h2' : (E : ℝ) ≤ A + 1 := by exact_mod_cast h2
  rw [abs_le]
  constructor <;> linarith

/-- OpenAI's real-endpoint natural density limit implies Formal Conjectures' `HasDensity`. -/
theorem hasDensity_of_realDensity {P : ℕ → Prop} {d : ℝ}
    (h : Tendsto (realDensity P) atTop (𝓝 d)) : {n : ℕ | P n}.HasDensity d := by
  unfold Set.HasDensity
  have hnat : Tendsto (fun b : ℕ => realDensity P (b : ℝ)) atTop (𝓝 d) :=
    h.comp tendsto_natCast_atTop_atTop
  have hsmall : Tendsto (fun b : ℕ => (2 : ℝ) / b) atTop (𝓝 0) := by
    simpa using (tendsto_const_div_atTop_nhds_zero_nat (2 : ℝ))
  have hdiff : Tendsto (fun b : ℕ =>
      ({n : ℕ | P n}.partialDensity Set.univ b) - realDensity P (b : ℝ)) atTop (𝓝 0) := by
    apply squeeze_zero_norm' _ hsmall
    filter_upwards [eventually_ge_atTop 1] with b hb
    rw [Real.norm_eq_abs]
    exact partialDensity_sub_realDensity P b hb
  have := hdiff.add hnat
  simp only [zero_add, sub_add_cancel] at this
  exact this

/-- Comparison of real densities when `P → Q` holds from `n₀` on (finitely many exceptions). -/
theorem realDensity_le_of_eventually {P Q : ℕ → Prop} (n₀ : ℕ) (hPQ : ∀ n, n₀ ≤ n → P n → Q n)
    {X : ℝ} (hX : 0 < X) : realDensity P X ≤ realDensity Q X + n₀ / X := by
  classical
  unfold realDensity empiricalCount
  rw [← add_div]
  apply div_le_div_of_nonneg_right _ hX.le
  have hsub : (Finset.Icc 2 ⌊X⌋₊).filter P ⊆ ((Finset.Icc 2 ⌊X⌋₊).filter Q) ∪ Finset.range n₀ := by
    intro n hn
    simp only [Finset.mem_filter] at hn
    by_cases h : n₀ ≤ n
    · exact Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨hn.1, hPQ n h hn.2⟩)
    · exact Finset.mem_union_right _ (Finset.mem_range.mpr (by omega))
  have := (Finset.card_le_card hsub).trans (Finset.card_union_le _ _)
  rw [Finset.card_range] at this
  exact_mod_cast this

/-- Monotonicity of real density under inclusion for `n ≥ 2` (no exceptions). -/
theorem realDensity_mono {P Q : ℕ → Prop} (hPQ : ∀ n, 2 ≤ n → P n → Q n) {X : ℝ} (hX : 0 ≤ X) :
    realDensity P X ≤ realDensity Q X := by
  classical
  unfold realDensity empiricalCount
  apply div_le_div_of_nonneg_right _ hX
  apply Nat.cast_le.mpr
  apply Finset.card_le_card
  intro n hn
  simp only [Finset.mem_filter, Finset.mem_Icc] at hn ⊢
  exact ⟨hn.1, hPQ n hn.1.1 hn.2⟩

/-- `(n+1)^β ≤ n^(β+δ)` for all large `n`. -/
theorem eventually_succ_rpow_le {β δ : ℝ} (hβ : 0 ≤ β) (hδ : 0 < δ) :
    ∃ n₀ : ℕ, ∀ n : ℕ, n₀ ≤ n → (((n + 1 : ℕ) : ℝ)) ^ β ≤ (n : ℝ) ^ (β + δ) := by
  have ht : Tendsto (fun n : ℕ => (n : ℝ) ^ δ) atTop atTop :=
    (tendsto_rpow_atTop hδ).comp tendsto_natCast_atTop_atTop
  have hev := (ht.eventually_ge_atTop ((2 : ℝ) ^ β)).and (eventually_ge_atTop 1)
  obtain ⟨n₀, hn₀⟩ := eventually_atTop.mp hev
  refine ⟨n₀, fun n hn => ?_⟩
  obtain ⟨h2, h1⟩ := hn₀ n hn
  have hn0 : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hle : ((n + 1 : ℕ) : ℝ) ≤ 2 * n := by
    push_cast
    have : (1 : ℝ) ≤ n := by exact_mod_cast h1
    linarith
  calc (((n + 1 : ℕ) : ℝ)) ^ β ≤ (2 * (n : ℝ)) ^ β :=
        Real.rpow_le_rpow (by positivity) hle hβ
    _ = (2 : ℝ) ^ β * (n : ℝ) ^ β := Real.mul_rpow (by norm_num) hn0.le
    _ ≤ (n : ℝ) ^ δ * (n : ℝ) ^ β := by
        apply mul_le_mul_of_nonneg_right h2 (by positivity)
    _ = (n : ℝ) ^ (β + δ) := by rw [Real.rpow_add hn0, mul_comm]

/-- The #928 event, exactly as Erdős posed it: P(n) < n^α and P(n+1) < (n+1)^β. -/
def event928 (α β : ℝ) (n : ℕ) : Prop :=
  (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧ ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ β

/-- #928 from the joint law: for α, β ∈ (0,1) the density of {n : P(n) < n^α, P(n+1) < (n+1)^β}
exists (as an ordinary real-endpoint limit) and equals ρ(1/α)ρ(1/β). -/
theorem realDensity_event928 (hJ : JointDickmanLaw) {α β : ℝ} (hα : 0 < α) (hα1 : α < 1)
    (hβ : 0 < β) (hβ1 : β < 1) :
    Tendsto (realDensity (event928 α β)) atTop (𝓝 (dickmanCDF α * dickmanCDF β)) := by
  set L := dickmanCDF α * dickmanCDF β with hL
  -- the moving-event limit, phrased with dickmanCDF
  have hmov : ∀ a b : ℝ, 0 < a → a < 1 → 0 < b → b < 1 →
      Tendsto (realDensity (movingEvent a b)) atTop (𝓝 (dickmanCDF a * dickmanCDF b)) := by
    intro a b ha ha1 hb hb1
    have := hJ a b ha ha1 hb hb1
    simpa [dickmanCDF, not_le.mpr ha, not_le.mpr hb] using this
  have hcont : Continuous (fun p : ℝ × ℝ => dickmanCDF p.1 * dickmanCDF p.2) :=
    (dickmanCDF_continuous.comp continuous_fst).mul (dickmanCDF_continuous.comp continuous_snd)
  rw [tendsto_order]
  constructor
  · -- lower bound: shrink both exponents
    intro a' ha'
    have hlim : Tendsto (fun δ : ℝ => dickmanCDF (α - δ) * dickmanCDF (β - δ)) (𝓝 0) (𝓝 L) := by
      have hc : Continuous (fun δ : ℝ => dickmanCDF (α - δ) * dickmanCDF (β - δ)) :=
        hcont.comp ((continuous_const.sub continuous_id).prodMk (continuous_const.sub continuous_id))
      simpa [hL] using hc.tendsto 0
    have hev : ∀ᶠ δ in 𝓝[>] (0 : ℝ), a' < dickmanCDF (α - δ) * dickmanCDF (β - δ) ∧ δ < min α β :=
      ((hlim.eventually (lt_mem_nhds ha')).filter_mono nhdsWithin_le_nhds).and
        ((gt_mem_nhds (lt_min hα hβ)).filter_mono nhdsWithin_le_nhds)
    obtain ⟨δ, ⟨hδa, hδm⟩, hδpos⟩ := (hev.and self_mem_nhdsWithin).exists
    have hδα : δ < α := lt_of_lt_of_le hδm (min_le_left _ _)
    have hδβ : δ < β := lt_of_lt_of_le hδm (min_le_right _ _)
    have hlow := hmov (α - δ) (β - δ) (by linarith) (by linarith) (by linarith) (by linarith)
    filter_upwards [hlow.eventually (lt_mem_nhds hδa), eventually_ge_atTop (0 : ℝ)] with X hX hX0
    refine lt_of_lt_of_le hX (realDensity_mono (fun n hn hP => ?_) hX0)
    have hn1 : (1 : ℝ) < n := by exact_mod_cast (show 1 < n by omega)
    have hn0 : (0 : ℝ) < n := by linarith
    obtain ⟨h1, h2⟩ := hP
    refine ⟨lt_of_le_of_lt h1 (Real.rpow_lt_rpow_of_exponent_lt hn1 (by linarith)), ?_⟩
    calc ((n + 1).maxPrimeFac : ℝ) ≤ (n : ℝ) ^ (β - δ) := h2
      _ < (n : ℝ) ^ β := Real.rpow_lt_rpow_of_exponent_lt hn1 (by linarith)
      _ ≤ (((n + 1 : ℕ) : ℝ)) ^ β :=
          Real.rpow_le_rpow hn0.le (by push_cast; linarith) hβ.le
  · -- upper bound: enlarge the second exponent
    intro a' ha'
    have hlim : Tendsto (fun δ : ℝ => dickmanCDF α * dickmanCDF (β + δ)) (𝓝 0) (𝓝 L) := by
      have hc : Continuous (fun δ : ℝ => dickmanCDF α * dickmanCDF (β + δ)) :=
        continuous_const.mul (dickmanCDF_continuous.comp (continuous_const.add continuous_id))
      simpa [hL] using hc.tendsto 0
    set m := (L + a') / 2 with hm
    have hLm : L < m := by rw [hm]; linarith
    have hma : m < a' := by rw [hm]; linarith
    have hev : ∀ᶠ δ in 𝓝[>] (0 : ℝ), dickmanCDF α * dickmanCDF (β + δ) < m ∧ δ < 1 - β :=
      ((hlim.eventually (gt_mem_nhds hLm)).filter_mono nhdsWithin_le_nhds).and
        ((gt_mem_nhds (show (0:ℝ) < 1 - β by linarith)).filter_mono nhdsWithin_le_nhds)
    obtain ⟨δ, ⟨hδm, hδ1⟩, hδpos⟩ := (hev.and self_mem_nhdsWithin).exists
    have hδpos' : (0 : ℝ) < δ := hδpos
    obtain ⟨n₀, hn₀⟩ := eventually_succ_rpow_le (β := β) hβ.le hδpos'
    have hup := hmov α (β + δ) hα hα1 (by linarith) (by linarith)
    have hsmall : Tendsto (fun X : ℝ => (n₀ : ℝ) / X) atTop (𝓝 0) :=
      tendsto_const_nhds.div_atTop tendsto_id
    filter_upwards [hup.eventually (gt_mem_nhds hδm), hsmall.eventually (gt_mem_nhds (sub_pos.mpr hma)),
      eventually_gt_atTop (0 : ℝ)] with X hX1 hX2 hX0
    have hcmp := realDensity_le_of_eventually (P := event928 α β) (Q := movingEvent α (β + δ)) n₀
      (fun n hn hP => ⟨hP.1.le, (hP.2.le.trans (hn₀ n hn))⟩) hX0
    linarith

/-- Erdős #928 (as posed), in Formal Conjectures' density language, from the joint law. -/
theorem erdos_928_of_jointLaw (hJ : JointDickmanLaw) {α β : ℝ} (hα : 0 < α) (hα1 : α < 1)
    (hβ : 0 < β) (hβ1 : β < 1) :
    {n : ℕ | (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧
        ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ β}.HasDensity
      (Erdos970.NumberTheoryLean.Dickman.rho (1 / α) * Erdos970.NumberTheoryLean.Dickman.rho (1 / β)) := by
  have h := realDensity_event928 hJ hα hα1 hβ hβ1
  simp only [dickmanCDF, not_le.mpr hα, not_le.mpr hβ, ite_false] at h
  exact hasDensity_of_realDensity h

end EPAD371

namespace Erdos371

/--
Let $P(n)$ denote the largest prime factor of $n$. Show that the set of $n$
with $P(n+1) > P(n)$ has density $\frac{1}{2}$.

This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked Lean proof.
-/
theorem erdos_371_of_increasingOrderLaw (h : OAI.JointDickman.IncreasingOrderLaw) :
    { n | Nat.maxPrimeFac (n + 1) > Nat.maxPrimeFac n }.HasDensity (1/2) := by
  have h' : Tendsto (OAI.JointDickman.realDensity (fun n => Nat.maxPrimeFac (n + 1) > Nat.maxPrimeFac n))
      atTop (𝓝 (1 / 2)) := h
  exact EPAD371.hasDensity_of_realDensity h'

end Erdos371

/-! ## Unconditional instantiations from OpenAI's library (`OAI.NumberTheory.JointDickman.UnconditionalMain`) -/

namespace Erdos371

/--
Let $P(n)$ denote the largest prime factor of $n$. Show that the set of $n$
with $P(n+1) > P(n)$ has density $\frac{1}{2}$.

This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked Lean proof.
-/
theorem erdos_371 :
    { n | Nat.maxPrimeFac (n + 1) > Nat.maxPrimeFac n }.HasDensity (1/2) := by
  exact erdos_371_of_increasingOrderLaw OAI.JointDickman.increasingOrderLaw_unconditional

end Erdos371

namespace EPAD371

/-- Erdős #928, as posed (strict inequalities, threshold (n+1)^β): for α, β ∈ (0,1) the density of
{n : P(n) < n^α, P(n+1) < (n+1)^β} exists and equals ρ(1/α)ρ(1/β). -/
theorem erdos_928 {α β : ℝ} (hα : 0 < α) (hα1 : α < 1) (hβ : 0 < β) (hβ1 : β < 1) :
    {n : ℕ | (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧
        ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ (β / 2)}.HasDensity
      (OAI.Erdos970.NumberTheoryLean.Dickman.rho (1 / α) *
        OAI.Erdos970.NumberTheoryLean.Dickman.rho (1 / β)) :=
  erdos_928_of_jointLaw OAI.JointDickman.jointDickmanLaw_unconditional hα hα1 hβ hβ1

/-- #928's literal question: the density exists. -/
theorem erdos_928_exists {α β : ℝ} (hα : 0 < α) (hα1 : α < 1) (hβ : 0 < β) (hβ1 : β < 1) :
    ∃ d : ℝ, {n : ℕ | (n.maxPrimeFac : ℝ) < (n : ℝ) ^ α ∧
        ((n + 1).maxPrimeFac : ℝ) < (((n + 1 : ℕ) : ℝ)) ^ β}.HasDensity d :=
  ⟨_, erdos_928 hα hα1 hβ hβ1⟩

end EPAD371
