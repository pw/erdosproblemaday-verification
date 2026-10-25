# Referee seat "inputs" — Appendices A–D (printed pp. 86–123), plus the LSS / KM / BS / SS external inputs

## Scope read (pages)
- PDF pp. 84–123 in full: the appendix preamble and Table 1 (pp. 84–85); A.1–A.3 (pp. 86–93: Def. A.1, Lemmas A.2–A.6, the lift to actual maps, (A.2)–(A.4), Theorem A.7 with its box and product-cyclic reductions, Lemmas A.8, A.9); B (pp. 93–100: Lemma B.1, Lemma B.2, the whole proof of B.1); C (pp. 100–114: Theorem C.1, Lemmas C.2–C.5, Prop. C.6, Lemmas C.7–C.11, Prop. C.12); D (pp. 114–123: Lemma D.1, Props. D.2, D.3, Def. D.4, Lemma D.5, Def. D.6, Prop. D.7, Remark D.8).
- Outside my scope I read only (a) the four other places where Theorem A.7 / [35] is applied (pp. 22, 38, 161, plus the §1.5 description), to check the degree and normalization bookkeeping, and (b) for the coordinator's hand-off: Prop. F.2 (p. 137), §3.4 (p. 23), Lemma 3.2 (p. 19), Lemma 4.7 (pp. 31–32), Prop. I.1 with Lemmas I.2–I.4, its proof and Remark I.5 (pp. 179–183).

## Method
I read the displayed math off the rendered PDF pages, not the pdftotext output: the extraction drops superscripts. For example M_r = M_{r−1}^{a_r}(1+ε)^{a_r} in D.1 comes out as "M_{r−1}(1+ε)^{a_r}", and κ^{1/2^q} as "κ^{1/2}". I re-derived every displayed identity and inequality in B.2, C.1 and D.1, and most of those in A, C.2–C.4 and D.2. I checked each constant-choice order for cycles. A few finite claims I also checked numerically with nice -n 19 python3 -I (/tmp/oaimath/159/seats/inputs_scratch/chk.py), all passing:
- the mixed-radix embedding Φ in Theorem A.7 lands in [L] and reflects two-face identities (200 random boxes);
- the cyclic partition pieces have diameter < N/3 and length ≥ N/8 (N ≤ 400);
- the kernels (D.3)/(D.4), B_{1/4}, and the deficit bound 1+τ/16 (exact rational arithmetic);
- Lemma C.4(2).

All four external papers were fetched as PDFs and read with pdftotext plus the rendered pages. The working notes in the appendix below record each step that was checked.

## Findings

No FATAL. No GAP.

EXPOSITION (repairable from the paper's own resources):

E1. **Constant order in Prop. C.6** (p. 104, proof lines 2–4): "Choose κ = e^{−c_cut p} and ζ = exp(−(2+p)^{C′_ε}) sufficiently small. Choose c_cut = c_cut(ϵ) first … The moment constant and the number of rounds will be chosen afterwards". On p. 105 the unbalanced alternative needs a shrink S′ whose regularity error is "small after multiplication by M^{2q}", with M = (c_0κ)^{−1} and q = 2m′ = O(c_mom p). That is a loss of exp(O(c_cut·c_mom·p²)), so ζ (whose exponent C′_ε must also make the admissible shells contain these dilates) has to be fixed after c_mom, not with κ. Nothing chosen earlier depends on ζ (c_mom = c_mom(ϵ, c_cut); B_ε is chosen after ζ), so there is no cycle. The order just needs restating.

E2. **"Regular" in Lemma C.2 versus Schoen–Sisask** (p. 101): "A regular Bohr set B of rank D ≥ 1 satisfies |B_{1+t}| = (1 + O(D|t|))|B| (|t| ≤ c/D)." [43, Thm 5.4] needs SS-regularity (Def. 4.3: 1 − 12d|δ| ≤ |B_{1+δ}|/|B| ≤ 1 + 12d|δ| for |δ| ≤ 1/12d), and outputs SS-regular sets. The paper should fix its regularity constant to SS's, or at least say that its regular sets are SS-regular. This is cosmetic, since SS Lemma 4.4 gives such dilates.

E3. **Prop. I.1 over-states its sampler hypothesis.** Hand-off item; see the section below. The hypothesis "assume Properties 1 and 2 of that proposition" should be replaced by the parts actually used.

E4. (Minor) Theorem C.1 assumes N odd. I found no step in Appendix C that uses oddness. It is harmless, and Appendix D supplies it anyway.

Points I specifically probed and found sound:
- Theorem A.7's interval-to-box and product-cyclic reductions (line by line).
- The fact that LSS's Lipschitz direction is the right one (only d_c ≤ d_R is needed).
- Lemma B.2's covolume/pivot argument.
- The z-scaling derivation of (B.7) (why Y_h(X) is linear in h, and why first-order bracket and subleading terms cancel).
- The grade-by-grade removal in B.2. The hypothesis list correctly carries [P_d, K] ⊆ V_{d+1} for every d ≤ j−2. This is needed because K ⊄ U_1 in general.
- In Prop. C.6: peeling and telescoping, error summability, the Markov/flat alternative and its smooth Bohr majorant, the dependent-random-choice (DRC) density selection Z ≥ exp(−O(p²)) feeding (C.4) with q = O(p²), and the autocorrelation maximum at 0.
- In Prop. C.12: the uniformity of exceptional sets in the lower test (used in C.7 and D.1), the translated-test family making Markov uniform over U_{h,j}, the order of factors in (C.24), branch selection, and the choice of ρ after the Lipschitz constant in (C.25).
- Lemma D.1's conditional exceptional sets and its backward budget recursion.
- Prop. D.2's sign trick. ν_i may be negative for b = 1/4, but only the squares 1 − b + buu′ ≥ 0 are bounded.

## External inputs checked

**[35] Leng–Sah–Sawhney, arXiv:2402.17994.** The current version is v3 (10 Aug 2024), which is the version the paper cites; file at refs/2402.17994/2402.17994v3.pdf. Theorem 1.2, verbatim: "Fix δ ∈ (0, 1/2). Suppose that f : [N] → C is 1-bounded and ‖f‖_{U^{s+1}[N]} ≥ δ. Then there exists a nilmanifold G/Γ of degree s, complexity at most M, and dimension at most d as well as a function F on G/Γ which is at most K-Lipschitz such that |E_{n∈[N]}[f(n)F(g(n)Γ)]| ≥ ε, where we may take d ≤ log(1/δ)^{O_s(1)} and ε^{−1}, K, M ≤ exp(log(1/δ)^{O_s(1)})."
- **Their conventions:**
  - Def. 1.1 normalizes via zero extension to Z/ÑZ with Ñ ≥ 2^{s+1}N, divided by ‖1_{[N]}‖.
  - Def. 3.4 uses a right-invariant chain metric in second-kind coordinates ψ(x_i x_{i+1}^{−1}), with ‖F‖_Lip = ‖F‖_∞ + Lip.
  - Def. 3.5: complexity means an adapted Mal'cev basis with rationality M and ψ_X(Γ) = Z^d.
- **(i) Interval vs box/product-cyclic.** The paper's interval norm (A.2) on [N] equals LSS's exactly: with Ñ ≥ (j+1)N, cyclic cubes with vertices in [N] are integer cubes. The box case embeds Q in [L] by Φ(x) = 1 + Σ a_i x_i with a_i = Π_{r<i}4T_r. Cube sums agree exactly (mixed radix with |c_i| < 4T_i). The norm loss is exp(O_j(n)) and the correlation gain is L/|Q| = 4^n. The pull-back g∘Φ is adapted. The product-cyclic case uses ≤ 4^n pieces of diameter < N_i/3, a bijection of group and integer cubes, C_j(Q) ≤ |H|^{j+1}, and a smooth selector with error O(nθ) and Lipschitz constant O(n/θ). All checked; the dimension convention n ≤ (2+p)^A is respected, with exponents depending on s, A.
- **(ii) Returned quantities.** With δ = e^{−p}: dimension ≤ p^{O(1)}, log M, log K ≤ p^{O(1)}, ε ≥ exp(−p^{O(1)}). This matches "complexity P(p), correlation B(p)^{−1}". Dividing by max(1, ‖F‖_∞) is legitimate because the LSS Lipschitz norm includes the sup norm. Conversions:
  - Metric: d_c ≤ d_R ≤ d·d_c. Only d_c ≤ d_R is needed, giving Lip_R F ≤ Lip_c F.
  - Second-kind to first-kind coordinates: polynomials of degree ≤ s with heights exp(poly p). They give lZ^d ⊆ log Γ ⊆ l^{−1}Z^d with l = (product of the two common denominators), log l = poly(p).
- **(iii) Degree bookkeeping.** At every application, U^{q} goes to degree q − 1:
  - C.12 (p. 111): U^{r+2} = U^{d+1}, giving degree d ≤ k−2;
  - p. 38: U^q, giving degree q−1;
  - p. 161: U^{r+1} on box U, giving degree r;
  - p. 22: "as in the cited detection proof".
  - Positive counting at length k uses tests of degree ≤ s = k−2 (D.2, D.3). Consistent.
- [35, Lemma B.5] (the converse, verbatim: "If f : [N] → C is a 1-bounded function such that |E f(n)F(g(n)Γ)| ≥ ε, then ‖f‖_{U^{s+1}[N]} ≥ (ε/M)^{O_s(d^{O_s(1)})}") is cited for the interval case. The paper proves its own box/cyclic version (Lemma A.9), which I checked.
- [35, Thm 5.4, Cor 5.5] are cited only as antecedents of Lemma B.1. Lemma B.1 is proved from scratch, and needs to be, since LSS Cor 5.5 is for cubes [N]^ℓ with fixed ℓ.

**[30] Kelley–Meka, arXiv:2302.05537.** Current version is v6 (28 Oct 2024), which the paper cites. §4 is "Proof of Theorem 2.8, and Sifting"; §5 is "Spectral positivity and k-norm inequalities for convolutions", containing Lemma 5.2: "‖A∗B − 1‖_k ≤ ‖A⋆A − 1‖_k^{1/2}‖B⋆B − 1‖_k^{1/2}". The paper cites them for methods only ("adapt the moment and sifting methods") and re-proves local versions: (C.12) is the physical-space analogue of KM Lemma 5.2, and (C.13) is positivity. No statement is imported, and the attribution is accurate.

**[8] Bloom–Sisask, arXiv:2302.07211.** Current version is v3 (13 May 2025), which the paper cites. §2.1 is Lemma 7 (unbalancing of spectrally non-negative functions, with Shkredov's physical proof of ⟨ν, f^k⟩ ≥ 0); §2.2 is Lemmas 8 and 10 (dependent random choice). These match the paper's unbalancing step in Lemma C.5 and its DRC step in Prop. C.6, which the paper re-proves in its local, weighted form. Attribution accurate.

**[43] Schoen–Sisask, arXiv:1408.2568.** Only v1 exists (11 Aug 2014). This is in my page range (Lemma C.2), so I checked it although the brief lists it as a separate input. Thm 5.4, verbatim core: "Let A, M, L be subsets of a finite abelian group G, and let B ⊆ G be a regular Bohr set of rank d and radius ρ. Suppose |A + S| ⩽ K|A| for a subset S ⊆ B with µ_B(S) ⩾ σ > 0, and assume η := |M|/|L| ⩽ 1. Then there is a regular Bohr set B′ ⩽ B of rank at most d + d′ and radius at least ρεη^{1/2}/d²d′, where d′ ≪ ε^{−2} log²(2/εη) log(2/η) log(2K) + log(1/σ), such that ‖1_A ∗ 1_M ∗ 1_L(· + t) − 1_A ∗ 1_M ∗ 1_L‖_∞ ⩽ ε|A||M| for all t ∈ B′."
- The paper renames SS's ε → η and SS's η → β, and then sets:
  - A = −A_2, with M = A_1, L = −K when |K| ≥ |A_1|, and M, L swapped when η|A_1| ≤ |K| < |A_1|;
  - S_0 = B_0 = S′_τ with τ ≍ 1/D, K_1 = 2/α_2, σ = 1/2;
  - when |K| < η|A_1| the bound is trivial.
- The triple convolution at −d counts the pairs with a_1 − a_2 + d ∈ K. This yields rank ≤ D + C_η(1+q)^4 and width ≥ w(S′)exp(−C_η(1+q+log(2+D))), i.e. (C.4). Checked; only E2 is noted.

## Hand-off: does Prop. I.1's proof use Property 1 of Prop. F.2? (Lemma 4.7 transfer)
- **Property 1 of F.2** (p. 137) has four parts:
  - (1a) "Each ψ(T) lies in U";
  - (1b) "the functions y_h∘ψ are fully slow polynomial lifts while β_h∘ψ have integer ordinary coefficients, all of degrees at most h";
  - (1c) "Noninjective maps have negligible probability";
  - (1d) "If the centers are mixed independently with Haar measure, the one-site law … approximates the uniform law on U at the prescribed forward accuracy".
- **What the §3 sampler supplies** (Lemma 3.2, p. 19):
  - item 1 gives (1b) exactly ("C(ψ(t)) − c = y(ψ(t)) + β(ψ(t)) is a polynomial identity. The small lift is fully slow at width v; β∘ψ has integral monomial coefficients");
  - item 3 gives (1c) and support on the buffered chart;
  - item 4 gives only a weak form of (1d) (a lower bound away from "a warm-thickness boundary strip").
  - So what it lacks, per §3.4 (p. 23), is the fine-accuracy (1d).
- **What the proof of Prop. I.1 (pp. 182–183) uses**, read to the end:
  - (1b): "Since the full substituted polynomial has ordinary degree at most d, the pure degree-d part in the retained variables is independent of the values fixed on short axes … Cancel the remaining lower-degree terms by an ordinary polynomial phase of degree at most d − 1."
  - Paths inside {χ = 1}: "Choose χ to equal one on all path supports and to vanish outside the buffered charts. The local correlation is then at least 9/10."
  - Property 2 at fixed centers: "Property 2 of the sampler, applied with degree d − 1, gives an early positive ambient correlation with a site twist times a degree-(d − 1) niltest."
  - Everything after that is on the ambient domain U: Fourier expansion on ambient covers, Lemma B.1 on the product group, the rank hypothesis ("an integer row forbidden by high rank"), and Lemmas I.3, I.4, A.5.
  - Mixed centers, the one-site law, and noninjectivity appear nowhere in the proof. Remark I.5 itself says "The preceding proof uses Property 2 of Proposition F.2 and Lemma B.1".
- **Verdict on the hand-off.** Property 1(d), the part the §3 sampler lacks, is not used in the proof of Prop. I.1. The parts of Property 1 that are used are exactly Lemma 3.2 items 1 and 3. So the "inspection of the proof" transfer at Lemma 4.7 is correct as far as Prop. I.1 is concerned. This is **EXPOSITION** (E3): Prop. I.1's statement should assume (1b), chart-supported paths, Property 2 and the rank hypothesis, instead of "Properties 1 and 2".
  - Caveat outside my scope: this relies on the §3 substitute for Property 2 (the cold clause of Theorem 3.4) being proved without fine (1d). That belongs to the §3 seat.

## What I skimmed / did not check
- **Read for logic, constants not tracked:** the rational-algebra Lemmas A.2–A.4 (heights B(p), Fejér cutoff counts) and Lemma A.3's local-inverse/separation argument.
- **Accepted as standard:** the closure of slow and rational symbol classes under products and inverses, and the BCH degree claims.
- **Accepted (textbook, Tao–Vu style):** the Bohr-set facts quoted at the start of C.1: |B|/N ≥ (w/10)^D, |B_ρ| ≥ (ρ/C)^{CD}|B|, existence of regular dilates, and (C.3).
- **Checked at sketch level:**
  - Lemma C.11 and Lemma A.3 as used in C.12, and the exact Lipschitz constants of the positive partitions of unity in C.12;
  - Lemma D.5's Lipschitz bound exp((1+d)^{C_s}) for F and its chart/atlas construction (the triangular-shear group, lattice grids s!Z^D ⊆ log Γ ⊆ (s!)^{−1}Z^D, and filtered-degree condition were checked);
  - Lemma A.9's cyclic smoothing constants.
- **Statement only:** Prop. D.7. Its proof is Theorem I.15 (Appendix I), not checked.
- **Not checked:**
  - how the main text (Lemma 2.2, §2–§9) uses D.3/D.5/D.7, beyond confirming that D.3 plus D.5 produce an "absolute rule" of D.7's form with Λ = (1+ξ)a;
  - whether the "warm/cold-pre" budgets at the outside application sites (pp. 22, 38, 161) really include the ambient dimension. Theorem A.7 permits n ≤ (2+p)^A, and the appendix convention says dimensions are inside p, but verifying that is for the §3/§5/G seats;
  - Appendices E–I, apart from the hand-off.

## Verdict
HOLDS AS READ IN SCOPE. The LSS input is applied with matching hypotheses (interval normalization identical; box and product-cyclic reductions correct; returned dimension/complexity/Lipschitz/correlation as claimed; degree bookkeeping consistent). The KM, BS and SS citations say what is claimed. There are four EXPOSITION items: E1 (constant order in C.6), E2 (SS regularity convention), E3 (Prop. I.1 hypothesis over-stated; hand-off answer: Property 1(d) is unused, so no GAP at Lemma 4.7 from this source) and E4 (unused oddness assumption).

---
# Appendix: line-by-line working notes (appended during the read)
