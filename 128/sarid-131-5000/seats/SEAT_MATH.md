# Seat MATH — the argument itself (Sections 2–4 of the paper)
Read COMMON.md first. Then read /tmp/erdos1800/claim/claim.txt in full.

Tasks (do all):
1. Lemma 2.1 (β ≤ β*): is the pair-shift argument complete? Watch: the relaxation's mass is n/2 while β uses ⌊n/2⌋;
   odd n; the concavity claim; existence of a minimiser with fewest nonintegral coordinates.
2. Lemma 2.2: all four blow-up identities; in particular D₂(G(k)) = k² D₂(G) (the paper proves ≥ via multilinearity
   — is the ≤ direction and the equality actually needed/established?). Does Corollary 4.2 need anything about
   n₀ being achievable (k ≥ n₀/n) — fine? Is the blow-up triangle-free?
3. Lemma 3.2: the identity (4), the sign of ρ/2 − e(N(u),N(v))/n², p ∈ [0,1] from Δ < n/2, and (5) with HOMOMORPHISM
   counting (degenerate 4-cycles included) — does t(C₄,G) in Prop 3.1 mean hom(C₄,G)/n⁴ consistently everywhere,
   including the certificate statement "t(C4) - rho^3 + (3/64 + 1/50000000000) rho >= 0" and the Lean's `c4Hom =
   trace(A⁴)`? A normalisation mismatch here (hom vs injective vs induced, factor 3) would be FATAL. Check against
   Razborov's conventions (razborov.txt, "Digression on quadriliterals counting") and confirm Prop 1.1 ⇔ Lemma 3.2.
4. Prop 3.3: the Δ ≥ n/2 case, the monotonicity for ρ > 1/4, the arithmetic. Recompute in exact rationals (Python
   fractions) and print.
5. Lemma 4.3: re-derive (7), the harmonic–arithmetic step (8), the averaging, the inequality 2R³/(R²+1) ≥ 2R−1, the
   role of σ. Then TEST it: for 200 random weighted triangle-free graphs (random weights on the simplex, graphs =
   random bipartite + random blow-ups of C5/Petersen/Clebsch + nauty-geng -t graphs on ≤ 8 vertices), compute
   max_x S_x − 4μ³ and print the minimum over graphs (must be ≥ 0; equality on regular uniform-weight graphs).
   Mutation control: replace 4μ³ by 4.01μ³ and show the test now FAILS on a regular graph.
6. Lemma 4.4: re-derive (10) and the barycentric average; the feasible interval; the three-case product t₊t₋ ≥ L(α)
   (also α > 1/2 by symmetry — check the symmetry claim is legitimate for the functional with the ψ term). TEST it
   numerically on random weighted triangle-free graphs: for random α and random ψ, construct the endpoint profiles
   and verify A(π) ≤ A(α) − 4L(α)μ³ for the better endpoint; print the worst slack.
7. Section 4.2: the two fractional halves have mass n/2 (check with s, a, c), the cost identities (13), the bound (12),
   the scaling of the saving by 1/(4c²), "increasing ρ and I can only increase B₁" (note μ is a graph quantity
   bounded by 4c²I_Y ≤ 4c²I — is relaxing I to I₀ legitimate in BOTH the objective and the domain?), and the
   reduction to F(a, μ) on 0 ≤ a ≤ 1/2, 0 ≤ μ ≤ 4I₀c².
8. Lemma 4.5: recompute the envelope (16), the derivative bounds, and the maximum by an INDEPENDENT route: grid +
   exact-rational evaluation of F(a,μ) on a fine grid (say 2000×2000 over the domain) and a local maximiser (scipy)
   — print max F and where; it must be < 131/5000 = 0.0262 and ≈ 0.026176 near a = 88/417. Also evaluate the
   two-branch balance claim: the high-density bound ρ/8 − ρ²/4 + γ/4 at ρ = 7/22 vs the low-density maximum, and
   the claimed optimum split ρ ≈ 0.3184 giving ≈ 0.026176 (recompute the balancing ρ; this is only a remark but
   a wrong remark is an exposition finding).
9. Anything else: hidden hypotheses (ρ > 0? n ≥ 2? connectedness? the bipartition from BCL being nontrivial?),
   the case a = 0, the case μ = 0, the case where Lemma 4.4's x has d = 1, and whether the perturbation could push
   a coordinate outside [0,1].
Write REPORT.md as specified. Put scripts in /tmp/erdos1800/seats/math/.
