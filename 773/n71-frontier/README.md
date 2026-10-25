# Erdős #773: conditional exact value at 71

Run date: 2026-08-12 UTC.

## Precise result

Let `a(N)` be the largest number of indices that can be selected from
`{1,...,N}` while keeping all unordered sums `i^2+j^2`, including `i=j`,
distinct.  Conditional on the frozen previously certified exact values

```text
a(1),...,a(68) = the published A390813 prefix,
a(69) = 32,
a(70) = 33,
```

this bundle proves

```text
a(71) = 33.
```

The displayed 33-set is an unconditional lower-bound witness.  The upper
bound is a finite exhaustive computation whose precise dependency is the
frozen prefix file and the prior public `n69-frontier` bundle identified in
`DEPENDENCIES.md`.

## Why the reduction is complete

Assume a square-Sidon 34-set `S` exists in `[71]`.  Since the frozen premise
includes `a(70)=33`, `S` cannot lie in `[70]`; hence `71` belongs to `S`.
Removing `71` leaves exactly 33 indices to choose from `[70]`.

The C++ checker fixes `71` selected and assigns every one of the remaining
70 Boolean variables.  A support is the union of two different unordered
index pairs with equal square sum.  Direct reconstruction gives 764 distinct
forbidden supports at `N=71`: 23 triples and 741 quadruples.  A set is
square-Sidon if and only if it contains none of these supports.

The checker uses the frozen `a(k)` values only as upper bounds on an extension
remaining inside `[k]`.  It additionally uses selected-support blocking and a
clique cover of the current pair-conflict graph.  The soundness of those
rules is inherited from, and independently audited in, the prior public
bundle; `audit_definition.py` separately checks this instance from the raw
definition.

The assignments to `(x_70,x_69,x_68)` are partitioned by the prefix-free
cube list

```text
00, 010, 011, 100, 101, 110, 111.
```

Cube `00` covers both `000` and `001`; every other 3-bit assignment has its
unique listed prefix.  Every cube exits 20 and prints `UNSATISFIABLE`.
Together they visit 114,296,406 search states:

| cube | nodes | prefix prunes | blocked prunes | color calls | color prunes |
|---|---:|---:|---:|---:|---:|
| `00` | 2 | 1 | 0 | 1 | 0 |
| `010` | 2 | 1 | 0 | 1 | 0 |
| `011` | 2 | 1 | 0 | 1 | 0 |
| `100` | 14,391,515 | 457,087 | 2,832 | 13,931,596 | 6,276,915 |
| `101` | 40,004,795 | 1,143,913 | 9,389 | 38,851,493 | 17,652,449 |
| `110` | 26,162,953 | 695,538 | 2,924 | 25,464,491 | 11,493,240 |
| `111` | 33,737,137 | 759,347 | 4,826 | 32,972,964 | 14,974,799 |
| **total** | **114,296,406** | **3,055,888** | **19,971** | **111,220,547** | **50,397,403** |

Therefore no 34-set exists at 71, conditional on the exact prefix.

## Lower witness

The already certified `N=70` witness remains valid in `[71]`:

```text
1,4,6,7,9,10,12,13,16,18,19,22,24,28,30,34,36,37,39,40,43,46,
49,51,52,57,58,60,64,65,67,69,70
```

It has 33 indices and all 561 unordered square sums are different.

## Independent definition-level audit

`audit_definition.py` does not use the C++ support builder.  It compares all
unordered square pairs directly, reconstructs the 764 supports, checks the
561 witness sums, validates the live gate and dependency row structure, proves
that the seven cubes cover all top-three assignments once, and totals every
frozen counter.  Its output ends with:

```text
DEFINITION-LEVEL AUDIT PASS
```

## Hostile audit

A separately assigned hostile audit reconstructed the dependency chain,
reviewed every pruning and rollback rule, rebuilt the executable byte for
byte, and reran all seven cubes from source.  Every fresh process exited 20
and reproduced every deterministic node/prune counter.  It also found and
corrected two reproduction-wrapper defects: elapsed seconds are now removed
before comparing the regenerated summary, and a cube worker now fails unless
its solver exits exactly 20.  The corrected fast and full reproduction paths
both pass.  See `HOSTILE_AUDIT.md`.

## Live gate and novelty boundary

Bright Data rendered both the live problem and its discussion on 2026-08-12.
They showed status `OPEN`, `0 claimed proofs`, current worker `None`, and
interested collaborator `None`.  The live OEIS b-file still stopped at 68.

The prior local certificate already supplied `a(69)` and `a(70)`.  Thus this
run extends that local finite frontier by one position and the currently
displayed OEIS frontier by three positions.  That is only a dated search miss:
no claim is made that `a(71)=33` is absent from private computations or all
literature.  This finite theorem does not improve either asymptotic exponent
in Erdős Problem #773.

## Reproduction

```bash
./reproduce.sh
FULL=1 ./reproduce.sh
```

`SITE_INTEGRATION.patch` is a clean patch against the exact site commit named
in `DEPENDENCIES.md`.  This task made no repository edits.
