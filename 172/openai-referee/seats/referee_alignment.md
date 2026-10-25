# Referee report — scope `alignment`: proof of Principle 2.4 (Sections 6, 7, 8; PDF pp. 38–67)

Paper: OpenAI, "Monochromatic finite sums and products in the positive integers" (23 Sept 2026).
Referee tag: alignment. Section 2 read only for the statement of Principle 2.4, Definitions 2.1/2.2, (2.12)–(2.13).

## 0. Where the uniformity of δ actually lives (answer to hunt item 1)

δ is defined once, explicitly, at (8.26), p. 67:

> "δ = ∏_{i∈I} 1/(3Q_iV_i) > 0, with the empty product equal to 1. This definition precedes the choice of admissible parameters, models, and τ."

Q_i (number of complete options at pivot i) and V_i (number of slots) come from Lemma 8.1 (p. 58):

> "All these lists depend only on n, r, s. There are finite lists B ⊂ Q^n_{>0} and A ⊂ Q_{>0} containing, respectively, the final scale tuples and every palette index consulted during the construction."

The chain that makes δ complexity-free has three links, and I checked each:

1. **Uniform finite coloring recurrence (Lemma 8.1, pp. 57–59).** Recurrence is used ONLY as a combinatorial statement about colorings of a group, never as a measure statement. Uniformity over all actions is obtained by working in the free nilpotent group of step s on the abstract letters and pulling colorings back: "Give every letter type its own generator in the free nilpotent group of step s ... these cylinders cover the space. A finite subcover gives finitely many pairs (k, J). Pulling a coloring back by the homomorphism that interprets the generators proves the same assertion in every nilpotent group of step at most s." This is correct: the free class-s nilpotent group on finitely many generators is countable (so [37, Cor. 3.7] applies), the success set of each (k,J) depends on finitely many coordinates (clopen cylinder), and the free class-s group is relatively free, so every assignment of the letters in any group of class ≤ s extends to a homomorphism. B is therefore fixed from n, r, s alone, before any model, residue, subsequence, period d0 or threshold appears. The model-dependent objects (microcell, residue r0, subsequences, d0, lifts) only select WHICH of the pre-listed options succeeds, which A_w permits ("some b ∈ B").
2. **Nilpotence of the acting group independent of complexity (Lemma 7.7, p. 55).** Verified line by line (see §3 below): all weight-(1..s) polynomial shears form a group of class ≤ s regardless of dimension and coefficients; lifts (7.18) are such shears; slot translations are weight-1 translations.
3. **Pointwise coverage → mass (Lemma 8.3, (8.22)–(8.24), pp. 65–66).** For every cover point z the plan yields an option o with Θ(J_o z) ∈ F_o; each J_o is a fixed shear preserving λ_E asymptotically ((7.20)); closed-set Portmanteau gives Σ_o μ_{β,r}(F_o) ≥ 1, hence μ(∪F_o) ≥ 1/Q_i. The sets F_o depend only on the limiting readings, not on the lifts. This is the only quantitative loss; it is exact on the limit measure. Equidistribution (rate-dependent) enters only to transfer the limit bound to the actual sampling with an o(1) error, which is all (2.13) asks ("no assertion of a convergence rate uniform over all complexities").

So the strongest uniformity in the paper IS proved, by an argument I could not break. The brief's worry (a BHMP-type uniform measure bound silently assumed from [37]) does not arise: the paper takes nothing measure-theoretic from [37].

## 1. Objections

No FATAL objection and no GAP found in this scope. The items below are the residue of a hostile read; none affects the proof.

**A1. §8.1, p. 57 — handedness/form of the cited recurrence (COSMETIC).**
Paper: "We use the finite-coloring consequence of nilpotent polynomial recurrence in [37, Corollary 3.7]. In the form needed here, for finitely many ordered words w_j(k) = a_{j,1}^{P_{j,1}(k)} ··· a_{j,l_j}^{P_{j,l_j}(k)}, P_{j,l} ∈ Z[k], P_{j,l}(0) = 0, in a nilpotent group of bounded step, every finite coloring admits k > 0 and J for which J, w_1(k)J, ..., w_q(k)J have the same color."
Source gives the left-translate pattern {s g(α) : g ∈ A} with an IP parameter α. The paper's stated conversion ("apply its left-translate formulation to the inverse words and to the coloring g ↦ C(g^{-1}), and then invert the resulting pattern") is correct: with C'(g)=C(g^{-1}) and A = {1, w_j^{-1}}, C'(s)=C'(s w_j^{-1}) gives C(s^{-1}) = C(w_j s^{-1}); inverses of VIP maps are VIP by [37, Thm 2.5(3)]. The claim "α ↦ a^{P(|α|)} is an IP polynomial for this filtration" is asserted with a one-line reason; it is exactly [37, Cor. 2.26] (products over α^d) with the stretched filtration (2.27) of the source, which the paper's H_j = γ_{⌈j/D⌉}(G) reproduces, and it vanishes at ∅ because P(0)=0. Nonemptiness of α (so k=|α| ≥ 1) is inherited from [37, Thm 3.6] ("non-empty subsets"). Fix: cite [37, Cor. 2.26] for the IP-polynomial claim. No effect.

**A2. §8.1, p. 58 — the compactness re-derivation is redundant (COSMETIC).** [37, Cor. 3.7] is already finitary for a fixed group ("there exists N ∈ N and finite sets S, T ⊂ G such that for every l-coloring of T ..."). The paper's cylinder/compactness argument reproves that and then adds the essential step (pullback from the free class-s group). Correct as written.

**A3. Notation "D ⊂ E_B" in Lemma 8.1, (8.18), §8.5 versus "D ⊆ E_B" in (2.12) (COSMETIC).** Principle 2.4 quantifies over "subset D ⊆ E_B"; §8 writes "every D ⊂ E_B". The paper uses ⊂ non-strictly throughout (e.g. "B ⊂ Q^n_{>0}", "A ⊂ qN"), so this is the same quantifier; if ⊂ were read as proper, D = E_B would be missing from the Alignment conclusion. Fix: write ⊆.

**A4. §6.1, Theorem 6.1, p. 39 — small mismatches with the source (COSMETIC).** Paper samples {0,…,N−1}^d and allows 0 < δ < 1; [12]/[13] use [N] = {1,…,N} and 0 < δ < 1/2, with a 1/δ-rational Mal'cev basis. All three are absorbed exactly as the paper says ("decreasing the accuracy below the reciprocal of its fixed rationality bound absorbs that hypothesis into A"; failure of δ-equidistribution implies failure of δ'-equidistribution for δ' < δ; a unit translation changes binomial Taylor coefficients by a bounded triangular map). No effect.

**A5. §7 preamble, p. 46 — "rational element" defined differently from the cited source (COSMETIC).** Paper: "A rational element is an element with rational logarithm in this structure ... see [12, Section 2 and Appendix A]." [12, Def. 1.11]: "A rational group element is any g ∈ G such that g^r ∈ Γ for some integer r > 0." These coincide for nilmanifolds with a rational Mal'cev structure (standard), so nothing breaks; the citation supports the paper's usage only after that standard identification.

**A6. §7.2, Lemma 7.3, p. 50 — discreteness of Λ′ is argued by a sketch (UNCLEAR, not a gap).** "Finitely many fixed rational elements, together with a finite generating set of Λ, generate a discrete group Λ′ containing Λ ... Applying the finite BCH formula to their ordered powers bounds every coordinate denominator by one fixed integer, independent of the word and its integer exponents." This is the standard fact that a finitely generated subgroup of a unipotent Q-group has Mal'cev coordinates in (1/N)Z for one N (Hall collection gives coordinates as Q-polynomials in integer exponents). The sketch is adequate; I did not write out the collection argument.

**A7. Prop 6.3 proof, pp. 42–45 — the induction is long and I did not re-derive every weight estimate (see §3 for exactly what I checked).** Not an objection; recorded so the "verified" label is not over-read.

## 2. Citation table (scope: §§6–8)

| Cited result | What the paper says it gives | What the source says (quote) | Verdict |
|---|---|---|---|
| [37] Zorin-Kranich, arXiv:1206.0287 **v4, 4 Jun 2018** (= current version; matches the paper's citation), Cor. 3.7 | Finite-coloring polynomial recurrence in a countable nilpotent group: ∃ k>0, J with J, w_1(k)J, …, w_q(k)J monochromatic | "Corollary 3.7. Let G• be a filtration on a countable nilpotent group G, m ∈ N, A ⊂ VIP(G•)^{⊗m} a finite set, and l ∈ N_{>0}. Then there exists N ∈ N and finite sets S, T ⊂ G such that for every l-coloring of T there exist α1 < ··· < αm ⊂ N and s ∈ S such that the set {s g(α), g ∈ A} is monochrome." | MATCH after the paper's (correct) inversion for handedness; source is combinatorial and finitary per group; NO measure lower bound is claimed or needed |
| [37] Thm 1.1 / Thm 5.32 (measure version) | not used | "the set {n : μ(A ∩ ∏ T_i^{p_{i,j}(n)}{}^{-1}A) > 0} is FVIP*" — positivity only, no uniform bound | not relied on (correctly) |
| [37] Thm 2.5 | products/inverses of polynomial maps are polynomial | "(2) ... the product g0g1 is also G•-polynomial. (3) ... its pointwise inverse g^{-1} is also G•-polynomial." | MATCH |
| [12] Green–Tao, arXiv:0709.3562 (current v6, 14 Aug 2015), Thm 2.9 | one-variable quantitative Leibman, unaffected by erratum | "If (g(n)Γ)_{n∈[N]} is not δ-equidistributed, then there is a horizontal character η with 0 < \|η\| ≪ δ^{−O_{m,d}(1)} such that ‖η∘g‖_{C^∞[N]} ≪ δ^{−O_{m,d}(1)}." (with a 1/δ-rational Mal'cev basis) | MATCH |
| [12] Thm 8.6 as corrected in [13] = arXiv:1311.6170 **v3, 14 Aug 2015** (current; matches citation), p. 3 & §3 | equal-side multiparameter quantitative Leibman (Theorem 6.1) | Erratum abstract: "The proof of Theorem 8.6 ... was incorrect, and furthermore fails when at least one (but not all) of the Ni are small ... we deduce the 'equal sides' case N1 = ··· = Nt = N of this result from the 1-parameter results." Corrected statement p. 3: "Then either (g(n)Γ) is δ-equidistributed, or Ni ≪ δ^{−O(1)} for some i, or else there is some horizontal character η with 0 < ‖η‖ ≪ δ^{−O(1)} such that ‖η∘g‖_{C^∞[N]} ≪ δ^{−O(1)}. In the 'equal sides' case N1 = ··· = Nt, the alternative Ni ≪ δ^{−O(1)} may be deleted." | MATCH. The correction changed the HYPOTHESIS (equal sides, or an extra small-side alternative), not the smoothness/rationality exponents. The paper uses only equal-side cubes (tiles boxes by cubes of side ⌊λZ⌋) and says so: "no assertion about unrestricted unequal side lengths is needed." |
| [12] Def. 1.2(iii) | δ-equidistribution = Haar error ≤ δ against Lipschitz norm ≤ 1 | "E F(g(n)Γ) − ∫F ≤ δ‖F‖_Lip ... ‖F‖_Lip := ‖F‖_∞ + sup..." | MATCH |
| [33] Szemerédi (finite), [35] van der Waerden (finite) | used in Prop 6.3 to extract/thin progressions | standard finite forms | MATCH (standard) |
| [16, Defs A.5–A.6, Lemma 2.9], [12, Thm 1.19] | context for factorization | — | not load-bearing: Lemma 7.3 is proved in the paper |
| [14, Prop 11.5, Appendix E], [24] Host–Kra | context for cubes / missing corner | — | not load-bearing: Lemma 7.2 proved in the paper (I checked it) |
| [1, proof of Prop 4.1] | "compensating rescalings follow the mechanism" | not fetched | not load-bearing: (8.2) verified directly |
| [26] Leibman | qualitative equidistribution, context | — | not load-bearing |

## 3. Verified line by line vs. skimmed

**Verified line by line (each inequality/identity re-derived):**
- (8.1)–(8.2): b′_{B0}=b_{B0}; b′_A/b′_U = (b_A/b_U)k^{λ_e}, λ_e = p_A − p_C + p_{T0} > 0 (since p_a = 2^{n−a} > Σ_{ℓ>a}p_ℓ ≥ p_C for a = min P).
- Lemma 8.1 backward recursion: (8.6) w[bκ(k)] = I_k(w)[b]; the preservation argument via (8.7)–(8.8); forward execution establishes all terminal lists; multi-pivot ordering via D_i; q0 chosen after the plan without affecting alternatives (alternatives are uniform over interpretations); slot list finite. The free-group compactness + pullback giving uniformity over all class-≤s actions.
- [37] Cor 3.7 statement, Thm 2.5, Cor 2.26, Thm 3.6 (nonempty α) against the paper's use.
- (8.9)–(8.11): integrality of q_e, r_e, Δ_e; W | r_e; W^w | Δ_e; t_C(p+mr_e)+mMΔ_e = t_Cp+mq_e.
- (8.12) R = M⌊H_i^{1/2}/M⌋ and the three domination claims; the H_i-boundary cost estimate.
- (8.14): array is in P_q(G); ℓ ↦ ℓ+1 is left multiplication by the constant array g^t (linear orbit).
- (8.15)–(8.16): change of variables; one residue class mod dt; (8.17) and the CRT representative independent of t_ℓ; S_e on face ω_j=1 ≡ x_j ↦ x_j + Δ_e at all slots; |Δ_e|/Z → 0.
- (8.21) and m_e q_e = (h_A b′_A d_A/(h_B b′_B d_B)) t_A, i.e. exactly the offset in (2.12) at b^fin = b′d.
- Lemma 8.3: palette (8.20); terminal own-letter words project to the commuting array shift u ↦ u+m and slot v ↦ v+m, so readings become R_{v,0} and R_{v+m,m}; closedness of F_o; coverage; (8.23) both derivations; open enlargement (8.24) with the 3τ/2, 7τ/4, 5τ/4, τ/4 margins; contradiction structure (subsequence selection).
- (8.25) against Lemma 3.1(2)/(3.3) (TV = half of ‖·‖_1); |s(v)| ≤ CMW^w ≤ CM² = o(X_i); W | s(v).
- (8.27)–(8.28) and the path iteration giving δ − o(1); preservation between pivots via D_i.
- Lemma 7.1 (face coordinates, suffix ideals, top-vertex statement, reflections); filtration (7.3) bracket condition.
- Lemma 7.2 (missing corner): uniqueness via face-coefficient recovery and G_{s+1} = {1}; continuity via compact injective deletion map; linear orbit cubes lie in the cube group.
- Prop 7.5: (7.15); Ψ(J) = J by path lifting under J → J/Γ_J and K′ → K′/Λ′; (7.16) via the (i+1)-cube with exp(tU) on the face [i] and the top-vertex element exp(−tU)Φ(exp tU) ∈ J_{i+1}; D in (7.17) has weighted degree < output weight; T = u + RD(pu) is a shear; (7.14).
- Remark 7.6 example (corner sum (1/3,0)).
- Lemma 7.7: representation on V_s, (T* − 1)V_d ⊆ V_{d−1}, I^{s+1}=0, [1+I^a,1+I^b] ⊆ 1+I^{a+b} ⇒ class ≤ s independent of dimension and coefficients; Jacobian 1; (7.20) with O_T(E^{−1}); left multiplication is a shear; uniqueness of H-invariant measure ⇒ Haar limit.
- Lemma 6.2 (exact division after interpolation): sup bound, extrapolated derivative bound C_q ε(1+2S)^q, denominator D_H m^q with m ≤ S, exact vanishing, integrality of R(z) and of M(z) via coprimality.
- Theorem 6.1 vs. [12]/[13], and the "box consequence" (tiling, (D_0!)^d clearing, translation estimate).
- Prop 7.4 key step: maximal j, ξ = χ_D|_{H_j} kills H_{j+1} and [H_i,H_{j−i}], coefficient (7.11) = ξ(a_{j,L})/(j−|D|)!, contradiction with (7.5).

**Checked at the level of each step's claim but not every constant (skimmed):**
- Prop 6.3 induction: I checked the passage failure ⇒ bad progression family (Szemerédi, w-smooth step jL), (6.13), the descending induction to (6.14) using Lemma 6.2 in both cases p_z ∈ {1, t_z}, the constant-term coloring, (6.16)–(6.18), H_ξ connected/simply connected/rational, the K-residue splitting giving σ_jΓ, and the induction landing on H_ξ/(H_ξ ∩ σ_jΓσ_j^{−1}). I did NOT re-derive the subbox weight comparison "differ in total by O(t_z/Z)" or the λ-freezing constant C_2 in detail.
- Corollary 6.4 and the Fubini/union-bound paragraph closing §6.4.
- Lemma 7.3 descent: termination by Σ dim H_i, adaptation of R′_L to the new filtration (I checked the degree-j coefficient lands in the new h_j), convergence of h_L(Lβ); the Λ′/Λ″ periodicity argument (A6).
- Prop 7.4 remaining parts (frozen h(β), mixture (7.8), uniformity over boxes/residues).
- Lemma 8.2 exposure: domination of the tail law by a constant times product-uniform (scale-invariance of harmonic mass, (1/M)log(1+t_lo R/Q) independent of t), discards of boundary bins, countable diagonal selection.
- Lemma 7.2's Stone–Weierstrass consequence (used in Prediction, outside my scope).

**Not checked (outside scope or not fetched):** anything in §§2–5; [1] Alweiss; GTZ/Tao–Ziegler; [16]/[14] (context only).

## 4. Hunt-list answers (short)

1. δ: (8.26), from Lemma 8.1 counts Q_i, V_i; depends only on n, r, s (word templates, exponents, palette size 2^{r|L|}, s). B fixed before models; residues/subsequences/d0 enter only the realization. Quote: "Every step of the construction used only n, r, s."
2. [37]: cited version v4 = current. Source gives only combinatorial/finitary coloring recurrence per countable group; no uniform measure bound, and the paper uses none. Uniformity across systems: free-group pullback (Lemma 8.1) + pigeonhole (8.23). No BHMP-type argument needed.
3. GT erratum: changes the hypothesis (equal sides), not exponents; paper uses only equal sides. Prop 6.3 survives.
4. Prop 6.3: an exceptional-proportion → 0 statement whose rate depends on the fixed nilmanifold list, D, c, C, B, η; uniform in coefficients, residue, boxes, observables. Used only for o(1) terms in Lemma 8.2. Compatible with δ.
5. Lemma 7.2 verified. Prop 7.5 verified. Class of the generated group ≤ s, proved in Lemma 7.7, independent of number of blocks and dimension: "This bound does not depend on the dimension or the coefficients of the shears."
6. Equidistribution is rate-dependent but enters only the transfer limit-law → actual law; the lower bound itself is exact on the limit. "For sufficiently late terms ... The compactness subsequence and how late the estimates hold may depend on τ and the fixed model complexity. The constants Q_i and the displayed lower bounds do not." Every "sufficiently large w" in §§6–8 is either integrality from fixed lists, a fixed-H threshold, or this late-term transfer.
7. The random offset is realized as an exact integer argument shift: (8.21) gives t(p+s(v)) + Σ m_e q_e with m_e q_e = (h_A b′_A d_A/(h_B b′_B d_B)) t_A; integrality uses Def 2.1(1) (h_A/h_U ∈ W^w Z for A ∈ E_U) and q0. The slot shift p ↦ p+s(v) is removed by (8.25) on the raw harmonic law, uniform in earlier variables.
8. No bound on g or x is used anywhere in §§6–8: Prop 6.3 is uniform over polynomial coefficients; Lemma 7.3 normalizes P_L(0) by λ_L ∈ Λ and states "No boundedness of the Taylor coefficients a_{j,L} is asserted or required"; arrays live in compact quotients P_q(G)/P_q(Γ). Bounded complexity (fixed finite nilmanifold list, uniform Lipschitz bounds) IS used — in Lemma 8.3's compactness of observables — and that is exactly what Def 2.2 grants.

## 5. Verdict for scope (§§6–8, proof of Principle 2.4)

**HOLDS AS READ.** The complexity-independence of δ is genuinely proved: Lemma 8.1 (finite plan, uniform over all class-≤s actions via the free nilpotent group and [37, Cor. 3.7], whose citation matches), Lemma 7.7 (class ≤ s of the lift group, independent of model complexity), and the coverage/pigeonhole step (8.23) in Lemma 8.3, with all complexity dependence confined to o(1) transfer errors. Residual risk: the Prop 6.3 induction and Lemma 7.3/Prop 7.4 were checked step-by-step, not constant-by-constant (§3). Nothing found in this scope would make the paper fail; if the paper fails, the failure is outside §§6–8.
