# Provenance

All network access and computation occurred on 2026-08-11 UTC.

## Problem state

- Live problem: <https://www.erdosproblems.com/1160>
- Live discussion: <https://www.erdosproblems.com/forum/discuss/1160>
- Frozen rendered text: `live_problem_1160_20260811.txt` and
  `live_discussion_1160_20260811.txt`

The discussion URL redirected to `/forum/thread/1160`. The snapshots were
captured in a Bright Data browser because the site is bot protected.

## Count table

- OEIS record: <https://oeis.org/A000001>
- B-file: <https://oeis.org/A000001/b000001.txt>
- Frozen files: `live_oeis_A000001_20260811.txt` and
  `b000001_20260811.txt`
- B-file SHA-256:
  `54358f9bf5875f13f2e56c89f55c5942f868cc96f7a7fa653e2b133d1ad5a0f3`

The live OEIS record says that the b-file covers indices 0 through 2047 and
that `a(1024)` was corrected on 2022-01-06.

## Mathematical sources

1. John H. Conway, Heiko Dietrich, and E. A. O'Brien, "Counting groups:
   gnus, moas and other exotica," Mathematical Intelligencer 30 (2008).
   Author-hosted PDF:
   <https://www.math.auckland.ac.nz/~obrien/research/gnu.pdf>

   Frozen PDF SHA-256:
   `a9b5b755414846b4269d5022b2df8f69633f43110517aac7b3c00651e5bfb480`

2. David Burrell, "Computation of finite groups," PhD dissertation,
   University of Florida (2022), Chapter 3. Official repository PDF:
   <https://ufdcimages.uflib.ufl.edu/UF/E0/05/97/47/00001/Burrell_D.pdf>

   Frozen PDF SHA-256:
   `b74dad8fef62868518a6919ac61f3ba81f93b0a31c88bbbd02cecef1878f6c2a`

   The corresponding journal result is David Burrell, "On the number of
   groups of order 1024," Communications in Algebra 50 (2022), 2408-2410,
   DOI <https://doi.org/10.1080/00927872.2021.2006680>.

   Caveat: the dissertation's printed Table 3-3 margins have opposing
   one-unit inconsistencies. The bundle relies on Theorem 3.2.1 and the
   explicit correction narrative, not those marginal totals.

3. Bettina Eick, "Classification of Finite Groups: Recent Developments and
   Open Problems," Foundations of Computational Mathematics (2024), DOI
   <https://doi.org/10.1007/s10208-024-09688-1>. Repository PDF:
   <https://d-nb.info/1354828763/34>

   Frozen PDF SHA-256:
   `93df98d88572734978d7e1c3b5f5669c1eabb50d7f999e120ed577f34109223e`

The `.txt` companions were produced locally with Poppler `pdftotext -layout`.
They make the cited constants machine-checkable; the PDFs are the controlling
source artifacts.

## GAP audit

The five `.deb` files in `debs/` are unmodified Ubuntu packages for GAP
4.12.1, GapDoc 1.6.6, and SmallGrp 1.5.3. Their exact names, versions,
architectures, and hashes are recorded in `PACKAGE_METADATA.txt` and
`SHA256SUMS`. No system package was installed. `reproduce.sh` extracts them
into a temporary directory.

## Targeted search record

The frozen rendered Google result pages correspond to these exact queries:

```text
"49910538480" "2048" groups
"Question 22.18" "m=11" groups
"sum" "g(2048)" "groups of order"
```

The first and second produced no exact-query result; the third produced only
an unrelated data-aggregation result. These searches supplement, but do not
replace, the live-page gate and source audit.

## Local-site gate

The source snapshots came from `/home/exedev/ErdosProblemADay/src/index.js`
and `src/ledger_data.js`. The working tree was dirty from concurrent work on
other problems; no file in that repository was changed for this result.
`SITE_SNAPSHOT.txt` records the snapshot hashes, Git state, exact token rule,
and upstream problem-data commit.

## Hostile audit

A separate agent independently audited the frozen v1 result rather than
importing either supplied Python verifier. It parsed all 2047 positive-order
cells from the 2008 appendix, found the expected sole stale cell at 1024,
used GAP 4.14/SmallGrp 1.5.4 for 2043 cells, and checked the remaining four
against the appendix. It also checked the current OEIS file, source semantics,
live problem/LaTeX/forum state, and local source-token gate. Its mathematical
verdict was PASS. The v1 cosmetic output error it identified is corrected in
this v2 bundle; the arithmetic assertions and report claim were already in
the correct direction.
