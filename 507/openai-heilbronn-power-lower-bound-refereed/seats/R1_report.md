# R1 report: §2, §3 (Lemmas 3.1, 3.3, digit construction (3.5)–(3.8)), §4, §6

Seat R1, hostile referee. Paper: OpenAI, "A power improvement in the Heilbronn triangle lower bound" (25 Sep 2026).
I read the whole paper once for context, then went line by line through my sections in the LaTeX (`build/sections/02–06*.tex`), checking every formula against the printed PDF text. Equation numbers below are the printed ones. Note one numbering difference from the brief: the coefficient bound is printed as (3.9) and the two carry inequalities as (3.10)–(3.11). There is no (3.12).

Scratch scripts are in `/tmp/oaimath/191/seats/R1_work/`. Each ran under `ulimit -v 4000000; timeout 900`.

## Bottom line

I found no FATAL issue and no GAP in §2, §3 (3.1, 3.3, (3.5)–(3.8)), §4 or §6. Every step I was asked to press on holds as written. The inequality directions are right, and the constants claimed absolute really are absolute. The objections below are all EXPOSITION. Numerical checks were run wherever a statement allowed one, and none came close to a violation. The Lemma 4.3 tail bound is attained with equality in one small case, which shows it is sharp, not wrong.

My sections depend on two results I did not referee in full:
- **Prop 5.3, first bound** (W(A) ≪ 1 for affinely independent residues; used in the t ≠ 0 case of Prop 6.3). I spot-checked it: the affine group is transitive on ordered affinely independent triples, conditioning on 𝒜 costs at most a factor 2 because |𝒜| ≥ q³/2, and W ≤ 2q⁶/((q³−1)(q³−q)) = O(1).
- **Prop 7.1** (the t = 0 case of Prop 6.3). This belongs to other seats.

---

## §2 Lattice counts

### Lemma 2.1: holds
- Lower bound: det⟨v_i⟩ ≤ ∏λ_i by Hadamard, and it is an integer multiple of det L.
- Upper bound: a nonzero lattice vector in Q whose last nonzero coordinate is j has length² < Σ_{i≤j} λ_i²/s ≤ λ_j², and it lies outside span(v_1..v_{j−1}). That contradicts the greedy choice of v_j. The Q/2 packing then gives vol(Q/2) = s^{−s/2}∏λ_i ≤ det L.
- Index ≤ s^{s/2}.
- The greedy lengths equal Minkowski's successive minima, though the paper never needs this.

### Lemma 2.2: holds
- First part: L₀ = ℤv₁ + ℤv₂. The parallelograms attached to the points have diameter ≤ λ₁+λ₂ ≤ 2R, are disjoint within each coset, and lie inside a disk of radius 3R. Summing over [L:L₀] cosets gives 9πR²/det L.
- Second part: it is used only for L itself, in balls centred at 0, and that is the only way the paper uses it.

### Lemma 2.3: holds
det Λ = det(Λ ∩ y^⊥) · (g/|y|), via the split surjection v ↦ y·v/g.

### Lemma 2.4: holds
**Setup.**
- u₂×u₃ = a·y gives |y| ≤ R₂R₃.
- μ₁ ≤ R₃ because u₃ ∈ L_y is nonzero; μ₂ ≤ R₂ because u₂, u₃ are independent vectors of length ≤ R₂.
- The u₁ solutions form a translate of L_y (or are absent), so there are ≤ C R₁²/|y| of them. This needs R₁ ≥ μ₂, which holds.
- The bound is independent of t: t ≠ 0 is used only to make u₂, u₃ independent. Divisibility a | t is ignored, which is legitimate for an upper bound.

**Case μ₂ ≤ R₃.** Σ_{|y|≤R₂R₃} |y|^{−3} ≪ log(2R₂R₃) ≤ 2 log(2R₁). Correct.

**Case μ₂ > R₃**, checked step by step.
- **|y| ≍ UZ.** Lemma 2.1 with s = 2 and det L_y = |y| (Lemma 2.3, y primitive) give UZ/2 ≤ |y| ≤ μ₁μ₂ < 4UZ.
- **At most C·U⁴Z² normals per group.**
  - The shortest z ∈ L_y is primitive and |z| ∈ [U,2U), so there are O(U³) choices for z.
  - y ∈ L_z with |y| < 4UZ.
  - In L_z: ν₁ ≥ 1 and ν₁ν₂ ≤ 2|z| < 4U, so ν₂ < 4U ≤ 4UZ. Lemma 2.2 therefore applies at radius 4UZ and gives ≤ C(4UZ)²/|z| ≤ 16C·UZ² normals per z.
- **All eligible u₃ lie on one line.** Since |u₃| ≤ R₃ < μ₂, u₃ ∈ ℤv₁. The shortest line is unique: two independent shortest vectors would force μ₂ = μ₁ ≤ R₃. So there are at most 1 + 2R₃/μ₁ ≤ 3R₃/U choices.
- **Per-group bound.** C·U⁴Z² · R₁²/(UZ) · R₂²/(UZ) · R₃/U = C·R₁²R₂²R₃U ≤ C(R₁R₂R₃)², using U ≤ μ₁ ≤ R₃.
- **Number of groups.** U ranges over powers of 2 in [1, R₃] and Z over powers of 2 in [1, R₂]; Z ≤ μ₂ ≤ R₂ and U ≥ 1 because μ₁ ≥ 1. That is O(log(2R₃)·log(2R₂)) ≤ O((log 2R₁)²) groups.
- **The constant** is absolute and uniform in t and the radii, as claimed.

**Numerical check** (`lem24.py`, `lem24b.py`). I brute-forced #{(u₁,u₂,u₃): |u_j| ≤ R_j, det = t} for t = 1..40 or 1..60 over 22 radius triples, from (3,3,3) to (40,3,1), (14,14,1) and (24,6,2).
- count/(R₁R₂R₃)² stays between 85 and 275 throughout, i.e. bounded.
- The maximum over t is reached at divisor-rich t (2, 4, 6, 12). That is the expected σ-type singular-series effect, bounded by log log and absorbed by the log² factor.
- The ratio to the full stated bound falls as the radii grow, e.g. 18.1 → 12.5 → 9.1 along R₁ = 10, 20, 40 with R₂ = 3, R₃ = 1.

> EXPOSITION (2.4-a): "There are O(log(2R₃)log(2R₂)) groups". This is correct but wasteful: the per-group bound C·R₁²R₂²R₃U sums geometrically over U (total ≤ 2C(R₁R₂R₃)²), so this case needs only log(2R₂). Nothing propagates from it.

### Prop 2.5: holds
- **m = |det V|/I ≤ 3^{3/2}.** This is the index statement of Lemma 2.1. Since m is an integer, m ≤ 5.
- **The Cramer step.** The paper writes:
  > "|α_j| ≤ X∏_{i≠j}λ_i/|det V| ≤ 3^{3/2} X/λ_j"
  - The first inequality is Hadamard applied to V with row j replaced by u.
  - The second needs ∏λ_i ≤ 3^{3/2}|det V|. That follows from Lemma 2.1's upper bound ∏λ_i ≤ 3^{3/2}·det Λ = 3^{3/2}·I, together with |det V| = m·I ≥ I.
  - So the direction is correct. The paper does not display this chain. **EXPOSITION (2.5-a).**
- **The map A ↦ mAV⁻¹.**
  - Rows of AV⁻¹ are the α-vectors, which lie in m⁻¹ℤ³, so Q is integral.
  - The map is injective because V is invertible.
  - det Q = m³t/det V ≠ 0. If it is not an integer the count is 0.
- **Column radii.** Column j of Q has entries ≤ m·3^{3/2}X/λ_j, so its length is ≤ 9m·X/λ_j ≤ 45·X/λ_j, and C₀ = 45 works.
  - R₁ ≥ R₂ ≥ R₃ because λ₁ ≤ λ₂ ≤ λ₃.
  - R₃ ≥ C₀ ≥ 1 because λ₃ ≤ X. This is where that hypothesis is used.
  - R_j ≤ C₀X because λ_j ≥ 1.
  - R₁R₂R₃ ≤ C₀³X³/I because ∏λ ≥ det Λ = I.
- **Conclusion.** Lemma 2.4 then gives C(log 2X)²X⁶/I², with an absolute constant since X ≥ 2.

**Numerical check** (`prop25.py`). I took five sublattices: ℤ³; {v₃ ≡ 0 mod 8}; ℤ×4ℤ×16ℤ (λ = 1, 4, 16, very anisotropic); and two index-25/27 congruence lattices. Counting matrices with rows in Λ, |row| ≤ X and det = t gave max_t count/(X⁶/I²) between 0.98 and 274. These are bounded, consistent constants.

---

## §3 Norm polynomial, digits, obstruction

### Lemma 3.1: holds
- **Coefficients in F_r.** σ(𝒩) = ∏_{j=1}^{d} σ^j(𝒟) = 𝒩 because σ^d = id on K, so every coefficient is Frobenius-fixed.
- **Evaluation.** At F_r-points, σ^j(𝒟)(U) = 𝒟(U)^{r^j}, which gives the norm.
- **Skew-symmetry.** A transposition flips the sign of 𝒟, hence of each conjugate. With d odd the product flips sign.
- **Monomial form.**
  - Every monomial of 𝒩 is m_p(X¹)m_q(X²)m_s(X³) by tri-homogeneity of degree d.
  - M = C(4d−1, d) is the right count: degree-d monomials in 3d variables.
  - Coefficients with a repeated index satisfy c = −c, so they vanish because r is odd.
  - Under π ∈ S₃, c_{(p,q,s)∘π⁻¹} = sgn(π)·c_{pqs}. Each orbit {p<q<s} therefore contributes exactly c_{pqs}·det[m_p; m_q; m_s](X¹, X², X³).
  - No division by 3! occurs, so the argument works for r = 3.

**Symbolic check** (`lem31.py`). I computed 𝒩 = 𝒟·σ(𝒟)·σ²(𝒟) exactly for d = 3, r = 3 and r = 5, in the polynomial basis of F_{r³}.

| r | d | monomials in 𝒩 | nonzero c_pqs | (out of T) |
|---|---|---|---|---|
| 3 | 3 | 179,910 | 29,985 | C(165,3) = 735,130 |
| 5 | 3 | 241,122 | 40,187 | C(165,3) = 735,130 |

In both cases:
- every coefficient lies in F_r;
- 𝒩 is homogeneous of degree d in each group;
- there are 0 repeated-index terms;
- the full S₃ sign rule holds term by term;
- Σ c_{pqs}·det(m_p, m_q, m_s) reproduces 𝒩 coefficient for coefficient;
- (3.4) holds on 40 random label triples: the value equals Nm(Vandermonde), is nonzero for distinct labels and zero for a repeated label.

The trivial d = 1 cases also pass.

### Digit construction (3.5)–(3.8): holds
- **Positions (3.6).** i_a ∈ [0, T−1], j_a ∈ [0, T²−T], ℓ_a ∈ [1, T²], and k−1 = T². Each position map is injective.
- **Matching (3.7).** a + Ta′ = (T+1)a″. Reducing mod T gives a = a″, and then a′ = a″. I also verified it exhaustively for all T < 40.
- **Residue classes.** L = r¹⁰ with r | L gives exactly r⁹ digits per residue class, including class 0.
- **Units.** L < B, so the lowest digit is nonzero mod the prime B and every entry is a unit of R_h.
- **Coprimality.** B > L > r, so B ≠ r, and B ≠ q.

### Lemma 3.3: holds
- **(3.9).** For each u, each of the 6 permutations and each choice of the first two positions, the third position is determined, giving ≤ 6k²L³.
- **γ_{k−1}.**
  - Row-multilinearity gives F(Y) = Σ_{v₁,v₂,v₃} Y^{v₁+v₂+v₃}·det(row₁ at v₁; row₂ at v₂; row₃ at v₃).
  - An undesignated (i, v_i) makes a whole row ≡ 0 mod r.
  - By (3.7) and injectivity of the position maps, the survivors are exactly the T matched triples.
  - The matched triple a has residue matrix (f_{ia}(X(ξ_j)))_{i,j}, so γ_{k−1} ≡ 𝒩(X(ξ₁), X(ξ₂), X(ξ₃)) ≢ 0 mod r.
- **Carries (3.10)/(3.11).**
  - B is an integer > 100k²L³, so B−1 ≥ 100k²L³ and A₀/(B−1) ≤ 3/50.
  - That gives |S_C| ≤ (3/50)(h−1) < h/2, and |S_C| ≥ B^{k−1} − (3/50)(B^{k−1}−1) = (47B^{k−1}+3)/50 > τ.
  - Every other representative has absolute value > h − h/2 > τ.
- **The statement is deterministic.** It holds for every digit choice meeting the residue requirements, which is what Cor 6.4 needs.

**Toy check** (`lem33.py`). I used T ∈ {1,2,3,4}, r ∈ {3,5,7}, L ∈ {r, r²}, the true position scheme, the true B > 100k²L³, and arbitrary prescribed residues; one third of the trials used repeated-label columns. Over 2,100 random digit matrices:
- (3.9) held every time;
- γ_{k−1} ≡ Σ_a det(ρ_{·a·}) mod r every time;
- S_C ≡ det C mod h with |S_C| < h/2 every time;
- there were 0 cases with nonzero target and a representative in [−τ, τ]; the minimum of |rep|/τ was 1.9995.

---

## §4 Orbits and divisor moment

### Lemma 4.1: holds
- **Reduction.** This is the local-ring Smith reduction, and the zero-block case b = e = k is handled.
- **Minors.** The minor ideal is GL-invariant and equals B^b·R_h, which gives the b ≥ j criterion and the invariance of b.
- **Index.** |row span| = h·(h/D)·(h/E) = h³/I, including when e = k (E = h as an integer, E·R_h = 0).
- **Containment.** E·R_h³ ⊆ the row span because D | E, and right multiplication by Q preserves it.

### Lemma 4.2: holds
- **Stabilizer.** H = P·Stab(diag(1,D,E))·P⁻¹. Column 1 is e₁ exactly; columns 2 and 3 differ from e₂, e₃ by entries in Ann(D) and Ann(E), of sizes D and E (size h = E when e = k). So |H| ≤ D³E³.
- **Determinant image when e = k.**
  - E = 0 in the ring, so diag(1,1,u) fixes Δ for every unit u. That gives φ(h) = (1−1/B)E distinct determinants, and the ratio |det H|/|R_h^×| = E/h.
  - When e < k there are exactly E units u ≡ 1 mod B^{k−e}, giving ratio ≥ E/h as well.
- **Orbit–stabilizer.** |O| = |SL₃|/|H ∩ SL₃| = (|G|/φ(h))·(|det H|/|H|) = |GC|·|det H|/|R_h^×|. Exact.
- **Order of G.** |G| ≥ (21/64)h⁹.
- **Uniformity.** Fibres of G ↦ GC are cosets of the stabilizer, so GC is uniform on the orbit.

**Numerical check** (`orbit.py`). I ran BFS orbit enumeration under the elementary generators of SL₃ for C = diag(1, B^b, B^e) over ℤ/4, ℤ/8, ℤ/9 and ℤ/25, for every (b, e) type whose orbit has at most 3 million elements (18 cases).
- The BFS orbit size equalled |SL₃|/|Stab_SL₃(Δ)| exactly in every case. The stabilizer was enumerated independently.
- The bound c₀h⁸/(D³E²) held with ratio between 2.00 and 3.02.
- |H| ≤ D³E³ and |det H| ≥ (1−1/B)E held in every case; e.g. h = 9, b = 1, e = 2 gives |H| = 13,122 ≤ 19,683 and |det H| = 6 = (1−1/B)E.

### Lemma 4.3 and (4.6)–(4.8): hold
- **Conditioning.** Condition on column 1 and on C₁₂, C₁₃. If b ≥ j, every 2×2 minor vanishes mod B^j. C₁₁ is a unit, so the minors on rows {1,i}, columns {1,v} give C_{iv} ≡ C_{i1}C₁₁⁻¹C_{1v} mod B^j. The right-hand sides are fixed by the conditioning.
- **Digit pinning is exact.** Digits lie in [1, L] ⊂ [0, B−1], so Σ_{u<j} d_u·B^u is the base-B expansion, lies in [0, B^j−1], and the residue mod B^j determines the j low digits uniquely. This includes j = k.
- **Independence when labels repeat.** The four entries (2,2), (2,3), (3,2), (3,3) use disjoint digit draws that are independent of the conditioned ones, whatever the labels. This is true by construction: fresh digits per column.
- **Each congruence** has probability 0 or (r/L)^j.
- **The event is contained in the intersection of the four congruences**, so (4.5) holds.
- **(4.6).** Follows from the telescoping identity B^b = 1 + Σ_j(B^j − B^{j−1})·1_{b≥j}.
- **θ.** θ = B·r⁴/r⁴⁰ ≤ 200k²r³⁰·r⁻³⁶ = 200k²r⁻⁶.
- **(4.7) and (4.8).** Conditional on labels, the digits are independent and uniform with exactly r⁹ choices each.

**Numerical check** (`lem43.py`, `lem43max.py`).
- **Exact enumeration** over all digit configurations for (B,k,r,L) = (5,2,2,4), (11,2,2,4), (7,1,3,6), (13,1,2,6) with 12 prescriptions each, including all-zero and repeated-label prescriptions, plus (7,2,2,6). Nothing came close: 49 of 49 runs within the bound, e.g. P(b≥1) = 2.73e−2 vs 6.25e−2 and P(b≥2) = 4.7e−4 vs 3.9e−3. E[D] ≤ 1/(1−θ) held throughout.
- **Exhaustive over all residue prescriptions** for k = 1 and (B,r,L) ∈ {(5,2,4), (7,2,6), (7,3,6), (11,2,4)}: no violation. For B = 7, r = 3, L = 6 with every residue equal to 2, P(b ≥ 1) = 1/16 = (r/L)⁴ exactly. The bound is sharp, which confirms the "probability either zero or (r/L)^j" step is exactly attained, not merely loose.

---

## §6 Sampling

### Shared randomness: handled correctly
- G_h is shared by all samples and is independent of V, of every label and digit, and of the lifts. V is independent of everything else.
- In Lemma 6.2, after conditioning on one triple's labels and digits:
  - A mod h = G_h·C, with one G_h for all three columns, which is exactly why A mod h is uniform on the orbit O_C;
  - A mod q has three independent uniform draws from V given V;
  - the lifts are independent and uniform given the residues.
- Probability of a fixed A is (1/|O|)·(W(A)/q⁹)·(hq/N)⁹ = h⁹W(A)/(N⁹|O|). Checked, including repeated aux residues: P = P(w ∈ V)/s³ still holds.
- The paper never uses independence between different triples. §8 uses only linearity of expectation.

### Lemma 6.1: holds
- Columns in the box have length < √6·N.
- Ordered proportional pairs number ≤ 6N²·Σ_{|z|≤√6N}|z|⁻² ≪ N³.
- Conditional on all residues and shared choices, the two lifts are independent and uniform on (N/(hq))³ points each, giving ≤ CN³·(hq)⁶/N⁶.

### Prop 6.3, case t ≠ 0: holds
- 0 < |t| ≤ τ < h < q, so det A ≢ 0 mod q. The rank mod q is 3, so the columns are linearly, hence affinely, independent, and Prop 5.3 gives W ≪ 1.
- Rows of A mod h lie in rowspan(G_h·C) = rowspan(C), so the rows of A lie in Λ_C.
- Row lengths are < 2√3·N < 4N.
- λ₃(Λ) ≤ E because E·e₁, E·e₂, E·e₃ ∈ Λ; and E ≤ h < 4N.
- Prop 2.5 with X = 4N then gives (log 2N)²N⁶/I².
- "Projections pairwise distinct" is not needed for t ≠ 0.

### Cor 6.4: holds
- For distinct labels the conditional probability is 0 by Lemma 3.3: det A ≡ det C mod h has no representative in [−τ, τ].
- Only one t ∈ [−τ, τ] can occur, because 2τ ≤ B^{k−1} < h.
- **Arithmetic checked:** (h⁹/N⁹)·(D³E²/h⁸)·(N⁶/(D²E²)) = h·D/N³.
- E[D·1_F] = E_labels[1_F·E(D | labels)] ≤ 2·Pr(F) ≤ 6r^{−d}, by (4.7), valid for every fixed label triple including repeated labels.
- The final constant is absolute once r ≥ r₀(k), where r₀(k) is the threshold making 200k²r⁻⁶ ≤ 1/2.

---

## Hidden-dependence audit (brief item 7)

- §2 constants are absolute: 9π in Lemma 2.2, C₀ = 45 in Prop 2.5, and the Lemma 2.4 constant.
- c₀ = 21/64 is absolute for every prime B.
- Lemma 4.3 is an exact inequality with no constant. (4.7) needs only r ≥ r₀(k), and it is stated that way.
- 𝒩, the f_{ia} and the basis depend on r; the paper says so explicitly, and nothing downstream uses their size.
- Cor 6.4's ≪ is absolute for r ≥ r₀(k).

I found no constant that silently depends on r, B, k or the labels.

## Context only: §8 consumes my results correctly

This is outside my sections and not binding.
- (8.2)–(8.3) arithmetic: the first term is r·τ^{−1/2}·(hq)^{−9}. The second is (log 2N)²·(h/τ)·r^{2−d} with h/τ ≤ 3B = O_k(r³⁰), giving O_k((log r)²·r⁻⁹).
- The exponent α = 1 + 30β = 45435k + 16 is right.
- The every-n interpolation (Bertrand prime r ∈ (m, 2m] with two-sided bounds n ≤ n_r ≤ C_k·n, then deleting points) reads correctly to me.

## Corroboration, not relied on

OpenAI's Lean contains statements matching three of my lemmas:
- `Anisotropic.anisotropic_count` matches Lemma 2.4, with explicit constant 35721000π³/(log 2)².
- `fixed_det_count` and `integer_fixed_det_count` match Prop 2.5.
- `Section04Orbit.slOrbit_lower_bound` matches Lemma 4.2 with exactly 21/64·h⁸/(D³E²).

I compiled nothing.

---

**VERDICT: HOLDS AS READ** (§2; §3 Lemmas 3.1, 3.3 and (3.5)–(3.8); §4; §6 including the t ≠ 0 case of Prop 6.3 and Cor 6.4; three EXPOSITION notes, no GAP, no FATAL).

**The three places I was most suspicious of, and what settled each:**

1. **Lemma 2.4, case μ₂ > R₃** (the U⁴Z² normal count, |y| ≍ UZ, the one-line claim, uniformity in t). Settled by checking each step: Lemma 2.1 at s = 2 gives UZ/2 ≤ |y| < 4UZ; the shortest z is primitive; ν₂ < 4U licenses Lemma 2.2 at radius 4UZ; μ₂ > R₃ forces a unique shortest line. Brute-force counts over 22 radius triples stay at 85–275·(R₁R₂R₃)² with no growth beyond the bounded divisor effect in t.
2. **Lemma 4.2 at e = k**, where E = h as a count but 0 in the ring, and the orbit–stabilizer identity. Settled by BFS orbit enumeration over ℤ/4, ℤ/8, ℤ/9 and ℤ/25 for every feasible (b, e). The BFS size equals |SL₃|/|Stab| exactly, and the 21/64 bound holds with margin ≥ 2.
3. **Lemma 4.3**: whether the four congruences pin exactly j digits when labels repeat, and whether (r/L)^{4j} is honest. Settled by noting digits ⊂ [0, B−1], so the base-B prefix is exact, and the four entries' digits are disjoint fresh draws. Exact enumeration found no violation in 49 prescriptions, including repeated-label ones, and an exhaustive k = 1 search over all prescriptions found the bound attained with equality (sharp, not wrong).
