# Hostile audit of the lean public package

Audit date: 2026-08-11 UTC

Audited path:
`/home/exedev/erdos_scratch/erdos132_convex_public_20260811`

Final public-package manifest SHA-256:
`9af6dabf0ffcf8d86ee3176c9bd7d875e18f9b341fda6e1aa126f04cfbd43db5`

## Verdict

**PASS.**  The package states only the convex-position theorem: a set of
`n >= 5` points, all vertices of their convex hull, determines a distance
`d` with `0 < d < diameter` and multiplicity between 1 and `n`.  It expressly
leaves unrestricted Problem 132 and the growth question OPEN.

## Replay and mutations

A disposable tar/extract copy was byte-identical to the audited directory.
Its full `reproduce.sh` exited zero and reported:

```text
MANIFEST_PASS files=7
CONVEX_PROOF_PASS pair_counts=9996 regular_models=496 deleted_models=247 hexagon_vectors=2
TAMPER_TESTS_PASS rejected=4 weakened_pair_count=detected
PROBLEM 132 CONVEX-POSITION PACKAGE PASSED
```

The normal, `-O`, and `-OO` outputs agree.  Separate disposable mutations
confirmed rejection of a changed byte, added file, missing file, symlink,
FIFO, and unmanifested empty directory.  Replay created no bytecode or other
unmanifested artifact.

Independently of the package checker, all deletion positions were checked in
every deleted-vertex model for even `8 <= n <= 100` (2,585 models total), the
regular pentagon and both six-point vectors were rechecked, and the pair-count
formula was tested on four even/odd integers up to `10^50+1`.  The displayed
parity algebra in the report, rather than a finite loop, proves the all-`n`
count.

## Source and payload boundary

The source URLs, exact hashes, theorem/proof locators, Fishburn VOR page
locators, and license restrictions agree with the independently inspected
sources.  In particular, Fishburn's 29-page VOR has SHA-256
`b63a4ff8d00e4b2fcc7acc68924c0975ffc9d4a640ce7c1962f2781525053935`;
the classification is at PDF page 2 (journal page 66), the hexagons at PDF
page 3 (journal page 67), and the six-point analysis at PDF pages 5--7
(journal pages 69--71).

The public payload is eight ASCII files: seven files covered by the manifest
plus the manifest itself.  It has no subdirectory and no third-party PDF,
image, HTML/site snapshot, XML/JSON metadata capture, extracted article, TeX
source, source tar, or bytecode.  It is safe to copy as original audit
material.  This conclusion does not extend to `bundle_ro/`, its source/site
captures, or `private_source_cache/`.
