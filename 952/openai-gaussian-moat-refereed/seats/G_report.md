# SEAT G report: printed §§1–4 (Thm 1.1/1.2, Prop 2.1, §3, §4)

Referee stance: hostile. I read `main.tex`, `periodicity.tex`, `preliminaries.tex` and `geometry.tex` line by line against `paper.txt`. Printed numbering is used throughout: (3.1) prime count; (4.1) fixed-line tail; (4.2) cube inequality; (4.3) enrichment; (4.4) difference coordinate; (4.5) product concentration; (4.6) enrichment chain.

I re-derived every inequality, its direction and its "sufficiently large" threshold. Where a cheap check existed I ran it. Scripts are in `/tmp/oaimath/028/seats/G_work/`, each run under `ulimit -v 4000000; timeout 900`.

**Bottom line:** I found no FATAL error and no GAP in §§1–4. Every load-bearing step holds. The items below are EXPOSITION points and unverifiable bibliographic details. None of them propagates.

---

## 1. Theorem 1.1 / 1.2 statements and introduction

- **Theorem 1.1 vs Erdős #952.** #952 asks for an infinite sequence of distinct Gaussian primes with |x_{n+1}−x_n| ≪ 1. Theorem 1.1 says that for every finite D no such sequence has more than B_D terms, so the answer is "no".
  - The comparator `ComparatorChallenges/GaussianMoat.lean` (`MainEndpoint ∧ UniformEndpoint`) states the same two conclusions. Components are finite with `ncard ≤ B`, and injective walks have length ≤ B.
  - `FC_952.lean` (∄ injective prime sequence with `(x(n+1)−x n).norm < C`) is implied.
  - The claim "for D<1, distinct lattice points cannot be adjacent, so B_D=1 suffices" is correct.
- **Prior-work claims.**
  - **Gethner–Stark.** I downloaded the published abstract (EMIS `abs-gethner.ps`). Verbatim: *"A question of Gordon, mistakenly attributed to Erdős, asks if one can start at the origin and walk from there to infinity on Gaussian primes in steps of bounded length. We conjecture that one can start anywhere and the answer is still no. We introduce the concept of periodic Gaussian moats to prove our conjecture for step sizes of √2 and 2."* This confirms the Gordon attribution, the any-start formulation, and the periodic obstructions for √2 and 2.
    - The narrower claim that G–S formulated a *uniform length bound*, and the 1962 ICM / Stockholm detail, are in the body (pp. 289–292), which I could not retrieve. → COULD NOT CHECK, not load-bearing.
  - **Erdős 1977.** The recollection (Motzkin, Pasadena, November 1963, Gordon and Motzkin) matches the Er77c quote on the live problem page. I did not verify the page number p. 69.
  - **GWW Theorems 4.1/4.4, Vardi §6 Prop 6.2, Tsuchimura.** These are consistent with secondary sources: prime-free stretches along lines, isolated primes, and the width-6 moat from the origin. The full texts were not retrievable (the Project Euclid PDF of Vardi was blocked), so the theorem numbers are unverified. Not load-bearing: Prop 2.1 is proved in full in the paper, and its correctness does not depend on the attribution.

## 2. Proposition 2.1 (periodic reduction). HOLDS

Checked step by step:

1. **Periodicity.** π_p | p | Q, so z + Qw ≡ z (mod π_p) and (mod π̄_p). Hence 𝒜(𝒫) and its D-graph are QZ²-invariant, and the graph is locally finite (≤ K_D−1 neighbours).
2. **Finite components.** "An infinite component would contain an infinite simple path." This is König's lemma, and the argument given (finitely branching tree of simple paths with arbitrarily deep vertices) is correct. Each such path is a self-avoiding walk in 𝒜(𝒫), which the hypothesis forbids.
3. **Size ≤ Q².** Suppose x ≠ y in a component C with y − x = v ∈ QZ². Translation by v is a graph automorphism mapping C to the component of y, namely C itself. A finite nonempty subset of Z² is not invariant under a nonzero translation, so C injects into (Z/QZ)².
4. **Components meeting E.** A Gaussian prime divisible by a selected factor is an associate of it. So primes ∖ E ⊆ 𝒜(𝒫), and G_D[primes∖E] is a subgraph of the avoiding graph.
   - If C meets E, each component of C∖E has at least one edge into C∩E, and distinct components use distinct edges. The number of edges leaving E is ≤ (K_D−1)|E|.
   - Each such piece lies in an avoiding-graph component of size ≤ Q². Hence #C ≤ |E| + (K_D−1)|E|Q².
   - Components not meeting E have size ≤ Q². The displayed bound max{Q², |E|+(K_D−1)|E|Q²} is correct.
5. **"Delete an initial segment" remark.** An injective walk visits each of the finitely many points of E at most once. The tail after the last such visit is an infinite injective D-walk in 𝒜(𝒫_D), which contradicts Theorem 1.2. Correct.

- EXPOSITION (P2.1-a). "let E be the set of associates of the selected Gaussian factors" must mean the associates of **both** π_p and π̄_p, so |E| = 8|𝒫|. With only the π_p, the inclusion primes∖E ⊆ 𝒜(𝒫) would fail. §1.1 "choose conjugate Gaussian prime factors π_p, π̄_p" makes the intent clear.

## 3. §3 (prime count, entropy conventions, Lemmas 3.1–3.3). HOLDS

- **(3.1).** θ(2T;4,1) − θ(T;4,1) = T/2 + o(T) follows from Selberg's ∑_{p≤x, p≡1(4)} log p ∼ x/2 (Canad. J. Math. 2 (1950) 66, the PNT in APs). The endpoint term at p = T is ≤ log T. The sum lies in [k_T log T, k_T log 2T], so k_T = (1/2+o(1))T/log T. log T ≤ L*_T ≤ log 2T is trivial. Correct.
- **§3.1 split-prime facts.** All correct:
  - π, π̄ | v ⇒ p | v.
  - π | a ∈ Z ⇔ p | a.
  - A nonzero multiple of π has length ≥ √p.
  - det(αv, αw) = N(α)·det(v,w).
- **§3.2.** Two facts checked:
  - D_KL(p‖Unif) = log a − H(p).
  - The Pinsker derivation: D ≥ D(Ber(u)‖Ber(v)) by log-sum; ∂²_u = 1/(u(1−u)) ≥ 4; value and derivative vanish at u = v; so the bound is ≥ 2(u−v)² = 2TV².
  - The citation is correct: Cover–Thomas Lemma 11.6.1 is Pinsker, stated in bits with 1/(2 ln 2), which is equivalent.
- **Lemma 3.1.** The displacement lies in a disk of radius Dn, which has ≤ C_D(n+1)² lattice points. F(z_{T0}) = F(z_{T1}) − F(Δ) because residue maps are additive. So H(F z_{T0}) ≤ H(F z_{T1}) + H(Δ). Correct.
- **Lemma 3.2.** The coupling plus Fano argument gives |H(U) − H(Ũ)| ≤ h(δ) + δ log(a−1) with δ = TV ≤ ε ≤ 1/2. h is increasing on [0, 1/2]. TV of the marginals is ≤ TV of the joints. Then subtract the joint and marginal bounds. Correct.
- **Lemma 3.3.** B is determined by (X, Y), so H(X|Y) = H(B|Y) + H(X|B,Y) ≤ h(ρ) + ρ log b + (1−ρ) log a. Correct. Fano is Cover–Thomas Theorem 2.10.1; the citation is correct.

## 4. §4

### Lemma 4.1 (many differences). HOLDS

- **Projection claim.** A projection beyond p₁ gives distance > R to p₀. So E lies in an R × 2W rectangle. R ≥ W ≥ 1 because R ≥ 1 and the max distance from the line is ≤ R.
- **Lower bound A ≥ cn.** Disjoint radius-1/3 disks fit in an area-(R+2/3)(2W+2/3) ≤ (40/9)RW region, giving c = π/40.
- **Upper bound.** A ≤ R² ≤ D²n².
- **W = 1 case.** |E−E| ≥ n+1 > A/D, since A = R ≤ Dn. This uses self-avoidance, which is assumed in §4.
- **W > 1 case.** |det(a,b)| = R·W = A.
  - The map (s,t) ↦ α(s) − γ(t) mod Λ is well defined: the edge identifications differ by a and −b.
  - Homotopies rel endpoints keep it well defined at every stage and connect it to (s,t) ↦ sa − tb, a homeomorphism of degree −1 for the (a,b) orientation.
  - Nonzero degree implies surjectivity (punctured torus has H₂ = 0). The citation is checked against Hatcher's text: Thm 3.26(a) is the fundamental class, Prop 3.29 is H_n = 0 for a noncompact manifold, and Ex. 3.3.7 is the definition of degree.
  - Interpolated points lie within D (in fact D/2) of a segment vertex. This is legitimate because the walk between p₀ and p₁ (or p₂) stays inside the segment.
  - So the 2D-disks about the image of E−E cover the torus, and A ≤ 4πD²|E−E|.
  - c_D = min(1/D, 1/(4πD²)).
- **Numerical check** (`lemma41.py`). I tested 1,547 walks for D = 1, √2, 2: random SAWs, direction-persistent SAWs, spirals, serpentines (also on 2Z² for D = 2), and straight lines in every step direction, with n ≤ 300.
  - The projection claim held in every case.
  - min |E−E|/A was 2.00 for D = 1, 1.42 for √2 and 0.66 for 2, against the paper's c_D of 0.080, 0.040 and 0.020.
  - min A/n = 0.447 against c = π/40 = 0.0785.
  - max A/(D²n²) ≤ 1.

### Lemma 4.2 (randomly signed product avoids a thin rectangle). HOLDS

(ii) items, each checked:

- **Collinearity.** Suppose σ and σ′ differ in h ≤ dr/4 coordinates, with c* the product of their common factors.
  - N(c*) ≥ P/(2T)^h.
  - det(w, w′) = N(c*)·det(u, v).
  - For w, w′ in an origin-centred rectangle, |det| ≤ 2R₁W₁ ≤ 2P^{1−d}.
  - log N(c*) − log(2P^{1−d}) ≥ d log P − h log 2T − log 2 ≥ dr(log T − ¼ log 2T) − log 2. This is exactly the printed expression.
  - For T ≥ 5, log T − ¼ log 2T ≥ 1.03. Since d < 1/4, dr ≥ 16 d³r ≥ 16 C₀, so the expression is positive and det = 0.
  - h = 0 gives a unique witness line per bad σ. This also follows independently: area(Q) = 4R₁W₁ < 2P = 2 covol(β_σ Z[i]) forces all lattice points in Q to be collinear.
- **Fixed line, E_σ log P_σ(v) ≤ log|v|.** v is primitive, so at most one factor over each p_i divides v. The eligible factors are distinct primes dividing v, so the norm of their product is ≤ N(v). Each is selected with probability 1/2. So E log P_σ(v) = ½ log N(∏ eligible) ≤ ½ log N(v) = log|v|. Correct.
- **Witness length.** π_i ∤ v and π_i | av imply p_i | a. The π_i are pairwise non-associate (distinct norms), so ∏π_i | av ⇔ each π_i | av. Hence the minimal witness length on the line is |v|P/P_σ(v), and a witness exists only if it is ≤ √2 R₁ ≤ √2 P^{1−d} (using W₁ ≥ 1). The required deviation is ≥ d log P − log√2.
- **Hoeffding constant.** Hoeffding (1963) Thm 2 eq. (2.6) is P(S − ES ≥ t) ≤ exp(−2t²/∑(b_i−a_i)²); the citation is correct.
  - Here the ranges are ≤ log 2T and t ≥ dr log T − 0.35.
  - With log 2T/log T ≤ log 10/log 5 = 1.431 for T ≥ 5, and dr log T ≥ 7, this gives c₀ ≥ 0.88. It is absolute.
- **Cube inequality (4.2).** The induction is correct:
  - The split gives |S|(r−1−log₂|S| + h₂(a)).
  - Cross edges number ≥ |1−2a||S|.
  - h₂(a) ≥ 1 − |1−2a| by concavity on each half.
  - Base case r = 0; empty halves contribute 0.
  - Dividing by r gives the vertex-boundary corollary.
- **Hamming separation and disjointness.** If x is within h = ⌊dr/10⌋ of both S_ℓ and S_ℓ′, then dist(S_ℓ, S_ℓ′) ≤ 2h ≤ dr/5 < dr/4. This contradicts the collinearity step, so the neighbourhoods are disjoint.
- **Growth.** While the relative size is ≤ e^{−c₀d²r/2}, the vertex boundary is ≥ |S|·c₀d²/(2 ln 2). So each step grows the set by a factor ≥ 1 + c₁d², with c₁d² ≤ 0.04.
  - With h ≥ dr/20 (dr ≥ 10 via C₀), h steps give ≥ e^{c₁d²h/2} ≥ e^{(c₁/40)d³r}.
  - Early threshold crossing gives growth ≥ e^{c₀d²r/2} ≥ e^{c₂d³r}, since d < 1 and enlargement is monotone.
  - Summing over the disjoint neighbourhoods gives Pr(bad) ≤ e^{−c₂d³r}, so C = 1 works.
- **Sanity check on strength** (`lemma42.py`). The setup: an exact integer lattice-reduction decision for all 2^16 sign vectors, 16 primes ≡ 1 (mod 4) in [220, 440], d = 0.249, R₁W₁ = P^{1−d}.
  - Six random orientations (W₁ from 1 to 1000) gave **0** bad sign vectors.
  - A rectangle aimed along the "dangerous" direction e = ∏_{i≤m} π_i⁺ gave exactly 2^{−9} bad for m = 9 and 2^{−10} for m = 10, all on one line, and 0 for m ≤ 8.
  - So the true worst case is ≈ 2^{−2dr·log 2T/log T}, here predicted as 2^{−8.99}, which matches. The lemma's e^{−cd³r} is weaker and so is consistent with this worst case. A claim of e^{−c·dr} with c > 2 ln 2 would have been false.
  - With r = 16, dr/4 < 1, so the Hamming-separation step is vacuous in these instances. It was verified by hand only.

### Lemma 4.3 (entropy enrichment). HOLDS

- **Concavity of f_Z.** Use a uniform random ordering with signs attached per prime. f(s+1) − f(s) = E H(next coordinate | first s). Exchangeability of positions s+1 and s+2, plus "conditioning reduces entropy", shows the increments decrease.
  - Exact check (`concavity.py`): 480 checks of increment monotonicity on three small batches and four kinds of Z (random, collinear, multiples of a factor, walk segments). There were 0 violations, and f(s) ≤ sL* held throughout.
- **Regime, items (iii).**
  - b = ⌊g²U/L*⌋ ≥ 1 and b < q.
  - log A ∈ [gU − O(1), 2gU + O_D(1)], with A ≥ c·⌊e^{gU}⌋.
  - r = ⌈(1+10g) log A/L*⌉ satisfies r ≥ gq/2. This needs gU/L* → ∞.
  - r ≤ 2.2gU/L* + O_D(1)/L* + 1 ≤ 3gq.
  - 3gq + b < q because g < 10⁻². So J fits in the q − b remaining coordinates.
- **Differences-of-differences rectangle.**
  - E ⊆ [0,R] × [−W,W] in diameter coordinates.
  - E − E ⊆ [−R,R] × [−2W,2W].
  - (E−E) − (E−E) ⊆ [−2R,2R] × [−4W,4W]. So the printed half-lengths 4R, 4W (product 16A) are a valid, slightly generous over-estimate, with 4R ≥ 4W ≥ 1 as Lemma 4.2 requires.
- **Product concentration (4.5).** The mean is exactly rL* ≥ (1+10g) log A. The deficit needed is ≥ 5g log A. The variance without replacement is ≤ r(log 2)²/4. log A ≥ (r−1)L*/(1+10g). Chebyshev then gives O(1/(g²rL*²)). Correct.
- **On the good event.** (1+5g)(1−g) ≥ 1+3g for g ≤ 1/5, and A^{3g} > 16 since g log A ≥ g²U − O(g) → ∞. So 16A ≤ P^{1−g}.
  - Lemma 4.2 applies with d = g < 1/4 and g³r ≥ g⁴q/2 → ∞.
  - Its probability is over J's fair independent signs, and the rectangle depends only on t.
  - No nonzero multiple of ∏_J π in the rectangle ⇒ F_J is injective on E_t − E_t.
- **Error terms are o(g) uniformly.**
  - 1/(gq) = o(g) ⇔ g²q → ∞ (C = 2).
  - 1/(g²rL*²) ≤ 2/(g³qL*²) = o(g) (C = 4).
  - g³r ≥ g⁴q/2 = (g⁵U/2L*)/g ≫ 1/g ≥ log(1/g), so e^{−cg³r} = o(g) (C = 5).
  - All bounds depend on t only through r ≥ gq/2, so they are uniform over walks, batches and time laws.
- **(4.4).** On good J, H(F_J(h) | τ=t) = log|E_t−E_t| ≥ log A − log(1/c_D).
  - Conditioning on (B_x, B_y) costs ≤ 2b log 2T.
  - Conditional subadditivity, with every member of a uniform J ⊆ Q∖S having uniform marginal, gives (1/r)·E ≤ E_j H(h_j | B_x, B_y, τ=t).
  - log A/(rL*) ≥ 1 − 10g − 1/r = 1 − O(g), and 2b log(2T)/(rL*) = O(g).
  - Averaging over t gives conditioning on τ. Removing τ increases entropy, which is the correct direction.
- **(4.6) chain.**
  - (F_jX, F_jY) ↔ (h_j, F_jX) is a bijection, since F_j is additive, so the first line is an identity.
  - The upper bound uses subadditivity, dropping conditioning on the other prefix, and replacing h_j by the finer h in the subtracted term (more conditioning gives a smaller subtracted entropy, so the inequality is preserved).
  - Exact check (`chain46.py`): 180 random small instances gave min(RHS − LHS) = 0, never negative.
- **Subtracted-term average.** ∑_{j∈Q∖S} H(F_jX | B_x, B_y, h) ≥ H(F_Q X | B_x, B_y, h), because B_x = F_S X.
  - This is ≥ H(F_Q X) − H(B_x, B_y, h) ≥ f_X(q) − 2b log 2T − H(h), as printed.
  - f_X(q) ≥ f_Z(q) − H(X−Z).
  - H(h) + H(X−Z) ≤ 4 log(n+1) + O_D(1) = O_D(gU) by the counting bound.
  - (f − O(gU))/(q−b) ≥ f/q − O_D(g)L* because f ≥ 0 and q − b ≥ q/2.
- **First-term averages.** These are f_X(b+1) − f_X(b) and f_Y(b+1) − f_Y(b). (S, j) is a uniform b-subset plus a uniform extra coordinate, with fair signs.
- **Concavity with f(0) = 0** gives f(b+1) − f(b) ≤ f(b)/b, with b ≥ 1.
- **Mixture.** F_S(V) has law ½F_S(X) + ½F_S(Y). By concavity of H, f_V(b) ≥ ½(f_X(b) + f_Y(b)). Also checked exactly in `chain46.py`: min slack 0.
- Dividing by bL* gives (4.3) exactly as printed. All directions are correct.

## 5. Objections (all non-fatal)

| # | Location / quote | Class | Comment |
|---|---|---|---|
| G1 | Lemma 4.3: "Consider any asymptotic family in which D is fixed, T→∞, q≤k, and g^C U/log T → ∞ for every fixed C>0" | EXPOSITION | **What the proof uses:** only C ≤ 5 (plus T ≥ 5 and g < 10⁻²). The proof therefore supports a cleaner threshold statement: ∃ C_D, Λ_D such that if q ≤ k, 0 < g < 10⁻², and g⁵U ≥ Λ_D log T, then (4.3) holds with error C_D·g uniformly.<br>**Why it matters:** §6 applies the lemma to many (U, g, batch) tuples at once for each M. The threshold form makes uniformity over tuples explicit, whereas the "family" phrasing leaves it implicit.<br>**Downstream check:** §6.2's verification (log U ≥ cX_{⌈M/2⌉}, log(1/g) = O(M^{20}), log log T = O(M)) does give min over tuples of g⁵U/log T → ∞. The output-to-input matching ⌊g²U/L*⌋ = b at U′ = g²U is exact, so the application is fine. |
| G2 | Lemma 4.3 proof: "Its average is at least f_X(q)−2b log(2T)−H(h)" followed by "(f_Z(q)−O_D(gU))/(q−b)" | EXPOSITION | The −2b log 2T term is silently absorbed into O_D(gU). This is valid because 2b log 2T ≤ 2g²U(1+o(1)). |
| G3 | Lemma 4.3 proof: "differences of differences … lie in an origin-centered rectangle of half-lengths 4R, 4W" | EXPOSITION | True. 2R, 4W already suffice, so the stated rectangle is a harmless over-estimate. |
| G4 | Prop 2.1: "let E be the set of associates of the selected Gaussian factors" | EXPOSITION | Must include both π_p and π̄_p (\|E\| = 8\|𝒫\|). Intended meaning is clear from §1.1. |
| G5 | Notation reuse | EXPOSITION | Q is the modulus in Prop 2.1, the rectangle in Lemma 4.2 and the signed set in Lemma 4.3. E is the exceptional associates in Prop 2.1 and the segment in Lemma 4.1. h is a Hamming distance / radius in Lemma 4.2 and the difference in Lemma 4.3. c₀ is the absolute Hoeffding constant in (4.1) and the schedule constant in §6.2. P is a prime product in Lemmas 4.2/4.3 and the batch 𝒫. No quantifier confusion results: Lemma 4.2's c₀ is absolute and independent of the §6 ordering D, e₀, l₀, g₀, c₀, B, M. |
| G6 | §1 prior-work sentences (G–S uniform-bound formulation and pp. 290–292; GWW Thms 4.1/4.4; Vardi §6 Prop 6.2; Erdős p. 69) | COULD NOT CHECK (bibliographic) | G–S abstract and the Erdős quote are verified. Body texts and theorem numbers were not retrievable. None is used in any proof. |

Cited results actually used in §§1–4, with my reading of what each says:
- Selberg PNT in APs: matches.
- Hoeffding Thm 2 / (2.6): matches.
- Cover–Thomas Thm 2.10.1 (Fano) and Lemma 11.6.1 (Pinsker, bits): match.
- Hatcher Thm 3.26(a), Prop 3.29, Ex. 3.3.7: checked against the text; they support the degree argument.
- Harper (cube isoperimetry): the inequality is standard and is proved in full in the text anyway.
- Conrad (splitting of p ≡ 1 mod 4): standard and correct.

Each hypothesis used is satisfied where the result is invoked.

## 6. Numerical checks run

All passed, with no violation of any claimed inequality.

1. `lemma41.py`: Lemma 4.1 on 1,547 walks, D ∈ {1, √2, 2}. Results are in §4 above.
2. `cube.py`: exhaustive check of (4.2) over all nonempty S ⊆ {0,1}^r for r ≤ 4 (65,535 sets at r = 4). The minimal slack is 0 (subcubes are tight), and the vertex-boundary corollary also holds with min slack 0. h₂(a) ≥ 1 − |1−2a| was checked on a 10⁵-point grid.
3. `concavity.py`: exact f_Z concavity, 480 checks, 0 violations.
4. `lemma42.py`: exact Lemma 4.2 experiment. Random orientations gave 0 bad; the dangerous direction gave 2^{−9}, matching the predicted 2^{−2dr log 2T/log T}.
5. `chain46.py`: (4.6) and the mixture step, 180 exact instances, min slack 0.

Within my scope (printed §§1–4), every load-bearing inequality, its direction, and every "for sufficiently large parameters" were re-derived and hold. The quantifier order inside Lemmas 4.2/4.3 is sound: c, C, C₀ are absolute, O_D constants depend on D only, and the thresholds depend only on g⁵U/log T and T. Parts outside §§1–4 (§5–§8 and the §6 schedule beyond its interface with Lemma 4.3) were not adjudicated by this seat.

VERDICT: HOLDS AS READ
