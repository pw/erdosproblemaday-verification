# Hostile referee report: "Monochromatic finite sums and products in the positive integers" (OpenAI, 23 Sept 2026)

Text read: `/tmp/oai-math/Monochromatic-finite-sums-and-products-i.txt`, all 3992 lines, §1–§8 in full. Line numbers below refer to that file. Primary sources checked: `sources/zk.txt` (Zorin-Kranich, arXiv:1206.0287v4), `sources/tz_concat.txt` (Tao–Ziegler, arXiv:1603.07815v4), `sources/gtz_erratum.txt`, `sources/gt_erratum.txt` (arXiv:1311.6170v3), `sources/alweiss.txt` (arXiv:2307.08901v6). I also downloaded GTZ arXiv:1009.3998v5 to `sources/dl/gtz.txt`. Python checks are in `/tmp/oai-math/checks/`.

**Bottom line: I found no fatal gap and no repairable gap.** Every objection I raised went away when I checked it. The only defects are expository (items 10 and 18).

---

## 1. The deduction in §2.5 (lines 440–513). NOT A GAP

> "For a nonsingleton J ⊆ [m], let d = max J. Each B_k, k ∈ J \ {d}, belongs to E_{B_d}. The corresponding instance of (2.12) therefore gives S_d(L_J(z(t))) > τ." (466–470)

What I checked:
- **Chain condition.** By (2.2), T_k < T_d < i_k < i_d for k < d. So B_k = T_k ∪ {i_k} has the form P ∪ {j} with P = T_k < T_d < j = i_k < i_d. That puts it in E_{B_d} by (2.1). So D = {B_k : k ∈ J∖{d}} ⊆ E_{B_d} is an instance Alignment provides.
- **Matching the shift.** The shift in (2.12) is Σ_{A∈D} (h_A b_A/(h_B b_B)) t_A. With c_k = h_{B_k} b_{B_k} this equals Σ_{k∈J∖{d}} (c_k/c_d) z_k, so the argument is exactly L_J(z(t)).
- **Centers.** Lemma 2.5 with x_i = h_i b_i t_i gives U(z(t)) = 1, so χ(h_{B_d} b_{B_d} t_{B_d}) = c. Since b_{B_d} ∈ A by (2.6), the calibration event G_w forces S_d(t_{B_d}) > 2τ. Each integrand is then ≥ τ^{2^m−m−1} ≥ τ^{2^m}.
- **Integrality.** Lemma 3.3(1) gives h_A/h_B ∈ W^w ℕ for adding pairs and c_u/c_d ∈ Wℕ for chained blocks. The fixed rational denominators are absorbed by W^w. So every color argument (c_d z_d, Σ_{k∈J} c_k z_k, ∏_{k∈J} c_k z_k) and every L_J(z) is eventually a positive integer.
- **Positivity gives a configuration.** A positive term of the nonnegative finite average (2.10) is a tuple with every factor positive. So f_{d(J)}(L_J) = 1 for every nonsingleton J and the masks are 1. The ν-factors only restrict the support (492).
- **Quantifier order.** s = s(m) and n = n(m,r) come first. Then (B, A, δ) from Alignment, which depend only on (n, r, s). Then C, K, then τ, then η by (2.14), then Prediction (its N is chosen inside, depending on τ and η), then w ∈ U. From (2.14): C(3τ+η) < δ/2 and Σ I ≥ δτ^{2^m}/2 − Kη > δτ^{2^m}/4 > 0. Nothing circular: δ does not depend on τ or on the complexity (line 403).
- **Separation (1.1).** a_d ≤ C_0 M X_{i_d}^2 ≤ C_0 V_e^3 for d < e, and log X_{i_e} dominates powers of H_{i_e}, which dominates powers of V_e. Correct.

## 2. Corollaries 1.2 and 2.6 (lines 527–562). NOT A GAP

The cancellation and greatest-index argument is correct. Python (`check_cor12_lemma62.py`): 300 sequences, both minimal and random, satisfying (1.1) with R = 2, D = 1, m ≤ 6. All have injective subset-sum and subset-product maps, FS ∩ FP = A, and |FS ∪ FP| = 2(2^m − 1) − m. The residue argument in 2.6 (v ≡ 2v mod q forces v ≡ 0) and the compactness step are fine.

## 3. Lemma 2.5 (lines 421–438). NOT A GAP. Attribution only: COSMETIC

> "In the homogeneous ordered index set, choose successive groups of q_1 − 1, ..., q_m − 1 indices for T_1, ..., T_m, followed by m indices for the pivots" (433–435)

- The proof is correct and self-contained: Ramsey-by-cardinality, then Folkman on a ↦ κ(2a), then q_d = 2u_d ≥ 2 and Σ q_d ≤ 2F = n_0.
- Python (`check_scales2.py`): 5000 random chains built exactly as described satisfy B_k ∈ E_{B_d} for k < d and |∪_{d∈J} B_d| = Σ_{d∈J} q_d.
- The ordering is not Alweiss's. In Alweiss §5 Step IV (alweiss.txt 658–668), X_i = x_{N−i} ∏_{S_i} x_j with S_{i+1} > S_i, so tails decrease as pivots increase. The paper's (2.2) has tails increasing with pivots, and its E_B puts the summands' tails *before* the anchor tail. Alweiss Prop 4.1 uses S > T. The paper says this openly (line 418). Since its proof stands alone, the words "following Alweiss" are only an attribution and nothing depends on them.

## 4. Zorin-Kranich Cor 3.7, used in §8.1 (lines 3263–3292). NOT A GAP

Source (zk.txt 598–603): *"Corollary 3.7. Let G• be a filtration on a countable nilpotent group G, m ∈ ℕ, A ⊂ VIP(G•)^{⊗m} a finite set, and l ∈ ℕ_{>0}. Then there exists N ∈ ℕ and finite sets S, T ⊂ G such that for every l-coloring of T there exist α_1 < ··· < α_m ⊂ N and s ∈ S such that the set {s g(α), g ∈ A} is monochrome."*

- **Handedness.** The configuration in ZK is left-translated: s·g(α). The paper needs J, w_j(k)J (lines 3274–3276). Its fix is correct. Apply ZK to the inverse words and to the coloring C'(g) = C(g^{-1}). That gives C(w_j s^{-1}) constant, so J = s^{-1} works. VIP(G•) is a group (ZK Thm 2.5 and Cor 2.9), so the inverse words are admissible. The identity word g ≡ 1 lies in VIP.
- **IP-polynomial specialization.** The map α ↦ a^{P(|α|)} with P(0) = 0 is G•-polynomial for H_0 = G, H_j = γ_{⌈j/D⌉}(G). Each derivative D_β lowers the degree of the exponent in |α|, values stay in ⟨a⟩ ⊆ H_k for k ≤ D, and the (D+1)st derivative is trivial. Ordered words are covered by product closure. k = |α| ≥ 1 because α is nonempty.
- **Uniformity.** ZK already supplies finite S and N. Pulling back through the free step-s nilpotent group on the letter types gives alternatives that depend only on the templates, the palette size and s, as claimed (3284–3292). The acting group G_i is a group of shears plus translations of class ≤ s (Lemma 7.7), so the homomorphism from the free group exists.

## 5. Tao–Ziegler Thm 1.23, used for (5.11) (lines 1935–1950). NOT A GAP

Source (tz_concat.txt 721–735): *"Let (Q_i)_{i∈I} be a finite non-empty family of coset progressions Q_i, all of rank at most r, in an additive group G. Let (X,T) be a G-system ... f in the unit ball of L^∞(X), and suppose E_{i,j∈I} ‖f‖_{U^{2d−1}_{εQ_i+εQ_j}(X)} ≤ ε ... Then E_{i∈I} ‖f‖_{U^d_{Q_i}(X)} ≤ c(ε) where ... c depends only on r and d. (In particular, c is independent of the size of I.)"*

- Rank-0 coset progressions are finite subgroups, and dilation leaves them unchanged (Def 1.10).
- With TZ's convention (Def 1.9), differences h − h' of uniform elements of a subgroup are uniform on it. The multiset Q_α + Q_{α'} induces Haar measure on the subgroup sum. So TZ's norm equals the paper's.
- X_l, the disjoint union of cells with weights, is a G_l-system with G_l = ℤ/q_l, finite. Weights by repetition, then approximation, then a monotone modulus: legitimate. Independence of the number of cells is honest, because the theorem is stated for an arbitrary probability G-system.
- The coprimality step: q_p = |D(p)|_{>w} divides q_l (Lemma 3.3(4)), and Lemma 3.5 gives gcd(q_p, q_{p'}) = 1 with probability 1 − o(1). On that event Q_p + Q_{p'} = G_l. I rechecked the induction in Lemma 3.5 (Brun–Titchmarsh below √Y_0, a bounded number of large prime factors above). Correct.

## 6. GTZ inverse theorem and its erratum (lines 1951–1965). NOT A GAP

- GTZ v5, Conjecture 1.2 (dl/gtz.txt 116–124): a finite collection M_{s,δ} of s-step nilmanifolds with G connected simply connected; F bounded by 1 with Lipschitz constant ≤ C(s,δ); correlation |E_{n∈[N]} f(n) F(g^n x)| ≥ c(s,δ); no bound on g. Theorem 1.3 proves it for s ≥ 3. GI(1) and GI(2) are recalled as known (lines 60–64). This is exactly the form used. GTZ's normalization of the interval norm is the one the paper uses (line 1963).
- The erratum (gtz_erratum.txt) corrects three things. (i) Tautness of filtrations G_0 = G_1, a "minor issue". (ii) Proposition 8.3, which is false as stated; it is replaced by a Proposition 3.1 that "still suffices for the deduction of [2, Proposition 7.3]". (iii) Typos in §§9–12. None of these changes the statement of Conjecture 1.2 / Theorem 1.3. The paper's sentence "We use only this inverse conclusion, not the original auxiliary Proposition 8.3" (1960) is accurate.
- The cyclic-to-interval transfer (5.14), and taking the real part after rotating the phase, are both correct.

## 7. Theorem 6.1, citing the GT erratum (lines 2179–2245). NOT A GAP

Source (gt_erratum.txt): the corrected [GT, Thm 8.6] says either the orbit is δ-equidistributed on [N]^t, or a horizontal character η with 0 < ‖η‖ ≪ δ^{−O(1)} has ‖η∘g‖_{C^∞[N]} ≪ δ^{−O(1)}. *"In the 'equal sides' case N_1 = ··· = N_t, the alternative N_i ≪ δ^{−O(1)} may be deleted."* The one-parameter Theorem 2.9 is "not affected".

- So the equal-side statement (6.1) holds with A depending on the fixed rational basis and δ. Absorbing the rationality hypothesis is fine: a Q-rational basis is 1/δ-rational for δ < 1/Q.
- I checked the box consequence (6.3) line by line. Tile by cubes of side ⌊λZ⌋. One cube has discrepancy ≥ η/2. Multiplying by (D_0!)^d converts binomial coefficients to monomial ones with error Σ_{J≥I} O(N^{−|J|}) = O(Z^{−|I|}). Re-centring by a with |a| = O(Z) costs Σ_{J≥I} O(Z^{|J|−|I|}) O(Z^{−|J|}) = O(Z^{−|I|}). Correct.
- Only equal sides are used, as the paper says.

## 8. Proposition 3.6 (lines 885–1053), press point (i). NOT A GAP

> "On G, the preceding kernel bounds give 0 ≤ α_p − 1 ≤ β_p." (971); "Hence µ_j(n) ≤ C_0 µ̃_j(n) pointwise, with an absolute constant C_0 ... one overall constant C_0^{bq}, rather than a separate constant for each prime." (1000–1002)

- **Local kernel bound.** α_p = p^{Σa_u} P(p^{a_u} | ℓ_u for all u). If the two top-valuation rows are independent mod p, a unit 2×2 minor makes the pair bijective mod p^A, so α_p ≤ p^{Σa−A−B}. Otherwise one primitive row gives α_p ≤ p^{Σa−A}. With a single positive valuation α_p = 1 exactly.
- **Domination.** This is a domination of measures on integers, not prime by prime: n^{−ε_j} ≥ e^{−2} on [X_j, X_j²), and the normalisers agree to 1 + o(1). The integrand ∏_{w<p≤V}(1+β_p) − 1 is nonnegative, so E_µ ≤ C_0^{bq} E_µ̃ with one constant.
- **Independence across primes.** Under µ̃ the valuations at distinct primes are independent (Euler product), and the T_p are independent under CRT-uniform slots. Then Eβ_p ≪ p^{−2} in both cases, and the product gives O(1/w).
- The two total-variation replacements each cost ≤ 2V^q ε. Correct.

## 9. Lemma 4.2 (lines 1196–1318), press point (ii). NOT A GAP

> "The p and q branches are parallel precisely when all e_k on the row support are equal. That is exactly the definition of an invariant row." (1289–1290)

- **Two-coordinate case.** After absorbing pq, branch p multiplies (u, v) by (q, p) and branch q by (p, q). Both are D(·) followed by the common right factor diag(pq on u). Right multiplication by an invertible diagonal matrix preserves parallelism, so the descendants of a row R are parallel iff p^{e_k}/q^{e_k} is constant on supp R, i.e. iff the e_k are constant. That is the invariance condition.
- **Different old rows.** Parallelism over the function field means all 2×2 minors vanish identically. Specialising p = q = 1 gives R ∥ R'.
- **Distinguished row.** It stays non-invariant: in the one-coordinate case it has u plus another index with exponents 1 and 0; in the two-coordinate case it has u and v with exponents −1 and +1. z_U is unchanged in both cases.
- **Invariant singleton.** Its weight at pqt equals its weight at t because the pool primes exceed every divisor.
- **Row count.** At most q_mask 2^{q_mask} = K_m rows.

## 10. Lemma 5.5, step (5.13) (lines 2002–2016), press point (iii). COSMETIC

> "Insert one uniform subgroup direction translating the root alone; the density is invariant in that direction. For each nonempty ω ⊂ [d], choose j ∈ ω and insert a direction x ↦ T^a x, v_j ↦ v_j − a, ... which leaves that vertex fixed. These invariant changes of Haar variables commute. ... After k = 1 + (2^d − 1) = 2^d steps its retained copies are a Haar subgroup k-cube." (2004–2014)

**Objection.** As written, the procedure is inaccurate in two ways.
- The direction attached to ω fixes *every* vertex that contains j, not only ω.
- The density ψ(v) is not invariant under v_j ↦ v_j − a. So these directions can be inserted only after ψ has been discarded, and the stated count k = 2^d is not what the described sequence of steps produces.

**Why the inequality still holds.** One Cauchy–Schwarz step in the root-only direction x ↦ T^a x, which preserves ψ, gives |cube|² ≤ E[ψ²] · ‖h‖^{2^{d+1}}_{U^{d+1}_{Q_p}}. Here E[ψ²] ≤ (2J_0)^d. Since ‖·‖_{U^{d+1}} ≤ ‖·‖_{U^{2^d}} and ‖h‖ ≤ 1, (5.13) follows with k = 2^d.

Python sanity check (`check_513.py`, d = 2, random h and ψ): the worst ratio of |cube| to the one-step bound is 0.63 ≤ 1.

The rest of Lemma 5.5 holds as written:
- Periodization costs O(d/J_0).
- The pushforward density is ≤ 2J_0.
- Bessel and the inverse theorem are applied cell by cell, keeping the cell probabilities. Cells with ‖h_C‖ ≥ δ/2 carry mass ≥ δ^{2^t}/2, giving ‖P_{i,l}h‖ ≥ ½ δ^{2^t} c_t(δ/4).

So κ is uniform in the number of cells. Only the exposition of (5.13) needs fixing; the step requirement (5.1) is larger than necessary but still correct.

## 11. Proposition 6.3, the descent (lines 2343–2573), press point (iv). NOT A GAP

> "For each z choose such a piece. Its subbox and frozen observable may vary arbitrarily with z ... Thin once more to make its residue vector u mod K and its coset index j common." (2544–2546)

What I checked:
- **Joint polynomiality.** The new map Q_z(x) = exp(−a_z(x)V) P_z(x) exp(−m_z(x)V) is jointly polynomial in (z, x). Here m_I(z) are rational polynomials from Lemma 6.2 or Newton interpolation, a_z = ξ∘P_z − m_z, and BCH is finite.
- **Where the arbitrary dependence goes.** It enters only through the frozen left factor ℓ_{z,*}, the subbox and the piece. ℓ_{z,*} is moved into the observable h ↦ F_z(ℓ_{z,*} h σ_j Γ), and the bad-family definition allows the box and the test to vary arbitrarily with z. So the new data form a bad progression family on H_ξ / (H_ξ ∩ σ_j Γ σ_j^{−1}).
- **Thinning.** van der Waerden thinning z = a + bu keeps the step bm w-smooth, keeps m_I integral at the retained indices, and keeps all bounds independent of H. The finitely many characters, residues and cosets are fixed by choosing one possibility that occurs for unboundedly many lengths.
- **Descent constants.** In the descending induction from (6.13) to (6.14), the error from higher degrees is ≤ (p_z/Z)^{|J|} ≤ (p_z/Z)^e. When p_z = 1, multiplying by t_z^e gives (6.5).
- **Lemma 6.2.** I checked it by hand: the derivative bound at a = −t_0/m, the denominator D_H m^q, and the exclusion of smooth denominators by gcd(t_z, W) = 1. Python (`check_lemma62.py`): with Z = S^{14}, 60/60 random instances recover the exact root multiplicity and an integral M. Negative control with Z = S: 0/60. The domination hypothesis Z ≫ S^a is genuinely used.

## 12. Proposition 7.5 (lines 3020–3112), press point (v). NOT A GAP

> "Apply the affine map cΦ on the upper face of the last coordinate. The resulting array z'(t) has its image in the same cube coset by hypothesis." (3070–3072)

- **The hypothesis does cover the affine map.** The identity S(hyσ)Λ = hΨ(y)cσΛ = h·cΦ(y)·σΛ (from (7.15) and Φ = c^{−1}Ψc) says that applying S to a face entry h y_ω σΛ is the same as replacing y_ω by cΦ(y_ω) in cover coordinates. So "S on a face preserves the coset" (7.13) and "cΦ on a face preserves the coset" are the same statement. This needs Ψ(J) = J first, which the path-lifting argument proves.
- **Path lifting.** The orbit J/Γ_J embeds as a closed submanifold, so lifts exist. Uniqueness of lifts for K' → K'/Λ' forces Ψ(y(t))c ∈ J. The same works for the cube group C^{i+1}(J•), whose quotient embeds because C ∩ Γ_J^{cube} = Γ^{[i+1]}.
- **(7.16).** After the two left multiplications the array is the identity off the top vertex, where it equals exp(−tU)Φ(exp(tU)). Lemma 7.1 puts this in J_{i+1}.
- **Shear.** T(u) = u + RD(pu) is a shear because D lowers weight strictly and R preserves the filtration.

## 13. Lemma 8.2, the exposure (lines 3495–3633), press point (vi). NOT A GAP

> "Its uniformity in endpoints is essential: the exact microcell and hence the endpoints may depend on the pivot sampled after the exposure." (3596–3598)

- **x_0 is a sample variable, not a coefficient.** Its *class* modulo dw' is fixed by M(x_0+Y*) + r* ≡ 0 (mod w') (8.17). Here r* = t r_0 mod M is fixed because every t_ℓ mod L is exposed and M | L, and Y* is fixed by the bin. The class mod t_ℓ may depend on t_ℓ, which Proposition 6.3 allows through the arbitrary class vector b.
- **Polynomial coefficients.** The exponent (8.16) has coefficients polynomial in t and fixed otherwise: the formula (F, g, x) is fixed on non-discarded bins, and r_e and q_e are fixed by the exposed residues. Joint polynomiality in (y, t_ℓ) is preserved because the CRT representatives a_j do not depend on t_ℓ.
- **Why the late choice of microcell is harmless.** The exceptional event is a function of t alone, given the exposure, and Proposition 6.3 is uniform over every box and class. So a box chosen after sampling p is covered.
- **Conditional law.** The pivot mass in the bin preimage is (1/M) log(1 + t_lo R/Q), independent of t, so the conditional law of t is dominated by a uniform law.
- **Face translation.** d | Δ_e and |Δ_e|/Z → 0, which makes the face translation harmless under the d-residue law.

## 14. Lemma 8.3, the Portmanteau step (lines 3645–3772), press point (vii). NOT A GAP

> "Equality of palettes implies (8.22), including at equality with the threshold." (3732); open relaxation "center < 7τ/4 or translated value > 5τ/4" (3754)

- **Palette equality implies (8.22).** If [R_c > 3τ/2] = [R_t > 3τ/2], then either R_c ≤ 3τ/2, or R_t > 3τ/2 ≥ 3τ/2.
- **Pointwise coverage.** Lemma 8.1 gives, for every starting (z, 0), an option whose terminal requirements hold at the jumped center. Terminal words contain only the target's own letters. By (7.14) these act on the B-component as the commuting array shift by m, and on the slot by +m. So the jumped state Θ(J_o z) lies in F_o, a lift-independent closed subset of K/Λ.
- **Closed-set Portmanteau.** For each fixed shear J_o, Law(Θ(J_o z)) → µ_{β,r} by Lemma 7.7. This gives Σ_o µ(F_o) ≥ 1, hence µ(∪F_o) ≥ 1/Q_i on each coset, and the bound integrates over the mixture (7.8) with no measurable choice of lifts.
- **Open relaxation.** It contains ∪F_o. Once observables are uniformly within τ/4, an actual center > 2τ gives a limiting center > 7τ/4, which forces limiting translated > 5τ/4, so the actual translated value is > τ. This closes the gap between 2τ and τ.
- **Numerical meaning (8.21).** This uses t r_e + MΔ_e = q_e for own pairs, and s(v+m) = s(v) + Σ m_e r_e. Correct.

## 15. Nilpotence class and circularity, press point (viii). NOT A GAP

- The models have step ≤ s = s(m). The arrays P_q(G) have step ≤ s, so K• has length ≤ s, and the H• from Lemma 7.3 has weights in {1, …, s}.
- Lemma 7.7's representation on V_s gives class ≤ s for the shear group. I checked the commutator argument [1+I^a, 1+I^b] ⊆ 1+I^{a+b} with I^{s+1} = 0. Translations add nothing.
- Lemma 8.1 is built for the free step-s group with the same s. Alignment's lists and δ depend only on (n, r, s), and Prediction is invoked afterwards with those lists. No circularity.

## 16. The compensating scales (8.1)–(8.2) (lines 3225–3245). NOT A GAP

Python (`check_scales2.py`), exhaustive for n = 4, …, 9: for every pivot i, every update target T_0 and every pair e = (C ∪ {i}, P ∪ {j}) at that pivot, b'_{B_0} = b_{B_0} and λ_e = p_A − p_C + p_{T_0} > 0. That is 49,328 (target, pair) checks with 0 failures. The same script verifies the sign claim in Lemma 3.3 (e_j = 2^{N−j}: Σ_A e > Σ_B e for every adding pair and for chained blocks) for N ≤ 10 with 0 failures. The backward recursion (8.6)–(8.8) is correct: equality through the old center gives preservation, and every letter at the pivot scales by k^{λ_e} with λ_e ≥ 1, so ZK's exponents vanish at 0.

## 17. Other steps checked. NOT A GAP

- Lemma 4.1 and the L² estimate for A_l.
- Lemma 4.3 integrality: S | W^{e_0−1} on good tuples, and W^{e_0+1} c_k | M.
- Lemma 4.4 moments (4.16) and the weighted replacement of Ψ.
- Prop 4.5 pushforward: b coprime to k because they are disjoint pool primes against a w-smooth scale ratio.
- Lemma 5.1 directions and minors: each distinguishing minor is a single modulus M_q times a fixed integer.
- Prop 5.2 minimax: ⟨ρ, G⟩ − ⟨1, G⁺⟩ ≤ ⟨ν − 1, G⁺⟩.
- Lemma 5.3 recipe selection and the boundary estimate (5.7).
- Lemma 5.4 Ramsey on (T, l, i)-tuples and the energy identity (5.8).
- Lemma 7.2 missing corner via face coordinates.
- Lemma 7.3 descent and termination: for every ξ, (7.5) holds along the final subsequence.
- Prop 7.4 coefficient extraction (7.11) against (7.5).
- Lemma 7.7 Haar limit via left-translation shears.
- (8.25)–(8.28) translation by slots and the path bookkeeping giving δ = ∏ 1/(3Q_iV_i).
- Remark 7.6 arithmetic: Sa − a = (1/3, 0).

## 18. Notation. COSMETIC

(2.12) says "D ⊆ E_B", while Lemma 8.1, (8.18) and the final display (line 3953) write "D ⊂ E_B". If ⊂ were read as proper subset, the Alignment output would miss D = E_B. But the paper uses ⊂ for ⊆ throughout (for example "∅ ≠ ω ⊂ [d]" in (5.2) must include ω = [d]), so this is notation only.

---

## Verdict

**HOLDS AS READ.** I tried hard to break the deduction from Prediction plus Alignment, all five external citations, and every one of the eight press points. Each objection dissolved on inspection. The citations say what the paper claims, including the handedness of ZK Cor 3.7, the rank-0 and repetition form of TZ Thm 1.23, the scope of the GTZ erratum, and the equal-sides scope of the GT erratum. The only defects are expository: the misdescribed Cauchy–Schwarz procedure behind (5.13), whose inequality is nonetheless true by a one-step argument, and the ⊂/⊆ notation. Neither affects the theorem.

Context, not checked by me: `/tmp/oai-math/hindman-lean` contains a Lean 4 formalization whose only `sorry` is in the challenge statement. Its docs say Alignment is imported from OpenAI's library, and that two §5 inputs are replaced: Tao–Ziegler by Kravitz–Kuca–Leng box-norm concatenation, and GTZ by a cyclic polynomial inverse theorem. I did not build it or audit its imported Alignment.

## Steps I did not verify in full detail
- Lemma 4.4 and Lemma 5.1: pairwise independence of *every* form in the fully expanded Cauchy–Schwarz systems. Checked in outline (the distinguishing-variable argument), not term by term.
- Lemma 3.1, Cor 3.2 and Lemma 3.3: the explicit constants and the full construction order of pools and gaps. Checked qualitatively.
- Remark 3.4 and the diagonal choices in Prop 5.2: checked in outline.
- Lemma 7.1, standard Host–Kra/Green–Tao material: skimmed.
- Prop 7.4 uniformity over boxes with fixed progression restrictions: checked only the coefficient-extraction core.
- Sources not opened: GT [12] itself (only its erratum), Yamada's Brun–Titchmarsh [36], Selberg [32], Sanders and Hindman for the finite sums theorem, Leibman [26].
- The Lean formalization: not built or audited.
