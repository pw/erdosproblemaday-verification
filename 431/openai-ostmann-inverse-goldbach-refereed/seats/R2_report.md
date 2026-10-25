# R2 referee report — §§4–5 (printed pp. 21–45)

STATUS: COMPLETE

Scope: §4 "Translated characters of higher order" (Prop. 4.1, eqs. (4.1)–(4.15), Cor. 4.2, eq. (4.16)),
§5 "A supply of nonsparse additive transforms" (Prop. 5.1, eqs. (5.1)–(5.22), Lemma 5.2, Lemma 5.3, Remark 5.4).
Read for definitions: §1, §2 in full (Lemmas 2.1–2.5, eq. (2.6) collision stability), Prop. 3.1 + Cor. 3.2;
for downstream use: §6 opening (ε_q of (6.1)) and p. 54 end of §6, §7 pp. 55–57, §8 p. 69.

## 1. VERDICT

**§4: HOLDS AS READ.** **§5: HOLDS AS READ.** No FATAL or GAP finding. Three EXPOSITION items below
(none load-bearing). Caveat on depth: §4 is written at very high compression (a ~13-page proof of a new
large-values estimate at the √X barrier); I reconstructed every step listed in §3 below, but some steps
("the elementary counting property of independent uniform group variables", the precision bookkeeping
"known modulo R^{k+2−h}", the "polynomial in m" degree/count bounds) were checked at the level of
"the claimed bound follows from the stated mechanism", not re-derived with explicit constants.

## 2. Objections

**E1 (EXPOSITION) — p. 44, Remark 5.4; reference [29].** The remark cites
"Theorem~1.1 of \cite{OpenAIQRH2026} implies that \eqref{eq:src33} also holds when the sum includes
\emph{all} primitive characters ... every nontrivial zero then has real part at most $7/8$."
[29] is "OpenAI, The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8, ... September-30-2026",
i.e. an unrefereed preprint asserting a zero-free half-plane for all Dirichlet L-functions, dated six days
AFTER this paper's own date (title page: "September 24, 2026"). The remark itself says
"The proof of Proposition~\ref{prop:supply} ... uses the classical estimate of
Lemma~\ref{lem:supply-total-prime-error}, not this zero-free theorem", and I confirm nothing in §5 or
later (grep of §§6–9 for the label/7/8) depends on it. Fix: delete the remark, or date the paper version.
A reader should not take the remark as evidence for [29].

**E2 (EXPOSITION) — p. 31, before (4.12).** "\(b_{aP}=\alpha_j\), where \(\alpha_j\) is the common parity
of the active pivot." Since every transfer keeps only the POSITIVE copy of a future pivot active
("For each future pivot retain only its positive copy as active"), α_j = 1 always; the case analysis
"either mixed pair corresponds to e_{j−1}=α_j" is correct but carries a vacuous parameter. My simulation
(below) confirms the pair formula with α_j ≡ 1. Harmless.

**E3 (EXPOSITION) — p. 36, proof of (5.4).** The letter U is used for R/t ("U=R/t=X^{1/2-o(1)}") and,
two pages later, for \(\mathcal U(1,1)\) (the main term of (5.21)); also z in §5 (=X/(m_A m_D)) collides
with z = exp(3εk) of §4. Local, harmless.

(No FIXABLE/GAP items. Specific candidate holes I examined and cleared are in §5 of this report.)

## 3. What I checked and how

### §4 (Prop. 4.1)
- Negation set-up, three-interval selection, density-increment for the late block [U,U+5k]
  (terminal k in {K_0,…,K_0M^h}; c_1, h independent of K_0), rich shells (c_0 = c_1/2 indep. of k).
- Typical endpoints: Lemma 2.5 with b=10 on any A' ⊂ A_X of size ≥ √X/(log X)^{10}; via (2.7)
  Σ(1/p)|E_{A'}f_p − E_{S_p}f_p|^2 ≤ e^{−αL}·O(log log X) = O(L e^{−αL}) = o(1); tested primes have
  log p ≤ (log X)/4 < cutoff. Bounded number of tested sets for fixed k. OK.
- Bin J: bulk contribution m·e^{u_2} = o(τ) (gap ≫ L), so (1−o(1))τ ≤ J ≤ eτ+o(τ) ≤ 4τ; pigeonhole
  losses e^{O(L)} = e^{O(m/z)} absorbed with C indep. of k. OK.
- Targets: T_j recurrence (S_j = c_j + 2S_{j+1} ⇒ ΣT_j = Σ2^{j−1}c_j, J-part (4^k−1)J/3); positivity
  and c_*2^kτ ≤ T_j,T_F ≤ 600·4^kτ; [log T−2εk, log T−εk] ⊂ late block and below (log X)/4 for
  e^{εk} > 2.4. Kneser/DeVos covering of multiples of g in [r_0 s,(n−r_0)s] re-derived. OK.
- ψ = φ^2 construction (ψ ≥ c on [0,1], \hat ψ = β*β compact). OK.
- Repeated-prime tuples: period ≤ M/p_min with log p_min ≥ e^{αL} ≫ Δ_0 = O_k(L); bandlimited Poisson
  leaves only the complete mean, zero if some prime occurs once (nonprincipal); all-multiple tuples:
  Σ_d d^{b_*}(CL)^d/d! ≤ b_*^{b_*}e^{CL}, and L^{−2m} cancels the log L in b_*^{b_*}; error
  √X exp(−B_D m/2 − 8 log z·m + Cm) ≤ ½ I_* once B_D > 4C. Hence (4.4) with B_0 indep. of B_D,k. OK.
- Level-zero phase (4.6): Gauss transform of zχ(x−t) at −a gives z e_p(at) χ̄(a) τ(χ)/p, so
  translation becomes the additive factor A_I(v), unary κ_iλ_i(v)^{−1}, rows λ_i(M/p_i) (b_ih=1);
  conjugate roles likewise. Zero frequency / non-coprime v vanish. OK.
- Transfer (4.7)–(4.9): re-derived the grouping by u = v/H mod P (pivot factors depend only on u,Y,tuple;
  regular-slot invariant), CS over u then priors, point mass e^{d_j}/P (d_j = Cn_jL+O_k(1)); off-diagonal
  substitution P=(vH_R−wH_L)/s, |s| ≤ V_j from E_j − E_{j−1} − Δ_j = 4^j√m/2 > 0; common prime of H_L,H_R
  impossible; additive-phase identities (left s/H_R, right s/H_L, shared v/(PH_L)−w/(PH_R)=s/(H_LH_R));
  incoming pivot rows ⇒ cross rows t·b_{iP}; Y–Y rows cancel; unaries of regular slots become
  λ_i(s)^{−tε_i}. All three invariants preserved. OK.
- History uniqueness: |vw'−v'w| ≤ |s|·2V_{j−1}e^{−Δ_j+O(1)} with E_{j−1}−Δ_j = −2·4^{j−1}√m ⇒ determinant 0;
  coprimality of pivot with frequencies forces ratio 1. OK.
- (4.10): |W_l|^2 ≤ e^{−rΔ_0+O_k(1)}; residue domination exp(CrL)/Q ≤ exp(CrL)/φ(Q); per-node
  square-root congruence X_L^2 ≡ c (mod |s|/g) with c a unit (g = gcd(v,s) = gcd(w,s) required),
  ≤ 2^{ω+1} roots ⇒ exp(o_k(m))g/|s|; Σ_s (v,w,s)/|s| = exp(o_k(m)); leaves (2V_0)^r = exp(rΔ_0+o_k(m))
  cancel. Bound is in fact exp(CrL+o_k(m)). OK.
- One-sided interaction (4.11): this is the only character-sum input of §4 and it is NOT a Weil bound.
  Translations never reach it: the centres t_p live only in the additive phases A_I, which cancel EXACTLY
  in every quotient that is estimated (cases (a),(b) compare terms with the same prime multiset, the same
  root frequency and prime-indexed centres), so degenerate/coinciding centres are irrelevant. What is used:
  after CS removes U(p) and positivity extends the long prime p to all integers n (point bound e^{CL}/p),
  for q≠q' the product ξ_q ξ̄_{q'} is a nonprincipal character mod qq' (ξ = λ^{±2}, ord λ > 2), with
  complete sums zero along any progression of step Q_* coprime to qq'; partial summation against weights of
  sup+variation ≤ exp(poly_k(m))/b gives exp(poly)Q_*qq'/b, and log b ≥ e^{Ω(L)}·log q, log b ≥ e^{αL},
  so this is ≤ exp(−ce^{αL}). q=q' costs the short-prime point mass ≤ exp(CL − e^{αL}). Hypotheses
  (nonprincipal; gap ≫ L in u between the two roles; no reverse factor) hold at both application sites. OK.
- Coprimality cleanup: x | N(x,·) iff x | N(0,·); identically-zero ⇒ discard; else Schwartz–Zippel with
  max point mass exp(−ce^{αL}) and ≤ exp(O_k(L)) prime divisors of a nonzero value (log|N| ≤ exp(O_k(L))). OK.
- Anchor codes and diagonal (4.12)–(4.13): **verified by exact simulation** of the update rule (4.9) for
  k = 1,…,6 (`R2_work/codes.py`): regular-slot invariant b_ih = ε_i; pair formula (4.12) (with α_j=1);
  every code occurs on ≤ 2 paths; code + final parity determines the path; for any two paths with
  different codes there is an anchor with net exponents (±2,0) (small anchor) when parities agree and
  (0,±2) (big anchor) when they differ. **Controls:** two mutated update rules (drop the copy sign on
  incoming outside rows; drop the sign on cross-copy rows) both FAIL the pair-formula assertion.
  Diagonal count: C_H ≤ L^{−rm}e^{Crm}, (2m)^{rm} code-preserving matchings, e^{T_j} values of P canceled by
  the extracted e^{−T_j−Δ_j}: exp(−Δ_j + rm(log z + C)), with Δ_j ≥ rm(B_D + 20 log z). OK.
- Budget (4.14): 𝔞_j ≤ B_0 + Σ(d_h+log 2)/(2^h m) < B_0 + 1 + o_k(1) using Σd_j ≤ Cn_cL < m
  (n_c ≪ ke^{2εk}, m = e^{3εk}L). Order of constants: δ,c → C → B_0 → B_1 → B_D → K_0 → k → L. Consistent.
- Final comparison (4.15): μ-invariance under within-parity permutations; ‖Φ_π‖^2 from (4.10) + uniqueness;
  π≠ρ ⇒ some bulk prime on two same-parity paths ⇒ different codes ⇒ small-anchor one-sided square;
  log J_* ≥ rm(k log 2 − C), log V_k = rm(B_D + 60εk) + o_k(m), margin k(log 2 − 0.006) − B_D − O(1). OK.
- Sanity test (the brief's item 6) for §4: the argument provably cannot run for quadratic characters —
  the code-changing interaction is λ^{±2}, principal when ord λ = 2 — consistent with the true obstruction
  A = squares (χ_p(n^2) = 1). For ord λ > 2 the analogous "power" sets (cubes etc.) have size X^{1/3} ≪ √X.

### Cor. 4.2 vs what is later needed
- Statement: outside harmonic mass o(L) in αL ≤ log log p ≤ βL, uniformly, σ_p = ½+o(1) and
  max over a ∈ F_p and ALL multiplicative λ (principal and quadratic included, zero at zero) of
  |E_v g_p(v)λ(v)e_p(av)| = o(1). Gauss-formula identity re-derived; principal case = p^{−1/2}F_p(a);
  quadratic case from Prop. 3.1/Cor. 3.2, order > 2 from Prop. 4.1; balance from (2.6)'s imbalance term.
- §6 needs exactly ε_q of (6.1) (max over χ ∈ \hat U incl. principal, a ∈ F_q), g(0)=0, E|g|^2 ≤ 1:
  matches. §7 (p. 55, item (iii)) uses it only on "a subset ... of harmonic mass ≫ L ... on which
  (4.16) holds uniformly"; no "most p" → "all p" slip. Prop. 5.1 is used in §7 only on "favorable" primes
  (g̃_p := 0 elsewhere), §8 only for the location [e^{.049L},e^{.95L}] of giant cells. OK.

### §5
- (5.2): Lemma 2.5 at Y = X(log X)^{40}, b = 4, cutoff > R; σ^{-1}+(1−σ)^{-1}−4 = κ+κ^{-1}−2;
  (log t)^2 ≤ t+t^{-1}−2; CS. OK.
- (5.3) energy identity: re-derived (Ramanujan sum factorises; p1_{x=y}−1 = κ_p + p⟨Q e_x,Q e_y⟩ on S_p,
  κ_p^{-1} on T_p). **Verified numerically** (`R2_work/supply_num.py`) for q = 3·5·7, 5·7·11, 3·7·13 with random
  half-sets S_p and 400 random integers with residues in S_p: |LHS−RHS| ≤ 2e−10; **control** with κ_p^{-1}
  in place of κ_p: discrepancy 2.3–4.0 (fails, as it must).
- (5.4)/(5.5): squarefree proportion ≥ 1−Σp^{-2}; coprime-to-t loss o(1); Markov on Σ_{p|u}|log κ_p|;
  large sieve (X+R^2)/m_A. OK.
- Lemma 5.2: u_S = p^{-1}(1+√κ F), u_T = p^{-1}(1−F/√κ) checked; u_S^*Πu_T = −‖ΠF‖^2/p^2; side blocks
  O(ε_0/√p) via Q_TF = 0 and ‖ΠF−F‖ ≤ ε_0√p; **‖Q_SΠQ_T‖ ≤ ½ uses Q_SQ_T = 0, i.e. disjoint supports**;
  B^{(2)} eigenvalues (t_0^2/p)#{h+h'=s} ≤ t_0^2ε_0; scalar block ≤ 1−(1.7−O(ε_0))/p; 2×2 block-norm
  eigenvalue bound; U_p via (5.9) (Σ_{x≠0}b = −t_0e*, Σ_{x≠0}b^2 = t_0^2(e*−e*^2)). OK.
- Tensor/truncation (5.11)–(5.13): R_K of ∏(1+ub)(1+vb) = W; Cauchy coefficient bound on the polydisc
  r_0 = 1.03; R_K𝓛 supported on ≤ 2K centred modes, so ‖P_AV_A‖^2 = Σ_{t∈𝒯_{C_*}}B_A(t) with C_* > 2C_K. OK.
- Lemma 5.3 (prime mean): Landau–Page + zero-free region (one character omitted, valid up to height T = Q^5);
  density bound ⇒ F(y) ≪ Be^{Ay}; integration by parts ⇒ B e^{−Mu_0/2}, Mu_0 ≫ e^{.1L}/K; low zeros
  X^{1/2}Q^7, high zeros XQ^{−8}, remainders Q^2; principal by PNT. Note: the argument only needs SOME
  density estimate of shape (Q^2T)^{C(1−σ)}(log QT)^{O(1)} (because M = e^L ≫ log Q = O(Ke^{.9L})), so the
  exact Montgomery/Inoue exponent is not load-bearing. Exceptional-conductor deletion: induced conductors are
  squarefree products of primes of the (reduced) 𝒮, so C(χ_exc) = 0. Grouped coefficients
  |C(χ)| ≤ ∏_{p|d}C/√p·∏(1+C/p) ≤ e^{C'L}; Mellin coefficient bounds (5.18) via CS and (5.9). OK.
- Coverage step (5.22): primes with a representation using a ≤ R+N_* or −d ≤ R+N_* number
  ≤ X^{3/4+o(1)} (by (2.4)) and W ≤ X^{o(1)}; every other prime in supp φ(·/X) has a representation in
  A_0 × D_0 (since a,−d ≤ p < X); distinct primes ⇒ distinct pairs; W ≥ 0. Final arithmetic:
  c z e^{−L} ≤ e^{−1.6H+o(L)}√z with H ≥ .68L ⇒ √z ≤ e^{−.088L+o(L)} vs z ≥ e^{−o(L)} (from (5.5)). OK.
- **Where coverage and exclusion enter (brief item 6).** §5 uses BOTH. Coverage enters only at (5.22)
  ("This step uses coverage of the full prime set"). Exclusion enters through the disjoint residue supports
  A_0 mod p ⊂ S_p, D_0 mod p ⊂ T_p = S_p^c (§2.3, which is exactly where composite-exclusion is used) and
  through (2.6) balance; both are load-bearing in Lemma 5.2: Q_SQ_T = 0 gives ‖Q_SΠQ_T‖ ≤ ½, and the
  scalar contraction is −2t_0‖ΠF‖^2/p^2 = u_S^*Πu_T with u_S ⊥-supported from u_T. For A = B = N_0
  (all large primes plus composites in the sumset) no partition S_p, T_p exists and the coordinates of
  (5.11)–(5.13) are undefined; if one forced S_p = T_p = F_p the lower-right block becomes ‖QΠQ‖ = 1 and the
  scalar block 1 + O(ε_0/p): no contraction. So the section cannot "prove" a false statement for a genuine
  sumset. **Numerical check of Lemma 5.2 with controls** (`R2_work/contraction.py`, 2 BLAS threads, exact matrices
  on C⊕H_T → C⊕H_S, t_0 = .85, E_p = {|g_p|>1}):
  | case | p | γ_p | \|E_p\|/p | p(‖L_p(1,1)‖−1) | ‖L‖ ≤ U_p(1,1)(1−1.6/p)? |
  |---|---|---|---|---|---|
  | S_p = interval [0,p/2) (sparse spectrum), T_p = complement | 1009 | .169 | .020 | −1.623 | yes |
  | same | 2003 | .130 | .014 | −1.645 | yes |
  | CONTROL: same kernel, T_p := S_p (no exclusion / overlapping supports) | 1009 / 2003 | | | +1.711 / +1.707 | NO |
  | CONTROL: random balanced S_p (non-sparse, γ ≈ .89) | 1009 / 2003 | .888/.883 | .38/.36 | −0.626 / −0.654 | NO |
  The lemma's contraction (≈ −(1.7−O(ε_0))/p) appears exactly when the hypotheses hold, and disappears
  (indeed reverses to +1.7/p) when the supports overlap — the numerical form of "exclusion is load-bearing here".
  (An earlier run of this script used too many BLAS threads on the shared box; it was stopped by me and rerun
  at 2 threads with smaller p after a coordinator request.)
  Note (not an objection): §5 alone would survive with coverage of only a positive proportion δ of primes
  (it gives √z ≤ δ^{-1}e^{−.088L}); this is consistent, since Prop. 5.1 is a structural conclusion about S_p,
  not the contradiction.

## 4. What I could NOT check
- Cited statements verbatim (no source access offline): Montgomery 1969 Thm 1 / Inoue 2021 Lemma 1 (density
  bound with exponent 3(1−σ)/(2−σ) and (log QT)^{13}); Ford–Green–Konyagin–Maynard–Tao 2018 Lemma 7.1 (form of
  Landau–Page used); DeVos 2014 Thm 1 (Kneser). I checked they are used for statements of the standard shape;
  as noted, Lemma 5.3 is robust to the precise density exponent.
- §4's precision bookkeeping ("known modulo R^{k+2−h}", "at most k divisions on a branch") and the
  "polynomial in m" degree/count claims for reconstructed numerators: checked for plausibility and order of
  magnitude, not re-derived with explicit polynomials.
- Did not open the Lean for §§4–5 beyond listing Ostmann/{Characters (1201 files), Supply (178),
  ZeroDensity (474)}; nothing in the paper needed rescuing.

## 5. Where a hole would most likely hide in §§4–5
The one-sided interaction (4.11) as applied to the DIAGONAL (case (b)) and to the final permutation
comparison: everything in §4 hinges on (i) the additive (centre-carrying) phases cancelling exactly in the
compared pair, and (ii) the only joint dependence between the chosen short and long primes being a single
character factor ξ_q(p) with no reverse factor λ_p(q), all other dependence being either unary or
archimedean/residue (bounded variation, modulus Q_* coprime to the primes). I checked (i) (same prime multiset,
same root, prime-indexed centres), and (ii) by tracing that reconstructed pivots carry no characters (their
outgoing rows are removed in (4.7) and incoming rows are substituted via (4.8)), and by simulating the
exponent graph to confirm the net exponents (±2,0)/(0,±2). Code-preserving matchings get no cancellation and
are paid for by Δ_j ≥ rm(B_D+20 log z) against (2m)^{rm}L^{−rm} — the reason for the L-normalised bulk prior.
I believe this holds. The second candidate, the coverage comparison in §5, is clean: W ≥ 0, one pair per
prime, the small-summand representations are X^{3/4+o(1)} in number.
