# Referee report — seat `incidence`: Appendix B (pp. 90–103), "Real incidence estimates" and the planar bound

Paper: OpenAI, "The higher-dimensional Erdős distinct-distances conjecture", 23 Sept 2026, `paper.pdf` sha256 37f6355365a18510e75d897dc9ab6d29305d7ff132cf148845b6f16d080ee1bf (re-checked). Formulas were read off the rendered PDF pages 90–101, not only the text extraction.
Primary source used for the step-by-step comparison: Guth–Katz, arXiv:1011.4105**v3** (28 Jun 2011, the current and last version; v1 17 Nov 2010, v2 24 Jun 2011), `refs/1011.4105v3/GK.pdf`. Also fetched: Elekes–Kaplan–Sharir arXiv:0905.1583v1 (only version), Guth–Katz "Kakeya" arXiv:0812.1043v1 (only version), Hatcher *Algebraic Topology* (author's PDF).

## 0. Bottom line

* Appendix B is a **proof, not a reduction**. Every result in it (Szemerédi–Trotter, polynomial partitioning, critical/flat lines, the Guth–Katz higher-richness theorem B.5, a flecnode-type Cayley–Salmon criterion B.7, the structure of ruled surfaces B.8–B.9, the two-rich-line theorem B.10, the planar Ω(n/log n) bound B.12) is proved in the text. The only things used without proof are the standard facts listed in the preamble on p. 90 (Bézout for common line components, unique factorization, implicit function theorem, Borsuk–Ulam, closed images of projective morphisms, dimension and generic-fibre-dimension theorems, extension of derivations). No step cites Guth–Katz for a hard part. Appendix B in fact proves **more** than Guth–Katz [16] do: GK cite the hard direction of the Cayley–Salmon theorem to Salmon without proof, and cite the critical-line and flat-line counts to EKS. Appendix B proves all three (Lemma B.7, Lemma B.4).
* I checked B.1–B.7 line by line, including every explicit constant. I found **no FATAL issue and no GAP**. All my objections are COSMETIC.
* **What is consumed is much weaker than what is proved.** The two-rich machinery (B.4–B.6) and the Ω(n/log n) bound (B.7) feed exactly one place: Lemma 2.1's plane row. That row is needed only when d = 3 (for d ≥ 4 the theorem in dimension 3 already caps planes), and only in the form "a plane holds ≤ N·B^{−c} points for some fixed c > 0". Any planar bound |Δ| ≥ c·n^{β} with **β > 2/3** suffices; Ω(n/log n) is never needed. The third-party Lean formalization reads the same way at source level. It replaces B.10–B.13 by a weak planar bound c·n^{3/4} (`ci_weak_planar_distances`), with plane occupancy C·M^{4/3} and flat-cap exponent c₀ = 1/3. It keeps the analogue of Corollary B.6 (`ci_planar_motions`). I read these statements in the source only; the kernel replay is a separate seat.
* The Appendix-B results that **are** consumed at full strength:
  * Theorem B.2 (Szemerédi–Trotter), in §2.2, §4.2, §4.3, §5.4 and §7.
  * Theorem B.5 / Corollary B.6 (the GK k ≥ 3 theorem with a plane cap, no reguli), in §7.2.3 → Theorem 7.1 → the d = 3 edge deletion.

  Both are proved in full in B.1–B.3, and I verified both.

## 1. Consumption table (done first, as the brief requires)

| # | Consumer (location) | Appendix-B result used | What the consumer needs (exact use) | Minimal strength sufficient | Slack |
|---|---|---|---|---|---|
| C1 | Lemma 2.1, u = 2 row, p. 7–8: "a real affine u-flat contains at most … CM log(2M), u = 2"; "The planar bound is Corollary B.13." | Cor B.13 ← Thm B.12 ← Thm B.10, Thm B.5, Lemma B.11 | Three downstream uses, C1a–C1c below. | — | — |
| C1a | Prop 2.2, p. 9: "It remains to consider ℓ ≤ 3. For a ≥ 2, Lemma 2.1 bounds the counted partners by O(A²), which is sufficient." | plane row (ℓ = 2) | plane occupancy ≤ C·A² = C·B⁴ | Erdős 1946's elementary n ≤ C·M² (|Δ| ≥ c√n) suffices, since M ≤ A | huge |
| C1b | Lemma 2.1, p. 7: "every proper real affine flat contains at most N B^{−c0} points"; consumed with any c₀ > 0 at §4.2 p. 28–29 ("Choose η < c0/4"), §6 p. 45 (B^{−c0+o(1)} fraction of centres in a tangent flat), and the "proper-flat cap" in §5–6. | plane row | d = 3: plane ≤ B^{3−c₀}. d ≥ 4: plane ≤ N·B^{−c₀}, which already follows from the **3-dimensional theorem** (plane ⊂ 3-flat ⇒ ≤ C₃M^{3/2} ≤ C·B³ = N·B^{−(d−3)}). | d = 3 only: planar |Δ| ≥ c·n^{β} with β > 2/3, giving plane ≤ C·M^{1/β} ≤ C·B^{2/β}, and 2/β < 3. | GK gives β = 1 − o(1) |
| C1c | "Planes have the more precise bound B^{2+o(1)}" (p. 7; restated p. 27). Consumed only at §4.3 p. 31 ("The contribution of N/s to hsF is at most CN B^{2+o(1)} (1 + log N)² = o(N²), using the plane cap and d ≥ 3"), p. 31 ("centers in its own plane also cost o(N²)") and p. 32 ("these pairs cost o(N²) by the plane cap"). | plane row | plane cap × log² N = o(N) | implied by C1b; the "more precise" B^{2+o(1)} is **never** needed | large |
| C2 | Prop 2.2, p. 8: "The rich-line consequence of Theorem B.2 therefore bounds the number of physical lines with at least t points by C(N²/t³ + N/t)"; dyadic sum O(N²/H) + o(N²) | Thm B.2 (rich lines), plus L_max ≤ 2M from the u = 1 row | Σ over t > H of #lines·t² = o(N²) as H → ∞ | any bound N²/t^{2+η} + N/t | yes |
| C3 | §4.2 Lemma 4.2, p. 29: "By the rich-line form of Szemerédi–Trotter, Theorem B.2, the number of these lines at dyadic occupancy t is O(e² exp(o(w))/t³ + e exp(o(w))/t)" | Thm B.2 (sliced, then projected) | sum over t ≥ e^{εw} of (count)·t²e^{−2} = o(1) | any power saving over t^{−2} | yes |
| C4 | §4.3 Prop 4.3 line case, p. 30–31: "The point-line estimate gives bhH ≤ C((bhH M)^{2/3} + hH + bM)", giving (4.1) bh_H ≤ CM², then (4.2) | Thm B.2 (incidence form, after a parabolic lift and a generic slice/projection) | the 2/3 exponents feed (4.1) and the Hölder sum | full ST as used (no slack checked; outside scope) | n/a (ST fully proved in B.1) |
| C5 | §5.4, p. 42: "Szemerédi–Trotter … summing its dyadic rich-line estimate gives O(N²/H + N hmax), and the proper-flat bound gives hmax = o(N)" | Thm B.2; h_max for lines ≤ 2M (u = 1 row, not planar) | as C2 | as C2 | yes |
| C6 | §7.1 Lemmas 7.2, 7.3, p. 62–63 ("Theorem B.2 gives (7.3)"), and §7.4 (7.20)–(7.21) | Thm B.2 (rich lines, also in RP² via a chart) | Beck-type dichotomy; O(m/H) H-rich lines for H ≥ √m | ST-level (not re-derived here; §7 seat) | n/a (proved) |
| C7 | §7.2.3, p. 67: "Corollary B.6 bounds the number of planar isometries giving at least u matches … by O((aa′)^{3/2}/u²)"; "Its proof uses the higher-richness Guth–Katz line theorem [16, Theorem 4.5] with a plane cap" | Cor B.6 ← Thm B.5 | #planar-type motions ≤ C·(m⁴/ℓ²)·Σ(hh′)^{−1/2} ≤ C·m⁴/ℓ³ ≤ C·m³/ℓ^{3/2}; the last step uses ℓ ≥ C_loc·m^{2/3} | **full** GK k ≥ 3 strength in the u-exponent: a bound (aa′)^{3/2}/u^{2−η} gives m⁴/ℓ^{3−η}, which exceeds m³/ℓ^{3/2} at ℓ ≍ m^{2/3} | none at the threshold scale |
| C8 | Lemma 2.1, u = 1 row and circle row ("2M"); Theorem 7.1's line cap (7.2) | elementary, proved in Lemma 2.1 / §7 (not Appendix B) | — | — | — |

Conclusions from the table:
* (i) **B.4, B.5 (as a section), B.6 and B.7 (as a section)** — i.e. Lemmas B.7–B.11, Theorems B.10, B.12 and Corollary B.13 — are load-bearing only through C1. C1 needs only a planar exponent > 2/3, and only in the least failing dimension d = 3. Székely's crossing-number n^{4/5} bound or the Lean's point–circle n^{3/4} bound would do. If B.4–B.7 contained an error, Theorem 1.1 would survive with this substitution.
* (ii) **Theorem B.5** (in section B.3) and **Corollary B.6** are load-bearing at full strength through C7, i.e. Theorem 7.1 and Lemma 2.5 in d = 3.
* (iii) **Theorem B.2** is load-bearing everywhere, and is proved.

## 2. Objections

No FATAL and no GAP. All objections are COSMETIC.

**O1 (COSMETIC, scope/attribution claim stronger than needed).**
* p. 2: "That bound supplies the two-dimensional input to our induction."
* p. 7: "Planes have the more precise bound B^{2+o(1)}."
* Figure 1 caption, p. 5: "Appendix B supplies the planar induction base".

What is wrong: nothing mathematical. As §1 shows, the induction needs a planar exponent > 2/3 only, and only at d = 3; the "more precise" bound is never consumed. A reader weighing risk should know that 7 of the 11 pages of Appendix B (B.4–B.7) are not load-bearing for Theorem 1.1.
Fix: none needed. One could state the minimal input in Lemma 2.1.

**O2 (COSMETIC, attribution).** p. 2: "their relation to the work of Szemerédi–Trotter, Beck, Elekes–Sharir, and Guth–Katz is recorded where each argument is used." Section B.7 (pp. 100–101) uses the Elekes–Sharir framework: rigid motions, the quadruple count Σa_ρ² = Σ_g k_g(k_g−1), lines in a 3-dimensional chart. But B.7 contains no citation of [11]; [11] is cited only on p. 2 and p. 62. B.7 also does not say that Lemma B.11 is Guth–Katz's Proposition 2.8 / Lemma 2.9 in different coordinates. GK v3 §2 has "Proposition 2.8. No more than N lines of L lie in a single plane. No more than O(N) lines of L lie in a single regulus." and "Lemma 2.9. Suppose that a regulus R contains at least five lines of L′p. Then all the lines in one ruling of R lie in L′p."
Fix: add the citations. No mathematical consequence.

**O3 (COSMETIC, notation collisions).** Appendix B reuses symbols that have fixed global meanings, though the preamble says "All constants in this section are absolute":

| Appendix-B symbol | Appendix-B meaning | Global meaning |
|---|---|---|
| A | large constant (B.5) | B² |
| B₀ | plane cap (B.5) | — (B = N^{1/d}) |
| D | partition degree | ⌊A⌋ |
| M | number of remaining lines (B.9, B.10) | 1 + \|Δ(P)\| |
| d | surface degree (B.7–B.9) | ambient dimension |
| H, K | H(m,s), the constant in B.10 | Prop 2.2's thresholds |

Within the appendix every use is local and consistent. I found no place where a global quantity leaks into an Appendix-B constant.

**O4 (COSMETIC, exposition).** Lemma B.4 proof, p. 92: "Square-freeness in characteristic zero implies that a generic constant linear combination of the first derivatives of f shares no irreducible factor with f." The statement is true, but the one-line reason is omitted. For each irreducible factor g of f = gh with g ∤ h, one has ∇f = h∇g on Z(g); some ∂ᵢg is not divisible by g, so some ∂ᵢf is not divisible by g; and finitely many proper linear conditions are then avoided. EKS give this as their Proposition 3.

**O5 (COSMETIC, wording).** Lemma B.3 proof, p. 92: "Replace each point in each of m finite sets by a disjoint small ball of the same radius within that set". A ball is not "within" a finite set. The intended construction is the union of small balls centred at the points, as in GK Corollary 4.4. The limiting argument that follows is correct.

**O6 (COSMETIC).** Theorem B.2 proof, p. 91: "Interchanging points and lines by planar projective duality proves the rich-line statement." The dual of an affine configuration lives in RP², so this step uses the projective form, which is proved in the last paragraph of the same proof. The order is awkward but not circular, and the text gives an independent direct argument: "One can instead apply the incidence bound directly to the finite collection of rich lines". I checked the direct argument.

**O7 (COSMETIC).** Lemma B.7, p. 95, states "at most 17d² affine lines". The proof gives d(17d − 24), which is < 17d², so the statement is consistent. The text says "the sharper flecnode degree used in that source is not needed here" (GK: "The polynomial Fl(p) is of degree 11d − 24"). Correct: Theorem B.10 only needs an O(d²) bound, used as b ≤ 18D².

I looked for, and did **not** find:
* a hidden rate (Appendix B is purely finite, with absolute constants);
* a constant depending on the configuration;
* a real/complex slip (handled in B.10, "A real line on a factor which is not real up to a scalar also lies on its distinct conjugate", and in B.9's restriction to real absolutely irreducible components);
* an upper/lower bound swap;
* a sentence citing GK for a hard step.

## 3. Step-by-step comparison with Guth–Katz [16] (arXiv v3)

### 3a. The two-rich-line theorem: Theorem B.10 vs GK §3 / Theorem 2.10

GK's statement (p. 11): "Theorem 2.10. Let L be any set of N² lines in R³ for which no more than N lie in a common plane and no more than O(N) lie in a common regulus. Then the number of points of intersection of two lines in L is O(N³)."
Paper's statement (p. 99): "Theorem B.10 (Two-rich points). For m distinct real affine lines, with at most s ≥ 1 in any plane or regulus, the number P2 of points lying on at least two lines satisfies P2 ≤ K(m^{3/2} + ms)". This is a mild generalization; B.12 uses m = n², s = 8n, which is GK's regime.

| Step | GK v3 §3 | Appendix B | Verdict |
|---|---|---|---|
| Induction frame | optimal counterexample in N ("assume that this is an optimal example"), cap rescaled | strong induction on m with **fixed** s and H(m,s) = m^{3/2} + ms | proved; cleaner, since no re-capping is needed because H(b,s) ≤ H(m,s)/4 |
| Pruning | "L′ … lines which intersect other lines of L in at least QN/10 different points" | delete lines with < T = (K/4)(√m + s) intersections; loss < mT = KH/4 | checked |
| Random sample | probability 100/Q | probability 64/K; witnesses distinct; Chernoff Pr(X < EX/2) ≤ e^{−EX/8}, derived explicitly; union bound m·e^{−2√m} ≤ e^{−2} | checked; numeric max of m·e^{−2√m} over m ≥ 1 is e^{−2} = 0.1353 |
| Degree reduction | R√Q·αN points per sampled line, polynomial vanishing on them | dimension count C(D+3,3) > q(D+1), D = ⌈√(6q)⌉, D < 4√q, D² ≤ 2048m/K, D < 8√m | checked; max ⌈√(6q)⌉/√q = 3.0 |
| Ruled/unruled split | p = p₁p₂ | factor over C; keep real, absolutely irreducible, geometrically ruled factors; non-ruled factors give ≤ 17dᵢ² lines; non-real factors give ≤ dᵢ² lines | checked; this handles the complex factors that GK leave implicit |
| Unruled line count | Cor 3.3: "> 11d² − 24d lines ⇒ p has a ruled factor", via **Prop 3.2 (Cayley–Salmon), cited, not proved**: "The reverse direction is more computational. It is indicated in a footnote to [Salm] Art. 588 page 278." | **Lemma B.7 proves it** (see 3b) | proved here, unlike GK |
| Singly-ruled structure | asserted: "Except for reguli and planes, every irreducible ruled surface (in R³) is singly-ruled. (See the explanation in Section 1)"; Lemma 3.5 / Cor 3.6 (≤ 1 exceptional point, ≤ 2 exceptional lines) | Lemma B.8 proves generic uniqueness of the generator, ≤ 1 exceptional point, ≤ 2 exceptional lines, and that every non-generator is exceptional | checked |
| Intersections in ruled surfaces | Lemma 3.4 via Salmon Art. 485 plane-section argument: "at most N − 1 non-exceptional points" per generator | Lemma B.9: generic complex plane H ⊃ ℓ, residual curve C_H of degree ≤ d − 1, with a regularity/closure argument at ℓ′ ∈ Γ_j; planes/reguli extracted with cap s; total 5dM + sM/2 | checked |
| Planes/reguli | "at most O(N³) points of intersection between lines of L4 because they lie in at most N planes and reguli each containing at most N lines" | inside Lemma B.9 (a_j ≤ s, a_j²/2 ≤ s·a_j/2, cross terms ≤ dM) | checked |
| Closing | optimality applied to L6 after re-capping | 6Dm + sm/2 + KH(b,s) ≤ (49 + K/4)H(m,s) < 3KH/4 for K > 98 | checked: 6·8 + 1/2 = 48.5 ≤ 49; (1/4)^{3/2} = 1/8 ≤ 1/4 |

Constants required of K: K ≥ 64 (probability ≤ 1), K > 32 (D < 8√m), K ≥ 147456 (36864m/K ≤ m/4), K > 98. All absolute.

### 3b. The ruled-surface criterion: Lemma B.7 vs GK Prop 3.2 / Cor 3.3

The criterion is flecnodal: V(u,v) = (Au, Av, −Bu − Cv) parametrizes the tangent plane where A = F_z ≠ 0, and R = Res(D²F[V,V], D³F[V,V,V]).
* Coefficient degrees are 3d − 4 and 4d − 6. The Sylvester determinant is of degree 3 in the quadratic's coefficients and 2 in the cubic's, so deg R ≤ 17d − 24.
* At A ≠ 0 a contained line gives a common root. At A = 0 the two forms are F_zz(Bu+Cv)² and −F_zzz(Bu+Cv)³, which share a root. So every contained line lies in Z(R).

The hard direction ("F | R implies ruledness") is proved by a Monge-type derivation argument in the algebraic closure of K = C(Z(F)):
* (a) Implicit differentiation gives D²F[(1,a,w)²] = −F_z·Q(a) and D³F[(1,a,w)³] = −F_z·P(a) − 3Q(a)(F_xz + aF_yz + wF_zz). Both are verified via Faà di Bruno with γ′ = (1,a,w), γ″ = (0,0,Q), γ‴ = (0,0,P).
* (b) The infinite slope is excluded after a linear change of (x,y) making t ≠ 0; q(0,1) = −A³t ≠ 0.
* (c) Simple root: D(Q(a)) = P(a) + 2(s+ta)Da. I re-derived this identity term by term, so Da = 0.
* (d) Repeated root: with s = −ta and r = ta², the mixed-partial identities give t(a_x + a·a_y) = 0. I re-derived both displayed lines.
* (e) Then D²x = D²y = 0 and D²z = Q(a) + z_y·Da = 0, so exp(TD) gives F(x+T, y+aT, z+wT) = 0. Closedness of the line–incidence image gives ruledness.

I also ran a symbolic sanity check (§7): on the ruled Whitney umbrella x² = y²z, R ≡ 0 on the surface; on the non-ruled Fermat cubic, R ≠ 0 at generic surface points but R ≡ 0 on the contained line (t,−t,1); deg R ≤ 17·3 − 24 = 27.

Verdict: a correct proof of a Cayley–Salmon-type theorem, which GK do not prove.

### 3c. Higher richness: Theorem B.5 vs GK Prop 4.7 / Prop 4.22 / Theorem 4.5

GK (p. 21): "Theorem 4.5. Let k ≥ 3. Let L be a set of L lines in R³ with at most B lines in any plane. Let S be the set of points in R³ intersecting at least k lines of L. Then |S| ≤ C[L^{3/2}k^{−2} + LBk^{−3} + Lk^{−1}]." B.5 has the identical statement.

The proof follows GK step for step:
* (B.1) is GK (4.1).
* r = ⌊θL²s^{−1}k^{−3}⌋ is GK's d.
* The cell claim is GK Lemma 4.8.
* (B.2) is GK Lemmas 4.9 and 4.20.
* The S∗ count is GK Lemma 4.13.
* The successful lines are GK Lemmas 4.17–4.18.
* The plane extraction is GK p. 30.
* The de-uniformization induction is GK Prop 4.22, with the same factor (20/9)(1/100)(10/9)³ = 0.0305 < 1.

Differences:
* B.3's cells are sign classes, so GK's connected-component cells are not needed. GK's cells are also sign classes ("the sets where the polynomials p1, ..., pJ have specified signs"), so this is consistent.
* B.4 proves the critical-line count (GK Lemma 4.19, cited to "[EKS] Proposition 3") and the flat-line count (GK Lemma 4.21, cited to "[EKS], Proposition 8").

I verified every inequality, including:
* the absorption order ε → θ(ε) → A(ε,θ);
* |S∖S∗| ≤ (ε + 3Cθ/A²)s;
* 800εL failing lines;
* critical + nonplanar-flat lines ≤ 4D² < L/400;
* B₀ ≥ L/(400D) ≥ c·sk³/L.

### 3d. The planar bound: Theorem B.12 vs GK §2

* Elekes–Sharir set-up in a Cayley chart c = (x−y)/2 − tJ(x+y)/2, with Z = tJ and R = (I+Z)^{−1}(I−Z) ∈ SO(2). Numerically verified (§7).
* Translations are included at t = 0. A generic R₀ excludes linear part −I, one rotation per motion, finitely many motions.
* Plane cap: if a = 0 the plane contains no such line; otherwise a·(x−y) = 2d and a·J(x+y) = 2b, with a and Jᵀa independent. Checked.
* Regulus cap (Lemma B.11): for fixed x the lines partition R³, are pairwise skew, and are tangent to W_x = (1+t², (tI+J)(c−x)). I verified the identity (tI+J)(I+tJ) = (1+t²)J and the tangency numerically. Bézout 2·3 = 6, then 7 lines force W_x·∇f = hf. The ODE (1+t²)g′ = hg has no real root unless g ≡ 0, so the whole ruling lies in the family; at most two values of x have ≥ 7 lines. Hence 6u + 2v. Checked.
* B.10 with m = n², s = 8n gives two-rich ≤ Cn³. B.5 with B₀ = n gives k-rich ≤ C′n³/k². Summing dyadically, Σ_g k_g(k_g−1) ≤ Cn³log(2n). Cauchy–Schwarz gives |Δ| ≥ c·n/log(2n). This is the full Guth–Katz Theorem 1.1, not something weaker.
* Corollary B.13: n ≤ CM log(2n) gives n ≤ C′M², which gives n ≤ C″M log(2M). Checked.

## 4. Citation table (Appendix B and the B-related citations in §1.1/§7)

| Cited result | What the paper says it says | What the source says (quote) | Verdict |
|---|---|---|---|
| [16] Thm 1.1 (p. 2) | "prove the planar bound Ω(n/log n) [16, Theorem 1.1 and Sections 2–4]" | "Theorem 1.1. A set of N points in the plane determines ≳ N/log N distinct distances." (v3 p. 1) | MATCH |
| [16, Theorem 4.5] (p. 67) | "the higher-richness Guth–Katz line theorem [16, Theorem 4.5] with a plane cap; that theorem has no regulus hypothesis" | "Theorem 4.5. Let k ≥ 3. Let L be a set of L lines in R³ with at most B lines in any plane. … \|S\| ≤ C[L^{3/2}k^{−2} + LBk^{−3} + Lk^{−1}]." No regulus hypothesis. | MATCH (and B.5 reproves it) |
| [16, Section 3, Prop 3.2, Cor 3.3] (p. 95) | "the flecnode approach to ruledness used in [16, …]"; "the sharper flecnode degree used in that source is not needed here" | "Proposition 3.2. The surface p = 0 is ruled if and only if Fl(p) is everywhere vanishing on it." "The polynomial Fl(p) is of degree 11d − 24." "Corollary 3.3. … Suppose that the surface contains more than 11d² − 24d lines. Then p has a ruled factor." GK also say: "The reverse direction is more computational. It is indicated in a footnote to [Salm] Art. 588 page 278." | MATCH (attribution only; GK do not prove the hard direction, while the paper does) |
| [16, Section 3] (p. 99) | "The sampling and degree-reduction argument follows the architecture of the two-rich-point proof in [16, Section 3]." | GK §3: "We now apply a degree reduction argument similar to the one in [GK]. … Now we select a random subset L′′ of the lines of L′ choosing lines independently with probability 100/Q." | MATCH |
| [16] partitioning (p. 92) | "Polynomial bisection is the Stone–Tukey ham-sandwich construction [22], as used in Guth–Katz polynomial partitioning [16]." | GK "Theorem 4.1. If S is a set of S points in Rⁿ and J ≥ 1 is an integer, then there is a polynomial surface Z of degree d ≲ 2^{J/n} … 2^J open cells Oᵢ, and each cell contains ≤ 2^{−J}S points"; "Theorem 4.3. (Stone-Tukey, [ST])" | MATCH |
| [15, 10] (p. 92) | "The critical-line and flat-line tests below are part of the algebraic incidence method of Guth–Katz and Elekes–Kaplan–Sharir" | GK-Kakeya 0812.1043v1: "Proposition 3.1. The set S contains no more than d(d − 1) critical lines." EKS 0905.1583v1: "Proposition 3 Any trivariate square-free polynomial p of degree d can have at most d(d−1) critical lines." "Proposition 8 Let p be any trivariate square-free polynomial of degree d with no linear factors. Then p can have at most 3d² − 4d flat lines." | MATCH (B.4 reproves both, with the weaker but sufficient 3D²) |
| [18, Corollary 2B.7] (p. 90) | "Borsuk–Ulam Theorem in its standard form that every continuous odd map S^q → R^q has a zero" | Hatcher: "Corollary 2B.7. For every map g : Sⁿ→Rⁿ there exists a point x ∈ Sⁿ with g(x) = g(−x)." For odd g this gives g(x) = 0. | MATCH |
| [22] Stone–Tukey (p. 92) | attribution of polynomial bisection | DOI landing (10.1215/S0012-7094-42-00925-6) returned an access stub | COULD NOT FETCH (attribution only; B.3 proves its own version from Borsuk–Ulam) |
| [23] Székely (p. 91) | "following Székely's crossing-number proof of the incidence estimate" | full text paywalled (CUP); the publisher abstract reads: "an old but not well-known lower bound for the crossing number of a graph yields short proofs for a number of bounds in discrete plane geometry … the number of incidences among points and lines" | COULD NOT FETCH full text (abstract consistent; attribution only; proof given in B.1) |
| [1] ACNS, [20] Leighton (p. 91) | crossing inequality | book chapter / monograph, not online | COULD NOT FETCH (attribution only; Lemma B.1 is proved) |
| [24] Szemerédi–Trotter (p. 90) | "historical sources" | Springer DOI returned a JS challenge | COULD NOT FETCH (attribution only; B.2 is proved) |
| [11] Elekes–Sharir | not cited in Appendix B although B.7 uses its framework | — | see O2 |

## 5. Constant-dependency table (Appendix B and its interface with §2)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Status |
|---|---|---|---|---|---|
| 64 in X ≥ e³/(64v²) | Lemma B.1, p. 91 | nothing (p = 4v/e) | B.2 | everything | verified |
| C in ST, C(L²/k³+L/k), C(n²/k³+n/k) | Thm B.2 | absolute (4, 32^{1/3}, the bounded-k threshold) | Prop 2.2, §4.2, §4.3, §5.4, §7, B.5 | configuration | verified |
| C in Lemma B.3 (degree Cr, Cr³ cells, C\|S\|/r³) | Lemma B.3 | absolute (binomial dimension count, 2^J ≍ r³) | B.5 | S, r | verified |
| D(D−1), 3D, 3D² | Lemma B.4 | explicit in D | B.5 | — | verified |
| ε, c_ε, C_ε, θ = θ(ε), A = A(ε,θ), C₀ | Thm B.5 proof | absolute, chosen in this order: ε ≤ 1/160000, then θ, then A | B.5, de-uniformization | L, k, B₀, S | verified; the induction keeps C₀ fixed since (20/9)(1/100)(10/9)³ = 0.0305 < 1 |
| C in Cor B.6 | Cor B.6 | 2·C_{B.5} (orientation split) | §7.2.3 (7.11) | U, V, k | verified |
| 17d − 24, 17d² | Lemma B.7 | d only | B.10 (b ≤ 18D²) | — | verified (degree formula and an example, §7) |
| ≤ 1 exceptional point, ≤ 2 exceptional lines | Lemma B.8 | — | B.9 | — | verified |
| 5dM + sM/2 | Lemma B.9 | d, M, s | B.10 | — | verified |
| K in B.10 | Thm B.10 | absolute: K ≥ 147456 and K > 98 suffice, with K ≥ 64 and K > 32 also needed | B.12 | m, s | verified |
| 6u + 2v; plane cap min(u,v) | Lemma B.11, Cor B.6 | Bézout 2·3 | B.12 (regulus cap 8n, plane cap n) | — | verified |
| c in cn/log(2n) | Thm B.12 | K, C_{B.5} | Cor B.13 | Q | verified |
| C, C′, C″ in CM log(2M) | Cor B.13 | c of B.12 | Lemma 2.1 u = 2 row | the set, the plane | verified |
| c₀ (= 1/2 claimed) | Lemma 2.1, p. 8 | fixed number; "after advancing along the sequence" only discards finitely many terms | §4–6 flat caps (any c₀ > 0) | N, δ, the window | verified for the B-dependent part (plane: CB²log B ≤ B^{3−1/2} eventually) |
| H (rich-line threshold), K (greedy constant) | Prop 2.2 | fixed after the diagonal argument | Prop 2.2 | — | only the B.2 input checked (outside scope otherwise) |

There is no cycle and no dependence on N, δ, the sequence or a window. Appendix B is purely finitary.

## 6. Verified line by line vs skimmed

**Verified line by line** (every displayed inequality and every constant):
* Lemma B.1.
* Theorem B.2, all four paragraphs: incidence bound, rich points, rich lines (both routes), higher-dimensional/projective transfer.
* Lemma B.3: ham-sandwich via Borsuk–Ulam on an (m+1)-dimensional coefficient subspace, ball-to-point limit, iteration, the line/cell count deg f + 1.
* Lemma B.4 (1)–(4), including the real-factor and conjugation handling.
* Theorem B.5: uniform version, de-uniformization induction, dyadic sum.
* Corollary B.6.
* Lemma B.7: degree count, "lines ⊂ Z(R)" at A ≠ 0 and A = 0, the derivation proof in both root cases, the closure argument, Bézout.
* Lemma B.8: dimension ≤ 1, covering, generic uniqueness, quadric/cone dichotomy, exceptional points and lines.
* Lemma B.9: both cases, including the C_H closure argument and the extraction of planes/reguli.
* Theorem B.10: every probability and degree estimate, the final count.
* Lemma B.11.
* Theorem B.12.
* Corollary B.13.
* In §2: Lemma 2.1's rows u = 0, 1, 2 and the circle claim; Prop 2.2's rich-line discard; Prop 2.2's sentence "For a ≥ 2, Lemma 2.1 bounds … O(A²)".

**Traced for consumption only (not verified; other seats):**
* §4.2 Lemma 4.2's flat-carrier count;
* §4.3's line-case Hölder computation and nonlinear-curve cases;
* §5.4 p. 42;
* the flat-cap uses in §6 (pp. 45, 50–51);
* §7.1 Lemmas 7.2 and 7.3;
* §7.2.3's planar-type sum (I re-did only the final exponent comparison m⁴/ℓ³ ≤ m³/ℓ^{3/2} ⟺ ℓ ≥ m^{2/3});
* §7.4 (7.20)–(7.21).

**Accepted without proof** (listed by the paper as standard, p. 90): Bézout for common line components (GK Lemma 3.1, EKS Prop 1), closedness of the Fano variety of lines and of incidence loci, closed images of projective morphisms, the dimension and generic-fibre-dimension theorems, derivations extending uniquely across separable algebraic extensions.

**Not fetched:** Stone–Tukey [22], Szemerédi–Trotter [24], ACNS [1], Leighton [20], Székely [23] full text. None carries load, because each is reproved in the appendix.

**Lean:** I read only the statements of `ci_weak_planar_distances`, `ci_planar_occupancy`, `planar_occupancy_sequence` (TrackC/WeakPlanar.lean) and `ci_planar_motions` (TrackC/Planar.lean) at source level, as corroboration of §1. I did not build or audit them.

## 7. Checks run (scripts in /tmp/oaimath/166/incidence_scripts/)

`checks.py` (nice 19) output, verbatim:
```
id1 0.0 (x3)                         # (tI+J)(I+tJ) = (1+t^2)J
cayley 2.2e-16 orth 2.2e-16 det 1.0  (x3)   # line (B.3) <=> y=(I+tJ)^{-1}((I-tJ)x-2c), rotation
Wx 5.6e-17 / 2.2e-16 / 0.0           # W_x tangent to the fixed-x family (Lemma B.11)
GK-induction factor 0.030483158055174524
B.10: 36864*4 = 147456  18*2048 = 36864  16*128= 2048
B.10: max m e^{-2 sqrt m} over m>=1: 0.1353352832366127 e^-2= 0.1353352832366127
B.10: tail exponent log2/2-1/2 = -0.15342640972002736  vs -1/8
B.10: max D/sqrt(q) = 3.0 (claim <4)
B.7 deg R: 3(3d-4)+2(4d-6) = [27, 44, 61, 78]  17d-24 = [27, 44, 61, 78]
B.10 final: 6*8 + 1/2 = 48.5  (<=49)  ; (1/4)^1.5 = 0.125
```
`flecnode.py` (sympy, nice 19), which builds R exactly as in Lemma B.7 (V = (Au, Av, −Bu−Cv), 5×5 Sylvester determinant):
```
umbrella: deg R = 24  bound 17d-24 = 27  R on surface = 0
fermat: deg R = 27
fermat: |R| at 3 generic surface points = [62011108239652.0, 2120855592.8768387, 284975946.6953349]
fermat: R on line (t,-t,1) = 0
```

## 8. Verdict for this scope

**HOLDS AS READ.** Appendix B proves, with absolute constants and no rate, the full Szemerédi–Trotter theorem, the Guth–Katz k ≥ 3 theorem (B.5), the two-rich-line theorem (B.10) and the full planar bound Ω(n/log n) (B.12, B.13). For the ruled-surface step it supplies a complete proof (Lemma B.7) that Guth–Katz themselves only cite to Salmon. No sentence imports a hard step from [16].

For the main theorem, the only Appendix-B inputs used at full strength are Theorem B.2 and Theorem B.5 / Corollary B.6 (the latter for d = 3 via Theorem 7.1). The two-rich/flecnode/Ω(n/log n) half (B.4–B.7) feeds only Lemma 2.1's plane row. That row needs just a planar exponent > 2/3, and only in the least failing dimension d = 3.
