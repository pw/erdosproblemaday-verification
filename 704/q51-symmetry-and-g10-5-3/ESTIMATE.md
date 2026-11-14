# #704 Q5.1 — is chi(J(13,5,3)) = 39?  (erdos seat, 2026-11-14 09Z tick)  ESTIMATE, written before spending CPU

Setting. alpha = 33 and 1287 = 39*33, so chi = 39 iff the 1,287 five-sets split into 39 maximum independent sets;
by yesterday's uniqueness theorem each is a relabelling of W. Structure of W (read off Appendix A, re-derived in
wstruct.py): a point INF; three private pairs (a_i,b_i); three shared pairs S_12,S_13,S_23; blocks
B_i = {a_i,b_i} u S_ij u S_ik (all six 5-subsets); 6-sunflower core {INF,a1,a2,a3} + the 6 shared points;
9-sunflower core {INF,b1,b2,b3} + the other 9 points. Copies: 13*C(12,3)*C(9,3)*540 = 129,729,600 (= 13!/48).

Steps and budgets (all single-digit core-minutes unless said):
 S1 lattice test: is the all-ones vector in the Z-span of the copies' indicator vectors? rank mod p for
    p in {2,3,5,7,11,13} on ~3000 random copies (1287 columns), then exact p-adic (mod p^k) membership for p | index.
    Cost: seconds-minutes numpy. An obstruction here = a counting proof of chi >= 40. No obstruction = no proof by
    linear counting mod m exists (worth saying on the page).
 S2 automorphism bookkeeping (by hand): an element of order 5, 7, 11 of Sym(13) fixes >= 4 of 39 classes, and would
    lie in Aut(W) (order 48) — impossible. So Aut(colouring) is a {2,3,13}-group.
 S3 order 13 exhaustively: a Z13-invariant colouring = 3 copies of W, each meeting 33 distinct Z13-orbits (of 99),
    jointly covering all 99. Enumerate ALL 129.7M copies in C (33 lookups each ~ 4e9 ops, < 1 core-minute), keep
    the partial transversals (heuristic ~1e6), then exact 3-cover by bitmask hash (<= ~1e11 AND ops worst case,
    minutes on a few cores). F39-transitive colourings are the sub-case 'one copy is a transversal of the 33
    F39-orbits' — same enumeration.
 S4 only if S1-S3 leave it open: think about the general exact cover (129.7M candidates; plain DLX is hopeless;
    needs a structural decomposition). Do NOT launch a long campaign without a written sub-estimate.
Memory: all scripts under ulimit -v 8 GB, nice 19. No Lean. Disk 20 GB free: no big artefacts.
Controls: copy generator must reproduce 129,729,600 distinct copies / each 5-set in 3,326,400 copies (sampled),
every generated copy independent in J(13,5,3) and of size 33; lattice code must reject a planted non-member.
