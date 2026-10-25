# #85 submission jhpvtq — from-scratch encoding v2 (fs/): H3, H5, H7 (t >= 1), H9 without the authors' code

Written 2026-10-19 by the 12:00Z erdos seat. Our own code end to end: normalisation (../h9/hrun.py, README of
../h9), base encoder ../h9/c4cnf.py (exact low degrees + codegree <= 1), plus three additions in fsenc.py.
Nothing here reads the authors' Lean, emitters, CNFs or certificates.

## What is added, and why each is sound

Setting: G C4-free on 49 vertices, min degree >= 7. (Paper 2.2 / our hand re-derivation.) Every degree is 7 or 8;
a degree-8 vertex x ("high") has only degree-7 neighbours; h = #high is odd and in {1,3,5,7,9}.

**R1 + R1b — for every high x, every vertex v != x has EXACTLY one neighbour in N(x).**
The non-returning 2-walks x-u-v (u in N(x), v != x) number sum_{u in N(x)} (deg u - 1) = 8 * 6 = 48 = |V \ {x}|.
C4-freeness makes their endpoints distinct (two walks x-u-v, x-u'-v with u != u' close a 4-cycle). So the 48
endpoints are all of V \ {x}, each once. For v in N(x) this says N(x) induces a perfect matching (R1); for v
outside N[x] it says v has exactly one neighbour in N(x) (R1b). The base encoder already has "at most one"
(codegree <= 1); R1/R1b add the "at least one" clauses. This is a pigeonhole consequence the solver would
otherwise have to rediscover by resolution, which is exponentially hard for pigeonhole.

**SB — lex-leader symmetry breaking on interchangeable low vertices.**
Two free (low) vertices i < j with the same fixed neighbourhood (same high-neighbourhood block) and the same
target degree are interchangeable: the transposition (i j) maps the whole formula, R1/R1b included, to itself.
With the edge variables ordered row-major over the upper triangle, the lex-leader constraint X <=lex (i j)X
unfolds to: row_i <=lex row_j over the columns k not in {i, j}, in increasing k (0 < 1). [Columns k < i are
compared at positions (k,i) vs (k,j), which come before row i; columns k > i at positions (i,k) in row i.]
Lex-leader constraints for any set of group elements under ONE variable order are jointly sound: the
lexicographically least member of each orbit satisfies all of them. We add it for every pair in each class.

## Controls (all must pass before any stratum verdict is read)
- sbtest.py — brute force on 7 tiny instances: (1) for every edge assignment (or 20,000 random ones + every
  solution when > 16 edges) the CNF's SB clauses accept iff the independent semantic check `lex_ok` does;
  (2) every solution's orbit under the class group contains a member passing `lex_ok` (SB loses no class);
  (3) MUTATION: one SB clause with flipped direction must produce mismatches. Result: sbtest.out.
- er7ctl.py — end to end on ER(7) (PG(2,7) polarity graph, 57 vertices, C4-free): for a passant point x
  (non-absolute, no absolute neighbour) R1 and R1b are TRUE; with x's edges + 37 other vertices fixed and 20 free
  (N(x) among them), R1/R1b/SB on, both solvers must return SAT and the model must re-check (degrees, codegree,
  R1+R1b, lex order). MUTATION: demand R1 for a SECANT point y (whose two absolute neighbours have no partner in
  N(y) in ER(7)) — must not return ER(7). Result: er7ctl_r1b.out (in /tmp/erdos85-fs, copied to the bundle).
- erqctl.py — POSITIVE composition control, exhaustive: ER(3) with a passant high, all edges at the high fixed,
  everything else free; R1/R1b are theorems there (saturation (q+1)q = n-1). BASE (c4cnf only) has 1,728 labelled
  solutions = 1 isomorphism class (ER(3)); PIPE (R1+R1b+SB) keeps exactly 1 solution of that class; R1/R1b hold on all
  1,728 BASE solutions. (ER(5) exhaustive enumeration hit the harness time limit — superseded by the descent tests.)
- erdescend_hsb.py — production-scale witness test for class SB + HIGH-PERMUTATION SB together (extends the referee's
  ref/erdescend.py): ER(5)/ER(7), 3–6 pairwise non-adjacent passant highs, every permutation of the highs that preserves
  the (block, target) multiset (up to 719 = all of S6 minus id), lex-descend ER(q) by all generators; the FULL CNF
  accepts the descended graph and rejects raw ER(q), 5/5 configurations.
- h1norm_erctl.py — same descent test for h1norm.py's anchor normalisation, on ER(7) (x passant, N(x)=1..8 matched,
  B_i of 6): 63 target-preserving matching permutations + 12 classes; descended accepted, raw rejected.
- Hostile referee (Opus, tools, told to refute): SOUND AS READ — referee/REPORT.md (scripts in ref/).

## Third addition: high-permutation SB (fsrun.py --hsb; fsenc.add_perm_sb/high_perm)
For a permutation sigma of the highs that maps the block multiset to itself (sigma in Aut of the high-low incidence),
the induced vertex permutation pi (lows with block B -> lows with block sigma(B), in order) maps the fixed edge set to
itself, so it acts on solutions. Lex-leader X <=lex X o pi over the same sorted free-edge order is sound jointly with
the class transpositions (same group, same order). Used with every TRANSPOSITION of highs that preserves the blocks
(21 for H7 t=0, 9 for H7 t=1). Results are reported with and without it.

## H1 anchor normalisation (h1norm.py) — a second, independent H1 encoding
x = 0; N(x) = 1..8, matching relabelled to 1-2,3-4,5-6,7-8 (R1); every other vertex has exactly one neighbour in N(x)
(R1b) and each of 1..8 has exactly 5 of them (degree 7 = x + partner + 5) -> relabel so B_i are consecutive blocks of 5.
WLOG by relabelling. Unknowns: the 780 edges among the 40. SB: transpositions inside each B_i + all 383 non-identity
matching-preserving permutations of 1..8 induced on the B_i. (The paper describes the same anchor structure in 2.4;
nothing of theirs — tables, orbits, profiles, miss tables — is used.)
