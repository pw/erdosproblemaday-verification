# Referee report — seat `continua` — §7 "Extraction of common exclusion continua" (PDF pp. 42–51)

Paper: OpenAI, "The Euclidean plane is not five-colorable" (23 Sep 2026), /tmp/oaimath/158/paper/paper.pdf.
All quotations below are read off the rendered PDF pages (Read with `pages=`), not the text extraction.
Lean read as text only (no lean/lake run): /tmp/oai-math/oai-sparse/lean/OAI/Geometry/PlaneColoring/{PlanarCovers,Five,Mesh,FullApproximation,GraphPatches,GraphCuts}.lean.

## 0. Numbering correction to the brief (read this first)

The brief calls the planar cover obstruction "Lemma 7.2" and describes it as "a cover of the closed 5-disk". In the PDF:
- **Lemma 7.2** (p. 44) is *"Disk inequalities and support detection"* (the pointwise inequality (7.2)).
- The planar cover obstruction is **Lemma 7.5** (p. 47), and its domain is **"a closed square of side ten"**, not a disk.
- The *closed 5-disk* is the **Lean** domain (`Metric.closedBall (0:ℂ) 5` in Five.lean). Lemmas 7.5/7.6 of the brief = PDF Lemma 7.5 (cover obstruction) and Lemma 7.6 (non-null core loops).
Section map used below: §7 intro + Prop 7.1 (pp. 42–43), §7.1 Lemmas 7.2–7.3 (pp. 43–44), §7.2 (7.4) + Lemma 7.4 (pp. 45–46), §7.3 (7.6) + Lemmas 7.5–7.6 (pp. 46–48), §7.4 Lemmas 7.7–7.8 (pp. 48–49), §7.5 proof of Prop 7.1 (pp. 49–51).

## 1. Exact statement of the planar cover obstruction, paper vs Lean

**Paper, Lemma 7.5 (p. 47), verbatim:** "A closed square of side ten has no relatively open cover of multiplicity at most two and mesh at most two, where mesh is the supremum of the Euclidean diameters of its members."

**Lean, PlanarCovers.lean l. 374, verbatim:**
```
lemma compact_open_cover_impossible {ι : Type*} {Q : Set ℂ}
    (hQ : Metric.ball (0:ℂ) 5 ⊆ Q) (hQc : IsCompact Q) (U : ι → Set Q)
    (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z : Q, ∃ i, z∈U i)
    (hm : ∀ z : Q, ∀ i j l, z∈U i → z∈U j → z∈U l → i=j ∨ i=l ∨ j=l)
    (hd : ∀ i, ∀ x∈U i, ∀ y∈U i, ‖x.val-y.val‖≤2) : False
```
| item | paper Lemma 7.5 | Lean | same? |
|---|---|---|---|
| domain | closed square of side 10 | any compact Q ⊇ open ball B(0,5) | Lean is MORE general; the side-10 square (centred at 0) is compact and contains B(0,5) |
| openness | "relatively open" | `IsOpen (U i)` in the subtype topology of Q = relatively open | same |
| cover | cover | `hcov` | same |
| multiplicity ≤ 2 | "multiplicity at most two" (each point in ≤ 2 members) | among any three indices containing z two coincide (index-based, hence ≥ as strong) | same (the application supplies it index-wise) |
| mesh ≤ 2 | sup of diameters ≤ 2 (non-strict) | every pair in each U i at distance ≤ 2 (non-strict) | same |
| index set | arbitrary (proof takes finite subcover) | arbitrary `ι` (proof takes finite subcover via `isCompact_univ.elim_finite_subcover`) | same |
| proof | partition of unity, F = Σφ_a z_a, \|F(z)−z\| ≤ 2, Brouwer on z ↦ y+z−F(z) ⇒ F(Q) ⊇ {dist(y,∂Q)>2}, but F(Q) ⊂ finite union of segments | partition of unity, F = Σ w_i p_i, \|F z − z\| ≤ 2, continuous-log/winding on circle of radius 3 inside B(y,4) ⇒ B(0,1) ⊆ range F, but range F ⊆ finite union of affine lines (measure 0) | different proofs, same theorem |

**Use in Five.lean `graph_map_small_mesh_impossible` (l. 22–89).** F : C(closedBall 0 5, GraphSpace ⊤ on Fin 5). Hypothesis `hmesh`: every *preconnected* K ⊆ closedBall(0,5) on which coordinate i of F is positive has all pairwise distances ≤ 2. The cover is W(i, connectedComponentIn (U i) x) with U i = {z : 0 < (F z) i}. Supplied hypotheses:
- `hQ`: `Metric.ball_subset_closedBall`; `hQc`: `isCompact_closedBall` ✓.
- openness: `(hU _).connectedComponentIn`, using a `LocallyPathConnectedSpace Q` instance obtained from convexity of the closed ball ✓ (components of open subsets of a locally connected space are open).
- cover: Σ_i (F z)_i = 1 (`graphRealization_sum`) ⇒ some coordinate positive ⇒ z ∈ its own component ✓.
- multiplicity: `graphRealization_positive_three` (a point of the realised complete graph has ≤ 2 positive coordinates) + `heq` (two members with the same label containing z are both the component of z, hence equal as indices) ✓ — this holds at EVERY point of the ball, holes included, because F is graph-valued everywhere.
- mesh: `hmesh` applied to the image of a component, which is preconnected ✓.
So the Lean lemma states the same obstruction as the paper's Lemma 7.5 (with a disk in place of the square), and Five.lean supplies exactly its hypotheses. The contrapositive `graph_map_large_positive` then feeds `FullApprox.no_large_positive_sequence` (Mesh.lean), which is the paper's mesh argument in Lemma 7.6 written with preconnected sets instead of paths (`connected_escape_holes`, `straddle_connected_unit`) and threshold 2 directly (escape moves ≤ 2t ≤ 1/8, leaving distance ≥ 3/2 > 1; ball radius 1/8 about the limit point).

## 2. Objections and notes (numbered)

No FATAL and no GAP found in §7. Items below are COSMETIC / UNCLEAR or concern the brief / the Lean correspondence.

**1. (Brief, not paper) — numbering/domain.** See §0. Severity: COSMETIC (brief). Fix: refer to PDF Lemma 7.5, square of side ten; the 5-disk is the Lean's choice.

**2. (Brief test (E) is mis-scoped) — Lemma 4.3 IS on the critical path of Theorem 1.4.** The brief says "THE DENSITY-POINT CONVERSE is not needed for Theorem 1.1 … do not spend time there". Only the *use* of Lemma 4.3 in the converse transfer (proof of Thm 1.3, p. 26) is unneeded. Its first assertion — "the full-density-point set of each A_i contains no unit pair" (p. 25) — is used in §5.1, p. 26: "By Lemma 4.3, any unit pair of typical points has different colors", and through that in every exclusion of §7: Lemma 7.2 (p. 44) "Almost every such translation puts both points in the typical set. They cannot then both have color i; averaging proves (7.2)." Inequality (7.2) is the only route by which §7 turns continuum geometry into colour exclusions (Lemma 7.6 and the proof of Prop 7.1 both use it). I therefore read Lemma 4.3's proof (p. 25) line by line: x' uniform in B(x,h), u' uniform on an arc with |u'−u|<h; P(x'∉A_i)=o(1) by density at x; x'+u' has density ≤ 1/(πh²) supported in B(y,2h), so P(x'+u'∉A_i) ≤ |B(y,2h)∖A_i|/(πh²) = 4·o(1); hence both points lie in A_i with positive probability, and the pair law is absolutely continuous w.r.t. dx dσ(u) with |u'|=1 — contradicting the weak condition. VERIFIED; correct. Severity: n/a for the paper; the coordinator should tell the `transfer` seat its (E) instruction was wrong for this one assertion.

**3. Lemma 7.2 proof (p. 44) does not cite Lemma 4.3.** Quote: "Almost every such translation puts both points in the typical set. They cannot then both have color i". The reason (two typical points at unit distance have different colours) is Lemma 4.3 via the §5.1 definition of "typical". COSMETIC (exposition); correct.

**4. Lemma 7.8 proof (p. 49), quasi-component step.** Quote: "Intersecting this clopen set with the open set containing the original point gives a smaller clopen neighborhood omitting the other part, a contradiction." That C∩U is closed (it equals C∖V because C ⊂ U∪V and U∩V=∅) is not said. COSMETIC; the step is correct.

**5. Lemma 7.6 proof (p. 47), endpoint replacement.** Quote: "Replace either endpoint lying in a hole by a boundary point on the path. The path must exit that disk because the other endpoint is distant". Implicitly: the FIRST exit point; it lies on ∂D∩Q, hence (closures pairwise disjoint) outside every open hole, so g̃_n = q^{ε_n} there, and the sub-path keeps the i-th coordinate positive. COSMETIC; correct.

**6. Lemma 7.3 (p. 44): the cover is constructed for every ε; only the radius bound needs "for small ε each [square] lies in B′".** Quote: "Select all squares touching the displayed violation set in B″. Their number N_ε is finite, and for small ε each lies in B′". The covering property holds for all ε; the estimate N_ε ℓ² α²/4 ≤ ∫_{B′} p_i p_j = o(ε) needs squares ⊂ B′. Lemma 7.4 then uses ε_n small (ε_n ↓ 0) so this is satisfied. COSMETIC.

**7. The Lean does NOT formalise §7.4–7.5 as written (Lemmas 7.7, 7.8 and Proposition 7.1 in its stated form).** The Lean route (FullApproximation.lean, GraphPatches.lean, GraphCuts.lean, ContinuumLimits.lean) replaces: (a) the paper's merged, possibly eccentric core disks by fixed-radius `centerDisks (activeCenters L) R`; (b) the reduced-word argument (Lemma 7.7) and the annulus-crossing lemma (Lemma 7.8) by `crossingGraph` (edges ij whose midpoint fibre has a compact connected piece meeting both annulus circles, `FiberCrosses`) and `annulus_forest_extension` ("if the crossing graph is acyclic the annulus map extends over the disk", via `finite_fiber_separation` + `graphCut_contractible`); (c) Proposition 7.1 + §8 by `commonInterface_of_compact_sequence` + `commonInterface_graph_acyclic` + `eventually_forest_of_bridges`; (d) Lemma 7.6's "some core loop is non-null" by its contrapositive `HoleApprox.eventually_fill_cores` → `fullApprox_exists` (a graph map on the WHOLE closed 5-disk) and then the mesh contradiction. A grep of the PlaneColoring files finds no reduced-word, `FreeGroup` or fundamental-group development; "winding" occurs only in one docstring (GraphPatches.lean l. 117, "winding detour for the existential interface-cycle producer"), and the only lifting argument is the continuous logarithm in `PlanarCover.hit_center`. Consequence: a green kernel replay certifies the theorem but NOT the paper's Lemmas 7.7–7.8 / Prop 7.1 as stated; those rest on this hand check (§3, all VERIFIED). Severity: UNCLEAR (formalisation–exposition correspondence), not a gap in either.

**8. Test (B) within §7 — §7 is k-agnostic.** "Five" enters §7 only through (i) "Fix 0 < α < 1/5" in (7.4) (needed so the denominator Σ(p_k−α)_+ is positive: some p_k ≥ 1/k), (ii) 𝒢 = 1-skeleton of the simplex on five labels, (iii) "There are only finitely many simple cycles in the complete graph on five vertices … ℓ ∈ {3,4,5}". With six labels every line of §7 goes through verbatim with α < 1/6, K₆, ℓ ∈ {3,…,6}, PROVIDED the six-label analogue of Theorem 6.5 (closed locally finite cyclic-centre locus) holds. So whatever breaks at six lies in §5–6 (Theorem 6.5 is proved "separately for each triangle, four-cycle, and five-cycle", p. 37) or in §8 — not in §7. (The `palettes` and `cycles` seats own those.)

**9. Lemma 7.5 is far from sharp (finite check, informational).** At grid resolution h = 1/2 the discrete multiplicity-2, mesh-2 problem is already UNSAT on disks of inradius 0.707–2.0, where the lemma's hypothesis (an interior point at distance > 2 from the boundary) fails; part of this is coarse-grid artefact. Irrelevant to the proof (side ten is generous), noted only so nobody reads the "ten" or "2" as tight. COSMETIC.

## 3. Line-by-line status of every item in scope

| item (PDF page) | status | notes |
|---|---|---|
| §7 intro, def. (7.1) of Δ(K) (p. 42) | VERIFIED LINE BY LINE | min/max distance are 1-Lipschitz ⇒ Δ(K) open; K connected ⇒ q ↦ \|z−q\| has interval image containing values <1 and >1 ⇒ a point of K at distance 1 |
| Proposition 7.1 statement (pp. 42–43) | VERIFIED (statement read; consistent with its proof and with its use in Lemma 8.1, p. 51) | K_j ⊂ closed B(x,ρ) compact connected, x ∈ K_j, K_j∩∂B(x,ρ) ≠ ∅, q_{j,k} ∈ K_j∖{x}, q_{j,k}→x with directions → v_j, H_{i_j}∩Δ(K_j) = H_{i_{j+1}}∩Δ(K_j) = ∅; cycle need not be in Γ_x |
| §7.1 p_i^ε: nonneg., Σ=1, Lip ≤ C/ε, L¹_loc convergence (p. 43) | VERIFIED | \|p(q)−p(q′)\| ≤ \|B(q,ε)∖B(q′,ε)\|/(πε²) ≤ 2ε\|q−q′\|/(πε²); Lean uses 4/ε |
| Lemma 7.2 (p. 44) | VERIFIED LINE BY LINE | common translation v ~ U(B(0,ε)); a.e. v makes q+v, z+v typical; typical unit pair ⇒ different colours (Lemma 4.3) ⇒ P(both ∈ A_i)=0 ⇒ p_i(q)+p_i(z) ≤ 1 for EVERY unit pair (no exceptional pairs). Second assertion: p_i^{ε_n}(q_n)>0 ⇒ \|A_i∩B(q_n,ε_n)\|>0 and B(q_n,ε_n) eventually inside any neighbourhood of q ⇒ q ∈ H_i |
| Lemma 7.3 (p. 44) | VERIFIED LINE BY LINE | ij ∉ Γ_x ⇒ ∃ ball B centred at x with limsup D_ij(B,h)/\|h\| = 0 (negation of (6.1), D ≥ 0); ω(r) nondecreasing → 0; ∫_{B′}p_ip_j = E_{h1,h2}\|{q∈B′: c(q+h1)=i, c(q+h2)=j}\| ≤ D_ij(B,h2−h1) ≤ 2εω(2ε) via r=q+h1 ∈ B when ε < dist(B̄′, ℝ²∖B); grid side ℓ=c_αε with oscillation ≤ α/2 on a square; N_ε ℓ²α²/4 ≤ o(ε) ⇒ N_ε ε = o(1); open disk of radius ℓ about a square's centre contains the closed square (circumradius ℓ/√2); total radii N_ε ℓ = o(1) |
| (7.4) thresholding (p. 45) | VERIFIED | max_k p_k ≥ 1/5 > α ⇒ denominator > 0; q_i>0 ⇔ p_i>α |
| choice of Q (∂Q∩L=∅), Q′, L_0 (p. 45) | VERIFIED | L locally finite (Thm 6.5, assumed); for a point p, translations t with p ∈ ∂(Q+t) form 4 segments; finitely many relevant p |
| Lemma 7.4 statement + proof (pp. 45–46) | VERIFIED LINE BY LINE | M_δ = Q′∖∪B(x,δ) compact, M_δ∩L=∅ ⇒ Γ_z forest; per z one s_z for all nonedges (Lemma 7.3 with B=B(z,3s_z), B′=B(z,2s_z), B″=B(z,s_z)); finite subcover + Lebesgue number λ_δ; outside marked disks positive labels form a clique of the forest Γ_z ⇒ ≤ 2 positive coordinates ⇒ value in 𝒢 (in the realisation of Γ_z); merging: enclosing disk of radius ≤ (d+r1+r2)/2 ≤ r1+r2 when closures meet; ≤ (#disks) merges so errors < η; final boundaries avoid all original open disks; total radii ≤ \|L_0\|δ + m_{δ,ε} + η → 0; one core disk per point of L_0, positions w.r.t. Q from dist(L_0, ∂Q) > 0; non-core closed disk meeting Q lies in Q′ and in M_{δ_n}, has diameter < λ ⇒ inside one selected ball ⇒ boundary image in one tree of the forest ⇒ extends (trees contractible); pasting over finitely many closed sets agreeing on circles |
| §7.3 E(u,r), (7.6) (p. 46) | VERIFIED | π(1+r)²−π(1−r)² = 4πr; z ∉ E_n ⇒ no unit-distance point of z in any closed hole disk (core and non-core: H_n contains both) |
| Lemma 7.5 (p. 47) | VERIFIED LINE BY LINE + Lean statement compared (§1) + finite check (§4) | dist(z,Q∖U_a) partition of unity well defined since no U_a = Q (diam Q = 10√2 > 2); F(Q) ⊂ Q by convexity; F(Q) ⊂ finite union of segments; \|F(z)−z\| ≤ 2; for dist(y,∂Q) > 2, z ↦ y+z−F(z) maps Q into B̄(y,2) ⊂ Q; Brouwer (Hatcher Thm 1.9, checked) ⇒ F(z)=y ⇒ F(Q) ⊇ open square of side 6, impossible |
| Lemma 7.6 (pp. 47–48) | VERIFIED LINE BY LINE | null core loops ⇒ extend over core disks ⇒ g̃_n : Q → 𝒢 everywhere; components of U_{n,i} open & path connected (Q locally path connected); multiplicity ≤ 2 at every point; mesh > 1+c along a subsequence ⇒ path in U_{n,i} with ends > 1+c apart ⇒ (first-exit) endpoints outside all open holes with p_i^{ε_n} > α ⇒ limits a, b, \|a−b\| ≥ 1+c, a ∈ H_i (Lemma 7.2); small ball U about a: every z ∈ U straddles ⇒ path point w with \|z−w\|=1; z ∉ E_n ⇒ w outside closed holes ⇒ p_i(w) > α ⇒ p_i(z) ≤ 1−α ⇒ (7.7) α\|A_i∩U\| ≤ ‖p_i−a_i‖_{L¹(U)} + α\|E_n∩U\| → 0, contradicting a ∈ H_i; mesh ≤ 1+o(1) < 2 contradicts Lemma 7.5; also excludes "no core disk in Q" |
| Lemma 7.7 (pp. 48–49) | VERIFIED LINE BY LINE | covering tree (locally finite, degree 4 for K₅) gives unique reduced representatives, also for arbitrary continuous paths; cyclic trimming; conjugation acts by cyclic rotation (no double cancellation because W is cyclically reduced); W^d cyclically reduced uses every edge of W; G∖{m} deformation-retracts onto G minus that edge, so a loop avoiding m has a cyclically reduced word without that edge; shortest subloop between repeated vertices has length ≥ 3 (no loops; length 2 = reversal) and no repeated interior vertex ⇒ simple cycle |
| Lemma 7.8 (p. 49) | VERIFIED LINE BY LINE | x ∈ B open disk ⇒ each ray meets ∂B once at continuous r(θ) < ρ ⇒ 𝒜 ≅ closed annulus preserving angle; components = quasi-components in compact metric Z (proof checked, see Obj. 4); clopen partition Z = Z_1 ⊔ Z_2 with I ⊂ Z_1, O ⊂ Z_2 (empty cases handled); C_1 = Z_1 ∪ B̄ compact, inside open outer disk, disjoint from Z_2; grid cells meeting C_1 (x on no grid line) ⇒ C_1 ⊂ int V, ∂V ⊂ int 𝒜 ∖ Z; cancelled cell boundaries = balanced chain on ∂V = union of closed loops with total winding 1 about x ⇒ one loop with winding d ≠ 0, freely homotopic in 𝒜 to (inner circle)^d, image avoids m, contradiction with Lemma 7.7 |
| Proof of Prop 7.1: subsequences, fixed x, ρ (pp. 49–50) | VERIFIED LINE BY LINE | pigeonhole on finite L_0∩Q; x ∈ int Q since ∂Q∩L=∅; ρ fixed before n; other core disks ⊂ B(y,2r_n) eventually disjoint from B̄(x,ρ); g_n defined on 𝒜_n (non-core holes inside 𝒜_n are tree-filled) |
| W_n, simple cycle, ℓ ∈ {3,4,5}, K_{n,j} (p. 50) | VERIFIED | non-null ⇒ W_n nonempty; finitely many simple cycles in K₅ ⇒ subsequence with one cycle; Lemma 7.8 per edge midpoint |
| Hausdorff limits K_j, compactness, connectedness, x ∈ K_j, outer contact (p. 50) | VERIFIED | Blaschke (sketched correctly); limit of connected compacta connected (argument correct); contact points on ∂B_{n,x} → x since x ∈ B_{n,x} and diam → 0 |
| Exclusion of BOTH endpoint labels from Δ(K_j) (p. 50) | VERIFIED LINE BY LINE | on K_{n,j} outside holes g_n = q^{ε_n} = m_j ⇒ both endpoint coordinates 1/2 ⇒ p_i > α for i ∈ {i_j, i_{j+1}}; closed ball U ⊂ Δ(K_j) has uniform margin; extrema move ≤ d_H(K_{n,j},K_j) ⇒ straddle for large n; connectedness ⇒ w ∈ K_{n,j} at distance 1; z ∉ E_n ⇒ w outside closed holes ⇒ p_i(z) ≤ 1−α ⇒ \|A_i∩U\| = 0 ⇒ H_i∩Δ(K_j) = ∅. Same argument works for both labels simultaneously (same K_{n,j}, same w) |
| radii [0,ρ], q_{j,k}, v_j (pp. 50–51) | VERIFIED | connected image of q ↦ \|q−x\| contains 0 and ρ; points at radii ρ/k; compactness of S |
| Lemma 4.3 (p. 25; out of scope but load-bearing here) | VERIFIED LINE BY LINE | see Obj. 2 |
| Theorem 6.5, Definition 6.1, H_i | ASSUMED (palettes seat's scope); Def. 6.1 and H_i read | §7 uses only: L closed and locally finite; z ∉ L ⇒ Γ_z acyclic; ij ∉ Γ_z ⇒ (6.1) fails at z |

### Test (F) within §7 — checklist
- **Compactness on compact spaces:** closed square Q (Lemmas 7.5, 7.6); M_δ (closed, bounded); Z = g^{-1}(m) ⊂ compact 𝒜; hyperspace of nonempty compacta of B̄(x,ρ) (Blaschke); S for v_j. All genuinely compact. ✓
- **Connected vs preconnected vs path connected:** Lemma 7.6 uses PATH-connected components, legitimately (Q convex ⇒ locally path connected ⇒ components of relatively open sets are open and path connected); Lemma 7.8 / Prop 7.1 use compact CONNECTED components and their Hausdorff limits (connectedness of the limit proved); Δ(K)'s unit-distance property needs only connectedness. The Lean uses `IsPreconnected` throughout (weaker, sufficient: intermediate values on preconnected sets). ✓
- **"The disk of radius 5":** paper domain = closed square of side 10; Lean domain = closed disk of radius 5 (Lemma needs only a disk of radius > 2 inside, Lean uses B(y,4) for \|y\|<1). ✓
- **≤ 2-fold overlap EVERYWHERE:** g̃_n is 𝒢-valued at every point of Q: outside holes by Lemma 7.4.2, on non-core holes by tree fillings, on core disks by the null-homotopy fillings. A point of 𝒢 has ≤ 2 positive coordinates, and components of one U_{n,i} are disjoint. ✓
- **Diameters ≤ 2 of connected components:** mesh ≤ 1+o(1) proved for components of each U_{n,i}. ✓
- **Exceptional sets / order of choices:** §7 has no "almost every" over choices: (7.2) holds for every unit pair; the A_i are fixed Borel representatives and H_i is representative-independent; E_n is explicit with \|E_n\| → 0; only L¹_loc convergence of p^{ε_n} (along any ε_n ↓ 0) is used. Every limit is along a subsequence of the single sequence (ε_n, H_n) fixed in Lemma 7.4: fixed x → fixed cycle → common Hausdorff subsequence → U fixed → n → ∞ along that subsequence. ✓
- **Hedge words in §7 (grep "clearly/it follows/similarly/standard/exactly as/likewise/for completeness/immediate"):** 5 occurrences — "It follows that" (7.7), "an immediate reversal" (Lemma 7.7), "For completeness" (Blaschke), "likewise" (outer contact), "Exactly as in (7.7)" (Prop 7.1). Each checked above; none hides a missing step.

## 4. Finite check — the planar cover obstruction on discretised domains

**Model (exact).** Domain = finite union of closed grid cells of side h. A cover = partition of the cells into pieces; each piece = closed union of its cells. Only grid vertices can lie in ≥ 3 cells, so "multiplicity ≤ m everywhere" ⇔ "every grid vertex sees ≤ m distinct pieces among its incident cells". Piece diameter = max corner-to-corner distance over pairs of its cells (exact, squared integers in units of h). A finite closed cover of order ≤ 2 and mesh ≤ D swells to an open cover of order ≤ 2 and mesh ≤ D+η, so when the cell union contains a disk of radius > 2, Lemma 7.5 (in its proved form: some y with B̄(y,2) ⊂ Q in an open set) predicts **UNSAT** for (m ≤ 2, D = 2). Conversely any open cover with mesh ≤ D, multiplicity ≤ 2 induces such a partition once h is below its Lebesgue number, so the discrete problem is the faithful finite shadow. Encoding: canonical representative form (cell c → its piece's minimum-index cell d, only d ≤ c with diam(c∪d) ≤ D), so no symmetry; every SAT model is decoded and re-checked by an INDEPENDENT checker (`check_cover`, direct recount of vertex multiplicities and piece diameters). Solver: glucose4 via pysat, cross-checked by the CaDiCaL CLI on dumped DIMACS.

**Results** (logs: /tmp/oaimath/158/seats/continua_check/run_*.log):
```
disk R=3.0 h=0.5: union of cells contains the disk of radius 2.500 about the origin
  MAIN   disk R=3.0: cells=88 h=0.5 m<=2 mesh<=2.0 clauses=8676 -> UNSAT (0.1s)  [expected UNSAT: OK]
  CTRL-a disk R=3.0, multiplicity<=3 allowed: cells=88 h=0.5 m<=3 mesh<=2.0 clauses=8401 -> SAT (0.1s)  pieces=25 independent-checker violations=0  [expected SAT: OK]
  CTRL-f disk R=3.0, m<=2 but mesh<=2.4 (inradius 2.5 > 2.4: lemma still predicts UNSAT): cells=88 h=0.5 m<=2 mesh<=2.4 clauses=18568 -> UNSAT (0.1s)  [expected UNSAT: OK]
  CTRL-b thin rectangle 6 x 1.5 (no disk of radius >2 inside): cells=36 h=0.5 m<=2 mesh<=2.0 clauses=2127 -> SAT (0.0s)  pieces=8 independent-checker violations=0  [expected SAT: OK]
  witness slabs on strip: checker violations (m<=2): []
  CTRL-c strip + forced slab witness: cells=36 h=0.5 m<=2 mesh<=2.0 clauses=2127 -> SAT (0.0s)  pieces=6 independent-checker violations=0  [expected SAT: OK]
  witness brick wall on disk: checker m<=2 violations=26 (e.g. [('multiplicity', (-4, -2), 3), ('multiplicity', (-4, 0), 3)]), m<=3 violations=0
  CTRL-d disk + forced brick witness, m<=3: cells=88 h=0.5 m<=3 mesh<=2.0 clauses=8401 -> SAT (0.1s)  pieces=21 independent-checker violations=0  [expected SAT: OK]
  CTRL-e disk + forced brick witness, m<=2 (must reject: T-junctions): cells=88 h=0.5 m<=2 mesh<=2.0 clauses=8676 -> UNSAT (0.0s)  [expected UNSAT: OK]
  checker negative control (whole disk as one piece): [('diameter', 0, 11.661903789690601)]     # in units of h: 5.83
disk R=2.6 h=1/3: inradius 2.134
  MAIN-mid disk R=2.6: cells=156 h=0.3333333333333333 m<=2 mesh<=2.0 clauses=92048 -> UNSAT (5.9s)  [expected UNSAT: OK]
  CTRL-a-mid disk R=2.6, m<=3: cells=156 h=0.3333333333333333 m<=3 mesh<=2.0 clauses=91229 -> SAT (0.5s)  pieces=39 independent-checker violations=0  [expected SAT: OK]
  SWEEP-R disk R=1.25 (inradius 0.707), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-R disk R=1.5 (inradius 1.000), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-R disk R=1.75 (inradius 1.118), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-R disk R=2.0 (inradius 1.414), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-R disk R=2.25 (inradius 1.803), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-R disk R=2.5 (inradius 2.000), mesh<=2: ... -> UNSAT (0.0s)
  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<=2.5: -> UNSAT (0.3s)
  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<=3.0: -> UNSAT (4.9s)
  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<=3.5: -> TIMEOUT (15.3s)
  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<=4.0: -> TIMEOUT (15.5s)
  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<=5.0: -> SAT (0.9s)  pieces=7 independent-checker violations=0
```
Independent solver (CaDiCaL CLI `cadical -q -t 50`) on the dumped CNFs:
```
disk3_h05_m2 exit=20 s UNSATISFIABLE
disk26_h033_m2 exit=20 s UNSATISFIABLE
disk26_h033_m3 exit=10 s SATISFIABLE
strip_h05_m2 exit=10 s SATISFIABLE
```
Reading: the obstruction holds on both disk instances where the lemma applies (inradius 2.5 and 2.134 > 2), at two resolutions, by two solvers. Controls that FAIL the obstruction's hypotheses admit covers, each re-verified by the independent checker: multiplicity 3 allowed (CTRL-a, CTRL-a-mid, brick wall CTRL-d), a domain with no disk of radius > 2 (thin 6 × 1.5 rectangle, CTRL-b; explicit slab witness CTRL-c), and mesh 5 on the same disk (SWEEP-D). The encoding rejects a known-bad witness (brick wall has T-junctions: CTRL-e UNSAT; the checker reports 26 multiplicity-3 vertices) and the checker rejects an over-wide piece. UNKNOWN (not counted): h = 1/4 at R = 2.75 (glucose4 timed out at 50 s; CaDiCaL-in-pysat ignored the interrupt and was killed at 80 s). SWEEP-R/-D TIMEOUT rows are informational only (Obj. 9).

**Script 1, verbatim** (/tmp/oaimath/158/seats/continua_check/planar_cover_sat.py, sha256 b417fb91…4b56; run as `python3 planar_cover_sat.py {main|mid|sweepR|sweepD} <timeout> [solver]` under `ulimit -v 2000000`):
```python
#!/usr/bin/env python3
"""Finite check of the planar cover obstruction (paper Lemma 7.5 / Lean
PlanarCover.compact_open_cover_impossible) on discretised domains.

Discrete model (exact, integer arithmetic):
  domain = finite union of closed grid cells of side h (cell (i,j) = [i h,(i+1) h] x [j h,(j+1) h]);
  a "cover" = partition of the cells into pieces; each piece is the CLOSED union of its cells.
  multiplicity at a point = number of pieces containing it; only grid vertices can see >2 cells,
  so multiplicity <= m everywhere  <=>  every grid vertex sees <= m distinct pieces among its incident cells.
  mesh = max piece diameter; diameter of a union of closed squares = max corner-to-corner distance
  over pairs of its cells (exact, squared, in units of h).
A finite closed cover of order <= 2 and mesh <= D swells to an open cover of order <= 2 and mesh <= D+eta,
so whenever the domain contains a disk of radius > D the lemma predicts UNSAT for (m=2, D).
Conversely every open cover with mesh <= D and multiplicity <= 2 induces such a cell partition once h is
below its Lebesgue number (cell -> any member containing it), so the discrete problem is the faithful
finite shadow of the lemma.

Encoding: canonical representative form (no symmetry): r[c][d] = "cell c lies in the piece whose
minimum-index cell is d"; only d <= c with diam(c u d) <= D are candidates.
"""
import itertools, sys, time, threading, math
from pysat.solvers import Solver
from pysat.formula import IDPool

def corners(c):
    i, j = c
    return [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]

def diam2(c, d):            # squared diameter of the union of closed cells c, d (units of h)
    return max((a[0]-b[0])**2 + (a[1]-b[1])**2 for a in corners(c) for b in corners(d))

def vertex_cells(cells):
    S = set(cells); V = {}
    for c in cells:
        for v in corners(c):
            V.setdefault(v, []).append(c)
    return V

def check_cover(cells, piece, D2, m):
    """Independent checker. piece: dict cell -> piece label. Returns list of violations."""
    bad = []
    for v, inc in vertex_cells(cells).items():
        k = len({piece[c] for c in inc})
        if k > m: bad.append(('multiplicity', v, k))
    groups = {}
    for c in cells: groups.setdefault(piece[c], []).append(c)
    for p, mem in groups.items():
        dm = max(diam2(a, b) for a in mem for b in mem)
        if dm > D2: bad.append(('diameter', p, math.sqrt(dm)))
    return bad

def encode(cells, D2, m):
    cells = sorted(cells); idx = {c: k for k, c in enumerate(cells)}
    pool = IDPool(); cl = []
    cand = {c: [d for d in cells if idx[d] <= idx[c] and diam2(c, d) <= D2] for c in cells}
    r = lambda c, d: pool.id(('r', c, d))
    for c in cells:
        lits = [r(c, d) for d in cand[c]]
        cl.append(lits)                                     # at least one representative
        for a, b in itertools.combinations(lits, 2): cl.append([-a, -b])   # at most one
        for d in cand[c]:
            if d != c: cl.append([-r(c, d), r(d, d)])       # representative represents itself
    members = {}
    for c in cells:
        for d in cand[c]: members.setdefault(d, []).append(c)
    for d, mem in members.items():                          # piece diameter <= D
        for a, b in itertools.combinations(mem, 2):
            if diam2(a, b) > D2: cl.append([-r(a, d), -r(b, d)])
    def eq(a, b):                                           # eq(a,b) -> same piece
        if idx[a] > idx[b]: a, b = b, a
        e = pool.id(('eq', a, b))
        if ('done', a, b) not in done:
            done.add(('done', a, b))
            common = [d for d in cand[a] if d in cand[b]]
            ys = []
            for d in common:
                y = pool.id(('y', a, b, d)); ys.append(y)
                cl.append([-y, r(a, d)]); cl.append([-y, r(b, d)])
            cl.append([-e] + ys)
        return e
    done = set()
    for v, inc in vertex_cells(cells).items():
        if len(inc) > m:                                    # among any m+1 incident cells two share a piece
            for sub in itertools.combinations(inc, m+1):
                cl.append([eq(a, b) for a, b in itertools.combinations(sub, 2)])
    return cells, cand, r, pool, cl

def solve(cells, D2, m, assume_piece=None, timeout=50, name='glucose4'):
    cells, cand, r, pool, cl = encode(cells, D2, m)
    assum = []
    if assume_piece is not None:      # force a given partition (canonical rep = min index cell)
        idx = {c: k for k, c in enumerate(cells)}
        rep = {}
        for c in cells:
            p = assume_piece[c]
            if p not in rep or idx[c] < idx[rep[p]]: rep[p] = c
        for c in cells:
            d = rep[assume_piece[c]]
            if d not in cand[c]: return 'UNSAT(assumption outside candidate set: piece too wide)', None, len(cl)
            assum.append(r(c, d))
    s = Solver(name=name, bootstrap_with=cl)
    timer = threading.Timer(timeout, s.interrupt); timer.start()
    t0 = time.time()
    res = s.solve_limited(assumptions=assum, expect_interrupt=True)
    timer.cancel()
    model = s.get_model() if res else None
    s.delete()
    if res is None: return 'TIMEOUT', None, len(cl)
    if not res: return 'UNSAT', None, len(cl)
    ms = set(l for l in model if l > 0); piece = {}
    for c in cells:
        ds = [d for d in cand[c] if r(c, d) in ms]; assert len(ds) == 1; piece[c] = ds[0]
    return 'SAT', piece, len(cl)

def disk_cells(R, h):          # cells fully inside the closed disk of radius R centred at the origin (a grid vertex)
    n = int(R/h) + 2
    return [(i, j) for i in range(-n, n) for j in range(-n, n)
            if all((x*h)**2 + (y*h)**2 <= R*R + 1e-12 for x, y in corners((i, j)))]

def rect_cells(W, H, h):
    return [(i, j) for i in range(round(W/h)) for j in range(round(H/h))]

def inradius_at_origin(cells, h):  # distance from origin to the complement of the union of cells
    S = set(cells); best = float('inf')
    for c in cells:
        i, j = c
        for (di, dj), seg in [((1,0), ((i+1,j),(i+1,j+1))), ((-1,0), ((i,j),(i,j+1))),
                              ((0,1), ((i,j+1),(i+1,j+1))), ((0,-1), ((i,j),(i+1,j)))]:
            if (i+di, j+dj) not in S:
                (x1,y1),(x2,y2) = seg
                # distance from origin to segment (axis parallel)
                xs = sorted([x1,x2]); ys = sorted([y1,y2])
                px = min(max(0, xs[0]), xs[1]); py = min(max(0, ys[0]), ys[1])
                best = min(best, math.hypot(px*h, py*h))
    return best

if __name__ == '__main__':
    part = sys.argv[1]
    TO = float(sys.argv[2]) if len(sys.argv) > 2 else 50
    solver_name = sys.argv[3] if len(sys.argv) > 3 else 'glucose4'
    def run(label, cells, h, m, D=2.0, assume=None, expect=None):
        D2 = round((D/h)**2)
        t0 = time.time()
        res, piece, ncl = solve(cells, D2, m, assume, timeout=TO, name=solver_name)
        line = f"{label}: cells={len(cells)} h={h} m<={m} mesh<={D} clauses={ncl} -> {res} ({time.time()-t0:.1f}s)"
        if piece is not None:
            viol = check_cover(cells, piece, D2, m)
            line += f"  pieces={len(set(piece.values()))} independent-checker violations={len(viol)}"
        if expect is not None: line += f"  [expected {expect}: {'OK' if res.startswith(expect) else 'MISMATCH'}]"
        print(line, flush=True)
        return piece
    if part == 'main':
        for (R, h) in [(3.0, 0.5)]:
            cells = disk_cells(R, h)
            print(f"disk R={R} h={h}: union of cells contains the disk of radius {inradius_at_origin(cells,h):.3f} about the origin")
            run(f"  MAIN   disk R={R}", cells, h, 2, expect='UNSAT')
            run(f"  CTRL-a disk R={R}, multiplicity<=3 allowed", cells, h, 3, expect='SAT')
            run(f"  CTRL-f disk R={R}, m<=2 but mesh<=2.4 (inradius 2.5 > 2.4: lemma still predicts UNSAT)", cells, h, 2, D=2.4, expect='UNSAT')
        h = 0.5
        strip = rect_cells(6.0, 1.5, h)
        run("  CTRL-b thin rectangle 6 x 1.5 (no disk of radius >2 inside)", strip, h, 2, expect='SAT')
        slabs = {c: c[0] // 2 for c in strip}
        print("  witness slabs on strip: checker violations (m<=2):", check_cover(strip, slabs, 16, 2))
        run("  CTRL-c strip + forced slab witness", strip, h, 2, assume=slabs, expect='SAT')
        cells = disk_cells(3.0, 0.5)
        brick = {c: (c[1] // 2, (c[0] + (c[1]//2) % 2) // 3) for c in cells}   # 1.5 x 1.0 bricks, rows offset by one cell
        vb2 = check_cover(cells, brick, 16, 2); vb3 = check_cover(cells, brick, 16, 3)
        print(f"  witness brick wall on disk: checker m<=2 violations={len(vb2)} (e.g. {vb2[:2]}), m<=3 violations={len(vb3)}")
        run("  CTRL-d disk + forced brick witness, m<=3", cells, h, 3, assume=brick, expect='SAT')
        run("  CTRL-e disk + forced brick witness, m<=2 (must reject: T-junctions)", cells, h, 2, assume=brick, expect='UNSAT')
        one = {c: 0 for c in cells}
        print("  checker negative control (whole disk as one piece):", check_cover(cells, one, 16, 2)[:1])
    elif part == 'fine':
        cells = disk_cells(2.75, 0.25)
        print(f"disk R=2.75 h=0.25: inradius {inradius_at_origin(cells,0.25):.3f}", flush=True)
        run("  MAIN-fine disk R=2.75", cells, 0.25, 2, expect='UNSAT')
    elif part == 'mid':
        h = 1/3
        for R in [2.6]:
            cells = disk_cells(R, h)
            print(f"disk R={R} h=1/3: inradius {inradius_at_origin(cells,h):.3f}", flush=True)
            run(f"  MAIN-mid disk R={R}", cells, h, 2, expect='UNSAT')
            run(f"  CTRL-a-mid disk R={R}, m<=3", cells, h, 3, expect='SAT')
    elif part == 'sweepR':
        for R in [1.25, 1.5, 1.75, 2.0, 2.25, 2.5]:
            cells = disk_cells(R, 0.5)
            run(f"  SWEEP-R disk R={R} (inradius {inradius_at_origin(cells,0.5):.3f}), mesh<=2", cells, 0.5, 2)
    elif part == 'sweepD':
        cells = disk_cells(3.0, 0.5)
        for D in [2.5, 3.0, 3.5, 4.0, 5.0]:
            run(f"  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<={D}", cells, 0.5, 2, D=D)
```
**Script 2, verbatim** (dump_dimacs.py, then `cadical -q -t 50 <tag>.cnf`):
```python
import sys
sys.path.insert(0, '.')
from planar_cover_sat import encode, disk_cells, rect_cells
for tag, cells, h, m in [('disk3_h05_m2', disk_cells(3.0, 0.5), 0.5, 2),
                         ('disk26_h033_m2', disk_cells(2.6, 1/3), 1/3, 2),
                         ('disk26_h033_m3', disk_cells(2.6, 1/3), 1/3, 3),
                         ('strip_h05_m2', rect_cells(6.0, 1.5, 0.5), 0.5, 2)]:
    D2 = round((2.0/h)**2)
    _, _, _, pool, cl = encode(cells, D2, m)
    nv = max(abs(l) for c in cl for l in c)
    with open(f'{tag}.cnf', 'w') as f:
        f.write(f'p cnf {nv} {len(cl)}\n')
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    print(tag, nv, len(cl))
```

## 5. Citation table (scope §7)

| cited | paper claims | source (fetched) | verdict |
|---|---|---|---|
| Hatcher [14, Theorem 1.9] (Lemma 7.5, p. 47) | "The Brouwer fixed point theorem, in its planar form" | AT.pdf (pi.math.cornell.edu/~hatcher/AT/AT.pdf), p. 31: "Theorem 1.9. Every continuous map h : D² → D² has a fixed point, that is, a point x ∈ D² with h(x) = x." (applies to the closed square, homeomorphic to D²) | MATCH |
| Hatcher [14, Section 1.A] (Lemma 7.7, p. 48) | "the reduced-path argument for graphs" | AT.pdf §1.A "Graphs and Free Groups", p. 83ff (universal cover of a graph is a tree) | MATCH |
| Sokolov–Voronov [25, Props 1–2] (p. 42) | "The connected-interface mechanism has a precedent … where interfaces come from a regular map" | arXiv:2502.01958v1: "Proposition 1. Let u and v be two points of the same color, connected by a continuous monochromatic curve uv. Then, there does not exist a point z of the same color such that ‖u − z‖ < 1, ‖v − z‖ > 1." / "Proposition 2. Let u and v lie on the boundary of two monochromatic regions. Then, no point z satisfying ‖z − u‖ < 1, ‖z − v‖ > 1 can be colored with either of the two colors of these regions." — exactly the straddling exclusion of Δ(K) for map-type colourings | MATCH (precedent only; not load-bearing) |
Fetched copies: /tmp/oaimath/158/seats/continua_check/src/{AT.pdf,AT.txt,sv.pdf,sv.txt}.

## 6. Verdict for §7

**HOLDS AS READ.** Every lemma of §7 (7.2–7.8), the construction (7.4)–(7.6), the limit construction of the continua K_j with their common point x, and the exclusion of BOTH endpoint labels from Δ(K_j) were verified line by line; no quantifier, compactness, connectedness or overlap error was found. The section is conditional only on (i) Theorem 6.5 (cyclic-centre locus closed and locally finite) and Definition 6.1 — `palettes` seat — and (ii) Lemma 4.3's first assertion, which I verified (it is on the critical path, contrary to the brief's test (E)). The planar cover obstruction (PDF Lemma 7.5, square of side ten) is the same statement as Lean's `PlanarCover.compact_open_cover_impossible` (disk version, more general domain), and Five.lean's `graph_map_small_mesh_impossible` supplies exactly its hypotheses (relatively open components, multiplicity ≤ 2 at every point, mesh ≤ 2 on preconnected components, compact domain containing B(0,5)). The Lean takes a different route through §7.4–7.5 (crossing graphs + forest extension instead of reduced words; fixed-radius centre disks instead of merged core disks), so the kernel does not certify the paper's Lemmas 7.7–7.8 / Prop 7.1 as written — they stand on this hand check. §7 itself uses k = 5 only through α < 1/5, K₅ and ℓ ≤ 5; it would run verbatim with six labels given a six-label Theorem 6.5.
