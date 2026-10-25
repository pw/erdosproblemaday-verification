# Erdős problem #819: exact finite extension through `N=120`

Date: 2026-08-12 UTC

Status: **computational finite partial**. This does not estimate the
asymptotic function and does not solve Problem #819.

## Live gate and collision checks

The live problem page and complete discussion were fetched through Bright
Data before this computation. The captures in this directory show:

- status `OPEN`;
- `0 claimed proofs`;
- `Currently working on this problem: None`;
- `Interested in collaborating: None`;
- no formalisation worker;
- two comments, both about the May 2026 asymptotic lower bound, and neither
  containing a finite table.

The live definition is

> Let `f(N)` be maximal such that there exists
> `A subset {1,...,N}`, with `|A|=floor(sqrt(N))`, such that
> `|(A+A) intersect [1,N]|=f(N)`. Estimate `f(N)`.

The public site already has a #819 ledger entry reproducing the older
MathDyad report through `N=80`, but no dedicated `verification/819` bundle.
This computation extends that existing finite table.

The published-table audit located the classical optimal-Golomb-ruler table
OEIS A003022, which gives lengths `G(8)=34`, `G(9)=44`, and `G(10)=55`.
The verifier below recomputes all three rather than trusting that table.
OEIS A392461 is a different invariant: it permits every difference to occur
twice, potentially many times overall, whereas the present sharp boundary
allows only one repeated pair-sum representation in total. Exact-statement,
exact-phrase, OEIS, Golomb-ruler, and Erdős-Freud searches located no public
table of the live `f(N)` values in this range. This is a search report, not a
priority claim; no claim of global novelty is made.

Relevant public records checked:

- <https://www.erdosproblems.com/819>
- <https://www.erdosproblems.com/forum/thread/819>
- <https://oeis.org/A003022>
- <https://oeis.org/A392461>
- P. Erdős and R. Freud, *On sums of a Sidon-sequence*, Journal of Number
  Theory 38 (1991), 196-205, DOI `10.1016/0022-314X(91)90083-N`.

## Exact result

The exact extension is

| `N` | `f(N)` |
|---:|---:|
| `81` | `43` |
| `82...89` | `44` |
| `90...99` | `45` |
| `100...101` | `53` |
| `102...111` | `54` |
| `112...120` | `55` |

Together with the previous table through 80, this determines every value
through 120. The SHA-256 of the forty comma-separated new values is

```text
d2ad1b092d5fa521efed367cbccfe256be6e68402c73749e3d69a5b046027fc4
```

Formally, throughout this report

```text
f(N) = max { |{a+b<=N : a,b in A}| :
             A subset {1,...,N}, |A|=floor(sqrt(N)) }.
```

The sumset is a set: repeated representations of the same integer count once,
and the diagonal sums `a+a` are included. Thus the required cardinality is
nine for `81<=N<=99`, then jumps to ten at `N=100`. This change of admissible
cardinality is why `f(100)=53` can be much larger than `f(99)=45`; it is not a
monotonicity inference.

## Loss identity

Let `A={a_1<...<a_k}` and let `P=k(k+1)/2`. For an integer `s`, put

```text
r_A(s) = #{(i,j): 1<=i<=j<=k and a_i+a_j=s}.
```

Define the number of overflowing pair representations and the collision
excess below the cutoff by

```text
O_N(A) = sum_{s>N} r_A(s),
C_N(A) = sum_{s<=N, r_A(s)>0} (r_A(s)-1).
```

Partitioning the `P` unordered pairs by their sum gives the exact identity

```text
|(A+A) intersect [1,N]| = P - O_N(A) - C_N(A).       (1)
```

## Sharp auxiliary lengths

For `delta>=0`, let `g_delta(k)` be the least `L` for which there are

```text
0=x_1 < x_2 < ... < x_k <= L
```

whose `P` unordered pair sums have collision excess at most `delta`. Exhaustive
search gives

```text
g_0(8)=34,  g_0(9)=44,  g_1(9)=40,
g_0(10)=55, g_1(10)=50.                              (2)
```

Here `g_0` is the classical optimal-Golomb-ruler length. The searches prove
both halves: no witness one unit below each stated length, and an explicit
witness at the stated length.

The lower-bound witnesses, translated into positive integers, are:

```text
k=9, defect 2: (1,2,5,10,13,14,20,34,36)
k=9, defect 1: (1,2,4,11,22,27,35,39,41)
k=9, defect 0: (1,2,6,13,26,28,36,42,45)

k=10, defect 2: (1,2,8,12,28,30,33,42,45,47)
k=10, defect 1: (1,2,5,13,19,29,42,44,49,51)
k=10, defect 0: (1,2,7,11,24,27,35,42,54,56)
```

Their maximum sums are respectively 72, 82, 90, 94, 102, and 112.
Direct definition-level evaluation gives the six rows of the table.

## The two exceptional upper bounds

The ceiling and one-below-ceiling cases away from `N=81,100,101` follow
immediately from (1) and (2). The only extra issue is whether losing exactly
one pair representation to overflow can do better.

### `N=81`

Suppose a nine-element set scored at least 44, so `O_81+C_81<=1`.

If `O_81=0`, then `max A<=40`. Translate the minimum to zero. The resulting
nine marks have span at most 39 and collision excess one, contradicting
`g_1(9)=40`.

If `O_81=1`, then `C_81=0`; all 45 pair sums are globally distinct and the
sole overflow is `2 max A`. Write the normalized marks as

```text
0=x_1<...<x_8=q<x_9=L,
```

and write `s=min A>=1`. The second-largest pair sum is not an overflow, so

```text
2s+q+L <= 81, hence q+L <= 79.                       (3)
```

The first eight marks and all nine marks are Sidon, so (2) gives `q>=34` and
`L>=44`. Thus only

```text
L=44 with q<=35, or L=45 with q<=34
```

can occur. Complete prefix enumeration returns no ruler in either case
(59,376 nodes/20 terminal prefixes and 46,443 nodes/2 terminal prefixes).
Therefore the score is at most 43, and the defect-two witness attains 43.

### `N=100,101`

Suppose a ten-element set scored at least 54. If there is no overflow,
translation
would give ten marks of span at most 49 and defect one, contradicting
`g_1(10)=50`.

If there is one overflow and no collision, normalize as above, now with a
nine-mark prefix of span `q` and total span `L`. Then

```text
q>=g_0(9)=44, L>=g_0(10)=55, and q+L<=N-2.          (4)
```

For `N=100`, (4) is impossible. For `N=101`, equality is forced:
`s=1`, `q=44`, and `L=55`. Complete enumeration of every Sidon nine-mark
prefix in `[0,44]` finds two terminal prefixes, neither of which remains
Sidon after appending 55 (365,812 search nodes). Thus both values are at most
53, and the displayed defect-two witness attains 53.

For `82<=N<=89` and `102<=N<=111`, the defect-one witnesses meet the upper
bound one below the pair-count ceiling. At `N>=90` in the nine-mark block and
`N>=112` in the ten-mark block, the Sidon witnesses attain the ceiling.

For completeness, here is the definition-level derivation of every interval,
including both jumps.

1. At `N=81`, the preceding case split proves the upper bound 43. The
   translated defect-two witness has largest sum 72, so (1) gives
   `45-0-2=43`.
2. For `82<=N<=89`, the nine-mark ceiling is 45. Equality would require a
   Sidon set with every sum at most `N`; after translating its minimum to
   one, this is a ruler of span at most `floor(N/2)-1<=43`, contradicting
   `g_0(9)=44`. The defect-one witness has largest sum 82, so it scores
   `45-0-1=44` throughout the interval.
3. For `90<=N<=99`, the nine-mark Sidon witness has largest sum 90, so it
   attains all 45 possible unordered pair sums. No set can exceed the
   pair-count ceiling 45.
4. At `N=100`, `floor(sqrt(N))` increases from nine to ten and the pair-count
   ceiling jumps from 45 to 55. The preceding `N=100,101` case split proves
   the upper bound 53. The ten-mark defect-two witness has largest sum 94,
   so (1) gives `55-0-2=53` at both `N=100` and `N=101`.
5. For `102<=N<=111`, equality with the ten-mark ceiling 55 would require a
   Sidon ruler of span at most `floor(N/2)-1<=54`, contradicting
   `g_0(10)=55`. The defect-one witness has largest sum 102, so it scores
   `55-0-1=54` throughout the interval.
6. At `N=112`, the ten-mark Sidon witness first fits completely: its largest
   element is 56 and hence its largest sum is exactly 112. It attains the
   ceiling 55 for every `112<=N<=120` (indeed through the rest of the
   ten-mark block). This proves the jump `54` to `55` directly from the live
   truncated-score definition.

The only times an overflow search is needed are `N=81,100,101`, where the
claimed upper bound is two below the pair ceiling. To see why the listed
overflow cases are exhaustive, suppose `O_N+C_N<=1`. If `O_N=0`, translation
reduces the problem to the appropriate `g_1` search. If `O_N=1`, then
`C_N=0`. The only overflowing representation must be `max A+max A`: were
some other pair above `N`, the strictly larger diagonal sum would give a
second overflowing representation. Consequently all pair sums are globally
distinct, and the candidate is exactly a Sidon ruler subject to (3) or (4),
which is what the fixed-last enumerations exhaust. There is no third case.

## Exhaustive-search completeness and audits

`verify.py` is dependency-free. At a prefix it records the exact bit set of
unordered pair sums and its collision excess. When a new mark `x` is added,
the new sums

```text
x+x_1, ..., x+x_t, 2x
```

are mutually distinct. The number already present in the bit set is exactly
the increase in collision excess. The recursion tries every possible next
integer and rejects precisely when the requested defect budget is exceeded.
It therefore enumerates every normalized candidate once. It also compares
189 small instances against literal `itertools.combinations` enumeration.

The producer visits, among other searches, 5,507,838 nodes to rule out a
ten-mark defect-one set of length 49 and 2,322,065 nodes to rule out a
ten-mark Sidon set of length 54. It finished in about 57 seconds on this VM.

`hostile_check.cpp` independently implements the same complete state space
using mutable arrays of representation counts rather than the producer's
immutable integer bit masks. It reproduces every existence result, witness,
node count, prefix count, and all forty scores in about two seconds. An
ASan+UBSan build produces byte-identical output with no diagnostic.

Reproduce with:

```bash
python3 verify.py
g++ -O3 -std=c++20 -Wall -Wextra -pedantic hostile_check.cpp -o hostile_check
./hostile_check
```

Every finite value here is computational-only. No priority claim is made for
the optimal Golomb rulers, the defect rulers, or the resulting table.

PARTIAL: dependency-free exhaustive search and an independent C++ audit determine the live Problem #819 function exactly for every 81<=N<=120, extending the local exact table through 120; the asymptotic estimation problem remains open.
