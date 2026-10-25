# Seat P: hostile referee report on printed Sections 6, 7, 8 (pp. 22–33)

Paper: OpenAI, "Short Egyptian fractions" (25 Sep 2026). My scope: Corollary 1.2 (counting), Corollary 1.3 (prescribed denominator), Lemma 6.1, (6.1)–(6.2), Lemma 7.1, Lemma 7.2, Proposition 8.1, Lemmas 8.2–8.4, (8.1)–(8.3), and the proof of Corollary 1.3 in §8.3.

I read the LaTeX source (`counting.tex`, `prescribed.tex`, plus `elementary.tex` for Lemma 2.2, which §8 uses) against the printed numbering in `paper.txt`. I re-derived every step by hand and ran exact-arithmetic checks, all under `ulimit -v 4000000; timeout 600`. Scripts are in `/tmp/oaimath/025/seats/P_scripts/`.

**Bottom line.** I found no FATAL or GAP objection in Sections 6–8. Every load-bearing inequality re-derives. The explicit constants recompute exactly. The cited external results say what is used, with the needed uniformity. Every small-case claim I could test passes, and I tested both branches of each case split. The objections below are ERROR-NONFATAL or EXPOSITION.

---

## 1. Section 6: Corollary 1.2

### 1.1 Lemma 6.1 (repetition removal at total one, keeping a multiple of odd Q)
- Both replacement identities check: 2/m = 1/(m/2) for m even, and 2/m = 1/((m+1)/2) + 1/(m(m+1)/2) for m odd.
- **Invariant.** A denominator divisible by Q survives. If Q | m and m is even, then Q | m/2 because Q is odd. If m is odd, m | m(m+1)/2. Holds.
- **Exclusions.** Denominator 1 forces the list (1), which has no multiple of Q > 1. A repeated 2 forces (2,2), which also has none. So every repeated odd m is ≥ 3, every repeated even m is ≥ 4, and every replacement is legal. Holds.
- **Termination.** An odd replacement strictly decreases the sorted tuple lexicographically. I checked this: let e be the multiplicity of (m+1)/2. Position p+e+1 holds (m+1)/2 in the new tuple and a larger entry in the old one. Lex order on ℕ^t is a well-order. Even replacements shorten the list, so at most t−1 of them occur.
- Stress test (`check_cleanup.py`): 4,000 random multisets (Q ∈ {3,5,9,15,21,45,105}, up to 400 terms, random choice of which repeat to resolve). 0 failures, at most 248 steps.

### 1.2 Branching over divisors, (6.1)
- **Identity.** 1/(n+d) + 1/(n+n²/d) = 1/n holds, and so does n < n+d < 2n < n+n²/d for proper d | n.
- **Collision count.** Each unchanged denominator kills at most one d through n+d and at most one through n+n²/d. That leaves at least τ(n)−1−2(s−1) = τ(n)−2s+1 ≥ 2^r−2s+1 good choices.
- **No double counting.** Every output set has exactly s+1 elements. Removing the fixed set S∖{n} leaves exactly {n+d, n+n²/d}, and the smaller one returns d. So the map d ↦ set is injective and the outputs are distinct sets. The brief's question 1 is answered: the k-term outputs are pairwise distinct as sets, and denominators within each expansion are distinct.
- Concrete run: Q = 105, shortest 104/105 = 1/2+1/3+1/7+1/70, giving S = {2,3,7,70,105}. This yields 7 distinct valid 6-term expansions, as expected.

### 1.3 Padding injection, (6.2)
- **Injectivity.** v ↦ (v+1, v(v+1)); these become the two largest entries, and the inverse is "delete the two largest, reinsert the second largest minus one". Injective.
- Exhaustive check on all expansions of lengths 3–6 (1 + 6 + 72 + 2320 tuples): every image is a valid expansion, inverts correctly, and no two collide.
- This is the folklore F(k) ≤ F(k+1). Bloom–van Doorn (BvD) also attribute it to the introduction of Konyagin [14]. Konyagin's p. 312 is his first page, so the citation is plausible; I could not open that paper. It is not load-bearing, because the proof is given.

### 1.4 Parameters and the upper bound
- r = ⌊exp(k/(2B))⌋ gives ℓ ≤ B log r ≤ k/2. Then F(k) ≥ 2^{r−1} for large r, since s = O(log r), and log log F(k) ≥ k/(2B) + O(1). Holds.
- **Upper bound.**
  - R_i ≥ 1/P_{i−1}, because R_i has a positive integer numerator over P_{i−1}.
  - R_i ≤ k/n_i, because the terms are ordered.
  - Hence n_i ≤ kP_{i−1} and P_i ≤ kP_{i−1}². Induction gives P_i ≤ k^{2^i−1} and n_i ≤ k^{2^{i−1}}, so F(k) ≤ k^{2^k−1}. Correct.

**Brief question 1, uniformity.** The lower bound needs only N(Q−1, Q) ≪ log log Q along Q = product of the first r odd primes: one numerator per denominator, not uniformity in a. Proposition 8.1 also supplies this independently of Theorem 1.1. With m = Q it gives a distinct expansion of 1 containing exactly 1/Q, of length O(log log Q), and Lemma 6.1 is then unnecessary. So Corollary 1.2's lower bound does not actually depend on Sections 3–5 (see O1).

---

## 2. Section 7: Lemma 7.1 and Lemma 7.2

### 2.1 Lemma 7.1 (greedy prefix that skips m)
I re-derived each step.

**Ordinary step**, a = ⌈q_i/R_i⌉:
- 1/n ≤ x_i < 1/(n−1).
- 0 ≤ R_{i+1} < R_i, because (n−1)R_i < q_i.
- x_{i+1} < 1/(n(n−1)) ≤ 1/n.
- n < 1/x_i + 1, which gives x_{i+1} < x_i²/(1+x_i).

**Exceptional step** (a = m, replaced by m+1):
- (m−1)R_i < q_i ≤ mR_i.
- R_i ≤ R_{i+1} < 2R_i.
- 0 < x_{i+1} < 2/(m²−1) < 1/(m+1). The last inequality is equivalent to m > 3, which is exactly why the lemma assumes m ≥ 4.

**Consequences.**
- After the exceptional step all later denominators exceed m+1, so it happens at most once and the denominators strictly increase.
- R stays below 2m.
- a ≤ q_i, so n_{i+1} ≤ q_i + 1.
- x_1 = (m−2)/(2m). With at most one non-squaring step, x_i ≤ 2^{−2^{i−2}} for i ≥ 2, so j < 3 + log₂log₂T.
- q_j ≤ (T−1)T < T², because T is an integer.

**Brief question 2, distinctness.** The tail is distinct from the prefix as well as from m. Every tail reciprocal is at most the tail sum R/q, and R/q < 1/n_i for every i and < 1/m. So every tail denominator exceeds every n_i and m. Nothing can be reused.

**Exhaustive test** (`check_prefix.py`): m = 4…3000, T ∈ {2m², 2m²+1, 7m³, m⁶, 2m·10³⁰}, every assertion of the lemma checked with exact Fractions. 0 failures. The exceptional step occurred 15 times, so that branch was exercised. The minimum slack in the j bound was 1.74, and R/m never exceeded 0.952. The uncut variant (run to R = 0) terminates for m = 4…40 with a valid marked expansion. This is the paper's "finite exceptional m" device.

**The qualitative argument.** With T = 2m², Lemma 7.1 gives 1 ≤ R < q and 2m² ≤ q < 4m⁴. Theorem 1.1 then applies to the unreduced R/q. N(a,b) depends only on the value, and the theorem is stated for unreduced fractions. Holds.

### 2.2 Lemma 7.2 (padding that keeps m)
- **Case m ≠ n_r:** split n_r.
- **Case m = n_r = v, s = n_{r−1}:** split s unless v ∈ {s+1, s(s+1)}.
- **Composite s = ab:**
  - Identity: b(s+a) = s(b+1), so 1/(s+a) + 1/(b(s+a)) = 1/s.
  - The chain s+1 < s+a < b(s+a) < s(s+1) puts both new denominators strictly between the two forbidden values.
- **Prime s = p:**
  - p is odd, because p > n_{r−2} ≥ 2 and this needs r ≥ 3.
  - The other terms sum to A/B with p ∤ B.
  - 1−A/B = (2p+1)/(p(p+1)) gives B ≡ 0 (mod p).
  - (p+2)/(p(p+1)) gives 2B ≡ 0 (mod p).
  - Both are impossible. Correct.

**Hypotheses.** r ≥ 3 is needed for n_{r−2} to exist, and it is enough. For r = 1, 2 we have D_1 = D_2 = ∅, so D_r ⊆ D_{r+1} trivially. The Corollary 1.3 proof correctly notes that any marked expansion has at least 3 terms. The lemma never removes or duplicates m: m is either untouched (it is not the split term), or it is v and both new terms avoid v and lie above every other denominator.

**Comparison with van Doorn–Tang (vDT) Lemma 2.1** (arXiv:2512.22083v2). vDT state it for k ≥ 2, and the paper's r ≥ 3 is equivalent. The paper calls this "the padding lemma of van Doorn and Tang; we include a proof", but its proof is sharper, not a copy:
- vDT show only that v = p+1 is impossible for prime p, treat v = p(p+1) as a live case, and handle it with a further split of n_{k−2}.
- The paper's mod-p argument shows v = p(p+1) is also impossible for odd p. I checked this, and it is correct. vDT's extra case is vacuous for r ≥ 3.

(See O4.)

**Exhaustive test** (`check_padding.py`, `check_exc7.py`):
- For every expansion of length 3–6 and every m in it (14,309 pairs), the lemma's construction yields a valid distinct (r+1)-expansion containing m. Each output is in the enumerated set for length r+1. 0 failures.
- The case v ∈ {s+1, s(s+1)} never occurs for r ≤ 6. At r = 7 it occurs exactly 4 times, and in every one s is composite (189, 35, 35, 20). The composite branch is correct there for every factorisation a·b = s. The prime case never occurs, as the lemma predicts.

---

## 3. Section 8: Proposition 8.1, Lemmas 8.2–8.4, Corollary 1.3

### 3.1 Lemma 8.2 (common supply)

**Size bound (8.1).**
- ℓ(Y) = ⌈16 log m/log 2⌉ and log ℓ(Y) = L + O(1).
- The prime number theorem (PNT) gives θ(p_ℓ) ~ ℓ log ℓ, so log P(Y) = (16/log 2 + o(1)) log m·L.
- Squaring gives 32/log 2. The ⌊L⌋! factor is O(L log L).
- P(Y) ≥ 2^{ℓ(Y)} ≥ Y⁴, so K_m > m. Holds.

**Larger-sieve count (8.3).**
- If |A_p| ≤ p^{3/4} ≤ u^{3/4}, then N²/u^{3/4} − N ≥ N²/(2u^{3/4}), because N = 2^{ℓ(u)} ≥ u⁴.
- Each difference |a−b| < P(u) has at most log P(u)/log 2 prime factors.
- This gives B(u) ≤ 2u^{3/4} log P(u)/log 2.

**Three primes.** Kumchev 1997, display (1) — I rendered and read the page — is Σ_{p1+p2+p3=N} 1 = ½(1+o(1)) 𝔖(N) N²/log³N for large odd N. This is an *ordered, unweighted* count with o(1) → 0 in N alone. Display (2) is exactly the singular series the paper prints.
- For odd u the p = 2 factor is 2, so 𝔖(u) ≥ 2∏_{p>2}(1−1/(p−1)²) ≈ 1.3203 (I computed this).
- That gives an absolute lower bound c·u²/log³u above an absolute threshold. The uniformity claim is correct.
- The threshold is ineffective (Siegel–Walfisz), which is harmless because Corollary 1.3 claims only "sufficiently large k".
- Excluding triples with an exceptional prime costs at most 3uB(u) ≪ u^{7/4+o(1)} = o(u²/log³u). Holds.

**Five products.**
- Glibichuk–Konyagin Proposition 1.1 (read in the arXiv PDF) is |Σ_{x∈X,y∈Y} e(axy/p)| ≤ √(p|X||Y|). That is exactly the bound used, and the paper also re-proves it.
- So |E e_p(rU)| ≤ √p/h < p^{−1/4}, and Pr(ΣU_i = 0) ≥ (1−(p−1)p^{−5/4})/p > 0.
- Lifting gives e_i | P(u)², a sum divisible by p, and p = Σe_i/t.
- 3·5 + 1 = 16 summands, P(u) | P(Y) for u ≤ Y, and s ≤ S_0 is handled through ⌊L⌋!. Holds.

**Numerics** (`check_supply.py`):
- For odd u ∈ {101, 501, 1001, 2001, 3001}: N ≥ u⁴, and the number of exceptional primes is B(u) = 0. Bound (8.3) is 8.5·10³ to 2.3·10⁵, so it is very loose but correct.
- Brute-force check of |E e_p(rU)| ≤ √p/h for p = 31, 61, 101 with |H| ≈ p^{3/4}: holds, with the maximum 4–5 times below the bound.

### 3.2 Lemma 8.3 (divisor density)
- The induction is correct. In the gap q < w < n the divisor q works, because w < n ≤ q+1 ≤ mq.
- Over all real w ∈ [1,q], the property is equivalent to "every ratio of consecutive divisors of q is at most m".
- Test: greedy q for m < 400 (two cutoffs) gives max ratio/m = 0.5. 3,000 random chains with n ≤ q+1, biased to n = q+1, give max ratio/m = 1.0, so the bound is attained and sharp.
- The paper correctly insists on the *unreduced* q (`Do not cancel common factors`). Reduced denominators would not have this property.

### 3.3 Lemma 8.4 (grouping)
- For X_i > m⁴: w = X_i/m² ∈ (m², q], d_i ∈ [X_i/m³, X_i/m²], s_i = ⌊X_i/d_i⌋ ∈ [m², m³], and X_{i+1} = X_i mod d_i < X_i/m².
- The count of big steps is at most ⌈log X/(2 log m)⌉, so G ≤ log X/(2 log m) + 2.
- The term identity 1/((q/d_i)(K/e)t) only needs d_i | q and e | K. Correct.
- Test with exact integers on greedy q for m = 4…59 and 205 values of X each: every invariant holds, and max(G − bound) = −1.0.

### 3.4 Proposition 8.1, end to end
- T = 2mK_m is an integer ≥ 2m².
- j ≤ (1/log 2 + o(1))L.
- X = RK_m < 2mK_m ≤ q.
- G ≤ (16/log 2 + o(1))L.
- Lemma 2.2 (Takenouchi) on the tail keeps the term count and makes the terms distinct. I re-checked its identities and the increases (p−1)² and 2p².
- Total length 1 + j + 16G ≤ ((1+256)/log 2 + o(1))L = (257/log 2)L. I recomputed this: 257/log 2 = 370.77.

**Full numerical run** (`check_supply2.py`, m = 50):
- K = P(m⁴)²·60!. This adds 60! to cover small s, standing in for the "sufficiently large m" device. log K = 1088.
- For every m < 400, the greedy prefix (with T = 2mK) stopped at R = 0, so the R > 0 branch is never reached at small m. I therefore drove the tail construction with a synthetic chain obeying exactly Lemma 8.3's hypothesis (q₀ = m, n ≤ q+1, up to q ≥ 2mK, 2,931 bits), plus R = 21.
- Results:
  - The divisors were found by the lemma's own constructive recursion, with no factoring.
  - G = 94 against the bound 141.5.
  - Every s_i had an explicit supply representation with at most 16 summands and e | K.
  - That gave 1,458 tail denominators (≤ 16G = 1504), all integers.
  - **Exact Fraction sum of the tail = R/q.**

### 3.5 Corollary 1.3
- **Lower bound.** Fix c < 1/A and ε with c(A+ε) < 1. Marked expansions for m < M come from the uncut greedy, and k* is their maximum length. For k ≥ k* every 2 ≤ m ≤ e^{e^{ck}} has length ≤ k, and Lemma 7.2 pads to exactly k. So v(k) > ⌊e^{e^{ck}}⌋.
- **Brief question 3, small markers.** Absorbing them into the liminf is legitimate: for fixed c they are finitely many, with bounded lengths.
- **c = 1/600.** Valid because 1/600 = 0.001667 < log 2/257 = 0.002697.
- **"Equivalently".** The statement "every fixed c < log 2/257 satisfies v(k) ≥ exp(exp(ck)) eventually" is genuinely equivalent to the liminf bound.
- **Endpoint.** The paper correctly refuses to claim the endpoint c = log 2/257.
- **Upper bound.** D_k ⊆ [2, k^{2^{k−1}}], so v(k) ≤ 1 + k^{2^{k−1}} for all k ≥ 1. For k ≥ 2, log log v(k) ≤ k log 2 + log log k, because log 2 ≤ 2^{k−1} log k. Hence limsup ≤ log 2.

**Brief question 4, consistency with Quanyu Tang (#293 thread).** Tang's v(k) ≤ s_k (Sylvester; max denominator s_k − 1) and the site's v(k) ≤ kF(k)+2 ≤ c₀^{(1/5+o(1))2^k} are both much sharper than 1 + k^{2^{k−1}}. All three give limsup ≤ log 2. The paper's intro says outright that its bound is "convenient rather than best known". Consistent.

---

## 4. Small-case numerics (brief question 5)

I enumerated all distinct expansions of 1 for k ≤ 7 exactly (`egy_enum.py`: DFS plus closed-form two-term tails via divisors of den², each tuple re-summed with Fraction). I did one more k than asked.

| k | F(k) (computed = public) | v(k) (computed = public) | max denominator (= s_k − 1) | 1 + k^{2^{k−1}} |
|---|---|---|---|---|
| 1 | 1 | 2 | 1 | 2 |
| 2 | 0 | 2 | – | 5 |
| 3 | 1 | 4 | 6 | 82 |
| 4 | 6 | 11 | 42 | 4097 |
| 5 | 72 | 17 | 1806 | 1+5¹⁶ |
| 6 | 2320 | 103 | 3263442 | 1+6³² |
| 7 | 245765 | 733 | 10650056950806 | 1+7⁶⁴ |

Checked for every k ≤ 7, across all expansions, with 0 failures (`check_small.py`):
- n_i ≤ k^{2^{i−1}} and P_i ≤ k^{2^i−1};
- F(k) ≤ k^{2^k−1};
- v(k) ≤ 1 + k^{2^{k−1}};
- v(k) ≤ kF(k) + 2 and v(k) ≤ s_k;
- log log v(k) ≤ k log 2 + log log k for k ≥ 2;
- D_3 ⊆ D_4 ⊆ D_5 ⊆ D_6 ⊆ D_7;
- "a marked expansion has ≥ 3 terms".

The eventual bound v(k) ≥ e^{e^{k/600}} ≈ 2.72–2.75 fails at k = 1, 2 (v = 2) and holds for 3 ≤ k ≤ 7. It is claimed only for large k, so there is no conflict. The public v(8) = 27539 and v(9) = 13856993 also sit comfortably inside both bounds.

---

## 5. Objections

- **O1. EXPOSITION (significant, not an error).** §8 needs nothing from Sections 3–5. Proposition 8.1 uses only Lemmas 2.2, 7.1, 8.2–8.4, PNT and Vinogradov.
  - Its machinery, started at q₀ = b instead of q₀ = m, proves Theorem 1.1 directly. Lemma 8.3 works with ratio b from q₀ = b, the greedy numerator stays < b, X = A·K_b, and G = O(log log b). BvD's exposition makes the same observation in its §6, and its Theorem 1 proof is extracted from this section.
  - It also proves Corollary 1.3 outright.
  - With v(k) ≤ kF(k)+2, it also proves Corollary 1.2's lower bound. The paper notes neither fact.
  - Consequence for the referee panel: Corollaries 1.2 and 1.3, and in fact Theorem 1.1's upper bound, survive any defect found in Sections 3–5.
- **O2. EXPOSITION.** In the Corollary 1.2 proof the paper writes "Our initial set contains a multiple of Q > 1, so it is not the singleton {1}; the operation applies to all the expansions just constructed." The branched expansions need not contain a multiple of Q any more, since n was replaced. (6.2) applies to them because they have s+1 ≥ 2 terms.
- **O3. EXPOSITION.** In the same proof the paper writes "Together with the lower bound, this yields log log F(k) ≤ k log 2 + log log k." The lower bound is used only to make log log F(k) defined (F(k) > e). The phrasing suggests it does more.
- **O4. ERROR-NONFATAL (attribution).** In Lemma 7.2 the paper writes "This is the padding lemma of van Doorn and Tang [22, Lemma 2.1]; we include a proof." vDT's Lemma 2.1 is stated for k ≥ 2, and its prime case keeps v = p(p+1) as possible and treats it separately. The paper's proof shows that case is impossible. That is a correct and simpler argument, but not vDT's proof. This is attribution only and does not propagate.
- **O5. EXPOSITION.** The thresholds in Lemma 8.2 (Vinogradov, the exceptional-prime count) and hence k₀ in Corollary 1.3 are ineffective as written. That is harmless, because only "sufficiently large k" is claimed and no explicit k₀ is asserted.

---

## 6. Cited results used in my sections
- **Kumchev 1997, (1)–(2)** — says exactly what is used: an ordered unweighted three-prime count with o(1) in N only, and the same singular series (verified on the rendered page).
- **Glibichuk–Konyagin 2007, Proposition 1.1** — the bilinear bound √(p|X||Y|), exactly as used (verified).
- **van Doorn–Tang, Lemma 2.1** — D_k ⊆ D_{k+1} for k ≥ 2 (verified). The proof differs; see O4.
- **Selberg 1949 (PNT)** — standard, used only as θ(p_n) ~ n log n.
- **Konyagin 2014, p. 312 (padding injection)** — not opened. It is folklore, BvD attribute it the same way, and it is not load-bearing.
- **Elsholtz–Planitzer, Corollary 3(2)** — used only in a remark, and consistent with the #148/#293 pages.

## 7. Lean statement alignment (statements only; the kernel replay is the coordinator's)
In `ComparatorChallenges/EgyptianFractions.lean`, these theorems match the printed statements, including the 0-indexed exponent `k^(2^i.val)` = k^{2^{i−1}} and `1 ≤ k →` on the v bound:
- `one_expansions_finite_and_bounded`
- `counting_double_log_order`
- `exact_marker_padding` (r ≥ 3)
- `quantitative_marked_length` (257/log 2 + ε)
- `missing_denominator_semantics`
- `prescribed_denominator_corollary` (1/600, liminf ≥ log2/257, limsup ≤ log 2, and the ∀c < log2/257 eventual form)

The `Filter.liminf`/`limsup` conjuncts are not junk-value-vulnerable: the sequence is bounded and eventually positive, and the junk-free conjuncts (the ∀c form and the v ≤ 1+k^{2^{k−1}} bound) carry the content independently.

VERDICT: HOLDS AS READ
