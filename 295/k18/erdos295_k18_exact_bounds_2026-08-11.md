# Erdős problem 295: exact computational bounds for `k(18)`

Date: 2026-08-11 (UTC)

## Result and claim labels

Let `k(N)` be the least `k` for which there are integers

```text
N <= n_1 < n_2 < ... < n_k
```

such that `sum_i 1/n_i = 1`.  This bundle proves

```text
                         33 <= k(18) <= 35.
```

The upper bound and the harmonic cutoff are elementary exact identities,
labelled **[E]** below.  The exclusions of 31 and 32 terms are finite,
exhaustive, exact-arithmetic computations, labelled **[C]**.  Thus the lower
bound is rigorous conditional on ordinary execution of the frozen programs,
but it is a computational result rather than a hand-checkable proof.  This
does not resolve whether `k(18)` is 33, 34, or 35, and it does not resolve the
asymptotic question in Erdős problem 295.

## Upper certificate: `k(18) <= 35` [E]

The following 35 denominators are strictly increasing and all at least 18:

```text
18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
34, 35, 36, 38, 39, 40, 42, 43, 44, 45, 48, 50, 52, 54, 63, 640,
337280, 1735650, 68479214496
```

Their reciprocal sum is exactly 1.  One construction starts with the checked
32-term identity

```text
17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33,
34, 35, 36, 38, 39, 42, 43, 44, 45, 48, 50, 52, 54, 63,
1735650, 68479214496
```

and replaces `1/17` by four new terms.  The replacement has the transparent
common-denominator certificate

```text
1/31 + 1/40 + 1/640 + 1/337280
  = (10880 + 8432 + 527 + 1) / 337280
  = 19840 / 337280
  = 1/17.
```

None of the four inserted denominators occurs among the other 31 source
denominators.  `check_k18_upper.py` independently checks both complete sums,
the surgery, cardinality, minimum, strict ordering, and the harmonic cutoff
using Python's exact `fractions.Fraction` arithmetic.  Its captured output is
`erdos295_k18_upper_check_2026-08-11.log`.

## The elementary cutoff through 30 terms [E]

For any `t` distinct integers `18 <= x_1 < ... < x_t`, monotonicity gives

```text
sum_i 1/x_i <= sum_{j=18}^{17+t} 1/j.
```

At `t=30`, the right side is exactly

```text
442017301628992345493 / 442720643463713815200 < 1.
```

Consequently no expansion with at most 30 terms exists.  (For orientation,
the sum from 18 through 48, containing 31 terms, is greater than 1, so the
remaining two lengths require search.)

## Exhaustive recursion [E]

A state is `(R,L,t)`: the positive rational remainder is `R`, exactly `t`
terms remain, and the next denominator must be at least `L`.  Define

```text
H(L,t) = 1/L + 1/(L+1) + ... + 1/(L+t-1).
```

This is the largest sum of `t` reciprocals of distinct integer denominators
at least `L`.  Therefore `H(L,t) < R` certifies that the state is impossible.

Suppose `t >= 2` and the first new denominator is `d`.  Every completion must
satisfy

```text
max(L, floor(1/R)+1) <= d <= floor(t/R).                 (1)
```

The lower inequality holds because `t-1` positive terms remain, so `1/d<R`.
The upper inequality follows because every one of the `t` denominators is at
least `d`, whence `R <= t/d`.  Thus every interior loop is finite without any
external upper bound on denominators.

After choosing `d`, the child can be discarded exactly when

```text
H(d+1,t-1) < R-1/d.                                     (2)
```

Moreover, once (2) holds, the loop may stop: its equivalent left side after
moving `1/d` is `H(d,t) < R`, and `H(d,t)` is strictly decreasing in `d`.
Hence all later choices also fail.

When `t=1`, a completion exists exactly when `R` is a unit fraction whose
denominator is at least `L`.  When `t=2`, write the reduced remainder as
`R=a/b`.  The program enumerates every integer

```text
max(L, floor(b/a)+1) <= x <= floor(2b/a)
```

and computes the forced second denominator

```text
y = bx/(ax-b).
```

It accepts exactly when this is an integer and `y>x`.  In particular, `y` is
not capped, so the computation is not a bounded-denominator search.

Equations (1) and (2), the one-term test, and the forced two-term formula prove
by induction on `t` that the recursion visits or soundly rejects every
strictly increasing expansion of the requested length.

## Frozen implementations [C]

`verify_k18_gmp.cpp` uses GMP integers and rationals.  It first enumerates an
exact static frontier and then assigns each surviving frontier state exactly
once using an atomic task index.  In these unsatisfiable runs no early-stop
flag is set, so all tasks are consumed.  A floating-point tail value is only
a one-sided prefilter: a branch is deleted only after the exact GMP comparison
also proves (2).  A bad floating approximation can therefore retain extra
work but cannot remove a valid branch.

The GMP program contains an optional factor/divisor method for unusually wide
two-term intervals.  Both `k(18)` runs report `factored_states=0`, so every
terminal interval here was checked by direct linear scan; the factorization
code is outside the executed proof path.

`verify_k18_fraction.py` uses Python arbitrary-size integers and
`fractions.Fraction`, a depth-two multiprocessing split, exact harmonic tails,
and only a linear terminal scan.  It shares the mathematical DFS above but not
the GMP implementation or arithmetic layer.  It is therefore a useful
implementation-separated audit, not a second independent mathematical method.
Its header records its derivation from the earlier banked Python lineage.

Successful results were:

| terms | engine | states | two-term states | scanned `x` values | result |
|---:|:---|---:|---:|---:|:---|
| 31 | GMP | 20,293 | 13,139 | 69,727 | none |
| 31 | Fraction | 20,293 | 13,139 | 69,727 | none |
| 32 | GMP | 14,678,224 | 11,753,049 | 114,603,091 | none |
| 32 | Fraction | 14,678,224 | 11,753,049 | 114,603,091 | none |

The identical counters are not assumed as a proof of completeness; they are a
cross-check on the two implementations of the proved recursion.  The exact
logs are:

```text
erdos295_k18_gmp_terms31_2026-08-11.log
erdos295_k18_gmp_terms32_2026-08-11.log
erdos295_k18_fraction_terms31_2026-08-11.log
erdos295_k18_fraction_terms32_2026-08-11.log
```

As a non-load-bearing runtime check, the complete 32-term GMP traversal was
also rebuilt with AddressSanitizer and UndefinedBehaviorSanitizer and again
returned the same counters and no solution, with no sanitizer diagnostic.
That run is captured in
`erdos295_k18_gmp_sanitizer_terms32_2026-08-11.log`.

The GMP verifier deliberately returns status 20 for a completed
unsatisfiable search and status 10 if it finds a solution.  The captured GNU
`time` message `Command exited with non-zero status 20` is therefore expected;
each log separately records `program_exit_status=20`.  Python returns 0 after
its completed no-solution traversals.

Combining the harmonic exclusion through 30 with both exact exclusions at 31
and 32 gives `k(18) >= 33` **[C]**.  Combining this with the explicit identity
gives `33 <= k(18) <= 35`.

## Reproduction and provenance

From this directory, run:

```bash
./reproduce.sh
```

The script rebuilds the C++ program, reruns both engines for lengths 31 and
32, and checks the upper certificate.  `erdos295_k18_build_2026-08-11.log`
records the frozen build environment and compiler invocation.
`SHA256SUMS` hashes the sources, frozen binary, report, and captured logs; the
manifest omits itself in the usual way.

The frozen binary was built on the x86-64 environment recorded in the build
log using GCC's `-march=native` and the GNU `unsigned __int128` extension.  It
is supplied for exact rerun provenance, not as a portable binary; the sources
should be rebuilt on another platform.

Provenance caveat: the GMP source is a frozen adaptation of the earlier
`verify_295_k17_independent.cpp`, and the Python header describes its earlier
banked lineage.  The implementations differ substantially in arithmetic,
parallel decomposition, and terminal handling, but they were not written as
two cold-room algorithms.  No heuristic 33- or 34-term exploration is used in
any claim in this report.

The upstream source hashes before the documentation-only adaptation were:

```text
16aba5c18a959760e60981c63da17faea0e880d0c7db7b8e4c2015bca4f6f8b6  verify_295_k17_independent.cpp
56b3b4ba1c8b1e455ab40e7de7dfe9659fb7503a2a63120efc61aee36e340658  erdos295_wave6_lineage2.py
```
