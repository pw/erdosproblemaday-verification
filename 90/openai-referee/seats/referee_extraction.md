# Referee report — seat "extraction" (Section 7, PDF pp. 36–42, + brief item (vi))

STATUS: COMPLETE (2026-10-14). Paper read from /tmp/oaimath/167/paper/paper.pdf (pp. 36–42 rendered and read
as images; every displayed formula below was checked against the rendered PDF, not the pdftotext).
Also read, for definitions only: §2.3 (Prop 2.4, (2.4), (2.5), (2.9)), Lemma 2.5–2.7, §4.1–4.2 (Lemma 4.1, 4.2,
(4.7)–(4.9)), §4.4 (consistency, Lemma 4.5), §5.1–5.2 (Lemma 5.1, levels C/B/G, I_x, H_x*, Lemma 5.2, the scores,
Prop 5.5's proof, Prop 5.6), statements of Prop 6.3 ((6.8),(6.9)) and Prop 6.5.

## Verdict for my scope

**HOLDS AS READ.** Every inequality, constant and identity in §7 checks out line by line, conditional on the
inputs §7 imports (listed in "Inputs" below; they are other seats' scope and I did not re-verify them). I found
no mathematical gap and no exposition gap of GAP severity in §7. All objections below are COSMETIC. The
finite checks (exact arithmetic in Q(i) with the full place list; brute force of the level-wise combinatorics;
a grid-label simulation of Lemma 7.1's archimedean place bound) all pass, and each has a control that fails.

Inputs §7 uses (not verified by this seat): Prop 6.3 (6.8) C_Q = o(S); Prop 6.5 (6.12) liminf E_µH_p*/S > 0;
Lemma 5.2 (5.5),(5.6); (5.3) W_c ≤ S/ε, W_b = o(S); Lemma 4.5 (4.18) E_E m = O(1) absolute; Lemma 4.5's
label-match implications (c_v = √2 at infinity); Lemma 4.2 (4.3) Σ*|log|u|_v| = 2h(u); Lemma 4.1 product formula;
Prop 2.4 (2.2)–(2.5); Lemma 5.1 (k^20/d_{Q,min} → 0, k = t^{o(1)}); S → ∞ (Prop 4.4).

## Status of each result in scope

| Result | Status |
|---|---|
| (7.1) (collected bounds) | VERIFIED (each item traced to its source: (5.5), (4.18), (5.3)) |
| Lemma 7.1 incl. (7.3), one-sided argument, (5.14)-identity, constants 3 and 2 log 2 | VERIFIED LINE BY LINE (+ brute force + place simulation) |
| Lemma 7.2 incl. absorption, (7.5), (7.6), layer cake, marginal expansion bound, Cauchy–Schwarz, Young | VERIFIED LINE BY LINE (+ exact layer-cake check) |
| (7.7) profiles | VERIFIED (well-defined; ‖a_p‖_1 ≤ H_p*) |
| Lemma 7.3 incl. the 4-case identity, residual, E_1/E_2 composition, exact identity, (7.9) | VERIFIED LINE BY LINE (+ brute force) |
| Lemma 7.4 incl. discards, bands, (7.10), (7.11), p ≠ r | VERIFIED LINE BY LINE |
| Lemma 7.5 incl. M, P_mult, three terms of (7.12), comparison with R_0 log 2R_0 | VERIFIED LINE BY LINE |
| Prop 7.6 incl. distinct-pair count, (7.13), (7.14), b_pr, rectangle cancellation, (7.15) | VERIFIED LINE BY LINE (+ exact Q(i) rectangle) |

## Line-by-line notes (what I actually derived)

### Lemma 7.1 (p. 36–37)
Setting at a good rare level (v,s): minority bit r, majority b = 1−r; the "relevant" coordinate (the one shared
by consistent majority-bit edges) is B1 if r = 1, A if r = 0 (§5.1, "On every consistent majority-bit edge the B1
labels match if r = 1, and the A labels match if r = 0" — correct: a consistent bit-0 edge has exactly B1 equal).
X, U, V = exception indicators (relevant label ≠ dominant ℓ) of p, q, q′; I, I′ = inconsistency of pq, pq′.

* "If U = V = I = I′ = 0, the two bits are the same function of X": r = 1: X = 0 ⇒ p, q share B1 ⇒ a consistent
  edge cannot be bit 1 (bit 1 needs B1 to differ) ⇒ Y = 0 = majority; X = 1 ⇒ B1 differ ⇒ cannot be bit 0 ⇒ Y = 1 =
  minority. r = 0 symmetric with A. With X = 1 both bits are r and the nonshared coordinate of q, q′ (B1 if both
  bits 1, A if both 0) equals ℓ for both, so N holds and P+ = 2 = 2X. So in that case P+ = 2X and N = 0; in every
  other case 2X − 2(U+V+I+I′) ≤ 0 ≤ P+ and U+V+I+I′ ≥ 1 ≥ N. Hence (7.3). Exhaustively confirmed (script b).
* Integration: ∫_G(P+ − N) ≥ 2H_p* − 3(∫_G U + ∫_G V + ∫_G I + ∫_G I′) ≥ 2H_p* − 3(H_q* + H_q′* + m_pq + m_pq′)
  (∫_G I ≤ m_pq since m_pq integrates over all of L). Off G there are no positive terms and ∫_{C∪B}N ≤ W_c + W_b.
  So the rare-only score Σ := ∫_G P+ − ∫_L N ≥ 2H_p* − 3(…) − W_c − W_b. ✓
* Upper bound. d = z_p − z_q, d′ = z_p − z_q′ (distinct since q ≠ q′ are distinct real points ⇒ distinct z).
  Opposite-endpoint differences: z_q − z_q′ = d′ − d, w_q − w_q′ = 1/d′ − 1/d (both unit equations (4.1)).
  α = u − b = log( max(|d|_v,|d′|_v) / |d − d′|_v ) ≥ −log 2 (archimedean), ≥ 0 (ultrametric): T_v ≥ 0 ✓.
  Bits both 1 ⇔ s < b. B1-match ⇒ |1/d − 1/d′|_v ≤ c_v e^s, and log|1/d−1/d′|_v = −u + b + b′, so
  s ≥ b′ − α − log c_v ≥ b − T_v (c_v = √2 ≤ 2 at infinity, 1 at finite places). Bits both 0 ⇔ s ≥ b′; A-match ⇒
  |d − d′|_v ≤ c_v e^{−s} ⇒ s ≤ u + log c_v = b + α + log c_v ≤ b′ + T_v. ✓ (The paper's T_v with log 2 is
  conservative; log √2 would do — see O1.)
* One-sided argument: π(v,s) = P_E(n_e(v) > s) is nonincreasing in s; minority bit 0 ⇔ π > 1 − ε, minority bit 1 ⇔
  π < ε. If s_0 is a minority-0 level and s_1 a minority-1 level then s_0 < s_1 (else π(s_1) ≥ π(s_0) > 1/2). A
  zero-bit rare positive has s_0 ≥ b′ ≥ b > s_1 for any one-bit rare positive — contradiction. So all rare positives
  at v lie in ONE of the two intervals, each of length T_v, with coefficient 2: total ≤ 2T_v. ✓
* Negative charge on all of I_v: ∫_{I_v}|1{n>s} − 1{n′>s}| ds = b′ − b because I_v ∋ n_pq(v), n_pq′(v) (§4.2). ✓
* (5.14): −log|(d−d′)(1/d−1/d′)|_v = u + (u − b − b′) = 2α − (b′ − b). ✓ So per place
  Σ_v ≤ 2T_v − (b′−b) = −log|x|_v + 2c′_v (c′_v = log 2 at infinity, 0 else), x = (d−d′)(1/d−1/d′) ∈ N^×.
  Summing with weights: product formula kills Σ* log|x|_v; archimedean weights total 1 ⇒ Σ ≤ 2 log 2. Places with
  I_v = [0,0] contribute 0 ≤ 2T_v − 0. ✓
* Combining: 2H_p* ≤ 3(H_q* + H_q′* + m_pq + m_pq′) + W_c + W_b + 2 log 2 — exactly (7.2), constants 3 and 2 log 2 ✓.

### Lemma 7.2 (pp. 37–38)
* R_0 = ε^{−2} = (k^{−1/16})^{−2} = k^{1/8} ✓. C_0 exists and is absolute: (5.5) comes from ∫_G(h_P + h_Q) ≤
  C∫(f + m) with Lemma 2.5's absolute C and (4.18)'s absolute constant.
* Absorption: (W_c + W_b + 2log2)/(R_0S) ≤ (S/ε)/(ε^{−2}S) + (W_b + 2log2)/(R_0S) = ε + o(1), uniformly in p; for
  p ∈ T this is ≤ H_p*·o(1) ≤ H_p* eventually, so (7.2) gives H_p* ≤ 3(H_q* + H_q′* + m_pq + m_pq′). ✓
* Capping (7.5): if H_q* ≥ H_p* the capped RHS is ≥ 3H_p* ≥ H_p*; otherwise unchanged. ✓
* (7.6): p ∼ µ, q, q′ i.i.d. uniform neighbours. P(q ≠ q′ | p) = 1 − 1/d(p) exactly. LHS restricted to {q≠q′}:
  E[H_p*1_T1{q≠q′}] = E_µ[H_p*1_T(1 − 1/d(p))] ≥ (1 − 1/d_{P,min})A_t. RHS (nonnegative) unrestricted:
  each of (p,q), (p,q′) has the uniform edge law, giving 6E_E[min(H_p*,H_q*)1_T] + 6E_E m_pq 1_T ≤ … + C_m. ✓
* Layer cake: min(H_p*,H_q*)1_T > u ⇔ H_p* > max(u, R_0S) and H_q* > u, i.e. (p,q) ∈ F_u × G_u. ✓
  ∫_0^∞ µ(F_u)du = E_µ[H_p*1{H_p*>R_0S}] = A_t, ∫ κ(G_u)du = E_κH_q* ≤ C_0S. ✓ (exact check, script e)
* Marginal expansion bound derived from (2.5) + (2.4): µ(F) ≥ γ|F|/|P| ⇒ u ≤ h/γ, v ≤ k/γ, so
  √(uv)((uv)^η + ξ_t) ≤ (√(hk)/γ)(γ^{−2η}(hk)^η + ξ_t) = √(hk)[γ^{−(1+2η)}(hk)^η + γ^{−1}ξ_t] — exactly the
  displayed bound (it is (2.9) with C = γ^{−1−2η} and the ξ-coefficient γ^{−1}). ✓
* ϑ_t at thresholds with κ(G_u) = 1: the η-power is of the PRODUCT h_P(u)h_Q(u) ≤ µ(T)·1 ≤ (C_0S)/(R_0S) = C_0/R_0
  (Markov), so ϑ_t = γ^{−(1+2η)}(C_0/R_0)^η + γ^{−1}ξ_t → 0 at every u. (2.5) is stated for every F ⊆ P, G ⊆ Q
  including G = Q, and is consistent there: with G = Q it reads µ(F) ≤ √µ(F)[…], true since √x ≤ x^η on [0,1]
  and γ^{−1−2η} ≥ 1.) ✓
* Cauchy–Schwarz ✓. With 1 − 1/d_{P,min} ≥ 1/2: ½A_t ≤ 6ϑ_t√(C_0A_tS) + C_m; Young xy ≤ x²/4 + y² with
  x = √A_t, y = 6ϑ_t√(C_0S) gives ≤ ¼A_t + 36C_0ϑ_t²S + C_m; hence A_t ≤ 144C_0ϑ_t²S + 4C_m, A_t/S → 0 (S → ∞). ✓

### §7.2, (7.7), Lemma 7.3 (pp. 38–39)
* σ = +1 iff minority bit is 1 ⇔ majority b = 0. Four cases (consistent edge): (X_p,X_q) = (0,0): Y = b;
  (1,0),(0,1): Y = r = b + σ; (1,1): Y ∈ {0,1} vs b + 2σ ∈ {2, −1}: residual ≤ 2 = 2X_pX_q. Inconsistent edge with
  ≤ 1 exception: residual ≤ 1 ≤ 2I_pq. So |Y_pq − (b + σ(X_p + X_q))| ≤ 2(X_pX_q + I_pq) ✓ (brute force, script b;
  the true residual is ≤ 2X_pX_q + I_pq).
* n_pq(v) − n_rq(v) = ∫_{I_v}(1{n_pq>s} − 1{n_rq>s})ds because ∫_{ℓ_v}^{u_v}1{n>s}ds = n − ℓ_v for n ∈ I_v and I_v
  contains every n_e(v) by its choice (§4.2). ✓
* (7.8): split I_v = C_v ∪ B_v ∪ G_v; on G the center term b + σX_q cancels; |∫_B| ≤ |B_v|. So
  ‖(n_pq−n_rq) − (a_p−a_r)‖_1 ≤ ∫_C|Y_pq−Y_rq| + W_b + 2∫_G(X_pX_q + X_rX_q + I_pq + I_rq) = E_1. ✓
  E∫_C|Y_pq − Y_rq| = ∫_C E_q P(Y_pq≠Y_rq | q) = ∫_C E_q[2ρ(1−ρ)] = C_Q EXACTLY (p, r i.i.d. given q in the wedge
  law = experiment Q of §5.2); C_Q = o(S) by (6.8). E∫_G X_pX_q = ∫_G P_E(I_p=I_q=1) = o(S) by (5.6) since (p,q)
  has the edge law; E∫_G I ≤ E_E m = O(1); W_b = o(S). ✓
* Exact identity: on I_v, 1{n_pq>s} − 1{n_rq>s} has constant sign, so |∫| = ∫|·|. ✓ (numerically: ‖n_pq−n_rq‖_1 =
  Σ*|log|λ|_v| = 6.2005 in script a.)
* (7.9) pointwise inequality: if none of X_pX_r, X_pX_q, X_rX_q, I_pq, I_rq is present and exactly one of X_p,X_r is 1,
  then X_q = 0, the exceptional endpoint's edge has bit r and the other has bit b: |ΔY| = 1 = RHS; if X_p = X_r = 0
  RHS = 0; if any subtracted term is present RHS ≤ 2 − 2 = 0. ✓ (brute force). E E_2: wedge joint term
  ∫_G P(I_p=I_r=1) = o(S) by (5.6), edge joint terms o(S), inconsistency O(1). ✓

### Lemma 7.4 (pp. 39–40)
* EW = 2E_µH_p* ≥ 4c_0S eventually (Prop 6.5) ✓. δ_t := e.g. max(√(EZ/S), 1/S) gives δ_t → 0 and EZ/δ_t = o(S) ✓.
* Losses in W-WEIGHT: E[W1{Z>δ_tW}] ≤ EZ/δ_t = o(S); E[W1{W<c_0S}] ≤ c_0S; W > 2R_0S ⇒ max(H_p*,H_r*) ≥ W/2 > R_0S so
  W1{W>2R_0S} ≤ 2H_p*1{H_p*>R_0S} + 2H_r*1{H_r*>R_0S}, expectation ≤ 4A_t = o(S) (both endpoints have marginal µ). ✓
* Surviving weight ≥ 4c_0S − c_0S − o(S) ≥ 2c_0S; each survivor has W ≤ 2R_0S ⇒ P(survivors) ≥ c_0/R_0 ✓.
* Bands: [c_0S·2^i, c_0S·2^{i+1}), i < 1 + ⌈log_2(2R_0/c_0)⌉ = O(log 2R_0) (R_0 → ∞); pigeonhole ⇒ one band of
  probability ≥ c/(R_0 log 2R_0). J = lower endpoint ⇒ J ≤ W ≤ 2J, J ≥ c_0S → ∞, Z ≤ δ_tW on survivors ⇒ (7.11) ✓.
  R_0 = k^{1/8}, k = t^{o(1)} (in fact k ≤ (log t)^{1/2} from §3.4) ⇒ c/(R_0 log 2R_0) ≥ t^{−o(1)} ✓.
* On the brief's "order of discards": the ORDER AMONG the three discards is immaterial (each is a W-weighted loss and
  they are union-bounded); what is essential — and what the paper does — is that all three are done in W-weighted
  measure BEFORE banding. Discarding {Z > δ_tW} by probability inside a band would be useless because the band
  probability c/(R_0 log 2R_0) → 0 while Markov only gives P(Z>δ_tW) small in absolute terms. Correct as written.
* p ≠ r: p = r ⇒ LHS of (7.9) = 0 while RHS ≥ W − E_2 ≥ (1 − δ_t)W ≥ (1−δ_t)J > 0. ✓

### Lemma 7.5 (pp. 40–41)
* M·C(⌈t^{9/10}⌉,2) ≤ 2C(|P|,2) (a pair of distinct points lies on ≤ 2 unit circles) ⇒ M ≤ (2+o(1))|P|²/t^{9/5}
  = t^{1/5+4a+o(a)} = t^{1/5+o(1)} ✓. |P_mult| ≤ 2C(M,2) ≤ M² = t^{2/5+o(1)} ✓.
* max µ = d(p)/|E| = t^{−1−2a+o(a)}, max κ = t^{−2−a+o(a)} ✓ ⇒ term 1: 2|P_mult|max µ = t^{−3/5+o(1)}; term 2: at most
  M centres have a popular own circle, M·max κ = t^{−9/5+o(1)} ✓.
* Term 3: p ∉ P_mult lies on ≤ 1 popular circle C_p; a shared popular circle must be C_p; r ∈ C_p ∩ Γ_q (Γ_q = unit
  circle about q); Γ_q ≠ C_p since Γ_q is not popular; |C_p ∩ Γ_q| ≤ 2; given (q,p), r is uniform on the d(q)
  neighbours of q (p, r conditionally independent given q) ⇒ ≤ 2/d(q) ✓. Every popular-pair wedge falls in one of
  the three classes ✓.
* R_0 log(2R_0)/min d(q) = [k^{1/8}log(2k^{1/8})/k^{20}]·[k^{20}/d_{Q,min}] → 0 by (5.2); the polynomial terms times
  R_0 log 2R_0 = t^{o(1)} → 0 ✓. Removal costs o(c/(R_0 log 2R_0)) ⇒ (7.10) survives with c/2 ✓.

### Proposition 7.6 (pp. 41–42)
* P(p,r) = Σ_q κ(q)d(q)^{−2} = Σ_{q: pq,rq∈E} 1/(|E|d(q)) ≤ 2/(|E| d_{Q,min}) (≤ 2 centres for p ≠ r) ✓ ⇒ number of
  distinct ordered pairs ≥ [c/(R_0 log 2R_0)]·|E|d_{Q,min}/2 = t^{2+3a+o(a)−o(1)} ≥ t^{2−o(1)} ✓; |P| = t^{1+o(1)} ✓.
  (Edges ≥ |P|^{2−o(1)} since a → 0: the graph is dense in the sense §8 needs.)
* (7.13): d = z_p − z_q, d′ = z_r − z_q, w_p − w_q = 1/d, w_r − w_q = 1/d′ ⇒ (z_p−z_r)(w_p−w_r) = (d−d′)(1/d−1/d′)
  = 2 − d/d′ − d′/d ✓ (exact in Q(i), script a, and on all four edges of a rectangle, script c).
* (7.14): log|λ_pr|_v = n_rq(v) − n_pq(v) (checked at all 12 place entries, script a) ⇒ 2h(λ) = Σ*|log|λ|_v| =
  ‖n_pq − n_rq‖_1 ≥ W − E_2 ≥ (1 − δ_t)J ⇒ h(λ) ≥ (1−δ_t)J/2 ≥ J/3 once δ_t ≤ 1/3 ✓.
* b_pr = log|λ_pr|_v + a_p − a_r = −[(n_pq−n_rq) − (a_p−a_r)] ⇒ ‖b_pr‖_1 ≤ E_1 ≤ δ_tW ≤ 2δ_tJ ✓. Around a complete
  rectangle every unary profile appears once with + and once with − ⇒ log|χ|_v = b_pr + b_p′r′ − b_pr′ − b_p′r ✓
  (script c, max error 1.8e−15; the non-alternating control leaves 16.9). Weighted ℓ¹ ≤ 8δ_tJ.
* Brief's question "is the height of the rectangle product really ≤ half the weighted ℓ¹ norm of its log profile?":
  YES, with EQUALITY: χ ∈ N^× and (4.3) gives 2h(χ) = Σ*|log|χ|_v| (product formula: Σ*log⁺ = Σ*log⁻). Checked:
  h(χ) = 5.633033 = ½Σ*|log|χ|_v| = ½log 78125 (independent Mahler-measure computation). So h(χ) ≤ 4δ_tJ, ω_t = 4δ_t ✓.
* Uniformity: each bound uses only its own retained wedge; the assigned centres of the four rectangle edges may
  differ (the a_p are centre-free) ✓. Popular-circle exclusion inherited ✓. Hypotheses (8.1)–(8.3) of Prop 8.1 are
  delivered with c = 1/3, J_n = J, o(J) = ω_tJ ✓.

## Objections (all COSMETIC; no FATAL, no GAP, no UNCLEAR)

1. **Lemma 7.1, p. 36–37**, "T_v = α + log 2, v archimedean" with "Matching coordinates in a square cell of side
   length r gives distance at most √2 r". The derivation only needs log √2; log 2 is a valid but loose constant
   (it feeds the 2 log 2 in (7.2)). COSMETIC; no fix needed (the simulation, script d, confirms log 2 holds and
   that c_v = 0 fails).
2. **Lemma 7.1, p. 36**, "For completeness, the upper bound for this rare-only score is also pointwise." The
   "rare-only score" (point-star score of §5.2 with the common-level positive term dropped and the bit-difference
   charge kept at EVERY level) is never defined in words; the reader must infer it from "the all-level negative
   charge" a paragraph later. (Related: in the §5.2 display on p. 25 the term "−1{Y_1≠Y_2}" is typeset to the right of
   the case brace, so whether it applies at all levels is visible only from Prop 5.5/5.6.) COSMETIC — Lemma 7.1 is
   self-contained once read as "∫_G P_+ − ∫_L |Y_pq − Y_pq′|". Fix: one defining sentence.
3. **Lemma 7.4, p. 39**, "This order matters because the probability of the eventual band tends to zero." The order
   among the three discards does not matter (each is a weighted loss); what matters is weighted-before-banding.
   COSMETIC wording.
4. **Notation collisions in §7**: N = bit-difference |Y_pq − Y_pq′| (Lemma 7.1) vs the match event N (§5.2) vs the
   number field N; I, I′ (inconsistency) vs I_x (exception); T (tail set, Lemma 7.2) vs tests T (§3) vs T_v;
   M (popular-circle count, Lemma 7.5) vs M (template count, (5.8)); C_0 reused from Lemma 2.2/4.3. COSMETIC.
5. **Cross-references** "Theorems 6.3 and 6.5", "Theorem 7.2", "Theorem 5.2", "Theorem 6.5", "Theorem 7.4",
   "Theorem 7.5", "Theorem 5.1" all label Lemmas/Propositions; each lands on the intended statement (table below).
   COSMETIC.
6. **Lemma 7.3, p. 39**, "In all cases the absolute residual in this identity is at most 2(X_pX_q + I_pq)": true;
   the sharp bound is 2X_pX_q + I_pq. COSMETIC (no effect).

## Brief items touching §7

* (vi) all sub-questions: answered affirmatively above ((7.3) and the one-sided argument; ϑ_t = o(1) at κ(G_u)=1 —
  yes, the η-power is of the product and h_P ≤ C_0/R_0; (7.6) distinctness — exact factor 1−1/d(p), dropped only on
  the nonnegative side; Y_pq = b + σ(X_p+X_q) and residual accounting; (7.9); discard order; band probability
  t^{−o(1)}; Lemma 7.5's counts; ≤ 2 centres ⇒ ≥ t^{2−o(1)} distinct ordered pairs; (7.14)–(7.15)).
* (i) Euclidean input inside §7: (a) Lemma 7.1's place identity −log|(d−d′)(1/d−1/d′)|_v = 2α − (b′−b) and the two
  windows [b−T_v,b], [b′,b′+T_v] need the opposite-endpoint w-difference to be 1/d − 1/d′, i.e. the reciprocal jump
  (4.1); (b) Lemma 7.3's identity Y_pq = b + σ(X_p+X_q) rests on §4.4 consistency, which needs "z-jump small ⇔
  w-jump large" (reciprocity); (c) (7.13) is the reciprocal relation verbatim. Everything else in §7 (Lemma 7.2,
  7.4, 7.5 counts, the rectangle cancellation, (7.14)) is metric-free. For a "parabola" unit curve the w-analogue
  of the jump would be ~d² (both coordinates small together), so consistency "exactly one label agrees" fails at
  every level and (a)–(c) have no analogue — §7 cannot be run for Valtr-type metrics as written.
* (viii)(b) near-4/3 density enters §7 only through |E|·d_{Q,min} = t^{2+3a+o(a)} = |P|^2·t^{−a+o(a)} = |P|^{2−o(1)} in Prop 7.6's
  count (giving a pair graph with |P|^{2−o(1)} edges), |P| = t^{1+o(1)} vs the t^{9/10} popular threshold in
  Lemma 7.5, and R_0 log 2R_0 = t^{o(1)} (band probability t^{−o(1)}).
* (viii)(c) d_N: irrelevant in §7 — every bound is a weighted sum with total archimedean weight 1; no constant
  depends on d_N.
* (viii)(d) reality used in §7: distinct real points have distinct z (d ≠ d′ in Lemma 7.1, needed for
  (d−d′)(1/d−1/d′) ≠ 0); ≤ 2 unit circles through two distinct points / ≤ 2 centres (Lemma 7.5, Prop 7.6; also
  true for complex points on the hyperbola model, since the two circle equations differ by a linear equation);
  popular REAL circles (Lemma 7.5). For complex points sharing a z-coordinate, Lemma 7.1's product-formula element
  can vanish.

## Internal cross-reference / citation table (§7 has NO external citations)

| Cited as | Intended | Says what §7 needs? |
|---|---|---|
| "Theorems 6.3 and 6.5" (p.36) | Prop 6.3 (6.8) C_Q + C_Pθ = o(S); Prop 6.5 (6.12) | MATCH |
| (7.1) items | (5.5); (4.18); (5.3) | MATCH |
| "Section 2" marginal expansion (p.38) | (2.5)+(2.4) ⇒ displayed bound (= (2.9) with explicit C) | MATCH (derived above) |
| "Theorem 5.2" (p.39) | Lemma 5.2 (5.6) joint edge/wedge exceptions | MATCH |
| "Theorem 6.5" (p.40) | Prop 6.5 | MATCH |
| "Theorem 7.2" (p.40) | Lemma 7.2 (7.4) | MATCH |
| "Theorem 5.1" (p.41) | Lemma 5.1 (5.2): k^20 d_{Q,min}^{−1} → 0 | MATCH |
| "Theorem 7.4", "Theorem 7.5" (p.41) | Lemmas 7.4, 7.5 | MATCH |
| product formula / (4.3) (p.42) | Lemma 4.1 (4.2), Lemma 4.2 (4.3) | MATCH |

## Finite checks

All scripts in /tmp/oaimath/167/checks/extraction/, run with `nice -n 19` (python3 -I; script d needs numpy, run
with ~/.venv/bin/python -I). Two instrument errors were caught during the run and are recorded honestly:
(1) script a's first prime-finder took primes of the NORM only; it silently dropped the places above 17 and 29
(norm-one elements), STILL passed the product-formula and 2h = Σ|log| checks, and reported h(λ) = 1.4166 instead of
3.1003 — fixed, and an independent Mahler-measure cross-check added (it would have caught it). (2) script c's first
control (flipping the sign convention of a_p) could not fail — unary profiles cancel around an alternating rectangle
with either sign — replaced by a non-alternating product, which fails as it must.


### (b) Brute force of the level-wise combinatorics: Lemma 7.1's (7.3), Lemma 7.3's identity/residual, (7.8) integrand, (7.9) integrand. CONTROLS: σ sign flipped; residual without X_pX_q.

Script `/tmp/oaimath/167/checks/extraction/b_cases.py` (verbatim):

```python
# Brute-force check of the pointwise combinatorics in Lemma 7.1 (7.3) and Lemma 7.3.
# Model of one good rare level: states (A,B1) with labels in {0,1,2}; dominant label ell=0 in the
# "relevant" coordinate (B1 if minority bit r=1, A if r=0).  Bits Y in {0,1} free; an edge is
# CONSISTENT iff (Y=1 and A agree and B1 differ) or (Y=0 and B1 agree and A differ)  [§4.4].
import itertools, sys
LAB = [0,1,2]
STATES = list(itertools.product(LAB, LAB))
def consistent(x, y, Y):
    Aeq, Beq = x[0]==y[0], x[1]==y[1]
    return (Y==1 and Aeq and not Beq) or (Y==0 and Beq and not Aeq)
def exc(x, r):           # exception indicator: relevant coordinate label != 0
    return int((x[1] if r==1 else x[0]) != 0)
def N_event(q, qq, Y1, Y2):   # nonshared-coordinate match of the two opposite endpoints
    if Y1==1 and Y2==1: return q[1]==qq[1]      # B1 match
    if Y1==0 and Y2==0: return q[0]==qq[0]      # A match
    return False

def check(sigma_sign=+1, residual_has_XX=True, verbose=False):
    bad = 0
    for r in (0,1):
        b = 1-r; sigma = (1 if r==1 else -1)*sigma_sign
        # --- Lemma 7.3 identity: |Y_pq - (b+sigma(Xp+Xq))| <= 2(XpXq + Ipq)
        for p, q in itertools.product(STATES, STATES):
            for Y in (0,1):
                Xp, Xq, I = exc(p,r), exc(q,r), int(not consistent(p,q,Y))
                res = abs(Y - (b + sigma*(Xp+Xq)))
                bound = 2*((Xp*Xq if residual_has_XX else 0) + I)
                if res > bound:
                    bad += 1
                    if verbose and bad<=3: print("  7.3-identity FAIL r=%d p=%s q=%s Y=%d res=%d bound=%d"%(r,p,q,Y,res,bound))
                if Xp*Xq==0 and I==0 and res!=0:
                    bad += 1
        # --- Lemma 7.1 (7.3): P+ >= 2X - 2(U+V+I+I'), N <= U+V+I+I'
        for p, q, qq in itertools.product(STATES, STATES, STATES):
            for Y1, Y2 in itertools.product((0,1),(0,1)):
                X, U, V = exc(p,r), exc(q,r), exc(qq,r)
                I, I2 = int(not consistent(p,q,Y1)), int(not consistent(p,qq,Y2))
                Pplus = 2*X*int(Y1==r and Y2==r and N_event(q,qq,Y1,Y2))
                Nn = abs(Y1-Y2)
                s = U+V+I+I2
                if not (Pplus >= 2*X - 2*s and Nn <= s): bad += 1
                if not (Pplus - Nn >= 2*X - 3*s): bad += 1
        # --- Lemma 7.3 (7.9) pointwise: |Ypq-Yrq| >= Xp+Xr-2(XpXr+XpXq+XrXq+Ipq+Irq)
        for p, q, rr in itertools.product(STATES, STATES, STATES):
            for Y1, Y2 in itertools.product((0,1),(0,1)):
                Xp, Xq, Xr = exc(p,r), exc(q,r), exc(rr,r)
                I1, I2 = int(not consistent(p,q,Y1)), int(not consistent(rr,q,Y2))
                lhs = abs(Y1-Y2)
                rhs = Xp+Xr-2*(Xp*Xr+Xp*Xq+Xr*Xq+I1+I2)
                if lhs < rhs: bad += 1
                # (7.8) integrand: |(Ypq-Yrq) - sigma(Xp-Xr)| <= 2(XpXq+XrXq+Ipq+Irq)
                lhs8 = abs((Y1-Y2) - sigma*(Xp-Xr))
                rhs8 = 2*((Xp*Xq + Xr*Xq) if residual_has_XX else 0) + 2*(I1+I2)
                if lhs8 > rhs8:
                    bad += 1
    return bad

print("paper's table (sigma=+1 iff minority bit 1, residual 2(XpXq+I)):  violations =", check())
print("CONTROL sigma sign flipped:                                       violations =", check(sigma_sign=-1))
print("CONTROL residual without the XpXq term:                           violations =", check(residual_has_XX=False, verbose=True))
```

Output (verbatim):

```
paper's table (sigma=+1 iff minority bit 1, residual 2(XpXq+I)):  violations = 0
CONTROL sigma sign flipped:                                       violations = 108
  7.3-identity FAIL r=0 p=(1, 0) q=(1, 1) Y=1 res=2 bound=0
  7.3-identity FAIL r=0 p=(1, 0) q=(1, 2) Y=1 res=2 bound=0
  7.3-identity FAIL r=0 p=(1, 0) q=(2, 0) Y=0 res=1 bound=0
CONTROL residual without the XpXq term:                           violations = 156
```

### (a) Exact toy in Q(i) with the full weighted place list of Lemma 4.1: unit equations, (7.13), log|λ|_v = n_rq − n_pq at every place, product formula, 2h = Σ*|log|, Lemma 7.1's (5.14)-identity and T_v ≥ 0, Mahler cross-check. CONTROLS: sign-flipped identity; archimedean weight 1 each; h = ¼Σ|log|.

Script `/tmp/oaimath/167/checks/extraction/a_qi_places.py` (verbatim):

```python
# Exact toy in N = Q(i) (normal, d_N = 2): all places with the weights of Lemma 4.1.
#  archimedean entries: identity and complex conjugation, weight 1/2 each (total 1)
#  finite place P above l: n_P = [N_P:Q_l] copies of weight 1/2, |l|_P = 1/l  =>  |u|_P = l^(-v_P(u)/e_P)
# Checks: unit equations; (7.13) exactly; log|lambda|_v = n_rq(v) - n_pq(v) at every place;
# product formula; 2h(lambda) = sum*|log|lambda|_v|; the (5.14)/(7.1) place identity
#   -log|(d-d')(1/d-1/d')|_v = 2alpha - (b'-b)  and  T_v >= 0  at every place.
from fractions import Fraction as F
import math, itertools

class G:  # Gaussian rational a + b i
    __slots__=("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __sub__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return G(o)-s
    def __neg__(s): return G(-s.a,-s.b)
    def __mul__(s,o): o=o if isinstance(o,G) else G(o); return G(s.a*o.a-s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def conj(s): return G(s.a,-s.b)
    def norm(s): return s.a*s.a+s.b*s.b
    def inv(s): n=s.norm(); assert n!=0; return G(s.a/n,-s.b/n)
    def __truediv__(s,o): o=o if isinstance(o,G) else G(o); return s*o.inv()
    def __rtruediv__(s,o): return G(o)*s.inv()
    def __eq__(s,o): o=o if isinstance(o,G) else G(o); return s.a==o.a and s.b==o.b
    def iszero(s): return s.a==0 and s.b==0
    def __repr__(s): return "(%s + %s*i)"%(s.a,s.b)

def gauss_divides(pi, u):   # u, pi Gaussian INTEGERS: does pi | u in Z[i]?
    q = u / pi
    return q.a.denominator==1 and q.b.denominator==1

def primes_above(l):
    """list of (pi, e, n_copies) for the Gaussian primes above rational prime l."""
    if l==2: return [(G(1,1), 2, 2)]
    if l%4==3: return [(G(l,0), 1, 2)]
    for a in range(1,int(math.isqrt(l))+1):
        b2=l-a*a; b=math.isqrt(b2)
        if b*b==b2: return [(G(a,b),1,1),(G(a,-b),1,1)]
    raise ValueError

def vpi(u, pi):
    """pi-adic valuation of a nonzero Gaussian rational u."""
    assert not u.iszero()
    den = math.lcm(u.a.denominator, u.b.denominator)
    num = u*den                       # Gaussian integer
    def vint(x):
        v=0
        while gauss_divides(pi, x): x = x/pi; v+=1
        return v
    return vint(num) - vint(G(den))

def relevant_primes(*els):
    ps=set()
    for u in els:
        den = math.lcm(u.a.denominator, u.b.denominator)
        num = u*den                     # Gaussian integer
        for x in (int(num.norm()), den):
            m=x; p=2
            while p*p<=m:
                while m%p==0: ps.add(p); m//=p
                p+=1
            if m>1: ps.add(m)
    ps.add(2)
    return sorted(ps)

def places(primes):
    """list of (name, weight, logabs function)"""
    pl=[("inf_id", F(1,2), lambda u: 0.5*math.log(float(u.norm()))),
        ("inf_conj", F(1,2), lambda u: 0.5*math.log(float(u.conj().norm())))]
    for l in primes:
        for (pi,e,ncop) in primes_above(l):
            for c in range(ncop):
                pl.append(("P%d[%s]#%d"%(l,pi,c), F(1,2),
                           (lambda pi,e,l: (lambda u: -(vpi(u,pi)/e)*math.log(l)))(pi,e,l)))
    return pl

def wsum(pl, f):  # weighted sum over places
    return sum(float(w)*f(name,lg) for (name,w,lg) in pl)

def height(pl,u): return wsum(pl, lambda n,lg: max(0.0, lg(u)))

def unit(m,n): # (m+ni)^2/(m^2+n^2): Gaussian rational of norm 1
    z=G(m,n); return (z*z)/(m*m+n*n)

def pt(x): # point -> (z,w) = (x1+i x2, x1-i x2)
    return (G(x[0],x[1]), G(x[0],-x[1]))

TOL=1e-12
fails=0
# configuration: centre q, neighbours p, r, and a second neighbour q' of p
q = (F(2,7), F(-1,3))
u1, u2, u3 = unit(4,1), unit(5,2), unit(3,2)          # norms 17, 29, 13
p = (q[0]+u1.a, q[1]+u1.b); r = (q[0]+u2.a, q[1]+u2.b)
qq = (p[0]-u3.a, p[1]-u3.b)                             # q' with p - q' = u3
zq,wq = pt(q); zp,wp = pt(p); zr,wr = pt(r); zqq,wqq = pt(qq)
d, dd = zp-zq, zr-zq
assert d*(wp-wq)==1 and dd*(wr-wq)==1 and (zp-zqq)*(wp-wqq)==1, "unit equations"
lam = d/dd
lhs = (zp-zr)*(wp-wr); rhs = 2 - lam - lam.inv()
print("(7.13) exact:", lhs==rhs, " |p-r|^2 =", lhs)
if not lhs==rhs: fails+=1
pl = places(relevant_primes(d,dd,lam, zp-zqq, d-(zp-zqq)))
print("number of place entries:", len(pl), " total weight", sum(w for _,w,_ in pl))
npq = lambda lg: -lg(d); nrq = lambda lg: -lg(dd)
for (name,w,lg) in pl:
    if abs(lg(lam) - (nrq(lg)-npq(lg)))>TOL: fails+=1; print("  FAIL log|lam| at",name)
pf = wsum(pl, lambda n,lg: lg(lam))
h = height(pl, lam); s_abs = wsum(pl, lambda n,lg: abs(lg(lam)))
print("product formula sum* log|lam|_v = %.3e ; 2h(lam) = %.12f ; sum*|log|lam|_v| = %.12f"%(pf, 2*h, s_abs))
if abs(pf)>TOL or abs(2*h-s_abs)>TOL: fails+=1
print("h(lam) = %.6f ;  ||n_pq - n_rq||_1 = %.6f"%(h, wsum(pl, lambda n,lg: abs(npq(lg)-nrq(lg)))))
# (5.14)-type identity of Lemma 7.1 for the point star p with neighbours q, q'
D, DD = zp-zq, zp-zqq
x = (D-DD)*(D.inv()-DD.inv())
for (name,w,lg) in pl:
    nb, nbb = -lg(D), -lg(DD); b, bp = min(nb,nbb), max(nb,nbb)
    u = -lg(D-DD); alpha = u-b
    cv = math.log(2) if name.startswith("inf") else 0.0
    if abs(-lg(x) - (2*alpha-(bp-b)))>TOL: fails+=1; print("  FAIL (5.14) at",name)
    if alpha+cv < -TOL: fails+=1; print("  FAIL T_v>=0 at",name)
print("sum* -log|(d-d')(1/d-1/d')|_v = %.3e (product formula)"%wsum(pl, lambda n,lg: -lg(x)))
# other elements: 2h(u) = sum*|log|u|_v|, h(1/u)=h(u)
for u in [G(3,4)/G(7,0), G(1,1), G(5,12)/G(2,3), lam*lam*G(1,2), x]:
    pl2 = places(relevant_primes(u))
    a, c = 2*height(pl2,u), wsum(pl2, lambda n,lg: abs(lg(u)))
    if abs(a-c)>TOL or abs(height(pl2,u)-height(pl2,u.inv()))>TOL: fails+=1
    print("  u=%-28s 2h=%.10f  sum*|log|=%.10f  h(1/u)=%.10f"%(u, a, c, height(pl2,u.inv())))
print("TOTAL FAILURES:", fails)

# ---------- CONTROLS (must FAIL) ----------
print("\nCONTROL 1: sign-flipped identity log|lam|_v = n_pq - n_rq :",
      sum(1 for (nm,w,lg) in pl if abs(lg(lam)-(npq(lg)-nrq(lg)))>TOL), "places disagree (expect >0)")
plbad = [(n, (F(1) if n.startswith("inf") else w), lg) for (n,w,lg) in pl]  # archimedean weight 1 each
print("CONTROL 2: archimedean weights 1 each -> product formula sum = %.4f (expect !=0)"%wsum(plbad, lambda n,lg: lg(G(3,0))))
print("CONTROL 3: 'h = (1/4) sum*|log|' -> %.6f vs h = %.6f (expect unequal)"%(s_abs/4, h))

# ---------- INDEPENDENT cross-check of h(lam) via the Mahler measure (no place list used) ----------
# lam has |lam|=1 at both archimedean embeddings and lam + 1/lam = 2 - |p-r|^2 (from (7.13)),
# so its minimal polynomial is a x^2 - b x + a with a = denominator; h = (1/2) log M = (1/2) log a.
tr = 2 - lhs.a            # lam + 1/lam, rational
a_lead = tr.denominator; b_mid = tr.numerator
g = math.gcd(a_lead, b_mid)
print("\nMahler cross-check: min poly %d x^2 - %d x + %d ; (1/2)log M = %.12f vs place-sum h = %.12f"
      %(a_lead, b_mid, a_lead, 0.5*math.log(a_lead), h))
assert g==1 and abs(0.5*math.log(a_lead)-h)<1e-12
print("NOTE: a first version of relevant_primes() took primes of the NORM only; it silently dropped the")
print("places above 17 and 29 (norm-1 elements), still passed the product formula and 2h=sum|log| checks,")
print("and reported h(lam)=1.4166 instead of 3.1003. The Mahler cross-check above is what catches that class.")
```

Output (verbatim):

```
(7.13) exact: True  |p-r|^2 = (36/493 + 0*i)
number of place entries: 12  total weight 6
product formula sum* log|lam|_v = 0.000e+00 ; 2h(lam) = 6.200509174043 ; sum*|log|lam|_v| = 6.200509174043
h(lam) = 3.100255 ;  ||n_pq - n_rq||_1 = 6.200509
sum* -log|(d-d')(1/d-1/d')|_v = -3.331e-16 (product formula)
  u=(3/7 + 4/7*i)                2h=3.8918202981  sum*|log|=3.8918202981  h(1/u)=1.9459101491
  u=(1 + 1*i)                    2h=0.6931471806  sum*|log|=0.6931471806  h(1/u)=0.3465735903
  u=(46/13 + 9/13*i)             2h=5.1298987149  sum*|log|=5.1298987149  h(1/u)=2.5649493575
  u=(459001/243049 + 291002/243049*i) 2h=14.0104562605  sum*|log|=14.0104562605  h(1/u)=7.0052281303
  u=(100/221 + 0*i)              2h=10.7963254030  sum*|log|=10.7963254030  h(1/u)=5.3981627015
TOTAL FAILURES: 0

CONTROL 1: sign-flipped identity log|lam|_v = n_pq - n_rq : 4 places disagree (expect >0)
CONTROL 2: archimedean weights 1 each -> product formula sum = 2.1972 (expect !=0)
CONTROL 3: 'h = (1/4) sum*|log|' -> 1.550127 vs h = 3.100255 (expect unequal)

Mahler cross-check: min poly 493 x^2 - 950 x + 493 ; (1/2)log M = 3.100254587021 vs place-sum h = 3.100254587021
NOTE: a first version of relevant_primes() took primes of the NORM only; it silently dropped the
places above 17 and 29 (norm-1 elements), still passed the product formula and 2h=sum|log| checks,
and reported h(lam)=1.4166 instead of 3.1003. The Mahler cross-check above is what catches that class.
```

### (c) Exact rectangle in Q(i) (an 8-cycle of unit edges from u1+u3+u5+u7 = u2+u4+u6+u8), (7.13) on all four edges, rectangle cancellation with random unary profiles, h(χ) = ½Σ*|log|χ|_v| with Mahler cross-check. CONTROLS: non-alternating product; h ≤ ¼Σ|log|. (Importing script a re-prints its output first.)

Script `/tmp/oaimath/167/checks/extraction/c_rectangle.py` (verbatim):

```python
# Rectangle cancellation behind (7.15), exact in Q(i).
# An 8-cycle of unit edges p-q1-r-q4-p'-q2-r'-q3-p exists iff u1+u3+u5+u7 = u2+u4+u6+u8 for unit
# Gaussian rationals (p=q1+u1, r=q1+u2, r=q4+u3, p'=q4+u4, p'=q2+u5, r'=q2+u6, r'=q3+u7, p=q3+u8).
# Then lam_pr=u1/u2, lam_p'r=u4/u3, lam_p'r'=u5/u6, lam_pr'=u8/u7 and chi = u1u3u5u7/(u2u4u6u8).
import sys, itertools, random, math
sys.path.insert(0, "/tmp/oaimath/167/checks/extraction")
from a_qi_places import G, F, places, relevant_primes, wsum, height, unit, pt   # (re-runs the toy; harmless)
random.seed(1)
units = set()
for (m,n) in [(2,1),(3,2),(4,1),(4,3),(5,2),(1,2),(2,3),(1,4),(3,4),(2,5)]:
    for sm in (1,-1):
        for sn in (1,-1):
            for sw in (False, True):
                u = unit(sm*m, sn*n); u = G(u.b,u.a) if sw else u
                units.add((u.a,u.b))
units |= {(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))}
units = sorted(units)
print("unit vectors:", len(units))
L = 1
for (a,b) in units: L = math.lcm(L, a.denominator, b.denominator)
iu = [(int(a*L), int(b*L)) for (a,b) in units]
sums = {}
for comb in itertools.combinations_with_replacement(range(len(units)), 4):
    s = (sum(iu[i][0] for i in comb), sum(iu[i][1] for i in comb))
    sums.setdefault(s, []).append(comb)
found = None
for s, lst in sums.items():
    if len(lst) < 2: continue
    for A, B in itertools.combinations(lst, 2):
        if set(A) & set(B): continue
        for pa in itertools.permutations(A):
            for pb in itertools.permutations(B):
                u = [None]*9
                u[1],u[3],u[5],u[7] = [G(*units[i]) for i in pa]
                u[2],u[4],u[6],u[8] = [G(*units[i]) for i in pb]
                q1 = G(0); p = q1+u[1]; r = q1+u[2]; q4 = r-u[3]; pp = q4+u[4]
                q2 = pp-u[5]; rr = q2+u[6]; q3 = rr-u[7]
                assert p == q3+u[8]
                P_ = [p,r,pp,rr]; Q_ = [q1,q2,q3,q4]
                if any(P_[i]==P_[j] for i in range(4) for j in range(i+1,4)): continue
                if any(Q_[i]==Q_[j] for i in range(4) for j in range(i+1,4)): continue
                chi = (u[1]*u[3]*u[5]*u[7])/(u[2]*u[4]*u[6]*u[8])
                if chi == G(1): continue
                found = (u, p, r, pp, rr, q1, q2, q3, q4, chi); break
            if found: break
        if found: break
    if found: break
u, p, r, pp, rr, q1, q2, q3, q4, chi = found
print("p=%s r=%s p'=%s r'=%s\nq1=%s q2=%s q3=%s q4=%s"%(p,r,pp,rr,q1,q2,q3,q4))
def W(zv): return zv.conj()        # real point: w = conj(z)
fails = 0
edges = {("p","r"):(p,r,q1), ("p'","r'"):(pp,rr,q2), ("p","r'"):(p,rr,q3), ("p'","r"):(pp,r,q4)}
lam = {}
for k,(a,b,q) in edges.items():
    for x in (a,b): assert (x-q)*(W(x)-W(q)) == 1      # unit incidences
    lam[k] = (a-q)/(b-q)
    ok = (a-b)*(W(a)-W(b)) == 2 - lam[k] - lam[k].inv()   # (7.13)
    fails += (not ok)
chi2 = lam[("p","r")]*lam[("p'","r'")]/(lam[("p","r'")]*lam[("p'","r")])
assert chi2 == chi
print("(7.13) on all four rectangle edges:", "OK" if fails==0 else "FAIL", "; chi =", chi)
pl = places(relevant_primes(*(list(lam.values())+[chi])))
names = [n for n,_,_ in pl]
# arbitrary unary profiles a_x(v) and the binary defects b_pr(v) = log|lam_pr|_v + a_p(v) - a_r(v)
a = {x:{n:random.uniform(-5,5) for n in names} for x in ["p","r","p'","r'"]}
lg = {n:f for n,_,f in pl}
def b(k,n): return lg[n](lam[k]) + a[k[0]][n] - a[k[1]][n]
# CONTROL: a NON-alternating product lam_pr*lam_pr'/(lam_p'r*lam_p'r') -- unary profiles must NOT cancel.
# (Note: flipping the sign convention of a in b_pr is NOT a valid control: any unary profile cancels
#  around an alternating rectangle whatever its sign; a first version of this script used it and it "passed".)
chi_bad = lam[("p","r")]*lam[("p","r'")]/(lam[("p'","r")]*lam[("p'","r'")])
mx = 0; mxw = 0
for n in names:
    lhs = lg[n](chi)
    rhs = b(("p","r"),n)+b(("p'","r'"),n)-b(("p","r'"),n)-b(("p'","r"),n)
    rhw = b(("p","r"),n)+b(("p","r'"),n)-b(("p'","r"),n)-b(("p'","r'"),n)
    mx = max(mx, abs(lhs-rhs)); mxw = max(mxw, abs(lg[n](chi_bad)-rhw))
print("max_v |log|chi|_v - (b_pr+b_p'r'-b_pr'-b_p'r)(v)| = %.2e   (CONTROL non-alternating product: %.2e, expect >> 0)"%(mx,mxw))
fails += mx > 1e-9
hchi = height(pl, chi); l1 = wsum(pl, lambda n,f: abs(f(chi)))
bnorm = {k: wsum(pl, lambda n,f,k=k: abs(b(k,n))) for k in edges}
print("h(chi) = %.6f ; (1/2) sum*|log|chi|_v| = %.6f ; (1/2)(sum of the four ||b||_1) = %.6f ; 4*max||b||_1/2 = %.6f"
      %(hchi, l1/2, sum(bnorm.values())/2, 2*max(bnorm.values())))
fails += abs(hchi - l1/2) > 1e-9
fails += hchi > sum(bnorm.values())/2 + 1e-9
# independent cross-check of h(chi): Mahler measure of the min poly of chi (|chi|=1 at both embeddings)
tr = chi + chi.inv(); assert tr.b == 0
print("Mahler: min poly %d x^2 - %d x + %d -> (1/2)log %d = %.6f"%(tr.a.denominator, tr.a.numerator, tr.a.denominator, tr.a.denominator, 0.5*math.log(tr.a.denominator)))
fails += abs(0.5*math.log(tr.a.denominator) - hchi) > 1e-9
print("CONTROL: claim h(chi) <= (1/4) sum*|log|chi|_v| ->", hchi <= l1/4 + 1e-12, "(expect False)")
print("TOTAL FAILURES:", fails)
```

Output (verbatim):

```
(7.13) exact: True  |p-r|^2 = (36/493 + 0*i)
number of place entries: 12  total weight 6
product formula sum* log|lam|_v = 0.000e+00 ; 2h(lam) = 6.200509174043 ; sum*|log|lam|_v| = 6.200509174043
h(lam) = 3.100255 ;  ||n_pq - n_rq||_1 = 6.200509
sum* -log|(d-d')(1/d-1/d')|_v = -3.331e-16 (product formula)
  u=(3/7 + 4/7*i)                2h=3.8918202981  sum*|log|=3.8918202981  h(1/u)=1.9459101491
  u=(1 + 1*i)                    2h=0.6931471806  sum*|log|=0.6931471806  h(1/u)=0.3465735903
  u=(46/13 + 9/13*i)             2h=5.1298987149  sum*|log|=5.1298987149  h(1/u)=2.5649493575
  u=(459001/243049 + 291002/243049*i) 2h=14.0104562605  sum*|log|=14.0104562605  h(1/u)=7.0052281303
  u=(100/221 + 0*i)              2h=10.7963254030  sum*|log|=10.7963254030  h(1/u)=5.3981627015
TOTAL FAILURES: 0

CONTROL 1: sign-flipped identity log|lam|_v = n_pq - n_rq : 4 places disagree (expect >0)
CONTROL 2: archimedean weights 1 each -> product formula sum = 2.1972 (expect !=0)
CONTROL 3: 'h = (1/4) sum*|log|' -> 1.550127 vs h = 3.100255 (expect unequal)

Mahler cross-check: min poly 493 x^2 - 950 x + 493 ; (1/2)log M = 3.100254587021 vs place-sum h = 3.100254587021
NOTE: a first version of relevant_primes() took primes of the NORM only; it silently dropped the
places above 17 and 29 (norm-1 elements), still passed the product formula and 2h=sum|log| checks,
and reported h(lam)=1.4166 instead of 3.1003. The Mahler cross-check above is what catches that class.
unit vectors: 44
p=(-1 + 0*i) r=(-24/25 + 7/25*i) p'=(-23/25 + 14/25*i) r'=(-18/25 + -1/25*i)
q1=(0 + 0*i) q2=(2/25 + 14/25*i) q3=(-18/25 + 24/25*i) q4=(1/25 + 7/25*i)
(7.13) on all four rectangle edges: OK ; chi = (76443/78125 + 16124/78125*i)
max_v |log|chi|_v - (b_pr+b_p'r'-b_pr'-b_p'r)(v)| = 1.78e-15   (CONTROL non-alternating product: 1.69e+01, expect >> 0)
h(chi) = 5.633033 ; (1/2) sum*|log|chi|_v| = 5.633033 ; (1/2)(sum of the four ||b||_1) = 27.465273 ; 4*max||b||_1/2 = 37.643552
Mahler: min poly 78125 x^2 - 152886 x + 78125 -> (1/2)log 78125 = 5.633033
CONTROL: claim h(chi) <= (1/4) sum*|log|chi|_v| -> False (expect False)
TOTAL FAILURES: 0
```

### (d) Lemma 7.1's per-place bound at an ARCHIMEDEAN entry, simulated with the actual shifted grid labels of §4.4, worst-case monotone minority pattern, 400 random (d, d′, shifts). CONTROL: c_v = 0 at infinity.

Script `/tmp/oaimath/167/checks/extraction/d_place_bound.py` (verbatim):

```python
# Lemma 7.1, per-place upper bound at an ARCHIMEDEAN entry, simulated with the actual grid labels of §4.4.
# Point star p with neighbours q, q' (jumps d, d' arbitrary distinct nonzero complex numbers, as at a
# non-identity embedding where sigma(w) is not conj(sigma(z))):  z_q = z_p - d, w_q = w_p - 1/d.
# A-label at level s: cell of side e^{-s} containing z, fixed fractional shift; B1-label: side e^{s}.
# Worst case: every level is good rare, p exceptional, minority bit 0 below a cut s*, 1 above (any
# monotone pattern).  Score_v = int 2*1{Y1=Y2=minority}*N ds - int |Y1-Y2| ds.
# Claim (Lemma 7.1 proof): Score_v <= 2T_v - (b'-b) with T_v = alpha + log 2, alpha = u - b,
# u = -log|d-d'|; and 2T_v-(b'-b) = -log|(d-d')(1/d-1/d')| + 2log2  [(5.14)].
import numpy as np, math
rng = np.random.default_rng(7)
def cells(x, side, sh):
    return np.floor(x.real/side + sh[0]).astype(np.int64), np.floor(x.imag/side + sh[1]).astype(np.int64)
def trial(cv, nscan=60, ds=2e-4):
    zp = complex(*rng.normal(size=2))*rng.uniform(0.1,10); wp = complex(*rng.normal(size=2))*rng.uniform(0.1,10)
    d  = complex(*rng.normal(size=2))*math.exp(rng.uniform(-3,3))
    dd = d*(1 + complex(*rng.normal(size=2))*math.exp(rng.uniform(-4,1)))   # d' near or far from d
    zq, wq, zqq, wqq = zp-d, wp-1/d, zp-dd, wp-1/dd
    n1, n2 = -math.log(abs(d)), -math.log(abs(dd)); b, bp = min(n1,n2), max(n1,n2)
    u = -math.log(abs(d-dd)); alpha = u-b; T = alpha + cv
    x = (d-dd)*(1/d-1/dd); assert abs(-math.log(abs(x)) - (2*alpha-(bp-b))) < 1e-9     # (5.14)
    lo, hi = b - abs(T) - 3, bp + abs(T) + 3
    s = np.arange(lo, hi, ds)
    shA, shB = rng.uniform(0,1,2), rng.uniform(0,1,2)
    sideA, sideB = np.exp(-s), np.exp(s)
    Aq, Aqq = cells(zq*np.ones_like(s), sideA, shA), cells(zqq*np.ones_like(s), sideA, shA)
    Bq, Bqq = cells(wq*np.ones_like(s), sideB, shB), cells(wqq*np.ones_like(s), sideB, shB)
    Amatch = (Aq[0]==Aqq[0]) & (Aq[1]==Aqq[1]); Bmatch = (Bq[0]==Bqq[0]) & (Bq[1]==Bqq[1])
    Y1, Y2 = (n1 > s), (n2 > s)
    neg = np.sum(Y1 != Y2)*ds
    both1 = Y1 & Y2 & Bmatch           # candidate positives with minority bit 1
    both0 = (~Y1) & (~Y2) & Amatch     # candidate positives with minority bit 0
    worst = -1e9
    for cut in np.linspace(lo, hi, nscan):
        pos = 2*ds*(np.sum(both0 & (s < cut)) + np.sum(both1 & (s >= cut)))
        worst = max(worst, pos - neg)
    bound = 2*T - (bp - b)
    # interval claims: bit-1 positives inside [b-T_v, b], bit-0 positives inside [b', b'+T_v] (T_v with log 2)
    T2 = alpha + math.log(2)
    out1 = np.any(both1 & ((s < b - T2 - 2*ds) | (s >= b)))
    out0 = np.any(both0 & ((s < bp) | (s > bp + T2 + 2*ds)))
    return worst - bound, out1 or out0, T2
viol = 0; maxexc = -1e9; intervals_bad = 0; N = 400
for _ in range(N):
    e, ib, T2 = trial(math.log(2)); maxexc = max(maxexc, e); viol += e > 1e-3; intervals_bad += ib
print("paper's bound (c_v = log 2): trials=%d violations=%d max(score-bound)=%.4f interval-claim failures=%d"
      %(N, viol, maxexc, intervals_bad))
viol0 = 0; maxexc0 = -1e9
for _ in range(N):
    e, _, _ = trial(0.0); maxexc0 = max(maxexc0, e); viol0 += e > 1e-3
print("CONTROL c_v = 0 at the archimedean entry: violations=%d max(score-bound)=%.4f (expect >0)"%(viol0, maxexc0))
```

Output (verbatim):

```
paper's bound (c_v = log 2): trials=400 violations=0 max(score-bound)=-0.1045 interval-claim failures=0
CONTROL c_v = 0 at the archimedean entry: violations=35 max(score-bound)=1.2154 (expect >0)
```

### (e) Lemma 7.2 bookkeeping, exact rationals on a random bipartite graph: layer cake, ∫h_P = A_t, ∫h_Q = E_κH_q, Cauchy–Schwarz, distinctness factor 1 − 1/d(p). CONTROL: F_u without the tail restriction.

Script `/tmp/oaimath/167/checks/extraction/e_layercake.py` (verbatim):

```python
# Lemma 7.2 bookkeeping on a random finite bipartite graph: layer-cake identity
#   E_E[min(H_p,H_q) 1{H_p > R}] = int_0^inf P_E(F_u, G_u) du,  F_u={H_p > max(u,R)}, G_u={H_q > u},
#   int_0^inf mu(F_u) du = E_mu[H_p 1{H_p>R}] = A,   int kappa(G_u) du = E_kappa H_q,
# the Cauchy-Schwarz step, and the distinctness factor (1 - 1/d(p)) for two uniform neighbours.
import random
from fractions import Fraction as Fr
random.seed(3)
P, Q = range(40), range(60)
E = [(p,q) for p in P for q in Q if random.random() < 0.15]
Hp = {p: Fr(random.choice([0,0,0,1,2,5,9,30])) for p in P}
Hq = {q: Fr(random.choice([0,0,1,3,4,7,12])) for q in Q}
R = Fr(4); nE = len(E)
deg = {p: sum(1 for e in E if e[0]==p) for p in P}; degq = {q: sum(1 for e in E if e[1]==q) for q in Q}
lhs = sum(min(Hp[p],Hq[q]) for (p,q) in E if Hp[p] > R) / nE
def PE(u): return Fr(sum(1 for (p,q) in E if Hp[p] > max(u,R) and Hq[q] > u), nE)
def mu(u): return Fr(sum(deg[p] for p in P if Hp[p] > max(u,R)), nE)
def ka(u): return Fr(sum(degq[q] for q in Q if Hq[q] > u), nE)
bps = sorted(set([Fr(0)] + list(Hp.values()) + list(Hq.values()) + [R]))
def integ(f):   # f is a right-continuous step function constant on [bps[i], bps[i+1]); f(u)=0 beyond max
    return sum(f(bps[i]) * (bps[i+1]-bps[i]) for i in range(len(bps)-1))
I_PE, I_mu, I_ka = integ(PE), integ(mu), integ(ka)
A = sum(Fr(deg[p], nE)*Hp[p] for p in P if Hp[p] > R)
Ekq = sum(Fr(degq[q], nE)*Hq[q] for q in Q)
print("layer cake:  E_E[min 1_T] =", lhs, " int P_E(F_u,G_u) du =", I_PE, " equal:", lhs == I_PE)
print("int mu(F_u) =", I_mu, "= A_t =", A, ":", I_mu == A, " ; int kappa(G_u) =", I_ka, "= E_kappa H_q =", Ekq, ":", I_ka == Ekq)
# Cauchy-Schwarz: int sqrt(h_P h_Q) <= sqrt(A * E H_q)
cs = sum(float(mu(bps[i])*ka(bps[i]))**0.5 * float(bps[i+1]-bps[i]) for i in range(len(bps)-1))
print("int sqrt(h_P h_Q) du = %.4f <= sqrt(A E_k H_q) = %.4f : %s" % (cs, float(A*Ekq)**0.5, cs <= float(A*Ekq)**0.5 + 1e-12))
# distinctness: P(q != q' | p) = 1 - 1/d(p) for two independent uniform neighbours
p0 = max(P, key=lambda p: deg[p]); d0 = deg[p0]
nb = [q for (p,q) in E if p == p0]
dist = Fr(sum(1 for a in nb for b in nb if a != b), d0*d0)
print("P(q != q' | p) =", dist, "= 1 - 1/d(p) =", 1 - Fr(1, d0), ":", dist == 1 - Fr(1, d0))
# CONTROL: dropping the max(u,R) (i.e. F_u = {H_p > u} intersect T computed WRONG as {H_p > u}) must disagree
def PEbad(u): return Fr(sum(1 for (p,q) in E if Hp[p] > u and Hq[q] > u), nE)
print("CONTROL F_u={H_p>u} (no tail restriction):", integ(PEbad), "!= lhs:", integ(PEbad) != lhs)
```

Output (verbatim):

```
layer cake:  E_E[min 1_T] = 481/343  int P_E(F_u,G_u) du = 481/343  equal: True
int mu(F_u) = 59/7 = A_t = 59/7 : True  ; int kappa(G_u) = 1342/343 = E_kappa H_q = 1342/343 : True
int sqrt(h_P h_Q) du = 3.9208 <= sqrt(A E_k H_q) = 5.7426 : True
P(q != q' | p) = 16/17 = 1 - 1/d(p) = 16/17 : True
CONTROL F_u={H_p>u} (no tail restriction): 620/343 != lhs: True
```

## Final verdict for scope (§7 + brief item (vi))

**HOLDS AS READ.** Lemma 7.1, Lemma 7.2, Lemma 7.3, Lemma 7.4, Lemma 7.5 and Proposition 7.6 are VERIFIED LINE
BY LINE; the constants (3, 2 log 2, 144C_0ϑ_t², c_0/R_0, t^{−3/5}, t^{−9/5}, 2/d(q), 2δ_tJ, 8δ_tJ, ω_t = 4δ_t,
J/3) are all correct, and the height of the rectangle product is exactly half the weighted ℓ¹ norm of its log
profile. §7 is correct conditional on its imported inputs — chiefly Prop 6.3's C_Q = o(S) and Prop 6.5's
liminf E_µH_p*/S > 0 (§6), Lemma 5.2's (5.5)–(5.6), and Lemma 4.5's O(1) inconsistency — which are other seats'
scope. If the paper fails, it does not fail in §7.
