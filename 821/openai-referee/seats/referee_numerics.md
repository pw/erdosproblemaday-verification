# Referee report — seat `numerics` (exact identities and small-case checks)

Paper: OpenAI preprint "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026, family 011), `/tmp/oaimath/011/paper.pdf`. Every formula used here was read off the rendered PDF pages (pp. 4–5, 8–9, 18–20, 23–25, 28–29, 32–34, 49–51, 57–61, 65–66), not off the text extraction.

Method: brute force / exact rational arithmetic / high-precision quadrature in python3 (numpy 2.4.4, scipy 1.17.1, sympy 1.14, mpmath 1.3), all run under `nice -n 19`, single-threaded BLAS, at most ~40 CPU-s per script. Scripts live in `/tmp/oaimath/011/numerics/` (my own directory; nothing from the downloaded files is executed). Each script that could pass vacuously carries a **negative control** (a deliberately wrong variant that must fail), and it does fail where shown. All scripts and their outputs are reproduced verbatim in the Appendix.

## Result table (items (a)–(k) of the numerics brief)

| item | location (PDF page) | claim tested | result |
|---|---|---|---|
| (a) | (3.40)–(3.41), p.23 | Σ_π μ(π)1_{C_π} = 1_{distinct performed values}, blocks of size ≥2 over *potential* addresses, repeats allowed, unperformed addresses allowed | **PASS** — 12,331 cases (exhaustive for n ≤ 5 addresses, values in {2,3,5}, all performed-patterns; 3,000 random for n = 6), 0 failures. Negative control (drop the (|B|−1)! factor): 123/364 failures. |
| (b) | (3.42), p.24 | [t^r]Π_{j<A}(1+jt) = Σ_{r(π)=r}\|μ(π)\| ≤ (Σj)^r/r! ≤ A^{2r}; "a rank-r collection involves at most 2r addresses" | **PASS** for all A ≤ 8, all r (coefficients are the unsigned Stirling numbers c(A,A−r)); max over r ≥ 1 of coefficient/A^{2r} = 0.4375 (A=8); max addresses/rank = 2 exactly. |
| (c) | (4.22)–(4.24), p.33 | C(M−m−ℓ,j−m)/C(M,j) = (j)_m(M−j)_ℓ/(M)_{m+ℓ}; ≤ 2(j/M)^m(1−j/M)^ℓ ≤ 2(m/(m+ℓ))^m(ℓ/(m+ℓ))^ℓ ≤ θ_m = 2ℓ^ℓm^{−ℓ} when M ≥ (m+ℓ)(m+ℓ−1); and the *meaning* (fraction of ‖F‖² surviving in F_full, and its tensorization over groups) | **PASS** — identity exact on 43,366 (M,m,ℓ,j) (m ≤ 6, ℓ ≤ 4, M < 60), 0 failures; bound chain 0 failures (max fraction/θ_m = 0.25). Direct Efron–Stein computation on random within-group-symmetric functions with non-uniform i.i.d. labels: ‖F_full‖² equals Σ_j frac·W_j to 1e−8…1e−16 (1 group, 5 cases) and the product-of-fractions prediction (2 groups, 3 cases); negative control (fraction without the last-ℓ exclusion) visibly wrong. |
| (d) | (4.26), p.34 | Σ_{∅≠A⊆U,∅≠B⊆V}(−1)^{\|A\|+\|B\|} = 1 for U,V ≠ ∅ | **PASS** (\|U\|,\|V\| ≤ 6); = 0 when U or V empty, matching "If either missing set is empty, no comparison survives". |
| (e) | (6.15)–(6.20), pp.50–51 | forward identities m′−m = 2ek, h′−h = kn, z = m′h, z+k = mh′; (6.20) formulas for e, n; converse; k < 0; role of (m,k) = 1 | **PASS** (forward: 47,400 solutions, 23,700 with k < 0, 0 failures; converse with (m,k)=1: 14,819 tuples, 0 failures). **Converse FAILS without coprimality**: explicit (k,m,m′,h,h′,e) = (3,3,9,2,7,1): m′h = 18 = z, mh′ = 21 = z+k, m′ ≡ m (mod 6), e = 1 > 0, (6.18) holds (15 = 15), but n = (2eh+1)/m = 5/3 ∉ ℤ. 11,964 such failures in the box. In the paper's W-rough setting coprimality is automatic and the map is a genuine bijection (toy W = 13: forward image = independently enumerated converse set, 16,706 elements, and the converse maps back exactly). See Objection 1 (COSMETIC). |
| (f) | (7.15), (7.18), (7.19), pp.59–60 | ∫_{b1}^{1/2} D_α(1−α)dα/α = D_{b1}(1) − 1, D from the simplex definition (7.15); D_{b1}(1) vs e^{−γ}/b1 | **PASS**: b1 = 0.3: both sides 0.8699640129 (diff 9e−16); b1 = 0.2: 1.8072723413 (4e−16); b1 = 0.15: 2.7430631053 (−3e−15). D computed by Fubini on the *last* coordinate (not the minimum-coordinate decomposition that (7.18) asserts), cross-checked by direct nested quadrature (b1 = 0.3, 12 digits) and by Buchstab's ω via its delay-differential equation (D_γ(w) = ω(w/γ)/γ, agreement 1e−9). D_{b1}(1)/(e^{−γ}/b1) − 1 = −8.4e−4, −8.9e−6, −3.2e−8: (7.19) holds with a super-exponentially small error, as claimed. Negative control (roughness level fixed at b1 instead of the minimum α): sides disagree (0.915 vs 0.870 etc.). |
| (g) | Lemma 2.9, (2.6), pp.8–9 | V ≤ 1_{no bad} ≤ U, U ≥ 0, U−V ≥ 0, \|coefficients\| ≤ 1 for U, V, U−V, level z^{4h+2} | **PASS** on z = 7, h = 2 (blocks {3,5,7},{2}; all 16 assignments), z = 50, h = 2 and h = 4 (15 primes, all 32,768 assignments); level exponents attained 2.75 / 4.26 / 6.06 vs proof bound Σh_j2^{−j}+1 and claimed 4h+2. Also Σ_{n≤5000}V(n) ≤ #{n ≤ 5000 coprime to the primes} ≤ ΣU(n) and E V ≤ Π(1−1/p) ≤ E U. Negative control (odd h = 1, excluded by the lemma): U ≥ 0 and the sandwich FAIL, as they must. |
| (h) | Lemma 4.2, (4.5), p.28 | \|Σa_nb_te(αnt)\| ≪_C ‖a‖‖b‖[U+(1+V/r){U+r log 2r}]^{1/2} | **PASS**: U = V = 50, r = 7, u ∈ {1,2,3,6}, β ∈ {0, ±1/49, 0.37/49}, intervals [1,50] and shifted: worst case (largest singular value) / bracket^{1/2} = 0.824; scan r ≤ 60 (all branches): worst 0.974 (at r = 1, the trivial branch); r ≥ 2 up to r = 120: worst 0.938 (r = 2); unbalanced (200,20),(20,200),(150,150),(300,300): ≤ 0.996. The implied constant is ≈ 1 for C = 1. |
| (i) | (8.1)–(8.2), p.66 | X = 10^6, δ = 0.1: k, M, both sides | **PASS as an asymptotic argument**. k = 15; M > X^{0.9} forces M ≥ 251,189, but π(10^6) = 78,498, so the hypothesis is **vacuous at this X** (for δ = 0.1 even π(X) < X^{1−δ} until X ≈ 3.4·10^{15}). Taking M = 251,189 hypothetically: ln C(M,k) = 158.61 ≥ ln(M/k)^k = 145.89 > ln X^{0.7k} = 145.06 ✓; (8.2): ln(1+k lnX/ln2)^{X^δ} = 22.71 vs k lnX = 207.23 (the "o(1)" = 0.110); resulting g(n) ≥ X^{0.594k} > n^{0.59} for ε = 0.41 ✓. At X = 10^{20}, 10^{40}, 10^{100} the o(1) is 2.9e−3, 2.5e−5, 4.3e−21; (8.1) strict with margin b−c > 0 in exact arithmetic. See Objection 3. |
| (j) | §2.3, p.9 | Σ_{j≥0} h(j+1)2^{−j} = 4h | **PASS** (exact rational partial sum + closed-form tail, h ∈ {1,2,6,10}). |
| (k) | (3.25), p.19 (and (3.19), p.18) | (j)_a/j! = 1/(j−a)! = (j−a+b)_b/(j−a+b)!; C(k+t,t)/(k+t)! = 1/(k!t!) | **PASS** (2,176 triples j,b ≤ 15; 400 pairs), plus the change-of-variables meaning on a toy finite measure: (1/j!)∫Σ_{ordered a-selections} φ dλ^{⊗j} = ∫φ dλ^{⊗a}dλ^{⊗(j−a)}/(j−a)! exactly (4 cases, exact rationals). |

**No identity in scope fails.** The only failure found is the one the paper itself announces (the converse in §6.5 needs (m,k) = 1), with an explicit counterexample supplied.

## Objections

1. **§6.5, p.50 — "bijection" stated without its domain.** Verbatim: *"Every prime factor of m exceeds W, whereas |k| is bounded by a fixed power of L. Hence (m, k) = 1 for sufficiently large x. Equation (6.18) implies m | 2eh + 1. … This proves a bijection, with all variables recovered by the displayed formulas. In particular, no additional divisibility condition is being dropped. The coprimality (m, k) = 1 is necessary to this converse."*
   What is true: the identities (6.16), (6.18), (6.20) are exact (47,400 forward solutions incl. k < 0, 0 failures), and on the set actually summed (m, m′ W-rough, 0 < |k| ≪ L^{K0+Cs} < W, e in the enlarged range) the forward and converse maps are mutually inverse (toy W = 13: 16,706 = 16,706, image = independent enumeration). What is imprecise: for general integers the forward map does produce non-coprime (m,k) — e.g. (e,n,m,m′,h,h′) = (1,1,3,9,1,4) gives k = 3 — and the converse genuinely fails without coprimality: (k,m,m′,h,h′,e) = (3,3,9,2,7,1) satisfies m′h = z, mh′ = z+k, m′ ≡ m (mod 2|k|), e > 0, (6.18), yet (2eh+1)/m = 5/3. So "no additional divisibility condition is being dropped" is true only because W-roughness of m and |k| < W hold on the support; the condition m | 2eh+1 (equivalently (m,k)=1 there) is part of the bijection's domain. The paper's own last sentence concedes this. **Severity: COSMETIC (exposition).** Fix: state the bijection as between solutions of (6.15) with m, m′ W-rough and data (k,z,m,m′) with m,m′ W-rough, 0 < |k| < W, m′ ≡ m (mod 2|k|), e > 0. Not used anywhere in a way that breaks.

2. **Lemma 2.9 proof, p.9 — "absolute constant" and the level exponent.** Verbatim: *"Indeed the factorial tails eventually decrease geometrically in their index, and h_j = (j + 1)h; the same sum is bounded by an absolute constant when h = 2."* R_2 = Σ_j e_j/a_j ≤ Σ_j C^{2j+3}/((2j+3)! a_*) with a_* = exp(−C/η0) depends on C and η0; it is not absolute (the lemma statement correctly says "The implied constants depend on η0, C", so this is a word slip). Verbatim: *"A correction adds at most one more unit to this upper bound. Hence the stated level z^{4h+2} is valid for all the polynomials above."* The argument gives z^{4h+1}; z^{4h+2} is merely weaker and is what all later uses quote (b1(4h+2) < ϑ in §7.2; W^{4h+2} in Lemma 7.3). **Severity: COSMETIC.** Numerically the toy level exponents (2.75, 4.26, 6.06) sit well inside both bounds; coefficients ±1 and the sandwich hold exactly.

3. **§8, p.66 — the quantitative content of "sufficiently large X".** Verbatim: *"Choose 0 < δ < 1/4 with 4δ < ε. By Theorem 1.2, for every sufficiently large X there are more than X^{1−δ} primes p ≤ X such that p − 1 is X^δ-smooth."* and *"The strict final inequality follows from 3δ + o(1) < ε and 1 − ε > 0."* The deduction (8.1)–(8.2) is correct line by line (verified in exact/high-precision arithmetic), and only 3δ < ε is used, so "4δ < ε" is a harmless over-requirement. For the record: at δ = 0.1 the hypothesis M > X^{1−δ} cannot hold for any X below ≈ 3.4·10^{15} (π(X) < X^{0.9} there; at X = 10^6, π = 78,498 < 251,189), and the o(1) in (8.2) is 0.110 at X = 10^6, 2.9·10^{−3} at 10^{20}. Nothing here is wrong; Theorem 1.1 is a pure "for infinitely many n" statement and inherits all its strength from Theorem 1.2. **Severity: COSMETIC.**

4. **(7.19) direction and the subtraction in (7.22) — checked, no objection.** (7.19) is stated as an upper bound *"D_{b1}(1) ≤ e^{−γE}/b1 (1 + O(e^{−c/b1}))"*; that is the direction (7.22) needs (the composite total, bounded above by ∫_{b1}^{1/2−κ} ≤ D_{b1}(1) − 1 plus mesh slack 1/10, is subtracted from the lower bound (7.11) of size e^{−γ}/b1·(1 − O(e^{−c/b1}))). Numerically D_{b1}(1) is *below* e^{−γ}/b1 at all three tested b1 with relative gaps 8.4·10^{−4}, 8.9·10^{−6}, 3.2·10^{−8} (ω(u) − e^{−γ} oscillates in sign, so for some b1 it is above — absorbed by the O(e^{−c/b1}) term, which is the classical |ω(u) − e^{−γ}| ≤ exp(−u log u + O(u))). One quantitative remark for whoever owns §7: after the subtraction only the "1" (the prime term) survives out of a main term ≈ 0.5615/b1, so the relative error O(e^{−c/b1}) in (7.11) — coming from Lemma 2.9 with h = 2⌊1/(40b1)⌋, i.e. e^{−h} ≈ e^{−1/(20b1)} — must beat b1 by a margin; with (0.56/b1)e^{−1/(20b1)} = 1.03 at b1 = 0.01 and 5·10^{−3} at b1 = 0.005, b1 must be genuinely tiny (times unknown Lemma 2.9 constants). The paper does choose b1 "sufficiently small" with all constants uniform in b1 (*"The constants in the exponential error are uniform for small b1 and 0 < κ < 1/50"*), so this is consistent. **Severity: none (observation).**

Hedge words in the passages of my scope (§2.3, §3.5 (3.19)–(3.25), §3.8, Lemma 4.2, §4.4, §6.5, §7.4, §8): "uniformly also when h grows" (Lemma 2.9 — verified structurally: R_h ≪ e^{−h} with constants depending on C, η0 only), "It follows that the reversed row operation retrieves…" (p.19, the meaning of (3.25) — verified on a toy measure), "For completeness, these conditional row bounds can be iterated although a pivot may have died before its dependent birth" (p.24, inside the large-rank bound (3.44) — this is a real proof step, not an identity; outside the numerics remit, flagged for the transference seat), "uniformly in θ" (p.25), "uniformly on compact sets…" and "strips … have uniformly vanishing volume" (p.59–60, (7.20); not numerically checked), "For completeness, the binomial inequality follows…" (p.66 — verified).

## Citation table (results cited inside my scope)

| cited result | what the paper says it gives | what the source says | verdict |
|---|---|---|---|
| Ford–Halberstam 2000 [8], §1 Lemma 1 (read: author PDF ford126.web.illinois.edu/wwwpapers/hooleysieve.pdf, 6 pp., saved `refs/ford_halberstam/fh.pdf`) | p.8: *"the product of block upper bounds and its one-block correction are the inequalities of Ford and Halberstam [8, Section 1, Lemma 1]"* | *"Lemma 1. Suppose that 0 ≤ x_j ≤ y_j (j = 1, …, r). Then (4) x_1 … x_r ≥ y_1 … y_r − Σ_{ℓ=1}^r (y_ℓ − x_ℓ) Π_{j≠ℓ} y_j."* applied with x_j = Σ_{d\|(a,P_j)} μ(d), y_j = the truncation ν(d) ≤ k_j (k_j even), and Brun's pure sieve *"(5) 0 ≤ y_ℓ − x_ℓ ≤ Σ_{d\|(a,P_ℓ), ν(d)=k_ℓ+1} 1"* | **MATCH** — (2.6) is exactly (4)+(5) with x_j = I_j, y_j = U_j, E_j = the degree-(h_j+1) sum. (The paper re-proves it; my check (g) confirms the polynomial statement.) |
| Buchstab 1937 [4] | p.59: *"These are Buchstab's rough-number densities in logarithmic coordinates, and the minimum-coordinate decomposition below is the corresponding Buchstab identity [4]."* | not fetched (Mat. Sbornik 1937). Standard content: uω(u) = 1 + ∫_1^{u−1}ω(v)dv, ω(u) → e^{−γ}. | **COULD NOT FETCH** — but (7.18) is re-proved in the paper and verified numerically here; with v = (1−α)/α it is literally the identity above, and D_γ(w) = ω(w/γ)/γ was confirmed to 1e−9. Not load-bearing. |
| Efron–Stein 1981 [5], §2 Decomposition Lemma | p.33: orthogonal product-space decomposition F = Σ_S F_S with F_S = Π_{i∈S}(1−E_i)Π_{i∉S}E_iF | Project Euclid returned an HTML interstitial (`refs/efron_stein/es.pdf` is HTML) | **COULD NOT FETCH** — the decomposition and the surviving-fraction claim (4.22) and its tensorization were verified directly by computation (item (c)), so the citation is not load-bearing for my items. |
| Pomerance 1980 [19], Theorem B | p.65: *"the classical connection between smooth shifted primes and large totient fibers; see [19, Theorem B and its proof]"* | Mathematika paywalled; no free copy found | **COULD NOT FETCH** — §8's argument is self-contained and verified line by line here; Theorem B is not needed. |

## Parameter-dependency table (scope)

| constant | fixed where | depends on | used where | claimed independent of / uniformity |
|---|---|---|---|---|
| h (Lemma 2.9) | statement: "every sufficiently large even integer h" | threshold depends on η0, C | (2.5); instantiated as h = 2⌊1/(40b1)⌋ (§7.2, (7.11), (7.19) proof), h = 2⌈T²⌉ (Lemma 7.3, §7.5) | implied constants "depend on η0, C, uniformly also when h grows" — consistent with the proof (R_h ≪ e^{−h}, e^{R_h} = 1+O(e^{−h})); evenness is essential (negative control h = 1 breaks U ≥ 0). |
| η0, C (2.4) | per application | — | Lemma 2.9 | for g(p) = 1/p or 1/(p−1) on odd p: η0 = 1/2, C absolute. "absolute constant when h = 2" should read "depending on η0, C" (Obj. 2). |
| level exponent 4h+2 | Lemma 2.9 | h | b1(4h+2) < ϑ (§7.2); W^{4h+2} = x^{o(1)} (Lemma 7.3) | proof gives 4h+1; 4h+2 is safe. |
| A_* | (3.39) | M = J+ℓ, \|B\| ≍ T, N, B = ⌈L²⌉ | (3.42) | A_* = L^{O(1)}, exponent independent of J for x ≥ x_0(J) — consistent. |
| r0 | (3.45) | C'' (after C_h, C, C′), N, T, log P_* = L^c | split in (3.44)/(3.47) | r0/N = O(T/L^c)+O(1/N) = o(1) — arithmetic re-done, correct. |
| m, ℓ, M = J+ℓ, θ_m | (4.23)–(4.24) | θ_m = 2ℓ^ℓm^{−ℓ} needs M ≥ (m+ℓ)(m+ℓ−1) | ‖F_full‖ ≤ θ_m^{s1/2}‖F‖ | θ_m independent of J provided J ≥ (m+ℓ)(m+ℓ−1) − ℓ; the paper imposes J ≥ J_0 after m (p.34: *"Only afterward require J ≥ m and J + ℓ ≥ (m + ℓ)(m + ℓ − 1)"*) — order consistent. |
| C (Lemma 4.2) | interval lengths ≤ CU, CV | — | (4.5), (4.6) | implied constant depends on C only; numerically ≤ 1 for C = 1. |
| k (§6.5) | 0 < \|k\| ≪ L^{K0+Cs} (6.17) | K0, Cs, U/E ≍ L^{K0} | (m,k) = 1 via W = exp(√L) > L^{K0+Cs} | needs x ≥ x_0(K0, Cs); fine since K0, Cs are fixed before x → ∞. |
| b1, κ | §7.2: κ < 1/50 fixed, then b1 small | — | (7.18) (exact, any b1 ≤ 1/2, no κ), (7.19) (error uniform in small b1) | (7.18) is κ-independent; verified for b1 ∈ {0.3, 0.2, 0.15}. |
| δ, ε, k = ⌊X^{2δ}⌋ | §8 | δ < 1/4, 4δ < ε (only 3δ < ε needed) | (8.1)–(8.2) | X ≥ X_0(δ, ε, rate of the o(1) in Theorem 1.2). |

## What I verified line by line vs what I only skimmed

Verified line by line (algebra by hand + computation):
- Lemma 2.9 proof (p.9): U_j = (−1)^{h_j}C(t−1,h_j) for t ≥ 1 (≥ 0 because h_j even); U_j − I_j ≤ E_j (C(t−1,h) ≤ C(t,h+1)); the telescoping inequality; disjointness of supports ⇒ |coefficients| ≤ 1; the level sum = 4h (+1); e_j ≤ C^{h_j+1}/(h_j+1)!; a_j ≤ EU_j ≤ a_j + e_j; the independence step. Computation (g).
- (3.19), (3.25) and their combinatorial meaning (k).
- (3.40)–(3.41) via partition-lattice Möbius inversion and the cycle/sign argument quoted on p.23 (a).
- (3.42) incl. "at most 2r addresses" and the e_r ≤ p_1^r/r! bound (b); the arithmetic after (3.45) and (3.47) (r0/N = o(1); Σ_{r≥r0} geometric; Σ_{r<r0} gives L^{(−G+Cv+o(1))N}).
- (4.22), (4.23), (4.24) incl. the tensorization over groups and the choice "−(c0/6)log θ_m > E_id + 3" with s1 ≥ c0T/3 (c).
- (4.26) (d).
- Lemma 4.2 proof: Cauchy–Schwarz, geometric sums, the block separation ‖α(h−h′)‖ ≥ 1/(2r) for |h−h′| ≤ r/2 and |β| ≤ r^{−2}, the count per block, the r = 1 case; (4.6) from (4.4)+(4.5) (h).
- (6.15)–(6.20) both directions, signs of k, positivity of e and n, (m,k) = 1 from W-roughness (e).
- (7.15) ↔ Buchstab ω; (7.18) proof on p.60 (minimum-coordinate selection, l/l! = 1/(l−1)!); (7.19) proof via the lower density + Lemma 2.9 upper bound (b1(4h+2) ≤ 1/5 + 2b1 < 1) (f).
- §8 in full: (8.1), (8.2), the pigeonhole, "unbounded" via Lemma 8.1 (i).

Only skimmed (not part of the numerics remit; owned by other seats): how (3.41)/(3.42) are inserted into the truncated memory identity and the large-rank bound (3.44) (incl. the "For completeness … iterated" step); Theorem 3.5/3.8 themselves; the use of Lemma 4.2 inside Theorem 4.3 and the comparison-kernel construction (4.7)–(4.20); the smooth separation §6.6 after (6.20); (7.16), (7.17), (7.20)–(7.22) beyond the direction check; Theorem 5.1, Theorem 6.1, Lemma 5.2–5.4.

## Verdict for scope

**HOLDS AS READ.** Every exact identity and small-case claim in items (a)–(k) checks out, with negative controls showing the checks can fail. The one failure found (converse of §6.5 without (m,k) = 1; explicit counterexample (k,m,m′,h,h′,e) = (3,3,9,2,7,1)) is the failure the paper itself declares and is excluded on the support by W-roughness. Three cosmetic slips (Objections 1–3). This seat's result is necessary-but-weak evidence: these finite identities are the parts of the paper most likely to be right; the load-bearing risk (Theorem 5.1, the transference across N ≍ L^{0.52} edges, the parameter order) is untouched by anything here.

---

# Appendix — scripts and outputs (verbatim)

## (a) distinctness inclusion–exclusion (3.40)–(3.41) — PASS

Script `/tmp/oaimath/011/numerics/a_distinct_ie.py` (run: `nice -n 19 python3 a_distinct_ie.py`, OMP/OPENBLAS threads = 1):

```python
# (a) Distinctness inclusion-exclusion (3.40)-(3.41):
#   1_{distinct performed values} = sum_pi mu(pi) 1_{C_pi},
#   pi = collection of disjoint blocks (size>=2) of POTENTIAL addresses (incl. empty collection),
#   C_pi = all addresses in the blocks performed AND values equal within each block,
#   mu(pi) = prod_B (-1)^{|B|-1} (|B|-1)!.
import itertools, random, math

def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i+1:]
        yield [[first]] + p

def collections(n):
    # collections of disjoint blocks of size>=2 on addresses 0..n-1 == set partitions, keep blocks of size>=2
    seen = set()
    for p in set_partitions(list(range(n))):
        c = tuple(sorted(tuple(sorted(b)) for b in p if len(b) >= 2))
        if c not in seen:
            seen.add(c)
            yield c

def mu(c):
    return math.prod((-1)**(len(b)-1) * math.factorial(len(b)-1) for b in c)

def rhs(values, performed, colls):
    s = 0
    for c in colls:
        ok = all(all(performed[a] for a in b) and len({values[a] for a in b}) == 1 for b in c)
        if ok:
            s += mu(c)
    return s

def lhs(values, performed):
    pv = [values[a] for a in range(len(values)) if performed[a]]
    return 1 if len(pv) == len(set(pv)) else 0

random.seed(1)
primes = [2, 3, 5, 7]
total = fails = 0
for n in range(0, 7):
    colls = list(collections(n))
    # exhaustive over values in a small prime alphabet and performed patterns for n<=5; random for n=6
    if n <= 5:
        cases = ((v, p) for v in itertools.product(primes[:3], repeat=n)
                         for p in itertools.product([0, 1], repeat=n))
    else:
        cases = ((tuple(random.choice(primes) for _ in range(n)),
                  tuple(random.choice([0, 1, 1]) for _ in range(n))) for _ in range(3000))
    for v, p in cases:
        total += 1
        if lhs(v, p) != rhs(v, p, colls):
            fails += 1
            if fails <= 5:
                print("FAIL", n, v, p, lhs(v, p), rhs(v, p, colls))
    print(f"n={n}: #collections={len(colls)}  cumulative cases={total}  fails={fails}")
# explicit toy instances with repeated values
for v, p in [((3, 3, 5, 3, 7), (1, 1, 1, 1, 1)), ((3, 3, 5, 3, 7), (1, 0, 1, 0, 1)),
             ((2, 2, 2, 2, 2, 2), (1, 1, 1, 1, 1, 1)), ((2, 3, 5, 7, 11, 13), (1, 1, 1, 1, 1, 1))]:
    print("instance", v, "performed", p, "LHS", lhs(v, p), "RHS", rhs(v, p, list(collections(len(v)))))
print("TOTAL cases", total, "FAILS", fails)
```

Output:

```
n=0: #collections=1  cumulative cases=1  fails=0
n=1: #collections=1  cumulative cases=7  fails=0
n=2: #collections=2  cumulative cases=43  fails=0
n=3: #collections=5  cumulative cases=259  fails=0
n=4: #collections=15  cumulative cases=1555  fails=0
n=5: #collections=52  cumulative cases=9331  fails=0
n=6: #collections=203  cumulative cases=12331  fails=0
instance (3, 3, 5, 3, 7) performed (1, 1, 1, 1, 1) LHS 0 RHS 0
instance (3, 3, 5, 3, 7) performed (1, 0, 1, 0, 1) LHS 1 RHS 1
instance (2, 2, 2, 2, 2, 2) performed (1, 1, 1, 1, 1, 1) LHS 0 RHS 0
instance (2, 3, 5, 7, 11, 13) performed (1, 1, 1, 1, 1, 1) LHS 1 RHS 1
TOTAL cases 12331 FAILS 0
```

Script `/tmp/oaimath/011/numerics/a_negctrl.py` (run: `nice -n 19 python3 a_negctrl.py`, OMP/OPENBLAS threads = 1):

```python
# Negative control for (a): replace mu by prod (-1)^{|B|-1} (drop the (|B|-1)! factor); checker must FAIL.
import math, itertools, importlib.util, sys
spec = importlib.util.spec_from_file_location("a", "a_distinct_ie.py")
src = open("a_distinct_ie.py").read().split("random.seed(1)")[0]
ns = {}; exec(src, ns)
ns['mu'] = lambda c: math.prod((-1)**(len(b)-1) for b in c)
fails = 0; tot = 0
for n in range(0, 6):
    colls = list(ns['collections'](n))
    for v in itertools.product([2, 3, 5], repeat=n):
        p = (1,)*n; tot += 1
        if ns['lhs'](v, p) != ns['rhs'](v, p, colls): fails += 1
print("mutated mu: cases", tot, "fails", fails)
```

Output:

```
mutated mu: cases 364 fails 123
```

## (b) cycle-generating bound (3.42), A ≤ 8 — PASS

Script `/tmp/oaimath/011/numerics/b_cycle_bound.py` (run: `nice -n 19 python3 b_cycle_bound.py`, OMP/OPENBLAS threads = 1):

```python
# (b) (3.42): sum_{r(pi)=r} |mu(pi)| = [t^r] prod_{j=0}^{A-1}(1+jt) <= (sum_j j)^r / r! <= A^{2r}, A <= 8.
import math
from collections import defaultdict

def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i+1:]
        yield [[first]] + p

def poly_coeffs(A):
    c = [1]
    for j in range(A):
        new = [0]*(len(c)+1)
        for i, a in enumerate(c):
            new[i] += a
            new[i+1] += a*j
        c = new
    return c

allok = True
for A in range(1, 9):
    tot = defaultdict(int)
    maxaddr = 0
    for p in set_partitions(list(range(A))):   # set partitions <-> collections of blocks of size>=2
        blocks = [b for b in p if len(b) >= 2]
        r = sum(len(b) - 1 for b in blocks)
        tot[r] += math.prod(math.factorial(len(b) - 1) for b in blocks)   # |mu(pi)|
        if blocks:
            maxaddr = max(maxaddr, sum(len(b) for b in blocks) / r)
    c = poly_coeffs(A)
    S = A*(A-1)//2
    for r in range(len(c)):
        eq = (tot.get(r, 0) == c[r])
        b1 = c[r] <= S**r / math.factorial(r) + 1e-9
        b2 = S**r / math.factorial(r) <= A**(2*r)
        allok &= eq and b1 and b2
    print(f"A={A}: coeffs={c}  enum={[tot.get(r,0) for r in range(len(c))]}  "
          f"eq={all(tot.get(r,0)==c[r] for r in range(len(c)))}  "
          f"max (addresses/rank)={maxaddr:.3f} (<=2 claimed)  "
          f"max_(r>=1) c_r/A^(2r)={max([c[r]/A**(2*r) for r in range(1,len(c))]+[0]):.3e}")
print("ALL OK:", allok)
```

Output:

```
A=1: coeffs=[1, 0]  enum=[1, 0]  eq=True  max (addresses/rank)=0.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=0.000e+00
A=2: coeffs=[1, 1, 0]  enum=[1, 1, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=2.500e-01
A=3: coeffs=[1, 3, 2, 0]  enum=[1, 3, 2, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=3.333e-01
A=4: coeffs=[1, 6, 11, 6, 0]  enum=[1, 6, 11, 6, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=3.750e-01
A=5: coeffs=[1, 10, 35, 50, 24, 0]  enum=[1, 10, 35, 50, 24, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=4.000e-01
A=6: coeffs=[1, 15, 85, 225, 274, 120, 0]  enum=[1, 15, 85, 225, 274, 120, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=4.167e-01
A=7: coeffs=[1, 21, 175, 735, 1624, 1764, 720, 0]  enum=[1, 21, 175, 735, 1624, 1764, 720, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=4.286e-01
A=8: coeffs=[1, 28, 322, 1960, 6769, 13132, 13068, 5040, 0]  enum=[1, 28, 322, 1960, 6769, 13132, 13068, 5040, 0]  eq=True  max (addresses/rank)=2.000 (<=2 claimed)  max_(r>=1) c_r/A^(2r)=4.375e-01
ALL OK: True
```

## (c) Efron–Stein fraction (4.22), bound (4.23), tensorization (4.24) — PASS

Script `/tmp/oaimath/011/numerics/c_efron_stein.py` (run: `nice -n 19 python3 c_efron_stein.py`, OMP/OPENBLAS threads = 1):

```python
# (c) (4.22): C(M-m-l, j-m)/C(M, j) == (j)_m (M-j)_l / (M)_{m+l}   (exact rationals)
#     (4.23): if M >= (m+l)(m+l-1): (4.22) <= 2 (j/M)^m (1-j/M)^l <= 2 (m/(m+l))^m (l/(m+l))^l <= 2 l^l m^-l = theta_m
# plus a direct Efron-Stein check: for a random SYMMETRIC f on M iid (non-uniform) coordinates,
#     ||F_full||^2 == sum_j frac(M,m,l,j) * W_j,  W_j = sum_{|S|=j} ||f_S||^2,
# where F' = average of f over the last l coords, F_full = prod_{probes i}(1-E_i) F'.
from fractions import Fraction as Fr
from math import comb
import numpy as np, itertools

def ff(x, k):
    r = 1
    for i in range(k): r *= (x - i)
    return r

def frac(M, m, l, j):
    lhs = Fr(comb(M-m-l, j-m), comb(M, j)) if (0 <= j-m <= M-m-l) else Fr(0)
    rhs = Fr(ff(j, m) * ff(M-j, l), ff(M, m+l))
    return lhs, rhs

bad_id = bad_bd = 0; ncase = 0; worst = 0.0
for m in range(1, 7):
    for l in range(1, 5):
        for M in range(m+l, 60):
            for j in range(0, M+1):
                lhs, rhs = frac(M, m, l, j)
                ncase += 1
                if lhs != rhs:
                    bad_id += 1; print("IDENTITY FAIL", M, m, l, j, lhs, rhs)
                if M >= (m+l)*(m+l-1):
                    x = j/M
                    a = float(lhs); b = 2*x**m*(1-x)**l
                    c = 2*(m/(m+l))**m*(l/(m+l))**l; d = 2*l**l*m**(-l)
                    if not (a <= b + 1e-15 and b <= c + 1e-15 and c <= d + 1e-15):
                        bad_bd += 1; print("BOUND FAIL", M, m, l, j, a, b, c, d)
                    if d > 0: worst = max(worst, a/d)
print(f"(4.22) identity: {ncase} cases, {bad_id} failures")
print(f"(4.23) chain on M>=(m+l)(m+l-1): {bad_bd} failures; max frac/theta_m = {worst:.4f}")
for (M, m, l) in [(12, 3, 1), (20, 4, 1), (12, 2, 2), (30, 5, 1), (56, 6, 2)]:
    mx = max(float(frac(M, m, l, j)[0]) for j in range(M+1))
    print(f"  M={M} m={m} l={l}: max_j frac={mx:.5f}, theta_m={2*l**l*m**(-l):.5f}, M>=(m+l)(m+l-1): {M >= (m+l)*(m+l-1)}")

# ---- direct Efron-Stein check ----
rng = np.random.default_rng(7)
def es_check(M, m, l, q, K=3):
    # alphabet {0..K-1} with law q; f symmetric = function of the multiset (count vector)
    shape = (K,)*M
    states = list(itertools.product(range(K), repeat=M))
    cache = {}
    f = np.empty(len(states))
    for i, s in enumerate(states):
        key = tuple(sorted(s))
        if key not in cache: cache[key] = rng.normal()
        f[i] = cache[key]
    f = f.reshape(shape)
    w = np.ones(shape)
    for ax in range(M):
        sh = [1]*M; sh[ax] = K
        w = w * q.reshape(sh)
    def E(g, ax):   # average over coordinate ax, broadcast back
        sh = [1]*M; sh[ax] = K
        return np.broadcast_to((g * q.reshape(sh)).sum(axis=ax, keepdims=True), shape).copy()
    def norm2(g): return float((w * g * g).sum())
    # F' : average last l coordinates; probes = first m coordinates
    Fp = f.copy()
    for ax in range(M-l, M): Fp = E(Fp, ax)
    Ff = Fp.copy()
    for ax in range(m): Ff = Ff - E(Ff, ax)
    lhs = norm2(Ff)
    # W_j via <f, T_rho f> = sum_j rho^j W_j, T_rho = prod_i (rho I + (1-rho) E_i)
    rhos = np.linspace(0.05, 1.0, M+1)
    vals = []
    for r in rhos:
        g = f.copy()
        for ax in range(M): g = r*g + (1-r)*E(g, ax)
        vals.append(float((w * f * g).sum()))
    V = np.vander(rhos, M+1, increasing=True)
    W = np.linalg.solve(V, np.array(vals))
    rhs = sum(float(frac(M, m, l, j)[0]) * W[j] for j in range(M+1))
    th = 2*l**l*m**(-l)
    return lhs, rhs, norm2(f), th, W

for (M, m, l, K) in [(5, 1, 1, 3), (6, 2, 1, 3), (7, 2, 2, 2), (12, 3, 1, 2), (12, 2, 2, 2)]:
    q = rng.dirichlet(np.ones(K))
    lhs, rhs, n2, th, W = es_check(M, m, l, q, K)
    cond = M >= (m+l)*(m+l-1)
    print(f"ES M={M} m={m} l={l} K={K}: ||F_full||^2={lhs:.10f}  sum_j frac*W_j={rhs:.10f}  "
          f"rel.err={abs(lhs-rhs)/max(abs(lhs),1e-300):.1e}  ||f||^2={n2:.6f}  "
          f"theta_m*||f||^2={th*n2:.6f} (cond M>=(m+l)(m+l-1): {cond})  ok={lhs <= th*n2 + 1e-12 or not cond}")
```

Output:

```
(4.22) identity: 43366 cases, 0 failures
(4.23) chain on M>=(m+l)(m+l-1): 0 failures; max frac/theta_m = 0.2500
  M=12 m=3 l=1: max_j frac=0.12727, theta_m=0.66667, M>=(m+l)(m+l-1): True
  M=20 m=4 l=1: max_j frac=0.09391, theta_m=0.50000, M>=(m+l)(m+l-1): True
  M=12 m=2 l=2: max_j frac=0.07576, theta_m=2.00000, M>=(m+l)(m+l-1): True
  M=30 m=5 l=1: max_j frac=0.07457, theta_m=0.40000, M>=(m+l)(m+l-1): True
  M=56 m=6 l=2: max_j frac=0.01200, theta_m=0.22222, M>=(m+l)(m+l-1): True
ES M=5 m=1 l=1 K=3: ||F_full||^2=0.1427067987  sum_j frac*W_j=0.1427067987  rel.err=7.8e-16  ||f||^2=0.736907  theta_m*||f||^2=1.473814 (cond M>=(m+l)(m+l-1): True)  ok=True
ES M=6 m=2 l=1 K=3: ||F_full||^2=0.1472245692  sum_j frac*W_j=0.1472245692  rel.err=2.7e-14  ||f||^2=1.382145  theta_m*||f||^2=1.382145 (cond M>=(m+l)(m+l-1): True)  ok=True
ES M=7 m=2 l=2 K=2: ||F_full||^2=0.0063378984  sum_j frac*W_j=0.0063378984  rel.err=8.5e-14  ||f||^2=0.426474  theta_m*||f||^2=0.852949 (cond M>=(m+l)(m+l-1): False)  ok=True
ES M=12 m=3 l=1 K=2: ||F_full||^2=0.0002059065  sum_j frac*W_j=0.0002059064  rel.err=3.0e-08  ||f||^2=1.391426  theta_m*||f||^2=0.927617 (cond M>=(m+l)(m+l-1): True)  ok=True
ES M=12 m=2 l=2 K=2: ||F_full||^2=0.0072224711  sum_j frac*W_j=0.0072224711  rel.err=3.2e-11  ||f||^2=0.427603  theta_m*||f||^2=0.855206 (cond M>=(m+l)(m+l-1): True)  ok=True
```

Script `/tmp/oaimath/011/numerics/c2_tensorization.py` (run: `nice -n 19 python3 c2_tensorization.py`, OMP/OPENBLAS threads = 1):

```python
# (c, addendum) Tensorization claim before (4.24): for a vector on TWO groups (M coords each, iid labels,
# symmetric WITHIN each group but NOT a product across groups),
#   ||F_full||^2 = sum_{j1,j2} frac(M,m,l,j1) frac(M,m,l,j2) W_{j1,j2},  W_{j1,j2} = sum_{|S1|=j1,|S2|=j2} ||f_{S1 u S2}||^2,
# where F' averages the last l coords of each group and F_full = prod over the 2m probes of (1-E_i) F'.
import numpy as np, itertools
from math import comb
def ff(x, k):
    r = 1
    for i in range(k): r *= (x - i)
    return r
def frac(M, m, l, j): return ff(j, m)*ff(M-j, l)/ff(M, m+l)
rng = np.random.default_rng(11)
def run(M, m, l, K):
    G = 2; n = G*M; shape = (K,)*n
    q = rng.dirichlet(np.ones(K))
    cache = {}; f = np.empty(K**n)
    for i, s in enumerate(itertools.product(range(K), repeat=n)):
        key = (tuple(sorted(s[:M])), tuple(sorted(s[M:])))
        if key not in cache: cache[key] = rng.normal()
        f[i] = cache[key]
    f = f.reshape(shape)
    w = np.ones(shape)
    for ax in range(n):
        sh = [1]*n; sh[ax] = K; w = w*q.reshape(sh)
    def E(g, ax):
        sh = [1]*n; sh[ax] = K
        return np.broadcast_to((g*q.reshape(sh)).sum(axis=ax, keepdims=True), shape).copy()
    Fp = f.copy()
    for g0 in range(G):
        for ax in range(g0*M + M - l, g0*M + M): Fp = E(Fp, ax)
    Ff = Fp.copy()
    for g0 in range(G):
        for ax in range(g0*M, g0*M + m): Ff = Ff - E(Ff, ax)
    lhs = float((w*Ff*Ff).sum())
    rhos = np.linspace(0.1, 1.0, M+1)
    rows, vals = [], []
    for r1 in rhos:
        for r2 in rhos:
            g = f.copy()
            for ax in range(n):
                r = r1 if ax < M else r2
                g = r*g + (1-r)*E(g, ax)
            vals.append(float((w*f*g).sum()))
            rows.append([r1**a * r2**b for a in range(M+1) for b in range(M+1)])
    Wv = np.linalg.solve(np.array(rows), np.array(vals)).reshape(M+1, M+1)
    rhs = sum(frac(M, m, l, a)*frac(M, m, l, b)*Wv[a, b] for a in range(M+1) for b in range(M+1))
    bad = sum((comb(M-m, a-m)/comb(M, a) if a >= m else 0)*(comb(M-m, b-m)/comb(M, b) if b >= m else 0)*Wv[a, b]
              for a in range(M+1) for b in range(M+1))      # negative control: ignores the averaged last-l slots
    print(f"2 groups, M={M} m={m} l={l} K={K}: ||F_full||^2={lhs:.12f}  product-of-fractions prediction={rhs:.12f}  rel.err={abs(lhs-rhs)/abs(lhs):.1e}"
          f"  | neg.control (fraction without the last-l exclusion) = {bad:.12f}")
run(4, 1, 1, 3)
run(4, 2, 1, 3)
run(5, 2, 2, 2)
```

Output:

```
2 groups, M=4 m=1 l=1 K=3: ||F_full||^2=0.029934303669  product-of-fractions prediction=0.029934303669  rel.err=3.4e-13  | neg.control (fraction without the last-l exclusion) = 0.290972244561
2 groups, M=4 m=2 l=1 K=3: ||F_full||^2=0.000007919910  product-of-fractions prediction=0.000007919910  rel.err=1.3e-08  | neg.control (fraction without the last-l exclusion) = 0.000009209551
2 groups, M=5 m=2 l=2 K=2: ||F_full||^2=0.000005367375  product-of-fractions prediction=0.000005367372  rel.err=6.0e-07  | neg.control (fraction without the last-l exclusion) = 0.000006535274
```

## (d) exact cancellation (4.26) — PASS

Script `/tmp/oaimath/011/numerics/d_cancellation.py` (run: `nice -n 19 python3 d_cancellation.py`, OMP/OPENBLAS threads = 1):

```python
# (d) (4.26): sum_{0!=A<=U, 0!=B<=V} (-1)^{|A|+|B|} = 1 for nonempty U, V (and the empty cases).
import itertools
def S(u, v):
    tot = 0
    for a in range(1, 2**u):
        for b in range(1, 2**v):
            tot += (-1)**(bin(a).count("1") + bin(b).count("1"))
    return tot
res = {(u, v): S(u, v) for u in range(0, 7) for v in range(0, 7)}
print("nonempty U,V all equal 1:", all(res[(u, v)] == 1 for u in range(1, 7) for v in range(1, 7)))
print("U or V empty (no comparison survives), sums:", {k: x for k, x in res.items() if 0 in k})
print("sample:", {(u, v): res[(u, v)] for u, v in [(1, 1), (2, 3), (6, 6)]})
```

Output:

```
nonempty U,V all equal 1: True
U or V empty (no comparison survives), sums: {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 0, (0, 6): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, (4, 0): 0, (5, 0): 0, (6, 0): 0}
sample: {(1, 1): 1, (2, 3): 1, (6, 6): 1}
```

## (e) determinant parametrization (6.15)–(6.20) — PASS (converse FAILS without (m,k)=1 — explicit counterexample (k,m,m',h,h',e)=(3,3,9,2,7,1); paper declares coprimality necessary; automatic on the W-rough support)

Script `/tmp/oaimath/011/numerics/e_determinant.py` (run: `nice -n 19 python3 e_determinant.py`, OMP/OPENBLAS threads = 1):

```python
# (e) (6.15)-(6.20): forward identities, converse reconstruction, k<0, and dependence on (m,k)=1.
from math import gcd
from fractions import Fraction as Fr

# ---- forward: enumerate (e,n,m,m',h,h') with mn=2eh+1, m'n=2eh'+1, m != m'
fwd = 0; fwd_fail = 0; negk = 0; noncoprime_fwd = []
for e in range(1, 13):
    for n in range(1, 40):
        if gcd(n, 2*e) != 1: continue
        for h in range(1, 60):
            v = 2*e*h + 1
            if v % n: continue
            m = v // n
            for hp in range(1, 60):
                vp = 2*e*hp + 1
                if vp % n: continue
                mp = vp // n
                if mp == m: continue
                fwd += 1
                ok = ((mp - m) % (2*e) == 0)
                k = (mp - m) // (2*e)
                z = mp * h
                ok &= (k != 0) and (hp - h == k*n) and (m*hp == z + k)
                ok &= (mp % (2*abs(k)) == m % (2*abs(k)))           # congruence m' = m mod 2|k|
                ok &= (Fr(mp - m, 2*k) == e) and e > 0               # (6.20) e
                ok &= (Fr((mp - m)*z, k*m*mp) + Fr(1, m) == n)       # (6.20) n
                if k < 0: negk += 1
                if gcd(m, k) > 1 and len(noncoprime_fwd) < 3: noncoprime_fwd.append((e, n, m, mp, h, hp, k))
                if not ok:
                    fwd_fail += 1; print("FWD FAIL", e, n, m, mp, h, hp)
print(f"forward: {fwd} solutions of (6.15) (incl. {negk} with k<0); identity failures: {fwd_fail}")
print("forward solutions with gcd(m,k)>1 (forward map does NOT force coprimality in general):", noncoprime_fwd)

# ---- converse: fix k != 0, positive m,m',h,h' with m'h = z, m h' = z+k, m' = m mod 2|k|, e=(m'-m)/(2k)>0
conv = conv_ok = 0; fails_cop = []; fails_noncop = []; noncop_ok = 0
for k in list(range(-12, 0)) + list(range(1, 13)):
    for m in range(1, 50):
        for mp in range(1, 120):
            if mp == m or (mp - m) % (2*abs(k)): continue
            e = Fr(mp - m, 2*k)
            if e <= 0: continue
            e = int(e)
            for h in range(1, 40):
                z = mp*h
                if (z + k) % m or z + k <= 0: continue
                hp = (z + k)//m
                conv += 1
                lhs6_18 = m*(hp - h) == k*(2*e*h + 1)
                assert lhs6_18
                recon = ((2*e*h + 1) % m == 0)
                if recon:
                    n = (2*e*h + 1)//m
                    recon = (hp - h == k*n) and (mp*n == 2*e*hp + 1) and (m*n == 2*e*h + 1)
                if gcd(m, k) == 1:
                    if recon: conv_ok += 1
                    else: fails_cop.append((k, m, mp, h, hp, e))
                else:
                    if recon: noncop_ok += 1
                    else: fails_noncop.append((k, m, mp, h, hp, e, z))
print(f"converse: {conv} tuples; coprime (m,k)=1 reconstruct OK: {conv_ok}; coprime failures: {len(fails_cop)}")
print(f"  non-coprime: reconstruct OK {noncop_ok}, FAIL {len(fails_noncop)}")
print("  first non-coprime failures (k,m,m',h,h',e,z):", fails_noncop[:4])
k, m, mp, h, hp, e, z = 3, 3, 9, 2, 7, 1, 18
print(f"  explicit: k={k} m={m} m'={mp} h={h} h'={hp} e={e}: m'h={mp*h}=z, mh'={m*hp}=z+k, "
      f"m'-m={mp-m} = 2ek={2*e*k}, (6.18) m(h'-h)={m*(hp-h)} = k(2eh+1)={k*(2*e*h+1)}, "
      f"but n=(2eh+1)/m={Fr(2*e*h+1, m)} is not an integer")
```

Output:

```
forward: 47400 solutions of (6.15) (incl. 23700 with k<0); identity failures: 0
forward solutions with gcd(m,k)>1 (forward map does NOT force coprimality in general): [(1, 1, 3, 9, 1, 4, 3), (1, 1, 3, 15, 1, 7, 6), (1, 1, 3, 21, 1, 10, 9)]
converse: 27723 tuples; coprime (m,k)=1 reconstruct OK: 14819; coprime failures: 0
  non-coprime: reconstruct OK 940, FAIL 11964
  first non-coprime failures (k,m,m',h,h',e,z): [(-12, 26, 2, 19, 1, 1, 38), (-12, 26, 2, 32, 2, 1, 64), (-12, 27, 3, 22, 2, 1, 66), (-12, 27, 3, 31, 3, 1, 93)]
  explicit: k=3 m=3 m'=9 h=2 h'=7 e=1: m'h=18=z, mh'=21=z+k, m'-m=6 = 2ek=6, (6.18) m(h'-h)=15 = k(2eh+1)=15, but n=(2eh+1)/m=5/3 is not an integer
```

Script `/tmp/oaimath/011/numerics/e2_rough_bijection.py` (run: `nice -n 19 python3 e2_rough_bijection.py`, OMP/OPENBLAS threads = 1):

```python
# (e, addendum) The paper's setting: m, m' "W-rough" with |k| < W. Toy analogue: W = 13, all prime factors of
# m, m' exceed W, 0 < |k| <= 12. Check that forward images satisfy the converse hypotheses (incl. (m,k)=1)
# and that forward and converse maps are mutually inverse on these sets (a genuine bijection).
from math import gcd
from fractions import Fraction as Fr
W = 13; EMAX, NMAX, HMAX, MMAX = 15, 60, 150, 2*15*150 + 2
lpf = list(range(MMAX + 1))                      # least prime factor sieve
for p in range(2, int(MMAX**0.5) + 1):
    if lpf[p] == p:
        for q in range(p*p, MMAX + 1, p):
            if lpf[q] == q: lpf[q] = p
rough = lambda x: x == 1 or lpf[x] > W
F = set()
for e in range(1, EMAX):
    for n in range(1, NMAX):
        if gcd(n, 2*e) != 1: continue
        hs = [h for h in range(1, HMAX) if (2*e*h + 1) % n == 0 and rough((2*e*h + 1)//n)]
        for h in hs:
            m = (2*e*h + 1)//n
            for hp in hs:
                mp = (2*e*hp + 1)//n
                if mp == m: continue
                k = (mp - m)//(2*e)
                if 0 < abs(k) <= 12: F.add((e, n, m, mp, h, hp))
C = set()
for (e, n, m, mp, h, hp) in F:
    k = (mp - m)//(2*e); z = mp*h
    assert gcd(m, k) == 1 and m*hp == z + k and (mp - m) % (2*abs(k)) == 0 and Fr(mp - m, 2*k) == e > 0
    C.add((k, m, mp, h, hp))
C2 = set(); back = set(); fails = 0
roughs = [x for x in range(1, MMAX) if rough(x)]
for k in [x for x in range(-12, 13) if x]:
    for m in roughs:
        for mp in roughs:
            if mp == m or (mp - m) % (2*abs(k)) or Fr(mp - m, 2*k) <= 0: continue
            e = (mp - m)//(2*k)
            if e >= EMAX: continue
            for h in range(1, HMAX):
                if (mp*h + k) % m: continue
                hp = (mp*h + k)//m
                if not (1 <= hp < HMAX): continue
                if (2*e*h + 1) % m: fails += 1; continue
                n = (2*e*h + 1)//m
                if n >= NMAX: continue
                C2.add((k, m, mp, h, hp)); back.add((e, n, m, mp, h, hp))
print(f"toy W={W}: forward set |F|={len(F)}, image |C|={len(C)}; independently enumerated converse set |C2|={len(C2)}; converse failures={fails}")
print(f"image == converse set: {C == C2};  converse map lands back on F exactly: {back == F}")
```

Output:

```
toy W=13: forward set |F|=16706, image |C|=16706; independently enumerated converse set |C2|=16706; converse failures=0
image == converse set: True;  converse map lands back on F exactly: True
```

## (f) Buchstab identity (7.18) and (7.19) — PASS

Script `/tmp/oaimath/011/numerics/f_buchstab.py` (run: `nice -n 19 python3 f_buchstab.py`, OMP/OPENBLAS threads = 1):

```python
# (f) Buchstab identity (7.18) and (7.19), with D_gamma(w) computed FROM THE SIMPLEX DEFINITION (7.15):
#   D_g(w) = 1/w + sum_{l>=2} (1/l!) int_{t_i>=g (i<l), sum_{i<l} t_i <= w-g} 1/(w - sum t_i) prod dt_i/t_i.
# The l-th term is G_l(w)/l!, G_l = l-fold convolution density of dt/t on [g,inf) (Fubini on the last
# coordinate -- NOT the minimum-coordinate decomposition that (7.18) asserts). Scaling t_i = w s_i gives
# G_l^{(g)}(w) = G_l^{(g/w)}(1)/w, so with g_l(b) := G_l^{(b)}(1):
#   g_1 = 1,  g_l(b) = int_b^{1-(l-1)b} g_{l-1}(b/(1-t)) dt/(t(1-t))  (b <= 1/l, else 0).
import numpy as np
from math import factorial, log, exp
from scipy.integrate import quad, nquad
from numpy.polynomial import chebyshev as C

BMIN = 0.149
LMAX = 7
EULER = 0.57721566490153286
cheb = {}
def g(l, b):
    if l == 1: return 1.0 if b <= 1.0 else 0.0
    if b >= 1.0/l: return 0.0
    if l == 2: return 2*log((1-b)/b)
    lo, hi, coef = cheb[l]
    x = (2*b - lo - hi)/(hi - lo)
    return float(C.chebval(x, coef))
def g_direct(l, b):
    if b >= 1.0/l: return 0.0
    f = lambda t: g(l-1, b/(1-t))/(t*(1-t))
    return quad(f, b, 1-(l-1)*b, epsabs=1e-13, epsrel=1e-12, limit=200)[0]
for l in range(3, LMAX+1):
    lo, hi = BMIN, 1.0/l
    if hi <= lo: break
    N = 48
    xs = np.cos(np.pi*(np.arange(N)+0.5)/N)
    bs = lo + (xs+1)*(hi-lo)/2
    vals = np.array([g_direct(l, b) for b in bs])
    cheb[l] = (lo, hi, C.chebfit(xs, vals, N-1))
    # interpolation self-check at off-node points
    tb = np.linspace(lo+1e-3, hi-1e-3, 5)
    err = max(abs(g(l, b) - g_direct(l, b)) for b in tb)
    print(f"g_{l} tabulated on [{lo:.3f},{hi:.4f}], interpolation check max|err|={err:.1e}")

def D1(b):          # D_b(1)
    return sum(g(l, b)/factorial(l) for l in range(1, int(1/b)+1))
def D(gam, w):      # D_gam(w) = D_{gam/w}(1)/w
    return D1(gam/w)/w

# Independent check of D_b(1) by direct nested quadrature of (7.15) at b1 = 0.3 (l <= 3):
b = 0.3
t2 = quad(lambda t: 1/(t*(1-t)), b, 1-b)[0]/2
t3 = nquad(lambda t1, t2_: 1/(t1*t2_*(1-t1-t2_)), [lambda t2_: [b, 1-b-t2_], [b, 1-2*b]])[0]/6
print(f"direct nested quad D_0.3(1) = 1 + {t2:.12f} + {t3:.12f} = {1+t2+t3:.12f};  via recursion: {D1(0.3):.12f}")

# Buchstab omega by its delay-differential equation (u w(u))' = w(u-1), w = 1/u on [1,2] (independent method)
def omega_table(umax, hstep=1e-4):
    us = np.arange(1.0, umax+hstep/2, hstep)
    w = np.where(us <= 2.0, 1/us, 0.0)
    uw = us*w
    n1 = int(round(1.0/hstep))
    i2 = int(round(1.0/hstep))      # index of u=2
    for i in range(i2+1, len(us)):
        # trapezoid on (u w)' = w(u-1)
        uw[i] = uw[i-1] + hstep*(w[i-1-n1] + w[i-n1])/2
        w[i] = uw[i]/us[i]
    return us, w
us, om = omega_table(7.0)
def omega(u): return float(np.interp(u, us, om))
print(f"sanity: omega(3)={omega(3):.6f} (exact (1+ln2)/3={(1+log(2))/3:.6f}), e^-gamma={exp(-EULER):.10f}")

for b1 in (0.3, 0.2, 0.15):
    rhs = D1(b1) - 1
    k_breaks = [1.0/(k+1) for k in range(1, 20) if b1 < 1.0/(k+1) < 0.5]
    lhs = quad(lambda a: D(a, 1-a)/a, b1, 0.5, points=k_breaks, epsabs=1e-12, epsrel=1e-11, limit=400)[0]
    print(f"b1={b1}: l up to {int(1/b1)};  D_b1(1)-1 = {rhs:.10f};  int_b1^1/2 D_a(1-a) da/a = {lhs:.10f};  "
          f"diff = {lhs-rhs:.2e}")
    print(f"        D_b1(1) = {D1(b1):.10f};  omega(1/b1)/b1 = {omega(1/b1)/b1:.10f};  e^-gamma/b1 = {exp(-EULER)/b1:.10f};  "
          f"D_b1(1)/(e^-gamma/b1) - 1 = {D1(b1)*b1/exp(-EULER)-1:+.3e}")

# Negative control: the identity must be sensitive -- replace the roughness level alpha of the cofactor
# by the fixed level b1 (i.e. drop the "minimum coordinate" constraint); the two sides must then disagree.
for b1 in (0.3, 0.2, 0.15):
    bad = quad(lambda a: D(b1, 1-a)/a, b1, 0.5, epsabs=1e-12, limit=400)[0]
    print(f"neg.control b1={b1}: int D_b1(1-a) da/a = {bad:.6f}  vs  D_b1(1)-1 = {D1(b1)-1:.6f}")
```

Output:

```
g_3 tabulated on [0.149,0.3333], interpolation check max|err|=2.0e-14
g_4 tabulated on [0.149,0.2500], interpolation check max|err|=1.0e-14
g_5 tabulated on [0.149,0.2000], interpolation check max|err|=1.7e-15
g_6 tabulated on [0.149,0.1667], interpolation check max|err|=1.4e-17
direct nested quad D_0.3(1) = 1 + 0.847297860387 + 0.022666152471 = 1.869964012858;  via recursion: 1.869964012858
sanity: omega(3)=0.564382 (exact (1+ln2)/3=0.564382), e^-gamma=0.5614594836
b1=0.3: l up to 3;  D_b1(1)-1 = 0.8699640129;  int_b1^1/2 D_a(1-a) da/a = 0.8699640129;  diff = 8.88e-16
        D_b1(1) = 1.8699640129;  omega(1/b1)/b1 = 1.8699640135;  e^-gamma/b1 = 1.8715316119;  D_b1(1)/(e^-gamma/b1) - 1 = -8.376e-04
b1=0.2: l up to 5;  D_b1(1)-1 = 1.8072723413;  int_b1^1/2 D_a(1-a) da/a = 1.8072723413;  diff = 4.44e-16
        D_b1(1) = 2.8072723413;  omega(1/b1)/b1 = 2.8072723421;  e^-gamma/b1 = 2.8072974178;  D_b1(1)/(e^-gamma/b1) - 1 = -8.933e-06
b1=0.15: l up to 6;  D_b1(1)-1 = 2.7430631053;  int_b1^1/2 D_a(1-a) da/a = 2.7430631053;  diff = -3.11e-15
        D_b1(1) = 3.7430631053;  omega(1/b1)/b1 = 3.7430631063;  e^-gamma/b1 = 3.7430632238;  D_b1(1)/(e^-gamma/b1) - 1 = -3.165e-08
neg.control b1=0.3: int D_b1(1-a) da/a = 0.915296  vs  D_b1(1)-1 = 0.869964
neg.control b1=0.2: int D_b1(1-a) da/a = 2.576937  vs  D_b1(1)-1 = 1.807272
neg.control b1=0.15: int D_b1(1-a) da/a = 4.506055  vs  D_b1(1)-1 = 2.743063
```

## (g) Lemma 2.9 block sieve (2.6) — PASS (negative control with odd h fails as it must)

Script `/tmp/oaimath/011/numerics/g_block_sieve.py` (run: `nice -n 19 python3 g_block_sieve.py`, OMP/OPENBLAS threads = 1):

```python
# (g) Lemma 2.9 block sieve, (2.6): blocks B_j = {p : z^(2^-j-1) < p <= z^(2^-j)}, h_j = (j+1)h,
#   U_j = sum_{S<=B_j,|S|<=h_j} (-1)^|S| x_S,  E_j = sum_{S<=B_j,|S|=h_j+1} x_S,
#   U = prod_j U_j,  V = U - sum_j E_j prod_{k!=j} U_k.
# Verify on all 0/1 assignments of the bad-condition indicators x_p: V <= 1_{no bad} <= U, U >= 0, U-V >= 0;
# all coefficients of U, V, U-V have |c| <= 1; level: every monomial d = prod_{p in S} p <= z^(4h+2),
# and the sharper log d/log z <= sum_j h_j 2^-j (+1 for a correction) <= 4h+1.
import itertools, math
import numpy as np
from sympy import primerange

def block_sieve(primes, z, h):
    blocks = {}
    for p in primes:
        j = 0
        while not (z**(2.0**(-j-1)) < p <= z**(2.0**(-j))): j += 1
        blocks.setdefault(j, []).append(p)
    def Uj(B, hj):
        return {frozenset(S): (-1)**len(S) for r in range(0, min(hj, len(B))+1) for S in itertools.combinations(B, r)}
    def Ej(B, hj):
        return {frozenset(S): 1 for S in itertools.combinations(B, hj+1)} if hj+1 <= len(B) else {}
    def mul(P, Q):
        R = {}
        for a, ca in P.items():
            for b, cb in Q.items():
                assert not (a & b)            # blocks disjoint -> multilinear
                R[a | b] = R.get(a | b, 0) + ca*cb
        return R
    js = sorted(blocks)
    Us = {j: Uj(blocks[j], (j+1)*h) for j in js}
    Es = {j: Ej(blocks[j], (j+1)*h) for j in js}
    U = {frozenset(): 1}
    for j in js: U = mul(U, Us[j])
    corr = {}
    for j in js:
        T = dict(Es[j])
        for k in js:
            if k != j: T = mul(T, Us[k])
        for s, c in T.items(): corr[s] = corr.get(s, 0) + c
    V = dict(U)
    for s, c in corr.items(): V[s] = V.get(s, 0) - c
    return blocks, U, V, corr

def evaluate(poly, primes):
    # value at every subset T of primes (bad conditions holding exactly on T) = sum_{S subset T} c_S (zeta transform)
    n = len(primes); idx = {p: i for i, p in enumerate(primes)}
    a = np.zeros(1 << n, dtype=np.int64)
    for S, c in poly.items():
        a[sum(1 << idx[p] for p in S)] += c
    for i in range(n):
        bit = 1 << i
        m = np.arange(1 << n)
        sel = (m & bit) != 0
        a[sel] += a[m[sel] ^ bit]
    return a

def run(zmax, h):
    primes = list(primerange(2, zmax+1)); z = zmax
    blocks, U, V, corr = block_sieve(primes, z, h)
    Ue, Ve = evaluate(U, primes), evaluate(V, primes)
    ind = np.zeros(1 << len(primes), dtype=np.int64); ind[0] = 1
    UmV = {s: U.get(s, 0) - V.get(s, 0) for s in set(U) | set(V)}
    lvl = lambda P: max((sum(math.log(p) for p in S)/math.log(z) for S, c in P.items() if c != 0), default=0)
    bound = sum((j+1)*h*2.0**(-j) for j in blocks)
    print(f"z={z}, h={h}: blocks={ {j: blocks[j] for j in sorted(blocks)} }, h_j={ {j:(j+1)*h for j in sorted(blocks)} }")
    print(f"  #monomials U={sum(1 for c in U.values() if c)}, V={sum(1 for c in V.values() if c)}")
    print(f"  V <= 1_nobad <= U on all {1<<len(primes)} assignments: {bool(np.all(Ve <= ind) and np.all(ind <= Ue))}")
    print(f"  U >= 0: {bool(np.all(Ue >= 0))};  U-V >= 0: {bool(np.all(Ue - Ve >= 0))};  "
          f"max|coef| U={max(abs(c) for c in U.values())}, V={max(abs(c) for c in V.values())}, U-V={max(abs(c) for c in UmV.values())}")
    print(f"  level: max log d/log z: U={lvl(U):.3f}, V={lvl(V):.3f}, U-V={lvl(UmV):.3f};  "
          f"sum_j h_j 2^-j over nonempty blocks={bound:.3f} (+1 for correction);  4h+1={4*h+1}, claimed level exponent 4h+2={4*h+2};  "
          f"max d={max(math.prod(S) for S in V if V[S]) if V else 1} <= z^(4h+2)={z**(4*h+2)}: "
          f"{max(math.prod(S) for S in V if V[S]) <= z**(4*h+2)}")
    # expected values with independent probabilities g(p)=1/p  (cf. (2.5))
    g = {p: 1.0/p for p in primes}
    EU = sum(c*math.prod(g[p] for p in S) for S, c in U.items())
    EV = sum(c*math.prod(g[p] for p in S) for S, c in V.items())
    prod = math.prod(1-g[p] for p in primes)
    print(f"  g(p)=1/p: E V={EV:.6f} <= prod(1-g)={prod:.6f} <= E U={EU:.6f}: {EV <= prod <= EU}")
    # integer sieve: objects n <= N, bad condition at p is p | n
    N = 5000
    lamU = {math.prod(S): c for S, c in U.items() if c}; lamV = {math.prod(S): c for S, c in V.items() if c}
    SU = sum(c*(N//d) for d, c in lamU.items()); SV = sum(c*(N//d) for d, c in lamV.items())
    S = sum(1 for n in range(1, N+1) if all(n % p for p in primes))
    print(f"  integers n<={N}: sum V = {SV} <= S = {S} <= sum U = {SU}: {SV <= S <= SU}")

run(7, 2)
run(50, 2)
run(50, 4)
print('--- negative control: odd h (h=1 gives h_0=1 odd), the lemma requires even h; checks must fail ---')
run(7, 1)
```

Output:

```
z=7, h=2: blocks={0: [3, 5, 7], 1: [2]}, h_j={0: 2, 1: 4}
  #monomials U=14, V=16
  V <= 1_nobad <= U on all 16 assignments: True
  U >= 0: True;  U-V >= 0: True;  max|coef| U=1, V=1, U-V=1
  level: max log d/log z: U=2.183, V=2.748, U-V=2.748;  sum_j h_j 2^-j over nonempty blocks=4.000 (+1 for correction);  4h+1=9, claimed level exponent 4h+2=10;  max d=210 <= z^(4h+2)=282475249: True
  g(p)=1/p: E V=0.228571 <= prod(1-g)=0.228571 <= E U=0.233333: True
  integers n<=5000: sum V = 1143 <= S = 1143 <= sum U = 1167: True
z=50, h=2: blocks={0: [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], 1: [3, 5, 7], 2: [2]}, h_j={0: 2, 1: 4, 2: 6}
  #monomials U=1072, V=3712
  V <= 1_nobad <= U on all 32768 assignments: True
  U >= 0: True;  U-V >= 0: True;  max|coef| U=1, V=1, U-V=1
  level: max log d/log z: U=3.312, V=4.262, U-V=4.262;  sum_j h_j 2^-j over nonempty blocks=5.500 (+1 for correction);  4h+1=9, claimed level exponent 4h+2=10;  max d=17400810 <= z^(4h+2)=97656250000000000: True
  g(p)=1/p: E V=0.138471 <= prod(1-g)=0.138704 <= E U=0.141475: True
  integers n<=5000: sum V = 679 <= S = 679 <= sum U = 688: True
z=50, h=4: blocks={0: [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], 1: [3, 5, 7], 2: [2]}, h_j={0: 4, 1: 8, 2: 12}
  #monomials U=8992, V=16384
  V <= 1_nobad <= U on all 32768 assignments: True
  U >= 0: True;  U-V >= 0: True;  max|coef| U=1, V=1, U-V=1
  level: max log d/log z: U=5.185, V=6.063, U-V=6.063;  sum_j h_j 2^-j over nonempty blocks=11.000 (+1 for correction);  4h+1=17, claimed level exponent 4h+2=18;  max d=19958729070 <= z^(4h+2)=3814697265625000000000000000000: True
  g(p)=1/p: E V=0.138704 <= prod(1-g)=0.138704 <= E U=0.138717: True
  integers n<=5000: sum V = 679 <= S = 679 <= sum U = 679: True
--- negative control: odd h (h=1 gives h_0=1 odd), the lemma requires even h; checks must fail ---
z=7, h=1: blocks={0: [3, 5, 7], 1: [2]}, h_j={0: 1, 1: 2}
  #monomials U=8, V=14
  V <= 1_nobad <= U on all 16 assignments: False
  U >= 0: False;  U-V >= 0: True;  max|coef| U=1, V=1, U-V=1
  level: max log d/log z: U=1.356, V=2.183, U-V=2.183;  sum_j h_j 2^-j over nonempty blocks=2.000 (+1 for correction);  4h+1=5, claimed level exponent 4h+2=6;  max d=70 <= z^(4h+2)=117649: True
  g(p)=1/p: E V=0.090476 <= prod(1-g)=0.228571 <= E U=0.161905: False
  integers n<=5000: sum V = 453 <= S = 1143 <= sum U = 810: False
```

## (h) Lemma 4.2 bilinear bound (4.5) — PASS (implied constant ≤ 0.996 in all instances; ≤ 0.938 for r ≥ 2)

Script `/tmp/oaimath/011/numerics/h_bilinear.py` (run: `nice -n 19 python3 h_bilinear.py`, OMP/OPENBLAS threads = 1):

```python
# (h) Lemma 4.2: |sum_{n,t} a_n b_t e(alpha n t)| <<_C ||a|| ||b|| [U + (1+V/r){U + r log(2r)}]^{1/2},
# alpha = u/r + beta, (u,r)=1, |beta| <= r^-2.  Worst case over a,b = largest singular value of the
# matrix e(alpha n t) on the two intervals.  Report ratio = sigma_max / bracket^{1/2} (the implied constant),
# plus random coefficients, plus a scan over r and beta, intervals not starting at 1.
import numpy as np
from math import gcd, log, pi
rng = np.random.default_rng(2026)

def mat(alpha, n0, U, t0, V):
    n = np.arange(n0, n0+U)[:, None]; t = np.arange(t0, t0+V)[None, :]
    return np.exp(2j*pi*alpha*n*t)
def bracket(U, V, r):
    return np.sqrt(U + (1 + V/r)*(U + r*log(2*r)))

U = V = 50; r = 7
print(f"U=V=50, r=7: bracket^(1/2) = {bracket(U, V, r):.3f}; trivial bound sqrt(UV) = {np.sqrt(U*V):.1f}")
for u in [1, 2, 3, 6]:
    for beta in [0.0, 1/r**2, -1/r**2, 0.37/r**2]:
        for (n0, t0) in [(1, 1), (1000, 37)]:
            M = mat(u/r + beta, n0, U, t0, V)
            smax = np.linalg.svd(M, compute_uv=False)[0]
            a = rng.normal(size=U) + 1j*rng.normal(size=U); b = rng.normal(size=V) + 1j*rng.normal(size=V)
            val = abs(a @ M @ b)/(np.linalg.norm(a)*np.linalg.norm(b))
            print(f"  u={u} beta={beta:+.5f} n0={n0} t0={t0}: sigma_max={smax:7.3f} ratio={smax/bracket(U,V,r):.3f};"
                  f" random a,b: |form|/(|a||b|)={val:.3f}")
# scan: worst ratio over r <= 60 (U=V=50), all u coprime to r (sampled), beta in a grid of [-r^-2, r^-2]
worst = (0, None)
for rr in range(1, 61):
    us = [u for u in range(0, rr) if gcd(u, rr) == 1][:6]
    for u in us:
        for beta in np.linspace(-1/rr**2, 1/rr**2, 7):
            for (n0, t0) in [(1, 1), (500, 900)]:
                s = np.linalg.svd(mat(u/rr + beta, n0, U, t0, V), compute_uv=False)[0]
                ratio = s/bracket(U, V, rr)
                if ratio > worst[0]: worst = (ratio, (rr, u, beta, n0, t0, s))
print(f"worst implied constant over r<=60, U=V=50: {worst[0]:.3f} at (r,u,beta,n0,t0,sigma)={worst[1]}")
# unbalanced sizes
for (U2, V2) in [(200, 20), (20, 200), (150, 150), (300, 300)]:
    w = 0
    for rr in [1, 2, 5, 7, 13, 31, 97]:
        for u in [u for u in range(rr) if gcd(u, rr) == 1][:3]:
            for beta in (0.0, 1/rr**2, -1/rr**2):
                s = np.linalg.svd(mat(u/rr + beta, 1, U2, 1, V2), compute_uv=False)[0]
                w = max(w, s/bracket(U2, V2, rr))
    print(f"U={U2} V={V2}: worst ratio over r in {{1,2,5,7,13,31,97}} = {w:.3f}")
```

Output:

```
U=V=50, r=7: bracket^(1/2) = 24.649; trivial bound sqrt(UV) = 50.0
  u=1 beta=+0.00000 n0=1 t0=1: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.578
  u=1 beta=+0.00000 n0=1000 t0=37: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.168
  u=1 beta=+0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.822
  u=1 beta=+0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.162
  u=1 beta=-0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.639
  u=1 beta=-0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.934
  u=1 beta=+0.00755 n0=1 t0=1: sigma_max= 10.798 ratio=0.438; random a,b: |form|/(|a||b|)=1.276
  u=1 beta=+0.00755 n0=1000 t0=37: sigma_max= 10.798 ratio=0.438; random a,b: |form|/(|a||b|)=1.319
  u=2 beta=+0.00000 n0=1 t0=1: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.663
  u=2 beta=+0.00000 n0=1000 t0=37: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.288
  u=2 beta=+0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.944
  u=2 beta=+0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.142
  u=2 beta=-0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.309
  u=2 beta=-0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.236
  u=2 beta=+0.00755 n0=1 t0=1: sigma_max=  8.607 ratio=0.349; random a,b: |form|/(|a||b|)=1.823
  u=2 beta=+0.00755 n0=1000 t0=37: sigma_max=  8.607 ratio=0.349; random a,b: |form|/(|a||b|)=1.383
  u=3 beta=+0.00000 n0=1 t0=1: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=1.034
  u=3 beta=+0.00000 n0=1000 t0=37: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.865
  u=3 beta=+0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.804
  u=3 beta=+0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.338
  u=3 beta=-0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.344
  u=3 beta=-0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.296
  u=3 beta=+0.00755 n0=1 t0=1: sigma_max= 10.155 ratio=0.412; random a,b: |form|/(|a||b|)=0.452
  u=3 beta=+0.00755 n0=1000 t0=37: sigma_max= 10.155 ratio=0.412; random a,b: |form|/(|a||b|)=0.731
  u=6 beta=+0.00000 n0=1 t0=1: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=0.798
  u=6 beta=+0.00000 n0=1000 t0=37: sigma_max= 20.305 ratio=0.824; random a,b: |form|/(|a||b|)=1.244
  u=6 beta=+0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.438
  u=6 beta=+0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=0.529
  u=6 beta=-0.02041 n0=1 t0=1: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.397
  u=6 beta=-0.02041 n0=1000 t0=37: sigma_max= 10.412 ratio=0.422; random a,b: |form|/(|a||b|)=1.210
  u=6 beta=+0.00755 n0=1 t0=1: sigma_max= 10.657 ratio=0.432; random a,b: |form|/(|a||b|)=0.210
  u=6 beta=+0.00755 n0=1000 t0=37: sigma_max= 10.657 ratio=0.432; random a,b: |form|/(|a||b|)=1.121
worst implied constant over r<=60, U=V=50: 0.974 at (r,u,beta,n0,t0,sigma)=(1, 0, np.float64(-1.0), 1, 1, np.float64(50.00000000000001))
U=200 V=20: worst ratio over r in {1,2,5,7,13,31,97} = 0.952
U=20 V=200: worst ratio over r in {1,2,5,7,13,31,97} = 0.978
U=150 V=150: worst ratio over r in {1,2,5,7,13,31,97} = 0.991
U=300 V=300: worst ratio over r in {1,2,5,7,13,31,97} = 0.996
```

Script `/tmp/oaimath/011/numerics/h2_bilinear_r2.py` (run: `nice -n 19 python3 h2_bilinear_r2.py`, OMP/OPENBLAS threads = 1):

```python
# (h, addendum) worst implied constant of Lemma 4.2 restricted to r >= 2 (the nontrivial branch of the proof).
import numpy as np
from math import gcd, log, pi
def mat(alpha, n0, U, t0, V):
    n = np.arange(n0, n0+U)[:, None]; t = np.arange(t0, t0+V)[None, :]
    return np.exp(2j*pi*alpha*n*t)
def bracket(U, V, r): return np.sqrt(U + (1 + V/r)*(U + r*log(2*r)))
for (U, V) in [(50, 50), (200, 20), (20, 200)]:
    worst = (0, None)
    for rr in range(2, 121):
        for u in [u for u in range(1, rr) if gcd(u, rr) == 1][:4]:
            for beta in np.linspace(-1/rr**2, 1/rr**2, 9):
                s = np.linalg.svd(mat(u/rr + beta, 1, U, 1, V), compute_uv=False)[0]
                if s/bracket(U, V, rr) > worst[0]: worst = (s/bracket(U, V, rr), (rr, u, round(float(beta), 6), round(float(s), 3)))
    print(f"U={U} V={V}: worst ratio over 2<=r<=120 = {worst[0]:.3f} at (r,u,beta,sigma_max)={worst[1]}")
```

Output:

```
U=50 V=50: worst ratio over 2<=r<=120 = 0.938 at (r,u,beta,sigma_max)=(2, 1, 0.0, 35.355)
U=200 V=20: worst ratio over 2<=r<=120 = 0.907 at (r,u,beta,sigma_max)=(2, 1, 0.0, 44.721)
U=20 V=200: worst ratio over 2<=r<=120 = 0.928 at (r,u,beta,sigma_max)=(2, 1, 0.0, 44.721)
```

## (i) (8.1)–(8.2) at X = 10^6, δ = 0.1 (+ larger X) — PASS as an asymptotic argument (hypothesis M > X^{1−δ} vacuous at X = 10^6)

Script `/tmp/oaimath/011/numerics/i_totient.py` (run: `nice -n 19 python3 i_totient.py`, OMP/OPENBLAS threads = 1):

```python
# (i) Section 8, (8.1)-(8.2) at X = 10^6, delta = 0.1 (and larger X where the hypothesis can hold).
# Paper: M = |P| > X^(1-delta) (hypothesis from Thm 1.2), k = floor(X^(2 delta)), C(M,k) >= (M/k)^k > X^((1-3delta)k)  (8.1)
#        #values <= (1 + k log X/log 2)^(X^delta) = X^(o(k))                                                     (8.2)
#        => some n <= X^k has g(n) >= X^((1-3delta-o(1))k) > n^(1-eps)  (needs 3delta+o(1) < eps; paper takes 4delta < eps)
# High-precision arithmetic (mpmath, 80 digits); M taken as the smallest integer > X^(1-delta).
import mpmath as mp
from sympy import primepi
mp.mp.dps = 80

def report(E, delta, eps):
    X = mp.mpf(10)**E; delta = mp.mpf(str(delta)); eps = mp.mpf(str(eps))
    from fractions import Fraction as Fr
    def floor10(ex):            # exact floor(10^ex) for rational ex (integer ex handled exactly)
        return 10**int(ex) if ex.denominator == 1 else int(mp.floor(mp.mpf(10)**(mp.mpf(ex.numerator)/ex.denominator)))
    dF = Fr(str(delta))
    k = floor10(E*2*dF)
    M = floor10(E*(1-dF)) + 1
    lnX = mp.log(X)
    a = mp.loggamma(M+1) - mp.loggamma(k+1) - mp.loggamma(M-k+1)
    b = k*mp.log(mp.mpf(M)/k); c = (1-3*delta)*k*lnX
    nval = (X**delta)*mp.log(1 + k*lnX/mp.log(2))
    line = f"X=10^{E} delta={mp.nstr(delta,3)} eps={mp.nstr(eps,3)}: k={k}, smallest M with M>X^(1-delta): M={M}"
    if E <= 12:
        piX = int(primepi(10**E)); line += f"; pi(X)={piX} -> hypothesis {'satisfiable' if piX >= M else 'VACUOUS at this X'}"
    print(line)
    print(f"   (8.1): ln C(M,k)={mp.nstr(a,12)} >= ln (M/k)^k={mp.nstr(b,15)} > ln X^((1-3d)k)={mp.nstr(c,15)}: {a >= b and b > c}"
          f"   [margin b-c = {mp.nstr(b-c,5)}]")
    print(f"   (8.2): ln[(1+k lnX/ln2)^(X^d)] = {mp.nstr(nval,8)};  k lnX = {mp.nstr(k*lnX,10)};  ratio (the o(1)) = {mp.nstr(nval/(k*lnX),5)}")
    e1 = (b - nval)/(k*lnX); e2 = (a - nval)/(k*lnX)
    print(f"   pigeonhole: g(n) >= X^({mp.nstr(e1,6)} k) via (M/k)^k  [X^({mp.nstr(e2,6)} k) via exact C(M,k)];"
          f"  g(n) > n^(1-eps) for n <= X^k needs exponent > {mp.nstr(1-eps,4)}: {'YES' if e1 > 1-eps else 'NOT YET (statement is asymptotic)'}")

report(6, 0.1, 0.41)
# where X/ln X can exceed X^(1-delta) at all (X^delta > ln X):
t = mp.findroot(lambda s: mp.e**(s/10) - s, 35)
print(f"delta=0.1: X^delta = ln X at ln X = {mp.nstr(t,6)}, X = {mp.nstr(mp.e**t,5)}; below this even pi(X) < X^(1-delta) asymptotically")
report(20, 0.1, 0.41)
report(40, 0.1, 0.41)
report(40, 0.05, 0.21)
report(100, 0.2, 0.81)
```

Output:

```
X=10^6 delta=0.1 eps=0.41: k=15, smallest M with M>X^(1-delta): M=251189; pi(X)=78498 -> hypothesis VACUOUS at this X
   (8.1): ln C(M,k)=158.609724438 >= ln (M/k)^k=145.888660825594 > ln X^((1-3d)k)=145.062860858625: True   [margin b-c = 0.8258]
   (8.2): ln[(1+k lnX/ln2)^(X^d)] = 22.706816;  k lnX = 207.2326584;  ratio (the o(1)) = 0.10957
   pigeonhole: g(n) >= X^(0.594413 k) via (M/k)^k  [X^(0.655799 k) via exact C(M,k)];  g(n) > n^(1-eps) for n <= X^k needs exponent > 0.59: YES
delta=0.1: X^delta = ln X at ln X = 35.7715, X = 3.4306e+15; below this even pi(X) < X^(1-delta) asymptotically
X=10^20 delta=0.1 eps=0.41: k=10000, smallest M with M>X^(1-delta): M=1000000000000000001
   (8.1): ln C(M,k)=332356.388902 >= ln (M/k)^k=322361.913019166 > ln X^((1-3d)k)=322361.913019166: True   [margin b-c = 1.0e-14]
   (8.2): ln[(1+k lnX/ln2)^(X^d)] = 1340.662;  k lnX = 460517.0186;  ratio (the o(1)) = 0.0029112
   pigeonhole: g(n) >= X^(0.697089 k) via (M/k)^k  [X^(0.718792 k) via exact C(M,k)];  g(n) > n^(1-eps) for n <= X^k needs exponent > 0.59: YES
X=10^40 delta=0.1 eps=0.41: k=100000000, smallest M with M>X^(1-delta): M=1000000000000000000000000000000000001
   (8.1): ln C(M,k)=6547238250.25 >= ln (M/k)^k=6447238260.38333 > ln X^((1-3d)k)=6447238260.38333: True   [margin b-c = 1.0e-28]
   (8.2): ln[(1+k lnX/ln2)^(X^d)] = 233101.06;  k lnX = 9210340372.0;  ratio (the o(1)) = 2.5309e-5
   pigeonhole: g(n) >= X^(0.699975 k) via (M/k)^k  [X^(0.710832 k) via exact C(M,k)];  g(n) > n^(1-eps) for n <= X^k needs exponent > 0.59: YES
X=10^40 delta=0.05 eps=0.21: k=10000, smallest M with M>X^(1-delta): M=100000000000000000000000000000000000001
   (8.1): ln C(M,k)=792873.407501 >= ln (M/k)^k=782878.931617976 > ln X^((1-3d)k)=782878.931617976: True   [margin b-c = 1.0e-34]
   (8.2): ln[(1+k lnX/ln2)^(X^d)] = 1409.9766;  k lnX = 921034.0372;  ratio (the o(1)) = 0.0015309
   pigeonhole: g(n) >= X^(0.848469 k) via (M/k)^k  [X^(0.859321 k) via exact C(M,k)];  g(n) > n^(1-eps) for n <= X^k needs exponent > 0.79: YES
X=10^100 delta=0.2 eps=0.81: k=10000000000000000000000000000000000000000, smallest M with M>X^(1-delta): M=100000000000000000000000000000000000000000000000000000000000000000000000000000001
   (8.1): ln C(M,k)=9.31034037198e+41 >= ln (M/k)^k=9.21034037197618e+41 > ln X^((1-3d)k)=9.21034037197618e+41: True   [margin b-c = 1.4694e-39]
   (8.2): ln[(1+k lnX/ln2)^(X^d)] = 9.7909119e+21;  k lnX = 2.302585093e+42;  ratio (the o(1)) = 4.2521e-21
   pigeonhole: g(n) >= X^(0.4 k) via (M/k)^k  [X^(0.404343 k) via exact C(M,k)];  g(n) > n^(1-eps) for n <= X^k needs exponent > 0.19: YES
```

## (j) Σ_{j≥0} h(j+1)2^{−j} = 4h — PASS

Script `/tmp/oaimath/011/numerics/j_level_sum.py` (run: `nice -n 19 python3 j_level_sum.py`, OMP/OPENBLAS threads = 1):

```python
# (j) Section 2.3: sum_{j>=0} h (j+1) 2^-j = 4h  (exact, as rationals: partial sums + closed-form tail)
from fractions import Fraction as Fr
for h in (1, 2, 6, 10):
    partial = sum(Fr(h*(j+1), 2**j) for j in range(0, 200))
    # exact tail sum_{j>=J}(j+1)2^-j = (J+2) 2^{1-J}
    J = 200; tail = h*Fr(J+2, 2**(J-1))
    print(f"h={h}: partial(200 terms)+tail = {partial+tail} (=4h? {partial+tail == 4*h}); float partial={float(partial):.15f}")
```

Output:

```
h=1: partial(200 terms)+tail = 4 (=4h? True); float partial=4.000000000000000
h=2: partial(200 terms)+tail = 8 (=4h? True); float partial=8.000000000000000
h=6: partial(200 terms)+tail = 24 (=4h? True); float partial=24.000000000000000
h=10: partial(200 terms)+tail = 40 (=4h? True); float partial=40.000000000000000
```

## (k) factorial identities (3.25), (3.19) — PASS

Script `/tmp/oaimath/011/numerics/k_factorial.py` (run: `nice -n 19 python3 k_factorial.py`, OMP/OPENBLAS threads = 1):

```python
# (k) (3.25): (j)_a / j! = 1/(j-a)! = (j-a+b)_b / (j-a+b)!   for 0 <= a <= j, b >= 0 (exact),
#     and (3.19): C(k+t,t)/(k+t)! = 1/(k! t!).
# Plus the combinatorial meaning on a toy finite measure: for symmetric memory measure lambda^{(x)j}/j!,
# "select a ordered old indices" integrates to lambda^{(x)a} x lambda^{(x)(j-a)}/(j-a)!.
from fractions import Fraction as Fr
from math import factorial, comb
import itertools, random
def ff(x, k):
    r = 1
    for i in range(k): r *= (x - i)
    return r
bad = 0; n = 0
for j in range(0, 16):
    for a in range(0, j+1):
        for b in range(0, 16):
            n += 1
            x = Fr(ff(j, a), factorial(j)); y = Fr(1, factorial(j-a)); z = Fr(ff(j-a+b, b), factorial(j-a+b))
            if not (x == y == z): bad += 1; print("FAIL", j, a, b)
print(f"(3.25): {n} triples (j<=15, b<=15), failures {bad}")
bad = 0
for k in range(0, 20):
    for t in range(0, 20):
        if Fr(comb(k+t, t), factorial(k+t)) != Fr(1, factorial(k)*factorial(t)): bad += 1
print(f"(3.19) selection identity: 400 pairs, failures {bad}")
# toy measure check: points {0,1,2} with weights lam; F(list) = sum over ordered a-tuples of distinct indices
random.seed(3)
lam = [Fr(1, 2), Fr(1, 3), Fr(2, 7)]
def phi(sel, rest):            # arbitrary test function of (selected ordered values, remaining multiset)
    return Fr(1 + 3*sum(i*v for i, v in enumerate(sel)) + sum(v*v for v in rest), 1 + len(rest))
for (j, a) in [(3, 1), (4, 2), (5, 2), (5, 3)]:
    lhs = Fr(0)
    for u in itertools.product(range(3), repeat=j):
        w = 1
        for v in u: w *= lam[v]
        s = Fr(0)
        for idx in itertools.permutations(range(j), a):
            rest = tuple(sorted(u[i] for i in range(j) if i not in idx))
            s += phi(tuple(u[i] for i in idx), rest)
        lhs += w*s
    lhs /= factorial(j)
    rhs = Fr(0)
    for sel in itertools.product(range(3), repeat=a):
        for rest in itertools.product(range(3), repeat=j-a):
            w = 1
            for v in sel + rest: w *= lam[v]
            rhs += w*phi(sel, tuple(sorted(rest)))
    rhs /= factorial(j-a)
    print(f"toy measure j={j} a={a}: (1/j!) int sum_ordered-selections = {lhs}  vs  int dlam^a dlam^(j-a)/(j-a)! = {rhs}: {lhs == rhs}")
```

Output:

```
(3.25): 2176 triples (j<=15, b<=15), failures 0
(3.19) selection identity: 400 pairs, failures 0
toy measure j=3 a=1: (1/j!) int sum_ordered-selections = 41971/49392  vs  int dlam^a dlam^(j-a)/(j-a)! = 41971/49392: True
toy measure j=4 a=2: (1/j!) int sum_ordered-selections = 9863185/6223392  vs  int dlam^a dlam^(j-a)/(j-a)! = 9863185/6223392: True
toy measure j=5 a=2: (1/j!) int sum_ordered-selections = 1693249307/3136589568  vs  int dlam^a dlam^(j-a)/(j-a)! = 1693249307/3136589568: True
toy measure j=5 a=3: (1/j!) int sum_ordered-selections = 92713939/29042496  vs  int dlam^a dlam^(j-a)/(j-a)! = 92713939/29042496: True
```
