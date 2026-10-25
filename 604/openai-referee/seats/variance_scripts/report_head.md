# Hostile referee report — seat `variance`

Paper: OpenAI, "The weak pinned planar distance theorem" (23 Sep 2026, 27 pp), local copy `/tmp/oaimath/604/paper.pdf`.
Scope (brief item (vi)): **§5 in full** (Lemma 5.1, its proof, the two applications and (5.8), PDF pp. 15–17) and **§6.1** ((6.1)–(6.7), PDF pp. 17–19).
Every displayed formula below was read from the rendered PDF (Read tool, pages 15–19), not from paper.txt. Quotes are verbatim from the PDF.
Seat date: 2026-10-14.

## Verdict for this scope

**HOLDS AS READ.** Lemma 5.1 is correct as stated, with the stated constant C_M = 8(M+1); every cell formula, (5.4), (5.5), (5.6), (5.7), the m ∈ {0,1} exact cancellation, the integrability bookkeeping, the doubling, both applications and (5.8) check line by line, and the exact-rational finite check passes with all six deliberately-wrong controls failing. §6.1 — (6.1) through (6.7), including (6.2) (re-derived here from (3.6) and W₂ = b* + 2A), the min inequality, the giant-nesting layer-cake identity and (6.4) with its factor 2 — also checks line by line. I found **no FATAL and no GAP**; the five objections below are COSMETIC (exposition). The verdict is **conditional on inputs outside this seat**: the additive identity (3.6) (scope iv), (4.1), Lemma 4.1 and (4.5) (scope v), (2.2) (scope ii), and Lemma 3.1/(3.4) (scope iii). Nothing in §5/§6.1 uses the characteristic-zero/Euclidean input directly: all of it is finite-population algebra plus (3.6); the Euclidean content enters only through (3.6) and the grid lemma.

## Status of each item in scope

| Item (PDF page) | Status |
|---|---|
| Lemma 5.1 statement, hypotheses (p. 15) | VERIFIED LINE BY LINE |
| k ≥ n^γ > 1 ⇒ k ≥ 2 (p. 15) | VERIFIED |
| Definition of R_B incl. B = P branch (p. 15) | VERIFIED |
| Marginals of R_B: ν and exactly α (p. 15) | VERIFIED LINE BY LINE + exact check |
| P_B − 2R_B + π: zero mass, marginals α−ν and ν−α (p. 15) | VERIFIED + exact check |
| (5.3) incl. "finite integrals" sentence and averaging over F (p. 15) | VERIFIED (uses (3.6), outside seat); see Obj. 1 |
| Three cell-probability formulas (p. 15) | VERIFIED LINE BY LINE (algebra) + exact check |
| "middle identity also holds when k = n" (p. 16) | VERIFIED |
| (5.4) | VERIFIED LINE BY LINE + exact check (400 random instances) |
| H̄, ω, "last term multiplied by ω" (p. 16) | VERIFIED + exact check |
| Large-cell bound H̄ ≥ E(p−a)² − 2(M+1)n^{−γ}a, (5.5), (5.6) (p. 16) | VERIFIED LINE BY LINE + exact check (pre-γ form) |
| Small-cell P_B(C²) ≥ ½p² on p ≥ 2/k, R_B(C²) ≤ ap, (5.7) (p. 16) | VERIFIED LINE BY LINE + exact check |
| m ∈ {0,1} exact zero; singleton p ∈ {0,1/k} (p. 16) | VERIFIED (also: formula (5.4) itself evaluates to 0 at m ≤ 1, see below) |
| Integration of (5.6)/(5.7) + (5.3) ⇒ displayed ½-bound; integrability/Tonelli (p. 16) | VERIFIED LINE BY LINE |
| Doubling ⇒ (5.1) with C_M = 8(M+1) | VERIFIED |
| B = P special case remark | VERIFIED (dead code in both applications, Obj. 2) |
| (5.2) from c < γ, W₂ ≤ W, (4.5) | VERIFIED (conditional on (4.5)) |
| Application 1: fiber laws, weights k_e/|E|, E_e µ_e = q_Y ≤ B₀α, k_e ≥ n^γ (p. 17) | VERIFIED |
| Application 2: ρ_y, d_y ≥ n^γ, weights q_Y(y), Σ q_Y(y)ρ_y ≤ q_X ≤ B₀α (p. 17) | VERIFIED |
| (5.8) | VERIFIED |
| (6.1) statement and proof skeleton (pp. 17–18) | VERIFIED LINE BY LINE |
| S(Y) = M₁+M₂−S(x_e)−h_e+L(x_e,Y)−Δ₁−Δ₂ (p. 17) | VERIFIED (from (3.5), (3.3)) |
| ⟨E|S(Y)−S(Y′)|⟩ ≤ 2⟨E_qL⟩ + O(1) = O(W₂)+O(1) (p. 17) | VERIFIED |
| (6.2) and the average formula (pp. 17–18) | VERIFIED LINE BY LINE (re-derived) + exact check; constant 2 is sharp at n = 3, false at n = 2 |
| (6.3) | VERIFIED |
| min{a₁+a₂,b₁+b₂} ≤ Σ min{a_i,b_j} and its one-line proof (p. 18) | VERIFIED + exact check |
| Giant-nesting identity {S_i > u} = P∖G_i(M_i−u) (p. 18) | VERIFIED + exact check on random hierarchies |
| (6.4) incl. the factor 2 | VERIFIED LINE BY LINE + exact check |
| Bound of RHS(6.4) to O(W₂)+o(W)+O(n^{−γ}A) (p. 18) | VERIFIED LINE BY LINE |
| A ≤ O(W₂)+o(W)+O(1) ⇒ (6.1); I(q(C²)) ≫ W | VERIFIED |
| δ-split, T(2δ) via Lemma 4.1 hypotheses, (6.5) (p. 18) | VERIFIED LINE BY LINE (conditional on Lemma 4.1) |
| w, ℓ_j, transform invariance, (6.6) (p. 19) | VERIFIED + exact check of invariance |
| (6.7), both terms, both regions (p. 19) | VERIFIED LINE BY LINE |

## Derivations (my own, written out so they can be audited)

**R_B and its marginals.** For k < n: R_B(x,y) = (1/k)(k/n)(1/(k−1)) = 1/(n(k−1)) for x,y ∈ B, x ≠ y; R_B(x,y) = (1/k)((n−k)/n)(1/(n−k)) = 1/(nk) for x ∈ B, y ∉ B; 0 otherwise. First marginal: x ∈ B gets (k−1)/(n(k−1)) + (n−k)/(nk) = 1/n + 1/k − 1/n = 1/k = ν(x). Second marginal: y ∈ B gets (k−1)·1/(n(k−1)) = 1/n; y ∉ B gets k·1/(nk) = 1/n. So the second marginal is exactly α, as the paper says (PDF p. 15: "a point y ∈ B receives mass (k−1)(1/k)(k/n)(1/(k−1)) = 1/n, and a point y ∉ B receives mass k(1/k)((n−k)/n)/(n−k) = 1/n"). (This is also exactly the Lean `mixedProb`, Variance.lean l.37.) Signed measure D = P_B − 2R_B + π: mass 1−2+1 = 0; first marginal ν−2ν+α = α−ν; second ν−2α+α = ν−α; sum 0. Against L* = b* + S*(x) + S*(y): ∫L* dD = b*·0 + Σ S*(α−ν) + Σ S*(ν−α) = 0.

**(5.3).** For any law Q on distinct pairs, Tonelli (finite sum over pairs, nonnegative integrands, countable sum over places with σ_v ≥ 0) gives I(Q(C²)) = Σ_{x≠y} Q(x,y) L*(x,y) — the same rearrangement the paper writes for Q = π in (3.7). Each of I(P_B(C²)), I(R_B(C²)), I(π(C²)) is ≤ n(n−1)W₂ < ∞ (paper: "any probability law on distinct pairs is bounded by n(n−1)π pointwise"), so linearity applies and (5.3) = ∫L* dD = 0. Averaging over the finite family is a finite sum.

**Cell probabilities and (5.4)** (b = |B∩C|, p = b/k, a = m/n):
- P_B(C²) = b(b−1)/(k(k−1)); p² − p(1−p)/(k−1) = [b²(k−1) − b(k−b)]/(k²(k−1)) = b(b−1)k/(k²(k−1)) ✓.
- R_B(C²) = p[(k/n)(b−1)/(k−1) + (m−b)/n] = pa + (p/n)[k(b−1)/(k−1) − b] = pa − (p/n)(k−b)/(k−1) = ap − (k/n)p(1−p)/(k−1) ✓ (k − b = k(1−p)). At k = n (R_B := π, C ⊂ B so b = m, p = a) the formula gives a² − a(1−a)/(n−1) = π(C²) ✓.
- π(C²) = a² − a(1−a)/(n−1) (same algebra) ✓.
- H_B = P_B − 2R_B + π = (p−a)² + (2k/n − 1)p(1−p)/(k−1) − a(1−a)/(n−1) ✓ = (5.4). Matches Lean `signedCell_formula` (Variance.lean l.304) term for term.

**Singletons.** Not only do all three pair probabilities vanish for m ≤ 1, the closed form (5.4) itself evaluates to 0 there: m = 0 trivially; m = 1, b = 0: 1/n² − (1/n)(1−1/n)/(n−1) = 0; m = 1, b = 1: (1/k − 1/n)² + (2k/n − 1)/k² − 1/n² = 0. But its *separate* terms do not vanish (e.g. −a(1−a)/(n−1) = −1/n² on every singleton), and singleton cells persist on an infinite ray of levels at every complex place, so integrating the three terms separately would be ∞ − ∞. The paper's sentence "We never integrate the separate correction terms in (5.4) over those tails" is exactly the right precaution, and the proof honours it: (5.6)/(5.7) are only used on m ≥ 2, and on m ≤ 1 the comparison is H̄ = 0 = the left integrand.

**Large cells** (m > n^{1−c}). With ε := max(1/(k−1), 1/(n−1)) ≤ 2n^{−γ} (k ≥ 2 ⇒ k−1 ≥ k/2 ≥ n^γ/2; n−1 ≥ n/2 ≥ n^γ/2): the middle term of (5.4) is ≥ −p(1−p)/(k−1) ≥ −εp (coefficient 2k/n − 1 ∈ [−1,1]); averaged ≥ −εE_F p ≥ −εMa. Last term ≥ −ωa/(n−1) ≥ −εa. So H̄ ≥ E_F(p−a)² − ε(M+1)a ≥ E_F(p−a)² − 2(M+1)n^{−γ}a ✓. (5.5): m(m−1)/(n(n−1)) ≤ m²/n² iff m ≤ n; ≥ m²/(2n²) iff 2(m−1)n ≥ m(n−1), true for m ≥ 2. m > n^{1−c} ≥ 2^{2/3} forces m ≥ 2. a > n^{−c} ⇒ n^{−γ}a = n^{−γ}a²/a < n^{c−γ}a² ≤ 2n^{c−γ}π(C²) ⇒ (5.6) ✓.

**Small cells** (2 ≤ m ≤ n^{1−c}). p ≥ 2/k ⇔ b ≥ 2; P_B(C²) = p²·(k/(k−1))·((b−1)/b) ≥ ½p² ✓. R_B(C²) = ap − (k/n)p(1−p)/(k−1) ≤ ap; E_F R_B ≤ aE_F p ≤ Ma² ≤ 2Mπ(C²) ✓. H̄ = E_F P_B − 2E_F R_B + ωπ ≥ ½E_F[p²1{p≥2/k}] − 4Mπ(C²) ✓ (5.7).

**Integration.** Put G(C) = E_F[(p−a)²1{m>n^{1−c}} + ½p²1{m≤n^{1−c},p≥2/k}] ≥ 0 and E(C) = 4(M+1)n^{c−γ}π(C²)1{m>n^{1−c}} + 4Mπ(C²)1{2≤m≤n^{1−c}} ≥ 0. Pointwise G ≤ H̄ + E on every occurrence (m ≤ 1: 0 ≤ 0). H̄ + E = (E_F P_B + ωπ + E) − 2E_F R_B is a difference of nonnegative integrands with finite I, so I(H̄ + E) = I(H̄) + I(E) = 0 + I(E) ≤ 4(M+1)n^{c−γ}W₂ + 4M·W_{2,sm} (W_{2,sm} = I(π(C²)1{|C| ≤ n^{1−c}}) from (4.5); singleton π-mass is 0). Monotonicity gives I(G) ≤ that. Doubling: (5.1) LHS ≤ 2I(G) ≤ 8(M+1)n^{c−γ}W₂ + 8M W_{2,sm} ≤ C_M(n^{c−γ}W₂ + W_{2,sm}) with C_M = 8(M+1) ✓. This is the structure of Lean `integrated_variance` (Variance.lean l.687), whose error constant 2ε(M+1)/τ with ε = 2n^{−γ}, τ = n^{−c} is the paper's 4(M+1)n^{c−γ}.

**(5.2).** n^{c−γ}W₂ ≤ n^{c−γ}W = o(W) since c < γ; W_{2,sm} = o(W+1) by (4.5) (stated to hold "before passing to either a bounded or an unbounded subsequence"); C_M is fixed (M = B₀ = 2/θ in both applications) ✓.

**Applications.** Fibers: Σ_e k_e/|E| = 1; E_eµ_e(y) = Σ_e (k_e/|E|)(1/k_e)1_{F_e}(y) = d⁻(y)/|E| = q_Y(y) ≤ B₀α(y) by (2.2); k_e ≥ n^{s−o(1)} ≥ n^γ eventually since γ < s; F_e ⊂ P∖{x_e} so B ≠ P. Incoming: edges are a set of ordered pairs, so ρ_y is uniform on d_y distinct sources; q_Y(y)ρ_y(x) = (d_y/|E|)(1/d_y) = 1/|E| = q(x,y), so Σ_{all y} q_Y(y)ρ_y = q_X and the retained subfamily is ≤ q_X ≤ B₀α; total weight ≤ 1; d_y ≤ n−1 so B ≠ P. Weights do not depend on places or grids. (5.8): Σ_{d_y<n^γ} q_Y(y) ≤ n·n^γ/|E| = n^{1+γ}/(d_n n(n−1)) = O(n^{γ−1}) with d_n → θ > 0 ✓ (it repeats (2.3)).

**§6.1, first display.** (3.5) summed over j: d₁+d₂ = M₁+M₂+L(x,y)−S(x)−S(y); on a fiber d₁+d₂ = i₁+i₂+Δ₁+Δ₂ = h_e+Δ₁+Δ₂ by (3.3); solving gives the paper's S(Y) formula ✓. In S(Y)−S(Y′) the terms M₁+M₂, S(x_e), h_e cancel (same fiber), so |S(Y)−S(Y′)| ≤ L(x_e,Y)+L(x_e,Y′)+Σ_j(|Δ_j(x_e,Y)|+|Δ_j(x_e,Y′)|). Averaging (e with weight k_e/|E|, Y ∼ µ_e gives (x_e,Y) ∼ q): E ≤ 2E_qL + 4E|Δ| at a complex place, 2E_qL at a finite place; ⟨·⟩ with Σ_{v|∞}σ_v = 1 and the grid-law independence of Lemma 3.1 (grids independent of vertex sampling) gives ≤ 2E_qL* + 4E|Δ| ≤ 2B₀W₂ + O(1) by (4.1) ✓.

**(6.2), re-derived.** π has both marginals α, so (3.6) gives W₂ = E_πL* = b* + 2A, i.e. b* = W₂ − 2A. For fixed x, (1/(n−1))Σ_{y≠x}L*(x,y) = b* + S*(x) + (nA − S*(x))/(n−1) = W₂ − 2A + S*(x)(n−2)/(n−1) + nA/(n−1) = W₂ + ((n−2)/(n−1))(S*(x) − A) ✓ (the paper's display). L* ≥ 0 (each L_j ≥ 0, σ_v ≥ 0), so S*(x) − A ≥ −W₂(n−1)/(n−2) ≥ −2W₂ for n ≥ 3 ✓. Sharpness: n = 3, S* = (0,1,1), b* = −1 gives L* ≥ 0, W₂ = 1/3, A = 2/3 and S*(1) − A = −2W₂ exactly; at n = 2 the average carries no information and S*(x) ≥ A − 2W₂ fails (S* = (0,10), b* = −10). Both are in the finite check. Lean: `point_potential_lower` (GlobalPotentials.lean l.358) with hypothesis 3 ≤ card P.

**(6.3).** ⟨ES(Y)⟩ = Σ_y q_Y(y)S*(y) ≥ A − 2W₂ (pointwise bound averaged). min{s,t} = (s+t)/2 − |s−t|/2 and Y, Y′ equidistributed: ⟨E min⟩ = ⟨ES(Y)⟩ − ½⟨E|S(Y)−S(Y′)|⟩ ≥ A − 2W₂ − O(W₂) − O(1) ✓ (all terms finite, so subtraction is legitimate).

**Min inequality.** WLOG a₁+a₂ ≤ b₁+b₂. For each i: if some b_j ≥ a_i, Σ_j min{a_i,b_j} ≥ a_i; otherwise Σ_j min{a_i,b_j} = b₁+b₂ ≥ a₁+a₂ ≥ a_i. Summing over i gives Σ_{i,j} min ≥ a₁+a₂ = min ✓. (The paper's one-liner, PDF p. 18, is this argument; the second branch uses the "first sum is smaller" hypothesis.) Lean `min_add_four` (MinPotentials.lean l.286).

**Giant nesting.** Giants are nested decreasing in r (a giant's ancestor is giant) and exist exactly on an initial ray ending at M_i. With r_z = sup{r : z ∈ G_i(r)}, S_i(z) = ∫_{r<M_i}1{z ∉ G_i(r)}dr = M_i − r_z (0 if z never leaves), so {S_i > u} = {r_z < M_i − u} = P∖G_i(M_i − u) except at the finitely many u = M_i − r_z ✓.

**(6.4).** E min{S_i(Y),S_j(Y′)} = ∫₀^∞ Pr(S_i(Y)>u, S_j(Y′)>u)du = E_e∫₀^∞ µ_e(P∖G_i(M_i−u))µ_e(P∖G_j(M_j−u))du (conditional independence given e) ≤ ½(f_i + f_j), f_i := E_e∫_{r<M_i}µ_e(P∖G_i(r))²dr. Sum over the four (i,j): ½·(2(f₁+f₂) + 2(f₁+f₂)) = 2(f₁+f₂) ✓ — the paper's factor 2 is right.

**RHS of (6.4).** For r < M_i, P∖G_i(r) is the giant-complement occurrence in C_i(r), so RHS = 2I(E_e p²·1{giant-complement}) — a sub-collection of the occurrences in (5.1)/(5.2) with nonnegative integrands, so (5.2) applies to it. Three regions: (a) m > n^{1−c}: p² ≤ 2(p−a)² + 2a², a² ≤ 2π(C²) ⇒ ≤ o(W+1) + 4W₂; (b) m ≤ n^{1−c}, p ≥ 2/k_e: o(W+1); (c) m ≤ n^{1−c}, p < 2/k_e: p² ≤ 2n^{−γ}p, E_e p = q_Y(C) ≤ B₀a, and I(a·1{giant-complement}) = ⟨Σ_j∫_{r<M_j}α(P∖G_j(r))dr⟩ = E_αS* = A ⇒ ≤ 2B₀n^{−γ}A ✓. Hence ⟨E min⟩ ≤ O(W₂) + o(W) + O(n^{−γ}A); with (6.3): A(1 − O(n^{−γ})) ≤ O(W₂) + o(W) + O(1), and under W → ∞ (§6's standing assumption, "o(W+1) = o(W)"), W = W₂ + A ≤ CW₂ + o(W) ⇒ W₂ ≥ W/(2C) eventually ⇒ (6.1) ✓. Then (4.1): I(q(C²)) ≥ W₂ − o(1)A ≥ c₁W − o(W) ≫ W ✓. Lean `cell_second_moment` (MinPotentials.lean l.38) is region (a)/(b)/(c) in one statement.

**(6.5).** q(C²) = E_e 1_C(x_e)µ_e(C) (all edges of a fiber share x_e). On {a ≤ δ}: p < 2δ part ≤ T(2δ) (drop a ≤ δ); p ≥ 2δ part: p ≤ p²/(2δ), and a ≤ δ ≤ p/2 ⇒ p ≤ 2(p−a) ⇒ p² ≤ 4(p−a)², so large cells ≤ (2/δ)E(p−a)², small cells (p ≥ 2δ ≥ 2/k_e once n^γ ≥ 1/δ) ≤ (1/(2δ))E p²1{p≥2/k_e}; both integrate to o_δ(W) by (5.2) ✓. Lemma 4.1 hypotheses at λ = 2δ, τ = λ^{1/3}, fixed H ≥ 1: λ < 1/2 ⇔ δ < 1/4 ✓ (stated); 2/n ≤ τ ≤ 1 for large n ✓; then T(2δ) ≪ (λ^{1/3}+λ)W₂ + λ^{1/3}A + λH + e^{−b₁H} ≤ C′δ^{1/3}W + O_{δ,H}(1), C′ depending only on B₀ and absolute constants ✓. Choose δ with C′δ^{1/3} ≤ c₂/4 where I(q(C²)) ≥ c₂W; then I(1{a>δ}q(C²)) ≥ c₂W/2 eventually, and q(C²) ≤ 1 gives I(1{a>δ}) ≫ W ✓. a ≥ δ/4 ⇒ m ≥ δn/4 ≥ 2 ⇒ π(C²) ≥ a²/2 ≥ δ²/32 ⇒ I(1{a≥δ/4}) ≤ 32δ^{−2}W₂ ✓.

**(6.6).** w(α(G)) = w(1−α(G)) = w(α(P∖G)), so Σ_{B∈Π_j(r)}w(α(B)) = Σ_{C∈C_j(r)}w(α(C)) occurrence by occurrence (including the duplicated-cell case of Figure 1: w(α(G)) + w(α(C)) = 2w(α(C)) when C = P∖G). Transformed cells have a ≤ 1/2 ≤ 1−δ, so 1{a ≥ δ} ≤ w(a) ≤ 1{a > δ/2}; ⟨ℓ₁+ℓ₂⟩ = I(w(a)) is between I(1{a>δ}) ≫ W and I(1{a≥δ/4}) ≪_δ W ✓. ℓ_j is finite: w(1) = 0 on the coarse ray and w(1/n) = 0 on the singleton ray once n > 2/δ.

**(6.7).** The integrand f(p,a) = |w(p)−w(a)| + w(a)|p−a| satisfies f(1−p,1−a) = f(p,a) (w symmetric), and ν(P∖B) = 1−ν(B), α likewise, so the original-partition integral equals the transformed-occurrence integral. On a ≥ δ/4 (m ≥ δn/4 > n^{1−c} eventually): f ≤ (2/δ + 1)|p−a| (w is 2/δ-Lipschitz); E_F|p−a| ≤ (E_F(p−a)²)^{1/2} (ω ≤ 1); Cauchy–Schwarz on the positive measure underlying I: I(1{a≥δ/4}(E_F(p−a)²)^{1/2}) ≤ I(1{a≥δ/4})^{1/2}·I(E_F(p−a)²1{m>n^{1−c}})^{1/2} = O_δ(W)^{1/2}o(W)^{1/2} = o(W) ✓. On a < δ/4: w(a) = 0, f = w(p) ≤ 1{p > δ/2}; then p − a > δ/4 ⇒ 1 ≤ 16δ^{−2}(p−a)² on large cells; 1 ≤ 4δ^{−2}p² and p > δ/2 ≥ 2/k on small cells (k ≥ n^γ); (5.2) ⇒ o(W) ✓. Valid for both families (the incoming family's ω < 1 only helps).

## Objections

1. **§5, proof of Lemma 5.1, PDF p. 15** — "Thus the signed measure P_B − 2R_B + π has total mass zero. Its first and second marginals are α − ν and ν − α, respectively, so their sum is zero. The additive overlap identity (3.6) gives I(P_B(C²) − 2R_B(C²) + π(C²)) = 0. (5.3)". The step from "zero integral against L*" (what (3.6) gives) to "I(Q(C²)) for the signed combination" needs I(Q(C²)) = E_Q L* for a general pair law Q, which the paper writes only for Q = π ((3.7): "W₂ = I(π(C²)) = E_π L*(x,y)"). The rearrangement is the identical Tonelli step (finitely many pairs, nonnegative integrands, σ_v ≥ 0) and each term is finite as the next sentence says. **COSMETIC — exposition**, not a proof gap. Fix: one sentence "for any law Q on distinct pairs, I(Q(C²)) = E_Q L* by Tonelli."

2. **§5, PDF p. 15/16** — "If B = P, define R_B = P_B = π directly" and "In the special case B = P, the signed expression and the large-cell variance are zero; the small-cell term may equal a², which is absorbed by 2π(C²) as above." Neither application ever has B = P (F_e ⊂ P∖{x_e} so k_e ≤ n−1; d_y ≤ n−1). The branch is correct (and the general proof already covers it: with R_B = π, R_B(C²) ≤ ap and P_B(C²) ≥ ½p²1{p≥2/k} still hold), just unused. **COSMETIC.**

3. **Lemma 5.1 statement, PDF p. 15** — "Let F be a finite family of probability measures ν, each uniform on a subset B ⊂ P of size k ≥ n^γ. Give the family nonnegative weights …". In the fiber application two fibers with different sources can have the same target set, hence the same ν; "family" must be read as an indexed family (multiset), not a set of measures, or the weights k_e/|E| would have to be merged. Merging is harmless (weights add, the bound is linear), and the Lean states it with an index type (`w : I → ℝ`, `B : I → Finset P`). **COSMETIC.**

4. **Notation, pp. 5, 10, 17, 18** — in-degree is d⁻(y) in §2 ("Let d⁻(y) denote the number of incoming edges at y") but d_y in §5 ("retain the targets whose incoming degree d_y is at least n^γ"), while d₋ / d₊ are the min/max depths in the proof of Lemma 3.2; (6.4) switches the coordinate index from j to i ("Σ_{i=1}^2 E_e ∫_{r<M_i} µ_e(P∖G_i(r))² dr") while i_j already denotes raw depth; "p ≥ 2/k_e" vs "p ≥ 2/k". No ambiguity in context. **COSMETIC.**

5. **§6.1, PDF p. 18** — "To bound the right side, write p = µ_e(C) and a = α(C) for a giant-complement occurrence. If |C| > n^{1−c}, use p² ≤ 2(p−a)² + 2a², the variance estimate (5.2), and a² ≤ 2π(C²)." (5.2) is a bound over all transformed occurrences; here it is applied to the sub-collection of giant-complement occurrences. Legitimate because every integrand involved is nonnegative, but unstated. Similarly "a² ≤ 2π(C²)" there tacitly uses m ≥ 2, which holds since m > n^{1−c} > 1. **COSMETIC.**

Points examined and found **not** to be problems (recorded so other seats need not redo them): the outside-branch probability (n−k)/n is what makes the second marginal *exactly* α (a wrong branch probability breaks the marginal, (5.3) and (5.4) simultaneously — see control `wrongR`); "1/(k−1) ≤ 2n^{−γ}" needs k ≥ 2, which the paper derives ("The integer k ≥ n^γ > 1 is at least two"); "1/(n−1) ≤ 2n^{−γ}" holds for every n ≥ 2 since γ < 1; the threshold m > n^{1−c} automatically gives m ≥ 2 (n^{1−c} ≥ 2^{2/3}); the singleton/empty-cell zero is exact and the paper never integrates the separately-infinite correction terms; the integrability claim "The nonnegative left-hand terms are integrable by these pointwise bounds and the integrability of H̄ and the displayed errors" is right as written; (6.2)'s hypothesis n > 2 is needed and its constant 2 is sharp; the factor 2 in (6.4) is the exact count of the four (i,j) pairs; Lemma 4.1 is applied inside its hypotheses (λ = 2δ < 1/2 by "0 < δ < 1/4"; 2/n ≤ τ = λ^{1/3} ≤ 1 for large n); the δ in (6.5) is fixed before n → ∞ ("We may thus choose δ sufficiently small once and for all, and then let n → ∞") with the O(δ^{1/3}W) constant genuinely δ-free; the o(·) terms in scope are uniform along the sequence and depend only on the fixed parameters (θ, s, c, γ, B₀, δ). Hand-wave count in scope: "The same argument will apply to the conditional law of sources arriving at a target" (§5 intro) — discharged explicitly by the second application, whose hypotheses are checked in the text; "The same variance estimate again gives o(W)" ((6.7)) — checked above; no "clearly"/"similarly"/"it follows" elsewhere in scope.

## Citation table

No external result is cited inside §5 or §6.1 (grep of the scope for "[n]" returns nothing). Internal inputs and their owners: (3.3), (3.5) [scope iii]; (3.6), W₂ = b* + 2A [scope iv]; Lemma 3.1/(3.4) first-moment bound [scope iii]; (4.1), Lemma 4.1, (4.5) [scope v]; (2.2), (2.3), k_e ≥ n^{s−o(1)} [scope ii]. My verdict is conditional on these. By-product for scope (iii): the identity (3.5) d = M + L − S(x) − S(y), with giant replacement and multiset duplication, holds exactly on 150 random nested (finite-place-type) hierarchies in my script (block B); this does not test the archimedean grid construction.

## Finite check

Script: `/tmp/oaimath/604/seats/variance_scripts/check_variance.py` (sha256 at time of run given below), exact `fractions.Fraction` arithmetic throughout except one float comparison for the n^{c−γ} combination step (tolerance 1e-12). Runtime ≈ 5 s, RSS ≈ 14 MB per run. Blocks:
- **A** (400 random instances, n ≤ 9, any k ∈ [2,n], any C incl. |C| ∈ {0,1}): R_B built from its *sampling definition*; checks total mass, first marginal = ν, second marginal = α, the three closed cell formulas, (5.4) against the brute-force signed cell mass, exact zero at m ≤ 1, zero total mass and zero marginal sum of P_B − 2R_B + π, and zero integral against a random additive kernel b* + S(x) + S(y).
- **B** (150 random nested hierarchies with giant replacement, rational levels): (3.5) exactly; and the per-place form of (5.3): ∫Σ_C D(C²)dr = E_D[d] and ∫Σ_C H_B(C)dr (formula (5.4)) = E_D[d]. (Summing E_D[d_v] over places to 0 is exactly where (3.6)/the product formula enters; ultrametric places alone cannot realize a product formula, so that summation is not simulated.)
- **C** (400 random weighted families, ω ∈ (0,1], M = max E_Fν/α): H̄ via the ω-weighted formula = H̄ via the three laws; (5.5); (5.6) in pre-γ form H̄ ≥ E_F(p−a)² − ε(M+1)a; (5.7) and its two ingredients; m ≤ 1 zero; pointwise G ≤ H̄ + E with γ = log k_min / log n and random 0 < c < min(γ, 1/3).
- **D** min inequality (5000 random nonnegative rational lists).
- **E** (6.2) and the average formula (3000 random additive L* ≥ 0, 3 ≤ n ≤ 10), plus the sharp n = 3 example.
- **F** (120 instances, two random hierarchies + random fiber family): layer-cake identity {S_i > u} = P∖G_i(M_i−u) at random u, and (6.4) exactly.
- **G** w-symmetry: original vs transformed Σ w(α(·)) per level, and f(p,a) = f(1−p,1−a) for (6.7).

Controls (each must FAIL, and does): `wrongR` (inside-branch probability (k−1)/n instead of k/n) — breaks the second marginal, the zero marginal sum, the additive-kernel integral, the R_B formula, (5.4) and the integrated per-place identity; `noexcl` (drop the p ≥ 2/k restriction in P_B(C²) ≥ ½p²) — fails on b = 1 cells; `n2` ((6.2) at n = 2) — fails; `const1` ((6.2) with constant 1 at n = 3) — fails; `diagmin` (min inequality with only diagonal terms) — fails; `dependent` ((6.4) with Y′ = Y, i.e. no conditional independence) — fails on 55/120 instances.

Note on my own harness: the first run reported 1020 failures of the check "H̄ averaged formula" on the correct code. Cause: a stale loop variable `k` (my bug) in block C, not the paper; fixed to `len(B)`, after which the correct run is clean and every control still fails.
