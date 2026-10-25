# Erdős #773 finite-frontier certificate

Run date: 2026-08-11 UTC.

## Precise result

Let `a(N)` be the maximum size of a set `I` contained in `{1,...,N}` for
which all unordered sums `i^2+j^2`, with `i,j` in `I` and `i<=j`, are
distinct.

**Conditional on every value in the published exact A390813 table through
68, this certificate proves**

```text
a(69) = 32 and a(70) = 33.
```

The size-32 witness at 69 and size-33 witness at 70 are unconditional lower
bounds.  The upper proof uses the full published prefix `a(1),...,a(68)`:
`a(68)=32` drives the first reduction, and the other values are prefix upper
bounds inside the search.  This bundle freezes that table but does not
independently re-prove it.

This is only a finite-frontier result.  It gives no improvement to the open
asymptotic question in Erdős problem #773.  The local Erdős Problem A Day
ledger already records a prior CODEX attempt on #773 dated 2026-07-25, so
this is not a first site attempt.  See `PROVENANCE.md` for the full scope and
source audit.

## Proof reduction

The frozen OEIS b-file has SHA-256

```text
dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916
```

and contains the published values `a(1),...,a(68)`, ending in `a(68)=32`.
If a valid 33-set existed at 69 without index 69, it would contradict that
input.  Thus a hypothetical 33-set must contain 69, leaving exactly 32
indices to choose from 1 through 68.

`dfs_hypergraph_coloring.cpp` reconstructs every collision of two unordered
square pairs.  There are 712 distinct forbidden supports: 21 triples and
691 quadruples.  A selected set is valid exactly when it contains no full
support.  The program fixes 69 as selected and exhaustively assigns indices
68 down to 1, using three sound upper bounds:

1. At a node with remaining prefix `1,...,k`, at most the published `a(k)`
   further indices can be chosen.
2. A candidate is blocked when all other vertices of a forbidden support
   have already been selected.
3. If exactly two unassigned vertices remain in a live support, those two
   candidates conflict.  Partitioning viable candidates into cliques of
   this conflict graph bounds a valid extension by the number of cliques.

The assignments to `(x_68,x_67,x_66)` are covered disjointly by these prefix
cubes:

```text
00, 010, 011, 100, 101, 110, 111
```

Cube `00` covers both `000` and `001`.  Every cube completed with exit code
20 (`UNSATISFIABLE`).  Together they visited 171,546,643 recursive nodes.
Therefore no valid 33-set containing 69 exists, and the unconditional
size-32 witness gives `a(69)=32`, conditional on the published prefix.

The frozen run counters are:

| cube | nodes | seconds | prefix prunes | blocked prunes | color calls | color prunes |
|---|---:|---:|---:|---:|---:|---:|
| `00` | 3 | 0.000045 | 1 | 0 | 2 | 0 |
| `010` | 19,911,189 | 57.0193 | 556,112 | 5,119 | 19,349,958 | 8,746,556 |
| `011` | 28,735,030 | 80.7858 | 655,227 | 4,392 | 28,075,411 | 12,703,186 |
| `100` | 23,960,293 | 65.8242 | 733,686 | 6,157 | 23,220,450 | 10,444,670 |
| `101` | 37,889,705 | 100.7600 | 1,008,817 | 9,074 | 36,871,814 | 16,490,069 |
| `110` | 30,478,167 | 83.8387 | 750,827 | 5,406 | 29,721,934 | 13,570,819 |
| `111` | 30,572,256 | 84.2968 | 551,088 | 2,590 | 30,018,578 | 13,696,070 |
| **total** | **171,546,643** | **472.5248 solver-seconds** | **4,255,758** | **32,738** | **167,258,147** | **75,651,370** |

Finally, deleting 70 from any set proves `a(70)<=a(69)+1=33`; the checked
size-33 witness at 70 proves equality under the same dependency.

## Witnesses

At `N=69`, these 32 indices produce 528 distinct unordered sums:

```text
3,4,6,12,13,15,17,19,23,25,28,34,35,38,42,45,48,49,53,54,56,57,58,60,61,62,63,64,65,66,68,69
```

At `N=70`, these 33 indices produce 561 distinct unordered sums:

```text
1,4,6,7,9,10,12,13,16,18,19,22,24,28,30,34,36,37,39,40,43,46,49,51,52,57,58,60,64,65,67,69,70
```

## Independent checks

`audit_dfs_certificate.py` verifies the b-file hash and rows, reconstructs
all collision supports, checks the cube cover and every completed log,
checks both witnesses directly, and rebuilds the optimized executable
byte-for-byte.  Its frozen output ends with:

```text
CERTIFIED conditional_on_frozen_A390813_prefix a69=32 a70=33
```

`audit_pair_bound.py` independently compares the support-derived pair graph
against direct square-sum incompatibility on 200 deterministic random DFS
states and checks the clique upper bound against 60 exact independence
computations.  A separately compiled `ERDOS773_AUDIT` build checked the
incremental block/pair invariants during 15 completed searches.
`crosscheck_dfs_variants.log` records agreement with the simpler reviewed
sum-based DFS on 30 deeper cubes.

Two hostile audits then started from the frozen package.  The first
independently fetched the live OEIS input, rebuilt the solver byte-for-byte,
reran all seven proof cubes with identical counters, checked a deep cube
under ASan and UBSan with extra state invariants, and reviewed every pruning
rule.  Its report is `HOSTILE_AUDIT_1.md`.  A second separately assigned
audit repeated the core reconstruction and fresh cube run before publication;
its report is `HOSTILE_AUDIT_2.md`.  Both returned PASS for the conditional
theorem.  `CHANGES_V2.md` records the non-mathematical documentation and
packaging corrections made after those audits, including a qualification to
the clique-cover routine's early-return comment.

## Verification

Run the fast frozen-artifact audit:

```bash
./reproduce.sh
```

Run `FULL=1 ./reproduce.sh` to rebuild the proof executable, rerun all seven
cube searches into a temporary directory, and audit those fresh logs too.
The frozen file hashes are listed in `SHA256SUMS`.
