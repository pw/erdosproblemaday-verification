# Hostile referee report — scope `concentration`
## Appendix A (pp. 74–90): "Uniform concentration of evaluation flats", and its two uses in §2.4 (Lemmas 2.4, 2.5)

Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…). All page numbers are printed = PDF pages. Displayed formulas were read from the rendered PDF (pp. 74–90, 11–13), not from the text extraction.
Primary sources fetched (current arXiv versions): Walsh, *The polynomial method over varieties*, arXiv:1811.07865**v2** (12 Jun 2020) → refs/1811.07865/v2.txt; Walsh, *Concentration estimates for algebraic intersections*, arXiv:1906.05843**v2** (26 Dec 2019) → refs/1906.05843/v2.txt; Tidor–Yu–Zakharov, *The Erdős distinct distances problem in R^3*, arXiv:2608.14454**v1** (14 Aug 2026; v1 is the only version) → refs/2608.14454/v1.txt; Stacks tags 00OQ, 00NQ, 02JN, 00NO, 00NA → refs/stacks/. Fulton *Intersection Theory* [14] and Hartshorne [17] are books: COULD NOT FETCH.
Small checks (nice 19): conc_scripts/segre_check.py (sympy: identity (A.25), nonnegativity of c(p,u), sign pattern at h = r), conc_scripts/exceptional_check.py (numpy: one isometry's matches ⇒ one maximal isotropic subspace; common Cayley point).

---

## 1. Theorem A.1 verbatim (p. 75) and the exact exponents

> **Theorem A.1 (Uniform concentration).** Fix C₀ ≥ 1. Let A ≥ 1 and let 𝒫 be a finite set of distinct parameters [v : y] ∈ 𝒬, all with v ≠ 0. Assume:
> (i) For every λ ∈ 𝒫 there is a homogeneous polynomial of positive degree at most C₀A which is nonzero at λ and zero at every other member of 𝒫.
> (ii) Every projective P^r ⊂ 𝒬 contains at most C₀A^{r−1} members of 𝒫.
> There is a constant C = C(e, C₀) such that
> #{λ ∈ 𝒫 : F_λ ⊂ V} ≤ C deg(V)A^h, dim V = s₀ + h, 1 ≤ h < r, (A.2)
> for irreducible proper affine varieties V ⊂ S, in either of these settings:
> (a) All such V are allowed, and |𝒫| ≤ C₀A^r.
> (b) Only V contained in the zero set of some nonzero polynomial of degree at most C₀A are allowed. No bound on |𝒫| is required.

Setting (p. 74): E complex, dim E = e ≥ 3; S = Λ²E*; n = C(e,2); r = e − 1; s₀ = n − r = C(e−1,2); 𝒬 = {[v:y] ∈ P(E⊕E*) : y(v) = 0} (smooth split quadric in P^{2e−1}); F_λ = {z ∈ S : zv = y} (affine s₀-flat, direction K_v = Λ²(E/Cv)*). Maximal linear subspaces of 𝒬 are P^r = P(e-dim totally isotropic). Exponents: separator degree O(A); isotropic cap A^{r−1}; total count A^r (not A^e); conclusion A^h with h = dim V − s₀.

| Use | e | r | s₀ | n | separators (i) | cap (ii) needed / supplied | total / setting | V allowed | conclusion |
|---|---|---|---|---|---|---|---|---|---|
| Lemma 2.4 (global, p. 12) | d+1 | d | d(d−1)/2 | d(d+1)/2 | s_p·s_q, deg ≤ 4(M−1) ≤ 4A (Lemma 3.1, M ≤ A eventually) | C₀A^{d−1} / ≤ N = A^{d/2} ≤ A^{d−1} | ≤ N² = A^d = A^r, setting (a) | all irreducible | C deg V A^h, 0 ≤ h ≤ d (endpoints trivial) |
| Lemma 2.5 (local, pp. 12–13) | d | d−1 | (d−1)(d−2)/2 | d(d−1)/2 = dim F_{p,q} | sep_u·sep_w, deg 2⌊A⌋ ≤ 2A (Prop 2.3) | C₀A^{d−2} / d ≥ 4: ≤ N = A^{d/2} ≤ A^{d−2}; d = 3: < C_rich A (Thm 7.1 deletion) | none, setting (b) | hypersurface components of a nonzero poly of degree ≤ A | Σ C deg V A^{d−2} ≤ CA^{d−1} |

Every exponent above was recomputed: N = A^{d/2}, N² = A^d; A^{d/2} ≤ A^{d−1} (d ≥ 2) and ≤ A^{d−2} iff d ≥ 4; neighbour flat {Z skew : Z(u+w) = u−w} has dimension C(d,2) − (d−1) = C(d−1,2) = s₀^loc, so codimension d − 1 = r^loc in F_{p,q}, and a hypersurface component has h = r^loc − 1 = d − 2 ≥ 1 exactly when d ≥ 3. The "useful consequence of (b)" (p. 75: "a nonzero polynomial of degree D ≤ C₀A contains at most CDA^{r−1} of the flats") gives C·A·A^{d−2} = CA^{d−1}, which is exactly Lemma 2.5.

## 2. The two uses, hypothesis by hypothesis

**Lemma 2.4** (p. 12). Quoted: "Physical separators from Lemma 3.1, one in p and one in q, have a product of degree O(M). Express them in the coordinates v₀, y₀ and homogenize with the last coordinate of v, which is 1 on every parameter. They give positive-degree homogeneous separators of degree O(M) ≤ O(A)."
- Parameter (2.7) [v:y] = [(v₀,1):(y₀,−v₀·y₀)] lies on 𝒬 (y(v) = y₀·v₀ − v₀·y₀ = 0) with v ≠ 0. Checked that F_{p,q} of (2.6) equals F_λ: the extra (d+1)-st coordinate of zv = y is −c·v₀ = −v₀·y₀, automatic from Zv₀ + c = y₀ and v₀·Zv₀ = 0. dim = n − r = d(d−1)/2 ✓.
- (i): s_p(v₀+y₀)·s_q(v₀−y₀)·(homogenised by v_{d+1}) is homogeneous in (v,y), nonzero at (p,q), zero at every other retained (p′,q′) (one factor vanishes). Lemma 3.1 gives deg s_p ≤ 2(M−1) (verified p. 15 formula), Δ(Q) = Δ(P) for Q = RP. ✓ Uses M ≤ A *eventually* only — no rate.
- (ii): "Suppose parameters lie in one projective maximal isotropic plane … Polarization gives … (v₀ − v₀′)·(y₀ − y₀′) = 0, |p − p′|² = |q − q′|² … There are at most N ≤ A^{d−1} such parameters." Recomputed: the polar form B((v,y),(v′,y′)) = y(v′) + y′(v) evaluates on two (2.7)-representatives to −(v₀−v₀′)·(y₀−y₀′) = −¼(|p−p′|² − |q−q′|²). Real representatives of points of a complex isotropic P^d lie in the complex isotropic subspace, so B = 0 is a correct real identity. p = p′ ⇒ q = q′ ✓; cap N ✓.
- (a): m ≤ N² = A^d = A^r ✓. Endpoints h = 0 (distinct parameters ⇒ distinct flats, p. 74) and h = d (count ≤ A^d, deg S = 1) ✓.

**Lemma 2.5** (pp. 12–13).
- Local model: F_{p,q} ≅ Λ²(C^d)* via Z ↦ (Z, y₀ − Zv₀); F_{p,q} ∩ F_{p′,q′} = {Z : Z(u+w) = u − w} (subtracting the two copies of (2.6): Z(v₀′−v₀) = y₀′−y₀ with v₀′−v₀ = (u+w)/2, y₀′−y₀ = (u−w)/2) ✓. Parameter [u+w : u−w] ∈ 𝒬_loc since (u−w)·(u+w) = |u|² − |w|² = 0 ✓; v = u+w ≠ 0 by genericity of R (finitely many proper closed conditions R w₀ ≠ −u on connected SO(d)) ✓.
- Distinctness: "proportional parameters give (u′,w′) = λ(u,w). Since the vectors are real and nonzero, λ is real; uniqueness of a selected partner in its projective direction first gives u′ = u, then λ = 1" ✓ (projective direction identifies ±, so this is right even for λ < 0).
- (i): product of Prop 2.3 degree-⌊A⌋ homogeneous direction separators; vanishes at every other neighbour because u′ ≠ u forces [u′] ≠ [u] (≤ 1 partner per projective direction) ✓. Pruning keeps substars, so separators persist (p. 11) ✓.
- (ii): polarization (u_i−w_i)·(u_j+w_j) + (u_j−w_j)·(u_i+w_i) = 2(u_i·u_j − w_i·w_j) — recomputed ✓. Real Gram equality ⇒ well-defined linear isometry on span(u_i) (real coefficients, positive definite) ⇒ extend to S ∈ O(d) ⇒ all are matches of x ↦ q + S(x−p) ✓. d ≥ 4: ≤ N ≤ A^{d−2} ✓. d = 3: the motion g has ≥ C_rich A + 1 matches, and Theorem 7.1 as stated (p. 61) covers *all* "motions satisfying k_g ≥ C_rich A … The same estimate holds with k_g = |gP ∩ Q|", both orientations; every edge inside V_g was deleted (p. 11), contradicting that the neighbours are H-edges ✓. (The matched set is non-collinear automatically: two neighbours have distinct projective directions from p.)
- (b): "Factor the polynomial on F_{p,q} into irreducible hypersurfaces … lies in a hypersurface of degree at most A. Specification (b) … applies" ✓ (C₀ ≥ 1 absorbs A ≤ C₀A).
- Use in Prop 2.6 (p. 13): f has degree ≤ D = ⌊A⌋ ≤ A; f|_F is a nonzero polynomial of degree ≤ D in the Z-coordinates (affine-linear parametrisation) ✓.

Conclusion of §2: every hypothesis of Theorem A.1 that §2 claims is met, is met, with the exponents claimed, and with C₀ depending only on d (and on the absolute C_rich when d = 3).

## 3. Objections

No FATAL objection and no mathematical GAP found in Appendix A or in the §2.4 hypothesis checks. The items below are what a hostile reader can actually hold against the text.

**C-1. COULD NOT CHECK (dependency, outside this scope) — the only quantitative input of Appendix A is Lemma 3.6.** p. 75: "the component Hilbert bounds in Lemma 3.6 are the only quantitative algebraic input." p. 76: "(A.6) H_X(m) ≤ b_n deg(X)m^k … and, if X is a component of a system whose equations have degrees at most m, then H_X(m) ≥ a_n deg(X)m^k (m ≥ 1). (A.7)" p. 77: "The second assertion is the bound at the equation degree in (3.7), applied with L = m. It permits other components of the system to have larger dimension." I checked that (A.6) is (3.5) and (A.7) is (3.7) *as stated* on pp. 17–18 (hypothesis "every member of this family is an irreducible component of a common locus defined by equations of degree at most L ≥ 1. Other components of that locus may have any dimension"), so the hand-off is textually exact. The truth of (3.7) (which rests on Lemma 3.3 and Chardin–Philippon [7, Cor. 3] + erratum [8]) is the algebra referee's job. If (3.7) failed, C_n in Theorem A.2 and hence every constant of Appendix A would fail. Sanity: (A.7) is not absurd — a k-dimensional component of a degree-≤m system has degree ≤ m^{n−k} (Bézout for components), so a_n deg X m^k ≤ a_n m^n, consistent with dim C[x]_{≤m} ≍ m^n/n!.

**C-2. COSMETIC — symbol overloading.** U is the rank-(s₀+1) bundle of (A.18) and also "U = E/Cv" on p. 86; B is the bundle (A.15) and the barrier B_h on p. 90; C is a constant and the map "C : A_* → U*/B_* ≃ H_*^*" (p. 86); c₁ is a Chern class and the constant "c₁ > 4C + 4" (p. 90); q is the Lemma-A.4 separator, "q = dim(A_* ∩ H_*)" (p. 86), the quadratic form q₀ (p. 87) and the minimal-degree generator (p. 89); P is the prime ideal (p. 78), the gcd P(τ) (p. 81) and the sample 𝒫. I checked each occurrence in context; none causes a wrong inference.

**C-3. COSMETIC/UNCLEAR (exposition) — Prop A.7 tangent constraint, p. 86.** "At general points its differential has rank at most dim V = n − 1. Hence (A.28) has rank less than r for general D and general λ." This needs F_λ ⊄ Sing V for general λ, which holds because the incidence over Λ is irreducible and maps dominantly onto V (so the preimage of Sing V is a proper closed subset and misses the fibre over a general λ). Not stated; true.

**C-4. COSMETIC/UNCLEAR (exposition) — Lemma A.6, p. 80.** "Rank conditions which vanish generically vanish on all of V; excluding the nonzero minors consequently controls all remaining fibers." Correct by semicontinuity of rank (minors of size > generic rank vanish on irreducible V; a nonvanishing generic-size minor fixes the rank on Ω), but stated in one line at a load-bearing step (it is what makes the solution set of (A.12) a graph over Ω or over Ω × A¹ uniformly).

**C-5. UNCLEAR (attribution, not mathematics) — §1.1 p. 1 and p. 75 vs TYZ.** The paper says TYZ provide "close antecedents for … the recovery of actual families of contained flats from tangent data … [26, Sections 3–6 and 10.2–10.3]" and that "the controlled-ruling strategy and the isotropic exception are closely related to … [26, Sections 5–6]". Accurate as attribution. Two facts a reader should know, both verified in TYZ v1: (1) TYZ's general Cayley–Monge–Salmon-for-flats (their Thm 5.4) depends on their Thm 4.1(3), which TYZ prove only in codimension ≤ 2 ("In Section 4.2 we prove (3) for varieties of codimension at most 2. The full proof is more challenging technically so we defer it to a companion paper [56]"). Appendix A does **not** use it: Lemma A.5 proves a weaker statement (new equations g_i of degree O_n(max deg f_i) with independent differentials, no product control), and A.5's two-case split makes that sufficient because the exceptional polynomial H only needs degree O(K_hA). I checked Lemma A.5 line by line (below). (2) TYZ §10.2–10.3 (curves and cones in C³, trisecants) are not used anywhere in Appendix A.

**C-6. COSMETIC — Lemma 2.5's d = 3 sentence "a collection with at least C_rich A neighbors would, together with the center, violate the survivor property".** The isometry S extending u_i ↦ w_i is non-unique when the u_i span < 3 dimensions; the argument works for any extension because Theorem 7.1's deleted family is *all* motions with k_g ≥ C_rich A, of both orientations (p. 61, p. 10). Not said, but no gap.

## 4. Citation table (scope: Appendix A and §2.4)

| Cited | Paper's claim | Source says (quote) | Verdict |
|---|---|---|---|
| Walsh [27, Thm 1.3] (arXiv 1811.07865v2) | p. 75: "We prove Walsh's approximate complete-intersection theorem"; Thm A.2: V ⊂ A^n irreducible, codim c > 0 ⇒ nonconstant f₁..f_c ∈ I(V), V a component of Z(f), Π deg f_i ≤ C_n deg V | "Theorem 1.3. Let V ⊆ C^n be an irreducible variety of dimension d. Then V is an irreducible component of Z(f₁, …, f_{n−d}) for some polynomials f_i with Π_{i=1}^{n−d} deg(f_i) ≲_n deg(V)." | MATCH (paper proves it, does not import it; proof checked) |
| Walsh [27, Def 2.2] | p. 76: δ_i = smallest t s.t. every component of Z(I_{≤t}(V)) containing V has codim ≥ i | "δ_i(V) stand for the minimal integer δ for which we can find a finite set of polynomials g₁, …, g_t … of degree at most δ such that V ⊆ Z(g₁, …, g_t) and the highest dimension of an irreducible component of Z(g₁, …, g_t) containing V is equal to n − i." | MATCH (equivalent: using all of I_{≤t} gives ≤ n−i; Krull lets a subset hit exactly n−i) |
| Walsh [27, Lemma 5.3] | "construction of compatible cuts follow[s]" | Lemma 5.3: P₁..P_{n−d} with "the maximal dimension of an irreducible component of Z(P₁, …, P_i) containing V is n − i", degrees (δ₁(V), …, δ_{n−d}(V)) | MATCH (Lemma A.3 is the same construction, phrased via all components having codim exactly i) |
| Walsh [27, proof of Lemma 3.5] | "comparison of restriction spaces appears in the proof" | "We claim there is some 1 ≤ j ≤ r such that I(V)_{≤m} = I(V_j)_{≤m}." (under m < δ_{s+1}) | MATCH ((A.4)) |
| Walsh [27, Thm 5.5] | "Walsh obtains a corresponding prefix degree estimate for his chosen cuts" | "every irreducible component W of Z(P₁, …, P_m) having dimension n − m and containing V has degree ∼_n Π_{i=1}^m δ_i(V)" | MATCH (paper proves the lower half (A.5) for any compatible choice) |
| Walsh [28, §1.1, D_m] (arXiv 1906.05843v2) | p. 75: normalise #flats in V by deg V "following Walsh's concentration parameters" | "D_m(T) = max { deg(T_W)/deg(W) : dim(W) = m } … a typical family of l-dimensional varieties in K^n satisfies D_m(T) ∼ deg(T)^{(m−l)/(n−l)}" | MATCH (normalisation only; note A^h = |𝒫|^{h/r} is exactly Walsh's "typical" scale with n−l = r, m−l = h) |
| TYZ [26, §§5–6] (arXiv 2608.14454v1) | p. 75: controlled rulings and isotropic exception "closely related" | Thm 5.4 (CMS for flats): "Γ₁,…,Γ_ℓ … rules V; … polynomial g of degree O_φ(δ(V)) … if L_{v,θ} ⊆ V … either (v,θ) ∈ Γ₁ ∪ ⋯ ∪ Γ_ℓ or v ∈ Z(g)"; Thm 6.1: "#{(p,q) ∈ P×P : F⁺_pq ⊆ V} ≲ N^{2(d−3)/3} deg V"; Cor 6.6: hypersurface ruled with dim Γ ≥ 6 ⇒ "Λ = F^Phy_ρ for some ρ ∈ E⁺ ⊔ E⁻"; Thms 6.2/6.7: deg Λ ≤ deg V, ≤ C deg V | MATCH as attribution. Lemma A.6 ≈ TYZ Thm 5.4 specialised to flats z + K_v; Prop A.7 ≈ TYZ Thms 6.2/6.7 + Cor 6.6 generalised from e = 4 to all e (different proof: Segre classes instead of linear projection; tangent-space isotropy + rigidity instead of TYZ Lemmas 6.4–6.5). Thm A.1(a) at e = 4 reproduces TYZ Thm 6.1's exponent: N^{2h/3} = A^h. Nothing imported. |
| TYZ [26, §2.6] (context, not cited in App. A) | — | "for d ≥ 4 it may be possible to perform a computation similar to the argument in Section 6 … Unfortunately, it is out of reach of our current techniques to prove this bound with a linear dependence on deg V for any i > 0." and "the desired bound on D¹₃(F) is simply false due to the presence of rich rigid motions of the opposite orientation" | Theorem A.1 is precisely the i = 0 (containment) case, which TYZ flag as within reach; the paper never claims any i > 0 statement. The TYZ d = 3 obstruction reappears as the j = 1 planes of the local model (improper isometries, I + S singular), which is why hypothesis (ii) and Thm 7.1 are needed. |
| TYZ [26, Thm 4.1(3)] (relevance check) | not used | "(3) the Jacobian of f₁, …, f_r has full rank … In Section 4.2 we prove (3) for varieties of codimension at most 2 … defer it to a companion paper [56]" | NOT USED (see C-5) — no dependence on unpublished material |
| Stacks 00OQ | R = C[x]_P regular local (p. 78) | "A polynomial algebra in n variables over a field is a regular ring." (regular ring = all localizations at primes regular) | MATCH |
| Stacks 00NQ | regular ⇒ CM | "… In particular R is Cohen-Macaulay." | MATCH |
| Stacks 02JN | parameter sequence regular; initial segments height i | "x₁,…,x_c is a regular sequence ⇔ dim(R/(x₁,…,x_c)) = dim(R) − c" | MATCH |
| Stacks 00NO | gr(R_u) ≅ Sym (p. 79) | "The graded ring ⊕ m^n/m^{n+1} is isomorphic to the graded polynomial algebra κ[X₁,…,X_d]." | MATCH |
| Stacks 00NA | heights of initial segments (p. 88) | "dim(R) = dim(R_p) + dim(R/p)" (CM local) | MATCH |
| Fulton [14] Thm 12.3, Ex 12.3.1, Ex 12.3.7(ii)–(iii); §3.1, Ex 3.1.1; §§1.4, 2.3, 2.5, 3.1–3.3 | isolated Bézout with multiplicities; multiplicity = length for CM; lines convention; proper pushforward / projection formula; s_t = c_t^{−1} on singular base | — | COULD NOT FETCH (book). The facts as *used* are standard and I checked the conventions independently: with Fulton's s_i(E)∩α = p_*(c₁(O(1))^{e+i}∩p*α), a line bundle L gives s_t(L) = 1/(1 + c₁(L)t), so (A.23) with s_t = c_t^{−1} is the right sign; the e = 3 case of (A.25) gives s₁ = ℓ, i.e. deg Λ = d_Γ deg V, the classical "ruled surface of degree d ↔ ruling curve of degree d in the Klein quadric". |
| Hartshorne [17] | generic "standard facts" (p. 78) | — | COULD NOT FETCH (book); no specific statement relied on |
| Lemma 3.1 (internal) | separators of degree O(M) | p. 15: "Each p ∈ P has a polynomial s_p of degree at most 2(M − 1) such that s_p(p) = 1, s_p(q) = 0" | MATCH |
| Theorem 7.1 (internal) | d = 3 deletion supplies the local cap | p. 61: "absolute constants C_rich, K_rich … If M ≤ A, then the motions satisfying k_g ≥ C_rich A form a finite set … The same estimate holds with k_g = |gP ∩ Q|" | MATCH as used (truth of Thm 7.1 = motions scope) |
| Prop 2.3 (internal) | homogeneous degree-⌊A⌋ direction separators; ≤ 1 partner per projective direction | p. 10: "each selected star admits homogeneous separators of degree D … A selected star has at most one partner in any projective direction" | MATCH as used (truth = reduction scope) |

## 5. Constant-dependency table (scope)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Status |
|---|---|---|---|---|---|
| C₀ (input of Thm A.1) | Lemma 2.4: absorbs sep. degree 4(M−1)/A ≤ 4, cap N/A^{d−1} ≤ 1, |𝒫|/A^d ≤ 1 ⇒ C₀ = 4. Lemma 2.5: max(2, C_rich) (d = 3), 2 (d ≥ 4) | d; C_rich (absolute) | hypotheses (i), (ii), (a)/(b) | N, M, A, δ, the sequence | ✓ (needs M ≤ A *eventually* only) |
| C = C(e, C₀) in (A.2) | A.5 closure: R_h ≤ B_h | e, C₀ | Lemma 2.4 (C a_h A^h in Prop 2.6), Lemma 2.5 (CA^{d−1}) | A, |𝒫|, V, description degrees | ✓ verified |
| a_n, b_n | (A.6),(A.7) from Lemma 3.6 | n (if Lemma 3.6 is right) | Thm A.2 | — | dependency (C-1) |
| γ_n ≤ min{1, a_n/(2^n b_n)}; C_n = γ_n^{−n} | p. 77 | n | (A.9), (A.31), (A.33) | — | ✓ arithmetic checked |
| L = O_n(1) ≥ length_R(R/J) | (A.9)–(A.10) | n (via C_n) | Lemma A.5 degree bookkeeping | V, D | ✓ |
| O_n(D) in Lemma A.5 | p. 79 | n, L; linear in D (E_{u+1} ≤ D + (L−1)(uE_u)) | Lemma A.6 | V | ✓ |
| deg H = O_e(D), #incidences O_e(1), fibre size ≤ deg_τ G | Lemma A.6 | e | A.5 case 1 | V, A | ✓ |
| d_Γ ≤ C_e (=1 if j = 1) | (A.21) | e | (A.22),(A.26) | V | ✓ |
| deg Λ ≤ d_Γ deg V | (A.26) | e | A.5 case 1 | — | ✓ (Segre identity + nonnegativity checked symbolically) |
| C_{e,C₀} (Lemma A.4) | C_a = C₀C_{a−1} + 1 | e, C₀ | j = 0 incidences | A | ✓ |
| K_{r−1} ≥ max(2, C₀+1), K_h = κK_{h+1}; c₁ > 4C+4; κ > 4Cc₁; B₀ ≥ max(1,C₀); B_h = c₁K_hB_{h−1} | p. 90 | e, C₀ | (A.32)–(A.35) | A, |𝒫|, V | ✓ all three barrier inequalities re-derived |
| D = K_hA (variable) | A.5 case 1 | K_h, A | Lemma A.5/A.6 | — | enters only as deg H ≤ C_eK_hA with C_e independent of K_h ✓ |
| C_rich, K_rich | Thm 7.1 | absolute | Lemma 2.5 d = 3 cap | rate of M/A → 0 (stated p. 61) | as used ✓ |

No constant in Appendix A depends on N, M, the sequence, δ, a window, or a rate; Appendix A has no sequence at all. The only sequence-dependent input in §2.4 is "M ≤ A eventually", which needs no rate.

## 6. Real vs complex crossings

Appendix A is entirely over C (p. 74: "varieties are reduced complex algebraic varieties"). The crossings are all in §2.4 and all check:
1. Real parameters are points of the complex quadric 𝒬; (A.2) counts them on complex V — no real-dimension claim is made.
2. Hypothesis (ii) must hold for **every complex** P^r ⊂ 𝒬, not only "real" ones. The proofs only use that real representatives lying in a complex totally isotropic subspace have B = 0, which is a real identity (B bilinear, real inputs). ✓
3. Gram ⇒ isometry uses real coefficients and positive definiteness of the real norm (p. 13) — correct only because the u_i, w_i are real; they are. ✓
4. "Since the vectors are real and nonzero, λ is real" (p. 12). ✓
5. Separators are real polynomials regarded over C (Lemma 3.1, Prop 2.3); vanishing at real points is unaffected. ✓
6. Genericity of R: u + w ≠ 0 is finitely many proper real-algebraic conditions on SO(d)(R). ✓

## 7. Exceptional parameter families (what they are, how bounded, uniformity)

- Definition: j = 1 ruling incidences (Lemma A.6 item 2): through a generic point of V a one-parameter family of flats F_λ ⊂ V. Possible only if V is a hypersurface (c = 1), because the solution space of v ∧ dg_i = 0 has dimension ≤ 2 and dimension 2 forces all dg_i ∝ a ∧ b. Checked.
- Classification (Prop A.7): Λ is a maximal isotropic P^r ⊂ 𝒬. Proof checked: (A.27) isomorphism T_λ𝒬 ≅ U ⊕ U* with tangent form β(α); rank deficiency of (A.28) for all skew D; singular-skew-pencil lemma (A_* = H_*, p odd, C skew ⇒ Θ maximal isotropic; both explicit invertible restriction matrices and the t^{p−1} coefficient checked); rigidity F_{ij} = 0 from g_{ij} = δ_{ij} by the Christoffel identity; linear span totally isotropic of dimension r+1.
- Bound: hypothesis (ii) alone, C₀A^{r−1} = C₀A^h (h = r − 1); at most O_e(1) such incidences per V. Uniform: independent of V and of the family.
- Geometric meaning (verified numerically, conc_scripts/exceptional_check.py, d = 3,4,5, both orientations): for one isometry S, the parameters [u + Su : u − Su] have pairwise B = 0 to 1e−15 and span an e-dimensional (maximal) isotropic subspace; when I + S is invertible all neighbour flats pass through the Cayley point z₁ = (I−S)(I+S)^{−1} (skew to 1e−15). So for even d and proper S they all lie in the degree-d/2 hypersurface Pf(Z − z₁) = 0, and for d = 3 improper S (I + S always singular) they lie in a plane — exactly TYZ's "opposite orientation" obstruction. Hypothesis (ii) is therefore necessary, not decorative; the paper supplies it by N ≤ A^{d−2} (d ≥ 4) and the Thm 7.1 deletion (d = 3). Globally (e = d+1) the exceptional P^d's are graphs of rigid motions (cf. TYZ Cor 6.6), capped by N.

## 8. Verified line by line vs skimmed

**Verified line by line** (every inequality and identity recomputed):
- p. 74 setup: surjectivity of evaluation onto v^⊥, dim F_λ = s₀, K_v = Λ²(E/Cv)*, distinct parameters ⇒ distinct flats (radical of K_v is Cv for e ≥ 3), maximal linear subspaces of 𝒬 are P^r.
- Theorem A.2 and Lemma A.3 in full: existence/monotonicity of δ_i (δ₁ ≥ 1), the prime-avoidance choice of f_i, codimension exactly i, (A.4) both inclusions, the induction (A.5) including the j = 0 and δ_s = 1 cases, (A.8) (δ_s = m+1 ≤ 2m), the choice of γ_n, and the final Π deg f_i ≤ γ_n^{−n} deg V. Compared with Walsh's Def 2.2, Lemma 3.5 (proof), Lemma 5.3, Thm 5.5.
- Lemma A.4 (separator induction, C_a recursion).
- Lemma A.5: m-primarity of J, generic-projection model of R, [K:F] = deg V, splitting over F̄, (A.9), (A.10), regular-system induction, Jacobian-adjugate vector fields (δ_α g_i = 0 identically: J₀ adj(J₀) J_t = Δ J_t), descent of the residue functionals to m_u/m_u² and their spanning of the dual, order-b leading form and polarization in characteristic 0, g_{u+1} ∈ P with independent conormal, degree bookkeeping O_n(D), H₀ and the germ argument for T_zV.
- Lemma A.6: v ∧ dg_i = 0 ⇔ K_v ⊂ T_zV; solution-space dimension ≤ 2 and c = 1; normal forms (A.13); the B_α basis (degree ≤ 2 in v); first test, gcd/squarefree/discriminant step, second test R_α, P₂ sheets, tangency ⇒ flows ⇒ containment of whole flats, coverage of every flat meeting Ω, fibre = F_λ ∩ Ω, dim Λ = h + j.
- Prop A.7: (A.14) ranks s₀, n, r; (A.15)–(A.17) including ℓ = a + b; U and (A.18); (A.19), (A.20); birationality of Λ̃ → Λ; X, f and its surjectivity; generic fibre degree and multiplicity one; (A.22); (A.23) sign convention; c_t(K)^{−1} = (1+at)^e/(1+2at); (A.24); expansion and (A.25) [sympy: identity for e = 3..8, all h ≤ e−2]; nonnegativity of c(p,u) for p ≥ u+1 [sympy, u ≤ 11] and the recursion; necessity of h ≤ r−1 (at h = r the expansion has negative coefficients, e.g. e = 4: −a³ + a²ℓ − aℓ² + ℓ³); (A.26) via nefness of a, ℓ; the j = 1 tangent constraint and linear algebra; local rigidity.
- A.5: replacement of the first equation by a minimal-degree q (height bookkeeping in C[S]_{I(V)}), (A.31); case 1 (all d_i ≤ K_hA) and (A.32); case 2 and (A.33)–(A.34), including p ≥ 1 in case (b) because deg q ≤ C₀A < K_hA, and the impossibility of case 2 for hypersurfaces in (b); (A.35); all three barrier inequalities (interior ≤ C(c₁/κ)^{i−h} < 1/4, ambient ≤ C/(c₁K_h^{r−h+1}) < 1/2, transition ≤ 2C/c₁ < 1/2); the max argument with R₀ ≤ 1 ≤ B₀ and R_r ≤ C₀ ≤ B₀; edge cases r = 2 (local d = 3) and r = 3 (global d = 3).
- §2.3–2.4: (2.6)–(2.8), parameter (2.7) on 𝒬 and the automatic last coordinate, s₀ = d(d−1)/2, both polarization identities, the Gram ⇒ isometry step, the exponent comparisons N ≤ A^{d−1}, N ≤ A^{d−2} (d ≥ 4), the codimension d−1 of neighbour flats and excess h = d−2, and the reduction of Lemma 2.5 to the "useful consequence" of (b).

**Only skimmed / not verified (and why):**
- Lemma 3.6 / Lemma 3.3 / Chardin–Philippon + erratum — consumed as (A.6)/(A.7); algebra scope (C-1). Textual hand-off checked only.
- Fulton/Hartshorne numbered locators — books not fetched; the mathematical facts were checked independently (isolated Bézout, length = multiplicity for regular sequences, projection formula, Segre-class conventions, nefness of globally generated classes).
- Prop 2.3 (independence ⇒ separators; ≤ 1 partner per direction), Lemma 3.1 beyond its displayed formula, Theorem 7.1 — other scopes; checked only that their *statements* deliver what §2.4 consumes.
- Lemma A.6's claim that all exclusion polynomials have degree O_e(D): checked at the level "bounded number of field operations on ambient fractions of degree O_e(D)"; I did not write out explicit degree constants for the Euclidean/discriminant steps.

## 9. Verdict

**HOLDS AS READ** for Appendix A in full (Theorem A.1 (a) and (b), Theorem A.2, Lemmas A.3–A.6, Proposition A.7, the A.5 closure with constants C(e, C₀)) and for the hypothesis checks that §2.4 makes when applying it (Lemma 2.4: e = d+1, r = d, setting (a); Lemma 2.5: e = d, r = d−1, setting (b)). No hidden rate, no constant depending on N, M, δ or the sequence, no real/complex slip, no citation mismatch found.

**COULD NOT CHECK**, with reason: (1) Lemma 3.6's lower bound (3.7) and its supporting Lemma 3.3 / Chardin–Philippon — the sole quantitative input of Appendix A (C-1), belongs to the algebra scope; (2) Fulton [14] / Hartshorne [17] locators — books not fetched (facts checked independently); (3) the truths of Prop 2.3 and Theorem 7.1, consumed only through their statements.

Note for the architecture: Appendix A is where the paper meets TYZ's explicitly stated obstacle, and it does so honestly — it proves only the containment (i = 0) concentration that TYZ §2.6 say is within reach, and replaces TYZ's (false for d = 3, "out of reach" for d ≥ 4) codimension-positive concentration by the local containment Lemma 2.5 inside one flat plus the rich-motion deletion. Whatever risk remains in the main theorem does not sit in Appendix A; it sits in what Appendix A consumes (Lemma 3.6) and in what consumes Appendix A (the rank comparison of Prop 2.6, which also rests on Lemma 3.6).
