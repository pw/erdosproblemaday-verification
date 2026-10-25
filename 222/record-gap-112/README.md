# Problem 222: record gap 112 between sums of two squares

This directory certifies the bounded exact statement that the next record gap
after the published difference-107 record is

```text
133858454292 .. 133858454404
```

The endpoints are consecutive sums of two squares. Their difference is 112,
so the 111 interior integers are not representable. The gap is the first new
record and remains maximal through the represented endpoint
`200000000000`.

- `author/` contains the baseline scan, three post-anchor scans using two
  implementations, a direct 111-row factor obstruction, sources, logs, and
  provenance. Its manifest hash is
  `527f91bb0b9388cee3fabd49c0781d7292a8ebda720aba189469bcf158152622`.
- `hostile_audit/` contains a fresh combined scan from zero with a fourth
  chunk geometry, independent factor-certificate regeneration, boundary
  tests, current-source checks, and the audit verdict. Its manifest hash is
  `d2bcfd35f48d701daec2d3bb057ccb0f81fc132603a1fbc50cadc3338e57ab30`.

The immutable author manifest also names two prepublication site snapshots.
Those copies are deliberately omitted here because one captured concurrent,
uncommitted site work unrelated to Problem 222. The root reproducer verifies
the original manifest identity and every included author artifact after
filtering exactly those two snapshot paths. The mathematical certificate and
both scanner sources are unaffected.

Run `./reproduce.sh` for manifest, certificate, frozen-output, and small-range
scanner checks. Set `FULL=1` to recompute the complete frontier through
200 billion and compare its output byte-for-byte with the hostile audit.

This is a finite computational extension. It does not improve the asymptotic
bounds in Erdos Problem 222 or claim anything beyond the stated endpoint.
