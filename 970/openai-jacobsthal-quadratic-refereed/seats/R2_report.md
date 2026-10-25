# R2 referee report — printed §7 (boxes), §8 (inverse estimate), §9 (variance)

Paper: OpenAI, "A quadratic bound for Jacobsthal's function" (25 Sep 2026). Scope: printed §7 (Lemma 7.1,
Proposition 7.2, Remark 7.3; pp. 36–43), §8 (Definition 8.1, Proposition 8.2, Lemma 8.3; pp. 43–53),
§9 (Lemma 9.1, Proposition 9.2, Corollary 9.3; pp. 53–61). I read the TeX source (boxes.tex, inverse.tex,
variance.tex) and cite printed numbers from the PDF.

STATUS: COMPLETE (03:05Z–~04:00Z).

## 1. Verdict

**HOLDS AS READ** for §8 and §9, and for the internal logic of §7.

That verdict is conditional on inputs from outside my scope, which I did not re-prove: the §5 path estimates
(Prop. 5.5 prime occupation, Prop. 5.3 coupling, Lemma 5.2 high-state removal, Lemma 4.3 regeneration, Lemma 4.6 band
bounds) that the proof of Prop. 7.2 uses as black boxes; Lemma 2.1 (fundamental lemma); Lemma 2.2(iii)
(Brun–Titchmarsh); and Lemma A.1 (modular hyperbola count), which the second range of Prop. 9.2 uses.

I found **no FATAL and no GAP**. Every step of the novel core (§8) checks out, including all of the numerology.
What I have is EXPOSITION-level only (§2 below).

On the brief's specific questions:
- **The §8 list is fixed per (box, candidate edge) and finite, with a bound F independent of z and of ξ.** Definition:
  𝒜 = ALL reduced A/D satisfying (8.7). That depends only on R, S_q, n_p, c_p and the classes {a_p : p ∈ 𝒫}. It is
  fixed before any failure set, cell or sample is chosen. F = ⌈2/c_p²⌉ with c_p = γ_inc/32, which depends only on σ
  and a⋆ (through h₁ > 2400). The Cauchy-inequality list bound is correct (reconstructed below). It needs only
  n_p ≥ 2C_{α_min}/c_p², a threshold on z.
- **No averaging over the classes a_p anywhere in §8–§9.** All averaging is over the box variables (p, q, u), over a
  uniform sample of edge primes u₁,…,u_{h₁}, and (in §9) over explicit dominating measures on (m₀, p mod T₁,
  k mod T₀). The large-sieve step (8.18)–(8.19) holds for an arbitrary survivor set supported on an interval. The
  inverse argument is a contradiction argument valid for each fixed choice of classes.
- **Jarník and Gallagher.** Both are used as self-contained reconstructions in the text, not as black-box citations.
  Each reconstruction is correct (§3).
- **Independence inside a box (§7).** The full-box measure is exactly a product over bins. The isolated bin and the
  candidate bin are singletons, and the bin labels are ordered. So p, q, u and the descendants use pairwise disjoint
  bin sets and are independent (Prop. 7.2(iv)). Correct.
- **Witness on a recent edge (Lemma 7.1).** Correct. The crossing index i ≥ 2 is essential, because at the root
  x₁ ≤ r₁ can fail. The paper handles this ("it is not the first index", since v₁ ≥ log_w Y − B → ∞).
- **§9 pair moment.** Lemma 9.1's uniformity is proved: dominated convergence over odd squarefree l, with the
  w-uniform majorant 2λ_l/l, which is summable. The finite product identity
  ∏(1 − 1/(t−1)²)(1 + 1/(t(t−2))) = 1 holds exactly. The stable version is applied correctly in both ranges of
  Prop. 9.2. Range 1 uses a product measure that dominates the actual primes up to an absolute Brun–Titchmarsh
  constant. Range 2 uses the uniform pattern measure, again up to an absolute constant, plus R^{9/10+o(1)}.
  Chebyshev is applied under the dominating measure and transferred by domination of sets. That is legitimate.

## 2. Objections

None of FATAL / GAP / FIXABLE severity. EXPOSITION items:

E1 (EXPOSITION; throughout the scope, e.g. p. 51 and p. 60). Cross-references produced by `\cref` render lemmas,
propositions and corollaries as "Theorem". In §7–§9 the PDF says "Theorem 7.2" seven times for Proposition 7.2,
"Theorem 8.2" four times for Proposition 8.2, and "By Theorem 8.3" on p. 51 for Lemma 8.3. It also says
"Theorem 2.1" for Lemma 2.1, "Theorem 9.1/9.2" for Lemma 9.1/Proposition 9.2, and "Theorem A.1" for Lemma A.1.
§10 similarly has "Theorem 9.3" for Corollary 9.3. These are cosmetic but misleading for a referee hunting a locator.

E2 (EXPOSITION; Prop. 7.2 proof, "Near-threshold even prefixes", p. 41). "At its preceding odd state, let the gap be
R and the next ratio be t". Here R is a gap, which clashes with R = the isolated-bin lower endpoint in Prop. 7.2(iv),
(7.13) and all of §8–§9.

Other symbol clashes:
- H is used three ways: H = Dq_{f,E} in (9.1); 𝓗(x) = max(2x, x+2); and H_e.
- N is used two ways: N = HT₀ in §9.4, and N = the number of points on the extracted line in §8.
- δ is used two ways: the witness threshold, and the exponent in Lemma 9.1.

None of these causes a logical error.

E3 (EXPOSITION; Lemma 9.1 stable version vs. its use in Prop. 9.2, first range, p. 58). The lemma's hypotheses are
stated with relative error O(ζ). The application delivers O(ζ) + o(1) ("relative error O(ζ)+o(1)"). The lemma's
conclusion ≪ (ζ + o(1)) absorbs this, but the hypothesis should read 1 + O(ζ) + o(1).

E4 (EXPOSITION; Prop. 8.2 statement, p. 44). "constants … independent of the eventual choice of fixed 0 < ξ ≤ ξ_inv".
However, the hypotheses (8.3)–(8.5) that are "fixed" include (8.5), which contains ξ. The intended order is clear from
Remark 7.3 and the proof: σ, then h₁, then c_p and F, then ξ_inv, then ξ, then z. It would be cleaner to state that
(8.5) is part of the box data supplied for each ξ.

E5 (EXPOSITION; Lemma 8.3, p. 45). The bound O(D₀⁴(1 + S^{2/3})) is stated. The proof gives O(D₀³(1 + S^{2/3}))
(Σ dᵢ³ ≤ D₀³). The authors flag it as "slightly looser", so this is harmless.

## 3. What I checked, and how

**§7.**
- Lemma 7.1: every line reconstructed. Points checked:
  - v_j drops by > 1 per edge;
  - the crossing index i ≥ 2;
  - x_i ≤ r_i from the admission rule (3.3) at a nonroot lower parent (r ≥ 2b, r ≥ b+2), and from 𝓗(x) ≥ 2x for
    even children;
  - v_{i−1} < 2K⋆ + 2 ⇒ fewer than H_e edges;
  - the telescoping e_{d′u} − e_{d′} = (N_{d′u} − N_{d′}/u)/(μ_{d′}/u) using μ_{d′u} = μ_{d′}/u.
- Prop. 7.2, (i)–(v): the movement bound mh ≤ 2C_len ξ = Δ; (7.10) from (7.9) via 𝓗 being 2-Lipschitz and
  h = o(Δ); the enlargement to standard paths from r₀+1, using Δ + 2h < 1; and the disjointness of boxes of a given
  length, which makes (7.11) follow from Prop. 5.5(i) with no box-counting factor.
- Independence: the product structure over bins plus ordered labels gives disjoint bin sets for p, q, u and the
  descendants.
- The isolated position precedes every witness. A witness parent has r ≤ 2K⋆ + 5, whereas every prefix up to and
  including the isolated position has gap ≥ α_min B.
- The "isolated position" crossing argument: a child keeps at least 1/2 (from a lower parent) or 2/3 (from an upper
  parent) of the gap, so the arrival gap lies in [.4θB, θB], and bounded ratio puts x in [α_min B, α_max B].
- The repeated-bin width (7.15), and the near-threshold widths O(Δ/R) in both branches (x ≥ 2 and 1 < x ≤ 2).
- (v): m_s ≥ (log B − ½ log w)/log 3.

  The probability inputs (band bounds, coupling, regeneration speed) I took as given.
- Remark 7.3: checked.

**§8.**
- Definition 8.1: checked.
- Prop. 8.2, step by step:
  - List finiteness: two distinct list rationals share ≤ log(2S_qR²𝒵²⁰)/log R ≤ C_{α_min} aligning primes, and the
    Cauchy inequality gives M ≤ 2/c_p².
  - #𝒬 ≥ S_q/𝒵^{o(1)}, and the cells number 𝒵^{o(1)}, using log M₀ = O(w) = o(log 𝒵).
  - Retained-cell density ≥ σ/2, then count density ≥ σ/16.
  - Freezing: the initial hit lies in [1, pq]; the classes at t ≤ w depend only on p, the cell residues and v; the
    interval-replacement errors are O(ξJV₀) and O(ξJV₀/u) via Lemma 2.3's upper bound at length ≥ w^{a⋆/2}.
  - (8.8) ⇒ (8.17) with δ′ = δ/4 for ξ small in terms of δ and the upper-sieve constant, using Y/(pq) ≥ J.
  - The edge class (8.16).
  - The orthogonality identity (8.18): verified numerically.
  - The large sieve with spacing ≥ ((1+ξ)U)⁻², and the arithmetic (8.19). This needs J/U ≥ w^{3a⋆/4},
    U ≥ w and a⋆ < 2; a⋆ = 1/100.
  - Sampling: the fraction ≥ β/2 of pairs, and probability ≥ (β/4)^{h₁} once n_u ≥ 4h₁/β.
  - The CRT slope count (8.21). The coefficient of s in (8.16) is −p̄, and the bound is independent of the refinement
    centres.
  - The product-over-distinct-tuples inequality, (8.22), Markov, and the existence of a good sample (8.23).
  - The refinement count W² = 𝒵^{o(1)}, rich points and (8.25).
  - The Siegel step: index ≤ ∏ p^{(D₀+1)|T_p|}, giving log H_P = O(R/L⁴). I redid this as
    ≈ 2ξR/(α_min L⁴).
  - (8.27): log|P(q,b_q)| ≤ 2R/L, versus c₅n_p log R ≍ c₅ξR, which forces P(q,b_q) = 0.
  - The extraction exponents: R⁴𝒵⁴S_q^{−1/3} = z^{(13α−2)/3}, and R²𝒵⁶/S_q = z^{3α−2}. Both are negative for
    α ≤ 1/100.
  - Line heights (8.29); g | q (8.30); the nonaligned primes of q divide g (8.31).
  - The pair-collision bound (8.32)–(8.33).
  - The final dichotomy. If A/D ∉ 𝒜, the aligned primes would supply ≥ (c₅ − o(1))n_pN incidences, which forces
    A/D ∈ 𝒜. If A/D ∈ 𝒜, aligned pairs on the line are structured. Either way this contradicts c₅n_pN incidences.
    The logic is not circular.
- Lemma 8.3, every case:
  - a non-real factor: Bézout with its conjugate;
  - a real factor: Q_{X₁}, Q_{X₂} ≢ 0; Q | 𝓘_Q forces a line; extension of graphs between marked abscissae; the fibre
    bound d;
  - the Jarník step: distinct integer difference vectors, total ℓ¹ length ≤ 2S, O(T²) vectors of length ≤ T, hence
    m ≪ S^{2/3}.
  - Lemma B.3 (Bézout) checked as stated and proved.

**§9.**
- (9.1)–(9.11): every identity checked. Points covered:
  - C₀ ∈ ℤ, (C₀, H) = 1 (including primes common to D and q_{f,E}), T/H ≤ 𝒵¹²;
  - m₀ in (9.5) and the progression (9.6);
  - the common interval lies inside every allowed j-interval;
  - (9.9), including the fact that t ≤ w with t | H are exactly the small primes of D.
- Lemma 9.1, both parts: checked.
- Prop. 9.2, range 1:
  - X₁Y₁ ≪ ξRH, Y₁ ≫ ξT, X₁ ≥ R/𝒵^{O(1)};
  - the residue class of p mod HT₀T₁ is a unit, and φ(HT₀T₁) = φ(H)T₀φ(T₁);
  - Brun–Titchmarsh at modulus ≤ R^{4/5+o(1)} with length R^{1−o(1)};
  - the domination constant X₁Y₁/(ξRH) is absolute;
  - the local factors are exact at T₀ (p mod t is determined by m);
  - (9.17), and the fundamental lemma at level w^{A₁} with remainder relative to the main term
    ≪ Y₁^{−3/4}w^M(log w)²;
  - the order ζ → A₁ → M → C_s, all fixed before ξ.
- Prop. 9.2, range 2:
  - block count 𝒵^{O(1)}, Y₂ ≤ 3H;
  - Lemma A.1's hypotheses hold in this application: T₀ squarefree with primes dividing H, (T₁, HT₀) = 1, H ≥ 2,
    (C₀, H) = 1, l squarefree with (l, HT₁) = 1;
  - the main term multiplied by the sieve product gives (9.24);
  - the error R^{9/10+o(1)} = o(n_p);
  - each prime has a unique pattern (k ≡ k₀ mod T₀ from pm₀ = C₀ + Hk);
  - uniform patterns give exactly independent uniform forbidden j-classes.
- Cor. 9.3: the order σ → F → σ₂ → C_s; the discarded mass is H_e(σ + CFσ₂)C′_K B⁻²; the nonaligned primes are
  ≤ w^{C_s}; |A| ≤ 2Yw^{C_s}.

**Numerics.** All runs used ulimit -v 8 GB and nice 19. Scripts are in /tmp/oaimath/021/seats/R2_work/.

- **N1 `n1_pairfactor.py` — the pair factor (9.12).** The exact independent-model pair probability matches (9.12)
  for every h < 200 at w = 13. The control, replacing 1/(t−2) by 1/(t−1), mismatches 61 of 199. The truncated
  identity ∏_{2<t≤w}(1 − 1/(t−1)²)(1 + 1/(t(t−2))) = 1 holds exactly at w = 13, 50 and 200. The control version gives
  0.8554.
- **N2 `n2_variance.py` — Lemma 9.1.** Exact relative variance in the independent model.
  - J = w^{1.5}: 0.0142, 0.0071, …, 8e−5 as w runs 11 → 797.
  - J = w: 0.116 → 0.0028.
  - Control with J = 12 fixed, which violates J ≥ w^δ: the relative variance grows 0.09 → 0.67. So the uniformity
    hypothesis is necessary, and the decay is not an artefact.
- **N3 `n3_orth_largesieve.py` — (8.18) and the large-sieve step.** The identity is exact to 1e−10 at u = 17, 19, 23.
  The control including a = 0 is off by m², which is 330,625 here. The large-sieve sum over a prime bin is
  ≤ (J + 4U²)m in all cases tried (ratios 0.002–0.008).
- **N4 `n4_coords_toy.py` — a faithful toy of §9.1.** Actual classes, actual hit progressions, primes p ∈ [3000, 3600],
  q_f = 17·19·23, D ∈ {1, 3}.
  - The direct survivor count on the common interval equals the count from (m₀, k) via (9.9) for all 73 primes in
    all four configurations. The asserts k ↦ n₀ = b + q_f k, m₀ ∈ [C₀/p, C₀/p + H) and pm₀ ≡ C₀ (mod H) all pass.
  - Control (m₀ + 1): it mismatches 20–73 of 73.
  - Dichotomy. With large T (|C₀|/R ≈ 3·10⁵), the empirical second moment over p is 0.0068 against the model's
    0.0079, and 0.146 against 0.167. With T = 1 (C₀ = 1, H = 1, small classes aligned to A/D), S/JV₀ = 0.521 for
    every p: a constant bias. That is the hard-endpoint case Cor. 9.3 hands to §10; Prop. 9.2 correctly excludes it
    via T > w^{C_s}.
- **N5 `n5_list.py` — Prop. 8.2's list mechanics.** Toy bin of 75 primes in [2000, 2600], with adversarial classes
  aligning 8 rationals. Across all 2,181 reduced rationals with D < 30, |A| ≤ 60:
  - common aligning primes ≤ log|A₁D₂ − A₂D₁|/log R for every pair (0 violations);
  - control: a non-reduced duplicate has determinant 0 and shares all its aligning primes;
  - the list size is 8 against the bound 2/c_p² = 139–800.

## 4. What I could NOT check

- The §5 path estimates used in Prop. 7.2's proof. These are Prop. 5.5(i)–(ii) (compact mass O_K(B⁻²) and the
  compact-history conversion), Lemma 5.2 (high states), Prop. 5.3 (coupling: N⋆ = O((log B)³) steps,
  h₀ < every negative power of log B), Lemma 4.3 (regeneration, exponential moments), and Lemma 4.6 (band bounds,
  ratio tails uniform in B). In particular, the claim that C_th and the density and band constants are independent
  of ξ rests on these lemmas. That is outside my scope.
- Lemma A.1 (Kloosterman completion, error τ(N)²log²(2N)√(NT₀)(1 + X/(lN) + Y₂/N)) and Lichtman 2022, Lemma 7.1,
  which it uses. I checked only that its hypotheses hold where Prop. 9.2 applies it.
- Lemma 2.1 (dimension-two fundamental lemma; source Sofos 2023 / Friedlander–Iwaniec Cor. 6.10, not accessed).
  I checked only that its hypotheses (g(p) ≤ 2/p, g(2) ≤ 1/2, the empty-case exception) are met in each use.
- Gallagher 1971, Gallagher 1976 and Walsh 2014 were not available as files. None is load-bearing, since the text
  reproves each step it uses. Jarník 1926 (§§1–2, Satz 1 via (x)-systems of distinct difference vectors) and
  Helfgott–Venkatesh §2 (the larger-sieve difference product) were read, and match what is attributed.

## 5. Where a hole would most likely hide

Inside my scope, the most fragile point is not in §8. It is in Prop. 7.2's "isolated position" exclusion. Every
regular compact endpoint must carry a singleton-bin factor with exponent in [α_min B, α_max B], where α_max = 1/100.
All of §8's exponent bookkeeping depends on this: z^{(13α−2)/3}, z^{3α−2}, and log S_q ≈ (2−α)L.

The paper gets this from a crossing argument. A path from gap ≈ 2B to a fixed compact must arrive in
[.4θB, θB], θ = α_max/4, and the arrival's ratio is ≤ T except on a set whose probability → 0 uniformly in B as
T → ∞ (the band bounds). The crossing step is airtight. The burden is entirely on the uniform ratio-tail bound and on
the compact-history conversion (cost C_K B⁻² × probability), both from §4–§5. I believe it holds: the deterministic
part (gap retention ≥ 1/2 per step, hence an arrival in a band of fixed proportion) is correct as written. But this is
the single place where a defect in another section would propagate into a positive-mass set of compact endpoints that
§8 cannot treat.

Within §8 itself, I looked hardest for three things: an implicit average over classes, a list depending on the failure
set, and a numerology slip in the Siegel/divisibility/extraction exponents. I found none. The construction has large
slack: polynomial-in-L savings against 𝒵-losses, and K_p/p ≤ w^{−12} ≪ L^{−6}.
