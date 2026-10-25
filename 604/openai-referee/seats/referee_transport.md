# Referee report — seat `transport` — §6.2–6.4 of "The weak pinned planar distance theorem" (OpenAI, 23 Sep 2026)

Scope: §6.2 (cut distances D_j^ν, formal endpoint ∞, (6.8), (6.9), fiber equation (6.10), U/V comparison, Tonelli bound,
(6.11) incl. the weight swap via (6.7)); §6.3 (tree representation of D_j, transport formula (6.12) and its proof, (6.13),
coupling chain to (6.14)); §6.4 (Lemma 6.1 and its application; brief item (vii)). Every displayed formula below was read off
the rendered PDF (pp. 17–22), not paper.txt. Dependencies from §6.1 that the scope consumes ((6.5), (6.6), (6.7)) were checked
to the extent stated in the status table.

## Verdict for this scope

**HOLDS AS READ.** I found no FATAL and no GAP in §6.2–6.4. Every step was re-derived by hand; the identities (6.8), (6.9), (6.10),
the U−V identity, the tree representation, the transport formula (6.12), the pointwise coupling inequality before (6.14) and
Lemma 6.1 (all its intermediate claims) were also checked numerically, each with a control that fails. The objections below are
COSMETIC/UNCLEAR only. Brief item (vii): YES — in the w-weighted tree every positive edge separates α-mass > δ/2 on both sides
(the edge above cell B has length (interval length)·w(α(B)), and w(α(B)) > 0 forces α(B) ∈ (δ/2, 1−δ/2)).

Conditional on: (6.5) (§6.1, SKIMMED here, other seat), (5.2) (Lemma 5.1, other seat), (3.4) (Lemma 3.1, other seat).

## Status of each item in scope

| Item (PDF page) | Status |
|---|---|
| Definition of D_j^ν(a₀,a₁), formal endpoint ∞, finiteness remark (p.19) | VERIFIED LINE BY LINE |
| (6.8) and its proof incl. ties and ±∞ (p.19) | VERIFIED LINE BY LINE + numerics (720 cases, 0 fail; asymmetric-w control fails 71/100) |
| (6.9) (p.19) | VERIFIED LINE BY LINE + numerics (720 + 800 cases, 0 fail) |
| Fiber map Z_{j′}(z)=Z_{j′}(x)+t_e/(Z_j(z)−Z_j(x)) and the difference formula (p.20) | VERIFIED — derived independently from (3.1) (below) |
| (6.10) (p.20) | VERIFIED LINE BY LINE + exact p-adic check over Q (12,000 cases) + generic complex place (7,200 cases); off-fiber controls fail |
| U(z), V(z), the bound \|U−V\| ≤ \|Δ_{j′}(y,z)\|+\|Δ_j(y,z)\|+\|Δ_j(x,z)\|, diagonal atom z=y, z=x null (p.20) | VERIFIED LINE BY LINE + numerics with the paper's random nested grids (7,200 cases, exact identity U−V = Δ_{j′}(y,z)−Δ_j(y,z)+Δ_j(x,z)) |
| Tonelli bound ∫\|Pr(U≥u)−Pr(V≥u)\|du ≤ Σ μ_e(z)\|U(z)−V(z)\| (p.20) | VERIFIED LINE BY LINE |
| Translation invariance, Lipschitz step, ⟨E_q\|D_j^{μ_e}(x,y)−D_{j′}^{μ_e}(∞,y)\|⟩ = O_δ(1) (p.20) | VERIFIED LINE BY LINE + numerics (800 cases, max ratio 0.193 ≤ 1) |
| μ_e → α swap, (6.11) (p.20) | VERIFIED LINE BY LINE (given (6.7)) |
| (6.7) proof (p.19, §6.1 but consumed here) | VERIFIED LINE BY LINE (given (6.5), (5.2)) |
| (6.6) from (6.5) (p.19) | VERIFIED (one line: 1{a>δ} ≤ w(a) ≤ 1{a≥δ/4} on transformed cells, a ≤ 1/2, δ<1/4) |
| (6.5), (6.1)–(6.4) | SKIMMED (other seat's scope); (6.5) re-derived in outline only |
| §6.3 tree: vertices = distinct cells, parent = least strict supercell, l_j(B), leaves = singletons, cut formula, total length = ℓ_j, root ↔ ∞ (pp.20–21) | VERIFIED LINE BY LINE + numerics (6,051 leaf pairs by graph path distance, 595 root distances, 60 totals; 0 fail) |
| (6.12) statement and proof (p.21) | VERIFIED LINE BY LINE + LP check (180 cases, 0 fail; signed-formula control fails 10/10); citation MATCH |
| (6.13) both estimates incl. omitted targets (p.21) | VERIFIED LINE BY LINE |
| Coupling chain and the pointwise inequality E_{α⊗3}F ≤ 2E_q\|…\| + 2E_{q_Y}T_j(ρ_y,α) + 2T_j(q_Y,α) (p.21) | VERIFIED LINE BY LINE + numerics (120 cases, 0 fail; control without the transport terms fails 10/10); identical constants in Lean `iid_transfer` |
| (6.14) (p.21) | VERIFIED |
| Lemma 6.1 statement and proof: far event, closed walk, M = ⌈16/δ⌉+1, classes, Cauchy–Schwarz, conditional independence (p.22) | VERIFIED LINE BY LINE + numerics (2,478 trees + hill-climb; every intermediate claim checked; hypothesis-violating control fails) |
| Application of Lemma 6.1 and the contradiction W ≪ o(W) (p.22) | VERIFIED LINE BY LINE |

"Hand-wave" phrases in scope (6 found, each checked): "Directly from the cell definition" (6.9) ✓; "and hence" (6.10) ✓;
"Tonelli's theorem therefore gives" ✓; "Thus (6.7), with D_j = D_j^α, yields" ✓; "This standard formula" (6.12) — with its own
proof ✓; "Thus Pr{d(X′,Y) ≤ δL/8} ≥ …" ✓. None hides a hard step.

## Independent derivations (the load-bearing steps)

**(6.10) from (3.1).** For z ∈ F_e: (Z_j(z)−Z_j(x))(Z_{j′}(z)−Z_{j′}(x)) = t_e ≠ 0 (t is symmetric under swapping the endpoints), so
Z_{j′}(z) = Z_{j′}(x) + t_e/(Z_j(z)−Z_j(x)). Subtracting the same for y:
Z_{j′}(z)−Z_{j′}(y) = t_e[(Z_j(y)−Z_j(x)) − (Z_j(z)−Z_j(x))]/((Z_j(z)−Z_j(x))(Z_j(y)−Z_j(x))) = t_e(Z_j(y)−Z_j(z))/((Z_j(z)−Z_j(x))(Z_j(y)−Z_j(x))),
exactly the PDF's display. Applying −log|·|_v (multiplicative at every place):
i_{j′}(y,z) = h_e + i_j(y,z) − i_j(x,z) − i_j(x,y). ✓ Requires z ≠ y (injectivity of Z_j), z ≠ x (x ∉ F_e), t_e ≠ 0. Valid at every
place, archimedean or not. Note: at the original real embedding Z₂ = conj(Z₁), so i₁ = i₂ and (6.10) degenerates to
i(x,z)+i(x,y) = h_e (true since both equal h_e/2); the identity has content only at the other places — which is why my numerical
check uses a p-adic place and a generic complex place where Z₁, Z₂ are not conjugate.

**U − V.** For z ∈ F_e∖{y}: U−V = d_{j′}(y,z) − d_j(y,z) + d_j(x,z) − h_e + i_j(x,y)
= Δ_{j′}(y,z) − Δ_j(y,z) + Δ_j(x,z) + [i_{j′}(y,z) − i_j(y,z) + i_j(x,z) − h_e + i_j(x,y)] = Δ_{j′}(y,z) − Δ_j(y,z) + Δ_j(x,z) by (6.10).
At z = y, U = d_{j′}(y,y) = +∞ and V = +∞ − d_j(x,y) + const = +∞. Pr(V ≥ u) = μ_e{d_j(y,z) − d_j(x,z) ≥ u − c}, c = h_e − i_j(x,y)
(= i_{j′}(x,y) by (3.3)), so ∫w(Pr(V≥u))du = D_j^{μ_e}(x,y) by (6.8) and ∫w(Pr(U≥u))du = D_{j′}^{μ_e}(∞,y) by (6.9). Hence
|D_j^{μ_e}(x,y) − D_{j′}^{μ_e}(∞,y)| ≤ Lip(w)·Σ_{z≠y} μ_e(z)(|Δ_{j′}(y,z)| + |Δ_j(y,z)| + |Δ_j(x,z)|); every pair is distinct, so
E_grids of each |Δ| ≤ ∫₀^∞ C₀e^{−b₀u}du; Δ = 0 at finite places; Σ_{v|∞}σ_v = 1 ⇒ O_δ(1) with Lip(w) ≥ 2/δ. ✓ (The Lean's
`arch_fiber_cut` proves exactly this step with explicit constant 12 for its 1-Lipschitz tent weight.)

**(6.8).** Put d₀ = d_j(a₀,a₁). The original sum at level r is nonzero only for r > d₀, where it equals w(ν(B₀(r))) + w(ν(B₁(r))),
B_i(r) = cell of a_i. The depths form an ultrametric similarity (d(a,c) ≥ min(d(a,b), d(b,c)), from nestedness), so among
d₀, d(a₁,z), d(a₀,z) the minimum is attained twice. For u > 0: d(a₁,z) − d(a₀,z) ≥ u > 0 forces d(a₀,z) = d₀ and d(a₁,z) ≥ d₀+u,
and conversely; so the event is exactly B₁(d₀+u) (no tie issue). For u < 0 the complement is {d(a₀,z) > d₀ − u}, which differs
from B₀(d₀−u) only when d₀−u is one of finitely many depth values; w(1−t) = w(t) converts. ✓ This is the only place the
symmetry of w is used in §6.2, and my asymmetric-w control (still vanishing near 0 and 1, so every integral finite) breaks (6.8)
in 71/100 random cases.

**(6.7) (consumed by (6.11), (6.13)).** Integrand |w(p)−w(a)| + w(a)|p−a| is invariant under (p,a) ↦ (1−p,1−a), so the giant
can be replaced by its complement occurrence (multiset) and Lemma 5.1's transformed cells used. On a ≥ δ/4: m ≥ δn/4 > n^{1−c};
integrand ≤ (Lip(w)+1)|p−a|; Cauchy–Schwarz on I ⊗ E_F (family mass ω ≤ 1) gives ≤ √(I(1{a≥δ/4}))·√(I(E_F(p−a)²1{m>n^{1−c}})) =
√(O_δ(W)·o(W+1)) = o(W) ✓. On a < δ/4: w(a) = 0 and w(p) ≠ 0 needs p > δ/2, so (p−a)² > δ²/16 (large cells) and p² > δ²/4 with
p > δ/2 ≥ 2/k (small cells, k ≥ n^γ → ∞) — both dominated by (5.1)'s left side ✓.

**Tree (§6.3).** For fixed place/grids, the cells containing a point form a chain decreasing in r, so each distinct cell B is a
cell exactly on one interval of levels; the distinct cells form a laminar family (≤ 2n−1 sets) whose Hasse diagram, rooted at P,
is the tree. Regrouping ∫Σ_{B∈Π_j(r)}(…)dr by distinct cell gives D_j^α(a₀,a₁) = Σ_{B≠P} l_j(B)|1_B(a₀) − 1_B(a₁)|, and the edge
above B lies on the leaf-to-leaf path iff B contains exactly one endpoint ✓. Total length = ℓ_j (P contributes w(1)·∞ = 0 as an
integral of the zero function) ✓. Singleton edges: l_j({x}) = ∫1{{x}∈Π_j(r)}w(1/n)dr over an infinite ray; it is 0 only
because w(1/n) = 0 once 1/n ≤ δ/2 (see Objection 2). Root ↔ ∞: D_j(∞,y) = Σ_{B∋y} l_j(B) = root-to-leaf distance ✓.

**Coupling chain.** With (X,Y), (X′,Y) ∼ q conditionally independent given Y: E F ≤ 2E_q|D_j(x,y) − D_{j′}(∞,y)| (triangle
inequality through D_{j′}(∞,Y)). Replace X, X′ by U, U′ via two conditionally independent copies of an optimal coupling of ρ_Y
and α: |F(X,X′,Y) − F(U,U′,Y)| ≤ D_j(X,U) + D_j(X′,U′), conditional mean 2T_j(ρ_Y,α). (U,U′) is α⊗α and independent of Y. Draw V
from the optimal (q_Y,α) coupling's conditional given Y with fresh randomness ⇒ (U,U′) ⊥ (Y,V); |F(U,U′,Y) − F(U,U′,V)| ≤
2D_j(Y,V), mean 2T_j(q_Y,α). ✓ The resulting pointwise inequality is exactly Lean's `TreeTransport.iid_transfer`
(constants 2, 2, 2), there proved by Kantorovich–Rubinstein duality on laminar families rather than couplings.

**Lemma 6.1.** E d(X,y) = Σ_e l_e·Pr(e separates X,y) ≥ (δ/2)L ✓; E d ≤ (δL/4)(1−p) + Lp ⇒ p ≥ δ/4 ✓; the DFS closed walk has
length 2L, ⌈2L/(δL/8)⌉ = ⌈16/δ⌉ ≤ M pieces, and two vertices with visits in one piece are joined by a sub-walk of length ≤ δL/8
⇒ class diameter ≤ δL/8 ✓; Pr(same class) = Σα(C_r)² ≥ 1/M (Cauchy–Schwarz over ≤ M classes) ✓; conditional independence of X
and X′ given Y ⇒ Pr(far ∧ near) ≥ (δ/4)·(1/M) ✓; difference ≥ δL/4 − δL/8 ✓. Constant δ²L/(32M) ✓.

**Application.** Edge above B positive ⇒ w(α(B)) > 0 ⇒ δ/2 < α(B) < 1−δ/2; α is uniform on the leaves, so the two sides carry
α(B) and 1−α(B), both > δ/2 ✓. Σ_j ⟨E|D_j(x,y)−D_j(x′,y)|⟩ ≥ (δ²/(32M))⟨ℓ₁+ℓ₂⟩ ≫_δ W by (6.6), while the left side is o(W) by
(6.14); W → ∞ ⇒ contradiction ✓.

## Objections

1. **§6.4, Lemma 6.1, p.22 — COSMETIC (exposition; no gap).**
   Quote: "If X, X′, Y are independent with law α, then E|d(X,Y) − d(X′,Y)| ≥ δ²/(32(⌈16/δ⌉ + 1)) L." and "Traverse the tree in a
   closed walk crossing each edge twice, of total length 2L. Partition this walk into at most M = ⌈16/δ⌉ + 1 intervals of length
   at most δL/8, and assign each vertex to an interval containing one chosen visit."
   The lemma and proof are correct. The constant is of order δ³/512 while the truth is of order δ²: the uniform k-leaf star
   (δ = 2/k) gives E|…| ≈ (0.8–1.0)·δ²L (numerics below: 0.80, 0.95, 0.995 at δ = 0.4, 0.1, 0.01), and on 2,478 random hypothesis-satisfying trees the smallest ratio
   LHS/(stated bound) was 288. A three-line proof with a better constant is the one the Lean uses
   (`TreeTransport.fluctuation_lower`): a positive-length cell C of minimal cardinality has zero internal diameter, so for
   X′, Y ∈ C (probability ≥ (δ/2)²) one has |d(X,Y) − d(X′,Y)| = d(X,Y), whose conditional mean is ≥ (δ/2)L; total ≥ (δ/2)³L.
   Fix: none needed; optional simplification.

2. **§6.3, edge lengths of singleton leaves, p.20 — COSMETIC (exposition).**
   Quote: "Give this edge length l_j(B) = ∫_ℝ 1_{B∈Π_j(r)} w(α(B)) dr." with "The points of P are singleton leaves."
   A singleton is a cell on an infinite ray, so l_j({x}) is finite (= 0) only because w(α({x})) = w(1/n) = 0, i.e. n ≥ 2/δ. The
   paper states the analogous fact once, on p.19 ("These quantities are finite for all sufficiently large n … on the final ray all
   cells are singletons, of ν-mass either 0, 1/n, or 1/k_e, so their weights vanish too"), but not where the tree is built. Same
   for the root, which needs w(1) = 0 ("since the root-cell weight is zero"). Fix: say "for n ≥ 2/δ" at the tree construction.

3. **§6.2, proof of (6.8), p.19 — COSMETIC.**
   Quote: "Nestedness implies that if d_j(a₁,z) > d₀, then d_j(a₀,z) = d₀, and conversely with the indices exchanged. Otherwise the
   two depths to z agree."
   True, but what is used is the ultrametric (isosceles) property of the sharing depth, which nestedness gives; "Otherwise the two
   depths agree" needs the case d(a₀,z), d(a₁,z) ≤ d₀ ⇒ equal, again by "minimum attained twice". One sentence would make it
   self-contained. No gap.

4. **§6.2, p.20 — COSMETIC.**
   Quote: "Tonelli's theorem therefore gives the precise bound ∫_ℝ |Pr(U ≥ u) − Pr(V ≥ u)| du ≤ Σ_{z∈F_e∖{y}} μ_e(z)|U(z) − V(z)|."
   It is an inequality (|Pr−Pr| ≤ E|1−1|, then Tonelli), not a "precise" identity; the word is harmless. Also the letter V is
   reused for four different objects in §4–§7 (V± cells, V(z), V ∼ α, V_v) — readability only.

5. **Paper vs Lean correspondence for §6.2–6.4 — UNCLEAR → informational (not a defect of the paper).**
   The Lean does not formalize this section's text verbatim. It uses (i) the weight `tent δ u = max 0 (min (u-δ) (1-δ-u))`
   (CutApproximation.lean:39; zero on [0,δ]∪[1−δ,1], 1-Lipschitz, NOT the paper's flat-top w with w = 1 on [δ,1−δ]); (ii) the
   δ³ minimal-cell fluctuation bound instead of the closed-walk Lemma 6.1 (TreeContradiction.lean:134 `δ^3*(∑ … cutLength …) ≤ …`);
   (iii) Kantorovich–Rubinstein duality on a laminar family (`signed_lipschitz_bound`) instead of optimal couplings. Steps that do
   match one-for-one: `arch_cross_defect` = the U−V identity; `arch_fiber_cut` = the O_δ(1) step before (6.11); `iid_transfer` =
   the pointwise inequality before (6.14), same constants. So a compiled Lean certifies the theorem and an equivalent route through
   §6, not the paper's particular constants in Lemma 6.1 — which I verified by hand and numerically anyway.

No other objections. In particular I checked and found correct: the formal endpoint conventions (no ∞ − ∞; z = x is μ_e-null;
z = y gives +∞ on both sides); the μ_e → α swap bound "at most ∫Σ_B|w(μ_e(B)) − w(α(B))|dr, independently of the endpoints"
(|1_B(a₀) − 1_B(a₁)| ≤ 1, also for a₀ = ∞) applied in BOTH coordinates, which (6.7) covers since it sums j = 1, 2; the omitted
incoming targets in (6.13) (every transport cost ≤ Σ_B l_j(B) = ℓ_j; q_Y-mass O(n^{γ−1}) is graph-only, so it factors out of
⟨·⟩); Lemma 5.1's hypotheses for both families (E_e μ_e = q_Y ≤ B₀α; Σ_{d_y≥n^γ} q_Y(y)ρ_y ≤ q_X ≤ B₀α; sizes ≥ n^γ; weights
independent of places/grids, total ≤ 1); the existence of the joint couplings (finite LP for each fixed hierarchy; no measurable
selection needed because the final inequality is pointwise between explicit finite sums).

## Brief item (i), restricted to this scope (characteristic-zero / Euclidean input)

§6.2–6.4 use: (6.10), an identity valid in ANY field for a fiber of a product form t = (Z₁-difference)(Z₂-difference) with Z_j
injective and t ≠ 0; Δ = 0 at finite places and (3.4) at archimedean places; Σ_{v|∞}σ_v = 1; and the inputs (6.5)–(6.7). Nothing
here uses that Z₂ = conj(Z₁) at the real embedding (at that embedding (6.10) is in fact vacuous, see above), nor anything
Euclidean. So the argument of §6.2–6.4 holds verbatim for any finite P ⊂ K² with two injective coordinate maps and nonzero products —
e.g. the Minkowski form u² − b² with Z = u ± b on sets with no two points on a common isotropic line. If the generalised statement
were false, the failure would have to lie outside this scope (§2–§5, §7: the product formula in (3.6), the subset estimate, the
nonatomic limits).

## Citation table (scope)

| Cited | Paper's claim | Source says (arXiv:1005.1699v3, 4 May 2011, pdftotext) | Verdict |
|---|---|---|---|
| [5] Evans–Matsen, JRSS-B 74(3) 2012, "Section 2, Equation (5)" | finite-tree form of T_j(ρ,α) = Σ_{B≠P} l_j(B)\|ρ(B) − α(B)\| | §2 "The phylogenetic Kantorovich-Rubinstein metric", eq. (5): "Z(P, Q) = ∫_T \|P(τ(y)) − Q(τ(y))\| λ(dy)", where "τ(x) := {y ∈ T : x ∈ [ρ, y]} … the sub-tree below x" and λ is the length measure; Z is the KR (W₁) distance, eq. (4). | MATCH (journal version not fetched; arXiv v3 numbering matches the citation). The paper also gives its own proof, so the citation is not load-bearing. Zero-length edges (pseudometric) are outside [5]'s setting but covered by the paper's direct proof. |

Internal references used in scope: (3.4) (uniform first moment of Δ) — consumed as stated; (5.2) — consumed as stated; (6.5) —
consumed as stated.

## Finite checks (scripts verbatim, outputs, failing controls)

All scripts are in /tmp/oaimath/604/seats/transport_checks/, run with `ulimit -v 2500000`, each under 5 s and under 80 MB.
sha256: lemma61_check.py 75da9a73…, scaling_probe.py 5be0e46c…, cut_tree_check.py 5fbe863c…, fiber_grid_check.py 1fa4646d….

### Check 1 — Lemma 6.1 (exact enumeration over all triples), all intermediate claims, Lean's δ³ variant

What it does: random trees (2–10 vertices, some zero-length edges, α on all vertices or on leaves only) plus perturbed stars with
small δ; δ := 2·(min side mass over positive edges) = the largest δ the hypothesis allows (the bound is increasing in δ); checks
the main inequality and s1 (E d(X,y) ≥ δL/2 ∀y), s2 (Pr(d(X,y) ≥ δL/4) ≥ δ/4), s3 (Euler-tour classes: diameter ≤ δL/8, #classes ≤ M,
Pr(near) ≥ Σα(C_r)² ≥ 1/M), s4 (Pr(far ∧ near) ≥ δ/(4M)), and the Lean bound (δ/2)³L. Then an adversarial hill-climb on lengths and
masses minimising LHS/bound. Controls: (1) hypothesis violated (2-vertex tree, masses 1−ε, ε, claimed δ = 1/2) — the checker
must reject the hypothesis and the inequality must fail; (2) a deliberately too-strong constant δL/4 must be violated.

```python
# Lemma 6.1 check (paper p.22): finite tree, nonneg edge lengths, total L, alpha prob on vertices,
# every POSITIVE edge separates alpha-mass >= delta/2 on both sides, 0<delta<1  ==>
#   E|d(X,Y)-d(X',Y)| >= delta^2 L / (32 (ceil(16/delta)+1)),  X,X',Y iid alpha.
# Exact enumeration over triples. Also checks the proof's intermediate claims and the Lean variant
# (TreeTransport.lean fluctuation_lower: eta^3 L <= E|...| with eta = delta/2).
import random, math, sys
from fractions import Fraction

def build(parent, ln):
    N = len(parent)
    ch = [[] for _ in range(N)]
    for v in range(1, N): ch[parent[v]].append(v)
    # subtree sets
    sub = [None]*N
    def dfs(v):
        s = {v}
        for c in ch[v]: s |= dfs(c)
        sub[v] = s; return s
    dfs(0)
    # distances: d(x,y) = sum_{v!=0} ln[v] * [exactly one of x,y in sub(v)]
    d = [[0]*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            d[x][y] = sum(ln[v] for v in range(1, N) if ((x in sub[v]) != (y in sub[v])))
    return ch, sub, d

def euler_tour(ch, ln):
    # closed walk from root crossing each edge twice; returns list of (time, vertex) visits
    visits = []; t = 0
    def walk(v):
        nonlocal t
        visits.append((t, v))
        for c in ch[v]:
            t += ln[c]; walk(c); t += ln[c]; visits.append((t, v))
    walk(0)
    return visits, t

def check(parent, ln, al, delta, verbose=False):
    N = len(parent)
    ch, sub, d = build(parent, ln)
    L = sum(ln[1:])
    # hypothesis
    for v in range(1, N):
        if ln[v] > 0:
            m = sum(al[x] for x in sub[v])
            if not (m >= delta/2 and 1-m >= delta/2): return ('HYP_FAILS', None)
    M = math.ceil(16/delta) + 1
    lhs = sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(N) for xp in range(N) for y in range(N))
    bound = delta**2 * L / (32*M)
    res = {'lhs': lhs, 'bound': bound, 'L': L, 'ok_main': lhs >= bound - 1e-12}
    # intermediate claims
    res['s1'] = all(sum(al[x]*d[x][y] for x in range(N)) >= delta*L/2 - 1e-12 for y in range(N))
    res['s2'] = all(sum(al[x] for x in range(N) if d[x][y] >= delta*L/4 - 1e-12) >= delta/4 - 1e-12 for y in range(N))
    visits, T = euler_tour(ch, ln)
    assert abs(T - 2*L) < 1e-9
    h = delta*L/8
    nint = max(1, math.ceil(2*L/h)) if L > 0 else 1
    assert nint <= M
    cls = {}
    for v in range(N):
        tv = next(t for (t, u) in visits if u == v)   # one chosen visit
        k = min(int(tv // h), nint-1) if h > 0 else 0
        cls.setdefault(k, []).append(v)
    diam_ok = all(d[a][b] <= h + 1e-9 for c in cls.values() for a in c for b in c)
    near = sum(al[xp]*al[y] for xp in range(N) for y in range(N) if d[xp][y] <= h + 1e-12)
    sq = sum(sum(al[v] for v in c)**2 for c in cls.values())
    res['s3'] = diam_ok and len(cls) <= M and near >= sq - 1e-12 and sq >= 1/M - 1e-12
    both = sum(al[x]*al[xp]*al[y] for x in range(N) for xp in range(N) for y in range(N)
               if d[x][y] >= delta*L/4 - 1e-12 and d[xp][y] <= h + 1e-12)
    res['s4'] = both >= delta/(4*M) - 1e-12
    res['lean'] = lhs >= (delta/2)**3 * L - 1e-12
    return ('OK', res)

def rand_tree(rng, N, leaf_only):
    parent = [0] + [rng.randrange(v) for v in range(1, N)]
    ln = [0.0] + [rng.choice([0.0, rng.random(), rng.random()*5]) for _ in range(1, N)]
    ch = [[] for _ in range(N)]
    for v in range(1, N): ch[parent[v]].append(v)
    if leaf_only:
        leaves = [v for v in range(N) if not ch[v]]
        w = {v: rng.random() for v in leaves}
        s = sum(w.values()); al = [w.get(v, 0)/s for v in range(N)]
    else:
        w = [rng.random()**2 for _ in range(N)]; s = sum(w); al = [x/s for x in w]
    return parent, ln, al

def delta_hyp(parent, ln, al):
    N = len(parent); _, sub, _ = build(parent, ln)
    etas = [min(sum(al[x] for x in sub[v]), 1-sum(al[x] for x in sub[v])) for v in range(1, N) if ln[v] > 0]
    return 2*min(etas) if etas else None

if __name__ == '__main__':
    rng = random.Random(604)
    stats = {'trees': 0, 'main': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 'lean': 0}
    minratio = float('inf'); minratio_lean = float('inf')
    for trial in range(3000):
        N = rng.randrange(2, 11)
        parent, ln, al = rand_tree(rng, N, leaf_only=(trial % 2 == 0))
        dh = delta_hyp(parent, ln, al)
        if dh is None or dh <= 1e-6: continue
        delta = min(dh, 0.999)   # largest admissible delta (bound increasing in delta)
        st, r = check(parent, ln, al, delta)
        assert st == 'OK', (parent, ln, al, delta)
        stats['trees'] += 1
        for k in ['main', 's1', 's2', 's3', 's4', 'lean']:
            stats[k] += int(r['ok_main'] if k == 'main' else r[k])
        minratio = min(minratio, r['lhs']/r['bound'])
        minratio_lean = min(minratio_lean, r['lhs']/((delta/2)**3*r['L']))
    # structured family: stars with k leaves (delta ~ 2/k, small), random lengths, near-uniform leaf masses
    for k in [4, 8, 20, 50]:
        for rep in range(5):
            parent = [0]*(k+1); ln = [0.0]+[rng.random()+0.01 for _ in range(k)]
            w = [0.0]+[1+0.2*rng.random() for _ in range(k)]; s = sum(w); al = [x/s for x in w]
            dh = delta_hyp(parent, ln, al); delta = min(dh, 0.999)
            st, r = check(parent, ln, al, delta); assert st == 'OK'
            stats['trees'] += 1
            for kk in ['main', 's1', 's2', 's3', 's4', 'lean']:
                stats[kk] += int(r['ok_main'] if kk == 'main' else r[kk])
            minratio = min(minratio, r['lhs']/r['bound']); minratio_lean = min(minratio_lean, r['lhs']/((delta/2)**3*r['L']))
    print('random trees (hypothesis satisfied at delta = 2*min side mass):', stats)
    print('min LHS/paper_bound = %.3f   min LHS/lean_bound(eta^3 L) = %.3f' % (minratio, minratio_lean))

    # adversarial hill-climb: minimise LHS/(delta^2 L) subject to hypothesis (delta = 2*min side mass)
    best = float('inf')
    for start in range(40):
        N = rng.randrange(3, 9)
        parent, ln, al = rand_tree(rng, N, leaf_only=False)
        def score(parent, ln, al):
            dh = delta_hyp(parent, ln, al)
            if dh is None or dh < 1e-3: return float('inf'), None
            delta = min(dh, 0.999)
            st, r = check(parent, ln, al, delta)
            return r['lhs']/r['bound'], r
        cur, _ = score(parent, ln, al)
        for it in range(150):
            ln2 = ln[:]; al2 = al[:]
            v = rng.randrange(1, N); ln2[v] = max(0.0, ln2[v] + rng.gauss(0, 0.5))
            u = rng.randrange(N); al2[u] = max(0.0, al2[u] + rng.gauss(0, 0.05)); s = sum(al2)
            if s <= 0: continue
            al2 = [a/s for a in al2]
            sc, r = score(parent, ln2, al2)
            if sc < cur: cur, ln, al = sc, ln2, al2
        best = min(best, cur)
    print('adversarial hill-climb: min LHS/paper_bound = %.3f (must be >= 1)' % best)

    # CONTROL 1: hypothesis violated (2-vertex tree, masses 1-eps, eps; claim delta=1/2) -> bound must FAIL
    eps = 1e-5
    parent, ln, al = [0, 0], [0.0, 1.0], [1-eps, eps]
    st, _ = check(parent, ln, al, 0.5)
    _, sub, d = build(parent, ln)
    lhs = sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(2) for xp in range(2) for y in range(2))
    b = 0.25*1.0/(32*(math.ceil(16/0.5)+1))
    print('CONTROL 1 (hypothesis violated): checker status =', st, '| LHS = %.3e < bound %.3e ?' % (lhs, b), lhs < b)
    # CONTROL 2: a deliberately too-strong constant (delta*L/4 instead of delta^2 L/(32M)) must be violated somewhere
    viol = 0
    for k in [4, 8, 20, 50]:
        parent = [0]*(k+1); ln = [0.0]+[1.0]*k; al = [0.0]+[1.0/k]*k
        dh = delta_hyp(parent, ln, al); delta = min(dh, 0.999)
        st, r = check(parent, ln, al, delta)
        if r['lhs'] < delta*r['L']/4 - 1e-12: viol += 1
    print('CONTROL 2 (fake constant delta*L/4, uniform stars k=4,8,20,50): violations found =', viol, 'of 4 (must be > 0)')
```

Output:
```
random trees (hypothesis satisfied at delta = 2*min side mass): {'trees': 2478, 'main': 2478, 's1': 2478, 's2': 2478, 's3': 2478, 's4': 2478, 'lean': 2478}
min LHS/paper_bound = 288.577   min LHS/lean_bound(eta^3 L) = 4.012
adversarial hill-climb: min LHS/paper_bound = 288.553 (must be >= 1)
CONTROL 1 (hypothesis violated): checker status = HYP_FAILS | LHS = 2.000e-05 < bound 2.367e-04 ? True
CONTROL 2 (fake constant delta*L/4, uniform stars k=4,8,20,50): violations found = 3 of 4 (must be > 0)
[2.37 s, 12868 KB]
```

Scaling probe (shows the true order is δ², not δ³):
```python
import sys, math, random
sys.path.insert(0, '.')
from lemma61_check import build, delta_hyp
def lhs(parent, ln, al):
    N=len(parent); _,_,d=build(parent,ln)
    return sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(N) for xp in range(N) for y in range(N))
for dl in [0.4, 0.1, 0.01]:
    # path a-b-c, masses delta/2, 1-delta, delta/2
    parent=[0,0,1]; ln=[0,1.0,1.0]; al=[dl/2,1-dl,dl/2]   # root a=0, b=1, c=2
    print('path3 delta=%.2f  delta_hyp=%.3f  LHS/L=%.4e  LHS/(delta L)=%.3f' % (dl, delta_hyp(parent,ln,al), lhs(parent,ln,al)/2, lhs(parent,ln,al)/(2*dl)))
    # star: centre mass 0, k leaves; one heavy leaf mass 1-delta/2... edges each must separate >= delta/2
    k=int(round(2/dl)); parent=[0]+[0]*k; ln=[0]+[1.0]*k; al=[0]+[1.0/k]*k
    dh=delta_hyp(parent,ln,al)
    print('   uniform star k=%d delta_hyp=%.3f LHS/L=%.4e LHS/(delta_hyp L)=%.3f' % (k, dh, lhs(parent,ln,al)/k, lhs(parent,ln,al)/(dh*k)))
```
```
path3 delta=0.40  delta_hyp=0.400  LHS/L=2.7200e-01  LHS/(delta L)=0.680
   uniform star k=5 delta_hyp=0.400 LHS/L=1.2800e-01 LHS/(delta_hyp L)=0.320
path3 delta=0.10  delta_hyp=0.100  LHS/L=9.0500e-02  LHS/(delta L)=0.905
   uniform star k=20 delta_hyp=0.100 LHS/L=9.5000e-03 LHS/(delta_hyp L)=0.095
path3 delta=0.01  delta_hyp=0.010  LHS/L=9.9005e-03  LHS/(delta L)=0.990
   uniform star k=200 delta_hyp=0.010 LHS/L=9.9500e-05 LHS/(delta_hyp L)=0.010
```
Reading: stars give LHS/L ≈ (0.8–1.0)·δ², so the stated δ²/(32(⌈16/δ⌉+1)) (order δ³/512) and the Lean's (δ/2)³ are both correct but
lossy by a factor ~1/δ. The bound holds on every tree tried (min margin 288×); both controls fail as they must.

### Check 2 — (6.8), (6.9), tree representation, (6.12) vs LP, the coupling inequality before (6.14)

What it does: random ultrametric depth matrices on 8–12 points (agglomerative, with ties ⇒ multiway splits); ν = α and ν = uniform
on a random subset of size ≥ 7 (fiber-like; δ = 0.3 so singleton masses ≤ δ/2). D^ν is computed from the definition (level
integral over the original partitions) and from the u-integrals (6.8)/(6.9) exactly (piecewise constant). The tree is built as in
§6.3 (distinct cells, parent = least strict supercell, l(B) = level-span·w(α(B))) and graph path distances / root distances / total
length are compared with D^α / D^α(∞,·) / ℓ. (6.12): scipy HiGHS LP optimum vs Σ l(B)|ρ(B)−α(B)| vs the level form. Coupling
chain: arbitrary joint law q on distinct pairs, arbitrary g(y), check E_{α⊗3}|D(x,y)−D(x′,y)| ≤ 2E_q|D−g| + 2E_{q_Y}T(ρ_y,α) +
2T(q_Y,α). Controls: (A) a weight that is NOT symmetric under t ↦ 1−t but still vanishes near 0 and 1 must break (6.8);
(B) the signed formula Σ l(B)(ρ(B)−α(B)) must disagree with the LP; (C) the chain without the two transport terms must be
violated (q puts each target's incoming mass on one source s(y), g(y) = D(s(y),y) ⇒ 2E_q|D−g| = 0 < LHS).

```python
# Checks for paper section 6.2-6.3 on random hierarchies (random ultrametric "sharing depths" d):
#  (6.8)  D^nu(a0,a1) := int sum_{B in Pi(r)} |1_B(a0)-1_B(a1)| w(nu(B)) dr  ==  int w(nu{z: d(a1,z)-d(a0,z) >= u}) du
#  (6.9)  D^nu(oo,y)  := int sum_B 1_B(y) w(nu(B)) dr                       ==  int w(nu{z: d(y,z) >= u}) du
#  tree:  cells as vertices, parent = least strict supercell, edge length l(B) = |levels where B is a cell| * w(alpha(B));
#         graph path distance == D^alpha, root distance == D^alpha(oo,.), total edge length == ell
#  (6.12) optimal transport cost (LP) == sum_B l(B)|rho(B)-alpha(B)|
#  (6.14) chain: E_{alpha^3}|D(x,y)-D(x',y)| <= 2E_q|D(x,y)-g(y)| + 2E_{qY} T(rho_y,alpha) + 2T(qY,alpha)
import random, math
from scipy.optimize import linprog
import numpy as np
INF = float('inf')

def make_w(delta, symmetric=True):
    def w(t):
        if symmetric: t = min(t, 1-t)
        if t <= delta/2: return 0.0
        if t >= delta: return 1.0 if (not symmetric or t <= 1-delta) else 1.0
        return (t - delta/2)/(delta/2)
    if symmetric: return w
    # control: NOT symmetric under t -> 1-t, but still 0 on [0,delta/2] u [1-delta/2,1] (all integrals finite)
    def w2(t):
        if t <= delta/2 or t >= 1-delta/2: return 0.0
        if t <= delta: return (t - delta/2)/(delta/2)
        if t <= 0.4: return 1.0
        return (1-delta/2 - t)/(1-delta/2-0.4)
    return w2

def random_ultrametric(rng, n):
    # agglomerative: clusters merge at decreasing depths; ties produce multiway splits
    clusters = [[i] for i in range(n)]
    d = [[INF if i == j else None for j in range(n)] for i in range(n)]
    depth = 10.0
    while len(clusters) > 1:
        depth -= rng.choice([0.0, rng.random(), 2*rng.random()]) if depth < 10.0 else rng.random()
        r = rng.choice([2, 2, 2, 3]) if len(clusters) >= 3 else 2
        pick = rng.sample(range(len(clusters)), r)
        merged = []
        for p in pick:
            for a in clusters[p]:
                for b in merged: d[a][b] = d[b][a] = depth
            merged += clusters[p]
        clusters = [c for k, c in enumerate(clusters) if k not in pick] + [merged]
    return d

def levels(d, n):
    vals = sorted({d[i][j] for i in range(n) for j in range(n) if i != j})
    return vals

def partition(d, n, r):
    # classes of {d >= r}
    seen = [False]*n; parts = []
    for i in range(n):
        if seen[i]: continue
        c = [j for j in range(n) if j == i or d[i][j] >= r]
        for j in c: seen[j] = True
        parts.append(frozenset(c))
    return parts

def hierarchy(d, n):
    # list of (interval_length, partition) for finite intervals (D_k, D_{k+1}], plus partitions on rays
    vals = levels(d, n)
    segs = []
    for k in range(len(vals)-1):
        segs.append((vals[k+1]-vals[k], partition(d, n, vals[k+1])))
    return vals, segs   # ray r<=vals[0]: {P}; ray r>vals[-1]: singletons

def mass(nu, B): return sum(nu[x] for x in B)

def D_cells(d, n, nu, w, a0, a1):
    vals, segs = hierarchy(d, n)
    # rays: initial ray has only P (a0,a1 both in P => 0 unless a0 = oo); final ray: singletons
    tot = 0.0
    def ind(B, a): return 0 if a is None else (1 if a in B else 0)
    P = frozenset(range(n))
    if a0 is None:   # formal endpoint oo: initial ray contributes w(nu(P)) * infinity -> must be 0
        assert w(mass(nu, P)) == 0
    for x in range(n):
        if (a0 is not None and x == a0) or x == a1:
            assert w(nu[x]) == 0, 'singleton weight must vanish on final ray'
    for length, part in segs:
        tot += length*sum(abs(ind(B, a0)-ind(B, a1))*w(mass(nu, B)) for B in part)
    return tot

def integrate_tail(vals_at, nu, w, n):
    # int_R w(nu{z: f(z) >= u}) du, f(z) in R u {+-inf}; piecewise constant between finite values
    fin = sorted({v for v in vals_at if math.isfinite(v)})
    def g(u): return w(sum(nu[z] for z in range(n) if vals_at[z] >= u))
    lo, hi = fin[0]-1.0, fin[-1]+1.0
    assert g(lo) == 0 and g(hi) == 0, 'tails must vanish'
    pts = [lo] + fin + [hi]
    tot = 0.0
    for k in range(len(pts)-1):
        mid = 0.5*(pts[k]+pts[k+1])
        tot += (pts[k+1]-pts[k])*g(mid)
    return tot

def D_u(d, n, nu, w, a0, a1):
    if a0 is None: f = [d[a1][z] for z in range(n)]
    else:          f = [d[a1][z]-d[a0][z] for z in range(n)]   # +inf at a1, -inf at a0
    return integrate_tail(f, nu, w, n)

def tree(d, n, w, alpha):
    vals, segs = hierarchy(d, n)
    P = frozenset(range(n))
    span = {}   # cell -> total level length where it is a cell (finite segments only)
    for length, part in segs:
        for B in part: span[B] = span.get(B, 0.0) + length
    cells = set(span) | {P} | {frozenset([x]) for x in range(n)}
    l = {}
    for B in cells:
        if B == P: continue
        wt = w(mass(alpha, B))
        if len(B) == 1:
            assert wt == 0; l[B] = 0.0   # infinite final ray times zero weight
        else:
            # cell persists on finite segments; it can also be P-ray? no (B != P)
            l[B] = span.get(B, 0.0)*wt
    parent = {}
    for B in cells:
        if B == P: continue
        sup = [C for C in cells if B < C]
        parent[B] = min(sup, key=len)
    return cells, parent, l, P

def path_dist(parent, l, P, u, v):
    # graph distance between tree vertices u, v
    def anc(x):
        out = [x]
        while x != P: x = parent[x]; out.append(x)
        return out
    au, av = anc(u), anc(v)
    common = set(au) & set(av)
    du = 0.0
    for x in au:
        if x in common: lca = x; break
        du += l[x]
    dv = 0.0
    for x in av:
        if x == lca: break
        dv += l[x]
    return du + dv

def transport_lp(C, rho, alpha):
    n = len(rho)
    c = np.array(C).reshape(-1)
    A = []; b = []
    for i in range(n):
        row = np.zeros(n*n); row[i*n:(i+1)*n] = 1; A.append(row); b.append(rho[i])
    for j in range(n):
        row = np.zeros(n*n); row[j::n] = 1; A.append(row); b.append(alpha[j])
    res = linprog(c, A_eq=np.array(A), b_eq=np.array(b), bounds=(0, None), method='highs')
    assert res.status == 0
    return res.fun

def rand_prob(rng, n, support=None):
    w = [0.0]*n
    for i in (support if support is not None else range(n)): w[i] = rng.random()+0.05
    s = sum(w); return [x/s for x in w]

rng = random.Random(6082)
w = make_w(0.3)
fails = {'6.8': 0, '6.9': 0, 'tree_path': 0, 'tree_root': 0, 'tree_total': 0, '6.12': 0, '6.12_levelform': 0, 'chain': 0}
counts = dict.fromkeys(fails, 0)
for trial in range(60):
    n = rng.randrange(8, 13)
    d = random_ultrametric(rng, n)
    alpha = [1.0/n]*n
    # a fiber-like law: uniform on a subset of size k >= 7 (so 1/k <= delta/2 = 0.15)
    k = rng.randrange(7, n+1); F = rng.sample(range(n), k); mu = [1.0/k if x in F else 0.0 for x in range(n)]
    for nu in (alpha, mu):
        for _ in range(6):
            a0, a1 = rng.sample(range(n), 2)
            counts['6.8'] += 1
            if abs(D_cells(d, n, nu, w, a0, a1) - D_u(d, n, nu, w, a0, a1)) > 1e-9: fails['6.8'] += 1
            y = rng.randrange(n); counts['6.9'] += 1
            if abs(D_cells(d, n, nu, w, None, y) - D_u(d, n, nu, w, None, y)) > 1e-9: fails['6.9'] += 1
    # tree representation with alpha weights
    cells, parent, l, P = tree(d, n, w, alpha)
    vals, segs = hierarchy(d, n)
    ell = sum(length*sum(w(mass(alpha, B)) for B in part) for length, part in segs)
    counts['tree_total'] += 1
    if abs(sum(l.values()) - ell) > 1e-9: fails['tree_total'] += 1
    Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
    for a in range(n):
        counts['tree_root'] += 1
        if abs(path_dist(parent, l, P, frozenset([a]), P) - D_cells(d, n, alpha, w, None, a)) > 1e-9: fails['tree_root'] += 1
        for b in range(n):
            counts['tree_path'] += 1
            if abs(path_dist(parent, l, P, frozenset([a]), frozenset([b])) - Dm[a][b]) > 1e-9: fails['tree_path'] += 1
    # transport formula (6.12)
    for _ in range(3):
        rho = rand_prob(rng, n, rng.sample(range(n), rng.randrange(1, n+1)))
        lp = transport_lp(Dm, rho, alpha)
        cutform = sum(l[B]*abs(mass(rho, B)-mass(alpha, B)) for B in l)
        levelform = sum(length*sum(w(mass(alpha, B))*abs(mass(rho, B)-mass(alpha, B)) for B in part) for length, part in segs)
        counts['6.12'] += 1; counts['6.12_levelform'] += 1
        if abs(lp - cutform) > 1e-7: fails['6.12'] += 1
        if abs(levelform - cutform) > 1e-9: fails['6.12_levelform'] += 1
    # coupling chain to (6.14): arbitrary joint law q on distinct pairs, arbitrary g(y)
    for _ in range(2):
        q = {}
        for x in range(n):
            for y in range(n):
                if x != y and rng.random() < 0.3: q[(x, y)] = rng.random()
        s = sum(q.values()); q = {k: v/s for k, v in q.items()}
        qY = [sum(v for (x, y), v in q.items() if y == yy) for yy in range(n)]
        g = [rng.choice([D_cells(d, n, alpha, w, None, yy), rng.random()*3]) for yy in range(n)]
        lhs = sum(alpha[x]*alpha[xp]*alpha[yy]*abs(Dm[x][yy]-Dm[xp][yy]) for x in range(n) for xp in range(n) for yy in range(n))
        t1 = sum(v*abs(Dm[x][y]-g[y]) for (x, y), v in q.items())
        t2 = 0.0
        for yy in range(n):
            if qY[yy] > 0:
                rho_y = [q.get((x, yy), 0.0)/qY[yy] for x in range(n)]
                t2 += qY[yy]*sum(l[B]*abs(mass(rho_y, B)-mass(alpha, B)) for B in l)
        t3 = sum(l[B]*abs(mass(qY, B)-mass(alpha, B)) for B in l)
        counts['chain'] += 1
        if lhs > 2*t1 + 2*t2 + 2*t3 + 1e-9: fails['chain'] += 1
print('checks run:', counts)
print('failures  :', fails)

# CONTROL A: non-symmetric weight (w(t) != w(1-t)): (6.8) must FAIL for some pairs
wbad = make_w(0.3, symmetric=False)
bad = 0; tot = 0; asserts = 0
for trial in range(20):
    n = rng.randrange(8, 13); d = random_ultrametric(rng, n); alpha = [1.0/n]*n
    for _ in range(5):
        a0, a1 = rng.sample(range(n), 2)
        try:
            tot += 1
            if abs(D_cells(d, n, alpha, wbad, a0, a1) - D_u(d, n, alpha, wbad, a0, a1)) > 1e-9: bad += 1
        except AssertionError:
            asserts += 1
print('CONTROL A (asymmetric w, finite integrals): (6.8) numeric mismatches = %d / %d, assertion trips = %d (mismatches must be > 0)' % (bad, tot, asserts))
# CONTROL B: wrong transport formula (signed instead of absolute imbalance) must disagree with the LP
n = 10; d = random_ultrametric(rng, n); alpha = [0.1]*n
cells, parent, l, P = tree(d, n, w, alpha)
Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
mis = 0
for _ in range(10):
    rho = rand_prob(rng, n, rng.sample(range(n), 3))
    if abs(transport_lp(Dm, rho, alpha) - sum(l[B]*(mass(rho, B)-mass(alpha, B)) for B in l)) > 1e-7: mis += 1
print('CONTROL B (signed imbalance formula): LP mismatches = %d / 10 (must be > 0)' % mis)
# CONTROL C: dropping the two transport terms from the (6.14) chain must be violated:
# q puts each target's whole incoming mass on one source s(y), g(y) = D(s(y),y) => 2E_q|D-g| = 0 but LHS > 0
viol = 0
for trial in range(10):
    n = rng.randrange(8, 12); d = random_ultrametric(rng, n); alpha = [1.0/n]*n
    Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
    src = [rng.choice([x for x in range(n) if x != y]) for y in range(n)]
    q = {(src[y], y): 1.0/n for y in range(n)}
    g = [Dm[src[y]][y] for y in range(n)]
    t1 = sum(v*abs(Dm[x][y]-g[y]) for (x, y), v in q.items())
    lhs = sum(alpha[x]*alpha[xp]*alpha[yy]*abs(Dm[x][yy]-Dm[xp][yy]) for x in range(n) for xp in range(n) for yy in range(n))
    if lhs > 2*t1 + 1e-9: viol += 1
print('CONTROL C (chain without transport terms): violations = %d / 10 (must be > 0)' % viol)
```

Output:
```
checks run: {'6.8': 720, '6.9': 720, 'tree_path': 6051, 'tree_root': 595, 'tree_total': 60, '6.12': 180, '6.12_levelform': 180, 'chain': 120}
failures  : {'6.8': 0, '6.9': 0, 'tree_path': 0, 'tree_root': 0, 'tree_total': 0, '6.12': 0, '6.12_levelform': 0, 'chain': 0}
CONTROL A (asymmetric w, finite integrals): (6.8) numeric mismatches = 71 / 100, assertion trips = 0 (mismatches must be > 0)
CONTROL B (signed imbalance formula): LP mismatches = 10 / 10 (must be > 0)
CONTROL C (chain without transport terms): violations = 10 / 10 (must be > 0)
[2.30 s, 79596 KB]
```

### Check 3 — fiber equation (6.10), U−V identity, and the O_δ(1) step with the paper's random nested grids

What it does: (a) exact over Q at p ∈ {2,3,5,7}: Minkowski-type coordinates Z₁ = u+b, Z₂ = u−b, fiber points z with
Z₁(z)−Z₁(x) = a, Z₂(z)−Z₂(x) = t/a (a random rational), −log|·|_p = v_p·log p, (6.10) checked as an identity of valuations.
(b) a complex place where Z₁, Z₂ are not conjugate (fiber built from (Z₁(z)−Z₁(x))(Z₂(z)−Z₂(x)) = t_e with complex t_e), then the
paper's grids exactly as in §3.2 (uniform orientation, ξ ~ U[0, log 2), sides e^ξ2^m, uniform shift mod l₀, nested shifts by adding
0 or l_m for m ≥ 0, reduction mod l_m for m < 0; nestedness asserted at every pair), one grid family per coordinate; checks (6.10),
U−V = Δ_{j′}(y,z) − Δ_j(y,z) + Δ_j(x,z), ∫w(μ{V≥u})du = D_j^μ(x,y) (translation + (6.8)), ∫w(μ{U≥u})du = D_{j′}^μ(∞,y) ((6.9)), and
|D_j^μ(x,y) − D_{j′}^μ(∞,y)| ≤ Lip(w)·Σ_z μ(z)(|Δ_{j′}(y,z)| + |Δ_j(y,z)| + |Δ_j(x,z)|). Controls: a point moved off the fiber must
break (6.10), in both (a) and (b).

```python
# Checks for paper section 6.2, (6.10) and the U/V comparison, with genuine random nested grids.
# (a) exact p-adic check of (6.10) over Q (Minkowski-type factorisation Z1=u+b, Z2=u-b; the identity is algebraic)
# (b) complex place where Z1, Z2 are NOT conjugate (generic embedding): Z2 on the fiber defined by
#     (Z1(z)-Z1(x))(Z2(z)-Z2(x)) = t_e ; check (6.10) with complex moduli,
#     then build the paper's random grids (random orientation, xi ~ U[0,log2), side e^xi 2^m, nested shifts)
#     and check  U(z)-V(z) = D_{j'}(y,z) - D_j(y,z) + D_j(x,z)  [Delta's], (6.8)/(6.9) via u-integrals, and
#     |D_j^mu(x,y) - D_{j'}^mu(oo,y)| <= Lip(w) * sum_z mu(z)(|Delta_{j'}(y,z)|+|Delta_j(y,z)|+|Delta_j(x,z)|).
import random, math, cmath
from fractions import Fraction
INF = float('inf')

# ---------- (a) p-adic, exact ----------
def vp(q, p):
    q = Fraction(q); assert q != 0
    a, b, v = q.numerator, q.denominator, 0
    while a % p == 0: a //= p; v += 1
    while b % p == 0: b //= p; v -= 1
    return v
rng = random.Random(1604)
bad_a = 0; tot_a = 0
for trial in range(200):
    p = rng.choice([2, 3, 5, 7])
    x1, x2 = Fraction(rng.randint(-50, 50), rng.randint(1, 30)), Fraction(rng.randint(-50, 50), rng.randint(1, 30))
    t = Fraction(rng.choice([1, -1])*rng.randint(1, 500), rng.randint(1, 50))
    fib = []
    while len(fib) < 6:
        a = Fraction(rng.choice([1, -1])*rng.randint(1, 300), rng.randint(1, 40))
        z = (x1 + a, x2 + t/a)
        if all(z[0] != w[0] for w in fib): fib.append(z)
    X = (x1, x2)
    i = lambda j, A, B: vp(A[j]-B[j], p)        # -log|.|_p = v_p * log p ; work in units of log p
    h = vp(t, p)
    for y in fib:
        for z in fib:
            if z == y: continue
            for j in (0, 1):
                jp = 1-j
                tot_a += 1
                if i(jp, y, z) != i(j, y, z) - i(j, X, z) + h - i(j, X, y): bad_a += 1
# control: move one point off the fiber -> identity must fail somewhere
ctrl_a = 0
for trial in range(50):
    p = 2; X = (Fraction(0), Fraction(0)); t = Fraction(12)
    y = (Fraction(3), Fraction(4)); z = (Fraction(4), Fraction(3) + Fraction(1, 2**rng.randint(1, 6)))  # z off fiber
    if vp(z[1]-y[1], p) != vp(z[0]-y[0], p) - vp(z[0]-X[0], p) + vp(t, p) - vp(y[0]-X[0], p): ctrl_a += 1
print('(a) p-adic exact (6.10): %d checks, %d failures | CONTROL (z off fiber): %d/50 failures (must be > 0)' % (tot_a, bad_a, ctrl_a))

# ---------- (b) complex place with random nested grids ----------
def make_grid(rng, mlo, mhi):
    th = rng.random()*2*math.pi; xi = rng.random()*math.log(2)
    l = {m: math.exp(xi)*2.0**m for m in range(mlo, mhi+1)}
    s0 = [rng.random()*l[0], rng.random()*l[0]]
    sh = {0: s0}
    for m in range(0, mhi):
        sh[m+1] = [(sh[m][a] + (l[m] if rng.random() < 0.5 else 0.0)) % l[m+1] for a in (0, 1)]
    for m in range(mlo, 0): sh[m] = [s0[a] % l[m] for a in (0, 1)]
    return th, l, sh
def cell(g, zc, m):
    th, l, sh = g
    r = zc*cmath.exp(-1j*th)
    return (math.floor((r.real - sh[m][0])/l[m]), math.floor((r.imag - sh[m][1])/l[m]))
def depth(g, za, zb, mlo, mhi):
    prev = False
    for m in range(mlo, mhi+1):
        same = cell(g, za, m) == cell(g, zb, m)
        assert not (prev and not same), 'grids not nested'
        if same and not prev: first = m
        prev = prev or same
    assert prev, 'never share'
    return -math.log(g[1][first])

def make_w(delta):
    def w(t):
        t = min(t, 1-t)
        if t <= delta/2: return 0.0
        if t >= delta: return 1.0
        return (t-delta/2)/(delta/2)
    return w
delta = 0.3; w = make_w(delta); Lip = 2/delta

def tail_integral(f, nu, n):
    fin = sorted({v for v in f if math.isfinite(v)})
    def g(u): return w(sum(nu[z] for z in range(n) if f[z] >= u))
    lo, hi = fin[0]-1, fin[-1]+1
    assert g(lo) == 0 and g(hi) == 0
    pts = [lo]+fin+[hi]
    return sum((pts[k+1]-pts[k])*g(0.5*(pts[k]+pts[k+1])) for k in range(len(pts)-1))

def D_cells(dm, n, nu, a0, a1):
    vals = sorted({dm[i][j] for i in range(n) for j in range(n) if i != j})
    tot = 0.0
    for k in range(len(vals)-1):
        r = vals[k+1]
        def cellof(a): return frozenset(z for z in range(n) if z == a or dm[a][z] >= r)
        cells = {cellof(a) for a in range(n)}
        for B in cells:
            inA0 = 0 if a0 is None else int(a0 in B)
            tot += (vals[k+1]-vals[k])*abs(inA0 - int(a1 in B))*w(sum(nu[z] for z in B))
    return tot

stats = dict(fib610=0, fib610_bad=0, UV=0, UV_bad=0, eq68=0, eq68_bad=0, eq69=0, eq69_bad=0, bound=0, bound_bad=0)
maxratio = 0.0
for trial in range(40):
    k = 10; nextra = 3; n = 1 + k + nextra
    Z1x, Z2x = complex(rng.gauss(0, 1), rng.gauss(0, 1)), complex(rng.gauss(0, 1), rng.gauss(0, 1))
    t = complex(rng.gauss(0, 1), rng.gauss(0, 1))*rng.choice([0.1, 1, 10])
    Z1 = [Z1x]; Z2 = [Z2x]
    for _ in range(k):
        a = cmath.rect(math.exp(rng.gauss(0, 1.5)), rng.random()*2*math.pi)
        Z1.append(Z1x + a); Z2.append(Z2x + t/a)
    for _ in range(nextra):
        Z1.append(complex(rng.gauss(0, 2), rng.gauss(0, 2))); Z2.append(complex(rng.gauss(0, 2), rng.gauss(0, 2)))
    x = 0; F = list(range(1, k+1)); mu = [1.0/k if z in F else 0.0 for z in range(n)]
    Z = [Z1, Z2]
    i_ = lambda j, a, b: -math.log(abs(Z[j][a]-Z[j][b]))
    he = -math.log(abs(t))
    for y in F:
        for z in F:
            if z == y: continue
            for j in (0, 1):
                stats['fib610'] += 1
                if abs(i_(1-j, y, z) - (i_(j, y, z) - i_(j, x, z) + he - i_(j, x, y))) > 1e-9: stats['fib610_bad'] += 1
    # grids: one family per coordinate
    seps = [abs(Z[j][a]-Z[j][b]) for j in (0, 1) for a in range(n) for b in range(n) if a != b]
    mlo = math.floor(math.log2(min(seps)/math.sqrt(2))) - 2
    mhi = math.ceil(math.log2(max(seps))) + 30
    G = [make_grid(rng, mlo, mhi) for _ in (0, 1)]
    dm = [[[INF if a == b else depth(G[j], Z[j][a], Z[j][b], mlo, mhi) for b in range(n)] for a in range(n)] for j in (0, 1)]
    Dl = lambda j, a, b: dm[j][a][b] - i_(j, a, b)
    for j in (0, 1):
        jp = 1-j
        for y in F:
            U = [dm[jp][y][z] for z in range(n)]
            V = [dm[j][y][z] - dm[j][x][z] + he - i_(j, x, y) for z in range(n)]
            errsum = 0.0
            for z in F:
                if z == y:
                    assert U[z] == INF and V[z] == INF
                    continue
                stats['UV'] += 1
                pred = Dl(jp, y, z) - Dl(j, y, z) + Dl(j, x, z)
                if abs((U[z]-V[z]) - pred) > 1e-9: stats['UV_bad'] += 1
                errsum += mu[z]*(abs(Dl(jp, y, z)) + abs(Dl(j, y, z)) + abs(Dl(j, x, z)))
            Djxy = D_cells(dm[j], n, mu, x, y); Djp_root = D_cells(dm[jp], n, mu, None, y)
            # (6.8) with translation: int w(mu{V>=u}) du == D_j^mu(x,y); (6.9): int w(mu{U>=u}) du == D_j'^mu(oo,y)
            stats['eq68'] += 1; stats['eq69'] += 1
            if abs(tail_integral(V, mu, n) - Djxy) > 1e-8: stats['eq68_bad'] += 1
            if abs(tail_integral(U, mu, n) - Djp_root) > 1e-8: stats['eq69_bad'] += 1
            stats['bound'] += 1
            lhs = abs(Djxy - Djp_root)
            if lhs > Lip*errsum + 1e-9: stats['bound_bad'] += 1
            if errsum > 0: maxratio = max(maxratio, lhs/(Lip*errsum))
print('(b) complex place + random grids:', stats)
print('    max |D_j^mu(x,y)-D_jprime^mu(oo,y)| / (Lip(w) * Delta-error) = %.3f (must be <= 1)' % maxratio)

# CONTROL (b): perturb one fiber point's Z2 off the fiber -> the U-V identity must fail for that point
fails = 0
for trial in range(20):
    k = 6; n = 1 + k
    Z1x, Z2x = complex(rng.gauss(0, 1), rng.gauss(0, 1)), complex(rng.gauss(0, 1), rng.gauss(0, 1)); t = complex(1, 0.5)
    Z1 = [Z1x]; Z2 = [Z2x]
    for _ in range(k):
        a = cmath.rect(math.exp(rng.gauss(0, 1)), rng.random()*2*math.pi); Z1.append(Z1x + a); Z2.append(Z2x + t/a)
    Z2[3] += 0.3*cmath.exp(1j*rng.random()*6.28)     # point 3 leaves the fiber
    Z = [Z1, Z2]; i_ = lambda j, a, b: -math.log(abs(Z[j][a]-Z[j][b])); he = -math.log(abs(t))
    y, z, x, j = 1, 3, 0, 0
    if abs(i_(1, y, z) - (i_(0, y, z) - i_(0, x, z) + he - i_(0, x, y))) > 1e-6: fails += 1
print('CONTROL (b) (one point off the fiber): (6.10) failures = %d / 20 (must be > 0)' % fails)
```

Output:
```
(a) p-adic exact (6.10): 12000 checks, 0 failures | CONTROL (z off fiber): 50/50 failures (must be > 0)
(b) complex place + random grids: {'fib610': 7200, 'fib610_bad': 0, 'UV': 7200, 'UV_bad': 0, 'eq68': 800, 'eq68_bad': 0, 'eq69': 800, 'eq69_bad': 0, 'bound': 800, 'bound_bad': 0}
    max |D_j^mu(x,y)-D_jprime^mu(oo,y)| / (Lip(w) * Delta-error) = 0.193 (must be <= 1)
CONTROL (b) (one point off the fiber): (6.10) failures = 20 / 20 (must be > 0)
[1.47 s, 12608 KB]
```

Caveat on check 3(a)'s control: it is a single deterministic off-fiber configuration repeated 50 times (shift 2^{−r}, r ∈ 1..6), so
"50/50" means "the identity fails off the fiber", not 50 independent witnesses. Check 3(b)'s control uses 20 independent random
configurations.

## Summary

§6.2–6.4 HOLD AS READ. Every step was re-derived by hand: the cut-distance identity (6.8) and its tie and ±∞ conventions, (6.9),
the fiber equation (6.10) from (3.1), the U/V comparison, the Tonelli bound, the μ_e → α swap via (6.7), the tree representation,
(6.12), (6.13), the coupling chain to (6.14), Lemma 6.1 line by line, and its application. Brief item (vii) is answered YES: a
positive edge needs w(α(B)) > 0, so both sides carry more than δ/2 of the α-mass. The only objections are cosmetic: Lemma 6.1's
constant is weak, and three phrasings need a sentence each. The result rests on (6.5), (5.2) and (3.4), which belong to other
seats.
