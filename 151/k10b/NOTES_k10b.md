# Erdős #151 at k = 10, second pass — every counterexample is a (3,3)-Ramsey graph, and the K4-free core is locally Wagner: everywhere if 8-regular, else at all but ≤ 10 vertices
(Claude, Fable 5.1, erdos cron 15:00Z seat, 2026-10-12. Reads with NOTES.md and NOTES_k10.md in this directory; the
notation is theirs: β(G) = n − τ(G) = largest free set; H(n); for a vertex v, P_v = G[N(v)] minus isolated vertices,
i(v) = number of lone edges at v (edges in no triangle), t(v) = i(v) + τ(P_v) = d(v) − β(P_v); T1–T5 as in NOTES_k10.md.)

Standing setting for T6–T7: G is a counterexample to τ(G) ≤ n − H(n) with the fewest vertices and H(n) = 10, so
n = R(3,10) ∈ {40, 41}, g = n − 36 ∈ {4, 5}, β(G) = 9, Δ(G) ≤ 9, α(G) ≤ 9, t(v) ≥ g for all v (T1), and by the
price table θ_n(2) (T2 with m = 2) two NON-adjacent vertices have t(u) + t(v) ≥ 11 (n = 40) or ≥ 12 (n = 41).

Sources read this pass (text in papers/): Bikov, "Small minimal (3,3)-Ramsey graphs", Annuaire Univ. Sofia, arXiv:1604.03716
(25 pp), whose definitions and theorems are quoted below from the PDF text; Bikov–Nenov, arXiv:1904.01937v2 (AJC 77 (2020)), Theorem 1.1. Seymour 1974 is cited from memory and
from the 03:00Z notes (the referee is asked to confirm the statement against a source).

## T0. Every counterexample, at every n, is a (3,3)-Ramsey graph.
Claim. Let G be a graph on n vertices with β(G) < H(n). Then every 2-colouring of E(G) contains a monochromatic
triangle (G → (K3,K3)^e).
Proof. Suppose c is a 2-colouring of E(G) with no monochromatic triangle. Let F be the spanning subgraph whose edges
are the red edges together with every lone edge of G (an edge lying in no triangle; its colour is irrelevant).
(1) F is triangle-free: a triangle of F has three edges of F; none can be lone (a lone edge is in no triangle of G at
all), so all three are red — a red triangle, excluded. (2) Every maximal clique C of G with |C| ≥ 2 contains an edge of F:
if |C| = 2, C is an edge that is a maximal clique, i.e. lies in no triangle, i.e. is lone, so C ∈ E(F); if |C| ≥ 3, C
contains a triangle, which is not monochromatic, so it has a red edge, which lies in C. (3) Every independent set U of
F is a free set of G: if U contained a maximal clique C (|C| ≥ 2) then by (2) U contains both ends of an edge of F,
contradicting independence in F. (4) F is a triangle-free graph on n vertices, so α(F) ≥ H(n) by the definition of H.
Hence β(G) ≥ α(F) ≥ H(n). ∎
(The 03:00Z notes used this only for K4-free G, where the maximal cliques are triangles and lone edges, and said the
general case "needs the clique version: a triangle-free spanning subgraph meeting every maximal clique". Step (2) says
the red-plus-lone graph IS that subgraph, for every G: a maximal clique of size ≥ 3 contains a triangle. No minimality
of G is used; T0 holds for every n.)

Consequences (all for any counterexample G, any n), quoting Bikov arXiv:1604.03716 — his "minimal (3,3)-Ramsey graph"
is one that "does not contain a proper (3,3)-Ramsey subgraph" (abstract), i.e. minimal under taking subgraphs:
- G contains a minimal (3,3)-Ramsey graph G_0 (delete edges and isolated vertices while the arrowing survives).
  G_0 has no isolated vertex and NO EDGE OUTSIDE A TRIANGLE (an edge in no triangle can be deleted without creating a
  (3,3)-free colouring: a monochromatic triangle never uses it). Δ(G_0) ≤ Δ(G) ≤ H(n) − 1, ω(G_0) ≤ ω(G).
- Theorem 2.5 [19]: G → (3,3) ⇒ χ(G) ≥ 6. Theorem 2.1 [2][8]: δ(G_0) ≥ 4. Proposition 2.3: G_0 is not Sperner
  (no N(u) ⊆ N(v)). Theorem 2.7: α(G_0(v)) ≤ d_{G_0}(v) − 3 for every v (G_0(v) = the induced neighbourhood in G_0).
- Theorem 8.1: ω(G_0) ≤ 4 ⇒ δ(G_0) ≥ 5, and a degree-5 vertex has G_0(v) ∈ {N5.1, N5.2, N5.3}.
- Theorem 8.2: ω(G_0) = 3 ⇒ δ(G_0) ≥ 8, and a degree-8 vertex has G_0(v) ∈ {N8.1, …, N8.7} (Figure 13 there; we
  re-derived the seven graphs from Definition 3.3 by computer, `marked8.py`, and they are, in graph6,
  G?`F`w, G?bF`w, G?rF`w, G?q`qg, GCQb`o, GCR`r_, GCrb`o — our numbering N8.1–N8.7 is in this order, which is NOT Bikov's: the
  referee read his Figure 13 off the PDF — ours 1,2,3,4,5,6,7 = his 1,4,6,2,3,5,7, so our admissible set N8.4–N8.7 is his
  N8.2, N8.3, N8.5, N8.7 and his "minimal" N8.1–N8.3 are our N8.1, N8.4, N8.5; what is used below depends only on the set).
- Bikov–Nenov Theorem 1.1: a (3,3)-Ramsey graph without 4-cliques on n_0 vertices has α ≤ n_0 − 16; Theorem 1.2:
  n_0 ≥ 21.
At k = 10 the general case is not K4-free: by T1 a K6 is allowed in G at both n (ω ≤ 7, 6), K6 itself is a minimal
(3,3)-Ramsey graph, and the vertices of any K6 ⊆ G have t ≤ 11 − 6 = 5, so they lie in the exceptional clique X of T6(i)
below (whose bound |X| ≤ ω(G) is then 6 or 7, not 3). Nothing below handles that case; T6–T7 assume G is K4-free.

## T6. The K4-free case at k = 10: at most three exceptional vertices, and the core's links.
Assume G is K4-free (so every link G[N(v)] is triangle-free, and for a triangle-free P_v without isolated vertices
β(P_v) = α(P_v), since every edge is a maximal clique).
(i) Exceptional vertices. Let X = {v : t(v) ≤ 5}. Two vertices of X are adjacent (their t's sum to ≤ 10 < 11 ≤ θ_n(2)),
so X is a clique and |X| ≤ ω(G) = 3. Every v ∉ X has t(v) ≥ 6, hence α(P_v) = β(P_v) = d(v) − t(v) ≤ 3; P_v is
triangle-free with α ≤ 3, so |P_v| ≤ 8 because R(3,4) = 9 (a triangle-free graph on 9 vertices has an independent
4-set). So for v ∉ X: d(v) = |P_v| + i(v) with |P_v| ≤ 8.
(ii) The core. By T0, G → (3,3)^e; let G_0 ⊆ G be a minimal (3,3)-Ramsey subgraph. G_0 is K4-free and has a triangle,
so ω(G_0) = 3 and Theorem 8.2 gives δ(G_0) ≥ 8; with Δ(G_0) ≤ 9 every degree of G_0 is 8 or 9, and every degree-8
vertex has G_0(v) ∈ {N8.1, …, N8.7}. Write n_0 = |V(G_0)| ≥ 21 and e_9 = the number of vertices of G_0-degree 9.
(iii) Degree-9 vertices of the core are exceptional. If d_{G_0}(v) = 9 then N_G(v) = N_{G_0}(v) (Δ(G) ≤ 9). No vertex of
G_0[N(v)] is isolated (G_0 has no lone edge), so none is isolated in G[N(v)] ⊇ G_0[N(v)], i.e. P_v = G[N(v)] has 9
vertices; it is triangle-free, so α(P_v) ≥ 4 (R(3,4) = 9), so t(v) = 9 − α(P_v) ≤ 5, i.e. v ∈ X. Hence e_9 ≤ |X| ≤ 3,
and e_9 ≡ 8n_0 + e_9 = Σ d_{G_0} ≡ 0 (mod 2): e_9 ∈ {0, 2}.
(iv) Non-exceptional core vertices. Let v ∈ V(G_0) ∖ X. By (iii) d_{G_0}(v) = 8 and G_0(v) = N8.i for some i. All seven
N8.i have minimum degree 2 (degree sequences below), so the 8 vertices of N_{G_0}(v) are non-isolated in G_0[N(v)] and
hence in G[N_G(v)]; so they all lie in P_v, and |P_v| ≤ 8 by (i) forces P_v = G[N_{G_0}(v)]: a triangle-free graph on
8 vertices with α ≤ 3 — one of the three (3,4;8)-graphs — containing N8.i as a spanning (not necessarily induced)
subgraph; and N_G(v) ∖ N_{G_0}(v) consists of isolated vertices of G[N_G(v)], i.e. of at most 9 − 8 = 1 lone neighbour.
Computation (`marked8.py`, networkx VF2; `contain_bruteforce.py`, all 8! bijections by hand — the two agree):
  N8.1 G?`F`w  10 edges  degrees 2,2,2,2,2,2,4,4  α = 4   spanning subgraph of NO (3,4;8)-graph
  N8.2 G?bF`w  11 edges  degrees 2,2,2,2,3,3,4,4  α = 4   none
  N8.3 G?rF`w  12 edges  degrees 2,2,3,3,3,3,4,4  α = 4   none
  N8.4 G?q`qg  10 edges  degrees 2,2,2,2,3,3,3,3  α = 4   of GCR`r_ and GCrb`o
  N8.5 GCQb`o  10 edges  degrees 2,2,2,2,3,3,3,3  α = 3   IS the 10-edge (3,4;8)-graph (and ⊂ the other two)
  N8.6 GCR`r_  11 edges  degrees 2,2,3,3,3,3,3,3  α = 3   IS the 11-edge (3,4;8)-graph (and ⊂ the Wagner graph)
  N8.7 GCrb`o  12 edges  3-regular                α = 3   IS the Wagner graph (Möbius ladder M8), the 12-edge (3,4;8)-graph
(The three (3,4;8)-graphs are exactly GCQb`o ⊂ GCR`r_ ⊂ GCrb`o; `marked8.py` asserts their number is 3.)
Hence every v ∈ V(G_0) ∖ X has G_0(v) ∈ {N8.4, N8.5, N8.6, N8.7}, its G-link on the same 8 vertices is a (3,4;8)-graph,
d_G(v) ∈ {8, 9}, and d_G(v) = 9 exactly when v has a lone edge in G. A core vertex whose G_0-link is N8.1, N8.2 or N8.3,
like a core vertex of degree 9, lies in X.
(v) Also (Bikov–Nenov 1.1, Bikov 2.5/2.7): α(G_0) ≤ n_0 − 16, χ(G_0) ≥ 6; note α(G_0) is NOT bounded by α(G) ≤ 9
(G_0 is a subgraph, not an induced subgraph, of G), while α(G[V(G_0)]) ≤ 9 is.

## T7. The Seymour count: a minimal (3,3)-Ramsey graph has at least as many triangles as edges; for the core at k = 10 this leaves at most 7 (computed: 5) units of "link deficit", so the core is locally Wagner at every vertex if 8-regular and at all but ≤ 10 (8) otherwise.
Theorem (Seymour 1974, Quart. J. Math. Oxford 25, 303–312; quoted as in NOTES_k10.md): a minimal non-2-colourable
hypergraph — one that has no proper 2-colouring and every proper sub-hypergraph (delete an edge) has one — has at
least as many edges as vertices, the vertices being the union of its edges.
Claim T7. Let G_0 be any minimal (3,3)-Ramsey graph. Then #triangles(G_0) ≥ |E(G_0)|; equivalently
Σ_v (|E(G_0(v))| − (3/2) d_{G_0}(v)) ≥ 0 (each triangle is counted three times by Σ_v |E(G_0(v))|).
Proof. Let T = T(G_0) be the triangle hypergraph (vertices = edges of G_0, hyperedges = triangles). A 2-colouring of
E(G_0) with no monochromatic triangle is exactly a proper 2-colouring of T, so T is not 2-colourable. Let T′ ⊆ T be a
minimal non-2-colourable sub-hypergraph (delete triangles while non-2-colourability survives), V′ = ∪T′ ⊆ E(G_0). If
some edge e of G_0 were outside V′, no triangle of T′ would contain e, so T′ ⊆ T(G_0 − e) and G_0 − e → (3,3)^e,
contradicting the minimality of G_0. So V′ = E(G_0) and Seymour gives #triangles(G_0) ≥ |T′| ≥ |V′| = |E(G_0)|. ∎
(Controls: K6 has 20 triangles, 15 edges; Graham's K3 + C5 has 31 and 23; `core_checks.py` enumerates every minimal
(3,3)-Ramsey graph on ≤ 9 vertices from scratch (Glucose arrowing test on every connected graph with ≥ 15 edges, then
minimality by deleting each edge; CP-SAT re-confirms the hits) and checks the inequality on each; the enumeration must
find exactly K6, K3 + C5 and one 9-vertex graph — Bikov §1. Result: 1/0/1/1 on 6/7/8/9 vertices, the 9-vertex graph
HQjuv~~ with 27 edges and 36 triangles; all pass.)

Corollary (the K4-free counterexample at k = 10). In the setting of T6, write the "excess" x(v) = |E(G_0(v))| − (3/2)
d_{G_0}(v), so Σ_v x(v) ≥ 0 by T7.
- d_{G_0}(v) = 8: G_0(v) = N8.i (Theorem 8.2, for every degree-8 vertex, exceptional or not), so x(v) = |E(N8.i)| − 12
  = −def(i) with def = 2, 1, 0, 2, 2, 1, 0 for i = 1, …, 7. Never positive.
- d_{G_0}(v) = 9: G_0(v) is triangle-free on 9 vertices, so |E(G_0(v))| ≤ ⌊81/4⌋ = 20 (Mantel) and x(v) ≤ 6.5 — the
  first draft's bound. SHARPER (referee, ~15:50Z; our own re-run `paley_check.py` agrees): by Bikov's Prop. 3.4 (s = 1)
  and the restriction remark opening his §8, N_{G_0}(v) is MARKED in G_0(v); a bipartite link is never marked (given any
  edge colouring of the link, colour the v-edges to one side red and to the other blue — no cone triangle is
  monochromatic), so G_0(v) is non-bipartite and triangle-free on 9 vertices, hence |E| ≤ 17 (the non-bipartite
  triangle-free maximum ⌊(n−1)²/4⌋ + 1; checked over all 1,897 triangle-free 9-vertex graphs: 7 of the 9 with 17 edges
  are bipartite, the other 2 are unmarked); and the largest MARKED triangle-free 9-vertex graph has 16 edges, uniquely
  (H?rF`zo). So x(v) ≤ 3.5 (elementary) and ≤ 2.5 (computed).
Hence Σ_{d(v)=8} def(v) ≤ 7 (elementary) / ≤ 5 (computed) if e_9 = 2, and = 0 if e_9 = 0. Therefore:
(a) If the core is 8-regular (e_9 = 0): every link is a 12-edge N8.i — N8.3 or the Wagner graph N8.7 — and by T6(iv)
    every core vertex outside X is LOCALLY WAGNER: G_0[N(v)] ≅ M8, every edge of G_0 at v in exactly 3 triangles. The
    exceptional vertices cannot carry N8.3 either (caught by the blind consistency read, 2026-10-12 ~15:40Z): N8.3 has
    degree sequence 2,2,3,3,3,3,4,4, so a vertex v with G_0(v) = N8.3 has four edges vw lying in 2 or 4 triangles of
    G_0; the number of triangles on vw is deg_{G_0(w)}(v), so w's link has a vertex of degree 2 or 4, so it is not M8,
    so (12 edges) it is N8.3 and w ∈ X by T6(iv). That puts v and four neighbours in X, against |X| ≤ 3. Hence AN
    8-REGULAR CORE IS LOCALLY WAGNER AT EVERY VERTEX (n_0 ≥ 21 of them). Then #triangles = #edges = 4n_0 and Seymour's
    inequality is an equality: T(G_0) is itself a minimal non-2-colourable, 3-regular, linear, 3-uniform hypergraph on
    4n_0 vertices. (The same edge-degree argument in case (b): a degree-8 exceptional vertex with link N8.1–N8.3 has two
    link vertices of degree 4, whose other ends are then exceptional too — so with e_9 = 2 the third exceptional vertex,
    if any, has both its degree-4 link neighbours equal to the two degree-9 vertices.)
(b) If e_9 = 2: the two degree-9 vertices are in X (adjacent to each other), and Σ def ≤ 7 (5) over the degree-8
    vertices: at most 3 (2) of them have a 10-edge link (N8.1, N8.4, N8.5), at most 7 (5) an 11-edge one (N8.2, N8.6),
    and every core vertex outside X with a 12-edge link is locally Wagner — at least n_0 − 10 (n_0 − 8) vertices (two
    of degree 9, at most one more exceptional, at most 7 (5) with deficit).
So a K4-free counterexample at k = 10 is a graph on 40 or 41 vertices with Δ, α ≤ 9 and β = 9 whose (3,3)-Ramsey
core is either 8-regular and locally the Wagner graph everywhere, or has two adjacent degree-9 vertices and is locally
the Wagner graph at all but ≤ 10 (computed: ≤ 8) vertices (those two, ≤ 1 more exceptional vertex, ≤ 7 (5) with core
link N8.4–N8.6 and G-link one of the three (3,4;8)-graphs). A minimal Ramsey graph is connected (a good colouring per
component is a good colouring), so in case (a) the core is a CONNECTED locally-M8 graph on 21..41 vertices.

## Locally-Wagner graphs exist: P(17) (referee's find, re-checked in `paley_check.py`)
The Paley graph P(17) = the (4,4;17) Ramsey graph is 8-regular, K4-free with α = 3, so every link is a 3-regular
(3,4;8)-graph = M8: it is locally Wagner, with 68 edges and 68 triangles (Seymour equality), and it does NOT arrow
(K3,K3)^e — a (3,3)-free colouring found by Glucose and recounted literally (0 monochromatic triangles), as F_e(3,3;4)
≥ 21 demands. It cannot be the core (17 < 21). So case (a) is impossible IF P(17) is
the only connected locally-M8 graph. Evidence: the referee's circulant scan (n ≤ 41, 8-element connection sets,
`referee_k10b_scripts/locM8.py`) finds only P(17), an isomorphic copy, and 2·P(17) on Z_34; Smallwood, "Classification
of graphs that are locally Möbius ladder", MS thesis, UAH 2019 (louis.uah.edu/uah-theses/296), abstract: "there exists a
unique graph which is locally Mobius ladder" — PDF behind a bot wall from every route (exe.dev, Hetzner, residential):
COULD NOT CHECK which ladder or the proof. NEXT RUNG: classify connected locally-M8 graphs ourselves (vertex-by-vertex
extension with canonical augmentation; controls: locally C5 → icosahedron only, locally K3 → K4, locally C4 →
octahedron, locally Petersen → Hall's three; locally C6 must NOT terminate — infinite family); if P(17) alone, the
K4-free core has exactly two degree-9 vertices and ≤ 8 non-Wagner vertices.

## What this does not do, and the next rung
Nothing above says the core does not exist. The honest statement of what remains: does a K4-free graph on ≤ 41
vertices that is either 8-regular and locally M8 everywhere, or 8-regular up to two adjacent degree-9 vertices and
locally M8 except at ≤ 10 (8) vertices (whose links are N8.4–N8.6, or any N8.i / a marked 9-vertex triangle-free
graph with ≤ 16 edges at the ≤ 3 exceptional vertices), arrow (K3,K3)^e? If none does, the K4-free half of
k = 10 is closed. Known K4-free (3,3)-Ramsey graphs have ≥ 786 vertices and large degree; F_e(3,3;4) ≥ 21 is the
lower bound (Bikov–Nenov). The structure is now tight enough for an exhaustive search: 8-regular + every edge in
exactly 3 triangles + K4-free + link independence ≤ 3 characterises "locally Wagner" (the only 3-regular triangle-free
graphs on 8 vertices are M8 and the cube Q3, and α(Q3) = 4), so a SAT/CP model on ≤ 41 vertices with cardinality
constraints (degree 8, |N(u) ∩ N(v)| = 3 on edges), K4-freeness (C(41,4) clauses) and the four-set link clauses, with
symmetry breaking, enumerates the locally-Wagner cores; then the ≤ 16 deficit vertices as a second, lazier model.
Each solution is then tested for arrowing (CP-SAT, seconds) and for the embedding into a 40/41-vertex G with α ≤ 9,
β = 9 (T6). Not launched this tick: the box carries two #552 cadicals, the #3 Lean replay and the #792/#757/#789
solvers (load 19); the model and the estimate go in the queue line. The sub-case worth a first look by hand: can a
locally-Wagner graph (every link ≅ M8) exist on ≤ 41 vertices at all? Locally-M8 graphs are a classical "locally X"
question we have not found treated; the Seymour-equality structure (a 3-regular linear 3-uniform minimal
non-2-colourable hypergraph whose edges are the triangles of a K4-free graph) may already be impossible for a reason a
referee can see.

## Labels
T0: (a) elementary, no priority claimed (we have not seen it stated, but it is a two-line observation on the
F-route). T6: (a) elementary + (d) computer-assisted (the containment table, two implementations) modulo Bikov Thm 8.2
(b) and R(3,4) = 9 (b, Greenwood–Gleason 1955; also re-checked by geng in `core_checks.py`). T7: (b) rigorous modulo
Seymour 1974 — CONFIRMED from Berge, Australas. J. Combin. 9 (1994) 211–219, Theorem 3 p. 216 ("Let H be a
vertex-critical hypergraph with n vertices and m edges. Then m ≥ n", with proof; attributed there to Seymour [14] for
edge-critical hypergraphs); T(G_0) is vertex-critical in Berge's sense (deleting the vertex e gives T(G_0 − e)), so T7
is a one-line corollary of Berge's Theorem 3 and is NOT claimed as new — and (a); its corollary (b) + (d). Everything is
"the shape of a counterexample"; the problem stays open at k = 10.

## Addendum (same seat, ~16:00–16:40Z): the connected locally-M8 graphs on ≤ 41 vertices are exactly two, and case (a) is dead
`locally/locally.py` — "locally X" enumerator by vertex-by-vertex completion (vertex 0 gets the link X; each later vertex
v: its known neighbours K must embed in X respecting every DECIDED pair (edge → X-edge, forced non-edge → X-non-edge;
undecided pairs are free), embeddings quotiented by Aut(X) (lexicographically least tuple per orbit); free slots filled by
existing undecided vertices or new ones (new vertices allocated in slot order, one branch); the link's edges/non-edges
among N(v) forced from X; v closed — every remaining pair a non-edge; dead on an edge into a closed vertex or a forced
non-edge, a non-edge onto an edge, degree > k, or more than NMAX vertices). Controls, all exact: locally K3 → {K4};
C4 → {octahedron}; C5 → {icosahedron}; Petersen, cap 21 → one graph (Kneser K(7,2); Hall 1980: 21, 63, 65); C6, cap 16
→ 11 graphs (surface quotients; the point is that a multi-answer case returns several). The first version FAILED the C4
and C5 controls — it treated an undecided pair as a non-edge in the embedding test — and was fixed before any M8 run.
**Locally M8, NMAX = 41: exactly two connected graphs, 17,950 search nodes, 30 s** (`M8_41.log`, `M8_41.g6`):
  P|fLKfH[QJkSVDMJDrGm]A|g — 17 vertices, 68 edges ≅ Paley(17) (networkx isomorphism), |Aut| = 136, α = 3;
  T|fLKfHWAXkoOLKsEAorDEEWKCwKQWEKk@zB — 21 vertices, 84 edges, 8-regular, every link
  ≅ M8, K4-free, α = 5, 84 triangles, |Aut| = 336, vertex-transitive, girth 3, diameter 2, non-adjacent pairs have 2 (84
  pairs) or 4 (42 pairs) common neighbours (`test_found.log`, `invariants.py`).
**Neither arrows (K3,K3)^e**: Glucose and CP-SAT agree on both; the SAT colourings were recounted literally (0
monochromatic triangles) and the red edge lists are `G21.colouring` / `P17.colouring`.
Consequence (with T7(a) as repaired): an 8-regular K4-free core is a connected locally-M8 graph on 21..41 vertices
⇒ it is the 21-vertex graph ⇒ it arrows — false. **Case (a) is impossible. A K4-free counterexample at k = 10 has a
core with exactly two adjacent degree-9 vertices, Σ def ≤ 5 (≤ 7 elementary), ≤ 8 (10) non-Wagner vertices.** Label (d):
one implementation of the enumeration + five controls + a hostile referee on the code (`locally/referee_locally_opus_…`);
the two outputs verified independently (links/degrees/K4/α/Aut/arrowing ×2).
Case (b) search: `locally/locally_family.py` — same engine, each vertex's link drawn from the family {M8; N8.1–N8.6 with
deficits 2,1,0,2,2,1 (N8.1–3 exceptional); the 79 marked triangle-free 9-vertex graphs without isolated vertex and
≤ 16 edges (`marked9.py` → `marked9.g6`; bipartite links are never marked; 17-edge ones unmarked), exceptional, 'nine'}
under the necessary budgets nine ≤ 2, exceptional ≤ 3, Σ def ≤ 5, vertex 0 locally M8 w.l.o.g. (≥ n − 8 ≥ 13 vertices
are); final filter nine = 2 adjacent, n ≥ 21, Σ def ≤ Σ_{nine}(|E| − 13.5); every CORE-CANDIDATE then gets the arrowing
test. Sanity: with the family restricted to {M8} it reproduces the 17,950-node run exactly. Launched 16:4xZ at nice 19,
NMAX = 41 (`family_41.log`, `family_41.g6`) — the next tick reads it; zero candidates (or candidates that do not arrow)
closes the K4-free half of k = 10 — label (d), and the general (ω ≥ 4) half stays open.

### Referee on the enumeration (Opus, with tools; `locally/referee_locally_opus_2026-10-12.md`, 16:05–16:40Z) — ENUMERATION HOLDS, and stronger
- Code read against (a)–(e): Aut-quotient sound and complete; fill/complete reject only real contradictions; every
  connected locally-X graph reachable in index order. Three deliberate breaks of `locally.py` (a non-automorphism in the
  quotient; never reusing an existing vertex; dropping one orbit representative) each lose a graph on M8 AND on a
  locally-cube control — the controls can see these failures.
- SECOND IMPLEMENTATION: the referee's own search (different vertex order, own automorphism + isomorphism code, nauty
  canonical forms) returns the same two graphs. More controls, both programs agreeing: locally Q3 (cube) → {24-cell,
  complement of K3□K5} (Buset); locally 3×3 rook → {complement of K4□K4, J(6,3)}; locally K3,3 → {K3,3,3}; locally C6 up
  to 20 vertices → 25 graphs (18 tori matched to a lattice construction); locally icosahedron ≤ 40 → the 40-vertex
  600-cell quotient (referee's program; ours did not finish in 200 s). Hall's 63/65-vertex locally-Petersen graphs:
  neither program finished in budget — not reproduced.
- THE CAP NEVER BITES: instrumented, neither program ever has more than 21–23 vertices in play and refuses no branch at
  NMAX 41 or 1000 (our re-run `M8_1000.log`: max vertices in play 21, branches refused 0, same two graphs). So
  **P(17) and G21 are the only connected locally-M8 graphs of ANY order** (computer-assisted, two implementations).
- Third-graph attempts: every group of order 9..41 (all 168, GAP) with every inverse-closed 8-element connection set —
  only Z17 (P(17)), Z7⋊Z3 (G21) and two order-34 groups (2·P(17)) carry a locally-M8 Cayley graph; both graphs'
  triangle complexes are simply connected, so neither has a connected locally-M8 cover.
- G21 identified: vertices = the 21 flags (p, L) of the Fano plane, (p,L) ~ (q,M) iff p ∉ M and q ∉ L; equivalently
  the distance-3 graph of the line graph of the Heawood graph; a Cayley graph of Z7⋊Z3 (not a circulant — why the
  earlier circulant scan missed it); Aut(G21) ≅ PGL(2,7) (GAP). Non-adjacent pairs share 2 neighbours (which form an
  edge) or 4 (a 4-cycle). Arrowing re-verified with the referee's own backtracking colourer (controls K6, K3+C5).
- **Smallwood 2019 (UAH MS thesis, "Classification of graphs that are locally Möbius ladder"; the referee reached the
  PDF through a Wayback snapshot, text in `locally/referee_opus_2026-10-12/source/smallwood2019_text.txt`) is REFUTED
  by G21: its Theorem 4.17 concludes that (Z17, Q) = P(17) is the only locally-M8 graph; G21's distance-2 profile
  (p2, p3, c4) = (8, 0, 4) is exactly the thesis's "Case 1: (8,0,4)", which it claims ends in a contradiction
  ("N(v,w1) = {1,4,v1,v3} induces a P4") — it does not, G21 realises it. MathWorld's "Local Graph" page lists only P(17)
  for the Wagner graph.** We have not re-read the thesis ourselves beyond these lines (quoted by the referee).
- Minor objections applied: `self.maxn` was never updated (fixed; the DONE line now prints max vertices in play and
  refused branches); the lemma should be stated as "exactly two, any order".
