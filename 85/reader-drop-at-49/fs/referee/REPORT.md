# Hostile referee — fs/ encoding (R1 + R1b + lex-leader SB) for #85 jhpvtq
Seat: separately briefed Opus with tools, told to refute; 2026-10-19 ~12:20–12:52Z; 39 tool calls; scratch /tmp/fsref
(copied to fs/ref/). Transcribed by the main seat from the seat's final message.

**Verdict: SOUND AS READ.** No path found by which a satisfiable cell could read UNSAT. Reviewed fsenc.py as of 12:18:45;
rebuilding h3_t1 / h5_t1 gives byte-identical CNFs (sha bba31f7e4afde651, a2c26f8de02d3ee3).

1. NOTE — R1/R1b correct and exactly encoded. Re-derived: 2-walks x-u-v number sum(deg u - 1) <= 48 by codegree <= 1, so
   deg <= 8; deg 8 tight => all nbrs deg 7, every v != x has exactly one common nbr with x; k <= 3 (each high nbr of a low
   needs its own low matching partner, 2k <= 7); s(x) = 9-h+r3; h odd; h <= 9 by block count. Code: "at least one" clause
   per u in N(x); `if v == h or v in adjS[h]: continue`; free v outside N[x] one clause; other highs asserted exactly one
   fixed hit. Counts h3 3x38=114, h5 5x36=180. pysat seqcounter CardEnc.equals exhaustively correct for <= 9 literals.
2. NOTE — SB correct. var row-major (combinations of sorted F); first-difference positions for (i j) are (k,i), k<i and
   (i,k), k>i, i.e. increasing k => X <=lex (i j)X == row_i <=lex row_j over free k not in {i,j}. Skipping S columns fine
   (equal fixed entries). Same block => (i j) preserves fixed edges and N(x) as a set => solution set of base+R1+R1b
   invariant; all-pairs jointly sound. One-directional e-chain sound. Full-scale: 1,200 assignments on the real h3_t1 CNF,
   475 accepted, 0 mismatches vs lex_ok (sb49.py). Witness test (erdescend.py): ER(q), pairwise non-adjacent passant
   points as highs (deg q+1 = 8 at q=7), real fsenc.build with R1+R1b+SB, ER lex-descended by violating class
   transpositions: FULL CNF accepts the descended graph in all 7 configurations up to ER(7) 6 highs classes
   [3,3,10,3,3,8,3,3] and ER(7) 1 high classes [8,40,8] (~ the h=1 cell); raw ER rejected every time (discriminating).
   Exhaustive ER(3) 1 high: 1,728 solutions without SB, one orbit, SB keeps exactly one.
3. NOTE — normalisation loses no generality (block multiset forced; block-label order WLOG; every low-low pair a
   variable; c4cnf complete here: fixed_common = 0 for high-low, free-free c0 = |B_v n B_w| <= 1). Rep files checked by an
   independent canonical form: 7 points 1,1,2,3,3,2,1,1; 9 points 1,1,2,5,11; all linear.
4. MINOR — our own controls had not tested SB together with R1/R1b (er7ctl classes=[]; sbtest r1=False; 4/7 sbtest cases
   vacuous). Closed by the referee's descent test. [Main seat, after: erdescend_hsb.py extends it to the high-permutation
   SB — ER(5)/ER(7) with 3–6 highs, up to 719 block-preserving permutations of the highs: descended accepted, raw rejected,
   5/5.]
5. MINOR — smallctl.py skipped h=0 and direct runs were UNKNOWN (d=4 h=2 at 120 s, d=5 at 240 s) => that control never
   exercised the SAT direction. [Main seat: killed it; replaced by the ER(q) controls.]
6. MINOR — files changed during review (hdeg, add_perm_sb, high_perm, stratum_gen). add_perm_sb/high_perm reviewed anyway:
   sound as written (X <=lex X o pi, pi induced by sigma in Aut(T) maps fixed edges to fixed edges, same sorted(var)
   order). Nits: unused `blocks_lowstart`; the tag did not record high-perm SB. [Main seat: tag now carries 'hsb'.]
7. NOTE — coverage: H1 and H7 t=0 were outside the fs scope when read; a full independent f(49)=7 needs every cell.
