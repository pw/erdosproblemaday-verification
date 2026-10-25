HOLDS AS READ

Seat O: printed §2 (the scale and the coefficient), §3 (the long prime prefix), §6 (the coefficient and the limit). I checked these against Ford arXiv 1104.3264v2. I re-derived every displayed identity in §2.1, Lemma 3.4, (6.8) and (6.12) by hand, and checked the constants numerically at 60 digits.

I found no false step and no unjustified step in these three sections. Two conditions apply:
- **Proposition 5.1 decides the corollary.** The fixed-scaling corollary needs nothing beyond Propositions 3.3, 3.8 and 5.1, Lemma 5.2, (3.4) and the prime number theorem. Proposition 5.1 (the collision count K, seat T) is the only one of these I did not check, so it decides whether the corollary stands.
- **The theorem forces a property the paper says it does not need.** Theorem 2.1's two conclusions together imply that A(1;·) is continuous and satisfies a specific wrap-around relation. The paper never says this (finding 2).

Scripts and outputs: /tmp/oaimath/024/seats/O_work/scripts/{consts.py, scale.py, scale2.py}. Ford's text is in O_work/ford/.

## Findings

**1. §2.1, (2.2)–(2.4) and (1.1): the scale is right. Verified.**
- **Constants.**
  - ρ = 0.5425985860984710219594, λ = 0.6113854845504703457, γ = 0.3234575341913806766.
  - C0 = 1/(2λ) = 0.8178146400836322315.
  - D0 = (1+log(λ/γ))/λ − 1/2 = 2.17696874355941032173. This agrees with Ford's D = 2C(1+log F′(ρ) − log 2C) − 3/2 to all 60 computed digits.
  - (3.3) "0.54 < ρ < 0.545" holds. So do "18 < 30λ < 20" (30λ = 18.34) and "1.1ρ < 0.6" (1.1ρ = 0.5969).
- **The renewal sequence.** g_nρ^n → γ fast: |g_n − γρ^{−n}| = 9.5e−4 at n = 10, 3.8e−5 at n = 40, 1.5e−6 at n = 160. This agrees with Ford Lemma 3.7 ("|g_i − λρ^{−i}| ≤ 5", where Ford's λ is our γ), so (3.5) holds. The product ∏_{i≥1}(g_iρ^i/γ) converges to K = 0.61788.
- **m, θ and b_i match Ford.** ψ is continuous and strictly increasing for B > e, so m and θ are well defined. m = ⌊ψ(B)⌋ is exactly Ford's L0 = ⌊2C(log3 x − log4 x)⌋, since 2C = 1/λ. The paper's b_i = αh_iρ^{−h_i} is exactly Ford's β_i log2 x.
- **log G_m minus Ford's bracket stays bounded.** The difference is log G_m − [C0(log3 x − log4 x)² + D0 log3 x − (D0 + 1/2 − 2C0) log4 x].
  - For B ∈ [e³, 10⁶] (m from 3 to 18) it lies in [−2.006, −0.928].
  - For B ∈ [100, 10⁶] it lies in [−2.006, −0.992].
- **The difference depends only on θ asymptotically.** By Stirling it tends to the explicit limit
  E∞(θ) = θ(log(γ/λ) + λ/2) − λθ²/2 − ½log(2π/λ) − log K.
  - The remainder is O((log log B)²/log B). It is −0.34 to −0.62 at B ≈ 10⁴–10⁶, −0.036 to −0.043 at log B = 10³, and −0.007 at log B = 10⁴.
  - E∞ decreases on [0,1), from −0.683 to −1.320.
  - E∞ jumps by log(λ/γ) = +0.6367 when m increments. In other words, G_{m+1}/G_m at the switch point equals 2.34 at m+1 = 18 and 1.944 at m+1 = 300, tending to λ/γ = 1.8902.
- So (3.4), "V(x) ≍ (x/log x)G_m", is consistent with Ford's (1.1).

**2. §2.1, "No regularity of s ↦ A(1; s) is asserted or needed" (also §1: "neither conclusion assumes continuity of the coefficient"). Exposition.**
- The sentence is true about the proof, and Corollary 6.2 genuinely avoids A (finding 5).
- But the two conclusions of Theorem 2.1 together force regularity. V is regularly varying, so V(cx)/V(x) → c uniformly for c ∈ [1,2]. One dilation moves θ by about log c/(λ·B·log x) → 0, while G_m changes by a factor tending to 1 inside a cycle and by λ/γ across a jump.
- It follows that A(1;·) must be continuous on [0,1), and that lim_{s→1⁻} A(1;s) = (λ/γ)·A(1;0) ≈ 1.8902·A(1;0).
- Equivalently: V(x)·log x/x·exp(−Ford's bracket) → Φ(θ(x)), where Φ = e^{E∞}·A(1;·) is continuous and 1-periodic.
- The (2.8) normalization is compatible with this. As s → 1⁻, α_s → λ/ρ, and the prefactor ρ^{H(H−1)/2}(γ/α_s)^H equals (λ/γ) times the prefactor for H+1 at s = 0, under the index shift h → h+1. D(h,η) is shift-invariant.
- I could not test it numerically: A_H for H ≥ 16 involves primes with log log Q up to about 3.5·10⁵.
- The paper should state this. It is a free, falsifiable consequence, and the "needed/asserted" wording invites the reader to think A may be irregular.

**3. §3.1, (3.7) and (3.8): the deduction from Ford is correct as used.**
- **Theorem 10 split.** Ford's Theorem 10 (rendered page 5) reads "(a) If 0 < ε ⩽ i/(3L0)" and "(b) If i/(3L0) ⩽ ε ⩽ 1/8". So the paper's split "For i ≤ 3ηm, Theorem 10(b) … For i > 3ηm, Theorem 10(a)", with 0 < η ≤ 1/8, is right. (pdftotext of Ford garbles i/(3L0) as "3Li 0", which looks like the opposite split; the rendered page settles it.)
- **The bound arithmetic holds.** "(i/(ηm)) exp{−η²m(m−i)/(4i)} ≤ η^{−1} e^{−η²(m−i)/4}" is correct, and summing over m − i ≥ P gives ≪_η e^{−η²P/4}.
- **Theorem 16.** It is used with Ψ = P, L = L0 − P and ξ_i = 1 + 10^{−4}e^{−(L0−i)/40}, all exactly Ford's (6.1)–(6.2). "Its final adjacent-coordinate inequality has coefficient 1 in place of a1 < 1" is accurate: Ford's (I_{L−1}) is 0 ≤ x_L ≤ ξ_{L−1}x_{L−1}.
- **Quantifier order.** Ford's V(x; C) counts values with some preimage satisfying C, so the complement controls every preimage, as the paper says.
- **Other inputs.** q_i(n) counts primes with multiplicity (Ford: q_i(n) = 1 for i ≥ Ω(n)), so a missing p_L falls in Theorem 16's exceptional set. (3.9) matches Ford Lemma 2.6 verbatim.
- **Side remark (exposition).** With η = 0.04, the constant in e^{−cP} is c = η²/4 = 4·10⁻⁴, and P = ⌊log log H⌋. So ε_H in Proposition 3.3 decays like (log H)^{−0.0004}, with a prefactor of about η^{−3}. This is harmless for an iterated limit. It does mean the approximants A_H carry no usable rate (see finding 9).

**4. §3.2–§3.6: Lemmas 3.4–3.7 and Propositions 3.3 and 3.8. Verified.**
- **Lemma 3.4, re-derived:**
  - the inversion u_i = Σ g_{t−i}s_t, giving Vol S_j(1) = G_j and W_t ~ Dirichlet(1,…,1);
  - the scaling u_i/K_i maps S_j(β) into S_j(1), with Jacobian ∏β_r^{j−r};
  - the identity Σγ′_t s_t = β_0 B, with γ′_t ≤ g_t, gives the slice bounds jg_tD/B and jg_tβ_tD/B.
- **Lemma 3.5.** The Dirichlet concentration and the ratio (j−i+1)/(j+1) ÷ (h_i/m) = 1 + O((Q+1)/h_i) check out.
- **Lemma 3.6.** The unit-box perturbation is O(h_t²) and is absorbed by C·h_t²ρ^{h_t}·u_t ≫ h_t³. The shell fraction is C_A(h^{−3} + he^{−h/40} + h³ρ^h), and Σ_{h≥H} h^{−3} gives H^{−2}.
- **Lemma 3.7.** The Rankin argument is correct.
- **Proposition 3.3:**
  - removing Ω(v) > 5B is valid, since z − 5 log z = −1.309 < −1;
  - Ω(n) ≤ Ω(φ(n)) + 1;
  - p0 ≥ x^{0.9} follows from log p1 ≤ (log x)^{0.61}, because 1.1ρ = 0.597 < 0.61;
  - the p0-count bound for a with log a > exp(2b̃_L) holds.
- **(3.11).** The bounds 0.62b_R, exp(0.89b_R) < log p_R (note α/α_θ ≥ 1, so b̃ ≤ b) and "w bounded in terms of H alone" all hold.
- **Proposition 3.8.** (3.19) holds since ρ^J = h^{−18.34}. The bound (3.20) uses Ford Lemma 2.6 with log S = e^{b^{1/3}}; (3.21) counts squares of q > z_i; (3.22) uses the Ω(D_i) bound. In the Ω(D_i) step, the overlap correction 1 − Ω(p_L − 1) ≤ 0 is right.
- I found no step that assumes its conclusion, and no "clearly" covering a hard step.

**5. §6.1, Proposition 6.1 and Corollary 6.2: the fixed scaling holds, given Proposition 5.1.**
- **T(t) factors exactly into a p0 count times x-data.** T(t) = {(p0, datum) : datum ∈ D_H(x), x^{0.9} ≤ p0, (p0 − 1)D ≤ t}. This holds because the index-0 simplex inequality uses u0 = B(x), not p0, and p1 < x^{0.9}.
- **The p0 count is a plain prime count.** Since log D ≤ (log x)^{0.8}, PNT gives the count t/(D log x)·(1 + o(1)) uniformly in the datum.
- **Coverage at t = x/c uses x-parameters.** Ford's V(x; C) counts all values ≤ x, so values ≤ x/c are covered. Moreover D(x/c) ⊆ D(x) and K(x/c) ≤ K(x), because G(t) = G(x) ∩ T(t).
- **Subtraction.** Subtracting the t = x and t = x/c identities cancels M_1(x;H) exactly.
- **Quantifiers.** lim sup over x is taken at fixed H, then the H-independent left side is bounded by inf over H. The order is correct.
- So "the latter integer never enters the comparison" is accurate: neither θ(cx) − θ(x) nor the wrap at s → 1⁻ / s = 0 plays any role.
- (5.12) carries absolute-value bars in the TeX (the pdftotext copy lost them), so both directions are available.

**6. §6.2, Lemmas 6.3 and 6.4. Verified.**
- **Finiteness.** The witness universe is ⊆ {1..q_H}^{H−P} × {1..A*_H}, independent of s and x. D(h,η) ≤ Σ log(j+1) ≪_H log 2h.
- **(6.8).** The t_i-slack translation gives (B − Σ g_iC_i)₊^R/(R!∏g_i). I re-derived it.
- **The datum is counted once.** M_f = Σ_d (f/d)·(prime mass of ⋃_η region_η). This is exactly the union structure of (2.8).
- **Primes to volume.** The relative error is O(e^{−c b_R}), independent of R.
- **ξ → 1 and the shells.** Both cost O_{K_H}(Σ_{h≥H}(he^{−h/40} + h³ρ^h)).
- **Band removal.** (6.10) checks out: u_i ≥ g_{R+1−i}v_{H−1} by keeping one tail term and using the renewal. Lemma 3.5 then applies with Q = P, since h_i ≥ H ≫ P. With K_H = H^{o(1)}, all errors are o_H(1) after x → ∞.

**7. §6.3, Proposition 6.5, and (6.12): the normalization of (2.8) is right.**
- G_{m−H}/G_m = ∏_{l<H}(m−l)g_{m−l}/B → (γ/α_θ)^H ρ^{H(H−1)/2}.
- (1 − q_{m,T})^{m−H} → exp(−(γ/α_θ)S_T), using α/α_θ = log B/(λm) = 1 + (λθ + log log B)/(λm).
- This matches (2.8) exactly: exponent H, ρ^{H(H−1)/2}, and threshold (γ/α_s)ρ^h·max D.
- The inclusion–exclusion has boundedly many terms for fixed H, and the same W_{H,θ(x)} sits on both sides. So the errors are uniform in phase without comparing witness sets at nearby phases.

**8. §6.4, Lemma 6.6, and the proof of Theorem 2.1. Verified.**
- Exact-phase sequences x_n (ψ(B_n) = n + s) give |A_H(s) − A_K(s)| ≤ ζ_H + ζ_K uniformly in s, so the limit exists and sup_s|A_H − A| ≤ ζ_H.
- The bounds c₋ ≤ A ≤ c₊ come from (3.4).
- The definition (2.8) is finite and absolutely convergent. It uses V only as the name of the index set (d = φ(w(η))), and for f = 1 no ℓ appears.
- The Lean comparator statement (ComparatorChallenges/TotientAsymptotic.lean: IsWitness, AH, A, mainTerm, totient_asymptotic_formula) matches (2.1)–(2.8) and Theorem 2.1 as printed, checked line by line. ρ^{H*(H−1)/2} uses natural-number division, which is exact. The finsum supports are finite, so finsum is not silently 0.

**9. §1, "We obtain an explicit asymptotic equivalent"; §2.1, "an explicitly constructed function of the phase θ". Exposition.**
- A(1;·) is a limit whose existence, and both bounds, are proved through V itself. The paper says so honestly.
- No value or numerical range of A is given beyond Ford's O(1).
- Already for H = 16, A_H needs primes with log log Q up to 1.1(λ/ρ)·Hρ^{−H} ≈ 3.5·10⁵.
- ζ_H has no rate (≥ (log H)^{−4·10⁻⁴}, finding 3).
- So "explicit" holds only in the definitional sense. Whether this answers #416's second part ("is there an asymptotic formula?") is a framing question; that belongs to seat W. The real mathematical content beyond Corollary 6.2 is the log-periodicity in finding 2. That is a genuine strengthening, but it is not a computable formula.

**10. Minor.**
- **Definition 3.1, "For S ≥ e^e".** Ford's Definition 1 says "When S ⩾ 2". This is immaterial, since every S used is exp exp(b^{1/3}). Severity: typo.
- **Theorem 2.2's error term.** The TeX reads (x/log x)·G_m·(A(f_k;θ) + o(1)), so the o(1) is relative to G_m. pdftotext misplaces the bracket. This is not an error in the paper.

## Results from other sections I used as given
- Proposition 5.1, the K(t) bound. Everything in Proposition 5.3, and therefore Proposition 6.1, Corollary 6.2 and Theorem 2.1, rests on it.
- Lemma 5.2 I did check; it is elementary and correct.
- §4 in full.

## Not checked
- §4 and §5 beyond the statements above.
- §7 (Lemmas 7.1–7.3 and the k = 1, 2 seed).
- Ford's own proofs of Theorems 1, 10 and 16, Lemmas 2.6 and 3.7, and Corollary 3.5. I used them as stated, and checked their statements against the rendered PDF.
- Any Lean proof content.
- A numerical test of the implied continuity of A(1;·) (finding 2). It is infeasible: the witness primes are astronomically large.
