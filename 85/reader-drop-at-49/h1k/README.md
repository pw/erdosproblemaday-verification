# H1 by hand reduction + Lemma D + a 5-case split (2026-10-19, 15:00Z erdos seat)

Goal: an INDEPENDENT proof that stratum H1 of the #85 submission is empty — i.e. there is no C4-free graph G on 49
vertices with one vertex x of degree 8 and all other degrees 7 — without the authors' 13,351 orbits / ~28 TB of LRAT.
Everything here is our code; nothing reads the authors' artefacts. Written for general odd k (n = k², deg x = k+1,
all others k; k = 7 is H1) so the machinery can be exercised at k = 3, 5.

## 1. Reduction (label (a))
Put d = k − 1. Non-returning 2-walks from x: Σ_{u∈N(x)} (deg u − 1) = (k+1)(k−1) = n − 1, and C4-freeness makes their
endpoints distinct, so they are exactly V∖{x}. Hence (R1) N(x) induces a perfect matching u_X ~ u_X' and (R1b) every
vertex outside N[x] has exactly one neighbour in N(x). Each u ∈ N(x) has degree k = 1 (x) + 1 (partner) + (k−2), so
the far set F = V ∖ N[x] (|F| = (k+1)(k−2)) is partitioned into k+1 blocks X = N(u_X) ∩ F of size k−2, paired as the
u's are. Let H = G[F]: every far vertex has degree k − 1 = d in H. C4-freeness of G is then EQUIVALENT to:
  (i) H is C4-free; (ii) no H-edge joins paired blocks (else w–u_X–u_X'–w' is a C4);
  (iii) every vertex has ≤ 1 H-neighbour in each block (two in Y share u_Y with it).
(Conversely (i)–(iii) give a C4-free G: a 4-cycle through x has its opposite vertex either in N(x) (excluded: N(x)
induces a matching, so two N(x)-vertices have no common neighbour there besides x) or far with two N(x)-neighbours
(excluded by R1b); one through
u_X but not x needs two vertices of X with a common H-neighbour (iii), or an X–X' edge (ii), or two N(x)-neighbours.)
So H1 is empty ⇔ no such H. Note F has d+2 blocks; each z ∈ F has d+1 available blocks (all but its partner).

## 2. Lemma D (label (a))
Notation: N[X][Y] = #H-edges between blocks X ≠ Y; N[X][X] = 2e(X), e(X) = #H-edges inside X; N[X][X'] = 0.
For blocks X ≠ Y let q(X,Y) = #{(a,b) ∈ X × Y : a, b have no common neighbour in G}.

**Lemma D.** q(X,Y) = N[X'][Y] + N[X][Y'] − (d − 1). In particular N[X'][Y] + N[X][Y'] ≥ d − 1, and for Y = X':
e(X) + e(X') ≥ (d − 1)/2.

Proof.
1. Each z ∈ F has H-neighbours in exactly d of its d+1 available blocks (degree d, ≤ 1 per block by (iii), none in
   the partner block by (ii)); so z MISSES exactly one available block.
2. Each block Y is missed by exactly d − 1 vertices: the z ∉ Y ∪ Y' adjacent to Y are the far ends of the
   d(d−1) − 2e(Y) H-edges leaving Y (none go to Y' by (ii); far ends distinct by (iii)), out of |F ∖ (Y ∪ Y')| = d(d−1) candidates, so 2e(Y) of them
   miss Y; inside Y the vertices with no H-neighbour in Y number (d−1) − 2e(Y). Total d − 1.
3. For X ≠ Y, a common G-neighbour of a ∈ X and b ∈ Y is a far vertex (by (R1b) the only N(x)-neighbour of a is u_X
   and of b is u_Y ≠ u_X; x is adjacent to neither). The map z ↦ (its X-neighbour, its Y-neighbour) is a bijection from
   {z ∈ F : z has an H-neighbour in X and one in Y} onto the pairs with a common neighbour (injective by C4-freeness,
   since a ≠ b). So q(X,Y) = (d−1)² − m(X,Y) with m(X,Y) = #{z adjacent to both X and Y}.
4. Such z lies outside X' ∪ Y' (vertices of X' have no neighbour in X by (ii)); for z ∉ X' ∪ Y' both X and Y are
   available, and by step 1 z misses at most one of them. With μ(Z,X) := #{z ∈ Z missing X} (Z ≠ X'),
   m(X,Y) = d(d−1) − [(d−1) − μ(Y',X)] − [(d−1) − μ(X',Y)]   (|F ∖ (X'∪Y')| = d(d−1); step 2 for the missers —
   all d−1 missers of X lie outside X', since X is not available to vertices of X').
5. μ(Z,X) = (d−1) − N[Z][X] for Z ∉ {X, X'} (each vertex of Z has ≤ 1 neighbour in X), and μ(X,X) = (d−1) − 2e(X).
   So q(X,Y) = (d−1)² − (d−1)(d−2) − μ(Y',X) − μ(X',Y) = N[Y'][X] + N[X'][Y] − (d−1). ∎

k = 7 (d = 6): e(X) ≤ 2 (a 5-vertex block of N(u_X) induces a matching) and e(X) + e(X') ≥ 3, so every pair has
{e(X), e(X')} = {1, 2} or {2, 2}; and N[X'][Y] + N[X][Y'] ≥ 5 for the 24 non-paired pairs {X,Y}, which the identity
(X,Y) ~ (X',Y') pairs up into 12 distinct constraints (the encoder adds each twice, harmlessly).  k = 5 (d = 4): e ≤ 1 and e(X) + e(X') ≥ 2 force e ≡ 1.

## 3. The case split (k = 7)
Symmetries of the H1 setting: swapping a pair (u_X ↔ u_X', X ↔ X') and permuting the four pairs. So WLOG the pairs
are ordered with the j pairs of type (2,2) first and every (1,2) pair oriented (2,1): **cases j = 0..4**. Inside each
block the internal matching (2 or 1 edges on 5 vertices) is unique up to the block's S5, so it is fixed to local edges
(0,1)(2,3) or (0,1). Residual SB: lex-leader for the transpositions that fix the internal matching (swap the ends of a
matched edge; swap two unmatched vertices), row-lex form as in fs/README.md. Lemma D's 24 cross constraints are added
as cardinality constraints. Encoder: `h1cube.py k j cap solver`.

### 2b. Implied additions in h1cube2.py (second referee: referee2/)
- `--pairsb`: lex-leader (fs/fsenc.add_perm_sb, same row-major order) for every non-identity block-level symmetry of the
  case (permute same-type pairs; swap inside (2,2) pairs).
- `--slots`: unmatched vertices have EXACTLY one neighbour in each of the 6 non-partner other blocks; matched vertices
  hit at least 5 of those 6.
- `--ph` (PIGEONHOLE): every far vertex w has 6 H-neighbours; for a block Y ≠ blk(w), the neighbours of w that touch Y
  map injectively (C4-free) to their unique Y-neighbour, into |Y| = 5 ⇒ at least one neighbour of w has no neighbour in
  Y. Equivalent form: writing μ(z) for the block z misses, every far vertex w has a neighbour z with μ(z) = μ(w)'
  (the partner blocks of w's 6 neighbours are 6 distinct blocks: every block other than blk(w) and μ(w)', so PH is
  automatic for those and says something only for Y = μ(w)'; for an unmatched w, μ(w) = blk(w)), i.e. the 'paired-miss' edges form a
  spanning subgraph of H of minimum degree ≥ 1.

## 4. Evidence so far
- k = 3: UNSAT (h1k.py plain and h1kb.py block form).
- k = 5: block form UNSAT with within-block lex SB (kissat 0.5 s; CaDiCaL agrees), UNKNOWN at 600 s without SB;
  the paired-block restriction RELAXED is SAT (control). Case form `h1cube.py 5 0`: UNSAT with and without residual
  SB; `--drop-c4` SAT and the model re-checks clean (degrees, block rules, fixed internal edges, lex order).
- k = 7: `--drop-c4` controls SAT and re-check clean for all five cases. Case results: runs/ (see RESULTS below).

## RESULTS (k = 7, kissat 4.0.4, nice 19 on a box at load ~20–24; 2026-10-19)
| run | flags | cap | verdict |
|---|---|---|---|
| case 4 (probe) | base (transposition SB + Lemma D) | 600 s | UNKNOWN |
| case 4 | + pair-level SB (383 perms) | 1800 s | UNKNOWN |
| case 0 | + pair-level SB (23 perms) | 1800 s | UNKNOWN |
| case 4 | + pair-level SB + slots | 1800 s | UNKNOWN |
| case 4, case 0 | + pair-level SB + slots + PH | 7200 s | RUNNING (runs/c4_case{4,0}.out, launched 16:13Z) |
Controls (all as expected): k = 5 case form UNSAT (± SB, kissat); k = 5 block form UNSAT with SB (kissat + CaDiCaL);
`--drop-c4` SAT + clean semantic re-check for k = 5 and all five k = 7 cases (with and without pair SB; pair-perm lex
check discriminates: 0 violations with the clauses, 28/47 and 323/383 without); the relaxed-pairs block-form model from h1kb.py (a real C4-free H
obeying the block rules, paired-block edges allowed) has 0 PH violations. Referees: referee/ (HOLDS AS READ — Lemma D,
reduction, case split, h1cube.py; clause audit + positive controls with C4 on) and referee2/ (HOLDS WITH FIXES —
pairsb/slots/PH sound with equivalence + implication + orbit tests; **h1cube2's `--relax-pairs` is NOT a valid
positive control** — the fixed case pattern excludes relaxed solutions by construction — and is not cited as evidence).
**k = 5 analogue also EMPTY BY ENUMERATION, no SAT** (referee2/geng_blocks.py: all 64 4-regular C4-free graphs on 18
vertices; 7 admissible block partitions, none pairable).
**Reading:** as single monolithic SAT calls the five k = 7 cases do not fall in 30 min. Closing H1 this way = a cube
campaign (cube on the miss function μ, §2c) — not started from a cron tick. If a 2-h run returns UNSAT: certify with
`runs/certify_case.sh runs/c4_case<j>.cnf` (CaDiCaL DRAT + drat-trim) and run the other four cases with the same flags.

### 2c. Next-rung notes (15Z seat, UNVERIFIED — derived by hand, not yet refereed or tested)
- Every per-vertex count is automatic: with r(w) = #{z ~ w : μ(z) = μ(w)'}, the codegree-0 degree of w is
  (r(w) − 1) + (6 − r(w)) = 5 identically; PH is exactly r(w) ≥ 1.
- Symmetry of the codegree-0 relation gives a GLOBAL identity: q(X,Y) = E(X, C_Y) − |X ∩ C_{Y'}| = E(Y, C_X) − |Y ∩ C_{X'}|
  (C_Y = vertices missing Y, |C_Y| = 5; E = #H-edges). In case j = 4 this reads E(X, C_Y) = 5 − M[X'][Y] for generic Y,
  M[X][Y] = #matched vertices of X missing Y. Once μ is FIXED (a cube), these are cardinality constraints on known sets
  and every "≤ 1 neighbour in Y" becomes "exactly one" for Y ≠ μ(w). A cube-on-μ campaign = enumerate μ up to the case
  group (row sums 2e(X), column sums 2e(Y), Lemma D), then one SAT call per μ-class. Size unknown; NOT started.
- TRI (by hand, unrefereed): in G, |M(w)| = 6 for a far w while its 7 neighbours not in a G-triangle all lie in M(w),
  and N_G(w) induces a matching ⇒ τ_G(w) ≥ 1; τ_G(w) = o(w) + t_H(w) (o = has an own-block neighbour) ⇒ **every
  unmatched far vertex lies in an H-triangle** (≥ 1 per block in every case). Equivalently from H alone: the ball
  {w} ∪ N_H(w) ∪ (30 distinct H-2-walk ends) has 37 − 2t_H(w) vertices and misses w's 4 − o(w) non-neighbour block
  mates ⇒ 2t_H(w) + o(w) ≥ 1. NOTE this rules out the (6,5)-cage route (H is never triangle-free).
- COV (by hand, unrefereed): the 30 H-2-walk ends of w are distinct and avoid w's block ⇒ they cover exactly 30 of the
  35 vertices outside it; an explicit "≥ 30 covered" cardinality over coverage indicators is the global form of PH.
- Both are candidate additions for a campaign encoder (pigeonhole facts CDCL does not rediscover; R1b was the same kind).
