# Seat O — printed §2 (From two adjacent intervals to gap counts), §3 (A square with a small marked moment),
# §4 (Cancellation between adjacent dimensions), plus §1's Corollary 1.2 proof.
Read COMMON.md first. Your scope (TeX files 02-counting.tex, 04-weights.tex, 05-cancellation.tex, and the corollary proof in 01):
1. The deduction of Theorem 1.1 from the weight proposition (printed Prop 2.1 or whatever it is numbered): both Cauchy–Schwarz
   steps, the choice ε = λ²/(2K_λ), the ordering of quantifiers (K_λ independent of ε; M allowed to depend on ε), Lemma 2.? (adjacent
   gaps: multiplicity ≤ h), the passage from X to N with X = ⌊p_N/3⌋ (indices ≤ N? ≥ 1? the PNT step X/log X ≥ N/4), h > C log p.
   Is V_B ≥ 1 when V_B > 0 really true for all primes in the interval? Is 1_B ≤ V_I right?
2. Corollary 1.2: is "apply Theorem 1.1 with C = 2 and discard finitely many indices" correct (p_n/n vs log p_n, direction of inequalities)?
3. §3: the prime-deletion identity — the claim that when m+a is prime every nonzero term from a subset containing a has divisor one
   in that coordinate (support of F_j, log(m+a)/L > 1 > τ); the cumulative-derivative identity (−1)^j ∂_1…∂_j F_j = f_j; that the signed
   mixed derivative of F̃_j = F_j + F_{j+1}(·,0) is f_j + T f_{j+1}; the formulas for w and v as stated in the moment proposition (do
   the combinatorial factors α_j = λ^j/j! come out right for subsets of I of size j, and for (a,U) with U ⊂ I∖{a}?).
4. §4: Lemma 4.1 (the profile g: check A_R ≥ log R, B_R ≤ log(4R), 1/2 ≤ N_R² ≤ 2, the scaling identities, μ_g bound — verify
   numerically with an explicit smooth φ_R); Proposition 4.2: ‖Q_j‖=1, T Q_{j+1} = √(λ/k) Q_j, the bracket identity, the Chebyshev
   bounds, the two endpoint terms, the final bound on v/λ, and that the support condition Σ t_i < τ really holds for the chosen f_j
   (χ(S_j) cutoff at γ < τ) AND that f_j ∈ C_c^∞ of the OPEN simplex in (0,∞)^j as required in §3 (interior support, coordinates bounded
   away from 0). Numerically build the family for λ = 3 (and one more λ) at a few k and compute w and v by Monte Carlo or quadrature;
   check w → 1, v → 0 at the rate claimed.
5. Sanity: think about whether the conclusion of the moment proposition is too strong to be true (a nonnegative weight built from
   divisors of m+b, b ∈ I, of level X^{1/8}, under which the expected number of primes in I is ≤ ε while it stays λ in J). Is there a
   known obstruction (parity, a theorem that such weights cannot exist)? If you believe it is fine, say why in two sentences.
Out of scope: printed §5 (the analytic moment estimates) — another seat has it; take its statements as given.
