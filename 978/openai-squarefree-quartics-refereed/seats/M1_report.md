# Seat M1 — hostile referee report

**Scope:** printed §2 (Prop 2.1, Rem 2.2, Lemma 2.3, proofs of Cor 1.2 / Cor 1.3), §3 (Theorem 3.1, Lemmas 3.2–3.4, the counting tree), §4 (Lemmas 4.1–4.2), §10 + Appendix A (Prop 10.1, Table 1, the exact certificate, A.1), §11 (assembly of Prop 1.4). §§5–9 were taken as black boxes. For each I checked that the statement §11 uses matches the statement that section proves.

**Method:** I read the LaTeX and PDF text line by line. I re-derived every inequality the certificate asserts in my own exact-arithmetic checker and ran six mutation tests against it. I fetched the cited sources (Reuss arXiv:1307.2802v1, Xiao arXiv:1505.05587v2) and checked them against how the paper uses them. I read the quartic and medium-degree parts of the Lean. I compiled nothing.

Everything is in `/tmp/oaimath/020/seats/M1_work/`:
- `cert_v2.py`: my checker. It derives R(A,B) independently, encloses every radical rigorously to 1e-30, and checks cell coverage, the direct range and the shift inequality. Mutations run with `python3 cert_v2.py mut`.
- `cert_v2.out`, `mutations.out`, `shift_mut.out`, `cut_margins.out`: saved outputs.
- `paper_cert_full.py` / `.out`: the paper's own Appendix A listing, verbatim (main program and A.1). All asserts pass.
- `paper_instrumented.py`: the same listing, instrumented to report where each minimum gap occurs.
- `hilbert_sanity.py`: checks that R(A,B) is the leading term of the actual bigraded Hilbert function.
- `lean_quartic_bins.py`: recomputes the Lean's quartic bins.
- `refs/`: the Reuss and Xiao PDFs.

---

## 1. Section 2 (sieve transfer): HOLDS

- **Normalization.** (2.2) `ρ_f(p^k) = p^e ρ_g(p^{k−e})` is correct for every e = v_p(c) ≥ 0. p^k | f(a) is equivalent to p^{k−e} | g(a), and each class mod p^{k−e} has p^e lifts. If e ≥ k then every value of f is divisible by p^k, so ρ_f(p^k) = p^k and admissibility fails; admissibility therefore forces e < k. The claim "Once X exceeds every prime divisor of c, the large-prime exceptional sets for f and g are therefore identical" is correct, because p > X forces p ∤ c, and then p^k | f(n) ⇔ p^k | g(n). So T_g really is the tail of the **primitive** g, which is exactly what Prop 1.4 bounds (it needs primitive, irreducible, positive leading coefficient, 4 ≤ d ≤ 8).
- **(2.3)–(2.5).** Hensel lifting outside 𝓑 is fine. The tail bound uses Σ_{m>Y} m^{−k} ≤ Y^{1−k}/(k−1), which is correct.
- **Order of limits.** Y is held fixed while X → ∞, with the CRT error O(Q_Y). The intermediate primes contribute at most (d/(k−1))Y^{1−k}X + dπ(X). Then Y → ∞, then the dyadic intervals are summed with J fixed, then J → ∞. Every limit is taken in a legitimate order, so there is no transfer failure.
- **Lemma 2.3.** The inclusion (inputs counted by B_{f,Y} − S_f) ⊆ (inputs counted by B_{g,Y} − S_g) is correct: g | f up to the constant, and p > Y forces p ∤ c. The two limits give c_{f,Y} − (c_{g,Y} − c_{g,k}) ≤ liminf, as claimed.
- **Cor 1.2 for d ≥ 9 (Xiao).** Xiao's Thm 9.1 (arXiv v2, §9) states: "Let f(x) ∈ Z[x] be an irreducible polynomial of degree d ≥ 3. Suppose that k ≥ (3d+1)/4. Then #{n ∈ Z∩[1,B] : f(n) is k-free} ∼ c_{f,k}B". Xiao's (1.5) defines c_{f,k} = ∏_p(1 − ρ(p^k)/p^k), the same Euler product the paper uses. Xiao needs neither primitivity nor a positive leading coefficient, so the paper's restriction to "the primitive positive-leading part" is harmless but unnecessary. The arithmetic d − 2 ≥ (3d+1)/4 ⇔ d ≥ 9 is correct.
- **Cor 1.3, case d = k+1 (Reuss).** Reuss never states "o(X) triples with a > X^{1−δ}" as a lemma. The estimate is assembled from two pieces:
  - the last paragraphs of the proof of Reuss's Lemma 3, which bound the triples with a > X^{1−δ} and dispose of B ≪ X^{1−δ} (this covers large A, i.e. a > X^{1+δ}) via Heath-Brown's Thm 15;
  - Reuss §6 "Finishing the Proof", which gives N(X;A,B) ≪ M^{1−1/d} X^{1−1/d+ε} for A, B ≍ X^{1±δ}.

  Reuss counts (n,a,b) ∈ ℕ³ with n ∼ X, which matches the interval X < n ≤ 2X. The paper also correctly notes that positivity of g(n) is needed to take a = p. The citation "Lemma 3 and its proof, and Section 6" is accurate. EXPOSITION only: the assembled statement could be spelled out.
- **Cor 1.3, case d = k+2 ≥ 9.** Xiao's E(ξ) is "#{x ∈ [1,B] : ∃ b > ξ, b^k | f(x), μ²(b)=1}", and his §9 bounds E(B^{1−δ}). With B = 2X, a prime p > X > (2X)^{1−δ} qualifies, so the citation is correct.
- **Cor 1.3, cases d ≤ k.** Correct, including d < k (the tail is eventually empty) and d = k (π(C_g X) = o(X)).

## 2. Section 3 (affine counting with adaptive primes): HOLDS

I checked each step:
- **Lemma 3.2.** The descent to Q-components via σ(A) ∩ A is sound. The generic Jacobian rank N − h of I(A)_{≤e'} follows from the projection-and-separability argument. The nullspace W of an integer evaluation matrix with boundedly many columns has a spanning set of height X^{O(1)} (cofactors). Bézout bounds the length of the patch list and every degree independently of coefficient heights, and the construction is deterministic in (Z′, S).
- **Lemma 3.3.** Hensel lifting at q ∤ Δ(z) gives integral power-series coordinates on the entire residue class, so the q-adic valuation of the determinant is at least s_h(L). The weight of the j-th monomial is at most δ_h(h!j)^{1/h} + O(1), which follows from (3.2) with a constant C_1 depending only on C_e and δ_h. ν s_h(L) > C_2 L once L is large. The resulting linear combination does not vanish on A because the chosen monomials are independent on A.
- **Lemma 3.4 (deletion).** This is the genuinely new step, and it is correct:
  - The record (3.6) is lexicographically non-increasing when a prime is added: kernels are nested, and equal codimension forces equal kernels and hence equal deterministic patches.
  - Averaging over T_0 consecutive block sizes gives P(change) ≤ B_0/T_0.
  - Conditional on B′ = B∖{q}, the deleted prime q is uniform on P_i∖B′, and the minors of the deleted path have only O(1/ζ) prime factors ≥ X^ζ.
  - The containment {q divides a full-path minor} ⊆ {record changes} ∪ {q divides a deleted-path minor} is right.
- **Tree accounting.** (3.10) holds because Σ_{j≤i} a_j = E_{h_i}, together with (3.8). The branch count (3.11) is right: isolated zeros of a square system are bounded by Bézout without any good-reduction assumption. (3.12) telescopes to Σ_h E_h. The order in which γ, D_i, B_0, ξ, T_0, ζ and then X are chosen is non-circular.
- **Consistency checks.** I tested Theorem 3.1 against known bounds:
  - r = 1, unweighted, degree e: it gives X^{1/e+ε} (Bombieri–Pila).
  - Surfaces: it gives X^{1/√e + δ_1} (Heath-Brown).
  - Full space with unequal weights: Σ_h GM(top-h weights) ≥ Σω, so it never beats the trivial count.

  No contradiction with any of them.

**Uniformity map, and the weakest link.** Within §3 every constant is coefficient-free:
- Bézout degrees;
- isolated-zero counts;
- heights X^{O(1)} for the minors, which bound their number of large prime divisors;
- the L of Lemma 3.3, which depends only on (δ_h, C_e, weights, ν).

Theorem 3.1 deliberately moves all uniformity into its hypothesis: "The constants in these alternatives are uniform in X, Z, S, A." The weakest link is therefore not inside §3. It is the hypothesis (3.2)/(3.1) as supplied by Prop 7.1, Prop 8.1 and Prop 9.2, which must hold for every Q-irreducible subvariety of degree ≤ e of moving cut sets, written in moving unimodular coordinates whose heights are X^{O(1)}.
- Prop 7.1's uniformity argument is clean: the Hilbert series (7.7) is determined by (h, A, B, Q, E), and only finitely many values occur.
- Prop 9.2 (curves) is the most delicate. That is the other seat's territory, but its stated uniformity ("may also depend on a fixed compact subset … containing U, V"; uniform in the integral changes) is exactly what §11 needs.
- In §11 only **finitely many** weight vectors (U,V) = (u+j+τ, v+j+τ) ever occur. They are finitely many cells times finitely many j ∈ τℤ ∩ [0, m/d]. So uniformity over a continuum of weights is never needed.

## 3. Section 4 (factorization, balancing, paired boxes): HOLDS

- **Lemma 4.1.** Dedekind–Kummer applies outside the primes dividing c, disc F and [O_K : ℤ[cθ]]. 𝔭 is the degree-1 prime attached to the simple factor T − cn. Its valuation in (cn − cθ) is v_p(f(n)), because no other prime above p contains cn − cθ.
  - Class group: 𝔭𝔠 is principal for a fixed representative 𝔠.
  - Unit step: the weighted log vector minus (1/d)·log(pN𝔠) lies in the weighted sum-zero hyperplane, and Dirichlet moves it into a bounded fundamental domain. This gives |σ_i α| ≍ P^{1/d} with constants depending only on f (regulator, class representatives).
  - μ = cq with q·𝔠^{−k} ⊆ O_K makes β integral. |n − θ_i| ≍ X gives |σ_iβ/μ| ≍ X/P^{k/d} = X^{b/d}.
  - "At most d values of n per α" is correct because p^k > X.
- **Lemma 4.2.** κ ≍ 1. The forward map's normalising denominator is κ. The reverse map needs local k-th roots, at most k^d branches, continued from a counted point to the grid base over distance O(M^{−1} + X^{−1}). Derivatives are bounded on fixed-radius polydiscs. The partner bound needs w < 1, which the certificate guarantees (m < 1).

## 4. Section 10 + Appendix A: exact recomputation

**Paper's code, verbatim.** The main listing and A.1 run, and every assert passes.

**My independent checker.**
- R(A,B) is computed as the leading term of the (d−2)-fold (k,1)-difference of C(A+d−1,d−1)·C(B+d−1,d−1). It matches (5.1) exactly. H, H_a, H_b match (10.7) and the code's `polynomials`.
- The ratio HF/R tends to 1 for d = 4..8 (for d = 8: 0.850, 0.960, 0.990 at A = 200, 800, 3200).
- t* is chosen by any rule and then verified exactly. My t* agree with the paper's prescription at every minimising cell.

| d | z_d | cells | true min gap 1−m−ΣE_h (rigorous, 1e-30) | where | paper Table 1 (rounded lower bound) | final exponent incl. dτ |
|---|---|---|---|---|---|---|
| 4 | 5124 | 2124 | **0.0019350** | z=3555, η∈[1.18500,1.18533], t*=47/50, w=5967/25000 | 191/100000 = 0.00191 | 0.998145 |
| 5 | 4084 | 1084 | 0.0058911 | z=3000 (η=1) | 293/50000 = 0.00586 | 0.994209 |
| 6 | 3552 | 552 | 0.1284445 | z=3000 | 321/2500 = 0.1284 | 0.871676 |
| 7 | 3226 | 226 | 0.2318140 | z=3000 | 23177/100000 | 0.768326 |
| 8 | 3003 | 3 | 0.3168660 | z=3000 | 31683/100000 | 0.683294 |

Every Table 1 entry is a valid lower bound for the true gap, and the stopping indices agree.

**Other margins.** All are strictly positive and exact:
- **Mode Q:** min(999/1000 − m − 2u) = 0.0055733, at z = 3999.
- **Ratio window:** v/u stays in [0.1717, 4.9040] ⊂ [3/20, 5].
- **m slack:** min(η_−, b_−) − m ≥ 0.232.
- **Cut inequalities (10.4):** the first has relative margin only **1.5e−8** (d=4, z=4902). This happens because w is the least grid point that works. The inequality is strict, so it is valid, but the "sufficiently large A, B" in Prop 5.2 must be enormous there. Harmless, since nothing effective is claimed. The second cut inequality has margin ≥ 0.038.

**Coverage.**
- The cells [z/3000, (z+1)/3000] are closed and contiguous from η = 1 to z_d/3000.
- φ(z_d/K_0) < 0.2495 ≤ φ((z_d−1)/K_0) for every d.
- φ' = 1 − 2kη/d ≤ (4−d)/d ≤ 0 for η ≥ 1.
- The direct range uses the exhaustive 1e−4 grid plus the overshoot pair (e, d/k + e). The worst value of b′η′/d is 0.2495367 (d=8), against a limit of 0.4999² = 0.24990001.
- The shift inequality (10.6) holds: a dense check gives max D(t) on [3/20, 5] = 0.9603, and 20 000 random tests on the actual threshold formulas give a maximum violation of 6e−17 (rounding).

There is no gap between cells, and both endpoints η = 1 and η = d/k (b = 0), plus the overshoot, are covered.

**Mutation tests.** Each mutation must make the checker report failure, and all six do:
- (M-a) Shrinking cell 3500 (d=4) by 1e−6 → **coverage FAIL**.
- (M-b) Raising the stop threshold to 0.26 → **direct-margin FAIL** (0.26 > 0.4999²).
- (M-c) Replacing D = U+V by min(U,V) in δ_d → **gap FAIL** in 1125 cells.
- (M-d) Replacing the quartic curve constant g = 4 by 3 (no quintic removal) → **FAIL** in 434 cells.
- (M-e) Replacing 3/U² by 2/U² in the quartic surface bound → **FAIL** in 609 cells.
- (M-f) Shrinking w by 1% in one cell → **cut FAIL**.
- Separately, widening the ratio window to [0.05, 5] or [0.15, 20] breaks D ≤ 1.

Mutations (d) and (e) show that Prop 8.2 (quintic discard) and Prop 8.1 (quadric/plane 3/U²) are load-bearing for the paper's quartic route.

## 5. Section 11 (assembly): HOLDS

- **Coverage of prime sizes.** p^k ≤ f(n) ≪ X^d gives η ≤ d/k + O(1/log X). The number-field range (φ > 0.2495) lies in [1, z_d/K_0) and is covered by the cells. The direct range (φ ≤ 0.2495) is [z_d/K_0, d/k + o(1)]. Both endpoints are covered.
- **Direct surface.**
  - The surface is irreducible (Gauss's lemma).
  - (11.4) is right: the filtered dimension is N(T) − N(T−D); non-unit roots of unity have pole order ≤ 2 because o | A, B, C implies o | E.
  - δ_2 = √(b′η′/D) ≤ √(b′η′/d) < 0.4999.
  - The curve alternatives with δ_1 = 1/2 are complete: constant x; field degree ≥ 2 giving H ≥ 2T − O(1); a non-polynomial rational coordinate (Lemma 9.1); both coordinates polynomial forcing z constant, hence O(1) inputs.
  - This reproduces Browning's threshold exactly (φ(1) = 2/d < 1/4 ⇔ d ≥ 9), which is a good sign.
- **Number-field range.** The per-pair bound X^{ΣE_h(U,V)+ε} times the O(X^{m−dj}) pairs, with the shift s = j + τ, gives m + ΣE_h(u,v) + dτ + ε < 24979/25000 + ε. The fibre cost is m + 2u − 2j + 2τ < 3122/3125. The pieces are finitely many cells, boundedly many j, charts, ideal classes and components, and O(log X) dyadic intervals (X^{o(1)}). The single quintic set has size O(X^{1/5}). Theorem 3.1's ε is chosen below the margin.
- **Consumed statements match what is proved:**
  - §11 says "the resulting affine sets have dimension at most d−1, except for the mixed-cut components of dimension d". Prop 5.2 says "the corresponding dimensions are d and at most d−1".
  - §11 (11.5) "O_f(X^{m−dj}) pairs, |x′_i| ≪ X^U, |y′_i| ≪ X^V, U = u+j+τ" is Prop 6.2 (6.2)–(6.3) verbatim. Prop 6.2 needs m < min(η_+, b_+); the certificate gives the stronger m < min(η_−, b_−).
  - Thresholds: δ_d = Ψ_d(U+V) comes from §7's "D = λU + s_0V ≥ U+V". δ_h = Ψ_h(min(U,V)) for 2 ≤ h ≤ d−1 comes from (7.6). δ_3 = Ψ_3(V) in mode Q comes from "D ≥ V" after Lemma 6.3. δ_2 in mode Q equals Prop 8.1's min{(2U+V)D_0/(U²V²), 3/U²}. δ_1 equals Prop 9.2's max{U/2, min(U, V/g)}.
  - Prop 5.2's cut conditions (5.2) are identical to (10.4). Its hypotheses ("|x_i| ≪ X^{η_+/d}, |y_i| ≪ X^{b_+/d}", width O(X^{−w}), z = O(X^{−1})) are upper-exponent statements. So checking each cell at (η_+, b_+) is valid on the whole cell, as the paper says.

## 6. Lean comparison

The Lean does **not** formalize the paper's certificate, or its route, in any degree.

- **Quartics** (`RadialFibres.lean`, `QuarticComponents.lean`): `quarticLowerEta j = 1 + j/100`, `quarticUpperEta j = 1 + (j+1)/100`, j : Fin 100, so 100 bins of width 1/100 covering η ∈ [1, 2] **entirely**. There is no direct-surface range.
  - Weights: `quarticU j = (101+j)/400 = η_+/4` and `quarticV j = (200−2j)/400 = b_+/4`. These are the full box sizes P^{1/4} and X/P^{1/2}. There is no paired-box partition (m = 0), no lattice reduction, no archimedean cut, and no quintic removal.
  - The count is done directly on the 5-fold `QuarticBoxSystem 8 5`.
  - Its thresholds differ from the paper's: the curve bound uses V/3 (g = 3, not 4), and δ_2 uses a "pole" bound UV²/(V+4U) that does not appear in the paper.
  - Envelope sums are 0.994 for j < 60 and 0.983 for j ≥ 60, and `quartic_sum` asserts sum + 1/1000 ≤ 997/1000, hence the saving 3/1000. I recomputed all 100 bins: 0 envelope violations.
- **Degrees 5–8** (`MediumDegree.lean`): a single box with |x| ≪ X^{1/3}, |y| ≪ X^{2/5}, no bins, using the norm relation |N(α)| = p·N(J). Saving 3/1000.
- **Degrees ≥ 9** (`HighDegree.lean`): the Lean's own `high_degree_dyadic_tail`, saving 1/2000. It does not use Browning or Xiao.

**The two savings.** The paper's δ_f is never computed. From its own certificate it is at most about 5×10^{−4}: the bottleneck is the direct range, where 1/2 + √(b′η′/d) reaches 0.99954 for d = 8 and 0.99943 for d = 4. The Lean's 3/1000 is therefore larger than anything the paper's route yields, so it cannot come from the paper's certificate. The two are "consistent" only in that both are positive. A kernel-checked Lean certifies the theorem but certifies none of the paper's §§4–11 machinery.

## 7. Objections

| # | Location | Quote | Class |
|---|---|---|---|
| 1 | §11 first paragraph | "Partition the primes p>X into O_f(log X) dyadic intervals [P,2P] … Thus 1≤η≤d/k+O_f(1/log X)." | **EXPOSITION.** η ≥ 1 needs the partition anchored at P = 2^iX. A standard grid P = 2^i puts the first η just below 1, which no main-theorem cell covers; only A.1's ad hoc cell for §12 goes below 1. State P = 2^iX. |
| 2 | Proof of Cor 1.3, case d = k+1 | "the unweighted triple estimates of Reuss [Lemma 3 and its proof, and Section 6] give o_g(X) triples …" | **EXPOSITION.** Correct, but assembled from proof text, not stated by Reuss. Checked against arXiv v1 only; the published BLMS numbering was not checked. |
| 3 | Proof of Cor 1.2 | "applies to the primitive positive-leading part of f" | **EXPOSITION.** Xiao Thm 9.1 has no primitivity or sign hypothesis. Xiao's §9 proof is itself a sketch ("as per our analysis in the binary form case in Section 8"); Browning 2011 is the primary source. |
| 4 | (10.4) / Prop 5.2 | "w = up_{d−1}(…)" | **Remark, not an error.** The first cut inequality holds with relative margin 1.5e−8 (d=4, z=4902). It is strict, so valid, but the implied "sufficiently large A, B" is huge. Irrelevant to an ineffective δ. |
| 5 | Table 1 / Prop 1.4 | "There exists δ=δ_f>0" | **EXPOSITION.** The δ the certificate actually yields is ≲ 5×10^{−4}, set by the direct range, not by the Table 1 gaps. Worth stating, since a reader may take the 0.00191 gap as the saving. |

I found no FATAL issue and no GAP in my scope. The exact certificate is correct, covers the whole η-range with strictly positive margins, and my checker demonstrably fails under perturbation. §§2–4 prove what they claim. The uniformity burden is legitimately pushed into the hypotheses of Theorem 3.1. The statements §11 consumes from §§5–9 match their statements as proved, which I did not audit.

VERDICT: HOLDS AS READ
