HOLDS AS READ

Seat O — printed §2 (From two adjacent intervals to gap counts), §3 (A square with a small marked moment), §4 (Cancellation between adjacent dimensions), and the proof of Corollary 1.2 in §1. Paper: "Positive lower density of large prime gaps" (OpenAI, 25 Sep 2026). Printed numbering checked against `pdftotext -layout` (O_work/paper_layout.txt): Prop 2.1, Lemma 2.2, Prop 3.1 with displays (4)–(8), Lemma 4.1, Prop 4.2 with displays (9)–(12).

I looked for a false step in every line of these sections and found none. Everything below is either verified (by hand, with the arithmetic shown, plus an independent numeric or symbolic check where one was possible) or is a remark about exposition. Scripts and outputs are in /tmp/oaimath/026/seats/O_work/ (new files are prefixed `v2_`; the earlier seat's files were re-read line by line and re-run before I relied on them).

## Findings

1. **§2, proof of Theorem 1.1 (both Cauchy–Schwarz steps, choice of ε, quantifier order): verified. Severity: none.**
   - "Weighted Cauchy–Schwarz gives E_X(W_X 1_{A_X}) ≥ E_X(W_X V_J)^2 / E_X(W_X V_J^2)". This holds because V_J = V_J·1_{A_X} and W ≥ 0. The denominator is positive once the numerator is, because W ≥ 0 and V_J ≥ 0. The lim inf being ≥ λ²/K_λ uses the lim sup of the denominator from (2). Correct.
   - "Since 1_{B_X} ≤ V_I". True. If m+b is prime with b ∈ I, then ϑ(m+b)/L = log(m+b)/log X > 1, because m > X. So V_I > 0 implies V_I ≥ 1. The same argument proves the §2 sentence "V_B ≥ 1 whenever V_B > 0, since all its prime arguments exceed X."
   - Taking ε = λ²/(2K_λ) gives Δ = λ²/K_λ − ε = λ²/(2K_λ) > 0. K_λ = C_* = λ + λ²c_G² is fixed by λ and G alone; the "Proof of Proposition 2.1" (end of §4) sets it before ε is chosen. M = sup over large X of E_X W_X² is allowed to depend on ε, and it is used only after ε is fixed. The order of quantifiers is right.
   - The second Cauchy–Schwarz, E(W 1_{A∖B})² ≤ E(W²)·|A_X∖B_X|/X, holds as written. Its "≥ Δ²/(4M)" uses E(W 1_{A∖B}) ≥ Δ/2 for large X, which follows from lim inf ≥ Δ. Correct.
   - Lemma 2.2. The last prime p(m) in (m, m+h] satisfies p(m)⁺ > m+2h ≥ p(m)+h, so the inequality is strict. Each p arises from at most the h integers m ∈ [p−h, p−1], and every p(m) lies in (X, 2X+h]. Correct.
   - Passage from X to N. With X = ⌊p_N/3⌋, we have 2X + h ≤ 2p_N/3 + λ log p_N < p_N for large N, so every counted start is some p_n with 1 ≤ n ≤ N−1. Also X/log X ~ p_N/(3 log p_N) ~ N/3, so X/log X ≥ N/4 eventually. Correct.
   - Final step: δX/h ≥ δX/(λ log X), using h ≤ λL. And h > C log p: h ≥ λL − 1 while C log p ≤ C(L + log 3), so h > C log p once L > (1 + C log 3)/(λ − C). Correct.
   - Exposition only: the "1" in "choose λ > max{C, 1}" is never used (h ≥ 1 holds for large X for any λ > 0).

2. **§1, proof of Corollary 1.2: verified. Severity: none.**
   - "The displayed inequality is equivalent to p_{n+1} − p_n > p_n/n". Check: (n+1)p_n < n p_{n+1} ⟺ p_n < n(p_{n+1} − p_n). Correct.
   - The prime number theorem gives p_n/n = log n + log log n − 1 + o(1) and log p_n = log n + log log n + o(1). So p_n/n < 2 log p_n for all n ≥ n_0. Theorem 1.1 with C = 2 then gives at least c(2)N − n_0 indices n ≤ N in the set. The direction of every inequality is right. (Any C > 1 would do.)

3. **§3, the prime-deletion identity (8) and the derivative identities: verified exactly. Severity: none.**
   - Quote: "When m + a is prime, every nonzero term from a subset containing a has divisor one in that coordinate: the other possible divisor satisfies log(m + a)/L > 1 > τ, so its contribution vanishes by the support condition on F_j."
     - This is correct. F_j(v) = ∫_{s≥v} f_j vanishes on the nonnegative orthant once Σv_i ≥ τ, because f_j is supported in {Σ t_i < τ}. The coordinate log(m+a)/L > 1 > τ forces that.
     - The identity only needs m+a to have no divisor in (1, X^τ]. So it holds for every X^τ-rough m+a, not just primes (this matters for item 7).
   - Exact integer check (`v2_identity8.py`).
     - Setup: X = 10⁹ with τ = 1/8, λ = 0.4; and X = 10⁷ with τ = 0.45, λ = 0.5. In both, k = 3, h = 8, and the F_j are random real symmetric functions vanishing for Σv ≥ τ.
     - Both sides of (8), computed from the definition of D_F with sympy divisors and Möbius, agree to ≤ 2.2e-16 at 12 events where m+a is prime.
     - Negative control: at m+a composite the two sides differ by 0.05–0.40, so the test can fail.
   - (4) "(−1)^j ∂_1⋯∂_j F_j = f_j" and the statement "The signed complete mixed derivative of F̃_j is f_j + T f_{j+1}". Both verified symbolically with sympy (`v2_deriv.py`: zero residual for j = 1, 2, and the scalar case F̃_0 = f_0 + ∫f_1). By hand: F_{j+1}(·,0) is the cumulative integral of T f_{j+1}. The face vanishing holds because T f_{j+1} keeps interior support: its coordinates are bounded below by the same constant as those of f_{j+1}.
   - "Each subset occurs once, so deletion introduces no dimension factor." Correct: (j+1)-sets containing a correspond bijectively to j-sets U ⊂ I∖{a}.
   - Combinatorial factors are right:
     - C(h,j)/L^j → λ^j/j! = α_j gives w.
     - (h/L)·C(h−1,j)/L^j → λα_j gives v = λ Σ α_j ‖f_j + T f_{j+1}‖², including the scalar term λ|f_0 + ∫f_1|².
     - (h/L)·C(h,j)/L^j → λα_j gives E(Z²V_J) → λw.
     - The last-subsection proof of Prop 3.1 (printed §5, end) uses the same counts.
   - Exposition only: the letter B is used for the interval label (V_B, B = I, J; also the sets B_X), for B_R in Lemma 4.1, and for the support endpoint of g in Prop 4.2.

4. **§4, Lemma 4.1: verified. Severity: none.**
   - By hand:
     - A_R ≥ ∫_1^R du/u = log R.
     - B_R ≤ ∫_{1/2}^{2R} u·u⁻² du = log(4R).
     - 1 − 1/R ≤ N_R² ≤ ∫_{1/2}^∞ u⁻² du = 2, and R ≥ 2 gives the lower bound 1/2.
     - Scaling: ∫g² = 1, ∫g = c^{1/2}∫g_0 = √λ, and μ_g = c∫v g_0² = λN_R²/A_R² · B_R/N_R² = λB_R/A_R². All exact.
   - Numeric check (`v2_lemma41_direct.py`). I built an explicit C^∞ φ_R from exp(−1/x) steps, then g by its definition, and integrated g², g and ug² directly:
     - ∫g² = 1.00000000 and ∫g = √λ to 1e-8.
     - μ_g = λB_R/A_R² to 1e-6.
     - A_R − log R = +0.693, log(4R) − B_R = +0.820, N_R² = 1.264, for every R tested (λ = 0.5, 1, 3).

5. **§4, Proposition 4.2: verified. Severity: none. One quantitative remark.**
   - Algebra checked by hand:
     - ‖Q_j‖ = 1.
     - "T Q_{j+1} = √(λ/k) Q_j (0 ≤ j < k)", including j = 0.
     - α_j/α_{j+1} = (j+1)/λ.
     - The bracket in (11), including the factor √((j+1)/(λk)) after substituting u = k t_{j+1}.
     - The first inequality in (10), w ≥ 1 − s_g²/(kd²). It holds because E_j S_j = jμ_g/k ≤ μ_g and Var_j S_j = j s_g²/k² ≤ s_g²/k.
     - The tail bound P_j(S_j > β − B/k) ≤ 4s_g²/(kd²) for k ≥ 2B/d. It holds because β − B/k − E_j S_j ≥ d/2.
     - The sentence "the passage between them uses no comparison of these measures". On {S_j ≤ β − B/k}, both cutoffs in (11) equal 1 for every u ∈ supp g.
     - On that event the bracket is 1 − √((j+1)/k) ≤ (k − j − 1)/k ≤ r/k, since j ≥ a = k − r + 1. Everywhere else the bracket lies in [−1, 1], since √((j+1)/(λk))·∫gχ ≤ √((j+1)/k) ≤ 1.
     - Top term: α_k‖f_k‖² = E_k χ²/r ≤ 1/r.
     - Bottom term: α_{a−1}‖T f_a‖² ≤ (1/r)(a/(λk))·λ = a/(kr) ≤ 1/r.
     - So (12) holds: v/λ ≤ 2/r + (r/k)² + 4s_g²/(kd²).
   - Support condition from §3. f_j = c_j Q_j χ(S_j) is real, symmetric and C^∞. Its support lies in {t_i ≥ (lower support endpoint of g)/k > 0} ∩ {t_i ≤ B/k} ∩ {S_j ≤ γ}, and γ < τ. That is a compact subset of the open region {t ∈ (0,∞)^j : Σt_i < τ}, so f_j ∈ C_c^∞ of the open region, as Prop 3.1 requires. The claim "Each selected finite family has compact interior support" is correct.
   - Literal check at k = 4 (`literal_k4.py`, re-run; r = 2, a = 3; λ = 1, log R = 12, β = 0.10, γ = 0.12).
     - Tensor quadrature of the *definitions* w = Σα_j‖f_j‖² and v = λΣα_j‖f_j + T f_{j+1}‖² (T computed as a literal u-integral) gives w = 0.941382 / 0.941412 and v/λ = 0.723886 / 0.723909 on 70⁴ / 100⁴ grids.
     - The route through (10)/(11) by Monte Carlo (N = 2·10⁶) gives w = 0.941397 and v/λ = 0.723874.
     - The earlier seat's run at λ = 3, log R = 33 agreed in the same way (w 0.97707 vs 0.97665, v/λ 0.84930 vs 0.84893).
   - Large-k Monte Carlo, λ = 1 (log R = 12, μ_g = 0.0780, d = 0.022, B = 2553, s_g² = 11.13, so 2B/d = 2.3e5); w and v/λ are computed through (10)/(11). Bound (12) is only claimed once k ≥ 2B/d.

     | k | w | v/λ | bound (12) |
     |---|---|---|---|
     | 1e3 | 0.872 | 0.117 | not claimed |
     | 1e4 | 0.894 | 0.0317 | not claimed |
     | 1e5 | 0.974 | 6.48e-3 | not claimed |
     | 3e5 | 1.000000 | 3.653e-3 | 0.31 |
     | 1e6 | 1.000000 | 1.999e-3 | 0.094 |
     | 3e6 | 1.000000 | 1.154e-3 | 0.032 |

     The earlier seat's λ = 0.5 run behaves the same way, down to v/λ = 6.3e-4 at k = 1e7. In the asymptotic regime v/λ ≈ 2/r: the two endpoint terms dominate, and the paper's bound is valid but loose.
   - λ = 3: see item 6.
   - Exposition: display (12) does not restate its hypothesis k ≥ 2B/d. That hypothesis is introduced a paragraph earlier ("For k ≥ 2B/d, Chebyshev's inequality gives …"), and since (12) is used only as k → ∞, nothing breaks.
   - Remark, not an error: the bound (r/k)² for the interior is generous (the true interior sum is ≈ r²/(12k²)). The choice r = ⌊√k⌋ gives v/λ ≍ k^{−1/2}, and r ≍ k^{2/3} would give k^{−2/3}. This is irrelevant to correctness.

6. **λ = 3 in the regime where (10) and (12) actually apply: constants and characteristic-function check. Severity: none (an observation about effectivity).**
   - Lemma 4.1 forces large constants for λ = 3. With β = 0.1 < τ = 1/8 we need log R ≈ 33 to get μ_g = 0.0887 < β. Then d = 0.0113, B = 1.41e12 and s_g² = 2.66e9. So 2B/d = 2.5e14 and s_g²/d² = 2.1e13.
   - The bounds in (10) and (12) say nothing until k ≳ 10^14–10^15, so for λ = 3 the family Z has dimension of order 10^15. Direct Monte Carlo is impossible there.
   - Method (`v2_cf.py`). I computed the law of S_k by inverting its characteristic function exp(k[log ψ(ξ/k) − iξμ_g/k]), with ψ evaluated by quadrature over g². I then assembled w and v/λ from (10)/(11), using the deficiency variables 1 − χ and 1 − H/√λ so that 1 − 2c + c² never cancels catastrophically. Approximation: every j ∈ [a−1, k] uses the law of S_k; the means differ by at most μ_g r/k.
   - Positive control: the same code at λ = 1 against the Monte Carlo of item 5.

     | k | w (cf) | w (MC) | v/λ (cf) | v/λ (MC) |
     |---|---|---|---|---|
     | 1e4 | 0.8794 | 0.894 ± 0.015 | 0.03154 | 0.03173 ± 0.0008 |
     | 1e5 | 0.9881 | 0.974 ± 0.007 | 6.534e-3 | 6.48e-3 ± 7e-5 |
     | 3e5 | 0.99990 | 1.000 (0/400 exceedances) | 3.6536e-3 | 3.6533e-3 |
     | 1e6 | 1 − 1e-10 | 1.000 | 1.999084e-3 | 1.9991e-3 |

   - λ = 3 (log R = 33, β = 0.10, γ = 0.12):

     | k | P(S > β − B/k) | w | v/λ | bound (12) |
     |---|---|---|---|---|
     | 1e14 (below 2B/d; B/k > d) | 0.68 | 0.99595 | 1.16e-5 | not claimed |
     | 1e15 | 5.3e-7 | 1.0000000000 | 6.3246e-8 = 2/r | 0.083 |
     | 3e15 | 4.9e-15 | 1.0000000000 | 3.6515e-8 = 2/r | 0.028 |

     So w → 1 and v → 0 at λ = 3 as well, inside the bound (12), which is loose by about 6 orders of magnitude.
   - Consequence for the paper: nothing is false. Theorem 1.1 asserts only existence, and the paper says "the bound in (3) need not be uniform as ε decreases". But M in the proof of Theorem 1.1 bounds E Z⁴/w² for a family of dimension ≈ 10^15, so c(C) = Δ²/(16λM) and N_0(C) are ineffective in practice. The paper never claims otherwise.

7. **Sanity: is a weight with E(WV_I) ≤ ε but E(WV_J) → λ too strong? I see no obstruction. Severity: none.**
   - The only lower-bound input is the asymptotic E(Z²V_J) → λw, for primes at shifts outside the divisor support. That is exactly GPY/Maynard's Σ θ(n+h₀)Λ_R², at level 2τ = 1/4 < 1/2.
   - Suppression in I is an upper-bound (L²) phenomenon. It comes from the exact identity (8), which needs only that m+a is X^{1/8}-rough, plus cancellation in the limiting quadratic forms between dimensions j and j+1.
   - So the argument applies verbatim to any X^{1/8}-rough "pseudo-prime" set with level of distribution 1/4 (for example rough numbers, or suitably weighted P₂'s with large factors). For such sets the conclusion (a positive proportion of large gaps) is also expected, so there is no parity contradiction.
   - The method never has to tell primes from P₂'s.
   - Why high dimension is essential: with only dimensions 0 and 1, the generalized-eigenvalue computation gives v/w ≥ λ(1 + t/2 − √(t + t²/4)) with t = τ/λ. That is ≥ 0.81λ at λ = 3.
   - No conflict with the Cramér heuristic either: the expected true proportion is ≈ e^{−C}, and c(C) is astronomically small.

## What I did NOT check
- Printed §5 in its entirety: Prop 5.1, Lemmas 5.2–5.4, the uniform-error and equality-pattern arguments, the singular-series average, and the limits (5)–(7) themselves (including E Z⁴ = O(1) and the detector bound (7) with C_* = λ + λ²c_G²). I took Prop 3.1 as given. The only exception is the elementary inequalities displayed in its last proof (ϑ/L ≤ q_X D_G², with D_G = 1 at a relevant prime), which I read and which are correct.
- The Lean formalisation and its statement match.
- Literature and attribution claims in §1 (BLZ Theorem 5's threshold 2/3.454, Gallagher, Jha, the Goldston–Yıldırım citation).
- Whether τ = 1/8 is the paper's intended budget relative to §5's support table (2τ < 1/2, 6τ < 1). I only noted that it is consistent.

## Reproducibility (all in /tmp/oaimath/026/seats/O_work/)
- `v2_identity8.py`: exact integer check of (8), with a composite negative control.
- `v2_deriv.py`: sympy check of (4) and of the signed derivative of F̃_j.
- `v2_lemma41_direct.py`: Lemma 4.1 by direct quadrature, plus the Prop 4.2 thresholds 2B/d and s_g²/d².
- `literal_k4.py`: literal definitions vs (10)/(11) at k = 4. Outputs: `v2_literal_k4_lam1_n70.out`, `v2_literal_k4_lam1_n100.out`, `literal_k4.out`.
- `largek.py`: Monte Carlo via (10)/(11). Outputs: `v2_largek_lam1.out` (λ = 1) and `largek_lam05.out` (λ = 0.5, earlier seat).
- `v2_cf.py`: characteristic-function evaluation at huge k. Outputs: `v2_cf_lam1_control.out` (control) and `v2_cf_lam3.out`.
- `common.py`: shared profile and cutoff code from the earlier seat. I re-read it and cross-checked it against the independent `v2_lemma41_direct.py`: μ_g and s_g² agree.
- All jobs ran under ulimit -v 8 GB and nice 19, on at most 2 threads.
