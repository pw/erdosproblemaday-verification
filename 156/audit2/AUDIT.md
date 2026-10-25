# Cold audit 2: Problem 156 / A382397 exact values 66 through 95

Date: 2026-08-11 UTC

## Verdict

**PASS.** The frozen bundle rigorously proves

```text
a(66) = a(67) = 6,
a(n) = 7 for 68 <= n <= 95.
```

This is an exact finite extension of OEIS A382397, not a solution or an
asymptotic improvement to Erdos Problem 156. Novelty is search-qualified only.

The frozen report has SHA-256
`f5828c4234b9c163c294e2890a80fca5fb8f05ba3af57aa6e49618e6d6d4e1cc`.
Its manifest has SHA-256
`491d5683f8d1b5e5ca196a59fd61b7bd94a574b5df659cf25397e74d14e2f351`,
and all ten entries pass `sha256sum -c`.

## Current source check

Checked directly on 2026-08-11:

- The current OEIS entry defines A382397 as the minimum size of a maximal
  subset of `{1,...,n}` having distinct positive differences. Its comment
  explicitly gives the equivalent convention of distinct unordered pair sums
  with repetition. The current b-file contains exactly `n=0..65`, ends in
  `65 6`, and has SHA-256
  `04af52cd250baff9c7247481747389e448942eccfc0e324dc996d0073cc28b29`.
  Sources: <https://oeis.org/A382397> and
  <https://oeis.org/A382397/b382397.txt>.
- The primary ESS94 abstract defines a Sidon set by uniqueness of `a+a'` for
  `a<=a'`: <https://doi.org/10.1006/jnth.1994.1040>.
- The current Problem 156 page says `OPEN`, explicitly says a finite
  computation cannot resolve it, and reports no claimed partial or complete
  solution: <https://www.erdosproblems.com/156>.
- A fresh clone of <https://github.com/teorth/erdosproblems> was at commit
  `579b259ef6b1392637427292273edd1e14440045`; `data/problems.yaml` still marks
  156 open and links A382397.
- Four targeted current searches for A382397 with 66, 67, 68, GitHub, and the
  finite maximal-Sidon wording found no published extension. This supports only
  a search-qualified novelty statement, never an absolute one.

One non-mathematical wording correction is recommended: frozen-report line 39
says the OEIS page was last modified on 2026-08-10. The displayed footer is a
volatile site-wide OEIS timestamp, not the A382397 revision date. The sequence
revision shown by OEIS is #14, dated 2025-09-10. Omit the volatile date.

## Proof audit

The definitions and blocking lemma are at frozen-report lines 54-89.

1. Distinct positive differences and distinct unordered sums with repetition
   are equivalent. A repeated difference `a-b=c-d`, with both differences
   positive, gives `a+d=c+b`. Conversely, from a nontrivial equality
   `p+q=r+s`, order the pairs so `p<r`; then `q-s=r-p>0`. The only way the
   resulting sum pairs or difference pairs are identical is the trivial
   equality already excluded.
2. For Sidon `A` and `x` outside `A`, the only new sums are `x+a` and `2x`.
   The sums `x+a` are mutually distinct, and `x+a=2x` would force `a=x`.
   Therefore insertion fails exactly when `x+a=s` or `2x=s` for an old sum
   `s`. This is precisely the displayed `B(A)`. The difference form follows by
   checking collisions of each `|x-a|` with an old positive difference and
   collisions between two new differences, the latter occurring exactly at a
   midpoint. Since the Sidon property is hereditary, single-point insertion is
   also equivalent to inclusion-maximality.
3. If `m=min(A)` and `R=A-m`, then `B(A-m)=B(A)-m`: old sums translate by
   `-2m`, so both `s-a` and even half-sums translate by `-m`. The translated
   domain is `[1-m,n-m]`, has length `n`, and contains `[0,L]`, where
   `L=max(R)`. It can be wholly blocked exactly when it lies in the consecutive
   blocked component containing `[0,L]`. Hence its length is at most that
   component's run length. Conversely, every subinterval of that component
   containing the hull translates back to a maximal set in an interval of the
   same length. This proves frozen-report lines 91-128.
4. For `n<=95`, every normalized candidate has maximum mark at most 94. Each
   size-`k` candidate is uniquely `{0}` plus a `(k-1)`-subset of `{1,...,94}`.
   Thus the complete raw count is `C(94,k-1)`. A repeated difference or sum in
   a prefix cannot be repaired by later marks, so both frozen prefix prunes are
   sound.

The reported maximum blocked-run lengths for sizes 1 through 6 are
`1,4,10,22,42,67`. Consequently sizes at most 5 are impossible at 66 and 67,
while the two six-mark witnesses prove equality there. A size at most 6 is
impossible for every domain length 68 through 95, while the listed seven-mark
witnesses prove the matching upper bounds.

## Frozen code audit

The difference engine's complete enumeration is in `verify_156_a66.cpp`, lines
48-58 and 133-150; its exact blocked-run and placement scans are lines 60-131.
For the frozen `N=66,67,95` runs, every `unsigned __int128` shift is in
`1..94`. Coordinates lie in `[-94,188]`, with allocated false sentinels at
`-95` and `189`. Counts are far below `uint64_t`; digest overflow is unsigned
and defined. All other arithmetic is tiny signed `int` arithmetic.

The sum engine's direct prefix check is in `audit_156_size6_sums.cpp`, lines
41-52, and its blocked-set construction and scan are lines 54-97. Sum indices
are exactly `0..188` in a 189-bit bitset. Its recursive bounds at lines 99-111
enumerate each normalized combination once. No out-of-range index, signed
overflow, uninitialized read, or incomplete prune was found in either engine.

Both frozen engines were rebuilt with GCC 13.3 using
`-O2 -Wall -Wextra -Wconversion -D_GLIBCXX_ASSERTIONS -fsanitize=undefined
-fno-sanitize-recover=all`. The diameter-94 runs exited zero with the frozen
counts and no sanitizer finding. The difference run took 35.53 seconds and the
sum run 36.20 seconds. A separate `N=67` sanitized build found exactly two
six-mark placements and concluded `a(67)=6`.

## Third enumeration

`sidon_audit2_third.cpp` is intentionally decorrelated:

- it visits every full combination, with no Sidon prefix prune;
- it rebuilds positive differences at each leaf rather than maintaining either
  frozen representation; and
- it decides blocking by directly trying to insert `x` into the difference set,
  rather than constructing either algebraic formula for `B(A)`.

It visited 58,079,029 raw normalized sets. The totals were 33,158,929 Sidon
sets and 21,355 hull-covered sets. Every per-size count, first extremizer,
blocked interval, and best run matches both frozen engines. The source has
SHA-256 `6eb71e3d11d65522018463ffc8a132df6d2a0d2cb83d8424e46ddf5351580e50`.
The optimized run took 2.65 seconds; an assertion-enabled UBSan build also
passed.

## Witness replay

`witness_replay.py` independently uses the positive-difference convention. It
checks all 30 witnesses, all 618 base difference pairs, and every one of the
2,207 outside insertions. Those enlarged sets contain 60,949 difference pairs.
Every insertion fails. Its compact transcript digest is
`35c29abd065c58c2e70f7232adab30edcec97ed616355d3d3ad4d64887b12edb`.

## Reproduction

From `/home/exedev/erdos_scratch`:

```bash
sha256sum -c erdos156_A382397_exact_66_95_manifest_2026-08-11.sha256

g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -pedantic \
  sidon_audit2/sidon_audit2_third.cpp -o /tmp/sidon_audit2_third
/tmp/sidon_audit2_third

python3 sidon_audit2/witness_replay.py
```

The expected outputs are frozen in `third_enumeration.log` and
`witness_replay.log`.

## Residual risk

- Exhaustive computation is not a machine-checked formal proof. Three
  differently structured exact engines, sanitizer builds, and direct witness
  replay substantially reduce ordinary implementation risk.
- The novelty search is not an exhaustive literature proof.
- Nothing here applies beyond `n=95` or removes the logarithm in the known
  asymptotic construction. The parent problem remains open.
- No site source was edited during this audit.
