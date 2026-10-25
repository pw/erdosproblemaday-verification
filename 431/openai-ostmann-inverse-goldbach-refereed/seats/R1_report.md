# R1 report — scope §1–§3 (printed pp. 1–21)

STATUS: COMPLETE (2026-10-23)

## 1. VERDICT for §§1–3: HOLDS AS READ

I rebuilt every load-bearing step of Lemmas 2.1, 2.2, 2.4 and 2.5, Theorem 2.3's setup (§2.3), Proposition 3.1 and Corollary 3.2,
and found no gap. The objections below are EXPOSITION only. None of them affects correctness.

## 2. Objections

E1 (EXPOSITION), pp. 13 and 15, the bounds after (3.14), at (3.17), and the sentence before (3.21). The paper writes
"their weighted square norm in (3.13) is at most Z^{-1}\sqrt L\,(1+\lambda)^K\exp(o(K))". It also writes "The weighted square norm
of each small-$s$ array ... is at most exp((-.9+log(1+\sqrt2\lambda)+o(1))K)", and "bound all large-$s$ arrays ... by
exp((.006+o(1))K) in the weighted square norm". Each bound is for the ROOT (\sum_s u_0^{\omega(s)}|b_s|^2)^{1/2}, which is the
quantity on the right of (3.13). The bounds are correct for that quantity. "Square norm" is a misnomer; read it as "weighted
norm".

E2 (EXPOSITION), p. 18, (3.30). "the number of distinct kernels ... is at most X^{3\varepsilon+o(1)}". Heath-Brown's bound gives
X^{2\varepsilon+o(1)} directly, and the paper itself says the 2ε version "would also suffice". This is a deliberate weakening, not
a slip.

E3 (EXPOSITION), p. 3, after (2.1). The large sieve is attributed to "the separated-frequency inequality of Montgomery and
Vaughan [MV1973, Theorem 1]". I could not open MV 1973 to confirm the theorem number. The inequality (2.1) is the standard
(M+Q^2) large sieve, and it is used correctly: with c_n = 1_U/|U| and M ≍ Q^2 = Y it gives O(Y/|U|).

No other objection survived checking.

## 3. What I checked and how

### §1 (pp. 1–3)
- Theorem 1.1 and its "Equivalently" clause. This is the same statement up to wording. The N0 convention is formally slightly
  stronger than the positive-integer convention used by Elsholtz, Elsholtz–Harper and Ostmann. The Lean also uses `Set ℕ`
  (with 0 ∈ ℕ).
- The citations that carry weight were checked against the sources. Results are in the next block.

### Cited sources
- **Laffer–Mann [25, Theorem 12]** (PJM 14 (1964), p. 557; fetched from msp.org). It reads "If A + B ~ P, the set of all primes,
  then (A) = (B) = ∞." Their proof uses Dirichlet's theorem and CRT, not a sieve. The citation is accurate. The paper's own proof
  is different and is independently valid (see Lemma 2.2). The Lean `FiniteSummands.lean` follows the Laffer–Mann/Dirichlet
  route, not the paper's sieve route. This is not a defect, because the paper's proof stands on its own.
- **Elsholtz 2006 [10, Theorem 1.9]** (Funct. Approx. 35, pp. 63–64; fetched). It reads "Suppose that there is an asymptotic
  additive decomposition of the set of primes, A+B = P', then √N(log N)^{-3} ≪ A(N) ≪ √N(log N)^2. The same bounds hold for
  B(N)."
  - Sets are of POSITIVE integers (his Defs 1.1–1.3).
  - The exponents are identical to the paper's (2.4).
  - The paper re-proves (2.4) in the N0 convention, so the convention difference is not load-bearing. The "reproduced" claim is
    accurate.
- **Elsholtz–Harper [11, Theorem 2.6]** (Trans. AMS 367; fetched). It reads x^{1/2}/(log x loglog x) ≪ A(x) ≪ x^{1/2} loglog x,
  "P ∼ A+B ... A, B contain at least two elements each", with positive integers (their Def. 1.1).
  - The intro on p. 2 quotes this exactly and labels it "positive-integer formulation".
  - It is never used downstream: grep shows no `\cite{ElsholtzHarper}` outside §1.
  - So the paper uses nothing beyond what that source gives, and nothing beyond Elsholtz 2006 either, since Lemma 2.4 is proved
    in-house.
- **Heath-Brown 1995, Theorem 1**, used as (3.28) on p. 17. I could not fetch the PDF (the impan mirror returned HTML).
  - I compared against the Lean transcription `QuadraticSieve/PublishedQuadraticSieve.lean`: Σ*_{m≤M} |Σ*_{n≤N} b_n (n/m)|^2 ≤
    C_ε (MN)^ε (M+N) Σ|b_n|^2, with both variables odd squarefree.
  - That matches (3.28), with s on top and u on the bottom, and matches my recollection of the theorem.
  - The Lean proves it in-house (`Quadratic/QuadraticSieveProof.lean`, discharged in `Complete.lean`).
  - The signed and even extension on p. 17 is correct: reciprocity gives (v/s) = (s/v)·(sign depending on s and v mod 4), and
    the factors (±1/s), (2/s) are absorbed into b_s. That makes 8 cases.

### Lemma 2.1 (p. 4), checked in full
- For p > p_0 the j classes −b_i mod p are distinct, and c > Q + C_0 ≥ p makes c+b_i a prime > p, so U avoids them.
- The local test function has mean 0 and probability norm (p−j)/j. The tensor has only primitive modes, and Cauchy–Schwarz
  gives (2.2).
- Large sieve with Q = √Y gives the bound O(Y/|U|).
- Weight: the Mertens product gives ≫ (log Q)^j. Under the normalized law each prime is included with probability j/p, and
  E log u = (1/10+o(1)) log Q. Markov then keeps ≥ 9/10 of the weight on u ≤ Q.
- Numerics:
  - (2.2) holds with equality when U is uniform on the allowed classes, and holds strictly on random U: min lhs/rhs = 1.000000,
    0 fails out of 300.
  - Control: claiming 1.5× the right side FAILS (100 of 300).
  - Script: `R1_work/scripts/fourier_checks.py`.

### Lemma 2.2 (p. 4), checked in full, including edge cases
- Case A finite with |A| ≥ 2. Pick a_1 ≠ a_2 (0 allowed). For large b ∈ B, a_i+b ∈ A+B with a_i+b ≥ b > N, so both are prime.
  Lemma 2.1 applies with j = 2 and C = B, giving B(Y) ≪ Y/(log Y)^2.
- Coverage: every prime p ∈ (N, Y] is a+b with a, b ∈ [0, p] ⊆ [0, Y], since a, b ≥ 0. So π(Y) − O(1) ≤ A(Y)B(Y) ≤ |A|·B(Y),
  which gives the contradiction.
- B finite: symmetric. Both finite: immediate.
- 0 ∈ A: the shift 0 is allowed in Lemma 2.1.
- Small primes are absorbed into N and the threshold p_0.
- Both requirements are used: exclusion for the shifts, coverage for the lower bound. So BOTH summands are infinite, as claimed.

### §2.3 complementary residue supports (p. 5)
- A common residue of a > p+N_* and d with −d > p+N_* gives p | a+b with a+b > 2p+2N_* > max(p, N). Since a+b ∈ A+B, this
  contradicts exclusion.
- Both tail images are nonempty because A and B are infinite.
- The partition S_p, S_p^c is arbitrary off the two images. Everything later in §§2–3 holds for any such choice.

### Lemma 2.4 (pp. 5–6), checked in full
- Coverage gives A(Y)B(Y) ≫ Y/log Y. Lemma 2.1 with j elements of B gives A ≪_j Y/(log Y)^j, and hence A ≫_j (log Y)^{j−1}.
- Lower bound (2.5): U = A∩(√x+N_*, x] avoids −B mod p for p ∈ (√x/2, √x]. Here exclusion is used: a+b > p, N. The energy is
  ≥ ν_p/p. The large sieve gives Σν_p/p ≪ x/m, and then Cauchy–Schwarz + PNT give H ≫ m/(√x log x). Reconstructed.
- Upper bound (2.6): the collision argument on B∩[0,Y] gives probability ≥ 1/ν_p. Unequal pairs contribute ≤ log Y; equal pairs
  have probability 1/B(Y) and contribute O(√x).
- The ε-bootstrap with log Y = x^{ε/2} gives B(Y) ≪ x^{1/2−ε} log x, which contradicts B(Y) ≫_j x^{ε(j−1)/2} for j > 1+1/ε.
  Then Y = x² gives m ≪ √x(log x)².
- The source uses positive integers. The paper's proof handles 0 ∈ B: for a large, a+0 must be prime, which is consistent.

### Lemma 2.5 (pp. 6–7), checked in full
- Unequal-pair count: Σ_{p≤Q} log p ‖μ_p‖² ≤ log X + O(Q max μ) = log X + O(1/log X).
- Supports: elements > √X+N_* ≥ p+N_* land in S_p, and similarly for ν. So ‖μ_p − U_{S_p}‖² = ‖μ_p‖² − 1/|S_p|, and
  1/|S_p| = σ_p^{-1}/p cancels against the density term exactly.
- Mertens with Q = √X/(log X)^{b+1} gives 4Σ log p/p = 2 log X − 4(b+1) log log X + O(1).
- Test-function form (2.8): Cauchy–Schwarz with probability norm ≤ 1 gives a factor p. Correct.
- The tails A∩[X^{9/10}, X] satisfy the point-mass hypothesis with b = 4, using (2.4).

### Brief question: "on suitable prime averages" — what is proved, and where is it used for individual primes?
- Lemma 2.5 proves only that the log p-weighted sum, over ALL p ≤ √X/(log X)^{b+1}, of three nonnegative terms is
  O_b(log log X). The total available weight Σ log p/p is ≍ log X.
- In §3 this is converted to individual primes only by Chebyshev deletion:
  - In the band T ≤ log p ≤ 2T, of weight T+O(1), it deletes an O_δ(log T) weight of primes. That set has σ_p ∉ [1/3, 2/3] or
    an empirical-vs-uniform error > δ/8 (p. 8).
  - The same is done in the band T^γ ≤ log p ≤ 2T^γ, of weight T^γ, which supplies the amplifier primes ℓ | L (p. 8).
- Only retained primes are used afterwards. No "for most p" is silently promoted to "for all p" in §§2–3.
- The individual-prime facts used in §3's endgame — kernel-prime disjointness on p. 18, and R_1 ∩ c_pR_2 = ∅ at split primes
  on p. 20 — come from exact exclusion ("x−y is a prime exceeding X^{9/10}"), not from Lemma 2.5.
- Downstream uses of (2.7)/(2.8) that convert averages to individual primes, for the §4/§5/§7 seats:
  - p. 22 (§4, subset version, |A'| ≥ √X/(log X)^{10}). I checked that the hypotheses hold there: b = 10, tested primes are
    below the cutoff.
  - p. 34, Corollary 4.2 / (4.16). Its Markov conversion to "outside harmonic mass o(L)" is legitimate. It is the only place
    Prop. 3.1 / Cor. 3.2 is consumed.
  - p. 36 (§5, Y = X(log X)^{40}) and pp. 55–57 (§7). Not audited by me.

### Proposition 3.1 (pp. 7–20), checked step by step

**Biased block (p. 8).**
- Weight argument; Chebyshev on (2.8).
- The identity E_{S^c}χ = −σ/(1−σ)·E_Sχ, which holds because the complete character sum is 0.
- With σ ∈ [1/3, 2/3] this gives c_δ = 3δ/8 on both sides.
- Dyadic subdivision: O(T) intervals, so some [Z, 2Z] has J ≫ Z/log Z primes.
- Scales (3.3) verified: K ≍ T^{1−γ}, L ≤ Z^{.02}, k ≍ T^{.6}, K/k ≫ T^{.4−γ}, and the factors of L are below Z.

**Moment (p. 9).**
- W > 0, has mean 1 by CRT, and W ≥ (1+λ/3)^K on A_X (elements > ℓ+N_*, so f_ℓ = 1−σ_ℓ ≥ 1/3).
- Jensen over A_X only, with all terms nonnegative (k even), gives (3.4). log(1+1/48) = .02062.
- (3.5) holds exactly, since ψ̂ is compactly supported and X/L → ∞.

**(3.6), the elementary bound, p. 9.**
- The permutation expansion k!e_k = Σ_σ sgn σ Π p_{|c|} was reconstructed.
- Odd cycles give p_m = JH; even cycles give ≤ J.
- #cycles = k−2j+e with e ≤ j, so each non-identity term is ≤ J^{−j}|H|^{k−2j}. Moved positions ≤ 3j, so C = 3 works.
- Numerics:
  - 2,755 random cases with y ∈ {0,±1}, k ≤ 10: 0 failures with C = 3 (max lhs/rhs = 0.125).
  - Control C = 0 FAILS 1,679 times.
  - Script: `R1_work/scripts/src5_check.py`.
- The Hölder relative-error bound k^C log Z exp(−.032K/k) → 0 was verified from X^{1/k} ≤ Z and J ≫ Z/log Z.

**Poisson / Gauss sums (3.9), p. 10.**
- Reconstructed the CRT splitting e(ur/(Md)) = e_d(ur M̄) e_M(ur d̄), the factor √d·g_d(−uM̄), and τ(χ_M)χ_M(u)χ_M(d)e_M(t_M u d̄).
- The identity e_M(t_M u d̄) = e((θ+h_0)u/d) holds because d | t_M + Mh_0.
- Normalization X√(Md)/(Md) = √X/√(Rd). Negative frequencies are χ_M(−1) times the conjugate.
- Numerics:
  - The complete-sum identity Σ_{r mod Md} f_d(r)χ_M(r−t_M)e(ur/(Md)) = √d·g_d(−uM̄)τ(χ_M)χ_M(u)χ_M(d)e((θ+h_0)u/d) was checked
    on 40 random (M = p_1p_2, d | L, S_ℓ, t_p) × 7 values of u. Max error 6e−12.
  - Control with the wrong sign of h_0 FAILS (error 91.6).
  - Script: `R1_work/scripts/poisson_check.py`.
- (3.7) Z^{10} ≤ R ≤ Z^{12+o(1)}, using 2^k = Z^{o(1)}. (3.10): (J)_k/J^k → 1, then the factor 1/2 for |(3.9)| ≤ 2|F_M|.

**(3.8), (3.11), (3.12), p. 10.**
- Multiplicativity of g_d and E|g_d|² ≤ 1 are correct.
- u = svw² decomposes uniquely, and χ_M(w²) = 1_{(w,M)=1} gives the Möbius sum over P | M.
- Support gives u < Z^{14}, w < Z^7, and P has ≤ 7 prime factors, hence O(k^7) terms.

**Moment over a fixed family (3.13), pp. 11–12.**
- Domination of the tuple average by all odd m ≤ (2Z)^k uses tuple probability k!/(J)_k and positivity.
- For a nonsquare product n, m ↦ (n/m) on odd m is periodic with period ≤ 8n and mean 0. I checked nonprincipality, including
  even s and the square part of n. Partial sums are ≤ period ≤ 8Z^{28l}.
- Square case: this is the sign-moment of F(ε). I re-derived Bonami's inequality: C(2l,2i)/C(l,i) = Π_{j<i}(2l−1−2j)/(2(i−j)−1)
  ≤ (2l−1)^i. Minkowski induction on the square functions then gives ‖F‖²_{2l} ≤ Σ(2l−1)^{ω(s)}|b_s|².
- Root factors: exp(O((T + k log T)/l)) = exp(o(K)) because μ_0 > γ and ρ < 1, and the nonsquare term is O(Z^{−10}) because
  l = o(k). Both verified.

**Discretization, p. 12.**
- The coefficients depend on M mod 4L by reciprocity (L odd), on h_0, θ, R and P.
- Derivatives: ∂_θ ≪ R√L/P and ∂_R ≪ √L/(RP), so mesh Z^{−100} gives O(Z^{−80}). The summed error is o(1).
- The max over a family fixed before sampling M legitimately dominates the adaptive (M-dependent) array. This is the uniformity
  that makes the moment transfer work.

**P ≠ 1 terms, p. 13.**
- P ≥ Z, the crude bound |G^{(P)}| ≪ √L/P, and the norm is ≤ Z^{−.99+o(1)}. With O(k^7) terms this is o(1).

**Witness event (3.15)–(3.22), pp. 13–15.**
- (3.16): the fibres of squaring on (Z/d)^* have size 2^{ω(d)}, and N/d ≥ Z^{4.9}.
- Small-s norm exp(O(K)). Off the event, the subfamily norm is exp(−.815K).
- Large s, low weight: the correlation (3.18) was reconstructed. The local Fourier bounds are 1/√ℓ at a prime dividing exactly
  one of d, d' (computed exactly as (1/√ℓ)·f_ℓ(−h c̄)) and 1 at a common prime.
  - Numerics: 200 random cases with d, d' | 105, 0 fails, max coefficient/A = 0.686. Control A/1.5 FAILS.
  - The geometric-sum bound is uniform in α (q ≤ L ≤ S^{1/4}). The normalization v/(R√(dd')) is independent of s. Pair
    count R√(dd')/(Sv).
  - The divisor product is Π(1+λ²+2λ/√ℓ).
- High weight (3.20): Rankin with T^{1/4}; the exponent −τK/(8 log u_0)·log T = −625K. Residue-uniform count, using
  S/(Lr) ≥ √S/(√2 L) ≫ 1. E_{s mod L}|F| ≤ 1.
- Constants: (τ + log(1+λ²))/2 = .00445 < .006 < .015.
- Hölder with the L^{2l} norm exp(O(K)) gives P(E) ≥ exp(−O(K)).

**Rational approximation (3.23), p. 16.**
- Splitting into progressions mod d gives quadratic coefficient α = svdθ and linear coefficient 2θsvx. The amplitude sum is
  ≤ d·2^{ω(d)/2}, so some progression has a sum of size ≥ Y_0e^{−K}.
- Weyl differencing plus the standard Σ_h min(Y, ‖hβ‖^{−1}) ≪ (H/r+1)(Y + r log r), with Dirichlet at Q_1 = Y_0²e^{−8K},
  forces r ≤ e^{8K}.
- (3.24): |n| = M‖aθ‖ ≤ X·svd·e^{O(K)}. Pigeonhole over a ≤ Z^{.12+o(1)}.

**Common centre (3.25)–(3.27), pp. 16–17.**
- Factorial moments: lifts mod a product ≥ Z^{k−10} number O(Z^{.15}). Low r(n) contributes ≤ Z^{6.15}J^{k−10} = o(J^kZ^{−.13}).
- Pairwise intersections ≤ k because 2H_0 < Z^{k+1}.
- Cauchy–Schwarz gives R_0 ≤ 2J, and then J_0 ≥ JZ^{−O(1/k)}.
- p ∤ a, hence p ∤ m, so t_p ≡ h/m.

**Kernels (3.28)–(3.31), pp. 17–18.**
- ε'_p = ε_pχ_p(m) is correct, since χ_p(x − h m̄) = χ_p(m)χ_p(mx−h).
- Dropping p | t_x costs O(k/J_0).
- (3.6) with J_0, single coefficient array, Σ|b_s|² ≤ k!/J_0^k. S = (2Z)^k > U, and S·k!/J_0^k = X^{o(1)}.
- Kernel count X^{2ε+o(1)}.
- Populations: (ut_x, m) = 1 since (h, m) = 1; O(2^{ω(m)}) roots; the diameter bound uses √a − √b ≤ √(a−b).

**Disjoint supports, p. 18.**
- A prime ℓ ≤ X^η dividing u_x and u_y gives ℓ | x−y. Since x−y is prime > X^{9/10}, this is impossible.
- So vw is squarefree and determines (|v|, |w|).

**Exceptional zero and split primes, pp. 19–20.**
- The Hadamard identity for real χ, and the ratio bounds b/a ≤ 1+1/c_1 (|γ| ≤ 1) and ≤ 5 (|γ| > 1).
- Siegel with ε_1 = 1/200 at conductor ≤ (log X)^{100}.
- Discarded pairs ≪ X/(log X)^{50}.
- Arithmetic: .05 − .01 − .0007 > .03.
- s = 1+10/log X ≤ s_0 = 1+1/log Q_0 because η ≤ 1/1000.

**Final collision, p. 20.**
- Upper bound (1+o(1)) log X. The equal-root term is X^{−2η}.
- Lower bound: at split primes, R_1 and c_pR_2 are disjoint by exclusion, so 1/a+1/b ≥ 4/(a+b) ≥ 4/p. The total is
  (1−10η+.06) log X, a contradiction since 10η ≤ .01.

**Parameter order.**
- δ is fixed from the assumed failure. Then (ρ, μ_0, γ, λ, τ) are absolute, η depends only on c_1, ε < η/100, and the
  Heath-Brown constant depends on ε.
- The X^{o(1)} terms depend on δ but tend to 0 along the T-sequence.
- I found no constant that silently depends on a later parameter.

**Sanity tests (brief item 6).**
- Drop exclusion, e.g. A = B = squares. Then §2.3's disjointness already fails at p ≡ 1 (mod 4). §3's two exclusion steps (pp. 18
  and 20) fail at exactly the split primes, where the example lives.
- Drop coverage, e.g. sparse infinite A, B with A+B ⊆ P, which exist conditionally under Dickson. Then §2.3 survives, but Lemma
  2.4's √X/(log X)³ lower bound fails. That bound is used in (3.4) (I ≫ √X e^{.016K}) and in the population sizes.
- So §3 uses both requirements where the intro says it does. I found no step that would also "prove" a false statement.

### Corollary 3.2 (p. 21)
- Dyadic decomposition in log p, O(L_*) intervals, each o(1) uniformly because T ≥ e^{αL_*}/2 → ∞. Correct.

## 4. What I could NOT check
- Heath-Brown 1995 (Acta Arith. 72), Theorem 1. The PDF was not retrievable. I relied on the Lean transcription plus memory; the
  Lean proves it in-house.
- Montgomery–Vaughan 2007 theorem numbers: 9.6–9.7 (Gauss sums), 11.3 / Cor. 11.10 (zero-free region + Landau–Page),
  Cor. 11.15 (Siegel), App. D.2 (Poisson). The book was not accessible. The mathematical statements used are standard and
  correctly applied.
- MV 1973 Theorem 1, Bonami 1970, Rota 1964, Gallagher 1971, Green–Harper. These are not load-bearing beyond standard facts I
  reconstructed; I did not check their theorem numbers.
- The §1 survey citations (Hanson, Croot–Mao–Yip, Croot–Mao–Pohoata–Yip, Shao, Croot–Elsholtz) are expository only and were not
  checked.
- I did not read the Lean beyond locating `FiniteSummands.lean`/`FiniteFactor.lean` and the quadratic-sieve statement.

## 5. Where a hole would most likely hide in §§1–3
The most delicate point is the moment transfer (3.13) together with the discretization on p. 12. The arrays C_s^{(P)} depend on
the random tuple M (through M mod 4L, h_0, θ, R and P|M), yet (3.13) is a statement for arrays fixed in advance. The argument is
only valid if:
- every M-dependent quantity is captured by a family of polynomial size fixed before sampling;
- the "max over family" step is paid for honestly (factor Z^c^{1/(2l)} = exp(o(K)));
- the off-event subfamily on p. 13 is itself a fixed family. It is: it is defined by grid values, not by the tuple.

I checked each of these, plus the exponent bookkeeping that makes Z^{O(1)/l} = exp(o(K)) (this needs μ_0 > γ) and
(J^{−k}k!)^{1/(2l)} kill the nonsquare term (this needs l = o(k)). They hold. The second candidate is the common-centre
pigeonhole (pp. 16–17), where averaged information (probability exp(−O(K))) becomes a single rational centre for J·Z^{−O(1/k)}
specific primes. The intersection bound (≤ k common primes, since 2H_0 < Z^{k+1}) makes that step rigorous, not heuristic. I
believe no hole is present in §§1–3.
