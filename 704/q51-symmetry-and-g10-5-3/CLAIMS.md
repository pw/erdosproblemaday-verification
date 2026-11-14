# #704 follow-up (Question 5.1) — claims to be refereed, 2026-11-14

Graph J(n,5,3): vertices = 5-subsets of an n-set, adjacent iff they share exactly 3 elements. "Independent" = no two share exactly 3.
All files are in this directory (n = 10 material in `n10/`).

## A. n = 10 (the R^9 graph G(10,5,3), 252 vertices)

**A1 (computation).** alpha = 12, and there are exactly 285,600 independent 12-sets.
 - `n10/mis10.py` (Python backtracking: 13,600 contain {0,1,2,3,4}; no independent 13-set contains it; 13,600*252/12 = 285,600).
 - `n10/dlx10.c` (C, own enumeration, smallest-vertex-first): 285,600.

**A2 (explicit certificate).** chi(J(10,5,3)) = 21. A proper 21-colouring: three base classes of 12 sets and their images under
g = (0 1 2 3 4 5 6)(7)(8)(9) (`n10/colouring21_sym_7_1_1_1.json`). Found by `n10/quotient10.py "7,1,1,1"` (CP-SAT exact cover of the 36
g-orbits by maximum independent sets meeting 12 distinct orbits). Checked by `n10/verify_colouring.py` (shares no code with the search;
two negative controls reject). A second colouring invariant under a 5-cycle: `n10/colouring21_sym_5_1_1_1_1_1.json`.
Exactly 1,056 proper 21-colourings are invariant under g (`n10/count_z7.py` hash-join; `n10/count_z7_cpsat.py` solver enumeration;
both 1,056), and the 285,600 maximum independent sets form exactly 11 orbits under Sym(10) (`n10/orbits10.py`).
Lower bound 21 = 252/12 from A1 (also Kupavskii–Raigorodskii 2008, Theorem 2).

**A3 (literature, see world_seat_q51.md and world_seat_n10.md when present).** Kupavskii–Raigorodskii (2008) prove 21 <= chi <= 63 and
report chi <= 30 from a greedy run; Balogh–Kostochka–Raigorodskii (2013) write "chi(G(10,5,3)) = 21 (see [4])". We found no proof or
colouring in print. (Wording on the page: "we found none", not "none exists".)

## B. n = 13 (the R^12 graph, 1,287 vertices), Question 5.1: is chi = 39?

Standing facts (yesterday's page, /day/704-chi-r12-39-refereed-and-the-33-set-is-unique): alpha = 33; every independent 33-set is a
relabelling ("copy") of the Appendix A family W. STATUS OF THAT INPUT: alpha = 33 is certified by the submitter's VeriPB logs (not re-run by us) and
re-derived by our own uncertified computation; the uniqueness theorem is our computation, uncertified (three enumerations + nauty, no
proof log). Everything in B2, B4 and the reading of B3 as 'no obstruction to a 39-colouring' is CONDITIONAL on it. So a proper 39-colouring = a partition P of the 1,287 sets into 39 copies of W
(39*33 = 1287 forces every class to have exactly 33 sets).

**B1 (structure of W; elementary + checked).** W is determined by: a point INF; three "private" pairs (a_i, b_i), i = 1,2,3; three
"shared" pairs S_12, S_13, S_23 (these 1 + 6 + 6 points are all 13). Blocks B_i = {a_i, b_i} u S_ij u S_ik (all six 5-subsets of each);
6-sunflower: core {INF,a_1,a_2,a_3} + each of the 6 shared points; 9-sunflower: core {INF,b_1,b_2,b_3} + each of the other 9 points.
18 + 6 + 9 = 33. Appendix A = (INF=11; a=(1,12,7); b=(2,13,8); S_12={3,6}, S_13={4,5}, S_23={9,10}) in the paper's 1-based labels.
Aut(W) (permutations of the 13 points fixing W) = Z_2 wr S_3, order 48: permute the block indices, swap inside shared pairs.
Number of copies 13!/48 = 129,729,600 = 13 * C(12,3) * C(9,3) * 540. (`wstruct.py` selftest; `prep_lp.py` builds 48 automorphisms and checks them, which shows >= 48. EXACTLY 48: yesterday's bundle
`704/stanikzai-39-refereed` (`autW.py` backtracking over all point maps, and nauty), and today's referee recount `referee/autW.py`.)

**B2 (symmetry theorem).** IF a proper 39-colouring P exists: let Aut(P) = {permutations of the 13 points that map every class of P to a class of P}. Then
|Aut(P)| is 1 or 3, and if it is 3 the generator has cycle type 3^4 1^1 and fixes no class (part (v)).
Proof. Let pi in Aut(P) have prime order q.
 (i) q in {5,7,11}: pi permutes 39 classes; the number of fixed classes is = 39 mod q, i.e. 4, 4, 6 mod q, so some class C has pi(C) = C,
     i.e. pi in Aut(C), a group of order 48. Contradiction.
 (ii) q = 13: pi is a 13-cycle; relabel so pi = (x -> x+1 mod 13). No class is fixed (13 does not divide 48), so the classes form 3 orbits
     of 13. INF(pi^i C) = INF(C) + i, so each orbit has exactly one class with INF = 0. A class C cannot contain two sets S, pi^i S
     (else pi^i C meets C, so pi^i C = C). Two base classes cannot meet the same Z13-orbit of 5-sets (else they are in the same
     class-orbit). So the three base classes (INF = 0) have 33 sets in 33 distinct Z13-orbits each, and together cover each of the 99
     Z13-orbits exactly once. COMPUTATION: of the 9,979,200 copies with INF = 0, exactly 136,540 meet 33 distinct orbits; no three of
     them have disjoint orbit-sets covering the 99 orbits. (`z13.c`; second instrument `z13_check.py`, same counts 9,979,200 /
     histogram tail 30:1548588, 31:1045260, 32:493500, 33:136540 / 0 solutions; planted-solution control `z13_plant.py` +
     `z13_search_only.c` finds the planted cover.)
 (iii) q = 3: cycle type 3^k 1^(13-3k). If k <= 3 then pi fixes some 5-set S (five fixed points, or a 3-cycle plus two fixed points);
     the class C containing S satisfies pi(C) = C, so pi in Aut(C); but all 8 elements of order 3 in Aut(W) have cycle type 3^4 1
     (`involutions.py` table). So k = 4.
 (iv) q = 2: cycle type 2^k 1^(13-2k), 1 <= k <= 6. Let N_k = number of 5-subsets of [13] fixed by pi (sum_j C(k,j) C(13-2k,5-2j)):
     N = 627, 303, 147, 71, 35, 15 for k = 1..6. Every fixed 5-set lies in a pi-invariant class. For an invariant class C = sigma(W),
     sigma^-1 pi sigma is an involution of Aut(W) with the same cycle type, and the number of pi-fixed sets in C equals the number of
     sets of W it fixes, phi. Table over all 19 involutions of Aut(W) (`involutions.py`): type 2^1: phi = 25; 2^2: 17; 2^3: 9; 2^4: 7;
     2^5: 3; no involution of type 2^6. So N_k = (#invariant classes) * phi_k, but 627 = 25*25+2, 303 = 17*17+14, 147 = 9*16+3,
     71 = 7*10+1, 35 = 3*11+2, and for k = 6 there are 15 fixed sets and no possible invariant class. Contradiction in every case.
 (v) ADDED 10:1xZ. If |Aut(P)| = 3, its generator g (type 3^4 1, fixed point p0, 3-cycles O_1..O_4) fixes NO class. Proof: the number f of
     fixed classes is = 39 = 0 mod 3. A fixed class C has g in Aut(C); Aut(C) preserves INF and the triples {a_i}, {b_i}, so INF(C) = p0 and
     {a_1,a_2,a_3}, {b_1,b_2,b_3} are g-invariant 3-sets without fixed points, i.e. two of the cycles O_i. So the 9-core of C is
     T_i = {p0} u O_i and its 6-core is T_j = {p0} u O_j, i != j. A 4-set is the 9-core of at most one class (its 9 supersets all lie in
     that class), the 6-core of at most one class (6 + 6 > 9 supersets), and not both. So f fixed classes use 2f distinct sets among
     T_1..T_4: f <= 2, hence f = 0.
 So Aut(P) has no element of prime order other than 3; by Cauchy's theorem |Aut(P)| = 3^m, and elements of order 3 have type 3^4 1. A group of order 9 cannot occur: Z_9 would
 contain an element with a 9-cycle whose cube has type 3^3 1^4; Z_3 x Z_3 with all 8 non-identity elements of type 3^4 1 would have
 (13 + 8*1)/9 = 21/9 orbits by Burnside's lemma, not an integer. A 3-group of order >= 9 has a subgroup of order 9. Hence |Aut(P)| <= 3. QED

**B3 (lattice; no counting obstruction).** Let L be the subgroup of Z^1287 generated by the indicator vectors of all 129,729,600 copies.
Then L = {x : sum of coordinates = 0 mod 33}. In particular the all-ones vector is in L: an integer combination of copies (negative
coefficients allowed) covers every 5-set exactly once, so no argument by integer-linear identities or congruences (parity, divisibility) on
incidence counts can exclude a 39-colouring. (Inequality arguments, which use non-negativity, are a different matter: see B4.)
Proof. L is inside the right side (each copy has 33 sets). Q = Z^1287 / L:
 - p in {2,5,7,13,17,19,59,347,389}: 1,287 sampled copies are linearly independent mod p (`lattice_modp.py`, `rank_big.py`), so Q has no
   p-part.
 - p > 13 in general: p does not divide 13!, so F_p^1287 is a semisimple Sym(13)-module, multiplicity-free with six irreducible
   constituents (the eigenspaces E_i of the Johnson scheme J(13,5), i = 0..5, dimensions 1, 12, 65, 208, 429, 572). The submodule
   generated by v = 1_W contains E_i's constituent iff E_i v != 0, which holds if v^T E_i v != 0 mod p.
   Why E_i reduces mod p: E_i = (1/1287) sum_j (m_i P_j(i)/v_j) A_j with valencies v_j in {1,40,280,560,350,56}, so its entries lie in
   Z[1/(2*3*5*7*11*13)]; the reductions are orthogonal idempotents summing to 1 that commute with Sym(13), of ranks m_i. For p not
   dividing |Sym(13)| the reduction mod p of each irreducible rational constituent stays irreducible (the decomposition matrix is the
   identity), and the six have distinct dimensions, so they are pairwise non-isomorphic. (23 and 47 were also checked directly:
   logs/rank_extra.out.) Exact values
   v^T E_i v = 11/13, 32/715, 389/77, 472/35, 347/35, 128/35 (`johnson_modp.py`; numeric cross-check `johnson_check.py`); the only
   primes > 13 in numerators/denominators are 59, 347, 389, handled directly above.
 - p = 3 and p = 11: the rank mod p of the sampled copies is 1,286, and it cannot be more because L lies in the sum = 0 mod 33 lattice
   (so Q/pQ = Z/p, Q_p cyclic). The class of e_S generates Q_p, because the coordinate sum maps Q onto Z/33 and sends e_S to 1.
   So p*e_S in L + p^2 Z^1287 forces p*Q_p = 0: and PARI found integer vectors X, Y with
   sum X_i 1_{C_i} = 3 e_S (mod 9) and sum Y_i 1_{C_i} = 11 e_S (mod 121) (`cert_X9.txt`, `cert_Y121.txt`, verified in exact integers by
   `cert_check.py`), so Q_3 = Z/3 and Q_11 = Z/11.
 Hence |Q| = 33 = index of the right side. QED

**B4 (LP; no one-class weight certificate).** Fix class 1 = W. There is a non-negative rational weighting z of the copies disjoint
from W (69,046,650 of them) with total weight exactly 1 on every 5-set outside W — even with three families of valid integrality
cuts added (per 4-set: #blocks through it + 4[9-core] + 3[6-core] <= 4; per 6-set: 3[block] + #sunflower pairs <= 3; every point is
INF of at least one class). The LP is solved in aggregated form: variables = the 1,410,555 distinct Aut(W)-orbit feature vectors of those copies, rows = the 101
Aut(W)-orbits of 5-sets outside W (plus cut rows per orbit). A solution of the aggregated LP lifts to a weighting of copies by spreading
each column's weight evenly over the 48 images of a representative copy, and conversely any weighting can be averaged over Aut(W).
Exact rational solution on 101 columns verified in Fractions (`lp.py`, `lp_exact.py`, `lp_cuts_exact.json`); the referee lifted it to
an explicit weighting of 4,548 copies and checked every 5-set, 4-set, 6-set and point condition exactly (`referee/lp_lift_check.py`). So no Farkas-type certificate ("weights on 5-sets, non-negative on every copy disjoint from W, negative in
total") exists at this level. This is a negative statement about one proof technique only.
 (Why the cuts are valid for a true partition: for a 4-set U, a class contains exactly 9 of its supersets if U is the class's 9-core,
 exactly 6 if U is its 6-core, exactly 2 if U lies in one of its blocks, and otherwise at most 1 (as part of a sunflower set); 9 = 9c9 + 6c6 + 2*blk + sat with sat >= 1 unless c9 = 1 — parity —
 gives blk + 4 c9 + 3 c6 <= 4. For a 6-set H: if H is a block all six 5-subsets are in one class; otherwise two 5-subsets of H in one
 class form a sunflower pair with core inside H and pairs are disjoint, so at most 3 pairs. Point rule: the degree count
 15c + 14b + 12(39-b-c) = 495 gives 3c + 2b = 27, so c is odd, c >= 1.)

**B5 (upper bound).** chi(J(13,5,3)) <= 48: explicit proper colouring `colouring48_n13.json` (TabuCol, `tabucol.c`; an earlier 49 is also
shipped), checked by `n10/verify_colouring.py colouring48_n13.json 13`. So 39 <= chi <= 48. (If a 48- or 47-colouring lands before publication the number
on the page changes accordingly; the checker is the authority.)

## What is NOT claimed
 - Question 5.1 itself (chi = 39 or >= 40) is NOT settled.
 - Nothing about a 3-fold symmetric colouring (type 3^4 1) existing or not.
 - No "first" claims; novelty wording is "we found no earlier ...".
