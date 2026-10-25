# Referee report — seat `incidence`
**Scope:** §2 in full (PDF pp. 4–11): the sequence reduction at the start of §2, Lemma 2.1, Lemma 2.2, Prop 2.3, Prop 2.4 line by line, Lemmas 2.5, 2.6 and 2.7. Also brief items (ii) and (ix), plus the parts of (i) and (viii) that concern §2.
**Read:** `paper.pdf`, PDF pp. 1–12, from the page renders (PDF page = printed page), and the final paragraph of §8 ("Proof of Theorem 1.1", p. 51, from paper.txt). Sources were downloaded to `/tmp/oaimath/167/refs/{szekely1997,clarkson1987,kuhlmann09}/`.
**Checks:** `/tmp/oaimath/167/checks/incidence/{exponents.py,wedge_entropy.py}` with outputs `*.out`. Both are reproduced verbatim below.

## Verdict for this scope

**HOLDS AS READ.** I re-derived every inequality, exponent, deletion count and constant in §2 by hand. The exponent bookkeeping was also checked by machine: 33/33 claims pass and 5/5 deliberately wrong inputs are rejected. The finite content of Lemma 2.7 was checked on explicit graphs: every check holds on graphs that satisfy the hypothesis, and they fail on a graph that violates it.

I found **no FATAL and no GAP.** I have 5 objections: 4 COSMETIC and 1 UNCLEAR that does not affect correctness. §2 is not where the paper breaks, if it breaks.

Two scope facts matter downstream:
- **(a) How D depends on a.** D ≤ [a + (2+3a)·t^{−a+o(a)} + o(a)]·log t. Generically this is attained up to the constant on the t^{−a} term, so D is genuinely of order (a + t^{−a})·log t, not smaller.
- **(b) Nothing in §2 is Euclidean-specific** beyond the algebraicity used in Lemma 2.1. The rest runs verbatim for any strictly convex norm, including Valtr's. The Euclidean input must therefore come later (§4 onwards), as the brief expects.

---

## Status of each result in scope

| Item | Status |
|---|---|
| §2 opening, sequence reduction (p. 4) | VERIFIED LINE BY LINE |
| Lemma 2.1 (algebraic specialisation) | VERIFIED LINE BY LINE (+ citation checked) |
| Lemma 2.2 (cutting) | VERIFIED LINE BY LINE (sweep, O(1+s²) count, C₀(1+l)⁶ candidates, union bound) |
| Prop 2.3 (Székely + log) | VERIFIED LINE BY LINE (+ citation checked) |
| Prop 2.4 (unbalanced piece, (2.2)–(2.9)) | VERIFIED LINE BY LINE (+ sympy exponent check) |
| Lemma 2.5 (matching labels, (2.10)) | VERIFIED LINE BY LINE |
| Lemma 2.6 (i)–(iii) and the "error factors outside integrals" remark | VERIFIED LINE BY LINE |
| Lemma 2.7 ((2.16)–(2.18)) | VERIFIED LINE BY LINE (+ exact numerical check) |
| Final "Proof of Theorem 1.1" paragraph (p. 51), quantifiers only (brief (ix)) | VERIFIED LINE BY LINE as logic. It depends on Prop 4.4, Prop 7.6 and Prop 8.1, which are NOT in my scope. |

---

## Objections

**O1. Cross-references name the wrong kind of result.** §2.3, p. 7: *"First use Theorem 2.1. … Apply Theorem 2.2 with R = t^{1−a}"*. p. 8: *"For the sequence of edge laws in Theorem 2.4"*. These are labelled Lemma 2.1, Lemma 2.2 and Proposition 2.4. Each reference points to the intended result.
- Severity: COSMETIC.
- Fix: relabel.

**O2. The j = 2 case of the sequence reduction is outside the theorem's exponent range.** p. 4: *"for each j ≥ 2, failure of a bound with exponent 4/3 − 1/j allows the constant in that bound to be chosen large enough to force a counterexample with n ≥ j. Its ordered unit-pair count is at least n^{4/3−1/j} = t^{4−3/j}."*
- For j = 2 the exponent is 5/6, outside Theorem 1.1's range 1 ≤ β < 4/3. Failure at β = 1 implies failure at 5/6, so nothing breaks.
- "Large enough to force n ≥ j" is correct but unexplained. Since u(n) ≤ n²/2 < j² for n < j, any C ≥ j² forces n ≥ j. Then u(n) > C·n^{4/3−1/j} ≥ n^{4/3−1/j} unordered pairs, so ordered pairs are at least 2·n^{4/3−1/j} = 2t^{4−3/j}.
- Passing to strictly increasing n_j keeps the exponent error 3/j → 0.
- Severity: COSMETIC. This is a true statement with an omitted one-line justification.

**O3. The last paragraph of §8 contains a redundant step.** p. 51: *"Enlarging the positive constant covers the finitely many remaining sizes n ≥ 2"*.
- The contrapositive of the reduction already gives some j and some C with u(n) ≤ C·n^{4/3−1/j} for every n, because the reduction negates "for all C there is an n". There are no remaining sizes to cover.
- The other steps are correct: raising the exponent to ≥ 1, ordered vs unordered pairs costing a factor 2, n = 0, 1 trivial, and S having a bounded or a divergent subsequence. All asymptotic statements survive passage to subsequences, because a, b, k, … are chosen along the sequence before the S-dichotomy is applied.
- Severity: COSMETIC (harmless redundancy). The quantifier structure is correct.

**O4. The Clarkson attribution describes a different argument from the one actually used.** p. 5: *"The cutting proof uses the random-sampling principle for regions with bounded defining data developed by Clarkson [5, Section 4]."*
- Clarkson's Thm 4.1 / Cor 4.2 union-bounds over regions defined by i-tuples **of the sample**. It uses the independence of the r − i non-defining draws, with bound O(r^i)(1−α)^{r−i}.
- Lemma 2.2's proof does something cruder and self-contained. It union-bounds over **all** C₀(1+l)⁶ candidate regions defined by tuples of the full family, each of which is fixed independently of the sample. That is why s carries log(2+l) rather than log s.
- The proof as written is correct and invokes nothing from [5]. The citation is attribution only and is not load-bearing.
- Severity: COSMETIC.

**O5. Lemma 2.7's rate in a is never stated.** p. 10, (2.18): *"D := D_KL(L(p,r) ‖ µ⊗µ) = o(log t)."*
- The proof yields D ≤ 2·log|P| − (1 − |Q|/|E|)·log(|E|·d_min,Q/2). In the exponents of (2.2)–(2.3) this is

  **D/log t ≤ 2(1+2a) − (1 − t^{−a+o(a)})·(2+3a) + o(a) = a + (2+3a)·t^{−a+o(a)} + o(a).**
- This bound is generically sharp in order. On random codegree-≤2 graphs at the paper's exponents, D/log t ≈ a + (1+a)·t^{−a}: measured 0.627 against the model's 0.672 at t = 60, a = 0.4; see the numerical check. So D/log t → 0 only at rate ≍ a + t^{−a}, and both a → 0 and a·log t → ∞ are needed.
- Consequence for later choices: (D/K)^{1/4} ≤ (D/log t)^{1/8} ≲ (a + 3t^{−a})^{1/8} when K = ⌈√((D+1)·log t)⌉. So §5's requirement k^{20}(D/K)^{1/4} → 0 forces roughly k ≪ (a + t^{−a})^{−1/160}. The paper's "chosen after" convention permits this.
- Not an error. Severity: UNCLEAR (implicit rate). Seats on §3–§5 should know that k must grow more slowly than a fixed tiny power of 1/(a + t^{−a}).

---

## Detailed verification notes

### Sequence reduction (p. 4) and final paragraph (p. 51) — brief item (ix)
- Negating Theorem 1.1 gives: for every β ∈ [1, 4/3) and every C there is an n with u(n) > C·n^β. Apply this with β = 4/3 − 1/j (j ≥ 3; j = 2 by monotonicity) and C = j². That gives n_j ≥ j with at least 2·n_j^{4/3−1/j} ordered pairs. Take a strictly increasing subsequence and set t = n^{1/3}: the ordered pairs number at least t^{4−3/j} = t^{4−o(1)}. ✓
- Ordered unit pairs are exactly the incidences between the point copy and the centre copy, with distance 0 excluded. ✓
- Final paragraph: assume no power saving, build the sequence, take the S-dichotomy by subsequence, exclude both branches. Hence some j and C satisfy u(n) ≤ C·n^{4/3−1/j} for all n. ✓ (See O3.)

### Lemma 2.1 (p. 4)
- The system consists of: the unit equations (polynomials over ℚ); the strict inequalities (X_{i1}−X_{j1})² + (X_{i2}−X_{j2})² > 0 for distinctness; and rational open rectangles, i.e. strict linear inequalities over ℚ.
- It has a real solution (the original configuration). Kuhlmann Thm 3.1 (K = ℚ, R₁ = ℝ, R₂ = ℝ_alg) or Thm 4.1 (R = ℝ_alg ⊆ R₁ = ℝ) gives a solution in ℝ_alg. Both allow ">" relations. ✓
- New unit pairs may appear after specialisation. Discarding them is legitimate, because every later count is a lower bound on the incidences retained. ✓
- The coordinates generate a number field (finitely many algebraic numbers). ✓

### Lemma 2.2 (pp. 5–6)
- **Auxiliary direction.**
  - For an input point p and an intersection point x ≠ p of two original circles, sharing an abscissa excludes only the two unit directions perpendicular to x − p.
  - The extremum condition e·(p−c) = ±1 has at most 4 solutions e when |p−c| ≠ 1, none when p = c, and only e = ±(p−c) when |p−c| = 1. Those are exactly "p is that extremum", which is allowed.
  - So finitely many directions are excluded. ✓
- **Sweep.**
  - A gap continues across an event abscissa iff its boundary graphs and their adjacency persist and its closed limiting vertical segment holds no event point.
  - Graphs appear or disappear only at extrema (event points) and swap order only at intersections (event points). So any gap with no event point in its closed segment has a same-boundary left neighbour, and each new piece is charged to an event point in its closed segment. ✓
  - At most O(1 + c_x) right-hand gaps touch an event point x lying on c_x sampled circles. Σ c_x over intersection points ≤ Σ 2·C(c_x, 2) ≤ 4·C(s, 2), since each pair of circles meets at most twice. Extrema contribute O(s), and an extremum on ≥ 2 circles is an intersection. There is exactly one initial gap, the whole left strip. Total: O(1 + s²). ✓
- **Coverage.** An undeleted point at a non-event abscissa lies strictly inside some gap: it is on no sampled graph because it was not deleted. A point at an event abscissa is, by the choice of direction, an extremum or intersection of original circles, hence on a sampled circle, hence deleted. ✓
- **Candidates.** Each endpoint abscissa has ≤ (1+l)² choices (≤ 2l extremal, ≤ l(l−1) intersection, or ∞). Each boundary graph has ≤ 2l+1 choices. Total ≤ (1+l)⁴·(2l+1)² ≤ 4(1+l)⁶. ✓
- **Probability.**
  - A fixed candidate meeting more than l/R circles is met by a uniform draw with probability > 1/R. So P(missed by all s draws) < (1−1/R)^s ≤ e^{−s/R} ≤ (2+l)^{−C}.
  - The union bound gives 4(1+l)⁶·(2+l)^{−C} ≤ 4·2^{6−C} ≤ 1/10 for C ≥ 12.
  - Every actual piece equals some candidate and avoids all sampled circles. ✓

### Prop 2.3 (p. 6)
- Székely's Theorem 8 with t = m = 2 gives c·(lp)^{2/3}·4^{1/3} + l + 10p = O(m^{2/3}l^{2/3} + m + l) in the paper's notation (m points, l curves). ✓
- Cutting circles at 2 points outside the point set gives 2l arcs. Two arcs of the same circle share at most the 2 cut points; two input points lie on at most one arc per circle and on at most 2 circles. So the pair bounds hold. ✓
- The log² weakening is trivially implied. ✓

### Prop 2.4 (pp. 6–8) — brief item (ii), redone line by line
All exponents are of t. "err" means an o(a) error and b = o(a) dominates every err. Every row is also machine-checked (script below).

| Step | Paper's claim | Check |
|---|---|---|
| Choice of a | count ≥ t^{4−o(a)}, (log t)^{O(1)} = t^{o(a)} ⇒ a·log t → ∞ | ✓ needs a ≫ max(input deficit, log log t / log t) |
| Lemma 2.2 with R = t^{1−a}, l = t³ | s = O(t^{1−a}·log t) | ✓ |
| Deleted incidences | ≤ s·t³ on sampled circles + 2s·t³ at deleted points with other circles | ✓ Σ over c ∈ sample, c′ ≠ c of \|c∩c′∩P\| ≤ 2 |
| Cost | O(t^{4−a}·log t) = o(t^{4−o(a)}) | ✓ exponent gap −a + o(a) and a·log t → ∞ |
| Circles per region | ≤ l/R = t^{2+a} | ✓ |
| Pieces | ≤ C′(1+s²) + O(t³/t^{1+2a}) = t^{2−2a+o(a)}, pieces of size ≤ 2t^{1+2a} | ✓ greedy split gives ≤ 1 + n_r/t^{1+2a} pieces per region |
| Pigeonhole | some piece has e₀ ≥ t^{4−o(a)} / t^{2−2a+o(a)} = t^{2+2a−o(a)} | ✓ |
| Upper e₀ via (2.1) | (2t^{1+2a})^{2/3}·(t^{2+a})^{2/3} = O(t^{2+2a}); linear terms ≤ t^{2+a} | ✓ |
| Markov counts | #{d(p) > t^{1+b}} ≤ t^{1+2a−b+o(a)} ≤ t^{1+2a−b/2}; #{d(q) > t^{a+b}} ≤ t^{2+a−b/2} | ✓ (err < b/2) |
| Mixed terms | (t^{1+2a−b/2})^{2/3}·(t^{2+a})^{2/3} = t^{2+2a−b/3}; the other side is also t^{2+2a−b/3} | ✓ o(e₀) since −b/3 + err < 0 and b·log t → ∞ |
| Linear terms | t^{2+a+o(b)}, t^{1+2a+o(b)} = o(e₀) | ✓ |
| Trimmed sizes | \|P₀\| ≥ e/t^{1+b} = t^{1+2a−o(a)}, \|Q₀\| ≥ t^{2+a−o(a)} | ✓ |
| (2.6) | normalisations: (uv)^{2/3}·t⁰, t^{−a}·v, t^{−1}·u; plus w ≤ T_t·min(u, v) | ✓ |
| (2.6) ⇒ (2.7) | min(t^{−a}v, u) ≤ t^{−a/2}√(uv); min(t^{−1}u, v) ≤ t^{−1/2}√(uv) | ✓ Mixing the two bounds term by term is valid by case analysis: in each case one of w ≤ T(A+B+C), w ≤ Tu, w ≤ Tv suffices. |
| (2.8) | 1 ≤ T_t·((UV)^{19/150} + 2t^{−a/2}·(UV)^{−1/25}); UV ≥ τ² = t^{−a/4} ⇒ 2nd term ≤ 2t^{−49a/100+o(a)} | ✓ 2/3 − 27/50 = 19/150; −1/2 + 1/100 = −49/100 |
| Scales | \|P\| = U·\|P₀\|, \|Q\| = V·\|Q₀\|, \|E\| = W·\|E₀\|, all within t^{o(a)} | ✓ (2.2) kept |
| Degree upper bounds | inherited from the induced subgraph | ✓ |
| Feasible subsets | P_E(F,G) ≤ (uv)^γ = √(uv)·(uv)^η from optimality (fractions Uu, Vv in P₀, Q₀) | ✓ |
| Infeasible subsets | uv ≤ τ/min(U,V) = t^{−a/8+o(a)}; (2.7) divided by W ⇒ ≤ t^{o(a)}·√(uv)·((uv)^{1/6} + 2t^{−a/2}) ≤ ξ_t·√(uv), ξ_t = t^{−a/48+o(a)} | ✓ (UV)^{1/6} ≤ 1 and √(UV)/W ≤ t^{o(a)} |
| (2.4) | U(1−1/\|P\|) ≥ τ, so P∖{p} is feasible; 1 − µ(p) ≤ (1−1/\|P\|)^γ ≤ 1 − γ/\|P\| (Bernoulli, 0 < γ < 1) | ✓ |
| (2.3) lower bounds | d(p) ≥ γ\|E\|/\|P\| = t^{1+o(a)}, d(q) ≥ γ\|E\|/\|Q\| = t^{a+o(a)} | ✓ |
| (2.9) | \|F\|/\|P\| ≤ h/γ etc. ⇒ C = γ^{−1−2η} | ✓ |

The maximising rectangle keeps **both** degree bounds (upper by inheritance, lower by (2.4)) and the scales (2.2) (by (2.8)). ✓

### Lemma 2.5 (pp. 8–9)
- 1 − s = Σᵢ P_E(Fᵢ × Gᵢ) ≤ maxᵢ (uᵢvᵢ)^η·Σ√(uᵢvᵢ) + ξ_t·Σ√(uᵢvᵢ), and Σ√(uᵢvᵢ) ≤ 1 by Cauchy–Schwarz. So u_{a₀}·v_{a₀} ≥ (1 − s₀ − ξ_t)^{25}.
- Applying (2.5) to a complement against the full opposite side gives h ≤ √(1−u_{a₀})·((1−u_{a₀})^η + ξ_t), so h and k are as small as desired.
- Proportionality: J ≤ C√(hk)·((hk)^η + ξ_t) ≤ C·((h+k)/2)·((hk)^η + ξ_t) ≤ (h+k)/4 once (hk)^η + ξ_t ≤ 1/(2C). Requiring h, k ≤ ε₁ := (4C)^{−25/2} and t large is enough, which fixes s₀ as an absolute constant.
- "Exactly one endpoint has label a₀" has probability h + k − 2J, and these are mismatches. So s ≥ (h+k)/2. ✓
- (2.10): P(ℓ(p) ≠ ℓ(p′)) ≤ 2h ≤ 4s; for s > s₀ take C ≥ 1/s₀. ✓
- This holds for any finite label set of any size (Cauchy–Schwarz). The centre case is symmetric. ✓

### Lemma 2.6 (pp. 9–10)
- (i): hk ≤ h ≤ δ_t in (2.9). ✓
- (ii): hk ≤ δ_t² and √(hk) ≤ (h+k)/2. ✓
- (iii):
  - Under the wedge law, p and r are conditionally i.i.d. given q, so P(p∈F, r∈F) = E_κ[g²] with E_κ[g] = h. ✓
  - Split at g ≤ d: E[g²] ≤ d·h + E_κ[g·1_{G_d}] = d·h + P_E(F, G_d). ✓
  - Markov gives κ(G_d) ≤ h/d. (2.9) is monotone in the second mass, so P_E(F, G_d) ≤ C·h·d^{−1/2}·((δ_t²/d)^η + ξ_t). ✓
  - d_t = max(δ_t^η, ξ_t, 1/t) gives δ_t^{2η}·d_t^{−1/2−η} ≤ δ_t^{η(3/2−η)} → 0 and ξ_t·d_t^{−1/2} ≤ ξ_t^{1/2} → 0. ✓
- "Error factors outside sums": each bound has the form ε_t × (h, √(hk), or h+k), where ε_t depends only on (δ_t, ξ_t, C). Summing over a family whose masses obey the same δ_t keeps the same ε_t. ✓

### Lemma 2.7 (pp. 10–11)
- (2.11): κ(q)·ω(p|q)·ω(r|q) = (d(q)/|E|)·d(q)^{−2}. ✓
- (2.16): two distinct points have ≤ 2 common unit-distance centres, so P(p,r) ≤ 2/(|E|·d_min) = t^{−2−3a+o(a)}. ✓
- (2.17): Σ_p Σ_{q∼p} 1/(|E|·d(q)) = |Q|/|E| = t^{−a+o(a)}, exactly. ✓
- H(p,r) ≥ Σ_{off-diagonal} π·log(1/π) ≥ (1 − P(p=r))·log(1/M_t), with log(1/M_t) = (2 + 3a + o(a))·log t. ✓
- H(p) ≤ log|P| = (1 + 2a + o(a))·log t. ✓
- D = 2H(p) − H(p,r). The resulting rate is given in O5. ✓
- How D depends on a: the off-diagonal part contributes ≈ log(|P|²/(|E|·d)) = a·log t (the imbalance), and the diagonal part ≈ t^{−a}·log(|P|·t^{−a}). In the balanced SST shape (|P| = |Q| = t³, |E| = t⁴, d = t) the same bound gives D ≤ log t = (1/3)·log|P|, which is not o(log t). **The unbalanced cut with a → 0 is exactly what makes D small.** ✓

### Euclidean-specificity (brief (i)) and density (brief (viii)(b),(d)), restricted to §2
- §2 uses only four facts:
  1. Two distinct unit circles meet in ≤ 2 points.
  2. Two distinct points lie on ≤ 2 unit circles.
  3. Each circle splits into one upper and one lower x-monotone graph with 2 extrema.
  4. The unit circle is algebraic over ℚ (Lemma 2.1 only).
- Facts 1–3 hold for every strictly convex norm, including Valtr's. Without fact 4, §2 still runs; only the number-field setting downstream needs it.
- **So for Valtr's metric, §2 produces the same unbalanced piece with D = o(log t).** No Euclidean feature is used here, consistent with the brief's reading.
- **Realness used in §2:** Lemma 2.1 (real closed fields), Lemma 2.2 (the planar sweep needs an order), and Prop 2.3 (planar crossing lemma). A complex configuration on the graph of zw = 1 would need a different incidence and cutting toolkit.
- **Near-4/3 density is essential in §2.**
  - With only t^{4−c} pairs, the pigeonhole gives e₀ ≥ t^{2+2a−c}, so d(q) ≈ t^{a−c}, which is below 1 for a < c.
  - Taking a ≥ c instead, the D-bound becomes D/log t ≤ 2(1+2a) − (2+2a−c + a−c) = a + 2c, which does not tend to 0.
  - So §2 cannot be run at density n^{1+o(1)}, or at any fixed deficit (sympy control 5).
- **No effective δ:** §2 is purely sequential, with o(·) along t → ∞.

---

## Finite checks

### Check 1 — exponent bookkeeping (sympy)
The regime is err ≪ b ≪ a ≪ 1, encoded as symbols a, b, e. A claimed inequality holds iff the leading coefficient of the exponent difference is negative in the order 1 ≫ a ≫ b ≫ e.

**Instrument note:** my first run reported 2 FAILs ("retained |P₀| ≥ …", "retained |Q₀| ≥ …"). These were my own encoding error: I wrote lower bounds as LHS ≤ RHS. After fixing the direction, all 33 claims PASS. The verbatim script below is the fixed version.

```python
# Exponent bookkeeping for Prop 2.4 / Lemma 2.7 of "A power saving for planar unit distances".
# Every quantity is t^{exponent}; exponents are linear in the small parameters
#   a  (a -> 0, a log t -> oo),  b = o(a) (b log t -> oo),  e = generic o(b) error  (e << b << a << 1).
# A claim "X <= Y" (or "X = o(Y)") holds asymptotically iff exp(X) - exp(Y) is eventually negative,
# i.e. iff its most dominant nonzero coefficient, in the order  1 >> a >> b >> e, is negative.
# ("eventually" uses a log t -> oo and b log t -> oo so t^{-c a}, t^{-c b} -> 0.)
import sympy as sp
a, b, e = sp.symbols('a b e', positive=True)
R = sp.Rational
gamma = R(27, 50); eta = gamma - R(1, 2)

def lead_sign(expr):
    expr = sp.expand(expr)
    poly = sp.Poly(expr, a, b, e)
    const = poly.coeff_monomial(1)
    if const != 0: return sp.sign(const), '1'
    for v in (a, b, e):
        c = poly.coeff_monomial(v)
        if c != 0: return sp.sign(c), str(v)
    # higher-order monomials only (e.g. a*b): check by substitution regime
    return 0, 'zero'

checks = []
def claim(name, lhs, rhs, strict=True, equality=False):
    d = sp.expand(lhs - rhs)
    s, by = lead_sign(d)
    if equality:
        ok = (d == 0)
    else:
        ok = (s < 0) if strict else (s <= 0)
    checks.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}:  exp(LHS)-exp(RHS) = {d}   [sign {s} via {by}]")
    return ok

def run(gamma, eta, label):
    print(f"--- {label}: gamma={gamma}, eta={eta}")
    # e_err : any o(a) error; b chosen to dominate them; we model o(a) errors as +-e.
    s_exp = 1 - a + e          # s = O(t^{1-a} log t), log t = t^{o(a)}
    claim("deletion cost s*t^3 = o(t^{4-o(a)})", s_exp + 3, 4 - e)
    claim("pieces: s^2 + t^3/t^{1+2a} <= t^{2-2a+o(a)}", 2*s_exp, 2 - 2*a + 2*e, strict=False)
    claim("  second term t^{3-(1+2a)} equals t^{2-2a}", 3 - (1 + 2*a), 2 - 2*a, equality=True)
    e0_low = (4 - e) - (2 - 2*a + 2*e)
    claim("pigeonhole e0 >= t^{2+2a-o(a)}", 2 + 2*a - 3*e, e0_low, equality=True)
    claim("Szekely upper: (|P0||Q0|)^{2/3} = t^{2+2a}", R(2,3)*(1+2*a) + R(2,3)*(2+a), 2 + 2*a, equality=True)
    claim("  linear |Q0| = t^{2+a} below t^{2+2a}", 2 + a, 2 + 2*a)
    e0_up = 2 + 2*a + e
    claim("#points deg>t^{1+b} <= t^{1+2a-b/2}", e0_up - (1 + b), 1 + 2*a - b/2)
    claim("#centers deg>t^{a+b} <= t^{2+a-b/2}", e0_up - (a + b), 2 + a - b/2)
    mixed1 = R(2,3)*(1 + 2*a - b/2) + R(2,3)*(2 + a)
    mixed2 = R(2,3)*(1 + 2*a) + R(2,3)*(2 + a - b/2)
    claim("mixed term (excess points) = t^{2+2a-b/3}", mixed1, 2 + 2*a - b/3, equality=True)
    claim("mixed term (excess centers) = t^{2+2a-b/3}", mixed2, 2 + 2*a - b/3, equality=True)
    claim("mixed term o(e0)", 2 + 2*a - b/3 + e, 2 + 2*a - 3*e)
    claim("linear t^{2+a+o(b)} = o(e0)", 2 + a + e, 2 + 2*a - 3*e)
    claim("linear t^{1+2a+o(b)} = o(e0)", 1 + 2*a + e, 2 + 2*a - 3*e)
    claim("retained |P0| >= e/maxdeg = t^{1+2a-o(a)}  [encoded as t^{1+2a-2b} <= e0/t^{1+b}]", 1 + 2*a - 2*b, (2 + 2*a - 3*e) - (1 + b), strict=False)
    claim("retained |Q0| >= t^{2+a-o(a)}  [encoded as t^{2+a-2b} <= e0/t^{a+b}]", 2 + a - 2*b, (2 + 2*a - 3*e) - (a + b), strict=False)
    # (2.6) normalisations relative to |E0| = t^{2+2a}
    claim("(2.6) (|F||G|)^{2/3}/|E0| -> (uv)^{2/3} t^0", R(2,3)*(1+2*a) + R(2,3)*(2+a) - (2+2*a), 0, equality=True)
    claim("(2.6) |G|/|E0| -> t^{-a} v", (2 + a) - (2 + 2*a), -a, equality=True)
    claim("(2.6) |F|/|E0| -> t^{-1} u", (1 + 2*a) - (2 + 2*a), -1, equality=True)
    claim("(2.7) t^{-1/2} <= t^{-a/2}", -R(1,2), -a/2)
    # (2.8): second term exponent with UV >= t^{-a/4}
    claim("(2.8) 2nd term exponent -a/2 + eta*a/4 = -49a/100", -a/2 + eta*a/4, -R(49,100)*a, equality=(gamma==R(27,50)))
    claim("(2.8) 2nd term -> 0", -a/2 + eta*a/4 + e, 0)
    claim("(2.8) first-term power 2/3-gamma > 0  [UV<=t^{-ca} => T_t (UV)^{2/3-gamma} -> 0]", -(R(2,3) - gamma)*a + e, 0)
    claim("eta = gamma - 1/2 > 0 (needed for (2.5) to beat sqrt(uv))", -eta, 0)
    # infeasible subsets: uv <= tau/min(U,V) = t^{-a/8+o(a)}
    claim("xi_t: (uv)^{1/6} <= t^{-a/48+o(a)}", (-a/8 + e)/6, -a/48 + e, strict=False)
    claim("xi_t -> 0", -a/48 + e, 0)
    claim("2 t^{-a/2} <= t^{-a/48}", -a/2, -a/48)
    claim("tau = t^{-a/8} below U = t^{-o(a)} (single-vertex removal stays feasible)", -a/8, -e)
    # (2.3)
    claim("d(p) >= gamma|E|/|P| = t^{1+o(a)}", (2 + 2*a) - (1 + 2*a), 1, equality=True)
    claim("d(q) >= gamma|E|/|Q| = t^{a+o(a)}", (2 + 2*a) - (2 + a), a, equality=True)
    claim("max mu(p) = t^{-1-2a+o(a)}", (1) - (2 + 2*a), -1 - 2*a, equality=True)
    # Lemma 2.7
    claim("(2.16) 2/(|E| d_min) = t^{-2-3a}", -(2 + 2*a) - a, -2 - 3*a, equality=True)
    claim("(2.17) |Q|/|E| = t^{-a} -> 0", (2 + a) - (2 + 2*a) + e, 0)

run(gamma, eta, "paper's constants")
D_over_logt = 2*(1 + 2*a) - (2 + 3*a)   # leading part of D/log t, ignoring the (2+3a) t^{-a} diagonal term
print("Lemma 2.7: D/log t <= 2(1+2a) - (1 - t^{-a+o(a)})(2+3a) - o(a) =", sp.simplify(D_over_logt), "+ (2+3a) t^{-a+o(a)} + o(a)")
ok_all = all(c[1] for c in checks)
print("ALL PAPER CLAIMS PASS:", ok_all)

print("\n===== CONTROLS (must FAIL) =====")
checks.clear()
print("[control 1] gamma = 7/10 > 2/3: the 'first term -> 0' step of (2.8) must fail")
g2 = R(7,10); claim("(2.8) first-term power 2/3-gamma > 0", -(R(2,3) - g2)*a + e, 0)
print("[control 2] gamma = 1/2 (eta=0): expansion (2.5) gives nothing beyond sqrt(uv)")
claim("eta > 0", -(R(1,2)-R(1,2)), 0)
print("[control 3] no cutting (R = 1, i.e. a = 1 'balanced' piece |P|=|Q|=t^3, |E|=t^4, d(q)=t): D/log t bound")
Dbal = 2*3 - (4 + 1)
print("   balanced D/log t <=", Dbal, "-> not o(1):", 'FAIL (as expected)' if Dbal > 0 else 'unexpected')
print("[control 4] mis-claimed excess count t^{1+2a-2b} (Markov only gives t^{1+2a-b+o})")
claim("#points deg>t^{1+b} <= t^{1+2a-2b}", (2 + 2*a + e) - (1 + b), 1 + 2*a - 2*b)
print("[control 5] density deficit: configuration with t^{4-c} pairs, fixed c=1/10: d(q) exponent a - c stays negative as a->0")
c = R(1,10); claim("d(q) -> oo with deficit c", -(a - c), 0)
print("CONTROLS that passed (should be none):", [n for n,o in checks if o])
```
Output:
```
--- paper's constants: gamma=27/50, eta=1/25
PASS  deletion cost s*t^3 = o(t^{4-o(a)}):  exp(LHS)-exp(RHS) = -a + 2*e   [sign -1 via a]
PASS  pieces: s^2 + t^3/t^{1+2a} <= t^{2-2a+o(a)}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS    second term t^{3-(1+2a)} equals t^{2-2a}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  pigeonhole e0 >= t^{2+2a-o(a)}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  Szekely upper: (|P0||Q0|)^{2/3} = t^{2+2a}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS    linear |Q0| = t^{2+a} below t^{2+2a}:  exp(LHS)-exp(RHS) = -a   [sign -1 via a]
PASS  #points deg>t^{1+b} <= t^{1+2a-b/2}:  exp(LHS)-exp(RHS) = -b/2 + e   [sign -1 via b]
PASS  #centers deg>t^{a+b} <= t^{2+a-b/2}:  exp(LHS)-exp(RHS) = -b/2 + e   [sign -1 via b]
PASS  mixed term (excess points) = t^{2+2a-b/3}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  mixed term (excess centers) = t^{2+2a-b/3}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  mixed term o(e0):  exp(LHS)-exp(RHS) = -b/3 + 4*e   [sign -1 via b]
PASS  linear t^{2+a+o(b)} = o(e0):  exp(LHS)-exp(RHS) = -a + 4*e   [sign -1 via a]
PASS  linear t^{1+2a+o(b)} = o(e0):  exp(LHS)-exp(RHS) = 4*e - 1   [sign -1 via 1]
PASS  retained |P0| >= e/maxdeg = t^{1+2a-o(a)}  [encoded as t^{1+2a-2b} <= e0/t^{1+b}]:  exp(LHS)-exp(RHS) = -b + 3*e   [sign -1 via b]
PASS  retained |Q0| >= t^{2+a-o(a)}  [encoded as t^{2+a-2b} <= e0/t^{a+b}]:  exp(LHS)-exp(RHS) = -b + 3*e   [sign -1 via b]
PASS  (2.6) (|F||G|)^{2/3}/|E0| -> (uv)^{2/3} t^0:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.6) |G|/|E0| -> t^{-a} v:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.6) |F|/|E0| -> t^{-1} u:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.7) t^{-1/2} <= t^{-a/2}:  exp(LHS)-exp(RHS) = a/2 - 1/2   [sign -1 via 1]
PASS  (2.8) 2nd term exponent -a/2 + eta*a/4 = -49a/100:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.8) 2nd term -> 0:  exp(LHS)-exp(RHS) = -49*a/100 + e   [sign -1 via a]
PASS  (2.8) first-term power 2/3-gamma > 0  [UV<=t^{-ca} => T_t (UV)^{2/3-gamma} -> 0]:  exp(LHS)-exp(RHS) = -19*a/150 + e   [sign -1 via a]
PASS  eta = gamma - 1/2 > 0 (needed for (2.5) to beat sqrt(uv)):  exp(LHS)-exp(RHS) = -1/25   [sign -1 via 1]
PASS  xi_t: (uv)^{1/6} <= t^{-a/48+o(a)}:  exp(LHS)-exp(RHS) = -5*e/6   [sign -1 via e]
PASS  xi_t -> 0:  exp(LHS)-exp(RHS) = -a/48 + e   [sign -1 via a]
PASS  2 t^{-a/2} <= t^{-a/48}:  exp(LHS)-exp(RHS) = -23*a/48   [sign -1 via a]
PASS  tau = t^{-a/8} below U = t^{-o(a)} (single-vertex removal stays feasible):  exp(LHS)-exp(RHS) = -a/8 + e   [sign -1 via a]
PASS  d(p) >= gamma|E|/|P| = t^{1+o(a)}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  d(q) >= gamma|E|/|Q| = t^{a+o(a)}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  max mu(p) = t^{-1-2a+o(a)}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.16) 2/(|E| d_min) = t^{-2-3a}:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
PASS  (2.17) |Q|/|E| = t^{-a} -> 0:  exp(LHS)-exp(RHS) = -a + e   [sign -1 via a]
Lemma 2.7: D/log t <= 2(1+2a) - (1 - t^{-a+o(a)})(2+3a) - o(a) = a + (2+3a) t^{-a+o(a)} + o(a)
ALL PAPER CLAIMS PASS: True

===== CONTROLS (must FAIL) =====
[control 1] gamma = 7/10 > 2/3: the 'first term -> 0' step of (2.8) must fail
FAIL  (2.8) first-term power 2/3-gamma > 0:  exp(LHS)-exp(RHS) = a/30 + e   [sign 1 via a]
[control 2] gamma = 1/2 (eta=0): expansion (2.5) gives nothing beyond sqrt(uv)
FAIL  eta > 0:  exp(LHS)-exp(RHS) = 0   [sign 0 via zero]
[control 3] no cutting (R = 1, i.e. a = 1 'balanced' piece |P|=|Q|=t^3, |E|=t^4, d(q)=t): D/log t bound
   balanced D/log t <= 1 -> not o(1): FAIL (as expected)
[control 4] mis-claimed excess count t^{1+2a-2b} (Markov only gives t^{1+2a-b+o})
FAIL  #points deg>t^{1+b} <= t^{1+2a-2b}:  exp(LHS)-exp(RHS) = b + e   [sign 1 via b]
[control 5] density deficit: configuration with t^{4-c} pairs, fixed c=1/10: d(q) exponent a - c stays negative as a->0
FAIL  d(q) -> oo with deficit c:  exp(LHS)-exp(RHS) = 1/10 - a   [sign 1 via 1]
CONTROLS that passed (should be none): []
```
**Controls (must fail, all do):** γ = 7/10 > 2/3 breaks the (2.8) step; η = 0 gives no expansion gain; the balanced SST piece gives D/log t ≤ 1, which is not o(1); a mis-claimed excess count t^{1+2a−2b} is rejected; a fixed density deficit c = 1/10 makes d(q) → 0. The checker's list of controls that wrongly passed is empty.

### Check 2 — Lemma 2.7 on explicit graphs (exact D)
**Graphs tested:**
- **Random unbalanced graphs** at the paper's exponents: |P| = t^{1+2a}, |Q| = t^{2+a}, d(q) ≈ t^a, codegree ≤ 2 enforced.
- **Random balanced graphs** of SST shape: |P| = |Q| = N, d = N^{1/3}.
- **A control that violates the hypothesis:** 30 blocks of K(2, 900), codegree 900.

**What is checked:**
- (2.16): every off-diagonal atom is ≤ 2/(|E|·d_min).
- (2.17): P(p=r) equals |Q|/|E| exactly.
- H(p,r) ≥ (1 − P(p=r))·log(1/M).
- The direct KL computation equals the entropy identity.
- D ≤ B := 2·log|P| − (1 − |Q|/|E|)·log(|E|·d_min/2).

**Honest limit of the toy:** "D = o(log t)" needs a → 0 and t^{−a} → 0 *at once*, which is impossible at toy sizes (here t^{−a} = 1/d(q) ≈ 0.2). The toy therefore verifies the **finite inequality chain** and the shape of D(a). It does not verify the asymptotic smallness itself.
- In the toy, unbalanced D/log|P| ≈ 0.35 and balanced ≈ 0.36, so at these sizes the two are indistinguishable.
- Asymptotically, unbalanced D/log t ≈ a + (1+a)·t^{−a} → 0, while balanced D/log N stays near 1/3. That comparison comes from the analytic formula, not the toy.

```python
# Toy check of Lemma 2.7 (wedge law, (2.16)-(2.18)) on explicit bipartite graphs.
# Wedge law (2.11): P(p,q,r) = 1/(|E| d(q)) for (p,q),(r,q) in E.
# Lemma's finite content (codegree <= 2 hypothesis: two distinct points share <= 2 centres):
#   (2.16) every off-diagonal atom pi(p,r) <= M := 2/(|E| d_min)
#   (2.17) P(p=r) = |Q|/|E|   (exact)
#   H(p,r) >= (1-P(p=r)) log(1/M);  H(p) <= log|P|
#   => D = KL(pi || mu x mu) = H(p)+H(r)-H(p,r) <= B := 2 log|P| - (1-|Q|/|E|) log(|E| d_min / 2)
import sys, math, random
import numpy as np, scipy.sparse as sps

def random_codeg2_graph(NP, NQ, d, seed):
    rng = random.Random(seed)
    cover = {}
    rows, cols = [], []
    q = 0; tries = 0
    while q < NQ:
        tries += 1
        if tries > 50 * NQ: raise RuntimeError("could not place centres")
        nb = rng.sample(range(NP), d)
        pairs = [(min(x,y), max(x,y)) for i,x in enumerate(nb) for y in nb[i+1:]]
        if any(cover.get(pr, 0) >= 2 for pr in pairs): continue
        for pr in pairs: cover[pr] = cover.get(pr, 0) + 1
        rows += [q]*d; cols += nb; q += 1
    A = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NQ, NP))
    return A

def analyse(A, label, eps_small=None):
    NQ, NP = A.shape
    dq = np.asarray(A.sum(axis=1)).ravel(); dp = np.asarray(A.sum(axis=0)).ravel()
    keepq = dq > 0; keepp = dp > 0
    A = A[keepq][:, keepp]; dq = dq[keepq]; dp = dp[keepp]
    NQ, NP = A.shape
    E = A.sum()
    W = sps.diags(1.0 / (E * dq))
    pi = (A.T @ W @ A).toarray()          # NP x NP wedge point-pair law
    mu = dp / E
    assert abs(pi.sum() - 1) < 1e-9
    assert np.allclose(pi.sum(axis=0), mu) and np.allclose(pi.sum(axis=1), mu)
    codeg = (A.T @ A).toarray(); np.fill_diagonal(codeg, 0)
    maxcodeg = codeg.max()
    dmin = dq.min()
    M = 2.0 / (E * dmin)
    off = pi.copy(); np.fill_diagonal(off, 0)
    diag = np.trace(pi)
    nz = pi[pi > 0]
    Hpr = -(nz * np.log(nz)).sum()
    Hp = -(mu * np.log(mu)).sum()
    D_direct = (pi[pi > 0] * np.log(pi[pi > 0] / np.outer(mu, mu)[pi > 0])).sum()
    D_ent = 2 * Hp - Hpr
    B = 2 * math.log(NP) - (1 - NQ / E) * math.log(E * dmin / 2)
    res = {
      '|P|': NP, '|Q|': NQ, '|E|': int(E), 'd_min,Q': int(dmin), 'max codeg': int(maxcodeg),
      '(2.16) max offdiag <= M': bool(off.max() <= M * (1 + 1e-12)),
      '(2.17) P(p=r) == |Q|/|E|': bool(abs(diag - NQ / E) < 1e-12),
      'H(p,r) >= (1-P(p=r))log(1/M)': bool(Hpr >= (1 - diag) * math.log(1 / M) - 1e-12),
      'D_direct == H(p)+H(r)-H(p,r)': bool(abs(D_direct - D_ent) < 1e-9),
      'D <= B': bool(D_direct <= B + 1e-12),
    }
    print(f"== {label}")
    for k, v in res.items(): print(f"   {k}: {v}")
    print(f"   D = {D_direct:.4f}   B = {B:.4f}   D/log|P| = {D_direct/math.log(NP):.3f}   B/log|P| = {B/math.log(NP):.3f}   P(p=r) = {diag:.4f}")
    return res, D_direct, B

if __name__ == "__main__":
    ok = True
    # (1) unbalanced toy at the paper's exponents: |P|=t^{1+2a}, |Q|=t^{2+a}, d(q)=t^a
    for (t, a, seed) in [(60, 0.40, 1), (100, 0.35, 2), (150, 0.30, 3)]:
        d = max(2, round(t ** a)); NP = round(t ** (1 + 2 * a)); NQ = round(t ** (2 + a))
        A = random_codeg2_graph(NP, NQ, d, seed)
        res, D, B = analyse(A, f"UNBALANCED t={t}, a={a}: |P|=t^(1+2a)={NP}, |Q|=t^(2+a)={NQ}, d(q)=t^a~{d}")
        L = math.log(t)
        print(f"   D/log t = {D/L:.3f};  paper's leading form a + (2+3a) t^-a = {a + (2+3*a)*t**(-a):.3f};  exact finite B/log t = {B/L:.3f}")
        ok &= all(res.values())
    # (2) balanced toy: |P|=|Q|=N, d(q) ~ N^{1/3} (SST shape)
    for (N, seed) in [(1000, 4), (2400, 5)]:
        d = round(N ** (1/3)); A = random_codeg2_graph(N, N, d, seed)
        res, D, B = analyse(A, f"BALANCED (SST shape) N={N}, d={d}")
        ok &= all(res.values())
        print(f"   balanced: B/log N = {B/math.log(N):.3f} (~1/3 + diag term, does NOT tend to 0)")
    print("ALL LEMMA-2.7 CHECKS PASS ON VALID GRAPHS:", ok)

    print("\n===== CONTROL (hypothesis violated, must FAIL) =====")
    # blocks of 2 points sharing m = B^2 centres: codegree m >> 2
    Bk = 30; m = Bk * Bk
    rows, cols = [], []
    q = 0
    for blk in range(Bk):
        for j in range(m):
            rows += [q, q]; cols += [2 * blk, 2 * blk + 1]; q += 1
    A = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(q, 2 * Bk))
    res, D, B = analyse(A, f"CODEGREE-VIOLATING control: {Bk} blocks K(2,{m})")
    print("   control rejected (some check False):", not all(res.values()))
    print(f"   exact D = log B = {math.log(Bk):.4f}")
```
Output:
```
== UNBALANCED t=60, a=0.4: |P|=t^(1+2a)=1587, |Q|=t^(2+a)=18517, d(q)=t^a~5
   |P|: 1587
   |Q|: 18517
   |E|: 92585
   d_min,Q: 5
   max codeg: 2
   (2.16) max offdiag <= M: True
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): True
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: True
   D = 2.5661   B = 4.8575   D/log|P| = 0.348   B/log|P| = 0.659   P(p=r) = 0.2000
   D/log t = 0.627;  paper's leading form a + (2+3a) t^-a = 1.022;  exact finite B/log t = 1.186
== UNBALANCED t=100, a=0.35: |P|=t^(1+2a)=2512, |Q|=t^(2+a)=50119, d(q)=t^a~5
   |P|: 2512
   |Q|: 50119
   |E|: 250595
   d_min,Q: 5
   max codeg: 2
   (2.16) max offdiag <= M: True
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): True
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: True
   D = 2.6085   B = 4.9794   D/log|P| = 0.333   B/log|P| = 0.636   P(p=r) = 0.2000
   D/log t = 0.566;  paper's leading form a + (2+3a) t^-a = 0.959;  exact finite B/log t = 1.081
== UNBALANCED t=150, a=0.3: |P|=t^(1+2a)=3032, |Q|=t^(2+a)=101160, d(q)=t^a~4
   |P|: 3032
   |Q|: 101160
   |E|: 404640
   d_min,Q: 4
   max codeg: 2
   (2.16) max offdiag <= M: True
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): True
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: True
   D = 3.0175   B = 5.8310   D/log|P| = 0.376   B/log|P| = 0.727   P(p=r) = 0.2500
   D/log t = 0.602;  paper's leading form a + (2+3a) t^-a = 0.945;  exact finite B/log t = 1.164
== BALANCED (SST shape) N=1000, d=10
   |P|: 1000
   |Q|: 1000
   |E|: 10000
   d_min,Q: 10
   max codeg: 2
   (2.16) max offdiag <= M: True
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): True
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: True
   D = 2.4953   B = 4.0777   D/log|P| = 0.361   B/log|P| = 0.590   P(p=r) = 0.1000
   balanced: B/log N = 0.590 (~1/3 + diag term, does NOT tend to 0)
== BALANCED (SST shape) N=2400, d=13
   |P|: 2400
   |Q|: 2400
   |E|: 31200
   d_min,Q: 13
   max codeg: 2
   (2.16) max offdiag <= M: True
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): True
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: True
   D = 2.8203   B = 4.2865   D/log|P| = 0.362   B/log|P| = 0.551   P(p=r) = 0.0769
   balanced: B/log N = 0.551 (~1/3 + diag term, does NOT tend to 0)
ALL LEMMA-2.7 CHECKS PASS ON VALID GRAPHS: True

===== CONTROL (hypothesis violated, must FAIL) =====
== CODEGREE-VIOLATING control: 30 blocks K(2,900)
   |P|: 60
   |Q|: 27000
   |E|: 54000
   d_min,Q: 2
   max codeg: 900
   (2.16) max offdiag <= M: False
   (2.17) P(p=r) == |Q|/|E|: True
   H(p,r) >= (1-P(p=r))log(1/M): False
   D_direct == H(p)+H(r)-H(p,r): True
   D <= B: False
   D = 3.4012   B = 2.7403   D/log|P| = 0.831   B/log|P| = 0.669   P(p=r) = 0.5000
   control rejected (some check False): True
   exact D = log B = 3.4012
```
**Reading:**
- On every hypothesis-satisfying graph, all five checks are True. The bound is attained up to a constant: D/log t = 0.57–0.63 against the leading-order model a + (1+a)·t^{−a} = 0.67 / 0.62 / 0.59 for the three (t, a) cases. The paper's bound gives 0.95–1.02, slack coming only from the constant 2+3a on the t^{−a} term.
- **Control (codegree 900):** (2.16) is False, the H(p,r) bound is False, and D = log 30 = 3.40 > B = 2.74. The check rejects it. This shows the two-circle property is what Lemma 2.7 rests on.
- **Balanced control:** B/log N = 0.55–0.59, and asymptotically ≈ 1/3, so it does not tend to 0. D is not small in the SST shape.

---

## Citation table (scope)

| Cited result | Paper's claim | What the source says (quote) | Verdict |
|---|---|---|---|
| Székely [25], Theorem 8 (read: preprint copy at cs.umd.edu/users/gasarch/TOPICS/erdos_dist/szekely.pdf; its header carries a template "CPC (1993) 11, 1–10"; the published CPC 6(3):353–358 version was not seen. The theorem numbers agree with the paper's "[25, Theorems 4 and 8]" in §1.1, and Iosevich's lecture notes also cite "[28], Theorem 8" for the curve version) | "gives the stronger bound I = O(m^{2/3}l^{2/3} + m + l) when distinct curves meet in at most two points and distinct points belong to at most two curves" | "**Theorem 8.** Given p points and l simple curves in the plane, such that any two curves intersect in at most t points and any two points belong to at most m curves, the number of incidences is at most c(lp)^{2/3}(tm)^{1/3} + l + 5mp." With t = m = 2 this is the claimed bound. Theorem 4 there is the SST unit-distance bound c·n^{4/3}. | **MATCH** (preprint version) |
| Clarkson [5], §4 (read: DCG 2 (1987) 195–222, Springer PDF, 28 pp.) | "the random-sampling principle for regions with bounded defining data developed by Clarkson [5, Section 4]" | Thm 4.1 / Cor 4.2: "Prob{∃A ∈ F_R with #(A,R) = 0 and #(A,S) > αs} ≤ O(r^i)(1−α)^{r−i}, for fixed i and n. For suitable α = O(log r/r), this probability is no more than 1/2." The proof uses that "the samples not indexed by a number in τ are chosen independently of those that are indexed in that way." | **MATCH as attribution** (O4). The paper's union bound is over all regions defined by the full family, not by the sample. It is self-contained and does not use Clarkson's independence step. |
| Kuhlmann [17], Lecture 09, Thms 3.1 / 4.1 (read: Notes09.pdf, 5 pp., 17/11/09) | "The transfer principle for real closed fields [17, Theorems 3.1 and 4.1] gives a solution in the field of real algebraic numbers." | "**Theorem 3.1.** Let (K, ≤) be an ordered field, R₁, R₂ two real closed extensions of (K, ≤). Then a system of polynomial equations and inequalities … where ∀i ⊳ᵢ ∈ {≥, >, =, ≠} and fᵢ(X) ∈ K[X₁,…,Xₙ], has a solution x ∈ R₁ⁿ ⇔ it has a solution x ∈ R₂ⁿ." "**Theorem 4.1.** Suppose that R ⊆ R₁ are real closed fields. Then a system … with coefficients in R … has a solution x ∈ R₁ⁿ ⇔ it has a solution x ∈ Rⁿ." Apply with K = ℚ (or R = ℝ_alg), R₁ = ℝ. The system uses only = and >. | **MATCH** |

---

## Hand-wave phrases in scope (all checked)
- "with the evident interpretation when R = 1" (p. 6): (1−1)^s = 0 and no region can meet more than l circles. ✓
- "(2.1) follows" (p. 6): ✓
- "the upper bound follows from (2.1)" (p. 7): ✓
- "The center comparison is identical" (p. 8): 1 − κ(q) ≤ (1−1/|Q|)^γ. ✓
- "The center assertion is identical", "The analogous statement holds for independent centers" (p. 9): ✓
- "follow directly from (2.9)" (p. 10): ✓
- "The same assertion holds with the sides interchanged" (p. 9): (2.9) is symmetric. ✓
- "The asymptotics follow from the same estimates and a log t → ∞" (p. 10): ✓

No step in §2 is quantified over an uncountable family. The only probabilities called exact, (2.11) and (2.17), are exact.

---

## Summary
§2 holds as read. Every count, exponent and constant re-derives. The Prop 2.4 bookkeeping (deletion O(t^{4−a}·log t), pieces of size ≤ 2t^{1+2a}, Markov counts t^{1+2a−b/2} and t^{2+a−b/2}, (2.6)⇒(2.7)⇒(2.8) with 19/150 and −49a/100, ξ_t = t^{−a/48+o(a)}, (2.4) by single-vertex removal) is machine-confirmed with failing controls. The maximising rectangle keeps the scales and both degree bounds. D ≤ [a + (2+3a)·t^{−a+o(a)} + o(a)]·log t, and this is sharp in order. There are no FATAL or GAP objections; four objections are COSMETIC and one is UNCLEAR (the implicit rate of D). §2 is metric-agnostic: it runs verbatim for Valtr's norm, so the paper's Euclidean input must enter in §4 or later.
