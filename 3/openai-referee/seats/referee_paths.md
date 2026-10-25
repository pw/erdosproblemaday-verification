# Referee seat: paths (§3 pp.14–24, App. F pp.136–146 up to the start of G)

## Scope read (pages)
- Read line by line, from the rendered PDF: pp.14–24 (§3.1–§3.5, Lemma 3.1, Lemma 3.2 and its proof, §3.3.1, §3.3.2, Lemma 3.3 statement, Theorem 3.4 and its cold-clause proof, §3.4, §3.5) and pp.136–146 (F.1, Definition F.1, Proposition F.2, Remark F.3, Lemma F.4, F.3 coefficient tilt, Lemmas F.5–F.7, Remark F.8, Corollaries F.9–F.10, the closing budget display on p.146).
- Read for context: pp.8–13 (§2, Theorem 2.1, Definition 2.3).
- Read to check how the §3 guarantees are used: pp.28–31 (§4.3, Lemma 4.4, Lemma 4.6 moduli), §5 pp.36–40 (Lemma 5.1 statement, Lemma 5.3, warm-clause proof paragraph), §6 pp.41–43 (Lemma 6.1 item 4, §6.2 use of (3.6), e_j, Lemma 3.2(4)), §7 p.49, p.56, p.58 (finite-residue use, warm approximation use), G.7 (Lemmas G.10, G.11), G.8 (first paragraph, where it lists how the §3 law differs), H.4 parameter-order paragraphs (pp.175–177), I.1 statement and proof (pp.179–183), Lemma B.1 statement, Theorem A.7 statement.

## Method
1. For each displayed inequality in Lemma 3.1 and Lemma F.4 I redid the estimate (reduced basis of Λ′, covol(Λ)·covol(Λ′)=1, the bounds on k_i/K_i, lattice-point counts for the upper and lower chart-mass bounds).
2. For Lemmas F.5–F.7 I rechecked the algebra (the vanishing ideal of the Boolean cube, factoring through evaluation equals vanishing on the kernel, the h-fold box difference isolating h!·λ′(Pol C_h^top)(w−w′), the Cauchy–Schwarz count (δ/2)^{2^h}, the displacement versus width requirement, and whether the hypotheses of Lemma B.1 hold at the point where it is applied).
3. I wrote out the law (3.3)/(F.4) explicitly and checked each assertion of Lemma 3.2 and Corollaries F.9–F.10 against it: normalization, the one-site cap via convolution, the constant-mode cancellation under mixed centers, the finite-residue total-variation count, and noninjectivity.
4. Parameter order: I traced each "sufficiently large" requirement to the quantities it depends on, through §3.2, F.1 (F.2), the p.146 display and the H.4 assembly, and looked for any requirement that depends on a later choice.
5. Interface: I listed what §4, §5, §6, §7 and App. I take from §3 and compared it with what §3 and F state.

## What is constructed (precise statement)
At one layer j, given the parent box U = ∏{0..H_a−1} ⊂ Z^n, a polynomial C: Z^n → W ⊂ R^{d} of degree ≤ j with rational W (lower layers already substituted), a chart width v (a warm fraction of w_j), and a center c ∈ W/Λ:
- **Sample space:** integer pairs (x,V) ∈ Z^n × Z^{n×m}, giving the affine map ψ(t)=x+Vt on the parameter box T=∏_ℓ{0..T_ℓ−1}. The law is finitely supported. m is structural, i.e. fixed before any numerics. The sides are L for kernel, dedicated and free columns; ≍k_i^{1/j} for dedicated columns on inactive axes; ≍k_i for the extra column t_{i,0} on an inactive axis. So T_ℓ = O(L^j).
- **Reference (abstract) law:** a product density D_c on ∏_{|ν|≤j} W/Λ with respect to Haar measure. Per coefficient and axis it is a smooth density on continuous (W) coordinates, a smooth discrete bump or a point mass on the integer sheet coordinates z_i (Lemma F.4 charts), and it is shifted by c only in the constant coefficient. ∫D_c = 1.
- **Spatial law ρ(x,V):** a product law. x is nearly uniform on a buffered interior box. Kernel blocks lie near fixed invertible matrices at a warm spatial scale. Nonkernel entries are smooth on |V_{aℓ}| ≤ c_0σH_a/(mT_ℓ).
- **Actual law (3.3):** dP_c = ρ·D_c(coeff C(x+Vt))/Z_c, a different probability space from the reference law (the paper says so explicitly, p.14 and p.18).
- **Guarantees (Lemma 3.2, Theorem 3.4, Lemma 3.3):**
  - Z_c = 1+o(1), uniformly in c.
  - On the support the exact identity C(ψ(t))−c = y+β holds, with y fully slow at width v and β∘ψ having integer coefficients.
  - Non-site modes are removed.
  - At each individual modulus, the coefficient residues are within total variation η of (Haar-cover chart/deck law) × (unweighted spatial residues).
  - Noninjectivity has arbitrarily small probability.
  - The fixed-center one-site density is ≤ B/m_j (B warm), up to an arbitrarily small excess mass.
  - The mixed-center one-site law lies between (1−ε)·uniform (off a strip of warm thickness) and (1+ε)·uniform, up to a cold-pre additive error.
  - Detection and approximation: cold clause for all testing degrees; warm clause for r<j, proved in §5.
- **Tree (§3.5):** at each layer: rank test (stop the history on failure) → center from Haar on W_j/Λ_j conditioned on C_j (3.6) → ψ ~ P_c → discard rules kill outcomes without renormalizing. The result is a subprobability measure on histories of fixed depth D.

## Findings

No FATAL. No GAP. EXPOSITION items (Lemma F.4's stated covolume range e^{±O(d^3)} is looser than what its proof gives, [e^{−O(d^3)}, e^{O(d^2)}], so it is not a finding):

**E1. §3's one-layer law is not an instance of Proposition F.2. It is a modified ensemble, and its guarantees are re-derived rather than cited.**
- The two constructions differ in five ways:
  - **Chart and classification variable.** §3 uses chart width v and classifies axes by k_i = max(1,⌈K_i v⌉) (p.16 l.45–47). F.3 uses the 1/4 chart and classifies by K_i: "Call a projection axis inactive if K_i ≤ L^h, moderate if L^h < K_i ≤ L^{C_s}" (p.139 l.27).
  - **Side bound.** §3 says "Every side is O(L^j)" (p.17 l.47). F.2 says "T_j ≤ L" (p.137 l.42).
  - **Extra column.** §3 adds an extra coefficient-one column t_{i,0} on each inactive axis (p.17 l.21).
  - **Moderate-axis perturbations.** §3 puts pure-free perturbations on moderate axes (p.17 item 4), whereas F.3 says "All remaining nonconstant coefficients vanish on inactive and moderate axes" (p.139 l.46–47).
  - **Degree range.** §3 runs at layers j ≤ D, while F.1 is stated "For 1 ≤ h ≤ s" (p.136 l.41).
- The paper handles this as follows:
  - Lemma 3.2's proof verifies the Fourier-removal hypotheses directly: "The displacement proof of Lemma F.7 only changes by replacing its parameter bound L with O(L^j)" (p.20 l.19).
  - G.8 re-proves Lemma 3.3 for this law and lists the differences (p.163 l.28).
  - §3.4 transfers App. I by "inspection" (p.23 l.24–33).
- I checked that Lemma F.7 uses L only through the B(b) factor that dominates mT_ℓ/σ, so the change to O(L^j) is harmless.
- I checked that I.1's proof uses only fixed-center detection (Property 2), Lemma B.1 and rank. It does not use the mixed-center one-site accuracy, which §3 weakens to a warm strip.
- I did not check I.6 or the body of G.8.
- **Repair (exposition only):** state in §3 that Proposition F.2 is not invoked as stated, and list in one place which F/G/H lemmas are re-run with which changes.

**E2. Degree range.**
- §3 needs Lemma F.7, Corollaries F.9–F.10, the G cube lemmas and the enormous exponent C* at polynomial degree j up to D > s. F.1/F.2 are stated for degrees h ≤ s.
- H.4 fixes "The cube orders required below are 0 ≤ q ≤ s+1" (p.175 l.18) and takes the enormous-axis exponent as a maximum over 1 ≤ h ≤ s (p.175 l.24).
- §3 covers this with "All degrees and cube orders below belong to a fixed finite range" (p.14 l.46) and "a fixed sufficiently large degree-dependent C*" (p.16 l.47).
- The proofs I read (F.5–F.7, B.1 with general degree, F.9, F.10) are fixed-degree arguments, so taking constants at degree D is legitimate.
- Testing degrees stay ≤ s at every layer (p.56 §7.7: "At j > s, all degrees that occur in ordinary partner selection are strictly below j"; p.58: "The local testing degree is at most s < j"), so cube orders ≤ s+1 suffice.
- **Not checked:** whether the choice of D (§9 weight argument) is made before the D-dependent C*, J_0 and block counts. This is outside my scope; it is the only place a cycle involving my scope could hide.

**E3. Lemma 3.3 states no uniformity in the center.**
- The statement (p.21 l.43–49) fixes a slice and asserts uniformity "for |P_ω| ≤ 1". Theorem 3.4 asserts "uniformly in the center and the site input" (p.22 l.39) and rests on Lemma 3.3.
- Center-uniformity holds by the phase argument used for Lemma 3.2 ("Translating c changes Fourier phases but none of the bounds", p.20). It should be stated in Lemma 3.3.

**E4. "Chart widths" in the F.1 pre budget.**
- "Next choose a budget b_pre ≥ 2 for the fixed dimensions, testing complexities, logarithms of inverse chart widths…" (p.137 l.11). F.1 itself fixes the chart at |y_h|_∞ < 1/4 (F.1), so it is unclear what chart width is meant inside App. F.
- In §3 it is v, which makes "pre" there equal to cold-pre. That reading is consistent with every use, but it is not said.

**E5. Overloaded symbols in scope.**
- B means: blocks in ∏_{ℓ∈B}; slices B; the warm constant in "density at most B/m_j" (p.19 l.43); the budget function B(b); the cell indicators B^±.
- m means the number of columns (p.18 l.32); m_j is the chart mass and m_U the one-site density.
- D means both the cell depth and the coefficient density D/D_c.
- The authors flag only the clash between the width w and the deck coordinate w.

**E6. The "omission threshold" in Theorem 3.4 is not defined by that name.**
- It is the "specified warm minimum" of item 3 on p.17 (l.21, l.47), which "may include higher-layer parent and separation requirements".
- Under Definition 2.3 this is warm at layer j: it uses Q_{>j} and not Q_j. So the claim "may use the omission threshold but do not use Q_j" is consistent. A one-line definition would help.

## Line-by-line checks that held

**Lemma 3.1 (p.15–16).**
- covol(Λ) ≍ ∏K_i follows from Lemma F.4.
- K_i v ≤ k_i ≤ 2max(1, K_i v) gives the following, independent of height:
  - |z_i/k_i| ≤ e^{O(d^3)}|y|/v;
  - exp(−poly d)·v^d ≤ m_j ≤ exp(poly d)·v^{dim W}.
- The z_i row is the dual-basis vector v_i^* ∈ W^⊥∩Z^d (the dual of Λ′), so it is integral, annihilates W, and has norm ≤ e^{O(d^3)}K_i.
- Upper chart mass: the integer points in |z_i| ≤ Ce^{O}K_i v number ≤ (Ce^{O})^q ∏k_i, times the W-volume, divided by covol, gives a warm multiple of m_j.
- Lower bound: the box |z_i − z_{0,i}| ≤ e^{−O}τK_i v contains ≥ e^{−O}τ^q ∏k_i points, giving ≥ warm^{−1}·m_j. A feasible center is needed, as the lemma says.
- The unimodularity of β ↦ (z,w) follows from primitivity of Λ.

**Lemma F.4 (p.138–139).**
- LLL on a lattice generated by vectors of length ≤ 1 gives lengths and defect 2^{O(d^2)}.
- |K_i v_i| ∈ [1, e^{O(d^2)}].
- The singular-value bounds give e^{O(d^3)} for the coordinate maps.
- covol(Λ)·covol(Λ′) = 1 via the block-triangular basis.
- The Haar formula holds.

**Scale gap (p.16; F.3 p.139).**
- Among q+1 disjoint ratio-A intervals, one avoids all q numbers k_i^{1/j}. So L ∈ [A, A^{q+1}] and no k_i lies in (L^j, (AL)^j).
- Inactive, moderate and enormous axes are then well defined.
- A moderate principal integer interval has length γk_i/L^j ≥ γA^j ≥ 1 once A is late.

**Coefficient law (p.17–18; F.3 p.139–141).**
- The discrete-bump normalization holds.
- The Haar density covol(Λ)f∏p_i equals [covol/∏K_i]·f·∏(K_i p_i), with every factor height-free:
  - K_i p_i ≤ max(1/δ, K_i);
  - singletons occur only when k_i ≤ L^{C*}, costing O(log L) + cold-pre;
  - enormous widths are k_iσ/T^ν ≥ σL^{C*−j^2} ≫ 1 once L ≥ A ≫ σ^{−O(1)}, given C* > j^2.
- Smooth interpolation of the discrete bump (p.140 q(u)): the derivative bounds C_rδ^{−r−1} are independent of K_i, by Poisson summation on the denominator.
- Inactive axes: the sheet output (3.2) stays at O(c^j J_0 + c)·k_i, which is small in normalized units.
- Chart containment, the lift identity, and the homogeneous identity β_[j] − C_[j](Vt) = −y_[j] (p.16) all hold.

**Lemma F.5.**
- Reduction by z_i and a_i^2 = a_0 a_i, with the subset monomials ∏_{i∈S}ω_i linearly independent on {0,1}^q, puts the vanishing polynomials in the ideal (z_i, a_i(a_i − a_0)).
- The generators times monomials give products of h forms with one factor vanishing at each site. For h = 1 only the z_i appear. The q = 0 case is fine.
- The height bound follows from Cramer's rule.

**Lemma F.6.** The kernel of evaluation is W ⊗ (scalar kernel), so a non-factoring λ is nonzero on some w⊗P. The bounds do not depend on the height of W.

**Lemma F.7 (p.142–143).**
- Absorbing the higher layers into the site functions is valid pointwise for real coefficients; Remark F.8 handles the torus cover.
- Each site factor misses some shift w_i, so h Cauchy–Schwarz steps give (δ/2)^{2^h}. The lower layers die under the h-fold box difference.
- The top term h!·λ′(Pol C_h^top)(w − w′) is independent of the base point. The lower-degree λ case works because forms may include T_0.
- Displacement \tilde H = H/B(b) ≪ c σ H_a/(mT_ℓ) and ≪ kernel width, given B(b) ≥ mT/σ.
- The hypotheses of Lemma B.1 hold: G = R, filtration of length h, frequency 1, 2hn variables (so p ≥ 2hn, and b contains n, m), bias log O_h(1 + log δ^{−1}), no coefficient bound needed. B.1's conclusion with η(W_h) = 0 forces the top symbol to be slow plus rational.
- Restricting to w′ = 0 and the diagonal keeps slow and rational bounds up to h! and B(b). The stride is cleared, and the integer row λ′ is nonzero on W_h, which contradicts Definition F.1 once R > B(b).
- The rank notion is the same in Definition F.1, §2.6.1 and §3 ("single tag j", p.14 l.43–44).

**Corollary F.9 and Lemma 3.2(1),(3),(4).**
- Z_c: sup-norm Fourier approximation of the ambient extension. Ambient modes annihilating W integrate to ∫_{W/Λ}; the others are removed; |Z_c − 1| ≤ 2ε′ + mass·ε_F7. Uniform in c because c enters only as a phase in the constant coefficient.
- Fixed-center one-site cap: the projection of D onto the modes factoring through ev_t equals g∘ev_t, where g is the pushforward of D under ev_t, a convolution with the constant coefficient's law.
  - The constant coefficient's density is ≤ m_j^{−1}·(v^{dim W} f)·∏(k_i p_i) ≤ warm·m_j^{−1}. Axes forced to zero have k_i ≤ warm.
  - Combined with the spatial root cap this gives density ≤ B/m_j, and with Pr(E) ≤ C·Pr_U(E) + η it gives excess mass ≤ 2η (verified).
- Mixed centers: a site-factoring mode has the site row as its constant row and is killed by the center average, so only the unweighted spatial law remains. This gives (1±ε) with a warm strip and a cold additive error.

**Corollary F.10 and Lemma 3.2(2).**
- Λ/MΛ deck coordinates are uniform under Haar on the cover.
- W ∩ MZ^d = MΛ, so the ambient extension on R^d/MZ^d is well defined.
- w and z are integer-linear in β, with rows reduced mod M, so no height enters.
- Per-atom error is η/#atoms, with log #atoms = poly(d)·log M.
- The normalization contributes |Z − 1|, using Σ|U||1 − 1/Z| = |Z − 1|.
- Moderate pure-free widths are k_iσ/T^ν ≥ A^jσ (pure-free sides are L), so they are uniform modulo M once A is chosen after M and σ.

**Noninjectivity (p.20; F.9 p.144).**
- At most |T|^2 = O(L^{2jm}) pairs. For a ≠ 0, one row of V·a = 0 fixes one entry, with probability ≤ max(mT_ℓ/(c_0σH), L/(scale·H)).
- Multiply by sup D_c/Z_c, which is a late quantity, height-free and includes m_j^{−1}. The total tends to 0 as the parent sides go to infinity.
- In the tree, the parent sides at layer j are the sides of T^{(j−1)}, which are ≥ the warm minimum at layer j−1, which in turn includes the layer-j requirements. Consistent with descending budgets.

**Theorem 3.4 cold clause (p.22–23).**
- X_r(φ) ≤ δ_sl^{−1}·E_U m_U|φ| holds because B ⊂ T with |B| ≥ δ_sl|T|.
- The tail bound uses m_U·1{m_U > 2cap} ≤ 2(m_U − cap)_+.
- Meshing and pigeonholing over a pre-bounded slice family (independent of g), then Lemma 3.3 in place of G.1, then the G.10 route via Gowers–Cauchy–Schwarz and Theorem A.7. On the box U, A.7 allows dimension n ≤ (2+p)^A, and here n is polynomial in the dimensions.
- Lemma G.11's Hahn–Banach argument: I rechecked the clipping estimate E|χ − v| ≤ (C/η)·E[m·1_{m>C_0}] and X(v) ≥ η·E|v|^2.

**§3.5 tree.**
- Feasibility (3.6) does not depend on the choice of representative, and b_{j,0} is unique since (1+γ/2)w_j < 1/2.
- Feasible center plus |y| ≤ v ≤ γw_j/2 gives the enlarged constraint along the whole path.
- e_j depends only on (W_j, l_j, w_j, γ). It is positive because a strict point gives an open feasible neighborhood in W_j/Λ_j.
- b_j(t) equals round(C_j(u) + l_j) when the constraint is < 1/2, so higher-layer constraints are genuine site functions of u. This is needed for §6's use of item 4 with insertions.
- Termination is trivial (fixed depth D). §3.5 claims no quantitative mass; the lower bound on e_j and the strict/enlarged comparison are deferred to Proposition 6.2, which uses Lemma 3.1 (ball of radius τv ≤ γw_j/2) and Lemma 3.2(4) with the conversion from unrestricted Haar to feasible centers (factor e_j). That use matches what §3 states.

## Parameter order and constant-cycle audit (F.1, §3.2, p.146, H.4)
- **Structural stage:** m, J_0, the kernel/free/modular block counts and C* depend only on dimensions and degrees. Lemma 4.6's needed number of axes, M ≥ (N+11)/c_r′, is structural.
- **Pre / cold-pre stage:** includes v (so Q_j), slices (relative costs, hence independent of L), test complexities, accuracies, the modulus caps (Lemma 4.6: log of moduli ≤ the cold-pre bound H and log(2/δ); §6: log Z pre; H.4: log Q pre), and family sizes.
- **σ:** chosen after the pre stage. Principal and constant widths are not narrowed by σ.
- **A:** chosen after σ and after all moduli. It must dominate σ^{−1}, M, γ^{−1}, and the enormous-axis fiber error L^{O(1)}/k_i times a factor which G.8 says is "independent of log L". I did not verify that this factor is free of R.
- **L:** chosen inside [A, A^{O(1+d)}].
- **R:** chosen after A, uniformly over that L range (p.146). It does not depend on the height or on the coefficients.
- **Parent sides:** chosen last.
- **Across layers:** layer-j late data, which are polynomial in cold-pre_j ∋ Q_j, enter only the layer-j parent sides and rank. The parent sides are T^{(j−1)}, fixed at the warm stage of layer j−1. Within my scope, nothing chosen earlier depends on anything chosen later.
- **Rank cuts:** they change W_j and hence the k_i and L, but neither R (uniform over the L range) nor cold-pre_j (forecasts only; "not … height of the prepared value space", Def. 2.3).
- **No constant cycle found in scope.**

## Union-bound bookkeeping (in scope)
- **Noninjectivity:** O(L^{2jm}) events, each ≤ sup D_c·L^{O(j)}/(σH). The budget is any prescribed accuracy, paid by H. §6 needs it ≪ a·∏_{i>j} e_i, which is warm at layer j and paid by the layer-(j−1) sides.
- **Mode removal:** the number of modes and the coefficient mass are exp(poly(log L, log σ^{−1}, cold-pre)), each removed to the F.7 error. The required R grows accordingly, and R is chosen after A.
- **Finite residues:** at most (number of coordinates)·M atoms, each with error η/#atoms.
- **One-site excess:** 2η.
- **Downstream (checked only for order):**
  - rank-stop at layer j ≪ a·∏_{i≥j} e_i, at cold cost in layers ≥ j;
  - modular-goodness ≪ a·∏_{i>j} e_i, warm;
  - flag errors per prime summed over ϖ ≤ Z, so the per-prime error must be ≤ c⋆/Z, with log Z pre.
  - All of these are fixed before the late choices, with no cycle.

## External inputs checked
- No bibliography item is cited inside §3 or pp.136–146.
- The analytic inputs are internal: Lemma B.1 (assumed in F.7; I checked that its hypotheses are met at the point of application), Theorem A.7 (used in the cold clause via G.10; I checked only that its box version allows dimension n ≤ (2+p)^A, which covers n = m_{j−1}), and Lemma G.11 (rechecked).
- I did not open LSS [35] or Schoen–Sisask [43]; they are other seats' scope.

## What I skimmed / did not check
- The proof of Lemma 3.3 (G.8 body, G.1–G.6).
- The warm clause of Theorem 3.4 (§5, Lemmas 5.1–5.2).
- Proposition H.1 and Property 3 of F.2.
- I.6 and the rest of App. I beyond I.1, so the §3.4 "same inspection" claim for I.6 is unchecked.
- Lemma B.1's proof.
- Whether D (§9) is fixed before the D-dependent structural constants.
- Whether the "late factor" in the enormous-axis fiber error (G.8) avoids R.
- Theorem A.7's proof.
- Lemma 6.1 and Proposition 6.2 proofs beyond the interface.

## Verdict
HOLDS AS READ IN SCOPE (EXPOSITION only: E1–E6; E1 and E2 are the substantive ones — §3's ensemble is a modified version of F.2's, re-verified piecemeal rather than cited, and App. F is stated for degrees ≤ s while §3 runs at degrees up to D).
