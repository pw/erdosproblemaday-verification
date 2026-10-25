# Hostile audit of the frozen Erdős #813 bundle

Date: 2026-08-12 UTC

Audited source bundle: `/tmp/erdos813_attack`. The versioned publication
copy is the parent directory of this audit.

## Verdict

The structural reduction is correct, and every reproducible finite check I
could make passed.  In particular, the neighbourhood family is defined and
augmented correctly, the order-10 direct census anchors completeness, the
fixed-neighbourhood CNFs express exactly the graph problem, and the archived
CaDiCaL/Kissat records cover all 403 degree-11 and all 8 degree-12 cases.

The correct qualification is essential: the 411 UNSAT outcomes have no
DRAT/LRAT (or other replayable) proof traces.  Thus
`maximum degree <= 10` is a strong two-solver computational conclusion, not a
formally replayed finite proof.

## Mathematical reduction

Let `C_d` be the isomorphism types of `d`-vertex graphs which are K4-free and
have no triangle-free seven-set.

If `G` is K5-free and every seven vertices of `G` contain a triangle, then for
every vertex `v`:

1. `G[N(v)]` is K4-free, since a K4 in the neighbourhood together with `v`
   would be a K5;
2. `G[N(v)]` has no triangle-free seven-set, because it is an induced subgraph
   of `G`.

Therefore a degree-`d` vertex has a neighbourhood in `C_d`.

For `H in C_d`, add a vertex whose neighbourhood in `H` is `A`.  The child is
in `C_(d+1)` if and only if:

1. `A` is triangle-free (otherwise the new vertex completes a K4); and
2. for each triangle-free six-set `S` of `H`, `A intersect S` contains an edge
   (otherwise `S` plus the new vertex is a triangle-free seven-set).

These conditions are both necessary and sufficient.  Also `|A| <= 6`, since
`A` itself is triangle-free and `H` has no triangle-free seven-set.  The two
defining properties are induced-hereditary, so every child deletes to a valid
parent.  Hence exhaustive one-vertex augmentation followed by canonical
deduplication is complete.

The independent checker rebuilt all downstream transitions:

```text
TRANSITION 9133->403 labelled=3989 canonical_bytes=PASS COMPLETE
TRANSITION 403->8    labelled=16   canonical_bytes=PASS COMPLETE
TRANSITION 8->0      labelled=0    canonical_bytes=PASS COMPLETE
```

The canonical outputs agree byte-for-byte with the frozen files.

## Direct census control

`direct_filter.c` is independent of the producer's recursive filter.  It
checks K4s by direct quadruple enumeration and covers the seven-sets with the
graph's triangle masks.  Piping the complete `nauty-geng` streams through it
gave:

| order | unlabeled inputs | valid outputs |
|---:|---:|---:|
| 7 | 1,044 | 578 |
| 8 | 12,346 | 3,128 |
| 9 | 274,668 | 11,005 |
| 10 | 12,005,168 | 9,133 |

The order-10 raw output SHA-256 was
`66c6eb718c18c48e3135254a8d8355a412ba7007c65c89e576c33d09dc688c6f`,
exactly matching frozen `direct_n10.g6`.  Canonicalising those 9,133 lines
gave the exact bytes and hash of `census_n10.g6`.  This independently anchors
the augmentation chain; the earlier orders are not needed for the conclusion.

## Fixed-neighbourhood CNF

The independent checker rebuilt the natural formula.  It has:

- 153 edge variables and 816 triangle variables, 969 total;
- 2,448 binary and 816 four-literal clauses encoding
  `t_ijk <-> (e_ij and e_ik and e_jk)`;
- 8,568 ten-literal clauses forbidding K5s;
- 31,824 35-literal clauses requiring a triangle in every seven-set.

Thus the unrestricted base has 43,656 clauses.  Fixing vertex 0 to have
neighbourhood `{1,...,d}` adds 17 units, and fixing the induced census
representative adds `C(d,2)` units:

| degree | cases | clauses per case |
|---:|---:|---:|
| 11 | 403 | 43,728 |
| 12 | 8 | 43,739 |

No maximum-degree condition is added.  Consequently, if a candidate graph
has even one degree-11 or degree-12 vertex, relabelling that vertex as 0 and
its neighbourhood to the appropriate census representative puts it in one
of these cases.  Empty `C_13` independently excludes every degree at least
13: any 13 selected neighbours would induce a member of `C_13`.  Eliminating
the 411 fixed cases therefore gives maximum degree at most 10, modulo their
UNSAT outcomes.

The independently generated base clauses agree literally with the frozen
checker, including variable numbering and clause order.

## Solver-record audit

The current raw records and consolidated tables agree case-for-case:

```text
D11 CaDiCaL: raw_cases=403 table_cases=403, each index 0..402 once,
             all UNSAT, conflicts=34,864,416, seconds=2307.669,
             slowest case 394 at 38.498 s
D11 Kissat:  raw_cases=403 table_cases=403, each index 0..402 once,
             all UNSAT, seconds=1621.060,
             slowest case 197 at 26.420 s
D12 CaDiCaL: cases 0..7 once, all UNSAT
D12 Kissat:  cases 0..7 once, all UNSAT
```

Every raw log's recorded neighbourhood edge count also matches the
corresponding graph6 representative.  The incomplete CaDiCaL shard tails are
completed by exactly ten single-case rerun logs; there are no gaps or
duplicates after combining them.

These are still solver assertions.  Running two independently implemented
CDCL engines makes a shared solver bug less likely, but it does not substitute
for checked UNSAT proof traces.

## Near miss

The mask file is symmetric, loop-free, and has no out-of-range bits.  Direct
subset enumeration gives:

```text
vertices               18
edges                   96
triangles               180
K4s                     99
K5s                     0
triangle-free 7-sets    9
clique number           4
degree sequence         10^6 11^12
automorphism group      12
```

There are 39 missing edges whose addition repairs at least one of the nine
bad seven-sets; each such addition creates between 3 and 6 K5s.  Hence the
reported minimum of three is correct.  I also reran the Hamming-ball SAT
queries at radii 1 through 7 with CaDiCaL; all returned UNSAT.  Those bounded
search results likewise lack proof traces.

The phrase “three overlapping clusters” in the original source report has no stated
clustering rule and is not independently auditable.  Under the natural
automorphism-group action the nine bad sets form two orbits, of sizes 6 and 3.
The phrase should be removed or precisely defined; it is not used anywhere in
the reduction.

## Source-packaging findings

1. `d12_census_sat.py` uses `sys.argv` without importing `sys`, so that
   auxiliary script fails when run standalone.  The generic
   `neighbourhood_census_sat.py` handles degree 12 correctly and is the command
   shown in the report's central reproduction recipe.
2. `MANIFEST.sha256` verifies all 18 entries it lists, including the
   consolidated degree-11 tables and both degree-12 logs.  It does not list
   the 30 raw degree-11 shard/single-case log files.  The raw logs currently
   match the manifest-bound consolidated tables exactly, but their individual
   bytes are not frozen by that manifest.
3. The order-7/8/9 direct files are not included in the frozen attack bundle.
   The independent full-generator rerun reproduced their stated counts, and
   completeness of the actual reduction is already anchored directly at
   order 10.

The versioned publication copy addresses the first two packaging points: it
omits the broken auxiliary degree-12 script in favour of the generic driver,
removes the undefined cluster sentence, and binds every raw log in its top-level
`SHA256SUMS`.

## Reproduction

```bash
cd verification/813/n18-degree10

python3 -u hostile_audit/audit_813.py

cc -O3 -std=c11 -Wall -Wextra -pedantic hostile_audit/direct_filter.c -o direct_filter
nauty-geng -q 10 | ./direct_filter | sha256sum

# Optional: rerun all eight degree-12 cases and selected degree-11 cases
# with both archived solver backends.
python3 -u hostile_audit/audit_813.py --quick --rerun-sat
```

Recorded outputs are in `full_audit.log`, `direct_full.log`, and
`sat_rerun.log`.
