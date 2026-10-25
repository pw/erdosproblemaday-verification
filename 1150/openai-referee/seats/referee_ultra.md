# Referee report — seat `ultra` — "Ultraflat real Littlewood polynomials" (/tmp/oaimath/076/paper/paper.pdf, 5 Oct 2026, 16 pp)
**This paper is NOT needed for Erdős #1150** (the #1150 answer rests on sib1's one-sided theorem / the Lean `main`); this report's
verdict is about THIS paper's two-sided theorem only. Inherited inputs: sib2 Lemmas 3.1 and 6.2.
Seat started 2026-10-12. Status: COMPLETE (running notes kept below; final sections at the end).

## Scope read (pages)
Paper pp. 1–16, every page from the rendered PDF (displayed math read off the render, text extraction only for grep). sib2:
p. 9 (Lemma 3.1 statement + Theorem 3.2), pp. 10–13 (proof of Lemma 3.1, read at skim-plus level), p. 13 top (fixing H, θ
before N), pp. 23–25 (Lemma 6.1 statement, Lemma 6.2 statement + full proof, start of §6.2). Lovett–Meka arXiv:1203.5747v2
Theorem 4 + §5 opening (refs/1203.5747/paper.txt, header confirms v2). Erdős 1957 pp. 296–298 (refs/erdos1957, scanned;
read from the render). BBMST Thm 1.1 (refs/1907.09464), Erdélyi Thm 2.1 (refs/2608.00744v1).

## Method
Read PDF render (displayed math) of every page, cross-checked with layout text; re-derive each estimate; check uniformity in t,
N, and across wave gaps; quote sib2 lemmas verbatim and compare hypotheses at the point of use.

## Findings (running)

### Running notes (first pass, after reading the PDF render of all 16 pages)
- Read pp. 1–16 from the rendered PDF (not the text extraction). Structure: Thm 1 (p.1) ⇐ §6 (pp.14–15) ⇐ Prop 5.1 (p.9) +
  Lemma 3.2 (p.4–5); Prop 5.1 ⇐ Prop 4.1 (p.6), Lemma 5.2 = sib2 Lemma 3.1 (p.10), Lemmas 2.2–2.3 (pp.3–4); Prop 4.1 ⇐ Lemma 4.2
  (p.6–7) ⇐ Lemma 2.1 + Lemma 3.2; Lemma 3.2 ⇐ Lemma 3.1 = sib2 Lemma 6.2.
- Design point that answers the scope question "is the lower bound uniform across the gaps": the LOWER bound is never a
  Fourier statement. B_N is built with |B_N(t)| = m_a ∈ [1, 1+Cδ] on main intervals and |B_N| = m_j(t) (linear interpolation of
  endpoint moduli in [1, 1+Cδ], and 1 at 0, 1/2) on gaps — so |B_N| ≥ 1 on all of T by construction (5.1). The gaps cost only
  on the FOURIER side ((5.2): outer pieces C√δ via (5.15), the one near-stationary middle piece + reflection C√L, L ≤ Cδ). The
  passage to signs is uniform on T because the exterior tail is absolutely summable (5.3) ⇒ (6.1) uniformly in t. So the gaps do
  not threaten the lower bound; checked line by line below.
- §2 Lemmas 2.1–2.3 (pp.3–4): re-derived. 2.1: completing the square + Fresnel transform gives the exact bracket
  ∫ĝ(ξ)e(ξy₀)e(−ξ²/(2Tβ))dξ; |e(−ξ²/(2Tβ))−1| ≤ πξ²/(T|β|) ⇒ error (π/(T|β|))∫ξ²|ĝ|, independent of y₀ (=u/(Tβ)) — uniform in
  u as claimed. 2.2: after the Morse change of variable the integral is Lemma 2.1 with T=N, β=±1, u=0 and amplitude
  g_x = f(t(y))t'(y); its ∫ξ²|ĝ_x| is bounded by finitely many C^k norms, uniformly in t_x ∈ I because y(t;t_x) is jointly smooth
  on a compact set with ∂y/∂t bounded above/below; the x ∉ φ'(I) case: dist(x, φ'(supp f)) ≥ dist(φ'(supp f), ℝ∖int φ'(I)) > 0
  since supp f ⋐ int I — the "bounded below uniformly" claim is correct. Uniform o(1) on x ∈ [0,1] holds. 2.3: standard
  (Fresnel primitive bounded; van der Corput first-derivative with monotone 1/Φ'). No objection.
- §3 Lemma 3.2 (pp.4–5): re-derived every step. Initial rounding cost ≤ n2^{−J} ≤ 1; odd multiples of 2^{−h} lie in
  [2^{−h},1−2^{−h}] so ±2^{−h} stays in [0,1] on the coarser grid; sign reversal keeps mass ≤ μ; s_h ≤ min(n,2^hμ) (each active
  coordinate has mass ≥ 2^{−h}); s log(80n/s) increasing on (0,n] (80n/s ≥ 80 > e); the 2^hμ>n case needs only μ ≤ n; geometric
  sum Σ2^{−h/2} gives (3.2). Grid-to-circle: |Q(z)| ≤ S|z|^{n−1} on |z| ≥ 1 (reversed polynomial), (1+1/n)^{n−1} ≤ e, Cauchy on
  radius 1/n ⇒ |d/dt Q(e(t))| ≤ 2πenS; grid spacing 1/(20n) ⇒ distance ≤ 1/(40n) ⇒ S ≤ max_grid + (πe/20)S, πe/20 ≈ 0.427 < 1.
  η_j − Z_j = −2d_j(p'_j − p_j) so ℜ,ℑ of Q(e(t_ℓ)) are −2(A(p'−p))_{2ℓ}, −2(A(p'−p))_{2ℓ+1}. Lemma 3.1 hypotheses at use:
  R = 40n, 1 ≤ s_h ≤ n ≤ R, entries ℜ/ℑ(d_j e(jt_ℓ)) ∈ [−1,1]. HOLDS.
- §4 Lemma 4.2 (pp.6–7): (4.3) from Lemma 2.1 (|g| ≤ 1) and L_β/(T|β|) → 1; exterior: for |u| > T|β|/2 and y in a
  neighbourhood of supp g ⊂ (−1/2+c, 1/2−c), |Tβy−u| ≥ max(2c|u|, cT|β|) ≳ T+|u|; two IBPs give terms g''/Φ'², g'Tβ/Φ'³,
  g(Tβ)²/Φ'⁴, each ≲ (T+|u|)^{−2} ⇒ (4.4) O(T^{−1}). Parseval: retained Σ|I|² ≥ 1−q−O(T^{−2}); 1−|Z| ≤ 1−|Z|² ⇒ μ/L ≤
  (4q+q²)/(2(1+q)²) ≤ 2q; Lemma 3.2 on L_β consecutive frequencies (shift) + x log(80/x) increasing on (0,1/2] ⇒ the displayed
  bound; pre-rounding distance ≤ q·(1+O(1/T)) + O(1/T). Order α → q → g → T. Equal magnitudes |a_{β,u}| = L_β^{−1/2} come out
  because Lemma 3.2's outputs are ±d_u, unimodular. f_{−β} := conj f_β is legitimate (target conjugates, frequency box
  symmetric). HOLDS.
- §4 Prop 4.1 (pp.6–9): p_j recursion |p_j| ≤ 1 via (1−r²)/2 ≤ 1−|r|; M_j−M_{j−1} = (1/8)∫(1−p²_{j−1})² ≥ (1/8)(1−M_{j−1})²;
  frequency bookkeeping (old frequencies persist with last coord 0; new ones have last coord ±1 ⇒ parallel members of S equal up
  to sign; ≥2 sign pairs since ∫(1−p₁²) > 0). W_j⁰ ∈ s_j^⊥ avoiding finitely many proper subspaces (needs d ≥ 2, pairwise
  nonparallel reps); (1/τ)Π_j|s·W_j| → |b_s|²/ρ_s since exactly one factor vanishes at τ=0. Telescoping ‖F − target‖ ≤
  (Σ|b_s|)Dα(1+α)^{D−1} ≤ δ; target = Πg(z_j)·p_d(y + (T/2)ΣW_j z_j²), norm ≤ 1. Box over s: n_s = ΠL members, magnitude
  |b_s|/√n_s; distinct a, a' parallel ⇒ s' = λs ⇒ λ = ±1. (4.8)/(4.9) recomputed from (4.5)+(4.7) and w_a = ρ_s/(τT^D(1+δ)³):
  |c_a|²/w_a ∈ [1+δ, (1+δ)³/(1−δ)²] — exactly as printed; total weight ∈ [(1−δ)³/(1+δ)³, 1/(1+δ)] so Σw_a < 1 strictly and
  ≥ 1−Cδ. Choice order δ, p_d, γ, (W⁰,W¹), τ, α, g, T: no parameter depends on a later one. HOLDS.
- §5 Prop 5.1 (pp.9–14), line by line:
  * Packing input (p.10): reps of the ≥2 sign pairs are pairwise nonparallel (Prop 4.1), w_{−a} = w_a, and
    2Σ_reps w = Σ_{a∈A} w_a < 1 — exactly sib2 Lemma 3.1's hypotheses. Arc for a is centred at −a·θ_h, its reflection is the
    arc for −a ⇒ disjoint ⇒ avoids 0, 1/2 ⇒ each arc sits in (0,1/2) or (−1/2,0); t*_{−a,h} = −t*_{a,h}.
  * |Q_h'(x)| = |∫_{x*}^x χ²| ≤ |J_h|/2 < 1/(2H) ⇒ |T_{a,h} − t*| < w_a/(2H): I_{a,h} strictly inside its packed arc (gaps > 0).
    T' = −λ_aχ_h² ≠ 0 (χ_h ≥ σ > 0) ⇒ diffeomorphism. ψ' = X + (t−t*)X' + λQ'(X)X' = X since t−t* = −λQ'(X); ψ'' = X' =
    −1/(λ_aχ_h(X)²). Symmetry: T_{−a} = −T_a, X_{−a}(−t) = X_a(t), ψ_{−a}(−t) = −ψ_a(t), c_{−a} = conj c_a ⇒ B_N(−t) = conj B_N(t).
    |I_{a,h}| = w_a∫χ² ⇒ (5.11). All correct.
  * Endpoint parts (p.11): on the support of 1−G_h∘X the phase is exactly quadratic, |ψ''| = 1/(w_aσ²); Lemma 2.3 with
    ‖f‖∞ + ∫|f'| ≤ 2 ⇒ √N·m_a·C√(w_aσ²/N) = C|c_a|σ; σ is chosen after H and A are fixed, so Σ_{a,h} ≤ δ is legitimate.
  * Coherent part: Lemma 2.2 at x = k/N; main term (√w_aχ_h·G_h)·(c_a/√w_a)·e(sgnλ_a/8 + sgnψ''/8)·e(N(ψ(T(x)) − xT(x))),
    sgnψ'' = −sgnλ_a so the eighth-phases cancel; ψ(T(x)) − xT(x) = −xt* + λ_aQ_h(x); e(−kt*) = e(k a·θ_h) because k ∈ ℤ;
    λ_a = a·v ⇒ Σ_a = G_hχ_h F(kθ_h + NvQ_h(x)), |·| ≤ 1+δ. J_h ⊂ ((h−1)/H, h/H) are disjoint ⇒ one h. Finite (a,h) ⇒ uniform
    o(1). (5.13) correct. NUMERIC CHECK (toy F on T², H = 2, σ = 0.2; script /tmp/ultra_scratch/coh*.py): Σ_a √N∫G_h(X)B_N e(−kt)
    vs G_hχ_hF(kθ_h+NvQ_h(k/N)) — max error over 10 indices 0.183 / 0.056 / 0.027 at N = 3e3 / 3e4 / 3e5 (pre-asymptotic: my
    cutoffs are sharp), mid-J_h indices agree to 4e−5–2e−3 with |pred| up to 1.07. NEGATIVE CONTROLS: flipping t* ≡ +a·θ_h, or
    flipping the eighth-phase sign, gives max error 0.97 / 1.56 — the instrument can fail; the paper's conventions are right.
  * Gaps (pp.12–13): the LOWER modulus bound across gaps is by construction (m_j ≥ 1, linear between endpoint moduli in
    [1,1+Cδ], 1 at 0 and 1/2) — not a Fourier statement, so "uniform across the gaps" holds trivially for B_N. Fourier cost:
    outer pieces exactly quadratic with |Λ| arbitrary large (P_j ≠ x_{u_j}, R_j ≠ x_{v_j}), Σ|Λ|^{−1/2} ≤ √δ, (5.18) constant
    absolute (sup ≤ 2, ∫|m'| ≤ Cδ, ∫|γ'| ≤ 1) ⇒ C√δ irrespective of x; middle pieces slope ∈ [1/(4L), 1/(2L)], derivative ranges
    [P_j,R_j] disjoint with total length 1/4 and the reflected piece has the SAME range (φ̃' (t) = φ_j'(−t)) ⇒ at most one pair
    near-stationary, contributing 2C√L ≤ C√δ; the rest O(1/(ρ√N)). (The disjoint-range device is essential: with a common
    range the middle pieces would cost ~Σ_j √l_j, not small.) (5.2) with an absolute C: verified.
  * Exterior tail (pp.13–14): φ' ∈ [c,1−c] everywhere (J_h ⊂ (0,1), P_j,R_j ∈ (1/4,3/4), x_0 = x_{1/2} = 1/8) ⇒ |V| ≥ (c/2)(N+|k|)
    for k < 0 and k ≥ N (checked: k−N(1−c) ≥ (c/2)(N+k) for k ≥ N). First IBP boundary term B_N e(−kt)/(2πiV) is continuous
    across every join (B_N continuous, φ' matched incl. at 0 and ±1/2 where B_N = 1, φ' = 1/8, e(−k/2) = e(k/2)) ⇒ telescopes.
    Second IBP: A = f'/V² − fV'/V³, A' as printed; |A|+|A'| ≲ D^{−2} using N ≤ D; boundary terms need not cancel. ⇒ |B̂(k)| ≲
    (N+|k|)^{−2} ⇒ Σ_ext = O(1/N) = (5.3). NUMERIC CONTROL (/tmp/ultra_scratch/tail.py, generic piecewise-linear φ'): matched φ'
    ⇒ N·Σ_ext = 4.81/4.83/4.87/4.86/4.86 for N = 256…4096 (i.e. O(1/N)); NEGATIVE: one jump in φ' with B continuous ⇒ Σ_ext ≈
    0.34–0.35 flat in N (O(1), as the IBP predicts); a jump in B ⇒ Σ_ext ≈ 1.4 (truncated at M/2). The derivative matching is
    exactly what the summable tail needs, and the paper supplies it.
- §6 (pp.14–15): Y_k ∈ [−1,1] by (5.2) with C_1 := C; (6.1) = B_N/S_δ minus S_δ^{−1}Σ_ext, ≤ K_δ/(NS_δ) uniformly; Parseval +
  |B_N| ≥ 1 ⇒ (1/N)ΣY_k² ≥ S_δ^{−2}(1 − K_δ²/N²); |Y| ≥ Y² ⇒ μ/N ≤ ½(1−S_δ^{−2}) + o(1) ≤ q_δ < ½; Lemma 3.2 (real inputs ⇒
  ±1 outputs) ÷ √N with x log(80/x) increasing on (0,½]. Lower bound S_δ^{−1} − E_δ − o(1), upper (1+Cδ)/S_δ + E_δ + o(1),
  E_δ ≍ δ^{1/4}√log(1/δ) → 0; ε → δ → N₀ order is correct. z = ±1: B_N(0) = B_N(½) = 1 so P(±1)/√N → 1/S_δ — no special case,
  no parity obstruction. No divisibility condition on N anywhere (N enters only via e(Nψ), e(Nφ_j+γ_{j,N}), x = k/N). HOLDS.

## Findings
No FATAL. No GAP. EXPOSITION only:

1. EXPOSITION (p.2, §1.2, lines 1–3): "Its Fourier coefficients of indices 0, . . . , N − 1 are real and at most (1 + o(1))/√N
   in absolute value". Prop 5.1 delivers (1 + C√δ)/√N with δ FIXED as N → ∞ ((5.2)); the "o(1)" is only true in the iterated
   limit N → ∞ then δ ↓ 0. Same for "whose modulus is close to one" (within Cδ). §6 handles the quantifiers correctly (δ fixed,
   N → ∞, then δ chosen from ε), so this is a loose overview sentence, not a proof defect.
2. EXPOSITION (p.10, after (5.6)): "Choose smooth real Q_h with Q_h'' = χ_h², Q_h'(x*_h) = 0, and with a smooth extension to a
   neighborhood of J_h." Lemma 2.2 (applied on p.11) needs ψ_{a,h} smooth with ψ'' ≠ 0 on a NEIGHBOURHOOD of I_{a,h}, i.e. the
   extension must keep Q_h'' > 0 (so that T_{a,h} stays a diffeomorphism and X_{a,h}, ψ_{a,h} extend). Not said; trivially
   available since χ_h ≡ σ near the endpoints (extend Q_h'' ≡ σ²).
3. EXPOSITION (p.11, "Split each integral over I_{a,h} using the cutoff G_h(X_{a,h}(t)). On either endpoint part the phase has
   constant second derivative of modulus 1/(w_aσ²)."): Lemma 2.3 requires ψ'' = Λ on the WHOLE interval of integration; the
   interval to use is T_{a,h}(E_±) with E_± the endpoint intervals where χ_h = σ (which contain supp(1−G_h) by the choice of
   G_h). Correct as intended; the interval is left implicit.
4. EXPOSITION (p.10, Lemma 5.2): restatement of sib2 Lemma 3.1 drops "Let m ≥ 1 … be integers" — harmless (A ⊂ ℤ^m, m = d+D ≥ 3).
   (Otherwise a faithful restatement — see External inputs.)
5. EXPOSITION (p.4, Lemma 3.1 proof): "This is [13, Lemma 6.2], whose statement applies to arbitrary real matrices in the displayed
   rectangular range." Accurate (sib2 Lemma 6.2 is stated for "a real matrix B ∈ [−1,1]^{R×s}", 1 ≤ s ≤ R); only the matrix
   letter and constant name differ.

Things I specifically tried to break and could not:
- Uniformity of stationary phase in the angle/index (Lemma 2.2 uniform on x ∈ [0,1], including t_x at ∂I and x ∉ φ'(I)).
- Constant cycles: §4 order δ → p_d → γ → (W⁰,W¹) → τ → α → q → g → T; §5 order (Prop 4.1 data) → (H,θ) → σ → (J_h,χ_h,G_h,Q_h) →
  gaps (u_j,v_j,P_j,R_j, outer lengths per (5.15), ρ) → N₀(δ); only γ_{j,N} depends on N and its bounds (∫|γ'| ≤ 1,
  |γ'| ≤ 1/l_j) do not. No constant multiplying δ or √δ depends on δ-dependent data (checked each: 2δ, σ-endpoints ≤ δ,
  (5.18) absolute, L ≤ Cδ from (5.11) with the absolute C of Prop 4.1). This matters because S_δ = 1 + C₁√δ must have C₁ absolute.
- Two-sided comparison (4.9): recomputed from (4.5), (4.7) and the definition of v; matches to the exponent.
- Coherence breaking between a and −a (would happen if the e(·/8) sign or the t* ≡ −a·θ convention were wrong): numerically
  confirmed right, with negative controls that fail by O(1).
- The "summable exterior tail" (the new part): the IBP is correct and the first boundary terms genuinely telescope; numeric
  control shows that without the φ'-matching the tail is O(1), with it O(1/N).
- Every-N delivery: no divisibility, block or H | N condition; H is a packing multiplicity, not a block count.

## External inputs checked (source, version, exact statement vs use)
- sib2 Lemma 3.1 (p.9), verbatim: "Lemma 3.1 (Signed interval packing). Let m ≥ 1 and r ≥ 2 be integers, and let
  a1, . . . , ar ∈ Z^m\{0} be pairwise nonparallel. If w1, . . . , wr > 0 and 2 Σ_{i=1}^r wi < 1, there are an integer H ≥ 1 and
  points θ1, . . . , θH ∈ T^m for which the 2rH closed intervals I(σai · θh, wi/H), 1 ≤ i ≤ r, 1 ≤ h ≤ H, σ ∈ {−1, 1}, are
  pairwise disjoint." [I(c,ℓ) = {c + x (mod 1) : −ℓ/2 ≤ x ≤ ℓ/2}.] Use (p.10): one representative per sign pair of A; hypotheses
  — integer nonzero vectors ✓ (A ⊂ ℤ^m∖{0}); r ≥ 2 ✓ ("at least two pairs"); pairwise nonparallel ✓ ("distinct pairs
  nonparallel"); w > 0 ✓; 2Σ_reps w = Σ_A w_a < 1 ✓ ((4.1), strict, total ≤ 1/(1+δ)). Conclusion used: arcs centred at −a·θ_h
  for all a ∈ A — this is the σ-family. H, θ fixed before N (sib2 p.13: "we fix one prime and one matching"). Same statement as
  sib1 Lemma 3.1 (sib1 p.5) word-for-word up to "there exist"/"there are". Proof skimmed at the level of: degree via fibre count
  q^{b−1}Z, codegree ≤ q^{b−2} (pairwise rank 2 over F_q), exclusion set E_i = O(R), first/second conditional moments
  p^{r−1}+O(q^{−1/2}), Chebyshev with ε_q = q^{−1/8}, deletion of ≤ q^{7/8} vertices costing O(q^{−1/8}D_q), Pippenger–Spencer
  ⇒ H = (1+o(1))q/(2L), w_i/H < L_i/q ⇒ strict containment in slot intervals with disjoint interiors. Nothing wrong found at that
  level; the Alon–Yuster quantifier check is the `construct` seat's (sib1 Theorem 3.2 is the same text).
- sib2 Lemma 6.2 (p.24), verbatim: "Lemma 6.2. There is an absolute constant C0 such that, for integers 1 ≤ s ≤ R and a real
  matrix B ∈ [−1, 1]^{R×s}, there is a vector ξ ∈ {−1, 1}^s satisfying ‖Bξ‖∞ ≤ C0 √(s log(2R/s))." Use (p.5, via Lemma 3.1):
  R = 40n, s = s_h with 1 ≤ s_h ≤ n ≤ R (applied only at nonempty stages), entries ℜ/ℑ(d_j e(jt_ℓ)) ∈ [−1,1] ✓. Proof read in
  full: Lovett–Meka partial colouring with c_i = 4√log(16R/u) (threshold sum exactly u/16), ‖restricted row‖₂ ≤ √u, u_h ≤ 2^{−h}s,
  u log(16R/u) increasing on (0,R], Σ2^{−h/2}√(1+h/4) < ∞, log(16R/s) ≤ 4 log(2R/s) for s ≤ R ⇔ (R/s)³ ≥ 1. Correct; the
  η → 0 compactness step (finitely many coordinate sets, closed inequalities) is valid.
- Lovett–Meka arXiv:1203.5747v2 Theorem 4 (paper.txt l.114–120, header "arXiv:1203.5747v2"): vectors v_1..v_m ∈ ℝ^n, x_0 ∈
  [−1,1]^n, c_j ≥ 0 with Σexp(−c_j²/16) ≤ n/16, small δ > 0 (the proof assumes δ < 0.1); with probability ≥ 0.1 finds
  x ∈ [−1,1]^n with |⟨x−x_0,v_j⟩| ≤ c_j‖v_j‖₂ and |x_i| ≥ 1−δ for ≥ n/2 indices. sib2's paraphrase ("for every sufficiently small
  η > 0 … existence") matches.
- Erdős 1957 (refs/erdos1957, scanned, read from render): Problem 26 (pp.297–298) is "Does there exist, for each n, a polynomial
  f_n(z) = Σ_{k=1}^n ε_{nk}z^k (ε_{nk} = ±1) such that, for all θ, c₁√n < |f_n(e^{iθ})| < c₂√n …?" — the paper's "[8, Problem 26]"
  attribution for the two-sided question is CORRECT. (Problem 22 is the unimodular |a_k| = 1, (1+c)√n question — consistent
  with the live-thread remark that Problem 22 reads like #230.)
- sib2 Theorem 1.1 (p.2): (1/16)√N ≤ |Σε_kz^k| ≤ (1+η)√N — matches the paper's p.2 quotation.
- BBMST arXiv:1907.09464v1 Thm 1.1: constants Δ > δ > 0, all n ≥ 2, Littlewood polynomial of degree n with δ√n ≤ |P| ≤ Δ√n —
  matches "two-sided constant-factor statement at every degree at least two".
- Erdélyi arXiv:2608.00744v1 Thm 2.1: max|P_n(e^{it})|² ≥ n + 1 + n^{1/3}/38 for P_n ∈ L_n (degree n) — with N = n+1 equals the
  paper's N + (N−1)^{1/3}/38; compatible with Theorem 1 (o(N)). Not an input.

## What I skimmed / did not check
- sib2 Lemma 3.1's PROOF: skimmed (pp.10–13), not re-derived inequality by inequality; Pippenger–Spencer/Alon–Yuster quantifiers
  not checked against Alon–Yuster here (that is the `construct` seat's scope for the identical sib1 Lemma 3.1).
- Lovett–Meka's proof of Theorem 4 (only the statement and the δ < 0.1 assumption).
- Not checked (not load-bearing, not on disk): Bombieri–Bourgain [3, Theorems 4 and 7]; Erdélyi [7, Theorem 2.1] (J. Approx.
  Theory 313, 2026); Kahane [9]; Littlewood [10]; Rudin [15]; Spencer [16]; BBMST Sections 2.1 and 4.
- No end-to-end numerical construction of B_N with small δ (would need a real packing with large H); numerics were targeted
  toy checks of the two load-bearing mechanisms (coherent identity incl. sign conventions; exterior-tail summability), each with
  negative controls that fail.
- Lean: this paper has no formalization; nothing here bears on the #1150 Lean object.

## Verdict
HOLDS AS READ IN SCOPE — the two-sided theorem (Theorem 1, both bounds, all |z| = 1 incl. z = ±1, every N ≥ N₀(ε)) follows from
Prop 5.1 + Lemma 3.2 as written; sib2 Lemmas 3.1 and 6.2 are quoted faithfully and applied within their hypotheses; five
EXPOSITION items, none affecting the proof. (Reminder: this paper is NOT needed for Erdős #1150.)
