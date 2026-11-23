## Referee report: Della Pietra, Erdős #301 lower bound (repo commit 789c6f0, manuscript dated 30 July 2026)

### Verdict: HOLDS WITH FIXES

I re-derived every step of the human argument and could not refute it. I found no MUST-level error. The quantifier order is correct, every implied constant has the dependence the proof needs, and the specialization of de la Bretèche–Tenenbaum Theorem 3.1 checks out against the arXiv v6 text. The problems are expository: five SHOULD items and some NITs in the paper, plus one SHOULD against the README, whose numerical claim is not presented fairly.

Two caveats on what this rests on. It assumes BT Theorem 3.1 is correct as published. I checked Tenenbaum's inequality for content, not against the book's numbering. The proven ε is about exp(−exp(10⁹)).

I did not fetch erdosproblems.com by any route. The problem wording comes from the manuscript and your brief. The teorth/erdosproblems GitHub data still lists #301 as "open" (last update 2025-08-31).

---

### 1. Quantifier order (the crux)

| step | chosen | depends only on | check |
|---|---|---|---|
| 0 | A_h, z_h, q_h, A_t, z_t, q_t, c (eq. 22) | nothing | margins in Table 1 recomputed at 50 digits; all printed digits agree, E = −1.000317439… |
| 1 | K_h | step 0 | Lemma 2.2 (rough part) gives at most C(A_h,z_h)·Nρ_L·z_h^(−K_h), with C uniform in L, Y and K. So K_h is a constant fixed before L, and q_h^(K_h) is a constant, not a function of L. |
| 2 | L | steps 0–1 | needs three things, each uniform in L and K: Lemma 2.2's constant, Prop 4.1's constant, and Prop 5.1's constant |
| 3 | K_t = ⌈c log log L⌉ | L | top loss at most C(A_t,z_t)·N·(log L)^(−c log z_t) = N(log L)^(−1.000211), which is o(Nρ_L) as L→∞. The conflict cost is q_t^(K_t) ≤ q_t(log L)^(0.999782), which leaves a saving of (log L)^(−0.000218). |
| 4 | N₀ | L, K_h, K_t | absorbs three things: the inclusion–exclusion error, the second residual term of (21), which decays like (log N)^(E+1) = (log N)^(−0.000317), and the o(N) error inside |H_N|. |

Answers to your specific questions:

- **Is the constant in (16) independent of L, A, K?** It depends only on q_h, q_t, A_h, A_t, through α, β, γ, M and the factor 1/(−1−E) ≈ 3150. It is uniform in L > 2. The K's appear only as the explicit factors q^K. I re-derived (17)–(21): the first term carries (log X)^E(log L)^(−E−3) and the second (log L)^(−H−2)(log X)^H.
- **Does q^K growth kill the (log L)^(−1) saving?** No.
  - For q_h, K_h is fixed before L, so q_h^(K_h) is a constant.
  - For q_t, the growth is exactly offset by c·log q_t < 1.
  - The top loss is o(Nρ_L) because c·log z_t > 1. Lemma 2.2's unrestricted bound is uniform in K, so growing K_t does not break this.
- **Is ε = ρ_L/24 absolute?** Yes, since L is fixed once. The Lean development uses the same order: in `ConflictGlobal.lean`, `exists_eventualRoughThirdBudgets` picks K_h, then L (with K_t = `oddBudget L`), then N. `Conclusion.lean` uses ε = roughDensity L / 24.
- **How small is ε under this proof's own constants?**
  - The head margin A_h log z_h − (z_h − 1) is 5.0·10⁻⁹, so Lemma 2.2's geometric constant is about 2·10⁸.
  - That forces K_h ≳ 2.2·10⁵ and q_h^(K_h) ≈ e^(2.0·10⁵).
  - Closing the conflict budget then needs log log L ≳ 2·10⁵ / 0.000218 ≈ 9·10⁸.
  - Result: ε ≈ exp(−exp(~10⁹)). This is my back-of-envelope estimate, not a printed figure.

### 2. Input hypotheses

**de la Bretèche–Tenenbaum Theorem 3.1** (arXiv:2403.19320 v6, quoted from the TeX source):

> "For all α∈]0,1], β∈]0,1[, A⩾1, B⩾1, 0<ε⩽αβ/{50g²(βg+1)}, and uniformly under the conditions F∈M_k(A,B,ε), x∈N^{*t}, y∈N^{*t}, x:=min x_j ⩾ c{max x_j+‖Q‖}^β, x_j^α⩽y_j⩽x_j, we have Σ_{x_j−y_j<n_j⩽x_j} F(|Q_1(n)|,…,|Q_k(n)|) ≪ ℘y E_R(𝔰x) ∏_{g<p⩽x}(1−ρ_Q^+(p)/p^t), where c and the implicit constant depend at most upon g, α, β, A, B"

Here E_R(v) = Σ_{℘s⩽v} F̂(s)ρ#_R(s)/K(s)^t and 𝔰x = Σ x_j. The class M_k is defined by F(ab) ⩽ min{A^Ω(℘a), B(℘a)^ε}·F(b) whenever (℘a,℘b) = 1.

How each hypothesis holds in the manuscript's specialization (k = 3, t = 2):

- **Forms:** Q = X₁X₂(X₁+X₂) is primitive with g = 3, and the R_h are the Q_j themselves, so F̂ = F.
- **Class membership:** F_L(ab) = F_L(a)F_L(b) for coprime tuples. The gcd factor is multiplicative because the cross gcds equal 1, and every weight is ≤ 1. So F_L(ab) ≤ F_L(b), and F_L is in M₃(1,1,ε) for every ε > 0, uniformly in L.
- **Box:** take x₁ = 2X, y₁ = X+1, x₂ = 4X, y₂ = 3X, with BT's α = β = 1/2. The geometric conditions hold for X ≥ X₀, an absolute constant.
- **Local factors** (densities of exact valuation patterns): (10), (11) and (12) are correct.
  - A pattern with p dividing two of R, S, R+S has ρ# = 0, because p then divides the third.
  - If all three are divisible, F_L's coprimality factor kills the term.
- **Sieve product:** ∏_{3<p⩽2X}(1−(3p−2)/p²) ≍ (log X)^(−3).
- **Result:** (9) holds, uniformly in L.

**Tenenbaum, Theorem III.3.5 (3rd ed.)** — not checked against the book.
- The 3rd edition's table of contents has a §III.3.5, "Effective mean value estimates for multiplicative functions", which is consistent with the citation.
- The standard statement there is: Σ_{n≤x} f(n) ≤ (A+B+1)·(x/log x)·Σ_{n≤x} f(n)/n, given Σ_{p≤y} f(p) log p ≤ Ay and Σ_p Σ_{ν≥2} f(p^ν) log(p^ν)/p^ν ≤ B.
- Prop 2.1 follows from it via Mertens and the bound (1−1/p)(1+S_p) ≤ 1 − 1/p + S_p. The manuscript does not write this deduction (S5).
- The hypotheses hold uniformly in L: the weights z < 2 sit only on primes ≥ 3 > z.

### 3. Every other step re-derived

- **Lemma 3.1:** ak < N. Correct.
- **Lemma 3.2:** k = 2 only, head in H. Odd head forces t, r, s odd, so both endpoints are even and lie in T. Coordinates unique, and s < 2r from c < 3a. Correct.
- **Lemma 2.2:** the maximal argument by Markov is correct, with ratio exp((z−1) − A log z) < 1.
- **Lemma 2.3:** both regimes correct.
- **Joint indicator (19):** exponents γ (on t), γ (on r), α (on s), β (on r+s) confirmed.
- **Second term:** H + γ = E + 1 < 0 confirmed.
- **Assembly:** 1/6 − 1/24 ≥ 1/12, so |A_N| ≥ N/2 + Nρ_L/24. Correct.

### 4. Objections

**MUST:** none.

**SHOULD (paper):**

- **S1 (Prop 5.1, eq. 16):** "If E<−1, then, for fixed real parameters, E_N ≪ q_h^{K_h}q_t^{K_t}{N(log L)^{−2}+o_L(N)}." The statement never says the constant is uniform in L and in K_h, K_t ≥ 0. Section 7 depends on exactly that, since it sends L→∞ with K_t = K_t(L). The proof does deliver it; the statement should say so.
- **S2 (eq. 21):** "One dyadic block contributes ≪ … (log(3N/X²))^{γ−1}." This replaces log(3N/(r(r+s))) by log(3N/X²) under the negative exponent γ−1. That needs a lower comparison which the text omits. The fix is in AUDIT §4: Z ∈ [2,12], V ≥ 1, so log 3V ≥ (log 3/log 36)·log 3ZV. AUDIT.md says all three of its corrections are "present in the current paper/main.tex"; this one is not.
- **S3 (§5 and §7):** the same symbol o_L means opposite limits.
  - In (16), o_L(N) means o(N) as N→∞ with L fixed.
  - In §7, "so the last display is o_L(Nρ_L)" means o(Nρ_L) as L→∞, uniformly in N.
  - The quantifier order can only be recovered from the final "parameter order" line.
- **S4 (eqs. 4–5):** these are displayed for all Y ≥ 1 but are false uniformly in L when Y < L. For example at Y = 2 the left side is 2 while the right side → 0 as L grows. "If Y<L, the claim is immediate" comes after them. Harmless, since they are only used with Y ≥ L, but as printed they are wrong.
- **S5 (Prop 2.1):** it is presented as "the specialization of [5, Theorem III.3.5]". It is in fact a corollary that needs Mertens plus the Euler-product bound on Σ f(n)/n. The deduction should be written out.

**SHOULD (README):** the N = 10⁶, L = 7 numbers are not presented fairly.
- My independent C implementation reproduces them exactly: 44,445 heads, 4,242 deleted, 5,391 relations, 540,204 elements.
- That set is the simple proxy: all 7-rough heads and the full top half, with no head or top regularity. The paper's §8 calls it a "proxy"; the README calls it "the construction".
- The README's sentence "The distance between the proven ε and this observed ≈0.04 is analytic loss … not a property of the construction" is wrong. At fixed L the proxy's advantage shrinks:

| N | heads deleted | relations per head | density − 1/2 |
|---|---|---|---|
| 10⁴ | 6.1% | 0.070 | 0.0419 |
| 10⁵ | 8.0% | 0.094 | 0.0409 |
| 10⁶ | 9.5% | 0.121 | 0.0402 |
| 10⁷ | 10.6% | 0.148 | 0.0397 |
| 10⁸ | 11.7% | 0.174 | 0.0392 |

- Relations per head grow linearly in log N. That matches the paper's own exponent E = 0 when there is no regularity, and is expected (Maier–Tenenbaum divisor propinquity) to push the deleted fraction toward 1. I have not proved that for rough integers.
- The actual construction has no heads at any computable N, because L must be astronomically large.

**NIT:**
- **"at most its full Euler product" (§4 proof):** the untruncated product diverges. It must be the product over p ≤ 𝔰x ≍ X, which is what the next display actually uses.
- **"Because of the factor (n₁,n₂)=1, no local pattern with two positive form valuations contributes":** incomplete. The (R, R+S) and (S, R+S) patterns vanish because ρ# = 0, not because of the gcd factor.
- **BT's geometric parameters:** never specified, and the letters clash with the paper's weights α, β.
- **"Hence, for all sufficiently large N, |H_N| ≥ Nρ_L/12":** stated before L is chosen.
- **Abstract:** "bounds the mixed conflicts by O(N(log L)^{−2+θ})" drops the q_h^{K_h} factor and the o_L(N) term.
- **README:** calls it the Erdős–Graham "conjecture"; they asked a question.
- **AUDIT.md:** overstates which of its corrections reached main.tex. The Y < L split is present but comes after (4) and (5); the two-valuation reason is truncated; the S2 comparison is absent.

### Not refereed

- The Lean development: I consulted it only for the parameter order. A separate replay of it was in progress at the time (logs/replay.out).
- The README's upper-bound claim (15437/19344).

Scratch files are in `/home/exedev/MathDyad/erdos301/dellapietra/referee/`: `margins.py`, `sim/sim.c`, `sim/trend_L7.txt` and the BT source under `bt/`. Ignore the "simple" column of `sim/trend_L7_full.txt`: it uses the wrong head count when head regularity is on.

Sources:
- [AMS GSM 163 end matter (§III.3.5 table of contents)](https://www.ams.org/books/gsm/163/gsm163-endmatter.pdf)
- [TauCetiRoadmapJobs issue #6063 (Hall–Tenenbaum inequality summary)](https://github.com/TauCetiProject/TauCetiRoadmapJobs/issues/6063)
- arXiv:2403.19320 v6, fetched directly