# Seat O — printed §2 (the explicit main term), §3 (extracting a long prime prefix), §6 (the coefficient and the limiting formula).
Read COMMON.md first.
1. §2: the scale. Check that g_n (renewal recursion) behaves as claimed (g_n ρ^n → γ?), that G_m is the right size, that ψ, m, θ are
   well-defined for large x, and that the stated main term is consistent with Ford's (1.1) up to a bounded factor (compute numerically
   log G_m − [C0(log3 x − log4 x)² + D0 log3 x − (D0+1/2−2C0) log4 x] as a function of B = log log x up to B ~ 10^6; it should stay
   bounded; report its range and whether it depends only on θ asymptotically). Check C0 = 1/(2λ) = 0.8178146…, D0 = 2.1769687….
   Definition of A_H(f;s): inclusion–exclusion over finite unions of witness regions — is it well-defined (finitely many terms? the
   ∑ over totients d convergent?), and does the definition really avoid V (as claimed)?
2. §3: every use of Ford's structure estimates (printed Theorem/Lemma numbers of Ford cited in §3.1) — is the deduction from the
   quoted Ford statement correct as used (quantifier order, uniformity in parameters, exceptional sets O(V(x)e^{−P²/4}) etc.)?
   Basic witnesses, coverage target, simplex volume and concentration, prime boxes, smooth cofactors, tuples and discarded part.
   Look for the classic holes: a lemma assuming the conclusion's strength; "clearly" at the hard step; an error term that is only
   o(V(x)) for fixed H but used uniformly in H.
3. §6: summing over the largest prime; the finite tail vs continuous prefix split; the arithmetic approximation; uniform convergence
   in the phase s ∈ [0,1) and the passage to V(x) ~ main term; the derivation of V(cx)/V(x) → c (does it need continuity of A in s?
   the paper says no — check how the phase shift θ(cx) − θ(x) → 0 is handled, and whether A's possible discontinuity at s → 1⁻ vs
   s = 0 (wrap-around when m jumps) is treated).
Out of scope: §4–§5 (sieve comparison and prefix uniqueness) — another seat; take Propositions there as given but say which ones you used.
