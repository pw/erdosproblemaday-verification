# Erdős #151 — notes, 2026-10-11 (Claude, reasoning seat)

Question: for every graph G on n vertices, is τ(G) ≤ n − H(n)?  τ = clique-transversal number (hit every maximal
clique of size ≥ 2); H(n) = max{k : R(3,k) ≤ n} = min independence number over triangle-free n-vertex graphs.
Equivalent: G has a set S, |S| = H(n), containing no maximal clique. Writing R = Ḡ: maximal cliques of G are the
maximal independent sets (= independent dominating sets) of R, so S must contain no independent dominating set of R.

**Reduction 1 (the closed-neighbourhood trick).** For any vertex w, S = V ∖ N_R[w] contains no independent
dominating set of R (nothing in S dominates w). So τ(G) ≤ deg_R(w) + 1 for every w, i.e. τ(G) ≤ n − Δ(G)... more
precisely τ(G) ≤ δ(R) + 1 = n − Δ(G). Hence the conjecture holds whenever Δ(G) ≥ H(n). [Elementary; probably in
Erdős–Gallai–Tuza 1992 already.]

**Reduction 2.** Otherwise Δ(G) ≤ H(n) − 1. If α(G) ≥ H(n) an independent set works. So a counterexample needs
Δ(G) ≤ H(n) − 1 AND α(G) ≤ H(n) − 1. Caro–Wei gives α(G) ≥ n/(Δ+1) ≥ n/H(n), so n < H(n)²; and n ≥ R(3,H(n)) by
definition. Since R(3,k) < k² for k ≥ 5 (R(3,5)=14), this window is nonempty for most n: a counterexample is a
graph with maximum degree < H(n) and independence number < H(n), with R(3,H) ≤ n < H², and it is not a disjoint
union of cliques (those satisfy the conjecture: S = each clique minus one vertex).

**Small cases (brute force, `small151.py`):** no counterexample on n ≤ 9 (at n = 9, H = 4; 103,164 graphs with
α < 4 checked, each has a 4-set containing no maximal clique).

**What a counterexample would look like:** near-regular of degree H−1 with every independent set small — i.e. a
sparse graph that is "locally clique-like" everywhere, where every H-set traps a maximal clique. Candidates to test
next: line graphs / Kneser-type / strongly regular graphs with λ large, at n just above R(3,H). Not pursued tonight.

---
# 2026-10-12 — straight-reasoning run (Claude, Fable 5.1, interactive; ~1 h time-box)

**What the thinking produced before any literature lookup.** (1) Let β(G) = n − τ(G) be the largest set containing no
maximal clique (≥2). If G has a triangle-free *spanning* subgraph F ⊆ G such that every maximal clique of G contains an
edge of F, then every independent set of F is β-free in G, so β(G) ≥ α(F) ≥ H(n) and the conjecture holds for G *exactly*
(not just up to constants). F may be taken inside G. (2) Where this route must fail: for K4-free G the maximal cliques
are the triangles and the edges lying in no triangle; the latter are forced into F, so F exists iff the edges of G can be
2-coloured (red = F) with red triangle-free and every triangle containing a red edge — i.e. with NO monochromatic
triangle. That is exactly the statement that the 3-uniform "triangle hypergraph" T(G) on E(G) has Property B, and its
failure is exactly G being an edge-Folkman graph G → (K₃,K₃)^e. Such K4-free graphs exist (Folkman 1970; 20 ≤ F_e(3,3;4) [correction 2026-10-12 03:00Z seat: the lower bound has been 21 since Bikov–Nenov, AJC 77 (2020)]
≤ 786, Bikov–Nenov / Lange–Radziszowski–Xu), so the F-route cannot prove the conjecture in general; any K4-free exact
counterexample is a Folkman graph with Δ(G) ≤ H(n) − 1 and α(G) ≤ H(n) − 1 (Reductions 1–2 above) — a *sparse* Folkman
graph, which no known construction is (the known ones have degree ~ n/3 and so β ≥ Δ ≫ H(n)). (3) Random graphs cannot
be counterexamples: at any density α·Δ ≳ n log(np) while a counterexample needs α·Δ < H(n)² ~ n log n with both factors
below H(n) — the window n ∈ [R(3,H), H(H−1)] needs α and Δ both ≈ √n·(1..√log n), i.e. Caro–Wei nearly tight, which
pushes toward clique-like structure that has huge β. (4) n = 10..13 exhaustively under the lossless restriction
Δ ≤ H(n) − 1 (`small151_deg.py`, nauty-geng -D): 3547 / 10946 / 36327 / 124380 graphs, 6 / 1 / 1 / 0 with α < H(n), no
counterexample. With the n ≤ 9 run: the conjecture holds for all n ≤ 13.

**Then the literature.** (a) erdosproblems.com/610 already records τ(G) ≤ n − c√(n log n) via Joret–Micek–Reed–Smid
(EJC 28(3) P3.51, 2021: clique chromatic number O(√(n/log n)); the largest colour class of a clique colouring is a free
set) — so #151 is settled up to the constant and only the exact Ramsey-sharp form is open. (b) A proof claim sits on
the #151 page (Daniel Veljjanoski, 2026-09-28, "using Claude", repo veljjanoski/erdos151 `PROOF.md`): τ(G) ≤ n − H(n)
for every n ≤ 39, by a minimum-counterexample reduction (credited to the-omega-institute/trureturing#9934, 25 Sep 2026:
a minimum counterexample has n = R(3,k) and every link P_v has β(P_v) ≤ B := k − 1 − (R(3,k) − R(3,k−1))) plus a new
elementary Case C for B = 2: then every edge lies in ≤ 2 triangles, and alternately colouring an Euler circuit of the
triangle–edge incidence multigraph gives exactly a triangle-free spanning subgraph meeting every clique — item (1)
above, in the special case where the triangle hypergraph has max degree 2 (which their Euler trick shows always has
Property B). The claim covers k ≤ 9 since R(3,10) ≥ 40. So the reasoning run converged on a two-week-old public claim's
key lemma; what is ours is the Property-B / Folkman framing of exactly where that method stops (k = 10: B ∈ {4,5}, links
may hold K4's and edges in up to 5 triangles — the triangle hypergraph no longer has bounded degree), the random-graph
exclusion, and the n ≤ 13 check. (c) My line-by-line read of PROOF.md: holds as read (Lemma 2's size count, Corollary
2's direction, the Euler-circuit both-colours argument incl. the wrap-around at z, Case C's edge-in-≤2-triangles
consequences, the Ramsey table). A blind Opus referee seat was run separately — see the /day entry.
