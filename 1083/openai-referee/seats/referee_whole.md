# Referee report — WHOLE-PAPER seat (tag: whole)

Paper: OpenAI, "The higher-dimensional Erdős distinct-distances conjecture", 23 Sept 2026, /tmp/oaimath/166/paper.pdf (103 pp.; PDF page = printed page).
Scope: whole-paper hostile read aimed at the architecture: (1) hidden rates, (2) the induction and its base, incl. how strong the planar input must be, (3) the either-endpoint alternative of Theorem 6.1, (4) the classic holes (circularity, citations, hedge words), (5) real vs complex, (6) the global constant-dependency graph.

Method. I read §1.2–1.3, §2 and §5.1–§6.5 from the rendered PDF, §3, §4, §7 and Appendices A–B from the text extraction, rendering the PDF wherever a formula mattered. I wrote §§1–8 below **before** opening any other seat's report. Afterwards I read the verdict lines of the nine seats, sparse_a's objections and the Lean seat's planar-input section; §9 records where I agree or disagree. Numeric sanity checks (identities (2.6)–(2.8), both polarization identities, the Segre coefficients c(p,u) ≥ 0, every exponent in §7.5) are in `/tmp/oaimath/166/whole_scripts/checks.py`; all passed.

---

## 0. Bottom line

**I found no FATAL objection and no mathematical GAP in the architecture.**
- **Assembly (§2).** The §2 deduction is correct and rate-free, given Theorem 6.1, Theorem A.1 (a)/(b), Theorem 7.1 and Lemma 3.6. I checked it line by line.
- **Hidden rates.** Each of the 28 asymptotic steps I list in §2 is a genuine limit along the sequence. None needs a power saving, and none is a union bound over a super-polynomial family.
- **Pigeonholes over scales.** The one pigeonhole over a growing number of scales (Prop. 5.5) is defused. The paper bins the dyadic index *modulo* an integer m(h) → ∞, so for fixed h there are finitely many bins.
- **δ.** δ is never asked to beat an exp(o(s)) factor. It enters only where its plain vanishing suffices:
  - Prop. 4.3: the bound "NAE = δN²";
  - the choice of s_* with δe^{6s_*} → 0;
  - the pool size n₀ ≥ N√δ, used in §6.2 as √δ·M/A → 0;
  - Prop. 2.2: δ = 1/K_n.
- **The induction.** The planar distinct-distance theorem (B.12, Guth–Katz strength Ω(n/log n)) is consumed only through Corollary B.13, and always with polynomial room. Any planar exponent β > 2/3 suffices at d = 3 (β > 2/d in general). So §§B.4–B.7 (ruled surfaces, the two-rich theorem B.10, and n/log n) are off the critical path.
  - **However, the Guth–Katz higher-richness incidence theorem B.5 is consumed at full strength (exponent k⁻²).** The route is Cor. B.6 → Lemma 7.4 (planar type) → Theorem 7.1 → the d = 3 edge deletion → Lemma 2.5's isotropic cap. Through the induction it is therefore on the critical path for every d.
  - The lower-dimensional theorem (3 ≤ u < d) is consumed at full constant-factor strength at exactly one place: Prop. 2.2, case ℓ = 4, fibres in a (d−4)-flat, which only arises for d ≥ 7. The margin there is the rate-free M/A → 0. Every other use has polynomial room.
- **The either-endpoint alternative** is reduced to one orientation by an airtight pigeonhole (Prop. 5.5: "pass to an orientation containing at least half the covered pairs").
  - Every concrete covering I tried — lines, planar curves, products with a line, circles on spheres, quadric-cone rulings, pencils of planes, the lattice — is excluded either by an elementary occupancy count (Lemma 2.1 / Lemma 3.1) that Prop. 4.3 implements, or does not exist at all.
- **Citations.** The four heavy citations match their sources: Chardin; Chardin–Philippon Cor. 3 plus the erratum; Walsh Thm 1.3; Guth–Katz Thm 4.5 and Thm 2.10; Bardwell-Evans–Sheffer Thm 6.1. All of them are **re-proved in the paper**, so none is load-bearing as a citation.
- **Constant graph.** I found no cycle (table in §7).
  - The constants H, K, c, C, c₁, c′, c₂, c₃ depend on the hypothetical sequence. The paper says so: "fixed along the subsequence". That is legitimate for a proof by contradiction.
  - It does make c_d ineffective, which the introduction words loosely (Objection 2).

**Verdict: HOLDS AS READ.** The parts I only skimmed are listed in §8 with the seat that owns each.

---

## 1. Objections

**1. The planar input is over-strong: Guth–Katz Ω(n/log n) is never consumed. Guth–Katz's k ≥ 3 incidence theorem is.** — COSMETIC (exposition / scope). Not an error.
- Location: Lemma 2.1 (p. 7), its proof (p. 8), Cor. B.13 (p. 101), App. B §§B.4–B.7.
- Verbatim (p. 7): "We also use the planar result proved in Theorem B.12." … "Planes have the more precise bound B^{2+o(1)}."
- Verbatim (p. 8): "Thus, for example, c₀ = 1/2 works after advancing along the sequence."
- What is true: Corollary B.13 is consumed at exactly four places (grep of "plane cap", "B^{2+o(1)}", "Corollary B.13", "Theorem B.12"):
  - (a) Prop. 2.2, case ℓ ≤ 2, a ≥ 2. It needs ≤ O(A²), i.e. planar exponent β ≥ 1/2.
  - (b) Prop. 4.3, line case, p. 31: "CN B^{2+o(1)}(1 + log N)² = o(N²), using the plane cap and d ≥ 3". It needs β > 2/d.
  - (c) Prop. 4.3 with d = 3, p. 32: "these pairs cost o(N²) by the plane cap". It needs plane cap = o(N), i.e. β > 2/3.
  - (d) c₀ > 0 in Lemma 2.1. Any c₀ > 0 serves its consumers: Lemma 4.2 "η < c₀/4", Prop. 6.5 "B^{−c₀+o(1)}", and §6.3 "first-cut bound". This needs β > 2/d.
- So |Δ| ≥ c·n^β with any β > 2/3 serves the paper at d = 3. With β = 3/4: plane cap ≤ C·M^{4/3} ≤ C·B^{8/3} = N·B^{−1/3}, i.e. c₀ = 1/3.
- Consequence: the ruled-surface lemmas B.7–B.9, the two-rich theorem B.10 and the log-loss Theorem B.12 are needed only to supply something far weaker.
- **What is NOT off the critical path:** Theorem B.5 (Guth–Katz higher richness). p. 62: "The incidence inputs are the Szemerédi–Trotter bound, Theorem B.2, and the higher-richness Guth–Katz bound, Theorem B.5."
  - Its k⁻² exponent is critical in Lemma 7.4's planar-type count (p. 67): "#{planar-type motions} ≤ C (m⁴/ℓ²) Σ (hh′)^{−1/2} ≤ C′ m⁴/ℓ³ ≤ C″ m³/ℓ^{3/2}. The last inequality uses ℓ ≥ C_loc m^{2/3}."
  - Suppose (7.11) were only O((aa′)^{3/2}/u^{2−η}). Then the count is m⁴/ℓ^{3−η}. In Theorem 7.1's bottom bucket (t ≈ C_rich, so ℓ ≈ b ≈ βN^{2/3}, m ≈ 8N), the required bound K m³/ℓ^{3/2} fails by a factor N^{2η/3}.
- Fix: state Lemma 2.1 with any planar exponent > 2/3, or note that B.12 is used only at that strength. Mark B.5 as the indispensable Guth–Katz input.

**2. "The positive constant" is existential and ineffective. Part of the chain depends on the hypothetical sequence.** — UNCLEAR (exposition). True as a proof.
- p. 4, verbatim: "The sample uses one fixed probability, and all concentration constants are uniform; this is where the preceding quantitative estimates produce the positive constant in Theorem 1.1."
- p. 8, verbatim: "There must be fixed H, K and a subsequence on which a positive fraction of pairs survives." … "The positive constants c, C are fixed along the subsequence."
- What is wrong: H, K, c, C (Prop. 2.2) and, downstream, c₁ (2.3), c′ (Prop. 2.3), c₂ (2.4) and c₃ (2.5) are numbers attached to a counterfactual sequence. θ and the concentration constants are not; they depend on d only (§7 below).
- The contradiction needs only "fixed along the sequence", so the logic is sound. But the proof yields no explicit or computable c_d. Neither does any diagonal step in §5.4 or Prop. 2.2.
- Fix: say the constant is obtained by contradiction and is ineffective.

**3. The diagonal step of Prop. 2.2 is one sentence.** — COSMETIC.
- p. 8, verbatim: "Otherwise, a diagonal choice with H, K → ∞ sufficiently slowly would make the surviving fraction tend to zero, while the first, rich-line discard also has vanishing fraction."
- The negation used is: for every fixed (H, K), the surviving fraction tends to 0 along the whole sequence. One then takes H_n = K_n = k on [n_k, n_{k+1}), with n_k chosen so the fraction is < 1/k beyond n_k. No monotonicity in (H, K) is needed.
- I verified that this produces exactly the hypotheses of Theorem 6.1:
  - all but O(N²/H_n) + C·N·L_max = o(N²) unordered pairs are removed at an endpoint (L_max ≤ 2M = o(N));
  - deg C_p ≤ N/(K_n A) with δ = 1/K_n → 0.
- Fix: write the two lines.

**4. Theorem 6.1 is stated without the hypotheses it consumes.** — COSMETIC. Concurs with sparse_a O1.
- p. 42, verbatim: "Along a sequence with M = o(A), there cannot be families C_p …"
- The proof uses the least-failing-dimension bounds of Lemma 2.1: the flat cap, the plane cap, h_max = o(N) and the (k+1)-flat cap in §6.2. The preamble ("We retain the contradiction hypotheses, including the lower-dimensional induction bounds") supplies them, and the application on p. 8 is "In the regime (2.1)".
- Fix: state "in the regime (2.1)".

**5. Heavy notation overloading across sections.** — COSMETIC. No instance changes a proof, but several sit near load-bearing formulas:
- A: A = B² = N^{2/d} globally, but a large free constant in (B.1), p. 93: "where A will be chosen sufficiently large". It is also the local ring O_{π(X)} in Lemma 3.12, p. 25.
- B: N^{1/d}; also the plane cap B₀ (B.5); the branching vertices (proof of Lemma 7.5); the barriers B_h (A.5); the bundle B (A.15); the local ring O_{X,p} (Lemma 3.12).
- K: the greedy constant (Prop. 2.2), the deletion constant (Prop. 4.3), the number of grid indices (§5.1), C(t₁, …, t_k) (Lemma 3.6/3.8), K = C(X) (§6.3), K_h (A.5), the two-rich constant (B.10), and the bucket size (Lemma 7.3).
- c₀: Lemma 2.1's flat exponent vs Lemma 7.2's "at least c₀n² spanned lines". C₀: Theorem A.1's input vs Theorem B.5's uniform constant.
- M: 1 + |Δ| vs "L consist of M ≥ 1 distinct real affine lines" (Lemma B.9) vs "the remaining set of M ≤ m lines" (B.10).
- D: the testing degree vs a skew form D ∈ Λ²U* (A.28–A.29).
- δ: the sparse-cone degree factor vs δ(H) vs δ_i (A.3) vs δ₀ (Lemma 7.2).
- s: the window width vs the number of points s in B.5 vs the plane/regulus cap s in B.9/B.10.
- e: the dimension e in App. A vs e_j vs e_γ.
- Fix: rename locally.

**6. Prop. 5.5's outermost pool and its mass condition.** — UNCLEAR (exposition). Concurs with sparse_a O2/O3; I verified the same repair independently.
- p. 41, verbatim: "the two factors may instead be the same pool of pieces in a shrinking profile bin. That pool has size n ≥ N√δ".
- §6.2 needs the pool, and the refinement on p. 42 forces it: "If its mass is bounded below on a subsequence, work only there."
- The pool must also absorb the global o(N²) losses as o(n₀²). This works because the pool is a largest bin at precision h, of mass ≥ c(h)·N with c(h) independent of N. One then diagonalises h → ∞ with c(h) ≥ √δ.
- Fix: write n₀ ≥ max{N√δ, c(h)N} and diagonalise.

No other objection. In particular I have no objection at FATAL or GAP level.

---

## 2. Hidden-rate audit

The contract is that M/A → 0 and δ → 0 at no rate. I classified every asymptotic step I found by grepping "sufficiently large", "o(1)", "o(N", "o(n", "o(s)", "eventually", "subsequence", "tends to", "→ 0", "→ ∞" and "slowly" (paper_plain.txt; 202 o(·) tokens).

| # | Location | Asymptotic step | What it needs | Rate-free? |
|---|---|---|---|---|
| 1 | (2.1) p. 7 | N → ∞, M/A → 0 | definition | — |
| 2 | Lemma 2.1 p. 7–8 | flat ≤ N·B^{−c₀} "for all sufficiently large terms" | only M ≤ A eventually | ✓ |
| 3 | Prop 2.2 p. 8 | rich-line discard ≤ CN²/H + CN·L_max | L_max ≤ 2M = o(N) | ✓ |
| 4 | Prop 2.2 p. 8 | diagonal H_n, K_n → ∞ | for each fixed (H, K) the fraction → 0 | ✓ (Obj. 3) |
| 5 | Prop 2.2 p. 9 | "O(M^{d/2}), contradicting N/M^{d/2} → ∞" | N/M^{d/2} = (A/M)^{d/2} → ∞ | ✓ (no power needed) |
| 6 | §2.3 p. 11 | Σ_{k_g ≥ C_rich A} k_g² ≤ K_rich N⁴/A = o(N⁴/M) | M/A → 0 | ✓ |
| 7 | (2.5) p. 11 | δ(H)/A^{d−1} ≥ c₃ A/M → ∞ | M/A → 0 | ✓ |
| 8 | Prop 2.6 p. 13 | union bound N²·exp(−cθδ(H)) → 0 | δ(H) ≥ c₃N²/M ≥ c₃N^{2−2/d}: a fixed power, using only M ≤ A | ✓ |
| 9 | Prop 2.6 p. 13 | θδ(H)/2 > C·A^{d−1} | θ, C fixed; ratio → ∞ by #7 | ✓ |
| 10 | Lemma 4.2 p. 28–29 | exp(o(w)), w → ∞, w ≤ log B; t_H ≤ e·B^{−c₀/2}; sum exp(−εw+o(w)) + B^{−c₀/2}·exp(o(w)) | w → ∞ only | ✓ |
| 11 | Prop 4.3 lines p. 30–31 | NAE = δN²; N·B^{2+o(1)}·log²N = o(N²); L/s ≤ CM²/A² = o(1); total O(N²M²/A²) | δ → 0, M/A → 0, and a polynomial room | ✓ |
| 12 | Prop 4.3 d ≥ 4 p. 31–32 | KNME = KδMN²/A; ε²N ≤ 2CE | δ, M/A → 0 | ✓ |
| 13 | Prop 4.3 d = 3 p. 33 | N⁴/E² ≫ N³ | E = δN^{1/3} = o(N^{1/2}): power room | ✓ |
| 14 | Prop 5.1 p. 35 | s_* → ∞ "sufficiently slowly that … δ·exp(6s_*) → 0"; EL² = δN·e^{6s_*} = o(N) | s_* is adapted to δ, not δ to s_* | ✓ |
| 15 | Prop 5.1 p. 36 | (5.4) exp(−7a_i/18) → 0; (5.5) summable over all windows "even if s_* grows arbitrarily slowly"; thresholds a_1 = 10^{K−1}s^{1/10} = s^{1/10+o(1)} because K = O(√log s) | s ≥ s_* → ∞ | ✓ (no factor equal to the number of windows) |
| 16 | Prop 5.2 p. 37–38 | exp(o(s)) errors against strict profile margins | — | ✓ |
| 17 | Prop 5.3, Lemma 5.4 p. 39–41 | o(n) uniform over pieces ("sequence quantifier"); exp(o(s)) pieces per pool | uniformity by contradiction along sequences | ✓ |
| 18 | Prop 5.5 p. 41–42 | precision h → ∞ slowly; dyadic index binned **mod m(h)** | finitely many bins for fixed h | ✓ (the growing-scales pigeonhole is defused) |
| 19 | Prop 5.5 p. 42 | light-line threshold H → ∞ with H ≤ B^{o(1)}; O(N²/H + N·h_max) | h_max ≤ 2M = o(N) | ✓ |
| 20 | §6.1 (6.7) p. 46–47 | min(A/(δD_d), A/(δD₁D₂))·exp(−o(s)) → ∞ | strict margins c·s (b₁+b₂ < 0; s ≤ ½log B or b_d < 1). "No comparison between δ and an uncontrolled exp(o(s)) factor has been made" — confirmed | ✓ |
| 21 | §6.2 p. 47–51 | n₀ ≥ N√δ; E·B^{2−c+o(1)}/n ≤ C√δ·B^{−c+o(1)}; EM/n ≤ C√δ·M/A → 0; B^{d−k+1+o(1)} = o(n₀) using n₀ = N·exp(−o(s)) | products of vanishing quantities | ✓ |
| 22 | §6.3 p. 53–57 | R = B^{1+o(1)}; Markov fraction exp(−ηs+o(s)); q = B^{1/2} ≪ r = B^{1+o(1)}; cut degree B·exp(O(s)) = o(B·exp(τv)) since s = o(v) | v/s → 0 or → ∞ | ✓ |
| 23 | Lemma 6.7, (6.27) p. 58–59 | ratio ≥ δ^{−1}·exp(cs/3) → ∞ | strict margin c > 0; δ ≤ 1 only helps | ✓ |
| 24 | §6.5 (6.29) p. 60 | ratio O(δ·exp(−(η−ε)s)) → 0 | holds even at δ = 1 | ✓ |
| 25 | Theorem 7.1 p. 61 | absolute constants; "M ≤ A will be used only through the elementary line cap" | M ≤ A eventually | ✓ |
| 26 | App. A | finite inequalities, C = C(e, C₀) | none | ✓ |
| 27 | App. B, Cor B.13 | B^{2+o(1)} from M = o(B²) | none | ✓ |
| 28 | (2.1) final paragraph p. 13 | "if it did not, a sequence with ratio tending to zero would give (2.1)" | — | ✓ |

**Union bounds.**
- Prop. 2.6: over N² vertices.
- B.10: over ≤ m lines.
- Prop. 6.5 / Remark 6.6: none needed. The subcollection uniformity is deterministic once the Markov-row deletion is made: centres whose deleted mass is ≤ √α keep every fixed-mass subcollection.
- None of these is over a family of size exp(N^c).

**Bézout products against δ^{−1}.** None needs to beat δ^{−1}:
- EL² = o(N) is arranged by choosing s_*;
- (6.29) wins by exp(−(η−ε)s);
- §6.2 wins by B^{−c}.

---

## 3. The induction and its base

**Where each lower-dimensional input is consumed, and with how much room:**

| Input | Where consumed | Room |
|---|---|---|
| line ≤ 2M (u = 1) | Lemma 2.1; Prop 2.2 L_max; Prop 4.3 "Centers on their assigned target line … 2M Σn_i"; Prop 5.5 h_max; Thm 7.1 line cap (7.2) | elementary |
| circle ≤ 2M | Prop 2.2, fibre with d − ℓ = 2 (d ≥ 6); Lemma 2.1 | elementary |
| plane ≤ C·M·log 2M (u = 2, Cor B.13) | (a)–(d) of Objection 1 | needs only β > 2/3 at d = 3 (β > 2/d in general; β ≥ 1/2 for (a)) |
| 3 ≤ u < d: ≤ C_u·M^{u/2} | Lemma 2.1, c₀ (u = d−1: B^{d−1} = N·B^{−1}) | polynomial |
| | Prop 2.2, ℓ = 3 (d ≥ 4): ≤ C_3·A^{3/2} ≤ A² | A^{1/2} |
| | §6.2, carriers with span ≤ k+1, k ≥ 2: B^{k+1+o(1)}·B^{d−2k} = o(n₀) | B^{k−1} |
| | Prop 4.3, d ≥ 4: three-flat cap; Lemma 4.2 / Prop 6.5 tangent flats (c₀) | polynomial |
| | **Prop 2.2, ℓ = 4, d − ℓ ≥ 3 (only for d ≥ 7): fibres on spheres in a (d−4)-flat, total < 2M²·C·M^{(d−4)/2} = O(M^{d/2}) against N = A^{d/2}** | **none: full constant-factor strength, beaten only by the rate-free A/M → 0** |

- **The induction at full strength.** This is the only place where the induction is consumed at full constant-factor strength. It is legitimate: the least failing d makes the (d−4)-dimensional theorem available with its constant.
  - For ℓ ≥ 5 there is room M^{1/2}.
  - For 3 ≤ d ≤ 6, every use of the u ≥ 3 theorem has polynomial room.
  - I checked the arithmetic M^{2+(d−ℓ)/2} = O(M^{d/2}) ⇔ ℓ ≥ 4, and the fibre structure: |q−p| and π_U(q−p) fixed ⇒ q lies on a (d−ℓ−1)-sphere in a (d−ℓ)-flat.
- **No use of the dimension-d statement for a proper variety.** No bound on points in a proper variety uses the theorem in dimension d itself.
  - Lemma 3.1 (3.2), |P ∩ V| ≤ C_n·a·M^u, is proved from the separators s_p alone.
  - (5.8) and (6.17) are Bézout along the piece's own cut path.
  - Proper flats use only u < d.
  - So no lemma assumes the conclusion's strength.
- **d = 3, 4, 5 special cases.**
  - Lemma 2.5 needs an isotropic cap O(A^{d−2}). For d ≥ 4, N = A^{d/2} ≤ A^{d−2}, with equality at d = 4 (constant 1, which C₀ ≥ 1 absorbs). Only d = 3 needs Theorem 7.1.
  - d = 4: Prop 2.2 has ℓ = 4 ⇒ d − ℓ = 0 (fibre ≤ 1 point, total O(M²) = O(M^{d/2}), rate-free); §6.2 has k = 2 using the d = 3 theorem on 3-flats with room B. Nothing is missing.
  - d = 5: ℓ = 4 ⇒ fibres ≤ 2 points, O(M²) ≤ O(M^{5/2}). Nothing is missing.
  - d = 3: Prop 2.2 has ℓ ≤ 3 always, so the radius argument is never used and every curve is in P² (the greedy bound applies); Prop 4.3 has its own d = 3 branch with room N^{1/3}; §6.2 has k = 1 only.
  - I found no missing small-d case.
- **The Lean seat's claim** (a |Δ| ≥ c·n^{3/4} planar bound with c₀ = 1/3 suffices). **Confirmed from the paper's text**, with the qualification in Objection 1.
  - The paper's argument never consumes more than n^{2/3+ε} of planar *distinct distances*. Its four consumers are listed in Objection 1; the tightest is Prop. 4.3 at d = 3, which needs plane cap = o(N/log²N).
  - The paper first consumes genuine Guth–Katz strength at Lemma 7.4 (planar type), through B.5/B.6. That is the k ≥ 3 incidence theorem, not B.12.
  - Theorem B.10 and Lemmas B.7–B.9 are consumed only by B.12.

---

## 4. Theorem 6.1's either-endpoint alternative: counterexample attempts

**How the reduction works.** Prop. 5.5 selects a pair of pieces (or a pool) whose relative uncovered fraction → 0. It then does: "pass to an orientation containing at least half the covered pairs." A covering that uses the cheap endpoint for some pairs and the other endpoint for others therefore still yields a dense bipartite graph covered from the centre side. In the separated case both centre/target width orders are treated (v/s → 0 in (6.15) and §6.5; v/s → ∞ in (6.16)). In the common window the two pieces have the same limiting profile, so the orientation is symmetric. The global terminal deletion (o(N²)) is counted as "uncovered" *before* the selection, so it is relatively negligible in the selected pair. I found no hole in this reduction.

**Attempts.** For each I give the lemma that excludes it, and whether its proof visibly handles the example. E = δN/A.

| Attempt (d) | Covering | What kills it | Handled by |
|---|---|---|---|
| P on L lines, any d | C_p = the L projected lines | N ≤ 2M·L ≤ 2MδN/A ⇒ M ≥ A/(2δ) | Lemma 2.1 (u = 1); in the proof, Prop 4.3 line case: planes with S_H < A cost ≤ NAE = δN²; S_H ≥ A killed by (4.1) bh_H ≤ CM². Visible. |
| X × T, T an AP on a line (d = 3, or X ⊂ R^{d−1}) | lines through [e_d], one per x′ (\|X\| of them); vertical pairs on e_d | \|T\| ≤ 2M ⇒ \|X\| ≥ N/2M > δN/A | same as above (the carriers are the vertical lines). Visible. |
| P on L planar conics/circles, d ≥ 4 (also circles in d = 3) | one conic per curve, total 2L | Lemma 3.1: n_i ≤ CM·d_i, so per centre ≤ CME = o(N) | Prop 4.3 nonlinear: groups with W_{p,γ} ≤ KMe_γ discarded at cost KNME = o(N²). Visible. |
| circles through p on S^{d−1} (planes through p) | ≤ δN/A lines in P^{d−1} | circle ≤ 2M ⇒ M ≥ A/(2δ) | elementary circle cap. In the proof the targets' terminal curves need not be these circles; exclusion is by the label-rank comparison (Lemma 6.3/(6.6), or Lemma 6.7/(6.27)), which is structure-blind. Covered. |
| rulings of a quadric cone (d = 3) | projected rulings (lines) | each ruling ≤ 2M | Prop 4.3 line case. Visible. |
| pencil of K planes, plane curves from each p | plane curves in each Π_j, from p ∉ Π_j | curve ∩ plane-curve occupancy: per centre ≤ CM·Σe_j ≤ CMδB ≪ N (d = 3) | elementary (Lemma 3.1); the proof's rank comparison is structure-blind. Covered. |
| integer grid [B]^d (M ≈ dA, so the regime fails) | — | no sparse covering exists even at δ ≈ 1: rational planes through p of height ≤ h cover ≈ h²B² points with ≈ h³ planes; covering B³ (d = 3) needs h ≈ √B, i.e. ≈ B^{3/2} ≫ N/A = B planes | not applicable |
| hub set U with rich stars | — | pairs inside P∖U still need covering from inside | the pigeonhole above |

**Observations.**
- A configuration in which the targets' physical carriers are curves is killed by occupancy (Lemma 3.1 / 2.1), and the paper implements this in Prop. 4.3. That is why Prop. 4.3 together with the identification of the assigned terminal curve (§6.2 for k = 1, §6.5) closes the two zero-margin endpoints.
- A "genuinely conical" covering is excluded by the rank comparisons. There the cones over C_p are 2-dimensional and hold up to E·M² points each; with B ≪ M ≪ B² the counts above no longer bite. The comparisons are Lemma 6.3 against (6.6) in a common window, and Lemma 6.7 against (6.27) in separated windows. Their proofs depend on the example only through its profile.
- The spanning-≤-P² hypothesis on the curves matters only in Prop. 4.3 for d ≥ 4 (affine span ≤ 3) and for line components. I agree with sparse_a O5.

---

## 5. Classic holes, real vs complex, and hedge words

- **Circularity.** None found.
  - Lemma 3.6, the "component Hilbert lower bound at the defining degree", is proved from Lemma 3.3. That lemma gives separators of degree ≤ c(L−1) at isolated points via the Scheja–Storch-type determinant of Lemma 3.2. I checked the generic-fibre argument, (3.6) with q ≤ (n−k)(L−1), and (3.8). The bound is uniform in the component degree a; consistently, a ≤ C·L^{n−k} is forced by (3.5).
  - Theorem A.2 (Walsh) is proved from (3.7). Theorem A.1 is closed by the explicit barrier system (A.35). I checked that C(e, C₀) is fixed before κ, c₁, K_h and B_h (§7).
- **Hedge words.** "clearly", "similarly", "easily", "obvious" and "straightforward" each occur 0 times. "standard" occurs 6 times; each is benign (standard monomials, the standard diagonal choice, standard local algebra, the standard bilinear pairing, Borsuk–Ulam). "same argument" occurs once (§7.2.2 descent: the derivative has strictly smaller degree, so the iteration is well-founded). "It follows" occurs 5 times, all at routine steps. "generic" (154) and "uniform" (49) are pervasive. I checked:
  - the generic rotation R: finitely many conditions u + w ≠ 0, each R x ≠ −y a proper subvariety of SO(d); plus Theorem 7.1's "any rigidly congruent copy";
  - the generic projections in B.2, Prop 2.2 and Lemma 7.2 (they preserve existing incidences, which is all an upper bound needs);
  - the generic linear normalisation in Lemma 3.6;
  - every uniformity claim in §§5–6 that is load-bearing:
    - Prop 5.1 no-capture: exp(−7a_i/18) with a_i ≥ s^{1/10} ≥ s_*^{1/10}, uniform over pieces;
    - Prop 5.3: exceptional components removed by (5.8);
    - Prop 6.5 / Remark 6.6: a single Markov row deletion;
    - Lemma 6.7: the typical-centre set is chosen before ρ;
    - §6.5: "If their target mass were not o(\|P_y\|) uniformly …".
- **Real vs complex.** I found no error at any of these crossings:
  - Lemma 2.1, complex flats: real points of a complex affine flat span a real flat of real dimension ≤ the complex dimension.
  - Lemma 2.4: polarization over C applied to real representatives.
  - Lemma 2.5: λ is real because the vectors are real; the Gram-matrix isometry uses positive definiteness of the real norm.
  - Lemma 4.2: "every flat member is real" is required for the real slicing and Szemerédi–Trotter; Prop 5.3's last paragraph and Prop 5.5 discard nonreal flats and lines.
  - Prop 4.3: planes H are real (spanned by p and a real line); complex planar curves use the complex-flat cap.
  - Theorem 6.1 / Prop 2.2: curves are complex-irreducible and directions are real points of P^{d−1}(C).
  - Lemma 3.1: complex varieties, real sample.
  - §7: everything real.
  - App. A: everything complex, with real parameters.

---

## 6. Citation table (the four heavy citations; existence is left to the citations seat)

All sources were read at /tmp/oaimath/166/refs/. **Each of these results is re-proved inside the paper**, so the citations are attributions, not dependencies.

| Cited result | Paper's claim | Source, verbatim | Verdict |
|---|---|---|---|
| Chardin 1989 [6] (Lemma 3.6 upper bound (3.5)) | p. 17: "The upper estimate below is Chardin's Hilbert-function bound [6]." (3.5): H_V(D) ≤ a·C(D+k, k) | chardin1989.txt l. 101–105: "THÉORÈME. — Soient k un corps et R = k[X₀,…,X_n]. Soient I un idéal homogène E.G.R. de R, de dimension D > 0 … On a alors : H_I(ν) ≤ C(ν+D−1, D−1)·deg I" (OCR-garbled binomial, read against the standard statement). Affine dimension D = projective k + 1 | MATCH (and re-proved on p. 18 by hyperplane sections) |
| Chardin–Philippon [7, Cor. 3] + erratum [8] (Lemma 3.6 shifted bound (3.6)) | p. 17: "the shifted lower estimate follows from the isolated-component bound of Chardin–Philippon [7, Corollary 3]; see also their erratum [8]. We give the proof" | RI.txt l. 302–307: "Corollaire 3. Soit I un idéal homogène, engendré par des polynômes de degrés d₁ ⩾ … ⩾ d_m. Si J ⊇ I^{<r>} est un idéal de codimension r, on a, pour tout ν > d₁+⋯+d_r − r, H(A/J, ν) ⩾ deg J·C(ν+n−(d₁+⋯+d_r), n−r)." Same shift q = Σd_i − r ≤ r(L−1). Erratum, Err.txt: "the proof of the equivalence in the definition of (m, b)-regularity is not correct … Nevertheless, it does not affect the other results of the article since we only use the definition (∗)₀, except at one point where it can be easily repaired as explained in Remark A" (Remark A concerns Prop. 2) | MATCH. Cor. 3 is untouched by the erratum, so original and corrected statements agree, and the paper proves its own version anyway |
| Walsh [27, Thm 1.3] (Theorem A.2) | p. 75: "We prove Walsh's approximate complete-intersection theorem [27, Theorem 1.3]." Thm A.2: V irreducible of codimension c > 0 ⇒ nonconstant f_i ∈ I(V), V a component of Z(f₁…f_c), Π deg f_i ≤ C_n·deg V | Walsh1.txt l. 162–165: "Theorem 1.3. Let V ⊆ Cⁿ be an irreducible variety of dimension d. Then V is an irreducible component of Z(f₁,…,f_{n−d}) for some polynomials f_i with Π deg(f_i) ≲_n deg(V)." | MATCH (re-proved on pp. 76–77; I checked the (A.5) induction and (A.8)) |
| Guth–Katz [16] Thm 4.5 / Thm 2.10 (Thm B.5, Thm B.10) | B.5: "Let L be L distinct lines in R³, with at most B₀ in any affine plane. For every integer k ≥ 3, … R_k ≤ C(L^{3/2}/k² + L·B₀/k³ + L/k). There is no assumption about lines on quadrics." B.10: "at most s ≥ 1 in any plane or regulus … P₂ ≤ K(m^{3/2} + ms)" | GK.txt l. 948–953: "Theorem 4.5. Let k ≥ 3. Let L be a set of L lines in R³ with at most B lines in any plane. … \|S\| ≤ C[L^{3/2}k^{−2} + LBk^{−3} + Lk^{−1}]." l. 450–452: "Theorem 2.10. Let L be any set of N² lines in R³ for which no more than N lie in a common plane and no more than O(N) lie in a common regulus. Then the number of points of intersection of two lines in L is O(N³)." | MATCH (B.5 verbatim; B.10 is the s-uniform form of GK's §3 argument, re-proved on pp. 99–100) |
| Bardwell-Evans–Sheffer [4, Thm 6.1] (pair flats (2.6)) | p. 11: "Each F_{p,q} is the complexification of the corresponding real point-pair flat in the construction of Bardwell-Evans and Sheffer before their generic section [4, Theorem 6.1]." | BES.txt l. 1928–1936: "Theorem 6.1. Given a, p ∈ R^d, the flat η_d(T_{ap} ∩ Spun(d)+) is defined by … a₁ − p₁ = (a₂+p₂)x_{1,2} + ⋯ + (a_d+p_d)x_{1,d} + 2x_{1,d+1}, a₂ − p₂ = −(a₁+p₁)x_{1,2} + ⋯" — i.e. (a−p)/2 = X(a+p)/2 + c with X skew. The generic hyperplane section comes later (§7.2) | MATCH (attribution only; (2.6)–(2.8) verified directly and numerically) |

---

## 7. Global constant-dependency table

"seq" means the constant is a fixed number attached to the (hypothetical) contradiction subsequence; "profile" means it is fixed from the limiting profile (b_i) of the selected subsequence. Both are legitimate in a proof by contradiction.

| Constant | Fixed where | Depends on | Used where | Claimed independent of | OK? |
|---|---|---|---|---|---|
| c₀ (flat exponent) | Lemma 2.1 (c₀ = 1/2; 1/3 with an n^{3/4} planar input) | d, the planar exponent | Lemma 4.2 (η < c₀/4), Prop 6.5, §6.3 | N, δ | ✓ |
| C_u (u-flat cap) | Lemma 2.1 | c_u of the u-dimensional theorem (minimality) | Prop 2.2, §6.2, Prop 4.3 | N | ✓ |
| H (light-line threshold) | Prop 2.2, after the subsequence choice | seq | (2.2) base a = 0; C of (2.2) | N | ✓ (seq) |
| K (greedy factor) | Prop 2.2 | seq | (2.2), a = 1 in P² | N | ✓ (seq) |
| c, C (Prop 2.2) | p. 8, "fixed along the subsequence" | H, K, d (C doubles per dimension step a) | Prop 2.3 | N | ✓ (seq) |
| c_d (= c_{n,k} of (3.7)) | Lemma 3.6 | n, k only | (2.3), (2.9), §5, §6 | component degrees, L | ✓ |
| c₁ | (2.3) | C, c_d, d | Prop 2.3 maximal-set argument | subset S | ✓ (seq) |
| c′ = c/(1 + 2/c₁) | Prop 2.3 | seq | (2.4) | N | ✓ (seq) |
| c₂ = 2c′² | (2.4) | seq | (2.5) | N | ✓ |
| C_rich, K_rich | (7.15), §7.5 | absolute, chosen after η₂, η₁, K₃, C_loc, K_loc, α = 1/14, β = 1/(4K_part), ν = η₁/4 | §2.3 deletion; Lemma 2.5 cap (d = 3) | M/A, N | ✓ |
| c₃ ≈ c₂/4 | (2.5) | seq | final inequality θc₃A/(2M) > C | N | ✓ |
| C₀ for Lemma 2.4 | Lemma 2.4 | separator degree 4(M−1) ≤ 4A; caps N ≤ A^{d−1}, N² = A^d | Thm A.1(a) | seq, N | ✓ (absolute) |
| C₀ for Lemma 2.5 | Lemma 2.5 | separators of degree 2⌊A⌋; cap N ≤ A^{d−2} (d ≥ 4) or C_rich·A (d = 3) | Thm A.1(b) | seq | ✓ (absolute) |
| C(e, C₀) | A.5 | e, C₀ only (C → c₁ > 4C+4 → κ > 4Cc₁ → K_{r−1} ≥ max(2, C₀+1), K_h = κK_{h+1} → B₀ ≥ max(1, C₀), B_h = c₁K_hB_{h−1}) | Lemmas 2.4 and 2.5 | A, the sample P, the description degrees | ✓ — no cycle: "C depends only on e, C₀, not on the K_i" is true (incidence count O_e(1), Prop A.7's C_e and Lemma A.4's C_{e,C₀} are all K-free; the K_h factor is explicit in (A.32)) |
| C_n = γ_n^{−n}, γ_n ≤ min(1, a_n/(2ⁿb_n)) | Thm A.2 | a_n, b_n from (3.5) and (3.7) | (A.31), (A.33) | V | ✓ |
| L = O_n(1) (length bound) | Lemma A.5 (A.9) | C_n | regular-equation degrees O_n(D) | D | ✓ |
| c₄, C₄ | (2.9) | Lemma 2.4's C, Lemma 3.6's c, d | θ | seq | ✓ |
| θ < c₄/C₄ | Prop 2.6 | d only | sampling | N, seq, M/A | ✓ |
| η (Lemma 4.2) | p. 29, η < c₀/4 | c₀ | t_H bound | N | ✓ |
| ε (Lemma 4.2, Lemma 6.2) | "for every fixed ε" | free | root count exp(εw) | — | ✓ |
| K (Prop 4.3) | p. 32–33 | C of Lemma 3.1 (×24) | group discard | N, δ | ✓ |
| s_* | Prop 5.1 | the δ-sequence and B (s_* ≤ ¼log B, δe^{6s_*} → 0) | windows, core degree | — (a sequence, not a constant) | ✓ |
| widths s = 2^{−a}·log B ≥ s_*; their number ≈ log₂(log B/s_*) | Prop 5.1 | N | partition | — | ✓ ("No factor equal to the number of windows is used": verified in (5.5)) |
| thresholds N·e^{−√s}, B·e^{±s/2}, N·e^{−s^{1/3}} | Prop 5.1 | s | batches | — | ✓ |
| G = O(1+√log s), K = O_d(G), a_K = s^{1/10}, a_i = 10a_{i+1}, λ_i = e^{−a_i} | (5.3) | s, d | (5.4), (5.5) | pieces | ✓ (Σa_i = s^{1/10+o(1)} needs G = O(√log s); verified) |
| b_i, D_i = B·e^{b_i s}, e_j, σ | (5.6) | profile | §6 | — | ✓ |
| h (precision), m(h) (modulus), c(h) (largest-bin mass) | Prop 5.5 | h → ∞ slowly | selection | N for fixed h | ✓ |
| light-line H ≤ B^{o(1)} | Prop 5.5 | → ∞ slowly | §6.2 | — | ✓ |
| τ_eq < τ_test < τ; t₀ < t₁ < t₂; ε < (t₁−t₀)/4; ξ; c = 1 − t₂ (degrees B^{2−c}) | Lemma 6.2, (6.10), Lemma 6.4 | profile (β = b_j, b₁ + b₂) | §6.2 | N, δ | ✓ |
| η (Prop 6.5 slack), ρ (density) | §6.3 | free; "only the large-index threshold may depend on ρ" | depth deletions | ρ (typical set) | ✓ |
| q = B^{1/2}, r = ⌈B·e^{−2s}⌉, L ≥ max(L₀, B) | §6.3 | B, s | Sylvester / multiplicity compression | — | ✓ |
| c (Lemma 6.7) | from the margins (6.26) | profile | (6.25) vs (6.27) | N, δ | ✓ |
| b₀ < b_eq < b_test < b_d; η = b_eq − b₀; ε < η | §6.5 | profile | (6.29) | N, δ | ✓ |
| App. B: C (B.2, B.5), ε, θ, the constant "A" of (B.1), K > 98 (B.10), δ₀, γ₀, u₀ (Lemma 7.2), C₂, K₂, C₃–C₅ (Lemma 7.3) | App. B, §7.1 | absolute | §7, B.12 | everything | ✓ |
| K_part | Lemma 7.5 | absolute (volume packing) | β | r, N | ✓ |

- **Cycles:** none. The only feedback-shaped chains are the following, and both are acyclic:
  - §2: θ ← (c₄, C₄) ← (Lemma 2.4's C, Lemma 3.6's c), which is independent of c₃. The final inequality compares θc₃A/M → ∞ with Lemma 2.5's C, which is independent of H, K and c₃.
  - App. A: C → c₁ → κ → K_h → B_h, with C independent of K_h.
- **Dependence on N, δ or the window where independence is claimed:** none.
  - The seq-dependent constants are declared as such by the paper ("fixed along the subsequence").
  - The concentration and sampling constants that the paper calls "uniform" (θ, C(e, C₀), C_rich, K_rich, c_d) depend only on d.

---

## 8. Verified line by line vs only skimmed

**Verified line by line (by me):**
- **§1.2–1.3:** checked against §2.
- **§2 in full:**
  - Lemma 2.1 and its proof (c₀ = 1/2; the circle bound; complex flats);
  - Prop 2.2: the rich-line dyadic sum; the greedy charging; the diagonal; the induction on a, including the radius-class argument (L²/M − L ≥ L²/(2M) ⇔ L ≥ 2M), the section properness, the double count, the fibre count for ℓ ≥ 4, and the ℓ ≤ 3 cases;
  - Prop 2.3, including the maximal-independent-set charging;
  - (2.4); the §2.3 deletion and pruning;
  - (2.6)–(2.8), also numerically; the distinctness of flats;
  - Lemma 2.4: separator homogenisation and the isotropic-plane polarization;
  - Lemma 2.5: distinct parameters, separators, the Gram-matrix isometry, the d ≥ 4 and d = 3 caps, the hypersurface excess h = d−2 = r−1;
  - Prop 2.6: Markov, the rank bound, θ, Chernoff, the union bound, the final contradiction.
- **§3:**
  - Lemma 3.1; Lemma 3.2 (structure); Lemma 3.3 (divided differences, the adjugate argument, the functional λ); Lemma 3.5;
  - Lemma 3.6: (3.5) by sections, (3.6) by generic-fibre interpolation, (3.8), (3.7), and the projective version;
  - Lemma 3.8: the J functionals and (3.11); Lemma 3.9;
  - Lemma 3.10: the char-p Frobenius argument and the specialization; Lemma 3.11;
  - Lemma 3.15 (statement).
- **§4:**
  - Lemma 4.1: the generic part and the local assertion (6.12);
  - Lemma 4.2: all bounds;
  - Prop 4.3: the line case ((4.1), (4.2), the Hölder step and the dyadic sums), the d ≥ 4 nonlinear case (stabilizer count, Cauchy–Schwarz), and the d = 3 case ((4.4), (4.5) in both sub-cases, the invalid-triple weight, Hölder, N⁴/E² ≫ N³).
- **§5:**
  - Prop 5.1: (5.2), both batch kinds, the isolation degree B·e^{s/2+O(√s)}, EL² = o(N), the thresholds, (5.4), (5.5) summability, the size N·e^{−o(s)}, the imbalance;
  - Prop 5.2: Σb_i = 0 in both directions, (5.9) propagation, b₁ < 0 < b_d, b₁ + b₂ < 0;
  - Prop 5.5: core count O(EL²) per centre, the binning and diagonal, the mod-m(h) defusing, the outermost pool, the light lines.
- **§6:**
  - (6.5)–(6.7) and the margins; Lemma 6.3's induction (initial interval, h ≥ 2k+1, h = 2k with k = d−1 and with k < d−1);
  - §6.2: balance (6.9); (6.10); the carrier deletion B^{d−k+1+o(1)}; Lemma 6.4's first contradiction (strict margins t₀ − β and t₀ − 1 − b₁ − b₂); (6.29)-type exceptional mass; the row count E·B^{2−c+o(1)}/n; the lift argument; (6.12); EM/n;
  - §6.3: the narrower-window count (6.20) and R; the wider-window Sylvester rank drop ≥ r/2; Q of degree ≤ 2L² and multiplicity ≥ r/2 ⇒ a cut of degree O(L²/r) = B·e^{O(s)};
  - Lemma 6.7: initial interval A/T² and the three margins (6.26);
  - §6.5: the h ≥ 2 exclusion, (6.28), (6.29), the identification π_pY = γ.
- **§7:**
  - §7.2.3 planar-type sum;
  - §7.5: (7.15)–(7.25), all exponents (numerically), (7.19)'s derivation, (7.21), (7.22).
- **App. A:**
  - Theorem A.1's statement; Theorem A.2 with Lemma A.3 and the (A.5) induction;
  - Lemma A.4; the Segre expansion (A.24)–(A.26) with c(p,u) ≥ 0 (also numerically for p ≤ 60);
  - A.5: (A.31)–(A.35), the barrier inequalities, the maximality argument; the (b) hypersurface case where Alternative 2 is impossible.
- **App. B:**
  - B.1, B.2; B.5 (uniform version, (B.1)–(B.2), the √θ step, the induction on L); Cor. B.6; B.12; B.13;
  - the B.10 probabilistic step.
- **Citations:** the five rows of §6, at source.

**Skimmed only.** I read these, but did not re-derive every step. The owning seat is named.
- §3.6: Lemma 3.12 (blow-up intersection numbers, Artin–Rees), Cor. 3.13, Cor. 3.14 — algebra.
- §5.3: the proofs of Prop 5.3 and Lemma 5.4, in their pooled versions — §4–5 seat (running).
- §6.1: Lemma 6.2's generic-flatness fibre identification (Stacks 052A, 0559, 0C0E, 0B9T) — sparse_a.
- §6.2: Lemma 6.4's tangent-inequality minors — sparse_a.
- §6.3: the DVR specialization of the gcd and "at most q distinguished roots lie in the support of D₀"; Prop 6.5's first-cut bound — sparse_b.
- §7.1–7.4: Lemmas 7.2–7.7, the null-flat descent of §7.2.2, the Lemma 7.5 thickness/packing — motions.
- App. A: Lemma A.5 (derivation construction), Lemma A.6 (ruling incidences), the Prop A.7 tangent constraint, the singular skew pencil and local rigidity (pp. 86–88) — concentration.
- App. B: Lemmas B.3–B.4, B.7–B.9, the B.10 degree reduction, Lemma B.11 — incidence. B.7–B.11 are off the critical path in any case (Objection 1).

---

## 9. Comparison with the other seats (read after writing §§0–8)

- **No seat reports FATAL or GAP.** My reading agrees.
- **sparse_a.** O1 (Theorem 6.1's hidden hypotheses), O2/O3 (outer pool) and O5 (span ≤ P² used only through Prop 4.3) coincide with my Objections 4 and 6 and my §4 observation. I reached the same repair for O3 independently.
- **Lean seat.**
  - "App. B §§B.4–B.7 … are off the critical path … B.2, B.5 and B.6 remain on": I agree. My §3 traces this to the paper's own consumers, with the threshold β > 2/3.
  - "Theorem 7.1 does consume Guth–Katz higher-richness": I agree. I add that it is consumed at **full** strength. A k^{−2+η} bound fails at the bottom bucket t ≈ C_rich of §7.5 by N^{2η/3}.
- **motions seat O4** (Cor. B.6 could cite the published GK theorem): consistent with my citation row.
- **Disagreements:** none of substance.

---

## 10. Verdict for the whole paper

**HOLDS AS READ.**
- §2 is a correct, rate-free deduction from Theorem 6.1, Theorem A.1 (a)/(b), Theorem 7.1 and Lemma 3.6, which are consistently stated and used.
- There is no hidden rate on δ or M/A; every step in the §2 audit is a genuine limit.
- The induction is sound:
  - the full-strength lower-dimensional input enters only at Prop 2.2, ℓ = 4, d ≥ 7, with a rate-free margin;
  - the planar distinct-distance input enters only at exponent > 2/3;
  - Guth–Katz k ≥ 3 enters at full strength through §7 at d = 3.
- The either-endpoint alternative is disposed of by an airtight orientation pigeonhole.
- The four heavy citations match their sources and are re-proved in the paper.
- The constant graph is acyclic.

**COULD NOT CHECK (by me) line by line:** the items in §8's "skimmed" list, for lack of seat time. Each is owned by a seat that reports HOLDS AS READ; the §4–5 seat's report on Prop 5.3 / Lemma 5.4 was still running when I wrote this.

**Objections:** 6 total — 4 COSMETIC (1, 3, 4, 5) and 2 UNCLEAR (2, 6), all exposition. None is FATAL or a mathematical GAP.
