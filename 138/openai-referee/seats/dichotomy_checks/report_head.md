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
