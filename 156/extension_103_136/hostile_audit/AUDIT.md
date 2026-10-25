# Hostile audit: Problem 156 finite frontier through 136

Date: 2026-08-11 UTC

## Verdict

**PASS. No mathematical, completeness, counter, bounds, concurrency, witness,
dependency, or scope gap was found.** The frozen target bundle proves the
finite computational statement

```text
a(n) = 8 for every 102 <= n <= 136,
```

and hence adds the new rows `a(103)=...=a(136)=8` beyond the site's prior
through-102 result. This does not resolve or improve the asymptotic problem.

The audited target is identified by

```text
SHA256SUMS  566ac359a544556f7453a1b02044692488ed91f0ad2eb4cc09ca24a1503ecd89
REPORT.md   d9576cc509c93b0330486960f806b2acb1d4c1f5d08e873e014e544a7a14a864
```

Its own manifest passed before and after every rerun.

## Reduction and normalization

If `A` is Sidon and `x` is not in `A`, all sums internal to `A` are already
distinct and all new sums are `2x` and `x+a`. The new sums are mutually
distinct unless `x` is an old mark. Thus insertion fails exactly when `2x` or
some `x+a` is an old unordered sum. This is precisely the target sum predicate
(`verify_size7_sums.cpp:66-75`). Equivalently, a new absolute difference either
repeats an old positive difference or repeats another new difference, which is
the target difference predicate (`verify_size7_differences_words.cpp:66-77`).

Translation preserves these collisions. A maximal nonempty `A` in `[1,n]`,
translated by `-min(A)`, has `0=r_1<...<r_k=L<=n-1`; its translated domain is
a blocked length-`n` interval containing `[0,L]`. Therefore its hull lies in a
blocked component of length at least `n`. Conversely, if `[lo,hi]` is such a
component, `hi-lo+1>=n`, and `L<=n-1`, an admissible domain left endpoint is

```text
d = max(lo, L-n+1).
```

It satisfies `lo<=d<=0` and `L<=d+n-1<=hi`, so translating `[d,d+n-1]` to
`[1,n]` gives a maximal set. The independent checker exercised this interval
construction on 6,794,725 boundary tuples (`independent_reduction_witness.py:
64-77`) and compared literal insertion, pair sums, and positive differences on
3,535 insertions (`:44-61`). The empty set is trivially nonmaximal for these
nonempty domains, so sizes one through seven are complete.

## Target enumeration audit

For seven marks, both target programs form every disjoint task `(L,r_2)` with
`6<=L<=135` and `1<=r_2<=L-5`, giving
`sum_{L=6}^{135}(L-5)=8,515` tasks
(`verify_size7_sums.cpp:135-160` and
`verify_size7_differences_words.cpp:144-167`). Their recursive upper limit
leaves exactly enough positions for the unchosen interior marks
(`verify_size7_sums.cpp:103-122`; difference version `:106-131`). A branch is
pruned only when an existing sum or difference collision has already occurred;
later marks cannot remove it (`verify_size7_sums.cpp:53-63`; difference version
`:54-63`). Each valid six-mark prefix attempts the fixed endpoint exactly once.

The pair-sum and three-word-difference reruns both reproduced:

```text
tasks=8515/8515
endpoint_tests=4664137760
sidon=3188523904
hull_covered=455390
best_run=101
best_marks={0,24,27,35,39,41,75}
best_interval=[-17,83]
```

The target hard-checks all of those values
(`verify_size7_sums.cpp:170-187` and difference version `:176-185`).

For sizes one through six, the parallel target enumerates every exact
`(size,L,first)` task and recurses over the remaining increasing marks
(`verify_size6_sums_parallel.cpp:151-193`). The sequential target instead
visits every subset containing zero with maximum at most 135
(`verify_size6_sums.cpp:102-113,138-162`). Both frozen outputs agree on every
Sidon, hull-covered, and best-run row. One minor assurance weakness in the
parallel target is that its exit condition does not hard-check the printed
endpoint-attempt rows (`verify_size6_sums_parallel.cpp:195-218`); the
independent audit below checks all six of those rows exactly.

## Independent exact enumeration

`independent_k7_byte.cpp` is a third full implementation. It partitions by
valid `(L,r_2,r_3)` prefixes, producing 370,370 tasks (`:189-216`), uses mutable
byte arrays rather than machine-word masks for collision state (`:16-20,
39-80`), and maintains an independently asserted unordered-sum table for
blocking (`:55-64,82-99`). It enumerates one orientation of each ruler under
reflection: equal first and last gaps would already repeat a difference, and
reflection swaps their strict order (`:138-150`). It counts every endpoint
attempt before that symmetry reduction, doubles the canonical full-ruler and
hull counts, and explicitly accumulates hull coverage for diameters 102 through
135 (`:218-245`). The exact output was:

```text
endpoint_attempts=4664137760
canonical_sidon=1594261952  full_sidon=3188523904
canonical_hull=227695       full_hull=455390
hull_with_length_102_135=0
best_run=101 best_marks={0,24,27,35,39,41,75} best_interval=[-17,83]
INDEPENDENT_BYTE_SYMMETRY_K7=PASS
```

`independent_kle6_byte.cpp` uses one prefix tree rooted at every candidate
three-mark prefix, not the target's separate size/diameter searches
(`:179-219`). Every attempted extension from a valid prefix is counted before
collision testing (`:135-149`), and reflection again halves only completed
Sidon-ruler evaluation. It independently reproduced every printed row,
including endpoint attempts:

```text
k  endpoint attempts  Sidon       hull  longest
1                 1          1        1        1
2               135        135        2        4
3             9,045      8,978        8       10
4           396,506    383,262       76       22
5        12,452,396 11,347,918    1,102       42
6       285,696,286 233,716,482   20,166       67
```

The exact comparisons and exit checks are at
`independent_kle6_byte.cpp:221-250`; the frozen output ends in
`INDEPENDENT_BYTE_SYMMETRY_KLE6=PASS`.

## Witnesses

The target ruler is `{0,39,47,51,52,61,67,101}`
(`verify_witness_102_136.py:7`). The target rebuilds all 36 unordered sums,
checks the exact blocked component `[-16,119]`, constructs all 35 translations,
and tests the domain (`:31-56`). The independent audit instead literally
rebuilds the sums of `A union {x}` for each outside `x`, without calling either
blocking formula (`independent_reduction_witness.py:18-26,80-101`). It found 36
distinct old sums, confirmed both neighboring points `-17` and `120` are
insertable, and rejected all 3,885 outside insertions across every
`102<=n<=136`. Thus all 35 upper certificates are valid.

## Bounds and concurrency

- Differences inserted by either target search are in `1..135`; the difference
  engine allocates `135/64+1=3` words (`verify_size7_differences_words.cpp:
  14-20,43-52`).
- Old sums are in `0..270`; both sum engines allocate
  `270/64+1=5` words and range-check every probe before indexing
  (`verify_size7_sums.cpp:13-19,42-50`; size-at-most-six version `:13-16,
  39-48`).
- Every blocked integer has the form `s-a`, `s/2`, or an old mark, so it lies in
  `[-L,2L]`. The expansion loops therefore stop by the probes `-L-1` and
  `2L+1`; all signed arithmetic remains below 542 in magnitude. The sequential
  arrays explicitly include those sentinels (`verify_size6_sums.cpp:18-21,
  61-86`).
- The largest reported counter is 4,664,137,760, far below `uint64_t` capacity.
  All target local and atomic counters use `uint64_t` (`verify_size7_sums.cpp:
  21-38`; difference version `:22-39`).
- Task vectors are immutable during OpenMP loops; recursive marks and masks are
  task-local; totals are atomic; best updates hold a mutex; and the implicit
  loop barrier precedes reads (`verify_size7_sums.cpp:35-40,143-168`; difference
  version `:36-41,152-175`). No race was found. The independent implementations
  use thread-local totals and merge them only in an OpenMP critical section.
- The frozen max-110 ASan/UBSan target run passed. The max-135 source crosses
  the 128-bit boundary only by increasing the statically sized word arrays; the
  index analysis above covers that changed boundary.

## Prior dependency and scope

The prior bundle `ErdosProblemADay/verification/156/extension_96_102` and its
separate hostile-audit manifest both pass. Its report proves `a(102)=8`
(`erdos156_A382397_exact_96_102_2026-08-11.md:66-89`), and the current site
states the same at `src/index.js:4856-4911`. The new target actually re-proves
the lower and upper bound at 102, so the mathematical theorem does not depend
on trusting that prior computation; the dependency is only the accurate claim
that rows 103 through 136 are new relative to the site.

OEIS A382397 was opened live on 2026-08-11 and still displayed terms only
through `n=65`. Its definition by distinct positive differences is equivalent
to distinct unordered sums including diagonal sums. This audit makes no
literature-novelty claim beyond the finite extension and no statement about the
open `O(n^(1/3))` asymptotic problem. The random search source is explicitly
non-load-bearing and was not treated as proof.

## Reproduction

Run `./reproduce.sh`. It verifies both frozen target digests and manifests,
compiles the two independent exact enumerators with strict warnings, compares
their full outputs, reruns the literal witness/reduction checker, reruns both
target max-135 seven-mark engines plus its default smaller-size checks, and
verifies the prior-through-102 manifests. Remaining risk is ordinary
finite-code/compiler/hardware risk, not an identified proof gap.
