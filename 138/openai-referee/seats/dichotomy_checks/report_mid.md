
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
