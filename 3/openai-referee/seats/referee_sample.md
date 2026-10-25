# Referee seat "sample": §6 (pp. 40–44), §7 (pp. 44–60), and Schoen–Sisask [43, Thm 5.4] where the paper applies it (Lemma C.2, p. 101)

Paper: /tmp/oaimath/159/paper/paper.pdf (198 pp.). I read the math from the rendered PDF pages, not the text extraction.

## Scope read (pages)
- **Line by line (PDF):** pp. 40–60, i.e. all of §6 and §7, including the tail of the §5 proof at the top of p. 40.
- **Read to check interfaces** (statements, and the proof passages my scope leans on):
  - pp. 8–14: §2, i.e. Thm 2.1, Lemma 2.2, Def 2.3, §2.8.
  - pp. 14–15, 18–24: Lemma 3.1, Lemma 3.2, Lemma 3.3, Thm 3.4 and the cold-clause proof, §3.5 including (3.6) and e_j.
  - pp. 24–25: Prop 4.1 (statement only).
  - pp. 29–33: Lemmas 4.5, 4.6, 4.7.
  - pp. 36–39: Lemmas 5.1, 5.2, 5.3.
  - pp. 69–70: Prop 9.1 and (9.1). This is where Cor 7.9's output is consumed, and where Lemma 6.1(3) is used.
  - pp. 80–81: §10.4 and Prop 10.4.
  - pp. 100–102: Thm C.1, Lemma C.2, and the use of (C.4) on p. 105.
  - Lemma H.2 statement, including (H.5).
- **External source:** Schoen–Sisask, arXiv:1408.2568, plus the published Forum Math. Sigma version (details below).

## Method
- Re-derived every displayed inequality in §6.2 and §7.3, and the arithmetic in (7.8)–(7.9), Cor 7.9, the deaveraging step of Prop 7.8, Lemma 7.1, and the conditional-averaging step of §7.1.
- For each invocation of a §3/§4/§5 result, compared the form used with the cited statement.
- For Lemma 7.6, re-proved the algebra.
- For [43, Thm 5.4], quoted the source and matched every hypothesis and every returned quantity against Lemma C.2.
- Tracked warm, cold-pre and late dependencies against Def 2.3 throughout. I also tracked:
  - whether any constant depends on the incoming certificate surplus;
  - whether any constant depends on the iteration count;
  - whether errors summed over primes, witnesses or layers are requested uniformly.

## The inductive score (§7.1, written out)
At entry to layer j, for j = D, D−1, …, 1, the "ascent format" (Def 7.2) asks for the following, on the parameter box T of a layer-j path ψ (a child of a fixed parent box U with a fixed feasible center c):
- a slice Σ ⊂ T of warm cost; and
- the full-mass score

  Score_j = |T|^{-1} Σ_{t∈Σ} [ f_0(ψ(t)) · 1_{no bad}(t)^{[j≤s]} · Σ_{tuples} ∏_{abs a} U^-_{r_a,c_a}(S_t(a)) · ∏_{i>j} U^-_{r_i,l'_i}(b_i − C_i(u,b_{≤i−1})) − λ · Σ_{tuples} ∏_{abs a} U^+(…) · ∏_{i>j} U^+(…) ] ≥ δ.

Its requirements:
- log(1/δ) is warm at layer j: no Q_i with i ≤ j enters.
- f_0 is the pulled-back input. It already carries the flag masks of the lower active layers.
- U^∓ are the paired product cutoffs of (7.1). They act on the actual residuals of the determining blocks i > j, with radii whose log-loss relative to w_i is warm at layer i, and on the absolute slots.
- Each unsigned sum is ≤ 1, by triangular uniqueness.
- Determining polynomials never use absolute slots. Absolute polynomials may use b_i only for j < i ≤ s. All identities are formal.

**What "inductive" means.** The induction runs over layers in descending order, D → 1, which is the reverse of the sampling order 1 → D.
- **Base case:** Lemma 7.1 applied to the Lemma 2.2 patch on a productive terminal path. This gives the format at entry to layer D, with no determining slots i > D.
- **Hypothesis at stage j:** the ascent format holds on a warm-inverse fraction κ_j of the layer-j children of a fixed parent and feasible center.
- **Step, passive layers j > s:** Prop 7.8, then Cor 7.9, then Prop 9.1 (§9, outside this scope). The output is the format at entry to layer j−1 on the parent, with the raw block b_j added. Its score may carry the factor m_j, so log(1/δ_{j−1}) may charge Q_j, which is warm at j−1.
- **Step, active layers:** Theorem 8.2 instead (outside this scope).
- **Fractions:** the conditional-averaging step on p. 46 turns "total productive probability ≥ κ" into "parents of probability ≥ κ/2, each with conditional productive probability ≥ κ/2". I checked this: E q ≥ κ with 0 ≤ q ≤ 1 implies Pr(q ≥ κ/2) ≥ κ/2. A center is then fixed. So κ_{j−1} ≥ κ_j/4, κ_D ≥ ηa, and κ_1 ≥ ηa·4^{-D}, which is warm.
- **The fraction never multiplies the score.** κ is only used to guarantee that some productive child lies outside Prop 7.4's exceptional set. The parent score comes from K, which is a parent-level integral.
- **Nested induction:** inside Prop 7.8 there is a second induction, on the degree (≤ s) of G^0, through Lemma 7.6.

## Findings

**FATAL: none. GAP: none.**

### EXPOSITION
**E1 (p. 43, l. ~2258).** Quoted: "If a spatial boundary cutoff has thickness θ and mean O(nθ) on this parent, the marginal rank estimate proved with Lemma 5.1 gives E_U 1_boundary 1_current strict ≤ O(nθ)e_j + δ".
- Lemma 5.1's stated marginal clause (pp. 36–37) is about the chart weight ν = χ(C(u)−c)/a_χ of (5.1). That chart has mass a_χ ≍ m_j around one center.
- What is needed here is equidistribution of C_j(u) mod Λ against the torus majorant G_j of the strict constraint, which has mass ≤ e_j, restricted to a boundary strip.
- This follows from Lemma 5.1's *proof*: Fourier-expand G_j at cold-pre cost (its transition scale is ~γw_j), then kill the nontrivial characters using rank R_j, which is late at j.
- But it is not the lemma's statement. Repairable from the paper's own tools; it should be stated as a variant.

**E2 (p. 41, (6.3)).** The exceptional depths b_ϖ in "∏_{ϖ≤Z} ϖ^{b_ϖ} ≤ D_0'", and the phrase "modular rank hypotheses through Z", are undefined in §6. They are b_p and hypothesis (H.2) of Lemma H.2. A cross-reference is missing.

**E3.** The bare qualifier "pre" is used without definition in Def 2.3, in phrases such as "pre bound", "pre-cost", "pre-count", "pre-small" (Lemma 7.3, Prop 7.4, Cor 7.9).
- The only operative definitions are on p. 41 ("warm pre at a passive layer and cold pre at an active layer") and p. 50 ("The budget is warm for passive uses and cold pre otherwise").
- The intended reading is consistent everywhere I checked. It should be stated once.

**E4 (p. 44, l. ~2335).** Quoted: "We now return from a productive terminal path to its ancestors". The argument actually returns from a warm-inverse-probability family of productive paths at each fixed parent and center (p. 46; hypothesis of Prop 7.8), not from one path. Wording only.

**E5 (p. 48, (7.6)).** Quoted: "Using the trivial joint probability bound on these bad pairs gives … O(ℓP^{2ℓ−N+2J})". This is correct but wasteful: bounding by P^{-J} instead of 1 gives P^{2ℓ−N+J}. Harmless, since N is a free structural polynomial.

**E6 (p. 41, Lemma 6.1).** Quoted: "the full number of solutions is at most (1+ϵ_ϖ)ϖ^{v_f ℓ−J}". "Full number" means the count N_0 of full-column-rank solutions, as in the proof on p. 48. It is not the count of all solutions. Should say so.

**E7 (p. 101, Lemma C.2 and p. 100).**
- The paper's "regular" ("|B_{1+t}| = (1+O(D|t|))|B| (|t| ≤ c/D)") is an O-constant version of Schoen–Sisask's Def 4.3, which has the explicit constant 12 and range |δ| ≤ 1/12d. SS Thm 5.4 assumes regularity in *their* sense.
- B_0 is chosen as "a regular dilate", which exists in SS's sense by their Lemma 4.4. The text should say which notion is meant.
- Also quoted: "a subset of relative density greater than σ". SS's hypothesis is μ_B(S) ≥ σ. This does not affect the argument (σ = 1/2, with S = B_0 of density 1).

**E8 (p. 42, statement of Prop 6.2).** The phrase "after harmless adjustment of the loss constants" is superfluous. The proof yields Pr(Y ≥ (1−2η)a) ≥ ηa directly from EY ≥ (1−η)a.

## Line-by-line results (what holds)

### Prop 6.2 (pp. 42–44), and its use in §10.4
**The recurrences close.**
- e_j depends only on W_j, l_j, w_j, γ, not on the prefix (p. 24). So s_j = S_j/∏_{i≥j}e_i and t*_j = T_j/∏_{i≥j}e_i are legitimate normalizations.
- (6.6) divided by ∏_{i>j}e_i gives s_{j+1} ≥ (1−ε)s_j − O(εa). (6.7) divided by ∏_{i≥j}e_i gives t*_j ≥ (1−ε)t*_{j+1} − O(ε). Stopped parents contribute 0 to the right side, so the averaged forms hold.
- t*_{D+1} = Pr(survive) = 1 − O(Dε), hence T_1 ≥ (1−O(Dε))∏e_i.

**The derivation of (6.6).**
- Child mass averaged over unrestricted centers: ≥ (1−ε)E_U[F·1_{¬strip}] − δ, by Lemma 3.2(4), with F = input × strict_j × strict_{>j}.
- strict_j at a site forces c ∈ C_j, because ‖b_{j,0} − c − l_j‖ < w_j + v < (1+γ/2)w_j. So the unrestricted average equals e_j × the average over feasible centers.
- The strip is removed at cost O(nθ)e_j + δ.
- The flag loss is O(c*)·S, by Lemma 6.1(4).
- Requests: θ ≪ εa∏_{i>j}e_i/n (warm); δ ≪ a∏_{i≥j}e_i (cold).

**Requested error bounds.** Rank stop at h: ≪ εa∏_{i≥h}e_i. Output discards at h: ≪ εa∏_{i>h}e_i. These match the statement's "data at layers ≥ h", and log(1/a) ≤ p.

**No surplus dependence.**
- The certificate is used only as S_1 ≥ aT_1, i.e. the non-strict inequality. So s_1 ≥ a(1−O(Dε)) and s_{D+1} ≥ (1−O(Dε))a.
- No request involves E fB^- − aEB^+.
- Pr(Y ≥ (1−2η)a) ≥ EY − (1−2η)a ≥ ηa holds because Y ∈ [0,1], with stopped paths counted as Y = 0 in the same tree measure.

**Supporting facts.**
- The progression-free property survives injective integer-affine pullback, and masks only remove points.
- log(1/e_j) is cold-pre and independent of the height of W_j. This holds because Haar measure on W/Λ counts sheets (Lemma 3.1, m_j ≍ v^{dim W}∏_i max(1/K_i, v)). I first suspected a height dependence here; it is not there.

**Verdict on the §10.4 use.** §10.4 says Prop 6.2 "supplies productive terminal paths on a fraction at least a fixed multiple of a, at a threshold differing from a by a sufficiently small fixed proportion … does not charge the inverse of the incoming strict surplus". Prop 6.2 as stated gives exactly this:
- the fraction is ηa;
- the threshold is (1−2η)a, applied at preparation's discounted threshold a' = (1−ε')a;
- no constant depends on the surplus.

The one external requirement is that preparation (Prop 4.1) delivers rank-stop bounds ≪ εa∏_{i≥h}e_i. Those are cold at h, which Def 2.3 and Prop 4.1's "prescribed bound" permit. Whether §4 achieves this with a warm width loss belongs to §4's referee.

### Lemma 6.1, and its proof in §7.3 (pp. 41–42, 48–50)
**Uniform-model assertions.**
- Pr((6.4)) = P^{-J} exactly. This holds by surjectivity of substitution x ← x_0 + V(s,h) on nonconstant coefficients: use a left inverse of a full-rank V; fixed contributions are translations.
- (7.5)–(7.7) hold: direct-sum pairs and triples give independent restrictions, and the bad proportions are O(ℓP^{2ℓ−N}) and O(ℓP^{3ℓ−N}).
- The Jacobian argument holds. Only transverse-exponent-one monomials matter at y = 0. N−ℓ independent uniform vectors fail to span F^{n_der} with probability O(P^{n_der−N+ℓ}). Spanning gives all J equations, since every nonconstant monomial of degree ≤ d_i equals a plane coordinate times a monomial of degree ≤ d_i − 1.
- (Also: the Jacobian condition is basepoint-independent along the plane, so the union over basepoints is not even needed for it.)
- Chebyshev at ε_P/2 with a union over the P^ℓ basepoints, followed by Markov on the deleted count, gives item 2 with C = 2, once N ≫ ℓ, J, n_der, log(1/c*).

**Item 1.**
- Selection is plane-invariant. I checked that V solves (6.4) at every translated basepoint: b(x'+V(s,h), r_0+h_0+h) = b(x', r_0+h_0) + s.
- w_{ϖ,a} = w_{ϖ,1} follows from Hensel's lemma with a rank-J Jacobian mod ϖ. Each solution mod ϖ^a has exactly ϖ^{Nℓ−J} lifts, and a ≥ 1 gives (ϖ^a)² ≡ 0 mod ϖ^{a+1}.

**Item 3.**
- W_* ≤ ∏(1 + c*ϖ^{-2}) = 1 + O(c*), and W_* ≥ 1 − O(c*) off bad flags. Both are deterministic, so no simultaneous law mod 𝔐 is needed.
- The joint bad-flag bound ∏c*ϖ^{-10} ≤ d^{-10} follows from independence across primes via the Chinese remainder theorem.
- Its consumer, (9.1) on p. 70, re-checked: W_*(P − λ'N) ≥ (1−η)(1_{nobad}P − λN) with λ' = (1−η)λ/(1+η).

**Item 4.** Flag modes that factor through the site have constant row 0, hence are trivial. The remaining dependence is through A_sp, with a per-slope-tuple site upper density of 1+o(1), and per-prime errors are summed explicitly through Z. This rests on Lemma 3.2(2),(4) and Lemma F.7 (not re-proved).

### §7.2 and Lemma 7.3
- The normalizations are consistent: (7.3) times the bounded inactive-grid, congruence and real densities gives a site weight ≤ Bm_j^{-1}, so K(1) = O(1) on the chart.
- The cap on d comes from Lemma H.2 ((H.3)/(H.4) with D_0' warm). Its "homogeneous part independent of z" hypothesis holds: the t_∥-degree-h part of a polynomial of total degree ≤ h has no t_I.
- Lemma G.4 smoothing and the Fourier truncation: read, not re-proved.

### Prop 7.4 (pp. 50–52)
- The structure is sound. Thm 3.4 is applied at testing degree 0, so the warm clause is available (r = 0 < j). Thm 3.4 holds "uniformly in the center and the site input", so a union bound over a menu that depends on parent data (but not on the individual child) is legitimate.
- Atom moduli ≤ Z are covered by 𝔐 = lcm(1..Z).
- (7.8) checked. The truncation is exact when ∏bad ≤ T, and otherwise errs by at most T (the paper says 1+T).
- Witness: either a bad ϖ > T, or a squarefree d ∈ (T, T²]. Exceptional probability O(T^{-9}), giving error O(T^{-8}).
- (7.9) checked: log Q_d ≤ ω(d) log Z ≤ (2 log T/log 2)·log Z.
- (7.10) checked, with the errors summed over ≤ Z + T² witnesses.

### Lemma 7.1 (p. 45)
- The approximate-identity error is ≤ C·Lip(Φ)·poly(d_0')·r.
- At most one tuple contributes on the enlarged union.
- Averaging over c with weight Φ gives ≥ V_-[EfB − λ(V_+/V_-)EB] − err ≥ V_-σ/2.
- Since ∫Φ ≤ 2^{-d'}, some center has score ≥ V_-σ/2.
- log(1/V_-) ≲ d' log(2/r). No width enters.

### Lemma 7.5 (pp. 52–54)
The logic is consistent with Def 7.2(iii). Determining slots are ordered before absolute ones, with absolute weights exceeding theirs. "Forget the absolute slots" is a homomorphism because determining maps have no absolute argument. The shear normalization is cited from Lemma D.5 (not re-proved).

### Lemma 7.6 (p. 55)
Re-proved:
- H_i ⊇ G_{i+1}, so the H_i are nested.
- [H_i, H_j] ⊆ H_{i+j}, from the graded subalgebra.
- π(H_i) = H_{F,i}, using a lift in G_{i+1} ⊆ H_i and strongness.
- (7.12) is injective by top-layer injectivity, and onto by the unique correction z ∈ H_r ⊆ H_i at every layer.
- Also checked the injectivity claim on p. 56: v ∈ 𝔳_r with trivial projection has zero partner coordinates. Its G^0-coordinate lies in ker π^0 ∩ G^0_r and is annihilated by the basis frequencies, so it lies in L.

### Lemma 7.7 (pp. 56–57)
Degree d ≤ s < j, so there is no β argument. The uses of Lemma 4.6 and Lemma 4.7 are checked in the interface list below.

### Prop 7.8 (pp. 57–59)
- Deaveraging checked. A signed X ≤ B with EX ≥ δ_1 has Pr(X ≥ δ_1/2) ≥ δ_1/(2B). Fubini gives one translation for ≥ κδ_1/(2B) of the paths.
- J-input Markov checked: Σ_h E e_h/τ ≤ κ/4.
- Partner degrees are ≤ s < j, so the warm clause of Thm 3.4 applies.
- The number of target discounts is bounded by the degree s, not by the pivot or partner count. The pivot count enters only the error budgets.

### Cor 7.9 (pp. 59–60)
- From (1−η)B_± ≤ A_± ≤ (1+η)B_±: B_- − λ(1−η)/(1+η)·B_+ ≥ (A_- − λA_+)/(1+η). So P_0 is independent of the surplus.
- The comparison is pointwise in site and inactive data. The CRT separation needs ℓ ∤ q, which is the stated condition.
- ‖d_ℓ − 1‖_∞ ≤ 2ℓ^{-2} is exactly (H.5) (b_p = e_p = 0, P ≥ m+2).
- log M_* ≤ (#{ϖ ≤ P_0} + log_2 D_0' + log_2 q)·log Z.
- The output matches Prop 9.1's stated hypotheses on p. 69 ("Corollary 7.9 leaves a fixed polynomial orbit and a matching modulus M_* of warm log cost … full-mass surplus at least δ, δ^{-1} warm").

### Interfaces with §3/§4/§5
For each: where it is used, what is used, and whether that is the cited statement.
1. **Lemma 3.1** (p. 42): log(1/e_j) is cold-pre via a ball with room γw_j/2 around the root torus point. This is Lemma 3.1's lower-bound clause, independent of height. ✓
2. **Lemma 3.2(4)** (p. 43): one-site (1−ε) lower bound off a warm strip, and (1+ε) upper bound, each with a cold-pre additive error, for every nonnegative F ≤ 1. Used verbatim. ✓
3. **Lemma 5.1** (p. 43): see E1. The form used is a variant, not the statement.
4. **Prop 4.1** (p. 42): only "every rank-stop probability … at most its prescribed bound" is used, with the bounds cold at their own layer. ✓ This matches the statement; whether it can be achieved is out of scope.
5. **Lemma 3.2(2)** (pp. 41, 49–50): product residue laws at individual moduli; pure-free coefficients uniform in all nonconstant degrees; non-site-mode removal of Lemma F.7 at cold-pre cost. Flags exist only at active layers, where Z is cold pre. ✓
6. **Lemma 3.2(1)** (p. 45): the lift identity (3.4). ✓
7. **Theorem 3.4** (Prop 7.4, §7.7, Prop 7.8): warm clause with r ∈ {0, …, s} and r < j (j > s in the passive uses). Uniform in center and input. Probabilities refer to the law before selection. ✓
8. **Lemma 4.7** (Lemma 7.7): its hypotheses are supplied with warm bounds, which are a subset of the cold-pre bounds it requires. Lemma 7.7 quotes a *weaker* conclusion (cold-pre bounds) than Lemma 4.7 provides (B·exp(poly)), then sharpens it itself. Nothing stronger than the statement is assumed. ✓
9. **Lemma 4.6** (Lemma 7.7): δ is chosen below the warm-inverse fraction. log D_0 ≤ poly(d + n + log(2/δ)), independent of H. H is forecast before the late choices. Used exactly as stated. ✓
10. **Lemma 5.3** (Prop 7.4, through "Lemma G.11 … in the warm case its inner product is the normalized chart measure"): G.11 with a general probability measure, as Lemma 5.3 asserts. ✓

## External inputs checked
**Schoen–Sisask, "Roth's theorem for four variables and additive structures in sums of sparse sets".**
- arXiv:1408.2568: **only v1 exists** (submission history: v1, Mon 11 Aug 2014). PDF at /tmp/oaimath/159/refs/1408.2568/ss_v1.pdf.
- Published version, Forum Math. Sigma 4 (2016) e5, fetched from Cambridge Core: refs/1408.2568/fms.pdf.
- Theorem 5.4 has the same number and the same statement in both.
- Conventions in both: f∗g(x) = Σ_y f(y)g(x−y), unnormalized; Bohr(Γ,ρ) = {x : |γ(x)−1| ≤ ρ ∀γ}; a sub-Bohr set B' ≤ B means Γ' ⊇ Γ and ρ' ≤ ρ.

**SS Thm 5.4, quoted from v1:**
"Let ε ∈ (0,1). Let A, M, L be subsets of a finite abelian group G, and let B ⊆ G be a regular Bohr set of rank d and radius ρ. Suppose |A + S| ⩽ K|A| for a subset S ⊆ B with µ_B(S) ⩾ σ > 0, and assume η := |M|/|L| ⩽ 1. Then there is a regular Bohr set B′ ⩽ B of rank at most d + d′ and radius at least ρεη^{1/2}/d²d′, where d′ ≪ ε^{−2} log²(2/εη) log(2/η) log(2K) + log(1/σ), such that ‖1_A ∗ 1_M ∗ 1_L(· + t) − 1_A ∗ 1_M ∗ 1_L‖_∞ ⩽ ε|A||M| for all t ∈ B′."

I also scanned SS's own proof (Thm 5.1, Chang–Sanders Prop 5.3 with δ = 1/2 and ν = εη^{1/2}, Lemma 4.4); nothing amiss.

**Where the paper applies it.** Only in Lemma C.2 (p. 101). It is not invoked anywhere in §6–§7. A grep for "Schoen" and "[43" hits pp. 7, 8, 101 and 198 only. Hypotheses, case by case:
- **Ambient Bohr set:** B := B_0 = S'_τ, regular, rank D ≥ 1, radius τw(S'), τ ≍ 1/D.
- **Sumset hypothesis:** SS's S := B_0, so μ = 1 ≥ σ = 1/2. SS's A := −A_2 ⊆ −s_0 + S', using that S' is symmetric. Then |A + B_0| ≤ |S'_{1+τ}| ≤ 2|S'| = (2/α_2)|A|, by regularity of S'. So K_1 ≤ 2e^q.
- **Case |K| ≥ |A_1|:** M = A_1, L = −K. Then β ∈ [α_1/2, 1], using |K| ≤ 2|S|.
- **Case η|A_1| ≤ |K| < |A_1|:** swap, M = −K, L = A_1. Then β ∈ [η, 1), and the error is η|A_2||K| ≤ η|A_1||A_2|.
- **Case |K| < η|A_1|:** trivial; both probabilities are < η.
- **Identity checked:** 1_{−A_2}∗1_{A_1}∗1_{−K}(0) = #{a_1 − a_2 ∈ K}, and (f∗µ_{B'})(0) = E_{t∈B'} #{a_1 − a_2 + t ∈ K}. Symmetry of B' handles the sign.
- **Rank:** d' = O_η((1+q)^4). ✓
- **Radius:** ≥ c·τw(S')·η√β/(D²d'), which implies w(D_*) ≥ w(S')·exp(−C_η(1+q+log(2+D))). ✓ The incoming radius w(S') is retained multiplicatively, exactly as §1.3 claims.
- **Containment:** D_* = B' ≤ B_0 ⊆ S', and the common width is preserved.

**What Lemma C.2 uses.** Only SS's rank bound, radius bound, regularity of B', and the sup-norm error at the single point 0. All of these are in SS's conclusion. The downstream use on p. 105 was spot-checked: A_1 ⊆ S, A_2 ⊆ s_0 + S' with S' a regular shrink of S; |K_0| ≤ |S + S'| ≤ 2|S| by regularity; q = O_ε(p²). Rank +O(p^8) and log-width loss O(p² + log D) are consistent with (C.7). The only quibble is E7.

## What I skimmed / did not check
- **Proofs of the external-to-scope results §7 relies on:** Lemma 3.2 (all items), Theorem 3.4 (both clauses), Lemma 5.1/5.2 proofs, Lemmas F.7, G.4, G.11, H.2, H.3, (H.1)/(H.10), Lemmas A.2/A.5/A.6, Lemma D.5, and Props I.1 and I.6. I checked only that the invoked *forms* match their statements.
- **The adaptation of Prop I.6 inside Prop 7.8:** pivot/partner selection, step drop, field and point-value meshes, the McShane extension, and the lower-degree induction on the reconstructed quotient. I read it for structure, dependence order and the bounded number of target discounts. I did not verify the cited proof's internal steps.
- **Lemma 7.3's density-continuity argument:** spare smoothing blocks, pivot-determinant strips. Read, not re-derived.
- **§8 (active layers), §9 (extraction, where b_j's cutoff and its warm radius are created) and §10:** outside scope. The passive inductive step does not close inside §7: it closes only with Prop 9.1.
- **Prop 4.1 (§4):** whether it delivers the rank-stop bounds that Prop 6.2 requests (≪ εa∏_{i≥h}e_i, cold at h) with a width loss independent of Q_h.
- **The rest of Appendix C:** beyond the hypotheses of Lemma C.2 and the bookkeeping on p. 105.

## Verdict
**HOLDS AS READ IN SCOPE** (§6, §7, and the Schoen–Sisask application in Lemma C.2). Eight EXPOSITION items, E1–E8; none rises to GAP.
