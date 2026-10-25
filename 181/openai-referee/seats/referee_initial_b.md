# Referee report — seat `initial_b`
## Scope: §6 (Lemma 6.1, pp. 51–63), §7 (claim (7.1), Lemma 7.1, Corollary 7.2, pp. 64–68), Table 1 rows "Polynomial broad-side concentration" / "Small-grid purity" (p. 167)

Paper: OpenAI preprint "The hypercube Ramsey number has linear order" (23 Sept 2026), `/tmp/oaimath/171/paper.pdf`. I read the rendered PDF pages (4–35, 48–69, 166–172) and used `paper_plain.txt` only for verbatim quotes; displayed formulas below are transcribed from the rendered pages.
Statements used from other seats' scope (read for their hypotheses only, proofs NOT refereed here): Lemma 3.2 (p. 11), 3.3 (pp. 11–12), 3.5 (pp. 12–13), 3.6 (p. 13), 3.7 (p. 14), 3.8 (p. 15), 3.9 (p. 19), 3.10 (p. 21), Lemma 4.1 (p. 26), Lemma 5.1 (p. 34).

**Bottom line.** I found no FATAL issue and no mathematical GAP in §6–7. The combination giving (7.2) is correct: the quantifiers are in the right order, the dependency graph of constants has no cycle, η0 is an absolute constant, Lemma 3.2 is applied to a finite list of three fixed properties, and no rate of C_n is used. Everything I list below is COSMETIC/EXPOSITION or UNCLEAR-because-imported (it rests on §5.3 state geometry or on Lemma 3.8 internals, which belong to other seats).

---

## 1. The combination that gives (7.2), written out (item (d))

Constants, in order (all fixed before n → ∞):
1. D* > 0: universal (Lemma 6.1; checked in §3 below that it doesn't depend on K, γ, p0).
2. D0 ∈ Q with 0 < D0 < min(.1, D*/2) (p. 64).
3. d ∈ (0, D0/1000); b = d/4; c = b/20 = d/80 (p. 64). (d is not said to be rational; that doesn't matter, see step 6.)
4. β = γ = d/4 in Lemma 4.1. Then h = h(β,γ) = ω/10^6 with ω = min(β, 1−γ)/1000 = d/4000 (p. 26), so h = d/(4·10^9).
5. η0 = any fixed value in (0, min(γ,h)], e.g. η0 = h.

Stabilization steps (Lemma 3.2), in order, each on the sequence left by the previous step:
- **(S1) P71** = "∃ σ on X, τ on Y (retained), N max σ ≤ n^{D0}, width(τ) ≤ n^{1/4}, some color has d ≤ n^{−c}". Suppose it is available. Lemma 3.2 lets us pass to a subsequence on which one color is available. Markov restricts σ to σ′. That gives an available family with N max σ′ ≤ 2n^{D0} ≤ n^{D*} and every x ∈ supp σ′ of G-degree ≥ 1 − n^{−c/2} into τ. Lemma 3.2 turns this into a finite menu, and Lemma 3.3 into a balanced mixture with K = 4/κ. Lemma 6.1 with X↔Y and (γ, p0) = (1/4, c/2) then gives a cube, contradiction. So P71 is not available, and by Lemma 3.2 it is eventually absent after o(N) removals. That is (7.1). Absence persists under every further removal or subsequence, because the property is intrinsic to supports and removal only shrinks the family of laws.
- **(S2) P_pur(d/4, h)** = "∃ μ, ν with widths ≤ 2n^{d/4} and defect ≤ e^{−n^h} in some color". Suppose it is available. Pass to one available color. Restrict ν to columns of defect ≤ e^{−n^{h/2}}; Markov loses mass ≤ e^{−n^h + n^{h/2}} = o(1). The widths become ≤ 2n^{d/4} + o(1) ≤ n^{d/2}. Lemma 7.1 with p = h/2 (it needs (7.1), which holds after S1) gives a contradiction. So P_pur is not available, hence eventually absent.
- **(S3) P_bias(d/4, h)** = "∃ μ, ν with widths ≤ n^{d/4} and |d_G − ½| ≥ n^{−h}". After S2, hypothesis (ii) of Lemma 4.1 holds (eventually, on current sets), so if P_bias were available, Lemma 4.1 would give a cube. Hence P_bias is eventually absent.
- Conclusion: for every μ, ν on the retained sides with widths ≤ n^{η0} ≤ n^{d/4}, |d_G − ½| < n^{−h} ≤ n^{−η0}. Since d_R = 1 − d_G, this covers both colors. That is (7.2).

Orientation check: (7.1) is used only with σ on X and τ on Y, both inside Lemma 7.1 Step 2 (p. 65) and in the claim's own proof. Lemma 7.1 restricts the Y-side law, and P_pur/P_bias with β = γ are symmetric. So no reverse-orientation version of (7.1) is ever needed.

Countability: the list is finite (P71, P_pur, P_bias), each with fixed real parameters. The countable-list clause of Lemma 3.2 and rationality are not needed here. The "finite union ⇒ available member" step is used only for the two-color union. The "available menu ⇒ finite menu" step is used before each Lemma 3.3 call (p. 64 twice, p. 65).

η0 depends only on d, hence only on D0 and D*. It does not depend on the subsequence, the removed sets, the tolerances κ, the balance constants K or K′, or n. Only the threshold n0 beyond which (7.2) holds depends on the sequence. **Verified.**

---

## 2. Objections (numbered)

**O1. §7 p. 64, application of Lemma 6.1 "with the sides interchanged".**
Quote: "Choose a balanced mixture by Lemma 3.3, and apply Lemma 6.1 with the sides interchanged: its narrow law is τ, its broad law is σ′, and its defect exponent is p0 = c/2."
Lemma 6.1 (p. 51) is stated with μ_i on X (narrow) and ν_i on Y (broad). No interchanged version is stated. It follows from the X↔Y symmetry of the setting: both sides have size N, only cross edges are colored, and Q_n's parity classes are swapped by the automorphism v ↦ v ⊕ e_1. §2 (p. 10) also says "we may interchange the host sides".
Budget check for (b): narrow τ has width ≤ n^{1/4}, so γ = 1/4 < 1 ✓. Broad σ′ has N max σ′ ≤ 2n^{D0} ≤ n^{D*} ✓; only D0 < D* is needed, D0 < D*/2 is slack. Balance: N E σ′, N E τ ≤ K = 4/κ ✓. Degree: d_G(x, τ) ≥ 1 − n^{−c/2} for every x ∈ supp σ′ ✓.
Severity: COSMETIC (EXPOSITION). Fix: state Lemma 6.1 for either orientation.

**O2. §6 p. 54 and p. 60: "O(1)" hides a K-dependence.**
Quotes: "The parent and conditional candidate priors have normalized caps O(1), and only boundedly many tag factors occur." (p. 54) and "posterior cancellation bounds the mean by the candidate prior, hence by O(1) after normalization." (p. 60)
The normalized cap is O(K), not O(1): Π′ ≤ O(K)/N (p. 51), and the priors are ≤ 10Π′ and ≤ (1/.7)Π′. The extra factor is absorbed into n^{d1} (Step 1 cap) or into the bounded average (p. 60) once n is large in terms of K. That is legitimate, because p. 51 says "only subsequent auxiliary choices and the sufficiently large dimension threshold may depend on the fixed input parameters". I checked every appearance of K in §6: it enters only the threshold, never D*, d0–d2, δ1, δ2, κ (tuple factor), c2, c3, or α.
Severity: COSMETIC.

**O3. §6 p. 53, parameter list. The order is stated loosely, but it is consistent.**
Quote: "Use very small successive constants d2, δ2, d1, δ1, d0, D∗ > 0, each sufficiently small in terms of previous ones and the absolute coarse dimension (in particular d2 ≪ κ). Choose 2D∗ < d0 … require Cd1 + δ2 + d0 < d2 … also take d0, δ1 ≪ d1."
These are the inequalities actually used later. I extracted them and checked they can all be met in the stated order:
- κ(1 + log(4/c1)) < .001, with c1 = .005.
- d2 ≪ κ: needed so that d2(J+1)log n ≪ k on p. 56, and so that the coefficient O(d2) + O(d1) + .002 < .05 on p. 58.
- δ2 < d2.
- C·d1 + δ2 + d0 < d2.
- Step 1 absolute cap with ≤ 602 tag factors and ≤ 601 candidate factors: roughly 602·d0 + δ1 < d1.
- d1 < .05 (p. 60: n^{−.05+d1} = o(1)).
- d2 < .065 (p. 61: Σ_j n^{−.13j + d2(j+1)} = o(1)).
- 2D* < d0.

No inequality involves K, γ or p0. α is chosen afterwards, in terms of these constants and p0. The places that need it are: α < p0 (so mε → 0, p. 54); .04α < p0 ((T+J)kε = o(k), p. 57); α < .1 (o(n^{.4}) chunk flips, p. 62); Cα < c3/4 (p. 58); α small against δ2 and κ (pattern unions, pp. 58–59).
Severity: COSMETIC. **The universality claim for D* is correct.**

**O4. §6 p. 59, the marking rule has no stated tie-breaking.**
Quote: "At each odd state and each pair of consecutive levels, take a maximal family of disjoint ID sets whose Step 3 descriptors fail. Mark their union forbidden at the adjacent even sites."
The proof needs the mark to be a deterministic local function: "A mark reads only the incident-star Step 3 tests, their base and hidden inputs, the listed center tuples and position counts." That fails unless one fixed maximal family is chosen by a fixed rule (for example, greedy in a fixed ID order). The maximality argument is correct for any choice: "A failed actual descriptor would be disjoint from the marked union, contradicting maximality." The count is also correct: Pr(≥ n disjoint failed sets) ≤ D_n^n e^{−c2 kn} ≤ e^{−c2 kn/2} beats exp(O(n)).
Severity: COSMETIC. Fix: "the lexicographically first maximal family".

**O5. §6 p. 62 (also §4 p. 32): "apply Lemma 3.9 with d = N".**
Quote: "On entering histories with odd columns at most 1/10, apply Lemma 3.9 with d = N."
Lemma 3.9 (p. 19) is for "laws on d labels", and its dummy-row completion uses p_dum(y) = (t/d − c_y)/(t − m) over exactly d labels. After o(N) removals the retained Y has fewer than N labels. The fix costs nothing: pad with N − |Y_ret| zero-mass phantom labels. Real rows never use them, and the hypotheses hold: atoms N^{−1+o(1)} ≤ N^{−.95}, columns ≤ .1 < .4, n² ≤ N^{.025}, and m = 2^{n−1} ≤ N/2 because C_n → ∞.
Severity: COSMETIC.

**O6. §6 p. 55, descriptor counts imported from §5.3 (UNCLEAR, out of scope).**
Quote: "At low center severity j, adjacent types observed with at most T distinct IDs altogether give O(T + j + 1) tuples; as before generic variants are constantly many (same t, F, coarse choices and severity variants), while exceptional adjacent states changing F or t number O(j + 1)."
The bounds log|D_b| = O(T log n + (J+1) log T) and O(T log T + (J+1) log m) follow from the stated structural facts. I checked that arithmetic. The facts themselves come from the state geometry of Lemma 5.1 (§5.3): "All neighbors across a low/high transition form one state at the paired fine-count fringe"; "All nonmatching-primary neighbors also form one state"; and the merging of counts at R_f and R_f + 1. I could only check them in outline: R_f = 5.5 merging and one-sign flips only at chunks at distance ½. The fringe-merging claim is plausible, but its proof is in §5.3, which is another seat's.
Severity: UNCLEAR (dependency, not a defect found).

**O7. §6 p. 59, Lemma 3.8 parameters are not exhibited.**
Quote: "Choose the other height parameters to give crowd at most T/2 and short-truncation error o(e^{−2m^{1/5}})."
Here T = ⌈m^{.001}⌉ = n^{.001α + o(1)}, so the crowd exponent must satisfy b < .001α. Lemma 3.8 then requires b0 > a > ζ + σ + (1−θ), b > a + 4σ, θ > .9 (for (iii)), r = ⌊ρn⌋ ≤ (¼ + o(1))d, and λ = n^{10} (J0 = 10 > 2). I checked that these can be met together. For example:
- θ = 1 − 10^{−4}α, ζ = 3·10^{−4}α, σ = 4·10^{−5}α, a = 7·10^{−4}α, b0 = 8·10^{−4}α, b = 9·10^{−4}α.
- Lemma 3.8 Step 4 needs a − σ − (1−θ) > 0 and b − a − 2σ > 0: both hold.
- Lemma 3.8(iii) needs a − σθ + α(θ/2 − 1/5) > 0: holds.
- √m ≤ H = n^{1−ζ+σ}: holds.
Severity: COSMETIC.

**O8. §7 p. 64: d, b, c are not declared rational.**
Quote: "Take rational constants 0 < D0 < min(.1, D∗/2) … Fix 0 < d < D0/1000, b = d/4, c = b/20."
This is harmless inside §7, which stabilizes three fixed properties. Later sections stabilize "every fixed admissible rational choice" (Table 1, p. 167), and their parameters are built from η0 = min(d/4, h), which need not be rational. That is only harmless if those families are indexed by rationals below η0, not by functions of η0. Not my scope; noted for the §8–12 seat.
Fix: take d rational.
Severity: COSMETIC.

No other objections. In particular: no FATAL, no GAP, and no rate of C_n.

---

## 3. Item-by-item findings

### (a) Lemma 6.1
- **D* universal**: verified (O3). D* enters only through two bounds:
  - "η_y(i) = Λ(i)ν_i(y)/Π(y) ≤ n^{2D*}Λ(i)" (p. 52). Uses ν_i ≤ n^{D*}/N and NΠ ≥ n^{−D*} on supp Π′.
  - "2D* < d0, so … that bound is n^{d0}Λ" (p. 53).
- **Broad-side degree cap ≥ 1 − n^{−p0}**: used only through support properties of tags, the label factor (1 + 4ε/c1)^k = e^{o(k)}, and the common-hit mass c1 − O(mε) ≥ c1/2 (p. 54). All three need only α < p0.
- **N^k max Π_v ≤ e^{.4kn}** (p. 62): F_z ≤ e^{.34kn}Q and m_c ≥ e^{−.02kn}Q give posterior/prior ≤ e^{.36kn}. The prior's per-coordinate density relative to uniform is ≤ e^{n^γ}·(2/c1) = e^{o(n)}. Total ≤ e^{.36kn + o(kn)} ≤ e^{.4kn} ✓. The input F_z ≤ e^{.34kn}Q itself:
  - ≤ n matching neighbors, each with p_b ≤ e^{.2k}|D_{b,c}|q_b and log|D_{b,c}| < .1k;
  - plus o(n^{.4}) chunk-flip neighbors at cost ≤ max(m^{.15}, .05J log n) each, which is o(kn);
  - total .3kn + o(kn) ✓.
- **N max p_v ≤ O(e^{.55n})** (p. 63): |H|/N ≤ e^{−.55n}, so Pr_post(#{j : x_j ∈ H} > .8k) ≤ 2^k e^{.4kn} e^{−.44kn} = 2^k e^{−.04kn} = o(1). The heavy marginal mass is ≤ .8 + o(1), and renormalizing costs ≤ 5 + o(1) ✓.
- **§6.1 first case** (p. 52), reduction to Lemma 5.1 in the opposite color:
  - Partner mass ≥ .05 on a set S1 with Π′(S1) > .05, so χ = Ω(1/K).
  - E B_y ≤ O(1)·E_Π B_y = O(1)·E_Λ μ_i ≤ O(K)/N ("indeed E_{y∼Π}η_y = Λ") ✓.
  - Width of B_y ≤ n^γ ✓; the degree .99 > .95 ✓.
  - Matches Lemma 5.1's hypotheses (p. 34) exactly.
- **§6.1 second case** (pp. 52–54):
  - Mass of ≍ > .8, and V0's prior is ≤ Π′/.7 ✓.
  - Candidate prior Π′|≍V0 ≤ 10Π′ ✓.
  - Base-tag restriction mass ≥ (c0 − c1)/(1 − c1) ≈ .005 ✓.
  - Coarse relation C(h) and the "only the opposite key at the same bin can have a nonmatching primary" claim ✓.
  - Step 1 predictive-density argument: Pr(p(I_s) < n^{−δ1}Λ(I_s)) ≤ n^{−δ1}, so the posterior multiplier is ≤ n^{d0+δ1} ✓.
  - Step 2: m_S is the gated true-data density relative to Π π_{ℓ,−h}, because I_h ∼ T0 given the rest of the base and the tags are conditionally independent given the parents ✓. The exception masses are ≤ a ✓. T_β ≤ n^{d0 + d1|S| + δ2 u_β}Λ ≤ n^{d2 u_β}Λ with |S| ≤ C u_β ✓. The support-degree claims are checked case by case: matching gives 1−ε, crossing gives c1 ✓.
- **§6.2–6.3**:
  - Step 3 low: tag factor n^{d2u_β}; label factors (1+2ε/c1)^k ≤ (1+4ε/c1)^k and (2/c1)^k; the M tests with mass ≤ e^{−.02k} each (∫M_{−c}dQ ≤ 1); log(L_b/Q_{−c}) < .16k; cap O(J² log n) = o(m^{.15}) ✓.
  - Step 3 high: four-line budget, coefficient ≤ κ(log(2/c1) + .02) + O(d1 + d2) < .05 ✓.
  - Markov "alarm" halvings: e^{−.018k} → e^{−.009k} → e^{−.0045k} → e^{−.00225k} ≤ e^{−c2 k} with c2 = .001 ✓.
  - LLL charges, coarse stage: bounded degree, p = o(1) ✓.
  - LLL charges, hidden stage: n^{−c3} ≤ x(1−x)^{m^C} with x = n^{−c3/2} and Cα < c3/4 ✓.
- **Selection bias (brief item 4)**:
  - *Low odd rows*: P_ξ(presentation of 𝔡, O ∈ do) = F_ξ a_ξ Q(do), with a_ξ recomputed under candidate-dependent regeneration of tuples. This gives E[p^pr 1_adj] ≤ π_ℓ(y) by cancellation and disjointness, and E[p^pr 1_fb] ≤ e^{−.02k}·#descriptors·π_ℓ = o(π_ℓ) ✓.
  - *Long vs short rule*: coupled with error O(n)·e^{m^{.15}}·o(e^{−2m^{1/5}}) = o(1) ✓.
  - *High odd rows*: these ignore selection, which is legitimate. Their load is bounded deterministically by rarity × cap, n^{−.13(J+1)}·n^{.05J} → 0. Their only other use is p_b ≤ e^{.2k}Q_{−c} in F_z, which needs no posterior property ✓.
  - *Even rows*: E contains "presence and legitimate long selection of c at v", recomputed at z (p. 62: "All choices and kernel evaluations in this formula are recomputed at z"). The cancellation "∫ m_c (F_z dP_c/m_c) dy = dP_c(z)∫F_z dy" keeps the selection indicator, and it is then bounded by O(1/λ) at level 0 and e^{−n^{Ω(1)}} above, so the sum over presence is O(1) ✓.

### (b) Interchanged application near p. 64: budgets met ✓ (see O1).

### (c) Lemma 7.1
- log(N max p_b) ≤ n^{d/2} + 2cs log n + O(1), with s = ⌈n^d⌉. That equals n^{d/2} + 2cn^d log n + O(log n), as in Table 1 ✓.
- log(N max p_v) ≤ .04q + o(q) with q = ⌈n^{4d}⌉, i.e. .04n^{4d} + o(n^{4d}) ✓.
- (7.1) is used once, in Step 2: σ = α|H_τ normalized has N max σ ≤ (K′/N)/(K′n^{−D0})·N = n^{D0}, and width(τ) ≤ log L < n^{1/4} because d < 10^{−4} ✓.
- Line-by-line checks:
  - Deletion bounds: own hit (1 − n^{−2})^{−1}, because S_{−w} ⊆ S_cross; cross hit n^c(1 − n^{−2})^{−1}, via the order with w last ✓.
  - Profiles via Lemma 3.3 (price separation + Kakutani) ✓.
  - Pr(B_g) ≤ n^{−D0/2 + 2d + o(1)} ≤ n^{−D0/3} ✓; tag LLL with charges n^{−D0/4} and degree O(s²) ✓.
  - Typicality moment: nfL_μ = n^{O(1)}(2n^{−b})^s e^{n^{d/2}} → 0 ✓.
  - F_z ≤ n^{2cm}(1 − n^{−2})^{−n}Q_v = e^{o(q)}Q_v ✓; E r_v ≤ e^{−.04q} ✓.
  - (n+1)^{2s+1} formulas: the formula is determined by 2s+1 counts, q auxiliary cells and a fixed residual count ✓.
  - Anchor LLL: degree O((s+q)^4) = O(n^{16d}) with 16d < D0/4 ✓.
  - Odd moment: nfL ≤ exp(−(b − 2c + o(1))s log n) ✓.
  - Lemma 3.10 hypotheses: θ0 column bound, atoms ≤ L/N ≤ n^{−A*}, predicates ≤ e^{−.02q} ≤ n^{−P*}, n ≤ n^B reads, log g = O(n) ✓.
  - Even posterior cancellation Σ_y M_v·F_xμ/M_v ≤ μ(x) ✓.
  - Near fraction f ≤ q^5·2^{−q}; nfL_even → 0 ✓.
  - Even columns O(2^n/N) → 0 ✓.

### (d) See §1. Correct.

### (e) Rate of C_n and use of N ≤ n2^n
**C_n → ∞ enters only as:**
- |B|/N = 1/(2C_n) → 0 (pp. 61, 67);
- |A|/N → 0 (p. 63);
- O(2^n/N) = o(1) (p. 68);
- m = 2^{n−1} ≤ N/2 (implicit in the Lemma 3.9 use).

**N ≥ 2^n enters as:**
- atoms e^{o(n)}/N ≤ N^{−.95} and ≤ n^{−A*};
- n² ≤ N^{.025}.

**N ≤ n2^n enters as:**
- the union over labels after the n-th-moment Markov step (pp. 60, 63, 66, 67, 68). This needs (C/M)^n·n2^n → 0, which holds for a large fixed threshold M;
- log g = O(n) in Lemma 3.10 (p. 68).

Every other union is over exp(O(n)) role/ID/state choices against e^{−Ω(kn)} with k → ∞. **No rate of C_n is used anywhere in §6–7.**

### (f) Hand-wave phrases in scope (all checked)
| p. | phrase | verdict |
|---|---|---|
| 54 | "The same predictive-denominator calculation, with d0, δ1 ≪ d1, proves the absolute test." | OK. Bounded number of tag and candidate factors, O(K) absorbed (O2). |
| 54 | "The same bounds hold at alternative observations satisfying the gates." | OK. The bounds come from the gates alone. |
| 55 | "as before generic variants are constantly many …" | imported from §5.3 (O6) |
| 55 | "At high states the same description uses O(J) coordinates near the interface" | OK. Sign matters only at j_x = J+1, so ≤ j_b ≤ J+2 flippable chunks. |
| 57 | "The absolute tag bound in Step 2 gives the same tuple comparisons as in the low calculation." | OK (T_β ≤ n^{d2u_β}Λ). |
| 57 | "As at low targets, the denominator tests are data tests" | OK |
| 58 | "The coarse stage has bounded degree and the same inequality with charges tending to zero." | OK |
| 59 | "the other n − 1 failures give the same negligible bound" | OK (D_n^{n−1}e^{−c2k(n−1)}) |
| 60 | "These are the validity conditions of the previous lemma with its singleton and optional-pool conditions removed." | depends on §5 wording; the list given here is self-contained and is what is used |
| 60 | "Use this same table also for descriptors presented by the long selection." | OK. This is what makes long = short off the coupling exception. |
| 61 | "the additive comparison gives the same for long means" | OK |
| 61 | "The near-bin fraction is the one in the preceding odd base estimate" | OK (O((2n^{−.04})^{300})) |
| 62 | "The same near-sign count applies" | OK (j = 0 rows read sign t only) |
| 67 | "Its fraction is again f ≤ n^{O(1)}(2n^{−b})^s" | OK |
| 68 | "Lemma 3.6 and the same Markov and column union" | OK |

### (g) Citation table (scope §6–7)
The only external result invoked directly in §6–7 is Hall's theorem (pp. 51, 63, 68). The rest enter through the paper's own §3 lemmas, whose proofs are given in-paper.

| cited result | paper's claim | source | status |
|---|---|---|---|
| Hall [20], via p. 12 | rows supported on allowed labels with Σ_v p_v(y) ≤ 1 ⇒ \|S\| ≤ \|∪ supp\| ⇒ SDR | Hall 1935, J. London Math. Soc. 10, 26–30. Wiley returned a Cloudflare page (`refs/initial_b_hall/h.pdf` is HTML). The textbook statement (SDR iff every k sets have union ≥ k) is what the paper uses, and the double-counting reduction on p. 12 is correct. | COULD NOT FETCH (statement standard, reduction verified) |
| Lu–Székely [27, Lemma 3], cited for Lemma 3.5's "asymmetric formulation"; Lemma 3.5 is used on pp. 58, 60, 66, 67 | E_i with nonneighbor-conditional probability ≤ p_i, p_i ≤ x_iΠ_{j∼i}(1−x_j) ⇒ avoidance, plus conditional comparisons | EJC #R63 (2007), PDF read from `refs/lu_szekely/ls.pdf`, p. 2: "**Lemma 3** … Let A1,…,An be events with a negative dependency graph G. If there exist x1,…,xn ∈ [0,1) with Pr(Ai) ≤ xi ∏_{ij∈E(G)}(1−xj) for all i, then Pr(∧_{i=1}^n Ā_i) ≥ ∏_{i=1}^n (1−xi) > 0", where the negative dependency graph means "Pr(Ai \| ∧_{j∈S} Āj) ≤ Pr(Ai) … for any subset S ⊆ {j \| ij ∉ E(G)}". | MATCH. The paper's version (p_i instead of Pr(E_i), plus E[W\|A_{S∪T}] ≤ ∏_T(1−x_j)^{−1}E[W\|A_S]) is a mild generalization, and its in-paper proof is the standard induction, which I verified. |
| Kakutani [24], via Lemma 3.3; used on pp. 64–65 | fixed point of a closed-graph, nonempty, convex-valued correspondence on a product of simplices | Duke Math. J. 8 (1941). projecteuclid returned HTML (`refs/initial_b_kakutani/k.pdf`). The standard statement (u.s.c. map of a simplex into closed convex subsets has a fixed point; it extends to compact convex sets) covers the use. | COULD NOT FETCH (use standard) |
| Lemma 3.8 / Dirr et al. [8] | cited as "related"; no statement imported | — | n/a (other seat) |

The Lemma 3.9 and 3.10 citations ([16], [23], [1], [15]) are in §3 proofs (other seat). §6–7 use only the in-paper statements, and I checked their hypotheses (O5, §3(c)).

### (h) Parameter-dependency table
| constant | fixed where | depends on | used where |
|---|---|---|---|
| c0 = .01, c1 = .005 | p. 52 | absolute | partner relation; tag restriction; common-hit mass |
| d_c = 300, coarse length n^{1/5}, bins ≤ 2n^{−.04} | p. 52 (from §5) | absolute | boundary fraction n^{−.05}; near-bin fraction n^{−12} |
| R_f = 5.5 | p. 52 | absolute | severity j; rarity n^{−.13q} |
| κ (tuple factor) | p. 53 | c1 | k = ⌈κJ log n⌉; budget coefficient < .002 |
| d2 ≪ κ; δ2; d1; δ1; d0 | p. 53 | κ, c1, d_c | Steps 1–3 caps and deletions; rarity sums |
| **D*** | p. 53 | d0 (2D* < d0), hence absolute | Π′ cutoff; η ≤ n^{2D*}Λ; §7's D0 |
| c2 = .001 | p. 58 | absolute | Step 3 alarm threshold; log D_n < c2k/2 |
| c3 | p. 58 | δ2 | hidden-stage charges |
| C (dependency exponent) | p. 58 | absolute | Cα < c3/4 |
| p0, γ, K (inputs of 6.1) | statement | — | α (via p0); n0 (via K, γ) |
| α | p. 53 | all above + p0 | m = n^α, J = m^{.04}, T = m^{.001} |
| ρ | p. 63 | absolute (H_bin(2ρ) < log 2 − .55, r ≤ d/4) | r = ⌊ρn⌋; even near fraction |
| λ = n^{10}; b, b0, a, θ, ζ, σ | p. 59 | α (b < .001α; see O7) | crowd ≤ T/2; short truncation |
| D0 ∈ Q | p. 64 | D* | (7.1); B_g; LLL charges n^{−D0/4} |
| d, b = d/4, c = d/80 | p. 64 | D0 | grid s = n^d, m = Θ(n^{2d}), q = n^{4d}; (7.1)'s n^{−c} |
| p0 = c/2, γ = 1/4, K = 4/κ_avail | p. 64 | c; availability tolerance | Lemma 6.1 application |
| K′ | p. 65 (Lemma 3.3 profiles) | tolerance of 7.1's family | Step 2 (Nα ≤ K′); load means |
| C (Steps 4, 6) | p. 67 | K′, absolute | Lemma 3.6 constant |
| B = 3, A*, P*, θ0 = 10^{−8} | p. 68 (Lemma 3.10) | absolute | odd injection |
| p (Lemma 7.1 input) | Cor. 7.2 | p = h/2 | own-test failure n²(q+1)e^{−n^p} |
| β = γ = d/4, h = d/(4·10^9) | Cor. 7.2 | d | P_pur, P_bias |
| η0 ∈ (0, min(d/4, h)] | Cor. 7.2 | d | (7.2) and everything downstream |

Dependency graph: absolute constants → D* → D0 → d → {b, c, h} → η0. K, K′ and κ_avail feed only n0. α depends on p0 = c/2, and nothing upstream of p0 depends on α. **No cycle.**

---

## 4. Verified line by line vs only skimmed

**Verified line by line** (every displayed inequality re-derived, every tool application checked against the hypotheses on the cited page):
- Claim (7.1) and its proof (p. 64), including the Lemma 6.1 interchanged budgets.
- Lemma 7.1, Steps 1–6 in full (pp. 64–68).
- Corollary 7.2 (p. 69), including the stabilization order, orientation and η0.
- Lemma 6.1:
  - statement; preliminary reduction and first case via Lemma 5.1 (pp. 51–52);
  - parameter paragraph and D* universality (p. 53);
  - Step 1 deletion bound and absolute cap (pp. 53–54);
  - Step 2 in full (p. 54);
  - Step 3 low targets in full (p. 56);
  - Step 3 high-target budget arithmetic (pp. 57–58);
  - §6.3 alarm halvings, global-parent unions, coarse and hidden LLL charges (p. 58);
  - local height selection: marking, maximality, D_n^n e^{−c2kn}, eligible-size loss O(n²T) ≪ λ (p. 59);
  - selected odd posteriors: cancellation, fallback, long/short coupling (pp. 59–60);
  - odd loads, all three stages (pp. 60–61);
  - additional even mean, cancellation through the "true I_h ∈ G_β" gate (pp. 61–62);
  - odd injection hypotheses (p. 62);
  - even reconstruction: F_z ≤ e^{.34kn}Q, Lemma 3.7 use, e^{.4kn}, H truncation, selection probability, even loads, Hall (pp. 62–63).

**Only skimmed or accepted as imported:**
- §6.2's structural facts about the quotient state (p. 55): bounded encoded distance D0 = 10, degree O(n), fringe merging, "O(j+1) exceptional states", "at most one adjacent low tuple and at most one nonmatching-primary tuple". These rest on §5.3 (O6). I verified only the descriptor counting that follows from them.
- Construction of H_loc for high targets (p. 57): I accepted "O(1) coarse bins and O(J) hidden scalars" after a sanity check of where the hidden keys come from (keys in C(h_b) × signs t_b or t_b^a with a ∈ F_b).
- The claim that, conditional on V0, every failure probability depends only on the abstract shape (p. 58). I checked the iid-given-V0 structure of (A_w, I_{(w,int)}, I_{(w,bdy)}) and the sign-translation invariance of π_ℓ, but I did not enumerate the finitely many coarse shapes.
- Lemma 5.1's inputs: Pr(j ≥ q) ≤ n^{−.13q} and boundary fraction ≤ n^{−.05} (p. 52, from §5).
- Internals of Lemmas 3.2–3.10, 4.1 and 5.1 (other seats). I checked their statements and every application's hypotheses.
- Well-definedness of a_ξ (the short-rule selection probability) as a measurable [0,1]-valued function of local data: assumed.

---

## 5. Verdict for scope

**HOLDS AS READ** for §6 (Lemma 6.1), §7 (claim (7.1), Lemma 7.1, Corollary 7.2), and the combination producing (7.2).

**COULD NOT CHECK:**
- the §5.3 state-geometry facts that the §6.2 descriptor counts rely on (O6, other seat);
- primary sources for Hall 1935 and Kakutani 1941 (paywall/Cloudflare; standard statements, uses verified).

Remaining objections O1–O5, O7 and O8 are COSMETIC/EXPOSITION; O6 is UNCLEAR only because it depends on §5.3. None of them changes a conclusion.
