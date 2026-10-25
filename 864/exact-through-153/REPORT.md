# Erdős problem #864: target-20 finite boundary

Date: 2026-08-12 UTC

Claim label: **computational-only**.  The reflected-core reduction below is
elementary.  The finite nonexistence claim depends on two exhaustive C++
programs and is not an asymptotic result.

## Result

Write `F(N)` for the maximum size of a subset of `{1,...,N}` for which at
most one unordered pair-sum value has multiple representations, with diagonal
pairs allowed.  The computation proves

```text
F(135) = F(136) = ... = F(152) = 19,
F(153) = 20.
```

The mandatory live gate was refreshed through Bright Data immediately before
the search.  Problem #864 was **OPEN**, with **0 claimed proofs**, no listed
current worker, and no listed collaborator.  The rendered text is frozen in
`live_gate.txt`.

## New 20-point witness

The public optimal-Golomb-ruler table supplied the 10-mark ruler

```text
B = {0,1,6,10,23,26,34,41,53,55}.
```

A direct center scan found that `B union (152-B)` is

```text
{0,1,6,10,23,26,34,41,53,55,
 97,99,111,118,126,129,142,146,151,152}.
```

Its only repeated sum is 152, in the ten ways

```text
0+152 = 1+151 = 6+146 = 10+142 = 23+129
      = 26+126 = 34+118 = 41+111 = 53+99 = 55+97.
```

`verify_witness.py` does not trust the table: it checks the 45 positive
differences of `B` and recounts all 210 diagonal-inclusive unordered sums of
the 20-point witness.  Adding one to every mark gives a valid 20-set in
`{1,...,153}`.

As a positive control, the direct exhaustive program was then run at cap 152.
It independently found another reflected 20-set after 18,689 orbit nodes:

```text
{0,1,3,8,14,26,30,47,62,71,
 81,90,105,122,126,138,144,149,151,152}.
```

The definition-level Python checker independently verifies this second
witness as well.

## Complete reflected-core reduction under diameter 151

Translate a hypothetical 20-set so its minimum is 0 and write `L` for its
diameter.  Translation preserves equality of sums.  If there is no repeated
sum, all `C(20,2)=190` positive differences are distinct, impossible for
`L<=151`.

Otherwise let `sigma` be the unique repeated sum and suppose

```text
x-y = u-v,  x>y, u>v
```

has two distinct representations.  Then `x+v=u+y`, so this common sum must be
`sigma`; hence the two difference pairs are reflections in `sigma/2`.
Consequently each positive difference appears at most twice, and every
duplicate is a reflected pair.

Let `R=A intersect (sigma-A)` be the exact reflected core.  If `sigma` has
`q` unordered representations, then

```text
|R| = 2q       without the midpoint sigma/2,
|R| = 2q-1     with the midpoint sigma/2.
```

The number `D` of duplicated positive-difference values is

```text
D = q(q-1)       without a midpoint,
D = (q-1)^2      with a midpoint.
```

Thus `A` has exactly `190-D` distinct positive differences, all in
`{1,...,L}`.  Under `L<=151`, the complete retained case list is:

| q | midpoint | core size r | outliers | D | lower bound on L |
|---:|:---:|---:|---:|---:|---:|
| 10 | no  | 20 | 0 | 90 | 100 |
| 10 | yes | 19 | 1 | 81 | 109 |
| 9  | no  | 18 | 2 | 72 | 118 |
| 9  | yes | 17 | 3 | 64 | 126 |
| 8  | no  | 16 | 4 | 56 | 134 |
| 8  | yes | 15 | 5 | 49 | 141 |
| 7  | no  | 14 | 6 | 42 | 148 |

The next case, a 13-point core with a midpoint, has `D=36` and would force
`L>=154`; all smaller cores are still worse.  Therefore core sizes 20 through
14 are exhaustive.

Normalize the core itself to `[0,T]`; its exceptional reflection sum is then
`T`.  Its lower half

```text
0=b_0 < b_1 < ... < b_(k-1) < T/2
```

is a Golomb ruler, since a repeated difference wholly below `T/2` would give
a repeated sum strictly below `T`.  Reflection forces the upper half, and the
midpoint `T/2` is added precisely in odd-core cases.  Every outlier is in
`[T-151,151]`, cannot be the midpoint, and cannot be selected with its
reflection partner.  Adding outliers in increasing order therefore enumerates
every normalized candidate exactly once.

Crucially, `T` is the **core** diameter and need not equal the total diameter
`L`.  Every parity-admissible center from the core's own lower bound through
151 is searched;
the global lower bounds in the table are not used to skip centers.

An early scratch slicing wrapper briefly made exactly that invalid skip.  It
was caught before any claim: the shortcut was retracted, every omitted center
was rerun, and the frozen `verify_direct_logs.py` requires each legal center
exactly once.  The canonical output excludes the retracted `SKIP` records.

## Two exhaustive implementations

`search20_direct.cpp` constructs reflection orbits `{b,T-b}` and maintains a
full multiplicity array for unordered sums.  It rejects a branch only when a
second repeated sum has already appeared, then tries all increasing outlier
tuples in the signed coordinate interval.

`audit20_lowerhalf.cpp` is independently organized.  It enumerates Golomb
lower halves with a Boolean difference table, visits diameters in descending
order, reconstructs and directly recounts every proposed core, and extends
with a separate signed-sum bitset.  It includes assertions that every newly
introduced sum is internally unique.

The prior target-19 audit caught an exclusive-endpoint error in an early
scratch orbit generator.  Both frozen target-20 programs use the corrected
endpoint: for an even core, lower marks run inclusively through `(T-1)/2`.
The audit generator reaches the same boundary through its independent
`T >= 2*largest+1` condition.

The direct implementation completed all 239 exact-center slices for core
sizes 16 through 14 and the four whole ranges for core sizes 20 through 17.
`verify_direct_logs.py` rejects missing or duplicate centers and produced:

| core r | centers | valid cores | direct extension nodes |
|---:|---:|---:|---:|
| 20 | 52 | 0 | 0 |
| 19 | 31 even centers | 489 | 489 |
| 18 | 71 | 240,837 | 240,851 |
| 17 | 40 even centers | 758,979 | 770,944 |
| 16 | 88 | 27,176,695 | 32,545,628 |
| 15 | 48 even centers | 11,169,166 | 26,205,666 |
| 14 | 103 | 109,972,454 | 697,583,479 |

The independent program then completed the same seven rows and ended with

```text
EXHAUSTED: no valid 20-set has diameter <= 151
```

Its independently generated census was:

| r | lower halves | core candidates | valid cores | audit extension nodes |
|---:|---:|---:|---:|---:|
| 20 | 555,596 | 2,408,120 | 0 | 0 |
| 19 | 23,306,506 | 73,972,592 | 489 | 489 |
| 18 | 23,306,506 | 171,251,690 | 240,837 | 240,855 |
| 17 | 64,133,594 | 323,515,188 | 758,979 | 771,955 |
| 16 | 64,133,594 | 711,163,974 | 27,176,695 | 32,993,607 |
| 15 | 37,339,096 | 271,684,326 | 11,169,166 | 27,471,924 |
| 14 | 37,339,096 | 580,707,816 | 109,972,454 | 750,820,452 |

The extension-node totals differ because the programs order and represent
outlier branches differently.  The exact valid-core totals agree in all seven
rows.  `compare_counts.py` parses the frozen outputs and enforces those seven
equalities.  The audit additionally freezes order-sensitive aggregate core
digests in `audit_output.txt`.

## Exact-value inference

The prior 19-point witness of diameter 134 is rechecked from the definition in
this bundle.  The exhaustion rules out a 20-point set of diameter at most 151.
An interval `{1,...,N}` has diameter at most `N-1`, so `F(N)=19` for every
`135<=N<=152`.  Finally `F(N+1)<=F(N)+1`, by deleting `N+1` when present.
Thus `F(153)<=20`, while the translated new witness supplies equality.

## Scope

This determines one new finite boundary only.  It does not prove a uniform
bound, identify the asymptotic constant, or resolve the open Erdős problem.
