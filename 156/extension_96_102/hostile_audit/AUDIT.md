# Hostile audit: Problem 156 finite frontier through 102

Date: 2026-08-11 UTC

## Verdict

**PASS, with no mathematical or implementation gap found.** The audited
artifacts prove

```text
a(n) = 7 for 68 <= n <= 101,
a(102) = 8.
```

This is an exhaustive finite computation, not a formalized proof. The only
remaining qualification is ordinary finite-code/compiler/hardware risk.

## Reduction audit

For a Sidon set `A`, direct insertion of `x` fails precisely when one of the
new distances `|x-a|` repeats an old positive difference or two new distances
coincide. The latter case is exactly an integral midpoint of two old marks.
This agrees with the old-pair-sum formulation. I exhaustively compared the
difference formula, sum formula, and full insertion predicate on all 139 Sidon
subsets of `{0,...,8}`, over 4,031 tested insertions; every result agreed.

Translation sends both the set and its blocked set by the same shift. Thus a
candidate in an `n`-point interval normalizes uniquely to a set with minimum
zero and maximum at most `n-1`. It can be maximal exactly when the consecutive
blocked component containing its hull has length at least `n` and can contain
an `n`-point interval around that hull. This validates both the normalization
and blocked-run reductions.

## Exhaustive results

I independently rebuilt and ran the production seven-mark engine through
maximum 105. It reproduced exactly:

```text
tasks=5050
endpoint_tests=860633378
golomb=516985552
hull_covered=455390
best_run=101
best_marks={0,24,27,35,39,41,75}
best_interval=[-17,83]
seven_mark_upper_bound_contiguous_through=101
```

I then wrote `hostile_audit_156_k7_direct.cpp`. It does not use a Sidon prefix
prune or the production blocked-set construction. It visits every one of the
`C(101,6)=1,267,339,920` full normalized seven-mark combinations, reconstructs
positive differences at each leaf, and tests insertions directly. Its frozen
output is `direct_enumeration.log`; it independently found:

```text
sidon=386623922
hull_covered=455390
best_run=101
best_marks={0,24,27,35,39,41,75}
best_interval=[-17,83]
seven_mark_upper_bound_contiguous_through=101
HOSTILE_DIRECT_ENUMERATION=PASS
```

At maximum mark 101, three size-at-most-six engines using incremental
differences, incremental pair sums, and unpruned leaf testing agreed on every
raw count, Sidon count, hull-covered count, extremizer, and best run. Their
size-six totals were `79,208,745` raw, `46,198,688` Sidon, `20,166`
hull-covered, and best run 67 at `{0,7,19,22,28,39}` on `[-15,51]`.

## Witnesses

Fresh direct replays confirmed every upper witness for `68 <= n <= 101`.
The claimed seven-mark extremizer is Sidon and its blocked component is exactly
`[-17,83]`: both neighboring points `-18` and `84` are insertable. The
eight-mark set

```text
{10,33,38,42,59,69,71,89}
```

has 28 distinct positive differences and rejects all 94 outside points of
`{1,...,102}`. Its blocked component is `[0,110]` before normalization.

## Bounds and concurrency

For the required maximum 101, every shift into an `unsigned __int128` is in
`1..101`. In the auxiliary maximum-105 run it is in `1..105`; both are below
128. Production blocked coordinates lie in `[-L,2L]`, and the arrays include
the two sentinels `-L-1` and `2L+1`. The direct size-six insertion bitset may
test distances through 203 and has 305 bits. All counters are far below
`uint64_t` capacity, and recursion depths and signed coordinates are small.

The OpenMP task list is immutable. Search state is task-local, counters are
atomic, best-record writes hold one mutex, and the implicit loop barrier
precedes all main-thread reads. Tie-breaking is deterministic. GCC
ThreadSanitizer with `libgomp` emitted an apparent task-vector/stack race across
that implicit barrier, so TSan is not usable as clean evidence in this runtime;
the report's concurrency conclusion rests on this synchronization audit and
matching exact runs under different schedules.

Full ASan/UBSan runs passed for all three size-at-most-six engines and for the
complete maximum-101 seven-mark production enumeration. Strict warning builds
also passed. No source in `ErdosProblemADay` was edited by this audit.

One pre-freeze editorial sentence needed clarification: base differences in
the 128-bit masks are at most 101, but the direct insertion auditor can test
distances up to 203 in its larger bitset. This does not affect safety or the
result.
