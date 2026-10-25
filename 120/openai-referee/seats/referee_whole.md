# Referee report — YOURTAG = whole

Scope: whole-paper hostile read of the GEOMETRIC paper ("The geometric case of the Erdős similarity conjecture", OpenAI, 5 Oct 2026, 13 pp; /tmp/erdos0300/geometric.pdf), then the DYADIC paper (25 Sep 2026, 16 pp) as second witness. Aim: why the geometric case stayed open from 1974 to 2026, and what in this argument gets past the obstruction.

Method: I read both papers in full from the text extractions and checked every displayed formula in §§2–5 of the geometric paper against the rendered PDF (pp. 4–12). I re-derived every inequality by hand. Then, as an independent instrument, I ran a small exact-arithmetic Monte Carlo of the paper's own construction (written from the definitions, never from code in the papers) on six small instances, with two negative controls that are built to fail (§F). Sources fetched: Chlebík arXiv:1512.05607v1 (read §§3 and 5, Prop. 1, Thm 15, final remarks); Kolountzakis–Papageorgiou arXiv:2208.02637v2 (read §3.1).

---

## A. The obstruction and the mechanism that gets past it

### A1. The standard random-cell attempt, and exactly why it fails for G_q

Normalize as the paper does (§2): it is enough to build, for every p > 0, a 1-periodic open H with ρ(H) = O(p) that meets x + tG_q for every x ∈ ℝ and every t ∈ [1,2]. The global step then needs Σ_k ρ(H_k) < η over all dyadic bands k ∈ ℤ, so **ρ(H) must go to 0**. A fixed small density is not enough; this is the real constraint.

*Version 1 (independent layers).* B = ∪_n B_n, with B_n a random union of cells at resolution about q^{−n}, independent across n, density p_n. For a fixed (x,t), P(x + tq^n ∉ B ∀n) ≈ Π(1 − p_n). If Σp_n < ∞ (needed for small measure), this product is bounded below, so each (x,t) is missed with probability bounded away from 0. If Σp_n = ∞, B has full density. Dead either way.

*Version 2 (one window, one resolution; Kolountzakis/Chlebík style).* Take a window of r consecutive indices [a,b] and one random set of density p at resolution N ≈ c q^{−b}, fine enough to separate x + tq^n, n ∈ [a,b]. Then:
- At a fixed (x,t) the r test points lie in distinct cells, so the miss probability is exactly (1−p)^r.
- As t runs over [1,2], the first point x + tq^a sweeps about q^a·N ≈ c·q^{−r} cells. So the number of distinct scale configurations is about r·c·q^{−r}.
- The union bound is r·c·((1−p)/q)^r. This tends to 0 only if **p > 1 − q**. The heuristic is not just the union bound's weakness: the expected number of missed configurations really diverges when (1−p)/q > 1.

So p cannot be taken small, and the global step fails. In Chlebík's language (his Theorem 15; see §G), m points with normalized minimum gap δ need −log δ = o(m). For G_q, −log δ ≈ m·log(1/q), linear in m. The paper's §1.1 computation of this (normalized gap ≤ q^{m−2}/(1−q)) is correct.

*Version 2′ (several windows, independent sets).* Split the budget over M−1 windows of length r, each with its own random set of density p/(M−1) at its own resolution. Scale counts now ADD, giving (M−1)·r·q^{−2r}, but the failure is (1 − p/(M−1))^{(M−1)r} ≈ e^{−pr}. You need p > 2·log(1/q). No gain.

Chlebík's own 2015 remark puts the target precisely. Universality of a bounded X with 0 ∈ X is equivalent to a bound λ{a : {a}×[1,2] ⊆ L_X(G)} ≤ C·λ(G). Here L_X(G) is Chlebík's notation for the set of pairs (a,b) with (a + bX) ∩ G ≠ ∅, so {a}×[1,2] ⊆ L_X(G) means G meets a + bX for every b ∈ [1,2]. The paper's (5.6)/(5.7) shows this ratio is at least (1 − 3p)/(2p) → ∞ for X = G_q ∪ {0}. That is exactly the quantity nobody could make large for a geometric sequence.

### A2. The mechanism in §4 that breaks it

1. **Density is spent once; resolution is free.** Every point z reads exactly one terminal Bernoulli-p entry. The routing only decides which one (Lemma 4.1: P(z ∈ B | A) = p, where A is the σ-field of all selector entries). Selector tables at arbitrarily fine grids cost no measure. So Eρ(B) = p exactly, for any tree. B is a finite union of half-open cells of the finest grid per period, hence 1-periodic and Borel. Verified.
2. **Conditioning on the centre's own route amplifies the local share.** Globally, the points routed to child i of a vertex U are a 2^{−i} share of those reaching U. At a stable centre x whose first default is at U:
   - x's coarse keys are inherited by y_n(t) = x + tq^n for every n ∈ W_{e_i}, by (3.3).
   - So y_n(t) reaches U and inherits x's zeros on (U,1), …, (U,i−1).
   - Its bit on e_i = (U,i) is read at the finer grid b_{e_i} at a fresh address (Lemma 3.3).
   - So it enters child i with conditional probability 1/2, not 2^{−i}, and then hits B with probability p.
   - This gives (M−1)r conditionally independent tests of success p/2 (Lemma 4.3, an exact identity).
3. **The scale count stays local.** Test i depends only on the key at b*_{e_i} ≤ a_{e_i} + 2r − 1 (Lemma 3.1). That is because the window length r_h is at least the following gap plus the whole child-subtree span, and later siblings' finer grids are never consulted by a successful local test. Per pair (i,n) the count is ≤ 1 + 2c·q^{−2r}, so the total is about (M−1)·r·4c·q^{−2r}.

Failure × count ≈ (M−1)·r·4c·[q^{−2}(1 − p/2)^{M−1}]^r. **M can push the base (1 − p/2)^{M−1} below q², while the scale base q^{−2} does not depend on M.** That is the whole trick: increasing the branching increases independent tests multiplicatively and the scale count only linearly.

- Depth d makes a default somewhere on the route likely: (1 − 2^{1−M})^d < p.
- Depth costs only K (the number of edges), hence only g (the gap length), and g is absorbed into r_h by the span condition. Since every r_h ≥ r_*, the trade-off holds at every height with the same bases.

### A3. Trying to break it: shared randomness across t and across x

- **Across t.** All scales use the same tables. Lemma 5.1 needs no independence across t: it uses the union bound over a finite set T_{x,ξ} that depends only on (x, U), and U is F_x-measurable. Each t′ ∈ T_{x,ξ} is a constant on the atom ξ, and Lemma 4.3 is an identity at each such constant. I found no way the shared randomness re-enters.
- **Across x.** Only per-centre probabilities are used, through linearity of expectation (Fubini on a finite Ω times [0,1)): Eρ(R) ≤ 2p·ρ(S) + ρ(ℝ∖S) ≤ 3p. One outcome with ρ(B⁺) + ρ(R) ≤ 5p is then fixed. For that outcome R is closed (a finite intersection of closed preimages, projected out of the compact (ℝ/ℤ)×[1,2]) and is covered by an open V with ρ(V) ≤ ρ(R) + p. For x ∈ R ⊆ V, x + tq^n ∈ V for all large n. **No measure-zero claim appears anywhere.** The exceptional set has positive measure (≤ 3p) and is repaired by an open set. Verified.
- **Adaptive conditioning, with explicit σ-fields.** Ω is a finite product. F_x = σ(S_e(J_{b_e}(x)) : e non-default) ⊆ A = σ(all selector entries) ⊆ 2^Ω. The terminal entries are independent of A.
  - U, h, r, e_i, W_{e_i}, b*_{e_i} and T_{x,ξ} are all F_x-measurable.
  - A_{i,n}(t) is A-measurable. On ξ it is a function of unexposed coordinates of S_{e_i} only, at pairwise distinct addresses that are also distinct from the single exposed address (e_i, J_{b_{e_i}}(x)) by Lemma 3.3. Entries exposed in other tables are irrelevant to A_{i,n}.
  - L_{i,n} and κ_{i,n} are A-measurable.
  - P(F_t | ξ) = E[P(F_t | A) | ξ] is legitimate because ξ ∈ F_x ⊆ A. P(F_t | A) = (1−p)^{ΣA_{i,n}} on ξ, because the addresses κ_{i,n} are distinct for every selector realization.
  - E[(1−p)^{ΣA} | ξ] = Π_{(i,n)} (1/2 + (1−p)/2) by conditional independence on ξ.
  - **No quantity treated as fixed is random.** Nothing requires selectors read below U to be fresh: the proof conditions on all of A. Below U they cannot coincide with x's exposed entries anyway, because separation persists at finer grids.

---

## B. "Prove too much" tests

### B(a) A finite pattern (Steinhaus: every finite set is universal)

Infinitude of G_q is used in **two** places, not one:

1. **Unbounded index sets as p → 0.**
   - Prop. 2.1 at density p needs r_* → ∞ and d → ∞ as p → 0, so |N| ≥ K·r_* → ∞.
   - §2 needs Prop. 2.1 for p_k = η·4^{−|k|}/64 → 0.
   - A pattern with m points supports the construction only for p above an m-dependent threshold, so §2 cannot be run.
2. **The repair.** x + tq^n ∈ V for all large n, with indices outside N. This needs infinitely many n and tq^n → 0.

With p fixed and N ⊆ {1,…,m}, the argument through (5.6)/(5.7) proves a TRUE finite statement: at scales t ∈ [1,2], all but a closed set of centres of density ≤ 3p are hit. This is consistent with Steinhaus, whose copies sit at scales s → 0, i.e. at k → −∞ in §2. Those scales need p_k → 0 (step 1), and each H_k's own exceptional centres are repaired only by indices beyond N_k (step 2). **No false finite statement is proved.**

### B(b) An arbitrary null sequence a_n ↓ 0

The geometric ratio enters at **three** places. The brief names two; Lemma 3.2 is a third.

- **Lemma 3.2 (stability density)** needs N_{b′}·a_{b′+g+1} small uniformly. Geometric: 2N_{b′}q^{a_e} ≤ 4c·q^{g+1}.
- **Lemma 3.3 (separation)** needs 1/N_b < min(a_b, the minimum within-window gap). Geometric: 1/N_b ≤ (1−q)q^b/4 < (1−q)q^b.
- **(5.3) (scale count)** needs a_{a_e}·N_{b*_e} ≤ C·e^{βr} with β < α = p(M−1)/2, uniformly in the window position a_e. Geometric: 1 + q^n·N_{b*} ≤ 1 + 2c·q^{−2r}, independent of a_e.

How other sequences fare:
- **Ratio → 1 (Falconer–Eigen; known).**
  - Example a_n = 1/n. Separation forces N_b ≳ b².
  - Lemma 3.2 then needs b′²/(b′+g) small, which fails at fixed g as b′ → ∞.
  - (5.3) gives about (a+2r)²/a, which grows with the window position.
  - So the proof as written does not run. It would need position-dependent gaps, or a pass to a lacunary subsequence.
  - No danger here: the class is known.
- **Ratio → 0 (super-geometric).**
  - Example a_n = q^{n²}: (5.3) becomes a_a/a_{a+2r} = q^{−4ar−4r²}. That is superexponential in r and grows with a, and no choice of M beats it.
  - The method fails irreparably here.
  - These are subsets of G_q, and non-universality passes to supersets, not to subsets. So the theorem says nothing about them.
- **Conclusion.** The method does not prove the full conjecture.
  - Its natural reach appears to be lacunary sequences with ratios in a fixed [q₁,q₂] ⊂ (0,1). The three bounds above survive with q₁, q₂ in place of q. I did not write this extension out.
  - By passing to supersets, that reach would cover every positive null sequence with liminf a_{n+1}/a_n > 0.
  - That is a strong but not suspicious consequence. It is not claimed by the paper, and the super-lacunary case stays open.

### B(c) q → 1 (c = 4/(1−q) → ∞)

Every constant is finite for each fixed q:

| Constant | Behaviour as q → 1 | Behaviour as q → 0 |
|---|---|---|
| n₀ | about log 8 / log(1/q) → ∞ | |
| c = 4/(1−q) | → ∞ | |
| N_b | nondecreasing powers of 2; consecutive b may share an N_b, which is harmless | |
| M | as small as 2 once p/2 > 2·log(1/q) | about 4·log(1/q)/p → ∞ |
| d | finite (needs (1 − 2^{1−M})^d < p) | enormous, but finite |
| g | about log(4Kc/p)/log(1/q) → ∞ | |
| r_* | finite, since D·e^{−αr} → 0 because α > 2·log(1/q) | finite |

The O-constant in (5.5) depends on M and c, which are fixed before r_*. The proof is **not uniform in q** at either end, but nothing is infinite for any fixed q, and ρ(H) ≤ 6p holds uniformly. The abstract's "the set may depend on q" is accurate.

---

## C. Dyadic (25 Sep) vs geometric (5 Oct), paragraph by paragraph for §4

| Dyadic | Geometric | Comparison |
|---|---|---|
| §4.1 tables, B, (11) | §4.1, Lemma 4.1 | Identical argument (S ↔ A). |
| §4.2 F_x (12), Lemma 4.1 "= (1−2^{1−M})^d < p" | §4.2 (4.2), (4.3) "= (1−2^{1−M})^d" | Geometric drops the "< p" only because the parameters are not yet chosen there. It is restored at (5.4)ff. Not a weakening. |
| §4.3 "Routing trials through the first default", Lemma 4.2 + Fig. 2 | Second half of §4.2, Lemma 4.2 | Same proof. The dyadic adds "Later sibling selectors at an ancestor are not needed to make its choice", which is implicit in the geometric "reads zeros at indices less than a and one at a". Nothing dropped. |
| §4.4 Lemma 4.3 (separation inline: distances ≥ 2^{−b}, cell 2^{−(b+2)}, a ≥ 3) | §4.3 Lemma 4.3 (separation delegated to Lemma 3.3) | Equivalent. The dyadic adds "even for pairs with A_{i,n} = 0" and "The empty-success case has exponent zero"; both are cosmetic. |
| (3): 20Mr(1 + 2^{2r+2})·e^{−p(M−1)r/2} < p, with p(M−1)/2 ≥ 10 | (5.1)/(5.5): D = 4 + 2(M−1)r(1 + 2c·q^{−2r}), with p(M−1)/2 > 2·log(1/q) | Different constants, both correct. Dyadic count: 2^{b*+2−n} ≤ 2^{2r+1}, written as 2^{2r+2}. Geometric at q = 1/2: q^n·N_{b*} ≤ 2^{2r+2}, written as 2c·q^{−2r} = 2^{2r+4}. The dyadic "≥ 10" is a stronger demand chosen for a clean r_* > log(100M/p)/7. I re-checked 1 + 2^{2r+2} ≤ 5e^{2r} and r ≤ e^r, so LHS ≤ 100M·e^{−7r}. |

Two further differences:
- **The grids at q = 1/2 are different.** Geometric N_b = 2^{⌈log2(8·2^b)⌉} = 2^{b+3}; dyadic N_b = 2^{b+2} by (6). So the geometric construction at q = 1/2 is **not** the formalized dyadic construction (see Objection 4).
- **§6 vs §2.** Dyadic §6 uses only contracting copies 2^{−j}H_j (j ≥ 1) plus an index shift N = n + j − k. That shift needs scale 2 = 1/q. Geometric §2 uses k ∈ ℤ, two-sided, with the 4^{−|k|} weights, and needs no algebraic relation between 2 and q. Both verified; 7η/16 and η/2 recomputed.

**No mathematical claim is weakened or dropped between 25 Sep and 5 Oct.** Expository changes:
- The geometric paper drops the remark on the withdrawn Cruz–Lai–Pramanik preprint and the remark on IKMC Prop. 3.2.
- It adds Tom [Tom15].
- It re-attributes the open-neighbourhood repair from Kolountzakis [11, §§2.2, 3.2] to Tom Lemma 0.2 plus Chlebík; see Objection 2.

---

## D. Every "indeed / thus / hence / therefore / consequently / it follows" in the geometric paper (from grep; plain-text line numbers)

Every inference marker was reproduced. None needed more than a minute except Lemma 4.3 and Lemma 5.1, which I did in full.

| Line | Inference | Status |
|---|---|---|
| l.42 | "Indeed": m(∩_{a∈F}(A − sa)) → m(A) | ✓. m(A ∖ ∩) ≤ Σ_a m(A ∖ (A − sa)) → 0 by L¹ continuity. |
| l.74 | "therefore at most q^{m−2}/(1−q)" | ✓. Min gap < a_{m−1} ≤ q^{m−2}a₁, and a₁ − a_m ≥ (1−q)a₁. |
| l.188, l.214 | (2.3) and m(E) > 1 − η | ✓. 12·(η/64)·(1/3 + 1 + 1) = 7η/16. Pieces: k ≤ 0 gives exactly ρ(H_k) per sign; k > 0 gives ≤ 2^k·ρ(H_k). |
| l.220, l.224 | Rescaling and reflection | ✓. 2^{−k}x + tq^n ∈ H_k ⇒ x + sq^n ∈ 2^kH_k. For s < 0 use C = −C. A hit outside [0,1] is still a point not in E. |
| l.246, l.252 | Half-open cells; nesting | ✓. ⌊⌊y⌋/m⌋ = ⌊y/m⌋ for integer m; N_b nondecreasing because c·q^{−b} is increasing. |
| l.268, l.300, l.302 | Preorder blocks; span r_h + g + σ_{h−1} ≤ 2r_h | ✓. Recomputed from the recursion. |
| l.360–361 | No boundary of Γ_{b′} in (x, x+tq^n] ⇒ equal J_{b′} keys | ✓. tq^n ≤ 2q^{a_e} for n ≥ a_e. Γ_{b′} ⊇ ℤ, so wrap-around is a crossing. A left-boundary x lies in its right cell. |
| l.376, l.392 | Separation | ✓. Length ≤ 2q^{n₀} ≤ 1/4 < 1/2, so circular distance = real distance. Pairwise ≥ (1−q)q^b > q^b(1−q)/4 ≥ 1/N_b. |
| l.433 | B periodic, finitely many half-open cells | ✓. |
| l.458, l.467 | Atoms keep the product law on unexposed coordinates; (4.3) | ✓. The tables at each vertex are disjoint from the ancestors' tables. |
| l.495, l.510 | Lemma 4.2 | ✓ (§E). |
| l.531–545 | Lemma 4.3 | ✓ (§A3, §F). |
| l.635, l.646 | \|T\| ≤ D; fail at t ⇒ fail at some t′ | ✓. \|T\| = 2L − 1 ≤ 3 + 2(M−1)r(1 + 2c·q^{−2r}) < D. |
| l.676 | r_* exists | ✓. Limit 0 ⇒ eventually < p for all larger r. |
| l.711, l.722, l.744 | R closed; Eρ(R) ≤ 3p; hitting | ✓. |

---

## E. Lemma-by-lemma status

### Geometric paper

| Item | Status | Notes |
|---|---|---|
| §1.1 Steinhaus remark; Chlebík-criterion failure computation | VERIFIED LINE BY LINE | |
| §2 Proof of Thm 1.1 from Prop 2.1 (C open and symmetric, E compact, (2.3) = 7η/16, reduction s = 2^k t, centre 2^{−k}x, s < 0, hit outside [0,1]) | VERIFIED LINE BY LINE | |
| §3 window assignment, r_h/σ_h recursion | VERIFIED LINE BY LINE | Preorder ⇒ endpoints strictly increasing along the global list, consecutive windows a_e = b′ + g + 1, so every edge f preceding e has b_f ≤ b′. |
| Lemma 3.1 | VERIFIED LINE BY LINE | |
| Lemma 3.2 | VERIFIED LINE BY LINE | Density ≤ 2N_{b′}q^{a_e} ≤ 4c·q^{g+1} per window, ≤ (K−1) windows. (3.3) via nesting. |
| Lemma 3.3 | VERIFIED LINE BY LINE | |
| §4.1 + Lemma 4.1 | VERIFIED LINE BY LINE | Eρ(B) = p exactly. |
| (4.2), (4.3) | VERIFIED LINE BY LINE | |
| Lemma 4.2 | VERIFIED LINE BY LINE | See below. |
| Lemma 4.3 | VERIFIED LINE BY LINE | All three distinctness cases. The conditioning order is legitimate. The equality is exact. |
| Lemma 5.1 | VERIFIED LINE BY LINE | See below. |
| Proof of Prop 2.1 | VERIFIED LINE BY LINE | See below. |
| §1.2 mechanism prose | READ | Consistent with the proofs. |

Lemma 4.2 detail. At every strict ancestor P of U, x's choice a < M:
- (P,a) precedes e_i because e_i lies in P_a's subtree.
- (P,j) for j < a precedes it with its whole block.
- At U, (U,j) for j < i precedes (U,i).
- All of these have b ≤ b′ = the predecessor endpoint of W_{e_i}, so (3.3) applies.
- It holds for every t ∈ [1,2] simultaneously. This t-invariance is what keeps coarse grids out of the scale count.

Lemma 5.1 detail:
- Q_i reads only S_{e_i} at b_{e_i}, selectors on edges of the subtree of U_i, and a terminal table of a leaf of that subtree. All of these have resolution ≤ b*_{e_i}. **No finer table is consulted.**
- Breakpoints: ≤ 1 + q^n·N_{b*} < 1 + 2c·q^{a_e − b*} ≤ 1 + 2c·q^{−(2r−1)}, with n ≥ a_{e_i} and b* − a_{e_i} ≤ 2r − 1.
- T_{x,ξ} is F_x-measurable.
- Breakpoints and midpoints represent every t, including boundary values and the endpoints 1 and 2.

Proof of Prop 2.1 detail:
- Parameter order: M(p,q) → d(M,p) → K(M,d) → g(K,c,q,p) → r_*(M,q,p) → r_h(r_*, g, M). There is no circularity: neither g nor r feeds back into K or M.
- r_h ≥ r_* for all h, including h = 1 (r₁ = r₀ = r_*).
- (5.5) follows from α > 2·log(1/q) using 1 − u ≤ e^{−u}.
- (5.6) ≤ p + p.
- B⁺, Eρ(B⁺) ≤ 2p; R closed; Eρ(R) ≤ 3p via ρ(ℝ∖S) < p; choice of outcome; V by outer regularity; ρ(H) ≤ 6p; hitting for x ∉ R (an index in N) and x ∈ R (indices beyond N).

### Dyadic paper (second witness)

| Item | Status |
|---|---|
| (1)–(5) and the r_* bound | VERIFIED LINE BY LINE |
| Lemma 3.1 (2^{b′+2}δ_e = 2^{2−g}) | VERIFIED LINE BY LINE |
| §4.1 / (11) | VERIFIED LINE BY LINE |
| Lemma 4.1 | VERIFIED LINE BY LINE |
| Lemma 4.2 | VERIFIED LINE BY LINE |
| Lemma 4.3 | VERIFIED LINE BY LINE |
| Lemma 5.1 (16) | VERIFIED LINE BY LINE |
| Prop 5.2 | VERIFIED LINE BY LINE |
| §5.1 (19)–(23), including the explicit ε-neighbourhood repair | VERIFIED LINE BY LINE |
| §6 (Σ = η/2; index shift N = n + j − k ≥ n because j = max(1,k) ≥ k) | VERIFIED LINE BY LINE |
| §1 introduction and citations | SKIMMED |

---

## F. Independent numerical check (an instrument that can fail)

Script: /tmp/erdos0300/whole_sim/sim.py (+ rerun.py, forceroot.py). Python Fractions, so no floating-point keys. The script implements: the tree; preorder windows with gap g; N_b = the least power of 2 ≥ c·q^{−b}; stability exactly as defined; lazily sampled fair selector and Bernoulli-p terminal tables; routing; Q_i as in (4.4).

For random stable x, random t ∈ [1,2] and fresh tables, it checks two things:
- **(a) Lemma 4.2's implication Q_i(y_n(t)) = 1 ⇒ y_n(t) ∈ B,** by routing y_n(t) from the root.
- **(b) The all-fail frequency, grouped by the height of U, against (1 − p/2)^{(M−1)r_h}.**

| Configuration | Lemma 4.2 checks / violations | All-fail observed vs exact (z) |
|---|---|---|
| q = 1/2, M = 3, d = 2, g = 10 | 1379 / **0** | h=1: 0.901 vs 0.904 (−0.2); h=2 (72 tests): 0.146 vs 0.162 (−1.1) |
| q = 3/5, M = 3, d = 2, g = 14 | 1517 / **0** | h=1: 0.919 vs 0.922 (−0.3); h=2 (96 tests): 0.157 vs 0.144 (+1.1) |
| q = 1/3, M = 3, d = 2, g = 6 | 1172 / **0** | h=1: −0.3; h=2: +0.3 |
| q = 1/2, M = 4, d = 2 (three seeds) | 889 + 1348 + 1473 / **0** | h=2 pooled 0.100 vs 0.1135 (z ≈ −1.7). Re-tested by conditioning directly on the root-default atom, 6000 samples each: p = 0.0096 gives 0.5022 vs 0.5001 (+0.3); p = 0.03 gives 0.1128 vs 0.1135 (−0.15). The −1.7 was noise. |
| q = 1/2, M = 2, **d = 3** (deeper ancestors, preorder across 3 levels) | 2973 / **0** | h=1: −0.4; h=2: −0.9; h=3 (116 tests): +0.1 |

P(no default) matched (1 − 2^{1−M})^d in every run (largest |z| ≈ 2.1 over nine runs).

Negative controls, built to fail:
- **Unstable centres.** x placed just left of a Γ_{b(root,1)} point, so that translates from W_{(root,2)} cross it. Lemma 4.2's implication fails **361 times in 2133**. The instrument can see a route-preservation failure.
- **Selectors read at a coarse grid (a_e − 6).** This breaks separation. All-fail is **0.898 vs 0.162 (z = +56)**. The instrument can see a dependence failure. It also cleanly separates the wrong formula (1−p)^{(M−1)r} from the right one in every positive run.

This corroborates the two novel lemmas on the paper's own construction. It does not test Lemma 5.1's union bound, whose breakpoint set at the root is about 10^22 points here; that lemma I verified by hand.

---

## G. Citation table (my scope)

| Cited result | Paper's claim | Source says | Verdict |
|---|---|---|---|
| Chlebík arXiv:1512.05607v1, Thm 15 | A bounded infinite set is nonuniversal if it contains arbitrarily large finite subsets with −log(min gap/(a₁ − a_m)) = o(m). | "Theorem 15. Let X ⊆ R be a bounded infinite set which contains, for arbitrarily small σ > 0, a subset {x1, …, xn} with x1 > x2 > · · · > xn, n ≥ 3, and min (xi − xi+1)/(x1 − xn) ≥ (1 − σ)^n. Then X is non-universal …"; proof: "(which by our assumptions can satisfy − log δ = o(n) with n → ∞)". | MATCH |
| Chlebík §3 final remark; Prop 1(vi), (viii) | "Open-neighborhood repair for null sequences … see also Chlebík [Chl15, Section 3, final remark …]" | "Using the fact that 0 ∈ X, we can add to H that small set of a's in [0, 1] for which {a} × [1, 2] is not covered by L_X(H) and conclude non-universality of X this way." That is repair by adding the centres for X ∋ 0, not an open neighbourhood for a null sequence. Prop 1(viii) is open-set approximation, which is relevant. | LOOSE ("see also"); the dyadic paper's wording was accurate. Objection 2. |
| Chlebík §5 final remark (context, not cited) | — | "the universality/non-universality status is known for no zero-sequence {x_k} that decreases geometrically or faster" | Confirms the problem's status as of 2015. |
| KP25 (arXiv:2208.02637v2) §3.1 | Fixed-centre scale discretization and integration of exceptional-centre probabilities; treats unbounded sequences. | §3.1: fixed x; "it is sufficient to check whether such a t exists in a finite set S = S(x)", made of interval-endpoint crossings; then E\|B\| = ∫ P(…) dx; sequences with (x + tA) ∩ [−N,N]. | MATCH |
| Kol97 Thm 3; Fal84; Eig85; HL98; Bou87; MCIK+26; IKMC+26; CLP23; FLX24; Tom15; Sol11 | Background | Not fetched. Kol97 is described consistently by Chlebík §5. Tom15 and Sol11 are unpublished reports. | COULD NOT FETCH (not load-bearing; the proof is self-contained) |

---

## Objections (numbered)

1. **COSMETIC (exposition).** §3 "Assigning the windows" and "Preserving earlier keys", p. 5.
   - Quoted: *"Assign an integer interval W_e = [a_e, b_e] ∩ ℕ to each edge, in preorder, leaving exactly g unused indices between consecutive windows."* … *"Call x ∈ ℝ stable if, for every window W_e other than the first, writing b′ for the endpoint of its immediate predecessor, (x, x + 2q^{a_e}] ∩ Γ_{b′} = ∅."*
   - Problem: "immediate predecessor" must mean the predecessor in the **global preorder window list**. Read as the tree-parent edge, (3.3) would be false, because earlier sibling subtrees use finer grids than the parent. The relation a_e = b′ + g + 1 first appears inside the proof of Lemma 3.2 (p. 6).
   - Under the intended reading everything holds, and the density computation forces that reading.
   - Fix: write "immediate predecessor in the preorder list, so a_e = b′ + g + 1" in the definition.

2. **COSMETIC (citation precision).** §5, p. 11.
   - Quoted: *"Open-neighborhood repair for null sequences is explicit in Tom [Tom15, Lemma 0.2]; see also Chlebík [Chl15, Section 3, final remark; Proposition 1(vi), (viii)]."*
   - Problem: Chlebík's remark repairs by adding the uncovered centres themselves when 0 ∈ X (quote in §G), not by an open neighbourhood. The 25 Sep dyadic paper said exactly this ("Chlebík also describes adding the centers themselves when the pattern contains zero"); the 5 Oct wording blurs it.
   - No mathematical dependence: the repair is proved in full on p. 12.
   - Fix: restore the dyadic wording.

3. **COSMETIC.** Lemma 5.1 proof, pp. 10–11.
   - Quoted: *"Taking a union bound and using (4.6) gives P(…|ξ) ≤ |T_{x,ξ}|(1 − p/2)^{(M−1)r}, which proves (5.2)."*
   - Problem: (5.2) is stated with e^{−p(M−1)r/2}, so the step silently uses 1 − u ≤ e^{−u}. The dyadic Prop 5.2 writes it out.
   - True and trivial. Fix: one clause.

4. **UNCLEAR (scope of certification, not an error).** Geometric (3.1)ff, p. 4, versus dyadic (6), p. 6.
   - Quoted: geometric *"N_b = 2^{⌈log2(cq^{−b})⌉}"* with c = 4/(1−q); dyadic *"J_b(z) = ⌊2^{b+2}{z}⌋"*.
   - Problem: at q = 1/2 the geometric construction uses N_b = 2^{b+3}, a different M-condition (p(M−1)/2 > 2·log 2 versus ≥ 10), and a different global step (two-sided k ∈ ℤ versus index shift j ≥ 1). So the brief's statement that the dyadic version was formalized in Lean does **not** certify any line of the geometric paper. In particular it does not certify the q-dependent bookkeeping: Lemma 3.2's 4c·q^{g+1}, Lemma 3.3's (1−q)q^b/4, (5.3)'s 2c·q^{−2r}, (5.4)–(5.5), and §2's 7η/16.
   - I re-derived each of these by hand and found them correct.
   - Fix: formalize general q, or say explicitly that the formalization is q = 1/2 only.

**No FATAL and no GAP found.**

---

## Verdict

**HOLDS AS READ** — for the geometric paper (Theorem 1.1, all q ∈ (0,1)) and for the dyadic paper as second witness. Every lemma in both is VERIFIED LINE BY LINE (§E). The two lemmas that carry the novelty (4.2, 4.3) are also corroborated numerically on the paper's own construction, with negative controls that do fire (§F). Each "prove too much" test comes out the right way:
- The finite-pattern version proves only a true statement.
- The method breaks for super-geometric sequences.
- Every constant is finite for each fixed q.

**Credence that Theorem 1.1 is true as stated: 0.95.** The residual is mostly the base rate for a 50-year-old problem combined with the chance of a blind spot I share with the paper. Every individual step is elementary and was reproduced.

**Step I would attack first if forced to bet against:** the "all t ∈ [1,2] at once" pair, Lemma 4.2 together with Lemma 5.1. Specifically:
- the claim that at a stable centre the whole route above U, and the rejections at U, are t-invariant on [1,2], via stability w.r.t. the predecessor endpoint b′ of W_{e_i};
- and that the local test then depends only on J_{b*_{e_i}}.

This is precisely where the 1974–2026 obstruction lived: the scale count costs about q^{−span}. If either claim leaked a coarser or finer grid into the breakpoint count, the count would revert to q^{−(global span)} and the proof would die. I checked both, and Lemma 4.2's t-invariance numerically, and could not break them.
