HOLDS AS READ

Seat T — printed §4, §5, §7 of "An asymptotic formula for the number of totients" (OpenAI, 25 Sep 2026).
Work dir: /tmp/oaimath/024/seats/T_work/ (scripts lpre.py, seeds.py, invphi.py, expcheck.py; log lpre.log; Ford PDF/text in ford/, Ford sieve notes in sieve/).
About 60 minutes of work. I found no false step and no unjustified step in my scope. Everything below is either a verification (V) or an exposition note (E). Nothing is fatal or a gap.

## Findings

1. **§4.1 Lemma 4.1, eq. (4.3). Severity: V.**
   The paper says "Ford's uniform upper sieve [8, Theorem 2.5] gives … ≪k X/(log X)^k (∆/φ(∆))^k … the implied constant depends only on k".
   I fetched Ford's sieve notes (sieve2023.pdf, p. 19) and checked the statement word for word. It asks for (a_j,b_j)=1, distinct forms and admissibility, and gives "the implied constants may depend on k alone".
   - Determinants: for the two forms n, An+1 the determinant is A. For the three forms n, An+1, A'n+1 it is A·A'(A−A'). Both are at most y^3, and the second is nonzero exactly because A≠A'.
   - The inadmissible case: an offending prime is at most k, and each form equals that prime for at most one n. So it contributes a bounded number of n, which (4.1) absorbs.
   - ∆/φ(∆) ≪ log2 ∆ holds by splitting at log(d+10).
   - (4.2) follows from (4.1) by partial summation and is uniform in the coefficients.

2. **§4.2 Proposition 4.2, the whole chain. Severity: V.**
   - Top layer: "Only the zeroth shift can have a prime factor greater than Y1". Normality gives Ω(p0−1) ≤ 3By and Q ≥ y^{1/(8By)}. With X ≥ Q, (log X)^{-3} ≤ (8By)^3 (log y)^{-3}. Mertens bounds Σ1/t′ ≪ (log y)^{1−ν1}. Together these give (4.7).
   - Intermediate layer: "Q1 = Q2" uses the three-form sieve; "Q1 ≠ Q2" uses two two-form sums. In the cross-slot incidence "AQ2Q1 + 1 and A′Q2 + 1", the inner sum is taken while AQ2 ≤ y is still in force. The two cross incidences cannot both hold, as the paper says. Every primality condition is available at that layer, because slot i−1 is complete once layer i is added.
   - (4.10): "Σ i^{2Ω(t)}/t ≤ Σ_{n≤Ii}(i²Mi)^n/n! ≤ i^{Ii} exp(iMi)". Checked numerically on 20,000 random (i, M, I): no violation.
   - The exponent identity "−2−ν1+Σ_{i=2}^b{−2µ_{i−1}+c_i(ν_{i−1}−ν_i+δ)} = −2+Σ a_jν_j+2Σ(ν_j−µ_j)+δΣc_i−c_bν_b" and c_{j+1}−c_j−2 = a_j both hold, to 2e−14 over 2,000 random instances (expcheck.py).
   - Smooth part: Ω(s) ≤ 3bL_b from normality on (S,Y_b], then Σ_{P+(s)≤Y_b} 1/s ≪ log Y_b. This gives (b+1)^{Ω(D)}(log Y_b)^{1+3b log(b(b+1))}/D.
   - Remark 4.3's claim about how E_b grows is correct.

3. **§4 opening and Prop 4.2(iii) against Ford's Lemma 5.1. Severity: V (the paper is stronger than its source here).**
   The paper says: "we assume squarefreeness of the whole product above the last cutoff; squarefreeness of each individual shift would not suffice for our factor-allocation estimate."
   This is right, and it fixes a step in Ford. Ford's hypothesis (1) only says "neither pi − 1 nor qi − 1 is divisible by r² for a prime r ⩾ vk". His proof then asserts "Also, by assumption (1), t is squarefree", which fails when one prime divides two different shifts.
   OAI has the matching cost: (3.21) in printed §3 charges for "divides two different shifts" (I did not check that cost; it is outside my scope).
   The paper also drops two of Ford's hypotheses, and both drops are sound:
   - Ford's ν_{j−1}−ν_j ≥ 2δ. Quote: "It is valid without any lower bound on ∆i/δ". Checked: (4.10) never uses it.
   - Ford's r ≤ y^{1/10} and d ≤ y^{1/100}. Quote from Remark 4.3: "the large top part supplies the lower bound for the actual sieve endpoint". Checked: X ≥ Q ≥ y^{1/(8By)}.

4. **§5.1 Proposition 5.1, collision coverage. Severity: V.**
   The paper says: "If two distinct tuples have the same value, some displayed prime differs: equality of all the primes p0, …, pR would also force equality of d."
   So every ordered pair of distinct good tuples with equal value has a first unequal index i ≤ R, and it is counted once at that i. Equal prefixes with different tails give one tuple, which is allowed. Equal prefix primes with different d give different values.
   I tried to build a collision family the argument misses:
   - Prefixes that differ in many primes. Up to J+1 differing indices are handled by the layers, with b ≤ J+1 ≤ By. Deeper differences sit in the z-smooth Di, D′i, and are paid for by Σ_{P+(D)≤z} 1/D ≪ log z = exp(O(b_i h^{-18})) and by (5.8).
   - Equal primes at different positions. Ruled out by the disjoint bands: the gap is ≍ b_i h^{-20}, much larger than the O(log b_i) error.
   - p−1 and q−1 sharing their largest prime. This is the Q1 = Q2 three-form case.
   - Two shifts on one side sharing a prime above z. Excluded by the good condition (3.18), whose cost is in §3.
   I found no case the argument misses.

5. **§5.1, checking Prop 4.2's hypotheses inside Prop 5.1. Severity: V.**
   - S = Si < z = Yb.
   - Grid intervals of width O(Jδ), with Jδ = o(h^{-20}). They stay separated and lie below height 0.8: u_{i+1}/By ≤ 0.62/0.88 ≈ 0.705. Index 0 lies above height 0.9.
   - The top part of pi−1 above Y1 exceeds √y, because log of the Y1-smooth part ≤ 4By(log y)^{0.8}.
   - The squarefree condition survives cancelling the equal shifts.
   - pj ≠ qj on the surviving indices.
   - (5.5): "(j+1)(e−δ) ≤ j(e+δ)". Normality applies at endpoints A′j > z > S, and both residuals are z-smooth.
   - (5.6): ν_k ≤ log2 A_{j_k}/By + O(Jδ) and log2 A_j ≤ u_{i+j}, so the O(log b_i) error in (5.4) is one-sided and harmless. Then the strict slack gives an exponent ≤ −1 − h^{-4}(1−o(1)).
   - (5.9): the costs are O(h²) + O(b_i log h/h^8) + O(b_i log h log log h/h^18), all o(b_i/h^4).
   - The dyadic sum (5.11) gives h^4 e^{−c3 b_i/h^4}.
   - Restoring the prefix through (3.13) gives Σ_h h^4 exp(−c4 ρ^{−h}/h^3) → 0, and i = 0 gives exp(−cB/m^4) = o(G_m).
   - Numerical side conditions: ρ = 0.5425986, λ = 0.6113855, 30λ = 18.34 ∈ (18,20), 1.1ρ = 0.597 < 0.6, C0 = 0.8178146, D0 = 2.1769687. All match (3.3), (5.2) and (1.1).

6. **§5.2 Lemma 5.2 and Proposition 5.3. Severity: V.**
   - −|E| ≤ |T|−|W| ≤ |D|+K/2.
   - |E*| ≤ |E|+|D|+K/2 and |F⁻¹(E*)| ≤ |E|+2|D|+K, using r ≤ 1 + r(r−1)/2.
   - The map is a bijection off E*.
   - (5.13), "ℓ(v) = p0···pR ℓ(d)": the lower bound uses "every preimage" from Prop. 3.3, together with v ∉ F(D) and r_v ≤ 1. The upper bound uses ℓ(d) ≤ w < pR, so ℓ(d) is coprime to Q. Correct as written.

7. **§7.1 Lemma 7.1. Severity: V.**
   - The interval length "min{T, (k+1)U} − min{T, kU} = T fk(r/q)" holds with U = Tq/r. This identity was the one place I expected an error, and it is right.
   - "z ↦ fk(1/z) is (k+1)-Lipschitz on [0,1]": the true constant is max(1,k), so the claim holds.
   - The prime number theorem is applied additively with endpoints x^{1−o(1)}, and the lower cutoff is inactive. The error is O_k(K_H Σ1/p_i) → 0.
   - I also checked the piecewise form of fk at the start of §7 against (2.9), and the Lean comparator `fk`, `ell` and `N`. They agree.

8. **§7.2 Lemma 7.2 (Ford's inverse-fiber propagation). Severity: V.**
   I checked this against Ford arXiv 1104.3264v2 (pp. 24–26 and p. 39). Ford writes: "n1 = ndi for some i. These we will call the trivial solutions to (5.18). We then have A(dφ(n)) = κ for each n ∈ B for which (5.18) has no non-trivial solutions … In particular, for such n we have φ(n′) ≠ φ(n) for n′ ≠ n". He ends with "Vκ(x) ⩾ |B|/2 ≫ε d^{−1−ε}V(x)". On p. 39 he writes: "for at least half of the numbers b ∈ B, the totient φ(b)d has only the pre-images bmi".
   So the full fiber {b d1, …, b dκ} holds on at least |B|/2 distinct values ≤ x, exactly as the lemma uses it. P+(di) ≤ d+1 < pL, so the fiber argument closes. Then ℓ(v) = bℓ(d), and ℓ(v)/v = (b/φ(b))(ℓ(d)/d).
   Ford's own sentence "none of the primes qi (0 ⩽ i ⩽ L) occur to a power greater than 1" should read pi. This is Ford's typo and does not matter.

9. **§7.2 Lemma 7.3 and §7.3 positivity. Severity: V.**
   - The ordering of constants is right. η and δ come from the seed, C from Lemma 7.3 with ε = η/4, and all three are fixed before H. Prop. 5.3 then removes at most ηV(x)/4.
   - The tail ratio lies in [k+δ, C], since the prefix product is 1+o(1), giving M_{1_I} ≥ c1 Gm. Then inf_I fk ≥ min{δ/(k+δ), 1/C}, so M_{fk} ≥ c2 Gm, and C_{fk}(x) ≥ c2/2.
   - The bounds clause of Lemma 6.6 (printed §6) is valid without continuity, because "θ(xn) = s exactly" holds along x_n = exp exp B_n. I read Lemma 6.6 but did not check its Prop. 6.5 input.
   - The zero alternative is trivially correct.
   - The claim that the first alternative for all k is equivalent to sup ℓ(d)/d = ∞ is a tautology, and correct.

10. **§7.3 Remark 7.4, where k = 2 is shown. Severity: V for the claim, E for the route.**
    The paper says: "Ford gives d = 2^18 · 257 as a totient all of whose preimages are divisible by 8 [7, Section 7.3, p. 39] … ℓ(d) > 2d."
    Verified by exhaustive inverse totient (invphi.py): φ⁻¹(67,371,008) has exactly 8 elements, all ≡ 0 (mod 8). ℓ(d) = 2^11·257² = 135,268,352, and ℓ(d)/d = 257/128 = 2.0078125.
    k = 1 is not argued separately. It follows from the same seed (ℓ(d) > 2d > d), and also holds trivially for any totient d ≥ 2.
    The "divisible by 8" route is more than is needed. The smallest seed is d = 5888 = 2^8·23, whose least preimage 11985 = 3·5·17·47 is odd and gives ℓ(d)/d = 2.0355. Sieve and inverse totient agree on this; it has 9 preimages.

11. **Requested numerics (lpre.py, sieve of φ to 5.9·10^7; n/φ(n) < 5.85 below 223092870, so every preimage is captured). Severity: V and E.**
    Positive control: V(10^6) = 180,184 and V(10^7) = 1,634,372, equal to Ford's Table 1.

    | | x = 10^6 | x = 10^7 |
    |---|---|---|
    | N1(x)/V(x) | 16,323/180,184 = 0.09059 | 148,579/1,634,372 = 0.09091 |
    | N2 … N5 | 0 | 0 |

    - N1/V stays between 0.089 and 0.091 for x = 10^4 … 10^7.
    - Max ℓ(d)/d over d ≤ 10^6 is 2.035496, at d = 5888 and d = 276736.
    - Max ℓ(d)/d over d ≤ 10^7 is 2.041379, at d = 2,037,248 = 2^9·23·173, with ℓ = 4,158,795 = 3·5·17·47·347. Only 10 totients d ≤ 10^7 have ℓ(d) > 2d.
    - N2 = 0 does not contradict Theorem 2.2(i). Here m(10^6) = m(10^7) = 1 with θ ≈ 0.636, while the proof needs R = m − H ≥ 0 with H large, and m = 10 already needs x ≈ 10^(4·10^1613). So these numbers neither support nor test the asymptotic.

## Statements from other sections used as given
- (3.4), (3.5), (3.6) and (3.11).
- Lemma 3.6 / (3.13).
- Prop. 3.3, including the "every preimage" quantifier.
- Prop. 3.8, together with the good conditions (3.18), (3.19) and the costs (3.20)–(3.22).
- Normality estimate (3.9).
- Lemma 6.6 and Prop. 6.5 (§6).

## Not checked
- The proof of Ford's sieve Theorem 2.5 itself (I checked the statement only).
- Ford's internal estimates (5.20)–(5.37) behind |B| − Σ|Bj| ≥ |B|/2 (I checked only that the construction yields full fibers).
- All of printed §2, §3 and §6 beyond the statements listed above.
- The literature claim that unboundedness of ℓ(d)/d is open ([5, §I.9]).
- The Lean: I read the comparator statement only. It includes `weighted_totient_asymptotic` and `weighted_totient_one_two`, matching Theorem 2.2 and the k ∈ {1,2} claim. I did not build or replay anything.
