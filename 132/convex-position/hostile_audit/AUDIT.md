# Independent hostile audit

Audit date: 2026-08-11 UTC

## Disposition

**PASS only for the exact convex-position theorem in `CLAIM.txt`.**

**GAP / OPEN for full Problem 132.**  The evidence does not prove the result
for arbitrary planar point sets and says nothing about whether the number of
distances of multiplicity at most `n` tends to infinity.  The current live
record remains `OPEN`; informal small-order claims in its discussion thread
were not used.

The input bundle is mathematically sound at grade **rigorous modulo the named
Altman--Fishburn classification**.  No independent new proof of that deep
classification is claimed.  Its consequences and every boundary case used by
the short deduction were rebuilt independently below.

## Frozen-input integrity

The requested `bundle_ro/MANIFEST.sha256` has SHA-256

`4e2716c6aec0c0a50d1ffc64286559cccef3cdbc28c33e409a08a71d5965d4b7`.

Every one of its 45 entries verifies.  The sibling archive has SHA-256

`a738c216386c79d09ab3fb77bb7feb69168d9ceca6a8a853c99d79e90f8736a1`,

matches its checksum file, extracts byte-for-byte to the frozen tree, and
preserves the read-only modes.  The supplied `reproduce.sh` also completed
with `FULL BUNDLE REPLAY PASSED`.

## Primary-source reconstruction

For a finite set `A`, let `mu_A(d)` be the number of unordered pairs at
distance `d`, and let `m(A)` be the number of distinct positive distances.

The load-bearing published paper is F. C. Clemen, A. Dumitrescu, and D. Liu,
*On multiplicities of interpoint distances*, Acta Mathematica Hungarica 177
(2025), 231--245, DOI `10.1007/s10474-025-01562-y`.  Its Version of Record
Theorem 1.2 (PDF p. 3, journal p. 233) states exactly the claim in `CLAIM.txt`;
its proof is on PDF p. 6, journal p. 236.  The official arXiv v5 source states
the same theorem and proof at frozen TeX lines 199--203 and 371--394.

The equality input was independently checked against Peter Fishburn,
*Convex polygons with few intervertex distances*, Computational Geometry 5
(1995), 65--93, DOI `10.1016/0925-7721(94)00020-V`.  The complete 29-page
publisher VOR was inspected, not merely its abstract:

- journal p. 66, Theorem 1, states Altman's lower bound
  `m(A) >= floor(n/2)` and the unique regular-polygon equality case for odd
  `n`;
- journal p. 66, Theorem 2, gives exactly `R_n` and `R_(n+1)` with one vertex
  removed for even `n >= 8`;
- journal p. 67, Figure 1, displays all three six-point equality polygons and
  labels their vectors `(6,6,3)`, `(6,6,3)`, and `(5,5,5)`;
- journal pp. 69--71 prove the six-point classification, and Section 3 proves
  the larger even case.

The independently acquired VOR has 1,798,795 bytes and SHA-256
`b63a4ff8d00e4b2fcc7acc68924c0975ffc9d4a640ce7c1962f2781525053935`.
It is kept outside this audit archive under the restrictions documented in
`SOURCE_LICENSE.md`.

Altman 1972, Theorem 3 (journal pp. 338--340), independently supplies the
lower bound.  The full internal pages of Altman 1963 were not available
without subscription; for the odd equality classification this audit relies
on Fishburn's explicit Theorem 1 and the 2025 VOR's direct attribution.  This
is why the grade remains "modulo named published classification."

## Deduction

Let `m=m(A)`.  If `m > floor(n/2)`, then there are at least `floor(n/2)`
non-diameter distance classes.  If every one occurred more than `n` times,
integer multiplicity would give

`C(n,2) >= floor(n/2)(n+1)+1`.

For `n=2k` the right side minus `C(n,2)` is `2k+1=n+1`; for `n=2k+1` it is
`k+1=(n+1)/2`.  Both are positive.  This branch is impossible.

It remains to inspect `m=floor(n/2)`:

- Odd `n`: the classification gives a regular `n`-gon.  Cyclic steps
  `1,...,(n-1)/2` are distinct chord lengths and each has exactly `n` pairs.
  Since `n>=5`, a step smaller than the maximum exists and is a non-diameter
  witness.
- Even regular `n`: steps `1,...,n/2-1` each have `n` pairs, while the
  antipodal diameter has `n/2` pairs.  Any non-antipodal step is a witness.
- Even `n>=8`, deleted-vertex model: begin with the regular odd
  `(n+1)`-gon.  Every step class has `n+1` pairs.  Deleting one vertex removes
  exactly its two incident pairs from every step, leaving `n-1` pairs in each
  of the `n/2` classes.  The maximum step remains represented, and every
  smaller step is a non-diameter witness.
- `n=6`: each of the only two possible frequency vectors has three entries,
  sums to 15, and every entry is at most 6.  Whichever entry belongs to the
  diameter, both remaining distance classes satisfy the required bound.

## Boundary cases

For `n=5`, the strict-count branch would require at least
`2*6+1=13 > 10` pairs.  The equality branch is the regular pentagon with
vector `(5,5)`; its side length is the required non-diameter distance.

For `n=6`, the strict-count branch would require at least
`3*7+1=22 > 15` pairs.  The equality branch is handled by the primary-source
vectors above.  Thus no small-order case is silently delegated to an
asymptotic statement.

For all `n>=7`, the same parity identities prove the strict branch for every
integer `n`, while the odd, regular-even, and deleted-vertex classifications
exhaust equality.  The checker enumerates the combinatorial chord counts as a
diagnostic; the all-`n` proof is the displayed algebra, not a finite test.

## Hostile findings

1. **No mathematical defect found.**  The theorem, count, small cases, and
   equality-model multiplicities all survive independent reconstruction.
2. **Primary-source caveat repaired.**  The input bundle had not inspected
   Fishburn's internal hexagon page.  This audit did; it directly confirms
   both vector types and the existence of three geometric configurations.
3. **Redistribution gap.**  The input's third-party PDFs and extracted source
   text are not uniformly licensed for republication.  This does not affect
   mathematical correctness, but the input bundle itself must not be copied
   wholesale into a public repository.  See `SOURCE_LICENSE.md`.
4. **Snapshot qualification.**  The input site snapshots are valid for their
   recorded bytes, but `src/index.js` has changed since capture.  A fresh
   independent search of the current site tree still found no Problem 132
   object or defining-paper sentinel.  The audit records both hashes rather
   than calling the old snapshot current.

## Public-package hostile replay

The final public-safe package at
`/home/exedev/erdos_scratch/erdos132_convex_public_20260811` is anchored by
`MANIFEST.sha256` SHA-256
`9af6dabf0ffcf8d86ee3176c9bd7d875e18f9b341fda6e1aa126f04cfbd43db5`.
An archive/extract copy was byte-identical and completed the full normal,
`-O`, and `-OO` replay.  Independent mutations of a byte, an added or missing
file, a symlink, a FIFO, and an empty directory were all rejected.  An
independent model checker also covered all 2,585 deletion choices for even
`8 <= n <= 100` and four parity cases as large as `10^50+1`.

The payload consists only of eight ASCII files (seven manifested files plus
the manifest), has no subdirectory, and contains no PDF, image, page scrape,
publisher XML, TeX source, source tar, or Python bytecode.  It is suitable for
public copying as original audit prose and code.  The restricted sibling input
bundle and private Fishburn cache are not suitable for wholesale copying.

Final verdict: **PASS for `CLAIM.txt`; GAP/OPEN for unrestricted Problem 132
and its growth question; GAP for wholesale public redistribution of the input
source payload.**
