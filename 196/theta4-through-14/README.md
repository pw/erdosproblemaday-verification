# Problem 196: exact finite monotone 4-AP counts

This package certifies the exact values

```text
theta_4(13) =   949,812,334
theta_4(14) = 9,471,574,188
```

where `theta_4(n)` counts permutations of `[n]` containing no four values in
arithmetic progression in increasing or decreasing positional order.

The author computation also reproduces the full exact table through `n=14`.
Goh and Zhao's peer-reviewed 2021 paper publishes the equivalent distribution
through `n=10`, and the public arXiv v2 table includes `n=11,12`. Accordingly,
only the `n=13,14` rows are described as search-limited not-found extensions.
This is not a claim of absolute priority.

The computational result has three exact implementations:

- the author endpoint recursion with complement symmetry;
- a hostile-audit subsequence automaton with no endpoint or complement
  reduction;
- a maximum-insertion recursion with a different search tree.

All three agree through `n=14`. Direct permutation checks, sanitizer builds,
thread-count controls, an AP-incidence identity, and a parser for the prior
Goh-Zhao table provide additional checks.

The immutable author manifest also names two prepublication site snapshots.
Those files are deliberately omitted here because one contains concurrent,
uncommitted ledger work unrelated to Problem 196. The root reproducer verifies
every included author artifact after filtering exactly those two paths. Their
names, sizes, and hashes remain recorded in `hostile_audit/REPORT.md`.

Run `./reproduce.sh` for manifest, strict-build, frozen-log, literature-table,
and small exact checks. Set `FULL=1` to recompute all three searches through
`n=14`; the no-symmetry audit is the slow stage.

This finite enumeration does not advance the infinite problem. A known
doubly-infinite avoiding order already gives finite avoiders for every `n`;
the unresolved issue is obtaining an order of type omega, equivalently
controlling predecessor sets in a singly infinite permutation.
