# Independent hostile audit 2: Erdos Problem 132

Input bundle: `../bundle_ro`

Input manifest SHA-256:
`4e2716c6aec0c0a50d1ffc64286559cccef3cdbc28c33e409a08a71d5965d4b7`

## Verdict

- **PASS (narrow):** the bundle correctly supports only this published result:
  every convexly positioned planar set of `n >= 5` points has a distance
  different from its diameter that occurs on at most `n` unordered pairs.
- **GAP / OPEN:** unrestricted Erdos Problem 132 for arbitrary planar point
  sets, and its growth question, remain open.  Nothing in this audit closes
  either question.
- **GAP (redistribution):** the input bundle contains third-party source bytes
  whose licenses do not all permit republication.  Do not copy the input
  `sources/`, source screenshots, or site snapshots into a public repository
  without separate clearance.  This second-audit bundle contains none of
  those bytes and is safe to copy as original audit material.

Read `AUDIT.md` for the proof audit and `SOURCE_LICENSE.md` for the packaging
restriction.  Replay the frozen checks with:

```bash
./reproduce.sh
```

The arithmetic/model checks and exact claim gate run when this directory is
copied alone.  Source-byte and snapshot checks run when the restricted sibling
`bundle_ro/` is present; the replay prints an explicit `SKIP` when it is not.
The locally frozen full-source replay used `--require-input --require-private`
and is recorded in `logs/independent_checks.log`.

The lean public package was independently audited at
`/home/exedev/erdos_scratch/erdos132_convex_public_20260811`.  Its final
manifest SHA-256 is
`9af6dabf0ffcf8d86ee3176c9bd7d875e18f9b341fda6e1aa126f04cfbd43db5`.
See `PUBLIC_PACKAGE_AUDIT.md` for the disposable-copy replay and mutation
tests.

No production/site file was edited, committed, or deployed by this audit.
