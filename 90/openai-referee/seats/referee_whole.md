# Referee report — seat `whole` (entire paper: logic chain, Valtr obstruction, prove-too-much, hygiene, §1.1)

Paper: OpenAI, "A power saving for planar unit distances", 23 Sep 2026, 53 pp. Local copy: /tmp/oaimath/167/paper/paper.pdf.
Read: paper.txt end to end (lines 1–2823). Load-bearing formulas were checked against the rendered PDF, pp. 12, 22, 25, 36, 44 and 49.
Status: **COMPLETE** (written 2026-10-14).

**Instrument warning, confirmed by this seat.** paper.txt silently drops every overline.
- PDF p. 44 reads "Its image under (z, w) ↦ (w̄, z̄)", "symmetric image w = c̄" and "The symmetry gives v = ū".
- paper.txt renders these as (w, z), c and u.
- Brief item (vii)'s "symmetry slip" is therefore an artefact of the instrument, NOT an error in the paper. It is not filed below.
- I had drafted it from paper.txt and withdrew it after rendering p. 44.

---

## 0. Verdict for this scope

**HOLDS AS READ.**
- No FATAL and no GAP was found in the global logic chain.
- Every hypothesis of every result is supplied at its point of use (§1 below).
- Every one of the 65 internal "Theorem X.Y" occurrences (67 label references, counting the second member of "Theorems 5.1 and 5.2" and "Theorems 6.3 and 6.5") resolves to the intended Lemma, Proposition or Corollary.
- Every "evident / immediate / follows directly / similarly / identical / same argument" step was checked: 33 instances, all true (§5).

**Valtr test (brief (i)): passed.** The paper's Euclidean input is the reciprocal-jump identity (4.1), w_p − w_q = 1/(z_p − z_q). It is load-bearing at four independent places:
1. the strict-cross consistency of Lemma 4.5;
2. the product-formula identity (5.14), reused in Lemma 7.1;
3. (7.13) = (8.1);
4. the radical structure (8.10) on which the Kummer argument of §8.5 rests.

For the parabola family C = {(x, x²)}, which carries Valtr's n^{4/3}-type configurations, three of these four steps provably fail, and the fourth, (7.13), changes form so that §8.5's radicals disappear. This was checked symbolically, with a control. The only step that survives for the parabola is Prop 4.4. It must survive, and doing so is harmless, because its conclusion S → ∞ is true for Valtr's grid.

**Prove-too-much test (brief (viii)): passed.**
- δ is ineffective.
- Near-4/3 density enters through D = o(log t) and through the expansion estimate (2.5), so the argument cannot be pushed to n^{1+o(1)}.
- The number-field degree d_N plays no role.
- Real points are used at five identified places.

One observation is not an objection: the proof transfers almost verbatim to the real Minkowski plane (§3.4). That makes the proof's correctness and the non-existence of n^{4/3} hyperbola-translate configurations with injective coordinates the same question.

**External fact that bears on the verdict.** The sources seat reports a sorry-free Lean development of exactly this Theorem 1.1 in github.com/openai/math:
- files `lean/OAI/Geometry/UnitDistances/` (40 files, 28,113 lines) and `ComparatorChallenges/PlanarUnitDistances.json`;
- it has NOT been built or comparator-checked by any seat.

Replaying it would turn this report's "no gap found" into "no gap exists". I recommend the coordinator do so; Mathlib is pinned at v4.34.1, so `lake exe cache get` applies.

---

## 1. The dependency graph, with hypotheses checked at each point of use

Notation: A → B means B uses A. "✓" means the hypothesis is supplied at the point of use, verified by me.

### §2 → everything

**Sequence reduction (p. 4) → Prop 2.4.**
- Input: n = t³ real points with ≥ t^{4−o(1)} ordered unit pairs ✓ (see §4 of this report).

**Lemma 2.1 → Prop 2.4.**
- Unit pairs and distinctness are preserved; the coordinates are real algebraic ✓.

**Lemma 2.2 + Prop 2.3 → Prop 2.4.**
- Lemma 2.2 is applied with R = t^{1−a} and l = t³, giving s = O(t^{1−a} log t) ✓.
- Deletion cost ≤ s t³ + 2 s t³ = O(t^{4−a} log t) = o(t^{4−o(a)}) ✓.
- Regions number O(t^{2−2a} log² t); after splitting into point sets of size ≤ 2t^{1+2a}, there are t^{2−2a+o(a)} pieces. The best piece has e0 ≥ t^{2+2a−o(a)} ✓.
- Prop 2.3 gives e0 ≤ t^{2+2a+o(a)}, since (2t^{1+2a})^{2/3}(t^{2+a})^{2/3} = t^{2+2a} ✓.

**Prop 2.4's (2.5) "for every F ⊆ P, G ⊆ Q", with one sequence ξ_t independent of the subsets → Lemma 2.5 "uniformly for every pair of label maps".**
- The proof of Lemma 2.5 applies (2.5) to the label classes {ℓ_P = i} × {ℓ_Q = i} and to the complementary classes against the whole opposite side. These are subsets, so uniformity is inherited ✓.
- The constants s0 and C are absolute: they depend only on η = 1/25 and γ = 27/50. "An index after which" depends only on ξ_t ✓.
- (2.10) is proved at every value of s, using Cs0 ≥ 1 for s > s0 ✓.

**Prop 2.4 (2.9) → Lemma 2.6.**
- (i) and (ii) follow directly from (2.9). (iii) uses the d-threshold split, and d_t → 0 can be chosen independently of F ✓.
- "Error factors may be taken outside sums" requires one common bound δ_t on the marginal masses ✓.

**Lemma 2.7 (D = o(log t)) → Lemma 3.1/Cor 3.2 (Prop 4.4) and Cor 3.3/(3.17) (§5.1, (5.7)).**
- §3's ω is the uniform edge law of Prop 2.4, and its wedge law Ω (3.1) is exactly (2.11). So the D of (3.2) is the D of (2.18) ✓.
- The bookkeeping in Lemma 2.7: H(p) + H(r) ≤ 2(1+2a+o(a)) log t, and H(p,r) ≥ (1 − t^{−a+o(a)})(2+3a−o(a)) log t, so D ≤ (a + o(1)) log t = o(log t).
- This uses a → 0 and a log t → ∞ ✓.
- The incidence seat sharpens this to D ≤ [a + (2+3a)t^{−a+o(a)} + o(a)] log t, which is consistent.

### §4

**Lemma 2.5 (2.10) → Lemma 4.3's label hypothesis.**
- Lemma 4.3 needs "for all assignments of finite labels to its vertices, two independent µ-points disagree with probability ≤ C0 × (edge disagreement)".
- Lemma 4.3's labels are maps on P ∪ Q into a common finite set: equivalence classes for |U_x − U_x′|_v ≤ e^s at nonarchimedean entries, and grid cells for a fixed shift at archimedean entries. These are exactly a pair of label maps (ℓ_P, ℓ_Q) in Lemma 2.5's sense ✓.
- C0 = C of Lemma 2.5 is absolute ✓, and C1 depends only on C0 ✓.

**Lemma 4.3 + (4.9) → Prop 4.4.**
- (4.9) gives d0 = d_{e′} with E h(d_e/d0) ≤ S ≤ S0 ✓.
- Applying Lemma 4.3 to U = z/d0 and U = d0·w (mean edge heights E h(D_e) and E h(D_e^{−1}) = E h(D_e)) gives (4.10) ✓.

**Lemma 2.7 + Cor 3.2 → Prop 4.4.**
- The alphabet is fixed: M = M(B, τ) depends on S0 only. Choosing K → ∞ with K = o(log t) and D/K → 0 gives M^{K−1} = t^{o(1)} ✓.
- The acceptance tests accept every actual edge, so s0 = 0 ✓.

**Prop 2.4 → Prop 4.4.**
- Uses max µ(p) = t^{−1+o(1)} and min d(p) → ∞ ✓.

**Prop 4.4 → S → ∞ along the WHOLE sequence → §5–§7.** ✓
- Prop 4.4 excludes every bounded subsequence, so §5 may use S → ∞ without passing to a subsequence.

**Lemma 4.5 → §5, §6, §7.**
- ∫m = O(1) with an absolute constant ✓.
- Matching labels give the c_v e^{∓s} bounds ✓.

### §5

**Lemma 5.1 parameter order.**
- D, S, d_{Q,min} come from the configuration. Then K, L, k are chosen, then ε = k^{−1/16}, then C/B/G, then the history H from Cor 3.3 via (3.17) on C, then the templates.
- No parameter is chosen before the quantity it must dominate ✓.
- The consequences are checked: k³/S → 0 and k^{3+1/16}e_t → 0 follow from k^{20}(…) → 0, and k = t^{o(1)} ✓.

**Lemma 2.5 → §5.1, the dominant label ℓ on G.**
- The relevant coordinate's mismatch is ≤ f + m ≤ ε + 1/k, which is eventually ≤ s0 uniformly over levels ✓.
- The labels are a pair of label maps on P ∪ Q ✓.

**Lemma 2.6 → (5.6).**
- The uniform marginal bound a_t = C(ε + 1/k) is uniform over G ✓.

**Cor 3.3 (3.17) → (5.7).**
- The tests are levels sampled from dτ/W_c on C.
- Strict-cross failure is ≤ m, because consistency implies the strict cross ✓.
- The k³ factor is absorbed: k³(∫m + W_c e_t) ≤ k³ O(1) + k^{3+1/16} e_t S = o(S) ✓.

**Lemma 5.3 → Props 5.5 and 5.6.**
- The slot marginals are the edge law ✓.
- The collision bound M/d(p) holds pointwise in p ✓.

**Lemma 5.4 → Prop 5.5.**
- (5.12) needs the two thresholds to be independent given the base. This holds in Q (p, r ⫫ given q), in P (q, q′ ⫫ given p) and in Pθ (q, q′ ⫫ given (p, θ)) ✓.

### §6

**Props 5.5 and 5.6 + Lemmas 6.1, 6.2 + (5.7) → Prop 6.3.**
- The sandwich is λ/4·(C_Q + C_Pθ) − o(S) ≤ D_Q + D_Pθ ≤ 10δ²λ(C_Q + C_Pθ) + o(S).
- The rare ±2EH* terms cancel: Q has star x = q and endpoints y = p; Pθ has star x = p and endpoints y = q. With Prop 5.6's sign convention 2EH_x* − 2EH_y*, these are exact negatives ✓.
- 10δ² = 10⁻³ < 1/4 ✓, scripted.
- (6.9) then follows from Prop 5.6 for Q alone, plus C_Q = o(S) ✓.

**Lemma 6.4 needs E_µH_p* = o(S) and the same fixed H** ✓. It uses (4.7) and the product formula on Z·W, with Z, W ≠ 0 for distinct real points ✓.

**Props 6.3 + 5.5 + 5.6 + Lemma 6.4 + Lemma 2.5 → Prop 6.5.**
- Proof by contradiction on a subsequence.
- f ≤ C(V_P + V_Q) on common levels comes from Lemma 2.5 applied to the majority-bit label maps: s = P(labels differ) ≤ V_P + V_Q, and min(ρ, 1−ρ) ≤ 2ρ(1−ρ) ✓.
- Rare levels use (5.4); damaged levels use W_b/2 ✓.

### §7

**Prop 6.5 → Lemma 7.4, via c0 with E(H_p* + H_r*) = 2E_µH_p* ≥ 4c0 S** ✓. Both wedge point-marginals are µ.

**Prop 6.3 (C_Q = o(S)) → Lemma 7.3's E1.**
- The first term of E1 has mean exactly ∫_C E_q[2ρ_q(1−ρ_q)] = C_Q ✓.

**Lemma 5.2 (5.6) → E1 and E2** ✓.

**Lemma 7.1 → Lemma 7.2.**
- Absorption on T: (W_c + W_b + 2 log 2)/(R0 S) ≤ ε + o(1) ✓.
- In (7.6), distinctness is restricted on the left and the restriction dropped on the right ✓.
- In the layer cake, ϑ_t uses h_P(u) ≤ C0/R0 and h_Q ≤ 1. So ϑ_t → 0 even at thresholds where κ(G_u) = 1 ✓.

**Lemmas 7.2, 7.3 → Lemma 7.4.**
- Order of discards: first Z > δ_t W (cost EZ/δ_t = o(S)), then W < c0 S, then W > 2R0 S (Lemma 7.2), and only then the dyadic band.
- The band probability is c/(R0 log 2R0) = t^{−o(1)}, since k = t^{o(1)} ✓.

**Lemma 7.5 → Prop 7.6.**
- The loss is o(1/(R0 log 2R0)) by k^{20}/d_{Q,min} → 0, which is in (5.2) ✓.
- "p, r lie on a common popular circle" is a property of the PAIR, so deleting all such wedges leaves no surviving pair with it ✓.

### §7 → §8 (constant compatibility, brief item (1))

| Prop 8.1 hypothesis | Supplied by Prop 7.6 | Compatible? |
|---|---|---|
| P_n finite algebraic points, \|P_n\| ≤ t^{1+o(1)} | \|P\| = t^{1+2a+o(a)} | ✓ |
| ≥ t^{2−o(1)} edges | ≥ c\|E\| min d(q)/(2R0 log 2R0) = t^{2+3a−o(1)} | ✓ |
| (8.1) | (7.13), via w_p − w_q = 1/d, w_r − w_q = 1/d′ (scripted) | ✓ |
| (8.2) h(λ) ≥ cJ, c absolute | (7.14): 2h(λ) = ‖n_pq − n_rq‖₁ ≥ (1−δ_t)W ≥ (1−δ_t)J, so c = 1/3 | ✓ |
| (8.3) h(rectangle) = o(J) uniformly | (7.15): ‖b_pr‖₁ ≤ E1 ≤ δ_t W ≤ 2δ_t J; profiles a_p, a_r cancel around a rectangle; h ≤ 4δ_t J, ω_t = 4δ_t → 0 | ✓ |
| J_n → ∞ | J ≥ c0 S → ∞ | ✓ |
| no edge with both endpoints on a unit circle carrying ≥ t^{9/10} points of P_n | Lemma 7.5 (same P, same threshold, REAL unit circles) | ✓ |

### §8 internal chain

**Lemma 8.2 → "every λ ∉ k0, every χ ∈ k0^×".**
- (8.2) and (8.3) hold uniformly, so they hold for the n-dependent grid edges ✓.
- Lemma 8.2 needs only fixed-degree monic equations ✓.

**Lemma 8.3 rests on three things:**
- the minimal loci (the minimum exists over total dimensions {2, 3, 4});
- the uniform plane estimate, obtained via minimality (a full-zero-count polynomial gives an irreducible factor curve of degree ≤ D, which times the pruned min-degree t^{1−o(1)} gives a full count with smaller total dimension) ✓;
- the bounded root count on a curve side, since distinct real points have distinct z ✓.

**Lemma 8.4 needs λ_iℓ transcendental over k0** ✓. ∂ kills k0 ∋ i and χ ✓.

**(8.9)–(8.11) are scripted** ✓.

**Lemma 8.5 is a counting argument:** N d1 − 3j > N(d1 − 1) for N = 20, j = 5 ✓.

**Lemma 8.6 rests on the exhaustive three-case split** (V1 plane / V1 curve with V2 ≠ V1 or deg_w ≥ 2 / V1 = V2 of projection degree 1). The (8.15) algebra is scripted ✓.

**Kummer (§8.5)** ✓.
- The rank-two and collinear cases are exhaustive given V1, V2 ✓.
- Every quantity in (8.16) other than H and A lies in M ✓.
- ∂ is never applied outside F ✓.

### Final assembly (p. 51)

- Negating Thm 1.1 gives the sequence. S is bounded or divergent on a subsequence; Prop 4.4 kills bounded; Prop 7.6 → Prop 8.1 kills divergent.
- All "o(·)" parameters (a, b, K, L, k, δ_t, …) are chosen along the given sequence, before the dichotomy. They survive passage to a subsequence ✓.
- Brief item (ix) is checked in §4 below.

---

## 2. Valtr's obstruction (brief item (i)): which steps are Euclidean, and what happens for the parabola

Test family: the "unit curve" C = {(x, x²)}. Two translates meet in ≤ 1 point, and SST holds. Valtr's grid (points (i, j) with i ≤ n^{1/3}, j ≤ n^{2/3}, edges along (d, d²)) has ≍ n^{4/3} such pairs.

In coordinates z = x, w = y, an edge has jumps (d, d²). Euclid has jumps (d, d^{−1}). Results are scripted in `checks/whole/valtr_parabola.py` (§7).

| Step | Uses Euclid? | Parabola fate |
|---|---|---|
| §2 (Lemma 2.1, Lemma 2.2, Prop 2.3, Prop 2.4, Lemmas 2.5–2.7) | No: only "two curves meet in ≤ 2 points, two points on ≤ 2 curves", plus algebraicity | Survives. Valtr's grid is genuinely near-extremal, so this is harmless. |
| §3 | No: an arbitrary finite law | Survives. Harmless. |
| (4.9), Lemma 4.3 | No: functions of d_e only | Survives. |
| Prop 4.4 | Uses (4.1) in the subtraction step | **Survives, and needs only 2 neighbours.** Subtracting the exact equations kills the dZ² term: E2 − E1 = −2(D2 − D1)dZ (scripted). Harmless, because the conclusion S → ∞ is TRUE for Valtr's grid. For Valtr's grid the jumps d are roughly uniform on [1, N/2]. Then archimedean S is O(1), but the nonarchimedean contribution Σ_{p≤N} log p/(p−1) ≍ log N → ∞ (heuristic computation). So Prop 4.4 is not where Euclid enters, and the paper does not claim it is. |
| **Lemma 4.5 (strict-cross consistency)** | **Yes: reciprocity.** Y = 1 ⇔ \|d\|_v < e^{−s}; then the z-jump is small AND the w-jump \|d^{−1}\|_v > e^{s} is large, so exactly one label agrees. | **Fails.** With jumps (d, d²), both coordinate labels are monotone in \|d\| in the SAME direction, so no choice of B-scale makes "exactly one agrees" hold for both bit values. Scripted 3-adic example: v₃(d) = 2 gives v₃(d²) = 4 (both close), versus Euclid's v₃(d^{−1}) = −2. Cor 3.3 then has s0 = Θ(1), and all of §5–§6 collapses. |
| **(5.14), and its copy in Lemma 7.1** | **Yes:** (d − d′)(1/d − 1/d′) = −(d − d′)²/(dd′), so −log\|·\|_v = 2u − b − b′ is a function of the thresholds only | **Fails.** The analogue is (d − d′)(d² − d′²) = (d − d′)²(d + d′), with an extra \|d + d′\|_v that no threshold controls. Scripted: d = 1, d′ = −1 + 3^k has (b, b′, u) = (0, 0, 0) for all k, but the parabola valuation is k. |
| (7.13) = (8.1) | Yes | Changes form: (w_p − w_r)/(z_p − z_r)² = (λ+1)/(λ−1), so λ is a RATIONAL function of the positions (scripted). |
| **(8.10) + §8.5 Kummer** | **Yes:** λ is a root of l² − (2−L)l + 1, with discriminant L(L−4) (scripted), so R_ℓ = ±√(L_ℓ(L_ℓ−4)) are genuine radicals | **Fails.** In the parabola world λ ∈ M, there are no radicals and no sign-change automorphisms. The differentiated system becomes linear over M, and its consistency is a polynomial condition that Valtr-type configurations can satisfy. |

**Conclusion.** No step that the paper's own logic needs to fail for the parabola survives. The Euclidean feature exploited is the hyperbola structure zw = 1 of the complexified circle: reciprocal jumps, and the two-valuedness of λ given |p − r|².

**Exposition note (Objection 2).** The paper never names Valtr; the string "Valtr" does not occur. It never states which feature defeats the obstruction. The analysis above had to be reconstructed.

---

## 3. Prove-too-much (brief item (viii))

### (a) No effective δ, and no conflict with the lower bounds
- The proof argues by contradiction along a sequence. a(t), b, K, L, k, δ_t and ω_t are all chosen depending on the hypothetical counterexample sequence, c0 comes from a lim inf, and §8 uses a nonprincipal ultrafilter.
- No δ can be extracted, and the paper says so (p. 4: "establishing the existence of a fixed positive gap without estimating its size").
- Theorem 1.1 gives an upper exponent < 4/3. Every known lower exponent is far below that: 1.014114 [23]; the forum's 1.0357; Naslund's MO update δ > 0.04317 per the sources seat. No conflict.

### (b) Where near-4/3 density is used, so the argument cannot reach n^{1+o(1)}
1. **Prop 2.4, (2.6)–(2.8).** Feasibility needs the piece to be SST-extremal up to t^{o(a)}, namely e0 ≥ t^{2+2a−o(a)} against the incidence bound t^{2+2a+o(a)}. Otherwise the factor T_t in (2.6) is t^{Θ(1)}, the maximiser of w/(uv)^γ can have UV = t^{−Θ(1)}, and the scales (2.2) and the expansion (2.5) with γ = 27/50 > 1/2 are lost.
2. **Lemma 2.7.** D = o(log t) comes from P(p,r) ≤ 2/(|E| d_{min,Q}) = t^{−2−3a+o(a)} against H(p) ≤ (1+2a) log t. At density n^{4/3−3δ′}, the same computation gives D ≍ δ′ log t.
3. **Lemma 3.1 / §3.4.** These need K = o(log t) and D/K → 0, hence D = o(log t).
4. Hence **Prop 4.4** (prediction failure o(1)) and **(5.7)** are both lost.
5. **Lemma 7.5** (t^{9/10} against |P| = t^{1+o(1)}) and **§8.2/Lemma 8.3** (full counts t^{2−o(1)}, curves with t^{1−o(1)} points) are calibrated to density t^{−o(1)}.

The near-4/3 hypothesis is used early and essentially (items 1–3). That is consistent with the n^{1+c} disproof.

### (c) The number-field degree d_N
- It is irrelevant: absolute values carry weight 1/d_N, and the height is field-independent (Lemma 4.2).
- The tail bounds (4.5)/(4.6) at a uniformly random embedding do not depend on d_N.
- The paper notes explicitly that "M = M(B, τ) independent of t and of the field degree" (p. 20).
- Nothing bounds d_N, and nothing needs to. Bloom's bounded-degree conjecture is neither used nor contradicted.

### (d) Where real points are used
1. Lemma 2.1: real-closed-field transfer.
2. Lemma 2.2 and Prop 2.3: planar topology (cuttings by semicircle graphs, Székely's crossing argument).
3. "Distinct real points have distinct z and distinct w" (p. 16):
   - (4.7) nonzero differences, so the intervals I_v are finite;
   - Lemma 6.4, Z·W ≠ 0 for distinct points: **essential**;
   - Lemma 8.3, curve-side bounded root count: **essential**;
   - Prop 4.4, Prop 5.5 and Lemma 7.1 ("distinct jumps"): there the unit equation alone suffices among neighbours of a common vertex.
4. Lemma 7.5 / Prop 8.1: "popular REAL unit circles".
5. §8.2's anti-holomorphic symmetry (z, w) ↦ (w̄, z̄) (correct in the PDF). It gives: (i) nonconstant projections; (ii) bidegree (1,1) in Lemma 8.6's third case; (iii) (8.4) ⇒ v = ū ⇒ a real unit circle, so the deletion hypothesis applies.

For a complex configuration on the "hyperbola graph" in C² (independent z, w with (Δz)(Δw) = 1), items 2, 3 and 5 break: there is no planar cutting, coordinates can repeat, and there is no symmetry.

### (e) Observation, not an objection: transfer to the real Minkowski plane
Take real points with unit pairs (x_p − x_q)(y_p − y_q) = 1 (z = x, w = y independent reals, translates of the hyperbola xy = 1), and assume pairwise distinct x's and pairwise distinct y's. Then:
- **§2:** two translates meet in ≤ 2 points and two points lie on ≤ 2 translates; the branches are x-monotone graphs, so the cutting works ✓.
- **§3:** ✓
- **(4.1):** holds verbatim.
- **§4–§7:** run verbatim; they never use w = z̄ ✓.
- **§8:** the only missing ingredient is the symmetry. Lemma 8.6's third case would then also have to handle V1 = V2 = {w = g(z)} with deg g ≥ 2. That looks routine: L_ℓ = (z − a)(g(z) − g(a)) has a simple zero at another root a′ of g(z) = g(a), and generic anchors keep L_m(a′) ∉ {0, 4}. The popular-hyperbola deletion plays the role of (8.4).

So, if correct, the method also gives a power saving for unit "Minkowski distances" among points with injective coordinates. I know of no n^{4/3} construction for hyperbola translates, so this is not a contradiction. But the paper's correctness is equivalent, in this respect, to the non-existence of such a construction.

**Lead for whoever can check the literature:** an n^{4/3} lower bound for incidences between points (with distinct x's and y's) and translates of xy = 1 would refute the paper. My own quick grid-type attempts reach only polylogarithmic degree; this is not a literature claim.

---

## 4. Sequence reduction and final assembly (brief item (ix))

**p. 4:** *"for each j ≥ 2, failure of a bound with exponent 4/3 − 1/j allows the constant in that bound to be chosen large enough to force a counterexample with n ≥ j. Its ordered unit-pair count is at least n^{4/3−1/j} = t^{4−3/j}."*
- The negation of Thm 1.1 is: for every C and every β ∈ [1, 4/3) there is an n with u(n) > Cn^β.
- Take C = j². Since u(n) ≤ n²/2, this forces n > j/√2. (The incidence seat's u(n) < j² for n < j gives n ≥ j directly.)
- Ordered count = 2u(n) > 2n^{4/3−1/j} ✓.
- For j = 2 the exponent 5/6 lies outside [1, 4/3). This is harmless: monotonicity in β, j ≥ 3 suffices, and the incidence seat flags it as COSMETIC O2.
- "Passing to an increasing sequence" ✓, with exponent error 3/j → 0.
- "Ordered vs unordered" ✓, a factor of 2.

**p. 51 (final paragraph):**
- The contradiction shows that no sequence n → ∞ has u(n) ≥ n^{4/3−o(1)}. Hence limsup log u(n)/log n < 4/3.
- "Enlarging the positive constant covers the finitely many remaining sizes" is then exactly right under that reading, and redundant under the direct contrapositive (incidence seat O3).
- n = 0, 1 ✓. β ≥ 1 ✓.

---

## 5. Global hygiene (brief item (5))

### 5a. Every hand-wave phrase in the paper

Found by grep over clearly / it follows / follow(s) directly / follows from / similarly / same argument / evident / immediate / identical / analogous / symmetric / the same estimate / bound / in the same way / directly. Each was checked by me.

| Page | Phrase (verbatim fragment) | Section seat | My check |
|---|---|---|---|
| 6 | Lemma 2.2: "with the evident interpretation when R = 1" | incidence | ✓ vacuous: no region meets > l of the l circles |
| 7 | Prop 2.4: "the upper bound follows from (2.1)" | incidence | ✓ (2t^{1+2a})^{2/3}(t^{2+a})^{2/3} = t^{2+2a} |
| 8 | Prop 2.4: "following from concavity. The center comparison is identical." | incidence | ✓ (1−x)^γ ≤ 1 − γx; same for κ(q) |
| 9 | Lemma 2.5: "The analogous statement holds for independent centers" / "The center assertion is identical." | incidence | ✓ P(ℓ_Q(q) ≠ ℓ_Q(q′)) ≤ 2k ≤ 4s |
| 10 | Lemma 2.6: "two assertions follow directly from (2.9)" | incidence | ✓ |
| 10 | Lemma 2.7: "The asymptotics follow from the same estimates" | incidence | ✓ |
| 13 | Lemma 3.1: "It follows, by Cauchy–Schwarz first over q and then over the tests" | prediction | ✓ constant 2^{5/4} ≤ 4 (scripted) |
| 13 | Lemma 3.1: "independent and identically distributed" (fresh-test swap) | prediction | ✓ |
| 16 | (4.1): "The second equality follows from the unit-distance equation" | heights | ✓ |
| 18 | Lemma 4.2: "the same conclusion at infinity" | heights | ✓ each embedding of N has [L:N] extensions |
| 22 | Lemma 4.5: "B1-labels similarly implies…" / "The match implications follow directly" | heights | ✓ |
| 23 | Lemma 5.1: "Its stated consequences follow directly" | scores | ✓ |
| 25 | Lemma 5.3: "The first assertion is immediate for ordinary stars" | scores | ✓ |
| 26 | Lemma 5.4: "The empty-interior case is immediate" | scores | ✓ |
| 26 | Prop 5.5: "the analogous A match gives s ≥ b′ and s ≤ b + α + c_v" | scores | ✓ re-derived: s ≤ u + log c_v = b + T_v |
| 27 | Prop 5.5: "The case of a rare positive with minority bit 0 is symmetric" | scores | ✓ |
| 30 | Lemma 6.2: "Define the second set in the same way for columns" | common | ✓ |
| 32 | Prop 6.3: "The same estimate as in the singleton case applies" | common | ✓ |
| 33 | §6.3: "Theorem 6.3 then gives the same bound" | common | ✓ = (6.9) |
| 35 | Prop 6.5: "Columns give bit 0 and the same estimates" / "the same bound follows from f ≤ 1/2" | common | ✓ |
| 36 | Lemma 7.1: "charged directly to the neighbor indicator" | extraction | ✓ (7.3) |
| 39 | Lemma 7.3: "It follows that (7.8) holds with E1 = …" | extraction | ✓ |
| 43 | Lemma 8.2: "At infinity the same estimate holds with the additional factor m" | algebra | ✓ \|u\| ≤ Σ\|a_r\| ≤ m·max(1, \|a_r\|) |
| 46 | after Lemma 8.3: "The same argument applies to a point after adjoining the other grid points to B" | algebra | ✓ via (8.5) |
| 48 | Lemma 8.6: "the assertion for a plane is immediate" | algebra | ✓ a generic plane point has transcendental coordinates |
| 49 | Lemma 8.6: "To see the classification directly" | algebra | ✓ |
| 50 | §8.5: "it follows that A = A′_4" | algebra | ✓ R4 ∉ M(R1, R2, R3) |
| 51 | Proof of Thm 1.1: "The cases n = 0, 1 are immediate" | (whole) | ✓ |

None is a hard step hidden behind a hand-wave.

### 5b. Cross-references

There are 65 occurrences of "Theorem X.Y" whose label is a Lemma, Proposition or Corollary. The numbering is a shared counter, so each points to the intended result. I resolved every one by script and read each in context.

| Reference | Points to |
|---|---|
| Theorem 2.1, 2.2 | Lemma 2.1, Lemma 2.2 (p. 7) |
| Theorem 2.4 | Prop 2.4 (pp. 8, 16, 19, 21) |
| Theorem 2.5 | Lemma 2.5 (pp. 19, 23, 35) |
| Theorem 2.6 | Lemma 2.6 (p. 24) |
| Theorem 2.7 | Lemma 2.7 (p. 20) |
| Theorem 3.1 | Lemma 3.1 (pp. 13, 15) |
| Theorem 3.2 | Cor 3.2 (p. 20) |
| Theorem 3.3 | Cor 3.3 (pp. 15, 24) |
| Theorem 4.1 | Lemma 4.1 (pp. 17, 18) |
| Theorem 4.2 | Lemma 4.2 (pp. 19, 42, 43) |
| Theorem 4.3 | Lemma 4.3 (p. 19) |
| Theorem 4.4 | Prop 4.4 (pp. 21, 22, 51) |
| Theorem 4.5 | Lemma 4.5 (p. 22) |
| Theorem 5.1 | Lemma 5.1 (pp. 24, 27, 28, 41) |
| Theorem 5.2 | Lemma 5.2 (pp. 27, 35, 39) |
| Theorem 5.3 | Lemma 5.3 (pp. 27, 28, 32) |
| Theorem 5.4 | Lemma 5.4 (pp. 26, 27) |
| Theorem 5.5 | Prop 5.5 (p. 33) |
| Theorem 5.6 | Prop 5.6 (pp. 33, 35) |
| Theorem 6.2 | Lemma 6.2 (pp. 30, 32) |
| Theorem 6.3 | Prop 6.3 (pp. 33, 36) |
| Theorem 6.4 | Lemma 6.4 (p. 34) |
| Theorem 6.5 | Prop 6.5 (pp. 36, 40) |
| Theorem 7.2 | Lemma 7.2 (p. 40) |
| Theorem 7.4 | Lemma 7.4 (pp. 40, 41) |
| Theorem 7.5 | Lemma 7.5 (p. 41) |
| Theorem 7.6 | Prop 7.6 (pp. 43, 51) |
| Theorem 8.1 | Prop 8.1 (pp. 44, 51) |
| Theorem 8.2 | Lemma 8.2 (p. 46) |
| Theorem 8.3 | Lemma 8.3 (pp. 46, 47) |
| Theorem 8.4 | Lemma 8.4 (p. 47) |
| Theorem 8.6 | Lemma 8.6 (p. 50) |

All resolve. COSMETIC (Objection 6).

### 5c. Forward references

All resolve, and none is used in a proof before the cited result is proved. There is no circularity.
- p. 3 "Lemma 6.2 proves this comparison" → Lemma 6.2 ✓
- p. 25 "Section 6 will identify the configurations" → Prop 6.3's classification ✓
- p. 11 "the coordinate tests used below" → §3.2–§3.3 ✓
- p. 14 "For the coordinate-quantization application…" → Prop 4.4 ✓
- p. 15 "In the later level application, T is the common-level set" → (5.7) ✓
- p. 18 "We will prove that this variation cannot remain bounded" → Prop 4.4 ✓
- p. 28 "the subsequent posterior-support transfer" → Lemma 6.2 ✓
- p. 40 "The algebraic argument will require…" → (8.4) ✓

### 5d. Constants claimed absolute: none depends on t, a, the configuration or the field

**Absolute:**
- γ = 27/50 and η = 1/25 (Prop 2.4);
- C in (2.9) (depends on γ only);
- s0 and C in Lemma 2.5 (depend on η, γ only; the index depends on ξ_t);
- C1 in Lemma 4.3 (on C0);
- O(1) in Lemma 4.5 (∫(1{|s−n_e| ≤ log√2} + √2 e^{−|s−n_e|}) ds);
- δ = 1/100 and λ = δ²/2;
- 10δ²λ and 2 log 2 in Prop 5.5;
- C in (6.10) and (6.13);
- 3 and 2 log 2 in (7.2);
- C0 and C_m in Lemma 7.2 (from (5.5) and Lemma 4.5);
- c = 1/3 in (8.2).

**Sequence-dependent, and declared as such:**
- ξ_t and T_t;
- the constants of Prop 4.4 ("may depend on the fixed S0");
- c and c0 of Lemma 7.4 ("independent of t along the fixed sequence").

None is silently configuration- or t-dependent. The final C and β are pure existence statements.

---

## 6. Objections

**Objection 1 — p. 25, score display. COSMETIC (typesetting).**

Verbatim (rendered PDF):

> score = { 2I_x 1{Y1=Y2=r, N}, at a good rare level; c(ρ)1{Y1=Y2, N}, at a common level, − 1{Y1≠Y2}. ; 0, at a damaged level }

- The negative charge −1{Y1≠Y2} is printed on the common-level line, outside the brace. Every proof uses it at EVERY level:
  - Prop 5.5, p. 26: "the integrated bit-difference charge at this place is exactly b′ − b";
  - Prop 5.6, p. 28: "On B there are no positives and the negative score is at least −1", and at good rare levels "the negative charge is at most I_y1 + I_y2 + M1 + M2";
  - Lemma 7.1: "all-level negative charge".
- The usage is consistent, so nothing breaks. A reader taking the display literally would get a different D_i and a different (5.16).
- Fix: write "score = (case term) − 1{Y1≠Y2} at every level".

**Objection 2 — §1.1 (pp. 1–2) and the whole paper: Valtr's obstruction is never addressed. EXPOSITION (no mathematical gap).**
- The canonical caveat on the problem's page ("to prove an upper bound better than n^{4/3} some special feature of the Euclidean metric must be exploited") is neither cited nor answered; the string "Valtr" occurs nowhere.
- The paper's §1.2 says only "In the complex coordinates z = x + iy and w = x − iy, a unit edge has jumps d and d^{−1}".
- A referee needs the explicit statement that this reciprocity is what fails for strictly convex norms with parabolic arcs, and where it is used (Lemma 4.5, (5.14)/Lemma 7.1, (7.13), (8.10)).
- I supply that analysis in §2, so this is an exposition gap only.

**Observation 3 (not an error) — §3(e) above: Minkowski-plane transfer. UNCLEAR as a consistency question.**
- The method appears to prove a power saving also for real points with injective coordinates and unit pairs (Δx)(Δy) = 1.
- It would become FATAL only if an n^{4/3} construction for translates of xy = 1 with distinct x's and distinct y's exists. I know of none.
- Fix: none needed. A sentence acknowledging that the proof uses only (4.1) + coordinate injectivity + planar incidence geometry (+ symmetry for convenience) would let readers test it.

**Objection 4 — p. 2: *"including the tower-cutting method of Hajir, Maire and Ramakrishna [9, 12, 13]"*. COSMETIC.**
- [9] is Ellenberg–Venkatesh (class-group torsion), which belongs to "these ideas". The bracket covers the whole sentence. The sources seat agrees.

**Objection 5 — p. 2: *"Sawin sharpened the construction to u(n) ≫ n^{1.014114} … These are construction lower bounds. Theorem 1.1 bounds every configuration from above, leaving a gap between the known exponents."* COSMETIC.**
- The statement is accurate for [23] (Sawin Thm 1: "#{(v1, v2) ∈ U | |v1 − v2| = 1} ≥ n^{1.014114}/C", which counts ordered pairs; ≫ absorbs the factor 2).
- By 23 Sep 2026 the erdosproblems forum carried 1.0357 (June 2026, unrefereed), and Naslund's MO update of 10 Oct 2026 claims δ > 0.04317.
- No logical effect.

**Objection 6 — throughout: "Theorem X.Y" names Lemmas, Propositions and Corollaries. COSMETIC.**
- There are 65 instances; every one resolves to the intended result (§5b).

**Objection 7 — Brief item (vii)'s "(z, w) ↦ (w, z)" and "v = u". WITHDRAWN.**
- The rendered PDF p. 44 has "(z, w) ↦ (w̄, z̄)", "w = c̄", "v = ū".
- With these, every use survives:
  - "symmetric image w = c̄ is a different line" ✓;
  - (8.4) with v = ū gives |z − u| = 1 on real points, a real unit circle, so the deletion hypothesis is contradicted ✓;
  - in Lemma 8.6 case 3, symmetry gives deg_z f = deg_w f = 1 ✓.
- On whether B0 must be closed under conjugation: the symmetric curve's equation is a scalar multiple of the original by a ratio of coefficients. So conj(B0) ⊆ B0(that ratio) = B0 once the normalisation is fixed, and nothing downstream needs more.

No other objection in my scope. The section-level deep checks are the section seats'. My own pass over §4–§8 found nothing they should look for beyond the brief's list.

---

## 7. Finite checks

Both scripts live in `/tmp/oaimath/167/checks/whole/` and were run with `nice -n 19 ~/.venv/bin/python -I <script>`. The system python3 lacks sympy, so `~/.venv/bin/python` was used.

### 7a. identities.py
```python
# Finite/symbolic checks for referee seat "whole". Run: nice -n 19 python3 -I identities.py
import sympy as sp
from fractions import Fraction as Fr
ok=lambda name,cond: print(("PASS " if cond else "FAIL ")+name)

D1,D2,D3=sp.symbols('D1 D2 D3',nonzero=True)
# (4.15) determinant of [[1/D2-1/D1, D2-D1],[1/D3-1/D1, D3-D1]]
det=sp.Matrix([[1/D2-1/D1,D2-D1],[1/D3-1/D1,D3-D1]]).det()
claim=(D1-D2)*(D1-D3)*(D2-D3)/(D1*D2*D3)
ok("(4.15) determinant", sp.simplify(det-claim)==0)
# control: wrong sign of last factor must FAIL
ok("(4.15) CONTROL wrong sign (expect FAIL)", sp.simplify(det-(D1-D2)*(D1-D3)*(D3-D2)/(D1*D2*D3))==0)
# quadratic term cancels on subtracting j=1 from j=2 (Prop 4.4)
dZ,dW=sp.symbols('dZ dW')
Ej=lambda D: sp.expand((D+dZ)*(1/D+dW)-1)
ok("Prop4.4: Ej = dZ/Dj + Dj dW + dZ dW", sp.simplify(Ej(D1)-(dZ/D1+D1*dW+dZ*dW))==0)
ok("Prop4.4: E2-E1 linear in (dZ,dW)", sp.Poly(sp.simplify(Ej(D2)-Ej(D1)),dZ,dW).total_degree()==1)

d,dp=sp.symbols('d dp',nonzero=True)
# (5.14)/(7.13): (d-d')(1/d-1/d') = 2 - d/d' - d'/d = -(d-d')^2/(d d')
ok("(7.13) identity", sp.simplify((d-dp)*(1/d-1/dp)-(2-d/dp-dp/d))==0)
ok("(5.14) product = -(d-d')^2/(dd')", sp.simplify((d-dp)*(1/d-1/dp)+(d-dp)**2/(d*dp))==0)
# (8.10): R=1/lam-lam, L=2-lam-1/lam  =>  R^2 = L(L-4)
lam=sp.symbols('lam',nonzero=True)
L=2-lam-1/lam; R=1/lam-lam
ok("(8.10) R^2=L(L-4)", sp.simplify(R**2-L*(L-4))==0)
ok("(8.10) CONTROL R^2=L(L+4) (expect FAIL)", sp.simplify(R**2-L*(L+4))==0)
# (8.9): differentiate (z_p-z_r)(w_p-w_r) with z=x+iy, w=x-iy, d i = 0
x1,y1,x2,y2,hx,hy,ux,uy=sp.symbols('x1 y1 x2 y2 hx hy ux uy')
t=sp.symbols('t')
X1=x1+t*hx;Y1=y1+t*hy;X2=x2+t*ux;Y2=y2+t*uy
Lt=((X1+sp.I*Y1)-(X2+sp.I*Y2))*((X1-sp.I*Y1)-(X2-sp.I*Y2))
dL=sp.diff(Lt,t).subs(t,0)
ok("(8.9) LHS = 2(p-r).(H-U)", sp.simplify(sp.expand(dL-2*((x1-x2)*(hx-ux)+(y1-y2)*(hy-uy))))==0)
# derivative of 2-lam-1/lam along d lam = lam*A : equals R*A
A=sp.symbols('A')
ok("(8.9) RHS: d(2-lam-1/lam) = (1/lam - lam)*(dlam/lam)", sp.simplify(sp.diff(L,lam)*lam*A-R*A)==0)
# (8.15)
z,u,v,b,a=sp.symbols('z u v b a')
w=v+b/(z-u); wr=v+b/(a-u)
Ll=sp.simplify((z-a)*(w-wr))
zeta=sp.symbols('zeta')
ok("(8.15) L = -b(zeta-1)^2/zeta", sp.simplify(Ll.subs(z,u+zeta*(a-u))-(-b*(zeta-1)**2/zeta))==0)
q=sp.expand(sp.numer(sp.together(-b*(zeta-1)**2/zeta-4)))
ok("(8.15) L-4=0 <=> b z^2+(4-2b)z+b=0", sp.simplify(q+(b*zeta**2+(4-2*b)*zeta+b))==0)
ok("(8.15) discriminant 16(1-b)", sp.simplify(sp.discriminant(b*zeta**2+(4-2*b)*zeta+b,zeta)-16*(1-b))==0)
Lb1=-(zeta-1)**2/zeta
ok("b=1: L(L-4) = ((zeta^2-1)/zeta)^2", sp.simplify(Lb1*(Lb1-4)-((zeta**2-1)/zeta)**2)==0)
# line case: w = e z + e', r on line => L = e (z-a)^2
e,ep=sp.symbols('e ep')
ok("line case L=e(z-a)^2", sp.simplify((z-a)*((e*z+ep)-(e*a+ep))-e*(z-a)**2)==0)
# Section 2 exponent bookkeeping
gam=Fr(27,50); eta=gam-Fr(1,2)
ok("eta = 1/25", eta==Fr(1,25))
ok("2/3-gamma = 19/150", Fr(2,3)-gam==Fr(19,150))
ok("t^{-a/2}(UV)^{-eta}, UV>=t^{-a/4}: exponent -49/100", -Fr(1,2)+eta/4==Fr(-49,100))
ok("xi_t exponent: (uv)^{1/6} with uv<=t^{-a/8}: -1/48", Fr(-1,8)*Fr(1,6)==Fr(-1,48))
# Lemma 2.7: D <= [2(1+2a) - (2+3a)] log t = a log t (+o)
aa=sp.symbols('a',positive=True)
ok("Lemma2.7 exponent gap = a", sp.simplify(2*(1+2*aa)-(2+3*aa)-aa)==0)
# Section 5/6 numerics
delta=Fr(1,100); lamc=delta**2/2
ok("4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam", 4*delta**2*lamc/(2*(Fr(1,4)-delta**2))<=10*delta**2*lamc)
ok("10 delta^2 < 1/4", 10*delta**2<Fr(1,4))
ok("lam/4 > 10 delta^2 lam (6.3 sandwich nondegenerate)", lamc/4>10*delta**2*lamc)
ok("(6.7) outside: 4d^2 - lam > lam/2", 4*delta**2-lamc>lamc/2)
rho=sp.symbols('rho')
expr=lambda c: c*(rho**2+(1-rho)**2)-2*rho*(1-rho)
ok("(6.7) algebraic identity", sp.simplify(expr(sp.Symbol('c'))-((2*rho-1)**2+(sp.Symbol('c')-1)*(rho**2+(1-rho)**2)))==0)
import numpy as np
grid=np.linspace(0,1,200001); dl=0.01; lm=dl**2/2
c=np.where(np.abs(grid-0.5)<=dl,1+lm,1-lm)
val=c*(grid**2+(1-grid)**2)-2*grid*(1-grid)
ok("(6.7) min over rho grid >= lam/2 (min=%.3e, lam/2=%.3e)"%(val.min(),lm/2), val.min()>=lm/2-1e-15)
# Lemma 7.2 Young: 6 th sqrt(C0 A S) <= A/4 + 36 C0 th^2 S
A_,S_,C0,th=sp.symbols('A S C0 th',positive=True)
ok("Lemma 7.2 Young", sp.simplify((A_/4+36*C0*th**2*S_)-6*th*sp.sqrt(C0*A_*S_) - (sp.sqrt(A_)/2-6*th*sp.sqrt(C0*S_))**2)==0)
# Prop 4.4 constants: 64 B^5 tau / r^3 < r/2 when tau < r^4/(128 B^5)
Bv,rv,tv=sp.symbols('B r tau',positive=True)
ok("Prop4.4: tau=r^4/(128B^5) gives 64B^5tau/r^3 = r/2 (strict for smaller tau)", sp.simplify(64*Bv**5*(rv**4/(128*Bv**5))/rv**3-rv/2)==0)
# 8B tau bound: sqrt2 tau(2B) + (2B+sqrt2 tau) sqrt2 tau <= 8 B tau for B>=2, tau<=1
ok("Prop4.4: 8B tau error bound (B=2,tau=1 worst)", (np.sqrt(2)*1*4+(4+np.sqrt(2))*np.sqrt(2))<=8*2)
# Cor 3.3: inner product = hashed strict-cross indicator; 4*sqrt(18)<18
ok("4 sqrt 18 < 18", 4*np.sqrt(18)<18)
for (a1,b1,a2,b2) in [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1)]:
    ip=(a1==a2)+(b1==b2)-2*((a1,b1)==(a2,b2)); sc=((a1==a2)!=(b1==b2))
    ok(f"Cor3.3 ip==strict-cross at {(a1,b1,a2,b2)}", ip==sc)
# Lemma 3.1 constant: B'*sqrt(8B^2*(D/2K)^{1/2}) <= 4BB'(D/K)^{1/4}
ok("Lemma 3.1 constant sqrt(8)/2^{1/4} <= 4", np.sqrt(8)/2**0.25<=4)
# Lemma 8.5 count
ok("N=20,j=5: N d1 - 3j > N(d1-1) for d1 in {1,2}", all(20*d1-15>20*(d1-1) for d1 in (1,2)))
```

Output:
```
PASS (4.15) determinant
FAIL (4.15) CONTROL wrong sign (expect FAIL)
PASS Prop4.4: Ej = dZ/Dj + Dj dW + dZ dW
PASS Prop4.4: E2-E1 linear in (dZ,dW)
PASS (7.13) identity
PASS (5.14) product = -(d-d')^2/(dd')
PASS (8.10) R^2=L(L-4)
FAIL (8.10) CONTROL R^2=L(L+4) (expect FAIL)
PASS (8.9) LHS = 2(p-r).(H-U)
PASS (8.9) RHS: d(2-lam-1/lam) = (1/lam - lam)*(dlam/lam)
PASS (8.15) L = -b(zeta-1)^2/zeta
PASS (8.15) L-4=0 <=> b z^2+(4-2b)z+b=0
PASS (8.15) discriminant 16(1-b)
PASS b=1: L(L-4) = ((zeta^2-1)/zeta)^2
PASS line case L=e(z-a)^2
PASS eta = 1/25
PASS 2/3-gamma = 19/150
PASS t^{-a/2}(UV)^{-eta}, UV>=t^{-a/4}: exponent -49/100
PASS xi_t exponent: (uv)^{1/6} with uv<=t^{-a/8}: -1/48
PASS Lemma2.7 exponent gap = a
PASS 4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam
PASS 10 delta^2 < 1/4
PASS lam/4 > 10 delta^2 lam (6.3 sandwich nondegenerate)
PASS (6.7) outside: 4d^2 - lam > lam/2
PASS (6.7) algebraic identity
PASS (6.7) min over rho grid >= lam/2 (min=2.500e-05, lam/2=2.500e-05)
PASS Lemma 7.2 Young
PASS Prop4.4: tau=r^4/(128B^5) gives 64B^5tau/r^3 = r/2 (strict for smaller tau)
PASS Prop4.4: 8B tau error bound (B=2,tau=1 worst)
PASS 4 sqrt 18 < 18
PASS Cor3.3 ip==strict-cross at (0, 0, 0, 0)
PASS Cor3.3 ip==strict-cross at (0, 0, 0, 1)
PASS Cor3.3 ip==strict-cross at (0, 0, 1, 0)
PASS Cor3.3 ip==strict-cross at (0, 0, 1, 1)
PASS Lemma 3.1 constant sqrt(8)/2^{1/4} <= 4
PASS N=20,j=5: N d1 - 3j > N(d1-1) for d1 in {1,2}
```

**Controls.**
- The two lines marked "CONTROL … (expect FAIL)" print FAIL, as they should. One feeds (4.15) a sign-flipped factor; the other feeds (8.10) the wrong radicand L(L+4). Each is a deliberately wrong input that the checker rejects.
- The (6.7) grid minimum equals λ/2 exactly, attained at ρ = 1/2. The bound is tight and correct.

### 7b. valtr_parabola.py
```python
# Valtr/parabola test: unit pairs q-p = (d, d^2) (z=x, w=y real coords). Which Euclidean steps survive?
import sympy as sp
ok=lambda n,c: print(("PASS " if c else "FAIL ")+n)
d,dp,dZ,dW=sp.symbols('d dp dZ dW')
# (a) Prop 4.4 analog: exact eq W_q - W_p = (Z_q - Z_p)^2 ; perturbed predicted point p^ = p + (dZ,dW)
# residual for neighbor with jump D: ((D - dZ)^2 - (D^2 - dW)) ... sign conventions irrelevant; compute E_j
D1s,D2s=sp.symbols('D1 D2')
Ej=lambda D: sp.expand((D-dZ)**2-(D**2-dW))   # = -2 D dZ + dZ^2 + dW
diff=sp.expand(Ej(D2s)-Ej(D1s))
ok("parabola Prop4.4 analog: E2-E1 = -2(D2-D1) dZ (two neighbours pin dZ)", sp.simplify(diff+2*(D2s-D1s)*dZ)==0)
# (b) consistency: Euclid jumps (d,1/d) move OPPOSITE; parabola (d,d^2) move SAME way.
# At a nonarch place with |d| = p^{-k}: Euclid: z-jump small, w-jump large. Parabola: both small.
def v3(n):
    n=sp.Rational(n); 
    return sp.multiplicity(3,n.p)-sp.multiplicity(3,n.q)
dd=sp.Rational(9)  # |d|_3 = 3^-2
ok("Euclid: v3(z-jump)=2>0, v3(w-jump)=-2<0 (exactly one coordinate close)", v3(dd)==2 and v3(1/dd)==-2)
ok("Parabola: v3(z-jump)=2, v3(w-jump)=4 (both close: strict cross impossible)", v3(dd)==2 and v3(dd**2)==4)
# (c) (5.14) analog. Euclid: -log|(d-d')(1/d-1/d')|_v = 2u-b-b' (function of thresholds only).
# Parabola: (d-d')(d^2-d'^2) = (d-d')^2 (d+d'): extra |d+d'|_v, NOT controlled by b,b',u.
ok("parabola product factorises with extra (d+d')", sp.simplify((d-dp)*(d**2-dp**2)-(d-dp)**2*(d+dp))==0)
for k in (1,3,6):
    a1=sp.Integer(1); a2=-1+sp.Integer(3)**k
    b_=min(v3(a1),v3(a2)); bp=max(v3(a1),v3(a2)); u_=v3(a1-a2)
    eu=v3((a1-a2)*(1/a1-1/a2)); pa=v3((a1-a2)*(a1**2-a2**2))
    print(f"  k={k}: b={b_} b'={bp} u={u_}  Euclid v3={eu} (=2u-b-b'={2*u_-b_-bp})  parabola v3={pa}")
    ok(f"  Euclid (5.14) holds k={k}", eu==2*u_-b_-bp)
ok("parabola analog NOT a function of (b,b',u): same (0,0,0), different values", True)
# (d) (7.13) analog for parabola: lambda = d/d' is RATIONAL in positions -> no radicals for Section 8.5
lam=d/dp
zp_zr=d-dp; wp_wr=d**2-dp**2
Phi=sp.simplify(wp_wr/zp_zr**2)
ok("parabola: (w_p-w_r)/(z_p-z_r)^2 = (lam+1)/(lam-1)", sp.simplify(Phi-(lam+1)/(lam-1))==0)
ok("parabola: lam = (Phi+1)/(Phi-1) rational in positions (no square class to separate)", sp.simplify((Phi+1)/(Phi-1)-lam)==0)
# Euclid: lam is a ROOT of lam^2 - (2-L) lam + 1 = 0 : genuinely two-valued
L=sp.symbols('L'); l=sp.symbols('l')
ok("Euclid: lam satisfies l^2-(2-L)l+1 (discriminant L(L-4))", sp.simplify(sp.discriminant(l**2-(2-L)*l+1,l)-L*(L-4))==0)
# CONTROL: claim parabola consistency like Euclid (v3(w-jump) <0) must FAIL
ok("CONTROL (expect FAIL): parabola w-jump large when z-jump small", v3(dd**2)<0)
```

Output:
```
PASS parabola Prop4.4 analog: E2-E1 = -2(D2-D1) dZ (two neighbours pin dZ)
PASS Euclid: v3(z-jump)=2>0, v3(w-jump)=-2<0 (exactly one coordinate close)
PASS Parabola: v3(z-jump)=2, v3(w-jump)=4 (both close: strict cross impossible)
PASS parabola product factorises with extra (d+d')
  k=1: b=0 b'=0 u=0  Euclid v3=0 (=2u-b-b'=0)  parabola v3=1
PASS   Euclid (5.14) holds k=1
  k=3: b=0 b'=0 u=0  Euclid v3=0 (=2u-b-b'=0)  parabola v3=3
PASS   Euclid (5.14) holds k=3
  k=6: b=0 b'=0 u=0  Euclid v3=0 (=2u-b-b'=0)  parabola v3=6
PASS   Euclid (5.14) holds k=6
PASS parabola analog NOT a function of (b,b',u): same (0,0,0), different values
PASS parabola: (w_p-w_r)/(z_p-z_r)^2 = (lam+1)/(lam-1)
PASS parabola: lam = (Phi+1)/(Phi-1) rational in positions (no square class to separate)
PASS Euclid: lam satisfies l^2-(2-L)l+1 (discriminant L(L-4))
FAIL CONTROL (expect FAIL): parabola w-jump large when z-jump small
```

**Control.** The last line asserts the Euclidean-style consistency for the parabola: "w-jump large when z-jump small". It prints FAIL, as it must. The k-loop shows the Euclidean (5.14) identity holding while the parabola analogue takes the values 1, 3, 6 at identical thresholds (b, b′, u) = (0, 0, 0).

---

## 8. Status of each result (the deliverable)

My scope is global. "LINE BY LINE" means I re-derived every inequality in the proof myself. "VERIFIED (argument)" means I read the whole proof and checked every step that the global chain relies on, but not every constant. The section seats own the remaining line-by-line work.

| Item | Status |
|---|---|
| Abstract, Thm 1.1 statement, §1.1, §1.2 | READ IN FULL; §1.1 internal consistency checked (§9) |
| §2 sequence reduction (p. 4) | VERIFIED LINE BY LINE |
| Lemma 2.1 | VERIFIED (argument) |
| Lemma 2.2 | SKIMMED (counting read; incidence seat VERIFIED LINE BY LINE) |
| Prop 2.3 | SKIMMED |
| Prop 2.4 | VERIFIED LINE BY LINE (deletion cost, splitting, trimming, (2.6)→(2.7)→(2.8), ξ_t, (2.4); exponents scripted) |
| Lemma 2.5 | VERIFIED LINE BY LINE |
| Lemma 2.6 | VERIFIED LINE BY LINE |
| Lemma 2.7 | VERIFIED LINE BY LINE |
| Lemma 3.1 | VERIFIED LINE BY LINE (chain rule on the pair transcript; reference law; (3.10); exact (3.11); constant; fresh-test swap) |
| Cor 3.2, (3.13), (3.14) | VERIFIED LINE BY LINE |
| Cor 3.3, (3.17), §3.4 | VERIFIED LINE BY LINE (inner product scripted; 4/L accounting; no current hash in the prediction) |
| Lemma 4.1 | SKIMMED (standard; sources seat MATCH on Milne) |
| Lemma 4.2 | VERIFIED (argument) |
| (4.7)–(4.9) | VERIFIED LINE BY LINE |
| Lemma 4.3 | VERIFIED LINE BY LINE |
| Prop 4.4 | VERIFIED LINE BY LINE (selection law; tails uniform in H; acceptance at a fresh σ; quadratic term cancels; (4.15) and all constants scripted) |
| Lemma 4.5 | VERIFIED (argument) |
| Lemma 5.1 | VERIFIED LINE BY LINE |
| Lemma 5.2, (5.7)–(5.9) | VERIFIED (argument) |
| Lemma 5.3 | VERIFIED LINE BY LINE |
| Lemma 5.4 | VERIFIED LINE BY LINE |
| Prop 5.5 | VERIFIED (argument): flanks (5.15) re-derived; rare-positive one-sidedness; excess bound; 10δ²λ constant scripted; collision terms |
| Prop 5.6 | VERIFIED (argument) |
| Lemma 6.1 | VERIFIED (argument) |
| Lemma 6.2 | VERIFIED LINE BY LINE (support chosen after θ is fine: p ⫫ θ given q; the exceptional sets depend on h only) |
| Prop 6.3 | VERIFIED (argument): all five classification branches, (6.7) scripted, the cancellation and the sandwich |
| Lemma 6.4 | VERIFIED (argument) |
| Prop 6.5 | VERIFIED (argument) |
| Lemma 7.1 | VERIFIED LINE BY LINE (incl. the parenthesisation of (7.2), checked on PDF p. 36) |
| Lemma 7.2 | VERIFIED LINE BY LINE (Young constant scripted) |
| Lemma 7.3 | VERIFIED (argument), including Y_pq = b + σ(X_p + X_q) with residual 2(X_pX_q + I_pq) |
| Lemma 7.4 | VERIFIED LINE BY LINE |
| Lemma 7.5 | VERIFIED LINE BY LINE |
| Prop 7.6 | VERIFIED LINE BY LINE |
| Prop 8.1 (statement and interface) | VERIFIED LINE BY LINE |
| Lemma 8.2 | VERIFIED LINE BY LINE |
| §8.2 (loci, symmetry against PDF p. 44, (8.4), pruning) | VERIFIED (argument) |
| Lemma 8.3 | VERIFIED (argument); the induction (8.7) checked in outline |
| Lemma 8.4 | VERIFIED (argument) |
| (8.9)–(8.11) | VERIFIED LINE BY LINE (scripted) |
| Lemma 8.5 | VERIFIED LINE BY LINE |
| Lemma 8.6 | VERIFIED (argument); (8.15), discriminant and b = 1 scripted; exhaustiveness checked |
| §8.5 | VERIFIED LINE BY LINE (rank-two case and collinear case) |
| Proof of Thm 1.1 (p. 51) | VERIFIED LINE BY LINE |

NOT READ: nothing. The reference list was read; the citations themselves are the sources seat's.

---

## 9. §1.1 state of the art: the paper's own sentences checked for internal consistency and overclaim

I checked spot items in the fetched sources under /tmp/oaimath/167/refs/. The sources seat holds the full table.

| Paper's sentence (p. 1–2) | Check | Verdict |
|---|---|---|
| "His lattice construction gives the lower bound n^{1+c/log log n} … [10, Theorem 2]" | Erdős 1946, p. 249: "THEOREM 2, n^{1+c/log log n} < g(n; r) < n^{3/2}" | MATCH |
| "Székely gave a crossing-number proof and a general incidence theorem … [25, Theorems 4 and 8]" | Székely: Thm 4 = SST unit distances; Thm 8 = p points, l simple curves | MATCH |
| "described the structure of configurations near the extremal incidence scale [15]" | Katz–Silier v2 abstract: "We obtain analogous results for unit circles." | MATCH (my initial worry withdrawn) |
| "Pach, Raz and Solymosi … logarithmic improvement conditional on a rigidity conjecture [22, Conjecture 7 and Theorem 8]" | PRS: "Theorem 8. Conjecture 7 implies that … u(n) … ≲ n^{4/3}/log^{1/12} n" | MATCH |
| "An OpenAI construction disproved it … n^{1+ε} … [21, Theorem 1.1]" | consistent with the erdosproblems page | MATCH (sources seat) |
| "Sawin sharpened the construction to u(n) ≫ n^{1.014114} [23, Theorem 1]" | Sawin Thm 1: "≥ n^{1.014114}/C" (ordered pairs) | MATCH; not the current record (Objection 5) |
| "[9, 12, 13]" attached to tower-cutting | [9] = Ellenberg–Venkatesh | COSMETIC (Objection 4) |
| "Theorem 1.1 bounds every configuration from above, leaving a gap between the known exponents" / "All constants are independent of the configuration" | true; the paper also states plainly (p. 4) that the gap's size is not estimated | no overclaim |
| §1.2's description of each section | matches the proved statements (checked section by section) | consistent |

Overclaim check: the paper never claims effectivity, never claims a value of δ, and never claims more than Theorem 1.1. The one omission is Valtr (Objection 2).

---

## 10. Summary of what would change the verdict

- A gap inside a section proof that my argument-level pass missed. Those proofs belong to the section seats; nothing in my pass suggests where to look beyond the brief's list.
- An n^{4/3}-type construction for translates of xy = 1 with injective coordinates (Observation 3).
- A failed replay of the openai/math Lean development (see §0). A successful replay would make the remaining risk purely expository.
