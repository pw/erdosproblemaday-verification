# Referee report (hostile seat "kim"): J. Kim, "A proof of the Erdős–Gallai cycle decomposition conjecture", arXiv:2610.07840v2

**VERDICT: HOLDS AS READ.** I found nothing above EXPOSITION. Scope: I read the whole v2 TeX (`/tmp/oaimath/181/refs/kim_src/erdos_gallai_v2.tex`, md5 0c9ebad5…) line by line: §2.1, Lemmas 3.1–3.2, 4.1–4.3, all of §5 (Claims 2–7), Definition 6.1, Lemmas 6.4–6.9, §6.3 including Claim 8. I checked every cited statement against its source: BM arXiv:2211.07689v2 (Def 11, Lemma 14, Cor 22, Thm 24, and Thm 3 as quoted in §1.1) and CFS arXiv:1310.0632v2 (Def 1, Lemma 4.1, Lemma 4.2, Cor 4.3, Lemma 4.4). I did **not** re-verify the internal proofs of BM Lemma 14 or BM Thm 24 (published, Adv. Math. 2024), and I read CFS Cor 4.3 only as far as its Lemmas 4.1–4.2. I skimmed v1 only for what v2 changed.

arXiv check, 2026-10-20: the abstract page lists v1 (Tue 6 Oct 2026 06:42 UTC) and v2 (Fri 9 Oct 2026 04:08 UTC) only. There is no v3 and no withdrawal, so this report is on v2.

## 1. The architecture, and where the weight sits

Theorem 1.1 follows from Theorem 1.3 (the structure theorem) and Theorem 1.4 (the qoh theorem: polynomial minimum degree ⇒ O_ε(n) parts) by the procedure in §2.1. I checked that deduction exhaustively. I then tried to break each of the two theorems in turn and could not.

### 1a. Accounting in §2.1 (the brief's item 1)

**Step (a)** (step:a) records *every* edge at v, so v becomes isolated. Edges are only ever deleted, so a vertex that becomes isolated stays isolated. Hence:
- (a) runs at most n times;
- each run records fewer than k edges, so at most kn single edges in total.

The worry "vertices can regain small degree" cannot happen: degrees never go up, and a vertex that (a) processes is finished.

**Step (b)**:
- The drop identity is f(d)−f(d−2) = (d−1)^{-1/2} − (d+1)^{-1/2} = ½∫_{d−1}^{d+1} x^{-3/2} dx.
- By Hermite–Hadamard (x^{-3/2} is convex), this is ≥ d^{-3/2}, which is ≥ b^{-3/2} for 2 ≤ d ≤ b.
- So Φ drops by at least 1 per heavy cycle. Since 0 ≤ Φ < n, step (b) runs at most n times.

**Step (c)**:
- After E(R'[S]) is removed, the ≥ |S|/12 "credited" vertices have degree ≤ 2 < k (k ≥ 3).
- Step (a) is tested first in every iteration, so (a) isolates each credited vertex before any later (b) or (c).
- An isolated vertex is never in a later R', so each vertex is credited at most once.
- Hence Σ|S| ≤ 12n, and step (c) records at most 12kn parts (because C_{1/1000} ≤ k).
- Total: at most 14kn. Theorem 1.4 is applied with n := |S| and δ(R'[S]) ≥ |S|^{1/1000}, which matches its hypothesis exactly.

The paper is right that lightness never has to survive edge deletions: heaviness is re-tested at every step. Theorem 1.3 is only ever applied to the current R', which is light with respect to its own degrees.

### 1b. Theorem 1.3 (thm:structure) holds (brief item 2)

I verified every inequality:

- **Lemma 3.2 (lem:regions).** The DFS ancestor property gives back-edge span j < k−1. The key inclusion N_F(W_i) ⊆ B_{u_i} ∪ ⋃_{j<i} W_j holds. So do R_i ∩ S_i = ∅, N_F(R_i) ⊆ S_i, Σ|S_i| ≤ 2(p−1)k ≤ 2k|F|/m, and |W_i ∪ B_{u_i}| < 2m+1+k.
- **Lemma 4.1 (lem:expansion).** Greedy disjoint cherries: at least |X|/(2q). Pruning removes at most r|Z|(1+(r+m)/(m−r)) ≤ 3r|Z| edges; this needs m ≥ 3r, which holds because 20t ≥ 6t+12 iff t ≥ 6/7. In the longest alternating sequence (Claim 1), both terminal cases close a cycle through at least t+1 centres. I checked the index arithmetic j ≤ k−r+1 and j ≤ k−t−2.
- **Lemma 4.2 (lem:two-parents).** P[x ∈ X'] ≥ 1/16 needs m ≤ d/4+1 ≤ (d−2)/3 (true for d ≥ 20) and e^{−μ/18} < 1/4 (μ ≥ 499). The auxiliary subgraph meets Lemma 4.1's hypotheses exactly: designated edges only, exactly m edges to Z, X'/P'/Z disjoint because X', P' ⊆ W and Z = V∖W.
- **Lemma 4.3 (lem:down).**
  - d_j ≥ 1000t_j and d_j > b_j for d large, so X_j ∩ U-parents = ∅.
  - Times chosen ≤ d(z) ≤ b_j.
  - The sum Σ b_j^{5/2}/d_j = O(d^{-1/6}) splits correctly at b_j = 2d^{1/3}.
  - "d sufficiently large" means roughly d ≳ 10^{193} (see §4). That is harmless.
- **Claim 2 (cl:window).**
  - Every vertex degree ≥ δ lies in exactly one interval (δ^{3^{i−3}}, δ^{3^{i−2}}] with i ≥ 2. With i = σ+5j, each v ∈ A* lands in exactly one A_j^{(σ)}.
  - The windows with |L_j| < n/(1000 log a_j) hold fewer than Σ_j n/(1000·3^{5j}) < n/500 vertices.
  - Averaging then works: n/10 − n/500 > n/11.
- **Claim 3 (cl:U)**, the edge bound (eq:outside), and the ratio estimates (eq:ratios). Exponents: 2/300−1/81 < 0, 1/300+1/243−1/81 < 0, and 1/300−1/2 < 0.
- **§5.4 peeling.** Edge count Σ_{Q_i} d_{F_i} ≤ 2τ|V̄_i|. By (eq:region-edges), every G-edge from v ∈ Q_i into L∪U lies in F_i, so d_0Σ|Q_i| ≤ 4τλ + e_G(I, outside).
- **Claim 4 (cl:C):** V̄_i ∩ I ⊆ S_i ∪ Q_i.
- **Claim 5 (cl:union):** for y ∈ P_1 ∩ R_i, (D1) puts every C-neighbour of y in R_i, hence in V_i.
- **Claim 6 (cl:C2):** Lemma 4.2 is applied with t = a^{1/6}, q = τ, d = d_1 = a^{1/3}. The hypotheses hold: disjointness since a^{1/9} < d_1; lightness gives fewer than t vertices of C_2 on any cycle; designations fewer than τ by Claim 5.
- **Claim 7 (cl:two-outside):** the case split is exhaustive.
  - A neighbour of degree < d_0 is covered by (eq:one-low), at most one.
  - A neighbour in P_0 counts toward C_2.
  - Any other neighbour lies in L∪U, so it is in F_i. If it is removed, (D2) excludes S_i and I, which forces it into R_i ∩ V̄_i with degree > d_1, i.e. into P_1.
- **§5.6:** |C'| ≥ λ/11 − o(λ) ≥ Σ|F_i|/12. Also |S| ≤ |F_i| < 2a² + 4a^{3/2} ≤ a³, and τ = a^{1/300} ≥ a^{3/1000} > |S|^{1/1000}.

### 1c. Theorem 1.4 (thm:qoh) holds (brief item 3)

**Citations, each checked in the source:**

| Paper says | Source says | Match |
|---|---|---|
| Thm 6.2(ii) (thm:bm, bm:split) with s-expander = (2^{-5}, s)-expander | BM Lemma 14 (ε ≤ 2^{-5}, delete ≤ 4sn log n edges, Σ\|G_i\| ≤ 2n) and BM Def 11 (\|N_{G−F}(U)\| ≥ ε\|U\|/log²n for 1 ≤ \|U\| ≤ 2n/3, \|F\| ≤ s\|U\|) | yes |
| Thm 6.2(i) (bm:paths) | BM Cor 22 (each vertex an endvertex of ≤ 2 paths ⇒ ≤ n paths) | yes |
| Thm 6.2(iii) (bm:bulk) | BM Thm 24 ("at most 6n cycles and O(n log^{274} n) edges") | yes |
| Thm 6.3(i) (cfs:dec) | CFS Cor 4.3 (same notion of sparse, CFS Def 1) | yes |
| Thm 6.3(ii) (cfs:random) | CFS Lemma 4.4 | yes (see Objection 1) |

**The new lemmas, each checked:**
- **Lemma 6.4 (lem:split):** the bad-pair union bound Σ_u m^{2u}·m^{−8u} ≤ 2m^{−6}.
- **Lemma 6.5 (lem:core):**
  - The peeling invariant: an edge from D to outside D∪T lies in F or hits Q_U, and e(U, Q_U) ≤ |U|·s/2 (simple graph). Expansion of D (which has |D| < 2m/3) then forces |D| < 2|F|/s.
  - Ball growth: (1+η/2)^{r/2} ≥ e^{ηr/8} = e^L > |K|.
- **Lemma 6.6 (lem:routing):**
  - Maximal B_0, with |F_i| ≤ rt|J_i|/2 ≤ s|J_i|/12.
  - |Q| ≤ t + tr/2 ≤ rt ≤ s/2.
  - The new paths of B avoid F_i, D_i, Y_B∖{x,y} and B's earlier interiors, so they are vertex-disjoint from each other and edge-disjoint from the fixed paths.
  - Failure count ≤ tΣ|D_i| ≤ (rt²/s)Σ|J_i|.
- **Lemma 6.7 (lem:short-cycle)**, **Lemma 6.8 (lem:grouping)** (conflict degree ≤ |A|/2 + 2d − 3), and **Lemma 6.9 (lem:medium-cycle)**. In 6.9, BM Lemma 14 with s = 2λ+2 removes at most 8(λ+1)m log m edges; Lemma 6.5 is used with F = ∅, so D = ∅ and Q = X with |X| = λ+1 = s/2.

**The main proof (§6.3):**
- |Z| ≤ 2|F|/δ ≤ 8nℓ/n^α.
- Claim 8: s ≥ 64h log m_i; s/(2h) ≥ n^α; 1/h = n^{−α/2} ≤ m_i^{−α/4} because m_i ≤ n².
- After the bulk step, e(H) ≤ βnℓ^{274} ≤ nλ, and |W| ≤ 3n/λ².
- The three construction kinds:
  - Pieces are vertex-disjoint within a class, and leftovers are ≤ 2j*(λ+1) edges per class.
  - Cherries in a group are vertex-disjoint, so the centres are distinct.
  - In B_odd cycles, the indices are distinct, so the only coincidences are y_{p−1} = x_p.
- Demand ends:
  - Every demand end lies in X_1.
  - Within one construction the ends are pairwise distinct.
  - Assigning each end its own H-edge gives at most d_H(u) ≤ λ³ demands per vertex.
- Cycle formation:
  - Joining paths live in R, which is disjoint from H.
  - Their interiors are pairwise disjoint and avoid Y_C.
  - So each construction closes to a simple cycle. In the k = 1 single-edge case the joining path has length ≥ 2, since R ∩ H = ∅ and the graph is simple.
- Count: 6+1+1+1+1+2+2+1 + 2b_α, i.e. (15+2b_α)n.

**The polylog-versus-polynomial inequalities hold for large n.** For ε = 1/1000 (α = 1/3000) the binding one is 128rλ⁹n^{1−α} ≤ n, at log₂ n ≈ 2.8·10⁸. So n_0 ≈ 2^{2.8·10^8}, which is finite (see §4).

### 1d. Classic holes (brief item 4)

- **Lemma assuming the conclusion's strength:** none. Theorem 1.3 is pure counting and uses no decomposition statement. Theorem 1.4 uses only BM's O(n) cycles + n·polylog(n) edges, which is strictly weaker than the conclusion.
- **Citation not saying what is claimed:** none found. Objections 1 and 4 are wording only.
- **"Clearly"/"standard" at a hard step:** a grep for clearly|standard|easy|routine|similar|obvious|well known|it follows finds none in a proof. The only "we may assume" steps are ε ≤ 1 and B_odd having an edge, and both are trivial.

### 1e. v1 → v2 (brief item 5)

v2 swapped out four pieces of v1:

| v1 | v2 replacement |
|---|---|
| Vertex weights 1/(d·h(d)) with Σ1/(jh(j)) < ∞ (Def 1.3 of v1, heavy iff total weight ≥ 1) | f(d) = 1−1/√(d+1) and "≥ b^{3/2} vertices of degree ≤ b" |
| Birmelé's treewidth bound + tree decompositions (v1 App. A.2) | Elementary DFS Lemma 3.2 |
| Random colouring with κ = 1000ℓ³ colours, κ reservoirs per expander, BM path-connectivity through random sets (v1 App. A.1), Aharoni–Haxell hypergraph Hall | Deterministic Alon–Capalbo-style core Lemma 6.5 + routing Lemma 6.6, one reservoir per expander |
| Expander edges closed into cycles separately | Absorbed by applying BM Thm 24 to G − E(R) |

The near-closed constant also changed, from 1/50 to 1/12. Each replacement is self-contained in v2 and I verified each directly, so no v1 argument that v2 still needs was dropped. The new potential is a valid potential on its own terms: any heaviness notion under which removing a heavy cycle drops Φ by at least 1 works, and this one does.

## 2. Objections (numbered; none above EXPOSITION)

**1. EXPOSITION — Thm 6.3(ii) (thm:cfs, cfs:random), used in Claim 8 (cl:reservoirs).**
- *Quoted:* "With probability 1−o(1) as m→∞, uniformly in p ≤ m^{−ρ}, the random graph G(m,p) is (ρ,2/ρ)-sparse."
- *Why:* CFS Lemma 4.4 says only "for q ≤ n^{−ε}, G(n,q) is almost surely (ε,γ)-sparse". Uniformity is needed here because p = n^{−α/2} is fixed by n while m_i ranges over (n^{2α}, n].
- *Why it is still true:* CFS's own proof bound, Σ_{v≥1}(em/v)^{−v^{2−ρ}} = o(1), does not depend on q. Equivalently, "for every sequence p(m) ≤ m^{−ρ}" already implies uniformity.
- *Fix:* write "by the proof of [cfs, Lemma 4.4]" and display that bound.

**2. COSMETIC — Lemma 6.6 (lem:routing) application in §6.3, "Joining paths": "with … L = ℓ".**
- *Why:* Lemmas 6.5 and 6.6 need L to be a positive integer with m ≤ 2^L, but ℓ = log n need not be an integer.
- *Fix:* take L = ⌈ℓ⌉. All bounds stay polylogarithmic. The same rounding applies in the proof of Lemma 6.9 (already ⌈log m⌉ there) and to the "ball of radius 1+log m" in Lemma 6.7, which should be ⌊1+log m⌋. The cycle bound 2⌊1+log m⌋+1 ≤ 2log m+3 still holds, and depth j = ⌊log m⌋+1 still exceeds log m.

**3. COSMETIC — Thm 6.2(ii) (bm:split) and §6.3 use s = n^{2α}, and λ = ℓ^{300}, as integers.** This is covered by the stated rounding convention (§1.2 Notation), so nothing breaks.

**4. EXPOSITION — §1.1: "they decompose each expander J into O(|J|) cycles and O(|J| log^{O(1)}|J|) edges [bm, Theorem 3]".**
- *Why:* BM Thm 3 is stated for *arbitrary* r-vertex graphs. The expander-specific statement is BM Lemma 23. The description is still correct (expanders are a special case).
- *Fix:* cite Lemma 23, or say "each part".

**5. EXPOSITION — the size of the constants.** The O(n) constant is astronomically large. This is not an error, but the paper never says so.
- Theorem 1.3 needs δ_0 with log₂ a ≳ 7.9·10³ (the §5.6 bookkeeping is dominated by |U| ≤ 1000a^{−1/300}λ log a) and Lemma 4.3 at d ≳ 10^{193}.
- Theorem 1.4 at ε = 1/1000 needs n_0 ≈ 2^{2.8·10^8}.
- So C_{1/1000} ≥ n_0/2 and k ≥ C_{1/1000}.
- *Fix:* the closing remark "our constant is large" could quantify this.

**6. EXPOSITION — Claim 2 (cl:window) uses "log a_j ≥ 3^{5j}", which tacitly needs log δ ≥ 1.** That is implied by "δ sufficiently large"; state it.

**7. EXPOSITION — §2.1 proof, paragraph on (c): "each of these vertices has degree at most 2<k, so (a) removes all its remaining edges".** A credited vertex may already have degree 0, in which case (a) does nothing and the vertex is simply isolated. The argument is unaffected; one clause would cover it.

I have nothing at GAP, UNCLEAR or FATAL. My hardest tries were:
- forcing a per-step cost to accumulate in §2.1 (impossible: (a) isolates permanently, (b) is paid by Φ, (c) by isolations);
- a Theorem 1.3 counterexample built from pendant cliques K_{d_0} whose vertices each have three high-degree parents (lightness forces the parents to be shared, and then S = clique ∪ parents is near-closed, which the proof finds through U);
- the U-vertices of huge F-degree inside Lemma 3.2 (they are forced into separators, and if removed (D2) and Claim 5 handle them);
- edge-disjointness and simplicity of the closed constructions in §6.3.

## 3. What I checked numerically (files)

All runs used `ulimit -v 4000000; timeout 1200; ~/.venv/bin/python -I`. The system python3 under -I has no sympy, so ineq.py failed under it at first. Directory: `/tmp/oaimath/181/seats/referee_kim_checks/`.

- **`ineq.py` → `ineq.rerun.out`** (the previous seat's script, re-run by me): 104 PASS, 0 FAIL.
  - Covers the §2.1 identity and convexity, f(d)−f(d−2) ≥ d^{−3/2} for d ≤ 2·10⁴ and 10^5..10^12, every Lemma 4.1/4.2 constant, Lemma 4.3's threshold (≈10^{193}), Claim 2's δ ≥ 1.1·10^{15}, and §5.6's closure at log₂a ≳ 7914.
- **`lem31_32.py 7` → `lem31_32.rerun.out`** (previous seat's script, re-run):
  - Lemma 3.1: 376 light graphs / 2923 (G,b) pairs, 0 violations; the negative control found 3.
  - Lemma 3.2 implemented literally: 300 random bounded-circumference instances, 0 failures; the negative control (truncated B_u) failed 100/100.
- **`sec6_checks.py` → `sec6_checks.out`** (mine): OVERALL PASS.
  - Lemma 6.7 (short cycle): 20,000 random multigraphs, 0 violations. Weak test, since small random graphs are full of short cycles; the negative control (bound 2) fails 11,576 times.
  - Lemma 6.8 (grouping), the proof's greedy implemented literally: 3,000 instances, 0 violations, max groups/(|A|+2d) = 0.385; the negative control (drop +2d) fails 775 times.
  - Lemma 6.5 (core), the peeling process implemented literally in the small regime where the s-expander condition reduces to e(X,X^c) > s|X|, with exhaustive search over (Q,U): 95 expander instances, |D| ≤ 2|F|/s and core connectivity for every |Q| ≤ s/2 held; non-expander negative control failed 7 times.
  - §6.3 "n large" inequalities at ε = 1/1000 (thresholds printed in log₂ n): all eventually true; the binding one is 128rλ⁹n^{1−α} ≤ n at log₂ n ≈ 2.8·10⁸.

What numerics cannot reach: Theorem 1.3 and Theorem 1.4 only take effect at δ_0 and n_0 of the sizes above, so no small-graph test of either theorem means anything. Their correctness here rests on the line-by-line reading.
