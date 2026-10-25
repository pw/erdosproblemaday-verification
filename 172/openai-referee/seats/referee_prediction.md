# Referee report, scope `prediction`: proof of Principle 2.3 (§§3–5, PDF pp. 11–38) plus Lemma 7.2 (PDF p. 48)

Referee tag: `prediction`. Date read: 2026-10-11.
Text read: paper.txt, with every displayed formula that mattered checked against the rendered PDF: pp. 16–18, 25–37.
Sources fetched myself, each into its own directory under /tmp/oaimath/refs/:
- GTZ arXiv:1009.3998 v4 and v5, plus the abs page.
- The GTZ erratum PDF from people.maths.ox.ac.uk. It is byte-identical to the copy another referee fetched.
- Tao–Ziegler arXiv:1603.07815v4.
- Yamada arXiv:2312.16090v1.
- RTTV arXiv:0806.0381v1.
- Gowers arXiv:0811.3103.
- Green–Tao, Linear equations in primes, arXiv:math/0606088.

I read §2 only to learn what Principle 2.3 and Definitions 2.1/2.2 require. I did not re-referee it.

## Bottom line for this scope

I set out to break Principle 2.3 and could not. Every step from the count (2.10) down to the global Gowers norm is accounted for: masks, rows, Cauchy–Schwarz, transference, inverse theorem, Ramsey, projection. The parameter graph has no cycle. The four external results the proof uses say what the paper says they say. Every objection below is COSMETIC or UNCLEAR. None is FATAL or a GAP.

**Verdict for scope: HOLDS AS READ**, with the skim list below as the residual risk. That list mainly covers standard facts, plus §§6–8, which this Principle does not use.

---

## 1. Parameter and dependency graph (hunt items 1, 4, 8)

I traced every constant to its inputs.

| quantity | defined at | depends on | uniformity required / obtained |
|---|---|---|---|
| q_mask = 2^m−1, K_m = q_mask·2^{q_mask} | Lemma 4.2 | m | — |
| row templates, kernel vectors, polynomial list D, d ≤ K_m−1, C_m, θ = 2^{−(q_mask+d)} | Lemmas 4.2–4.3, Prop 4.5 | m, J* only ("Neither d, C_m, nor θ^{−1} depends on N, on the scales, or on the functions") | checked: built by a deterministic choice of mask order, coordinates, tracked branch and kernel vector (the first non-root integer t) |
| k = 2^d (subgroup-norm order), t = 2k−1 (global order), step t−1 = 2^{d+1}−2 | Lemma 5.5 | m | **s = s(m)** fixed by (5.1) "s + 1 ≥ 2(2^d) − 1 for every cube order d occurring in Proposition 4.5" ⇒ depends on m only. ✔ |
| b_k(·) | TZ Thm 1.23 | k (rank 0) | independent of the family, the group and the system ✔ (source quoted below) |
| c_t(δ), nilmanifold list, Lipschitz bound | GTZ GI(t−1) | t, δ | ✔ |
| C_{d,J0} in (5.13) | Lemma 5.5 | d, J0 | density ≤ (2J0)^d ✔ |
| κ(d,J0,γ) | Lemma 5.5 | d, J0, γ | "independent of the master count, the gap, the cutoffs, and the cell probabilities" ✔ |
| ζ, then J0, then ε | §5.4 | η, m (then ζ, then κ) | chosen **before** N ✔ |
| N | Lemma 5.4 | n, r, \|A\|, ε (Ramsey over (1/ε²+1)^{\|A\|r} colours) | ✔ |
| scales h_j, M, e0(w), pools, R_l, X_l | Lemma 3.3 | w, N, template list (diagonalised in Remark 3.4) | qualitative at each w ✔ |
| dense models F | Prop 5.2 | w, ρ, the finite set of test types (diagonal in J0) | complexity irrelevant ✔ |
| models S and their complexity | Lemma 5.4 | everything, including χ | allowed by Principle 2.3 ("may depend on all the fixed data and tolerances") ✔ |

**No cycle.** S is chosen after the Ramsey selection. The Ramsey colours are numbers (U-limits of ‖P F‖²) that do not involve S. κ and ε never see N or S.

Is any constant a function of w or of the model complexity where uniformity is needed?
- The o(1) terms are o(1) as w→∞ at fixed templates. Remark 3.4 diagonalises over the countable template list.
- In §5.4 every o(1) is either for fixed-complexity S (Lemma 5.3 applied to ψ(S)) or uniform over all bounded inputs (Props 3.6, 4.5, 5.2, Lemma 5.1).
- I found no o(1) that is uniform only for fixed complexity and is then fed a w-dependent complexity.

**Ultrafilter (hunt item 5).**
- Every lim_U in this scope is of an eventually bounded sequence: probabilities, counts bounded by 2^{O(1)}+o(1), cube means bounded by (1+V)^{2^d}·o(1)+O(1).
- Lemma 5.5 intersects only a single U-set.
- §5.4 combines finitely many blocks, labels, colours and telescoping steps.

---

## 2. Objections

**O1. Erratum date. Location: reference [18]; used at p. 34. Severity: COSMETIC.**
The paper writes: "[18] … Erratum for 'An inverse theorem for the Gowers U s+1 [N ]-norm', author-hosted erratum, April 2024, 6 pp."
- The fetched PDF's metadata reads `CreationDate: Sun Feb 25 15:55:39 2024 UTC`, and the PDF has 6 pages.
- Green's papers page says "An erratum for this paper was issued in 2024."
- The month is unsupported and nothing depends on it.

**O2. Mis-described Cauchy–Schwarz direction in the proof of (5.13). Location: Lemma 5.5, p. 35. Severity: COSMETIC.**
The paper says: "Insert one uniform subgroup direction translating the root alone; the density is invariant in that direction."
- The direction x ↦ T^a x translates every vertex, not "the root alone".
- What makes it usable is that it fixes the density factor ρ_p(v). That factor is the one eliminated at this step.
- The next sentence has the same slip: "insert a direction x ↦ T^a x, v_j ↦ v_j − a … which leaves that vertex fixed." That direction fixes every vertex containing j, not just ω.
- Neither slip affects the count: k = 1 + (2^d − 1) = 2^d eliminations leave the root's 2^k copies as a Haar Q_p-cube.
- I re-derived (5.13) and it holds, with C_{d,J0} coming from E ρ² ≤ (2J0)^d.

**O3. Scope of Prop 3.6's CRT hypothesis. Location: Prop 3.6, p. 17. Severity: UNCLEAR (wording); the mathematics is correct.**
The hypothesis is "The CRT law of all prime slots at the primes w < p ≤ V is within total variation ε_CRT of independent uniform units". This controls residues modulo p only.
- The local factor α_p = p^{Σa_u} P_{x mod p^A}(…) depends on the row coefficients modulo p^A.
- The proof never replaces α_p itself. It bounds 0 ≤ α_p − 1 ≤ β_p, and β_p depends only on the valuations and on the mod-p test T_p. It then swaps in the uniform law inside the β-bound: "we can first replace the prime residues by independent CRT-uniform units at cost at most 2V^q ε_CRT".
- Read this way, (3.11) is proved: a lower bound of 1 plus an upper excess ≪ 1/w + V^q ε_CRT, uniformly in the prime-only event ℰ.
- It does need to be read this way. The proof's sentence that "the CRT theorem now factors the normalized divisibility count" refers to the CRT applied to x mod K, not to the prime slots.

**O4. Erratum versus Appendix C. Location: §5.3, p. 34. Severity: COSMETIC; I checked whether it is a GAP and it is not.**
The paper says: "in its finite-list linear-nilsequence formulation [17, Conjecture 1.2 and Theorem 1.3], with the correction [18]".
- The erratum's first bullet says, in part: "the degree of the filtration does not control the nilpotency class of G0 (an issue in Appendix C)".
- It also says: "The issue in Appendix C … could be resolved in exactly the same way. However, it is best to simply remove the problem by insisting on the tautness condition G0 = G1 as part of the definition of filtered nilmanifold."
- Appendix C is exactly where GTZ pass from polynomial to linear nilsequences ("Lifting linear nilsequences to polynomial ones"), which is the form the paper uses.
- So the authors say the correction leaves the linear formulation (Conjecture 1.2) in force. The paper relies only on that statement, and says so: "We use only this inverse conclusion, not the original auxiliary Proposition 8.3 addressed by the erratum."
- arXiv v5 (23 Apr 2026) restates Conjecture 1.2 and Theorem 1.3 word for word as in v4. I diffed them; the only differences are glyph rendering.

No objection rises above these. Hunts I ran that came up empty:
- "Standard / clearly / by Ramsey" at a hard step: the Ramsey step in Lemma 5.4 is written out, including which tuples are compared.
- A uniformity used before it is established: none.
- A hidden majorant condition: none (see §4).
- Rational colour arguments: every χ-argument in §§4–5 is χ(Π c_k z_k), χ(c_{d(J)} L_J(z)) = χ(Σ c_k z_k) or χ(h_B a y), each an integer once w is large. Lemma 3.3(1) and the remark after Def 2.1 make c_k = h_{B_k}a_k an integer with c_u/c_d ∈ W·ℕ for u < d.

---

## 3. Citation table (scope)

| cited result | what the paper says it gives | what the source says (verbatim) | verdict |
|---|---|---|---|
| **GTZ [17]** Conj 1.2 + Thm 1.3, arXiv:1009.3998 (**latest = v5, Thu 23 Apr 2026 12:20:55 UTC**, as the paper cites; v4 = 22 Apr 2024; v5 comment: "corrects a mistake in the proof of Lemma 13.2 (the wrong filtration was specified) and two small typos on page 28") | p. 34: "a 1-bounded function on an integer interval with U^t norm at least δ correlates by at least c_t(δ) > 0 with a sequence Φ(g^k x) on a nilmanifold of step at most t − 1. There is a finite list of such nilmanifolds, with connected simply connected groups … ‖Φ‖∞ ≤ 1 and its Lipschitz bound depend only on t, δ. … No bound on g is asserted or needed." | "an s-step nilmanifold is a manifold of the form G/Γ, where G is a connected, simply-connected nilpotent Lie group of step at most s … Conjecture 1.2 (GI(s)). … there exists a finite collection M_{s,δ} of s-step nilmanifolds G/Γ, each equipped with some smooth Riemannian metric d_{G/Γ} as well as constants C(s,δ), c(s,δ) > 0 … Whenever N ⩾ 1 and f : [N] → C is a function bounded in magnitude by 1 such that ‖f‖_{U^{s+1}[N]} ⩾ δ, there exists a nilmanifold G/Γ ∈ M_{s,δ}, some g ∈ G and a function F : G/Γ → C bounded in magnitude by 1 and with Lipschitz constant at most C(s,δ) … such that \|E_{n∈[N]} f(n)F(g^n x)\| ⩾ c(s,δ)." "Theorem 1.3. For any s ⩾ 3, … GI(s), is true." Abstract: "for all s ⩾ 1". The U^d[N] norm is defined as ‖f̃‖_{U^d(Z_Ñ)}/‖1_{[N]}‖_{U^d(Z_Ñ)}, matching the paper's "zero-extension norm divided by the norm of the interval indicator". | **MATCH.** The complexity notion matches Def 2.2: a finite list, sup and Lipschitz bounds, g and x unrestricted. The complex-to-real step (rotate the phase, take the real part) is valid. t = 2, 3 are GI(1), GI(2), "recalled in the Introduction" ✔. |
| **GTZ erratum [18]** | p. 34: "We use only this inverse conclusion, not the original auxiliary Proposition 8.3 addressed by the erratum." | "The proof of Proposition 8.3 is incorrect, and this proposition does not hold as stated." The erratum reproves Prop 7.3 via its new Prop 3.1. Its title framing: "We correct some minor issues". Its Appendix C remark is quoted under O4. | **MATCH.** The date ("April 2024" against a PDF created 25 Feb 2024) is COSMETIC (O1). |
| **Tao–Ziegler [34] Thm 1.23**, arXiv:1603.07815v4 (= Discrete Anal. 2016:13) | (5.11): "for each k there is a function b_k(δ) → 0 … E_{α,α'}‖h‖_{U^{2k−1}_{Q_α+Q_{α'}}(X)} ≤ δ ⟹ E_α‖h‖_{U^k_{Q_α}(X)} ≤ b_k(δ), \|h\| ≤ 1. The bound is independent of the finite family, the group, and the probability system." | "Theorem 1.23 (Qualitative Bessel inequality for uniformity norms). Let (Q_i)_{i∈I} be a finite non-empty family of coset progressions Q_i, all of rank at most r, in an additive group G. Let (X,T) be a G-system, and let d be a positive integer. Let f lie in the unit ball of L∞(X), and suppose that E_{i,j∈I}‖f‖_{U^{2d−1}_{εQ_i+εQ_j}(X)} ≤ ε for some ε > 0. Then E_{i∈I}‖f‖_{U^d_{Q_i}(X)} ≤ c(ε) where … c depends only on r and d. (In particular, c is independent of the size of I.)" Def 1.10: rank-0 coset progression = finite subgroup H; dilate εQ := H + {…\|n_i\| ≤ εN_i}, which is H when r = 0. Def 1.9 uses pairs h, h′ ∈ Q, which equals the paper's single-v convention when Q is a subgroup. | **MATCH.** X_l (disjoint cells, cell-wise G_l action) is a G_l-system. Non-uniform weights on the index set are handled by repetition plus approximation, legitimate because c is independent of \|I\|. |
| **Yamada [36] Thm 2**, arXiv:2312.16090v1 | Lemma 3.5: "Theorem 2 of [36], together with log(Y/p) ≥ ½ log Y, bounds the number of primes in a reduced class in that interval by O(Y/(p log Y))" for p ≤ √Y. | "Theorem 2. Let k ≥ 1 and a be relatively prime integers. Then, for any positive real numbers x and y with y > k, we have π(x, x+y; k, a) < 2y/(φ(k)(log(y/k) + 0.8601))." | **MATCH.** With k = p ≤ √Y and y = Y the bound is ≤ 4Y/((p−1)log Y). |
| **Gowers [10] §4 / RTTV [28] §2** | Method attribution for Prop 5.2 (minimax plus polynomial approximation). The paper re-proves Prop 5.2 in full and does not import its hypotheses. | Gowers §4 is titled "The positivity and boundedness problems", with §4.1 "Algebra norms, polynomial approximation and a first transference theorem". RTTV §2 ("Our Proof") uses "the min-max theorem for 2-player zero-sum games" and "approximating the threshold function with a low-degree polynomial". | **MATCH** as attribution. No hypothesis gap is possible: the only pseudorandomness used is Lemma 5.1, proved in the paper. |
| **Green–Tao [14] Prop 11.5, Prop 11.2, App E** (cited before Lemma 7.2) | The missing-corner constraint and the coordinate-product decomposition. | "Proposition 11.5 (Parallelepiped constraint). There exists a compact set Σ ⊆ (G/Γ)^{{0,1}^{s+1}_*} and a continuous function P : Σ → G/Γ such that, for any (s+1)-dimensional parallelepiped … x_{0^{s+1}} = P((x_ω)…)". Lemma E.10: "Γ^{{0,1}} ∩ HK^{s+1}(G•) is a discrete and cocompact subgroup"; Lemma E.7 gives the corner uniqueness. | **MATCH.** Lemma 7.2 is re-proved in the paper; see §5 below. |
| Green–Tao [15] Def 3.1 and §5 | "plays the role of" only; not used. | — | Not needed, not checked. |
| Selberg [32] eq. (1.1) | Qualitative PNT in progressions modulo the fixed Q_l, used in Lemma 3.3. | — | COULD NOT FETCH (1950 journal, no arXiv copy). Only the qualitative PNT in APs at a fixed modulus is used, which is standard. Not load-bearing on rate. |
| Green–Tao [12] §2 and App. A | Rational-subgroup facts for Lemma 7.1. | — | Not fetched. The same fact (cocompactness of the cube lattice) is [14, Lemma E.10], quoted above. |

---

## 4. Hunt-list answers with locations

**(1) Which norm controls the count, and is its order a function of m?**
- Count (2.10): it is form (4.1), with masks b_J(z_J) = 1_{χ(Π_{k∈J} c_k z_k)=c}, singleton factors ν_d(z_d), and ρ_{d(J)} = f ν at each sum.
- Lemma 4.2 (q_mask weighted Cauchy–Schwarz steps, prime substitutions) yields ≤ K_m pairwise non-parallel rows.
- Lemma 4.4 (d = \|R\|−1 further steps plus a weighted second-moment removal of the retained weights Ψ) yields (4.13).
- Prop 4.5 identifies the law of the cube root with μ_{i_{a*}} and gives (4.17), a d-cube with prime-dependent step M(p) at scale R_l/J0.
- Lemma 5.5 bounds this by the subgroup norm U^{2^d}_{Q_p}(X_l) via (5.13). TZ Bessel then gives the global U^{2^{d+1}−1}_{G_l}(X_l), and GTZ gives step 2^{d+1}−2 ≤ s.
- d ≤ K_m − 1, so **k and s depend on m only.** ✔

**(2) Divisor weights and the "mean one on linear systems" claim.**
- Prop 3.6 is the linear-forms condition for these ν, proved in the paper. ν ≥ 0, and each occurrence carries an independent draw, which is automatic because ν is a deterministic function E_σ σ1_{σ|y}.
- Every use checks primitivity (the anchor coefficient is a pool-prime monomial, or the coefficient of y is 1). It checks pairwise independence outside a fixed polynomial test T_π, and the base residue law.
- Uses I checked: E Ω = 2^{s_inv}+o(1) in Lemma 4.2; the prefactors in (4.14); the three moments in (4.16); (5.3); (5.4).
- The only place pairwise independence can fail at a rough π is when π \| D(p), where M(p) is not a unit. That is exactly the T_π event. Prop 3.6 charges it only E β_π 1_{T_π} ≪ π^{−2}, using one primitive row. I re-derived this.
- **No unverified majorant condition is used.** The dense-model step needs only Lemma 5.1, itself proved from Prop 3.6.

**(3) Count of Cauchy–Schwarz steps, function, and scale.**
- Steps: Lemma 4.2 uses q_mask = 2^m − 1, one per mask. Lemma 4.4 uses d plus one weighted second moment. (5.13) uses 2^d. θ = 2^{−(q_mask+d)} is consistent.
- Function: the tested function is g_* = ρ − F (\|g_*\| ≤ 1+ν) in §5.1, and F − S ∈ [−1,1] in §5.4. Never f alone.
- Scale: the scale is the gap scale R_l/J0 (shifts M(p)u with u < R_l/(J0 M(p))). It is not H_i or X_i. This is why (5.10) is stated at the fine gap l.

**(4) Dense model.** The paper proves it in full (Prop 5.2): finite-dimensional minimax on supp μ_i, followed by polynomial approximation of G_+ on [−K,K]. Lemma 5.1 supplies both (5.3) and the clipping bound from the moment estimate (5.4).

**(5) Nested projections and Ramsey.**
- N_{i,l′} ⊆ N_{i,l} for l < l′ because R_l \| R_{l′}.
- The comparison in (5.10) uses tuples (T,l,j_u) and (T,k_u,j_u) from the homogeneous set. Both are increasing (T < l ≤ k_u < j_u), have the same length, and so the same bin.
- **No cycle.**

**(6) Completion.**
- (2.7): lim_U P ≤ ⟨S,ψ(S)⟩ + ε ≤ 3τ + ε < 3τ + η.
- (2.11): q_m telescoping steps, each < η/(2q_m) through (4.17) and Lemma 5.5 with cube ≤ 2ζ. Then o(1) from the ρ→F step and o(1) from Corollary 3.2 (joint law over disjoint blocks). Total ≤ η/2 + o(1).
- Every error is either o(1) uniform over bounded inputs, or bounded via κ chosen before N.

**(7) Lemma 3.3 against Definition 2.1.**
- h_j = W^{w2^{N−j}}. Super-increasing exponents give h_A/h_B = W^{w·(positive integer)} for A ∈ E_B: the smallest index of the symmetric difference lies in P ⊂ A. This survives relabelling to j_1 < … < j_n.
- M is a power of W chosen after e0(w), with W^{e0+1}c_d \| M.
- H_u = R_{k_u}: divisible by M; dominates powers of P^+_{k_u}+V_{k_u} ≥ 2 + M + Π_{ℓ<u} X_{j_ℓ}; and R_{j_u} is divisible by R_{k_u}, so log X_{j_u} ≥ wR_{j_u}^w dominates powers of H_u.
- X_l are powers of two. R_l is divisible by M\|D(p)\| for every pool value, so q_p \| q_l as Lemma 5.5 needs.
- The construction order (M, then for each l: Q_l, pool, R_l, X_l) never revisits a choice. ✔
- §3.4 / Lemma 3.5: the induction (leading coefficients, small primes through Brun–Titchmarsh, ≤ O(1) primes above √Y_0 tested against the independent tuple) is correct. It gives gcd(q_p, q_{p′}) = 1 with probability 1−o(1), so Q_p + Q_{p′} = G_l.

---

## 5. Lemma 7.2 (missing corner), as used by Lemma 5.3

- The face-coordinate argument is correct. Write z = a^{−1}b. The coefficient at each proper E is (Π_{D⊊E} g_D)^{−1} z_E ∈ Γ; the top coefficient lies in G_{s+1} = {1}; so z_top ∈ Γ.
- Linear orbit cubes are (g^{b_0})_∅ (x_0)_∅ Π_j (g^{b_j})_{{j}}, which lie in C^{s+1}.
- Compactness: the image is compact because C^q ∩ Γ^{2^q} is cocompact ([14, Lemma E.10]).
- A continuous injection from a compact space into a Hausdorff space is a homeomorphism onto its image. Stone–Weierstrass and an Arzelà–Ascoli net then give finitely many recipes.
- Lemma 5.3 realises a recipe as a sum of (s+1)-dimensional, modulus-M dual tests whose inputs are recipe-selector indicators times single-vertex factors. Roots near a boundary cost (5.7) = O_s(J0^{−1}) + o(1). ✔

---

## 6. Verified line by line versus skimmed

**Verified line by line** (re-derived; displayed formulas checked on the PDF):
- Lemma 3.1, all three parts. This includes the partial-summation error φ(W)/A, the residue bound (3.2), the translation identity (3.3), and the exact dilation formula behind (3.4).
- Corollary 3.2, including the joint statement.
- Lemma 3.3: the statements, the e_j super-increasing argument, the divisibility of v_{R,k}, and the construction order.
- Lemma 3.5, the full induction and the use of Yamada.
- Prop 3.6, all of it:
  - kernel bound α_p ≥ 1;
  - single positive valuation ⇒ α_p = 1;
  - two independent rows ⇒ α_p ≤ p^{Σa−A−B};
  - (3.12);
  - the domination μ_j ≤ C_0 μ̃_j and the independent valuations;
  - E β_p ≪ p^{−2} in both branches;
  - the product bound ≪ 1/w.
- The consequences paragraph after Prop 3.6 (2^q P(ℰ) main terms, cancellation, o(1) mass of exceptional events).
- Lemma 4.1, including E A_l² and ‖A_l − 1‖_2 ≤ S_l^{−1/2}.
- Lemma 4.2:
  - both substitution cases and their invariant rows;
  - why W_R(α_p t) = W_R(t), since pool primes exceed V;
  - the weighted Cauchy–Schwarz (4.7);
  - why only one weight survives on invariant rows;
  - the p = q diagonal bound V^{O(1)}/S_l;
  - absorption to (q,p), (p,q);
  - non-parallelism by specialisation and by the exponent argument;
  - the distinguished row stays non-invariant;
  - the K_m count.
- Lemma 4.3: the kernel-vector construction, the integrality of v_R and v_0 on good tuples (S \| W^{e0−1}, W^{e0+1}c_k \| M), the responses (4.11), and the exceptional-test list.
- Lemma 4.4: (4.14); all row-distinctness checks; t = d·2^{d−1}; (4.16) and E B(H−2^t)² = o(1).
- Prop 4.5: Y_* = kz_{a*} + h; (b,k) = 1; (4.19)–(4.20); averaging over z_j; exponent θ.
- Lemma 5.1:
  - the existence of the a_j;
  - the translation responses;
  - elimination of the non-root rows;
  - the main-term vanishing;
  - Jensen and (5.4);
  - the clipping tail 2K^{p−b}A_*^b;
  - the Hölder transfer.
- Prop 5.2: the minimax identity, ⟨ρ,G⟩ − ⟨1,G_+⟩ ≤ ⟨ν−1,G_+⟩, the polynomial step, the diagonal in J0.
- Lemma 5.3: recipe selection and (5.7).
- (5.8) and Lemma 5.4, including the clipping-decreases-distance-to-PF argument.
- Lemma 5.5:
  - periodisation cost;
  - the density ≤ 2J0;
  - the (5.13) Cauchy–Schwarz count;
  - Bézout;
  - Bessel;
  - (5.14), including \|A_L\| ≥ C(L+t, t+1);
  - the cell-weight identity and the δ^{2^t}/2 mass;
  - the inverse theorem per cell;
  - the projection lower bound.
- §5.4: the choice order, calibration, and both telescopes.
- Lemma 7.2, and Lemma 7.1's face decomposition as far as 7.2 uses it.

**Skimmed** (believed standard; not re-derived):
- Lemma 3.3: the p-adic null-set / Fubini argument for e0(w), and the PNT-in-APs residue uniformity for pools modulo the fixed Q_l (Selberg not fetched).
- The Remark 3.4 diagonal over countably many templates. Standard, but its "error bounds at stage j are ≤ 1/j for w ≥ w_j" relies on each stage's construction having explicit o(1) rates. I accept this and did not audit it per template.
- Prop 3.6's rational-row extension paragraph.
- Lemma 7.1's claims that C^q is invariant under reflections and that the lower-central terms are rational. These are standard, and [14, App. E] has them.
- Exact numeric constants in (4.20), in the boundary-strip count behind (5.7), and in the symmetric-difference count behind (5.14). I checked orders of magnitude only.
- How much of GI(2) the GTZ introduction attributes to [21] (Green–Tao U³). I accepted GTZ's own statement.
- §§6–8 (Alignment) and §2 are out of scope. Principle 2.3 does not use them, except Lemma 7.2, which I checked.

## 7. Verdict

**HOLDS AS READ** for the proof of Principle 2.3 (§§3–5) and Lemma 7.2.
- No fatal error, cycle, citation mismatch, or uniformity failure found.
- Residual risk is confined to the skim list above: standard number-theoretic and Lie-theoretic inputs, and exact constants.
- If the paper fails, my reading says the failure is outside this scope. The Alignment Principle (§§6–8) is the obvious place, because it carries the "δ independent of model complexity" claim that §2.5 needs.

---

## 8. Coordinator request: line-by-line read of the two §5.3 external inputs

Context from the coordinator: a third-party Lean formalisation swaps out exactly these two inputs. I re-read both applications against the sources, clause by clause. **Both hold.** Every difference between the paper's statement and the source is listed below, with the reason it is harmless.

### (a) Tao–Ziegler [34, Thm 1.23] as used in (5.11) and "Combining the subgroups" (pp. 34, 36)

Paper (p. 34): "the subgroup case of the finitary qualitative Bessel inequality [34, Theorem 1.23] says that for each k there is a function b_k(δ) → 0 as δ ↓ 0 such that E_{α,α′}‖h‖_{U^{2k−1}_{Q_α+Q_α′}(X)} ≤ δ ⟹ E_α‖h‖_{U^k_{Q_α}(X)} ≤ b_k(δ), |h| ≤ 1. The bound is independent of the finite family, the group, and the probability system. Finite subgroups are rank-zero coset progressions in that Theorem. Its dilations leave them unchanged, and its multiset sum of two subgroups induces uniform measure on their subgroup sum. … Rational probability weights on indices are implemented by repetition of indices; arbitrary finite weights follow by approximation. We choose b_k nondecreasing and enlarge its argument by a factor of two to absorb the approximation slack".

Source (TZ v4 = Discrete Anal. 2016:13, Thm 1.23): "Let (Q_i)_{i∈I} be a finite non-empty family of coset progressions Q_i, all of rank at most r, in an additive group G. Let (X,T) be a G-system, and let d be a positive integer. Let f lie in the unit ball of L∞(X), and suppose that E_{i,j∈I}‖f‖_{U^{2d−1}_{εQ_i+εQ_j}(X)} ≤ ε (15) for some ε > 0. Then E_{i∈I}‖f‖_{U^d_{Q_i}(X)} ≤ c(ε) (16) where c : (0,+∞) → (0,+∞) is a function such that c(ε) → 0 as ε → 0. Furthermore, c depends only on r and d. (In particular, c is independent of the size of I.)"

Clause-by-clause differences:

1. **Dilates.** The source's hypothesis uses εQ_i + εQ_j, with the same ε as the threshold. The paper drops the dilates.
   - Def 1.10 reads: "Q = H + {n_1v_1+…+n_rv_r : |n_i| ≤ N_i} … εQ := H + {… |n_i| ≤ εN_i}". With rank r = 0, εQ = H. So dropping the dilates is exact, not an approximation. ✔
2. **Multiset sum versus "uniform measure on the subgroup sum".**
   - Def 1.6: "A + B := {a_i + b_j}, where multiplicity is counted", and Def 1.10: "we view H as a multiset in which each element has an equal multiplicity".
   - So H_1 + H_2 lists each element of the subgroup H_1+H_2 exactly |H_1∩H_2| times, which is the uniform measure. ✔
   - When gcd(q_p, q_{p′}) = 1 and both divide q_l, Bézout gives Q_p+Q_{p′} = G_l, so the norm equals ‖h‖_{U^{2k−1}_{G_l}(X_l)} exactly. The exceptional pairs have probability o(1) by Lemma 3.5, and the norm is ≤ 1 there. ✔
3. **Norm convention.**
   - TZ Def 1.9: "‖f‖^{2^d}_{U^d_Q(X)} := E_{h_1,…,h_d,h′_1,…,h′_d∈Q} ∫_X Δ_{h_1,h′_1}…Δ_{h_d,h′_d} f dμ, ∆_{h,h′}f := (T^h f)(\overline{T^{h′}f})".
   - The paper (p. 34) uses one variable per direction: "‖h‖^{2^t}_{U^t_Q(X)} = E_{x∈X} E_{v_1,…,v_t∈Q} Π_ω h(T^{Σ_{j∈ω}v_j}x)".
   - For a subgroup (or a uniform multiset on one), shift by T^{−Σh_j} and put v_j = h′_j − h_j, which is again uniform on Q. The two conventions are identical. ✔
4. **Weighted index law versus uniform average over I.**
   - TZ average uniformly over the finite family I. The paper averages over prime tuples p under the normalised good-tuple law, which has irrational harmonic weights.
   - "Family" means an indexed family. TZ's own proof (§8) samples "M indices a_1,…,a_M uniformly and independently from I (with replacement)", so repeated members are admissible.
   - Rational weights therefore become repetitions. For irrational weights, approximate within total variation η′:
     - the hypothesis average moves by ≤ 2η′ and the conclusion average by ≤ η′, since all norms are ≤ 1;
     - so with η′ ≤ δ/2, E ≤ δ implies the approximating average is ≤ 2δ, hence E_α ≤ c(2δ) + η′;
     - letting η′ → 0 gives ≤ c(2δ). This is the paper's "enlarge its argument by a factor of two". ✔
5. **Monotonicity.** TZ do not say c is monotone. Replacing c by sup_{0<δ′≤δ} c(δ′) is finite and still tends to 0, because c(δ′) → 0. "We choose b_k nondecreasing" is legitimate. ✔
6. **Side conditions.**
   - TZ's G-system definition requires G to be at most countable and X to be countably generated modulo null sets. Here G = Z/q_lZ is finite and X_l is finite. ✔
   - X_l, a weighted disjoint union of cells with the G_l-action by translation inside each cell, is a G_l-system in exactly the sense of Def 1.7. ✔
   - f must lie in the unit ball of L∞; h ∈ [−1,1]. ✔
7. **Indices.** The paper's k is TZ's d, and the hypothesis order 2k−1 matches TZ's 2d−1. ✔

**Verdict (a): MATCH.** (5.11) is a correct specialisation of Thm 1.23 to rank-0 progressions with weighted indices. I found no normalisation mismatch.

### (b) The GTZ inverse theorem on one cyclic cell (pp. 34–37)

Paper (pp. 34–35): "a 1-bounded function on an integer interval with U^t norm at least δ correlates by at least c_t(δ) > 0 with a sequence Φ(g^k x) on a nilmanifold of step at most t − 1. There is a finite list … with connected simply connected groups … ‖Φ‖∞ ≤ 1 and its Lipschitz bound depend only on t, δ. … The interval norm here is the normalized cube mean with all vertices in the interval, equivalently the zero-extension norm divided by the norm of the interval indicator in a sufficiently large auxiliary cyclic group."

Source (GTZ v5, quoted in §3): f : [N] → C bounded by 1 with ‖f‖_{U^{s+1}[N]} ⩾ δ ⟹ there are G/Γ ∈ M_{s,δ}, g, and F with Lipschitz constant ≤ C(s,δ) such that |E_{n∈[N]} f(n)F(g^n x)| ⩾ c(s,δ). The interval norm is ‖f‖_{U^d[N]} := ‖f̃‖_{U^d(G)}/‖1_{[N]}‖_{U^d(G)}, G = Z/ÑZ, Ñ ⩾ 2^d N.

Step-by-step check:

1. **Norm equivalence.**
   - With Ñ ≥ 2^t N, a cube in Z/ÑZ whose 2^t vertices all lie in the image of [N] lifts uniquely to an integer cube with |h_j| < N and no wrap-around. Every partial sum then has absolute value < tN ≤ Ñ/2.
   - So ‖f‖^{2^t}_{U^t[N]} = |A_N|^{−1} Σ_{(x,a)∈A_N} Π_ω f(x+Σ_{j∈ω}a_j), where A_N is the set of integer cubes, increments of either sign allowed, with every vertex in [N].
   - This is the paper's A_L (p. 36), with [0,L) in place of [1,N]. ✔
2. **(5.14): ‖v^per‖^{2^t}_{U^t[Kq]} = ‖v‖^{2^t}_{U^t(Z/qZ)} + O_t(K^{−1}).**
   - For every integer cube point y, E_{r∈{0..q−1}^{t+1}} F_per(y+r) equals the cyclic mean exactly: (x+r_0, a_j+r_j) mod q is uniform on (Z/q)^{t+1} and v^per is q-periodic on Z.
   - Hence |E_{A_L}F − cyclic mean| ≤ E_r |(A_L+r) △ A_L| / |A_L|.
   - For a point in A_L \ (A_L+r), some vertex ω lies in [0, (t+1)(q−1)). That vertex together with its t neighbours determines (x,a), and the neighbours lie in [0,L). This gives ≤ (t+1)q·L^t points per ω. The other half of the symmetric difference is handled the same way.
   - |A_L| ≥ C(L+t, t+1) ≥ L^{t+1}/(t+1)! counts the nonnegative-increment cubes. The ratio is O_t(q/L) = O_t(1/K). ✔
   - The estimate is for 2^t-th powers, as the paper states. So "cyclic norm ≥ δ/2 ⟹ interval norm ≥ δ/4 for K ≥ K(t,δ)" holds. ✔
3. **Applying GTZ on [Kq].** f = v^per on [0,Kq) is real and in [−1,1], hence bounded in magnitude by 1. The shift from [N] = {1,…,N} to [0,Kq) re-indexes n ↦ n+1, which sends F(g^n x) to F(g^m(gx)): a base-point change only. ✔
4. **"Splitting the correlation into its K period averages shows that one period has correlation of at least the same modulus."**
   - E_{n∈[0,Kq)} = K^{−1} Σ_{j<K} E_{n∈[jq,(j+1)q)}, with equal weights because N = Kq exactly. So some j has |E_{m∈[0,q)} v(m)F(g^{m+jq}x)| ≥ c.
   - Since g^{m+jq}x = g^m(g^{jq}x), this is the same nilmanifold, the same g and the same F (so the same Lipschitz constant), with base point g^{jq}x. That is exactly "only replaces the nilsequence base point by a translate g^{jq}x". ✔
   - The correlator is not periodic, and is not claimed to be. It is used only on the fixed representatives [0,q) of the cell's progression indices, which is what membership in N_{i,l} requires: "a nilsequence in the progression index" on each R_l-interval × residue mod M piece. ✔
5. **Real part.** GTZ's F is complex. Re(e^{iθ}F(g^m x′)) is real, bounded by 1, and Lipschitz with the same constant, and its pairing with the real h_C equals the modulus. ✔
6. **Uniform complexity across cells.** Every good cell has interval norm ≥ δ/4, so every correlator comes from the single finite list M_{t−1,δ/4} with Lipschitz bound C(t−1,δ/4).
   - GTZ's s-step nilmanifolds are, by their definition, "G/Γ, where G is a connected, simply-connected nilpotent Lie group of step at most s". This matches Def 2.2.
   - The piecewise family V, set to 0 on cells that are not good, discarded partial intervals and non-unit residues, therefore has complexity depending on (t,δ) only. That is what makes κ independent of N, the gap and w. ✔
7. **Cell mass and projection.**
   - The identity ‖h‖^{2^t}_{U^t_{G_l}(X_l)} = Σ_C α_C ‖h_C‖^{2^t}_{U^t(G_l)} is exact.
   - Cells with ‖h_C‖ < δ/2 contribute < (δ/2)^{2^t}, so good cells carry mass ≥ δ^{2^t} − (δ/2)^{2^t} ≥ δ^{2^t}/2.
   - Hence ⟨h,V⟩ ≥ ½δ^{2^t}c_t(δ/4) + o(1), with the o(1) coming from replacing uniform measure by μ_i in each cell (R_l/X_i → 0).
   - Since ‖V‖ ≤ 1, ‖P_{i,l}h‖ ≥ that bound. ✔
8. **Degree bookkeeping.**
   - The d-cube with Q_p-increments of density ≤ (2J0)^d needs 1 (density) + (2^d − 1) (non-root vertices) Cauchy–Schwarz eliminations. The root's copies form a U^k_{Q_p} cube with **k = 2^d** (5.13).
   - Bessel raises this to **t = 2k − 1 = 2^{d+1} − 1** on G_l.
   - GTZ GI(t−1) gives **step t − 1 = 2(2^d) − 2**.
   - The hypothesis of Lemma 5.5, "Assume 2(2^d) − 2 ≤ s", is identical to (5.1), "s + 1 ≥ 2(2^d) − 1". ✔
   - Which GI(s) is actually used: |R| ≥ 2^m − 1 ≥ 3, because rows never merge and the distinguished row doubles at each step. So d ≥ 2 and t ≥ 7, and only GTZ Theorem 1.3 (s ≥ 3) is invoked. The paper's mention of t = 2, 3 (GI(1), GI(2)) covers cases that never occur.

**Verdict (b): MATCH.** The interval inverse theorem is used on the periodic extension exactly as GTZ state it. The cyclic-to-interval comparison (5.14) and the "one period, translated base point" step are correct as written, and the degree bookkeeping is consistent with (5.1).

**Bearing on the Lean swap.** The formalisation's replacement of these two inputs (Kravitz–Kuca–Leng box-norm concatenation; a cyclic inverse theorem for polynomial orbits plus BCH linearisation) tells us those results were easier to formalise, or already available, in Lean. It is not evidence that the paper's versions are misquoted. On my reading neither is misquoted, and neither application omits a hypothesis. **Verdict for §5.3 unchanged: HOLDS AS READ.**
