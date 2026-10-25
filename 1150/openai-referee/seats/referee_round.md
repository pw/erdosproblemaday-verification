# Referee report — seat `round` (family 076, sib1 "Asymptotically minimal maxima of real Littlewood polynomials")

Scope (verbatim): sib1 §6 (pp. 18–21) + §8 (pp. 21–23). Lemma 6.1 vs Lovett–Meka refs/1203.5747 (Theorem 4, v2);
§6.2 dyadic rounding; Lemma 2.2 as stated vs what §6 proves; §8 merit factor normalization vs Downarowicz–Lacroix
(Definition 2, Lemma 0, Theorem 2); Corollary 8.2 spectral statement.

Status: COMPLETE (running notes kept below the final sections).

## Scope read (pages)
- sib1 p.18 (from "6 Rounding with a small defect mass") through p.23 top (end of §8, before Appendix A) — every line, in the
  rendered PDF (pp.18–23) and in the layout text. Also p.4 (statement of Lemma 2.2; the §1 sentence describing §6) and the proof
  of Theorem 1.1 (p.4–5) at the point where Lemma 2.2 is applied; §1 p.~3 paragraph on Downarowicz–Lacroix; bib entries [7], [19], [20].
- Lovett–Meka arXiv:1203.5747v2 (local refs/1203.5747, header "arXiv:1203.5747v2 [cs.DS] 11 Oct 2012"): Theorem 4, §2.1, §4.1–4.2,
  §5 (Edge-Walk, Lemma 11, Claims 12–16) — read; Section 6 skimmed.
- Downarowicz–Lacroix author manuscript (refs/downarowicz_lacroix): whole paper (Definitions 1–3, Lemma 0, Lemma 1, Theorem 1,
  Corollaries 1–3, Lemma 2, Theorem 2, Facts 1–2, spectral preliminaries).
- BBMST arXiv:1907.09464v1 §4 (Theorem 4.1 / footnote 5) — for the attribution sentence on p.18.
- OpenAI companion [20] (on-disk copy, /tmp/oaimath/166/.../preprints/A-smooth-three-torus-diffeomorphism-with-simple-Lebesgue-
  spectrum-September-23-2026/paper.pdf, sha256 0a6684b3…): abstract + §1 Theorem 1.1 only.

## Running notes
### 09:3x — first pass notes (Lemma 6.1, §6.2)
- Read sib1 pp.18–21 in the rendered PDF (Read tool, pages 18–21) and text pp.18–23; Lemma 2.2 statement p.4 and its use in
  the proof of Theorem 1.1 (p.4–5).
- Lovett–Meka refs/1203.5747 = **v2** (header "arXiv:1203.5747v2 [cs.DS] 11 Oct 2012"). Theorem 4 verbatim: "Let v1,...,vm ∈ R^n
  be vectors, and x0 ∈ [−1,1]^n be a 'starting' point. Let c1,...,cm ≥ 0 be thresholds such that Σ_{j=1}^m exp(−c_j²/16) ≤ n/16.
  Let δ > 0 be a small approximation parameter. Then there exists an efficient randomized algorithm which with probability at
  least 0.1 finds a point x ∈ [−1,1]^n such that (i) |⟨x − x0, vj⟩| ≤ cj‖vj‖2. (ii) |xi| ≥ 1 − δ for at least n/2 indices i ∈ [n]."
  (Proof assumes δ < 0.1; vectors normalized WLOG — "this normalization does not change the problem".)
  sib1's paraphrase (p.18: "the theorem of Lovett and Meka gives, for every sufficiently small η > 0, a point x ∈ [−1,1]^u with
  |⟨vi, x − x0⟩| ≤ ci‖vi‖2 (1 ≤ i ≤ R), |xk| ≥ 1 − η for at least u/2 coordinates k") matches: same threshold sum, same row-norm
  scaling, same half-coordinates guarantee; positive success probability ⇒ existence. Zero rows (e.g. the sin row at ℓ=0) cannot
  be normalized but impose nothing and only lower the threshold sum — the paper says so ("Zero rows impose no restriction").
- Limit η→0 (p.18): finitely many coordinate sets of size ⌈u/2⌉, compactness of [−1,1]^u, closed constraints ⇒ a point with
  ⌈u/2⌉ exact signs and the same discrepancy bounds. Checked; correct.
- Threshold arithmetic: c_i = 4√log(16R/u) ⇒ R·exp(−log(16R/u)) = u/16 exactly; restricted rows have ‖v_i‖2 ≤ √u (entries in
  [−1,1], u coordinates). Step error 4√(u log(16R/u)). u_{h+1} ≤ u_h − ⌈u_h/2⌉ ⇒ u_h ≤ 2^{−h}s. f(u)=u log(16R/u) has
  f' = log(16R/u) − 1 > 0 for u < 16R/e, so increasing on (0,R] ✓. With L = log(16R/s) ≥ log 16 = 4 log 2:
  h log2/L ≤ h/4 ✓; log(16R/s) ≤ 4 log(2R/s) ⇔ 0 ≤ 3 log(R/s) ✓. C0 = 8·Σ_{h≥0}2^{−h/2}√(1+h/4) — absolute ✓.
- §6.2: p_k ∈ [0,1/2], Σp_k = µ; initial floor to 2^{−J}Z costs ≤ N2^{−J} ≤ 1 in every row (rows of A have entries in [−1,1]) ✓.
  Odd 2^j p^{(j)}_k ∈ [1, 2^j−1] ⇒ ±1 keeps it in [0,2^j] and even ✓ (p may rise above 1/2, up to 1 — harmless: ε_k = σ_k(1−2p'_k)
  with p'_k = 1 is the flipped sign). Global sign flip of ξ keeps ‖Bξ‖∞ and makes Σ_{S_j}ξ ≤ 0 ⇒ mass never increases ✓.
  Each k ∈ S_j has p^{(j)}_k ≥ 2^{−j} ⇒ s_j ≤ 2^j µ ✓. Lemma 6.1 applied with R = 40N rows, s_j ≤ N ≤ R columns:
  log(2R/s_j) = log(80N/s_j) ✓. Case analysis U_j ≤ N / U_j > N ✓ (second case uses L_µ ≥ log 160 ≥ log 80, i.e. only µ ≤ N,
  which is automatic since µ ≤ N/2 always). Per-step error ≤ C0 2^{−j/2}√(µL_µ); Σ_{j≥1}2^{−j/2} = 1/(√2−1) ✓. (42) ✓.
- (43): −Q/2 at e(t_ℓ) has real/imag parts = rows 2ℓ, 2ℓ+1 of A(p'−p) ⇒ |Q| ≤ 2√2‖·‖∞ ✓.
- Grid→circle: Bernstein-type via max principle on Q and z^dQ(1/z): |Q| ≤ S(1+1/N)^{N−1} ≤ eS on |z| ≤ 1+1/N ✓; Cauchy on radius
  1/N ⇒ |Q'| ≤ eNS at circle points ✓; |dQ(e(t))/dt| ≤ 2πeNS ✓; mesh 1/M = 1/(20N), distance ≤ 1/(2M) ⇒ S ≤ G + πeS/20,
  πe/20 ≈ 0.427 < 1 ✓. Final constant C = 2√2/(1−πe/20)·max(1, C0/(√2−1)) — absolute, independent of N, X ✓.
- µ = 0: handled separately (ε = X, LHS = 0 ≤ C) ✓. Tiny µ > 0: bound → C(1+0); degrades gracefully; the "+1" from (40) dominates ✓.
  N = 1 covered (R = 40, M = 20; Q constant) ✓.
- "≤ N/2" monotonicity (p.4, proof of Thm 1.1): u ↦ u log(80N/u) is actually increasing on (0, 80N/e); it is used to pass from
  µ(X_N) ≤ 4δN (< N/5) to µ log(80N/µ) ≤ 4δN log(20/δ). Correct and sufficient; µ = 0 gives 0 ≤ that bound ✓.
- Lemma 2.2 as stated (p.4: "There is an absolute constant C such that for every N ≥ 1 and every X ∈ [−1,1]^N, some signs
  ε0,...,εN−1 satisfy max_t |Σ(εk − Xk)e(kt)| ≤ C(1 + √(µ(X) log(80N/µ(X))))") is exactly what §6.2 proves. No N-dependence in C.
  So far: NO FINDING in §6.

### §8 notes
- DL Definition 1: Φ_A(n) = (1/a)Σ_{k=0}^{a−1−n} A(k)A(k+n); "each binary word is automatically normalized" (binary = ±1).
  Definition 2: "The merit factor of A is 1/(2M_A), where M_A = Σ_{n=1}^{a−1}|Φ_A(n)|²." Lemma 0: "If A is a normalized word then
  ‖P_A‖2 = 1 and 2M_A = ‖P_A‖4⁴ − 1", with P_A = a^{−1/2}ΣA(n)zⁿ and normalized Haar measure. For binary A, Φ_A(u) = C_u(A)/N, so
  M_A = N^{−2}ΣC_u² and 1/(2M_A) = N²/(2ΣC_u²) = sib1's F(A) ✓; un-normalizing Lemma 0 gives sib1 (44) ‖P_A‖4⁴ = N² + 2ΣC_u² ✓.
  Numerically confirmed (exact DFT of |P|⁴ on a grid of 8N points, random words N = 2, 5, 13, 30) and C_{N−1} = a0a_{N−1} ✓.
- Corollary 8.1: 1/F(A_N) = ‖P‖4⁴/N² − 1 ≤ ‖P‖∞²‖P‖2²/N² − 1 = m_N² − 1 (‖P‖2² = N by Parseval; ‖P‖∞ = m_N√N for the minimizer) ✓;
  F_N ≥ F(A_N) → ∞ through every N ≥ 2, given Theorem 1.1 ✓. Brute-force sanity (N ≤ 12, all words, grid sup = lower bound for the
  true sup, so the check is in the safe direction): inequality holds; Barker controls reproduced (N=7: 1/F = 0.1224 → F = 8.17;
  N=11: 1/F = 0.0826 → F = 12.1). Note Corollary 8.2 needs only words of arbitrarily large merit factor (any subsequence).
- DL Theorem 2 verbatim: "There exist binary words with arbitrarily large merit factors if and only if there exists a binary Morse
  flow (X, S, µ) such that the Fourier transform of the spectral measure µ_f of the 'zero coordinate function' belongs to ℓ². In
  particular, the spectrum of (X, S, µ) is then simple and not purely singular." Forward proof checked: B_p with M_{B_p} → 0 fast,
  B_p(0) = 1 after a global sign flip; Fact 1 ⇒ unique ergodicity; Fact 2 ⇒ simple spectrum; σ̂_f(n) = Φ_A(n) by unique ergodicity
  (f continuous); Theorem 1 upper estimate M_{A×B} ≤ M_A + M_B + 2M_AM_B + 2M_A√(M_B² + M_B) (Cauchy–Schwarz, checked) ⇒ M_{A_p}
  bounded if Σ√M_{B_p} < ∞; Lemma 2's easy half (Fatou: M_A ≤ liminf M_{A_p}) is all the forward direction needs ✓.
  DL "simple spectrum" = multiplicity one in the Hahn–Hellinger decomposition (m = 1) — same as sib1's "has a cyclic vector" ✓.
  DL assert only "not purely singular"; sib1 asserts σ_f = h dt, h ∈ L², h ≥ 0, ∫h = 1, and "the absolutely continuous spectral
  component is nonzero" — the same content made explicit (ℓ² Fourier coefficients ⇒ L² density by Plancherel + uniqueness of
  Fourier–Stieltjes coefficients; conjugate symmetry because f real) ✓. sib1 explicitly does NOT claim Lebesgue spectrum: "Here
  simplicity concerns the full Koopman operator, whereas absolute continuity is asserted for the cyclic subspace generated by f;
  the remaining spectral type is not identified." Correct and not over-claimed (a Morse flow's L² contains the odometer
  eigenfunctions, so the full spectrum cannot be Lebesgue).
- Product convention: DL "A × B(s + at) = A(s)B(t)" = sib1 "(B × C)(s + bt) = B(s)C(t)" ✓; B_p(0) = 1 ⇒ prefixes stabilize ✓;
  two-sided extension per DL Definition 3 + following paragraph (incl. DL's own caveat for periodic Morse sequences) ✓.
- Companion remark (p.23): "[20, Theorem 1.1]: it constructs a smooth volume-preserving diffeomorphism of T³ whose Koopman operator
  has simple Lebesgue spectrum on the entire mean-zero L² space." [20]'s Theorem 1.1 verbatim: "There exist a C∞ volume-preserving
  diffeomorphism T : T³ → T³ and a real function f ∈ L²₀(T³, µ) such that {f ∘ Tⁿ : n ∈ Z} is an orthonormal basis of L²₀(T³, µ).
  Consequently T is ergodic, and U_T on this space is unitarily equivalent to multiplication by the coordinate w on L²(S¹, m)."
  Attribution accurate. Truth of [20] NOT checked (unrefereed OpenAI release of the same date; it would answer Banach's
  simple-Lebesgue-spectrum question). It is used in no proof in sib1.

## Method
Line-by-line re-derivation of every inequality in §6.1–6.2 and §8 against the rendered PDF; each external input quoted from the
local primary copy and matched hypothesis-by-hypothesis at the point of use; a short numeric sanity script (written outside the
untrusted dirs, /tmp/round_seat_scripts/chk.py, `nice -n 19 python3 -I`, seconds) for the §6 constants (Σ_{h≥0}2^{−h/2}√(1+h/4)
= 4.2369 ⇒ C0 ≈ 33.9; πe/20 = 0.4270; Σ_{j≥1}2^{−j/2} = 1/(√2−1) = 2.4142) and for (44)/Corollary 8.1. Hostile angles tried and
cleared: N-dependence of C0 or C (none: C ≈ 2√2·1.745·max(1, 2.414·C0) ≈ 4×10², absolute); mass increase across rounds (prevented
by the global sign flip, which is free because ‖B(−ξ)‖∞ = ‖Bξ‖∞); p leaving [0,1] (odd 2^j p ∈ [1, 2^j−1]); Lemma 6.1 applied with
s > R (impossible: s_j ≤ N < 40N = R); zero rows in LM (the sin row at ℓ = 0 is identically zero — vacuous, and dropping it only
lowers the threshold sum); LM's ≥ n/2 at tiny n (u = 1 allowed; LM's Claim 16 gives E|C^var| ≥ 0.56n for every n, and mn ≥ 40 in
every application so Claim 13's failure bound is small); grid-to-circle constant (< 1 with M = 20N); µ = 0, tiny µ, N = 1;
whether (2) delivers the µ needed (1 − |x| ≤ 1 − x² ⇒ µ ≤ 4δN ⇒ loss ≤ 2C√(δ log(20/δ))·√N + C) ✓.

## Findings
No FATAL. No GAP.

EXPOSITION (all repairable in a line, none affects Theorem 1.1):
- E1 (p.22, proof of Cor 8.2): "Its defining words have frequencies of both signs tending to 1/2; their Fact 1 gives unique
  ergodicity". Asserted without argument (DL p.9 also says only "it follows automatically"). True: for sib1's minimizers
  |Σ_j a_j| = |P_{A_N}(1)| ≤ m_N√N = o(N); for arbitrary words with M_B → 0 one can argue via L⁴ mass near z = 1 (if |Σa_j| ≥ cb
  then |P_B| ≥ c√b/2 on an arc of length c/(πb), forcing ‖P_B‖4⁴ ≥ c⁵b/(16π), while M_B → 0 forces b → ∞). One line would close it.
- E2 (overloaded symbol): µ is the defect mass in §2/§6 (p.4 "µ(X) = ½Σ(1 − |X_k|)", p.19) and the invariant measure in §8
  (p.22 "a unique S-invariant Borel probability measure µ"). Harmless; a different letter would help.
- E3 (p.4, §1 roadmap): "A dyadic rounding procedure keeps the defect mass from increasing, which makes its total loss o(√N) as
  the target error decreases." For fixed δ the loss is ≈ 2C√(δ log(20/δ))·√N, i.e. a small multiple of √N, not o(√N); the
  intended meaning (relative loss → 0 as δ ↓ 0, after N → ∞) is exactly what the proof of Theorem 1.1 uses. Wording only.
- E4 (p.18): Lemma 6.1 proof says LM's theorem gives the point "for every sufficiently small η > 0"; LM state it "with probability
  at least 0.1" for an efficient randomized algorithm (proof assumes δ < 0.1). Existence follows from positive probability; the
  paper could say so. (BBMST footnote 5 makes the same continuity remark: "it is clear by continuity that we can take δ = 0 if
  we are only interested in an 'existence proof'.")
Not findings against sib1 but noted: LM v2's own proof has typographical slips (Claim 15 prints "≤ 1 − δ + γE[|(U_t)_i|²] ≤ 1"
where (1−δ)² + γ² is meant; Claim 13's bound 1/(mn)^{C−2} is vacuous at mn = 1 though γ-dependence repairs it) — the statement of
Theorem 4 is unaffected and the paper is published (SICOMP 44(5), 2015) and widely used.

## External inputs checked (source, version, exact statement vs use)
1. Lovett–Meka, arXiv:1203.5747v2 (= the version sib1 [19] says it cites), Theorem 4 — quoted in the running notes. Use on p.18:
   n = u (remaining coordinates), m = R rows restricted to them, x0 = current values, c_i = 4√log(16R/u) giving threshold sum
   exactly u/16 (hypothesis met with equality, allowed: "≤ n/16"), conclusion (i) used with ‖v_i‖2 ≤ √u, conclusion (ii) used
   after η → 0 to fix ⌈u/2⌉ coordinates. Hypotheses match; nothing on row norms is required beyond finiteness; no dimension
   constraint m vs n in Theorem 4 (m = 40N ≫ n is fine — the price is only in the c_i). C0 absolute ✓.
2. Downarowicz–Lacroix, author manuscript (the URL sib1 [7] gives; TCS 209 (1998) 377–387): Definition 2, Lemma 0, Theorem 2 +
   proof, Definition 3, Facts 1–2 — quoted in §8 notes; normalization and statement match sib1's use.
3. DL's Fact 1 (Iwanik–Lacroix, Studia Math. 110 (1994)) and Fact 2 (Kwiatkowski, Bull. Acad. Pol. Sci. 29 (1981)) — NOT fetched
   (paywalled / pre-arXiv; not attempted beyond identifying the entries). sib1 inherits unique ergodicity and simple spectrum
   from DL's citation of these. Robustness check: the L²-density conclusion survives without Fact 1 for SOME invariant measure
   (weak* limit of empirical measures along the prefixes A_p + Fatou), and DL remark that some invariant measure always gives
   simple spectrum — but the "unique" and "simple" in Cor 8.2 rest on [I-L], [Kw] as cited by DL.
4. BBMST arXiv:1907.09464v1 §4: Theorem 4.1 = LM Theorem 4 restated with exact signs; Sections 4–5 do use partial colouring to
   round to signs — sib1's attribution sentence (p.18) is accurate.
5. OpenAI [20] Theorem 1.1 — attribution accurate (quoted above); mathematical content not checked; not load-bearing.

## What I skimmed / did not check
- Did not check Theorem 1.1's other inputs (§3–§5, Prop 2.1) — other seats. §8's Corollaries are only as good as Theorem 1.1.
- LM §6 (their derivation of Spencer/Srinivasan) skimmed; LM's Lemma 11 proof read for the n/2 guarantee and small-n behaviour,
  not re-proved in full rigor.
- DL Lemma 1/Theorem 1 algebra checked at the level of the displayed identities and the Cauchy–Schwarz step; DL Lemma 2's harder
  half and the converse direction of Theorem 2 not needed and not checked.
- Kwiatkowski / Iwanik–Lacroix primary sources (Facts 1–2): COULD NOT FETCH / not attempted.
- The companion manuscript [20] beyond its Theorem 1.1 statement.
- Corollary 7.1 and Appendix A (reduce seat), although p.21–23 were read in passing; nothing there was examined adversarially.

## Verdict
HOLDS AS READ IN SCOPE — §6 (Lemma 6.1 vs Lovett–Meka v2 Thm 4, dyadic rounding, Lemma 2.2 with absolute C for every N ≥ 1 and
every X, incl. µ = 0) and §8 (merit-factor normalization = DL Def 2/Lemma 0; Cor 8.1 from Thm 1.1 via ‖P‖4⁴ ≤ ‖P‖∞²‖P‖2²;
Cor 8.2 = DL Thm 2 forward direction, not over-claimed) verified line by line; 4 EXPOSITION notes; DL's Facts 1–2 primary sources
not checked.
