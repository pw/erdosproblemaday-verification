# Problem 156 finite frontier: exact A382397 values through 136

Date: 2026-08-11 UTC

## Verdict

Let `a(n)` be the minimum size of a maximal Sidon subset of
`{1,...,n}`, with unordered sums including diagonal sums. This bundle proves

```text
a(n) = 8 for every 102 <= n <= 136.
```

The previously published bundle proved the result only at `n=102`. Thus the
new exact rows are `a(103)=...=a(136)=8`. This is a finite computational
extension of OEIS A382397 associated with Erdos Problem 156. It does not
improve the asymptotic bounds or resolve the parent problem.

## Blocking reduction

For a Sidon set `A`, adjoining an integer `x` fails precisely when one of the
new unordered sums `x+a` or `2x` equals an old unordered pair sum. If `B(A)`
is the set of such blocked integers together with `A`, then `A` is maximal on
an integer interval exactly when that interval is contained in `B(A)`.

Translate a candidate so that its least mark is zero. Translation preserves
the Sidon property and translates `B(A)` by the same amount. A `k`-mark
candidate maximal in `{1,...,n}` therefore becomes a normalized ruler

```text
0 = r_1 < r_2 < ... < r_k = L <= n-1
```

whose blocked component containing `[0,L]` has length at least `n`.
Conversely, any such blocked interval translates back to a maximal set.

## Complete lower bound

For `102 <= n <= 136`, every normalized candidate has `L <= 135`. Four
complete runs cover every candidate with at most seven marks in that range.

The sizes-one-through-six pair-sum enumeration reports:

| marks | Sidon rulers | hull-covered | longest blocked run |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 135 | 2 | 4 |
| 3 | 8,978 | 8 | 10 |
| 4 | 383,262 | 76 | 22 |
| 5 | 11,347,918 | 1,102 | 42 |
| 6 | 233,716,482 | 20,166 | 67 |

Both a direct sequential recursion and a separately written OpenMP task
enumerator reproduce those values. The hull-covered counts and extremizers
are unchanged from the previously hostile-audited max-101 computation, so
no newly admitted diameter contributes even one hull-covering ruler.

For seven marks, two implementations use different central representations:
one incrementally stores positive differences in three machine words; the
other stores all unordered sums. Each exhausts every normalized prefix and
may prune only after a repeated difference or sum has already made every
extension non-Sidon. They independently agree on

```text
tasks:                  8,515
endpoint attempts:      4,664,137,760
seven-mark Sidon rulers: 3,188,523,904
hull-covered rulers:          455,390
longest blocked run:              101
ruler:                {0,24,27,35,39,41,75}
blocked component:               [-17,83]
```

The hull-covered total and optimum again remain unchanged from the old
max-101 frontier. Since every set of at most seven marks has blocked-run
length at most 101, none can be maximal on any interval of length 102 through
136. This proves `a(n) >= 8` throughout the claimed range.

## Explicit upper bound

The normalized eight-mark ruler

```text
R = {0,39,47,51,52,61,67,101}
```

has all 36 unordered pair sums distinct. Its blocked component is exactly

```text
[-16,119],
```

which has length 136. For each `102 <= n <= 136`, put

```text
t = max(1, n-119).
```

Then `R+t` lies in `{1,...,n}`, and its translated blocked component
`[t-16,t+119]` contains the whole domain. Hence `R+t` is a maximal
eight-element Sidon set. The direct checker rebuilds all pair sums and tests
every outside insertion separately for all 35 values of `n`.

Representative certificates are

```text
n=102: {1,40,48,52,53,62,68,102}
n=128: {9,48,56,60,61,70,76,110}
n=136: {17,56,64,68,69,78,84,118}.
```

This proves `a(n) <= 8` and completes the equality.

## Cross-checks and scope

An exhaustive small-instance test compares the positive-difference formula,
pair-sum formula, and literal insertion predicate on 858 seven-mark rulers
and 77,514 candidate insertions. Every result agrees. A full ASan/UBSan run
of the pair-sum engine at maximum 110 reproduces its exact counters with no
diagnostic; the final max-135 runs use the same checked transitions and stay
well inside all integer and array bounds.

The eight-mark ruler was found by a deterministic seeded search and is
load-bearing only through the direct witness checker. The finite lower bound
depends on exhaustive C++ computation rather than a short hand proof.
Different representations, exact matching counters, direct witness replay,
sanitizers, and the earlier hostile audits reduce but do not eliminate
ordinary finite-code/compiler/hardware risk.

## Reproduction

Run from this directory:

```bash
./reproduce.sh
```

The default run compiles and executes both max-135 seven-mark enumerators,
the parallel sizes-one-through-six enumeration, the direct witness checker,
and the small formulation cross-check. Set `FULL=1` to add the slower
sequential sizes-one-through-six run and the max-110 sanitizer run.
