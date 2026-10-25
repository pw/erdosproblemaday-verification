# Hostile referee report — seat `perturbation` (§6, 06-perturbation.tex)

Paper: OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026), family 160, Erdős #138.
Source read: `build/sections/06-perturbation.tex` (286 lines, all of it) + `build/figures/norm-band.tex`, cross-checked against the
rendered PDF (printed pp. 16–19: §6 opens p. 16; Lemma 6.1 p. 16; Figure 1 and Lemma 6.2 p. 17; Theorem 6.3 p. 18; (6.7)–(6.9) p. 19).
Imported statements read in their TeX: 02-setup.tex (all), 03-counting.tex (all), 04-outer.tex (all), 05-dichotomy.tex (all),
01-introduction.tex (construction paragraph). Lean read AS TEXT ONLY (no lean/lake run): `NormBands.lean`, `KeyMultiplicity.lean`,
`Perturbation.lean`, `PerturbationScales.lean`, `ProbabilityScales.lean`, `SignatureCounting.lean` (ll. 180–253),
`CyclicSignatures.lean` (ll. 34–75), `Arrangement.lean` (declarations).
Referee: Claude (Opus 5.5), 2026-10-15. Checks: `/tmp/oaimath/160/seats/perturbation_checks/` (every run < 60 s, < 300 MB).

## Verdict for this scope

**HOLDS AS READ.** Every step of Lemma 6.1 (perturb:multiplicity), Lemma 6.2 (perturb:signatures) and Theorem 6.3 (perturb:cyclic)
was re-derived; no FATAL and no GAP found. The objections below are COSMETIC/UNCLEAR. Two findings worth carrying upward:

* the key-multiplicity bound "at most four" is true but loose by a factor 2 — the paper's own interval argument gives **at most two**,
  and that is exactly what the Lean proves (`affine_norm_band_card_le_two`, then weakened by `decide`); confirmed by exact checks;
* the Lean does **not** formalize the paper's displayed count (perturb:signature-count) with exponent 3: it proves
  `T_aff ≤ T_glob · 25·(k(Dq²+1)+1)^8` from a threshold-family/shatter-type arrangement bound `(e+2)²(s+1)^{2(e+1)}` (`Arrangement.lean: card_realizedSigns_le`), not the paper's
  `(e+1)²(s+1)^e`. The weaker exponent still gives `log T_aff = O(k^{9/10} log k) = o(pk)`, so the theorem is unaffected, but the
  paper's exponent-3 display rests on Lemma 3.1 (count:arrangement) alone, which the `counting` seat owns.

The binding inequality of the whole section is (6.8) `2c − γ/80 < 0`; it is what caps `c` (see "prove-too-much" below).

## Objections (numbered)

**1. COSMETIC (exposition; proof correct) — Lemma 6.1, proof, p. 17: the four-point bound is a factor 2 loose.**
TeX: "If it is nonempty, then $m+1-C'>0$, and on the half-line $t\ge0$ it is contained in the closed interval with endpoints
$\sqrt{\max\{0,m-C'\}},\ \sqrt{m+1-C'}$. … this interval has length at most one. … each of these intervals contains at most two sampled
points: three points in an interval of length at most one would have total separation at least two. Thus the key occurs at most four
times."
What is wrong: nothing false, but the relaxation to the CLOSED interval throws away the fact that the band is half-open in `t` on each
half-line: on `t ≥ 0` the band is exactly `[√u, √v)` with `√v − √u ≤ 1`, and two points at mutual distance ≥ 1 cannot both lie in a
half-open interval of length ≤ 1. So each half-line carries ≤ 1 point (if `u = 0` the two halves share `t = 0` and together form the open interval `(−√v, √v)` of
length ≤ 2, which also holds ≤ 2 points) and a key occurs **≤ 2** times. The Lean proves precisely this
(`NormBands.lean: weighted_scalar_band_card_le_two`, `KeyMultiplicity.lean: affine_norm_band_card_le_two`) and only then weakens to 4.
The Figure 1 caption ("at most 2 points per piece") inherits the slack. Exact checks below: with separation 1 the observed maximum is 2
(and 1 per closed half-line) in 4000 random exact-rational lines in dimensions 1–4, in a 160,400-case deterministic sweep, and over every
progression of all seven cyclic models of Check C. Fix (optional): state 2; Theorem 6.3 then gets `γk/2` keys in the rich case and `s ≥ k/2` in the
affine case, which loosens the cap on `c` to `2c < γ/40`. Nothing downstream depends on 4 vs 2.

**2. COSMETIC (exposition) — cross-reference names in the rendered PDF, pp. 16–19.**
Every `\Cref` to a lemma or proposition renders as "Theorem": "supplied by Theorem 4.2" (it is Proposition 4.2, outer:coloring),
"so Theorem 5.1 gives" (Lemma 5.1, dichotomy:affinity), "By Theorem 6.1" ×3 and Figure 1's "bound in Theorem 6.1" (Lemma 6.1),
"Theorem 3.1, in the fixed dimension three" (Lemma 3.1), "Theorem 3.2 bounds log T_glob" (Lemma 3.2), "using Theorem 6.2" (Lemma 6.2),
"allowed by Theorem 2.2" (Lemma 2.2). (Same defect outside scope: count:local renders "Apply Theorem 2.5" for Lemma 2.5.) Numbers are
right, so a reader can follow; the environment names are wrong. Fix: cleveref `\crefname` per environment (shared counter).

**3. COSMETIC (exposition) — Lemma 6.1 is stated unconditionally but uses standing large-k facts.**
TeX: "For every progression $n_j=n_0+jd$ in $G$ with $d\ne0$ and $0\le j<k$, every key occurs at most four times among the
$\kappa(n_j)$." The proof uses (a) distinct terms — from §2's "Every nonzero element of this prime-power cyclic group has order at least
$P>k$" (Lemma 2.2 holds only for large k); (b) `2kH < 1` inside Lemma 5.1, i.e. `2/k < 1`, k ≥ 3; (c) `|I| ≤ 2H` from Lemma 2.3;
(d) `gcd(λ,q)=1`, i.e. `h_0 < P`. All are covered by §2's blanket "Throughout the cyclic construction, $k$ is an integer exceeding an
absolute threshold", so this is not a gap. The Lean states (a),(b),(d) as explicit hypotheses (`hk : k ≤ P` — weaker than the paper's
`P > k` and sufficient, since index differences are `< k ≤ P`; `hsmall : 2kH < 1`; `hunit : Coprime dilation (q^D)`).

**4. UNCLEAR (paper-vs-Lean correspondence; theorem unaffected) — Lemma 6.2, (6.4), p. 17.**
TeX: "There is an absolute constant $C$ such that $T_{\mathrm{aff}}\le C T_{\mathrm{glob}}\bigl(k(Dq^2+2)\bigr)^3$." and in the proof
"\Cref{count:arrangement}, in the fixed dimension three, therefore gives at most $C\bigl(k(Dq^2+2)\bigr)^3$ such words."
The constant is never given; from Lemma 3.1 with `e = 3`, `s = k(B_*+1) ≤ S := k(Dq²+2)`: `16(s+1)³ ≤ 16(2S)³ = 128 S³`, so `C = 128`
works. The Lean (`SignatureCounting.lean: card_affine_yRep_fullLabel_signatures_le`, `CyclicSignatures.lean:
card_actual_affine_signatures_le`) proves instead `T_aff ≤ T_glob · 25·(k(Dq²+1)+1)^8`, because its arrangement lemma
(`Arrangement.lean: card_realizedSigns_le`, `(e+2)^2*(s+1)^(2*(e+1))`) is obtained from a threshold-family/shatter count
(`shatters_card_le`, `card_thresholdFamily_le`, squared), not from the paper's region count. So the
formal proof certifies a weaker statement than (6.4) and the paper's exponent 3 is supported only by the human proof of Lemma 3.1
(SKIMMED here; `counting` seat). For (6.5) either exponent gives `log T_aff ≤ O(k^{3/10}log k) + O(log q) = O(k^{9/10} log k)`; with
exponent 8 the term is `16 log q + 8 log k + 8 log D + O(1)` instead of `6 log q + 3 log k + 3 log D + O(1)`. Fix: state the constant
(128) and, if the paper is meant to track the Lean, say that any polynomial in `k(Dq²+2)` suffices.

**5. COSMETIC — Theorem 6.3, rich case, p. 18: "We may take $k$ sufficiently large that $p<1/2$."**
Correct; explicitly `p = k^{−1/20} < 1/2` iff `k > 2^{20} = 1,048,576` (`p = 1/2` exactly at `k = 2^{20}`, where the affine-case step
`p ≤ 1−p` still holds). This is the largest threshold that §6 itself introduces (table below). The Lean uses `p ≤ 1/2`
(`target_probability_le_stay_pow (hp2 : p ≤ 1 / 2)`).

**6. COSMETIC — the hedge words in scope.** `grep -i` for clearly / it follows / similarly / same argument / immediate / obvious / easily /
trivial / follows over 06-perturbation.tex finds exactly two: l. 43 "when $|J|\le1$ the claimed multiplicity bound is immediate" (true:
≤ 1 ≤ 4) and l. 183 "\Cref{perturb:entropy} follows" (checked: `k^{−1/20} log k → 0`). Neither hides a step.

No other objection. In particular I looked for, and did not find: a quantifier fixed after use; an inequality in the wrong direction; an
`o(1)` depending on the progression (all bounds are uniform over progressions and over the prime `P`, using only the upper bound in
(2.4)); a probability called exact that is approximate (the affine-case `p^u(1−p)^{s−u}` IS exact — independent bits on `s` distinct
keys); a lemma applied outside its hypotheses (Lemma 5.1 is applied to the V-box alone, whose coordinate widths are ≤ 2H — the
U-coordinates are not needed and not used); a dependence on `r` (none: `r` does not occur in §6).

## Item-by-item: what was checked and how

### (6.1) perturb:keys and finiteness — VERIFIED LINE BY LINE
`f(n) = ‖qỹ(n)‖²`, `κ(n) = ((V(y_i(n)))_{i≤D}, ⌊f(n)⌋)`. The V-label of a circle point is the mesh interval of its representative in
`[−1/2,1/2)` (§2: "the same intervals also denote their images in T"), and every mesh interval (mesh:intervals) is a real subinterval of
`[−1/2,1/2)`, so "the centered representative lies in the box" and "the V-label is that box" are the same condition. `𝒦` is the image of
the finite set `G`. ✓

### Lemma 6.1 (perturb:multiplicity) — VERIFIED LINE BY LINE (+ exact checks)
* *Affinity in a V-box.* `y(n_j) = y(n_0) + j·y(d)` in `T^D` because each `y_i = λ·(n/q^i mod 1)` is a homomorphism `G → T`
  (well defined since `q^i | q^D`). The V-box is a product of half-open intervals of length ≤ 2H (Lemma 2.3, last inequality, using
  `ρ+α ≤ 3/4`); two members of a half-open interval of length `w` differ by `< w ≤ 2H`. Lemma 5.1's hypotheses (`z_j = a+jb` in `T^e`,
  representatives for `j ∈ J` in one box of widths ≤ 2H, `2kH < 1`) hold with `e = D`, `2kH = 2/k < 1`. Its proof (integer combination
  `(j_3−j_2)(Z_{j_2}−Z_{j_1})−(j_2−j_1)(Z_{j_3}−Z_{j_2})` of size ≤ `2H(j_3−j_1) < 1`) re-checked. `J` need not be consecutive — Lemma 5.1
  allows any `J`. ✓
* *Separation (6.2).* Distinct terms: `(j−j')d = 0` in `Z/P^{eD}` would force `P | (j−j')`, impossible as `0 < |j−j'| < k < P`.
  `λ` is a unit mod `q^D` since every prime factor of `λ` is ≤ `h_0 < k < P`. So `λ(n_j−n_{j'})` is a nonzero residue; any integer
  representative `z ≠ 0` has `q^D ∤ z`, so the largest `a` with `q^a | z` lies in `{0,…,D−1}` and is independent of the representative.
  With `z = q^a u`, `q ∤ u`: `y_{a+1}(n_j) − y_{a+1}(n_{j'}) = λ(n_j−n_{j'})/q^{a+1} ≡ z/q^{a+1} = u/q (mod 1)`; `u mod q ∈ {1,…,q−1}`
  (q a prime POWER: `u` may be divisible by `P`, irrelevant — the paper says so), so the circle distance is ≥ `1/q`. "The difference
  between any two real representatives has absolute value at least their circle distance": for reals `a,b`,
  `dist_T = min_{m∈Z}|a−b−m| ≤ |a−b|` (take `m = 0`). Holds for CENTERED representatives as for any. Multiply by `q`: (6.2). ✓
  Exhaustive exact check: 0 failures over all ordered pairs `n ≠ n'` in seven models (up to 5,762,400 pairs); control with `λ = P`
  (not a unit) produces 14,406 failures.
* *Line geometry.* For `|J| ≥ 2`, the points `qA + j·qB` (`j ∈ J`) are pairwise ≥ 1 apart, so `qB ≠ 0` and they span a line `ℓ`;
  `z_0` = orthogonal projection of 0 on `ℓ`, `e` unit along `ℓ`, `‖z_0+te‖² = t² + ‖z_0‖²`. Band `m ≤ t²+C' < m+1`; nonempty ⇒
  `m+1−C' > 0`; on `t ≥ 0`, `t ∈ [√u, √v)` with `u = max(0, m−C')`, `v = m+1−C'`, `0 ≤ u ≤ v`, `v − u ≤ 1`.
  `(√v−√u)² = v+u−2√(uv) ≤ v−u ⟺ u ≤ √(uv) ⟺ √u ≤ √v` ✓, so length ≤ 1. Three points with pairwise gaps ≥ 1 span ≥ 2 > 1 ✓ (≤ 2 per
  closed piece). `t = 0` counted twice only enlarges the union bound ✓. Distances along `ℓ` are `|t−t'|` ✓. Bound 4 ✓ (sharp: 2, Obj. 1).
* *Figure 1* (norm-band.tex): `m = 1`, `z_0 = (0, 0.6)`, `C' = 0.36`, band `1 ≤ t²+0.36 < 2` ⇒ `t ∈ [0.8, √1.64)`; the drawn segments
  are `[±0.8, ±√1.64]` with solid inner and open outer endpoints ✓ (`√1.64 − 0.8 ≈ 0.48 ≤ 1`).

### Affine progressions and (6.3) perturb:signature — VERIFIED
"Affine" = `ỹ(n_j) = A + jB` for all `0 ≤ j < k` — word for word Theorem 5.5's alternative (ii). The signature is the literal word of
`(c_0(n_j), κ(n_j))`; keys are not renamed ✓ (Lean: `cyclicSignature`, events `targetEvent σ b` depend on `σ` only:
`targetEvent_eq_of_signature_eq`).

### Lemma 6.2 (perturb:signatures), (6.4), (6.5) — VERIFIED LINE BY LINE (Lemma 3.1 imported, SKIMMED)
* `f(n_j) = q²‖A+jB‖² = θ_0 + θ_1 j + θ_2 j²` with `θ_0 = q²‖A‖²`, `θ_1 = 2q²⟨A,B⟩`, `θ_2 = q²‖B‖²` — exact check, 48,910 instances, 0
  mismatches; controls (drop the 2 / `q` for `q²`) give 45,892 mismatches each.
* `0 ≤ f ≤ Dq²/4`: each `|qỹ_i| ≤ q/2` (`−1/2` attainable, so `≤`, not `<`) ✓. `B_* = ⌊Dq²/4⌋+1`; since `0 ≤ f < B_*`, the signs of
  `f − b`, `b = 0,…,B_*`, determine `⌊f⌋` (= #{b : f ≥ b} − 1) ✓ (checked exactly, 0 mismatches). `k(B_*+1) = k(⌊Dq²/4⌋+2) ≤ k(Dq²+2)`
  ✓. Each comparison `θ_0 + jθ_1 + j²θ_2 = b` is a genuine affine hyperplane in `R³` (coefficient of `θ_0` is 1) ✓; repeated
  hyperplanes are allowed by Lemma 3.1 anyway. Ignoring the Cauchy–Schwarz relation `θ_1² ≤ 4θ_0θ_2` only enlarges the count ✓
  (Lemma 3.1's "restricted to an arbitrary subset").
* Product with `T_glob`: the full-label word determines the V-boxes and (with `c_*` fixed) every `c_0(n_j)`; with the `⌊f⌋`-word it
  determines the signature. So the realized signatures are the image of a subset of
  (realized label words over ALL nonzero-step progressions) × (realized `⌊f⌋`-words over affine ones) ✓. No independence needed ✓.
* (6.5): `log T_aff ≤ log 128 + log T_glob + 3 log(k(Dq²+2))`; `Dq²+2 ≤ 3Dq²` ✓ (`Dq² ≥ 1`), giving
  `6 log q + 3 log k + 3 log D + O(1)` ✓. From (2.4) `log q ≤ (ck/D) log k + log(2k²) ≤ c k^{9/10} log k + log(2k²)` using
  `D ≥ k^{1/10}` ✓. `log T_glob = O(k^{3/10} log k)` imported from Lemma 3.2 (`D·log λ ≤ D·h_0 log(2M) = O(k^{3/10} log k)`) ✓.
  `pk = k^{19/20}`, ratio `k^{−1/20} log k → 0` ✓. All constants absolute; the dimension-3 arrangement constant does not grow with `D` ✓.

### Theorem 6.3 (perturb:cyclic), (6.6)–(6.9) — VERIFIED LINE BY LINE
* (6.6) `C(n) = c_0(n) + E_{κ(n)} mod 2`; `c_0` deterministic (all randomness of §4 resolved); `E_κ` i.i.d. Bernoulli(p) on the finite
  set `𝒦` ✓. Monochromatic in colour `b` ⟺ `E_{κ(n_j)} = b − c_0(n_j)` for all `j` ✓.
* *Rich case.* At least `γk` positions have `c_0 = 1−b` (Theorem 5.5(i) gives `≥ γk` of EACH bit); each needs `E = 1`; each key covers
  ≤ 4 positions (of either colour), so ≥ `γk/4` distinct keys must equal 1, a set fixed by `(progression, b)` before sampling;
  probability ≤ `p^{#keys} ≤ p^{γk/4}` since `p ≤ 1` ✓. A key carrying both outer colours forces contradictory values ⇒ empty event ⇒
  the bound holds a fortiori ✓ (Lean: `targetEvent_eq_empty_of_conflict`, `rich_target_probability_le` with exponent `⌈k/400⌉`).
  Union: `N(N−1) < N² = q^{2D}` pairs `(n_0, d)`, two colours ✓. (6.7): `log(2q^{2D}p^{γk/4}) = log 2 + 2D log q − (γ/80) k log k`, and
  `2D log q ≤ 2ck log k + 2D log(2k²)` by (2.4) ✓. (6.8) exact: `2·10^{−5} − (1/100)/80 = 1/50000 − 1/8000 = 4/200000 − 25/200000 =
  −21/200000` ✓ (Fraction-checked). Remainder `2D log(2k²) + log 2 = O(k^{1/10} log k) = o(k log k)` ✓.
* *Affine case.* Prescriptions `E_{κ_j} = b − c_j` ✓; inconsistent ⇒ empty ✓; consistent with `s` distinct keys, `u` of them prescribed 1:
  probability EXACTLY `p^u(1−p)^{s−u}` (independence) ✓ ≤ `(1−p)^s` needs `p ≤ 1−p`, i.e. `p ≤ 1/2` ✓ (Obj. 5);
  `s ≥ k/4` from multiplicity ✓; `(1−p)^s ≤ (1−p)^{k/4}` ✓; identical literal signatures ⇒ identical events on identical variables ⇒
  union over signatures, not progressions ✓; `1−p ≤ e^{−p}` ✓; (6.9) `A_k ≤ 2 max{1,T_aff} e^{−pk/4} = exp(−pk/4 + o(pk))` ✓.
* *Covering.* Theorem 5.5: every nonzero-step progression satisfies (i) [= rich] or (ii) [= affine]; overlap harmless ✓.
  `R_k + A_k = o(1) < 1` for large k ⇒ a good choice of bits exists ✓.
* *Threshold claim.* "All preceding thresholds and constants depend only on the fixed numerical parameters, and the bound in
  \Cref{setup:q-bounds} is uniform over every prime $P$ allowed by \Cref{setup:prime}." In §6 this is right: the only `P`-dependence
  enters through `q`, and only through `q ≤ 2k²k^{ck/D}`; every inequality is an explicit function of `k` tending to its limit, so
  "eventually" gives a single `K` beyond which ALL `k` work; none involves `r` or the progression. `N = q^D ≥ k^{ck}` from
  `q ≥ k^{ck/D}` ✓.

### Imported results (status as used here)
| Imported | Use in §6 | Status |
|---|---|---|
| Prop 4.2 outer:coloring | existence of `c_*` | statement only (outer seat) |
| Lemma 5.1 dichotomy:affinity | affine lift within a V-box | VERIFIED (proof re-read) |
| Theorem 5.5 dichotomy:main | rich-or-affine covering | statement matched word-for-word to §6's two cases; proof = dichotomy seat |
| Lemma 3.1 count:arrangement | `≤ 16(s+1)^3` at e = 3 | SKIMMED (counting seat); Lean uses a weaker bound (Obj. 4) |
| Lemma 3.2 count:global | `log T_glob = O(k^{3/10} log k)` | SKIMMED; arithmetic from `log λ ≤ h_0 log 2M` re-checked |
| Lemma 2.3 mesh:width | `|I| ≤ 2H` | SKIMMED (setup seat); `|I| ≤ 2H(ρ+α) ≤ 2H` re-checked |
| (2.4) setup:q-bounds | both bounds on `q` | VERIFIED (minimality of `q` among powers of `P ≤ 2k²`) |
| Lemma 2.2 setup:prime | `P > k` (distinct terms, `gcd(λ,q)=1`) | statement only (setup seat) |

## "Sufficiently large k" inequalities in §6 (brief item e)

| # | Inequality | Where | Needs | Holds |
|---|---|---|---|---|
| 1 | `2kH < 1` | Lemma 6.1 via Lemma 5.1 | `H = k^{−2}` | k ≥ 3 |
| 2 | `|I| ≤ 2H` | Lemma 6.1 | Lemma 2.3 (`α ≤ 1/4`, `R ≥ 1`, `θ ≤ 1`) | every k with `q ≥ 3` |
| 3 | distinct terms (`k < P`, Lean: `k ≤ P`) | Lemma 6.1, (6.2) | Lemma 2.2 | k ≥ threshold of Lemma 2.2 |
| 4 | `gcd(λ,q)=1` (`h_0 < P`) | (6.2) | `h_0 < k < P` | same |
| 5 | `B_*+1 ≤ Dq²+2`, `Dq²+2 ≤ 3Dq²` | Lemma 6.2 | — | always |
| 6 | `log q ≤ c k^{9/10} log k + log(2k²)` | (6.5) | `D ≥ k^{1/10}`, (2.4) | always |
| 7 | `log max{1,T_aff} = o(pk)` | (6.5), (6.9) | `k^{−1/20} log k → 0` | asymptotic; explicit (with Lemma 3.2's bound, C = 128): `log A_k ≤ −1.29×10^5` at k = 2^20, max −1.28×10^5 over 745 scanned k ∈ [2^20, 10^18] incl. every D-jump |
| 8 | `p ≤ 1/2` | affine case | `k^{−1/20} ≤ 1/2` | k ≥ 2^20 = 1,048,576 |
| 9 | `2c − γ/80 < 0` | (6.8) | — | absolute: −21/200000 |
| 10 | `R_k < 1/2` | (6.7) | 9 + `O(k^{1/10}log k)` remainder | from k ≈ 1.6×10^5; max `log R_k ≤ −1241` over the scan |
| 11 | `R_k + A_k < 1` | end of proof | 7, 8, 10 | all k ≥ 2^20 in the scan (asymptotically by the paper's o(1)) |

Every entry is a function of `k` alone: none depends on `r`, on the progression, or on which prime `P ∈ (k, 2k²]` was chosen. The
thresholds are finitely many. §6's own largest threshold is `k ≥ 2^20`; the paper's global `K_0` is set elsewhere (the LLL threshold of
§4 involving the unspecified absolute `C` of Lemma 3.4 is far larger) — not this seat's scope.

## Prove-too-much (brief item j)

The only place `c` enters §6 is the rich union bound: `N² = q^{2D} ≈ k^{2ck}` progressions against `p^{γk/4} = k^{−γk/80}`.
So the argument needs `2c < γ/80 = 1/8000`, i.e. `c < 1/16000`; the paper's `c = 10^{−5}` sits a factor 6.25 below the cap.
Within the architecture: `p = k^{−a}` needs `a < 1/10` for the affine case (`6 log q ≈ 6c k^{9/10} log k` must be `o(k^{1−a})`), and
`γ ≤ 1/10` (Theorem 5.5 delivers `k/10`), so `c < aγ/8 < 1/8000`; even with the sharp multiplicity 2 (Obj. 1) `c < 1/4000`. Nothing
here approaches `k^{k}`; the method genuinely caps `c`, at (6.8). Control: `thresholds.py control` with `c = 1/10000 > γ/160` makes
the rich bound blow up (`log R_k ≤ +1318` at k = 2^20) — the check rejects it.

## Citation table (§6)

| Cited | What §6 says it supplies | Source | Verdict |
|---|---|---|---|
| Behrend 1946, PNAS 32(12):331–332 (`behrend1946`) | "a bounded-width version of the equal-norm geometry in Behrend's construction" — attribution only; the band lemma is proved in full in §6 | tried `pnas.org` (stored copy in refs/ is a Cloudflare "Just a moment…" page), `pmc.ncbi.nlm.nih.gov/articles/PMC1078964/pdf/pnas01693-0039.pdf`, Europe PMC `?pdf=render` and `ptpmcrender.fcgi`: all bot-walled from this box; WebFetch of the PMC landing page returns metadata only (scanned pages) | COULD NOT FETCH. Not load-bearing: nothing in §6 depends on Behrend's paper. |
| Internal `\Cref`s (Prop 4.2, Lemma 5.1, (2.1), (2.7), (6.2), Lemma 3.2, Lemma 3.1, (2.4), Theorem 5.5, Lemma 2.2, Lemma 6.1, Lemma 6.2) | as listed above | the TeX of each | MATCH in content; rendered environment names wrong (Obj. 2) |

## Finite checks

All scripts are in `/tmp/oaimath/160/seats/perturbation_checks/`, run with system `python3` (numpy 2.4.4, mpmath 1.3.0), exact
`fractions.Fraction`/integer arithmetic wherever an identity or inequality is claimed (mpmath 50 digits only for the transcendental
adaptive-mesh endpoints, with the minimum point–endpoint gap printed). Each check has a control that FAILS.

### Check A — band length / key multiplicity on lines (exact rationals): `band_check.py`, `band_sweep.py`
Lines `z_0 + tB` with `B = s·e`, `e` a rational unit vector (inverse stereographic projection), `z_0 ⊥ e`, so `‖B‖ = s` is rational and
no square root is taken; `‖z_0‖²` steered to integers and integers ± 10^{−6} (adversarial band placement); 41 points per line with gaps
`SEP/s` (mostly exactly the minimum). The sweep is the 1-D reduction: points `δ + jg`, `δ ∈ g·{0,…,199}/200`, `C' ∈ {i/50, i/50+10^{−9}}`,
`i ≤ 400`. Claims tested: ≤ 2 per closed half-line and ≤ 4 per band (paper), ≤ 2 per band (Lean), `u ≤ t² ≤ v` containment.
Controls: `SEP = 99/100` must break the sharp bound; `SEP = 2/5` must break the paper's bound.

`band_check.py` (verbatim):
```python
#!/usr/bin/env python3
"""Exact check of the line/norm-band geometry in Lemma perturb:multiplicity.

Claim checked (06-perturbation.tex): points on an affine line, pairwise
Euclidean distance >= SEP (paper: SEP = 1), lying in one half-open band
m <= ||z||^2 < m+1, number at most two on each closed half-line from the
nearest point z_0, hence at most four in total.  We also record the
SHARPER count (at most one per half-open half-line, two in total), which is
what the Lean file KeyMultiplicity.lean actually proves
(affine_norm_band_card_le_two), and the band-interval containment
u <= t^2 <= v with u = max(0, m - C'), v = m + 1 - C'.

Everything is exact rational arithmetic: lines are A + t*B with B = s*e,
e a rational unit vector (inverse stereographic projection), so ||B|| = |s|
is rational and no square root is ever taken.

Usage: band_check.py SEP TRIALS SEED
"""
import sys, random
from fractions import Fraction as F
from math import floor

def rat_unit(D, rng):
    # inverse stereographic projection of a rational point of Q^{D-1}
    x = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(D - 1)]
    nx = F(0) + sum(v * v for v in x)
    e = [2 * v / (nx + 1) for v in x] + [(nx - 1) / (nx + 1)]
    assert sum(v * v for v in e) == 1
    return e

def dot(a, b): return sum(x * y for x, y in zip(a, b))

def trial(D, SEP, rng):
    e = rat_unit(D, rng)
    s = F(rng.randint(1, 40), rng.randint(1, 40))          # ||B|| = s
    B = [s * v for v in e]
    # nearest point z0 orthogonal to e, chosen so that C' = ||z0||^2 is often
    # an integer, or an integer +- a tiny epsilon (adversarial band placement)
    if D >= 2:
        w = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(D)]
        w = [wi - dot(w, e) * ei for wi, ei in zip(w, e)]   # project off e
        nw = dot(w, w)
        target = F(rng.choice([0, 1, 2, 3, 5, 10, 50])) + rng.choice(
            [F(0), F(1, 10**6), -F(1, 10**6), F(rng.randint(0, 99), 100)])
        if nw == 0 or target <= 0:
            z0 = [F(0)] * D
        else:
            # scale w by a rational r with r^2*nw close to target (exact when possible)
            r2 = target / nw
            r = F(round(float(r2) ** 0.5 * 10**6), 10**6)
            z0 = [r * wi for wi in w]
    else:
        z0 = [F(0)]
    # parameter t along B; point = z0 + t*B; separation |t-t'|*s >= SEP
    gap = SEP / s
    t0 = F(rng.randint(-50, 50), rng.randint(1, 50)) * gap     # random offset
    pts = []
    t = t0 - 20 * gap
    for _ in range(41):
        pts.append(t)
        t += gap * rng.choice([1, 1, 1, 1, F(101, 100), F(3, 2), 2])
    # nearest-point parameter is t* = 0 here because z0 is orthogonal to B
    return z0, B, s, pts

def main():
    SEP = F(sys.argv[1]); TRIALS = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    worst_total = worst_half_closed = worst_half_open = 0
    contain_fail = 0
    for it in range(TRIALS):
        D = rng.choice([1, 2, 3, 4])
        z0, B, s, ts = trial(D, SEP, rng)
        Cp = dot(z0, z0)
        bands = {}
        for t in ts:
            P = [a + t * b for a, b in zip(z0, B)]
            f = dot(P, P)
            # identity ||z0 + t B||^2 = (t s)^2 + C'  (z0 orthogonal to B)
            assert f == (t * s) ** 2 + Cp
            bands.setdefault(floor(f), []).append(t * s)   # arclength param
        for m, T in bands.items():
            u = max(F(0), m - Cp); v = m + 1 - Cp
            assert v > 0
            for tt in T:                                  # containment, exact
                if not (u <= tt * tt <= v):
                    contain_fail += 1
            pos = [tt for tt in T if tt >= 0]; neg = [tt for tt in T if tt <= 0]
            worst_total = max(worst_total, len(T))
            worst_half_closed = max(worst_half_closed, len(pos), len(neg))
            worst_half_open = max(worst_half_open, len([tt for tt in T if tt > 0]),
                                  len([tt for tt in T if tt < 0]))
    print(f"SEP={SEP} trials={TRIALS}: max per band={worst_total}, "
          f"max per closed half-line={worst_half_closed}, max per open half-line={worst_half_open}, "
          f"containment failures={contain_fail}")
    ok_paper = worst_total <= 4 and worst_half_closed <= 2 and contain_fail == 0
    ok_sharp = worst_total <= 2
    print("paper claim (<=2 per half, <=4 per band):", "HOLDS" if ok_paper else "REJECTED")
    print("sharp claim (<=2 per band, Lean affine_norm_band_card_le_two):", "HOLDS" if ok_sharp else "REJECTED")
    sys.exit(0 if ok_paper else 1)

main()
```

`band_sweep.py` (verbatim):
```python
#!/usr/bin/env python3
"""Deterministic adversarial sweep (1-D reduction of perturb:multiplicity).
Points t = delta + j*g (j integer), band m <= t^2 + C' < m+1, exact rationals.
g = separation (paper: 1). Report the largest band population.
Usage: band_sweep.py G"""
import sys
from fractions import Fraction as F
from math import floor
g = F(sys.argv[1]); worst = 0; arg = None
for di in range(0, 200):                     # delta in [0, g)
    delta = g * F(di, 200)
    for ci in range(0, 401):                 # C' in [0, 8] step 1/50, plus integer +- tiny
        for Cp in (F(ci, 50), F(ci, 50) + F(1, 10**9)):
            pop = {}
            for j in range(-12, 13):
                t = delta + j * g
                m = floor(t * t + Cp)
                pop[m] = pop.get(m, 0) + 1
            b = max(pop.values())
            if b > worst: worst, arg = b, (delta, Cp)
print(f"g={g}: largest band population {worst} at (delta, C')={arg}")
sys.exit(0 if worst <= 4 else 1)
```

Output:
```
$ python3 band_check.py 1 4000 7
SEP=1 trials=4000: max per band=2, max per closed half-line=1, max per open half-line=1, containment failures=0
paper claim (<=2 per half, <=4 per band): HOLDS
sharp claim (<=2 per band, Lean affine_norm_band_card_le_two): HOLDS
exit=0
$ python3 band_check.py 99/100 4000 7   # control: separation < 1
SEP=99/100 trials=4000: max per band=3, max per closed half-line=2, max per open half-line=2, containment failures=0
paper claim (<=2 per half, <=4 per band): HOLDS
sharp claim (<=2 per band, Lean affine_norm_band_card_le_two): REJECTED
exit=0
$ python3 band_check.py 2/5 4000 7      # control: separation 0.4
SEP=2/5 trials=4000: max per band=5, max per closed half-line=3, max per open half-line=3, containment failures=0
paper claim (<=2 per half, <=4 per band): REJECTED
sharp claim (<=2 per band, Lean affine_norm_band_card_le_two): REJECTED
exit=1
$ python3 band_sweep.py 1
g=1: largest band population 2 at (delta, C')=(Fraction(0, 1), Fraction(0, 1))
exit=0
$ python3 band_sweep.py 99/100   # control
g=99/100: largest band population 3 at (delta, C')=(Fraction(0, 1), Fraction(0, 1))
exit=0
$ python3 band_sweep.py 2/5      # control
g=2/5: largest band population 6 at (delta, C')=(Fraction(24, 125), Fraction(49, 50))
exit=1
```
Reading: with separation 1 the paper's bound holds and the observed maximum is 2 per band and 1 per closed half-line — the sharp
bound (Obj. 1). Controls fail as they must: separation 0.99 gives 3 in a band (`t = 0, ±0.99`, `C' = 0`), separation 0.4 gives 5–6.
Containment `u ≤ t² ≤ v` held at every point (0 failures).

### Check B — the quadratic identity and floor recovery (exact): `quadratic_identity.py`
Random `A, B ∈ Q^D` (D ≤ 6) with every coordinate of `A + jB` in `[−1/2, 1/2)` for `0 ≤ j < k`, random `q ≤ 40`, `k ≤ 30`. Asserts
`0 ≤ f ≤ Dq²/4`, tests `q²‖A+jB‖² = θ_0 + θ_1 j + θ_2 j²` exactly, and recovers `⌊f⌋` from the sign vector against `b = 0,…,B_*`.
Controls: `control_no2` (θ_1 without the factor 2), `control_scale` (θ_2 with `q` for `q²`).
```python
#!/usr/bin/env python3
"""Exact check of the identity in Lemma perturb:signatures:
  f(n_j) = q^2 ||A + jB||^2 = theta0 + theta1 j + theta2 j^2,
  theta0 = q^2||A||^2, theta1 = 2 q^2 <A,B>, theta2 = q^2 ||B||^2,
and that the signs of (theta0+theta1 j+theta2 j^2 - b), b = 0..B_*, recover
floor(f(n_j)) whenever 0 <= f <= D q^2/4 (B_* = floor(D q^2/4) + 1).
Usage: quadratic_identity.py MODE TRIALS SEED   (MODE = paper | control_no2 | control_scale)"""
import sys, random
from fractions import Fraction as F
from math import floor
mode, TRIALS, rng = sys.argv[1], int(sys.argv[2]), random.Random(int(sys.argv[3]))
bad = 0; floor_bad = 0; checked = 0
for _ in range(TRIALS):
    D = rng.randint(1, 6); q = rng.randint(2, 40); k = rng.randint(2, 30)
    # random affine data with every coordinate of A + jB inside [-1/2, 1/2)
    A = [F(rng.randint(-499, 499), 1000) for _ in range(D)]
    B = [F(rng.randint(-999, 999), 10**6 * k) for _ in range(D)]
    if any(not (-F(1, 2) <= a + j * b < F(1, 2)) for a, b in zip(A, B) for j in range(k)):
        continue
    nA = sum(a * a for a in A); nB = sum(b * b for b in B); AB = sum(a * b for a, b in zip(A, B))
    th0, th1, th2 = q * q * nA, 2 * q * q * AB, q * q * nB
    if mode == "control_no2": th1 = q * q * AB          # deliberately wrong: drop the 2
    if mode == "control_scale": th2 = q * nB            # deliberately wrong: q not q^2
    Bstar = floor(F(D * q * q, 4)) + 1
    for j in range(k):
        f = q * q * sum((a + j * b) ** 2 for a, b in zip(A, B))
        checked += 1
        assert 0 <= f <= F(D * q * q, 4)
        g = th0 + th1 * j + th2 * j * j
        if f != g: bad += 1
        # signs against b = 0..B_* ; floor recovered as (#b with g >= b) - 1
        signs = [(g > b) - (g < b) for b in range(Bstar + 1)]
        rec = sum(1 for sgn in signs if sgn >= 0) - 1
        if rec != floor(f): floor_bad += 1
print(f"mode={mode}: {checked} (j, data) instances, identity mismatches={bad}, floor-recovery mismatches={floor_bad}")
sys.exit(0 if bad == 0 and floor_bad == 0 else 1)
```
Output:
```
$ python3 quadratic_identity.py paper 3000 11
mode=paper: 48910 (j, data) instances, identity mismatches=0, floor-recovery mismatches=0
exit=0
$ python3 quadratic_identity.py control_no2 3000 11
mode=control_no2: 48910 (j, data) instances, identity mismatches=45892, floor-recovery mismatches=3106
exit=1
$ python3 quadratic_identity.py control_scale 3000 11
mode=control_scale: 48910 (j, data) instances, identity mismatches=45892, floor-recovery mismatches=19
exit=1
```

### Check C — the actual cyclic model: separation (6.2) over ALL pairs, key multiplicity over ALL progressions: `cyclic_keys.py`
`literal`: the paper's own parameters at `k = 10` — `D = ⌈10^{1/10}⌉ = 2`, `M = 4`, `h_0 = 4 < 2M = 8 < k`, `λ = 2^3·3 = 24` computed
from (setup:dilation-definition), `P ∈ {11, 13} ⊂ (10, 200]`, `q` = least power of `P` ≥ `k^{ck/D}` (= `P`), `H = 1/k²`,
`α = q^{−3}`, adaptive mesh exactly as (mesh:definition)–(mesh:intervals). This is literal but NOT stressful: every key holds one element
of `G` (boxes of width ≤ 2H(ρ+α) are far finer than the `1/q^i` grid at this size) — reported for completeness.
`stress`/`stress_adaptive`: the lemma's hypotheses kept (box widths ≤ 2H with `2kH = 0.98 < 1`, `λ` a unit mod `q^D`, `P > k`) but boxes
as WIDE as allowed and `q = 7²` a prime power, so whole progressions fit in one box (the `ctl_noband` run shows 3,528 progressions with
all 6 terms in one box) and only the norm band limits multiplicity. Every one of the 5,762,400 progressions of `Z/2401` is checked, and
all 5,762,400 ordered pairs for (6.2), in integer arithmetic.
Controls: `ctl_noband` (key = box only) and `ctl_nonunit` (`λ = P`, not a unit) must FAIL; `ctl_widebox` (one interval of width 1,
violating `|I| ≤ 2H` and `2kH < 1`) is reported as a probe of the box hypothesis.
```python
#!/usr/bin/env python3
"""Cyclic-model check of Lemma perturb:multiplicity and (perturb:separation).

G = Z/q^D, y_i(n) = lambda*n/q^i mod 1, centered representative
ytilde_i(n) in [-1/2,1/2) (exact rational r'/q^i), key(n) = (V-box of ytilde(n),
floor(||q ytilde(n)||^2)).  For every progression n0 + j d (d != 0, 0<=j<k)
we compute the largest multiplicity of a key, and for every pair n != n' we
check ||q ytilde(n) - q ytilde(n')||^2 >= 1 exactly (integer arithmetic).

MODE literal : the paper's literal parameters at k = 10 (D = 2, M = 4,
               h_0 = 4, lambda = 24, P prime in (10,200], q = P, H = 1/k^2,
               adaptive mesh (mesh:definition) with alpha = q^-(D+1)).
MODE stress  : hypotheses of the lemma kept (box widths <= 2H, 2kH < 1,
               lambda a unit mod q^D, P > k) but boxes made as WIDE as allowed
               (uniform mesh of width 1/ceil(1/(2H)) <= 2H, H = 0.49/k), q a higher prime
               power, so boxes contain whole progressions and only the norm
               band limits multiplicity.
MODE stress_adaptive : as stress but with the paper's adaptive mesh formula
               (geometric toward the cut) at scale H = 0.49/k.
Controls (must FAIL): ctl_nonunit (lambda = P, not a unit mod q^D),
               ctl_noband (key = box only), ctl_widebox (one interval, 2kH>=1).
Usage: cyclic_keys.py MODE k P e D
"""
import sys, math
import numpy as np
from fractions import Fraction as F
import mpmath
mpmath.mp.dps = 50

MODE = sys.argv[1]; k = int(sys.argv[2]); P = int(sys.argv[3]); e = int(sys.argv[4]); D = int(sys.argv[5])
q = P ** e; N = q ** D
assert all(P % r for r in range(2, int(P ** 0.5) + 1)) and P > k, "need prime P > k"

def paper_lambda(k, D):
    M = next(M for M in range(1, k + 1) if M * M >= k)
    h0 = D * D
    lam = 1
    for l in range(2, h0 + 1):
        if all(l % r for r in range(2, int(l ** 0.5) + 1)):
            a = 0
            while l ** (a + 1) <= 2 * M: a += 1      # = floor(log(2M)/log l)
            lam *= l ** a
    return lam, M, h0

if MODE == "literal":
    Dk = next(d for d in range(1, 100) if d ** 10 >= k)
    assert Dk == D, f"literal mode needs D = ceil(k^(1/10)) = {Dk}"
    lam, M, h0 = paper_lambda(k, D)
    assert h0 < 2 * M < k, (h0, M, k)
    # q = least power of P that is >= k^{ck/D}, c = 1e-5
    target = mpmath.power(k, mpmath.mpf(1) / 100000 * k / D)
    qq = 1
    while qq < target: qq *= P
    assert qq == q, f"literal q should be {qq}"
    H = F(1, k * k)
elif MODE == "ctl_nonunit":
    lam, H = P, F(49, 100 * k)
else:
    lam, H = 24, F(49, 100 * k)
assert math.gcd(lam, q) == 1 or MODE == "ctl_nonunit"
print(f"MODE={MODE} k={k} P={P} q={q} D={D} N={N} lambda={lam} H={H} 2kH={float(2*k*H):.3f}")

# centered numerators r'_i(n): ytilde_i(n) = r'_i(n) / q^i
n = np.arange(N, dtype=np.int64)
R = np.zeros((N, D), dtype=np.int64)
for i in range(1, D + 1):
    Q = q ** i
    r = (lam * n) % Q
    R[:, i - 1] = np.where(2 * r >= Q, r - Q, r)          # [-1/2,1/2): r/Q >= 1/2 -> subtract 1
# f(n) = ||q ytilde||^2 = sum_i r'_i^2 / q^{2(i-1)}; floor exactly via common denominator
den = q ** (2 * (D - 1))
num = sum((R[:, i - 1].astype(object) ** 2) * q ** (2 * (D - i)) for i in range(1, D + 1))
fl = np.array([x // den for x in num], dtype=np.int64)
assert all(0 <= x <= F(D * q * q, 4) * den for x in num), "0 <= f <= D q^2/4 violated"

# V labels
def adaptive_endpoints(Hs):
    alpha = mpmath.mpf(1) / mpmath.mpf(q) ** (D + 1)
    Rr = mpmath.log(1 + 1 / (2 * alpha))
    m = int(mpmath.ceil(Rr / Hs))                         # literal: m = ceil(k^2 R) when Hs = 1/k^2
    a = [alpha * (mpmath.e ** (l * Rr / m) - 1) for l in range(m + 1)]
    a[0] = mpmath.mpf(0); a[m] = mpmath.mpf(1) / 2          # exact by construction
    return a, m

if MODE in ("literal", "stress_adaptive"):
    a, m = adaptive_endpoints(mpmath.mpf(H.numerator) / H.denominator)
    widths = [a[l + 1] - a[l] for l in range(m)]
    assert max(widths) <= 2 * mpmath.mpf(H.numerator) / H.denominator, "mesh:width |I| <= 2H fails"
    lab = np.zeros((N, D), dtype=np.int64); margin = mpmath.mpf(1)
    import bisect
    af = a
    for idx in range(N):
        for i in range(D):
            Q = q ** (i + 1); y = mpmath.mpf(int(R[idx, i])) / Q
            if y < 0:                      # left family: x = y + 1/2 in [a_l, a_{l+1})
                x = y + mpmath.mpf(1) / 2
                l = bisect.bisect_right(af, x) - 1
                lab[idx, i] = l
            else:                          # right family: [1/2 - a_{l+1}, 1/2 - a_l), x' = 1/2 - y in (a_l, a_{l+1}]
                x = mpmath.mpf(1) / 2 - y
                l = bisect.bisect_left(af, x) - 1
                lab[idx, i] = m + l
            for ep in (af[max(l, 0)], af[min(l + 1, m)]):
                d_ = abs(ep - x)
                if d_ > 0: margin = min(margin, d_)
    print(f"adaptive mesh: m={m} intervals per family, max width={float(max(widths)):.3e} <= 2H={float(2*H):.3e}, "
          f"min nonzero point-endpoint gap={mpmath.nstr(margin, 5)}")
elif MODE in ("stress", "ctl_nonunit", "ctl_noband"):
    Wden = math.ceil(1 / (2 * H)); W = F(1, Wden); assert W <= 2 * H
    print(f"uniform mesh: {Wden} intervals of width {W} <= 2H")
    # interval index floor((y + 1/2)/W), exact
    lab = np.zeros((N, D), dtype=np.int64)
    for i in range(D):
        Q = q ** (i + 1)
        lab[:, i] = ((2 * R[:, i] + Q) * Wden) // (2 * Q)
elif MODE == "ctl_widebox":
    lab = np.zeros((N, D), dtype=np.int64)      # one interval [-1/2,1/2): width 1 > 2H, 2kH >= 1
else:
    raise SystemExit("bad mode")

keys = {}
kid = np.zeros(N, dtype=np.int64)
for idx in range(N):
    t = tuple(lab[idx]) + ((int(fl[idx]),) if MODE != "ctl_noband" else ())
    kid[idx] = keys.setdefault(t, len(keys))
print(f"distinct keys={len(keys)}, max elements of G per key={np.bincount(kid).max()}")

# separation over all pairs n != n' (exact integers)
sep_fail = 0
w = np.array([q ** (2 * (D - i)) for i in range(1, D + 1)], dtype=object)
Ri = R.astype(np.int64)
for s0 in range(0, N, 256):
    blk = Ri[s0:s0 + 256]
    diff = blk[:, None, :] - Ri[None, :, :]                  # (b, N, D)
    acc = np.zeros(diff.shape[:2], dtype=np.float64)
    tot = np.zeros(diff.shape[:2], dtype=object) if q ** (2 * D) > 2 ** 52 else None
    if tot is None:
        val = sum((diff[:, :, i - 1].astype(np.int64) ** 2) * int(q ** (2 * (D - i))) for i in range(1, D + 1))
        bad = (val < q ** (2 * (D - 1)))
    else:
        val = sum((diff[:, :, i - 1].astype(object) ** 2) * q ** (2 * (D - i)) for i in range(1, D + 1))
        bad = (val < q ** (2 * (D - 1)))
    for b in range(bad.shape[0]):
        bad[b, s0 + b] = False                              # skip n == n'
    sep_fail += int(np.count_nonzero(bad))
print(f"separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all {N*(N-1)} ordered pairs: failures={sep_fail}")

# key multiplicity over every progression (n0, d), d != 0
J = np.arange(k, dtype=np.int64)
dist = np.zeros(k + 1, dtype=np.int64)
worst = 0; witness = None
d_all = np.arange(1, N, dtype=np.int64)
for s0 in range(0, N, 64):
    n0 = np.arange(s0, min(N, s0 + 64), dtype=np.int64)
    idx = (n0[:, None, None] + J[None, None, :] * d_all[None, :, None]) % N
    kk = kid[idx]                                             # (b, N-1, k)
    eq = (kk[:, :, :, None] == kk[:, :, None, :]).sum(axis=3) # multiplicity of each position's key
    mx = eq.max(axis=2)
    dist += np.bincount(mx.ravel(), minlength=k + 1)
    if mx.max() > worst:
        worst = int(mx.max()); b, dd = np.argwhere(mx == worst)[0]
        witness = (int(n0[b]), int(d_all[dd]))
print(f"progressions checked={int(dist.sum())}; max key multiplicity={worst} (witness n0,d={witness}); "
      f"distribution of per-progression max: { {i:int(c) for i,c in enumerate(dist) if c} }")
ok = worst <= 4 and sep_fail == 0
print("Lemma perturb:multiplicity (<=4) and (perturb:separation):", "HOLD" if ok else "FAIL")
sys.exit(0 if ok else 1)
```
Output:
```
$ python3 cyclic_keys.py literal 10 11 1 2
MODE=literal k=10 P=11 q=11 D=2 N=121 lambda=24 H=1/100 2kH=0.200
adaptive mesh: m=651 intervals per family, max width=4.976e-03 <= 2H=2.000e-02, min nonzero point-endpoint gap=1.6513e-5
distinct keys=121, max elements of G per key=1
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 14520 ordered pairs: failures=0
progressions checked=14520; max key multiplicity=1 (witness n0,d=(0, 1)); distribution of per-progression max: {1: 14520}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[0.30s, 36100KB]
exit=0
$ python3 cyclic_keys.py literal 10 13 1 2
MODE=literal k=10 P=13 q=13 D=2 N=169 lambda=24 H=1/100 2kH=0.200
adaptive mesh: m=701 intervals per family, max width=4.974e-03 <= 2H=2.000e-02, min nonzero point-endpoint gap=6.6408e-6
distinct keys=169, max elements of G per key=1
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 28392 ordered pairs: failures=0
progressions checked=28392; max key multiplicity=1 (witness n0,d=(0, 1)); distribution of per-progression max: {1: 28392}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[0.33s, 38496KB]
exit=0
$ python3 cyclic_keys.py stress 6 7 2 2
MODE=stress k=6 P=7 q=49 D=2 N=2401 lambda=24 H=49/600 2kH=0.980
uniform mesh: 7 intervals of width 1/7 <= 2H
distinct keys=1947, max elements of G per key=8
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 5762400 ordered pairs: failures=0
progressions checked=5762400; max key multiplicity=2 (witness n0,d=(1, 49)); distribution of per-progression max: {1: 5747328, 2: 15072}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[2.57s, 87424KB]
exit=0
$ python3 cyclic_keys.py stress_adaptive 6 7 2 2
MODE=stress_adaptive k=6 P=7 q=49 D=2 N=2401 lambda=24 H=49/600 2kH=0.980
adaptive mesh: m=135 intervals per family, max width=3.907e-02 <= 2H=1.633e-01, min nonzero point-endpoint gap=4.9574e-7
distinct keys=2366, max elements of G per key=2
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 5762400 ordered pairs: failures=0
progressions checked=5762400; max key multiplicity=2 (witness n0,d=(1, 2351)); distribution of per-progression max: {1: 5761350, 2: 1050}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[3.00s, 87076KB]
exit=0
$ python3 cyclic_keys.py stress 4 5 2 2
MODE=stress k=4 P=5 q=25 D=2 N=625 lambda=24 H=49/400 2kH=0.980
uniform mesh: 5 intervals of width 1/5 <= 2H
distinct keys=469, max elements of G per key=8
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 390000 ordered pairs: failures=0
progressions checked=390000; max key multiplicity=2 (witness n0,d=(1, 8)); distribution of per-progression max: {1: 387768, 2: 2232}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[0.37s, 42576KB]
exit=0
$ python3 cyclic_keys.py stress 6 7 1 3
MODE=stress k=6 P=7 q=7 D=3 N=343 lambda=24 H=49/600 2kH=0.980
uniform mesh: 7 intervals of width 1/7 <= 2H
distinct keys=343, max elements of G per key=1
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 117306 ordered pairs: failures=0
progressions checked=117306; max key multiplicity=1 (witness n0,d=(0, 1)); distribution of per-progression max: {1: 117306}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[0.32s, 41252KB]
exit=0
$ python3 cyclic_keys.py stress 10 11 1 3
MODE=stress k=10 P=11 q=11 D=3 N=1331 lambda=24 H=49/1000 2kH=0.980
uniform mesh: 11 intervals of width 1/11 <= 2H
distinct keys=1331, max elements of G per key=1
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 1770230 ordered pairs: failures=0
progressions checked=1770230; max key multiplicity=1 (witness n0,d=(0, 1)); distribution of per-progression max: {1: 1770230}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[1.52s, 80892KB]
exit=0
$ python3 cyclic_keys.py ctl_noband 6 7 2 2
MODE=ctl_noband k=6 P=7 q=49 D=2 N=2401 lambda=24 H=49/600 2kH=0.980
uniform mesh: 7 intervals of width 1/7 <= 2H
distinct keys=49, max elements of G per key=49
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 5762400 ordered pairs: failures=0
progressions checked=5762400; max key multiplicity=6 (witness n0,d=(1, 100)); distribution of per-progression max: {1: 4822776, 2: 833784, 3: 82320, 4: 15288, 5: 4704, 6: 3528}
Lemma perturb:multiplicity (<=4) and (perturb:separation): FAIL
Command exited with non-zero status 1
[2.87s, 86752KB]
exit=1
$ python3 cyclic_keys.py ctl_nonunit 6 7 2 2
MODE=ctl_nonunit k=6 P=7 q=49 D=2 N=2401 lambda=7 H=49/600 2kH=0.980
uniform mesh: 7 intervals of width 1/7 <= 2H
distinct keys=332, max elements of G per key=14
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 5762400 ordered pairs: failures=14406
progressions checked=5762400; max key multiplicity=6 (witness n0,d=(0, 343)); distribution of per-progression max: {1: 5732902, 2: 15092, 6: 14406}
Lemma perturb:multiplicity (<=4) and (perturb:separation): FAIL
Command exited with non-zero status 1
[2.44s, 86716KB]
exit=1
$ python3 cyclic_keys.py ctl_widebox 6 7 2 2
MODE=ctl_widebox k=6 P=7 q=49 D=2 N=2401 lambda=24 H=49/600 2kH=0.980
distinct keys=495, max elements of G per key=16
separation ||q ytilde(n) - q ytilde(n')|| >= 1 over all 5762400 ordered pairs: failures=0
progressions checked=5762400; max key multiplicity=4 (witness n0,d=(1, 2351)); distribution of per-progression max: {1: 5606044, 2: 155718, 3: 604, 4: 34}
Lemma perturb:multiplicity (<=4) and (perturb:separation): HOLD
[2.63s, 86684KB]
exit=0
```
Reading: (6.2) holds with 0 failures over every pair in every model with `λ` a unit; with `λ = P` it fails on 14,406 pairs and a key
then occurs 6 times (all terms of `d = 343` coincide). Key multiplicity never exceeds 2 when the hypotheses hold (paper: ≤ 4); dropping
the norm band gives 6. Dropping the box hypothesis (`ctl_widebox`) gives multiplicities 3 and 4 (34 progressions at 4): it does not
break the paper's 4 at `k = 6`, but it does break the sharp 2 that holds with the box — i.e. the affinity-in-a-box step is load-bearing.
The `stress 6 7 1 3` and `stress 10 11 1 3` runs are non-stressful (one element per key) and are listed only because they ran.

### Check D — arithmetic and explicit thresholds: `thresholds.py`
Exact `2c − γ/80`; `p = 1/2` at `k = 2^20`; the (6.7) exponent, and an explicit (6.9) bound built from Lemma 3.2's
`T_glob ≤ [9(3k²F+1)²]^{2D}` (`F = k²λ + 2m`, `λ` computed exactly, worst admissible `q`), `C = 128`, over 745 values of
`k ∈ [2^20, 10^18]` including `j^{10}, j^{10}+1, j^{10}+2` (where `D` jumps and the `2D log(2k²)` term is worst).
Control: `c = 1/10000 > γ/160` must make the rich bound fail.
```python
#!/usr/bin/env python3
"""Arithmetic of Theorem perturb:cyclic and the 'sufficiently large k'
inequalities of Section 6, evaluated with the paper's literal parameters.

(1) exact: 2c - gamma/80 with c = 1e-5, gamma = 1/100  (perturb:negative-coefficient)
(2) p = k^(-1/20) < 1/2                       iff k > 2^20
(3) R_k bound  log R_k <= (2c-g/80) k log k + 2D log(2k^2) + log 2   (perturb:rich-bound)
(4) A_k bound  log A_k <= log 2 + log C_arr + log T_glob + 3 log(k(Dq^2+2)) - pk/4
    with C_arr = 128 (count:arrangement, e=3: 16(s+1)^3 <= 128 s^3),
    T_glob <= [9(3k^2F+1)^2]^{2D}, F = k^2 lambda + 2m (count:global),
    m = ceil(k^2 R), R = log(1 + q^{D+1}/2), and the WORST admissible q,
    log q <= (ck/D) log k + log(2k^2)        (setup:q-bounds)
All logs natural; lambda computed exactly (as a log).
Usage: thresholds.py [control]   ('control' sets c = 1/10000 > gamma/160: rich bound must fail)"""
import sys, math
from fractions import Fraction as Fr
c = Fr(1, 100000); g = Fr(1, 100)
if len(sys.argv) > 1 and sys.argv[1] == "control": c = Fr(1, 10000)
coef = 2 * c - g / 80
print("2c - gamma/80 =", coef, "  (1/50000 - 1/8000 =", Fr(1, 50000) - Fr(1, 8000), ")")
def iroot_ceil(k, r):
    x = max(1, int(round(k ** (1.0 / r))) - 2)
    while x ** r < k: x += 1
    while x > 1 and (x - 1) ** r >= k: x -= 1
    return x
def primes_upto(n):
    return [l for l in range(2, n + 1) if all(l % r for r in range(2, int(l ** 0.5) + 1))]
def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D * D
    loglam = 0.0
    for l in primes_upto(h0):
        a = 0
        while l ** (a + 1) <= 2 * M: a += 1
        loglam += a * math.log(l)
    return D, M, h0, loglam
def logR(k):
    D, M, h0, _ = params(k); L = math.log(k)
    return float(coef) * k * L + 2 * D * math.log(2 * k * k) + math.log(2)
def logA(k):
    D, M, h0, loglam = params(k); L = math.log(k)
    logq = float(c) * k / D * L + math.log(2 * k * k)          # worst admissible q
    R = (D + 1) * logq                                         # log(1+q^{D+1}/2) <= (D+1) log q
    logm = 2 * L + math.log(R + 1)                              # m <= k^2 R + 1
    logF = max(2 * L + loglam, logm + math.log(2)) + math.log(2)  # F <= 2 max(k^2 lambda, 2m)
    logTg = 2 * D * (math.log(9) + 2 * (math.log(3) + 2 * L + logF + 1e-9) + math.log(2))
    p = k ** (-1 / 20)
    return math.log(2) + math.log(128) + logTg + 3 * (L + math.log(3) + math.log(D) + 2 * logq) - p * k / 4
print("p < 1/2 iff k > 2^20 =", 2 ** 20, "; check p(2^20) =", (2 ** 20) ** (-1 / 20))
# scan: every D-jump point j^10+1 and a geometric grid, from 2^20 to 1e18
pts = set()
for j in range(4, 64):
    for kk in (j ** 10, j ** 10 + 1, j ** 10 + 2):
        if 2 ** 20 <= kk <= 10 ** 18: pts.add(kk)
x = 2.0 ** 20
while x <= 1e18: pts.add(int(x)); x *= 1.05
pts = sorted(pts)
worstR = max(logR(k) for k in pts); worstA = max(logA(k) for k in pts)
print(f"scanned {len(pts)} values of k in [2^20, 1e18]: max log R_k bound = {worstR:.1f}, max log A_k bound = {worstA:.1f} "
      f"(need both < log(1/2) = {math.log(0.5):.3f})")
for k in (2 ** 20, 10 ** 7, 10 ** 9, 10 ** 12):
    print(f"  k={k:>14}: D,M,h0={params(k)[:3]}, log lambda={params(k)[3]:.1f}, logR<={logR(k):.4g}, logA<={logA(k):.4g}")
# where does the rich bound first go below log(1/2)? (smallest k on a fine scan)
k = 2
while logR(k) >= math.log(0.5) and k < 10 ** 12: k = int(k * 1.01) + 1
print("rich bound < 1/2 from about k =", k if k < 10 ** 12 else "never below 1e12")
ok = worstR < math.log(0.5) and worstA < math.log(0.5)
print("Section-6 union bounds R_k + A_k < 1 on the whole scanned range:", "YES" if ok else "NO")
sys.exit(0 if ok else 1)
```
Output:
```
$ python3 thresholds.py
2c - gamma/80 = -21/200000   (1/50000 - 1/8000 = -21/200000 )
p < 1/2 iff k > 2^20 = 1048576 ; check p(2^20) = 0.5
scanned 745 values of k in [2^20, 1e18]: max log R_k bound = -1241.4, max log A_k bound = -128365.3 (need both < log(1/2) = -0.693)
  k=       1048576: D,M,h0=(4, 1024, 16), log lambda=38.8, logR<=-1298, logA<=-1.291e+05
  k=      10000000: D,M,h0=(6, 3163, 36), log lambda=81.0, logR<=-1.653e+04, logA<=-1.111e+06
  k=    1000000000: D,M,h0=(8, 31623, 64), log lambda=165.6, logR<=-2.175e+06, logA<=-8.854e+07
  k= 1000000000000: D,M,h0=(16, 1000000, 256), log lambda=646.0, logR<=-2.901e+09, logA<=-6.269e+10
rich bound < 1/2 from about k = 159151
Section-6 union bounds R_k + A_k < 1 on the whole scanned range: YES
exit=0
$ python3 thresholds.py control   # c = 1/10000 > gamma/160
2c - gamma/80 = 3/40000   (1/50000 - 1/8000 = -21/200000 )
p < 1/2 iff k > 2^20 = 1048576 ; check p(2^20) = 0.5
scanned 745 values of k in [2^20, 1e18]: max log R_k bound = 3060524171538492.5, max log A_k bound = -126795.4 (need both < log(1/2) = -0.693)
  k=       1048576: D,M,h0=(4, 1024, 16), log lambda=38.8, logR<=1318, logA<=-1.271e+05
  k=      10000000: D,M,h0=(6, 3163, 36), log lambda=81.0, logR<=1.248e+04, logA<=-1.097e+06
  k=    1000000000: D,M,h0=(8, 31623, 64), log lambda=165.6, logR<=1.555e+06, logA<=-8.714e+07
  k= 1000000000000: D,M,h0=(16, 1000000, 256), log lambda=646.0, logR<=2.072e+09, logA<=-6.176e+10
rich bound < 1/2 from about k = never below 1e12
Section-6 union bounds R_k + A_k < 1 on the whole scanned range: NO
exit=1
```
Reading: (6.8) is exactly −21/200000. With the paper's constants both union bounds are below 1/2 on the whole scanned range from
`k = 2^20` (where `p ≤ 1/2` starts); the rich bound alone is below 1/2 from `k ≈ 1.6×10^5`. With `c = 10^{−4}` the rich bound is
`e^{+1318}` at `k = 2^20` and grows — the check rejects it, confirming (6.8) is the binding inequality. (The scan is a sanity check of
explicit inequalities, not a proof for all k; the "for all large k" statement rests on the paper's asymptotics, which I re-derived, and is
also what the Lean's `richEnvelope_tendsto` / `affineEnvelope_tendsto` formalize.)

## Coverage ledger (the deliverable)

| Item (TeX label · printed number · page) | Status |
|---|---|
| §6 preamble (randomness of §4 resolved; keys finite) · p. 16 | VERIFIED LINE BY LINE |
| (perturb:keys) · (6.1) · p. 16 | VERIFIED LINE BY LINE |
| Lemma perturb:multiplicity · Lemma 6.1 · pp. 16–17 | VERIFIED LINE BY LINE (+ Checks A, C); bound is 2, not just 4 (Obj. 1) |
| (perturb:separation) · (6.2) · p. 16 | VERIFIED LINE BY LINE (+ Check C, all pairs) |
| Figure perturb:norm-band · Figure 1 · p. 17 (figures/norm-band.tex) | VERIFIED (coordinates re-computed) |
| "affine" definition, (perturb:signature) · (6.3) · p. 17 | VERIFIED |
| Lemma perturb:signatures · Lemma 6.2 · pp. 17–18, (6.4), (6.5) | VERIFIED LINE BY LINE (+ Check B); exponent 3 inherits Lemma 3.1 (SKIMMED); Lean proves exponent 8 (Obj. 4) |
| Theorem perturb:cyclic · Theorem 6.3 · pp. 18–19, (6.6) | VERIFIED LINE BY LINE |
| (perturb:rich-bound) · (6.7) · p. 19 | VERIFIED (+ Check D) |
| (perturb:negative-coefficient) · (6.8) · p. 19 | VERIFIED exactly (Fraction) |
| (perturb:affine-bound) · (6.9) · p. 19 | VERIFIED (+ Check D) |
| covering by Theorem 5.5; absolute `K_0`; uniformity in `P`; `N = q^D ≥ k^{ck}` · p. 19 | VERIFIED as far as §6 is concerned (Theorem 5.5's proof = dichotomy seat) |
| Lemma 5.1 dichotomy:affinity (as used) | VERIFIED |
| Lemma 3.1, Lemma 3.2, Lemma 2.3, Lemma 2.2, Prop 4.2, Theorem 5.5 (proofs) | SKIMMED / statement only — other seats |
| Lean counterparts (text): NormBands, KeyMultiplicity, Perturbation, PerturbationScales, ProbabilityScales, SignatureCounting (part), CyclicSignatures (part) | SKIMMED; route matches the paper except Obj. 1 (Lean sharper) and Obj. 4 (Lean weaker count) |

## Summary

§6 is correct as written. The key multiplicity lemma, the separation `‖qỹ(n)−qỹ(n')‖ ≥ 1` via the coordinate `a+1`, the affine-signature
count, and both union bounds were re-derived step by step; all hypotheses of the imported Lemma 5.1 are met by the V-box alone; the rich
case handles keys carrying both outer colours correctly; the affine case really counts literal SIGNATURES, and identical signatures do
define identical events; `p ≤ 1/2` (true from `k = 2^20`) is the only extra hypothesis the affine estimate needs; (6.8) is exactly
`−21/200000` and is the inequality that caps `c` (`c < 1/16000` with these `γ, p`; `< 1/8000` for the architecture), so the method does
not prove too much. No threshold in §6 depends on `r`, the progression, or the prime `P`. Findings: the "four" is really "two" (Lean
proves two); the Lean certifies a weaker exponent-8 version of (6.4), sufficient for the theorem but not the paper's display; every
`\Cref` to a lemma/proposition renders as "Theorem"; Behrend 1946 could not be fetched (bot wall) and is attribution only.
