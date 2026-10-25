# Cold hostile audit: Erdos problem 222 finite frontier

Audit date: 2026-08-11 UTC.

Author bundle:
`/home/exedev/erdos_scratch/fresh6_erdos222_20260811`

## Verdict

**PASS**, with two non-claim-impacting output edge cases documented below.

The evidence supports this bounded exact statement:

1. `133858454292` and `133858454404` are consecutive sums of two squares.
   Their difference is 112, so the 111 strictly interior integers are not
   sums of two squares.
2. This is the first gap larger than the published difference-107 record.
3. No gap ending at or before the represented endpoint `200000000000` has
   difference greater than 112.
4. The only gaps of difference at least 108 through that endpoint are
   `112 133858454292 133858454404` and
   `108 190766104961 190766105069`.

This does not address the next finite record or the asymptotic problem.

## Cold recomputation

I compiled the author's primary source independently with GCC 13.3.0 at `-O2`
and ran one closed combined scan, rather than relying on the author's stitched
baseline/post-anchor summaries:

```text
range       0 .. 200000000000
chunk width 73456789
chunks      2723
threads     14
```

The width is different from all author runs.  The scan exited zero after
140.386 wall seconds and returned:

```text
REPRESENTED_COUNT 30700929089
FIRST 0
LAST 200000000000
MAX_GAP 112
MAX_GAP_LEFT 133858454292
MAX_GAP_RIGHT 133858454404
NONREPRESENTED_RUN 111
REPORTED_GAP_COUNT 2
GAP 112 133858454292 133858454404
GAP 108 190766104961 190766105069
```

The count also satisfies the independent overlap identity

```text
15563133098 + 15137795993 - 2 = 30700929089,
```

because the author's two closed scans overlap on the two represented endpoints
of the old 107-gap.  `verify_full_scan.py` checks all fields and this identity.

## Scanner audit

The primary implementation enumerates every reordered nonnegative pair
`0 <= a <= b` in each closed chunk.  Its floating square-root estimate is
corrected in both directions using 128-bit exact products.  Every generated
sum is marked in a packed bitmap, so multiple representations are counted
once.  Chunks are disjoint; aggregation carries the last mark across any
number of empty chunks, so cross-boundary gaps are not lost.

The author's independent implementation transposes the loops, uses `b` as the
outer coordinate, derives exact `a` bounds, stores one byte per integer, uses
static scheduling, and agrees with the primary full post-anchor run.

For a cold small-range check, `scanner_harness.py` classified integers through
one million by the prime-exponent two-square criterion.  Across 35 intervals
with represented endpoints (including width-1 chunks), 30 deterministic
random partitions, and an arbitrary-boundary case, both C++ scanners matched
the independent truth for unique counts, first/last values in the claimed
boundary regime, maximum gap and endpoints, and every threshold-reported gap.

## Direct 111-row certificate

`regenerate_certificate.gp` independently factors all 111 interior integers
with PARI.  For each it selects the least prime congruent to 3 modulo 4 having
odd exact valuation.  The regenerated file is byte-identical to the author's:

```text
f20240fe78cd69e57121288a7175e18cb4d9de2bf08475405084f4ed99540770
```

The author's Python Miller--Rabin/valuation checker and PARI checker were also
rerun cold and both pass.  Endpoint arithmetic passes:

```text
133858454292 = 49986^2 + 362436^2
133858454404 = 35298^2 + 364160^2
```

Thus the new gap itself is certified without trusting either scanner.

## Live, OEIS, and collision scope

The live problem page was refetched independently and is byte-identical to the
author snapshot.  It says OPEN, zero comments, zero claimed proofs, no current
worker, and links A256435.

Official b-files A256435, A297350, and A357018 were independently refetched and
are byte-identical to the author's snapshots.  A297350 describes starts of
record gaps and ends at `99951600293`; A357018 describes record-length interior
runs and ends at 106.  Hence the proposed extensions `133858454292` and 111
have the correct conventions.

Exact-endpoint web searches found no relevant indexed prior occurrence.  This
is only a search miss, not proof of priority.  Current site sources were also
rechecked after the author snapshot: no problem-222, sequence, endpoint, or
same-framework reference is present.

## Scoped observations

1. In the primary scanner, the displayed `FIRST` and `LAST` fields are read
   directly from the first and last chunks.  If either boundary chunk is
   entirely empty, those display fields can be zero even though a later/earlier
   chunk contains marks.  Count and gap aggregation remain correct.  All
   claimed scans have explicitly represented `LO` and `HI`, so this cannot
   affect the frozen claim.
2. In the independent scanner, `NONREPRESENTED_RUN` underflows to `2^64-1`
   when the entire global interval contains no represented value.  Its claimed
   range has over 15 billion represented values and represented endpoints, so
   this case is unreachable there.

These are robustness issues worth fixing before treating the executables as
general interval-reporting tools; neither changes the bounded theorem above.

## Integrity

The author's `MANIFEST.sha256` verifies completely and has SHA-256
`527f91bb0b9388cee3fabd49c0781d7292a8ebda720aba189469bcf158152622`.
This audit was written outside the author bundle and did not modify it.
