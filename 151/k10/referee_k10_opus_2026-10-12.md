# Hostile referee — NOTES_k10.md (Erdős #151 at k = 10), Opus 5.5, 2026-10-12 ~03:45Z

**VERDICT: HOLDS AS READ for T1–T5. I found no gap in any proof step, and every lemma passes an exhaustive check on all
13,598 graphs with ≤ 8 vertices, with mutations that do fail. The errors are elsewhere: the K4-free / literature
paragraph makes one false literature claim and misses the strongest relevant theorem, which sits in a paper the
notes themselves cite. The summary overstates T3 and T4. The circulant-search sentence misreports a run that
crashed after about 4% of its jobs.**

Version reviewed: NOTES_k10.md mtime 03:34:40Z, md5 3724b9cd…. It was edited during the review: T4 now says "Let I be
any independent set … (Maximality of I is not used …)". That edit fixed what would otherwise have been objection 0:
the refinement applied T4 to I ∖ J, which is not a maximum independent set.

## Objections (most important first)

**1. False literature claim; the strongest relevant known result is missed.**
> "Nothing published bounds the maximum degree of a K4-free (3,3)-Ramsey graph from below"

This is false, and the counterexamples are in the very paper the notes cite (Bikov, arXiv:1604.03716):
- §6.1: every (3,3)-Ramsey graph has χ ≥ 6, so Δ ≥ 5. By Brooks' theorem, Δ ≥ 6 unless the graph is K6.
- **Theorem 8.2: "Let G be a minimal (3,3)-Ramsey graph and ω(G) = 3. Then δ(G) ≥ 8. If d(v) = 8, then G(v) = N8.i for
  some i ∈ {1,…,7}."** It follows that every K4-free (3,3)-Ramsey graph has Δ ≥ 8, because it contains a minimal one.

I checked Theorem 8.2 independently (command below). No triangle-free graph on ≤ 7 vertices has V(N) as a marked
vertex set, and exactly 7 triangle-free graphs on 8 vertices do.

Consequences for the notes:
- (a) > "which for a triangle-free link forces δ ≥ 5 and a C5 link at degree 5"

  The deduction from Thm 2.7 is correct, but the case it describes cannot occur: Thm 8.2 rules out degree 5 entirely.
- (b) The missing lemma already holds for Δ ≤ 7. The only open range is Δ ∈ {8, 9}. Equivalently, in a K4-free
  counterexample the minimal (3,3)-Ramsey core G0 ⊆ G has every degree in {8, 9}, and each G0-degree-8 link is one of
  N8.1–N8.7.
- (c) Consistency check: at n = 41, the three admissible degree-8 links with i = 0 in `link_census.log` are GCQb\`o,
  GCR\`r\_ and GCrb\`o. All three are among the 7 marked graphs. So the census and Bikov 8.2 are compatible: no
  contradiction, but a sharp local constraint that the notes should state.

**2. Ill-posed claim.**
> "A "no" would be a K4-free Folkman graph of bounded degree — not known to exist at any degree bound"

Every finite graph has bounded degree. The 786-vertex graph of Lange–Radziszowski–Xu is a K4-free Folkman graph with
some finite Δ, so as written the sentence is false. The intended statement is: "none is known with Δ ≤ 9, and Δ ≥ 8 is
forced (Bikov Thm 8.2)."

**3. "Exactly" and "equivalently" overclaim.**
> "**The missing lemma, exactly:** does every K4-free graph with maximum degree ≤ 9 (equivalently, in the minimal
> counterexample, every edge in ≤ 5 triangles and every link triangle-free with α ≤ 5) have …"

- The lemma is sufficient but not exact. It quantifies over all orders and ignores α ≤ 9 and β ≤ 9. A "no" on a large
  graph says nothing about #151, because Caro–Wei gives α ≥ n/10 there.
- The parenthetical is not equivalent to Δ ≤ 9. The local conditions do not bound the degree: the number of lone
  edges is unbounded, and a triangle-free link with α ≤ 5 can have up to 17 vertices.
- The numbers 5 and 5 are the n = 40 values. At n = 41 both are 4.

**4. Formula typo.**
> "every edge in ≤ B = 10 − g ∈ {5, 4} triangles"

The claim's B is k − 1 − g = 9 − g. The formula 10 − g gives {6, 5}. The values {5, 4} as stated are right.

**5. Missing qualifier.**
> "a triangle shares an edge with at most one of the triangles through any given edge"

This is false when the triangle itself contains that edge: it then shares e with every other triangle through e. It is
true for triangles not containing e. Computed over all K4-free graphs on ≤ 7 vertices: 497 violations, all with
e ∈ T, and 0 with e ∉ T. (Linearity of the triangle hypergraph holds for every graph, not only K4-free ones; that is
harmless.)

**6. Seymour count taken over the wrong set; the conclusion still holds.**
> "gives Property B at once when every edge is in ≤ 2 triangles (3|T| ≤ 2|E|)"

Seymour's bound (|E| ≥ |V| for a minimal non-2-colourable hypergraph, with vertices = union of its edges) must be
applied to the minimal sub-hypergraph T′. Its vertex set V′ is the set of edges of G lying in some triangle of T′. The
needed count is 3|T′| ≤ 2|V′|, which forces |T′| < |V′| and contradicts Seymour. The global count 3|T| ≤ 2|E(G)| proves
nothing by itself. The correct count holds because the degree bound is inherited by sub-hypergraphs, so the conclusion
stands; I verified it computationally (below). The statement of Seymour's theorem is quoted from memory (Quart. J.
Math. 1974) and is not among the PDFs.

**7. The summary overstates T3.**
> "every maximum-degree vertex at distance ≤ 2 from everything"

T3 gives U_w = ∅ only when d(w) = 9, and Δ(G) = 9 is never established. For d(w) = 8, U_w is only a clique. This should
read "every degree-9 vertex (if any)", which is what T3 itself says.

**8. The summary overstates T4.**
> "— unless α ≤ 5 — a large triangle-free spanning subgraph L of lone edges with every maximum independent set
> L-dominating (T4)"

Domination is proved only at α = 9, where F_I = ∅. For α = 6, 7, 8 the notes prove only Σ i(v) ≥ 4, 13, 22 (n = 40),
with |F_I| ≤ 30, 20, 10. At α = 6, L may have just 4 edges.

**9. The direction word is inverted.**
> "T1. Every link is cheap to hit: t(v) ≥ g"

The same phrase reappears in the summary as "every link cheap to hit". But t(v) ≥ g says the smallest transversal is
large: the links are expensive to hit, because β(P_v) is small. The wording contradicts the inequality it labels.

**10. The notes misreport their own computation.**
> "the circulant search (`vt_search.py`) finds … none with β ≤ 9 (β ≥ 16 on every candidate seen)"

- `vt_search.log` contains β = 14 (S = [1,2,6,11,20,29,34,38,39], ω = 3) and β = 15 (three candidates).
- The run did not finish. It died with `AssertionError: beta not solved to optimality` (120 s single-worker CP-SAT cap
  on a loaded box) at job index 513 of 12,597, about 4%, all on Z_40.
- The crashing instance is S = [1,4,5,6,34,35,36,39]. I solved it in 0 s with 4 workers: β = 28.
- "None with β ≤ 9" therefore covers ≈ 4% of the planned family.
- Relevant literature in `/tmp/erdos151-lit/2605.16542` (Hassan–Radziszowski–Van Overberghe 2026, §4.6.2): "no J5-free
  vertex-transitive graph on 36, 39, 40, 42 or 44 vertices arrows (3,3)e". So K4-free vertex-transitive counterexamples
  on 40 vertices are already excluded.

**11. The controls section overstates what was tested.**
> "`lemma_checks.py`: T2 (|I| ≤ 3), T3 and T4 on 400 random graphs …"

I read the script:
- T3 is tested only for |A| = 1, as the equivalence "N(w) ∪ {u} free ⟺ u ∈ U_w".
- T4 is tested only for |A| = 1, with I maximum and α = β.
- The hypotheses the proofs actually turn on (independence of I in T2, independence of A in T3 and T4) are never
  mutated.
- The T1 clique bound, the T4 Caro–Wei count, the W_J refinement and T5 have no control at all.

The mutations it does run are real, and its output reproduces exactly: tested 400 / 1683 / 679, mutations fail
99 / 428 / 568. My exhaustive run below fills the gaps.

**12. Minor points.**
- > "Since t(v) ≤ d(v) ≤ 9: two non-adjacent vertices have t(v) + t(w) ≥ 11 (12)"

  The conclusion is θ_n(2); it does not follow from t ≤ 9. This is a harmless non sequitur.
- The T4 refinement numbers are for n = 40 only. At n = 41 there are 32 vertices outside I, at least 23 of them have
  ≥ 2 lone I-neighbours, and Σ i(v) ≥ 55.
- "Bikov … Thms 2.1": Theorem 2.1 is Burr–Erdős–Lovász / Fox–Lin, quoted by Bikov.
- `NOTES.md` still says "20 ≤ F_e(3,3;4)". The current bound is 21 (Bikov–Nenov 2020; the 2026 paper says "best known
  bounds are 21 ≤ Fe(3,3;4) ≤ 786").

## Checked and holds (the questions asked)

- **Setting:** β = 9. H(39 or 40) = 9 in each case of R(3,10).
- **T1:** the bound β(P_v) ≥ |K| − 2 is right, and it is tight on K_m.
  - When |K − v| = 2, the "|K| − 2 vertices" set is a single vertex, which is free by (F4).
- **T2:**
  - The case C ∩ I = {v}, |C − v| = 1 is handled explicitly: the vertex is isolated in G[N(v)], and the transversal
    definition counts isolated vertices.
  - When G″ is empty: β = 0 ≥ H(0) = 0 (using the claim's convention R(3,0) = 0), and no minimality is needed.
  - The θ table, recomputed from R(3,·) = 1,3,6,9,14,18,23,28,36:
    - n = 40: 4, 11, 15, 19, 22, 26, 28, 30, 31
    - n = 41: 5, 12, 16, 20, 23, 27, 29, 31, 32

    Both rows match the notes.
- **T3:** "C − u is a maximal clique of G[N(u)]" is right. The single-isolated-vertex case is covered by the clause
  "isolated vertices counting".
- **T4:**
  - The Caro–Wei bound |F_I| ≤ 10(9 − m) and the values n + 9m − 90 = 4, 13, 22, 31 are right.
  - The W_J step is right: W_{v} lies inside N_L(v), which is independent, so |W_{v}| ≤ 1.
  - The minimum of Σ i(v) is min over x ≤ 9 of (x + 2(31 − x)) = 53. Some v has i(v) ≥ 6, so |P_v| ≤ 3.
- **T5:**
  - The two halves are independent and also disjoint: a common lone neighbour x would make vax a triangle through the
    lone edge va. So G[S] is bipartite and triangle-free, and no maximal clique of size ≥ 3 lies in S.
  - An edge inside S that is not lone lies in a triangle, so it is not a maximal clique.
  - Cliques that meet S but leave it are not subsets of S, so they are irrelevant.
  - The lone edges between the halves are exactly what must be covered. The 4-cycle conclusion is right.
- **K4-free paragraph:**
  - (i) The direction is right. Recolouring lone edges red is harmless because they lie in no triangle. Isolated vertices
    are harmless because the red graph spans all n vertices.
  - (ii) Each inequality is true. Δ(P) ≤ β(P) is (F3) applied to P, which holds for every graph; I checked it on all
    graphs with ≤ 8 vertices.
  - (iii) and (iv): see objections 5 and 6.
- **Literature:**
  - Bikov–Nenov 1904.01937, Thm 1.1 (α ≤ n − 16) and Thm 1.2 (F_e(3,3;4) ≥ 21). The Australas. J. Combin. 77:35–50
    (2020) reference is confirmed by the 2026 paper's bibliography.
  - Lange–Radziszowski–Xu 2014 (JCMCC 88): F_e(3,3;4) ≤ 786.
  - Bikov's "minimal" means no proper (3,3)-Ramsey subgraph (Def 1.1). The proof of Thm 2.7 uses only G − v ↛, so the
    result also holds for vertex-critical graphs. For the notes' use the notion does not matter: any Ramsey graph
    contains a minimal one, and Δ and K4-freeness pass to subgraphs.
  - Angeltveit 2401.00392: R(3,10) ≤ 41, and Exoo 1989 SIAM J. DM 2(4) for ≥ 40. The "43 117 868" (3,10;39)-graphs
    figure is confirmed. The journal reference "EJC 32(4) P4.30" cannot be verified from the arXiv file.
  - R(3,9) = 36 is used as such by Angeltveit.
  - "Erdős and Gallai made no progress … even when G is K4-free [Er88]" is confirmed via the Formal Conjectures
    151.lean docstring (erdosproblems.com is behind a Cloudflare block from this box).
  - I did not verify "the known ones have degree ~ n/3".
- **Novelty:**
  - T1 is correctly credited to the claim. T2–T5 are elementary and not claimed as new. The Folkman framing comes from
    our own NOTES.md.
  - One honest point to make explicit if this goes public: the Seymour remark shows the claim's self-described "new
    part" (Case C) is a special case of Seymour 1974. That bears on the claim's novelty statement, not on its
    correctness.
  - The missing-lemma statement needs objections 1–3 fixed before it is a fair statement of the literature.

## Computation (all scripts in /tmp/ref151/, outside the repo; nothing in erdos151/ edited)

```
$ nice -n 19 python3 /tmp/ref151/exhaust.py 8       # all graphs n<=8 via nauty-geng; each lemma in FULL generality:
  # T1 clique bound; T2 for EVERY independent I x EVERY combination of minimal transversals; T3 for every w and EVERY
  # independent A ⊆ U_w; T4 for every independent I and EVERY independent A with no lone edge to I; T5 for every lone
  # edge and EVERY vertex cover; Δ(G) <= β(G); t(v) = d(v) − β(P_v) vs brute-force min transversal
ALL EXHAUSTIVE CHECKS PASS {'graphs': 13598, 'T1': 183773, 'T2': 1173542, 'T3': 437274, 'T4': 5062110, 'T5': 299392, 'DeltaBeta': 13598}
$ for m in T1 T2 T3 T4 T5; do python3 /tmp/ref151/exhaust.py 6 $m; done   # mutations: T1 with |K|−1; T2 with ANY
  # (non-independent) I; T3/T4 with non-independent A; T5 without removing a cover
MUTATION T1 fails: {'T1': 385}   MUTATION T2 fails: {'T2': 50296}   MUTATION T3 fails: {'T3': 1293}
MUTATION T4 fails: {'T4': 15438} MUTATION T5 fails: {'T5': 736}
$ python3 /tmp/ref151/handpicked.py   # β brute force; T1 + T2 (all independent I, all minimal transversals)
Petersen: n=10 beta=4 alpha=4 omega=2 Delta=3 lone=15 t={3} T2-instances=75 OK
octahedron: n=6 beta=4 alpha=2 omega=3 Delta=4 lone=0 t={2} T2-instances=24 OK
K4+3 pendant triangles: n=7 beta=5 alpha=3 omega=4 Delta=5 t={1,2} T2-instances=62 OK
5-wheel: n=6 beta=5 alpha=2 omega=3 Delta=5 t={1,3} T2-instances=15 OK
K6+pendant triangle: n=8 beta=7 omega=6 T2-instances=139 OK ;  K_m: beta(link)=m-2 exactly, m=3..8
$ python3 /tmp/ref151/misc.py
theta 40: [4, 11, 15, 19, 22, 26, 28, 30, 31]   theta 41: [5, 12, 16, 20, 23, 27, 29, 31, 32]
T4 refinement min sum i(v): n=40 -> 53, n=41 -> 55
Property B holds on all 5540 graphs (n<=8) and 300 random graphs (n<=22) with every edge in <=2 triangles;
  K6 and K3+C5 controls correctly non-colourable (CP-SAT)
K4-free n<=7: T shares an edge with >1 OTHER triangle through e: 497 times, of which with e not in T: 0
Bikov Thm 8.2 check (V(N) marked in triangle-free N; controls: K4 marked, K3 not):
  p=1..7: 0 marked (1,2,3,7,14,38,107 graphs);  p=8: 7 of 410 marked:
  G?`F`w G?bF`w G?rF`w G?q`qg GCQb`o GCR`r_ GCrb`o
$ python3 /tmp/ref151/crasher.py      # the job that killed vt_search.py
crasher candidate index 513 of 12597 n 40 S [1, 4, 5, 6, 34, 35, 36, 39]; omega 4; beta OPTIMAL 28 (0s, 4 workers)
$ nice -n 19 python3 /home/exedev/MathDyad/erdos151/lemma_checks.py
tested: {'lemma2p': 400, 'blocking': 1683, 'lone': 679}; mutations failed {'lemma2p': 99, 'blocking': 428, 'lone': 568}; ALL CONTROLS PASS
```
