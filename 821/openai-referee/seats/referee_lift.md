# Referee report, seat "lift": §5.1–5.3 (PDF pp. 35–39). Theorem 5.1 and its reduction to the local energy bound (5.11)

Paper: "Weighted dilation graphs, smooth shifted primes and totient fibers" (OpenAI, 24 Sept 2026), /tmp/oaimath/011/paper.pdf.
Formulas were read off the rendered PDF pages 10–13 and 35–39, not off the text extraction.

**Verdict for my scope: HOLDS AS READ.** This is conditional on four results outside my scope:
- Corollary 3.11 and Theorem 3.5 (§3);
- Theorem 4.1 (§4);
- Lemma 4.2, whose short proof I did check;
- the local energy bound (5.11), proved in §5.4–5.8.

I found no FATAL problem and no mathematical GAP in §5.1–5.3. Every objection below is COSMETIC or UNCLEAR, meaning an unstated but true inequality.

The question singled out for this seat was whether the raw-pattern physical pairing is exactly the sum in (5.5). It is, once the shared labels are removed:
- the sign is +;
- the cutoff is Ψ(z/Z);
- the weight is 1/z;
- the twists are z^{ia1}(z+k)^{ia2};
- F0 carries a conjugate bar.

The only difference is the overlap configurations, which cost O(L^{O_J(1)} e^{−L^a}). I worked this out by hand (Section A) and confirmed the no-overlap identity exactly on toy instances, with mutation controls showing the check can fail.

---

## A. The raw-pattern pairing, written out (J = 1, ℓ = 1, one small group s, one big group b)

**Setup (Definitions 3.1–3.3, (3.3), (5.6)).**
- M = J + ℓ = 2 and s = 2.
- Raw pattern (Theorem 4.1): C_g = ∅ and K_0 = 1. So slot 1 is shared, slot 2 is unshared, t_s = t_b = ℓ = 1, there are no free labels, and D = x1·y1. Here x denotes small labels and y big labels.
- Inner product on H_ph: ⟨f,h⟩ = Σ_n Σ_{x1≠x2 | n} Σ_{y1≠y2 | n} V_s^{−2}V_b^{−2} \bar f h. Each state has mass Π V_g^{−M}.
- Row action of the raw edge, with the §5.2 insertions (weight Ψ(n/(ZD))/n and phase D^{−i(a1+a2)}). It sums over target states at n′ = n + kD with the shared labels x1, y1 kept, with coefficient Π V_g^{−t_g} = V_s^{−1}V_b^{−1}:

  (A g)(n; x1,x2; y1,y2) = Σ_{x2′≠x1, x2′|n′} Σ_{y2′≠y1, y2′|n′} V_s^{−1}V_b^{−1} · D^{−i(a1+a2)} Ψ(n/(ZD)) n^{−1} q^{(ω(n)−4)/2} q^{(ω(n′)−4)/2} · g(n′; x1,x2′; y1,y2′).

- With f = n^{−ia1}F0(n)q^{(ω(n)−4)/2} and g = n′^{ia2}G0(n′)q^{(ω(n′)−4)/2}, and the pairing conjugate-linear in its first argument:

  P_raw = Σ_n Σ_{x1≠x2|n} Σ_{y1≠y2|n} Σ_{x2′≠x1|n′} Σ_{y2′≠y1|n′} V_s^{−3}V_b^{−3} · n^{ia1} \bar F0(n) · n′^{ia2} G0(n′) · D^{−i(a1+a2)} · Ψ(n/(ZD))/n · q^{ω(n)−4} q^{ω(n′)−4}.

  The overall exponent V_g^{−3} = V_g^{−M−t_g} is (3.4).
- Symmetrization can be dropped because f and g do not depend on the marks: ⟨f, P A_ν P g⟩ = ⟨f, A_ν g⟩.

**Reindex by the shared labels.** For fixed x1 and y1, the shared labels divide n. Write n = x1y1·w; then n′ = x1y1·w′ with w′ = w + k.
1. **Weight.** 1/n = (x1y1)^{−1} w^{−1}, so V_s^{−3}V_b^{−3}/(x1y1) = μ_s(x1)μ_b(y1) · [V_s^{−1}V_b^{−1}] · [V_s^{−1}V_b^{−1}]. This is exactly "V_g^{−M−t_g} = V_g^{−s_R,g−2t_g}". Each shared label becomes a draw of mass 1/(pV_g), and each endpoint keeps V_g^{−t_g} for its unshared list.
2. **Phase.** n^{ia1} n′^{ia2} D^{−i(a1+a2)} = w^{ia1} w′^{ia2}.
3. **Cutoff.** Ψ(n/(ZD)) = Ψ(x1y1w/(Z x1y1)) = Ψ(w/Z).
4. **Endpoints.** F0(n) = F0(w) and G0(n′) = G0(w′). Both depend only on the P-free part, and x1y1 is a P-integer.
5. **No overlap (x1, y1 ∤ w w′).** The admissible x2 ≠ x1 dividing n are exactly the small group primes dividing w, so Σ_{x2} 1 = ω_s(w); likewise ω_b(w), ω_s(w′), ω_b(w′). Also ω(n) − Ms = ω(w) + 2 − 4 = ω(w) − Σ_g t_g, and the same at n′. The source factor is therefore V_s^{−1}V_b^{−1} ω_s(w) ω_b(w) q^{ω(w)−2} = W_1(w), exactly (5.1) with every t_g = ℓ = 1. Likewise W_1(w′).
6. **Result.** P_raw = Σ_{x1,y1} μ_s(x1)μ_b(y1) Σ_{w>0, w+k>0} [Ψ(w/Z)/w] w^{ia1}(w+k)^{ia2} \bar F0(w) G0(w+k) W_1(w) W_1(w+k) + (overlap terms). Since Σ μ_s Σ μ_b = 1, the main term is literally (5.5) with z = w. The sign is +, because K_0 = 1 and nothing else contributes a sign.
7. **Overlap terms.** These are configurations with x1 or y1 dividing w or w′, and they appear both in the iid main term and in the true physical sum.
   - Their μ-mass is at most (ω(w) + ω(w′))·max μ ≤ O(L^{1−a}) e^{−L^a}/v_−.
   - In the physical sum, the damping loses at most q^{−#overlap} ≤ q^{−2Ms} = L^{O_J(1)}, and the list counts can only shrink.
   - Multiplied by Σ_w |F0 G0| W W/w ≪ L^{O(1)} (Cauchy–Schwarz plus divisor moments), the total error is O(L^{O_J(1)} e^{−L^a}). This matches the paper's bound.

The general case (any J, ℓ, comparison patterns with free labels D_C, and the ban) is the same computation group by group. I re-derived each identity the paper states in §5.2:
- M + t_g = s_R,g + 2t_g;
- ω_g(D_R w) − M = ω_g(w) − t_g;
- ω(D_R w) − Ms = ω(w) − Σ t_g − #{p | D_R, p | w};
- (D_R w)^{ia1}(D_R w′)^{ia2}(D_R D_C)^{−i(a1+a2)} = (w/D_C)^{ia1}(w′/D_C)^{ia2};
- n/(ZD) = w/(Z D_C).
The ban argument is also right: if a free label p′ divides D_C and lies in an endpoint list, then p′ | w ⟺ p′ | w′, and Σ_{w ≍ Y0, p′|w} |F0 G0|/w ≪ L^{O(1)}/p′ ≤ L^{O(1)} e^{−L^c}.

**Numerical confirmation.** Scripts are in /tmp/lift_check/. They are toy, exact-arithmetic-in-floating-point brute force over the physical states; F0 and G0 are random functions of n_*.
- raw_identity.py (J=1, ℓ=1; groups {5,7,11} and {13,17,19}; q=.6, k=2, Z=400). Restricted to no-overlap configurations: physical pairing = 0.0035393803363141046 − 0.0029700411627642284i; (5.5)-side sum with shared μ-draws = the same to 3.9e−18.
- raw_identity_J2.py (J=2, ℓ=1, M=3; groups of 4 primes; ordered distinct shared draws). Agreement to 7.9e−19.
- comp_identity.py: a comparison-type pattern. J=2; slot 1 of the big group is free with law μ_b; t_b = 2; kernel κ(f)·λ(target slot-1 label); ban enforced; shift kD_C. This is (5.7) with E_free and E_marks. Agreement to 7.2e−20.
- Mutation controls:
  - mut1.py drops the target coefficient V^{−t}: mismatch 3.2e−4.
  - mut2.py uses 1/w in place of 1/n in the physical pairing: mismatch 14.7.
  So the check can fail.
- In the toys the full sums differ from the no-overlap sums by a lot, because toy primes are tiny and the overlap mass is large. In the paper that mass is O(L^{O_J(1)}e^{−L^a}). That bound is the paper's exclusion estimate, and I checked it analytically (step 7).

## B. Re-derivation: what does Theorem 4.1 → Theorem 3.5 → Corollary 3.11 actually bound, and is each comparison bounded separately?

**The Ψ/n insertion is reduced to the Definition 3.3 multiplier.**
- Write Φ(u) = Ψ(e^u). Then Ψ(n/(ZD)) = (2π)^{−1} ∫ \hat Φ(v) (n/Z)^{iv} D^{−iv} dv.
- On a dyad [X, 2X), absorb X/n and (n/Z)^{−iv} into the first vector, and divide by X. Both factors are functions of n alone: f stays mark-independent, sup|f| does not grow, and ‖f‖ does not grow.
- The edge multiplier becomes K_ν D^{iζ} with ζ = −a1 − a2 − v. That is exactly (3.3).
- |ζ| ≤ 2L^C + L^{C7}, so Theorem 4.1 is needed with C4 > max(C, C7). See Objection 2.
- Theorem 4.1's family does not depend on ζ (statement after (4.1)). Theorem 3.5 asks for nothing about ζ beyond (3.6) ("No bound on ζ is needed apart from the assumed ideal estimate"). So one J and one family serve every v.
- **Tails |v| > L^{C7}.** I checked that C7 = C + 1 suffices: |\hat Φ(v)| ≪_j L^{C(j+1)}|v|^{−j}, so the tail is ≪ L^{2C+1−j}. Raising j does not move C7, which confirms the paper's claim. The absolute bound of Lemma 3.4 (L^{C_abs}, depending on m and C1) then makes the tails negligible after j is chosen.

**Signs and patterns.**
- Corollary 3.11 bounds ⟨f, A g⟩ with A = Sym(Σ_ν A_ν)Sym. Since f and g are symmetric, this equals Σ_ν ⟨f, A_ν g⟩: the raw pairing plus the sum of the comparison pairings.
- The signs sit inside K_ν: K_0 = +1, and each comparison carries −(−1)^{|A|+|B|} K_A K_B.
- The hypothesis (3.6) of Theorem 3.5 is literally (4.1) for the same family and the same ζ. Lemma 3.10 identifies a clean physical edge with T(Θ), up to the μ̃ and ban perturbations.

So "raw + Σ comparisons = O(L^{−D1})" is exactly what the chain proves. The norm inputs to Corollary 3.11:
- **‖f‖, ‖g‖ ≤ X^{1/2}L^{C6}, with C6 = 2C + C5/2 + O(1), independent of J and of m_probe.** Verified via |F0| ≤ L^{2C}τ_3(n_*) ≤ L^{2C}τ(n_*)², exchanging the order to sum over S′ first, Σ_{v ≍ X/P(S′)} τ(v)^4 ≪ (X/P(S′))L^{15}, and Σ_{S′} P(S′)^{−1} Π V_g^{−M} ≤ 1 (the same computation as (3.10)).
- **sup|F0| ≤ exp(O(√L)).** Verified: there are O(√L) prime factors above W, so at most 2^{O(√L)} choices each for m and p.

**Each comparison is bounded on its own.** §5.3 works with one pattern ν and one of its terms after expanding into cells and characters. The bound is L^{−D2+C8} on the minor arcs plus L^{2C_arc+O(1)} · L^{−A/2+C8/2} on the major arcs. The total over patterns, cells and characters costs a fixed log power Γ that does not depend on J: the C1-type coefficient mass, N_A N_B Q⁴ ξ^{−2} cell and character terms, and the integral of the Mellin cutoff.

Hence raw = O(L^{−D1}) + O(L^{Γ}(L^{−D2+C8} + L^{2C_arc−A/2+C8/2+O(1)})) + O(L^{O_J(1)}e^{−L^a}). The logic "raw = −Σ comparisons + small, and each comparison is small, so raw is small" is sound.

**§5.3 checks.**
- **Separation.** After expanding K_A K_B into cells and characters, the factors on D_A and D_B separate, the mark functions land on X_A (target) and X_B (source), and U and V do not depend on D_A, D_B.
- **Size of the free product.** H′ ≥ exp(L^c), because each free product contains a big prime; also D_A D_B ∈ [H′, H′e^{2h}).
- **Bilinear form.** Σ_w \bar U(w) V(w + kD_AD_B) = ∫ \overline{\hat U}\hat V e(−θkD_AD_B) dθ gives the multiplier M(θ).
- **Minor arcs.**
  - Collapse to ρ(n) ≤ L^κ/n using (4.3); then Σ|bρ|² ≤ L^κ/U0.
  - Lemma 4.2 gives |M|² ≪ L^{O(1)}(1/V + 1/r′ + log(2r′)/U + r′log(2r′)/(UV)).
  - With L^{C′} < r′ ≤ H′/L^{C′} and UV ≍ H′, this is ≪ L^{O(1)+1−C′}.
  - If instead r′ ≤ L^{C′}, the reduced denominator is at most |k|r′ ≤ L^{C+C′} and the width is at most L^{C′}/(r′H′), so θ ∈ 𝔐 once C_arc ≥ C + C′.
- **Lemma 4.2.** I verified its proof line by line, including the 1/(2r) separation inside each block of h.
- **Major arcs.** These follow from Cauchy–Schwarz with (5.10), at most L^{2C_arc} arcs, and arc width L^{C_arc}/H′ = 1/H.

## C. Objections

1. **Cross-reference labels (COSMETIC).**
   - Location: §5.2 p.37 and §5.3 pp.38–39.
   - Quotes: "Consequently Theorem 3.11 and Theorem 4.1 bound the entire residual pairing"; "obey the same conclusion by Theorem 3.4"; "To verify the coefficient hypothesis of Theorem 4.2"; "Expand a comparison coefficient from Theorem 4.3".
   - Problem: these objects are Corollary 3.11, Lemma 3.4, Lemma 4.2 and Lemma 4.3 (probably a shared LaTeX counter). The same pattern appears in §3–4 ("Theorem 3.6", "Theorem 3.8", "Theorem 3.7").
   - Fix: relabel. There is no mathematical content.

2. **The ideal frequency range C4 is never tied to C and C7 by an inequality (UNCLEAR; exposition only, the statement is true).**
   - Location: §5.2 p.37.
   - Quote: "The required ideal frequency is ζ = −a1 − a2 − v. Consequently Theorem 3.11 and Theorem 4.1 bound the entire residual pairing by L^{−D1}". §5.8 adds only: "the fixed Mellin cutoff fixes the ideal frequency range."
   - Problem: Theorem 4.1 gives (4.1) only for |ζ| ≤ L^{C4}, and C4 is an INPUT to Theorem 4.1, so it feeds m, C1 and the kernel precision h* in (4.20). The text never writes C4 > max(C, C7) + 1.
   - Why it is still true: C7 depends only on the derivative exponent C of Ψ (C7 = C + 1 works, see Section B), and C is fixed in Theorem 5.1's hypotheses before anything else.
   - Fix: add "choose C4 > max(C, C7) + 1" before invoking Theorem 4.1.
   - Note for the global-order seat: through C7 and C4, the comparison family (m, C1, J) depends on the Ψ derivative exponent C. Any application, such as §6.6, must fix that C before Theorem 5.1 is invoked. Whether §6 does so is outside this seat.

3. **"Exactly" (COSMETIC).**
   - Location: p.38, after (5.7).
   - Quote: "The raw pattern has DC = 1 and tg = ℓ, so it is exactly the sum in Equation (5.5)."
   - What is true: (5.7) at D_C = 1, t = ℓ is literally (5.5), as verified above. The raw lifted pairing equals (5.7) only up to the shared-overlap error O(L^{O_J(1)}e^{−L^a}). The text does say so two sentences earlier ("up to errors smaller than every fixed negative log power").
   - Fix: none needed.

4. **The size of D2 relative to the comparison mass is not written (COSMETIC).**
   - Location: p.38.
   - Quote: "We claim that, for any fixed desired saving D2, it is O(L^{−D2}) outside 𝔐".
   - Problem: D2 (and likewise A) must exceed D0 + Γ + C8. Here Γ is the total pattern, cell and character cost from Section B, which depends on C1 and the §4 kernel precisions.
   - Why it is fine: §5.8 orders the choices correctly ("All pattern, cell, and absolute norm costs are now determined. Choose the separation accuracies, arc exponent, local energy target…").
   - Fix: state the inequality.

5. **Dyad count (COSMETIC).**
   - Location: p.36.
   - Quote: "A partition into at most O(L) dyads n ≍ X therefore suffices".
   - What is true: the count is O_J(TL^d). That is at most L for x ≥ x0(J), which is allowed because thresholds may depend on J. The cost L enters E, which is chosen before J, but as the J-free bound L, so this is harmless.

6. **"Coefficient hypothesis" (COSMETIC).**
   - Location: p.39.
   - Quote: "To verify the coefficient hypothesis of Theorem 4.2, collapse a free product of size U0 to integer weights ρ(n)."
   - What is true: Lemma 4.2 has no coefficient hypothesis beyond support in intervals of length O(U) and O(V). What is actually needed is the ℓ² size Σ|bρ|² ≪ L^{O(1)}/U0, and the paper proves it correctly.

7. **The proof uses less about G0 than the statement assumes (OBSERVATION, not an error).**
   - The proof in §5.2–5.3 uses only two properties of the second endpoint: (i) invariance under multiplication by P-integers (G0(D_R w′) = G0(w′)), and (ii) |G0(n)| ≤ L^{O(1)}τ(n_*)² (for ‖g‖ and (5.10)).
   - Corollary 3.11 even allows g to depend on the marks ("Only the first endpoint must be independent of its mark list").
   - So, if §3–4 and (5.11) are right, §5 proves the stronger statement: G0 may be ANY P-invariant, divisor-bounded function. (5.3)'s structure (α′, the rough p′, c′) is never used at the second endpoint.
   - This is the shape of Tao's logarithmic two-point Elliott theorem, where the second function needs only dilation-invariance, so it is not suspicious in itself. The claimed saving, however, is an arbitrary log power L^{−D0}. For comparison, Pilatte (arXiv:2310.19357, Thm 1.1) proves only a fixed power-of-log saving for λ(n)λ(n+1), and writes: "It appears that saving a fixed power of the logarithm is the best that is achievable with current techniques. Ultimately, our proof relies on the work of Matomäki and Radziwiłł … The exploitation of multiplicativity using an idea of Tao … also separately appears to limit our saving to a small power of log x."
   - The paper sidesteps both limits by hypothesis and design: (5.4) is ASSUMED at arbitrary strength L^{−B}, and the weights W_ℓ force ℓ marked primes in each of ≍ T groups.
   - Within my scope, the arbitrary saving enters only through two places: E (via J, in Theorem 3.5) and E_id (via θ_m^{c0T/6} in (4.24)).
   - Consequence: every bit of the claim's depth sits in §3 (the transference loss across N ≍ L^{0.52} edges) and §4 (the Efron–Stein/symmetry kernel). Nothing in §5.1–5.3 adds strength or hides a loss.
   - I tried to build counterexamples to Theorem 5.1 inside its hypotheses:
     - F0 = ψ(n_*)-type with ψ of conductor above L^B. Killed by Siegel–Walfisz averaging of ψ over the ℓ marked group primes in W_ℓ. My first heuristic, which forgot the marks, wrongly suggested a fixed-power obstruction.
     - Archimedean twists α_m = m^{iU} with U > L^B (these do satisfy (5.4)). Killed by the untwisted long rough factor p; making I_p short enough to freeze p^{iU} costs density L^{−B}.
     - Single-point I_p. The correlation becomes trivially small, because of the 1/z normalization.
     I found no counterexample.

No other objections. The hedge words in scope are "harmless" (the conjugation remark), "it follows" (p′ | w ⇒ p′ | w′), "negligible" (the ban error) and "uniformly" (in (5.2)). Each was checked and each holds.

## D. Citation table for §5.1–5.3

§5.1–5.3 cite NO external results; all references are internal.

| Cited | What §5 uses | What it says | Status |
|---|---|---|---|
| Cor 3.11 (called "Theorem 3.11") | f mark-independent, supported on [X,2X), sup ≤ exp(O(√L)), ‖f‖,‖g‖ ≤ X^{1/2}L^{C3} ⇒ \|⟨f,Ag⟩\| ≪ XL^{−E+2C3} | the same (p.26); also checked the Hölder bookkeeping (exponents 2, 2R/(R−1), 2R) giving XL^{2C3−C3/R−E} | MATCH |
| Thm 3.5 | (3.6) for the given ζ; J large; uniform in ζ given (3.6); I=[X,2X), x^γ ≤ X ≤ x^{1/γ} | the same (p.12) | MATCH (proof not verified by me) |
| Thm 4.1 | (4.1) for sup over Θ and \|ζ\| ≤ L^{C4}; family independent of Θ and ζ; raw K_0 = 1; comparison coefficients (4.2) use only D_A, D_B, X_A, X_B | the same (p.27) | MATCH (proof not verified by me) |
| Lemma 3.4 (called "Theorem 3.4") | absolute row and column sums ≤ L^{C_abs}, C_abs independent of J | the same (p.12) | MATCH |
| Lemma 4.2 (called "Theorem 4.2") and (4.6) | bilinear bound with α = u/r + β, \|β\| ≤ r^{−2} | the same; proof verified | MATCH |
| Lemma 4.3 / (4.7) | kernel = Σ over cells and characters of (1/ν)·1_{cell}(D)1_{cell}(X)·χ(D)χ̄(X) | the same (p.29) | MATCH |
| (4.3) | ρ_Λ(n) ≤ L^κ/n | the same | MATCH |
| Thm 2.5 (divisor moments) | Σ_{n≤Y} τ(n)^k ≪ Y(log 2Y)^{C_k} | the same | MATCH |
| Pilatte 2310.19357 (only for context in Obj. 7) | — | Thm 1.1 quoted above, from refs/Pilatte/paper.txt | context only |

## E. Parameter-dependency table for §5.1–5.3

| Constant | Fixed where | Depends on | Used where | Claimed independent of |
|---|---|---|---|---|
| a,b,c,d,c0,C0,v±,q,ℓ | Def 3.1 / §5 preamble; first | — | everywhere | — |
| τ, η, C, c_Ψ, C_Ψ, D0 | Thm 5.1 hypotheses; first | supplied by the application | everywhere | — |
| C(t_max) in (5.2) | (5.2) | q, v_−, C0, t_max (= ℓ + m_probe for comparisons) | (5.10), exclusion errors | J ✔ |
| C5 | divisor moment Στ⁴ | absolute | C6, C8 | J ✔ |
| C6 = 2C + C5/2 + O(1) | §5.2 p.36 | C | C3 in Cor 3.11, hence E | J and m_probe ✔ (verified) |
| exp(O(√L)) sup bound | §5.2 | C (absolute O) | Cor 3.11 | J ✔ |
| C7 (Mellin cutoff) | §5.2 p.36 | C (C7 = C+1 suffices) | C4, tails | the tail accuracy j ✔ (verified) |
| c_Φ (∫\|\hat Φ\| ≤ L^{c_Φ}) | §5.2 | C | E | J ✔ |
| C4 | implicit (Obj. 2) | C, C7; needs C4 > max(C,C7) | input to Thm 4.1 | — (never stated) |
| D1 | §5.2 | D0 (D1 ≥ D0) | E | — |
| E (transfer target) | §5.2 "first" | D1, C3 ≈ C6, c_Φ, dyad cost L | Thm 3.5 | J, m_probe ✔ |
| E_id | Thm 3.5 / (3.37) | E, C_v, C_s | Thm 4.1 | m, C1, J (claimed in §3; not verified here) |
| m_probe, J0, C1, q*, s*, h*, x*, D*, A0 | Thm 4.1 / (4.20) | E_id, C4, ℓ, group data | §5.3 costs Γ | J ✔ |
| J | after Thm 4.1 | J0, m, C1, E (Thm 3.5's lower bound) | the lift only (absent from (5.5)) | — |
| C_abs | Lemma 3.4 | m, C1, group data | Fourier tails | J (claimed in §3) |
| j (integrations by parts) | after C_abs | C_abs, C, D1 | tails | — |
| Γ (total comparison cost) | §5.3 | C1, N_A N_B Q⁴ ξ^{−2}, c_Φ | D2, A | J ✔ |
| C8 | (5.10) | C, C5, ℓ, m_probe, q, v_− | minor and major arcs | J ✔ |
| κ (ρ exponent) | (4.3) | m_probe, C0, v_− | C′ | J ✔ |
| D2 | §5.3 | D0, Γ, C8 | C′ | — |
| C′ | §5.3 | D2, κ | C_arc | — |
| C_arc | §5.3 | C′, C (\|k\| ≤ L^C) | H, arc count, A | — |
| H = H′/L^{C_arc} | §5.3 | C_arc and the cell | (5.11) | — |
| A (local energy target) | §5.3 | D0, Γ, C8, C_arc | §5.4–5.8 (A_s, B0, then B) | — |
| B | §5.8, last | all of the above | (5.4) | — |

I found no cycle. The only J-independence that is actually needed is C6, because E precedes J, and it holds. All later choices (D2, C′, C_arc, A, B) may depend on J and on m, and they come after both.

## F. What I verified line by line vs what I only skimmed

**Verified line by line:**
- (5.1)–(5.2), including the uniform supremum of q^{y−t}(y)_t/V^t.
- The form of (5.3): m, p and r are P-free because exp(L^d) < W; F0 depends only on n_*.
- (5.4): which characters (including principal and imprimitive), which intervals (I ⊂ [1,x²]), which u (|u| ≤ L^B).
- The statement of Theorem 5.1 and the conjugation remark: \bar F0 is again of form (5.3), and \bar α satisfies (5.4) with (χ̄, −u).
- §5.2 in full:
  - the insertion of Ψ/n and D^{−i(a1+a2)};
  - the Fourier inversion and its sign convention;
  - ζ = −a1 − a2 − v;
  - absorbing X/n and (n/Z)^{−iv} into f;
  - the dyads, and the restriction of g to positions [X/2, 4X];
  - the endpoint norm and C6's independence of J and m_probe;
  - sup|F0|;
  - the order "transfer target, then family, then J";
  - Fourier tails via Lemma 3.4, with C7 fixed;
  - the per-pattern lift: D = D_R D_C, n = D_R w, the normalization identity, the conversion of 1/D_R into draws, the damping identity and the exact overlap identity, the phase identity, Ψ(w/(ZD_C)), the shared-overlap error, the ban error, and (5.7).
- The raw case equals (5.5), by hand (Section A) and numerically (raw J=1, raw J=2, and a comparison pattern, each with mutation controls).
- §5.3 in full:
  - expansion into cells and characters, and separation;
  - H′ and (5.8);
  - the cutoffs, (5.9) and (5.10);
  - M(θ) and the Parseval identity;
  - minor arcs: ρ, the ℓ² bound, Q_D, Dirichlet approximation, the case r′ ≤ L^{C′} landing on 𝔐, and the bound from Lemma 4.2;
  - major arcs: H, the arc count, and the order of choosing A.
- The proof of Lemma 4.2, and the algebra of (4.6).
- The bookkeeping in the final step of Corollary 3.11 (Hölder exponents and powers of L).

**Read but not verified (outside my scope; my verdict is conditional on these):**
- The proof of Theorem 3.5. That includes (3.37), the constants C_v, C_s, C_a, the claimed independence of C_v and C_s from m, C1 and J, and the loss across N edges.
- The proof of Lemma 3.10.
- The proof of Theorem 4.1, including (4.20)–(4.26) and the θ_m mechanism.
- The proof of (5.11) in §5.4–5.8.

## G. Verdict

**§5.1–5.3: HOLDS AS READ, conditional on Theorem 3.5 / Corollary 3.11, Theorem 4.1, and (5.11).**

The lift is exact. The physical pairing with the inserted Ψ(n/(ZD))/n and D^{−i(a1+a2)} lies inside Definition 3.3's multiplier class once Ψ is Fourier-expanded. The raw pattern equals (5.5) up to O(L^{O_J(1)}e^{−L^a}). Each comparison pattern is bounded individually by the circle method, with costs that do not depend on J. The parameter order is non-circular, provided C4 > max(C, C7) is added explicitly (Objection 2).

The weight of the theorem, an arbitrary log-power saving against an arbitrary P-invariant second endpoint, rests entirely on §3, §4 and (5.11) (Objection 7).
