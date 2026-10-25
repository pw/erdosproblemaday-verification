# Cold hostile audit: Erdos Problem 196 finite enumeration

Audit date: 2026-08-11 UTC.

Input frozen bundle:
`/home/exedev/erdos_scratch/fresh9_erdos196_20260811/bundle_ro`.
No file in that bundle or in the site repository was edited by this audit.

## 1. Verdict and publication-safe scope

### PASS: exact finite computation

The exact computational assertion passes:

\[
\begin{array}{c|rrrrrrrrrrrrrr}
n&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\
\hline
\theta_4(n)&1&2&6&22&102&564&3336&22266&168864&1307470&11066766&101361722&949812334&9471574188.
\end{array}
\]

The author endpoint recursion was rebuilt and rerun through `n=14`, including a direct permutation
check through `n=10`. A forbidden-subsequence automaton using neither endpoint recursion nor
complement symmetry independently reached `n=14`. A third enumerator, based on insertion of the new
maximum, also independently reached `n=14`. All values agree exactly.

### GAP: frozen publication narrative

The frozen bundle is not publication-ready unchanged. Its primary-source section omits Marcel K.
Goh and Rosie Y. Zhao, *Arithmetic Subsequences in a Random Ordering of an Additive Set*, INTEGERS
21 (2021), A89. Their peer-reviewed Table 1 gives an equivalent distribution through `n=10`.
Moreover, the public arXiv v1/v2 Table 1 includes rows `n=11,12`, despite adjacent prose saying the
table stops at `n<=10`. Those rows translate exactly to the author's values.

The publication-safe claim is therefore:

> We independently recomputed the known exact prefix through `n=12` and computed
> `theta_4(13)=949,812,334` and `theta_4(14)=9,471,574,188`. Targeted searches did not locate the
> latter two exact values in prior public tables as of 2026-08-11; that absence is search-limited,
> not a priority or novelty theorem.

This correction supersedes the negative-literature paragraph in frozen `REPORT.md` lines 99-102.

## 2. Exact object being counted

Let `[n]={1,...,n}`. For a one-line permutation
`sigma=(sigma(1),...,sigma(n))`, define

\[
\theta_4(n)=\#\left\{\sigma\in S_n:\begin{array}{l}
\text{there are no }a,d\in\mathbb Z,\ d>0,\ a+3d\le n,\text{ and}\\
i_0<i_1<i_2<i_3\text{ with }(\sigma(i_0),\ldots,\sigma(i_3))\\
=(a,a+d,a+2d,a+3d)\text{ or }(a+3d,a+2d,a+d,a)
\end{array}\right\}.
\]

The C++ programs use values `0,...,n-1`; translation by one is a bijection and preserves arithmetic
progressions.

A one-line permutation gives a total order on `[n]` by
`x <_sigma y` exactly when `x` occurs before `y`. Conversely, listing the elements of any total order
from first to last gives one unique permutation. Under this bijection the forbidden condition is

\[
a<_\sigma a+d<_\sigma a+2d<_\sigma a+3d
\quad\text{or its reverse}.
\]

Thus there is no distinction between the finite permutations counted by the code, finite orderings
in the literature, and restrictions of an order on the positive integers.

## 3. Proof of the author recursion

### Endpoint test

Suppose an avoiding prefix is extended on the right by a previously unused value `x`. Any newly
created forbidden subsequence must use `x`, and because `x` is at the last position it is the final
value of the oriented four-term word. There are exactly two possibilities:

1. `x` is the largest value, and for some `d>0` the prefix already contains
   `x-3d, x-2d, x-d` in that positional order.
2. `x` is the smallest value, and for some `d>0` the prefix already contains
   `x+3d, x+2d, x+d` in that positional order.

These are exactly the triples constructed in `forbidden_endings_[x]` and tested by `CanAppend`.
Any forbidden word not using `x` would already have existed in the parent prefix. Induction on the
prefix length therefore proves soundness and completeness.

Every recursive edge appends one specified unused value. Deleting the last value recovers a unique
parent, so every permutation has exactly one root-to-leaf path. There are neither duplicate nor
omitted states. The Python control compared the endpoint decision with a full oriented-word
subsequence test at every extension of every avoiding prefix through `n=8`.

### Complement symmetry

Value complementation `c(x)=n-1-x` maps every ascending AP word to a descending AP word and vice
versa, so it bijects avoiding subtrees rooted at ordered prefixes `(a,b)` and `(c(a),c(b))`.

No ordered prefix with distinct entries is fixed. For even `n`, no value is fixed by `c`. For odd
`n`, equality would force both entries to be the single midpoint, contradicting distinctness.
Lexicographic comparison therefore selects exactly one prefix from every two-element orbit, and
doubling the selected subtree totals is exact. Exhaustive controls verified every paired prefix
subtree through `n=9`.

### Parallel execution

`prefix_counts` is fully sized before the OpenMP loop. Iteration `i` constructs a private
`EndpointCounter` and writes only `prefix_counts[i]`; summation occurs after the parallel region.
No mutable recursion state or vector element is shared between iterations. Runs with 1, 2, 3, 7,
and 16 threads produced identical values through `n=12`.

## 4. Structurally independent enumerations

### A. Forbidden-subsequence progress automaton

`code/automaton_count.cpp` explicitly constructs every oriented length-four AP word. For every word
it stores the length of the prefix already seen as a subsequence. Appending a symbol advances exactly
those words whose next required symbol it is; reaching offset three rejects the branch. AP words
have distinct symbols and a permutation never repeats a symbol, so the greedy progress length is the
complete subsequence state. Backtracking reverses the same updates.

The search partitions by all ordered three-symbol prefixes. Each permutation has one such prefix,
and each remaining-symbol recursion path is unique. It uses no complement reduction and does not
reason about the newly appended value being an AP endpoint. It reproduced all 14 terms:

- `n=13`: 949,812,334 in 62.307 seconds;
- `n=14`: 9,471,574,188 in 626.988 seconds;
- total wall time: 695.32 seconds; exit status 0.

### B. Insertion of the new maximum

`code/insertion_count.cpp` starts with `(0)` and, at size `m`, inserts new maximum `m` into every
slot of every current avoider. Any newly created forbidden AP must contain `m`, which is necessarily
the value endpoint of that AP. It rejects exactly when the three smaller values occur before `m` in
ascending order or after `m` in descending order.

Deleting the maximum from a child recovers its unique parent. Avoidance is hereditary under this
deletion, so every avoider is generated once and only once. This is a different recursion tree from
the author program. It reproduced all 14 terms; `n=14` took 31.799 seconds and the full process 35.32
seconds, with exit status 0.

### C. Direct small-n controls

`code/exhaustive_controls.py` iterated every permutation independently through `n=9`, searched for
the explicit oriented words, and agreed with the table. The author C++ program's separate
`next_permutation` checker agreed through `n=10` (`10! = 3,628,800` permutations).

As a negative control, checking only the ascending word at `n=4` gives 23, whereas the required two
orientations give 22. The control therefore detects deletion of either orientation.

## 5. Exact identities and controls

Let `q=floor((n-1)/3)`. The number of unoriented four-element AP subsets of `[n]` is

\[
A_4(n)=\sum_{d=1}^q(n-3d)=qn-\frac{3q(q+1)}2.
\]

For any fixed AP, exactly 2 of its 24 relative orders are monotone. Hence the total incidence of
oriented monotone APs over all permutations is

\[
\frac{n!A_4(n)}{12}.
\]

The Python exhaustive run recomputed both sides through `n=9`. At `n=9`, for example, it found 9 AP
subsets and 272,160 total incidences, exactly `9!*9/12`. It also checked preservation under value
complement and positional reversal, first-value complement symmetry, and every two-prefix orbit.

## 6. Translation of the prior exact table

Goh-Zhao define an ordering as a bijection from `[1,n]` to the additive set and define `L(sigma)` as
the longest arithmetic-progression subsequence, allowing positive or negative nonzero step. Let
`f_n(k)` count orderings of `[1,n]` with `L(sigma)=k`. A progression of length at least four contains
a four-term progression, so

\[
\theta_4(n)=f_n(1)+f_n(2)+f_n(3).
\]

The exact translation from the public arXiv v2 Table 1 is:

| n | f_n(1) | f_n(2) | f_n(3) | theta_4(n) |
|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 1 |
| 2 | 0 | 2 | 0 | 2 |
| 3 | 0 | 4 | 2 | 6 |
| 4 | 0 | 10 | 12 | 22 |
| 5 | 0 | 20 | 82 | 102 |
| 6 | 0 | 48 | 516 | 564 |
| 7 | 0 | 104 | 3,232 | 3,336 |
| 8 | 0 | 282 | 21,984 | 22,266 |
| 9 | 0 | 496 | 168,368 | 168,864 |
| 10 | 0 | 1,066 | 1,306,404 | 1,307,470 |
| 11 | 0 | 2,460 | 11,064,306 | 11,066,766 |
| 12 | 0 | 6,128 | 101,355,594 | 101,361,722 |

`code/check_goh_zhao_prefix.py` parsed these rows from the frozen TeX source, checked that each full
distribution row sums to `n!`, and checked the translated prefix against the author table. All 12
rows pass.

Source identities:

| artifact | SHA-256 |
|---|---|
| peer-reviewed INTEGERS 21 (2021) PDF, table through n=10 | `258b9a4f11de613c2efb80c9287d8cbcb0dd4e6aaa9f23dd4863d3dee97106d2` |
| arXiv v2 PDF, table visibly through n=12 | `7df4b770fe9ebcbe5ac19e0500c6fd372879255b6c3d0f4fb320577c14bed4d2` |
| arXiv v2 source tar | `8d3c0e72339252d4926554a907fb9faa37b28ef8d3fec22a06263dcf542c97ac` |
| extracted v2 `ap-permsout.tex` | `f4e649978b78dd4493875dbecccf235cfc5fde5f8c1df108965bcfe3b7053a72` |
| current arXiv PDF retrieved 2026-08-11 | `5a7d4a08fbe1d4b19c57d26639938ff682208ddd89afec3f12e85df207b83f03` |

The v2 TeX rows are at lines 458-469. Lines 420-425 say `n<=10`; the extra `n=11,12` rows are still
unambiguously present in both source and rendered PDF. The peer-reviewed version removes those two
rows. Search-engine, exact-value, exact-prefix, arXiv, and OEIS-indexed searches did not locate a
public `n=13` or `n=14` table. Direct OEIS search returned HTTP 403 in this environment. These are
documented search misses only.

The most recent inspected primary paper, Gaiser-Horn, *Subsequence Sums in Permutations* (submitted
27 May 2026), states that the positive-integer monotone 4-AP question remains open. Its frozen PDF
hash is `363eb2c2f7e9b901322e4a682c9cda2246af7d738f9270ea99efb1edf1147f0a`.

## 7. Bundle, build, overflow, and sanitizer audit

### Frozen author artifact

- Author manifest SHA-256:
  `033285315598188a76523d42a53d6a367bf9d3ca08a173276f39c8df7a89bf4d`.
- Author tarball SHA-256:
  `e51d912d6c6c7f979e144150410f0ceb00700b53291a7c519a9056498f633b1a`.
- The manifest contains 37 unique file records; together with the manifest the bundle has 38 regular
  files and no symlinks.
- All hashes pass. Extraction of the tarball is byte-identical to `bundle_ro` under recursive diff.
- Files/directories are frozen at modes 444/555.

The author source compiled with `-Wconversion -Wshadow -Werror` in addition to its published flags.
The rebuilt binary was byte-for-byte identical to the frozen binary:

`7d646c337b6b7f72fb684561d8b1da69600c3ebbc1400a52aae23c826ab29a6a`.

The complete frozen `reproduce.sh 14 10 16` run reported zero manifest, direct-cross-check, Python,
count-log, and reproduction discrepancies. It took 109.43 seconds overall; the optimized `n=14`
stage took 96.031 seconds.

### Numeric widths

At the frozen scope, `14! = 87,178,291,200 < 2^37`. Every subtree total and final count is at most
`14!`. The author's `unsigned __int128` therefore has enormous headroom. The audit enumerators use
`uint64_t`, which is also sufficient. The final `n=14` answer exceeds `2^32`, so narrowing it to a
32-bit counter would be wrong; no such narrowing occurs.

The automaton validates `n<=14`, uses only shifts through bit 13, and has at most 52 oriented words,
well within its byte word IDs. The insertion verifier validates `n<=14`, and its fixed 15-byte
position array covers values `0,...,13`. Integer loop arithmetic is bounded by this input gate.

### Diagnostics

- Strict optimized builds of all three C++ sources emitted no warning.
- AddressSanitizer plus UndefinedBehaviorSanitizer serial runs of both independent programs passed
  through `n=9`.
- The author program passed the same sanitizers, including direct checking, through `n=10`.
- The only sanitizer-build message was the expected warning that the OpenMP pragma is ignored in a
  deliberately serial build.
- OpenMP thread-count controls passed as described above.

Portability caveat: byte-identical rebuilding is specific to the stated Ubuntu/GCC/x86-64 VM.
`unsigned __int128` is a GCC/Clang extension, OpenMP must be available for the parallel build, and
`-march=native` intentionally produces a host-specific binary. These do not affect the stated run,
but a portable public source release should omit `-march=native` and avoid promising binary identity.

## 8. Live gate and site collision

A final Bright Data browser capture of `https://www.erdosproblems.com/196` on 2026-08-11 displayed:

- `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- three comments and no claimed solution.

The capture SHA-256 is
`62fa5d20a844734db5389cd2fc805e5b969f85d5b85fdc060ad21aa4b9c3dade`.

The current site source and frozen snapshots were checked for the actual `problemNum: 196` and
`n: 196` schemas, Erdos Problem 196 URLs/prose, `theta4`, and the monotone-4-AP framework. All counts
were zero. The final current-source identities were:

| file | SHA-256 |
|---|---|
| `ErdosProblemADay/src/index.js` | `f367fac843b163557e7a60b9b3c9ea92cc4c9d1a862c0eddc4f989575b689327` |
| `ErdosProblemADay/src/ledger_data.js` | `9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052` |

The author collision script does not inspect the site's actual `problemNum` field. This is a real
checker gap, but it is non-load-bearing because the independent strict checker does inspect it and
finds no collision.

Two full site snapshots inside the author bundle are also non-load-bearing and should be omitted
from any public copy while their exclusions are recorded:

| frozen path | bytes | SHA-256 |
|---|---:|---|
| `provenance/site_index_20260811.js` | 413,456 | `b7111451218492db6756cc88dde0a8b98700d4c6f47e476171a02950b6d9af8b` |
| `provenance/site_ledger_data_20260811.js` | 6,421,993 | `9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052` |

Do not mutate the frozen bundle to remove them: make a derived public package with an explicit
exclusion record. Neither snapshot is used by the mathematical computation.

## 9. Exact gap to the infinite problem

Davis, Entringer, Graham, and Simmons already constructed a doubly infinite ordering of the positive
integers with no monotone four-term AP. Restricting that order to `[n]` immediately proves
`theta_4(n)>0` for every finite `n`, without this computation. Their paper explicitly leaves the
singly infinite problem open, and the 2026 Gaiser-Horn paper says it remains open.

A coherent family of finite avoiding orders, or a compactness argument applied to the finite orders,
produces an AP-avoiding total order on the positive integers. It does not ensure that this order has
type `omega`. A singly infinite permutation induces a total order in which every element has only
finitely many predecessors; a doubly infinite order can have infinitely many predecessors. None of
the counts, recursions, incidence identities, or finite symmetries controls predecessor sets in an
infinite limit.

Consequently this audit certifies an exact finite enumeration only. It supplies no infinite
permutation, no obstruction proving every singly infinite permutation contains a monotone 4-AP, no
asymptotic estimate for `theta_4(n)`, and no advance on the order-type gap at the heart of Problem
196.

## 10. Audit artifacts

Load-bearing logs:

- `logs/author_reproduce_n14.log`
- `logs/automaton_n14.log`
- `logs/insertion_n14.log`
- `logs/exhaustive_controls.log`
- `logs/goh_zhao_prefix_check.log`
- `logs/author_thread_matrix_n12.log`
- `logs/author_strict_rebuild.log`
- `logs/audit_sanitizer_n9.log`
- `logs/author_sanitizer_n10.log`
- `logs/author_tar_integrity.log`
- `logs/site_collision_current_final_strict.log`
- `provenance/live_196_final_20260811.txt`

`code/verify_audit_logs.py` checks every numerical log against `expected_counts.tsv` and requires the
status/gate sentinels. `reproduce.sh check` verifies both manifests, the author file set, all frozen
logs, and byte-identical strict rebuilds. `reproduce.sh full` additionally reruns both independent
`n=14` computations and the complete author workflow.

**Final split verdict: computational core PASS; frozen literature/publication narrative GAP. A
corrected public finite result may safely state the exact table through `n=14`, credit the public
Goh-Zhao prefix through `n=12`, and describe only `n=13,14` as search-limited extensions.**
