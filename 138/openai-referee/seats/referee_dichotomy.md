# Referee report — seat `dichotomy` — §5 "Repeated labels and the outer-color dichotomy" (05-dichotomy.tex)

**Paper.** OpenAI, *Quantitative Superexponential Bounds for van der Waerden Numbers*, 23 Sep 2026 (paper.pdf sha256 042acea3…).
**Source read.** `build/sections/05-dichotomy.tex`, all 309 lines, plus every object it uses: 02-setup.tex (parameters, Lemma setup:dilation, the U/V meshes, Lemmas mesh:width and mesh:neighbors), 03-counting.tex (Definition count:eligible), 04-outer.tex (Prop. outer:coloring), and the two places 06-perturbation.tex uses §5 (Lemma perturb:multiplicity uses dichotomy:affinity; Theorem perturb:cyclic uses dichotomy:main). I did not run lean or lake. I read four Lean files as text, for cross-reference only.

**Verdict for this scope: HOLDS AS READ.** I found no FATAL and no GAP. Objections C1–C5 below are all COSMETIC and none touches the proof. Every "for sufficiently large k" inequality in §5 is in §3 with an exact threshold. All of them hold for every k ≥ 1056; the binding one is 2M/k ≤ 1/16 (eligibility (iii)). No inequality is reversed. None depends on r, q, P, λ or on the progression.

The finite model keeps the paper's formulas and chooses only q freely. It reproduces every conclusion of §5 with zero failures at k = 12, 100 and 1056. At k = 1056 that includes all of the longer-period block eligibility. 1056 is the smallest k at which every §5 inequality holds at once, so the whole theorem, including the longer-period case, can be simulated there with the paper's own constants. Three controls each break the short-period conclusion (ii), and each breaks it at the step the proof says depends on it:
- removing the dilation fails only at the "h | λ" step;
- α ≫ q^{−D} fails only at the cut claim;
- a non-adaptive V-mesh also fails only at the cut claim.

## 0. Label map (TeX \label → printed number, page)

| TeX label | printed | page |
|---|---|---|
| dichotomy:affinity | Lemma 5.1 | 12 |
| dichotomy:drift; eq. dichotomy:drift-bounds | Lemma 5.2; (5.1) | 12–13 |
| dichotomy:path; eq. dichotomy:path-equations | Lemma 5.3; (5.2) | 13 |
| dichotomy:heavy-width; eq. dichotomy:relative-width | Lemma 5.4; (5.3) | 14 |
| dichotomy:main; eqs. dichotomy:short-motion, dichotomy:step-lattice, dichotomy:regular-fraction | Theorem 5.5; (5.4), (5.5), (5.6) | 14–16 |

## 1. Status of each item in scope

| item | status |
|---|---|
| Lemma 5.1 dichotomy:affinity | **VERIFIED LINE BY LINE** |
| Lemma 5.2 dichotomy:drift, eq. (5.1), "v = λu as real vectors" | **VERIFIED LINE BY LINE** |
| Lemma 5.3 dichotomy:path, eq. (5.2), gcd assertion, order-h claim, "incongruent ⇒ distinct full labels" | **VERIFIED LINE BY LINE** |
| Lemma 5.4 dichotomy:heavy-width, eq. (5.3) | **VERIFIED LINE BY LINE** |
| Thm 5.5 — light-majority case | **VERIFIED LINE BY LINE**. Prop. outer:coloring(i) taken as stated; it belongs to another seat. |
| Thm 5.5 — short periods, eqs. (5.4), (5.5), the closed-segment cut argument, "(ii) for ALL j" | **VERIFIED LINE BY LINE** |
| Thm 5.5 — longer periods, eq. (5.6), eligibility (i)–(iii), h/8 per block, covering count | **VERIFIED LINE BY LINE**. Prop. outer:coloring(ii) and Def. count:eligible taken as stated. I re-read the proofs of Lemma setup:dilation, mesh:width and mesh:neighbors because §5 leans on them, and they look correct, but they belong to the setup seat. |
| Interfaces §2/§3/§4 → §5 → §6 | **VERIFIED** at the level of statements (see §5 of this report) |

## 2. Line-by-line notes

### Lemma 5.1 (dichotomy:affinity), p. 12
> "(j_3−j_2)(Z_{j_2}−Z_{j_1}) −(j_2−j_1)(Z_{j_3}−Z_{j_2})∈Z^e. In each coordinate its absolute value is at most 2H(j_3−j_1)≤2kH<1, so it is zero."

- **Integrality.** Z_{j_2}−Z_{j_1} ≡ (j_2−j_1)b (mod Z^e). So the combination is ≡ (j_3−j_2)(j_2−j_1)b − (j_2−j_1)(j_3−j_2)b = 0. ✓
- **Bound.** Both points of each difference lie in the same box of side ≤ 2H, so each coordinate is at most 2H(j_3−j_2) + 2H(j_2−j_1) = 2H(j_3−j_1) ≤ 2H(k−1) < 1. ✓
- **"Every triple has the same affine interpolation."** The vanishing identity is exactly Z_{j_2} = [(j_3−j_2)Z_{j_1} + (j_2−j_1)Z_{j_3}]/(j_3−j_1). Taking j_1 = min J and j_3 = max J puts every j_2 ∈ J on one line. The cases |J| ≤ 2 are trivial. ✓
- **Scope of the hypothesis.** Only the side lengths of the box are used, not half-openness or mesh structure. So the §6 use (V-box alone, e = D) is inside the hypotheses. ✓

### Lemma 5.2 (dichotomy:drift), pp. 12–13
- **"m_*−1 ≥ k/(2M)."** m_* > k/M gives m_*−1 > k/M − 1, and k/M − 1 ≥ k/(2M) ⇔ k ≥ 2M. This holds for k ≥ 6 (scan I1). ✓
- **"h ≤ (j_+−j_−)/(m_*−1) ≤ (k−1)/(m_*−1) ≤ 2M."** h is the smallest of the m_*−1 consecutive gaps, which sum to j_+−j_−. Then (k−1)·2M/k < 2M, so the inequality is in fact strict. ✓
- **Is the full-label box one that Lemma 5.1 accepts?** Yes.
  - The full label fixes the U-intervals [aH_x,(a+1)H_x) ⊂ [0,1) and the V-intervals ⊂ [−1/2,1/2) as **real** intervals.
  - x̂ ∈ [0,1)^D and ỹ ∈ [−1/2,1/2)^D, so all (x̂,ỹ)(n_j), j ∈ J, lie in one real box in R^{2D}.
  - Side lengths: H_x = H/λ ≤ 2H (by definition; see C2) and |V| ≤ 2H (mesh:width).
  - z_j = (x(n_j),y(n_j)) is an arithmetic progression on T^{2D} because x and y are homomorphisms.
  - 2kH = 2/k < 1. ✓
- **Proportionality.** On J, Z_j = A + jB. Hence Z_{j'+h} − Z_{j'} = hB = (h/(j_+−j_−))(Z_{j_+} − Z_{j_−}). Side remark: (u,v) does not depend on which minimal gap j' is used. ✓
- **Bounds.** The extreme differences are < H_x in the first system and ≤ 2H in the second. Since (j_+−j_−)/h ≥ m_*−1, this gives |u_i| ≤ H_x/(m_*−1) ≤ 2MH_x/k and |v_i| ≤ 2H/(m_*−1) ≤ 4MH/k. ✓
- **v = λu.** ỹ(n) − λx̂(n) ∈ Z^D for every n, because y = λx on T with λ ∈ Z. So v − λu ∈ Z^D. Also |v_i − λu_i| ≤ 4MH/k + λ·2MH_x/k = 6MH/k < 1, using λH_x = H. So v = λu. ✓

### Lemma 5.3 (dichotomy:path), p. 13
- **"Since h x(d)=u modulo Z^D, the vector t'=h x̂(d)−u is integral."**
  - h·x(d) = x(n_{j'+h}) − x(n_{j'}) on the torus, and u is a real representative of that difference. ✓
  - t = t' mod h coordinatewise. Then x(d) ≡ x̂(d) = (t'+u)/h ≡ (t+u)/h, so x(n_j) = x(n_0) + j x(d) gives the first equation.
  - Multiplying by λ and using λu = v gives the second. ✓
- **gcd(t,h) = 1.** Suppose e > 1 divides h and every t_i.
  - Then e | t'_i, because t' − t ∈ hZ^D.
  - The displacement from j' to j'+h/e is (h/e)x̂(d) = t'/e + u/e ≡ u/e in the first system, and λ(t'/e + u/e) ≡ v/e in the second.
  - The index is in range: j'+h/e < j'+h ≤ k−1. This is the "j'+h/e < k" item in the brief.
  - Z_{j'} + (u,v)/e = (1−1/e)Z_{j'} + (1/e)Z_{j'+h} is a convex combination of two points of one product of real intervals, so it lies in the same box.
  - That box sits inside [0,1)^D × [−1/2,1/2)^D, so the point **is** the chosen representative of n_{j'+h/e}. That index then carries the heavy label at gap h/e < h, which contradicts minimality. ✓
  - Half-openness is used only to place the box inside the representative domain; convexity holds for any product of intervals.
- **Order h.** gcd(t,h) = 1 gives Σc_i t_i + ch = 1 (Bézout). If h | a t_i for all i, then a = Σc_i(a t_i) + c a h ≡ 0 (mod h). ✓
- **Incongruent indices have distinct labels.**
  - If h ∤ (j_1−j_2), some coordinate has (j_1−j_2)t_i/h ∉ Z. That number is a multiple of 1/h, so its circle distance from 0 is ≥ 1/h.
  - The drift is |(j_1−j_2)u_i/h| ≤ (k−1)|u_i|/h ≤ 2MH_x/h.
  - So the actual displacement is at least (1−2MH_x)/h ≥ (1−2MH_x)/(2M), which is > H_x ⇔ 4MH_x < 1.
  - The paper writes the same chain with H in place of H_x: "(1−2MH)/(2M) > H ≥ H_x". That needs 4MH < 1, which holds for k ≥ 3 (I4), so it is valid but weaker. This answers the brief's question "is 1/h − k|u_i|/h > H_x right": yes, with a large margin.
  - Two points of one U-arc are at circle distance < H_x. Using only the first system is legitimate, since one differing U-coordinate already makes the full labels differ. ✓
- **"Consequently, all occurrences of any one full label lie in a single residue class modulo h."** This is the contrapositive of the previous claim. ✓

### Lemma 5.4 (dichotomy:heavy-width), p. 14
- **a = (j_+−j_−)/h is an integer.** By the last sentence of Lemma 5.3, all occurrences of the label at j_* lie in one class mod h. So the m'−1 consecutive gaps are positive multiples of h, which gives a ≥ m'−1. Also ah ≤ k−1, so a < k/h. ✓
- **|Δ_i| ≤ L_i.** j_± carry the same full label as j_*, so ỹ_i(n_{j_±}) lie in the same real V-interval, of length L_i ≤ 2H. ✓
- **Δ_i ≡ a v_i.** By (5.2), y(n_{j_+}) − y(n_{j_−}) = a(λt+v) ≡ av, since aλt ∈ Z^D. ✓
- **The integer is 0.** |av_i| ≤ (k/h)(4MH/k) = 4MH/h, and |Δ_i − av_i| ≤ 2H + 4MH/h < 1 (I5), so the integer Δ_i − av_i is 0. ✓
- **The chain.** |v_i| = |Δ_i|/a ≤ L_i/a ≤ L_i/(m'−1) ≤ (2M/k)L_i, since m' > k/M gives m'−1 ≥ k/(2M). ✓
- **"The heavy label here need not be the one used to choose h."** Correct. The proof uses only (5.2) and the global bound |v_i| ≤ 4MH/k for the single v of Lemma 5.2. Nothing in it refers to which heavy label defined h.
- **Model C (k = 1056).** The smallest observed value of (2M/k)|V(y_i(n_{j_*}))|/|v_i| over all heavy indices is **2.072**.
  - The lemma guarantees ≥ 1; the proof actually gives ≥ (2M/k)(m'−1) ≥ 66·32/1056 = 2. The model reaches that floor, so the lemma is essentially sharp.
  - Evaluated at LIGHT indices, the same inequality fails in 14,905 of 35,273 cases. "Heavy" is load-bearing, and the check can fail.

### Theorem 5.5 (dichotomy:main), pp. 14–16
**Light-majority case.**
- With ≥ δk light positions, Prop. outer:coloring(i) puts each bit on ≥ ¼ of the light positions, which is ≥ δk/4 = k/40 ≥ k/100 = γk. ✓
- Otherwise more than (1−δ)k positions are heavy, so a heavy label exists. ✓

**Short periods (h ≤ h_0).**
- **h | λ.** Take ℓ^a ∥ h. Then ℓ^a ≤ h ≤ h_0 < 2M, so a ≤ ⌊log 2M/log ℓ⌋ and ℓ^a | λ. This is Lemma 2.1, which applies because h ≤ h_0 < 2M (I13). ✓
- **w = v/h is the real step.** y(d) = (λt+v)/h ≡ v/h, because λt/h ∈ Z^D. ✓
- **(5.4).** k|w_i| = k|v_i|/h ≤ 4MH/h ≤ 4MH < ½ for k ≥ 5 (I6). ✓
- **(5.5).**
  - y_i(d) has the representative λd/q^i ∈ q^{−i}Z for any integer representative d. This is well defined on G because q^i | N.
  - Every other representative differs from it by an integer, so it stays in q^{−i}Z, and w_i is one of these representatives.
  - Hence |w_i| ≥ q^{−i} ≥ q^{−D} ≥ q^{−D−1} = α when w_i ≠ 0. ✓
- **Cut crossing.** Write P_j = ỹ_i(n_0)+jw_i.
  - If P_j ∈ [−½,½), then P_j is the representative of y_i(n_j). So a failure at some j means P_j ∉ [−½,½), which forces w_i ≠ 0.
  - Since P_0 ∈ [−½,½): if P_j ≥ ½ the closed segment [P_0,P_j] contains ½; if P_j < −½ it contains −½.
  - Exact hits are covered: P_j = ½ exactly, and P_0 = −½ with w_i < 0 (the segment contains −½ at τ = 0). The text's "closed … both directions of motion and exact cut hits are covered" is accurate. ✓
- **"ρ(y_i(n_j)) ≤ k|w_i| for every j."** Every sample lies on that segment, of length (k−1)|w_i|, and the segment contains a point c ≡ ½. So ρ(y_i(n_{j'})) ≤ |P_{j'} − c| ≤ k|w_i|. ✓
- **"|V(y_i(n_j))| ≤ 2H(ρ+α) ≤ 2H(k+1)|w_i| < |w_i|."** mesh:width applies at Y = y_i(n_j) ∈ its own interval. α ≤ |w_i| is (5.5). And 2(k+1)/k² < 1 for k ≥ 3 (I7). ✓
- **"Circle distance |j−j'||w_i| ≥ |w_i|."** The total real displacement is ≤ (k−1)|w_i| < ½, so the circle distance equals the real one: there is no wrap-around. ✓
- **The contradiction.** Two points of an arc shorter than |w_i| are closer than |w_i|. So all V-labels in coordinate i are distinct, hence all full labels are distinct, so no label has multiplicity > k/M ≥ 2. Therefore ỹ(n_j) = ỹ(n_0) + jw for **all** 0 ≤ j < k and all coordinates. That is (ii) with A = ỹ(n_0), B = w. ✓

**Longer periods (h_0 < h ≤ 2M).**
- **Blocks have the form of Def. count:eligible.**
  - By (5.2), X_z = x(n_{j_0}) + (z/h)(t+u) = x(n_{j_0+z}), and likewise Y_z = y(n_{j_0+z}).
  - t ∈ {0..h−1}^D and u, v ∈ R^D. So the recorded word is the true label word, with * at nonregular positions. ✓
- **Regular fraction.**
  - Rotating coordinates have s_i > h_0, by Lemma 2.1 (needs h ≤ 2M).
  - λt_i/h = p/s_i in lowest terms, so z ↦ zp/s_i (mod 1) visits each of the s_i grid points exactly h/s_i times. ✓
  - The actual value is the grid value + zv_i/h, with |zv_i/h| < |v_i| ≤ 4MH/k < η (I8).
  - A nonregular position (ρ < η) therefore has a grid value with ρ < 2η. That arc has length 4η and holds ≤ 4ηs_i+1 grid points, so the excluded fraction is ≤ 4η + 1/s_i < 4η + 1/h_0.
  - A union bound over ≤ D rotating coordinates gives ≤ D(4η+1/h_0) = 4/1000 + 1/D < ½ ⇔ D ≥ 3 ⇔ k > 1024 (I9). So **every** full block has ≥ h/2 regular positions. ✓
- **Eligibility (i).** The h consecutive indices of a block have distinct residues mod h, so by Lemma 5.3 their labels are pairwise distinct. ✓
- **Eligibility (ii).** |u_i| ≤ 2MH_x/k ≤ H_x (k ≥ 2M) and |v_i| ≤ 4MH/k ≤ H (k ≥ 4M) (I10). ✓
- **Eligibility (iii)** (this is the brief's item b). Take a block containing a heavy index j_* and a stationary coordinate i, so h | λt_i.
  - Then y_i(n_j) − y_i(n_{j_*}) ≡ (j−j_*)v_i/h with |j−j_*| ≤ h−1, so the distance is ≤ |v_i|.
  - |v_i| ≤ (2M/k)L_* by Lemma 5.4 **at j_***.
  - This is the right index and it is legitimate. There is no separate "block's own" (u,v): every block uses the single (h,t,u,v) of the one heavy label chosen in Lemma 5.2. Lemma 5.4 bounds that v against the V-width at *any* heavy index, whatever label sits there.
  - So y_i(n_j) ∈ N(I_*), which needs 2M/k ≤ 1. The closure of J = V(y_i(n_j)) meets N(I_*), so mesh:neighbors gives |J| ≥ L_*/16 ≥ (2M/k)L_* ≥ |v_i|, using 2M/k ≤ 1/16 (I11). ✓
  - This holds at every position, hence at every regular one. It is irrelevant whether j_* itself is regular, because stationary coordinates play no role in regularity.
- **Counting.**
  - Prop. outer:coloring(ii) applies to the block's eligible recorded pattern, and that event family is indexed by h_0 < h ≤ 2M, which matches. Each bit appears on ≥ ¼ of the ≥ h/2 regular positions, so ≥ h/8 per used block. ✓
  - Uncovered positions are the remainder (< h) plus unused full blocks, which are all light (< δk in total). So the used blocks cover > k − h − δk ≥ k − 2M − k/10 ≥ 4k/5 (I12, k ≥ 420).
  - Total per bit ≥ (covered)/8 ≥ k/10 ≥ γk. ✓

**Phrases checked.** §5 contains none of "clearly / it follows / similarly / the same argument / obvious". There are 10 "for (sufficiently) large k" and 12 "thus / therefore / consequently". Each "large k" is matched to an inequality in §3, and each "thus/therefore/consequently" step is verified above.

## 3. Every "for sufficiently large k" inequality in §5 (brief item e)

Parameters as in 02-setup: D = ⌈k^{1/10}⌉, M = ⌈k^{1/2}⌉, h_0 = D², H = k^{−2}, η = 1/(1000D), δ = 1/10, γ = 1/100. `thresholds.py` (§6.1) checks each inequality in exact rational arithmetic for every k with 3 ≤ k ≤ 20000, and spot-checks k = 10^6, 10^8, 10^12, 10^20, 10^40. The "Last failure" column is the largest k ≤ 20000 at which it fails; "None" means it never fails.

| # | inequality | where used | last failure (k ≤ 20000) |
|---|---|---|---|
| I1 | k ≥ 2M (⇒ m_*−1 ≥ k/(2M)) | Lemma 5.2 first line; also Lemma 5.4 | 5 |
| I2 | 2kH < 1 | Lemma 5.1 hypothesis, as used in Lemma 5.2 and §6 | None |
| I3 | 6MH/k < 1 | Lemma 5.2, v = λu | None |
| I4 | (1−2MH)/(2M) > H (⇔ 4MH < 1) | Lemma 5.3, incongruent ⇒ distinct | None |
| I5 | 2H + 4MH/h < 1, all h ≥ 1 | Lemma 5.4 | 3 |
| I6 | 4MH/h < ½, all h ≥ 1 | (5.4) | 4 |
| I7 | 2H(k+1) < 1 | short case, width < \|w_i\| | None |
| I8 | 4MH/k < η | longer case, drift < η | 38 |
| I9 | D(4η + 1/h_0) < ½ (⇔ D ≥ 3 ⇔ k > 1024) | (5.6) | **1024** |
| I10 | k ≥ 4M (⇒ 2MH_x/k ≤ H_x, 4MH/k ≤ H) | eligibility (ii) | 19 |
| I11 | 2M/k ≤ 1/16 | eligibility (iii) | **1055** |
| I12 | k − 2M − k/10 ≥ 4k/5 | covering count | 419 |
| I13 | h_0 < 2M < k | Lemma 2.1 needs h ≤ 2M; the longer range must be nonempty | 6 |
| I14 | k ≥ M (heavy ⇒ m_* ≥ 2) | h well defined | None |
| — | δ/4 ≥ γ; 1/10 ≥ γ | light case; final count | always |

**Behaviour beyond the scan (k > 20000).** Each inequality follows from an explicit elementary bound that only gets easier as k grows. For example:
- I11: 32⌈√k⌉ ≤ 32(√k+1) ≤ k once √k ≥ 16+√288 ≈ 32.97.
- I12: 2(√k+1) ≤ k/10 for k ≥ 439.
- I8: 4000(√k+1)(k^{1/10}+1) < k³ for k ≥ 40.
- The rest have the form c(√k+1)/k² < const.

All five exact spot checks pass.

**Conclusion.** §5's own thresholds are satisfied for every k ≥ **1056**. Thresholds from Prop. outer:coloring and Lemma mesh:width are separate and belong to other seats. None of the §5 inequalities is reversed.

**Quantifiers (brief item i).** No threshold involves r, q, P, λ, the progression, or the choice of heavy label. There are finitely many thresholds, all absolute.

**Prove-too-much (brief item j).** §5 never uses c or the size of q. The only facts it needs about q are that α ≤ q^{−D} and that coordinate steps lie in q^{−i}Z, and both hold for any prime-power q. §5 does not even use gcd(λ,q) = 1; that is used in §6. So §5 cannot be what caps c at 10^{−5}. Whatever caps c lies outside this section; §6's rich-case condition 2c − γ/80 < 0 is the obvious candidate, but checking that belongs to another seat.

## 4. Objections

**None is FATAL or GAP.** All of the following are COSMETIC, i.e. defects of exposition.

**C1 — COSMETIC (exposition, paper-wide).** In the printed PDF, every \Cref to a lemma or proposition is rendered with the word "Theorem". Examples from pdftotext of the PDF:
- p. 13: "By Theorem 5.1, their differences are proportional to differences of indices." The TeX is "By \Cref{dichotomy:affinity}", which is Lemma 5.1.
- p. 13: "With h, u, v as in Theorem 5.2" (Lemma 5.2).
- p. 14: "By Theorem 5.3, j_+ − j_− = ah" (Lemma 5.3).
- p. 14: "Theorem 4.2(i) supplies" (this is Proposition 4.2).
- p. 13: "by Theorem 2.3" (Lemma mesh:width).
- p. 15: "Theorem 2.4" (Lemma mesh:neighbors).

The numbers are right, because all environments share the theorem counter, so a reader can still navigate. The preamble loads cleveref before \newtheorem{lemma}[theorem]; the rendered type name is nonetheless the counter's. Fix: add explicit \crefname{lemma}{Lemma}{Lemmas} (and the same for proposition, corollary, definition), or check the cleveref/amsthm versions used in the build.

**C2 — COSMETIC.** In the proof of Lemma 5.2, p. 13:
> "All vectors (x̂(n_j),ỹ(n_j)), j∈J, lie in one full-label box, whose coordinate widths are at most 2H by \Cref{mesh:width}."

Lemma mesh:width covers only the V-intervals. The U-sides have width H_x = H/λ ≤ 2H by the definition of U in 02-setup ("[aH_x,(a+1)H_x)"). The statement is true; the citation covers only half of it. Fix: add "and H_x ≤ H by definition".

**C3 — COSMETIC.** Eq. (5.6), p. 15:
> "D(4η+1/h_0) = 4/1000 + 1/D < 1/2"

This is stated without its threshold. It needs D ≥ 3, i.e. k > 2^{10} = 1024. That is the second-largest threshold in §5, and the only one tied to D rather than M. The theorem's "for every sufficiently large k" covers it, but at this line the text gives no hint that D must be at least 3. Fix: write "since D ≥ 3".

**C4 — COSMETIC (harmless slack).** 02-setup sets
> "α=q^{−(D+1)}"

but in the whole paper α enters only through mesh:width, mesh:neighbors and (5.5) "q^{−i}≥q^{−D}≥α". The extra factor 1/q is never used.
- It only enlarges R and |V| = O(k³ log k), and those enter logarithmically, so nothing breaks.
- The short-period argument would tolerate any α ≤ (k²/2−k)q^{−D}, from 2H(k|w|+α) < |w| with |w| ≥ q^{−D}.
- The toy model has even more slack. With q ≈ 10^7 at k = 12, the cut claim first fails only around α ≈ 10^{−3}, and fails massively at α = 0.1. The reason is that a cut crossing in coordinate i propagates down the digit chain y_{i−1} = q·y_i to a coordinate whose step is ≥ 1/q.
- This is not an error.

**C5 — COSMETIC.** The statement of Theorem 5.5 says "with d≠0 in G", but nothing in §5 uses d ≠ 0. For d = 0 every label is heavy, h = 1, and (ii) holds with w = 0. The restriction is harmless.

**Remarks the brief asked about that turned out to be fine:**
- the box widths that Lemma 5.1 accepts (U-width H_x ≤ H, V-width ≤ 2H);
- half-openness in the gcd argument;
- j'+h/e < k;
- the 1/h − k|u_i|/h > H_x comparison;
- that a = (j_+−j_−)/h is an integer;
- both directions of motion and exact cut hits in the short-period case;
- no wrap-around in the circle distance;
- that (ii) holds for all j;
- Lemma 5.4 applied at a heavy index whose label differs from the one that defined h;
- the regular-fraction arithmetic and the coverage count.

All are verified in §2.

## 5. Interfaces (statement level)

- **§2 → §5.**
  - Lemma 2.1 gives h | λ for h ≤ h_0, and s_i ∈ {1} ∪ (h_0,∞) for h ≤ 2M. Both are used only within that range. ✓
  - mesh:width is applied at Y in its own interval. ✓
  - mesh:neighbors is applied with I = I_*, J = V(y_i(n_j)) and y_i(n_j) ∈ J̄ ∩ N(I_*). ✓
- **§3 → §5.** The block checks exactly Def. count:eligible:
  - (i) "At least h/2 positions are regular, and the full labels at those positions are pairwise distinct";
  - (ii) "|u_i|≤H_x for every i, and |v_i|≤H in every rotating coordinate";
  - (iii) "In every stationary coordinate i, one has |v_i|≤|V(Y_{z,i})| at every regular position z".

  Regularity, stationary and rotating are defined from the same h and t. ✓
- **§4 → §5.**
  - Prop. 4.2(i) requires "at least δk light positions". ✓
  - Prop. 4.2(ii) covers "every eligible recorded pattern", and its second family is indexed by h_0 < h ≤ 2M, the same range. ✓
  - c_0 = c_*∘L. ✓
- **§5 → §6.**
  - Lemma perturb:multiplicity applies Lemma 5.1 to the V-box alone (e = D, widths ≤ 2H, 2kH < 1). Lemma 5.1 needs nothing more. ✓
  - In Theorem perturb:cyclic, the rich case "a progression containing at least γk of each outer color" is alternative (i) verbatim.
  - "Call a cyclic progression affine when its entire sequence of centered representatives ỹ(n_j) is affine in j" is alternative (ii) verbatim. ✓

## 6. Finite checks

Everything lives in `/tmp/oaimath/160/seats/dichotomy_checks/`, and `run_all.sh` reproduces every output. The full suite takes 55 s wall time with a maximum RSS of 20 MB. No lean or lake was run.

**What the model is** (`toy_model.py`).
- It keeps the paper's **formulas** for D, M, h_0, H, η, λ (prime-power product), H_x = H/λ, α = q^{−(D+1)}, the U mesh, the adaptive V mesh (R, m, a_ℓ), x_i(n) = n/q^i, y_i = λx_i, the centered representatives, full labels, and light/heavy (multiplicity·M > k).
- Only q is chosen freely: a prime > k, large enough that labels actually repeat. With the paper's q ≥ k^{ck/D} and small k, the labels would be injective, because x_D determines n, and nothing could be tested.
- Arithmetic is exact over the integers on the common denominator Q = q^D. V-labels are computed in floating point, with an mpmath (120-digit) fallback whenever the index is within 10^{−5} of an integer.

**Models.**
- **A:** k = 12, D = 2, M = 4, h_0 = 4, λ = 24, q = 10000019.
- **B:** k = 100, D = 2, M = 10, h_0 = 4, λ = 144, q = 10000000019.
- **C:** k = 1056, D = 3, M = 33, h_0 = 9, λ = 2116800, q = 100000000000000003, α = 10^{−68}, |V| = 347,660,686.

In model C **every** §5 inequality I1–I14 holds, so the longer-period case is checked with the paper's own constants. In models A and B some longer-period inequalities fail (I9 needs D ≥ 3), so there the longer case is skipped and reported as "not checked".

**What is checked, per progression and per choice of heavy label.** Every heavy label is tried as "the" chosen one.
- Lemma 5.2: 1 ≤ h ≤ 2M; the |u_i| and |v_i| bounds; v = λu exactly.
- Lemma 5.3: t' integral; both path equations for every j; gcd(t,h) = 1; every label confined to one residue class mod h.
- Lemma 5.4 at every heavy index.
- If h ≤ h_0: h | λ; w_i ∈ q^{−i}Z; k|w_i| < ½; and **conclusion (ii) for all j**.
- If h_0 < h ≤ 2M (model C only), for every full block:
  - s_i > h_0 for rotating coordinates;
  - ≥ h/2 regular positions;
  - pairwise distinct labels;
  - and, for blocks containing a heavy index, eligibility (ii) and (iii) and coverage ≥ 4k/5.
- Independent of heaviness, the core cut claim: if every centred y-step has k|w_i| < ½ and the sampled representatives are **not** affine, then all labels are distinct.

**Not checked.** Alternative (i) cannot be checked, because c_* comes from the local lemma and cannot be constructed. The model records how many progressions fall into the light-majority case.

**Progression families.**
- d = small integer.
- d = (jQ+e)/h with small e, giving a rational step t/h with tiny drift, for h ∈ [1, 2M].
- d = e·q^a.
- d = λ^{−1}e.
- d random.
- In model C a 'ratsmall' family with h ∈ (h_0, 31].

n_0 is either random or engineered so that some coordinate passes within q^{−i}·10^{0..17} of its cut at a random index.

**Coverage reached.**
- The chosen-h histogram for model C is 1:132 2:16 3:18 4:4 5:15 6:6 7:21 8:8 9:27 **11:49 13:172 14:28 15:30 16:32 17:96 18:18 19:18 20:40 21:63 23:66 24:24 28:28 29:28 30:60 31:147 32:32**. That includes rotating periods (11, 13, 17, 19, 23, 29, 31) and all-stationary periods (14, 15, 16, 18, 20, 21, 24, 28, 30, 32, which divide λ).
- In model C, 1,044 used blocks have a stationary coordinate whose width/|v_i| is < 100; the minimum observed is 83.67.
- In model A, 67 short-period heavy cases came within ρ < 10^{−6} of the cut without crossing.

**Results summary.**

| run | change | (ii) failures (short) | cut-claim failures | other |
|---|---|---|---|---|
| A | none | 0 / 913 | 0 / 682 | all lemma checks 0 failures |
| A `--lam1` | λ := 1 (no dilation) | **425 / 1528** | 0 / 349 | "h \| λ" fails exactly 425; the path lemmas still pass |
| A `--alpha 0.1` | α ≫ q^{−D} | **372 / 1676** | **615 / 682** | all lemma checks pass |
| A `--uniformV` | V of uniform width H | **456 / 1984** | **625 / 682** | all lemma checks pass |
| B | none | 0 / 609 | 0 / 380 | lemmas incl. h = 5..9: 0 failures |
| B `--lam1` | λ := 1 | **133 / 576** | 0 / 239 | |
| C | none | 0 / 247 | 0 / 124 | longer: 52,388 block checks, 931 coverage checks, 0 failures; min (2M/k)\|V\|/\|v\| at heavy indices = 2.072 (proof floor 2) |
| C `--vscale 1e6` | feed 10^6·v to the (iii) checker | — | — | (iii) **11,546 / 29,179** fail (the checker can fail) |
| C diag | Lemma 5.4 inequality at LIGHT indices | — | — | **14,905 / 35,273** fail (heaviness is needed) |
| affinity, edge W(k−1) = 1 − 1/k³ | just inside the proof's bound | 0 non-affine (406 + 254 + 168 trials with \|J\| ≥ 3) | | |
| affinity CONTROL W = 1.5/(k−1) | outside | **45, 34, 25** non-affine | | |

Each control fails at the step the proof attributes to it. Without the dilation, only "h | λ" and its consequences fail. Without the α floor or the adaptive mesh, only the cut claim and its consequences fail. The drift, path and heavy-width lemmas never fail in any run.

## 7. Citation table (scope)

§5 cites no external source. Its only citations are internal: setup:dilation, mesh:width, mesh:neighbors, count:eligible, outer:coloring, outer:pullback, and its own lemmas. Each was checked at the statement level in §5 of this report. The nearby Fox–Hunter remark on least-common-multiple dilations is in §2, outside this scope.

| cited result | claimed | actual | verdict |
|---|---|---|---|
| — (no external citation in 05-dichotomy.tex) | — | — | n/a |

## 8. Lean cross-reference (read as text, not built)

- `ShortPeriodLift.lean`, `short_period_affine_lift` (l. 59) and `AdaptiveMesh.short_period_cyclic_lift` (l. 125).
  - Hypotheses: `hmotion : k*|w i| < 1/2`, `halpha : M.alpha ≤ 1/q^D`, `hsmall : 2*H*(k+1) < 1`, and one repeated label pair `hsame`.
  - The cut is taken on a closed segment, 0 ≤ t ≤ k. This is the paper's short-period argument.
  - It confirms that a single repeated pair, not heaviness, is what the cut step uses.
- `LongPeriodEligibility.lean`, `heavy_long_block_eligible` (l. 74).
  - Hypotheses: `hD : 3 ≤ D`, `hsmall : 2*M/k ≤ 1/16`, `hnear : |v i| < 1/(1000 D)` for rotating i, `hperiod : D^2 < h/gcd(h, λ t_i)`, and `hheavy` (stationary |v_i| ≤ (2M/k)·width at the anchor).
  - These are exactly I9, I11, I8 and Lemma 5.4 at the heavy anchor. The formalization needed the same binding constants that §3 identifies.
- `HeavyIntervalWidth.lean`, `heavy_fiber_relative_width` (l. 48).
  - Hypotheses: `hscale : 2*M ≤ k`, `hsmall : 2H + 4MH/h < 1`, `hdrift : |v i| ≤ 4MH/k`. These are I1 and I5.

## 9. Verdict

**HOLDS AS READ.** I checked every step of Lemmas 5.1–5.4 and Theorem 5.5 line by line, with every large-k inequality given an explicit threshold (k ≥ 1056 suffices for all of §5). I found no hole in the human-readable proof. The two points the brief singled out are correct as written:
- **The short-period cut argument.** It uses the lattice w_i ∈ q^{−i}Z, the bound |w_i| ≥ α, and the fact that a crossing forces every V-width in that coordinate below |w_i|.
- **Lemma 5.4 in the longer-period eligibility (iii).** It is applied at a heavy index whose label may differ from the one that defined h; this is valid because there is only one global (h,t,u,v).

The finite model with the paper's own constants at k = 1056 confirms every intermediate claim, including block eligibility. Controls show that the model detects violations and that each failure lands at the step the proof says depends on the changed ingredient. The only defects are cosmetic: C1–C5.

---

## Appendix A. Scripts (verbatim)

### `run_all.sh`  (sha256 98ad6b53d238f5de…)

```
#!/bin/sh
# Reproduces every finite check in referee_dichotomy.md. Each line < 60 s, < 200 MB.
cd "$(dirname "$0")"
timeout 120 python3 thresholds.py 20000            > out_thresholds.txt
timeout 100 python3 affinity_check.py 7            > out_affinity.txt
timeout 100 python3 toy_model.py A 3000 1          > out_A.txt
timeout 100 python3 toy_model.py A 3000 1 --lam1   > out_A_ctrl_lam1.txt
timeout 100 python3 toy_model.py A 3000 1 --alpha 0.1 > out_A_ctrl_alpha.txt
timeout 100 python3 toy_model.py A 3000 1 --uniformV  > out_A_ctrl_uniformV.txt
timeout 100 python3 toy_model.py B 1500 2          > out_B.txt
timeout 100 python3 toy_model.py B 1500 2 --lam1   > out_B_ctrl_lam1.txt
timeout 100 python3 toy_model.py C 300 6 --longer  > out_C.txt
timeout 100 python3 toy_model.py C 150 4 --longer --vscale 1e6 > out_C_ctrl_vscale.txt
```

### `thresholds.py`  (sha256 268110f30f35f683…)

```
# Exact threshold scan for every "for sufficiently large k" inequality used in 05-dichotomy.tex,
# with the paper's parameters (02-setup.tex): D=ceil(k^(1/10)), M=ceil(k^(1/2)), h0=D^2, H=k^-2, eta=1/(1000D).
# All comparisons in exact rational arithmetic (Fraction); integer roots exact via isqrt / integer search.
from fractions import Fraction as F
from math import isqrt
import sys

def ceil_root(k, r):
    # least integer D with D^r >= k  (= ceil(k^(1/r)))
    lo, hi = 1, 2
    while hi**r < k: hi *= 2
    while lo < hi:
        mid = (lo+hi)//2
        if mid**r >= k: hi = mid
        else: lo = mid+1
    return lo

def params(k):
    D = ceil_root(k, 10); M = ceil_root(k, 2)
    return dict(D=D, M=M, h0=D*D, H=F(1, k*k), eta=F(1, 1000*D))

# Each inequality: (name, paper location, predicate(k, p)) ; h ranges handled by worst case (h=1 or h=2M).
INEQ = [
 ("I1  m*-1 >= k/(2M)  [via k/M - 1 >= k/(2M), i.e. k >= 2M]", "drift proof l.1", lambda k,p: k >= 2*p['M']),
 ("I2  2kH < 1", "affinity hyp. as used in drift", lambda k,p: 2*k*p['H'] < 1),
 ("I3  6MH/k < 1", "drift: |v-lam u|", lambda k,p: 6*p['M']*p['H']/k < 1),
 ("I4  (1-2MH)/(2M) > H", "path: incongruent=>distinct", lambda k,p: (1-2*p['M']*p['H'])/(2*p['M']) > p['H']),
 ("I4' (1-2MH_x)/(2M) > H_x (first system only, H_x<=H; checked as 4MH<1)", "path (sharp form)", lambda k,p: 4*p['M']*p['H'] < 1),
 ("I5  2H + 4MH/h < 1 for all h>=1", "heavy-width", lambda k,p: 2*p['H'] + 4*p['M']*p['H'] < 1),
 ("I6  4MH/h < 1/2 for all h>=1", "short-motion", lambda k,p: 4*p['M']*p['H'] < F(1,2)),
 ("I7  2H(k+1) < 1", "short: width < |w_i|", lambda k,p: 2*p['H']*(k+1) < 1),
 ("I8  4MH/k < eta", "longer: drift < eta", lambda k,p: 4*p['M']*p['H']/k < p['eta']),
 ("I9  D(4 eta + 1/h0) < 1/2", "regular-fraction", lambda k,p: p['D']*(4*p['eta'] + F(1,p['h0'])) < F(1,2)),
 ("I10 2MH_x/k <= H_x and 4MH/k <= H (k >= 4M)", "longer: eligibility (ii)", lambda k,p: k >= 4*p['M']),
 ("I11 2M/k <= 1/16", "longer: eligibility (iii)", lambda k,p: F(2*p['M'], k) <= F(1,16)),
 ("I12 k - 2M - k/10 >= 4k/5 (worst h=2M)", "longer: covering count", lambda k,p: k - 2*p['M'] - F(k,10) >= F(4*k,5)),
 ("I13 h0 < 2M < k", "setup (used: dilation lemma needs h<=2M)", lambda k,p: p['h0'] < 2*p['M'] < k),
 ("I14 heavy => m*>=2 (k/M >= 1)", "drift: h well defined", lambda k,p: k >= p['M']),
]

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
for name, loc, pred in INEQ:
    last_fail = None
    for k in range(3, KMAX+1):
        if not pred(k, params(k)):
            last_fail = k
    print(f"{name:72s} | {loc:34s} | last failure k <= {KMAX}: {last_fail}")
# spot-check a few huge k (monotone regime) exactly
for k in [10**6, 10**8, 10**12, 10**20, 10**40]:
    p = params(k)
    bad = [n.split()[0] for n,_,pr in INEQ if not pr(k,p)]
    print(f"k=10^{len(str(k))-1}: D={p['D']} M={p['M']} failures={bad}")
```

### `affinity_check.py`  (sha256 805a45906083f2bc…)

```
"""Exact check of Lemma dichotomy:affinity (05-dichotomy.tex, printed Lemma 5.1).
z_j = a + j b on T^e (rational a,b), J = indices whose representative lies in a half-open box of side W.
Claim: if W <= 2H and 2kH < 1 (the proof only uses W*(j3-j1) <= W*(k-1) < 1), the in-box
representatives are affine in j on J.  Control: W = 1.5/(k-1) must produce non-affine J's."""
import random, sys
from fractions import Fraction as F

def rep_in_box(z, c, W):          # unique real rep of z (mod 1) in [c, c+W) if any (W<1)
    r = (z - c) % 1
    return c + r if r < W else None

def affine_on(J, Z):
    if len(J) <= 2: return True
    j0, j1 = J[0], J[-1]
    return all((Z[j] - Z[j0]) * (j1 - j0) == (Z[j1] - Z[j0]) * (j - j0) for j in J)

def trial(k, e, W, rng, den):
    a = [F(rng.randrange(den), den) for _ in range(e)]
    # step close to a rational with small denominator so that the box is revisited often
    b = []
    for _ in range(e):
        if rng.random() < 0.5:   # near a rational with small denominator: many revisits
            hh = rng.randint(1, 6); t = rng.randrange(hh)
            b.append(F(t, hh) + F(rng.randint(-den//(50*k), den//(50*k)), den))
        else:                    # generic step: revisits come from different laps
            b.append(F(rng.randrange(den), den))
    c = [F(rng.randrange(den), den) - F(1, 2) for _ in range(e)]
    Zs = {}
    for j in range(k):
        reps = [rep_in_box(a[i] + j*b[i], c[i], W) for i in range(e)]
        if all(r is not None for r in reps): Zs[j] = reps
    J = sorted(Zs)
    ok = all(affine_on(J, {j: Zs[j][i] for j in J}) for i in range(e))
    return len(J), ok

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for k in [12, 40, 100]:
    H = F(1, k*k)
    for label, W in [("paper: W=2H, 2kH<1", 2*H), ("edge: W=(1-1/k^3)/(k-1)", (1 - F(1, k**3)) / (k - 1)),
                     ("CONTROL: W=1.5/(k-1)", F(3, 2*(k-1)))]:
        n = bad = big = 0
        for _ in range(4000):
            m, ok = trial(k, 1, W, rng, 10**9)
            if m >= 3:
                n += 1; bad += (not ok)
        print(f"k={k:4d} {label:28s} trials with |J|>=3: {n:5d}   non-affine: {bad}")
```

### `toy_model.py`  (sha256 6269e155d772b993…)

```
"""Finite model of Section 5 (05-dichotomy.tex) of the OpenAI vdW preprint.

Keeps the paper's FORMULAS for D, M, h0, H, eta, lambda, H_x, alpha, the U mesh and the adaptive V mesh,
the coordinates x_i(n)=n/q^i, y_i=lambda*x_i, the centered representatives, labels, light/heavy.
Only q is chosen freely (a prime > k, coprime to lambda, large enough that labels actually repeat).

For every generated cyclic progression n_j = n0 + j d in Z/q^D Z it checks, EXACTLY (integer arithmetic over the
common denominator Q=q^D), every conclusion of Lemmas dichotomy:drift, dichotomy:path, dichotomy:heavy-width and
of Theorem dichotomy:main's short-period case (alternative (ii) for all j) and, when all of the paper's large-k
inequalities hold for this k, the longer-period block-eligibility claims (Definition count:eligible (i)-(iii),
>= h/2 regular positions, coverage >= 4k/5).

Controls (flags): --lam1 (drop dilation), --alpha 0.1 (alpha far above q^-D), --uniformV (no refinement at the cut),
--vscale X (feed X*v to the eligibility (iii) checker).
Usage: python3 toy_model.py MODEL NPROG SEED [flags]   MODEL in {A,B,C}
"""
import sys, random, math
from math import gcd
import mpmath
mpmath.mp.dps = 120

def ceil_root(k, r):
    lo, hi = 1, 2
    while hi**r < k: hi *= 2
    while lo < hi:
        mid = (lo+hi)//2
        if mid**r >= k: hi = mid
        else: lo = mid+1
    return lo

def primes_upto(n):
    return [p for p in range(2, n+1) if all(p % d for d in range(2, int(p**0.5)+1))]

MODELS = {  # k, q (prime)
    'A': (12, 10000019),
    'B': (100, 10000000019),
    'C': (1056, 100000000000000003),
}

class Model:
    def __init__(s, k, q, lam1=False, alpha=None, uniformV=False):
        s.k = k; s.q = q
        s.D = ceil_root(k, 10); s.M = ceil_root(k, 2); s.h0 = s.D**2
        # paper formulas (H = k^-2, eta = 1/(1000 D), delta = 1/10)
        s.Hden = k*k                     # H = 1/Hden
        s.etaden = 1000*s.D              # eta = 1/etaden
        lam = 1
        for l in primes_upto(s.h0):
            a = 0
            while l**(a+1) <= 2*s.M: a += 1
            lam *= l**a
        s.lam = 1 if lam1 else lam
        s.lam_true = lam
        assert gcd(s.lam, q) == 1 and q > k
        s.Q = q**s.D; s.N = s.Q
        s.Hxden = s.Hden*s.lam           # H_x = 1/(k^2 lambda)
        s.alpha = mpmath.mpf(1)/mpmath.mpf(q)**(s.D+1) if alpha is None else mpmath.mpf(alpha)
        s.uniformV = uniformV
        s.R = mpmath.log(1 + 1/(2*s.alpha))
        s.m = int(mpmath.ceil(k*k*s.R))
        s.theta = s.R/s.m
        s.Rf = float(s.R); s.alphaf = float(s.alpha); s.thetaf = float(s.theta)
        s.lam_inv = pow(s.lam, -1, s.Q)
        s.mesh_fallbacks = 0
    # ---- representatives (numerators over Q) ----
    def xnum(s, n):   # xhat_i(n) * Q, in [0,Q)
        return [ (n % s.q**i) * s.q**(s.D-i) for i in range(1, s.D+1) ]
    def ynum(s, n):   # ytilde_i(n) * Q, in [-Q/2, Q/2)
        out = []
        for i in range(1, s.D+1):
            Qi = s.q**i
            r = (s.lam*n) % Qi
            if 2*r >= Qi: r -= Qi
            out.append(r * s.q**(s.D-i))
        return out
    # ---- labels ----
    def Ulab(s, X):   # floor(xhat / H_x)
        return (X * s.Hxden) // s.Q
    def phi(s, a_num, a_den):  # (m/R) log(1 + a/alpha), with exact fallback near integers
        a = a_num / a_den
        v = s.m * math.log1p(a / s.alphaf) / s.Rf
        if abs(v - round(v)) < 1e-5:
            s.mesh_fallbacks += 1
            am = mpmath.mpf(a_num)/mpmath.mpf(a_den)
            return mpmath.mpf(s.m)*mpmath.log1p(am/s.alpha)/s.R, True
        return v, False
    def Vlab(s, Y):   # Y = ytilde*Q in [-Q/2,Q/2)
        if s.uniformV:  # control: uniform mesh of width 1/(k^2) = H on [-1/2,1/2)
            return ('U', ((2*Y + s.Q) * s.Hden) // (2*s.Q))
        if Y < 0:      # left half: a = ytilde + 1/2 in [0,1/2); a_l <= a < a_{l+1}
            v, ex = s.phi(2*Y + s.Q, 2*s.Q)
            l = int(mpmath.floor(v)) if ex else math.floor(v)
            return ('L', l)
        else:          # right half: b = 1/2 - ytilde in (0,1/2]; a_l < b <= a_{l+1}
            v, ex = s.phi(s.Q - 2*Y, 2*s.Q)
            l = (int(mpmath.ceil(v)) if ex else math.ceil(v)) - 1
            return ('R', l)
    def Vwidth(s, lab):  # |I| as float
        if s.uniformV: return 1.0/s.Hden
        l = lab[1]
        return s.alphaf * math.exp(l*s.thetaf) * math.expm1(s.thetaf)
    def labels(s, ns):
        XS = [s.xnum(n) for n in ns]; YS = [s.ynum(n) for n in ns]
        L = [tuple(s.Ulab(X) for X in XS[j]) + tuple(s.Vlab(Y) for Y in YS[j]) for j in range(len(ns))]
        return XS, YS, L

def centered(r, Qi):
    r %= Qi
    return r - Qi if 2*r >= Qi else r

MINS = {}
FAMILIES = ['small', 'rat', 'rat', 'rat', 'digit', 'rand', 'laminv']

def run(model, nprog, seed, vscale=1):
    s = model; k, D, M, Q, q, lam = s.k, s.D, s.M, s.Q, s.q, s.lam
    rng = random.Random(seed)
    C = dict()
    def bump(key, ok=True):
        C.setdefault(key, [0, 0]); C[key][0] += 1
        if not ok: C[key][1] += 1
    fails = []
    # does this k satisfy every large-k inequality of the longer-period case? (see thresholds.py)
    longer_ok = (s.D >= 3 and 32*M <= k and 20*M <= k and 4*M <= k)
    def gen():
        fam = rng.choice(FAMILIES)
        if fam == 'small':
            d = rng.randint(1, 60) * rng.choice([1, -1])
        elif fam == 'rat':
            h = rng.randint(1, 2*M); j = rng.randrange(h)
            while True:
                e = rng.randint(-60*h, 60*h)
                if e != 0 and (j*Q + e) % h == 0: break
            d = (j*Q + e)//h
        elif fam == 'ratsmall':   # rational step t/h with a tiny drift: heavy labels with long periods
            h = rng.randint(s.h0 + 1, max(s.h0 + 1, k // (k // M + 1)))
            j = rng.randrange(1, h)
            while True:
                e = rng.randint(-2*h, 2*h)
                if e != 0 and (j*Q + e) % h == 0: break
            d = (j*Q + e)//h
        elif fam == 'digit':
            a = rng.randint(1, D-1) if D > 1 else 0
            d = rng.randint(1, 60) * q**a
        elif fam == 'laminv':
            d = s.lam_inv * rng.randint(1, 60)
        else:
            d = rng.randrange(1, Q)
        d %= Q
        if d == 0: d = 1
        # n0: random, or engineered so that some coordinate passes near its cut at some index jc
        if rng.random() < 0.35:
            n0 = rng.randrange(Q); where = 'rand'
        else:
            i = rng.randint(1, D); Qi = q**i; jc = rng.randrange(k)
            off = rng.choice([rng.randint(-3, 3), rng.randint(-10**3, 10**3), rng.randint(-10**6, 10**6),
                              rng.choice([1, -1]) * rng.randint(1, 9) * 10**rng.randint(0, max(0, len(str(Qi)) - 2))])
            target = ((Qi - 1)//2 - off) % Qi
            nt = (pow(s.lam, -1, Qi) * target) % Qi + Qi * rng.randrange(Q // Qi)
            n0 = (nt - jc*d) % Q; where = f'cut{i}'
        return n0, d, fam, where
    for it in range(nprog):
        n0, d, fam, where = gen()
        ns = [(n0 + j*d) % Q for j in range(k)]
        XS, YS, L = s.labels(ns)
        mult = {}
        for lab in L: mult[lab] = mult.get(lab, 0) + 1
        heavy = {lab for lab, c in mult.items() if c*M > k}
        nlight = sum(1 for lab in L if lab not in heavy)
        bump('progressions')
        # ---- independent check of the core cut claim (needs no heavy label):
        # if every centred y-step w_i = ytilde(y_i(d)) has k|w_i| < 1/2 and the sampled representatives are NOT affine,
        # the paper's argument says all full labels are distinct.
        wv = []
        for i in range(1, D+1):
            Qi = q**i
            wv.append(centered(s.lam*d, Qi) * q**(D-i))
        small = all(2*k*abs(w) < Q for w in wv)
        affine = all(YS[j][i] - YS[0][i] == j*wv[i] for j in range(k) for i in range(D))
        if small and not affine:
            ok = len(mult) == k
            bump('cut-crossing small-step progressions: all labels distinct', ok)
            if not ok: fails.append(('cutclaim', n0, d, fam, where))
        if 10*nlight >= k:
            bump('case (i): >= delta k light (nothing to check without c_*)')
            continue
        bump('heavy case (< delta k light)')
        for lab in heavy:   # the paper says "choose a heavy label": test EVERY choice
            J = [j for j in range(k) if L[j] == lab]; ms = len(J)
            gaps = [(J[a+1]-J[a], J[a]) for a in range(ms-1)]
            h, jp = min(gaps)
            # drift lemma
            u = [XS[jp+h][i] - XS[jp][i] for i in range(D)]   # over Q
            v = [YS[jp+h][i] - YS[jp][i] for i in range(D)]
            bump('drift: 1<=h<=2M', 1 <= h <= 2*M)
            # |u_i| <= H_x/(m*-1) <= 2 M H_x / k ; |v_i| <= 2H/(m*-1) <= 4 M H / k   (exact, over Q)
            okb = all(abs(u[i])*s.Hxden*(ms-1) <= Q and (ms-1)*2*M >= k for i in range(D)) and \
                  all(abs(v[i])*s.Hden*(ms-1) <= 2*Q for i in range(D))
            bump('drift: |u_i|,|v_i| bounds', okb)
            bump('drift: v == lambda u (real)', all(v[i] == lam*u[i] for i in range(D)))
            # path lemma: t' = h xhat(d) - u integral, t = t' mod h
            Xd = s.xnum(d)
            tp = []
            okint = True
            for i in range(D):
                num = h*Xd[i] - u[i]
                okint &= (num % Q == 0); tp.append(num // Q)
            bump('path: t\' integral', okint)
            t = [x % h for x in tp]
            okp = True
            for j in range(k):
                for i in range(D):
                    # h*(xhat_j - xhat_0) - j*(t Q + u) == 0 mod hQ   (x-path)
                    if (h*(XS[j][i] - XS[0][i]) - j*(t[i]*Q + u[i])) % (h*Q): okp = False
                    if (h*(YS[j][i] - YS[0][i]) - j*(lam*t[i]*Q + v[i])) % (h*Q): okp = False
            bump('path: both path equations, all j', okp)
            g = h
            for x in t: g = gcd(g, x)
            bump('path: gcd(t,h)=1', g == 1)
            okr = all((J2[0] - J2[-1]) % h == 0 and all((a - J2[0]) % h == 0 for a in J2)
                      for J2 in ([j for j in range(k) if L[j] == lb] for lb in mult))
            bump('path: each label in one residue class mod h', okr)
            # heavy-width at every heavy index, every coordinate (|v_i| <= (2M/k)|V(y_i(n_j*))|)
            okw = True
            for js in range(k):
                if L[js] in heavy:
                    for i in range(D):
                        if abs(v[i]) / Q > (2*M/k) * s.Vwidth(L[js][D+i]) * (1 + 1e-12): okw = False
            bump('heavy-width at every heavy index', okw)
            for js in range(k):
                if L[js] in heavy:
                    for i in range(D):
                        if v[i]:
                            r_ = s.Vwidth(L[js][D+i]) * Q / abs(v[i]) * (2*M/k)
                            key_ = 'min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1)'
                            MINS[key_] = min(MINS.get(key_, 1e300), r_)
            # diagnostic (instrument can fail on natural data): the same inequality at LIGHT indices
            for js in range(k):
                if L[js] not in heavy:
                    bad = any(abs(v[i]) / Q > (2*M/k) * s.Vwidth(L[js][D+i]) for i in range(D))
                    bump('diag(control): heavy-width inequality evaluated at a LIGHT index', not bad)
            bump(f'diag: chosen heavy label has h={h}')
            if h <= s.h0:
                # short period
                minrho = min((Q - 2*abs(YS[j][i])) for j in range(k) for i in range(D)) / (2*Q)
                if minrho < 1e-6: bump('diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)')
                if any(t[i] != 0 for i in range(D)): bump('diag: short-period heavy case with t != 0 (genuine rational step)')
                bump('short: h | lambda', lam % h == 0)
                okl = all(v[i] % h == 0 and (v[i]//h) % (q**(D-1-i)) == 0 for i in range(D))  # w_i = v_i/h in q^-i Z
                bump('short: w_i in q^{-i}Z', okl)
                bump('short: k|w_i| < 1/2', all(2*k*abs(v[i]) < h*Q for i in range(D)))
                ok2 = all(h*(YS[j][i] - YS[0][i]) == j*v[i] for j in range(k) for i in range(D))
                bump('SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j', ok2)
                if not ok2: fails.append(('short', n0, d, fam, where, h, lab))
            elif longer_ok:
                # longer period: every full block; eligibility for blocks containing a heavy index
                rot = [ (h // gcd(h, lam*t[i])) != 1 for i in range(D) ]
                for i in range(D):
                    if rot[i]: bump('longer: rotating s_i > h0', h // gcd(h, lam*t[i]) > s.h0)
                covered = 0
                for j0 in range(0, k - h + 1, h):
                    blk = range(j0, j0+h)
                    reg = [z for z in blk if all((not rot[i]) or (Q - 2*abs(YS[z][i]))*s.etaden >= 2*Q for i in range(D))]
                    bump('longer: every full block has >= h/2 regular positions', 2*len(reg) >= h)
                    bump('longer: labels in a full block pairwise distinct', len({L[z] for z in blk}) == h)
                    if not any(L[z] in heavy for z in blk):
                        bad = not all(abs(v[i]) / Q <= s.Vwidth(L[z][D+i]) for z in blk for i in range(D) if not rot[i])
                        bump('diag(control): elig (iii) in a block with NO heavy index (not claimed)', not bad)
                    if any(L[z] in heavy for z in blk):
                        st = [i for i in range(D) if not rot[i]]
                        if st:
                            ratio = min(s.Vwidth(L[z][D+i]) * Q / max(1, abs(v[i])) for z in blk for i in st)
                            if ratio < 100: bump('diag: used block whose stationary coord has min width/|v_i| < 100 (stress)')
                            MINS['min over used blocks, stationary coords, positions of |V|/|v_i|'] = min(MINS.get('min over used blocks, stationary coords, positions of |V|/|v_i|', 1e300), ratio)
                            bump('diag: used blocks with >=1 stationary coordinate')
                        if any(rot): bump('diag: used blocks with >=1 rotating coordinate')
                        covered += h
                        bump('longer: elig (ii) |u_i|<=H_x all i, |v_i|<=H rotating',
                             all(abs(u[i])*s.Hxden <= Q for i in range(D)) and all(abs(v[i])*s.Hden <= Q for i in range(D) if rot[i]))
                        ok3 = all(abs(vscale*v[i]) / Q <= s.Vwidth(L[z][D+i]) for z in blk for i in range(D) if not rot[i])
                        bump('longer: elig (iii) stationary |v_i| <= |V(Y_z,i)| at every position', ok3)
                        if not ok3: fails.append(('iii', n0, d, fam, where, h))
                bump('longer: used full blocks cover >= 4k/5', 5*covered >= 4*k)
            else:
                bump('h > h0 but this k does not satisfy the longer-period inequalities: not checked')
    return C, fails

if __name__ == '__main__':
    name, nprog, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    lam1 = '--lam1' in sys.argv; uni = '--uniformV' in sys.argv
    alpha = float(sys.argv[sys.argv.index('--alpha')+1]) if '--alpha' in sys.argv else None
    vscale = float(sys.argv[sys.argv.index('--vscale')+1]) if '--vscale' in sys.argv else 1
    if '--longer' in sys.argv: FAMILIES[:] = ['ratsmall']*6 + ['rat', 'small', 'digit']
    k, q = MODELS[name]
    mdl = Model(k, q, lam1=lam1, alpha=alpha, uniformV=uni)
    print(f"model {name}: k={k} D={mdl.D} M={mdl.M} h0={mdl.h0} lambda={mdl.lam} (formula {mdl.lam_true}) q={q} "
          f"alpha={mpmath.nstr(mdl.alpha,5)} m={mdl.m} |V|={2*mdl.m} H_x=1/{mdl.Hxden} flags={sys.argv[4:]}")
    C, fails = run(mdl, nprog, seed, vscale)
    for key, (n, f) in C.items():
        print(f"  {key:95s} checked={n:6d} FAIL={f}")
    print(f"  mesh exact-fallbacks: {mdl.mesh_fallbacks}")
    for key, val in MINS.items(): print(f"  {key}: {val:.4g}")
    print(f"  total failures recorded: {len(fails)}")
    for x in fails[:3]: print("   e.g.", x)
```

## Appendix B. Outputs (verbatim)

### `out_thresholds.txt`

```
I1  m*-1 >= k/(2M)  [via k/M - 1 >= k/(2M), i.e. k >= 2M]                | drift proof l.1                    | last failure k <= 20000: 5
I2  2kH < 1                                                              | affinity hyp. as used in drift     | last failure k <= 20000: None
I3  6MH/k < 1                                                            | drift: |v-lam u|                   | last failure k <= 20000: None
I4  (1-2MH)/(2M) > H                                                     | path: incongruent=>distinct        | last failure k <= 20000: None
I4' (1-2MH_x)/(2M) > H_x (first system only, H_x<=H; checked as 4MH<1)   | path (sharp form)                  | last failure k <= 20000: None
I5  2H + 4MH/h < 1 for all h>=1                                          | heavy-width                        | last failure k <= 20000: 3
I6  4MH/h < 1/2 for all h>=1                                             | short-motion                       | last failure k <= 20000: 4
I7  2H(k+1) < 1                                                          | short: width < |w_i|               | last failure k <= 20000: None
I8  4MH/k < eta                                                          | longer: drift < eta                | last failure k <= 20000: 38
I9  D(4 eta + 1/h0) < 1/2                                                | regular-fraction                   | last failure k <= 20000: 1024
I10 2MH_x/k <= H_x and 4MH/k <= H (k >= 4M)                              | longer: eligibility (ii)           | last failure k <= 20000: 19
I11 2M/k <= 1/16                                                         | longer: eligibility (iii)          | last failure k <= 20000: 1055
I12 k - 2M - k/10 >= 4k/5 (worst h=2M)                                   | longer: covering count             | last failure k <= 20000: 419
I13 h0 < 2M < k                                                          | setup (used: dilation lemma needs h<=2M) | last failure k <= 20000: 6
I14 heavy => m*>=2 (k/M >= 1)                                            | drift: h well defined              | last failure k <= 20000: None
k=10^6: D=4 M=1000 failures=[]
k=10^8: D=7 M=10000 failures=[]
k=10^12: D=16 M=1000000 failures=[]
k=10^20: D=100 M=10000000000 failures=[]
k=10^40: D=10000 M=100000000000000000000 failures=[]
```

### `out_affinity.txt`

```
k=  12 paper: W=2H, 2kH<1           trials with |J|>=3:    51   non-affine: 0
k=  12 edge: W=(1-1/k^3)/(k-1)      trials with |J|>=3:   406   non-affine: 0
k=  12 CONTROL: W=1.5/(k-1)         trials with |J|>=3:   775   non-affine: 45
k=  40 paper: W=2H, 2kH<1           trials with |J|>=3:    15   non-affine: 0
k=  40 edge: W=(1-1/k^3)/(k-1)      trials with |J|>=3:   254   non-affine: 0
k=  40 CONTROL: W=1.5/(k-1)         trials with |J|>=3:   449   non-affine: 34
k= 100 paper: W=2H, 2kH<1           trials with |J|>=3:     2   non-affine: 0
k= 100 edge: W=(1-1/k^3)/(k-1)      trials with |J|>=3:   168   non-affine: 0
k= 100 CONTROL: W=1.5/(k-1)         trials with |J|>=3:   323   non-affine: 25
```

### `out_A.txt`

```
model A: k=12 D=2 M=4 h0=4 lambda=24 (formula 24) q=10000019 alpha=9.9999e-22 m=6864 |V|=13728 H_x=1/3456 flags=[]
  progressions                                                                                    checked=  3000 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   682 FAIL=0
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  2398 FAIL=0
  heavy case (< delta k light)                                                                    checked=   602 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=   913 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=   913 FAIL=0
  drift: v == lambda u (real)                                                                     checked=   913 FAIL=0
  path: t' integral                                                                               checked=   913 FAIL=0
  path: both path equations, all j                                                                checked=   913 FAIL=0
  path: gcd(t,h)=1                                                                                checked=   913 FAIL=0
  path: each label in one residue class mod h                                                     checked=   913 FAIL=0
  heavy-width at every heavy index                                                                checked=   913 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=   670 FAIL=0
  short: h | lambda                                                                               checked=   913 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=   913 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=   913 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=   913 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=    67 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=    83 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=   114 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   243 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=   129 FAIL=0
  mesh exact-fallbacks: 0
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 2.634
  total failures recorded: 0
```

### `out_A_ctrl_lam1.txt`

```
model A: k=12 D=2 M=4 h0=4 lambda=1 (formula 24) q=10000019 alpha=9.9999e-22 m=6864 |V|=13728 H_x=1/144 flags=['--lam1']
  progressions                                                                                    checked=  3000 FAIL=0
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  1788 FAIL=0
  heavy case (< delta k light)                                                                    checked=  1212 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=  1528 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=  1528 FAIL=0
  drift: v == lambda u (real)                                                                     checked=  1528 FAIL=0
  path: t' integral                                                                               checked=  1528 FAIL=0
  path: both path equations, all j                                                                checked=  1528 FAIL=0
  path: gcd(t,h)=1                                                                                checked=  1528 FAIL=0
  path: each label in one residue class mod h                                                     checked=  1528 FAIL=0
  heavy-width at every heavy index                                                                checked=  1528 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=  1103 FAIL=0
  short: h | lambda                                                                               checked=  1528 FAIL=425
  short: w_i in q^{-i}Z                                                                           checked=  1528 FAIL=425
  short: k|w_i| < 1/2                                                                             checked=  1528 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=  1528 FAIL=425
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=   241 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   349 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=   188 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   425 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=    43 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=   237 FAIL=0
  mesh exact-fallbacks: 515
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 3.543
  total failures recorded: 425
   e.g. ('short', 78725674976270, 50000190000156, 'rat', 'rand', 2, (77, 113, ('L', 6499), ('L', 6784)))
   e.g. ('short', 78725674976270, 50000190000156, 'rat', 'rand', 2, (5, 41, ('R', 6852), ('R', 6740)))
   e.g. ('short', 2422890331415, 66666920000183, 'rat', 'cut1', 3, (130, 99, ('L', 6834), ('L', 6725)))
```

### `out_A_ctrl_alpha.txt`

```
model A: k=12 D=2 M=4 h0=4 lambda=24 (formula 24) q=10000019 alpha=0.1 m=259 |V|=518 H_x=1/3456 flags=['--alpha', '0.1']
  progressions                                                                                    checked=  3000 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   682 FAIL=615
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  1929 FAIL=0
  heavy case (< delta k light)                                                                    checked=  1071 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=  1676 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=  1676 FAIL=0
  drift: v == lambda u (real)                                                                     checked=  1676 FAIL=0
  path: t' integral                                                                               checked=  1676 FAIL=0
  path: both path equations, all j                                                                checked=  1676 FAIL=0
  path: gcd(t,h)=1                                                                                checked=  1676 FAIL=0
  path: each label in one residue class mod h                                                     checked=  1676 FAIL=0
  heavy-width at every heavy index                                                                checked=  1676 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=  1279 FAIL=0
  short: h | lambda                                                                               checked=  1676 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=  1676 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=  1676 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=  1676 FAIL=372
  diag: chosen heavy label has h=2                                                                checked=   190 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   397 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=   538 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=   212 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=   207 FAIL=0
  mesh exact-fallbacks: 6009
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 2.773
  total failures recorded: 987
   e.g. ('cutclaim', 89583673750331, 50000190000178, 'rat', 'cut2')
   e.g. ('cutclaim', 67856392468768, 100000380000341, 'small', 'cut1')
   e.g. ('short', 67856392468768, 100000380000341, 'small', 'cut1', 1, (1224, 2345, ('L', 0), ('R', 165)))
```

### `out_A_ctrl_uniformV.txt`

```
model A: k=12 D=2 M=4 h0=4 lambda=24 (formula 24) q=10000019 alpha=9.9999e-22 m=6864 |V|=13728 H_x=1/3456 flags=['--uniformV']
  progressions                                                                                    checked=  3000 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   682 FAIL=625
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  1625 FAIL=0
  heavy case (< delta k light)                                                                    checked=  1375 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=  1984 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=  1984 FAIL=0
  drift: v == lambda u (real)                                                                     checked=  1984 FAIL=0
  path: t' integral                                                                               checked=  1984 FAIL=0
  path: both path equations, all j                                                                checked=  1984 FAIL=0
  path: gcd(t,h)=1                                                                                checked=  1984 FAIL=0
  path: each label in one residue class mod h                                                     checked=  1984 FAIL=0
  heavy-width at every heavy index                                                                checked=  1984 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=  1349 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=   688 FAIL=0
  short: h | lambda                                                                               checked=  1984 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=  1984 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=  1984 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=  1984 FAIL=456
  diag: chosen heavy label has h=2                                                                checked=   278 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   635 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=    93 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=   357 FAIL=0
  mesh exact-fallbacks: 0
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 10.96
  total failures recorded: 1081
   e.g. ('cutclaim', 89583673750331, 50000190000178, 'rat', 'cut2')
   e.g. ('cutclaim', 67856392468768, 100000380000341, 'small', 'cut1')
   e.g. ('short', 67856392468768, 100000380000341, 'small', 'cut1', 1, (1224, 2345, ('U', 0), ('U', 113)))
```

### `out_B.txt`

```
model B: k=100 D=2 M=10 h0=4 lambda=144 (formula 144) q=10000000019 alpha=1.0e-30 m=683845 |V|=1367690 H_x=1/1440000 flags=[]
  progressions                                                                                    checked=  1500 FAIL=0
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  1258 FAIL=0
  heavy case (< delta k light)                                                                    checked=   242 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=   671 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=   671 FAIL=0
  drift: v == lambda u (real)                                                                     checked=   671 FAIL=0
  path: t' integral                                                                               checked=   671 FAIL=0
  path: both path equations, all j                                                                checked=   671 FAIL=0
  path: gcd(t,h)=1                                                                                checked=   671 FAIL=0
  path: each label in one residue class mod h                                                     checked=   671 FAIL=0
  heavy-width at every heavy index                                                                checked=   671 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=   529 FAIL=0
  short: h | lambda                                                                               checked=   609 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=   609 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=   609 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=   609 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   380 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=  1290 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=   113 FAIL=0
  diag: chosen heavy label has h=4                                                                checked=    28 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=    80 FAIL=0
  diag: chosen heavy label has h=9                                                                checked=    27 FAIL=0
  h > h0 but this k does not satisfy the longer-period inequalities: not checked                  checked=    62 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=    22 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=    30 FAIL=0
  diag: chosen heavy label has h=8                                                                checked=    24 FAIL=0
  diag: chosen heavy label has h=6                                                                checked=     6 FAIL=0
  diag: chosen heavy label has h=5                                                                checked=     5 FAIL=0
  mesh exact-fallbacks: 13
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 2.556
  total failures recorded: 0
```

### `out_B_ctrl_lam1.txt`

```
model B: k=100 D=2 M=10 h0=4 lambda=1 (formula 144) q=10000000019 alpha=1.0e-30 m=683845 |V|=1367690 H_x=1/10000 flags=['--lam1']
  progressions                                                                                    checked=  1500 FAIL=0
  heavy case (< delta k light)                                                                    checked=   482 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=   961 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=   961 FAIL=0
  drift: v == lambda u (real)                                                                     checked=   961 FAIL=0
  path: t' integral                                                                               checked=   961 FAIL=0
  path: both path equations, all j                                                                checked=   961 FAIL=0
  path: gcd(t,h)=1                                                                                checked=   961 FAIL=0
  path: each label in one residue class mod h                                                     checked=   961 FAIL=0
  heavy-width at every heavy index                                                                checked=   961 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=   443 FAIL=0
  short: h | lambda                                                                               checked=   576 FAIL=133
  short: w_i in q^{-i}Z                                                                           checked=   576 FAIL=133
  short: k|w_i| < 1/2                                                                             checked=   576 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=   576 FAIL=133
  case (i): >= delta k light (nothing to check without c_*)                                       checked=  1018 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=    79 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked=   383 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   239 FAIL=0
  diag: chosen heavy label has h=7                                                                checked=   133 FAIL=0
  h > h0 but this k does not satisfy the longer-period inequalities: not checked                  checked=   385 FAIL=0
  diag: chosen heavy label has h=6                                                                checked=    36 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=    38 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   133 FAIL=0
  diag: chosen heavy label has h=4                                                                checked=    44 FAIL=0
  diag: chosen heavy label has h=5                                                                checked=    70 FAIL=0
  diag: chosen heavy label has h=9                                                                checked=    90 FAIL=0
  diag: chosen heavy label has h=8                                                                checked=    56 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=    51 FAIL=0
  mesh exact-fallbacks: 1339
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 3.182
  total failures recorded: 133
   e.g. ('short', 40725314830739933735, 50000000190000000163, 'rat', 'rand', 2, (8361, 9072, ('L', 679875), ('L', 681793)))
   e.g. ('short', 40725314830739933735, 50000000190000000163, 'rat', 'rand', 2, (3361, 4072, ('R', 672686), ('R', 666997)))
   e.g. ('short', 13872533217406174838, 75000000285000000299, 'rat', 'rand', 4, (1048, 1387, ('R', 681491), ('R', 680595)))
```

### `out_C.txt`

```
model C: k=1056 D=3 M=33 h0=9 lambda=2116800 (formula 2116800) q=100000000000000003 alpha=1.0e-68 m=173830343 |V|=347660686 H_x=1/2360519884800 flags=['--longer']
  progressions                                                                                    checked=   300 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=   124 FAIL=0
  case (i): >= delta k light (nothing to check without c_*)                                       checked=   208 FAIL=0
  heavy case (< delta k light)                                                                    checked=    92 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=  1178 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=  1178 FAIL=0
  drift: v == lambda u (real)                                                                     checked=  1178 FAIL=0
  path: t' integral                                                                               checked=  1178 FAIL=0
  path: both path equations, all j                                                                checked=  1178 FAIL=0
  path: gcd(t,h)=1                                                                                checked=  1178 FAIL=0
  path: each label in one residue class mod h                                                     checked=  1178 FAIL=0
  heavy-width at every heavy index                                                                checked=  1178 FAIL=0
  diag: chosen heavy label has h=13                                                               checked=   172 FAIL=0
  longer: rotating s_i > h0                                                                       checked=  1728 FAIL=0
  longer: every full block has >= h/2 regular positions                                           checked= 52388 FAIL=0
  longer: labels in a full block pairwise distinct                                                checked= 52388 FAIL=0
  diag: used blocks with >=1 rotating coordinate                                                  checked= 34554 FAIL=0
  longer: elig (ii) |u_i|<=H_x all i, |v_i|<=H rotating                                           checked= 52388 FAIL=0
  longer: elig (iii) stationary |v_i| <= |V(Y_z,i)| at every position                             checked= 52388 FAIL=0
  longer: used full blocks cover >= 4k/5                                                          checked=   931 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked= 35273 FAIL=14905
  diag: chosen heavy label has h=18                                                               checked=    18 FAIL=0
  diag: used block whose stationary coord has min width/|v_i| < 100 (stress)                      checked=  1044 FAIL=0
  diag: used blocks with >=1 stationary coordinate                                                checked= 17834 FAIL=0
  diag: chosen heavy label has h=11                                                               checked=    49 FAIL=0
  diag: chosen heavy label has h=31                                                               checked=   147 FAIL=0
  diag: chosen heavy label has h=23                                                               checked=    66 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=   132 FAIL=0
  short: h | lambda                                                                               checked=   247 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=   247 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=   247 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=   247 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=    49 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=    16 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=   115 FAIL=0
  diag: chosen heavy label has h=15                                                               checked=    30 FAIL=0
  diag: chosen heavy label has h=21                                                               checked=    63 FAIL=0
  diag: chosen heavy label has h=8                                                                checked=     8 FAIL=0
  diag: chosen heavy label has h=5                                                                checked=    15 FAIL=0
  diag: chosen heavy label has h=3                                                                checked=    18 FAIL=0
  diag: chosen heavy label has h=17                                                               checked=    96 FAIL=0
  diag: chosen heavy label has h=16                                                               checked=    32 FAIL=0
  diag: chosen heavy label has h=29                                                               checked=    28 FAIL=0
  diag: chosen heavy label has h=4                                                                checked=     4 FAIL=0
  diag: chosen heavy label has h=7                                                                checked=    21 FAIL=0
  diag: chosen heavy label has h=19                                                               checked=    18 FAIL=0
  diag: chosen heavy label has h=32                                                               checked=    32 FAIL=0
  diag: chosen heavy label has h=14                                                               checked=    28 FAIL=0
  diag: chosen heavy label has h=20                                                               checked=    40 FAIL=0
  diag: chosen heavy label has h=24                                                               checked=    24 FAIL=0
  diag: chosen heavy label has h=30                                                               checked=    60 FAIL=0
  diag: chosen heavy label has h=9                                                                checked=    27 FAIL=0
  diag: chosen heavy label has h=28                                                               checked=    28 FAIL=0
  diag: chosen heavy label has h=6                                                                checked=     6 FAIL=0
  mesh exact-fallbacks: 11
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 2.072
  min over used blocks, stationary coords, positions of |V|/|v_i|: 83.67
  total failures recorded: 0
```

### `out_C_ctrl_vscale.txt`

```
model C: k=1056 D=3 M=33 h0=9 lambda=2116800 (formula 2116800) q=100000000000000003 alpha=1.0e-68 m=173830343 |V|=347660686 H_x=1/2360519884800 flags=['--longer', '--vscale', '1e6']
  progressions                                                                                    checked=   150 FAIL=0
  heavy case (< delta k light)                                                                    checked=    49 FAIL=0
  drift: 1<=h<=2M                                                                                 checked=   597 FAIL=0
  drift: |u_i|,|v_i| bounds                                                                       checked=   597 FAIL=0
  drift: v == lambda u (real)                                                                     checked=   597 FAIL=0
  path: t' integral                                                                               checked=   597 FAIL=0
  path: both path equations, all j                                                                checked=   597 FAIL=0
  path: gcd(t,h)=1                                                                                checked=   597 FAIL=0
  path: each label in one residue class mod h                                                     checked=   597 FAIL=0
  heavy-width at every heavy index                                                                checked=   597 FAIL=0
  diag(control): heavy-width inequality evaluated at a LIGHT index                                checked= 22948 FAIL=12096
  diag: chosen heavy label has h=19                                                               checked=    92 FAIL=0
  longer: rotating s_i > h0                                                                       checked=   882 FAIL=0
  longer: every full block has >= h/2 regular positions                                           checked= 29179 FAIL=0
  longer: labels in a full block pairwise distinct                                                checked= 29179 FAIL=0
  diag: used blocks with >=1 rotating coordinate                                                  checked= 17633 FAIL=0
  longer: elig (ii) |u_i|<=H_x all i, |v_i|<=H rotating                                           checked= 29179 FAIL=0
  longer: elig (iii) stationary |v_i| <= |V(Y_z,i)| at every position                             checked= 29179 FAIL=11546
  longer: used full blocks cover >= 4k/5                                                          checked=   473 FAIL=0
  diag: chosen heavy label has h=15                                                               checked=    45 FAIL=0
  diag: used blocks with >=1 stationary coordinate                                                checked= 11546 FAIL=0
  cut-crossing small-step progressions: all labels distinct                                       checked=    60 FAIL=0
  case (i): >= delta k light (nothing to check without c_*)                                       checked=   101 FAIL=0
  diag: chosen heavy label has h=1                                                                checked=    96 FAIL=0
  short: h | lambda                                                                               checked=   124 FAIL=0
  short: w_i in q^{-i}Z                                                                           checked=   124 FAIL=0
  short: k|w_i| < 1/2                                                                             checked=   124 FAIL=0
  SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j                             checked=   124 FAIL=0
  diag: chosen heavy label has h=13                                                               checked=    52 FAIL=0
  diag: chosen heavy label has h=17                                                               checked=    16 FAIL=0
  diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)                      checked=    22 FAIL=0
  diag: chosen heavy label has h=26                                                               checked=    48 FAIL=0
  diag: chosen heavy label has h=20                                                               checked=    20 FAIL=0
  diag: chosen heavy label has h=31                                                               checked=    28 FAIL=0
  diag: chosen heavy label has h=7                                                                checked=    14 FAIL=0
  diag: short-period heavy case with t != 0 (genuine rational step)                               checked=    28 FAIL=0
  diag: chosen heavy label has h=12                                                               checked=    12 FAIL=0
  diag: chosen heavy label has h=14                                                               checked=    42 FAIL=0
  diag: chosen heavy label has h=23                                                               checked=    21 FAIL=0
  diag: chosen heavy label has h=25                                                               checked=    50 FAIL=0
  diag: used block whose stationary coord has min width/|v_i| < 100 (stress)                      checked=  1050 FAIL=0
  diag: chosen heavy label has h=5                                                                checked=    10 FAIL=0
  diag: chosen heavy label has h=11                                                               checked=    37 FAIL=0
  diag: chosen heavy label has h=2                                                                checked=     4 FAIL=0
  diag: chosen heavy label has h=10                                                               checked=    10 FAIL=0
  mesh exact-fallbacks: 4
  min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 3.21
  min over used blocks, stationary coords, positions of |V|/|v_i|: 57.24
  total failures recorded: 11546
   e.g. ('iii', 26785119044050597306835740794351124303219836238284, 866666666666666744666666666666669006666666666666690, 'ratsmall', 'rand', 15)
   e.g. ('iii', 26785119044050597306835740794351124303219836238284, 866666666666666744666666666666669006666666666666690, 'ratsmall', 'rand', 15)
   e.g. ('iii', 26785119044050597306835740794351124303219836238284, 866666666666666744666666666666669006666666666666690, 'ratsmall', 'rand', 15)
```
