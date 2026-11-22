# Proof that k(6,3) = r(I_6, L_3) <= 32

Written 2026-11-07. On 2026-11-08 a separate AI agent (Claude), which had not written the proof, checked every step, found it correct with no gap, and re-derived its one computed lemma (Lemma B) three ways: an exhaustive search with nauty checked against McKay's Ramsey(4,4) data, SAT with checked proofs, and McKay's 130,816 Ramsey(4,4) graphs on 14 vertices. The proof has not been peer reviewed.

Rerun Lemma B (about 15 seconds): `cc -O2 -o verify_small verify_small.c`, then `./verify_small count 8 3` (prints 5040), `./verify_small count 9 3` (0), `./verify_small glue8` (0) and `./verify_small glue8r` (0). Check the lower-bound witness: `python3 check_witness.py witness_n29_m6_anneal.txt`.

Reference: F. Ihringer, D. Rajendraprasad, T. Weinert, New bounds on the Ramsey number r(I_m, L_n), Discrete Math. 344 (2021) 112268 (IRW).

Notation: N+(v), N-(v), I(v) are the out-, in- and non-neighbours of v; d(v) = |N+(v)| + |N-(v)|; e(X) counts edges inside X, e(X,Y) edges between disjoint X and Y.

Facts used:
- (F1) In an L_3-free oriented graph, N+(v) and N-(v) are independent (IRW Cor. 2.2).
- (F2) If D is {I_m, L_3}-free, then D[I(v)] is {I_(m-1), L_3}-free (IRW Lemma 2.1).
- (F3) r(I_2,L_3) = 4, r(I_3,L_3) = 9, r(I_4,L_3) = 15, r(I_5,L_3) = 23 (Erdős-Rado; Bermond; IRW). Re-checked here: exhaustive counts give 0 graphs on 4 and on 9 vertices, and SAT gives UNSAT on 15 and 23.
- (F4) IRW Lemma 3.3: if D is {I_m, L_3}-free and |N-(v)| = m-1, then e(N-(v), I(v)) >= 2(|I(v)| - m + 1); the same holds for N+.
- (F5) **Lemma B (computed).** Every {I_4, L_3}-free oriented graph on 14 vertices has all degrees equal to 6, so 42 edges. Degrees are 5 or 6 by (F1) to (F3). Suppose u has degree 5. Then (out, in) is (3,2) or (2,3), and I(u) is an {I_3, L_3}-free graph on 8 vertices. That graph is Bermond's: there are exactly 5040 = 8!/|Aut| labelled ones, with |Aut| = 8 (nauty, and brute force over all 8! permutations). An exhaustive backtracking search tries all 50 remaining pairs in all 3 states, with no SAT and no symmetry breaking. It finds **no completion** in either case (`verify_small.c`, modes glue8 and glue8r, under 15 s together). The same result comes from SAT (kissat and cadical, no symmetry breaking) and from the SAT enumeration, which finds IRW's graph as the only 14-vertex graph.

**Lemma A.** Every {I_5, L_3}-free oriented graph H on 21 vertices has at least 74 edges.
Proof. By (F2) and (F3), every vertex has at most 14 non-neighbours, so degree >= 6; out- and in-degrees are <= 4 (F1). If every degree is >= 7, then e(H) >= 147/2, so e(H) >= 74. Otherwise take u with degree 6. J = I_H(u) has 14 vertices and is {I_4, L_3}-free, so e(J) = 42 (F5). Let P = N+(u), Q = N-(u) and t = e(P,Q). Then e(H) = 6 + t + e(P u Q, J) + e(J), and the degree sum over P u Q (each degree >= 6) gives 6 + 2t + e(P u Q, J) >= 36.
- Case (3,3). Two non-adjacent vertices of J with no neighbour in P would form, with P, 5 independent vertices. So such vertices form a tournament with no L_3, and there are at most 3 of them; hence e(P,J) >= 11, and likewise e(Q,J) >= 11. So e(P u Q, J) >= max(22, 30 - 2t). Since t + max(22, 30 - 2t) >= 26 for every t >= 0, e(H) >= 6 + 26 + 42 = 74.
- Case (4,2); (2,4) follows by reversing every arc. By (F4) with m = 5, e(P,J) >= 2(14 - 4) = 20. The vertices of J with no neighbour in Q contain no 3 independent vertices (with Q they would make 5), so there are at most 8 of them (F3), and e(Q,J) >= 6. So e(P u Q, J) >= max(26, 30 - 2t) and e(H) >= 6 + 28 + 42 = 76.

A SAT cross-check is stronger: gluing on IRW's 14-vertex graph shows that no 21-vertex {I_5, L_3}-free graph has a vertex of degree 6 at all (kissat and cadical, no symmetry breaking, `lemmaA_nodeg6.log`).

**Theorem.** No oriented graph on 32 vertices is free of both L_3 and I_6.
Proof. By (F1) to (F3), every vertex has out- and in-degree <= 5 and at most 22 non-neighbours, so d(v) is 9 or 10.
- Case A: some v has (out, in) = (5,5). Then C = I(v) has 21 vertices and D[C] is {I_5, L_3}-free, so e(C) >= 74 by Lemma A. By (F4) with m = 6, e(N+(v), C) >= 32 and e(N-(v), C) >= 32. Each c in C has d(c) <= 10 and no edge to v, so 210 >= sum of d(c) over C = e(N(v), C) + 2e(C) >= 64 + 148 = 212, a contradiction.
- Case B: no vertex has degree 10, so every vertex has degree 9. The out-degree sum equals the in-degree sum, so some v has (5,4). Then C = I(v) has 22 vertices and D[C] is {I_5, L_3}-free, so each c has degree >= 7 inside C and e(C) >= 77. By (F4), e(N+(v), C) >= 34. The vertices of C with no neighbour in N-(v) are pairwise adjacent (otherwise 6 independent vertices), so there are at most 3, and e(N-(v), C) >= 19. So 198 = sum of d(c) over C >= 34 + 19 + 154 = 207, a contradiction.

So r(I_6, L_3) <= 32, that is, k(6,3) <= 32.

Lower bound: simulated annealing found a 29-vertex oriented graph (140 arcs, out- and in-degrees 4 or 5, trivial automorphism group) with no transitive triangle and no independent 6-set. The independent checker passes it: 0 transitive triples, 0 independent sets among all 475,020 6-subsets (`witness_n29_m6_anneal.txt`, check output `witness_n29_m6_anneal.check.txt`; check_witness.py repeats both checks; SHA-256 5c1cc09c...cb3fa). So k(6,3) >= 30. The best structured witness is the circulant Cay(Z_28, {1,4,12,15,22}) (circulants exist for 23 to 28 vertices, none for 29 to 32; it also passes the checker), giving 29. Our circulant search found it independently on 7 November 2026. It is Daniel Kirtchakov's Cay(Z_28, {3,8,10,12,17}) relabelled by x -> 5x (mod 28); he published k(6,3) >= 29 with it on Zenodo on 11 August 2026 (https://doi.org/10.5281/zenodo.21890619), so the bounds before this record were 29 <= k(6,3) <= 33. **30 <= k(6,3) <= 32.** In the journal literature, the best lower bound stated is k(6,3) >= R(3,6) = 18 (IRW, p. 3); k(6,3) >= 26 follows at once from IRW's 22-vertex graph for k(5,3) = 23 together with a disjoint directed triangle (the largest independent set then has 4 + 1 = 5 vertices, and no transitive triangle can use both parts).

Side facts (SAT enumeration, uncertified): IRW's 14-vertex graph and IRW's Z_22 graph are the only {I_4,L_3}-free and {I_5,L_3}-free oriented graphs on 14 and 22 vertices. A 31-vertex witness would have every degree 9 or 10 and a (5,5) vertex: degree 8 is excluded by gluing on the unique 22-vertex graph (UNSAT), and all-9 is excluded by parity.

