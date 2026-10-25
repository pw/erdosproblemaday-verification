# Referee report — seat `motions` — §7 (pp. 61–74) "Very rich rigid motions in three dimensions", and its consumption in §2.3 / Lemma 2.5

Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…). PDF page = printed page. Displayed formulas read from the rendered PDF (pp. 61–67, 71–74), not only from pdftotext.
Sources read (pdftotext of downloaded PDFs): Tidor–Yu–Zakharov arXiv:2608.14454**v1** (current version; abs page shows only [v1], submitted 14 Aug 2026) at refs/2608.14454v1/TYZ.txt; Guth–Katz arXiv:1011.4105**v3** (current) at refs/1011.4105v3/GK.txt; Bardwell-Evans–Sheffer arXiv:1705.10963**v2** (current) at refs/1705.10963v2/BES.txt; Elekes–Kaplan–Sharir arXiv:0905.1583**v1** (current) at refs/0905.1583/paper.txt; Elekes–Sharir arXiv:1005.0982**v1** (current) at refs/1005.0982/paper.txt. Beck [5] (Combinatorica 1983) and Elekes–Tóth [12] (SoCG 2005): COULD NOT FETCH (no open copy found) — neither is consumed as a black box (see table).
Own checks (scripts in /tmp/motions_scripts/, numpy, run under `nice -n 19`, < 2 s): (i) exact-fraction recomputation of every exponent in (7.16)–(7.25) and the two series; (ii) numerical verification on 200 random reversing motions of the flat geometry (7.6)–(7.9): pair flats and motion flats are maximal B-null 3-flats; F_{x,g(x)} ∩ G_g is a 2-plane (200/200); F_{x,y} ∩ G_g for random y≠g(x) is a point (200/200); planes from two different reversing motions both sending x↦y are distinct (meet in a line, 200/200); G_g is independent of the choice of adapted frame (200/200); three matched points give a transverse triple point (200/200).

---

## 0. Bottom line for this scope

Theorem 7.1 is **strictly stronger than anything in the cited literature** (it gives, for any P ⊂ ℝ³ with a 2N^{2/3} line cap, #{g : k_g ≥ k} ≤ K N^{10/3}/k² for all k ≥ C N^{2/3}, which is exactly the consequence that Tidor–Yu–Zakharov attach to their *Conjecture 7.13* and describe as "out of reach of these techniques"). I therefore tested the two steps that make it stronger, line by line:

1. **Lemma 7.4** (local bound K m³/ℓ^{3/2} for non-line-type ℓ-rich motions at ℓ ≥ C m^{2/3}) — this is the log-free analogue of TYZ Theorem 7.10, proved here by a joints-style degree-reduction argument for the two opposite families of null 3-flats instead of TYZ's partitioning machinery. Its hypothesis is "no line with η₁ℓ matched points, no plane with η₂ℓ" (planar type handled separately by the planar Guth–Katz count), **not** TYZ's curve condition. I checked every step; it holds.
2. **Lemma 7.5 + the mass count (7.19)** — a fat (cube / cube-with-one-dyadic-hole) partition of each cloud into O(r) regions with ≤ 8N/r points such that *any* rigid motion meets only K_part·r region pairs. Because the local bound m³/ℓ^{3/2} is not scale-invariant (exponent 3/2 < 2), counting *match mass* per region pair gains r^{−1/2}; with r = t^{1+α} this is exactly the t^{−1/28} margin in (7.19). Lemma 7.5's packing proof is correct (thickness (7.13) checked in all three cases), and the mass count is a valid double count.

I found **no mathematical error** in §7 and no hidden rate: every constant is absolute and chosen in a fixed order before N; the hypothesis M ≤ A enters only through the line cap (7.2). The use in §2.3 matches the statement exactly (both orientations, k_g = |gP ∩ Q| for Q = RP, deletion cost K_rich N⁴/(2A) = o(N⁴/M) using only M/A → 0), and the survivor property is precisely the isotropic cap Lemma 2.5 needs at d = 3.

Verdict: **HOLDS AS READ** (objections below are COSMETIC; the only things not checked by me are the in-paper proofs of Theorems B.2/B.5, which belong to the `incidence` seat — but the statements §7 uses match published results I quoted, so §7 does not depend on those in-paper proofs).

---

## 1. Objections

### O1 — Novelty relative to [26] is not disclosed; Theorem 7.1 proves what [26] calls conjectural and out of reach (COSMETIC, exposition; no math defect)
- Location: §7 preamble, p. 62: *"The physical and opposite-orientation flat families below are the rigid-motion geometry developed by Tidor, Yu, and Zakharov [26, Section 3]. We give the construction and every estimate needed here."* This is the only mention of [26] in §7.
- What [26] actually says (TYZ v1, p. 6): *"The polynomial method tools which we develop in Part I also apply to this problem, showing that there are at most k^{−3/2} N³ log^{3/2} N such τ. Unfortunately this bound is too weak for us to apply outright – it implies that the contribution to L₂(S) from k-rich orientation-reversing rigid motions is at most k^{1/2} N³ log^{3/2} N. For every k ≫ N^{2/3}, this is not strong enough to attain the bound of N^{10/3+o(1)}. We believe that this bound is not tight and later state a conjectured bound which would be strong enough to complete the proof (Conjecture 7.13). Unfortunately, this bound seems out of reach of these techniques."* And p. 61–62, Theorem 7.10: *"Let P ⊂ ℝ³ be a set of size N such that |P ∩ γ| ≤ N^{2/3} deg γ for every curve γ ⊂ ℂ³. For H ⊆ P² and k ≥ C N^{2/3} log N, … |T| ≲ N|H| log^{3/2} N / k^{3/2}."* Remark after Conjecture 7.13: *"This conjecture implies that for k ≫ N^{2/3} and any set P ⊂ ℝ³ of size N with |P ∩ γ| ≤ N^{2/3} deg γ for every curve γ ⊂ ℂ³, the number of k-rich partial symmetries of P is bounded by ≲ N^{10/3}/k². Such a bound is strong enough on its own to replace Part III."*
- Paper's Theorem 7.1 (p. 61): *"If M ≤ A, then the motions satisfying k_g ≥ C_rich A form a finite set and Σ_{g: k_g ≥ C_rich A} k_g² ≤ K_rich N⁴/A."* Since N⁴/A = N^{10/3}, this gives #{g : k_g ≥ k} ≤ K_rich N^{10/3}/k² for k ≥ C_rich N^{2/3}, under only a line cap (weaker than TYZ's curve hypothesis), with no logarithm — i.e. the consequence of TYZ Conjecture 7.13, and strictly stronger than TYZ Theorem 7.10 for every k ≫ N^{2/3}.
- Why it matters: the constant-factor claim in d = 3 *requires* the log-free form (a deletion cost N^{10/3}·N^{o(1)} would not be o(N⁴/M) when M/A → 0 slowly), so the d = 3 case rests entirely on this new bound. The paper never tells the reader that §7 goes beyond [26] or which step does it (Lemma 7.5 + mass counting, and Lemma 7.4's elementary proof). I tested both steps (§0, §4) and they hold; the omission is expository.
- Fix: one paragraph comparing Theorem 7.1 with [26, Theorem 7.10, Conjecture 7.13 and the remark following it], and naming the spatial subdivision as the new ingredient.

### O2 — §7.2.2 is the Guth–Katz / Elekes–Kaplan–Sharir joints degree-reduction transposed to null 3-flats; not attributed in §7 (COSMETIC)
- Location: §7.2.2, pp. 65–67 (*"We next show that every first partial derivative of f vanishes on every retained motion flat … Iteration implies that a nonzero constant derivative of f vanishes on a nonempty flat"*). [10] and [15] are cited only in Appendix B (p. 92).
- EKS [10] Corollary 13 (arXiv v1 p. 15): *"the number M≥k of points of P incident to at least k lines of L satisfies O(n^{3/2}/k^{3/2}) for k ≤ n^{1/3}"* — the exact one-dimension-lower analogue of Lemma 7.4's general-type count (m²)^{3/2}/ℓ^{3/2} (m² labels ↔ n lines). The "transverse triple point ⇒ df = 0" step is the joints step (∇f = 0 at a point on three non-coplanar lines in Z(f)), with the raised-gradient/maximal-null trick replacing non-coplanarity.
- Fix: cite [10], [15] at §7.2.2.

### O3 — Frame-independence of the motion flat G_g is asserted with an argument that addresses a different property (COSMETIC, exposition; statement true)
- Location: p. 65: *"The orthonormal coordinates used to describe a particular G_g are only a means of writing its equations: within the normalized orientation class under consideration, every flat is regarded in the same original parameter six-space. Simultaneous rotations (w, c) ↦ (Rw, Rc) preserve q, so the null properties just checked hold there for the whole family."*
- The cited fact gives null-ness after transport, not that (7.8) defines the same subset for every admissible adapted frame (rotation about the axis; reversal of the axis orientation with a compensating positively-oriented frame). It is true: from (7.6)–(7.7) one computes, for arbitrary (w,c) and x on the graph, (w×v+c−b)_⊥ = ((ω−w₃)v₂ + c₁+v₀w₂−d₁, (w₃−ω)v₁ + c₂−v₀w₁−d₂), so G_g = {(w,c) : the component of w×v(x)+c−b(x) orthogonal to the axis vanishes for every x ∈ ℝ³}, a frame-free description (given positive orientation for ×). I also verified (i) the in-plane frame rotation and (ii) the axis flip (U = rotation by π about e₂: ω↦−ω, v₀↦−v₀, d↦U_⊥d, equations preserved) by hand, and numerically (200/200).
- Fix: replace the sentence by the frame-free description.

### O4 — Corollary B.6 is used through the paper's own Theorem B.5; the published theorem it reproduces would suffice (COSMETIC / scope note)
- Location: §7.2.3, p. 67: *"Its proof uses the higher-richness Guth–Katz line theorem [16, Theorem 4.5] with a plane cap; that theorem has no regulus hypothesis."* Cor B.6's proof (p. 95) actually applies the in-paper Theorem B.5. The statement of B.5 matches GK Theorem 4.5 (quoted in the citation table) in hypotheses and conclusion, so (7.11) holds from the published theorem regardless of B.5's in-paper proof (not checked by me; `incidence` seat). I checked Cor B.6's reduction: Cayley chart (B.3), distinctness of the uv lines, the plane cap B₀ ≤ min(u,v), and the absorption of the LB₀/k³ and L/k terms for 3 ≤ k ≤ min(u,v).

### O5 — Minor wording points (COSMETIC)
- p. 66: *"We used ℓ ≤ m here; if this fails the motion bucket is empty."* — correct (ℓ ≤ k_g ≤ min(|X|,|Y|) ≤ m), and also needed to absorb the ceiling in T (K₃m³/ℓ^{3/2} ≥ 1); the second use is unstated.
- p. 69: the constant K_part is never evaluated; the packing gives ≤ vol B(3√3s/2)/(s/4)³ = (4π/3)(3√3/2)³·64 ≈ 4.7·10³ partners per charged region, times ≤ 38r charged regions. Absolute, as claimed.
- p. 61 statement includes the identity motion (k = N) in the sum; harmless (N² ≤ N^{10/3}).

No FATAL or GAP objection in this scope.

---

## 2. Theorem 7.1 as stated vs as used (§2.3, Lemma 2.5)

- Stated (p. 61): absolute C_rich, K_rich; P ⊂ ℝ³, N ≥ 2, A = N^{2/3}, M = 1+|Δ(P)|; if M ≤ A then {g : k_g ≥ C_rich A} finite and Σ k_g² ≤ K_rich N⁴/A; *"The same estimate holds with k_g = |gP ∩ Q| for any rigidly congruent copy Q of P."* Both orientations (S ∈ O(3)). The only use of M ≤ A: *"|P ∩ L| ≤ 2M ≤ 2A for every affine line L"* (7.2). Proved in the stronger two-cloud form (any X, Y, |X|,|Y| ≤ N, line cap 2A).
- Used (pp. 10–11): *"For d = 3, let g(x) = Sx + h, with S ∈ O(3) … V_g = {(p, g(p)) : p ∈ P, g(p) ∈ Q}, k_g = |V_g|. … Since M ≤ A eventually, Theorem 7.1 shows that the motions with k_g ≥ C_rich A form a finite family, with both orientations included. … The number of deleted edges is at most Σ_{k_g ≥ C_rich A} C(k_g,2) ≤ ½ Σ k_g² ≤ K_rich N⁴/(2A) = o(N⁴/M)."*
  - Q = RP is a congruent copy; |V_g| = |gP ∩ Q|: matches the last sentence of Theorem 7.1. ✔
  - A = B² = N^{2/d} = N^{2/3}, M = 1+|Δ(P)| — same normalisation as Theorem 7.1. ✔
  - "M ≤ A eventually" follows from M/A → 0; no rate used. K_rich N⁴/(2A) = o(N⁴/M) ⟺ M/A → 0. ✔ No rate.
  - Edges inside V_g: at most C(k_g,2) vertex pairs. ✔
- Survivor property (p. 11): *"After this deletion, no vertex can have at least C_rich A remaining neighbors which, together with that vertex, are matches of one spatial isometry."* If (p,q) had n ≥ C_rich A such neighbours (p′ᵢ,q′ᵢ) (distinct vertices ⇒ distinct p′ᵢ since q′ᵢ = g(p′ᵢ)), then k_g ≥ n+1 ≥ C_rich A and every edge (p,q)–(p′ᵢ,q′ᵢ) has both endpoints in V_g, hence was deleted. ✔ Pruning only deletes more. ✔
- Lemma 2.5, d = 3 (p. 13): neighbours whose local parameters lie in one maximal isotropic plane satisfy uᵢ·uⱼ = wᵢ·wⱼ (polarization (uᵢ−wᵢ)·(uⱼ+wⱼ)+(uⱼ−wⱼ)·(uᵢ+wᵢ) = 2(uᵢ·uⱼ−wᵢ·wⱼ), checked), hence are matches, with the centre, of x ↦ q + S(x−p), S ∈ O(3) possibly reversing — covered because Theorem 7.1 includes both orientations. So the cap is < C_rich A = O(A^{r−1}) with r = 2. ✔ Exactly what is needed.

---

## 3. Citation table (§7 scope)

| Cited result | What the paper says it says | What the source says (quote) | Verdict |
|---|---|---|---|
| [16] GK, Theorem 4.5 (arXiv:1011.4105v3, p. 21) — via Thm B.5 / Cor B.6, used in (7.11) | p. 67: "higher-richness Guth–Katz line theorem [16, Theorem 4.5] with a plane cap; that theorem has no regulus hypothesis." Thm B.5: L lines, ≤ B₀ in any plane, k ≥ 3: R_k ≤ C(L^{3/2}/k² + LB₀/k³ + L/k). | "Theorem 4.5. Let k ≥ 3. Let L be a set of L lines in ℝ³ with at most B lines in any plane. Let S be the set of points in ℝ³ intersecting at least k lines of L. Then … \|S\| ≤ C[L^{3/2}k^{−2} + LBk^{−3} + Lk^{−1}]." | MATCH |
| [26] TYZ §3 (arXiv:2608.14454v1) — flat families | p. 62: "The physical and opposite-orientation flat families below are the rigid-motion geometry developed by Tidor, Yu, and Zakharov [26, Section 3]." | Def. 3.6: "F^+_τ = {ρ ∈ E⁺ : τ ⋆ ρ = 0}"; Prop. 3.7: "the intersection F^Phy_ρ ∩ F^Phy_τ is either a single point or a 2-plane"; geometric reading: "x ∈ F^Phy_τ if and only if τ ∈ F^−_x if and only if τ(p) = q … ρ ∈ F^+_τ if and only if … ρ, τ agree on a plane." The paper's G_g is TYZ's F^+_τ for reversing τ = g, its F_{x,y} is TYZ's physical 3-plane in positive space (Cayley chart), and (7.9) is the 2-plane case of Prop. 3.7 (my numeric check: point or 2-plane, 200/200 each). | MATCH |
| [26] TYZ Theorem 7.10, Conjecture 7.13 (not cited by the paper) — comparison | (not mentioned) | quoted in O1: TYZ prove only \|T\| ≲ N\|H\| log^{3/2}N/k^{3/2} (k ≥ CN^{2/3}log N, curve hypothesis) and call the N^{10/3}/k² bound conjectural. | Theorem 7.1 is STRONGER than the cited literature (O1) |
| [11] Elekes–Sharir (arXiv:1005.0982v1) | p. 62: "The passage from equal-distance configurations to rigid motions is the Elekes–Sharir framework [11], used by Guth and Katz in the planar problem [16]." | Abstract: "We first describe a reduction from the problem of lower-bounding the number of distinct distances determined by a set S of s points in the plane to an incidence problem between points and a certain class of helices … the number of such rotations which map at least k ≥ 3 points of S to k other points of S is close to O(s³/k^{12/7})." | MATCH (framework attribution only) |
| [5] Beck — Lemma 7.2 | p. 62: "the following form of Beck's dichotomy [5], derived from Szemerédi–Trotter" | — | COULD NOT FETCH; not load-bearing: Lemma 7.2 is proved in full from Thm B.2 on p. 62 (checked, §4) |
| [12] Elekes–Tóth — Lemma 7.3 | p. 63: "motivated by the nondegenerate rich-plane bounds of Elekes and Tóth [12] … we do not invoke their theorem verbatim." | — (ACM DL only) | COULD NOT FETCH; not load-bearing: Lemma 7.3 proved in full (checked) |
| Thm B.2 (Szemerédi–Trotter rich-line form) — (7.3), (7.21), Lemma 7.3 | "#{L : \|L∩X\| ≥ u} ≤ C₀(n²/u³ + n/u), u ≥ 2", in ℝ³ "applied after a generic projection" | standard ST consequence; B.2 itself states "The same assertions apply to finite point–line configurations in ℝ^s" | MATCH with the classical statement (in-paper proof = `incidence` seat) |
| [10] EKS (arXiv:0905.1583v1) — not cited in §7 — comparison | — | Cor. 13: "M≥k … O(n^{3/2}/k^{3/2}) for k ≤ n^{1/3}" (joints-type k-rich points) | analogue of Lemma 7.4 general type; attribution missing (O2) |
| [4] BES (arXiv:1705.10963v2) — comparison only | — | BES treat only "k-rich points, for every 2 ≤ k = O(n^{1/d+ε})" (Thm 1.2) in a *generic hyperplane section*; very rich k ≥ n^{2/3+ε} dispatched via Solymosi–Tao: "m≥k = O(n^{4+ε}/k³ + n²/k). This bound is stronger than the required bound when k = Ω(n^{2/3+ε})." (p. 20) — slice points, not partial symmetries, with n^ε loss. | No Theorem-7.1-type statement in BES |

---

## 4. What I verified line by line

- **Theorem 7.1 statement, (7.2)** (line cap, sharper 1+2(M−1)); finiteness (k_g ≥ C_rich A > 2·2A ⇒ noncollinear matched triple ⇒ ≤ 2 motions per ordered source/target triple). ✔
- **Lemma 7.2** (p. 62): generic projection preserves points, noncollinear triples, line occupancies and spanned-line counts (collinear images ⇒ collinear preimages); dyadic sum Σ_u C₀(n²/u³+n/u)(2u)² ≤ C₂(n²/u₀ + δ₀n²); ≥ n²/(4u₀²) lines; averaging for anchors (|P′|(n−1) + c₀n² ≥ 2c₀n²). Projective version via generic chart. ✔
- **Lemma 7.3** (p. 63): case "richest line holds half" (H-rich lines O(m/H) for H ≥ √m; ≤ m/H planes per line); case 2: line in ≤ 2m/K bucket planes; J ≥ K²f²/m − 2Kf; upper bound split at C₃√K, a = O(√K) by (7.3) with |X∩Π| < 2K, total occupancy ≤ |X∩Π| + C(a,2) = O(K), contribution O(m) per Π; J ≤ C₅f(m+√K f); K^{3/2} ≥ 2C₅m gives f ≤ 2(C₅+2)m²/K². ✔
- **§7.2 constants**: 4η₂/γ₀ ≤ δ₀/2, η₁ ≤ min(η₂/100, δ₀/8); η₁ℓ ≤ δ₀n_g/2 for n_g ≥ ℓ/4; η₂ℓ ≤ δ₀γ₀ℓ/8 ≤ δ₀n′/2 for the direction set. ✔
- **Generic rotation** (p. 64): only S = −I has ker(I+S) ≠ line in the reversing component; bad sets are proper algebraic in irreducible SO(3); finitely many motions and triples. ✔
- **§7.2.1 (7.6)–(7.9)**: Cayley derivation b = w×v + c ⇔ (I+Z)y = (I−Z)x − 2c; null-ness of both direction spaces (q(δw,−δw×v) = 0; −v₀δw₁δw₂ + v₀δw₂δw₁ = 0); (7.7) incl. v₀ = h₃/2, b_⊥ = ωJv_⊥ + d, d = −(I+ωJ)h_⊥/2; (7.9) by direct expansion of w×v+c on G_g; dir(F)∩dir(G) is exactly 2-dimensional; reconstruction S_⊥ = (I−ωJ)(I+ωJ)^{−1}, h_⊥ = −(I+S_⊥)d (using I+S_⊥ = 2(I+ωJ)^{−1}), h₃ = 2v₀; distinctness of H_{g,x} (transformed coordinates), of incident planes in F_{x,y} (ωJ_a invariant under a ↦ −a), and of G_g. Numerically confirmed (see header). ✔
- **§7.2.2**: parameter count C(D+6,6)/C(D+3,3) ≥ D³/120; (7.10); T ≥ 1 absorption; pruning (each removal type < Tℓ/4); K₃^{2/3} > 4C₆ ⇒ Tℓ/(4m²) > D; f|_F ≡ 0 via > D distinct planes; raised gradient ∈ W^{⊥_B} = W for maximal null W; triple point ⇒ ∇_B f ∈ ∩ dir(H_i) = 0; anchors (≥ γ₀ℓ/4), c₇ℓ² = γ₀³ℓ²/16 spanned planes through an anchor, nonvertical by condition 2, graph duality to transverse triple points in H_{g,x}; incidence count gives ≥ c₈ℓ lines with ≥ c₈ℓ designated points; D < εℓ with ε < min(c₈/2, γ₀/8) iff ℓ^{3/2} ≳ K₃^{1/3}m/ε — the source of the m^{2/3} threshold; vanishing on lines → anchor plane → G_g → all retained F; iteration on all derivatives ⇒ f ≡ 0. ✔ Real throughout (no ℂ crossing in §7).
- **§7.2.3**: removal of richest lines loses < η₁ℓ each; e_X(Π), e_Y(Π′) ≥ η₀ℓ; Lemma 7.3 pair count K₂²m⁴/(h²h′²); (7.11) with u = k₀ ≥ 3, a < 2h, a′ < 2h′; ≤ 2 spatial extensions; Σ_{h,h′ ≥ η₀ℓ}(hh′)^{−1/2} = O(1/ℓ); m⁴/ℓ³ ≤ m³/ℓ^{3/2} ⟺ ℓ ≥ m^{2/3}. Cor B.6 reduction checked (O4). ✔
- **§7.3, Lemma 7.5**: L < r heavy leaves, B ≤ L−1, ≤ B+L chains, D_i ≤ 7μ, runs ∈ [μ, 8μ), D_i∪…∪D_j = Q_i∖Q_{j+1}, |R_X| ≤ r + 9(B+L) ≤ 19r; thickness (7.13) in all three cases (cube; hole disjoint from A₀; hole a strict descendant of A₀ ⇒ sibling child of side a/2 > s/4 within √3 s); charging to the smaller outer side, disjoint E's in B(c_R, 3√3s/2), absolute partner bound; (7.12). ✔
- **§7.4**: Lemma 7.6(1) ≤ 4 sign choices × 2 normal choices, translation = intersection of two nonparallel affine lines; 7.6(2) Sa = ±b, Sd = e, ≤ 4 linear parts, 1-parameter translation family, Σ_τ w₁ ≤ H², w₂ ≤ H; Lemma 7.7 (K_{2,3}-freeness from two circles, Σ d_z² ≤ 3q(q−1), (2e)² ≤ qΣd_z², superadditivity of x^{3/2}). ✔
- **§7.5**: α, β, ν; (7.15); r ∈ [1,N]; K_part rb = k/4; (7.17) exponent 9/14; (7.18) exponent 3/7 and q ≥ √N ⇒ N²/q³ ≤ N/q; (7.19) exponents N^{10/3}, t^{−1/28}; G₁: line-type mass ≥ k/2, W_g ≥ η₁k/4, pooling without repetition, w ≤ 2A, target line gL is q-rich in Y; (7.21); (7.22) needs W_g ≥ 4A ⇐ νC_rich ≥ 4; nonparallel ≤ 8·(2A)²·L*⁴; parallel L*²·O(L*^{3/2})·4(2A)³; (7.24) N^{8/3}t^{2/7}, (7.25) N^{19/6}t^{1/4}; series to t ≤ N^{1/3}: N^{58/21}, N^{13/4} (savings N^{−4/7}, N^{−1/12} vs N^{10/3}); decreasing series Σ_j (2^jC_rich)^{−1/28}; factor 4 from k_g < 2k; bucket coverage of [C_rich A, N]. All by exact fractions. ✔
- **Remark 7.8 and the §2.3/Lemma 2.5 consumption** (section 2 above). ✔
- **Hedge words in §7** (12 occurrences: 6× generic, 1× generically, 3× sufficiently large, 2× sufficiently small, 1× "It follows", 1× "The same argument", 1× eventually): each checked; each is either a finite set of proper algebraic conditions, an absolute-constant choice, or M ≤ A from M/A → 0.

## 5. What I only skimmed / did not check

- The in-paper proofs of Theorem B.2 (crossing-lemma ST) and Theorem B.5 (polynomial bisection + critical/flat lines) — `incidence` seat. §7 needs only their statements, which match ST and GK Theorem 4.5 (quoted).
- Beck [5], Elekes–Tóth [12]: not fetched; the paper proves the needed statements itself (Lemmas 7.2, 7.3), which I checked.
- I did not attempt an independent lower-bound construction search beyond hand tests (grid, planar grid, stacked planar grids, circle/helix, k-gon): none comes close to violating Σ_{k_g ≥ CA} k_g² ≲ N^{10/3} (all give O(N³ log N)). As a further consistency check, the proof's own method with the largest admissible r (≈ k³/N²) gives #{non-line-type g : k_g ≈ k} ≲ N⁴/k³, which is tight for the cube grid at k ≈ N and is the Szemerédi–Trotter-shape bound BES obtain (in a generic slice, with n^ε loss) — no contradiction found.

## 6. Constant-dependency table (§7)

| Constant | Fixed where | Depends on | Used where | Claimed independent of |
|---|---|---|---|---|
| C₀ | Thm B.2 / (7.3) | absolute | Lemmas 7.2, 7.3, (7.21) | everything |
| u₀, δ₀, γ₀ (c₀) | Lemma 7.2 proof | C₀ | §7.2 thresholds, anchors | N, clouds |
| C₂, K₂ (C₃, C₄, C₅) | Lemma 7.3 | C₀ | §7.2.3 | N, clouds |
| η₂, η₁, η₀ = η₂/2 | §7.2, p. 64 ("order of choices was η₂, η₁, then K₃, then C_loc, and finally K_loc") | δ₀, γ₀ | Lemma 7.4 types; ν = η₁/4; q = η₁b | N, clouds |
| C₆, K₃ | §7.2.2 | binomials; K₃^{2/3} > 4C₆ | (7.10), label degree > D | N, m, ℓ |
| c₇, c₈, ε | §7.2.2 | γ₀ | degree reduction in G_g | N |
| C_loc | §7.2.2–7.2.3 | K₃, C₆, ε, C₂, η₀ | ℓ ≥ C_loc m^{2/3}; (7.15) | N, m |
| K_loc | end of §7.2.3 | K₃, K₂, C of (7.11) | (7.19) | N, m |
| K_part | Lemma 7.5 | volume ratio: ≤ 38 × (4π/3)(3√3/2)³·64 ≈ 1.8·10⁵, absolute | (7.12), β | r, N, clouds, motion |
| α = 1/14, β = 1/(4K_part), ν = η₁/4 | p. 71 | K_part, η₁ | (7.16)–(7.25) | N |
| C_rich | (7.15) | β, C_loc, η₁, ν | Thm 7.1 threshold; §2.3 deletion; Lemma 2.5 cap (d=3) | N, clouds, rate of M/A |
| K_rich | end of §7.5 | C′, C″, series sums, factor 4 | §2.3 deletion cost | N, clouds, rate of M/A |
| r, m, b, q, L*, t, k | per bucket (7.16) | N, j | §7.5 | — (parameters, not constants) |

No cycle; every constant is fixed before N; nothing depends on M/A or on a rate.

## 7. Verdict for scope `motions`

**HOLDS AS READ.** Theorem 7.1 is stated and used consistently; every step of §7.1–7.5 checks, including the two steps that make it stronger than TYZ Theorem 7.10 and give what TYZ called a conjecture out of reach (Lemma 7.4's elementary joints-type proof under a non-line/non-plane hypothesis, and the fat spatial subdivision with mass counting). Objections O1–O5 are COSMETIC (missing comparison with [26], missing attribution to [10]/[15], a frame-independence sentence that argues the wrong property of a true statement, Cor B.6 routed through an in-paper reproof of a published theorem, minor wording). Not checked by me: the in-paper proofs of Theorems B.2/B.5 (statements match the published ST and GK Thm 4.5, so §7 does not depend on them); Beck [5] and Elekes–Tóth [12] COULD NOT FETCH, but neither is used as a black box.
