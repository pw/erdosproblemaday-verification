# Seat O report — §§1.1–1.2 (statement), §2 (Prop 2.1, Rem 2.2, Rem 2.3, Prop 2.4), §3 (Lemma 3.1), §4 (Lemmas 4.1–4.3)

Paper: OpenAI, "A classification of finite Euclidean Ramsey configurations" (23 Sep 2026). Read: `src/paper.txt`
(printed numbering) alongside `build/sections/01-introduction.tex`, `02-tensors.tex`, `03-stencil.tex`, `04-pairs.tex`,
and, for interface/consistency only, `06-groups.tex` (Prop 6.4 and the proof of Thm 1.1) and `07-consequences.tex`.
Scripts and outputs: `/tmp/oaimath/172/seats/O_work/{checkA.py, checkA2.py, checkB.py, checkPipeline.py}` (run under
`ulimit -v 4000000; timeout 900`, with `~/.venv/bin/python -I`, since system python3 has no sympy).

Printed equation numbers in my scope: (1)–(2) in Thm 1.1; (3) tensor condition; (4) free expansion; (5)–(7) in
Prop 2.4; (8) U C Uᵀ = I_d; (9)–(10) in Lemma 3.1; (11) J_i R̂ = (h·Y); (12) in Lemma 4.1; (13) Lemma 4.2;
(14)–(15) in its proof; (16)–(17) in Lemma 4.3; (18) the convolution moments. Section 4 has exactly Lemmas 4.1, 4.2, 4.3.

**Bottom line for this scope: I could not refute any load-bearing step. Every step I checked holds, most of them line by
line, and two of them by exact computation.** What remains is exposition only (listed in §7 below). The coordinator's
derived consequence (B) is correct at every step. It follows from Theorem 1.1, the paper never states it, and it is
consistent with everything else in the paper. It is also a strong stress test for §§5–6 (see §9).

---

## 1. Theorem 1.1 statement (§1.1) and §1.2

- The statement matches the .tex. P ∈ Mat_{d+1}(B), B = F⊗_Q F, F = Q(all coordinates). (1) is
  `(p_i⊗1)^T P (1⊗p_i) = 0` with componentwise entries. (2) constrains m_F only on the spatial block. P need not be
  symmetric. Hypotheses are s ≥ 2 and affine span R^d. The singleton case is handled separately.
- §1.2 says "Applying m_F to the evaluation equations gives an ordinary sphere equation". Correct: m_F is a ring
  homomorphism, so m_F of (1) is p_iᵀ m_F(P) p_i = 0, and the spatial block of m_F(P) is I_d. This is Cor 7.1.
- "The condition is independent of the chosen congruent representative". This is proved by Rem 2.3 combined with
  Prop 2.1 (checked below).

## 2. Proposition 2.1 (matrix condition ⇔ tensor condition (3))

Checked line by line.

- **Identification of W⊗_Q W with (d+1)×(d+1) arrays over 𝓑 = R⊗_Q R.** W = ⊕_{α=0}^d R as Q-spaces, so
  W⊗W = ⊕_{α,β} R⊗R, with (w⊗w')_{αβ} = w_α⊗w'_β.
- **Evaluation formula.** e_i(w)⊗e_i(w') = (Σ_α p_{iα}w_α)⊗(Σ_β p_{iβ}w'_β) = Σ (p_{iα}⊗1)(w_α⊗w'_β)(1⊗p_{iβ}), using
  multiplication in the ring 𝓑. Correct.
- **Gradient matrix.** It is the m_R-image of the spatial block. Correct.
- **Flip.** The flip is Q*_{αβ} = τ(Q_{βα}), so E_i(Q*) = τ(E_i(Q)) and m_R transposes. Hence ½(Q+Q*) keeps zero
  evaluations and keeps a spatial block equal to I_d. Correct.
- **Forward direction.** It uses "the natural inclusion B ⊂ 𝓑". The map F⊗_Q F → R⊗_Q R is injective because tensor
  products of injections of Q-vector spaces are injective. This is true but unstated (EXPOSITION). On B, m_R restricts
  to m_F.
- **Converse, (4).** With an F-basis (r_λ) of R, R ≅ ⊕_λ F r_λ, so 𝓑 = ⊕_{λ,μ} (F r_λ)⊗_Q(F r_μ). Each summand is
  B·(r_λ⊗r_μ), a free rank-one B-module (b·(x r_λ⊗y r_μ) multiplies x and y componentwise). So (4) is a free B-basis.
  Correct.
- **Descent of the evaluations.** E_i is B-linear because its coefficients p_{iα}⊗1 and 1⊗p_{iβ} lie in B. Freeness
  then gives E_i(P^{λμ}) = 0 for each pair. Correct.
- **Multiplication.** m_R(b·(r_λ⊗r_μ)) = m_F(b) r_λ r_μ, so I_d = Σ r_λr_μ C^{λμ}. This is a linear system in the
  unknowns c_{λμ} with coefficients C^{λμ} ∈ Mat_d(F) and right-hand side I_d. It has the real solution
  c_{λμ} = r_λ r_μ. Rank is field-independent, so it has an F-solution. Then P = Σ(c_{λμ}⊗1)P^{λμ} satisfies (1)
  (B-linearity) and (2), because m_F((c⊗1)b) = c·m_F(b). Correct. The remark about non-symmetric C^{λμ} is right and
  harmless.
- **Foundations.** The proof uses AC (an F-basis of R). The paper declares ZFC.

## 3. Remark 2.2 and Remark 2.3

- **Rem 2.2.** B = S⁻¹(F⊗_Q F₀) with S = {1⊗f}, because localisation commutes with ⊗. F⊗F₀ is a finitely generated
  F-algebra, so it is Noetherian, and so is its localisation. The kernel of E: B^{(d+1)²} → B^s is finitely generated.
  Its m_F-spatial image is the F-span of the generators' blocks, because m_F is a surjective ring homomorphism. Correct,
  and not load-bearing.
- **Rem 2.3.** The map is H(v,u) = (v − t·Qu, Qu). Then e'_i(H(v,u)) = v − t·Qu + (Qa_i+t)·Qu = v + a_i·u, using
  Q ∈ O(d). Also G((H⊗H)T) = Q G(T) Qᵀ. H is Q-linear (it is R-linear) and invertible, and H⊗H preserves flip-invariance.
  Two congruent sets that both span R^d are related by an ambient isometry. Correct. Combined with Prop 2.1 this gives
  representative independence of the matrix criterion, even though F changes.

## 4. Proposition 2.4 (necessity) — line by line

- **The functional.** im Φ is a Q-subspace of Y and y₀ ∉ im Φ. Extending [y₀] to a Q-basis of Y/im Φ (AC) gives a
  **Q-valued** Q-linear ℓ with ℓ∘Φ = 0 and ℓ(y₀) = L(I_d) = 1. The text writes ℓ: Y → R; it is in fact Q-valued, so
  h_i and H_i are Q-valued. Harmless.
- **(5).** w⊗w ∈ T(W), and Φ(w⊗w) = ((e_i(w)⊗e_i(w))_i, uuᵀ), so ℓ(Φ(w⊗w)) = Σ h_i(e_i(w)) + L(uuᵀ). (5) holds for
  **every** (v,u) ∈ R×R^d.
- **(6).** Take u = 0. Then e_i(v,0) = v and L(0) = 0. Correct.
- **(7).** For a congruent copy, Gram matrices agree by polarisation. Well-definedness: Σc_i(a_i−a₁) = 0 implies
  ‖Σc_i(b_i−b₁)‖² = cᵀGc = 0. Affine span R^d gives a linear isometry Q: R^d → R^D (D×d, QᵀQ = I_d) and t with
  b_i = t + Qa_i. If D < d there are no copies and the claim is vacuous. With u_jᵀ the j-th row of Q,
  (b_i)_j = t_j + u_j·a_i = e_i(t_j,u_j) and Σ_j u_ju_jᵀ = QᵀQ = I_d. Apply (5) at (t_j,u_j) and sum over j = 1..D:
  Σ_i Σ_j h_i((b_i)_j) + Σ_j L(u_ju_jᵀ) = 0. The first term is Σ_i H_i(b_i). The second is L(I_d) = 1, by **additivity
  of L only**. So Σ_i H_i(b_i) = −1. Correct.
- **The brief's question: does h_i, derived from an arbitrary Q-linear functional, cause trouble when summing over
  coordinates?** No. h_i is never required to be additive or regular. (5) is applied pointwise, once per coordinate j,
  and the only linear structure used is the Q-additivity of L, a finite sum of D terms. H_i is a finite sum of D
  rationals.
- **Colouring.** K = 2s+1, and [0,2) is split into K half-open intervals of length 2/K. The colour of z is the s-tuple
  of labels of H_i(z) mod 2, which gives at most r₀ = K^s colours, independent of D. Suppose b_1, …, b_s are
  monochromatic. For each i, the i-th labels of b_i and b₁ agree, so the representatives differ by
  ε_i ∈ (−2/K, 2/K), and H_i(b_i) − H_i(b₁) = 2n_i + ε_i (ε₁ = 0). Summing and using (7) together with
  Σ_i H_i(b₁) = 0 (from (6)) gives −1 = 2Σn_i + Σε_i. Then Σε_i is an odd integer with |Σε_i| < s·2/K = 2s/(2s+1) < 1.
  Contradiction. Correct.
- **Counting remark (EXPOSITION).** ε₁ = 0, so (s−1)·2/K < 1, i.e. K ≥ 2s−1, already suffices. K = 2s+1 is
  conservative.
- **Conclusion.** The same r₀ works in every R^D, so A is not Ramsey (take r = r₀). Hence Ramsey implies (3), which by
  Prop 2.1 implies the matrix condition. Correct.

## 5. Lemma 3.1 (finite lattice identity) and the §3 preamble

- **Preamble, symmetry of C.** T symmetric and {w_a⊗w_b} Q-independent give C = Cᵀ.
- **Preamble, (8).** G(T) = UCUᵀ. Correct.
- **Preamble, V_i.** V_i = span_Q Λ_i equals the kernel of the Q-linear map λ ↦ e_i(w(λ)) on Q^k (clear denominators).
  So Q^k/V_i ↪ R.
- **Preamble, the hypothesis of Lemma 3.1.** (e_i⊗e_i)T is the image of ΣC_{ab}ε_a⊗ε_b under φ_i⊗φ_i, with φ_i
  factoring through Q^k/V_i ↪ R. A tensor product of injections over Q is injective. This gives the hypothesis.
- **Kernel of Q[Γ] → Q[Γ/Λ_i].** It is J_i = (X^h−1 : h ∈ Λ_i), via X^γ − X^{γ₀} = X^{γ₀}(X^{γ−γ₀} − 1). Correct.
- **Completion.** R = Q[Z]_{(1+Z_j)} with R/m^nR ≅ Q[Z]/(Z)^n, so R̂ = Q[[Z]]. log/exp have rational coefficients and
  give mutually inverse continuous automorphisms Q[[Z]] ≅ Q[[Y]] with (Z) = (Y).
- **(11).** X^h − 1 = exp(h·Y) − 1 = (h·Y)·unit, valid for negative h_j too. Hence (11). Correct.
- **Q₂ ∈ J_iR̂.** ker(Sym Q^k → Sym(Q^k/V_i)) is the ideal generated by V_i in degree 1. The image of
  ΣC_{ab}ε_a⊗ε_b in ⊗² is zero, hence its image in Sym² is zero. So Q₂ ∈ (h·Y : h ∈ Λ_i) ⊂ J_iR̂. Correct.
- **Flatness, verified against the source.** Stacks Lemma 10.97.2 (Tag 00MB), fetched:
  *"Let I be an ideal of a Noetherian ring R … The ring map R → R^∧ is flat."* This is exactly what is used. R is
  Noetherian. Then R/I ↪ ⊕R/J_i stays injective after ⊗R̂, so IR̂ = ∩J_iR̂. Correct.
- **Truncation.** Q₂ = Σf_aα_a (finite, by definition of the extended ideal). Truncate α_a in Z through degree 2 to get
  b_a ∈ Q[Z] ⊂ R, and set f = Σf_ab_a ∈ I. Then f − Q₂ = Σf_a(b_a−α_a) ∈ m³R̂ = (Y)³. Correct.
- **(9)–(10).** f ∈ each J_i gives the zero coset sums (9). X^γ = exp(γ·Y) ≡ 1 + γ·Y + ½(γ·Y)² mod (Y)³. Comparing with
  ½YᵀCY, and using C symmetric, gives (10). Correct.
- **Closing paragraph.** e_i(w(γ)) = e_i(w(γ')) ⇔ γ−γ' ∈ Λ_i, by additivity. Correct.

## 6. Section 4 (Lemmas 4.2, 4.3, 4.1)

**Lemma 4.2.**
- UCUᵀ = I_d gives rank U = d and C|_H > 0 on H = im Uᵀ, with R^k = H ⊕ ker U orthogonally.
- U P_H = U, so tr(USUᵀ) = ε·tr(UUᵀ). This gives (14).
- S + C is positive definite for large L (Schur complement). S + tC is positive definite as a convex combination.
- Heat identity: d/dt φ_{S+tC} = D_Cφ_{S+tC}. I checked it via the Fourier transform: exp(−½ξᵀQξ) gives the factor
  −½ξᵀCξ, and D_C corresponds to −½ξᵀCξ. It holds for indefinite C. Hence D_C b_* = φ_{S+C} − φ_S.
- (φ_{S+C} − φ_S)₋ ≤ φ_S, and ∫φ_S‖Ux‖² = tr(USUᵀ). This gives (15).
- Cutoff: the product rule is correct (the two cross terms merge by symmetry of C), and Schwartz decay kills the tails.
- Final bound: η/8 + η/8 = η/4 < η/2 < η∫b_R. Correct.

**Lemma 4.3.**
- Pushforward to Γ/Λ_i commutes with convolution: push(ν*d) = push ν * push d.
- (18) follows by substituting λ = β+γ, using Σν = 0 and Σνγ = 0.
- Taylor expansion: n²Σν(γ)b(x−γ/n) = D_Cb(x) + O(n⁻¹), uniformly in x, by the bounded third derivative and the finite
  Σ|ν||γ|³.
- All supports lie in a fixed ball, and there are O(n^k) points, so the negative-part sums differ by O(1/n). Then a
  Riemann sum of a continuous compactly supported function, together with ζ_n → ∫b, gives (17) for large n.
- Rational approximation: d ↦ ν*d and d ↦ ζ are linear on R^E. d ↦ Σ(ν*d)₋‖Uλ/n‖² is continuous. The strict
  inequalities survive a rational perturbation. The **exact** identities (zero pushforwards, (16)) hold for every
  finitely supported d, so they are preserved exactly. Correct.

**Lemma 4.1.**
- Lists: Mμ₊ (respectively Mμ₋) copies of w(λ/n).
- Zero pushforward on Γ/Λ_i, together with "same value ⇔ same coset", gives equal value multiplicities for each label i.
- Scaling by 1/√(ζM): B₊ − B₋ = ζ⁻¹ U(Σμ(λ/n)(λ/n)ᵀ)Uᵀ = U C Uᵀ = I_d, and tr B₋ < η.
- B₋ ⪰ 0 and λ_max ≤ tr, so P = ηI − B₋ ⪰ 0. Appending the same rows (0, r_j) gives Gram matrices (1+η)I and ηI and
  keeps multisets equal. Dividing by √(1+η) gives (12) with q = η/(1+η).
- "Equal length" uses Σμ = 0. This is not listed in Lemma 4.3's conclusion but follows from zero pushforward
  (EXPOSITION).

**Interface with §6.** The permutation taking f_i to g_i depends on i. Prop 6.4 assumes exactly this ("each g_i is a
coordinate permutation of f_i"; H is the full coordinate permutation group; "f_i, g_i lie in the same orbit for each
i"). The proof of Thm 1.1 uses q < 1/(2n), which η small provides. The interface matches.

**Exact end-to-end check (checkPipeline.py).** A = {0, 1} ⊂ R¹ with certificate w₁ = (0,1), w₂ = (1,0),
C = [[1,−½],[−½,0]], k = 2.
- Exact linear algebra found ν satisfying (9)–(10) (support 4).
- I convolved ν with a rationalised d_n built from Lemma 4.2's b_* (S = diag(0.01, 1), n = 16), giving μ with support
  28,154.
- Verified **exactly**: both zero pushforwards; Σμλλᵀ = (Σd)C (i.e. (16)); equal value multisets at a₁ and a₂;
  B₊ − B₋ = 1.
- Numerically: negative moment / ζ = 0.00957. That is about tr(USUᵀ) = 0.01, as (15) predicts.
- Result: ‖f₁−f₂‖² = 1 and ‖g₁−g₂‖² = 1/21 = q for η = 1/20.

The §§3–4 machinery produces what Lemma 4.1 claims on a real instance.

## 7. Objections (none FATAL, none GAP)

1. **EXPOSITION — Prop 2.1.** *"using the natural inclusion B ⊂ 𝓑"*: the injectivity of F⊗_QF → R⊗_QR is used but not
   stated. It holds by flatness over Q.
2. **EXPOSITION — Prop 2.4.** *"a Q-linear functional ℓ : Y → R"*: by construction ℓ takes values in Q. Also,
   K = 2s+1 is more than needed (ε₁ = 0, so K ≥ 2s−1 works). Neither affects correctness.
3. **EXPOSITION — Lemma 4.3 / proof of Lemma 4.1.** *"The zero total mass of μ shows that the two lists have the same
   length"*: Σμ = 0 is not in Lemma 4.3's conclusion but follows from any zero pushforward (s ≥ 1), or from (18).
4. **EXPOSITION — omitted corollary.** Remark 2.2 discusses "the algebraic nature of the criterion". Neither it nor §7
   mentions the number-field case (B) below, which is the most striking one-paragraph consequence of Theorem 1.1.

**Citations in scope.**
- Stacks 00MB is verified verbatim and is load-bearing for Lemma 3.1.
- EGMRSS "[4, Theorem 13 and Lemma 15]" and Rado [21] are **not load-bearing**: Prop 2.4 proves its modular colouring
  directly. I could not check the EGMRSS theorem/lemma numbering against the 1973 paper. Pálvölgyi cites the same
  numbers, but both texts are ChatGPT-written, so that is not independent corroboration.

## 8. Task (A) — explicit sanity check of Prop 2.4's colouring

**Explicit when A is non-spherical (checkA.py).** Take ℓ_i = c_i·m_R, which is Q-linear on R⊗R, and
L(M) = −Σc_i a_iᵀMa_i. Then ℓ∘Φ = 0 and L(I) = 1 if and only if
Σc_i = 0, Σc_ia_i = 0 and Σc_i‖a_i‖² = −1. This is solvable exactly when A is not spherical, and it is the classical
EGMRSS invariant. In this case h_i(x) = c_ix² and H_i(z) = c_i‖z‖².
- **Collinear {0,1,2} ⊂ R, F = Q.**
  - c = (−½, 1, −½). (5) verified symbolically, L(I) = 1.
  - 160 random exact-rational congruent copies in D = 1, 2, 3, 5: (7) gives exactly −1 every time; 0 monochromatic.
  - Adversarial exhaustive grid over all 769,470 copy-parameters (x, y) = (|t|², t·u) on a fine rational grid: 0
    monochromatic, and 0 "proof-relevant" coincidences (label_i(b_i) = label_i(b₁) for every i).
  - Negative controls, to show the instrument can fire:
    - K = 2: 436 monochromatic, 100,046 proof-relevant coincidences.
    - K = 3: 354 proof-relevant coincidences.
    - Wrong weights (1, −1, 0), which do not satisfy the moments: 48,018 monochromatic.
  - Threshold sweep: K = 4…7 give 0. The proof guarantees this for K ≥ 5.
- **Non-spherical planar {(0,0),(1,0),(0,1),(2,2)}.** c = (−¾, ½, ½, −¼). (5) holds symbolically. 75 random exact
  copies via rational Cayley-transform orthogonal maps into D = 2, 3, 4: (7) = −1 exactly, 0 monochromatic.

**Why it cannot be made explicit when A is spherical.** Any functional of the factored form ℓ_i = φ_i∘m_R (with φ_i
any Q-linear map) fails. Take T = Σ P0_{αβ} ε_α⊗ε_β, where P0 is the real sphere matrix. Then ℓ(Φ(T)) = Σφ_i(0) + L(I)
= L(I), so ℓ∘Φ = 0 forces L(I) = 0, which is incompatible with ℓ(y₀) = 1. checkA.py confirms that the
multiplicative ansatz has no solution for a triangle, a square and a 2-point set. So for spherical A some ℓ_i must be a
Q-bilinear form on R that is not of the form c·xy.

Such a form cannot be made explicit. In ZF + DC + "every set of reals has the Baire property" (consistent relative to
ZF, by Shelah), every additive R → R map is continuous (Pettis). Hence every Q-bilinear R×R → R map is c·xy, and no
separating ℓ exists for any spherical A. Prop 2.4's functional for a spherical set therefore exists only by choice. In
the paper's and Pálvölgyi's examples it comes from a derivation of R extended from Q(t) through a transcendence basis.
This matches the paper's statement *"no continuity or measurability is asserted or needed"* and its "ZFC" declaration.
It is not a defect.

## 9. Task (B) — the algebraic-coordinates consequence: every step checked; it holds (conditional on Thm 1.1)

Claim: *every spherical set with algebraic coordinates is Ramsey; every non-Ramsey spherical set has a transcendental
coordinate.*

1. **F is a number field, and B is a product of fields.** F = Q(θ) ≅ Q[x]/(f) with f separable (characteristic 0).
   Then F⊗_QF ≅ F[x]/(f) ≅ ∏_j F[x]/(f_j), with f = ∏f_j over F. The product is reduced, so it is a finite product of
   fields. ✔
2. **m_F is the projection onto exactly one factor.** m_F is surjective (x⊗1 ↦ x) onto a field, so ker m_F is maximal.
   The maximal ideals of ∏K_j are exactly the kernels of single projections. So m_F = ι∘π_{j₀} with ι: K_{j₀} ≅ F (a
   field homomorphism is injective, and it is onto). It is exactly one factor because the primitive idempotents sum to
   1 and are orthogonal, so m_F(e_j) ∈ {0,1} and exactly one equals 1. Concretely, j₀ is the factor F[x]/(x−θ),
   which occurs once since f is separable. ✔
3. **e·b vanishes exactly when m_F(b) does.** e·b has π_{j₀}-component π_{j₀}(b) and is 0 elsewhere. So e·b = 0 ⇔
   π_{j₀}(b) = 0 ⇔ m_F(b) = 0. Also e·b = e·(m_F(b)⊗1) and m_F(e) = 1. ✔
4. **The sphere matrix is available over F.** The centre z and κ = ρ² − ‖z‖² solve ‖a_i‖² − 2a_i·z − κ = 0, a system
   with coefficients in F. The rows p_i span R^{d+1} (affine span R^d), so the solution is unique, and a unique real
   solution of an F-system lies in F^{d+1}. So P0 = [[−κ, −zᵀ], [−z, I_d]] ∈ Mat_{d+1}(F), with p_iᵀP0p_i = 0. ✔
5. **P = e·(P0⊗1) satisfies (1) and (2).** (1) is e·X_i with X_i = Σ(p_{iα}P0_{αβ})⊗p_{iβ} and m_F(X_i) = p_iᵀP0p_i = 0,
   so e·X_i = 0 by step 3. (2) is m_F(eP0_{αβ}⊗1) = P0_{αβ} = δ_{αβ}. ✔
6. **Representatives.** "Algebraic coordinates" is congruence-invariant up to choosing the representative.
   Gram–Schmidt and Cholesky stay inside the real algebraic numbers (a real closed field). So the class is exactly
   *finite spherical sets all of whose squared distances are algebraic*. ✔

**Computational confirmation (checkB.py).**
- F = Q(2^{1/3}) is non-Galois. B = Q[x,y]/(x³−2, y³−2), and y³−2 = (y−x)(y²+xy+x²) over F.
- e = (xy² + x²y + 2)/6. Verified e² = e, (x−y)e = 0, m_F(e) = 1, and e·b = e·(m_F(b)⊗1) on random b.
- Test set: the 7-point spherical set α(1+u_j, v_j) (centre (α,0), radius α), with (u_j, v_j) rational points on the
  unit circle.
- Results: all 7 tensor evaluations (1) of P = e·(P0⊗1) are exactly 0, and the m_F-spatial block is I₂.
- Control: the naive lift P0⊗1 without e gives nonzero evaluations, e.g. −2x² + 2xy.
- The 7 quadratic rows have rank 5 < 7, so **Prop 7.3 / Cor 7.4 do not cover this set.** The consequence gives Ramsey
  sets beyond every stated corollary.
- With F = Q (any number of rational points on a circle), B = Q, m_F = id, and P = P0 works directly.

**Is it stated in the paper? No.** I searched paper.txt and all .tex files for "algebraic", "transcend", "number
field", "idempot" and "product of fields". The only hits are unrelated uses:
- "algebraic condition" / "algebraic separation" / "algebraic functionals";
- "algebraically independent" in Prop 7.6;
- "transcendental" in Cor 7.5 and Prop 7.7;
- the ultrafilter idempotents in §5.

It is also not in the Lean scope note (`docs/172.md`) or on the erdosproblems #174 page or forum (live text).

**Is it consistent with the rest of the paper? Yes.**
- Every non-Ramsey spherical example has transcendental coordinates, and each obstruction provably collapses for
  algebraic coordinates:
  - **Prop 7.7.** The derivation ∂ = ½(1+t²)d/dt on Q(t) needs t transcendental (Liouville's constant, proved
    transcendental there). Q-derivations of a number field are zero.
  - **Prop 7.6.** Algebraically independent t_i. For rational t_i the 9 rows (p_α(t_i)p_β(t_i)) have rank ≤ 6, so
    det D = 0.
  - **Pálvölgyi's Theorem 1.** "For any transcendental r > 2", with a derivation D(r) = 1. His appendix examples (e.g.
    A.13, with a = π − 3) and his "almost every"/generic statements are likewise transcendental.
- The positive results (Cor 7.2, Prop 7.3, Cor 7.4, Cor 7.5) are all consistent with it. Cor 7.5 needs transcendental
  a only for LRW's non-subtransitivity; its Ramsey part holds for all a.
- I know of no published non-Ramsey spherical set with algebraic squared distances. Before Pálvölgyi (Sep 2026) no
  spherical set was known to be non-Ramsey.

**Why it matters (for the coordinator, not a defect in my scope).** My §§2–4 verification already proves the following
unconditionally. Every spherical set with algebraic squared distances satisfies (3), hence admits the exact two-scale
coordinate-permutation pairs of Lemma 4.1 for every q > 0. The Ramsey conclusion then rests **entirely** on §§5–6
(Prop 5.1 and Prop 6.4). If §§5–6 are right, the paper proves Graham's spherical conjecture over the real algebraic
numbers in one paragraph — for example, every finite set of rational points on a circle is Ramsey. That is a far
stronger statement than the paper's Cor 7.4, and the paper does not make it. Seats auditing §§5–6 should treat this as
a stress test: for, say, 7 rational points on a circle, every step there must go through with nothing beyond P = P0.

VERDICT: HOLDS AS READ
