# Hostile referee report — #704 Question 5.1 claims (CLAIMS.md), 14 Nov 2026

(The referee instance could not write files outside its scratch; this is its returned report, saved verbatim by the driving
seat. Its own code is in this directory: autW.py, z13ref.c, z13ref_dump.c, cover_search.c, colcheck.py, alpha10.c, johnson_ref.py,
rank_ref.py, certref.py, lp_tables.py, lpfind.c, lp_lift_check.py.)

## Summary

1. **B2 (symmetry theorem, parts i–v): holds.** My own code reproduces everything from W alone: Aut(W) has order 48 (backtracking over all point maps), the involution table (19 involutions; phi depends only on cycle type: 25, 17, 9, 7, 3; none of type 2^6), N_k = 627, 303, 147, 71, 35, 15, and all 8 order-3 elements have type 3^4 1. My own 13-cycle run gives 9,979,200 distinct copies, a histogram identical to yours including 136,540 at 33 orbits, and 0 three-covers; a planted cover is found. The added part (v) is correct: all 48 automorphisms fix INF and preserve the a-triple and b-triple. The group-theory ending is complete, though the reason should be spelled out.
2. **A2 and B5: hold. A1 reproduced.** My own checker passes both 21-colourings (each invariant under its stated cycle) and the 49-colouring, and rejects two mutated files. My own search gives alpha(J(10,5,3)) = 12 with 285,600 maximum sets, so the lower bound 21 does not rest only on Kupavskii–Raigorodskii.
3. **B3: holds with fixes.** All numbers reproduce:
   - v^T E_i v = 11/13, 32/715, 389/77, 472/35, 347/35, 128/35 (sum 33), by a different route (exact Lagrange idempotents of A_1); the only primes above 13 are 59, 347, 389.
   - On 1,400 of my own random copies (PARI): rank 1287 mod 2, 5, 7, 13, 17, 19, 23, 59, 347, 389; rank 1286 mod 3 and mod 11.
   - All 1,600 certificate rows are genuine copies, and the X9 and Y121 certificates check in exact integers (with controls).

   Two proof steps are unstated, and one sentence overclaims.
4. **B4: holds with fixes.** I count 69,046,650 copies disjoint from W. I lifted your 101-column rational solution to an explicit weighting of 4,548 copies and checked it exactly: every 5-set outside W covered exactly 1, 4-set cut max = 4, 6-set cut max = 3, point minimum ≈ 2.34. All three cut families are valid.
5. **Overall: publishable after wording fixes. I found no mathematical error.**

## Must-fix items

1. **Say that B2 and B4 are conditional.** Every part of B2, all of B4, and the "no counting obstruction" reading of B3 use the uniqueness theorem (every independent 33-set is a copy of W). Yesterday's page says that theorem is "likewise uncertified in the paper's sense". CLAIMS calls it a "standing fact" with no label; the page needs the same "uncertified" label. Also state B2 as "If a 39-colouring P exists, then …".
2. **Cite a real source for "= 48".** "Aut(W) … order 48 … (`prep_lp.py` builds the 48 and checks them.)" Those scripts only build 48 role-preserving maps and check they fix W, which shows at least 48. No q51 script rules out other automorphisms, and every B2 table depends on it. It is true: my backtracking finds exactly 48, and yesterday's nauty result says the same. Cite one of those.
3. **B3, primes above 13:** add one sentence on why E_i can be reduced mod p. In the eigenvalue form its apparent denominators contain 17, 23 and 47, and 23 and 47 are not in your direct-rank list. The reason it works: E_i comes from a central idempotent of Q[S_13] whose denominators divide 13!. Also cite that for p not dividing |S_13| the six constituents stay irreducible and pairwise non-isomorphic mod p.
4. **B3, p = 3 and 11:** add two steps. The rank mod p is also at most 1286, because L lies inside the 33-congruence lattice. The class of e_S generates the cyclic p-part (it maps to 1 in Z/33), so the certificate for p·e_S gives p·Q_p = 0.
5. **B3 wording overclaims.** "no argument that only uses linear relations/congruences on incidence counts can exclude a 39-colouring": LP and cut arguments (B4) are also linear relations on incidence counts, and B3 says nothing about them. Restrict it to integer-linear congruence arguments.
6. **B4:** say the LP is aggregated over Aut(W)-orbits, and that its solution lifts by averaging a representative copy over the 48 automorphisms. "Exact rational solution on 101 columns" alone does not support the stated weighting of copies.

**Should-fix:** in B2, replace "every element has 3-power order" with "no element of prime order other than 3, so |Aut(P)| = 3^m by Cauchy's theorem". In B4, state the "exactly 9 / 6 / 2, otherwise at most 1 superset per class" facts in the 4-set cut explanation. I did not check the A3 literature claims.

## Driver's disposition (same day)

All six must-fix items and both should-fix items were applied to CLAIMS.md and to the page; primes 23 and 47 were also given a
direct rank check (logs/rank_extra.out).
