# Referee report — scope "grids": §3 of the GEOMETRIC paper (PDF pp. 4–7), cross-checked against §3 (+ the separation step of Lemma 4.3) of the DYADIC paper

Reader: hostile referee seat `grids`. Sources read: `geometric.pdf` pp. 3–7 rendered (formulas read off the PDF images, not the text extraction), `geometric.txt` §§1.2–5, `dyadic.pdf` pp. 3–7 rendered, `dyadic.txt` §§3–4.3. Finite checks: own scripts in `/tmp/grids_check/` (`layout.py`, `mutate_layout.py`, `grids.py`, `lemmas2.py`, `run_q09.py`, `adversarial.py`, `interface53.py`), all exact rational arithmetic (`fractions.Fraction`), run under `nice -n 19`, each a few seconds to a few minutes.

## Verdict for this scope

**HOLDS AS READ.** Every inequality in §3 checks, with the exponent bookkeeping as stated. I found no FATAL item and no GAP, mathematical or expository. Every objection below is COSMETIC: each is a true step whose one-line justification is missing in the geometric paper. The dyadic paper usually supplies that line. One item (O5) is about provenance rather than correctness: the geometric construction at q = 1/2 is **not** the dyadic construction. Any formal verification of the dyadic paper therefore does not mechanically cover geometric §3, even at q = 1/2.

## Lemma-by-lemma status

| Item (geometric §3) | Status | Finite check |
|---|---|---|
| Grid definitions: c = 4/(1−q), N_b = 2^⌈log2(cq^−b)⌉, Γ_b, J_b; the half-open convention | VERIFIED LINE BY LINE | `grids.py`, exact |
| (3.1) cq^−b ≤ N_b < 2cq^−b; N_b powers of 2, nondecreasing; nesting identity J_b = ⌊J_b′/(N_b′/N_b)⌋ | VERIFIED LINE BY LINE. The nesting identity is asserted, not proved (O1) | `grids.py`: q ∈ {1/20, 1/2, 9/10, 99/100}, b up to n_0+300; plus 2,000 random q ∈ (0,1), b < 60: 0 monotonicity violations |
| Window assignment: preorder, exactly g unused indices, r_1 = r_0, σ_1, r_h = max{r_0, g+σ_{h−1}}, σ_h, n_0, b_e, b*_e, 𝒩 | VERIFIED LINE BY LINE | `layout.py`: 36 configs (M∈{2,3,4}, d∈{1,2,3}, g∈{1,3}, r_0∈{1,5}), n_0 ∈ {1, 20} |
| Lemma 3.1 (b*_e − a_e + 1 ≤ 2r_h) and the remark "finest grid … at most 2r_h − 1 beyond a_e" | VERIFIED LINE BY LINE; the bound is **sharp** | `layout.py` 36/36 OK; mutation controls fail as they should (`mutate_layout.py`) |
| Definition of stable centers; the endpoint convention paragraph | VERIFIED LINE BY LINE | `adversarial.py` |
| Lemma 3.2, density bound ρ(ℝ∖S) ≤ 4Kc q^{g+1} | VERIFIED LINE BY LINE | `grids.py` (2N_b′q^{b′+g+1} ≤ 4cq^{g+1}, all b, g ∈ {1,3,7}); Monte Carlo in `lemmas2.py` |
| Lemma 3.2, key preservation (3.3) | VERIFIED LINE BY LINE | `lemmas2.py`, `run_q09.py`, `adversarial.py`: 0 violations in about 250k exact comparisons |
| Lemma 3.3 (separation, at b_e and every b ≥ b_e) | VERIFIED LINE BY LINE | 0 collisions in all runs; negative control (coarsened grid) does collide |

## The bookkeeping, redone

1. **(3.1).** With y = log2(cq^−b), N_b = 2^⌈y⌉ ∈ [2^y, 2^{y+1}), which gives cq^−b ≤ N_b < 2cq^−b. Since cq^−b is strictly increasing in b (q < 1), ⌈y⌉ is nondecreasing, so N_b is a nondecreasing power of two for **every** q ∈ (0,1). It is generally **not strictly** increasing: at q = 99/100, N_b is constant on runs of 69 consecutive b, and at q = 9/10 on runs of 6–7. No step in §3 or in its uses in §4–§5 needs strictness. Nesting needs only N_b′/N_b ∈ ℤ. The terminal-address step of Lemma 4.3 compares indices (b(L) ≥ b_{e_i}) and then uses nesting. N_b ≥ c > 4, so every N_b is an integer ≥ 8 and Γ_b ⊇ ℤ.

2. **Separation constant.** 1/N_b ≤ q^b/c = (1−q)q^b/4 < (1−q)q^b. Exactly, the margin (1−q)q^b·N_b is at least 4.0000 (attained at q = 1/2, where cq^−b is a power of 2) and at least 4.0019 / 4.0146 / 4.0135 at q = 1/20, 9/10, 99/100 (`grids.py`, b ≤ n_0+300 ⊇ b ≤ 40). The literal floating-point definition ⌈log2(·)⌉ agrees with the exact one for b ≤ 40 at all four q.

3. **a_e = b′ + g + 1.** This is the translation of "leaving exactly g unused indices between consecutive windows" (p. 5): the predecessor ends at b′, indices b′+1, …, b′+g are unused, and the next window starts at b′+g+1. `layout.py` confirms this for every consecutive pair in all 36 layouts. Endpoints are strictly increasing along preorder, and for every edge e the predecessor endpoint b′ ≥ b_f for **every** earlier f.

4. **Lemma 3.2 density.**
   - The failure set of window e is ⋃_{γ∈Γ_b′}[γ − 2q^{a_e}, γ), because γ ∈ (x, x+2q^{a_e}] ⇔ γ − 2q^{a_e} ≤ x < γ.
   - Per period that is N_b′ intervals of length 2q^{a_e}, so the density is at most 2N_b′q^{a_e} < 4c q^{a_e−b′} = 4c q^{g+1}. If the intervals overlap, the union bound still holds.
   - Summing over the K−1 noninitial windows gives the bound; the strict inequality and the factor K−1 are both slack.
   - Monte Carlo unstable fractions against the union sum and against 4Kcq^{g+1}: q=1/2, (M,d,g)=(2,2,8): 0.151 / 0.156 / 0.375. q=9/10, (2,2,71): 0.266 / 0.278 / 0.487. q=1/20, (2,2,1): 0.161 / 0.160 / 0.253. q=99/100, (2,2,980): 0.32 / 0.327 / 0.502.

5. **(3.3).** For n ∈ W_e and t ∈ [1,2], 0 < tq^n ≤ 2q^{a_e}, so (x, x+tq^n] ∩ Γ_b′ = ∅. The real cell [γ, γ+1/N_b′) holding x therefore also holds x+tq^n. Because ℤ ⊆ Γ_b′, ⌊·⌋ is constant on that cell, so the periodic key agrees. Nesting then carries this to every b_f ≤ b′.
   - Checked exactly at random x, at boundary x of the finest grid, at x making a translated point land exactly on an integer, at t ∈ {1, 3/2, 2} and random t: 0 violations.
   - Discriminating control: **every** sampled unstable x showed a key change at the predecessor resolution for t = 2, n = a_e. So the stability condition is not merely sufficient but exactly what the maximal displacement needs.
   - Endpoint convention: x = γ is stable for that window whenever 2q^{a_e} < 1/N_b′ (100/100 per q), and x = γ − 2q^{a_e} is unstable with a key change (100/100 per q).

6. **Lemma 3.3.**
   - All points lie in [x, x + 2q^{n_0}], because every window index n ≥ n_0. The length is ≤ 1/4 < 1/2, so circular distance equals real distance.
   - Distances: x to y_n is tq^n ≥ q^b. For n < n′ in W_e, y_n − y_{n′} = tq^n(1 − q^{n′−n}) ≥ q^b(1−q). This is lossy (the true minimum is q^{b−1}(1−q)) but valid.
   - Same periodic key ⇒ {z}, {z′} in one cell of width 1/N_b ⇒ circular distance < 1/N_b.
   - The extension to every b ≥ b_e is the contrapositive of nesting.
   - Checked exactly over all edges of six layouts (q ∈ {1/2, 9/10, 1/20, 99/100}) at resolutions {b_e, b_e+1, b*_e, b_max}, incl. adversarial x: 0 collisions.
   - Negative control (grid coarsened by 8 or 32): collisions 27/1200 and 938/1200 at q=9/10, and 1200/1200 at q=1/2 (coarsening 32). The checker can fail.

7. **Lemma 3.1.** h = 1: the block is W_e, span r_1 ≤ 2r_1. h ≥ 2: the child subtree follows W_e after exactly one gap. Endpoints increase along preorder and the subtree is a consecutive block, so b*_e is the subtree's last endpoint and b*_e − a_e + 1 = r_h + g + σ_{h−1} ≤ 2r_h, since r_h ≥ g + σ_{h−1}.
   - `layout.py` measures spans straight from the laid-out windows, not from the σ formula. Checked:
     - the span equals the formula in every case;
     - σ_h equals the measured span of every height-h subtree;
     - edge + child subtree is a consecutive block;
     - every subtree edge comes after e with a larger endpoint;
     - every root-to-P edge and every earlier sibling (P,j), j < i, precedes (P,i);
     - b*_e ≤ a_e + 2r_h − 1.
   - **Sharpness:** min slack 2r_h − span = 0 in all 24 configs with d ≥ 2. The inequality is used only as an upper bound, so this is harmless; it just means the "2r − 1" in (5.3) cannot be improved.
   - Mutations (r_h := r_0; r_h := g + σ_{h−1} − 1 − r_0, i.e. too short) produce 24 Lemma-3.1 failures each, so the checker discriminates.
   - Note: geometric r_1 = r_0 can be < g. Nothing needs r_1 ≥ g, because an edge into a leaf has no following subtree.

8. **Compatibility of 3.2 and 3.3 (sanity).** For x ∈ S and n ∈ W_e, Lemma 3.2 forces J_b′(x+tq^n) = J_b′(x), while Lemma 3.3 forces J_{b_e}(x+tq^n) ≠ J_{b_e}(x). Both can hold only if N_{b_e} > N_b′. This is guaranteed once 4Kcq^{g+1} < 1: N_{b_e}/N_b′ > q^{−(g+1)}/2 > 2Kc. When g is small and the bound is vacuous, S can be empty. Observed: q=1/2, g=1 gives per-window failure density exactly 2^{3−g} = 4, and 150/150 sampled centers were unstable. That is consistent with the lemma, not a contradiction.

## Objections (all COSMETIC)

**O1 — p. 4, nesting identity asserted without proof. COSMETIC (exposition; true).**
> "All N_b are powers of two and are nondecreasing in b. Consequently, if b′ ≥ b, then N_b′/N_b is an integer and J_b(z) = ⌊J_b′(z)/(N_b′/N_b)⌋."

Both facts are true, but neither is argued. "Nondecreasing" needs the line that cq^−b is increasing. The floor identity needs: write N_b′{z} = J_b′(z) + ε with 0 ≤ ε < 1, set m = N_b′/N_b ∈ ℤ, then ⌊(J+ε)/m⌋ = ⌊J/m⌋ because J ∈ ℤ and ε < 1. The dyadic paper gives exactly this at (7) ("This follows by writing 2^{B+2}{z} = J_B(z) + ε…"). Fix: insert those two lines.

**O2 — p. 6, Lemma 3.2 proof: passage from the real lattice to the periodic key. COSMETIC (exposition; true).**
> "Hence the segment from x to x + tq^n crosses no boundary of Γ_b′, with a possible boundary at x itself assigned to the cell on its right. It follows that J_b′(x + tq^n) = J_b′(x)."

J_b′ is defined through {z}. The step needs ℤ ⊆ Γ_b′, so that ⌊z⌋ cannot jump inside a Γ_b′-cell. That holds because N_b′ ∈ ℤ, but the text never says so. The dyadic paper says it ("An integer cannot lie in this interval either, so passing to periodic keys introduces no additional case"; also "every integer is a boundary" after (6)). Fix: one clause.

**O3 — pp. 5–6, monotonicity of window endpoints along preorder is only implicit. COSMETIC (exposition; true).**
> "Assign an integer interval W_e = [a_e, b_e] ∩ ℕ to each edge, in preorder, leaving exactly g unused indices between consecutive windows." … "place all subsequent windows with the prescribed lengths and gaps." … "Every preceding edge f has b_f ≤ b′, so nesting gives (3.3)."

Lemma 3.2 rests on b_f ≤ b′ for every earlier f, and Lemma 4.3's terminal-address step on b(L) ≥ b_{e_i}. Both rest on windows being laid out with increasing indices in preorder. The only explicit statement is Figure 1's axis label "increasing indices in preorder". The relation a_e = b′ + g + 1, used verbatim in the proof of Lemma 3.2, never appears in the construction. The dyadic paper writes it out: "An edge e from height h receives W_e = {a_e, …, b_e} with b_e = a_e + r_h − 1; if f immediately precedes e, set a_e = b_f + g + 1." Verified by `layout.py`. Fix: copy the dyadic sentence.

**O4 — p. 7, Lemma 3.3 proof: lossy bound. COSMETIC (correct).**
> "t(q^n − q^{n′}) = tq^n(1 − q^{n′−n}) ≥ (1 − q)q^b."

This uses q^n ≥ q^b. Since n < n′ ≤ b, in fact q^n ≥ q^{b−1}, and the sharp minimum is (1−q)q^{b−1}. The stated bound is valid and the margin over 1/N_b is still ≥ 4. No fix needed. Recorded only because the brief asked whether each inequality is used in the right direction: it is.

**O5 — Cross-paper: the geometric construction at q = 1/2 is not the dyadic construction. COSMETIC for correctness; load-bearing for provenance.**
Geometric p. 4: "N_b = 2^⌈log2(cq^−b)⌉", with c = 4/(1−q) = 8 at q = 1/2, so N_b = 2^{b+3}. Dyadic (6): "J_b(z) = ⌊2^{b+2}{z}⌋", i.e. N_b = 2^{b+2}. Exact check (`grids.py`): N_b^geom / 2^{b+2} = 2 for every b. Further differences at q = 1/2:
- r_1 = r_0 (geometric) vs r_1 = max{r_*, g} (dyadic (4) with σ_0 = 0);
- the stability failure density per window is 2^{3−g} (bounded by 2^{4−g}) vs exactly 2^{2−g} (dyadic);
- the separation margin is 4 in both, using different distance bounds.

Both versions are internally correct; I checked each. But any Lean formalization of the dyadic paper certifies a coarser-grid construction and does not mechanically certify geometric §3, even at q = 1/2. Fix: state in the geometric paper that it is a re-parametrisation, not a literal generalisation, of the formalized one.

**O6 — p. 6, Lemma 3.2 statement. COSMETIC.**
> "ρ(ℝ ∖ S) ≤ 4Kc q^{g+1}."

The proof gives the strict bound (K−1)·(something < 4cq^{g+1}). §5 uses it as "< p" after choosing 4Kcq^{g+1} < p, which is consistent. No fix needed.

## Cross-check against dyadic §3 (+ the separation in dyadic Lemma 4.3): steps present in one paper and missing in the other

| Step | Geometric | Dyadic |
|---|---|---|
| Proof of the nesting identity | asserted (O1) | proved under (7) |
| Integers are boundaries / periodic-key passage | implicit (O2) | explicit (after (6), and in the proof of Lemma 3.1) |
| Explicit a_e = b_f + g + 1, b_e = a_e + r_h − 1 | in words only (O3) | explicit |
| b_f ≤ b′ for every earlier window | asserted | asserted (same; true) |
| Stability density | upper bound, no disjointness needed | exact ρ(E_e) = 2^{2−g} via disjoint interiors (needs (2) first; it is chosen first) |
| r_1 | r_0 | max{r_*, g} (harmless difference; the geometric Lemma 3.1 h = 1 case needs nothing) |
| Separation lemma | standalone Lemma 3.3, includes x and every b ≥ b_e | inside the proof of Lemma 4.3, sharper distance 2^{−b} vs cell 2^{−(b+2)}; uses (7) for b(L) |
| Start index | n_0 with 2q^{n_0} ≤ 1/4 | 3 (identical at q = 1/2) |
| Grid resolution at q = 1/2 | 2^{b+3} | 2^{b+2} (O5) |

Every geometric step needed downstream has a dyadic counterpart. Nothing substantive is missing from either side.

## Interface facts for the other seats (derived from §3; checked)

- **(iii) Lemma 4.2's use of (3.3).** For every vertex U and child i, every edge on the root–U path and every (U, j), j < i, precedes (U, i) in preorder (`layout.py`, "anc" check). b′ (the predecessor endpoint of W_{(U,i)}) dominates all of them, so (3.3) covers every selector Lemma 4.2 consults.
- **(ii) The worry about selector entries below U_i.** Every edge in the subtree of U_i has endpoint > b_{e_i} (`layout.py`, "subafter" check). Lemma 3.3's second sentence then makes the key of y_n(t) differ from the key of x in **every** table below U_i. So no selector entry read by a translated point below U coincides with x's exposed entry in that table. This holds regardless of how Lemma 4.3 conditions.
- **(iv) Q_i reads only resolutions ≤ b*_{e_i}.** That covers the selector on e_i (b_{e_i}), the selectors in the subtree, and the terminal tables b(L) of leaves below U_i (or b_{e_i} if U_i is a leaf); all are endpoints inside the block. The (5.3) bookkeeping q^n N_{b*} < q^{a_e}·2cq^{−b*} ≤ 2cq^{1−2r} ≤ 2cq^{−2r} was checked exactly on the layouts (`interface53.py`): 0 violations. Max ratio LHS/RHS: 0.048 (q=1/20), 0.25 (1/2), 0.894 (9/10), 0.983 (99/100).
- **(v) Parameter facts.** n_0 exists for every q (n_0 = 1, 3, 20, 207 at q = 1/20, 1/2, 9/10, 99/100). r_h ≥ r_0 = r_* at every height including h = 1. Nothing in §3 feeds g or r_0 back into M, d or K.

## "Clearly / it follows / thus" audit (§3, plain-text lines 231–401)

There are 13 hits: "Thus" ×4, "therefore" ×3, "consequently/Consequently" ×2, "Hence", "It follows", "immediate", "immediately". Each one checked:
- "Thus the cells are closed on the left": true.
- "Consequently … N_b′/N_b is an integer and J_b = …": true but unproved (O1).
- "An edge and its child subtree therefore form a consecutive block": true by the definition of preorder.
- "child's subtree immediately after W_e" and "The span is therefore r_h + g + σ_{h−1}": true; measured.
- "Thus the finest grid … at most 2r_h − 1 beyond a_e": true; measured.
- Figure caption "Thus the entire block …": true.
- "Hence the segment … crosses no boundary": true.
- "It follows that J_b′(x+tq^n) = J_b′(x)": true, missing one clause (O2).
- "therefore equal their ordinary real distances": true (length ≤ 1/4).
- "Thus all the keys are distinct": true.
- "can consequently reuse all earlier decisions": a summary sentence.

## Citation table

There are no citations inside §3 of either paper. Nothing to fetch.

## Instrument notes (own errors, disclosed)

- My first subsampled separation run reported 564 "collisions" at q = 9/10. The cause was my own sampler: it prepended a_e and b_e to a random sample that could contain them again, so the same point was compared with itself. After deduplicating I got 0 collisions in the same configuration, and also 0 in a full unsampled run (`run_q09.py`, "full").
- With g = 1, the q ∈ {1/2, 9/10, 99/100} layouts have no stable centers (the density bound exceeds 1). The (3.3) checks were therefore rerun with g chosen so that 4Kcq^{g+1} < 1/2 (g = 8, 9, 71, 78, 980), giving 18k–99k exact comparisons per config.
