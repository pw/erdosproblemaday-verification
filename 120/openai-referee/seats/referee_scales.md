# Referee report — seat `scales`

**Paper under review:** "The geometric case of the Erdős similarity conjecture", OpenAI, 5 Oct 2026 (13 pp), `/tmp/erdos0300/geometric.pdf`.
**My scope:** §5 (Lemma 5.1, proof of Proposition 2.1 incl. the open-neighbourhood repair; PDF pp. 10–12) and §2 (the global deduction of Theorem 1.1 from Proposition 2.1; PDF pp. 3–4). Brief item (ix) within that scope. Cross-check against §5–§6 of the DYADIC paper (`/tmp/erdos0300/dyadic.pdf`, 25 Sep 2026, pp. 11–16).
**How read:** every formula in scope read off the rendered PDF pages (pp. 3–12 of geometric, pp. 11–16 of dyadic), not the text extraction. §§3–4 of the geometric paper (pp. 4–9) read in full as the dependencies Lemma 5.1 consumes.
**Computation:** small exact/float Python at `nice -n 19` in `/tmp/erdos0300_scales_scripts/` (scripts: `sum23.py`, `check55.py`, `lemma51_brute.py`, `lib51.py`, `lemma42_check.py`, `mut51.py`, `mut42.py`, `reconcile.py`; outputs `*.out`). Every simulation has a mutant negative control that fails as it should (below).

---

## 1. Verdict for my scope

**HOLDS AS READ** — §2 (proof of Theorem 1.1 from Proposition 2.1, including (2.3)), Lemma 5.1, and the proof of Proposition 2.1 (parameter order (5.4)–(5.5), (5.6), the B⁺/R/V repair and the hitting verification).

This verdict is **conditional on Lemmas 3.2, 3.3, 4.2, 4.3 and formula (4.3)**, which belong to other seats. I read them as dependencies and found no defect in the specific properties §5 consumes (listed in §4 below), but I do not certify them line by line.

I found **no FATAL and no GAP** in scope. All objections below are COSMETIC / exposition-level (true statements with a one-line missing justification that I supply), plus remarks relevant to the global assessment (notably objection 9: the Lean-formalized dyadic paper does **not** certify the geometric paper's §2 or its constants, even at q = 1/2).

---

## 2. Status of each item in scope

| Item | Status | Notes |
|---|---|---|
| Proposition 2.1 (statement, p. 3) | VERIFIED | quantifiers: one H for all x ∈ ℝ, t ∈ [1,2]; n ≥ 1 arbitrary (not restricted to 𝒩) |
| Proof of Theorem 1.1 assuming Prop. 2.1 (§2, pp. 3–4) | **VERIFIED LINE BY LINE** | incl. (2.2), period/measure bound, (2.3) recomputed exactly, compactness, normalization s = 2^k t, center 2^{−k}x, s < 0 reflection, points outside [0,1] |
| (2.3) | **VERIFIED** (exact rational arithmetic, `sum23.py`) | 12·Σ p_k max(1,2^k) = (12η/64)(1/3 + 1 + 1) = 7η/16 exactly |
| Lemma 5.1 (pp. 10–11) | **VERIFIED LINE BY LINE** + brute-force on small instances | single-key determination; (5.3) exponent bookkeeping; #𝒯 ≤ D; determinism of 𝒯 given ξ; boundary/endpoint representation; the miss ⇒ all-local-tests-fail ⇒ fail-at-representative inference; union bound |
| Proof of Prop. 2.1: parameter order (5.4)→d→K→g→r_* (p. 11) | **VERIFIED LINE BY LINE** | no circularity; r_h ≥ r_* for all h incl. h = 1 |
| (5.5) from α > 2 log(1/q) | **VERIFIED** analytically + numerically (`check55.py`) at q ∈ {1/2, 0.9}, smallest admissible M, p ∈ {0.5, 0.1, 1/64, 0.01, 0.001} |
| (5.6) at every stable center | **VERIFIED LINE BY LINE** | |
| Repair: B⁺, R closed, Eρ(R) ≤ 3p, Eρ(B⁺) ≤ 2p, outcome with ≤ 5p, V by outer regularity, H, hitting (pp. 11–12) | **VERIFIED LINE BY LINE** | measurability of x ↦ ℙ(x ∈ R) unstated but immediate (obj. 5) |
| Lemma 3.1 (p. 5) | VERIFIED (as input to (5.3)) | span = r_h + g + σ_{h−1} ≤ 2r_h; h = 1 span r_1 |
| (3.1), nesting, N_b nondecreasing (p. 4) | VERIFIED (as input) | also checked by assertion in `lemma51_brute.py` |
| Lemma 3.2 (p. 6) | READ AS DEPENDENCY (density chain and (3.3) checked; not certified by this seat) | |
| Lemma 3.3 (pp. 6–7) | READ AS DEPENDENCY (checked the distinct-keys-at-every-b ≥ b_e claim used in (ii) below) | |
| Lemma 4.1, (4.3) (pp. 7–8) | SKIMMED | consumed as Eρ(B) = p and ℙ(no default) = (1−2^{1−M})^d < p |
| Lemma 4.2 (pp. 8–9) | READ AS DEPENDENCY + simulated (`lemma42_check.py`) | consumed as "Q_i(y_n(t)) = 1 ⇒ y_n(t) ∈ B on ξ, for every t ∈ [1,2]" |
| Lemma 4.3 (p. 9) | READ AS DEPENDENCY, not certified | consumed as exact conditional failure probability at a fixed t on ξ |
| DYADIC §5 (Lemma 5.1, Prop. 5.2, §5.1) and §6 (pp. 11–15) | READ AND CHECKED for the comparison; (16), (3)-simplification, §6 identities and index shift recomputed | |

---

## 3. Line-by-line notes (what I actually checked)

### 3.1 Lemma 5.1

**(a) "Q_i(z) is determined by the single key J_{b*_{e_i}}(z)."** Quote (p. 10): *"Every table used by this test belongs to e_i or the subtree below it. By nesting of the grids, for every realization of the tables, Q_i(z) is determined by the single key J_{b∗_{e_i}}(z)."*
Q_i (4.4) reads: S_{e_i} at resolution b_{e_i}; every selector S_f with f = (P,j), j < M, P in the subtree of U_i, at resolution b_f; and the terminal table T_L at resolution b(L) = endpoint of L's incoming edge, which is e_i itself (if U_i is a leaf) or an edge of the subtree of U_i — **including default edges (P,M)**, which do carry windows ("Assign an integer interval W_e = [a_e,b_e] ∩ ℕ to each edge", p. 5). b*_{e_i} is "the largest endpoint among W_e and all windows in the subtree rooted at P_i" (p. 5), so every resolution read is ≤ b*_{e_i}. The N_b are powers of two, nondecreasing in b (c q^{−b} increasing ⇒ ⌈log₂⌉ nondecreasing), so N_{b*}/N_b ∈ ℤ and J_b = ⌊J_{b*}/(N_{b*}/N_b)⌋. **No table at resolution finer than b*_{e_i} is consulted.** Correct.

**(b) (5.3) exponent bookkeeping.** Quote: *"the number of recorded values is at most 1 + q^n N_{b∗_{e_i}} ≤ 1 + 2cq^{−2r}. (5.3) Here we used (3.1) and the block-span bound b∗_{e_i} − a_{e_i} + 1 ≤ 2r from Lemma 3.1."*
t ↦ y_n(t) = x + tq^n is injective, and y_n([1,2]) = [x+q^n, x+2q^n] is a closed segment of length q^n; it contains at most ⌊q^n N⌋ + 1 points of Γ_{b*} = N_{b*}^{−1}ℤ (which contains ℤ, so passages through integers — where the periodic key wraps — are counted). With n ≥ a_{e_i} (n ∈ W_{e_i}), b* ≤ a_{e_i} + 2r − 1 (Lemma 3.1) and N_{b*} < 2cq^{−b*} (3.1):
q^n N_{b*} < 2c q^{−(b*−n)} ≤ 2c q^{−(2r−1)} ≤ 2c q^{−2r}. Correct (with a slack factor q). b* − n ≥ 0 always since n ≤ b_{e_i} ≤ b*, not that it matters for an upper bound.

**(c) |𝒯_{x,ξ}| ≤ D_{M,q}(r).** Quote: *"There are (M − 1)r pairs (i, n), and hence |𝒯_{x,ξ}| ≤ D_{M,q}(r)."* Let L be the number of distinct values after adding 1 and 2: L ≤ 2 + (M−1)r(1 + 2cq^{−2r}). Then |𝒯| = L + (L−1) = 2L − 1 ≤ 3 + 2(M−1)r(1+2cq^{−2r}) < D_{M,q}(r) = 4 + 2(M−1)r(1+2cq^{−2r}). Correct (obj. 2: not displayed).

**(d) 𝒯 deterministic given ξ.** Quote: *"This set depends only on x, the deterministic windows and grids, and the vertex U determined by ξ; it is fixed before any remaining table entries are revealed."* True: the recorded values are lattice-crossing times of the deterministic maps t ↦ x + tq^n against deterministic lattices Γ_{b*_{e_i}}; the only ξ-dependence is through U (hence the edges e_i, windows W_{e_i}, endpoints b*_{e_i}). No table entry, exposed or not, enters. So Lemma 4.3 may be applied at each t′ ∈ 𝒯 (it requires t fixed on the atom) and the union bound over the fixed finite set is legitimate.

**(e) Boundary values / half-open cells / endpoints.** Quote: *"For every realization of those entries, the entire vector (Q_i(y_n(t)) : i < M, n ∈ W_{e_i}) is constant on each open interval between consecutive recorded values. Every boundary value is represented separately, so the half-open cell convention causes no loss at a boundary or at an endpoint of [1, 2]."*
On an open interval (d_j, d_{j+1}) between consecutive values of the combined list, for each pair (i,n) the path y_n(t) meets no point of Γ_{b*_{e_i}}, so it stays inside one open cell (k/N, (k+1)/N) and J_{b*_{e_i}}(y_n(t)) is constant ⇒ Q_i(y_n(t)) constant by (a). Every t ∈ [1,2] is either a listed value (then t ∈ 𝒯 is its own representative — this covers the lattice-hitting times, where the half-open convention assigns the right-hand cell, and the endpoints 1, 2 which are added explicitly) or lies in an open interval represented by its midpoint. Since 1 and 2 are in the list, there is no uncovered sub-interval at either end. Correct.
*Brute-force check* (`lemma51_brute.py`, exact rationals, q ∈ {1/2, 7/10, 9/10, 3/10}, M ∈ {2,3,4}, d ∈ {1,2}): for random rational centers (including centers with integer part ≠ 0), every first-default candidate U and every i, the per-pair list size ≤ 1 + q^nN_{b*} ≤ 1 + 2cq^{−2r}, |𝒯| ≤ D (max ratio |𝒯|/D observed 0.74), and for random table realizations the Q-vector at 200 random t and at points ±10^{−30} from 150 random recorded values equals the Q-vector at the representative. All assertions pass. **Negative control** (`mut51.py`): recording crossings of the coarser lattice Γ_{b_{e_i}} instead of Γ_{b*_{e_i}} produces 643 and 1144 constancy violations on the two instances — the instrument can fail, and the b* (not b_e) lattice is load-bearing.

**(f) The inference and the union bound.** Quote: *"If some t misses B at all indices in 𝒩, Lemma 4.2 implies that all these local tests fail at t. They therefore also fail at some t′ ∈ 𝒯_{x,ξ}. Each such t′ is a fixed real number under the conditioning on ξ, so Lemma 4.3 applies to it. Taking a union bound and using (4.6) gives ℙ(∃t ∈ [1,2] ∀n ∈ 𝒩 : x+tq^n ∉ B | ξ) ≤ |𝒯_{x,ξ}|(1 − p/2)^{(M−1)r}, which proves (5.2)."*
On ξ (x stable, U exists), Lemma 4.2 gives Q_i(y_n(t)) = 1 ⇒ y_n(t) ∈ B for every outcome in ξ, every i < M, n ∈ W_{e_i}, t ∈ [1,2]. Contrapositive: if y_n(t) ∉ B for all n ∈ 𝒩 ⊇ ∪_i W_{e_i}, then every Q_i(y_n(t)) = 0. By (e), the same vector is all-zero at the representative t′(t) ∈ 𝒯 (t′ depends on t, not on the outcome). Hence {miss} ∩ ξ ⊆ ∪_{t′∈𝒯} {all local tests fail at t′} ∩ ξ, and ℙ(·|ξ) ≤ Σ_{t′∈𝒯} (1−p/2)^{(M−1)r}. The last step to (5.2) uses (1−p/2)^{(M−1)r} ≤ e^{−p(M−1)r/2} (log(1−u) ≤ −u), unstated (obj. 1). No independence across different t′ is needed. Correct.
*Simulation of the Lemma 4.2 implication* (`lemma42_check.py`; g chosen so 4Kcq^{g+1} < 1/2, stability tested exactly): 40 stable centers per instance × 3 table seeds, q ∈ {1/2, 7/10, 3/10, 9/10}, (M,d) ∈ {(2,2),(3,2),(3,3)}; 463,830 (i,n,t) checks, 69,577 cases with Q_i = 1 — every one had y_n(t) ∈ B under the actual root-to-leaf routing. **Negative control** (`mut42.py`): the same check on UNSTABLE centers finds 84 and 156 cases with Q_i(y_n(t)) = 1 but y_n(t) ∉ B — stability is load-bearing and the instrument detects its absence.

### 3.2 Proof of Proposition 2.1 (pp. 11–12)

**Parameter order.** Quote: *"Choose an integer M ≥ 2 such that α := p(M − 1)/2 > 2 log(1/q). (5.4) Next choose an integer d ≥ 1 satisfying (1 − 2^{1−M})^d < p. For the resulting tree, let K be its number of edges and choose an integer g ≥ 1 such that 4Kcq^{g+1} < p. Finally, by (5.4), … Thus there is an integer r_∗ ≥ 1 such that D_{M,q}(r)e^{−p(M−1)r/2} < p for every integer r ≥ r_∗. (5.5) Construct the windows with r_0 = r_∗ and the chosen M, d, g."*
Dependencies: M ← (p,q); d ← (M,p); K = Σ_{ℓ=1}^d M^ℓ ← (M,d); c = 4/(1−q) ← q; g ← (K,c,q,p); r_* ← (M,q,c,p) only; n_0 ← q only; window lengths r_h ← (r_0 = r_*, g, M) bottom-up. Nothing downstream (g, r_h, σ_h, n_0, window positions) feeds back into M, d, K or r_*. The stability density bound 4Kcq^{g+1} uses only a_e = b′ + g + 1 (gap exactly g), independent of window lengths. **No circularity.**
**r_h ≥ r_* for every h:** r_1 = r_0 = r_*; r_h = max{r_0, g + σ_{h−1}} ≥ r_0 for 2 ≤ h ≤ d. Because (5.5) is required for *every* r ≥ r_* (not just r = r_*), it applies at r = r_h for whichever height the first default occurs — this uniformity is essential since r_h for h ≥ 2 is astronomically larger than r_*.
**(5.5) from (5.4):** D_{M,q}(r)e^{−αr} = 4e^{−αr} + 2(M−1)r e^{−αr} + 4c(M−1) r e^{−(α − 2log(1/q))r}; with β := α − 2log(1/q) > 0 each term → 0, so the stated O(r e^{−βr}) holds and an r_* with f(r) < p for all r ≥ r_* exists (f is decreasing for r ≥ 1/β > 1/α). Numerically (`check55.py`, log-space; tail checked to ≥ 50/β, beyond which f is provably decreasing):

| q | p | 2 log(1/q) | M_min | β | r_* |
|---|---|---|---|---|---|
| 1/2 | 0.5 | 1.3863 | 7 | 0.1137 | 93 |
| 1/2 | 0.1 | 1.3863 | 29 | 0.0137 | 1181 |
| 1/2 | 1/64 | 1.3863 | 179 | 0.00433 | 4921 |
| 1/2 | 0.01 | 1.3863 | 279 | 0.00371 | 6047 |
| 1/2 | 0.001 | 1.3863 | 2774 | 0.00021 | 146852 |
| 0.9 | 0.5 | 0.2107 | 2 | 0.0393 | 292 |
| 0.9 | 0.1 | 0.2107 | 6 | 0.0393 | 381 |
| 0.9 | 1/64 | 0.2107 | 28 | 0.00022 | 111575 |
| 0.9 | 0.01 | 0.2107 | 44 | 0.00428 | 5139 |
| 0.9 | 0.001 | 0.2107 | 423 | 0.00028 | 106106 |

All finite. (1−p/2)^{(M−1)r} ≤ e^{−αr} confirmed at each r_*. For q near 1 nothing breaks: c = 4/(1−q) large only enlarges g and r_*; N_b stays nondecreasing; Lemma 3.3's margin 1/N_b ≤ (1−q)q^b/4 holds for every q; n_0 with 2q^{n_0} ≤ 1/4 exists (n_0 = 20 at q = 0.9).

**(5.6).** Quote: *"Fix any stable center x. By (4.3), the probability that its route has no default is less than p. On each atom of 𝓕_x for which a default occurs, Lemma 5.1 and (5.5) bound the conditional probability of a miss at some normalized scale by p, since every r_h ≥ r_∗. Summing over the center-exposure atoms yields ℙ(∃t ∈ [1,2] ∀n ∈ 𝒩 : x+tq^n ∉ B) ≤ 2p (x ∈ 𝒮)."* The atoms of 𝓕_x partition Ω; "no default" is 𝓕_x-measurable with probability (1−2^{1−M})^d < p (this formula holds for every x, stable or not); on default atoms the conditional miss probability is ≤ D(r_h)e^{−αr_h} < p. So ℙ(miss) < p + p·ℙ(default) ≤ 2p. Correct. Measurability: Ω is a finite product space, every subset is an event — the quantifier over t ∈ [1,2] is harmless.

**Repair.**
* *B⁺:* B is, per outcome, a finite union of half-open cells [k/N, (k+1)/N) + ℤ of the finest grid; replacing each by (k/N − ε, (k+1)/N) + ℤ gives an open periodic B⁺ ⊇ B with ρ(B⁺) ≤ ρ(B) + (#cells)·ε ≤ ρ(B) + p. Finitely many outcomes ⇒ no selection issue. Eρ(B⁺) ≤ Eρ(B) + p = 2p by Lemma 4.1.
* *R closed:* the set {(x,t) ∈ (ℝ/ℤ)×[1,2] : x + tq^n ∉ B⁺ ∀n ∈ 𝒩} is an intersection of preimages of the closed set (ℝ/ℤ)∖B⁺ under the continuous maps (x,t) ↦ x + tq^n mod 1, hence closed; a closed subset of the compact (ℝ/ℤ)×[1,2] is compact, its projection to ℝ/ℤ is compact hence closed, and R is its periodic lift. **Finiteness of 𝒩 is not needed for closedness** (an arbitrary intersection of closed sets is closed); it is harmless (obj. 6).
* *Eρ(R):* for each outcome, R_ω is closed, so x ↦ ℙ(x ∈ R) = Σ_ω ℙ(ω)1_{R_ω}(x) is Borel and the interchange Eρ(R) = ∫₀¹ℙ(x∈R)dx is a finite sum/integral swap. x ∈ R ∩ 𝒮 ⇒ the event in (5.6) (since B ⊆ B⁺), so ℙ(x ∈ R) ≤ 2p on 𝒮 and ≤ 1 off 𝒮; ρ(ℝ∖𝒮) ≤ 4Kcq^{g+1} < p (Lemma 3.2 + choice of g). Hence Eρ(R) ≤ 2pρ(𝒮) + ρ(ℝ∖𝒮) ≤ 3p. Correct.
* *Outcome:* E[ρ(B⁺) + ρ(R)] ≤ 5p on a finite space with all outcomes of positive probability ⇒ some outcome has ρ(B⁺) + ρ(R) ≤ 5p.
* *V:* outer regularity of Lebesgue measure on ℝ/ℤ gives an open U ⊇ π(R) with m(U) ≤ m(π(R)) + p; V = π^{−1}(U) is open, periodic, ρ(V) ≤ ρ(R) + p (V = ∅ if R = ∅).
* *H = B⁺ ∪ V:* open, periodic, ρ(H) ≤ ρ(B⁺) + ρ(V) ≤ ρ(B⁺) + ρ(R) + p ≤ 6p.
* *Hitting:* x ∉ R is literally the negation of (5.7): ∀t ∃n ∈ 𝒩, x + tq^n ∈ B⁺ ⊆ H. x ∈ R ⊆ V open: some (x−ε, x+ε) ⊆ V, and 0 < tq^n ≤ 2q^n < ε for all large n uniformly in t ∈ [1,2], so x + tq^n ∈ V ⊆ H. Quote: *"These latter indices need not lie in 𝒩; the required conclusion allows every n ≥ 1."* Correct: Proposition 2.1 (2.1) and the §2 deduction only ever use "for some integer n ≥ 1". **Nothing anywhere uses that the hitting index lies in 𝒩.**

### 3.3 §2 global deduction (pp. 3–4)

* p_k = (η/64)4^{−|k|} ∈ (0,1). Each ±2^kH_k is open, 2^k-periodic, with measure 2^kρ(H_k) per period. k ≤ 0: [0,1] is exactly 2^{−k} periods ⇒ measure = ρ(H_k); k > 0: [0,1] ⊆ [0,2^k) ⇒ measure ≤ 2^kρ(H_k). So m((±2^kH_k) ∩ [0,1]) ≤ max(1,2^k)ρ(H_k) ≤ 6 max(1,2^k) p_k. **Factor 12 = 2 signs × 6.** Correct.
* (2.3): 12 Σ_k p_k max(1,2^k) = (12η/64)[Σ_{j≥1}4^{−j} + 1 + Σ_{k≥1}2^k 4^{−k}] = (12η/64)(1/3 + 1 + 1) = (12/64)(7/3)η = **7η/16** — confirmed with exact rationals (k ∈ [−400,400], residual 7·10^{−122}). m(E) ≥ 1 − 7η/16 > 1 − η.
* Compactness: C is a union of open sets, E = [0,1] ∩ (ℝ∖C) is closed and bounded. (Reflection symmetry is irrelevant here — obj. 7.)
* s > 0: k = ⌊log₂ s⌋, t = 2^{−k}s ∈ [1,2) ⊆ [1,2]; (2.1) for H_k at center 2^{−k}x gives n ≥ 1 with 2^{−k}x + tq^n ∈ H_k; multiplying by 2^k: x + sq^n ∈ 2^kH_k ⊆ C. s < 0: −x + (−s)q^n ∈ 2^kH_k for some k, n ⇒ x + sq^n ∈ −2^kH_k ⊆ C. The index n is untouched by the normalization; no relation between 2 and q is used. Correct.
* Points outside [0,1]: the conclusion is x + sq^n ∈ C, and C ∩ E = ∅ by definition (E = [0,1]∖C), so x + sq^n ∉ E regardless of whether it lies in [0,1]. The theorem's statement "x + sq^n ∉ E for some n ≥ 1" is exactly what is proved. Correct.

---

## 4. What §5 consumes from §§3–4 (dependency ledger)

For the hand-off to the seats certifying §§3–4, §5 needs exactly:
1. **(3.1) + nesting** (N_b powers of two, nondecreasing; J_b = ⌊J_{b′}/(N_{b′}/N_b)⌋) — verified.
2. **Lemma 3.1** b*_e − a_e + 1 ≤ 2r_h — verified.
3. **Lemma 3.2** ρ(ℝ∖𝒮) ≤ 4Kcq^{g+1} and 𝒮 measurable, periodic — chain checked; certification elsewhere.
4. **Lemma 4.1** Eρ(B) = p; B a finite union of half-open cells per period — skimmed.
5. **(4.3)** ℙ(no default) = (1−2^{1−M})^d for every fixed x — formula checked.
6. **Lemma 4.2** for every outcome in ξ and every t ∈ [1,2] (not just fixed t): Q_i(y_n(t)) = 1 ⇒ y_n(t) ∈ B — simulated with positive and negative control; certification elsewhere.
7. **Lemma 4.3** at every *fixed* t ∈ [1,2] (including t at which some y_n(t) is a lattice point): exact conditional failure (1−p/2)^{(M−1)r} given ξ — not certified by me.

On brief item (ii) (asked of all seats; answered here only because it bears on whether Lemma 4.3 can be applied at every t′ ∈ 𝒯): Lemma 4.3 conditions on the whole selector field 𝒜, so freshness of the selector entries read by y_n(t)'s route *below* U_i is never used; only (α) the A_{i,n} being unexposed distinct entries and (β) pairwise distinct terminal addresses κ_{i,n} are used. In any case those below-U_i entries are never x's exposed entries: every edge f in the subtree of U_i follows e_i in preorder, windows are disjoint and increase along preorder, so b_f > b_{e_i}, and Lemma 3.3 gives distinct keys for x and y_n(t) at every b ≥ b_{e_i}.

---

## 5. Objections (numbered)

**1. COSMETIC — last step of Lemma 5.1 unstated.** Location: Lemma 5.1, proof, pp. 10–11. Quote: *"Taking a union bound and using (4.6) gives ℙ(∃t ∈ [1, 2] ∀n ∈ 𝒩 : x + tq^n ∉ B | ξ) ≤ |𝒯_{x,ξ}|(1 − p/2)^{(M−1)r}, which proves (5.2)."* (5.2) has e^{−p(M−1)r/2}; the step (1 − p/2)^{(M−1)r} ≤ e^{−p(M−1)r/2} (from log(1−u) ≤ −u) is omitted. True; exposition only. Fix: one clause.

**2. COSMETIC — |𝒯| ≤ D arithmetic not displayed.** Location: Lemma 5.1, p. 10. Quote: *"There are (M − 1)r pairs (i, n), and hence |𝒯_{x,ξ}| ≤ D_{M,q}(r)."* Supply: L ≤ 2 + (M−1)r(1 + 2cq^{−2r}) distinct values, |𝒯| = 2L − 1 ≤ 3 + 2(M−1)r(1+2cq^{−2r}) < D_{M,q}(r). (D has one unit of slack.) Exposition only.

**3. COSMETIC — (5.3) is loose by a factor q and its "1 +" is unexplained.** Location: (5.3), p. 10. Quote: *"The segment traversed by y_n has length q^n, so the number of recorded values is at most 1 + q^n N_{b∗_{e_i}} ≤ 1 + 2cq^{−2r}."* The argument gives 2cq^{−(2r−1)}; the "1 +" accounts for a closed segment with lattice points at both ends. Both directions of slack are harmless. The dyadic paper states the "+1" reason explicitly (p. 12: "The extra one allows both endpoints to be lattice points").

**4. COSMETIC — single-key claim stated without enumerating default-child leaves.** Location: Lemma 5.1 proof, p. 10. Quote: *"Every table used by this test belongs to e_i or the subtree below it. By nesting of the grids, for every realization of the tables, Q_i(z) is determined by the single key J_{b∗_{e_i}}(z)."* The claim needs b(L) ≤ b*_{e_i} also for leaves reached through default edges (P,M); true because every edge, default ones included, carries a window inside the block whose maximum is b*_{e_i} (p. 5). The dyadic paper spells this out (pp. 11–12: "The incoming edge of every possible terminal leaf also has endpoint at most b*_i. This includes the case that U_i itself is a leaf …, as well as leaves reached through default children."). No gap.

**5. COSMETIC (exposition) — measurability of x ↦ ℙ(x ∈ R) not stated before integrating.** Location: proof of Prop. 2.1, p. 12. Quote: *"Integrating the probability bound over one period therefore gives 𝔼ρ(R) = ∫₀¹ ℙ(x ∈ R) dx ≤ 2pρ(𝒮) + ρ(ℝ∖𝒮) ≤ 3p."* Needs x ↦ ℙ(x ∈ R) measurable: it equals Σ_ω ℙ(ω)1_{R_ω}(x), a finite combination of indicators of closed sets, hence Borel; the swap is a finite sum. The dyadic paper states this (p. 14: "each indicator 1_{R_ω}(x) is Borel measurable in x. Since Ω is finite, it is also jointly measurable in (ω, x)"). Exposition only.

**6. COSMETIC — closedness of R: the justification given is right but the operative fact is unstated, and finiteness of 𝒩 plays no role.** Location: p. 11. Quote: *"This is a closed periodic set. Indeed, on the circle ℝ/ℤ it is the projection of the closed set {(x, t) ∈ (ℝ/ℤ) × [1, 2] : x + tq^n ∉ B⁺ for all n ∈ 𝒩} in a compact product."* The set is closed because each (x,t) ↦ x + tq^n mod 1 is continuous and (ℝ/ℤ)∖B⁺ is closed (B⁺ open); closedness would hold for any index set, finite or not. The brief's premise "because 𝒩 is FINITE" is not needed. Exposition only. (Also typographic: the paper uses R for the missed-center set and ℝ for the reals in adjacent formulas, e.g. "ρ(ℝ∖𝒮) < p" right after (5.7); unambiguous in the PDF, ambiguous in any text extraction — `geometric_plain.txt` renders it "ρ(R \ S) < p".)

**7. COSMETIC — irrelevant reason for compactness.** Location: §2, p. 4. Quote: *"The set C is open and symmetric under reflection, so E_{q,η} is compact."* Symmetry plays no role in compactness (E = [0,1]∖C is closed and bounded because C is open). The reflected components −2^kH_k are used, directly, in the s < 0 case. Not wrong.

**8. REMARK (no error) — expanding dilations k > 0 are redundant but harmless.** Location: (2.2)–(2.3). For s with sq(1−q) > 1 the points x + sq and x + sq² are more than 1 apart, so no such copy can lie in [0,1] anyway. These terms cost 12·Σ_{k≥1}2^k p_k = 12η/64 = 3η/16 of the 7η/16 total; the bound already includes them. No effect on correctness.

**9. REMARK (global assessment) — the DYADIC paper (the Lean-formalized one) is a different construction from the GEOMETRIC paper at q = 1/2, and does not certify the geometric §2 or the geometric constants.**
* Grids: geometric N_b = 2^{⌈log₂(8·2^b)⌉} = **2^{b+3}** at q = 1/2 (confirmed `reconcile.py`); dyadic J_b = ⌊2^{b+2}{z}⌋, i.e. N_b = **2^{b+2}** (dyadic (6), p. 6). Same mechanism, grids differ by a factor 2.
* Branching condition: geometric (5.4) α > 2 log 2 ≈ 1.386; dyadic (1) p(M−1)/2 ≥ 10.
* Scale count: geometric D_{M,1/2}(r) = 4 + 2(M−1)r(1 + 2^{2r+4}) (2cq^{−2r} = 16·4^r); dyadic (16) |ℛ(x,U)| ≤ 20Mr(1 + 2^{2r+2}). Reconciliation: true per-pair crossings are ≤ 1 + 2^{b*+3−n} ≤ 1 + 2^{2r+2} for the geometric grid and ≤ 1 + 2^{b*+2−n} ≤ 1 + 2^{2r+1} for the dyadic grid; the geometric bound loses a factor 4 (factor 2 from using N_b < 2cq^{−b} where at q = 1/2 actually N_b = cq^{−b}; factor 2 from q^{−(2r−1)} ≤ q^{−2r}), the dyadic bound a factor 2 (it writes 2^{2r+2} for 2^{2r+1}). Each is a valid upper bound for its own 𝒯/ℛ; 2L − 1 ≤ 2(M−1)r(1+2^{2r+2}) + 3 ≤ 20Mr(1+2^{2r+2}) checks; and D_{M,1/2}(r) < 20Mr(1+2^{2r+2}) for all M ∈ [2,300), r ∈ [1,60) (checked). The dyadic simplification "left side ≤ 100Me^{−7r}" under p(M−1)/2 ≥ 10 also checks (1 + 2^{2r+2} ≤ 5e^{2r}, r ≤ e^r).
* Stability density: dyadic exact 2^{2−g} per window; geometric bound 4cq^{g+1} = 2^{4−g} at q = 1/2 (actual for the geometric grid 2^{3−g}). Consistent.
* **§2 vs dyadic §6 are different deductions.** Dyadic uses only contracting dilations 2^{−j}H_j, j ≥ 1, and for large scales reuses H_1 by an index shift N = n + j − k ≥ n, which exploits 2^{−m}D ⊆ D — a self-similarity specific to q = 1/2 matching the dilation base 2. The geometric paper cannot do that and instead uses all k ∈ ℤ with weights max(1,2^k) and p_k ∝ 4^{−|k|}. I verified the geometric §2 independently (above); but anyone relying on the Lean formalization should know it covers neither this §2 nor the general-q constants.

**10. REMARK — steps the dyadic §5–§6 spells out that the geometric §5 compresses** (none missing mathematically): explicit enumeration of what Q_i reads (obj. 4); the "+1" in the crossing count (obj. 3); "No independence between different representative scales is required" (dyadic p. 13); measurability of 1_{R_ω} (obj. 5); explicit enlargement for B⁺ ("enlargement by circular distance p/(4Q) adds at most p/2", p. 13); explicit V as a metric neighbourhood of π(R) chosen by continuity from above, and explicit n_0 with 2^{1−n_0} < ε (p. 14), where the geometric paper says "outer regularity" and "for all sufficiently large n". Each geometric compression is a true statement with an immediate justification.

No other "clearly / it follows / similarly"-type step in scope: I checked every "hence", "therefore", "thus", "indeed", "it follows", "consequently" in §2 and §5 (p. 4 "Consequently" before (2.3); "It follows that m(E) > 1 − η"; p. 10 "and hence |𝒯| ≤ D"; "They therefore also fail at some t′"; p. 11 "Thus there is an integer r_*"; "Indeed, on the circle …"; "In particular, its density is defined"; p. 12 "therefore gives 𝔼ρ(R) …"; "Thus every center …"). Each holds as annotated above.

---

## 6. Brief item (ix) — Steinhaus sanity, within scope

**Where infiniteness of G_q is used.** Exactly two places:
1. **The repair** (p. 12): centers in V are hit at indices n → ∞ (tq^n → 0), *outside* 𝒩. This needs infinitely many terms accumulating at 0.
2. **The size of 𝒩 as p → 0.** §2 calls Proposition 2.1 at p_k → 0, and the finite index set 𝒩(p) must grow: from (5.5) with D > 4, e^{−αr_*} < p/4, i.e. (M−1)r_* > 2 log(4/p)/p, so |𝒩| ≥ (M−1)r_* → ∞. A finite pattern F could not supply this: by averaging, ∫₀¹ #{a ∈ F : x + ta ∈ H} dx = |F|ρ(H), so if 6|F|p < 1 some center misses H at a fixed t — Proposition 2.1 is *false* for a finite pattern once p < 1/(6|F|). The proof never contradicts this: everything through (5.6) and Eρ(R) ≤ 3p concerns the finite pattern {q^n : n ∈ 𝒩} with |𝒩|·p > 2 log(4/p) > 1, and it only claims hitting *off* an exceptional set of density ≤ 3p; the "every center" claim is obtained solely through the repair, which leaves 𝒩.
So the argument through (5.6) is a true statement about a finite pattern (Kolountzakis/Chlebík-type "almost every center"), and it is not secretly proving the false finite "every center" statement. Steinhaus (every finite set is universal) is a statement about scales s → 0; in this proof that regime is the k → −∞ part of §2, where it is paid for by |𝒩(p_k)| → ∞. Consistent.

**Would the argument prove the full conjecture for any null sequence? No.** The geometric structure is used at three named steps:
* **Lemma 3.3** (separation): t(q^n − q^{n′}) ≥ (1−q)q^b and tq^n ≥ q^b, against cell width 1/N_b ≤ (1−q)q^b/4 — needs consecutive gaps comparable to the terms.
* **Lemma 3.2** (stability density): 2q^{a_e}N_{b′} ≤ 4cq^{a_e−b′} = 4cq^{g+1} — needs uniform decay over a gap of g indices (fails for a_{n+1}/a_n → 1, which is Falconer's known case anyway).
* **(5.3)** (scale count, in my scope): q^n N_{b*} < 2cq^{n−b*} ≤ 2cq^{−2r} — the ratio "term at the window start / grid spacing at the block end" depends only on the index *difference* b* − n ≤ 2r − 1, not on where the block sits in the tree. For super-geometric decay (e.g. a_n = 2^{−n²}) the analogous ratio is 2^{Θ(nr)}, depends on the window's position, which itself depends on g, K and r through the tree — the parameter choice (5.4)–(5.5) would become circular. And (5.4) is literally a comparison of the branching rate with the exponential rate 2 log(1/q).
The mechanism therefore appears to extend at most to sequences with ratios a_{n+1}/a_n confined to a compact sub-interval of (0,1) (bounded-ratio lacunary sequences) — I have not checked this extension and the paper does not claim it. It does not reach arbitrary null sequences, so it is not "suspiciously general". (Context, not a finding: Chlebík 2015, p. 17, "the universality/non-universality status is known for no zero-sequence {x_k} that decreases geometrically or faster" — read in arXiv:1512.05607v1.)

---

## 7. Citation table (scope: §5's precedent citations; §2 has none)

Sources read from `/tmp/erdos0300/refs/` (downloaded by sibling seats; I read the files, checked version headers myself).

| Cited result | What the paper says it says | What the source says (quote) | Verdict |
|---|---|---|---|
| [Chl15, proof of Theorem 15] (arXiv:1512.05607**v1**, header "arXiv:1512.05607v1 [math.MG] 17 Dec 2015") | "The finite boundary-representative argument has precedents in [Chl15, proof of Theorem 15]" (p. 10) | p. 16: "it is sufficient to check whether such b exists in a finite set S(a) = {b₁ = 1, b₂, …, b_N} consisting of 1 and those b ∈ (1, 2] for which some a+by_i, i = 1, 2, …, n−1 is in the set {jτ : m < j < M} (as only those points (a, b) can be boundary points of the set L_Y(G))." | MATCH |
| [KP25, Section 3.1] (arXiv:2208.02637**v2**, header "arXiv:2208.02637v2 [math.CA] 6 Oct 2023") | same sentence, "and [KP25, Section 3.1]" | §3.1: "To check whether there exists t ∈ [a, b] such that (x + tA) ∩ [−N, N] ⊆ E, it is sufficient to check whether such a t exists in a finite set S = S(x) = {t₁, t₂, …, t_u} ⊆ [a, b]." | MATCH |
| [Tom15, Lemma 0.2] (local `refs/tom15/paper.pdf`, "Summer 2015 – NSERC USRA Report, Sets Avoiding Images of a Given Sequence, Foster Tom"; download URL not recorded by me) | "Open-neighborhood repair for null sequences is explicit in Tom [Tom15, Lemma 0.2]" (p. 11) | "Lemma 0.2 Suppose ∃E ⊂ ℝ with m(E) > 0 and m(P) = 0 where P = {x : ∃t : x + tA ⊂ E}. Then A is non-universal. Proof: P has an open cover Q with F = E \ Q having positive measure. If for some x, t, x + tA ⊂ F ⊂ E, then by definition x ∈ P ⊂ Q. But Q is open so ∃a ∈ A with x + ta ∈ Q, contradicting x + tA ⊂ F." | MATCH (Tom's exceptional set is null, the paper's has small measure; same open-cover mechanism; Tom's last step tacitly uses that 0 is a limit point of A, true for null sequences) |
| [Chl15, Section 3, final remark; Proposition 1(vi), (viii)] | "see also" for the open-neighbourhood repair (p. 11) | Final remark of §3, p. 12: "Using the fact that 0 ∈ X, we can add to H that small set of a's in [0, 1] for which {a} × [1, 2] is not covered by L_X(H) and conclude non-universality of X this way." Prop. 1(vi), p. 4: "L_{X̄}(G) = L_X(G) whenever G is open." (viii): "For each A ⊆ ℝ × (ℝ∖{0}) there are open sets G_k ⊆ ℝ … such that L_X(G_k) ⊇ A and λ(G_k) ≤ µ_X(A) + 2^{−k}." | MATCH as a "see also": the remark adds the centers themselves and needs 0 ∈ X; (vi) is what transfers it to a null sequence (0 ∈ X̄∖X) against open sets; (viii) supplies openness. The paper does not claim Chlebík does open neighbourhoods. |

None of these citations is load-bearing: the paper re-proves everything it uses in §5.

---

## 8. Summary

Lemma 5.1, the proof of Proposition 2.1 and the §2 deduction of Theorem 1.1 hold as written. The scale-count mechanism is sound: Q_i reads no table finer than b*_{e_i}; the crossing count 1 + q^nN_{b*} ≤ 1 + 2cq^{−2r} is correct (with a factor-q slack); 𝒯_{x,ξ} is a deterministic function of (x, U) so Lemma 4.3 and the union bound apply; boundary values and the endpoints 1, 2 are represented; and the union bound only ever uses the *local* sufficient tests, so finer grids elsewhere in the tree never enter the count. Parameters are chosen without circularity, r_h ≥ r_* at every height, and (5.5) holds with finite r_* at q ∈ {1/2, 0.9} for the smallest admissible M. The repair is correct (R closed for any index set; Eρ(R) ≤ 3p; V by outer regularity; ρ(H) ≤ 6p; hits at repaired centers use indices outside 𝒩, which the statement allows). (2.3) = 7η/16 exactly; the factor 12 = 2 signs × 6; the s < 0 case and points outside [0,1] are handled. Objections are cosmetic. The verdict is conditional on Lemmas 3.2/3.3/4.2/4.3, which other seats certify.
