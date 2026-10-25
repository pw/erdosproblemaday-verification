# Referee report — seat `whole` (whole-paper hostile read; global parameter graph)
Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026), /tmp/oaimath/011/paper.pdf (68 pp). Read in full once (text extraction plus PDF pages 35–38 and 51–52 for displayed formulas). Sources I fetched or re-read for content: Montgomery–Vaughan draft (refs/MV/mv.txt, 472 pp, pdf dated 2024-10-09), Efron–Stein 1981 (refs/EfronStein/es.pdf, JSTOR scan, pp. 587–588 read as images), Ford–Halberstam 2000 (refs/FH/fh.txt, author copy).

**Bottom line for this seat.**
- I found **no FATAL error and no mathematical GAP** at the whole-paper level. That covers the global order of choices (acyclic; table in §2), every interface between §§3–7 that I re-derived, and every use of the structural hypotheses (§4).
- I could **not refute Theorem 5.1**. Every standard obstruction is excluded by one of three things: (5.4), invariance under P-integers, or the compulsory long rough factor with trivial coefficient (§1).
- What I could **not check** is concentrated in one place. It is the exactness of the memory identity (Lemma 3.7) and the equality-rank restoration of distinct births (§3.8), i.e. the inside of Theorem 3.5. Every parity-breaking claim of the paper flows through Theorem 3.5 (§1.4). It is the single point of failure, and the transference seat's report did not exist in /tmp/oaimath/011 when I finished.

---

## 1. Is Theorem 5.1 true? (Scope item 1)

### 1.1 What the proof actually uses at each endpoint
I traced every occurrence of F0, G0 from §5.2 to §5.8.

**First endpoint (the conjugated, discrepancy-bearing one):**
- (a) Invariance under P-integers. Used in §5.2, "Invariance gives F0(D_R w) = F0(w)".
- (b) Mark-independence. Corollary 3.11: "Only the first endpoint must be independent of its mark list."
- (c) sup|F0| ≤ exp(O(√L)). Corollary 3.11 needs it so that (H·sup|f|²)^{1/(2R)} = O(1). It holds because only m and p, which are W-rough divisors, are chosen; r is then determined.
- (d) The norm bound X^{1/2}L^{C6}.
- (e) In §5.4–5.8 only, for the major-arc energy (5.11):
  - one small-group mark p_s, extracted by (5.12);
  - the exact Dirichlet-convolution factorization w = m·p_s·p·r;
  - the long rough factor p ∈ I_p ⊂ [x^τ, x^η] with coefficient p^{iσ1}, for Lemma 5.4 (pointwise) and Lemma 5.3 (U > Y^{0.6} needs η < 0.4);
  - (5.4) for the m-polynomial, only on |t| ≤ L^{B0};
  - the residual r enters only through |d_r| ≤ L^{O(1)} and the ℓ² bound (5.19).

**Second endpoint:**
- (a) Invariance. This is needed for G0(D_R w′) = G0(w′) in the lift. §5.2 writes the identity only for F0, but the computation leading to (5.7) uses it for G0 too.
- (b) |G0(n)| ≤ L^{O(1)}τ(n_*)², which gives the target-vector norm and the τ⁴-moments in the free/endpoint-ban error.
- (c) The ℓ²-bound (5.10).
- **Nothing else.** No small mark, no long rough factor, no α′ structure, no sup bound (Corollary 3.11 needs a sup bound only for f).

**Consequence (UNCLEAR, Objection W1).** The proof, if correct, proves something strictly stronger than Theorem 5.1 as stated. Let g be any function on P-free integers with |g(a)| ≤ L^C τ(a)². Then

  Σ_z Ψ(z/Z) z^{−1} z^{ia1}(z+k)^{ia2} F̄0(z) g((z+k)_*) W_ℓ(z) W_ℓ(z+k) ≪ L^{−D0}.

Taking g = a phase of the inner sum, this is equivalent by duality to

  Σ_{a P-free} | Σ_{b a P-integer} F0(ab−k) W_ℓ(ab−k) W_ℓ(b) Ψ((ab−k)/Z)/(ab−k) | ≪ L^{−D0}.

In words: for almost every P-free a, F0 cancels along the dilated progression {ab − k : b a marked P-integer}. That is the real mathematical content beyond the state of the art. It is a one-sided, single-scale, power-of-log Elliott-type statement for dilation-invariant functions. Its proof rests entirely on Theorem 3.5 plus Corollary 3.11 plus Theorem 4.1. The circle method in §5.3–5.8 only removes the comparison terms, whose shifts are kD_AD_B with D_AD_B ≥ exp(L^c).

### 1.2 Counterexample attempts (all inside the hypotheses), and why each fails
| # | Construction | Why it fails |
|---|---|---|
| 1 | **Archimedean pretender.** α_m = m^{iT}1_{P⁻(m)>W}1_{m∈[M,2M]}, M = x^{0.95}, any T ∈ (L^B, x^{0.9}]. (5.4) holds: m=1 is excluded, and for |u| ≤ L^B the frequency T+u is ≫ L^B. Main term ≪ 1/(T√L); error via the Vinogradov–Korobov zero-free region at height ≍ T is exp(−cL^{1/3}), with the finite Euler product over p ≤ W costing L^{O(1)}. Put c_r = r^{iT}, and make p^{iσ1}(p/P0)^{−iT} nearly constant on a short I_p of relative width L^{−B−3}. Then F0(z) ≈ C·z_*^{iT}·(positive count), and similarly G0(n) = n_*^{−iT}·(positive). | The product is (z_*/(z+k)_*)^{iT} = (z/(z+k))^{iT}·((z+k)_P/z_P)^{iT}. The first factor is 1 + o(1). The second averages to ≪ L^{−c} over the marked P-parts as soon as |T| ≫ L^{−a}, since E_g[p^{iT}] for p ∝ 1/p on a group is ≈ ∫_{L^a}^{L^b} e^{iTv}dv/v. Invariance kills |T| ≥ L^{−a+ε}, and (5.4) kills |T| ≤ L^B; the two ranges overlap. **Excluded.** |
| 2 | Small-conductor character pretender, α ≈ χ (q ≤ L^B). | Directly excluded by (5.4), which explicitly covers principal and imprimitive characters. |
| 3 | Large-conductor character pretender, q > L^B. | F0 ~ χ(z_*) needs χ(p) constant on the rough integers in I_p, which fails unless I_p is a single point; then the normalized sum is trivially O(x^{−τ}). Converting χ(z_*) into χ(z) (invariance) needs χ ≡ 1 on all group primes. That cannot be constructed; under GRH it is impossible, since Σ_{p≤t} χ(p) log p ≪ √t·log²(qt) = o(t) for every t ≥ exp(L^{1/10}). Even granting it, q ∤ k because |k| ≤ L^C < q, so Σ_{z mod q} χ(z)χ̄(z+k) = o(q) (it equals −1 for prime q) and there is no bias. **No counterexample.** |
| 4 | **Constant sign via a Dirichlet inverse.** α = μ·1_R·1_{m≥2}, c = 1_R (bounded on all r). Then α∗c = δ_1 − 1_R and F0 = −(1_I ∗ 1_R)(z_*) ≤ 0. | α fails (5.4): Σ_{2≤m≤y, rough} μ(m)/m = −1 + o(1) for y ≫ W^{O(1)}. In general (5.4) for α is inherited by β = α∗c with loss L^{C+1}, since Σ_{s∈I}(α∗c)_s/s = Σ_r (c_r/r)·Σ_{m∈I/r} α_m/m. So F0 = 1_I∗β can never be sign-pretentious. (5.4) is the right gatekeeper. |
| 5 | MRT-type scale-dependent pretender. These are the known counterexamples to the *unaveraged* Elliott conjecture; f pretends to n^{it_j} at scale x_j with large t_j. | Needs |t_j| ≫ L^{−a} at the relevant scale, so it is killed by invariance as in row 1. |
| 6 | Liouville-type, α = λ·1_R, c = λ. | F0 = λ(z_*)·Σ_{p\|z_*, p∈I_p} λ(p)·N(z_*/p). The compulsory p-factor has trivial coefficient, so λ(p) cannot be absorbed and the inner sum re-mixes parity. Shrinking I_p to one prime makes the normalized sum trivially x^{−τ}. No λ(z)λ(z+k)-with-positive-weight encoding (single-scale Chowla, open) is reachable. |
| 7 | Random completely multiplicative f (f = 1 on primes ≤ W, random ±1 above), α = f·1_R·1_{m>1}. | (5.4) holds w.h.p.: each test has variance ≤ W^{−1}, and a union bound over x^{O(1)} tests leaves failure probability exp(−e^{√L}L^{−2B})·x^{O(1)} → 0. Take I_p = {p0} for constancy and c = f. Then F0 ∝ f(z)·(positive) and the correlation is Σ f(z)f(z+k)·weights, which is small for random f. No counterexample. |
| 8 | G0 := conj F0(· − k). | Not admissible. It is not a function of n_*, because (n−k)_* is not determined by n_*. |
| 9 | **Residual at the FIRST endpoint** (brief's specific question): c_r = 1_{r≡a (q)}, c_r = r^{iT}, or c_r correlated with z mod small primes. | Harmless. In §5.4 the arc phase e(uw/r0) is expanded into characters of v = m p_s p (r/d0). I checked that (r/d0, r0/d0) = 1 always: if p \| both, then p d0 \| (r, r0) = d0. The r-character is absorbed into d_r. In Mellin space P = M·P_s·P_l·Res is an exact convolution. On \|t\| ≤ L^{B0}, \|M\| ≤ L^{−B} and \|Res\| ≤ L^{O(1)} trivially. On large \|t\| only ℓ² (Halász, Lemma 5.3) and the pointwise P_l bound are used. Low-complexity structure of c_r is invisible to every step. The transference never looks inside F0 at all. |

### 1.3 Verdict on item 1
- No counterexample exists among the natural constructions.
- Pretentious obstructions are excluded by (5.4) (small conductor, |u| ≤ L^B) together with invariance plus ≥ ℓ marks per group (all |t| ≫ L^{−a}). Sign/parity encodings are blocked by the trivial coefficient on the compulsory long rough factor.
- (5.4) on α alone is sufficient for the *major arcs*, for arbitrary bounded c_r at both endpoints and arbitrary α′ at the second. That part of the proof (§5.4–5.8) holds as read.
- The single-scale form is not by itself a red flag. Invariance turns the dilated root weight Ψ(n/(ZD))/n in §5.2 into a sum over many scales Z·D, and the CRT step (Lemma 3.6) works at every scale X ≥ x^γ. Tao's log-averaging was forced by the entropy-decrement step, which this paper replaces.

### 1.4 Where the truth of Theorem 5.1 actually rests
The residual pairing bound |⟨f, A g⟩| ≪ X L^{−E+2C3} (Corollary 3.11) is a statement about the dilation graph only, for *every* mark-independent f.
- I verified the spectral-Hölder/trace argument of Corollary 3.11 and the exponent bookkeeping (3.48). The PSD-matrix trick λ_max ≤ trace is correct, and the Hölder exponents 2, 2R/(R−1), 2R sum correctly.
- I checked the architecture of Theorem 3.5:
  - The per-visit costs are exactly G_i (L^{C_v}) and E_i (L^{−G}). Both are operator norms on the same Hilbert space H, so the product bound is legitimate.
  - Every other cost is global or o(N) in the exponent: baseline ≤ 1, θ-integral, residue replacement (relative error exp(−ANT), summed against absolute mass L^{C_abs N}), truncation (3.28), r < r0 = o(N) affected edges, and A*^{2r} coefficients.
  - The sanity picture is consistent. The raw operator alone has small ‖A u_n‖ (symmetrization spreads a delta over C(M,ℓ)^s positions) but norm ≈ 1 near Θ ≈ 0. The comparisons remove exactly that, uniformly in Θ (Theorem 4.1).
- I did **not** reconstruct the bijection in Lemma 3.7 in full. (I spot-checked lifespan cases: dropped vs stored, ghost birth before first activity, multiple runs, internal unmarked hits.) Nor did I reconstruct the conditional backward induction behind (3.44). If Theorem 5.1 is false, it fails there.

---

## 2. Global order of choices (Scope item 2)
I built the graph from: Convention 2.1 (p.5); Theorem 3.5's quantifiers; (3.37); the J-condition after (3.37); Theorem 4.1; (4.20) and the closing paragraph of §4.4; §5.2 "after choosing the transfer target first, then the ideal family, then J"; §5.8's last paragraph; §6.4 ("K0 chosen after C3, C5, C_f"); §6.6; Remark 6.2; §7.7 (i)–(v).

Notation: superscripts (k) mark the section where a re-used letter lives (see Objection W5).

| constant | fixed where | depends on | used where | claimed independent of | status |
|---|---|---|---|---|---|
| δ, Ψ (§7), r0, c1..c4=1,6/5,3/2,9/5, s′, λ=2 | §7.1, step (i) | δ | everything | everything later | ✔ |
| a,b,c,d = 1/10,1/5,3/10,2/5; v±; c0,C0 | §7.1 (P-groups at [c3 s_j, c4 s_j]) | r0, s′ | §3–6 | — | ✔ (d<0.47, 0.52+d=0.92<1) |
| q=1/2, ℓ=1 | §7.1 | — | §3–6 | — | ✔ |
| j′, θ (7.24); j0 | (i) | geometry | §7.6, §7.1 | κ, b1, j**, S | ✔ |
| C_A, C (7.2–7.3); C_bal (7.31) | (i) | geometry, Ψ, j′, θ | (7.22), (ii) | κ, b1, j**, S_proxy | ✔ (C_bal checked: depends only on (i)) |
| κ | (ii) | C_bal, S_sing (7.9) | ϑ=1/2−κ/2, bins, B_κ | — | ✔ (but see W3: S overloaded) |
| b1; h_(7.11)=2⌊1/(40b1)⌋; b*=b1/3 | (iii) | κ (only via κ<1/50) | (7.11), Thm 6.1 range | — | ✔ |
| j** ⇒ τ*,η* | (iii), (7.10) | b*, j0 | Thm 6.1, Thm 5.1 (τ,η), Lemma 5.4 (K=⌈4/τ⌉+3) | — | ✔ |
| bin mesh | (iii) | b1, κ, continuity of D_γ | (7.21) | — | ✔ |
| D*^(6) (Thm 6.1 saving) | (iv) | C_A, number of bins/dyads | §7.5–7.6 | S_proxy | ✔ |
| C=1 (coefficient bound in Thm 6.1) | — | \|I−B_I\| ≤ 1 | Thm 6.1 | S_proxy | ✔ (0 ≤ c_I ≤ 1 exactly, Lemma 7.3) |
| C_s^(6)=(c2+1)c+, C_F, C_f, C_a^(6), C3^(6), C4^(6) (majorant derivatives), C5^(6) | §6.3–6.4 | band constants, ℓ, group data | (6.13)–(6.14) | K0, J, all of §3–5 | ✔ |
| K0 | §6.4 | D*, C3^(6), C5^(6), C_f | E=U L^{−K0}, \|k\| ≤ L^{K0+C_s} | — | ✔ |
| C6^(6) (z-range), C7^(6), C8^(6) (cutoff separation) | §6.6 | K0 | twists ϱ, ξ_i | — | ✔ |
| C^(5) (all bounds fed to Thm 5.1: \|k\|, Z-range, \|a_i\|, \|σ\|, char modulus 2\|k\|, coefficients) | §6.6 | K0, C8^(6), C_a^(6) | Thm 5.1 | S_proxy | ✔ |
| Ψ^(5) = ψ̃_Z (dyadic partition × t) | §6.6 | — (O_j(1) derivatives) | Thm 5.1 | K0 | ✔ |
| D0 | §6.6 | K0, k-range, separation costs, target A | Thm 5.1 | — | ✔ |
| C6^(5) (endpoint norm) | §5.2 | C^(5), divisor moments | E | J, m_probe | ✔ (Σ_{S′}ΠV^{−M}/P(S′) ≤ 1 holds for every J) |
| C7^(5) (Mellin cutoff of Ψ^(5)) | §5.2 | derivative exponent of Ψ^(5) | C4^(4) | K0 (in §6 use) | ✔ |
| **C4^(4)** (ideal frequency range) | implicit in §5.2/§5.8 | must exceed \|a1+a2\|+L^{C7}: so C4 > max(C^(5),C7^(5))+1, **hence depends on K0** | Thm 4.1 input → m, h*, C1 | nothing chosen before K0 uses it | ✔ no cycle (W2) |
| D1 (residual-pairing target) | §5.2 | D0, normalization costs | E | — | ✔ |
| E | §5.2 | D1, C6^(5) | Thm 3.5 | — | ✔ |
| C_v | (3.22) | q, ρ, v, v± | (3.37) | m, C1, J (claimed; consistent with (3.21)) | ✔ as read |
| C_s^(3) | Lemma 3.10 | q, ℓ, v−, group data | (3.37) | m, C1, J (claimed; sup_y q^y(y+ℓ)_ℓ is J-free) | ✔ |
| G, E_id | (3.37) | E, C_v, C_s^(3) | Thm 4.1 | m, C1, J | ✔ (this is what breaks the would-be cycle E_id ↔ m, C1) |
| m_probe | Thm 4.1, (4.24) | E_id, ℓ, c0 | probes | J | ✔ |
| κ^(4) | (4.3) | m, C0, v− | (4.4), (4.6) | J | ✔ |
| A0 | §4.4 | E_id, m, C0 | Lemma 4.3 | J | ✔ |
| B0^(4), q*, s*^(4), h*, x*, D*^(4) | (4.20) | A0, κ^(4), d, C4^(4) | kernels | J, Θ, ζ | ✔ |
| C1 | §4.4 | m, C0, q*, x* | (3.2) | J | ✔ |
| C_abs, C_a^(3) | Lemma 3.4, 3.8 | m, C1, group data | (3.30), (3.47) | J (claimed; (3.5) and (3.26) are J-free) | ✔ |
| J0; J | Thm 4.1; after (3.37) | m, ℓ; C_a, G | everything in §3 | — | ✔ (only J depends on m, C1) |
| C_h, C′, C′′, r0^(3) | (3.42)–(3.45) | m, C1 (C_h); A* | large/small rank | — | ✔ (r0/N = O(T/L^c) → 0) |
| C2 (= exponent of \|k\|) | Def 3.3 | K0 in application | x-thresholds only | E_id | ✔ |
| D2 (minor-arc saving) | §5.3 | D0, C1, cell/character costs (q*, h*, x*) | C′ | J | ✔ |
| C′ (Dirichlet approx.), C_arc | §5.3 | D2, κ^(4), C^(5) | arcs | — | ✔ |
| A (local energy) | (5.11) | C_arc, C8^(5), D2 | A_s | — | ✔ |
| A_s | §5.6 | A, C11 | E-set | — | ✔ |
| B0^(5) (Lemma 5.4) | §5.7 | A, C12, C^(5), τ, η | \|t\| ≥ L^{B0} | — | ✔ |
| B (discrepancy) | §5.8; §6.6; (iv) | B0^(5), A, C_arc, C^(5) (moduli, frequencies up to L^{C8+1}) | (5.4) | — | ✔ chosen last in Thm 5.1/6.1 |
| S_proxy (cell precision Δ_L = L^{−S}) | (v) | B (S > 2B+3) | Lemma 7.3 | coefficient bound (=1) | ✔ |
| PNT/SW accuracies | (v) | S_proxy | (7.13), (7.20) | — | ✔ |

**Cycle search, case by case.**
- **E_id vs (m, C1).** No cycle. E_id depends only on E, C_v, C_s. C_v comes from (3.21)–(3.22), which involve only q, ρ, v, v±. C_s comes from sup_{z≥M} q^{z−M}(z−M+ℓ)_ℓ/V^ℓ, which does not involve m, C1 or J.
- **J vs C_a.** No cycle. Lemma 3.8's per-group costs (3.26), 4^{t_g}, 2^{t_g} and V_g^{b−a} involve t_g ≤ ℓ+m only.
- **C4 vs K0.** C4 depends on K0, but K0 depends only on §6's J-, m- and C4-free exponents (C3^(6), C5^(6), C_f, D*), and the Ψ fed to Theorem 5.1 is K0-free. **No cycle.** This answers the lift seat's open question: §6 fixes C^(5) (via K0) before invoking Theorem 5.1, so C4 > max(C, C7)+1 is legitimate.
- **B vs S.** No cycle. |α| = |I − c_I·1_{rough}| ≤ 1 for every S, because both tests select subsets of the rough integers of the cell ("Hence 0 ≤ c_I ≤ 1 exactly"). τ*, η* (hence B0^(5)) are fixed in (iii) before (iv).
- **C_arc vs q*, h*, x*.** C_arc is chosen after and only needs to beat their fixed costs.
- **D1 vs D2 vs A vs A_s vs B0 vs B.** These form a linear chain.

**I found no cycle.**

---

## 3. Classic holes across the paper (Scope item 3)

### 3.1 A lemma assuming the conclusion's strength
None found.
- Lemma 7.3's discrepancy is proved from Siegel–Walfisz plus Lemma 2.9 inside cells, not from Type II.
- Prop 7.2 is proved by large sieve plus SW. I recomputed its four-term bound xL^{O(1)}(R^{−1}+P^{−1/2}+U^{−1/2}+R/√x) from Theorem 2.3, Cauchy–Schwarz and PU ≍ x.
- Theorem 4.1 does not use transference.
- Theorem 5.1's major arcs use only (5.4).

### 3.2 Citations carrying weight
| cited result | paper's claim | source (verbatim; version read) | verdict |
|---|---|---|---|
| Efron–Stein [5] §2 Decomposition Lemma (JSTOR scan, pp. 587–588) | p.33 "orthogonal product-space decomposition of Efron and Stein"; components "separately mean zero in each indicated probe and independent of the other probes of their block" | p.587: "Here we do not have to assume that the X_i are identically distributed, nor that S is symmetrically defined … The only assumption is that ES² < ∞." "DECOMPOSITION LEMMA. The random variable S(X_1, X_2, ⋯, X_n) can be expressed as (2.4) S = µ + Σ_i A_i(X_i) + Σ_{i<i′} B_{ii′}(X_i, X_{i′}) + ⋯ + H(X_1, ⋯, X_n), where all 2^n − 1 random variables on the right side … have mean zero and are mutually uncorrelated with each other." | MATCH. The paper's partial version (decompose by block-1 probes, other coordinates as parameters) is the lemma with the non-probe coordinates grouped into one variable. Equal norms under symmetry: same page, "the functions A_i(·), B_{ii′}(·,·), ⋯ do not depend upon the subscripts". |
| Ford–Halberstam [8] §1 Lemma 1 (author copy) | p.8 "the product of block upper bounds and its one-block correction are the inequalities of Ford and Halberstam" | "Lemma 1. Suppose that 0 ≤ x_j ≤ y_j (j = 1, …, r). Then (4) x_1 ⋯ x_r ≥ y_1 ⋯ y_r − Σ_{ℓ=1}^r (y_ℓ − x_ℓ) Π_{j≠ℓ} y_j." with "(5) 0 ≤ y_ℓ − x_ℓ ≤ Σ_{d\|(a,P_ℓ), ν(d)=k_ℓ+1} 1" | MATCH. I also re-derived U_j = C(t−1, h_j) for t ≥ 1, U_j − I_j ≤ E_j = C(t, h_j+1), the disjoint supports, and the level Σ h(j+1)2^{−j} + 1 ≤ 4h+2. |
| MV draft [15] Thm 19.16 → Thm 2.3 | Σ_{r≤R}(r/φ(r))Σ*\|Σ_{n∈I} a_nχ(n)\|² ≪ (H+1+R²)Σ\|a_n\|² | "Theorem 19.16 Let M and N be integers with N ≥ 1, and let S(χ) be defined as in (19.28) [S(χ) = Σ_{n=M+1}^{M+N} c_n χ(n)]. Then for any integer Q ≥ 1, Σ_{q≤Q} (q/φ(q)) Σ★ \|S(χ)\|² ≤ (N + Q²) Σ_{n=M+1}^{M+N} \|c_n\|²" | MATCH (N ≤ H+1) |
| MV draft [15] Cor 16.6, Thm 16.7 → Lemma 2.7 | (i) f′ monotone in [j+λ, j+1−λ] ⇒ ≪ λ^{−1}; (ii) λ ≤ \|f″\| ≤ Cλ ⇒ ≪_C Hλ^{1/2} + λ^{−1/2} | "Corollary 16.6 … f′(x) is increasing … ∥f′(x)∥ ≥ M_1 … Then \|Σ_{a≤n≤b} e(f(n))\| ≤ 2/(πM_1)." "Theorem 16.7 … 0 < M_2 ≤ f″(x) ≤ AM_2 … Σ e(f(n)) ≪_A M_2^{1/2}N + M_2^{−1/2}. If instead we have −AM_2 ≤ f″(x) ≤ −M_2, then the same bound applies" | MATCH (decreasing f′ by conjugation; continuity of f″ forces constant sign) |

### 3.3 Hedge words at hard steps
Counts in the plain text: "clearly" 0, "similarly" 1, "standard" 1, "the same argument" 2, "For completeness" 5, "It follows/it follows" 5, "negligible" 6.

| location | phrase | finding |
|---|---|---|
| Cor 2.4 | "the same argument applies" | Induced characters; trivial. |
| p.16 | ghost factor "similarly split" | Definition. |
| p.42 | "standard prime-polynomial moment argument" | Lemma 5.2 is then proved; I checked the j0! fiber bound and the exponent exp(O(L^b + L^{1−a} log L)). |
| p.58 | "For I_pr this is the same argument with one prime" | Correct. |
| p.24 | "For completeness, these conditional row bounds can be iterated although a pivot may have died before its dependent birth" | **The one hedge at a genuinely hard step**, the large-rank backward induction in §3.8. Read, plausible, not reconstructed. |
| p.31, p.45, p.51, p.65 | "For completeness" | The noncircular choice (4.20) (I checked the logic, not each margin); the §5.8 order (verified, table above); the derivative bounds for the pulled-back cutoff (verified in substance); the binomial inequality (trivial). |
| p.13, p.22, p.37–39 | "negligible" | Each comes with a quantitative bound that I spot-checked: (3.9) exp(o(L)) via 0.52+d<1; the µ̃ vs µ density change O_J(L^{C1}sN/P*); shared exclusions L^{O_J(1)}e^{−L^a}; the square-multiple error Y L^{O(1)} e^{−L^a}. |

"Uniformly" occurs 25 times. I checked the load-bearing ones:
- Theorem 3.5 (uniform in ζ given (3.6));
- Lemma 4.3 (uniform in α ∈ ℝ, |ζ| ≤ L^{C4});
- Lemma 7.3 (uniform over intervals K inside a dyad);
- Lemma 5.2 (uniform in b_s);
- §6.3 (independent of K0).

None is misused.

---

## 4. Uses of the structural hypotheses (Scope item 4)
| hypothesis | where used | correct? |
|---|---|---|
| big groups are **intervals** of primes | (4.9) only: fixing all labels but one, the log-cell condition plus the group cuts the last prime to an interval, so SW applies with modulus ≤ Q² = L^{2q*} ≤ (log p)^{2q*/c}. That drives (4.11), (4.18), (4.19). §7.1's big groups {log p ∈ [c3 s_j, c4 s_j]} are intervals. | ✔ |
| ℓ ≥ 1 | (i) θ_m = 2ℓ^ℓ m^{−ℓ} < 1 for large m (4.23–4.24), the "only use of large m"; (ii) rare transfer needs D = C(J+ℓ, ℓ)^{\|S\|} > 1 (3.29–3.32); (iii) small-mark extraction needs t_{g_s} = ℓ ≥ 1 (5.12). §7 takes ℓ = 1. | ✔ |
| 0 < q < 1 | (3.5) sup_z V^{−t}(z+t)_t q^{z/2} < ∞; ρ² > √q with ρ < 1 for (3.21), (3.26); Lemma 3.10's sup q^{z−M}(z−M+ℓ)_ℓ; (5.2). §7 takes q = 1/2. | ✔ |
| d < 0.47 | exp(L^d) < W = exp(√L), so W-rough m, p are P-free (§5.1, §6.1); Cor 3.11 needs log H = O_J(TL^d) = o(L^{0.52}); §6.2 needs 1−d > 1/2. §7 takes d = 2/5. | ✔ |
| 0.52 + d < 1 | Lemma 3.6: log Q_act = O_J(NTL^d) = o(L), and the exp(o(L)) count of Bonferroni terms beats X^{−1} ≤ x^{−γ}. | ✔ (0.92 < 1) |
| η < 1/4 | Lemma 5.3 needs only η < 0.4 (U ≍ Y/(PP′) > Y^{0.6}); Lemma 5.4's "η < 1/4" is unused (W4). Application: η = η* < b*/4. | ✔ |
| δ < 1/4 | Only via c2 s′ < δ (top band below x^δ) and the final P⁺(p−1) ≤ x^δ; nothing in §3–6 needs δ < 1/4; the abstract's "every δ>0" follows by monotonicity, as the text says. | ✔ |
| every prime factor of u ≥ L^{20} | Prop 7.2's (u,d)>1 correction: (L/log L)·L^{−20}·O(L) ≪ L^{−18}; (7.29): Π_{l\|D1}(1−1/l)^{−3} bounded since ω(D1) ≤ log x^{1/20}/log L^{20}. Smallest Q-band c1 s_{jx} ≥ 20T; P-primes ≥ exp(L^{1/10}). | ✔ |

---

## 5. Objections (numbered)

**W1 — Theorem 5.1 (§5.1, p.35; §3.9, p.26; §5.3, p.39). UNCLEAR (not an error).**
Quoted: "We impose the following condition on the α of at least the first endpoint" (p.35). "Constancy on a mark fiber is needed only at the first endpoint; the second endpoint can be any vector with the stated norm." (p.26). "Its proof uses three features of the first endpoint" (p.39).
- **What I found.** The proof uses no feature of the second endpoint beyond invariance and τ²-size (§1.1). So it in fact claims the dual statement of §1.1: cancellation of F0 along dilated progressions {ab − k}. That is a new one-sided, single-scale Elliott-type theorem at power-log precision.
- **Status.** No counterexample was found (§1.2). Its truth is exactly as strong as Theorem 3.5 plus Theorem 4.1.
- **Fix/remark.** None needed for correctness. A reader should know that the "admissible shape" of G0 is a red herring.

**W2 — ideal frequency range (§5.2 p.37; §5.8 p.45). COSMETIC/UNCLEAR, exposition.**
Quoted: "The required ideal frequency is ζ = −a1 − a2 − v." and "the fixed Mellin cutoff fixes the ideal frequency range".
- **What is wrong.** The range must cover |a1 + a2| + L^{C7}, not just the Mellin cutoff. In the §6.6 application a1 + a2 = ξ3 with |ξ3| ≤ L^{C8^(6)+1}, which depends on K0. So C4^(4) depends on K0.
- **Status.** No cycle: nothing chosen before K0 depends on C4 (§2).
- **Fix.** State C4 > max(C, C7) + 1 before invoking Theorem 4.1 (the lift seat raised the same point; §2 settles §6's side).

**W3 — §7.7 (ii) vs (v) (p.64–65). COSMETIC, exposition.**
Quoted: "(ii) Fix κ ∈ (0, 1/50) so small that C_bal κ < S/4." and "(v) Choose S sufficiently large in Theorem 7.3 for that exponent".
- **What is wrong.** Read literally with one S, step (ii) would depend on step (v), which is a cycle. The S in (ii) must be the singular-series constant S = 2Π_{p≥3}(1 − (p−1)^{−2}) of (7.9). With that reading (7.22) leaves SX_A/(2L), and C_bal κ < S/4 leaves SX_A/(4L), so there is no cycle.
- **Fix.** Rename one of the two.

**W4 — Lemma 5.4 statement (p.43). COSMETIC.**
Quoted: "Fix τ > 0, η < 1/4, C > 0, and A > 0."
The proof never uses η < 1/4: only P′ ≥ x^τ/2, d ≤ D = x^{o(1)}, and |u| ≤ x² with K = ⌈4/τ⌉ + 3 derivative orders.

**W5 — Notation overloads that straddle the order-of-choices arguments. COSMETIC, but they make verification error-prone.**
- **C4.** §6.4: "Their derivatives of order j … are O_j(L^{C4(j+1)}), with C3, C4 independent of K0". Theorem 4.1's C4 depends on K0 (W2).
- **C6.** §5.2's C6 is "independent of J and the probe count", while §6.6 says "C6 now allowed to depend on K0". These are different objects.
- **C7, C8.** Same clash between §5 and §6.6.
- **B0.** Three meanings: Lemma 4.3's dyadic precision, Lemma 5.4's threshold, and B0 = AA* in Corollary 3.11.
- **S.** Four meanings: small-group index set, S = L^{s*} in Lemma 4.3, the proxy precision, and the singular series (W3).
- **D.** The count (3.29) and the edge product.
- **Others.** κ ((4.3) vs §7); h (sieve degree, cell width, cofactor of u); θ (Fourier variable, (7.24), §6.2 tilt, θ_m); A (operator, saving, weight A(u), free set).

**W6 — Theorem 3.5 is the single point of failure (§3, pp.10–26). COULD NOT CHECK (inside of the proof).**
Quoted: "Only the rare-transfer estimate needs the complexity-dependent choice of J; the ideal accuracy is fixed beforehand."
- **Checked** (§1.4): the quantifier order; the per-visit/per-edge cost accounting (nothing besides G_i costs L^{c} per visit); Lemma 3.6's relative-error summability; (3.28); Lemma 3.9's U < p distinctness; Lemma 3.10's Fourier reduction; the r < r0 = o(N) bookkeeping in (3.47).
- **Not reconstructed:** the full bijection of Lemma 3.7 and the backward induction behind (3.44).
- A FATAL error, if there is one, is most likely in these two places. I have no specific sentence to point to.

No FATAL or GAP objections.

---

## 6. Steps verified line by line vs skimmed

**Verified line by line (re-derived):**
- §5.2 lift. The normalization V_g^{−M−t_g} = V_g^{−s_{R,g}−2t_g}, the 1/D_R → harmonic draws, ω_g(D_R w) − M = ω_g(w) − t_g, the phase identity, and the raw pattern = (5.5) including the conjugate on F0 (PDF p.35 shows the conjugate F̄0 in (5.5)).
- The endpoint-norm computation and its J-independence.
- The Mellin step ζ = −a1 − a2 − v.
- §5.3 minor arcs. The collapse to ρ(n) ≤ L^{O(1)}/n, Lemma 4.2 with U0, V0 ≥ exp(L^c), Dirichlet approximation of kθ, the arc count L^{2C_arc+O(1)}, and Cauchy–Schwarz on arcs.
- §5.4 the unit claim (r/d0, q0) = 1.
- §5.5 the Plancherel direction (|K̂| ≥ 1/2 gives an upper bound for the arc energy) and the normalization H^{−2}·Y·h² = Y^{−1}.
- §5.6 outside-E (Y/P ÷ 2L/h = H/(2LP) → ∞); Lemma 5.2 (j0! fibers, N_E exponent); Lemma 5.3 (Gram rows U log Y + RY^{1/2}, (5.20) in both ranges, Schur).
- §5.8 the three regimes and the order of choices.
- §6.5 forward and converse determinant identities (m h′ − m′ h = k(mn − 2eh) = k; m | 2eh+1 from (m,k) = 1).
- §6.6 endpoint identification (6.22)–(6.23) by direct substitution, including h^{iϱ} = z^{iϱ}(m′)^{−iϱ} and c̄_r.
- §6.3 allocation induction (why x^{b*/2}: u_P ≤ x^{b*/4} plus exceptional integer ≤ x^{η*} < x^{b*/4}), the skip step via (6.1), and the frequency bound (6.9).
- §6.4 Cauchy–Schwarz and diagonal.
- Corollary 3.11 in full.
- §4.4 the proof of Theorem 4.1: Efron–Stein components; the vanishing for A ⊄ U or B ⊄ V; the conditional use of Lemma 4.3 with α = ΘC; (4.26); the exceptional-pair identity R(F_full, H′) + R(F′ − F_full, H_full); θ_m via max x^m(1−x)^ℓ; tensorization by cardinality profiles; the 3^P count.
- Lemma 4.2 and (4.6).
- Lemma 4.3 logic in both regimes (constants in (4.20) only skimmed).
- Lemma 3.6.
- (3.42), (3.45)–(3.47) and the inequality after (3.47).
- Lemma 3.9's argument.
- Lemma 2.9, Lemma 2.6, Lemma 2.7 vs MV, Theorem 2.3 vs MV.
- Prop 7.2's four-term bound.
- Lemma 7.3 (0 ≤ c_I ≤ 1; full-cell cancellation for principal characters; last-prime SW; proxy via sieve in classes).
- (7.18) symbolically (minimum-coordinate decomposition, l/l! = 1/(l−1)!).
- (7.19); (7.21)–(7.22) arithmetic and the direction of every subtraction.
- §7.7 final count and P⁺(p−1) ≤ x^δ.
- §8 (k = ⌊X^{2δ}⌋ ≤ M, (8.1), (8.2) with exponent O(X^δ log X) = o(k log X), and g(n) ≥ X^{(1−3δ−o(1))k} > n^{1−ε} from n ≤ X^k).

**Read but only skimmed / spot-checked:**
- Lemma 3.7 (bijection: only case-checked).
- (3.13)–(3.25): spot-checked (3.20), (3.25), (3.19)'s factorial identity.
- Lemma 3.8's column bound.
- The backward induction around (3.44).
- The phase insertion in ghost batches (§3.8).
- (4.9)–(4.11) constants; (4.20) margins.
- §6.3's smooth-separation constants.
- §7.1's localization lower bound.
- §7.6's two-variable sieve (7.27)–(7.30).
- Lemma 5.4's van der Corput exponents δ_k.

---

## 7. Verdict for this scope

**HOLDS AS READ at the whole-paper/interface level.**
- The global order of choices is acyclic (§2).
- The interfaces §3 → §5 (Corollary 3.11 → lift), §4 → §5 (comparison family → circle method), §5 → §6 (endpoint identification), §6 → §7 (Type II with the S-independent proxy coefficient) and §7 → §8 are correct as written.
- The structural hypotheses are used correctly (§4).
- Theorem 5.1: no counterexample, with the obstruction analysis in §1.2. As proved it is stronger than stated (W1).

**COULD NOT CHECK:** the exactness of the memory identity (Lemma 3.7) and the distinct-birth restoration (§3.8) inside Theorem 3.5. Every parity-breaking claim of the paper rests on these two, and a mistake there would be invisible to all the checks above.

Objections: W1–W6. W1 and W6 are UNCLEAR/COULD NOT CHECK; W2–W5 are COSMETIC. None is FATAL or GAP.
