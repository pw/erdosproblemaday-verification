import Erdos462

set_option pp.funBinderTypes true
set_option pp.numericTypes true
set_option pp.proofs false

-- Full types of the paper-facing theorems
#check @Erdos462RH.theorem_1_1
#check @Erdos462RH.composite_sum_384
#check @Erdos462RH.cully_dudek_wide_interval
#check @Erdos462RH.theorem_1_2_lower
#check @Erdos462RH.theorem_1_2_upper
#check @Erdos462RH.erdos_462_composites
#check @Erdos462RH.erdos_462_as_printed

-- Axioms
#print axioms Erdos462RH.theorem_1_1
#print axioms Erdos462RH.composite_sum_384
#print axioms Erdos462RH.cully_dudek_wide_interval
#print axioms Erdos462RH.theorem_1_2_lower
#print axioms Erdos462RH.theorem_1_2_upper
#print axioms Erdos462RH.erdos_462_composites
#print axioms Erdos462RH.erdos_462_as_printed

-- The analytic-input Props, verbatim (unfolded definitions)
#print Erdos462RH.SelbergBound
#print Erdos462RH.CullyDudekBound
#print Erdos462RH.Jtheta
#print Erdos462RH.squareError
#print Erdos462RH.SiebertBound
#print Erdos462RH.twinFactor
#print Erdos462RH.PrimeNumberTheorem
#print Chebyshev.theta
#print Nat.primesLE

-- Statement of Lemma 3.1 as formalized
#check @Erdos462RH.fixed_length_supply
#print Erdos462RH.SiebertFiniteBound
#print Erdos462RH.DyadicPrimeCounts

-- Non-vacuity probes: the Props are not trivially False by definitional accident
-- (cheap sanity: they are Props quantified over reals with the expected shape)
example : Erdos462RH.SelbergBound ↔ ∀ Y d : ℝ, 10^13 ≤ Y → 0 < d → d ≤ 1/10^13 →
    ∫ v in (1:ℝ)..Y, (Chebyshev.theta ((1+d)*v) - Chebyshev.theta v - d*v)^2
      ≤ (25571/10000 : ℝ) * d * Y^2 * Real.log ((20001/10000 : ℝ)/d)^2 := Iff.rfl
example : Erdos462RH.CullyDudekBound ↔ ∀ Y d : ℝ, 10^8 ≤ Y → 0 < d → d ≤ 1/10^8 →
    ∫ v in (1:ℝ)..Y, (Chebyshev.theta ((1+d)*v) - Chebyshev.theta v - d*v)^2
      < 202*d*Y^2*(Real.log Y)^2 := Iff.rfl
