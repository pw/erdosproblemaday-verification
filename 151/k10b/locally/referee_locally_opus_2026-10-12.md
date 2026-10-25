# Referee report: `locally.py` and the claim "locally-M8, connected, ≤ 41 vertices ⇒ P(17) or the 21-vertex graph"
(Claude Opus 5.5, hostile-referee seat, 2026-10-12 ~16:05–16:40Z. Scripts and logs are in `referee_opus_2026-10-12/`:
`scripts/` holds the code, `logs/` the outputs. Every number below comes from a log in that directory.)

**VERDICT: ENUMERATION HOLDS. It is also stronger than claimed: the NMAX cap never binds, so P(17) and G21 are the only connected locally-M8 graphs of ANY order.** I found no bug and no third graph.

## Objections, most important first

1. **The literature the notes cite is false. Treat the enumeration as the only evidence.** NOTES_k10b.md, section
   "Locally-Wagner graphs exist", cites Smallwood (UAH MS thesis, 2019) for "there exists a unique graph which is
   locally Mobius ladder" and records the PDF as COULD NOT CHECK. I retrieved it from the Wayback snapshot
   `web.archive.org/web/20240606050855id_/https://louis.uah.edu/cgi/viewcontent.cgi?article=1295&context=uah-theses`
   (47 pp; text in `referee_opus_2026-10-12/source/smallwood2019_text.txt`). Its Theorem 4.17 ends: "Thus, it has been shown that (Z17 , Q) is the
   only M8 -local graph."
   - **The theorem is false.** G21 is locally M8. `scripts/links.py` checks this by an explicit isomorphism
     C8(1,4) ← G21[N(v)] for each of the 21 vertices, found by brute force over all 8! maps (no networkx matcher).
   - **Where the proof breaks.** G21's distance-2 profile is (p2,p3,c4) = (8,0,4): from each vertex, 8 vertices have
     common neighbourhood K2 and 4 have common neighbourhood C4 (`logs/links.log`). That is exactly the thesis's
     "Case 1: (8,0,4)", which it claims ends in a contradiction ("N(v,w1) = {1,4,v1,v3} induces a P4").
   - **Another visible slip.** Corollary 4.7's list of possible G_{u,v} drops C4, even though the paragraph before
     Lemma 4.5 includes it. G21 has 42 pairs with G_{u,v} = C4.
   - **MathWorld is incomplete too.** Its Local Graph table lists only the 17-Paley graph for the "4-Möbius ladder".
   - So no published source corroborates the lemma, and the one cited contradicts the search. Drop the Smallwood
     citation as support. If cited at all, cite it as refuted by G21. I found G21 in no source as a locally-Wagner
     graph.

2. **Missing receipt: the cap never binds, and the code cannot show it.**
   - `self.found = []; self.nodes = 0; self.verbose = verbose; self.t0 = time.time(); self.maxn = 0` (line 25):
     `maxn` is declared and never updated.
   - Nothing counts the new-vertex branches refused at
     `if n + newcount + 1 <= self.nmax:` (line 105).
   - Instrumented with `scripts/capcheck.py`, logs `capcheck_M8_41.log` and `capcheck_M8_1000.log`:
     - locally.py: at most **23** vertices in any state, **0** refused branches. Node count **17950** at both NMAX=41
       and NMAX=1000.
     - My independent search: at most **21** vertices in any state, 0 refused, **9364** nodes at NMAX 41, 60 and 1000.
   - So the result is "exactly two connected locally-M8 graphs, of any order". The 21..41 window in §T7(a) no longer
     matters. Only G21 has the order the core needs (≥ 21), and it does not arrow (§5 below). State the lemma in this
     stronger form and make the script print maxn and the refusal count.

3. **`record()` (lines 56–63) never checks that its output is locally X.** A completion bug that produced a wrong
   graph would still be printed as `FOUND`. Here `test_found.py` re-checks both graphs and my re-run agrees
   (`logs/test_found_rerun.log`), so the result is unaffected. Add an assertion anyway.

4. **The docstring controls (lines 9–10) are too weak to catch a bug in the Aut quotient or the slot filling.**
   - K3, C4 and C5 take 4, 6 and 13 search nodes. Petersen ≤ 21 takes 30 nodes and has one answer.
   - Petersen ≤ 65 (Hall's 63- and 65-vertex graphs) did **not finish**: locally.py ran 300 s, the independent search
     200 s. Neither program has reproduced Hall's two larger graphs.
   - Replaced below by controls with several answers each. Mutation tests show these controls catch three distinct
     defects.

5. **Harmless inefficiency, no effect on completeness.** `U = [u for u in range(n) if u != v and u not in adj[v] and u not in non[v]]`
   (line 76) can contain CLOSED vertices. Closing writes `non` only for vertices that exist at that moment
   (lines 135–136), so a vertex created later is missing from the closed vertex's `non` set. Such a branch dies at
   `if a in closed or b in closed or b in non[a]: return False` (line 118). The pre-check at line 92 only catches
   closed vertices among v's known neighbours.

## The specific attacks, (a)–(e)
- **(a) `embeddings()`.** The test `(w in adj[u] and not ex) or (w in non[u] and ex)` (line 38) is invariant under
  Aut(X), so `out` is a union of Aut-orbits, and `orbit_min == phi` (lines 43–44) keeps exactly one map per orbit.
  - Completions from s∘φ match those from φ: send slot assignment A to A∘s⁻¹. The relations `complete()` forces
    (lines 128–132) depend only on X-adjacency of positions, which s preserves.
  - The two states therefore differ only in how the new vertices are numbered (slots are visited in increasing order,
    line 79). The search from a state is complete under any numbering (point (e)), so nothing is lost.
  - Mutation: adding a non-automorphism (i ↦ 3i mod 8) to `self.auts` loses G21 on M8 and the 15-vertex graph on Q3
    (`logs/mutate.log`).
- **(b) `fill()`.** The pre-checks (lines 88–101) reject a vertex u only in these cases:
  - u is already used;
  - X needs an edge to w, but uw is a forced non-edge, or w is closed and u is not already its neighbour;
  - X needs a non-edge, but uw is already an edge.

  Each case contradicts every completion of the current state. A single new-vertex branch is enough because new
  vertices carry no relations until `complete()`. Mutations: "never reuse an existing vertex" loses BOTH M8 graphs and
  Q3's 15. "Drop one Aut-orbit representative" loses P(17) and Q3's 15.
- **(c) `complete()`.** It adds only the X-structure on N(v). It rejects only on real contradictions:
  - the edge would touch a closed vertex that lacks it (a closed neighbourhood is final);
  - the pair is a forced non-edge;
  - a degree would exceed k;
  - X needs a non-edge where an edge already exists.

  A vertex that reaches degree k with the wrong link cannot survive. At its own turn, `embeddings` needs a bijection
  K→X that respects every decided pair. Any undecided pairs are then forced by `complete()`, and the degree cap at
  line 120 blocks extra edges. Both programs' outputs pass explicit link checks.
- **(d) NMAX.** Only line 105 reads `nmax`, and it never binds (objection 2).
- **(e) Start and order.** Let G be connected and locally X. Take any vertex g0 and label N(g0) by an isomorphism to X,
  matching `run()`.
  - Invariant: the state agrees with G. Decided edges and non-edges are G's, and closed vertices have their full
    G-neighbourhoods.
  - Step: when v is completed, an isomorphism ψ: G[N(v)]→X restricted to K is a valid embedding, so some s∘ψ|K is
    enumerated. Each slot of s∘ψ is either a labelled undecided vertex (in U, and it passes the pre-checks) or an
    unlabelled one (the new branch).
  - The labelled set never exceeds |V(G)|. By connectivity, all of G is labelled by the time v reaches n.

## Controls run (nice 19; `logs/`)
| X | answer expected (source) | locally.py | independent search (`scripts/indep_search.py`) |
|---|---|---|---|
| K3, C4, C5 (NMAX 30) | K4, octahedron, icosahedron | ✓ (4/6/13 nodes) | ✓ |
| Petersen, NMAX 21 | K(7,2) (Hall 1980) | ✓ 30 nodes | ✓ 68 nodes |
| Petersen, NMAX 65 | 21, 63, 65 (Hall) | did not finish in 300 s | did not finish in 200 s |
| **Q3**, NMAX 41 | 24-cell and complement of K3□K5 (Buset; I took the statement from Smallwood's survey §2.2, which I did not check against Buset) | [24, 15] ✓ 370 nodes | [15, 24] ✓ 62 nodes |
| **K3□K3** (3×3 rook), NMAX 40 | complement of K4□K4 and J(6,3) (Buset's locally-grid-complement theorem as surveyed by Smallwood; the 3×3 rook graph is self-complementary) | [16, 20] ✓ | [16, 20] ✓, AGREE |
| K3,3, NMAX 40 | K3,3,3 | ✓ | ✓, AGREE |
| **C6**, NMAX 15 and 20 (infinite family) | 6-regular torus and Klein-bottle triangulations | 5 / 25 graphs | 5 / 25, AGREE |
| **icosahedron**, NMAX 40 | only the 40-vertex 600-cell quotient (Blokhuis–Brouwer–Cohen–Buset: 40, 60, 120) | did not finish in 200 s | exactly one graph, 40 vertices, 81 s |

- Every named answer was checked by isomorphism to an explicit construction (`logs/ident_controls.log`), e.g. the
  24-cell built from the D4 roots joined at inner product 1.
- C6 third source (`scripts/torus.py`): all quotients of the triangular lattice by sublattices of index ≤ 20 give
  18 graphs. All 18 are in the search output, and the search output has exactly 18 orientable surfaces (H2(Z) = Z).
  The other 7 are Klein bottles.
- Mutations of locally.py (`scripts/mutate.py`):

  | mutation | M8 result | Q3 result |
  |---|---|---|
  | none | [17, 21] | [15, 24] |
  | over-quotient | [17] | [24] |
  | never reuse existing vertex | [] | [24] |
  | drop an orbit representative | [21] | [24] |

  The M8 result and the Q3 control each detect all three defects.
- **M8 re-run:**
  - locally.py, NMAX 41: two graphs (21 vertices then 17), 17950 nodes, 37.4 s, the same as `M8_41.log`.
  - Independent search: 3 labelled completions, 2 up to isomorphism, 9364 nodes, 18.4 s.
  - The nauty canonical forms of the two outputs are **identical**.

## Attempts to build a third locally-M8 graph (all failed)
- **Every group of order 9..41 (all 168 groups).**
  - Groups came from GAP 4.12.1 SmallGroups. This covers non-abelian orders 21, 24 (15 groups), 27, 32 (51), 36, 39,
    40 and the rest (`scripts/export.g`, `scripts/cayley_scan.c`, 5 s).
  - For each group I enumerated every inverse-closed 8-subset S of G∖{e} whose link graph (s~t ⟺ s⁻¹t ∈ S) is cubic,
    triangle-free and has α = 3. That characterises M8: `geng -t -d3 -D3 8` gives exactly Q3 (α = 4) and M8.
  - Hits:
    - Z17: 2 sets, both P(17);
    - F21 = Z7⋊Z3: 21 sets, all G21;
    - D34 and Z34: 2 sets each, all the disconnected 2·P(17).
  - No other group carries one (`logs/cayley_counts.txt`, `logs/cayley_post.log`).
- **Covers.**
  - Any connected cover of the clique complex has a 1-skeleton that is again locally M8: triangles lift, and a
    3-cycle downstairs can only be a triangle.
  - Both clique complexes are simply connected: coset enumeration gives |π1| = 1, and H1(Z) = H1(F2) = 0.
  - χ = n, and H2 is free of rank n−1 (`logs/pi1.log`).
  - So neither graph has a locally-M8 double or triple cover. The 34-vertex double of P(17) would have been inside the
    window; it does not exist.
- **Independent exhaustive search with no cap:** see objection 2.

## Identification of the 21-vertex graph G21 (`T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB`)
- **Basic invariants.**
  - 8-regular, 84 edges, 84 triangles. Every edge lies in exactly 3 triangles.
  - Girth 3, diameter 2. From any vertex, the distance counts are 1 / 8 / 12.
  - Non-adjacent pairs: μ = 2 for 84 pairs (common neighbourhood induces K2) and μ = 4 for 42 pairs (common
    neighbourhood induces C4). So it is **not distance-regular**.
  - Stab(0) has suborbits 1, 8, 8, 4 (a rank-4 scheme).
  - α = 5, ω = 3. Spectrum 8¹, (2√2)⁶, (−1)⁸, (−2√2)⁶.
- **Automorphism group.** |Aut| = 336. **Aut ≅ PGL(2,7) ≅ PSL(3,2):2**: GAP gives IdGroup(Aut) = [336,208] =
  IdGroup(PGL(2,7)). The derived subgroup has order 168 and the centre is trivial.
- **Fano flag model.** Vertices are the 21 flags (p,L) of the Fano plane (lines {i, i+1, i+3} mod 7), with
  **(p,L) ~ (q,M) ⟺ p ∉ M and q ∉ L**. This is isomorphic to G21.
  - Equivalently, G21 is the **distance-3 graph of L(Heawood)**, the point graph of the generalized hexagon GH(2,1),
    which is distance-regular with intersection array {4,2,2;1,1,2}. The distance-2 graph is NOT isomorphic to G21.
  - The μ = 4 relation is the 4-valent suborbit: flags sharing a point or a line, i.e. adjacency in L(Heawood).
- **Cayley model.** G21 is a **Cayley graph of F21 = Z7⋊Z3**, with (a,b)(c,d) = (a + 2^b·c mod 7, b + d mod 3) and
  S = {(0,1),(0,2),(1,0),(1,1),(2,1),(3,2),(6,0),(6,2)}. All 21 locally-M8 connection sets on F21 give G21, and Aut
  contains non-abelian regular subgroups of order 21.
  - It is not a circulant, so the previous referee's circulant scan could not have seen it.
- **Literature search.** Queries "locally Möbius ladder", "locally Wagner", and the Wagner/Paley-17/21-vertex
  combinations turned up only Smallwood (refuted above) and MathWorld (lists P(17) only).
- Scripts: `ident21.py`, `fano.py`, plus a GAP check.

## Arrowing re-verification (`scripts/arrow_bt.py`; no SAT/CP library)
- **Method.** A plain DFS over edges. Whenever two edges of a triangle share a colour, the third is forced to the
  other colour, and three equal colours is a conflict. The first edge is fixed red.
- **Controls.** K5 has a good colouring. K6 and Graham's K3+C5 have none, so both arrow.
- **Results.** Both graphs have a 2-colouring with no monochromatic triangle, so **neither arrows (K3,K3)^e**. A
  literal recount over all vertex triples finds **0** monochromatic triangles for each. Vertex labels follow the
  graph6 order in `M8_41.g6`.
  - G21 (40 DFS nodes), red edges: (0,1)(0,2)(0,3)(0,4)(0,5)(0,6)(0,7)(0,8)(1,9)(1,10)(1,11)(1,12)(2,9)(2,11)(2,13)(2,14)(3,13)(3,14)(3,15)(3,16)(4,10)(4,15)(4,16)(4,17)(5,10)(5,11)(5,17)(5,18)(6,11)(6,13)(6,18)(6,19)(7,13)(7,15)(7,19)(7,20)(8,10)(8,12)(8,15)(8,20)(9,16)(9,20)(12,14)(12,19)(14,17)(16,18)(17,19)(18,20); all other 36 edges blue.
  - P(17) (29 DFS nodes), red edges: (0,1)(0,2)(0,3)(0,4)(0,5)(0,6)(0,7)(0,8)(1,9)(1,10)(1,11)(1,12)(2,9)(2,11)(2,13)(2,14)(3,9)(3,12)(3,13)(3,15)(4,12)(4,13)(4,14)(4,16)(5,10)(5,12)(5,15)(6,11)(6,14)(7,10)(7,15)(7,16)(8,10)(8,11)(9,16)(10,13)(10,14)(11,15)(11,16); all other 29 edges blue.
- `test_found.py` re-run agrees: glucose = False and cpsat = False for both graphs.
- **What this means for the lemma.** G21 has exactly 21 vertices, so the order bound F_e(3,3;4) ≥ 21 does NOT rule
  it out. Its failure to arrow is what kills it, and that is now confirmed by three independent methods. With the
  classification complete for every order, the 8-regular case (T7(a)) is empty.
