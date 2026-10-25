# Referee seat "prepare": §4 (pp. 24–36) and §5 (pp. 36–40)

Paper: /tmp/oaimath/159/paper/paper.pdf (sha256 481eaf77…, 23 Sept 2026). All formulas read on the rendered PDF pages, not the text extraction.

## Scope read (pages)
- Line by line on the rendered PDF: pp. 24–40. That is §3.5 tail (3.6), Prop 4.1, §4.1 Lemma 4.2, §4.2 Lemma 4.3 with proof, §4.3 Lemmas 4.4, 4.5, 4.6 with proofs, §4.4 Lemma 4.7 with proof, §4.5 proof of Lemma 4.2, §4.6 proof of Prop 4.1, §5.1 (5.1) and Lemma 5.1, §5.2 Lemmas 5.2, 5.3, and the proof of the warm clause of Thm 3.4.
- Read for definitions and context: pp. 6–24 (§1.3; §2 incl. (2.1)–(2.4), Thm 2.1, Def 2.3, §2.8; §3 incl. (3.1), Lemma 3.1, Lemma 3.2, Lemma 3.3, Thm 3.4, §3.4, §3.5).
- Read downstream, to check what §10 charges for preparation: §10.2 Prop 10.2 and §10.3 steps 1–4, Prop 10.3 (pp. 77–80, text extraction).
- Spot-read out of scope: Prop I.1 statement and the start of its proof (p. 179ff.), Property 1/2 of Prop F.2 (p. 177), Lemma A.5 (Separation).

## Method
For each lemma I wrote out the claimed dependency of every output bound (warm / cold-pre / late, per Def 2.3). I then traced each loss to the layer whose width it shrinks. The test was the paper's own §1.3 promise: the loss at weight h may use only p, dimension forecasts and data at levels > h, and never Q_h or Q_{<h}. I re-derived every inequality in scope that has content: the coverage geometry of Lemma 4.3, the valuation argument of Lemma 4.5, the union bounds and witness products of Lemma 4.6, the extraction coefficient of Lemma 5.1, the Cauchy–Schwarz, Hölder and Gowers–Cauchy–Schwarz chain of Lemma 5.2, and the Hahn–Banach constants of Lemma 5.3. I fetched Conlon–Fox–Zhao and compared their densification hypotheses with what §5 proves.

## Findings

### FATAL
None found.

### GAP
None found in scope. One out-of-scope dependency is load-bearing for §4.4 and is justified in the paper only by an inspection argument. I flag it for the App. I seat (D1 below). I do not count it as a GAP because I did not read the proof it rests on.

### Dependency flag (hand-off, not a finding against §4–5)
**D1. Prop I.1 is invoked outside its stated hypotheses, and this is justified by inspection.**
- Lemma 4.7's proof (p. 32): "Apply Proposition I.1 at cold-pre cost to a fixed ambient extension of D … The proposition allows unrestricted coefficients. Its proof applies to the present sampler: the local correlation is obtained from a buffered chart-supported phase, fully slow and integral lift identities from Lemma 3.2, and the cold detection conclusion of Theorem 3.4. It does not use a fine mixed-center spatial boundary estimate."
- Prop I.1 (p. 179) is stated for "the data … of Proposition F.2 … and assume Properties 1 and 2 of that proposition". Property 1 (p. 177) includes the mixed-center one-site approximation. §3.4 (p. 23) says the §3 sampler deliberately does not have that: "There is a deliberate distinction from the packaged geometry in Property 1 … not claimed with a strip as thin as every cold detection accuracy … The same inspection applies to the symbol and modeling steps in Proposition I.6."
- The part of Prop I.1's proof I spot-read (opening paragraphs, p. 179–180) uses Property 2 at degree d−1, chart-supported phases on productive paths, and ambient Fourier covers. It does not use mixed-center comparison. That is consistent with the inspection claim, but I did not read the rest of App. I.
- Second point on the same statement: "For every fixed degree bound s there is an exponent C_s … degree 1 ≤ d ≤ s". Here s must be read as a generic degree bound, not s = k−2. §4 applies it to weighted degrees up to h ≤ D, and D ≥ s. If s meant k−2, layers h > k−2 would be uncovered. I read it as generic: EXPOSITION (overloaded symbol, see E4).

### EXPOSITION
**E1. Lemma 5.1, p. 36: "For 1 ≤ q ≤ j and any bounded Cartesian grid of distinct choice vectors S".**
"Cartesian grid" reads as a full product set. Every use needs arbitrary finite sub-collections of a bounded grid: expanding the (ν−1) and (1+ν) factors in (5.3), the 4-cube moment, and the U^q bound of F_s. The proof covers sub-collections: fix α, substitute x_{a,α_a} = t_a z and the rest 0, extract t_1^{j−q+1}t_2⋯t_q; every β ≠ α misses some t_a. So it is wording only. Re-derived coefficient: j!/(j−q+1)!·λ_α C_[j](z). This needs q ≤ j, matching the warm clause r < j, q = r+1.

**E2. Lemma 5.3 proof, p. 39: "X(v) ≥ ηℜ⟨v, v⟩_μ ≥ ηE_μ|v|^2 > η/2."**
The middle pairing should be ℜ⟨v, χ⟩_μ. The chain is X(v) ≥ |⟨v,χ⟩_μ|/X*(χ) ≥ η⟨v,χ⟩_μ = ηE_μ|χ|^2 min(1,B/|χ|) ≥ ηE_μ|v|^2 ≥ η(55/72)^2 > η/2. It is true as intended. Typo.

**E3. §4.5, p. 34: "allowing a common warm shrink ζ of the normalized t box".**
ζ is never assigned. From Lemma 4.7, (4.5) and "Each lift inserts the new deviation scale υ_jζ^j and spatial scale a_jζ" (p. 35), ζ at a given layer is the cumulative radius from the layers above it. Its warmness at j holds only because each a_{j''} (j'' > j) is warm at j'' ⊂ warm at j.
- This matters: Lemma 4.7 by itself assumes only "ζ^{−1} have cold-pre logarithms".
- If ζ were cold at j, then ε_j = (υ_j/w_j)ζ^j would be cold. Lemma 4.3's lower refinement at j (relative factor ∝ ε_jγw_h/(‖e‖·coeff)) would then charge Q_j to its own loss and break (2.4).
- As written, nothing forces ζ to be cold. The cumulative reading makes it warm. The argument holds, but the text should say this.

**E4. Overloaded symbols.**
- s in Prop I.1 (see D1).
- w is used for a width and for the deck coordinate (the paper itself warns, pp. 15, 28).
- D is used for the number of layers (§2), for the integer D_0 in Lemma 4.6, and for the polynomial D(u,b) in Lemma 4.7.
- e is used for the rational section in Lemma 4.3 and for the prime-power exponent in Lemmas 4.5–4.6.
- B is used for the function B(P), for B^±, for slow bounds, and in Lemma 4.5 for B = C(r+1,2).

## Checks that HOLD (with the sentences checked)

**§4.1 Lemma 4.2 (relation for a cut), p. 25.**
"an integral row λ, nonzero on W_h and of norm at most R_h, for which, on R^n × ⊕_{i<h}K_i, λA_h = S(u/H̃, ((b_i − A_i)/(w_iε_i))_{i<h}) + R(u,b_{<h})". Also: "The log coefficient bound for S and the log common denominator of R … are polynomial in the cold budget at h alone … Each log(ε_i^{−1}) is warm at i."
- Proved in §4.5 by backward induction over layers.
- S's normalized coefficient bound grows only by exp(poly(d+n)) per layer (Lemma 4.7).
- The denominator recursion is log ρ_j ≤ poly(d+n+log(2+D_0+ρ_{j+1})).
- All spatial shrink factors a_jζ go into H̃, which is a root slice cost and may use every Q.
- Composition depth ≤ h ≤ D is fixed, so the bounds stay polynomial.

**§4.2 Lemma 4.3 (cut preserving the box certificate), pp. 26–28. What a "box certificate" is:** the two-box certificate (2.2), E fB^− > aE B^+, with B^∓ the strict and (1+γ)-enlarged triangular indicators (2.1). What is preserved:
- The old integer tuple, by the exact substitution (4.3) b_h^old = b_h^new + b_in + I. Higher widths are untouched.
- All rational value spaces except W_h → W_h ∩ ker λ, plus a full R^{d_h} incoming copy at h−1.
- The certificate itself, with threshold a' = a·c_−/c_+ and c_+/c_− ≤ (1+O(γ))^{O(Σd_i+d_h)}. The multiplicative loss is independent of the excess and of the old mass.

Re-derived:
- λC_h^new = 0 and C_h^new ∈ W_h.
- Residual bookkeeping: b_h^old − C_h^old = r_h^new + r_in − c − E.
- Full strict coverage needs w_new + w_in + |E| ≤ γw_h/2.
- New enlarged ⊂ old enlarged needs (1+γ)(w_new + w_in) + |E| ≤ γw_h/2.
- Both follow from the stated "well below γw_h/8".
- Neither inequality contains e, R_h or Q_h. Hence "The new h radius can be a fixed dimension/gap fraction of w_h, independently of e or R_h" (p. 27) holds, and the own-layer log loss is O(log 1/γ + log dims).

Also checked:
- The residue modulus M clears only the denominator of eR. The rational affine projections onto the translates κ_i + K_i enter only Δ∘P, the lower-weight remainder, which is reduced mod 1, never cleared. So log M is not charged the height of K_i. That height is cold at i, so charging it would have used Q_i.
- Lower losses depend on ε_i, γ, w_h^{−1}, ‖e‖ and the S/R bounds, all warm at i. The absolute requirement w_{h−1} ≪ γw_h/(1+d_{h−1}) is implemented as a relative multiplier (p. 35), so Q_{h−1} is never compared.
- h = 1: no incoming copy and a constant remainder. Handled.

**§4.3 the two recovery estimates, quoted and checked for current-width dependence.**

(i) Lemma 4.4, p. 28: "substitution by Φ has a bounded inverse on its image when coefficients on R^n × K are measured in (u_i/(a_jH_i), (b − A(u))/v) … Both the forward operator norm and the inverse norm are bounded by dimension-controlled factors … The constants do not depend on the widths or on the coefficients of C."
- Mechanism: b − A(u) = −y_[j] on the lift, with y/v fully slow.
- v = υ_j ∝ w_j appears only as a normalization, and the output is re-expressed in (b_j − A_j)/(w_jε_j) with ε_j warm. So no Q_j enters any loss. No lower-weight precision enters at all.
- Checked: sheet directions are O(1) in (b−A)/v units, because |v_i|z_i ≈ k_i/K_i ≈ v when K_iv ≥ 1. Inactive retained axes have side product ≍ k_i.

(ii) Lemma 4.6, p. 30: "log D_0 ≤ poly(d + n + log(2/δ)) … The bound on D_0 is independent of H."
- Re-derived the pieces: the union bound q^N(C_r q^{−c_r})^M ≤ q^{−10}, with M = O((N+10)/c_r) above a constant q; the witness-product step (if Π p^{b_p} > R, then a factor exceeds R or a greedy subproduct lies in (R, R^2]), with Σ m^{−10} = O(R^{−9}); and e = v_p(d) − v_p(d') ≤ C b_p ⇒ d | d'(Π p^{b_p})^C.
- The tested range must reach H, which is cold at the layer where the lemma is applied. Only the sampler's late parameters depend on it, never D_0.
- This independence is essential. The root denominator goes through layers j below a level i whose loss it feeds, and the H at those layers may be cold at j < i. The paper states this correctly (p. 34): "Lemma 4.6 is simultaneous on these ranges, so its output D_0 does not acquire those larger costs."

(iii) Lemma 4.5 (auxiliary), re-derived:
- Vandermonde/adjugate: v(det) ≤ (ℓ−1)B < ηe/2.
- The midpoint-valuation moves, at most r of them, give e − v ≥ 2^{−r}e.
- Dominating monomials cannot cancel the chosen coefficient after fixing variables.
- C_r = r^2 and c_r = 1/(2^{2r}B) are consistent. The constants are independent of the number of variables, as needed.

**§4.4 Lemma 4.7 (sharpened major), pp. 32–33.**
Output: "coefficient norm of S is at most B exp(poly(d + n)) … logarithm of a common denominator of R … poly(d + n + log(2 + D_0 + ρ))".
- The cold output of Prop I.1 is matched termwise to the given path splittings by Lemma A.5 (Separation; elementary, checked) on pure-long sides, which exceed the cold separation scale. Lemma 4.4 and Lemma 4.6 then give the sharpened bounds.
- Inclusion K' ⊂ K_0: an integral annihilator of K_0 takes integer values on a retained v_i, of size ≪ height/K_i < 1, hence 0. Checked.
- Degree induction on the extra-sheet degree: the extraction loss Π(k_iζ^j)^{−α_i} in (4.6) is cancelled exactly by z^α, because z_i(A(u)) = 0 and |z_i(b−A)| ≲ K_ivζ^j ≲ k_iζ^j. Checked.
- Recursion depth is bounded by degree, not dimension. Holds as read, modulo D1.

**§4.5 the induction across layers, pp. 33–35.**
Inductive hypothesis, as I reconstruct it:
- Setting: a node at layer j, meaning a pruned history through layer j−1 with a fixed center c_j and conditional productive fraction ≥ φ^{O(1)}, φ cold at h.
- The productive children ψ_j satisfy λA_h(ψ_[1](t), β_[j](t), b_{>j}) = S^{(t)}(t/(Tζ), ((b_i − A_i(ψ_[1],β_[j],b_{>j,<i}))/(w_iε_i))_{j<i<h}) + R^{(t)}.
- Bounds: slow norm ≤ 𝔅_{j+1}, denominator ≤ ρ_{j+1}.
- Conclusion at the node: the same form on R^n × K_j × ⊕K_i, with new deviation scale υ_jζ^j = w_jε_j, 𝔅_j = 𝔅_{j+1}e^{poly}, and ρ_j as above.

Base case (j = h−1): "The initial such splitting is precisely the failed rank certificate". The degree-h symbol of the pulled-back C_h in t is λA_h at the leading substitution, which is consistent.

Step:
- Coefficient tensors are processed in lex order (highest layer first). Expanding Π(b_i − A_i(b_{<i}))^β contributes to b^α only for β ≥_lex α, with coefficient 1 at β = α. Checked.
- Exactness before multiplying by the unbounded A_i is enforced by Lemma A.5. The separation scale uses only Q_{>j} and data from higher levels, so the warm minimum side at j suffices.
- Constant tensors are handled by pigeonhole over a bounded-denominator lattice region.

Loss multiplied over layers: the S bound gets exp(h·poly), and the denominators get an h-fold composition of polynomials. Lemma 4.2 asserts exactly this ("polynomial in the cold budget at h alone"), and §10.3 consumes it as warm data at every lower j. Consistent.

Pruning to good prefixes: the standard bound P(X ∧ some bad prefix) ≤ Σ_j P(X | bad π_j)·P(bad π_j) ≤ φ/2 works within the stopped subprobability tree. Holds.

**§4.6 termination and budget order, pp. 35–36, and §10.**
- Each cut lowers dim W_h by exactly 1, since λ|_{W_h} ≠ 0. Residue rescalings and refinements preserve W_i. Incoming copies arrive with full value space.
- Prop 10.2 (p. 77): H_D = d_D, H_i = d_i + H_{i+1}^2, at most H_i cuts at i, N_c = Σ H_i. This bound is structural and order-independent of retests ("Restarting a probability test does not reset its value space"). It is fixed before any precision.
- The lexicographic potential (dim W_D, …, dim W_1) strictly decreases per cut, so the process terminates within N_c transactions. That is exactly what §10.3 charges ("Divide the permitted preparation discount among the Nc possible cuts"; preparation width ≤ q_j + N_c A_j).
- Order of choices, checked for cycles:
  1. Structural d*, N_c.
  2. γ and the discounts from (p, d*, N_c).
  3. Descending j: first the warm a_j, υ_j/w_j and minimum side from U_{>j}; then the warm A_j; then the cold-pre and late choices at j using q_j + N_c A_j; then U_j.
  4. The root cutoff last.
- R_j does not need the height of W_j (p. 80). That is consistent with the Lemma 3.2 / F.7 claims of height-independence (F.7 itself not checked).
- Rank-stop bounds at j are chosen after R_j. A failure at j is lifted only through layers < j. No cycle found.

**Coordinator question: repeated cuts at the SAME layer h (trace Part II §37).** HOLDS.
- Own-layer loss per cut is gap/dimension only. Quotes: Lemma 4.3(2) p. 26, "At weight h, the relative width loss uses only dimension and gap factors, independently of R_h, Q_h, and the size of the rational section used in the cut"; p. 27, "The new h radius can be a fixed dimension/gap fraction of w_h, independently of e or R_h"; §10.3 step 2 p. 79, "Its large rational section vector is handled in the lower localizations and the incoming copy, not by conditioning the new j-residual."
- The 1/‖e‖ scaling the trace worried about is charged to the lower refinements. Quote, p. 27: "The additional relative precision uses only dimension factors, γ^{−1}, w_h^{−1}, ‖e‖, and the coefficient bound in (4.1). For every lower level these are permitted higher-level costs."
- The section and kernel heights after repeated cuts at h come from stacked rows and Cramer's rule, poly(total dim, N_c, log R_h) (p. 35). They are not compounded per cut.
- The number of cuts at h is ≤ H_h, structural. log(1/γ) = poly(p, d*, N_c) (§10.3).
- So total own-layer loss is ≤ H_h·O(log 1/γ), and the per-cut losses multiply, i.e. add in log, into N_c A_h with A_h warm. Prop 10.3 absorbs exactly this: Q_j^out ≤ q_j + N_c A_j + A'_j.
- The repeated shrinking of w_h during preparation never feeds back into R_h, because R_h is chosen once against the forecast ("Only now choose cold-pre and late budgets at j, permitting this additive width bound", p. 36).
- Each cut at h re-shrinks h−1 relative to the current w_h, a loss of about Q_h. This costs ≤ N_c·(q_h + N_cA_h) at h−1, which is warm at h−1.

**§5.1 the pseudorandom chart weight.** ν(u) = χ(C(u)−c)/a_χ, with a_χ ≍_warm m_j (Lemma 3.1) and sparse factors ≤ Bν (B warm).
- Defining properties: Lemma 5.1, E Π_{α∈S} ν(Σ_{a≤q} x_{a,α_a}) = 1 + o(1) for distinct choice vectors with q ≤ j and x iid uniform on H = ΠZ/(4H_aZ). In particular Eν = 1+o(1), plus marginal boundary estimates.
- Proof: Fourier-expand χ in the ambient chart (integral rows, so no height of W). A nontrivial character with bias ⇒ by Lemma B.1 the joint degree-j symbol is slow+rational ⇒ the extraction above ⇒ λ_αC_[j] is slow+rational ⇒ contradicts rank R_j, which is late and so can exceed the cold Fourier mass M^{|S|}/ε. Wrap is handled by fine cells.
- Logic checked. The Fourier-approximation accounting and Lemma B.1 were taken on trust.

**§5.2 densification without paying chart mass (Lemmas 5.2, 5.3; warm clause of Thm 3.4).**
- Group cubes: vertices Σ_a x_{a,ω_a}, with x_{a,b} iid uniform on H pushing forward uniformly to (x,h) ∈ H^{q+1}.
- No-wrap for cubes inside U: re-derived by two-face induction (each new vertex is in (−H,2H), so mod 4H it is in [0,H) iff it is an integer there). κ = |Cub_q(U)|/|H|^{q+1} = e^{−O(n)}, warm.
- Replacing one vertex at a time:
  - E(1+ν)|D_i|^2 ≥ δ^2/(B'^2E(1+ν)).
  - (5.3): E(ν−1)|D_i|^2 = o(1) by q root-input Cauchy–Schwarz doublings (exactly CFZ Lemma 6.3's scheme, with "every nonroot factor misses a root input" playing the role of e ⊉ e_1). E|D_i|^4 = O(1) by four rooted cubes with distinct choice vectors.
  - Hölder: E|D| ≥ (E|D|^2)^{3/2}/(E|D|^4)^{1/2}.
- Final stage:
  - Pointwise |D_i| ≤ BE_Hν, since the s-site is exactly uniform.
  - ‖F_s‖_{U^q}^{2^q} ≤ B^{2^q}E Π ν = O(1), and Gowers–Cauchy–Schwarz gives ‖D_i‖_{U^q} warm-large.
  - The inverse theorem (Thm A.7, product-cyclic) is applied only to bounded D_i.
  - Dividing by ν on {χ = 1} converts the correlation to μ_c at warm cost.
- Every output (correlation, niltest complexity, atom count, coefficient mass) depends on δ, B, B', q, n and inverse-theorem constants. m_j enters only through the o(1) errors, which the late choices kill.
- Lemma 5.3: the Hahn–Banach constants were re-derived (|χ| ≤ Cm/η with the atom mass cancelling; E|χ−v| ≤ min(1/8, δ_0/4); E|v| ≥ 55/72; contradiction because 3δ_0/4 > 1/M). The change of measure m_rel = (E_Uν)m_U/ν is warm-capped on supports.
- So the §1.3 claim, "The comparison proved here has bounds independent of that layer's chart mass", holds for r < j as read.

## External inputs checked
- **Conlon–Fox–Zhao, "A relative Szemerédi theorem".**
  - Source: arXiv:1305.5440, current version v2 (25 Nov 2014; v1, v2 listed on abs page), saved at /tmp/oaimath/159/refs/1305.5440/cfz_v2.pdf. Paper's [11] = GAFA 25 (2015), the published form.
  - Cited place "[11, Sections 6.2–6.3]": §6.2 "Strong linear forms" (Lemma 6.2, Lemma 6.3); §6.3 "Counting lemma proof", i.e. densification for Thm 2.17. The citation locates the method correctly.
  - CFZ hypothesis: Def 2.8 H-linear forms condition (4). That is E Π_{e∈H}Π_{ω∈{0,1}^e} ν_e(x_e^{(ω)})^{n_{e,ω}} = 1 + o(1) for all exponent choices n ∈ {0,1}: two-sided, every sub-collection of the 2-blow-up.
  - The paper does not apply a CFZ theorem as a black box. It re-proves a different densification: dual-function phase replacement, then Hölder, then the inverse theorem, on Gowers cube averages, rather than CFZ's discrepancy-pair counting lemma with capping g'∧1.
  - The pseudorandomness it uses is supplied by its own Lemma 5.1. That lemma is two-sided (= 1+o(1)) for every finite family of distinct cube forms Σ_a x_{a,c_a} on a bounded index grid with q ≤ j.
  - This contains CFZ's condition for the q-partite octahedral q-graph (the cube) and all its sub-collections, and the larger grids needed for the 4th moment. So it is not weaker than CFZ's. The only restriction is q ≤ j, which is exactly why the warm clause is limited to r < j, and the paper states that limitation.
- **Prop I.1, Lemma A.5, Lemma B.1, Thm A.7, Lemma F.4/F.7, Lemma G.10/G.11, Lemma 3.3** are internal dependencies, not external. Lemma A.5 is checked (elementary); the others are not (see below).
- LSS [35] and Schoen–Sisask [43] are not invoked in pp. 24–40.

## What I skimmed / did not check
- Not checked:
  - Proof of Prop I.1 beyond its first page, and therefore the §3.4 inspection claim that it runs on the §3 sampler (D1).
  - Lemma B.1 (Weyl / step-drop), used in Lemma 5.1.
  - Thm A.7 (product-cyclic inverse theorem), used in Lemma 5.2.
  - Lemma F.4, Lemma F.7 / Cor F.9–F.10 (non-site mode removal, height-independence of rank thresholds).
  - Lemma G.10/G.11, Lemma 3.3 (cube comparison in chart units), Lemma 3.2 proof, Lemma 3.1 proof.
- Taken on trust: the cold-cost Fourier approximation of χ in Lemma 5.1, and the claim that the o(1) errors there can be made smaller than any pre bound with late R_j.
- Not checked: §6's requirement on the rank-stop bounds π_j ("small enough for the forward calculation using the current prepared width and higher-layer center masses"). I only checked that π_j is chosen after R_j and that a failure at j is lifted through layers < j only.
- Distinctness of all forms after the q doublings in (5.3): I checked the argument structure ("descendants of one vertex differ in a cloned coordinate …; every nonroot descendant retains an alternate coordinate"). I did not enumerate the forms for general q.
- §10 checked only for the preparation charges (Prop 10.2, §10.3 steps 1–4, Prop 10.3), not for ascent/extraction losses A'_j.


## Rank-stop hand-off (Prop 6.2 ← Prop 4.1)
Read on the rendered PDF: pp. 41–44 (§6.1 tail, Prop 6.2 statement and proof).

**What Prop 6.2 requires.**
- Statement, p. 42: "The rank-stop probability at layer h need only have inverse logarithmic cost polynomial in the data at layers ≥ h."
- Proof, p. 42: "Stop a prefix when it fails its current rank test … Preparation tests the actual conditioned procedure, including earlier stops. Its requested rank-stop probabilities are arbitrarily small at cold cost in the current and higher layers."
- Proof, p. 43, the precise requirement: "A rank stop at h loses at most its probability divided by ∏_{i≥h} e_i from normalized strict mass; … Request the former errors much smaller than εa∏_{i≥h} e_i … These are exactly the cold and warm dependencies in the statement."
- So the required inequality is P(stop at h) ≪ εa·∏_{i≥h} e_i, where:
  - e_i is the Haar measure of the feasible-center set (3.6) at layer i;
  - ε is a small fixed step loss;
  - a ≥ e^{−p}.
- Its log-cost is log(1/ε) + log(1/a) + Σ_{i≥h} log(1/e_i).
  - For i > h, log(1/e_i) is cold-pre at i, by p. 42: "Lemma 3.1 applied to a smaller ball about that point therefore gives a cold-pre bound on log(1/e_j) at layer j". Cold-pre at i is warm at h.
  - For i = h it is cold-pre at h.
  - So the requirement uses only data at layers ≥ h, never Q_{<h}. This agrees with §2.8 p. 13: "Its failure probability may charge Q_{≥j} but not lower widths".

**What preparation delivers.**
- Prop 4.1 statement, p. 25: "every rank-stop probability in the actual current sampling procedure is at most its prescribed bound."
- Proof, §4.6 pp. 35–36: "If a stop probability is too large, apply Lemma 4.2 at that level and then Lemma 4.3. Retest the resulting actual system … The finite cut bound then forces termination with the stated probability tests and costs."
- The bound is achieved because the loop exits only when every test passes, and at most N_c cuts can occur (Prop 10.2). So at exit P(stop at h) ≤ π_h for every h.
- The prescribed bound π_h is set in §10.3 step 4, p. 79–80: "Choose the rank-stop probability small enough for the forward calculation using the current prepared width and higher-layer center masses."
- The quantity tested is defined in §3.5, p. 24: "The rank-stop probability at j means the mass of histories that reach that test and fail it; histories already stopped contribute zero." The discard rules are part of the tested tree: "For applications that discard additional sampled paths, fix the discard rules as part of the current tree being tested … They delete probability mass; they do not renormalize the distribution".

**Comparison.**
- **Same quantity: yes.** Both are the unnormalized stop mass at layer h in one stopped subprobability tree.
  - The centers are Haar-conditioned on (3.6).
  - Earlier stops count as zero.
  - The discard rules are the same ones: noninjective paths and (6.3) modular-goodness failures. Prop 6.2 lists exactly these ("Also discard noninjective paths and failures of Equation (6.3)"), and §3.5 builds them into the tree preparation tests.
  - Flags are masks of the input, not conditioning ("A mask of the input function, such as a site-dependent flag, is likewise distinct from conditioning the path law", p. 24). So they do not change the tree.
  - Prop 6.2's loss accounting bounds the strict mass a stopped prefix carries by 1, then normalizes by ∏_{i≥h} e_i. This is conservative and consistent.
- **Same layer data: yes.**
  - π_h ≪ εa∏_{i≥h}e_i has log-cost cold-pre at h.
  - Preparation can deliver any π_h whose inverse log is polynomial in the cold budget at h. The constraint comes from Lemma 4.2's proof, p. 33: "Its failure fraction still has inverse logarithm polynomial in the cold budget at h". The fraction there is ≥ π_h/(1+2R_h)^{d_h}, with log R_h late at h, i.e. polynomial in cold-pre at h.
  - The extra cost of a smaller π_h is absorbed by the lifting at layers < h, where it is warm data. It is not absorbed at h.
  - The ordering is free of cycles: π_h is chosen after R_h (§10.3 step 4, "After all these pre requirements, choose the perturbation, range, rank, and parent-side bounds. Choose the rank-stop probability …"), and a failure at h is lifted only through layers < h (§10.3 step 1: "A rank failure at j itself is lifted only through layers below j").
- **Same direction: yes.** Prop 4.1 gives an upper bound on the stop probability, and Prop 6.2 consumes an upper bound.

**One point checked because it could have hidden a cycle.** Prop 6.2's e_i are measures of the PREPARED cell, while π_h must be fixed before the preparation loop runs. The loop's exit test uses π_h, and the cell, hence e_i, changes with each cut. This is consistent:
- log(1/e_i) has an a priori cold-pre lower-bound proof from the "room at least γw_i/2" ball and Lemma 3.1 (p. 42; m_j bounds independent of the height of W_j).
- Prepared widths are forecast by q_i + N_cA_i (§4.6, §10.3 step 2).
- γ is fixed structurally before any of this (§10.3).
- So π_h can be fixed against the forecast lower bound for ∏_{i≥h}e_i. That is what "using the current prepared width and higher-layer center masses" means.

§4 itself never states "π_h is fixed against the forecast lower bound for e_i". That is implicit in the words "prescribed bound" (EXPOSITION, minor; no change to the logic). The certificate threshold a also drifts by the preparation discount a' ≥ (1 − small)a, which is harmless in εa.

**Result: the hand-off MATCHES.** Same quantity, same layer data (layers ≥ h, cold-pre at h), same direction. Verdict unchanged.

## Verdict
HOLDS AS READ IN SCOPE (§4 pp. 24–36, §5 pp. 36–40). No FATAL or GAP findings. Four EXPOSITION items (E1–E4). One out-of-scope dependency to verify: D1, Lemma 4.7's use of Prop I.1 on the §3 sampler, which the paper justifies by inspection (§3.4). The coordinator's same-layer repeated-cut question holds: the per-cut loss at h is gap/dimension only, the cut count is structural, and both are warm, as charged in Prop 10.3. The rank-stop hand-off (Prop 6.2 ← Prop 4.1) matches: same quantity, layer data ≥ h, same direction.

---
## Appendix: running notes (as written during the read)

## Running notes
- Read context: §1.3 (pp.6–7), §2 (pp.8–14), §3 (pp.14–24) for definitions (cells, certificate (2.2), Thm 2.1, Def 2.3 warm/cold/late, lift charts, m_j, Lemma 3.2, Thm 3.4, stopped tree §3.5).
- p.25 Prop 4.1 / Lemma 4.2 / p.26–28 Lemma 4.3 read on rendered PDF. Averaging-over-centers argument (old strict point gets full strict coverage iff new radius + |E| <= gamma w_h/2; new enlarged inside old enlarged iff (1+gamma) w_new + |E| <= gamma w_h /2) checks with the stated "well below gamma w_h/8". Ratio c+/c- = (1+gamma)^{dims} per refinement, independent of the shrink factor. Own-layer loss log(16/gamma)-type: dimension/gap only. OK.
- pp.28–36 read on rendered PDF: Lemma 4.4 (normalized real recovery), Lemma 4.5 (prime-power test; proof re-derived: Vandermonde/adjugate step, valuation-midpoint moves, <= r moves; constants C_r=r^2, c_r=1/(2^{2r}B) consistent), Lemma 4.6 (denominator recovery), Lemma 4.7 (major refinement), §4.5 proof of Lemma 4.2 (backward induction), §4.6 proof of Prop 4.1.
- Checked Lemma 4.3 identity (4.2)/(4.3): lambda C_new = 0 and C_new in W_h; residual bookkeeping b_old - C_old = r_new + r_in - c - E; projection P onto affine translates kappa_i + K_i only enters Delta∘P (lower-weight remainder, reduced mod 1), NOT eR, so the residue modulus M is not charged the height of K_i (which would be cold at i, i.e. would use Q_i). OK.
- Termination count §4.6: c_h <= dimW_h(init) + c_{h+1} d_{h+1}^max; lexicographic potential (dim W_D,...,dim W_1) strictly decreases per cut regardless of retest order; depth D fixed -> polynomial (degree ~2^D). OK.
- §5 pp.36–40 read on rendered PDF. Lemma 5.1 extraction re-derived: substituting x_{a,alpha_a}=t_a z, others 0, coefficient of t_1^{j-q+1}t_2...t_q in C_[j]((t_1+..+t_q)z) is j!/(j-q+1)! C_[j](z); any beta != alpha misses some t_a -> vanishes; needs q <= j (consistent with warm clause r<j, q=r+1). Group-cube reparametrization vertices = sum_a x_{a,omega_a}, x_{a,b} iid uniform on H, pushes forward uniformly onto (x,h) in H^{q+1}: OK. No-wrap two-face induction for cubes with all vertices in U: re-derived, OK.
- Lemma 5.2 steps re-derived: CS bound E(1+nu)|D|^2 >= delta^2/(B'^2 E(1+nu)); Holder E|D| >= (E|D|^2)^{3/2}/(E|D|^4)^{1/2}; pointwise |D_i| <= B E_H nu when only s is sparse (s-i has a +-1 coordinate => site uniform on H); GCS with ||F_s||_{U^q}^{2^q} <= B^{2^q} E prod nu. Inverse theorem only applied to bounded D_i. OK.
- Lemma 5.3 (Hahn–Banach): re-derived |chi| <= Cm/eta (atom mass cancels), E|chi-v| <= min(1/8, delta_0/4), E|v| >= 8/9-1/8 = 55/72, X(v) >= eta E|v|^2 >= eta(55/72)^2 > eta/2, pairing contradiction 3delta_0/4 > 1/M. OK (display has <v,v> where <v,chi> is meant: exposition).

## Coordinator question: repeated cuts at the SAME layer h (trace Part II §37 worry)
Located the charges:
- Own-layer loss per cut, p.27: "The new h radius can be a fixed dimension/gap fraction of w_h, independently of e or R_h." and Lemma 4.3(2), p.26: "At weight h, the relative width loss uses only dimension and gap factors, independently of R_h, Q_h, and the size of the rational section used in the cut." The ||e|| (section) and coefficient-bound dependence is pushed into LOWER refinements: p.27 "The additional relative precision uses only dimension factors, gamma^{-1}, w_h^{-1}, ||e||, and the coefficient bound in (4.1). For every lower level these are permitted higher-level costs." and §10.3 step 2 p.79 "Its large rational section vector is handled in the lower localizations and the incoming copy, not by conditioning the new j-residual." I re-derived the coverage inequalities: old strict point fully covered iff w_new + w_in + |E| <= gamma w_h/2; new enlarged inside old enlarged iff (1+gamma)(w_new + w_in) + |E| <= gamma w_h/2. Both hold with radii, |E| <= gamma w_h/8 as stated; neither inequality contains e, R_h or Q_h. So per-cut own-layer log loss = O(log(1/gamma)) with log(1/gamma) = poly(p, d*, N_c) (§10.3 p.78: "gamma can be a sufficiently small fixed gain-dependent constant divided by a sufficiently large polynomial in 2 + p + d* + N_c"). Warm. HOLDS.
- Number of cuts at layer h: §4.6 p.35 "Each such cut removes one dimension of W_h. New dimensions there arise only from incoming copies at higher levels." Prop 10.2 p.77: H_D = d_D, H_i = d_i + H_{i+1}^2, "There are therefore at most H_i cuts at i ... Restarting a probability test does not reset its value space, so it does not affect this count." Structural (dimensions only, no width/rank/accuracy), fixed before any precision. I checked: residue rescalings C'_i = C_i/M and lower refinements preserve W_i (scalar rescale of a subspace), incoming copies arrive with full space and are counted in H_i, so the bound is order-independent of retests. HOLDS.
- Cuts ABOVE j charged at j (A_j): coefficient/denominator bounds of the higher failure (cold at h => warm at j), ||e|| (stacked-row Cramer bound poly(d, N_c, log R_h), p.35), epsilon_j (warm at j), spatial shrink, omission cutoff, and the absolute "lower width below upper width" requirement implemented as a RELATIVE multiplier (p.35 "If a common lower width must lie below an upper width, multiply its current width by the required small upper-scale factor; since all widths are less than 1, this also supplies the required absolute bound") so Q_j itself is never compared. Cuts below j: "A cut below j causes no shrinkage at j" (consistent with Lemma 4.3(2) "At weights above h, no width loss is necessary", and with the exact substitution (4.3)). Total: Q_j^prep <= q_j + N_c A_j (p.35, and §10.3 step 2 p.79), A_j warm. Multiplicative shrink factors compose additively in log, so the "product of per-cut losses" is N_c A_j, which is what Prop 10.3 absorbs (Q_j^out <= q_j + N_c A_j + A'_j). HOLDS AS READ.
- Residual same-layer subtlety checked: R_h (late at h) is chosen once against the forecast q_h + N_c A_h ("Only now choose cold-pre and late budgets at j, permitting this additive width bound", p.36), so the h-width shrinking during repeated cuts at h never feeds back into its own threshold choice. The height of W_h after repeated cuts is "not needed in choosing R_j" (p.80), consistent with Lemma 3.2/F.7 claims that rank/side thresholds do not depend on the height of W (I did not verify F.7 itself — out of scope).
- CFZ fetched: arXiv:1305.5440v2 (25 Nov 2014, current; v1 and v2 listed) -> refs/1305.5440/cfz_v2.pdf. §6.2 = Lemma 6.2 + Lemma 6.3 (Strong linear forms), §6.3 = proof of the counting lemma Thm 2.17 by densification. Hypothesis = Definition 2.8 H-linear forms condition (4): E prod_e prod_omega nu_e(x_e^(omega))^{n_{e,omega}} = 1+o(1) for ALL exponent choices n in {0,1} (two-sided, all subgraphs of the 2-blow-up).
