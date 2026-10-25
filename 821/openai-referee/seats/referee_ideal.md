# Referee report — seat `ideal` — Section 4 (PDF pp. 27–34): "Small ideal kernels at every frequency"

Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers", 24 Sept 2026 (family 011).
Scope: Theorem 4.1, §4.1 (4.3)–(4.6) + Lemma 4.2, §4.2 (4.7)–(4.11), §4.3 Lemma 4.3 (4.12)–(4.20), §4.4 proof of Theorem 4.1 (4.21)–(4.26), and the §3/§4 interface (Definition 3.2, Lemma 3.10) and the §4/§5 interface (§5.2–5.3 first paragraph).
All formulas were read from the rendered PDF (pp. 10–12, 21–39), not from the text extraction.

**Bottom line for this seat: I could not refute §4. Every displayed estimate and identity in §4 checks out on a line-by-line reading. I verified the sign and vanishing bookkeeping of §4.4 by an exact toy computation, and the combinatorics of (4.22)–(4.24) and (4.26) numerically. The objections below are all COSMETIC or UNCLEAR (exposition), with one statement-drafting point (Objection 1) that matters only if a downstream user cites the first paragraph of Theorem 4.1 without its "More precisely" clause. §5 does not do that.**

---

## 0. The single most important question: matching the comparison term to R(F_S, H_{T'}), written out

**Setting (explicit instance).** One big group per block: B_1 = {g1}, B_2 = {g2}. Take m = 2 probes per group (slots 1, 2), J = 3, ℓ = 1, M = 4. This is only for display. The argument does not use M ≥ (m+ℓ)(m+ℓ−1) except in (4.23). So
I_1 = {(g1,1),(g1,2)}, I_2 = {(g2,1),(g2,2)}.
Choose S = {(g1,1)}, so U = I_1∖S = {(g1,2)}. Choose T' = {(g2,2)}, so V = {(g2,1)}. Take A = {(g1,2)} ⊆ U and B = {(g2,1)} ⊆ V.

**Who is "input".** In ⟨F, T_ν H⟩ (Def. 3.2: "a row operator integrates a function at the target and returns a function at the source"), F is evaluated at the source x and H at the target y. Section 4 calls F the "input test" (p. 27: "decomposes the input test in the first-block probes and the target test in the second-block probes"; p. 33: "annihilates the mean-zero input component" = F_S). So **input = source = the F side**. The toy check below shows that this is the only reading under which the identity holds.

**The comparison pattern ν_{A,B}** has C_{g1} = {2} and C_{g2} = {1}. Shared slots: (g1,1), (g1,3), (g2,2), (g2,3), with y = x there. Fresh target labels: y_{1,2}, y_{2,1}, y_{1,4}, y_{2,4}. Fresh auxiliary labels: d_1 ~ μ_{g1} for slot (g1,2) and d_2 ~ μ_{g2} for slot (g2,1). So
D_𝓑 = C·D_A·D_B, with C = x_{1,1}x_{1,3}x_{2,2}x_{2,3}, D_A = d_1, D_B = d_2,
X_A = y_{1,2} (TARGET label in A), X_B = x_{2,1} (SOURCE/"input" label in B), and K_ν = −(−1)^{1+1} K_A(d_1, y_{1,2}) K_B(d_2, x_{2,1}) = −K_A K_B.

Pairing against (F_S, H_{T'}), after averaging the last ℓ slots (x_{·,4} and y_{·,4} occur only in F and H, so F → F', H → H'):

E[ conj F_S(x_{11},x_{12},x_{13},x_{21},x_{22},x_{23}) · (−K_A(d_1,y_{12}) K_B(d_2,x_{21})) · C^{iζ}(d_1d_2)^{iζ} e(ΘC d_1 d_2) · H_{T'}(x_{11},y_{12},x_{13},y_{21},x_{22},x_{23}) ].

- **Source label x_{12}** (coordinate in A): it appears only in F_S, and F_S is independent of it because (g1,2) ∈ U. It integrates to the factor 1. Had (g1,2) been in S, then E_{(g1,2)} F_S = 0 and the term would vanish. This is the paper's "A ⊆ U" condition.
- **Target label y_{21}** (coordinate in B): it appears only in H_{T'}, and H_{T'} is independent of it because (g2,1) ∈ V. It integrates to 1. Had it been in T', the term would vanish. This is "B ⊆ V".
- **Conditioning.** Condition on the shared labels outside A∪B, (x_{11}, x_{13}, x_{22}, x_{23}) = c, whose product is C.
  - F_S (evaluated at the source x) is independent of x_{12}, and it may depend on the block-2 coordinate x_{21}.
  - H_{T'} (evaluated at the target y) is independent of y_{21}, and it may depend on the block-1 coordinate y_{12}.
  - Put f(t) := F_S(c; x_{21}=t), a test on the B-tuple, and g(s) := H_{T'}(c; y_{12}=s), a test on the A-tuple. The conditioned comparison term is

  comp = −C^{iζ} · E[ conj f(X_B) g(X_A) K_A(D_A,X_A) K_B(D_B,X_B) (D_AD_B)^{iζ} e(α D_AD_B) ],  with α = ΘC, X_A := y_{12}, X_B := x_{21}.

- **The raw pattern** (all J shared, D_𝓑 = x_{11}x_{12}x_{13}x_{21}x_{22}x_{23} = C·x_{12}·x_{21}), under the same conditioning:

  R(F_S,H_{T'})|_c = C^{iζ} · E[ conj f(x_{21}) g(x_{12}) (x_{12}x_{21})^{iζ} e(α x_{12}x_{21}) ],

  since F_S|_c = f(x_{21}) (independent of x_{12}) and H_{T'}|_c = g(x_{12}) (independent of x_{21}).

- The two bracketed expectations are exactly the two terms of (4.12), with the same f and g, independent product tuples for X_A, X_B, D_A, D_B, and α = ΘC. Lemma 4.3 is uniform in α ∈ ℝ, and |C^{iζ}| = 1, so comp = −(R|_c + err_c) with |err_c| ≤ L^{−A_0}‖f‖‖g‖. Averaging over c and applying Cauchy–Schwarz gives (4.25) with ‖F_S‖‖H_{T'}‖ (E_c‖f‖² = ‖F_S‖², E_c‖g‖² = ‖H_{T'}‖²).
- **Signs.** For general nonempty U, V,
  Σ_{∅≠A⊆U, ∅≠B⊆V} −(−1)^{|A|+|B|} (R + err_{A,B}) = −R·(Σ_{∅≠A⊆U}(−1)^{|A|})·(Σ_{∅≠B⊆V}(−1)^{|B|}) + E = −R·(−1)(−1) + E = −R + E,
  so raw + Σ comparisons = E (the errors) for this component pair. If U = ∅ or V = ∅, no comparison term survives, and the leftover raw pieces sum exactly to Σ_{T'} R(F_{I_1},H_{T'}) + Σ_{S≠I_1} R(F_S,H_{I_2}) = R(F_full,H') + R(F'−F_full,H_full). **The bookkeeping collapses to exactly the exceptional pairs. Confirmed.**

**Exact toy verification** (`/tmp/oaimath/011/scripts_ideal/toy_cancel.py`, run with `nice -n 19 python3 -I`).
- Five coordinates: block-1 probes {0,1}, block-2 probes {2,3}, one non-probe shared coordinate {4}. Alphabet of size 3 with law (.5,.3,.2). Random complex F, H and a random unimodular multiplier Φ (an arbitrary function of the whole tuple).
- Lemma 4.3 is replaced by an EXACT reproducing (delta) kernel. The comparison multiplier is then Φ evaluated with the A-coordinates taken from {target or source} and the B-coordinates from {target or source}.
- Tested identity: raw + Σ_{A,B≠∅} −(−1)^{|A|+|B|} comp_{A,B} = R(F_full,H) + R(F−F_full,H_full).

Output, verbatim:
```
mode A-from-target B-from-source : total=(-0.09067+0.022329j)  exceptional=(-0.09067+0.022329j)  |diff|=2.055e-16
mode A-from-source B-from-target : total=(-0.039361+0.008514j)  exceptional=(-0.09067+0.022329j)  |diff|=5.314e-02
mode A-from-target B-from-target : total=(-0.090043+0.041153j)  exceptional=(-0.09067+0.022329j)  |diff|=1.884e-02
mode A-from-source B-from-source : total=(-0.062045-0.016546j)  exceptional=(-0.09067+0.022329j)  |diff|=4.828e-02
```
The identity holds to machine precision exactly for the paper's assignment: A labels from the TARGET, B labels from the SOURCE (= "input" = F side). It fails for the other three assignments. This confirms both the vanishing argument and that the asymmetry in (4.2) is load-bearing.

---

## 1. Objections

**Objection 1 — Theorem 4.1, first paragraph, is vacuous without its "More precisely" clause. Severity: UNCLEAR (statement drafting). Exposition only.**
- Location: p. 27, Theorem 4.1.
- Quote: "there is a family consisting of the raw pattern C_g = ∅ for every g, K_0 = 1, and signed comparison patterns satisfying C_g = ∅ (g ∈ S), |C_g| ≤ m (g ∈ B), Σ_ν sup|K_ν| ≤ L^{C_1}, such that the symmetrized ideal operator of Section 3 satisfies sup_{Θ∈ℝ, |ζ|≤L^{C_4}} ‖T(Θ)‖_{2→2} ≤ L^{−E_id}".
- What is wrong: "|C_g| ≤ m" admits C_g = ∅ for all g. The single comparison pattern "raw with coefficient −1" is therefore admissible and gives T(Θ) ≡ 0. As a standalone statement, the first paragraph has no content.
- Where the content lives: "Each comparison frees nonempty sets A and B of designated probes in the respective blocks, and its coefficient has the form (4.2)". This is what the proof delivers (A ⊆ I_1 and B ⊆ I_2 are both nonempty).
- Downstream: §5.3 (p. 39) uses the precise form: "Both free products are nonempty and each contains a big prime, so both sizes exceed every fixed power of L." So no mathematical gap results.
- Fix: put "A ≠ ∅ ≠ B" into the displayed hypotheses of the theorem.

**Objection 2 — "input" means source, contrary to the paper's own operator convention. Severity: COSMETIC, but the reading is load-bearing.**
- Location: p. 27 (4.2) and p. 33.
- Quotes: "X_A is the product of the target labels in A, and X_B the product of the input labels in B" and "its A labels come from the target, and its B labels from the input". Compare §3, p. 11: "a row operator integrates a function at the target and returns a function at the source". Under that convention the operator's input function lives at the target.
- What is wrong: in §4, "input" consistently means the source/F side ("decomposes the input test in the first-block probes"; "annihilates the mean-zero input component" = F_S). If "input" were read as the target, X_A and X_B would both be target labels. The vanishing for B∩T' then fails, and so does the cancellation: the toy's "A-from-target B-from-target" row has |diff| = 1.9e−2.
- §5.3 reads the factors as sitting "on specified big unshared marks at the two endpoints", which is consistent with the correct (source/target) reading.
- Fix: write "source" instead of "input".

**Objection 3 — Wrong cross-reference labels. Severity: COSMETIC.**
- Location: p. 34, "Theorem 4.3 therefore matches the comparison term before its sign to R(F_S,H_{T'})". Lemma 4.3 is meant.
- Same mislabel outside scope: p. 38 "a comparison coefficient from Theorem 4.3"; p. 39 "The normalized bilinear bound of Theorem 4.2" (Lemma 4.2 is meant).

**Objection 4 — "Choose D_* so that the displayed error is at most 1". Severity: COSMETIC.**
- Location: p. 32, after (4.18).
- What is actually needed: the reproduction is applied on both sides. With ε := O_{D_*}(Q²ξ^{−1}L^{−D_*}), the identity (ψ(X_A)+ε_A)(ψ(X_B)+ε_B) − ψ(X_AX_B) is bounded by 2ε + ε² ≤ 3ε once ε ≤ 1. Multiplying by Σ|c_ψ| ≤ √Q gives (4.19), O(Q^{5/2}ξ^{−1}L^{−D_*}). So "at most 1" is only used to linearise the product of two errors.
- Any D_* > 2q_* + x_* gives ε → 0, hence ε ≤ 1 for large x. The binding requirement is the last line of (4.20), D_* > B_0 + x_* + (5/2)q_* + 10, which implies this.
- The sentence is correct but redundant; it reads as if D_* were chosen twice.

**Objection 5 — Notation collisions inside one proof. Severity: COSMETIC.**
- D_𝓑 (calligraphic: the product over all big groups, in (4.21) and Def. 3.2) sits beside D_B (the free product on probe set B, in (4.2)) in the same paragraph of §4.4. They are distinguished only by font.
- S is used for the Dirichlet parameter (S = L^{s_*}), for the component index S ⊆ I_1, and for the small-group set 𝒮.
- D_* (§4.2–4.3 character accuracy) collides with D_* in (6.1). B_0 (Lemma 4.3 dyadic exponent) collides with B_0 in Lemma 5.4.
- None of these changes the mathematics as read from the rendered PDF.

**Objection 6 — (4.8): the implied constant also depends on C_0. Severity: COSMETIC.**
- Quote: "N_Λ ≪_m 1 + TL^d/h".
- log D ≤ (#labels)·L^d ≤ mC_0T·L^d, so the constant also depends on C_0. C_0 is fixed data; this is harmless, and (4.20)'s "N_A, N_B ≤ L^{d+1+h_*} for large x" holds.

**No FATAL and no GAP found in §4.**

---

## 2. Line-by-line checks (what was verified and how)

### Theorem 4.1 statement and the §4 interval assumption
- Assumption (p. 27): "each big group P_g … is the set of primes in an interval contained in [exp(L^c), exp(L^d)]". It is used only in (4.9).
- It is satisfied by §7.1 (p. 53): "take the primes in that interval of logarithms [c_3 s_j, c_4 s_j] as a … big P-group", with [c_3 s_j, c_4 s_j] ⊂ [L^{3/10}, L^{2/5}], so c = 3/10 and d = 2/5. Primes with log p in an interval form an interval of primes. ✓
- Independence claims, checked:
  - kernels independent of Θ, α, ζ: Lemma 4.3 constructs them before α appears ✓
  - all §4 constants independent of J: see the parameter table ✓
  - the threshold for x does not actually need J at all ✓
- ζ-range |ζ| ≤ L^{C_4} is used only in M′ (the r ≤ Q case); the r > Q case is uniform in ζ ✓.

### §4.1
- **(4.3).** P(P_Λ = n) = Π_g [k_g!/Π_p a_p!]·V_g^{−k_g}·Π_p p^{−a_p}, which is exactly (1/n)Π_g k_g!/(V_g^{k_g}Π a_p!). Each group factor is ≤ m!·max(1, v_−^{−1})^m, and there are ≤ C_0T groups, so the product is ≤ exp(C_0T(log m! + m log max(1, v_−^{−1}))) = L^κ. κ is independent of J ✓.
- **(4.4).** |a_n|² ≤ ρ_Λ(n)·E[|f|² 1_{P_Λ=n}] by Cauchy–Schwarz on the fiber; sum over n ≥ c_1U ✓.
- **Lemma 4.2.**
  - Cauchy–Schwarz in n, then the geometric sum ≤ min(CU, ‖αh‖^{−1}) ✓.
  - For r ≥ 2: blocks of diameter ≤ r/2, of which there are O(1+V/r). For 0 < |h−h′| ≤ r/2 < r, ‖u(h−h′)/r‖ ≥ 1/r and |β(h−h′)| ≤ (r/2)/r² = 1/(2r), so the phases are 1/(2r)-separated ✓. ≤ r points per block contribute O(U + r log 2r) ✓.
  - r = 1: the trivial bound (CU·CV)^{1/2}‖a‖‖b‖ is ≤ the right side ✓.
  - "At a zero denominator the minimum is interpreted as U" ✓.
- **(4.6).** L^{κ/2}U^{−1/2} · L^{κ/2}V^{−1/2} · [U + (1+V/r)(U + r log 2r)]^{1/2} = L^κ(2/V + 1/r + log(2r)/U + r log(2r)/(UV))^{1/2} ✓. The ζ-twist separates ✓.

### §4.2
- **(4.7)–(4.8).** #C_Q ≤ Σ_{q≤Q} φ(q) ≤ Q². A fixed (D, X) lies in at most one cell. sup|K| ≤ Q²ξ^{−1}. sup_X E_D|K| ≤ (ν_j/ν_j)·Q² ✓.
- **(4.9).** Fix all labels but one, p ∈ P_g. The cell condition is p ∈ [e^{jh}/D′, e^{(j+1)h}/D′). Intersected with the interval P_g, this is an interval of primes inside [exp(L^c), exp(L^d)] ✓.
  - ρ = χ̄χ′ is nonprincipal mod lcm ≤ Q² (otherwise χ and χ′ induce the same primitive character) ✓.
  - Theorem 2.2 is applied over reduced classes mod r′ ≤ Q² ≤ (log t)^{2q_*/c} for t ≥ exp(L^c), with accuracy K + 2q_*/c. The main terms cancel because Σ_a ρ(a) = 0 ✓.
  - Partial summation gives O_K((log y)^{1−K}) = O(L^{c(1−K)}); divide by V_g ≥ v_− and average the rest ✓.
  - Uniform in j, in the slot set, and in the interval ✓.
- **(4.10)–(4.11).** On a retained cell, (Tg)(D) = Σ_χ χ̄(D)·E[χ(X)g(X) | cell]. This is the frame operator VV* of {χ̄}, so ‖T_j‖ = ‖V*V‖ = ‖Gram‖.
  - Diagonal = 1 because every prime exceeds exp(L^c) > Q².
  - Off-diagonal ≪ ξ^{−1}L^{−D_*}, so ‖Gram − I‖ ≤ Q²ξ^{−1}L^{−D_*} ≤ 1.
  - ‖T_j g‖² ≤ 4 E[|g|² 1_{cell}]; cells are disjoint, so ‖T‖ ≤ 2 ✓.
  - "Neither a cell-count factor nor a factor ξ^{−1} is lost": correct. The 1/ν_j is exactly the conditional normalisation.

### §4.3, Lemma 4.3
- **Dyadic split.** Bilinear and exact. There are ≤ L^{d+1} dyads per product since log of the max ≤ mC_0TL^d. Crude summation gives L^{2(d+1)−B_0}‖f‖‖g‖ ✓.
- **(4.13).** Dirichlet with Q′ = ⌊Z/S⌋: |β| ≤ 1/(rQ′) ≤ r^{−2}, and |β|Z ≤ Z/(r⌊Z/S⌋) ≤ 2S/r. Reducing the fraction keeps these bounds ✓.
- **r > Q, raw term.** (4.6) with 1/V, log(2r)/U ≤ L^{d+1}e^{−L^c}; 1/r < Q^{−1}; r log(2r)/(UV) ≤ L^{d+1}/S. This gives (4.14) ✓.
- **r > Q, comparison term.** g̃(D_A) = E_X[K_A(D_A,X)g(X)] and f̃(D_B) = E_X[K_B(D_B,X)f̄(X)] have norm ≤ 2 each by (4.11). Their supports are within a factor e^{±h} of the dyads, i.e. inside [U/2, 4U] and [V/2, 4V]. (4.4) applies with c_1 = 1/2, and r ≤ Z/S survives up to constants ✓.
- **r ≤ Q.**
  - (4.15): characters of (ℤ/r)^×; Parseval in normalised counting measure gives Σ|c_ψ|² = 1, and Cauchy–Schwarz gives Σ|c_ψ| ≤ √φ(r) ≤ √Q. Primitive inducers lie in C_Q, and all products are coprime to r ✓.
  - (4.16): P(E) ≤ (N_A+N_B)ξ, and the comparison term vanishes on E. E[1_E|f g|] ≤ P(E)^{1/2}(E|f|²|g|²)^{1/2} = P(E)^{1/2}‖f‖‖g‖ by independence ✓. The "L² remark" is correct: this is Cauchy–Schwarz against an indicator, not an operator-norm claim.
  - M(v) = e^{iζv}e(βe^v): |M′| ≤ |ζ| + 2π|β|e^v = O(L^{C_4} + S) on the enlarged range, where e^v ≤ 16·e^{2h}Z ✓.
  - (4.17): |Δv| < 2h; E_D|K_A||K_B| ≤ Q⁴ ✓.
  - (4.18): the diagonal term is exactly ψ(X); the other ≤ Q² terms are each ≤ ξ^{−1}·O(L^{−D_*}) ✓.
  - (4.19): see Objection 4 ✓.
  - After these replacements, the comparison term on E^c equals E[f̄ g 1_{E^c} e(uX_AX_B/r)M(log X_AX_B)], which is identically the raw term on E^c ✓.
- **(4.20), line by line:**

  | Line | Controls | Check |
  |---|---|---|
  | B_0 > A_0 + 2(d+1) + 10 | dyadic sum | L^{2(d+1)−B_0} ≤ L^{−A_0−10} ✓ |
  | q_*, s_* > 2(B_0+κ+10) + d + 1 | (4.14) | L^{κ−q_*/2}, L^{κ+(d+1)/2−s_*/2} ≤ L^{−B_0−10} ✓ |
  | h_* > 4q_* + max(s_*, C_4) + B_0 + 10 | (4.17) | ≤ 2L^{−B_0−10} ✓ |
  | x_* > 2B_0 + d + 1 + h_* + 10 | √(4.16) | ≤ √2·L^{−B_0−5} ✓ |
  | D_* > B_0 + x_* + (5/2)q_* + 10 | (4.11) and (4.19) | ✓ |

  "None of these choices involves J" ✓.

### §4.4, proof of Theorem 4.1
- Symmetrisation reduction: ⟨F, PT′PH⟩ = ⟨PF, T′PH⟩ ✓.
- Last-ℓ averaging: the last ℓ slots are unshared in every pattern and unused by every coefficient. This gives contractions to F′ and H′ ✓.
- (4.21): |R| ≤ ‖F′‖‖H′‖ ✓.
- Efron–Stein components F_S and H_{T'}: orthogonal, mean zero on S (resp. T′), and independent of U (resp. V) ✓.
- **(4.22) and (4.23).**
  - In the full Hoeffding decomposition, F_full = Σ_{W ⊇ I_1, W ∩ Last = ∅} F^W. For symmetric F, ‖F^W‖ depends only on the cardinality tuple. The retained fraction is C(M−m−ℓ, j−m)/C(M,j) = (j)_m(M−j)_ℓ/(M)_{m+ℓ} (identity checked).
  - If M ≥ (m+ℓ)(m+ℓ−1), then Σ_{i<m+ℓ} i/M ≤ 1/2, so (M)_{m+ℓ} ≥ ½M^{m+ℓ}. The fraction is then ≤ 2t^m(1−t)^ℓ ≤ 2(m/(m+ℓ))^m(ℓ/(m+ℓ))^ℓ ≤ 2ℓ^ℓm^{−ℓ} = θ_m ✓.
- **(4.24) tensorisation.** Classes are (W restricted to block 2, cardinality tuple on block 1). Within-block-1 permutations act transitively on each class. The fraction is a product over the s_1 groups, and the block-2 constraint W ∩ Last = ∅ only removes whole classes. So ‖F_full‖² ≤ θ_m^{s_1}‖F‖², i.e. **‖F_full‖ ≤ θ_m^{s_1/2}‖F‖. The exponent s_1/2 is correct for the unsquared norm** ✓.
  - With s_i ≥ c_0T/3 and −(c_0/6)log θ_m > E_id + 3, this is ≤ L^{−E_id−3}. It needs ℓ ≥ 1, so that θ_m → 0 ✓.
- **Vanishing (A ⊆ U, B ⊆ V).** For i ∈ A∩S: the source label i is unshared, absent from K (K uses target-A and source-B labels only, and B ⊆ I_2 is disjoint from i ∈ I_1), and absent from D = C·D_A·D_B and from the target. By Fubini under the product measure, E_i F̄_S = 0. The case j ∈ B∩T′ is symmetric. ✓ (Section 0 and the toy.)
- **Conditioning, α = ΘC, (4.25).** Section 0 ✓. Uniformity of Lemma 4.3 in α is essential and is provided (the kernels precede α).
- **(4.26).** Σ_{∅≠A⊆U}(−1)^{|A|} = (1−1)^{|U|} − 1 = −1 for U ≠ ∅. The product is +1, and with the leading "−" the comparisons cancel the raw term ✓ (numerically checked for |U|, |V| ≤ 5).
- **Exceptional pairs.** {S = I_1} ∪ {T′ = I_2, S ≠ I_1} gives R(F_full,H′) + R(F′−F_full,H_full) exactly. These terms are summed before absolute values, giving ≤ 2L^{−E_id−3}‖F‖‖H‖ ✓.
- **3^P count and A_0.** Each probe is in S/T′, in A/B, or in U∖A / V∖B, giving 3^P triples. P = m|𝓑| ≤ mC_0T, so 3^P ≤ L^{mC_0 log 3}. A_0 > E_id + mC_0 log 3 + 10 gives ≤ L^{−E_id−10}‖F‖‖H‖ ✓.
- **C_1.** At most (2^{|I_1|}−1)(2^{|I_2|}−1) ≤ 2^P ≤ L^{mC_0 log 2} comparison patterns, each with sup|K| ≤ (Q²ξ^{−1})² = L^{4q_*+2x_*}. Adding the raw pattern, C_1 > mC_0 log 2 + 4q_* + 2x_* + 1 suffices ✓.
- **Final order.** m(E_id, c_0, ℓ) → A_0(E_id, m, C_0) → B_0, q_*, s_*, h_*, x_*, D_* (via κ(m, C_0, v_−), d, C_4) → C_1. Only afterwards J_0: J ≥ m and J+ℓ ≥ (m+ℓ)(m+ℓ−1). No cycle inside §4 ✓.

### Numeric checks run (all at nice 19, seconds each)
- `frac_check.py`: the identity (4.22) and bound (4.23) for ℓ ≤ 3, m ≤ 8, M < 60, all j. Result: 0 failures; max(fraction/θ_m) = 0.25. (4.26) equals 1 for 1 ≤ |U|, |V| ≤ 5.
- `tensor_check.py`: random symmetric F, 1–2 groups, alphabet {0,1}. ‖F_full‖²/‖F‖² = 0.122, 0.022, 0.011 against the bounds Π max frac = 0.20, 0.111, 0.040. The tensorised bound holds.
- `toy_cancel.py`: Section 0.

---

## 3. Interface questions

**Does Theorem 4.1's ideal operator include the free/active collision ban? No, and it need not.**
- Definition 3.2 (p. 11) samples the auxiliary labels "independently with the same laws", and states "repetitions of prime values are allowed". There is no ban.
- Lemma 3.10 (p. 22) obtains "T(Θ) or its adjoint, with two changes only: the measures … are μ̃_g in place of μ_g, and the free/active collision ban remains in force". It removes both changes itself, by a density perturbation O_J(L^{C_1}sN/P_*) and by the banned-transition estimate O_{J,m}(L^{C_1}s/P_*), using only Σ sup|K_ν| ≤ L^{C_1} (3.2), which Theorem 4.1 supplies.
- Birth distinctness is not a third change: it is omitted at (3.38) and restored by the equality-rank expansion of §3.8.
- So the §3 ↔ §4 interface is consistent as stated. The correctness of the two perturbation estimates belongs to the transference seat.
- The adjoint case is harmless, since ‖T*‖ = ‖T‖. The adjoint swaps which endpoint carries X_A and X_B.

**Does the raw ideal row operation match Definition 3.2 as used in §3.7? Yes.**
- Raw pattern: C_g = ∅, so all J slots are shared, t_g = ℓ unshared slots (the last ℓ) are resampled with μ_g, D_𝓑 = the product of the J shared labels per big group, and K_0 = 1.
- This is (4.21) after last-ℓ averaging, and it is the clean edge of §3.7: "drops every unshared big source slot, and fills every unshared big target slot freshly". The small-group factor and the memory have been absorbed into Θ.

**Consumer check (§5.2–5.3, read only for the interface).** §5 uses:
- "both free products are nonempty", which is supplied by the "More precisely" clause;
- the cells × characters form with polylog costs independent of J ((4.7)–(4.8)) ✓;
- coefficients using no shared labels ✓;
- |ζ| = |a_1+a_2+v| ≤ L^{C_4} with C_4 fixed before J. This is §5's responsibility; whether C_7/C_4 are chosen before J is the lift/energy seats' question.

---

## 4. Citation table (scope of §4)

| Cited result | What the paper claims | What the source says (quote) | Verdict |
|---|---|---|---|
| Efron–Stein 1981, Ann. Statist. 9(3) 586–596, §2 "Decomposition Lemma" (read: Project Euclid scan, pp. 587–588) | "orthogonal product-space decomposition of Efron and Stein [5, Section 2, Decomposition Lemma]"; components "separately mean zero in each indicated probe and independent of the other probes" (p. 33) | p. 587: "DECOMPOSITION LEMMA. The random variable S(X_1, X_2, ···, X_n) can be expressed as (2.4) S = μ + Σ_i A_i(X_i) + Σ_{i<i′} B_{ii′}(X_i,X_{i′}) + ··· + H(X_1,…,X_n), where all 2^n − 1 random variables on the right side of (2.5) have mean zero and are mutually uncorrelated with each other." Also p. 587: "Here we do not have to assume that the X_i are identically distributed, nor that S is symmetrically defined … The only assumption is that ES² < ∞." And p. 588, (2.7): "E{B_{ii′}(X_i,X_{i′}) \| X_i} = … = 0". | MATCH. The paper uses the partial version with probe coordinates individually and all other coordinates as parameters. This follows from the lemma (group the non-probe coordinates into one variable, or apply the ∏(1−E_i)∏E_i formula directly). The complex-valued case follows by linearity. Equal norms for symmetric S with i.i.d. coordinates is also stated there: "In this case the functions A_i(·), B_{ii′}(·,·), … do not depend upon the subscripts". |
| Theorem 2.2 ← Tao 254A Notes 2, Exercise 64 (fetched 2026-10-11 from the blog URL in [22]) | Siegel–Walfisz for π(y; r, a) with r ≤ (log y)^C, error O_{A,C}(y/(log y)^A), ineffective; "follows from its von Mangoldt formulation by partial summation" (p. 6); used in (4.9) | "Exercise 64 (Siegel-Walfisz theorem) For any A > 0, show that there exists an (ineffective) constant c_A > 0 such that Σ_{n≤x: n=a (q)} Λ(n) = x/φ(q) + O(x exp(−c_A √log x)) for all primitive residue classes a (q) and all x ≥ 2 with q ≤ log^A x. … Conclude in particular that … = x/φ(q) + O_A(x log^{−A} x) for all primitive residue classes a (q) and all x ≥ 2" | MATCH. Partial summation plus removal of prime powers gives Theorem 2.2. The (4.9) application stays inside the hypotheses: r′ = lcm ≤ Q² ≤ (log t)^{2q_*/c} for t ≥ exp(L^c). |
| Dirichlet approximation (uncited, standard) | (4.13) | standard | MATCH (bounds re-derived above) |
| Fourier analysis on (ℤ/r)^× (uncited, standard) | (4.15) | standard | MATCH |

There are no other external citations inside §4. Lemma 4.2 is proved in full in the paper and cites nothing.

---

## 5. Parameter-dependency table (§4)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Status |
|---|---|---|---|---|---|
| E_id | input (from (3.37)) | E, C_v, C_s | Thm 4.1, m, A_0 | J, m, C_1 | ✓ within §4 |
| C_4 | input (Thm 4.1 hypothesis; §5 sets it from a_1, a_2, v) | §5 constants | h_* in (4.20), M′ | J | ✓ within §4 |
| ℓ, q, c, d, c_0, C_0, v_± | fixed data (Def. 3.1; §7: ℓ = 1, c = 3/10, d = 2/5) | — | everywhere | x | ✓ |
| m (= m_probe) | (4.24): θ_m < 1, −(c_0/6)log θ_m > E_id + 3 | E_id, c_0, ℓ | κ, A_0, slot bound, 3^P, C_1, J_0 | J | ✓ |
| θ_m = 2ℓ^ℓm^{−ℓ} | (4.23) | m, ℓ | (4.24) | J, x | ✓ |
| κ | (4.3) | m, C_0, v_− | (4.4), (4.6), (4.14), (4.20) | J | ✓ |
| A_0 | §4.4: > E_id + mC_0 log 3 + 10 | E_id, m, C_0 | Lemma 4.3, (4.25) | J, Θ, ζ | ✓ |
| B_0 | (4.20) | A_0, d | per-dyad target | J | ✓ |
| q_*, s_* (Q = L^{q_*}, S = L^{s_*}) | (4.20) | B_0, κ, d | C_Q, (4.13), (4.14) | J, α, ζ | ✓ |
| h_* (h = L^{−h_*}) | (4.20) | q_*, s_*, C_4, B_0 | cells, (4.17), N_Λ | J, α | ✓ |
| x_* (ξ = L^{−x_*}) | (4.20) | B_0, d, h_* | discard threshold, (4.16), sup\|K\| | J, α | ✓ |
| D_* (character accuracy) | (4.20) | B_0, x_*, q_* | (4.9), (4.11), (4.18), (4.19); implied constant via Thm 2.2 at accuracy K(D_*, c) + 2q_*/c | J; does not affect the kernels | ✓ |
| C_1 | §4.4: > mC_0 log 2 + 4q_* + 2x_* + 1 | m, C_0, q_*, x_* (hence E_id, C_4, v_−, d) | (3.2) → Thm 3.5's J threshold | J | ✓ |
| J_0 | §4.4 | m, ℓ: J ≥ m, J+ℓ ≥ (m+ℓ)(m+ℓ−1) | Thm 4.1 | — | ✓ (chosen last) |
| s_1, s_2 | §4.4 | \|𝓑\| (x-dependent) | ≥ c_0T/3 | — | ✓ |
| P = m\|𝓑\| | §4.4 | m, x | 3^P, 2^P | — | ≤ mC_0T ✓ |
| N_Λ | (4.8) | m, C_0, h, x | (4.16) | J | ≤ L^{d+1+h_*} ✓ |
| x threshold | — | all of the above | — | stated "may depend on J"; actually does not | ✓ |

No cycle exists inside §4. The only cross-section dependencies are:
- C_4 must be fixed before J (§5).
- C_v and C_s must be independent of m and C_1. Lemma 3.10 and (3.22) claim this; the transference seat should verify it. Otherwise E_id → m → C_1 → … → C_v would close a loop.

---

## 6. Verified line by line vs skimmed

**Verified line by line:**
- Theorem 4.1 statement.
- §4 intro and the interval assumption, plus its satisfaction in §7.1.
- (4.3), (4.4), Lemma 4.2 (all cases), (4.6).
- (4.7)–(4.11), including the proof of (4.9) through Theorem 2.2.
- Lemma 4.3 in full: dyads, (4.13), r > Q, r ≤ Q with (4.15)–(4.19), and every line of (4.20).
- §4.4 in full: block split, probes, last-ℓ averaging, (4.21), the Efron–Stein components, (4.22)–(4.24) with tensorisation, vanishing, conditioning, (4.25), (4.26), the exceptional identity, 3^P/A_0, C_1, final order.
- Definition 3.2 vs the raw pattern.
- The Efron–Stein Decomposition Lemma (source read) and Tao Ex. 64 (source read).

**Skimmed, interface only, not verified:**
- Definitions 3.1 and 3.3, Lemma 3.4, Theorem 3.5, Lemma 3.10. In particular the two perturbation estimates (μ̃ density and ban removal) and the Fourier reduction to T(Θ).
- (3.37)–(3.47).
- Corollary 3.11.
- §5.1–5.3: the ζ = −a_1−a_2−v bookkeeping, and the use of the comparison coefficients in (5.7)–(5.11).
- I did not check whether §5's per-pattern lift reproduces Definition 3.2's coefficient conventions (which endpoint carries X_A). Theorem 4.1 is only correct for the target/source assignment shown in Section 0; §5's "at the two endpoints" wording is consistent with it.

---

## 7. Verdict for scope

**HOLDS AS READ.**
- Theorem 4.1, in its precise form (comparison patterns freeing nonempty A ⊆ I_1 and B ⊆ I_2, with coefficients −(−1)^{|A|+|B|}K_A(D_A, X_A)K_B(D_B, X_B), X_A = target labels and X_B = source labels), is proved correctly. The bound is uniform in Θ ∈ ℝ and |ζ| ≤ L^{C_4}, and every constant is independent of J.
- No FATAL or GAP. Objections 1–6 are COSMETIC/UNCLEAR.
- What a §4 pass cannot certify:
  - that the operator §3 actually produces is T(Θ) up to the two perturbations Lemma 3.10 removes (transference seat);
  - that §5 bounds each comparison correlation individually, and that C_4 is fixed before J (lift/energy seats).
