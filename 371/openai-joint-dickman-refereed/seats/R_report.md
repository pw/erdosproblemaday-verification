# Seat R — hostile referee report on printed §§5–11
Paper: OpenAI, "The joint Dickman law for consecutive integers" (24 Sep 2026), Erdős #371 (+ #928).
Scope: §5 graph.tex, §6 moments.tex, §7 channels.tex, §8 kernel.tex, §9 sampling.tex, §10 conclusion.tex, §11 distribution.tex. I read every statement and proof in these sections line by line in the .tex, using paper.txt for the printed numbers (e.g. (5.4) = block energy, (8.17) = feature kernel 𝓜, (8.19) = integral comparison, (9.1) = sampling bound, (10.4) = block mean square). I also read §1.2, §2 (Lemma 2.3 and its proof), §3 (the statements of (3.2)–(3.5), (3.7)–(3.8) and Def. 3.7) and §4 (the whole section), because §§5–11 use them. Results imported from §§2–4 are taken as given. Other seats check those sections.

Scripts and output are in `/tmp/oaimath/012/seats/R_work/` (`joint.py`, `ident.py`, `lag.py`, `alpha.py`). Each ran under `ulimit -v 4000000; timeout 900`.

## Summary
I could not find a FATAL error or a real GAP in §§5–11. I checked the order of limits everywhere in scope. Every object chosen after x is either used only at fixed B, or is covered by an estimate that is uniform in it:
- the optimizing cut;
- sign tests that depend on the sample;
- the origin n.

Every object treated as fixed in the inner x-limit really is fixed before B → ∞:
- C_*, η, C_6;
- the coarse partition (ε₁) and ε₂;
- ζ and the polynomial degrees;
- P₁ and D;
- δ and the number of blocks R₀.

The objections below are expository, plus one omission about what the paper proves.

## Objections

**R1 (EXPOSITION / omission: what is proved vs. the problem pages).**
(a) #928 as posed asks for the density of {n : P(n) < n^α, P(n+1) < (n+1)^β}, with strict inequalities and threshold (n+1)^β. Theorem 1.1 is stated with "P⁺(n) ≤ n^a, P⁺(n+1) ≤ n^b". The paper never derives the #928 form. It does follow at once:
- The equality P(n) = n^α forces n = p^{1/α}, which happens for at most X^α values of n ≤ X.
- For n ≥ εX and any fixed β′ > β, we have n^β ≤ (n+1)^β ≤ n^{β′}.
- So the #928 event is sandwiched between Theorem 1.1 events, and continuity of ρ closes the gap.

The r-fold conjecture on the #928 page (all of n,…,n+r−1 being n^α-smooth, density ρ(1/α)^r) is not addressed. The method is two-point only, and the paper does not claim it.

(b) The second question on the #371 page (Er79e) asks whether the density of {n : P(n+1) > P(n)·n^α} exists for every α. The paper never states this. It does follow from what §11 proves. In the proof of Corollary 1.2 the paper shows that (U_n, V_n) converges weakly to D⊗D, where U_n = log P(n)/log n, V_n = log P(n+1)/log n, and D is continuous. Now P(n+1) > P(n)n^α holds exactly when V_n > U_n + α. The line v = u + α has zero D⊗D mass, because D has no atoms. So the density exists for every real α and equals ∫∫ 1_{y>x+α} dD(x)dD(y), which is Teräväinen's logarithmic-density value.

Numerical check at n ≤ 10⁷ (`alpha.py`):

| α | empirical | limit |
|---|---|---|
| 0 | 0.5000 | 0.5000 |
| 0.1 | 0.372 | 0.361 |
| 0.2 | 0.257 | 0.241 |
| 0.4 | 0.094 | 0.077 |

This is consistent, with the expected slow convergence.

Neither omission affects correctness. Whoever relays the result should say "Theorem 1.1 + one line" for #928 and for the α-question.

**R2 (EXPOSITION).** §8.2 quotes "The Montgomery–Vaughan bound [MV77, Corollary 1] states that a multiplicative function f satisfying |f(p)| ≤ 1 for every prime p and Σ_{n≤Z}|f(n)|² ≤ Z … obeys |Σ_{n≤Y} f(n)e(nθ)| ≪ Y/log Y + Y(log R′)^{3/2}/√R′ whenever |θ−u′/q′| ≤ 1/q′², 2 ≤ R′ ≤ q′ ≤ Y/R′."

I could not retrieve the 1977 Inventiones paper to confirm the label "Corollary 1" or the exact hypothesis list. EuDML and GDZ searches from this box returned nothing.

This does not matter for the proof. The function used is f = μ²2^{−ω}1_rough, which is 1-bounded and multiplicative. So it satisfies both the standard "Theorem 1, |f| ≤ 1" form and the quoted form.

I checked how the bound is applied:
- Dirichlet approximation with denominator limit ⌊X/B¹²⌋ puts off-major-arc θ at B¹² < q′ ≤ X/B¹² with |θ − u′/q′| ≤ 1/q′².
- With R′ = B¹⁰, the condition q′ ≤ Y/R′ holds for every Y ≍ X in the smooth partial summation.
- This gives |S₃| ≪ X·B^{−1/2+o(1)}, which is (8.5).
- Then CB · XB^{−1/2} · B^{−7/4}/(TX) per box, over O(B) boxes, gives B^{−1/4}/T. That is o(1/T) per lag, so o(1) after summing lags (8.6).

The saving is only 1/log Y, but that is enough here.

**R3 (EXPOSITION).** In §5.4, Prop. 5.3 handles the site-square event in one sentence: "Equation (5.7) is handled in the resulting weights, as just explained."

The one-line fill: (5.7) gives P(site square) ≪ M/P₀. This depends only on u, not on any conditioning. The deterministic O(B^{10}) mass bound on both kernels then gives a contribution of O(B^{10}M/P₀) = O(B^{−989}). Correct, but terse.

**R4 (ERROR-NONFATAL, trivial).**
- §5.1 says "a−b = jc, 0 < |j| ≤ T". Since a, b ∈ (Tc, 2Tc) the bound is strict, |j| < T. Harmless.
- Prop. 7.1 states c₇ = 1/200, but its proof gives ‖(1−P_av)U_d‖ ≪ B^{−1/80}. Also harmless.

## Answers to the brief's priority questions

**(a) §5, the substitution, invariance and coupling.**
- *Algebra.* From c | am+1, c | bm+1 and a − b = jc we get b·l_a + j = (abm + b + jc)/c = (abm + a)/c = a·l_b. I verified this symbolically and on 11,804 random instances (`ident.py`).
- *Inverse map.* Write n′ = bz. Then a | n′+j means j(1−cz) ≡ 0 (mod a). We have (a,j) = 1 because a is rough and |j| < T < P₀. So m = (cz−1)/a is an integer and the substitution recovers both congruences.
- *Label transfer.* conj(F(am+1))F(bm+1) = conj(F(l_a))F(l_b) = conj(F(n′))F(n′+j). This uses only (2.7) for the finitely many multipliers c, b, a < e^{4B}, valid once x > e^{4BJ}, i.e. x → ∞ first.
- *Weights.* The two φ-arguments trade places with errors O_B(1/x), which gives Ψ_s.
- *Coupling.* It is done under Haar measure on Ẑ, not on the integers. That is legitimate because, at fixed B, every kernel is a finite-residue function, continuous in s, so ordinary scale averages converge to Haar×ds integrals. The paper notes this after (5.6) and at the end of §9.
- *Sites sharing a prime.* In the actual law two sites cannot share a prime: p > P₀ = B^{1000} > M exceeds every position gap. The only discrepancy at a prime p is the model's double hits, O(M²/p²), so the total is O(M²/P₀).
- *Extra roots.* Each candidate also needs "p | m". The paper handles this as follows:
  - It excludes coincident rational roots r = b/c − i: probability ≤ 1/(Tc) ≤ e^{−B} per third position.
  - It excludes forced hits at a third occupied site: p | b + (s′−i)c, reciprocal sum O(B/P₀).
  - It zeroes the tests at primes dividing abc and at occupied primes.
  - At each remaining unoccupied prime, the root classes are distinct and the law of u mod p is uniform on p − M classes. That is a disjoint-choice law, within total variation O((M + N_cand)²/p²) of independent Bernoulli(1/p) tests.
- *Uniformity in M.* All failures are O(B^C/P₀ + B^C e^{−B}) times the deterministic O(B^{10}) mass, i.e. o(1). This is uniform in M ≍ T because P₀ = B^{1000} dwarfs every polynomial loss.
- *Root fluctuations.* Each candidate weight is ≤ B^{−1+6h_τ} < B^{−0.07}, by (3.10): 1 − 6h₀ = 0.0794. Bernstein with a union over 4^M sign pairs gives expected cut norm ≪ √(B^{−0.07}·(1/M)Σ𝓛) + B^{−0.07}, and Lemma 5.2 gives E Σ𝓛 = O(M). Sound.

**(b) §§6–9.**
- **§6.** I re-derived the bookkeeping:
  - the entropy counts ½gH(2r_z), ½gH(2r_y), ½gH(2r_y);
  - the Chernoff rate I_{1/2};
  - the identity F₀(r) − I_{1/2}(½ − r) = ½H(2r);
  - the two-root sieve density 1 − (3/2 − λ)/p;
  - the maximum exponent g[H(2r_z)+H(2r_y)−1−h₀] ≤ 2log2 − 1 − h₀ = (5log2−3)/2 = 1−5h₀ = κ₁ (numerically 0.2328680 both ways).

  The margin κ₁ + 0.04 − 0.32 = −0.0471 is correct and depends on |j| ≥ ηT ≍ B^{0.32}, which holds because 𝓛 is zero on non-allowed pairs. The variance identity for D_i = Σ_k 𝓛_ik is valid: given S_i the summands are independent, since roots were averaged out in §5.
- **§7.**
  - ‖U_d‖ ≪ 1 follows from Schur with (3.3).
  - For the flattening, Lemma 7.2 (TV coupling to C·E₁, C·E₂ with C, E₁, E₂ i.i.d. ν_{1/4}) and Lemma 7.3 (two-sided Schur for small exclusives) are both correct. With exclusives above θ = B^{−1/10}, the cell masses are residue-independent up to O(B^{−80}) by (3.3) applied to E with residue r·c^{−1}. So ‖(1−P_av)U_dU_d^*(1−P_av)‖ ≪ B^{−1/40}.
  - Coarse compactness: U₁U₁^* is, up to a θ^{1/4} error, the fine-cell compression of a kernel with derivatives bounded uniformly in B. Hence ‖QU₁‖² ≤ Cθ^{1/4} + C_θ/m₁ + o(1).
  - These are operator-norm statements, so they are uniform over inputs that vary with position or with the sample. That uniformity is exactly what §§8–9 need.
- **§8.**
  - Removing the cutoffs (8.1) uses (3.4), (3.8) and Lemma 3.8. The gcd removal is right: a common prime of any two of a, b, c forces p | a and p | b.
  - Major arcs: q ≤ B^{12}, radius B^{13}/X, disjoint. Arcs with q > B^{0.4} cost B^{−0.15}/T, and the (3.2) error costs B^{−49.75}/T.
  - The lift parametrization d = jq, with exactly j lifts per arc, is correct.
  - The histogram and residue-projection errors (8.9)–(8.11) are right: finite Parseval, bounded overlap of the windows I_X, and Σ_q (1/φ(q))(jq/φ(jq)) ≪ (j/φ(j))log Q.
  - The Ramanujan-sum identity (8.12) checks exactly for 1 ≤ j, q ≤ 12 (`ident.py`). The singular series 𝔖(j) vanishes for odd j, which is consistent with parity, and has mean 0.9975 over j ≤ 2000.
  - Archimedean inversion produces (8.15). The change of variables (8.17) → (8.18) is correct (u = λ/(e^v − 1)).
  - The separation is c_{l,B}(j,s) = (k_B/T)·𝔖(|j|)·w(s,|j|/T)·h_l: an arithmetic factor in |j| times a smooth factor in (s, |j|/T), as claimed.
  - (8.19) is uniform over tests that differ from edge to edge, because every error was bounded per edge for an arbitrary pair of 1-bounded tests.
- **§9.**
  - The moment inputs that feed concentration are:
    - the every-type conditional degree bound (5.9);
    - the integrated row-square bound q_B = C₁B^{−0.21} (from (6.1) and Σ_k𝓜² ≪ 1/T);
    - E A_B² ≪ 1.
  - From these: the degree event via conditional Chebyshev, union M·q_B/d_B² = B^{−0.03}; the square-mass event via Markov, B^{−0.01}.
  - Skeleton: m₂ = MB^{−0.18}. The without-replacement variance gives loss 2M(B^{0.18−0.20})^{1/2} = O(MB^{−0.01}). Deleting the sampled columns costs m₂d_B/M = B^{−0.11}.
  - Conditional mean ≤ E₀ + o(1), by (8.19) applied to tests fixed by the conditioned types, plus a √q_B variance term.
  - Lipschitz constant 4d_B/M between good configurations, McShane extension, then McDiarmid with exponent ε₂²M/(128d_B²) ≍ B^{0.18}. The union bound over log N_B = O(B^{0.14}log B) assignments survives.
  - The sample size m₂ depends only on B; x does not occur in §9 at all. The large kernels are tamed by the truncation to d_B = KB^{0.07} on the good event and by Cauchy–Schwarz with E A_B² ≪ 1 off it.

**(c) §10, the final contradiction and the order of limits.**
- The averages A_{a,r,l}(n) are fixed linear combinations of (1/L_a)Σ_{i∈J_a} 1_{i≡r (D)} F_x(n+i)G_{B,v}(n+i), with the following parameters, which are exactly the hypotheses of Lemma 2.3 and (2.12):
  - P_B = 𝓟, so min P_B = B^{1000} → ∞;
  - v ∈ {0,…,d_l}, fixed integers;
  - D = ∏_{p≤P₁} p, fixed;
  - a_B = (start of J_a) − 1;
  - L_B = L_a ∈ [c_{δ,C₆}T, δT], so L_B → ∞;
  - origins n/(Tx) ∈ [s₀, s₁], a fixed compact interval depending only on φ and ψ.
- The identity Ṽ_{l,B}(S_i(n)) = Σ_v α_{l,v}G_{B,v}(n+i) is exact (fair-split Laplace transform).
- The order of choices is acyclic: grid and τ → C_* (so that C₁e^{−c₃C_*} < c₅/10, and c₅ is independent of C_*) → η, C₆ → ε₁ (the coarse partition), ε₂ → ζ (polynomial degrees), P₁, δ, R₀ → B → x along the fixed subsequence.
- "A subsequence of every bad sequence" is the standard compactness argument: boundedness plus the diagonal extraction in §2, so the full integer-scale limit follows.
- Integer x to real X: §11 sets x = ⌊X⌋ + 1 and sandwiches the rational exponents.

**(d) §11.**
- The Fourier inversion over (ℤ/(J+1))^{J−1} is exact on count vectors, whose entries are ≤ J.
- The marginal: inclusion–exclusion plus the factorial moments (2.9) give H(1/c). The delay identity I_h(y) − I_h(z) = h∫_z^y I_{h−1}(t−1)dt/t is correct (I re-derived it), so H = ρ.
- Irrational exponents and real X are handled by monotone sandwiching. Moving thresholds n^a for n ≥ εX are sandwiched between fixed exponents.
- The ordering corollary: the limit law is the product D⊗D with D continuous, D(0⁺) = ρ(∞) = 0, and no atoms, so the diagonal is null. The clamp Ṽ_n = min(V_n, 1) does not change interior distribution functions. The endpoint cases in (11.8) are handled.
- Corollary 1.2 matches the Formal Conjectures statement {n | P(n+1) > P(n)} has density 1/2.

**(e) Numerics, n ≤ 10⁷ (`joint.py`).**
- P(P(n) < P(n+1)) = 0.499995.
- Joint vs. product of empirical marginals at (a,b) = (½,½): ratio 0.827 on [10⁴,10⁵), 0.884 on [10⁵,10⁶), 0.918 on [10⁶,10⁷). This drifts toward 1, consistent with the claimed limit. The marginals themselves are still far from ρ (0.272 vs 0.307) at log n ≈ 16, so this is slow convergence and I do not read anything into the gap.
- 𝔖 vs 𝔖_{P₁}: sup_T (1/T)Σ_{j≤T}|𝔖−𝔖_{P₁}| for T ≤ 2·10⁴ is 0.127, 0.038, 0.020, 0.0073, 0.0021 for P₁ = 3, 7, 13, 31, 101. Consistent with Lemma 10.2.
- Constants: 2h₀ = 0.3069 < 0.32; 1−6h₀ = 0.0794 > 0.07; 1−5h₀ = 0.2329 > 0.229; α₀ = 1.6·log 2 = 1.109 > 1.

## Coordinator handoff from seat A: §10's coefficients must be bounded uniformly in B

Seat A's point: Lemma 2.3 (2.12) gives `lim_B limsup_x = 0` with **no rate in B**. So the factorized main energy (10.5) tends to zero only if:
- it has a fixed number of terms;
- every coefficient multiplying a product conj(A_{a,r,l})·A_{b,r′,l} is bounded uniformly in B (and in n);
- nothing chosen after B, or after the subsequence, is needed to keep those coefficients bounded.

§10 asserts this in one sentence: "The factors L_aL_b/(MT) are uniformly bounded. The numbers of cells, blocks, and residue classes are fixed, and k_B and the representative smooth weights are uniformly bounded … This remains true when the bounded coefficients depend on n/(Tx) or on B." I checked each factor against where it is actually proved.

- **Number of terms.** It is m₁ · R₀² · D² · (number of monomials v ≤ max d_l). Each of m₁ (coarse partition, chosen with ε₁), R₀ (in terms of δ, C₆), D = ∏_{p≤P₁}p, and the degrees d_l (Lemma 10.1, in terms of ζ) is fixed before B → ∞. **Bounded.**
- **k_B.** §5.3 states "Set k_B = E_S K(S) under the independent 1/p law. The untruncated Euler product gives k_B ≪ 1." §8.2 makes it explicit: "0 ≤ k_B ≤ E K₀(S) = R^{1/2}∏_{p∈𝓟}(1−1/(2p)) ≪ 1, uniformly in the truncation constant." I re-derived it: Mertens gives ∏_{P₀<p≤e^{4B}}(1−1/(2p)) ∼ (log P₀/4B)^{1/2}, and R^{1/2} = (B/log P₀)^{1/2}, so E K₀ → 1/2. k_B does not depend on n, C_*, or anything chosen after B. **Uniform in B: proved.**
- **h_l.** (8.17) defines h_l = ∫_{I_l} m(y)ρ₀(y)dy, where m(s) = c_A s^{−1/2} is the B-free limit of m_B from §3 ("m_B(s) → m(s) = c_A s^{−1/2} (0<s<4)"). ρ₀ is supported in (1,2). So h_l is a fixed number, **independent of B.**
- **w(s,λ).** By (8.17)/(8.18), w(s,λ) = ∫₀^∞ Ψ_s(u+λ,u)/(u(u+λ)) du. This is a B-free function. The paper says "this formula extends w smoothly to 0 ≤ λ ≤ 1, with uniformly bounded derivatives there". The arguments λ_ab = |i_b − i_a|/T depend on B, and s = n/(Tx) depends on n. But sup_{s∈𝓘_s, λ∈[0,1]} |w| is a fixed constant, and §10 notes explicitly that "neither the representatives nor their scaled lags have to converge as B grows; only this uniform bound is used." **Bounded.**
- **Lag factor.** 𝔖(j) itself is not uniformly bounded pointwise: 𝔖(j) ≤ j/φ(j) ≪ log log j. But it enters §10 only through the row bound (10.3), sup_i (1/T)Σ_k 𝔖(|k−i|) ≪ 1, which is uniform in T. Before Lemma 2.3 is invoked, 𝔖 is replaced by 𝔖_{P₁}, at a cost made uniform in T by Lemma 10.2 (a sup over T, which I confirmed numerically). The coefficients c_{r,r′} = 𝔖_{P₁}(r′−r) are bounded by ∏_{p≤P₁}(1−1/p)^{−1}, which depends only on P₁, chosen before B. **Bounded.**
- **Block normalization.** L_a ≤ δT + 1 and M ≥ C₆T, so L_aL_b/(MT) ≤ (δT+1)²/(C₆T²) ≤ 2δ²/C₆ for large B. **Bounded.**
- **Features.** Lemma 10.1 says the polynomials p_l are "independent of B". The approximants are bounded by sup_{[0,1]}|p_l| ≤ 1/|I_l| + 1, also B-free. The coefficients α_{l,v} are fixed, so A_{a,r,l} is a fixed linear combination of the Lemma 2.3 averages, with exactly the 1/L_a normalization of (2.12). **Bounded.**
- **The approximation errors before the factorization** must also have constants uniform in B. They do:
  - Feature replacement: cost ≤ C·ζ, using V_l ≤ 1/|I_l|, the bound on Ṽ, the uniform-in-T row bound (10.3), and ‖V_l − Ṽ_{l,B}‖_{L²} ≤ ζ "for all sufficiently large B".
  - Lag replacement: cost ≤ C·sup_T (2/T)Σ|𝔖 − 𝔖_{P₁}|.
  - Block discard and w-replacement: cost ≤ C_{η,P₁,m₁}·δ, from B-free derivative bounds of w on η ≤ λ ≤ 1.

  These constants depend only on parameters fixed before B, so each error is < γ/3 for all large B.
- **Things that depend on B or on n.** The blocks J_a (their start and length), λ_ab, and s = n/(Tx) all depend on B or n. Lemma 2.3 explicitly allows an arbitrary start a_B and any L_B → ∞, so the blocks are covered, and L_a ≥ c_{δ,C₆}T → ∞. λ_ab and s enter only through the uniformly bounded w. Nothing in §10 depends on the subsequence except through W and φ, which (as seat A notes) are extracted once, before any B.

Conclusion on the handoff: **the uniform-in-B bound holds and is proved.** It is not proved in §10 itself, which only asserts it. It comes from the definition of k_B and its bound in §5.3/§8.2, the B-free limit m from §3, the B-free w in (8.18), Lemma 10.1, and Lemma 10.2. Given this, the final step is a finite sum, with coefficients bounded uniformly in B and n, of products of quantities that each satisfy lim_B limsup_x = 0. The inner x-limit is taken at each fixed B, so Lemma 2.3 needs no rate. **No objection.** At most it is an EXPOSITION remark: §10's "uniformly bounded" could cite where each bound lives.

## Steps checked and found sound (one line each)
1. (5.1)–(5.2) reindexing: the algebra is verified and the bijection inverse is explicit. It needs only (a,j) = 1, which holds since a is rough and |j| < P₀.
2. 𝓚_j(u,s) = 𝓚_{−j}(u+j,s): exchanging a and b leaves c(u+j) − a = cu − b unchanged.
3. Lemma 5.1: the three zero classes 0, −j, b/c are distinct mod p ∤ abc. The local mean 1 − 3/(2p) combines with (3.7).
4. Lag removal and block averaging: the edge-mass bound gives O(η) and O(T/M) = O(1/C₆), with constants independent of C_*.
5. (5.6): a real cut norm controls complex labels with |z| ≤ 2 at factor 16. This is deterministic and needs no independence between labels and residues.
6. Lemma 5.2 holds for every S_i: the fair-split identity plus (3.4) and (3.6), which are uniform in b.
7. Prop. 5.3: the site, root and site-square couplings are all O(B^C/P₀). The Bernstein fluctuation bound works because the per-candidate weight is < B^{−0.07}.
8. Lemma 6.2: the tilted measure, the entropy and Chernoff exponents, the two-root sieve, and the margin −0.047 are all correct.
9. Prop. 6.1: the first-representation expansion gives the bound, using the five-weight cap (6.2) and (3.6).
10. Prop. 7.1, Lemmas 7.2–7.3 and Cor. 7.4: the operator-norm channel bounds are uniform in the input. V_l is the exact coarse value.
11. Lemma 8.1: cutoff removal costs (Σ(j)/T)(r_B + e^{−c₃C_*}). The gcd removal costs O(B^{3/2}/P₀).
12. §8.2: the minor-arc, large-q and (3.2)-error contributions are o(1/T). The lift parametrization is exact.
13. §8.3–8.4: histogram and residue projection cost o(1/T) summed. (8.12) is exact, and 𝔖(j) ≤ j/φ(j).
14. §8.5–8.6: the archimedean inversion, the coarse replacement C_ηε₁·𝔖(j)/j, and the same-cell replacement O(B^{−1}) are correct. 𝓜 has the stated separated form. The row bounds (8.20) hold.
15. Lemmas 9.2–9.4 and Prop. 9.1: the degree and square-mass events, the skeleton, the conditional mean, the McShane/McDiarmid step and the union bound are all correct, and B is the only growing parameter.
16. End of §9: per-n cut norm, then Haar expectation, then ∫ds by finite-residue counting at fixed B.
17. Lemma 10.1: polynomials in e^{−x_b} with fixed degrees. The ν_{1/2}-mass of the endpoint neighbourhoods is uniformly small by (3.3). Conditional expectation is a contraction.
18. Lemma 10.2: the divisor-expansion tail goes to zero uniformly in T; this is numerically confirmed.
19. Prop. 10.3: the block discard costs O(δ), the w-replacement O_η(δ), and the factorization (10.5) is exact with real features. Cauchy–Schwarz plus Lemma 2.3 finish it.
20. Proof of Prop. 2.2: the parameter order is acyclic, and c₅ and C₁ are independent of the later choices.
21. §11: the Fourier inversion, the Dickman identification, the real-X and moving-threshold sandwiches, and the weak-convergence/diagonal-null argument for Cor. 1.2 are all correct.

Caveats on what this verdict covers:
- It is conditional on the inputs from §§2–4. Those are Lemma 2.3 (built on MR16 Thm 1 and MRT15 Thm A.1), the local laws (3.2)–(3.5), the form bounds (3.7)–(3.8), the regularity loss (Lemma 3.8), and §4's lower bound c₅. Other seats are checking them.
- I could not see the primary source for the Montgomery–Vaughan label (R2). That point is not load-bearing.

VERDICT: HOLDS AS READ
