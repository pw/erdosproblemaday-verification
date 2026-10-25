# Problem 1117: maximum-modulus points

This package supports two narrowly scoped partial results:

1. Pardo-Simon and Sixsmith, arXiv:2607.09462v1, construct a finite-order
   entire function in class B for which the number of maximum-modulus points
   is unbounded along selected radii.
2. If the nonzero exponents of a non-monomial polynomial run from `m` to `d`,
   then every positive circle has at most `d-m` maximum-modulus points. This
   is sharp for binomials.

Problem 1117 remains open in its liminf form. The 2026 paper is an arXiv v1
preprint, and no novelty claim is made for the elementary polynomial bound.

The frozen author bundle is under `author/`; the independent hostile audit is
under `hostile_audit/`. Two non-load-bearing author files were deliberately
omitted from this public copy:

```text
author/sources/site_index_20260811.js
author/sources/site_ledger_data_20260811.js
```

The second file captured a user-dirty worktree and must not be published. The
original manifest and exact hashes are retained. `reproduce.sh` verifies every
other author artifact, the complete hostile-audit bundle, the live/source
quantifiers, and both independent polynomial checkers.

Run:

```bash
./reproduce.sh
```
