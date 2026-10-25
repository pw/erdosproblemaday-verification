VERDICT: HOLDS AS READ — the geometric transfer (Blinov's patch to OpenAI §§5–8 at e29a291; Chen §§3–4) survives every parameter change I could trace. I found no MUST-FIX. Two side results for the panel: (a) Chen's s0 = 102195 is not forced by anything. (b) The coordinator's item-8 ceiling 2/(246k+8) is correct only relative to the printed Lemma sam:proportional. It is not a ceiling for "this whole family of arguments" (finding 1).

Seat G (hostile referee, geometric transfer). Sources read: OpenAI TeX `/tmp/oaimath/191/paper/src/build/sections/0{1..9}-*.tex`; `blinov-fpc/patches/reserved-tags.patch` (sha256 a177ca56…, commit e29a2912f759…); `blinov-fpc/notes/sphere-packing.tex` (§sec:slab, §sec:rowdigits, §sec:five, §sec:reserved); `docs/review.md`; `chen191.pdf` (sha256 bc03013e…). I rendered pp. 5, 7–10 before relying on any formula. arXiv:1802.00085v3 is the current version (v3, 27 Nov 2018); I fetched it and rendered pp. 4–5.

---

## Findings

### 1. SHOULD-FIX (coordinator's item-8 claim, not either paper). The 2/(246k+8) "ceiling" comes from a residue-blind lemma; a short rigorous sharpening raises the family's supremum to at least 2/(183k+8).

**Brief, item 8:** "my (the coordinator's) claim to refute is: sup η = 2/(246k + 8) = 1/(123k + 4) = 1/50,280,067, not attained."

**What holds.** Take the printed bounds as fixed: Lemma sam:proportional, the bad-triple bound ≪ (log 2N)² h/(N³r⁸), q ≍ h⁶, B ≍ r⁶, h/τ ≍ B. Let N (any multiple of hq) and a_r be free. Then the claim is right. In exponents of r (x = log_r a_r, Y = 3 log_r N) the two deletion conditions are:
- (i) x + 252k − Y ≤ 0 (pairs);
- (ii) 2x + 6k − 8 − Y ≤ 0 (triples, up to (log r)²).

The objective is η = (2x + 6(k−1) − Y)/x. It is maximised at the vertex x = 246k+8, where η = 2/(246k+8). That vertex is not attained, because (ii) carries (log r)² with zero power saving there. Varying L3 = r^{1+μ} does not help: μ ≥ 3 is forced by θ ≤ 1/2, and every μ > 3 is strictly worse. Blinov (Y = 504k), Chen (s0 = 102195) and the best-s0 Chen variant (finding 2) all sit strictly below this ceiling. Verified exactly in `arith.py`.

**Why it is not a ceiling of the family.** Condition (i) is the only binding constraint besides (ii). It comes entirely from OpenAI's Lemma sam:proportional (eq. sam:pair-bound):

> "Pr(π(u)=π(v)) ≪ (hq)^6 N^{−3}" — proof: "The preceding count bounds the number of proportional pairs within any two such sets of lifts."

That proof throws away all residue information. Using only facts already in the paper, there is a short rigorous sharpening:

- **(α) Modulo h.** Suppose u and v are proportional over ℤ. Then every 2×2 minor of (u|v) vanishes. The minors of G_h(c|c′) are Λ²(G_h) applied to the minors of (c|c′), and det Λ²(G_h) = det(G_h)² = 1. So every minor of (c|c′) vanishes mod h. Since c₁ is a unit, this forces c′₃ ≡ (c′₁c₁⁻¹)c₃ (mod h).
  - Condition on everything except the k third-row digits of the second column. Those digits lie in [1, L3] with L3 < B, so the base-B expansion is injective mod h = B^k. At most one of the M^k equally likely digit vectors works. So the probability is ≤ M^{−k}.
- **(β) Modulo q.** Since 0 ∉ V, the point v_q must lie on the line through 0 and u_q. That line is a line in F_q³, and it meets the cap image V = G_q(a+S) in at most 2 points. So, given V, the probability is ≤ 2/s.
- **(γ) Combining.** Given (G_h, V), the mod-h and mod-q draws are independent. On the event that both (α) and (β) hold, the residue-blind count still bounds the conditional probability. So

  **Pr(π(u)=π(v)) ≤ 2C·M^{−k}·s^{−1}·(hq)⁶N^{−3}**, with C = 6750 in Chen's (B16) normalisation.

In exponents this subtracts log_r(M^k s) = 3k + 60k = 63k from (i). The new vertex is x = 183k+8, with log_r N = 124k + 8/3 ≫ log_r(hq) = 42k, so N is still a legal multiple of hq. The family supremum becomes

**sup η ≥ 2/(183k+8) = 2/74,806,931 ≈ 1/37,403,466**, which is 34% above 1/50,280,067.

Neither paper is affected: both use the weaker bound, which is still true. Heuristically, a lift count that also uses the compatible residues would relax (i) further. That is not proved here.

Toy checks of (α) and (β) are in `prop_toy.py`, with mutations that must fail.
- A rank-one G must break (α): it does, 5394 violations.
- L3 = B+1 must break digit injectivity: it does.
- A non-cap S (a plane slice) must give a line through 0 meeting V in ≥ 3 points: it does.

### 2. NIT (Chen, (9) and §4.2). s0 = 102195 is not forced. Chen's own argument allows every s0 ≤ 136,259, giving η = 2/(246k+17) = 2/100,560,143 > 2/100,866,719.

Chen, §4.2: "the first term is at most 2^{22} r^γ B^{(3s0−k+1)/2} = 2^{22} r^γ B^{−102195/2} < 2^{22} r^{γ−306585} < 1/8. This estimate retains the slack needed for the smaller lift box."

The value s0 = 102195 is exactly (k−1)/4, i.e. it is chosen so that 3s0 − k + 1 = −s0. I checked every other step of §§3–4 where s0 enters:
- hq | N needs s0 ≤ 3k.
- N ≥ h holds.
- N ≤ 16B^{28k−s0} holds.
- β ≥ 1 holds.
- δ = 2/(ρ+1) > 2^{−26} holds.
- D0 = 2^{20ρ}, C0, c = 2^{−100ρ} and N0 = 2^{(ρ+1)2^{50}} carry through with the new ρ.

None of these blocks a larger s0. The first-term inequality holds for every s0 with 3s0 < k−1, i.e. s0 ≤ 136259. At s0 = 136259 the first term is 2^{22}r^{γ}B^{−3/2} < 2^{22}r^{γ−9} < 1/8 for r ≥ 37, since 37⁸ > 2²⁵. That gives ρ = 249k + 3 − 9s0 = 100,560,141 and η = 2/(ρ+2) = 2/(246k+17). At s0 = 136260 the exponent becomes γ > 0 and the bound fails (control asserted in `arith.py`).

In general η(s0) = 2/(249k + 5 − 9s0). This is not an error — Chen's stated theorem is true — but his exponent is not the best his own bookkeeping gives.

### 3. NIT (Chen, (B8)). The stated reason for the first constant is loose; the constant itself is true.

"the stated constants follow since the denominators are at least half their leading powers for q ≥ 3."

For the affinely-independent bound, read literally, halving (q³−1) and (q³−q) separately and multiplying by the shift factor 2 gives 8, not 4. The true value is 2q⁶/((q³−1)(q³−q)) ≤ 2·729/624 < 2.34, so W ≤ 4 holds (it also follows if "half" is applied to the product). Nothing downstream changes; even 8 would only turn 2^{37} into 2^{38} in case (i).

### 4. NIT (Blinov's patch leaves stale text outside the six patched sections).

The patch is described in docs/review.md as a "six-section source patch" and does not touch §1 or §9 (app:prime-interval). Two sentences there still say Bertrand's lemma is used for interpolation:
- OpenAI §1 (Organization): "Appendix~\ref{app:prime-interval} gives the elementary prime-interval proof used in the parameter choices and interpolation."
- OpenAI §9: "the form of Bertrand's postulate used to choose the two moduli and to pass to every sufficiently large cardinality."

The patched §8 now uses the prime number theorem in the progression 1 mod 3 for r. The mathematics is fine; these sentences are now false descriptions. Similarly, the patched proof of Lemma aux:cap keeps the now-irrelevant sentence "Thus Γ, and every translate of it, has the asserted line property" — harmless.

---

## What I checked and how

### Item 1 — slab cap
- S = {(x,y,Q(x,y)) : 0 ≤ x < w, y ∈ F_q} lies inside Γ. Q = x² − νy² with ν a nonsquare is anisotropic, so any line with (v1,v2) ≠ 0 meets Γ in at most 2 points, and a vertical line meets it once. Hence S is a cap with exactly |S| = wq points.
- I traced every use of S:
  - Lemma aux:random-set uses only v₁ ∈ [0,w): the bound |Σx_i v_{i,1}| ≤ 3H(w−1), and 0 ∉ V via ‖a₁‖_q ≤ w−1.
  - Prop aux:weights uses only the cap property, |S| = s, 0 ∉ a+S and |𝒜| ≥ q³/2. Its count of s(s−1)(s−2) ordered triples is valid for any cap.
  - §§6–7 use only the W bounds and the support statement.
  - Nothing uses the second or third coordinate's size. The old box {0..w−1}³ is used nowhere beyond coordinate 1.
- 0 ∉ V still holds. Note that (0,0,0) ∈ S now, but a ∈ 𝒜 excludes it from a+S.
- s = wq ≥ q²/(2000H²) because q ≥ 2000H² forces w ≥ q/(2000H²). Hence q³/s ≤ 2000qH² = 8000qh².
- Exhaustive toy check `cap_toy.py`:
  - cap sweep at (q,w) = (31,31), (101,3), (101,10), (103,7), (127,5);
  - full short-relation check over all ordered pairs and all x with |x| ≤ 2 at (q,H,w) = (307,2,4) and (401,2,2): |V| = wq, 0 ∉ V, a nonzero-sum relation never occurs, a zero-sum relation occurs only among affinely dependent columns, and every line through 0 meets V in ≤ 2 points.
  - Base run: "ALL TOY CAP CHECKS PASSED" (2030 points). Mutations that must fail, all rejected:
    - ν a square → `three collinear points in S (q=31, w=31)`;
    - slab moved to coordinate 2 while only coordinate 1 is shift-protected → `short relation with nonzero sum, x=(-1, 1, -1)`;
    - a₁ = −1 (not an allowed shift) → `short relation with nonzero sum, x=(-1, 1, -1)`.
    - Log: `G_work/cap_toy.log`.
  - Instrument note: for w ≤ 2 the slab is a cap for ANY quadratic, because a line with v1 ≠ 0 meets at most w slab layers. My first toy run used w ≤ 2 and its cap check could not fail. I caught this because the square-ν mutation passed, and rebuilt the sweep with w ≥ 3.

### Item 2 — H = 2h
Every use checked:
- the set 𝒜 (m ≤ 3H < q, 3Hw < q/2, union bound 18/1000 + 3/(2000H));
- |x| ≤ H in Lemma aux:random-set and Prop aux:weights, with |Σx_i| ≤ √3H ≤ 3H;
- the affine case: a contributing x has |x| > 2h, so the shell R ≤ |x| < 2R has R > h, and Lemma zero:moment needs R ≥ h ≥ B^j (patched line "H/2 = h");
- q ≥ 2000H² = 8000h², which holds for h ≥ 10 (h⁴ ≥ 8000 needs h ≥ 9.46; the assertion with h = 9 is the control).

### Item 3 — h⁶ < q ≤ 2h⁶
Recomputed with q³/s ≤ 8000qh² and g³ ≤ Ih²:
- (zero:equal-additional): h²q^{−3}(q³/s)² ≤ 8000²·h⁶/q;
- (zero:special-rank-two): ≤ 8000·h⁴/q;
- (zero:special-rank-one): ≤ 8000²·h⁶/q².

All three are bounded. Also:
- τ < h < q, which is needed for rank 3 mod q when t ≠ 0;
- q ∤ E, since q is a prime > h ≥ E, which gives surjectivity in Lemma zero:plane;
- R > q/2 in the special case, which gives (1+R/q)³ ≪ (R/q)³;
- q is odd and coprime to h.

### Item 4 — N = (hq)⁴
- hq | N.
- λ₃(Λ) ≤ E ≤ h < 4N.
- Lemma sam:proportional is valid for any N with hq | N.
- First deletion term: n_r(hq)⁶N^{−3} ≤ r^γ(hq)⁶N^{−3/2}τ^{−1/2} = r^γτ^{−1/2} = O(r^{γ−3(k−1)}).
- log(2N) = O_k(log r).
- |x| ≤ 16N², giving O(log 2N) shells.
- a_r > r^γh^{11/2}.
- Nothing in §7 needs N large relative to q or h.

### Item 5 — corollary and deletion
- The patched proof of Cor sam:bad-triple bounds Pr(bad | C, labels) ≪ (log 2N)²·(hD/N³)·1_J. This uses: J is a function of det C mod h; SL₃ preserves it; 2τ < h leaves at most one t; the orbit bound and the weighted count. Averaging uses E[D1_J] ≤ 6/(Mr⁵) + 2/r¹⁰ ≤ 8r^{−8}, which I took as given (seat P).
- Exact Fractions (`arith.py`): β = 42k − (k−1)/2 = (83k+1)/2; 6β = ρ = 249k+3; α = γ + 6β = ρ + γ; η = 2γ/α = 2/(ρ+2) = 2/(249k+5) = **1/50,893,237**.
- The B interval 100k²P = 40000k⁴r⁶ < B ≤ 80000k⁴r⁶, and θ = B/M² ≤ 80000/400² = 1/2.
- h/τ ≤ 3B = O(r⁶). The second term is O((log r)²r^{2γ−2}) with 2γ−2 = −2/(ρ+1); the all-three-equal term is r^{2γ−4}.
- The bound √2·r^γB^β < a_r ≤ 2⁶√3·r^γB^β.
- Mutations rejected: k → 408782, β off by ½, ρ → 249k+4, s0 → 102196, smax → 136260, ceiling → 2/(246k+9).

### Item 6 — interpolation
π(x;3,1) ~ x/(2 log x) gives π(2m;3,1) − π(m;3,1) ~ m/(2 log m) > 0. This is enough for a prime r ≡ 1 (3) in (m, 2m] for all large m, hence r ≥ 37 eventually. The two-sided bound n ≤ n_r ≤ C_k·n with C_k = max{1, 4^α D_k/A_k} goes through with non-integer α.

### Item 7 — Chen §§3–4
- **Smaller N**: N/(hq) = B^{3k−s0}q³ ∈ ℤ; N ≥ h; λ₃ ≤ E ≤ h ≤ 4N; first term of (B17) as above; nothing in the zero count needs N ≫ q or h.
- **Constants (B2)–(B19)**, each recomputed:
  - (B2): index < 6, since 3^{3/2} < 6.
  - Plane count 9π < 32.
  - (B3): 2^{15}·250 ≤ 2^{23}; 125·512 < 2^{16}; 3·2^{28} < 2^{30}; (log₂ 2R₁)² groups.
  - (B4): coordinates ≤ 3^{3/2}X/(mλ_j); columns ≤ 9X/λ_j ≤ 64X/λ_j; 2^{33+36+6}.
  - (B6): 21/64 > 1/4.
  - (B7): 8000 < 2^{13}.
  - (B8): see finding 3.
  - (B9): 9·2^{94} < 2^{98}; |x| ≤ 16N²; 5 log₂(2N) shells.
  - (B11): 2^{27}.
  - (B12): 125(Y/B^j)³ and the geometric sum ≤ 2B^{b+e}.
  - (B13): fine.
  - Case (i): 2^{37}. Case (ii): 125·4·2^{27}·2^{26} ≤ 2^{62}. Case (iii): 2^8Y³/q², 2^{50}, (q+1) ≤ 2q, 2^{64}. Total < 2^{68}, and 5·2^{68} < 2^{71}.
  - (B15): 2^{122}, and 8/r⁸.
  - (B16): 750N and 6750 ≤ 2^{13}.
  - (B17): C(2n,2) ≤ 2n², C(2n,3) ≤ 2n³.
  - Second term: k < 2^{19}, 80000k⁴ < 2^{93}, 5 + 28k(93+6x) < 701kx for x ≥ log₂37, 701k < 2^{29}, 3·2^{277} ≤ 2^{279}, ρ+1 < 2^{27}, monotone for x ≥ 2^{50}, value 2^{400−2^{24}}.
  - (B18), (B19): a_r ≥ 2r^α; 64√3(80000k⁴)^β < 2^{7+93ρ/6} < 2^{20ρ}.
  - Transfer: y = n^{1/α} ≥ R; C0 = 2^{21ρ+1} ≥ D0·2^α; 64·D0·C0² = 2^{62ρ+8} < 2^{100ρ}.
  - c = 2^{−10086671700} and N0 = 2^{100866718·2^{50}} match (9).
  - **No wrong inequality found.**
- **BMOR (B1)**: arXiv:1802.00085v3 Theorem 1.2 (p. 5) gives |θ(x;q,a) − x/φ(q)| < c_θ(q)·x/log x for x ≥ x_θ(q), with c_θ ≤ c₀ and x_θ ≤ x₀. By (1.10)–(1.11) (p. 4), c₀(q) = 1/840 for 3 ≤ q ≤ 10⁴ and 1/160 for q > 10⁴; x₀(q) = 8·10⁹ for 3 ≤ q ≤ 10⁵.
  - So |θ(x;3,1) − x/2| < x/(840 log x) ≤ x/(160 log x) for x ≥ 8·10⁹, exactly as Chen uses it. His "1/840" remark is correct; the table gives x_θ(3) = 7,932,309,757.
  - His prime-in-(x,2x] derivation is correct. B and q intervals both start above 8·10⁹.

### Item 8
Covered by findings 1–2, with LP vertex plus brute sampling in `arith.py`.

### Commands
All run with `bash -c 'ulimit -v 8000000; exec timeout … nice -n 19 python3 -I <script>'` in `/tmp/oaimath/191b/seats/G_work/`:
- `arith.py` [mutation] — exact exponent bookkeeping, s0 range, ceiling LP, sharpened LP;
- `cap_toy.py` [square_nu | slab2 | badshift], driven by `run_cap.sh`, log in `cap_toy.log`;
- `prop_toy.py` [singularG | bigL | plane].

No script from `src/` was executed; the repositories were only read.

## What I did NOT check
- §§3–4 algebra: the CGLV 18-form identity, the 9-node descent, the reserved-tag packing, and Lemma orb:tagged-moment / Chen §2 (taken as given; seats P/W). Also the Lean files and the Blinov certificates/scripts.
- The orbit lemma and lattice lemmas of OpenAI §§2, 4 beyond re-deriving Chen's constants. (Treated as refereed baseline.)
- I did not attempt to prove the heuristic further relaxation of (i) mentioned in finding 1. Only the M^{−k}·(2/s) sharpening is claimed rigorous.
- I did not check whether the tag construction changes the hypotheses of Lemma sam:lifting (uniformity of G_hC on 𝒪); seat P's domain.
