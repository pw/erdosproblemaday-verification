# Blind read: #704 entry (page/entry.html, 14 Nov draft)

Reader: a blind seat. I did not read CLAIMS.md or referee/. My code is in /tmp/blind704/: check_part1.py, wsym.py, copies.c (+ copies_plant.c as the positive control), misc.py, johnson.py, rankp.py, mis10.c, shapes.py, n10files.py.

Bottom line: every number I recomputed matches. The mathematics of Theorem 1 holds, but three steps are asserted without the one-line reason a referee would ask for. The real problems are in the framing: Theorem 2's title and the homepage summary overclaim, the summary garbles the 2008 bounds, and one sentence about Davies goes beyond the sources.

---

## MUST FIX

**M1. Theorem 2's title and the homepage summary overclaim.**
- Page: "*Theorem 2 (b), (d). No counting argument can exclude a 39-colouring.*"
- Summary: "no counting argument can rule it out".

What is proved: the all-ones vector lies in the integer lattice spanned by the copies of W. That defeats every argument which applies one fixed integer-linear count to every class, sums over a partition, and compares (exactly or modulo some m). Note that 33·Σm_C = 1287 forces Σm_C = 39.

What it does not defeat:
- inequality and averaging arguments (the bound α = 33 that gives 39 is itself a counting argument of this kind);
- arguments that use non-negativity of the multiplicities;
- non-linear counts, such as pairs of classes or how two classes interact.

A signed cover with negative multiplicities satisfies none of the inequalities a real colouring must satisfy. The LP paragraph covers only one non-negative relaxation, at one level.

Corrected title: "*Theorem 2 (b), (d). No divisibility argument can exclude a 39-colouring.*"

Corrected body sentence: "So any argument that applies the same integer-linear count to every class (how often it covers given sets, points, pairs or other sub-configurations) and then compares totals, exactly or modulo any number, is satisfied by this signed cover. Such an argument cannot prove that a true cover is missing."

Corrected summary: "no divisibility (congruence) argument can rule it out".

**M2. The summary garbles what the 2008 source proves.**
- Summary: "citing a source that proves only that between 21 and 63 are needed".

The source (Kupavskii–Raigorodskii, Theorems 2 and 4) proves that at least 21 colours are needed and that 63 suffice. It also reports 30 from a greedy computer run (kr.txt l. 613–614, 659–660). "Between 21 and 63 are needed" reads as if 63 were also a lower-type statement.

Corrected: "citing a source that proves only that the answer lies between 21 and 63 (and reports 30 from a computer run)".

**M3. "we found no colouring in print, so here is one" (summary) is false as written.**
KR's Theorem 4 is an explicit printed construction of a 63-colouring, and they report a 30-colouring found by computer. The body of the page gets this right ("no published colouring with fewer than 30 colours").

Corrected: "we found no 21-colouring in print (nothing below 30), so here is one."

**M4. The Davies sentence says more than the sources.**
- Page: "James Davies's preprint, which claims far larger bounds in every dimension from no exhibited graph."

The notes support improved bounds from dimension 4 up (Voronov on Polymath16: "improved all bounds … starting from R^4"; Crocker: "R^4 and up but not R^3"). That is not every dimension: ℝ² and ℝ³ are not improved.

Corrected: "James Davies's unrefereed preprint, which claims far larger lower bounds in every dimension from 4 up (for ℝ¹², 164 and 2,516) without exhibiting a finite graph."

---

## SHOULD FIX (one line each; detail below)

- **S1. Order 2: "each fixed class contains the same number of them, a number that depends only on k"** is true, but it is a computed fact, not an obvious one. All involutions of W that swap k pairs fix the same number of W's sets: I checked this, and each k gives a single value. The page should say "(by the table: every symmetry of W that swaps k pairs fixes the same number of its sets)". Also say why a fixed class has such a symmetry: the colouring's symmetry restricts to a symmetry of that copy, with the same cycle type.
- **S2. "A 4-set can be the core of only one sunflower in the whole colouring"** is true but given no reason. Add: "since a 4-set lies in only 9 five-sets and each sunflower uses at least 6 of them". Also say why the fixed point must be the special point: every symmetry of W fixes it, and the order-3 ones fix nothing else. And say why each core is p plus a 3-cycle: σ preserves each sunflower, because they have different sizes.
- **S3. "Putting it together" leaves out two group-theory steps.** As written it rules out elements of order 2, 5, 7, 11, 13 and groups of order exactly 9. To conclude that the order is 1 or 3 it also needs: (i) Cauchy's theorem, so the group order is a power of 3 (this is what excludes 4, 6, 12 and so on); (ii) every group of order 3^m with m ≥ 2 contains a subgroup of order 9. Name Burnside's lemma for the (13+8)/9 count, and say that the cube of the order-9 element contradicts the four-3-cycles fact from the Order 3 bullet. The argument is correct once these are added.
- **S4. Summary: "so it cannot be found the way such colourings usually are"** overreaches. A search with a single order-3 symmetry is still possible, and the page itself lists that case as open. Suggest: "so it cannot be found by imposing a large symmetry group".
- **S5. "there are 285,600, of at least 11 different shapes"**: the number is exactly 11. I computed the S₁₀-orbits by union-find. The orbit sizes are 210, 1575, 1575, 5040, 25200×3, 50400×4, with stabilisers 17280, 2304, 2304, 720, 144×3, 72×4. Say "of exactly 11 shapes (up to relabelling the 10 points)".
- **S6. Notation:** J(13,5,3) and G(10,5,3) name the same family of graphs. Use one letter throughout, or say once that they are the same construction.
- **S7. "7-step shift" / "5-step shift"** reads as "shift by 7". Write "the shift of order 7 (a 7-cycle on 0–6, fixing 7, 8, 9)". Say why there are 36 orbits: 252/7, since no 5-set is fixed.
- **S8. The labels line lists (a), (b), (d) with no (c).** It looks like a typo. Either explain the gap or reletter.
- **S9. Undefined terms:** "fixed class" (a class carried to itself), "core" (first used in the Order 3 bullet, never defined in the anatomy paragraph), "mirror symmetry" (meaning an order-2 permutation; there is no geometric mirror here), "admissible class" and "three families of extra inequalities" in the LP paragraph (unspecified), "at this level".
- **S10. Brooks bullet:** state that 280 is the degree ("each set is joined to C(5,3)·C(8,2) = 280 others"). Otherwise the number has no referent.
- **S11. Theorem 2 "How" bullet:** "explicit combinations equal to 3 and to 11 times a single coordinate" means 3·e_i ∈ L + 9ℤⁿ and 11·e_i ∈ L + 121ℤⁿ. Spell it out, and add "by symmetry, for every coordinate", which the index argument needs. Also say that the projection argument needs the idempotents to be p-integral; they are for p > 13, since every denominator involves only primes ≤ 13.
- **S12. "This also closes the two symmetric searches that yesterday's entry reported as unfinished"**: an outsider cannot tell which searches these are. Name them.
- **S13. Attribution:** "Yesterday we showed, by computation, that every family of 33 sets … is a relabelling of one family W". Make clear whether uniqueness is our result or part of Stanikzai's refereed paper. The page credits Stanikzai with the 39 and "us" with uniqueness, and the homepage link slug reads "the-33-set-is-unique".

---

## CHECKED OK (numbered claims)

1. **The printed 21-colouring of G(10,5,3) is proper, partitions all 252 sets, and has 21 classes of 12.** Checked by my code, parsing from the HTML (check_part1.py): 3 families of 12 parsed; shifting 7 times by +1 mod 7 on digits 0–6 gives 21 classes and 252 distinct sets equal to all of C(10,5); 0 pairs share exactly 3. Negative control: swapping two sets between classes gives 14 bad pairs. The page colouring equals n10/colouring21_sym_7_1_1_1.json (n10files.py).
2. **The bundled second colouring is a proper 21-colouring invariant under a 5-cycle** (cycle type 5+1⁵). Checked by my code (n10files.py).
3. **There are 285,600 independent 12-sets in G(10,5,3), and no independent 13-set (α = 12).** Checked by my code (mis10.c, bitset enumeration): 285,600, and 0 of size 13.
4. **36 shift-orbits** = 252/7, since no 5-set is fixed by a 7-cycle with 3 fixed points. Checked by reasoning.
5. **"W has 48 symmetries"** Checked by my code (wsym.py, backtracking over all point maps): |Aut(W)| = 48. Element orders: 1×1, 2×19, 3×8, 4×12, 6×8. The description "permute blocks × swap inside shared pairs" (C₂ wr S₃) matches the order and the cycle types.
6. **The anatomy paragraph** matches W (wstruct role form, reproduced, plus point degrees). The special point has degree 15 and is unique. The three blocks are full 6-sets (6 sets each, 18 in total), each made of one private pair {aᵢ,bᵢ} and two shared pairs, and each shared pair lies in two blocks. The 9-sunflower has core {special, b₁,b₂,b₃} and the 9 other points as petals. The 6-sunflower has core {special, a₁,a₂,a₃} and the 6 shared points as petals. 18 + 9 + 6 = 33. Checked by reasoning and code.
7. **"the order-3 symmetries of W all consist of four 3-cycles"** All 8 have cycle type 3⁴1, and the fixed point is the special point. Checked by my code.
8. **Order-2 table.** Fixed 5-sets of 13 points for k = 1..6 are 627, 303, 147, 71, 35, 15. Fixed W-sets for W's involutions are k=1: 25, k=2: 17, k=3: 9, k=4: 7, k=5: 3, each a single value for that k. No involution of W swaps 6 pairs. Remainders 627 mod 25 = 2, 303 mod 17 = 14, 147 mod 9 = 3, 71 mod 7 = 1, 35 mod 3 = 2. Checked by my code (wsym.py, misc.py).
9. **39 mod 5, 7, 11 = 4, 4, 6.** Checked by my code.
10. **Orders 5, 7, 11 argument.** The number of fixed classes is ≡ 39 mod q, which is > 0, and 48 = 2⁴·3. Valid, checked by reasoning.
11. **Order 3 argument.** Fewer than four 3-cycles ⇒ a fixed 5-set (3+2 is available whenever there are ≥ 2 fixed points). With four 3-cycles there is no fixed 5-set. Each fixed class uses two of the four 4-sets {p} ∪ (3-cycle), and different classes use disjoint ones (true, see S2), so there are ≤ 2 fixed classes. The count is ≡ 39 ≡ 0 mod 3, so 0. Valid, checked by reasoning.
12. **Order 9 exclusion.** The cube of an element of order 9 on 13 points has exactly three 3-cycles. For C₃×C₃, Burnside gives (13 + 8·1)/9 = 7/3. Valid (gaps in S3), checked by reasoning and code.
13. **Order 13: 9,979,200 copies with special point 0** (= 13!/48/13), **136,540 orbit-transversal copies, and no three cover the 99 orbits.** Checked by my code (copies.c, enumeration of all 129,729,600 copies by role form). Results: total 129,729,600 = 13!/48; special point 0: 9,979,200; transversal: 136,540; covering triples: 0 (with orbit 0 in the first copy, which is no loss of generality). Positive control: a planted complementary pair is found (1 triple). The logic is valid: one class per orbit has special point 0, each representative is an orbit transversal, and together they partition the 99 orbits.
14. **69,046,650 copies of W disjoint from a fixed class.** Checked by my code (copies.c, disjoint from W itself).
15. **Squared lengths of W's components in the six J(13,5) eigenspaces:** 11/13, 32/715, 389/77, 472/35, 347/35, 128/35. Their sum is 33 = |W|. Checked by my code (johnson.py, projection onto spans of inclusion matrices; floats rationalised, matching to 1e-9).
16. **59, 347, 389 are exactly the primes > 13 dividing a numerator.** The numerators are 11, 2⁵, 389, 2³·59, 347, 2⁷. Checked by my code. The direction of the logic is right: if Eⱼv ≡ 0 mod p then p divides vᵀEⱼv.
17. **Mod-p ranks of copy vectors** (independent random sample of 1,450 copies). Rank 1287 mod 2, 5, 7, 13, 59, 347, 389; rank 1286 mod 3 and 11. Checked by my code (rankp.py).
18. **Brooks gives 280** (the degree is C(5,3)·C(8,2)). **Lovász gives (1+ln 33)·1287/33 = 175.36, so 175.** Checked by my code.
19. **colouring48_n13.json** has 48 non-empty classes partitioning all 1,287 sets, with 0 bad pairs (largest class 31). Checked by my code.
20. **1287 = 39·33; the sets sit in ℝ¹² (respectively ℝ⁹) at distance 1 after scaling** (the hyperplane Σx = 5; joined sets are at distance 2 before scaling). Checked by reasoning.
21. **Literature: KR 2008 Theorem 2 α = 12 ⇒ χ ≥ 21 ⇒ χ(ℝ⁹) ≥ 21; Theorem 4 χ ≤ 63; "огромен" ("huge"); greedy 30.** Checked against kr.txt l. 106, 115, 613–614, 659–660.
22. **BKR 2013 writes "χ(G(10,5,3)) = 21 (see [4])", with [4] = KR (the J. Math. Sci. 2009 translation).** Checked against bkr.txt l. 248 and 329.
23. **CKR has χ(ℝ⁹) ≥ 22 from a different graph.** Checked against ckr.txt l. 99 (Prop. 1). It is the DAM 2018 paper (arXiv 2015), per the notes.
24. **Q5.1: the Zenodo deposit has one version, last touched 12 Nov; nothing was found on arXiv, MathOverflow, Polymath16 or the forum; no earlier colouring of J(13,5,3).** Consistent with world_seat_q51.md §1–2 (an absence claim, worded correctly as "we found").
25. **"Two surveys by Raigorodskii (2013, 2014) behind paywalls"; "no published colouring with fewer than 30".** Consistent with world_seat_n10.md.

The page makes no priority claim in the body ("The value is right; here is a colouring") apart from the summary wording in M3.

## NOT CHECKED

- "Erdős 1981" and the paraphrase of #704: not in the sources I was given.
- The lattice index at 3 and 11: the explicit combinations giving 3·eᵢ mod 9 and 11·eᵢ mod 121. I checked only the logic and the mod-p ranks, not the combinations.
- The LP certificate: the exact-fraction weighting and the "three families of extra inequalities". They are unspecified on the page and the files are heavy.
- Provenance statements: "two programs, written separately, agree"; "a second program in another language"; "a constraint solver found one in seven seconds"; the 20-line checker rejecting two broken inputs; "Every count in Theorem 1 was produced twice". My own runs are a third independent reproduction of the counts.
- "Closes the two symmetric searches that yesterday's entry reported as unfinished": I have no access to yesterday's entry.
- Who proved that the 33-set is unique (see S13).
- That the 2013 and 2014 Raigorodskii items are "surveys": the notes' wording, not read.
- James's and Maschke's theorems were checked as correctly invoked (p > 13 ⇒ semisimple, Specht modules irreducible, M^{(8,5)} multiplicity-free with dimensions 1, 12, 65, 208, 429, 572). The citation of James's theorem itself was not checked.
