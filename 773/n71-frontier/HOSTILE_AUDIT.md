# Hostile audit: Erdős problem 773 at N=71

Audit date: 2026-08-12 UTC.

## Verdict

**PUBLISH the corrected bundle for the stated conditional theorem.**

Conditional on the published A390813 upper bounds through 68 and the prior
conditional certificates `a(69)=32`, `a(70)=33`, the exhaustive computation
proves `a(71)=33`.  The size-33 witness is an unconditional lower bound.  No
unconditional upper bound at 71, asymptotic advance, or absolute novelty claim
is established.

The originally frozen candidate had a reproduction-packaging blocker, not a
mathematical defect: `FULL=1 ./reproduce.sh` compared nondeterministic elapsed
seconds and therefore failed after a correct fresh run, while `run_cubes.sh`
did not propagate a non-20 child status.  Both wrappers are corrected in this
authoritative bundle, whose fast and full reproduction paths pass.

## Dependency audit

The claimed dependency is exact and noncircular.

- Rows 1 through 68 of `prefix_bounds_through_70.txt` are byte-identical to
  the data rows in the public `verification/773/n69-frontier` OEIS file.
- The base bundle's manifest and all of its listed files verify.  Its
  load-bearing manifest, README, solver source, and OEIS hashes agree with
  `DEPENDENCIES.md`.
- That base bundle conditionally proves `a(69)=32`; the direct size-33 witness
  at 70 plus `a(N+1) <= a(N)+1` then gives `a(70)=33` under the same premise.
- Therefore a hypothetical 34-set in `[71]` must contain 71.  Removing 71
  leaves exactly 33 lower indices, which is precisely the frozen search target.

At a recursive prefix `[k]`, the remaining selected indices alone form a
square-Sidon set, so the assumed `a(k)` is a valid extension upper bound even
after arbitrary higher indices have been fixed.  Thus all prefix prunes are
sound under the stated dependency.

## Model and search audit

An independent direct comparison of every two normalized unordered square
pairs reconstructs 764 distinct forbidden supports at 71: 23 triples and 741
quadruples.  A chosen set is square-Sidon exactly when it contains none of
these supports.  All arithmetic is integral and far below overflow.

The include branch maintains reference-counted one-vertex blocks and
two-vertex conflicts for every live support and reverses each transition in
the opposite order.  On an exclusion, a retained stale constraint necessarily
contains the just-excluded vertex, which lies outside the next prefix, so it
cannot cause an unsound lower-prefix prune.  The greedy conflict routine
constructs disjoint cliques; a valid extension takes at most one vertex per
clique.  Its early return occurs only once the part count reaches the needed
size, where the caller declines to prune.

The prefix-free cubes

```text
00, 010, 011, 100, 101, 110, 111
```

cover every assignment to `(x_70,x_69,x_68)` exactly once; `00` covers both
`000` and `001`.  Every frozen status is exactly 20 and every log says
`UNSATISFIABLE`.

The displayed 33-set was rechecked directly.  It contains 33 distinct indices
in `[71]`, and its 561 unordered integer square sums are all distinct.

## Fresh execution

- Every hash in the submitted manifest verified.
- The optimized executable rebuilt byte-for-byte from `dfs_n71.cpp`.
- The definition-level Python audit independently reproduced all support and
  witness counts, the exact cube cover, and the published counter totals.
- A fresh complete seven-cube run visited the same 114,296,406 states.  Every
  process again exited 20, and every deterministic node, prefix-prune,
  blocked-prune, color-call, and color-prune counter matched its frozen value.
- After correcting the two wrapper defects below, both `./reproduce.sh` and
  `FULL=1 ./reproduce.sh` completed with `REPRODUCTION PASS` and exit 0.

## Corrections made before publication

1. `reproduce.sh` now removes the nondeterministic `seconds=` field from both
   regenerated summary streams before diffing them.
2. Each `run_cubes.sh` worker now succeeds only when its solver exit status is
   exactly 20, so the parent script propagates SAT, crash, and input failures.
3. `audit_definition.py` now checks that dependency indices are exactly
   `1,...,70`, and its stale reference to an optional CaDiCaL proof was removed.
4. The site patch now says the definition audit totals and checks the recorded
   counters, and separately records the hostile fresh seven-cube replay.

## Site integration

The dependency site commit `422d5f768c80dca1911d0c9fe8e3eb2197f10b62`
is an ancestor of the audited current site HEAD
`97eadf8ee563489ea8b985b919d6159e620e43eb`.  Despite intervening commits,
the current `src/index.js` blob is still the patch base blob
`105b5faccbdfde00094fa6639d544a5d6d799d79`, and
`git apply --check SITE_INTEGRATION.patch` passes at current HEAD.

The publication must retain the word **conditional** wherever the exact upper
result is summarized.  Only the displayed size-33 witness is unconditional.
