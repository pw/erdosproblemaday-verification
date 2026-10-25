# Hostile audit: Erdos problem 773 finite frontier

Audit date: 2026-08-11 UTC.

## Verdict

**PASS for the stated conditional result**

> Conditional on every exact value in the published OEIS A390813 table
> through `a(68)=32`, the certificate establishes `a(69)=32` and
> `a(70)=33`.

This is a finite-frontier result only. It does not advance the asymptotic
question in problem 773.

## External premise

The live OEIS b-file was fetched independently on 2026-08-11 and compared
byte-for-byte with the frozen input. Both have SHA-256

```text
dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916
```

They contain exactly rows 1 through 68 and end in `67 32`, `68 32`. The
live OEIS entry defines the same square-Sidon extremal function, labels its
table `n=1..68`, and credits the values through 68 to Christian Sievers.
The earlier OEIS computations were treated as an external premise, not
independently proved here.

## Logical audit

1. Directly grouping all unordered pairs `(i,j)`, `1 <= i <= j <= 69`, by
   `i^2+j^2` gives 712 distinct collision supports: 21 of size 3 and 691 of
   size 4. A set is square-Sidon exactly when it contains no complete
   support.
2. A hypothetical 33-set at 69 not containing 69 would contradict
   `a(68)=32`. The remaining case fixes 69 and asks for 32 indices from
   1 through 68.
3. At a DFS node, selected lower-prefix vertices alone form a square-Sidon
   set, so the published `a(k)` is a valid extension bound. A live support
   with one remaining vertex blocks it. A live support with two remaining
   vertices makes that pair incompatible.
4. The pair graph is used soundly. Every valid extension is independent in
   it. The greedy routine constructs disjoint conflict cliques; a complete
   clique partition of size `q` bounds an extension by `q`. Its early return
   occurs only after `q >= needed`, where the caller does not prune.
5. The incremental selected/excluded, block, and pair state transitions
   are reversible. On an exclusion, a retained stale constraint necessarily
   contains the newly processed vertex, so it is outside the next prefix.
6. The prefix cubes `00,010,011,100,101,110,111` are prefix-free and cover
   every assignment to `(x_68,x_67,x_66)` exactly once.
7. The size-32 witness at 69 has all 528 unordered sums distinct. The
   size-33 witness at 70 has all 561 unordered sums distinct. Deleting 70
   proves `a(70) <= a(69)+1`, completing the conditional deduction.

No quantifier, model, cube-cover, or pruning gap was found.

## Reproduction

- All 38 hashes in the immutable manifest verified.
- The archive expanded byte-for-byte to the immutable directory.
- The fast `reproduce.sh` audit passed.
- A fresh optimized rebuild was byte-identical to the frozen executable.
- A separate fresh run of all seven cubes returned exit 20 and exactly the
  frozen node/prune counters, totaling 171,546,643 nodes.
- An ASan+UBSan build with `ERDOS773_AUDIT` completed a 14,474-node deep
  cube with no sanitizer or incremental-state invariant failure.
- A separate one-worker CP-SAT counterexample probe generated directly
  from the definition found no counterexample in 180 seconds. It ended
  `UNKNOWN` after 3,361,879 branches and 3,247,398 conflicts, so this is not
  counted as a proof.

## Artifact caveats

1. The immutable README refers to `audit_model.py`, but the immutable
   38-file bundle contains only `audit_model.log`. That auxiliary audit is
   therefore not reproducible from the bundle alone. This does not affect
   the main DFS proof or its included rebuild/checker.
2. The upper proof depends on the full published exact prefix table
   `a(1),...,a(68)`, because the DFS uses `a(k)` at every prefix. It should
   not be described as depending only on the single value `a(68)=32`.

## Principal hashes

```text
archive       6cc935660bc809462f8dcd97d6ae3b7fbe4662b8edaca4644e167e5fe98377fa
manifest      26147bd46934590c0a3c34e7aa1650c6c4c5ab43fb9d4e1e70192c107cf81816
OEIS b-file   dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916
DFS source    eb21d0f429881f61dd5148ab2a41da3fb6b57d1513ea2db656ae3ae69883e933
DFS binary    e9d471fb6df395f0807c21efc2fffbda64403511cd92b8098bb9100eaaa5655a
probe source  99525c51a8f13caa0ce601f74d972be4f4bf3d7faf6a4f5acfbef31427eaa1b7
probe result  9defcca2de4910d43cacd5cc73a3d347fbcc856f4239d499fe38b4e026a2b6bf
```
