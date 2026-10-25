# Problem 156 finite frontier: exact A382397 values through 95

Date: 2026-08-11 UTC

## Verdict

Let `a(n)` be the minimum cardinality of a maximal Sidon subset of
`{1,...,n}`. The certified values are

```text
a(66) = a(67) = 6,
a(n) = 7 for every 68 <= n <= 95.
```

This extends OEIS A382397 from its currently published endpoint `n=65` to
`n=95`. It is a finite exact extension associated with Erdos Problem 156. It
does **not** resolve the parent asymptotic problem, which asks whether maximal
Sidon subsets of `{1,...,N}` of size `O(N^(1/3))` exist for all `N`.

## Live status and source provenance

- The live Problem 156 page was accessed on 2026-08-11 through a Bright Data
  browser because the ordinary fetch returned HTTP 403. It said `OPEN`, had
  `0 claimed proofs`, and listed `Currently working on this problem: None`.
  Its statement was: "Does there exist a maximal Sidon set
  `A subset {1,...,N}` of size `O(N^(1/3))`?"
  <https://www.erdosproblems.com/156>
- The site's LaTeX page gives the same statement and citations:
  <https://www.erdosproblems.com/latex/156>.
- The primary source is P. Erdos, A. Sarkozy, and T. Sos, *On Sum Sets of
  Sidon Sets, I*, Journal of Number Theory 47 (1994), 329-347,
  DOI 10.1006/jnth.1994.1040. The paper defines Sidon sets by uniqueness of
  sums `a+a'` with `a<=a'`.
  <https://www.sciencedirect.com/science/article/pii/S0022314X84710407>
- The current asymptotic upper bound cited by the problem page is I. Z. Ruzsa,
  *A small maximal Sidon set*, Ramanujan Journal 2 (1998), 55-58,
  DOI 10.1023/A:1009757824153. It constructs a maximal set of size
  `O((N log N)^(1/3))`.
- OEIS A382397 was accessed on 2026-08-11. It defined the same
  minimum-cardinality sequence and linked a table only for `n=0..65`. The
  listed terms end with `a(43)=...=a(65)=6`.
  <https://oeis.org/A382397>
- Four targeted web searches for `A382397` with `66`, maximal Sidon sets on
  `{1,...,66}`, and GitHub occurrences found no later exact values. The only
  sequence mirror found also stopped at `n=65`.
- A fresh clone of the public problem database was checked at commit
  `579b259ef6b1392637427292273edd1e14440045`; Problem 156 was still `open`
  and linked A382397. <https://github.com/teorth/erdosproblems>
- ErdosProblemADay already has a 2026-07-27 in-progress article on the
  asymptotic log-factor obstruction for Problem 156. The finite exact result
  here is new relative to that article and must be described as an OEIS
  extension, not as a solution of Problem 156.

## Definitions and exact blocking lemma

A finite integer set `A` is Sidon when all unordered pair sums with repetition

```text
a_i + a_j,  i <= j,
```

are distinct. Equivalently, all positive differences between distinct marks
are distinct.

For a Sidon set `A`, let `S(A)` be its old pair-sum set. Define

```text
B(A) = A
       union {s-a : s in S(A), a in A}
       union {s/2 : s in S(A), s even}.
```

**Blocking lemma.** For an integer `x` not in `A`, the enlarged set
`A union {x}` is not Sidon if and only if `x` is in `B(A)`.

Proof: the new sums are `x+a` for `a in A` and `2x`. Distinct sums `x+a`
cannot collide with one another, and `x+a=2x` would imply `a=x`, excluded.
Thus a failure occurs exactly when `x+a=s` or `2x=s` for an old sum
`s in S(A)`, which is exactly the displayed set.

The difference-based engine uses the equivalent form

```text
B(A) = A
       union {a-d, a+d : a in A, d a positive old difference}
       union {(a+b)/2 : a<b in A, a+b even}.
```

The two forms were implemented separately. The engines deliberately share
normalization, traversal structure, run scanning, and reporting scaffolding,
but not their central Sidon or blocking representation.

## Normalization and completeness

Suppose `A subset {1,...,n}` is maximal. Put `m=min(A)`,
`R=A-m`, and `L=max(R)`. Then `min(R)=0`, `L<=n-1`, and translation preserves
the Sidon property and the blocking relation. The original domain becomes the
`n` consecutive integers

```text
[1-m, n-m],
```

which contains the whole hull `[0,L]`. Maximality is equivalent to every
integer of that translated domain belonging to `B(R)`.

If some integer of `[0,L]` is not blocked, no domain interval containing the
ruler can work. Otherwise let `[lo,hi]` be the maximal consecutive run in
`B(R)` containing `[0,L]`. Every maximal domain interval containing `R` is a
subinterval of this run, so its length is at most `hi-lo+1`. Conversely, any
length-`n` subinterval of this run which contains `[0,L]` gives a maximal
translate. If the run has length at least `n` and `L<=n-1`, such a subinterval
exists: slide an `n`-point window inside the run until it contains both 0 and
`L`.

For every `n<=95`, a normalized ruler has `L<=94`. For each size `1<=k<=6`,
both exact programs enumerate every set

```text
R = {0} union T,  T subset {1,...,94}, |T|=k-1.
```

There are exactly `binomial(94,k-1)` raw candidates. Marks are selected in
strictly increasing order. A branch is pruned only when its partial set
already has a repeated difference (first engine) or repeated pair sum (second
engine). Adding later marks cannot repair such a collision, so every prune is
complete. At a Sidon leaf, the appropriate exact formula above constructs the
full blocked set; no probabilistic or numeric comparison occurs.

The blocked coordinates lie between `-L` and `2L`, so both programs allocate
that whole range plus false sentinels. The scan first verifies every integer
of `[0,L]` is blocked, then extends left and right to the first unblocked
integer.

The separately obtained counts agree exactly:

| k | raw normalized | Sidon | hull covered | best run | first best ruler | blocked interval |
|---:|---------------:|------:|-------------:|---------:|------------------|------------------|
| 1 | 1 | 1 | 1 | 1 | `{0}` | `[0,0]` |
| 2 | 94 | 94 | 2 | 4 | `{0,1}` | `[-1,2]` |
| 3 | 4,371 | 4,324 | 8 | 10 | `{0,1,3}` | `[-3,6]` |
| 4 | 134,044 | 125,504 | 76 | 22 | `{0,1,5,7}` | `[-7,14]` |
| 5 | 3,049,501 | 2,434,706 | 1,102 | 42 | `{0,5,11,12,20}` | `[-12,29]` |
| 6 | 54,891,018 | 30,594,300 | 20,166 | 67 | `{0,7,19,22,28,39}` | `[-15,51]` |

In particular, among every normalized Sidon set of size at most 6 and
diameter at most 94, no blocked run has length at least 68. Therefore no
maximal Sidon set of size at most 6 exists in `{1,...,n}` for any
`68<=n<=95`. The rows `k<=5` also exclude sizes at most 5 at `n=66,67`.

The two engines do not share their central representation:

- `verify_156_a66.cpp` stores positive differences in an unsigned 128-bit
  mask and constructs `a+-d` plus midpoint blocks.
- `audit_156_size6_sums.cpp` stores unordered sums in `std::bitset`, rejects
  repeated sums directly, and constructs `s-a` plus half-sum blocks.

Their candidate counts, Sidon counts, hull-covered counts, best runs, first
best rulers, and intervals all match.

## Explicit upper-bound certificates

The following sets are Sidon and maximal in their indicated domains. Together
with the lower bounds above, they prove the verdict.

```text
66: {21,25,31,40,43,60}
67: {16,23,35,38,44,55}
68: {16,23,35,38,44,55,68}
69: {13,24,30,33,45,52,68}
70: {6,32,34,37,38,47,54}
71: {14,16,30,38,43,47,53}
72: {18,30,32,33,40,49,53}
73: {5,30,41,42,60,64,69}
74: {9,12,23,35,40,42,62}
75: {9,12,28,30,39,40,63}
76: {4,12,30,31,33,47,53}
77: {19,27,31,34,52,63,65}
78: {15,25,36,37,40,42,72}
79: {15,26,33,45,49,55,58}
80: {30,35,38,44,45,69,71}
81: {22,30,31,37,51,53,56}
82: {22,34,38,39,41,64,75}
83: {20,29,35,46,48,60,64}
84: {7,29,39,53,56,60,62}
85: {25,28,30,48,49,55,63}
86: {12,34,42,45,47,63,73}
87: {18,42,43,45,49,59,81}
88: {22,24,35,42,45,59,64}
89: {27,35,38,52,56,58,82}
90: {29,32,34,51,55,64,84}
91: {11,27,30,34,48,58,59}
92: {11,35,43,45,49,54,80}
93: {18,39,42,50,54,56,87}
94: {12,37,45,47,51,58,81}
95: {30,31,33,48,55,59,93}
```

`check_156_witnesses_66_95.py` verifies each certificate without using the
blocked-run search. It directly builds every unordered pair sum (including
diagonal sums), asserts uniqueness, and for every outside `x` finds an old
sum collision after inserting `x`. Its log gives a SHA-256 digest of the
chosen collision list for each domain.

## Separately frozen a(66) audit

The default C++ run restricts the diameter to 65 and finds exactly six
six-mark placements in `[1,66]`, with no placement of size at most 5. Its
counts include

```text
k=5: raw 677,040; Sidon 485,352; hull covered 1,102; placements 0;
k=6: raw 8,259,888; Sidon 3,415,896; hull covered 20,166; placements 6.
```

`audit_156_a66_sums.py` is a cold Python audit. It uses `itertools` to visit
all `binomial(65,k-1)` normalized candidates for `k<=5` without the C++
prefix pruning, tests Sidon by unordered sums, and checks translations using
the sum-collision formula. It independently obtains the same Sidon and
hull-covered counts and no small placement. It then validates all six C++
witnesses by rebuilding the full Sidon condition after every possible
insertion. The log prints a human-readable collision equality for each of the
60 outside points of the first witness.

## Reproduction

Toolchain used:

```text
g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
Python 3.12.3
Linux x86_64, kernel 6.12.93
```

Commands, from `/home/exedev/erdos_scratch`:

```bash
g++ -std=gnu++20 -O3 -Wall -Wextra verify_156_a66.cpp -o verify_156_a66
/usr/bin/time -v ./verify_156_a66
python3 audit_156_a66_sums.py

g++ -std=gnu++20 -O3 -Wall -Wextra -DVERIFY_156_N=95 \
  verify_156_a66.cpp -o verify_156_n95_differences
/usr/bin/time -v ./verify_156_n95_differences

g++ -std=c++20 -O3 -Wall -Wextra audit_156_size6_sums.cpp \
  -o audit_156_size6_sums
/usr/bin/time -v ./audit_156_size6_sums

python3 check_156_witnesses_66_95.py
```

All final commands exited with status 0. Wall times were approximately 2.3 s
for the `n=66` difference run, 6.8 s for the cold Python audit, 21.0 s for the
diameter-94 difference run, and 18.1 s for the pair-sum cross-check.

## Frozen source and log hashes

```text
3c9c9444f327a5f531ffa11fa048e9f276c59b716862b0b4ea9941a57081dff6  verify_156_a66.cpp
c1198747b6e04c80c4c0c400d7c1ee60766784b2e1b8b939df2ffc124cd8907e  audit_156_a66_sums.py
42a58a68dee5acfa748916908b3cdf17908c0743b37e7549c37c3720c31f8b32  audit_156_size6_sums.cpp
1dc4bd14f8932f243ae57968e3ea495aaa777ebd38579dfa09a4e6c127365194  check_156_witnesses_66_95.py
6ce638d3d048a32e8db9ab44bd23bbc5ede72709d7a0a0e62ac40444ccc4450f  erdos156_a66_difference_run_2026-08-11.log
3845a8fcec031ac95249f743a2e70051af4903afd0f013dbf391a6e0dbc86825  erdos156_a66_sum_audit_run_2026-08-11.log
70c77f5868047b1c6ef2e260f384d20ee2c273a9be22b2b7fec6ffc4e1ac58f6  erdos156_n95_difference_run_2026-08-11.log
d44d89abc419e678d395d396db4a71d5f9ff8f06844f7489a813d1aa9c29e5c4  erdos156_n95_sum_audit_run_2026-08-11.log
a22589f63c0d48501d1f4add5aff637f64bc96cb0078eb0a1fd1a4620f5b9f0c  erdos156_witness_run_2026-08-11.log
```

## Scope and non-claims

- The frozen computation itself did not edit or deploy site source.
- This is an exact OEIS/frontier computation, not a solution or asymptotic
  improvement to Erdos Problem 156.
- The enumeration proves the lower bound only through `n=95`; it does not
  assert that 67 is the global maximum blocked run for arbitrary six-mark
  rulers of diameter greater than 94.
- A fixed-seed exploratory search failed to find a seven-mark witness for
  `n=96` in 200,000,000 random samples. That is not a proof of nonexistence,
  is excluded from the exact verdict, and is not used by any certificate.
