# Independent audit of the Problem #864 extension through `F(117)`

Audit date: 2026-08-12 (UTC)

## Verdict

**PASS.**  The proposed extension is correct, conditional only on accepting
the supplied finite exhaustive computation in the same sense as the earlier
published `F(107)` result.

The independent checker in this bundle proves computationally that no valid
18-element set has diameter at most 115.  It separately verifies the proposed
18-element witness of diameter 116.  Together with the already certified
17-element witness of diameter 106, this gives

\[
 F(108)=F(109)=\cdots=F(116)=17,\qquad F(117)=18.
\]

The audit found no mathematical or implementation gap.  It did identify one
important audit trap: **all reflected-core sizes 14, 15, 16, 17, and 18 are
required**.  Output that stops at core size 15 is incomplete.  The final
adapted run `/tmp/erdos864_d115_complete.log` includes the core-14 branch; the
older short logs do not print it and must not be used as certificates.

## 1. Problem and normalization

Call a finite integer set valid if at most one integer has more than one
unordered representation `a+b` with `a <= b` in the set.  Translation
preserves validity.  Thus an 18-set contained in an interval of 116 integers
can be normalized to an integer set of diameter at most 115.

An ordinary Sidon 18-set is already impossible at this diameter: its
`C(18,2)=153` positive differences would all be distinct, but only the values
1 through 115 are available.  Hence a hypothetical set has a unique repeated
sum; call it `sigma`.

## 2. Independent reflected-core classification

If a positive difference has two distinct representations

```
x-y = u-v > 0,
```

then `x+v=u+y`.  The two sum representations are distinct, so their common
sum must be `sigma`.  Consequently the two difference pairs are reflections
of one another under `t -> sigma-t`.  No positive difference has multiplicity
greater than two.

Let

```
R = A intersect (sigma-A)
```

be the exact reflected core and let `q` be the number of unordered
representations of `sigma`, counting a possible midpoint representation.
The number `D` of duplicated positive-difference values is

```
without a midpoint: D = q(q-1),     |R| = 2q;
with a midpoint:    D = (q-1)^2,    |R| = 2q-1.
```

Therefore the number of distinct positive differences is `153-D`, which
cannot exceed the diameter 115.  Exhausting the possible `q` values leaves
exactly these five cases:

| `q` | midpoint | core `|R|` | outliers | `D` | distinct differences |
|---:|:---:|---:|---:|---:|---:|
| 7 | no  | 14 | 4 | 42 | 111 |
| 8 | yes | 15 | 3 | 49 | 104 |
| 8 | no  | 16 | 2 | 56 | 97 |
| 9 | yes | 17 | 1 | 64 | 89 |
| 9 | no  | 18 | 0 | 72 | 81 |

The tempting sixth case, `q=7` with a midpoint, has core size 13 but would
need `153-36=117` distinct positive differences.  It is impossible at
diameter 115.  Every case with `q<=6` needs at least 123.

This proves that the exhaustive core range is precisely 14 through 18.

## 3. Why the finite search is complete

Normalize the reflected core to minimum 0 and maximum `T`; its reflection sum
is then `T`.  If its lower half is

```
B = R intersect [0,T/2),
```

then

```
R = B union (T-B)                         (even core),
R = B union {T/2} union (T-B)             (odd core).
```

The marks in `B` have distinct positive differences.  Otherwise a repeated
difference inside `B` gives a repeated sum strictly below `T`, contradicting
the uniqueness of the exceptional sum.  Thus every possible `B` is generated
by elementary Golomb-ruler backtracking with minimum mark 0.

Because every lower mark is an integer strictly below `T/2` and `T<=115`,
its maximum is at most 57; the DFS includes that endpoint.  A **valid** reflected core of
size `r` has exactly `floor(r^2/4)` distinct positive differences (the only
duplicate pairs are reflection partners), so `T>=floor(r^2/4)`.  The checker
tries every remaining admissible integer `T`, even only in the odd-core case.

For each core it directly counts all unordered pair sums and accepts the core
only when `T` is the sole repeated sum.  If the core spans `[0,T]` and the
whole set has diameter at most 115, every outlier coordinate relative to the
core lies in

```
[-(115-T), 115].
```

The checker tries every increasing tuple of the required 0 through 4
outliers.  It rejects a midpoint or reflection partner, because `R` is the
*exact* reflected core; it checks the total diameter; and it rejects a new
sum collision anywhere except `T`.  A collision cannot be repaired by later
insertions, so this pruning is monotone.  These observations account for
every hypothetical 18-set.

## 4. Independent implementation

`verify_864_18.cpp` is standalone and does not import, patch, or execute the
published checker.  Its implementation was written from scratch for this
audit.  In particular it differs from the adapted run by:

- direct byte-array pair-sum counting for every reflected core;
- a bitset indexed by signed, unshifted relative sum coordinates;
- explicit assertions that all sums newly involving an outlier are distinct;
- descending diameter order and reverse core-size order;
- independent, order-insensitive 64-bit core-set checksums.

It also directly checks the 17- and 18-element witnesses and mechanically
reconstructs the five-row core classification before starting the full DFS.
Assertions were enabled in the certification run.

Build and run:

```bash
g++ -O3 -std=c++17 verify_864_18.cpp -o verify_864_18
./verify_864_18
```

The independent full run returned:

| core | outliers | lower halves | core candidates | valid cores | extension nodes | XOR digest | sum digest |
|---:|---:|---:|---:|---:|---:|:---|:---|
| 18 | 0 | 51,140 | 190,268 | 0 | 0 | `0000000000000000` | `0000000000000000` |
| 17 | 1 | 1,697,946 | 4,813,064 | 105 | 105 | `f70bafe43806e23b` | `015a7b729b7f2a77` |
| 16 | 2 | 1,697,946 | 11,324,078 | 43,399 | 43,405 | `8e825021c615f447` | `2a52b782d6196caf` |
| 15 | 3 | 3,367,288 | 15,775,280 | 114,112 | 116,930 | `ba0f90911b1e131d` | `cce71e73ac9b7c7b` |
| 14 | 4 | 3,367,288 | 34,917,916 | 2,837,087 | 3,816,277 | `de17c854c0d8de59` | `3eccf07f74284833` |

It ended with

```text
EXHAUSTED: no valid 18-set has diameter <= 115
```

The run took about 55 seconds on the audit host.  `SEARCH_OUTPUT.txt` and
`TIME.txt` contain the exact transcript and resource report.

Every enumeration count agrees exactly with the mechanically adapted earlier
checker (`/tmp/erdos864_d115_complete.log`), despite the changed traversal and
data representation.  The adapted checker's FNV digests were additionally:

| core | adapted FNV-64 |
|---:|:---|
| 18 | `14650fb0739d0383` |
| 17 | `c3c83e2f6b8342a9` |
| 16 | `a39619526e20f512` |
| 15 | `a0d101d950b97b11` |
| 14 | `02e0d02be7877dda` |

The same independent binary was also run under AddressSanitizer and
UndefinedBehaviorSanitizer.  That transcript is retained separately.

## 5. Witness and exact values

The normalized proposed witness is

```text
0, 1, 3, 11, 15, 20, 36, 43, 49,
67, 73, 80, 96, 101, 105, 113, 115, 116.
```

Its diameter is 116.  Its sole repeated sum is 116, in exactly the nine
representations

```text
0+116, 1+115, 3+113, 11+105, 15+101,
20+96, 36+80, 43+73, 49+67.
```

All other unordered pair sums occur once.  Translating by 1 puts the witness
in `[1,117]`, proving `F(117)>=18`.

The exhaustive result gives `F(116)<=17`.  The previously certified
17-element witness of diameter 106 gives `F(N)>=17` for every `N>=107`, hence
`F(108),...,F(116)=17`.  Finally, deleting 117 if present shows the elementary
one-step inequality `F(117)<=F(116)+1=18`, so the new witness gives
`F(117)=18` exactly.

## 6. Hostile checks and caveats

- **Core 14:** required and fully searched.  It is by far the largest branch.
- **Core 13:** excluded mathematically by the 117-difference lower bound, not
  silently omitted.
- **Endpoint 57:** included in the lower-half DFS.
- **Outliers on either side:** both are included; relative candidates start
  at `-(115-T)` and end at 115.
- **Exact core:** midpoint and reflection-paired outliers are rejected.
- **Exceptional multiplicity:** unrestricted; only the *number of sums* with
  multiplicity greater than one is constrained.
- **Bitset capacity in the adapted checker:** safe here.  Its inherited seven
  64-bit words hold 448 positions.  For the smallest searched core,
  `T>=49`, so its shift is at most 66 and its largest shifted sum is 362.
- **Expository precision:** the lower bound `T>=floor(r^2/4)` is valid for a
  reflected core satisfying the near-Sidon condition.  It is not true that an
  arbitrary centrally symmetric set must have that many distinct
  differences; the report above uses the qualified statement.
- **Scope:** this is a finite computational result.  It does not settle the
  asymptotic Problem #864.
