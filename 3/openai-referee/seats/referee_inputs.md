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
# Referee seat: inputs — Appendices A–D (printed pp. 86–123)

(Partial notes appended as work proceeds; final sections at the end supersede earlier notes.)

## Sources fetched
- [35] Leng–Sah–Sawhney arXiv:2402.17994 — CURRENT = v3 (10 Aug 2024); paper cites v3. /tmp/oaimath/159/refs/2402.17994/2402.17994v3.pdf
- [30] Kelley–Meka arXiv:2302.05537 — CURRENT = v6 (28 Oct 2024); paper cites v6. /tmp/oaimath/159/refs/2302.05537/2302.05537v6.pdf
- [8] Bloom–Sisask arXiv:2302.07211 — CURRENT = v3 (13 May 2025); paper cites v3. /tmp/oaimath/159/refs/2302.07211/2302.07211v3.pdf

## Notes in progress (A)
- LSS v3 Thm 1.2 quoted (see final section). Paper's interval normalization (A.2) with Q=[N] equals LSS's ‖f‖_{U^{s+1}[N]} exactly (zero-extend to Z/ÑZ with Ñ ≥ 4N: cyclic cube sum = integer cube sum; divide by ‖1_[N]‖^{2^j} = C_j([N])/Ñ^{j+1}). Checked.
- Metric comparison d_c ≤ d_R ≤ d·d_c (LSS Def 3.4 chain metric uses second-kind ψ(x_i x_{i+1}^{-1}), right-invariant; paper's d_R right-invariant Riemannian, basis orthonormal). Forward direction needs only d_c ≤ d_R (Lip_R F ≤ Lip_c F). Checked.
- Box reduction Φ(x)=1+Σa_i x_i, a_i=Π_{r<i}4T_r: Φ(Q)⊆[L] (max ≤ 1+L/3), |Q|/L=4^{-n}, mixed-radix injectivity of 2-face identities (|c_i|≤2(T_i−1)<4T_i). Cube sums agree exactly; C_j(Q)/C_j([L]) ≥ c_j^n 4^{-n(j+1)}/C'_j. Correlation transfers with factor L/|Q| ≥ 1. g∘Φ adapted. Checked.
- Product-cyclic reduction: ≤4^n pieces of diameter <N_i/3, length ≥N_i/8 (checked N_i=1..7 and N_i≥8); bijection group cubes in Q ↔ integer cubes in Q; C_j(Q) ≤ |H|^{j+1}; selector W error O(nθ); WT degree s (s≥1), Lip O(n/θ). Checked.
- Lemma A.9 (A.5) identity, 2^n|Q| shift count, τ-discard, ≥ρ²|Q|/2 retained shifts, side ≥ τ T_i, (A.4) nonnegativity of each term: checked.
- Lemma A.8: layer-1 of log d_h vanishes by choice of γ_h, ε_h; layer j degree ≤ j−1 since symbol of g(t+h) = symbol of g(t) and constants have zero symbol: checked. G□ is a filtration: checked.
## Notes in progress (B)
- Lemma B.2 checked line by line: invertibility; count (3R)^{n-1}ΠT_i/T_* (uses T_i ≥ T_* ≥ 1); covering radius dR/2 and disjoint Voronoi translates ⇒ (B.4); covol(Λ_Z)=covol(Λ_V)·I·E_A/ΠT_i (Λ_V primitive in Λ_Z); pivot argument det(MR_b)_J=det(R_b)_J; Cauchy–Binet (B.6); T_*>C_*l^m forces horizontal pivots; K basis via maximal minors in l^{-k}Z bounded by C_*; lift norm ≤ C_*l^k (singular values ≥1, product = expansion); R denominators | det(l(H_b)_{J0}); (B.3) from lifting I e_i. No objection.
- B.2 base case s=1: geometric-sum bound, decomposition (η(a_i)−q_i)v + q_i v + ker η. Checked.
- (B.7) z-scaling / dual-number derivation checked: coefficient of z in δ_z log d_h(t/z) is the degree-(j−1) part of layer j; first-order contributions of bracket deformation and subleading coefficients vanish because they are evaluated at zero shift/insertion (chain rule). Y_h(X) is linear in h (directional derivative). Layer-1 relative component vanishes. Checked.
- Common fast subalgebra: U_s=n_s, V_j relative kernel, (B.8) from Ũ subalgebra + abelian relative part. Re-normalising A_h,D_h to common A,D via Lemma A.6 + section lifts. (B.9) algebra re-derived (sign and Ad placement correct). Bounds on s_h (|h_i|≤T_i, overlap sides ≥ T_i/B(p)) and r_h (integrality of h) checked.
- (B.10) application of Lemma B.2: M=Ad_B block-unitriangular, identity on layer 1; L_T diagonal in monomial×basis coordinates; m ≤ d·n^s. Checked.
- Grade-by-grade removal: (B.11),(B.12) re-derived; stage 1 (B.13); (B.14) expansion (the hypothesis list explicitly carries [P_d,K]⊆V_{d+1} for all d ≤ j−2, which is needed because K ⊄ U_1 in general); Q_j separation; j=2 horizontal parts absorbed; Y_i(B)_j ≡ ∂_iP_j; final separation at scale T_iT^α. Checked. End state P ∈ W, η(W_s)=0.
## Notes in progress (C.1)
- Lemma C.3 (bilinear reduction) re-derived: H=e^{-p}J ∈[0,1], W(y)=1_E(−y), substitution n=x+y, h=−y. Checked.
- Lemma C.4 (1),(2) and the Cauchy–Schwarz consequence: checked (Bernoulli; (1+x)/2−√x=(x−1)²/(2(1+√x)²); E(X−1)² ≥ c uses EX ≤ 1).
- Lemma C.5: (C.12) re-derived (x_i = s_1 − t_i; Σ_t A(s−t)A(s'−t)=|L|(A∘A)(s−s')); (C.13) sum of squares; 1_L∗G=1+o, F∘F=1+F_1∘F_1+o (uses ΣF_1=0, cap M); binomial lower bound C(2Rm,2m) ≥ R^{2m}. Checked.
- Prop C.6: tiny cutoff e^p uv ≤ e^p κ^{3/4}Φ; peeling: removed contribution b·E_{y0}[node] + O(e^pζb), second means ≤ v exactly (μ_B∗μ_C ≤ 1/|B|), (C.8) gives drop > 2b(u_1v)^θ, telescoping 2S_peel+R_rem ≤ Φ, error summability via b ≤ κ^{-2θ}b(u_1v)^θ; matching (x=x0+r, y=y0−r+s) TV O(Dρ) twice; (C.15) Jensen; (C.16) incl. CS for dependent U,V; flat alternative: Markov 2^{-2m}, a(F∗G) ≤ (1+2δ)(f−g) on good set with δ=ε/8-type choice, smooth Bohr majorant/minorant argument for (C.1) ⇒ E_{s∈S}(f−g)(z+s) ≤ α^{-1}e^{-P}+O(e^pDρ); unbalanced alternative: regularity shift to s_0+S' (error M^q·O(Dρ'), forcing log(1/ρ') = O(p²) — still polynomial), DRC pair weight (|L|/(|L^+|M²))^q (Q∘Q)(a−b)^q (uses L−a ⊆ L^+), Z/Z_bad selection, densities ≥ Z ≥ exp(−O(p²)), (C.4) with q=O(p²), P_CP_{−C}(Q∘Q)=(P_CQ)∘(P_CQ), max at 0, Lemma C.4 contraction q_0; summing: A+q_0B_1 ≤ (1+q_0)Φ/2, S_peel+λR_rem ≤ max(1/2,λ)Φ. Rounds R=c_depth p ⇒ ranks and log(1/w) polynomial in p. Checked.
- Constant order in C.6 (κ, ζ, c_mom, A_ε, B_ε, c_depth, P): text says ζ chosen with κ "sufficiently small" before c_mom is named, but ζ must beat M^{2q}=exp(O(c_cut c_mom p²)) (unbalanced shift) — so ζ's exponent must be fixed after c_mom. Nothing chosen earlier depends on ζ (c_mom = c_mom(ε,c_cut)), so no cycle: EXPOSITION only.
- Lemma C.2 vs Schoen–Sisask arXiv:1408.2568 (only version v1, 11 Aug 2014) Thm 5.4: quoted; the paper's renaming (SS ε→η, SS η→β), the choice A=−A_2, M=A_1, L=−K (or M↔L when η|A_1| ≤ |K| < |A_1|), S_0=B_0=S'_τ, K_1=2/α_2, σ=1/2, and the radius/rank bookkeeping giving (C.4) all checked. Triple counting convolution at −d counts pairs with a_1−a_2+d ∈ K. Regularity constants (paper's O(D|t|) vs SS's 12d) — cosmetic.
- KM [30] v6 §4 = "Sifting", §5 = "Spectral positivity and k-norm inequalities" (Lemma 5.2 decoupling ‖A∗B−1‖_k ≤ ‖A⋆A−1‖^{1/2}‖B⋆B−1‖^{1/2}); BS [8] v3 §2.1 Lemma 7 (unbalancing, incl. Shkredov's physical positivity proof), §2.2 Lemmas 8/10 (dependent random choice). Paper cites them as methods only ("adapt") and re-proves the local versions (C.12),(C.13), unbalancing, DRC inline; no statement is imported. Attribution accurate.
## Notes in progress (C.2–C.4)
- Lemma C.7 checked: degree-r comparison applied to (fA_i, gA_i, JB_j) with slack ε/2 and budget q; hypothesis via A_i·T ∈ T_d; union over F² pairs; e^{-q}-bounds summed over M terms; error 3e^{2p}·δe^{-2p}/6 = δ/2; strictness gives contradiction. Exceptional sets are independent of C_{ℓ,h} (as Theorem C.1 requires). Checked.
- Lemma C.8 (Hahn–Banach) checked incl. positivity of RHS (X^*(ψ)>0 since X ≤ K‖·‖_1), ‖ψ‖_∞ ≤ K/τ via point masses, X(ψ)X^*(ψ) ≥ ‖ψ‖², sampling ℓ ≥ R²K²/τ². Compactness: paper takes closure and re-approximates (p.111) — handled.
- (C.18) re-derived (m=n+h, CS in m, n=m−h). Detector: Lemma A.9 (cyclic, ≤2 translated tests) ⇒ ‖Δ_j e‖_{U^{r+1}} ≥ B^{-1} for B^{-1} of j ⇒ ‖e‖_{U^{r+2}} ≥ B^{-1} ⇒ Theorem A.7 (n=1 cyclic) with s=r+1=d. Degree bookkeeping correct.
- Lemma C.9 checked (tensor, ‖E_hV_h‖² ≥ δ^{2m}, P(X ≥ a/2) ≥ a/2 for X ≤ 1, product of m factors in [0,1]).
- Lemma C.10 checked (partition of unity sums to one).
- Lemma C.11 checked (normal cover Λ=⟨γ^m⟩ ⊆ Λ_0; d(ε^{-1}xλγ^{-1}, ε^{-1}x'γ^{-1}) = d(ε^{-1}xλ, ε^{-1}x') by right invariance, γλγ^{-1} ∈ Λ; varying left normalizers d(ε^{-1},ε'^{-1})).
- Prop C.12 read in full: positive Fourier projection (averaging over connected annihilator keeps exactly the saturated span; change bounded by truncation error + #discarded·threshold); m=0 case via degree-r induction; two-site modelling with shift u=n+h (translated testing family makes Markov uniform over U_{h,j}); pigeonholing B(p)^{P(p)} = B(p) choices; Lemma C.9 anchor; wrap-point splitting; Lemma B.1 on D_{h,j} (one variable, interval ≥ N/B); Lemma A.6 intersection over m ≤ P(p) inverse images; K_h kernel and π_1(K_h)-invariance of averaged F_h (frequencies in the R-span of η_{h,j}); freezing E_h (variation Bρ on cells) and R_h (period q); Lemma A.3 on H→H/H_r×G_Z; (C.24) re-derived from (C.22) with left class λ_n: π(b_h)Λ = π(E_h)^{-1}Z_hπ(κ_h)^{-1}z_{h,c}^{-1}Λ; branch determination away from the O(ρN) wrap neighbourhood; (C.25) uniform in h; Lemma C.10 ⇒ approximation with E|e_h| ≤ B(p)ρ+O(1/N); Lemma C.7 closes. Order: ρ chosen after the Lipschitz constants B(p) of (C.25) and after δ, σ; family sizes depend on ρ only through log(1/ρ)=poly(p). No cycle found.
## Notes in progress (D.1)
- Lemma D.1 checked: telescoping identity; reading of one compression (fibers Φ_{β'}(y)=Π_{β_1} f_{(β_1,β')}(t_{1,β_1}+y), insertion a is (C.2) with shift −t_a and J_a=Π_{b>a}h_b(·+t_b), exceptional set for t_a depends only on t_{>a}, P(bad) ≤ A e^{-R}); cyclic translates of the lower test split at the wrap point with smooth cutoffs (complexity poly(log 1/ρ), error O(ρ+1/N)); budget order ρ before R; failure contribution e^{pV}Σ K e^{-R_r} < δ/4 given L ≥ pK+log(4(s+1)K/δ)+B_0 and V ≤ K; M_r = M_{r−1}^{a_r}(1+ε)^{a_r} (superscript lost in pdftotext; PDF shows it) and log M_r/A_r formula re-derived; degree after r compressions s−r ≥ 0 for j ≤ s+1, so every call of Theorem C.1 has d ≥ 1. Checked.
- Prop D.2 checked: (D.3),(D.4) expectations (E C_i=b, E C_1C_2=2b²−b, E C_i²=b); B_1=uv, B_{1/4}=3/8+3u/8+3v/8−uv/8; deficit ⇒ count ≥ (9/8)(1−τ/18)−(1/8)(1−τ)=1+τ/16; weighted Hölder (D.5) with D ≥ 0, F real; even-moment expansion d_b=d+z_b, x_b=x−p_{l+1}z_b reproduces the cell formula (redundant variable averaged); D is an (l+1)-axis grid with invertible coefficients p_{l+1}−p_a, so Lemma D.1 applies with l+1 ≤ k−1=s+1 axes and sides ≤ q ≤ C_0 p; final CS: squares are positive mixtures (1−b+buu') of grids with ≤ 2q^l vertices (ν_i themselves may be negative for b=1/4 — harmless, since only the squares are bounded); iteration exponent bookkeeping (1+δ)^{(1−1/q)} e^{p/q} per pivot re-derived. Checked.
- Prop D.3 checked: µ_φ ∈ [0, max(1,µ)]; |Eµ_φ−1| ≤ ξ+η via φ and 1−φ and E(µ−1)=0; E(µ_φ−(1+2ξ))T ≤ η; inclusion–exclusion ⇒ (D.7); W-support gives no wraparound and d ≠ 0, so (D.8)=0; trig approximation of W, two-site character splitting via invertible slope difference, one-site case by averaging over d; budget C_sc > D with (2+p)^{C_sc} ≥ (2+p)^D+p+1. Checked.
## Hand-off from §4–§5 seat: does Prop I.1's proof use Property 1 of Prop F.2? (notes)
- Property 1 of F.2 (p.137) has four parts: (1a) ψ(T) ⊆ U; (1b) y_h∘ψ fully slow, β_h∘ψ integer ordinary coefficients, degrees ≤ h; (1c) noninjective maps negligible; (1d) with Haar-mixed centers the one-site law approximates uniform on U "at the prescribed forward accuracy".
- §3 sampler (Lemma 3.2, p.19): item 1 = (1b) exactly (eq. (3.4) polynomial identity, small lift fully slow, β∘ψ integral coefficients); item 3 = (1c) and support on the buffered chart; item 4 = a WEAKER (1d) (lower bound only away from a warm-thickness strip). So the only missing piece is the fine-accuracy (1d).
- Prop I.1 proof (pp.182–183) read to the end. Uses: (1b) ("Since the full substituted polynomial has ordinary degree at most d…", "Cancel the remaining lower-degree terms by an ordinary polynomial phase of degree at most d − 1"); path supports inside {χ=1} ("Choose χ to equal one on all path supports and to vanish outside the buffered charts. The local correlation is then at least 9/10."); Property 2 at fixed centers ("Property 2 of the sampler, applied with degree d − 1, gives an early positive ambient correlation…"); then only ambient-U arguments (Fourier expansion on ambient covers, Lemma B.1 on the product group, rank hypothesis, Lemmas I.3, I.4, A.5). No mixed centers, no one-site law, no noninjectivity estimate appear anywhere. Remark I.5 itself lists only "Property 2 of Proposition F.2 and Lemma B.1".
- Conclusion: (1d) is never used; the used parts of Property 1 are supplied by Lemma 3.2 items 1 and 3. EXPOSITION (hypothesis over-stated), not a GAP — conditional on Theorem 3.4's cold clause (the §3 substitute for Property 2) being itself proved without (1d), which is outside my scope.
