# Hostile audit of the frozen Problem 196 finite-count bundle

Audit date: 2026-08-11 UTC.

Input bundle (left byte-for-byte unchanged):

`/home/exedev/erdos_scratch/fresh9_erdos196_20260811/bundle_ro`

## Verdict

- **PASS, computational core:** the exact values of `theta_4(n)` through `n=14` were reproduced by
  the author program and by two structurally different C++ enumerators. The no-symmetry
  subsequence automaton and the maximum-insertion recursion both reached `n=14`.
- **GAP, frozen publication narrative:** Goh-Zhao's 2021 journal paper publishes the equivalent
  distribution through `n=10`, and its public arXiv v1/v2 table includes `n=11,12`. Therefore only
  `n=13,14` are search-limited exact-table extensions. The frozen report's literature paragraph is
  superseded and must not be published unchanged.
- **No infinite result:** the finite table does not advance the order-type obstruction in Erdos
  Problem 196.

The complete reasoning, exact scope, hashes, and caveats are in `REPORT.md`.

## Reproduction

Fast integrity/build/log verification on the audited VM:

```bash
./reproduce.sh check
```

Full recomputation, including the roughly 12-minute no-symmetry `n=14` run:

```bash
./reproduce.sh full
```

`MANIFEST.sha256` covers every frozen audit artifact except itself. The two large author-bundle
site snapshots are recorded in the report but are non-load-bearing and should be omitted from any
public copy.
