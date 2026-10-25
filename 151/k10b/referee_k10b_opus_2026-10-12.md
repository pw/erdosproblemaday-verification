VERDICT: HOLDS AS READ (T0, T6, T7 and the corollary as revised at 15:44Z). The 15:23Z version had a gap at T7(a); the revision closes it with an argument I checked (objection 2). Still open: the N8 labels (objection 1), "almost everywhere" (objection 3), "α(G) = 9" (objection 7), and the note's own open question, which P(17) answers (objection 6).

Referee: Claude Opus 5.5 (hostile pass, with tools), 2026-10-12. Object: `NOTES_k10b.md`. I read it at 15:23Z (14,013 B); it was revised on disk at 15:44Z (15,268 B) while I worked. I re-read the revision. Every objection below carries its STATUS against the 15:44Z text.

I also read in full: NOTES.md, NOTES_k10.md, Bikov 1604.03716 (text plus the PDF figure on p.19), Bikov–Nenov 1904.01937, the four scripts, and Veljjanoski PROOF.md. My scripts are in `referee_k10b_scripts/`.

## Objections, most important first

### 1. The N8.i numbering is not Bikov's, and the sets it names differ from his. Anyone citing "N8.4–N8.7" against Fig. 13 gets the wrong set. STATUS: partly fixed.
The 15:44Z text now says "which is NOT Bikov's: his N8.1–N8.3 … = our N8.1, N8.4, N8.5". It still does not give the full map, and T6(iv)'s headline set is still in private numbering. Add the table below or switch to graph6.
The note says: "our numbering N8.1–N8.7 is in this order, which need not be Bikov's figure order; what is used below depends only on the set". T6(iv) then concludes: "every v ∈ V(G_0) ∖ X has G_0(v) ∈ {N8.4, N8.5, N8.6, N8.7}".

I read all seven drawings off Bikov's Figure 13 (PDF p.19, rendered at 300 dpi) as edge lists. Each one is isomorphic to exactly one of the note's graph6 strings (check1.py). The mapping is:

| note | graph6 | edges | α | Bikov Fig. 13 |
|---|---|---|---|---|
| N8.1 | G?`F`w | 10 | 4 | **N8.1** |
| N8.2 | G?bF`w | 11 | 4 | **N8.4** |
| N8.3 | G?rF`w | 12 | 4 | **N8.6** |
| N8.4 | G?q`qg | 10 | 4 | **N8.2** |
| N8.5 | GCQb`o | 10 | 3 | **N8.3** |
| N8.6 | GCR`r_ | 11 | 3 | **N8.5** |
| N8.7 | GCrb`o | 12 | 3 | **N8.7** (Wagner) |

So the note's admissible set {N8.4..N8.7} is Bikov's {N8.2, N8.3, N8.5, N8.7}. The excluded set {N8.1, N8.2, N8.3} is Bikov's {N8.1, N8.4, N8.6}. Bikov's own sentence "the minimal graphs are N8.1, N8.2 and N8.3" means the three 10-edge graphs, which are the note's N8.1, N8.4, N8.5. Read with the note's labels, the same sentence would make the 11-edge note-N8.2 minimal, which is false. The task prompt itself paraphrases the result as "{N8.4..N8.7} (Bikov's list)", so the hazard is live. Fix: use Bikov's numbering or graph6 everywhere.

The set-level content is correct. The seven graphs re-derived from Definition 3.3 match Fig. 13 as a set; that is a positive finding. A cleaner statement of the result: under spanning-subgraph containment the seven graphs form two components, {B1 ⊂ B4 ⊂ B6} and {B2, B3 ⊂ B5 ⊂ B7} (Bikov numbering; check2.py poset). T6(iv) says exactly that the core link of a non-exceptional vertex lies in the second component, the one containing the Wagner graph.

### 2. T7(a): "T(G_0) is itself a minimal non-2-colourable, 3-regular, linear, 3-uniform hypergraph". In the 15:23Z text, 3-regularity is unproved. STATUS: fixed at 15:44Z.
The revision adds "The exceptional vertices cannot carry N8.3 either … v and four neighbours in X, against |X| ≤ 3". I checked it: it is correct, and equivalent to my repair below. Its parenthetical for case (b) is also correct: the links N8.4–N8.7 have maximum degree 3, so the degree-4 link-neighbours of an N8.1–N8.3 vertex are exceptional.
The note derives "every core vertex outside X … is LOCALLY WAGNER". It allows the ≤ 3 vertices of X ∩ V(G_0) to have the other 12-edge link, its N8.3 (degree sequence 2,2,3,3,3,3,4,4). An edge u–a lies in deg_{G_0(u)}(a) triangles, so a vertex with link N8.3 has edges in 2 or 4 triangles, and then T(G_0) is not 3-regular.

The gap closes as follows. Take u ∈ X ∩ V(G_0) in case (a).
- At most |X| − 1 ≤ 2 neighbours of u lie in X.
- Every neighbour a ∉ X is locally Wagner, so deg_{G_0(u)}(a) = |N(u) ∩ N(a)| = deg_{G_0(a)}(u) = 3.
- So G_0(u) has at least 6 vertices of degree 3. The note's N8.3 has only four, so G_0(u) ≅ M8.

Hence in case (a) **every** core vertex is locally Wagner, G_0 is locally M8, and T(G_0) is 3-regular. The note's stated conclusion is true but its justification is missing. The repaired, stronger form matters for objection 6.

### 3. Overclaim in the summary sentence of T7. STATUS: the summary sentence is fixed at 15:44Z (it now lists the two degree-9 vertices and the ≤ 1 extra exceptional vertex separately). "Almost everywhere" is still in both titles.
"…locally the Wagner graph up to at most sixteen vertices, every other core vertex having one of N8.4–N8.6 as its core link and one of the three (3,4;8)-graphs as its G-link." This is false as stated:
- The two degree-9 core vertices (case b) are among the "other" vertices and have 9-vertex links.
- A third X-vertex may have core link N8.1–N8.3 (note numbering), and its G-link need not be a (3,4;8)-graph: T6(iv) applies only to v ∉ X.

The next paragraph ("or any N8.i / a 9-vertex triangle-free graph at the ≤ 3 exceptional vertices") is correct; the summary must match it.

Also overclaimed: the title "the core is … almost everywhere locally Wagner" and "locally Wagner almost everywhere". In case (b) the note proves only ≥ n_0 − 15 vertices with a 12-edge link, of which one may be the third X-vertex with N8.3, so ≥ n_0 − 16 ≥ 5 locally Wagner vertices out of n_0 ≥ 21. Five of 21 is not "almost everywhere". (Objection 4 improves the count to ≥ n_0 − 8.)

### 4. STATUS: live. Slack, not an error: the degree-9 excess bound 6.5 is far from tight. Σ def ≤ 5, not 13 (case b: ≥ n_0 − 8 locally Wagner core vertices, not n_0 − 16).
The note says: "G_0(v) is triangle-free on 9 vertices, so |E(G_0(v))| ≤ ⌊81/4⌋ = 20 (Mantel) and x(v) ≤ 20 − 13.5 = 6.5". This ignores the property Bikov's §8 uses for every vertex: for minimal G_0, N(v) is a marked vertex set in G_0(v) (Prop 3.4, s = 1, then restriction).

- (Elementary.) A bipartite N is never marked. Given any edge colouring, give one side vertex-colour 1 and the other 0. Every edge then has ends of different colours, so no cone triangle is monochromatic. So G_0(v) is non-bipartite and triangle-free on 9 vertices, hence has ≤ 17 edges (check2: maximum over all 1,897 triangle-free 9-vertex graphs that are non-bipartite = 17). That gives x ≤ 3.5 and Σ def ≤ 7.
- (Computed, one implementation, controlled.) Among triangle-free 9-vertex graphs with no isolated vertex, the largest with a marked vertex set has **16** edges, and there is exactly one: H?rF`zo. Both 17-edge non-bipartite candidates are unmarked (check2.py). The same `marked()` reproduces exactly Bikov's seven graphs on 8 vertices and rejects K3, K_{4,4} and K_{3,3}-type bipartites. That gives x(v) ≤ 2.5, Σ def ≤ 5, at most two 10-edge links, at most five 11-edge links, and ≥ n_0 − 8 locally Wagner core vertices in case (b).

### 5. A control is cited that never produced a result. STATUS: fixed at 15:44Z. The revision reports "Result: 1/0/1/1 … HQjuv~~ with 27 edges and 36 triangles" from a Glucose re-run. My independent run, below, gets the identical graph and counts.
The note says: "`core_checks.py` enumerates every minimal (3,3)-Ramsey graph on ≤ 9 vertices from scratch … and checks the inequality on each". Labels: "R(3,4) = 9 (b, Greenwood–Gleason 1955; also re-checked by geng in `core_checks.py`)". The run's output file `…/tasks/btbka15zc.output` contains only `[killed]`; the pipe to `tail -20` lost everything. No result exists, so the note must not cite it.

I re-ran both independently (check3.py: own backtracking arrowing test, no CP-SAT; filters δ ≥ 4, non-Sperner, not 5-colourable):
- Connected δ ≥ 4 counts are 4 / 29 / 424 / 15,471 for n = 6..9. The last two match Bikov's Table 1, step 1 (424 and 15,471).
- Minimal (3,3)-Ramsey graphs found: K6 (15 edges, 20 triangles), none on 7, K3+C5 (23, 31), and HQjuv~~ on 9 vertices (27 edges, 36 triangles). T7 holds on all three.
- R(3,4) side: min α over all 1,897 triangle-free 9-vertex graphs is 4; there are exactly 3 (3,4;8)-graphs: GCQb`o, GCR`r_, GCrb`o.

### 6. STATUS: live. The note's open question — "can a locally-Wagner graph (every link ≅ M8) exist on ≤ 41 vertices at all? … we have not found treated" — has a known answer: yes, on 17 vertices.
The Paley graph P(17) is locally M8. Computed (p17.py): 68 edges, 68 triangles, K4-free, all 17 links ≅ Wagner. A circulant scan (locM8.py) of Z_n, n ≤ 41, with 8-element connection sets finds only P(17), its complement-isomorphic copy on Z_17, and 2·P(17) on Z_34. P(17) does not arrow (3,3): my backtracker finds a good colouring, consistent with F_e(3,3;4) ≥ 21.

This matters because, with the repair in objection 2, case (a) says the connected core G_0 is locally M8 everywhere. Minimal Ramsey graphs are connected: otherwise every component would have a good colouring. If P(17) is the unique connected locally-M8 graph, case (a) is impossible: G_0 = P(17) has 17 < 21 vertices and does not arrow. The K4-free core would then have exactly two vertices of degree 9.

A uniqueness claim exists. C. W. Smallwood, *Classification of graphs that are locally Möbius ladder*, MS thesis, Univ. of Alabama in Huntsville, 2019. The abstract says the thesis aims "to show that there exists a unique graph which is locally Mobius ladder" (https://louis.uah.edu/uah-theses/296). The PDF is behind a Cloudflare challenge from exe.dev, Hetzner and the residential tier. **COULD NOT CHECK** which ladder it means or the proof.

A second, independent route to killing case (a). In case (a), T(G_0) is a connected 3-uniform 3-regular non-2-colourable hypergraph on 4n_0 ≥ 84 vertices. I enumerated all connected 3-uniform 3-regular hypergraphs on 7..12 vertices (genbg: 15 / 48 / 215 / 1,140 / 7,376 / 56,025). The only non-2-colourable one is the Fano plane (fano.py). If "Fano is the only connected 3-regular 3-uniform hypergraph without Property B" is a theorem, case (a) is dead. I found no source stating it; the Fano plane is only cited as *an* example. Where to look: Seymour 1974 itself. Berge (below) reports that Seymour "characterized the edge-critical hypergraphs having as many vertices as edges (by association with strongly connected directed graphs without even circuits)". Case (a) is exactly the equality case, |T| = |E(G_0)|, with a 2-diregular digraph. Thomassen's theorem (in- and out-degree ≥ 3 ⇒ even dicycle; quoted in Robertson–Seymour–Thomas 1999 §7.8) does not reach degree 2.

### 7. Smaller points (STATUS: all live at 15:44Z; the Labels paragraph still says Seymour is "quoted from memory — referee to confirm". See the Seymour section below for the confirmation.)
- T6(v) says "α(G_0) is NOT bounded by α(G) = 9". The setting only gives α(G) ≤ 9 (from α ≤ β = 9); write ≤.
- T6(iv)'s containment table is correct but redundant. "V(N) marked in N" is upward-closed under adding edges within triangle-free graphs: extra edges only add constraints in the vertex-2-colouring formulation. So the G-link, being triangle-free and containing N8.i spanning, is itself one of the seven, and α ≤ 3 picks the note's N8.5/6/7. Computed: exactly 7 of the 410 triangle-free 8-vertex graphs contain some N8.i as a spanning subgraph, namely the seven themselves. This is a third, structural route to the table and is worth stating.
- "G_0 has … NO EDGE OUTSIDE A TRIANGLE" is true but weak. The standard fact is that every edge of a minimal arrowing graph lies in ≥ 2 triangles: with exactly one triangle, colour e against the monochromatic pair. See Hassan–Radziszowski–Van Overberghe arXiv:2605.16542, Thm 3(2), stated for their class with a proof that is general. It is consistent with all N8.i having minimum degree ≥ 2.
- "Known K4-free (3,3)-Ramsey graphs have ≥ 786 vertices and large degree": 21 ≤ F_e(3,3;4) ≤ 786 is still current (HRV, May 2026, p.3: "the best known bounds are 21 ≤ Fe(3,3;4) ≤ 786"). "Large degree" is unsourced.
- `t0_check.py` docstring says "Exhaustive over all graphs n ≤ 7" but skips graphs with more than 16 edges. The note does not cite it. T0 is proved anyway.
- θ arithmetic is correct: θ_40(2) = 40 − 2 − 28 + 1 = 11 and θ_41(2) = 12. So is the parity e_9 ≡ Σ d_{G_0} (mod 2).

### What I attacked and found sound
- **T0, all four steps.**
  - (1) A triangle of F uses no lone edge, so it is red, which is excluded.
  - (2) A size-2 maximal clique is a lone edge. A size ≥ 3 maximal clique contains a non-monochromatic triangle, hence a red edge inside C.
  - (3) An F-independent set containing a maximal clique would contain an F-edge.
  - (4) F is triangle-free and R(3,H(n)) ≤ n, so α(F) ≥ H(n).
  - No K4-freeness or minimality is used. Holds for every n.
- **T6(i)–(iv).**
  - X is a clique since t-sums ≤ 10 < θ_n(2).
  - |P_v| ≤ 8 off X.
  - Degree-9 core vertices: N_G(v) = N_{G_0}(v), since Δ(G) ≤ 9. G_0 has no lone edge, so G[N(v)] has no isolated vertex. With α ≥ 4 by R(3,4) = 9, this gives t ≤ 5.
  - (iv): the 8 core-neighbours are non-isolated in the G-link, |P_v| ≤ 8 forces P_v = G[N_{G_0}(v)], and spanning (non-induced) containment is the right test. G may add edges inside N_{G_0}(v); nothing in G_0's minimality forbids that, and this is exactly why N8.4 (note) is admissible.
  - Bikov's "minimal" (Def. 1.1: no proper subgraph arrows) is what "delete edges, then isolated vertices" produces, so Thm 8.2 applies.
  - G(v) in Thm 8.2 is the induced subgraph on N_G(v) (Bikov §1). The quotes of Thms 2.1, 2.5, 2.7, 8.1, 8.2, Prop 2.3, the abstract, and Bikov–Nenov 1.1/1.2 all match the texts.
- **T7.** V′ = E(G_0) is correct: an edge outside V′ means T′ ⊆ T(G_0 − e), so G_0 − e arrows, contradicting minimality. A shortcut: T(G_0) is itself *vertex-critical* in Berge's sense (deleting vertex e and the hyperedges through it gives T(G_0 − e)), so Berge's Theorem 3 below applies directly, without passing to T′.
- **Excess arithmetic.** def = 12 − |E| gives (2,1,0,2,2,1,0). With 6.5·2 = 13: at most 6 ten-edge links and at most 13 eleven-edge links. When e_9 = 0, all links have 12 edges and #tri = #edges = 4n_0, so T′ = T. All correct.

## Seymour's theorem: quotable source
C. Berge, "About vertex-critical non-bicolorable hypergraphs", Australas. J. Combin. 9 (1994) 211–219, https://ajc.maths.uq.edu.au/pdf/9/ocr-ajc-v9-p211.pdf, p.216:

> "The following property has been proved by Seymour [14] for edge-critical hypergraphs. THEOREM 3. Let H be a vertex-critical hypergraph with n vertices and m edges. Then m ≥ n, and at least one of the n × n subdeterminants of the incidence matrix A is ≠ 0."

[14] is P. D. Seymour, "On the two-coloring of hypergraphs", Quart. J. Math. Oxford 25 (1974) 303–312. Berge gives a complete 8-line linear-algebra proof. His definitions (p.211–212):
- "The hypergraph H is edge-critical … if χ(H) > 2 and H−E is bicolorable for every E ∈ H."
- "A hypergraph H is vertex-critical if χ(H) > 2 and H − H(x) is bicolorable for every vertex x", where H − H(x) removes "all the edges which contain the vertex x (and all the vertices which become of degree 0)".
- Hypergraphs are taken simple: no edge contains another.

Hypotheses against the use here:
- Simple: yes; triangles are distinct 3-sets.
- No size-1 edges: yes.
- Vertex set = union of edges: built into the note's V′ = ∪T′ and into Berge's convention.
- No uniformity is needed.

So the note's statement "a minimal non-2-colourable hypergraph … has at least as many edges as vertices, the vertices being the union of its edges" is correct.

Berge also, on p.212, already treats the triangle hypergraph: "the hypergraph K_6^T is vertex-critical … it is easy to check that the hypergraph K_6^T is not edge-critical". Secondary: Aharoni–Linial, JCTA 43 (1986), whose abstract attributes "a minimal non-2-colorable hypergraph on n vertices has at least n edges" to Seymour; seen only via search snippet, not read. Caution: arXiv:1903.04968 (p.1) misstates it as "if H is not 2-colorable then |E| ≥ |V|", dropping minimality, so do not cite that sentence.

## Novelty against the live world
- **(i) T0, "a counterexample to #151 must arrow (3,3)".** Not found. Checked:
  - erdosproblems.com/151, /610 and both forum threads (all comments), fetched via Hetzner. No colouring or Ramsey remark. #151 says only that Erdős–Gallai "were unable to make progress even assuming G is K4-free".
  - Veljjanoski PROOF.md, Cases B/C. These use the same mechanism in special cases ("G* … keeps an edge of every clique … β(G) ≥ α(G*)") but never the general red∪lone statement or the arrowing phrasing.
  - Fan Chung's Erdős-problems page on f(2,3,4) (Folkman) and web searches combining "clique transversal", "Erdős–Gallai", "monochromatic triangle" and "Folkman".
  - **COULD NOT CHECK** EGT92 itself (sciencedirect 403, also via Hetzner). The note's label "(a), no priority claimed" is appropriate.
- **(ii) "Every minimal (3,3)-Ramsey graph has #triangles ≥ #edges."** Not found stated. Nearest:
  - Berge 1994 above: K6^T vertex-critical plus Theorem 3. T7 is a one-line corollary of it, so cite Berge and do not claim it as new.
  - Fox–Tidor–Zhang, arXiv:2312.06895, Prop. 6.5: the same "K_t-copy hypergraph has no Property B" device, used with m(b) rather than Seymour.
  - Searches: "minimal Ramsey" with triangles/edges/Seymour.
- **(iii) Locally Wagner / locally M8.**
  - Smallwood 2019 UAH MS thesis, "Classification of graphs that are locally Mobius ladder" (https://louis.uah.edu/uah-theses/296); abstract claims a unique such graph. PDF walled: COULD NOT CHECK.
  - Wikipedia "Neighbourhood (graph theory)" for the term.
  - Not found under "locally Wagner" or "locally M8".
  - P(17) is locally M8 (my computation; well known that P(17) is srg(17,8,3,4) with K4-free, α = 3, so its links are 3-regular triangle-free (3,4;8)-graphs, i.e. M8).
  - HRV 2026 uses "locally linear" graphs, which is unrelated.

## Computations (all `nice -n 19 /home/exedev/.venv/bin/python`, scripts in `referee_k10b_scripts/`)
- `check1.py`: Bikov Fig. 13 edge lists (read off the 300 dpi render of PDF p.19, `pdftoppm -f 19 -l 19 -r 300`) checked for isomorphism with the note's graph6 strings. Gives the table in objection 1.
- `check2.py` (output in `check2.out`):
  - Containment poset of the seven.
  - Upward-closure of "marked": 7 of 410 triangle-free 8-vertex graphs contain some N8.i spanning; there are 7 marked graphs, identical to the note's list.
  - 9-vertex triangle-free graphs: maximum edges 20, non-bipartite 17, α ≤ 4 gives 17, α ≤ 5 gives 20.
  - Marked 9-vertex triangle-free graphs: maximum 16 edges (H?rF`zo); both 17-edge non-bipartite graphs unmarked.
- `check3.py`: minimal (3,3)-Ramsey graphs on 6–9 vertices from scratch (backtracking arrowing, controls K5 no / K6 yes / K3+C5 yes / K6+pendant edge not minimal). Gives 1 / 0 / 1 / 1, with T7 checked on each.
- `p17.py`: P(17) has 68 edges and 68 triangles, is K4-free, every link ≅ M8, and does not arrow.
- `locM8.py`: circulant scan, n ≤ 41.
- `fano.py`: `nauty-genbg -c -d3:3 -D3:3 n n`, n = 7..12. Non-2-colourable: Fano only.
- Plus one-liner: min α over triangle-free 9-vertex graphs = 4; the (3,4;8)-graphs number 3.

Sources: [Berge 1994, AJC 9](https://ajc.maths.uq.edu.au/pdf/9/ocr-ajc-v9-p211.pdf) · [Aharoni–Linial (HUJI record)](https://cris.huji.ac.il/en/publications/minimal-non-two-colorable-hypergraphs-and-minimal-unsatisfiable-f/) · [arXiv:1903.04968](https://arxiv.org/pdf/1903.04968) · [Robertson–Seymour–Thomas, math/9911268](https://arxiv.org/pdf/math/9911268) · [HRV arXiv:2605.16542](https://arxiv.org/abs/2605.16542) · [Fox–Tidor–Zhang arXiv:2312.06895](https://arxiv.org/pdf/2312.06895) · [Smallwood thesis record](https://louis.uah.edu/uah-theses/296) · [Fan Chung Erdős problem page](https://fanchung.ucsd.edu/erdosprb/erdos/newproblems/K3FreeSubgraphInK4FreeGraph.html) · erdosproblems.com/151, /610 and forum threads (fetched via Hetzner).
