# Erdős problem #864: exact target-19 finite extension

Date: 2026-08-12 UTC

Claim label: **computational-only**. The reduction is elementary; the finite
nonexistence step is supplied in two exhaustive C++ implementations.

## Result

Let `F(N)` be the largest size of a set in `{1,...,N}` for which at most one
unordered pair-sum value has more than one representation. Then

```text
F(117) = F(118) = ... = F(134) = 18,
F(135) = 19.
```

The live gate was refreshed through Bright Data immediately before this run.
Problem #864 was still **OPEN**, with **0 claimed proofs**, no current worker,
and no listed collaborator. The extracted page is frozen in `live_gate.txt`.

## Complete reflected-core reduction

Translate a candidate set `A` so its minimum is 0, and let `L` be its
diameter. Translation preserves all equality relations among sums.

First suppose there is a repeated sum, and call the unique repeated value
`sigma`. If one positive difference has two representations

```text
x-y = u-v,  x>y, u>v,
```

then `x+v=u+y`. Those are distinct pair representations, so their common sum
must be `sigma`; consequently the two difference pairs are reflections of
one another in `sigma/2`. Thus a positive difference occurs at most twice,
and every duplicate is a reflected pair.

Put `R = A ∩ (sigma-A)`. If `sigma` has `q` unordered representations,
then each representation is one reflection orbit in `R`; a nondiagonal orbit
has two points, while a diagonal representation is the singleton midpoint.
The number `D` of duplicated positive-difference values is

```text
D = q(q-1)       without a midpoint,
D = (q-1)^2      with a midpoint.
```

Since `A` has `C(19,2)=171` positive-difference occurrences, it has exactly
`171-D` distinct positive differences. All lie in `{1,...,L}`, so
`L >= 171-D`.

For `L <= 133`, this leaves exactly the following cases:

| q | midpoint | exact core size r | outliers | D | lower bound on L |
|---:|:---:|---:|---:|---:|---:|
| 10 | yes | 19 | 0 | 81 | 90 |
| 9 | no | 18 | 1 | 72 | 99 |
| 9 | yes | 17 | 2 | 64 | 107 |
| 8 | no | 16 | 3 | 56 | 115 |
| 8 | yes | 15 | 4 | 49 | 122 |
| 7 | no | 14 | 5 | 42 | 129 |

The largest omitted duplicate count is `(7-1)^2=36`, from a 13-point core;
it would force `L >= 171-36=135`. Smaller cores are no better. If there is no
repeated sum at all, `A` is an ordinary Sidon set and all 171 positive
differences are distinct, also impossible under the cap. Therefore core
sizes 19 through 14 are complete; no assumption such as `r>=14` is left
unproved.

## Why the finite enumeration is complete

Normalize the exact reflected core itself to minimum 0. Its maximum is then
some `T`, and its reflection sum is `T`. Its lower half consists of marks

```text
0 = b_0 < b_1 < ... < b_{k-1} < T/2.
```

The rest of the core is forced by reflection, with `T/2` additionally present
in the odd-core cases. The lower half is a Golomb ruler: a repeated positive
difference there would give a second repeated sum below `T`.

A valid reflected core of size `r` has exactly `floor(r^2/4)` distinct
positive differences, so `T >= floor(r^2/4)`. Every outlier relative to a
core `[0,T]` inside a total diameter-133 set lies in
`[T-133,133]`. An exact-core outlier cannot be the midpoint and cannot be
selected with its reflection partner. Adding points in increasing order is
exhaustive; once a second repeated sum occurs, later points cannot repair it.

`search_direct.cpp` uses this description literally. It constructs core
orbits `{b,T-b}` recursively and rejects a partial core as soon as a sum other
than `T` repeats. It then tries every increasing outlier tuple in the signed
coordinate range.

`audit_lowerhalf.cpp` is independently organized. It enumerates all Golomb
lower halves with a Boolean difference table, visits diameters in descending
order, constructs and directly recounts each full core, and extends it with a
separate `std::bitset` representation of signed sums.

## Exhaustion results

Both programs found zero 19-point candidates through diameter 133. More
strongly, their counts of valid reflected cores agree exactly in every case:

| r | audit lower halves | audit core candidates | valid cores (both) | direct extension nodes | audit extension nodes |
|---:|---:|---:|---:|---:|---:|
| 19 | 1,816,422 | 4,158,788 | 0 | 0 | 0 |
| 18 | 1,816,422 | 10,133,998 | 1,297 | 1,297 | 1,297 |
| 17 | 13,014,892 | 51,701,290 | 22,271 | 22,274 | 22,275 |
| 16 | 13,014,892 | 116,417,476 | 1,920,748 | 1,952,412 | 1,955,252 |
| 15 | 12,586,664 | 75,685,308 | 1,565,022 | 2,028,528 | 2,073,894 |
| 14 | 12,586,664 | 163,957,348 | 22,183,488 | 59,933,185 | 63,239,114 |

The extension-node totals need not agree because the programs use different
orders and pruning. The exact valid-core counts do agree. For the largest
branch, `direct_core14_slices.log` contains one result for every center
`T=49,...,133`; `summarize_slices.py` verifies exact unique coverage and
totals the 85 logs.

The independent run's final line is:

```text
EXHAUSTED: no valid 19-set has diameter <= 133
```

## Witness and exact-value inference

The new normalized 19-point witness is

```text
{0,4,5,7,17,33,44,52,58,67,76,82,90,101,117,127,129,130,134}.
```

Its only repeated sum is 134, with the ten representations

```text
0+134 = 4+130 = 5+129 = 7+127 = 17+117
      = 33+101 = 44+90 = 52+82 = 58+76 = 67+67.
```

`verify_witness.py` directly counts all 190 unordered pairs. Translating by
one gives the valid set

```text
{1,5,6,8,18,34,45,53,59,68,77,83,91,102,118,128,130,131,135}
```

in `{1,...,135}`, whose exceptional sum is 136.

The previously certified 18-point witness has diameter 116, while this run
proves that no 19-point set has diameter at most 133. Hence
`F(N)=18` for every `117 <= N <= 134`. Finally,
`F(N+1) <= F(N)+1`: remove `N+1` if it is present, or the set already lies in
`{1,...,N}`. Therefore `F(135) <= 19`, and the new witness gives equality.

## Controls and audit history

- The corrected direct enumerator was specialized back to target 18 and cap
  115. Its valid-core counts were exactly the published counts:
  `0, 105, 43,399, 114,112, 2,837,087` for core sizes 18 down to 14.
- AddressSanitizer and UndefinedBehaviorSanitizer reported no issue on a
  negative branch and reproduced the 19-point witness at center 134.
- The independent checker verifies the 17-, 18-, and 19-point witnesses and
  derives the six-case reduction itself before searching.
- An early scratch version of the direct orbit generator used an exclusive
  upper bound that omitted `floor(T/2)` when an even core had odd `T`. This
  was caught before freeze; every affected scratch result was retracted and
  excluded from this bundle. The frozen source uses the inclusive bound
  `(T-1)/2`, all affected branches were rerun, and the independent lower-half
  implementation (which never used the faulty expression) matches all six
  valid-core counts.

The two full searches use no downloaded tables and no SAT/MIP solver.
