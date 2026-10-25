# Hostile audit of the `k(18)` certificate

Date: 2026-08-11 UTC

## Verdict

**PASS**, within the explicitly computational scope of this bundle:

```text
33 <= k(18) <= 35.
```

No load-bearing gap was found in the elementary certificates, recurrence,
finite searches, arithmetic, frontier partition, terminal scan, or captured
reproduction. This remains a finite computational result, not a resolution of
the exact value of `k(18)` or the asymptotic Erdos problem.

## Integrity and reproduction

Every entry in the original frozen archive manifest verified. That original
manifest had SHA-256

```text
8852ceb698ae6ff8b6788c0397a7041de2fe7c28b42dab575eadaf70dcadacde
```

The audited source hashes were:

```text
ee68d0ced8cdbb39a97f763c8f93fb2cfc91259148adb7497916088ca18c035e  verify_k18_gmp.cpp
f6e1f13252d60f42d6ff72cc60ac9901f0641992e00d2e38d32f91c06ca99c3d  verify_k18_fraction.py
0a84d4373381351c912127cd40bf884e241feb9cbf573367ea0c9043b1d2651c  check_k18_upper.py
6d74721f713fce0afa3299d44ef7f602d499c0cd33323d6fac12a97e917e8ddd  reproduce.sh
```

A fresh optimized build was byte-identical to the archived executable, with
SHA-256 `103f5d935f125c0814d90428f76c640e6eaf60950af7711446fa35fe9ba5f592`.
The nonportable executable is omitted from this publication bundle; it is
rebuilt by `reproduce.sh`.

The complete reproduction was run again from this publication directory. It
ended with `reproduction=PASS`; the output is frozen in
`reproduction_2026-08-11.log`.

## Exact search results

Both engines reproduced the same completed-search counters:

| terms | engine | states | two-term states | scanned `x` values | result |
|---:|:---|---:|---:|---:|:---|
| 31 | GMP | 20,293 | 13,139 | 69,727 | none |
| 31 | Fraction | 20,293 | 13,139 | 69,727 | none |
| 32 | GMP | 14,678,224 | 11,753,049 | 114,603,091 | none |
| 32 | Fraction | 14,678,224 | 11,753,049 | 114,603,091 | none |

A separate 32-term Fraction run with `procs=1` removed the depth-two
multiprocessing split and returned the same three counters. A GMP run with
one thread and frontier depth zero removed both task partitioning and worker
concurrency and also returned the same 32-term counters. Additional frontier
depth and thread-count variations agreed.

## Recurrence audit

For a positive reduced remainder `R=a/b`, next lower bound `L`, and `t>=2`
terms left, every completion has first denominator `d` in

```text
max(L, floor(b/a)+1) <= d <= floor(t*b/a).
```

The lower endpoint is strict because another positive term remains. The upper
endpoint follows because all `t` reciprocals are at most `1/d`. Thus every
interior loop is finite without an external denominator cutoff.

The exact tail

```text
H(L,t) = 1/L + ... + 1/(L+t-1)
```

is the largest possible sum of `t` distinct allowed reciprocals. The child
prune `H(d+1,t-1) < R-1/d` is therefore sound. After adding `1/d`, this is
`H(d,t) < R`; since `H(d,t)` strictly decreases with `d`, changing later
failed-child handling from `continue` to `break` omits no completion.

The one-term unit-fraction test is exact. For two terms, every possible first
denominator lies in

```text
max(L, floor(b/a)+1) <= x <= floor(2*b/a),
```

and the second is forced to be

```text
y = b*x/(a*x-b).
```

The programs test exact divisibility and `y>x`. They impose no bound on `y`.
As a direct stress test, both implementations found the state

```text
1/100 + 1/10^100
```

from `lower=100` in one scanned candidate, returning denominators
`[100, 10^100]`. A separate 2,000-case fuzz comparison matched the linear
terminal scan against enumeration through the divisor identity
`(a*x-b)(a*y-b)=b^2` in every case.

These bounds, the exact tail rejection, and the terminal tests prove by
induction that every increasing expansion of the requested length is visited
or soundly rejected.

## Arithmetic and concurrency audit

- GMP rationals and Python `Fraction` provide exact branch comparisons and
  divisibility tests. C++ floating point is only a gate before the exact GMP
  prune, so it can retain extra work but cannot delete a valid branch.
- The C++ native terminal fast path is entered only when all operands fit
  `unsigned long`. Its products use `unsigned __int128`; otherwise the scan
  remains in GMP integers.
- Temporary full-run instrumentation measured maximum recursive `lower=131`
  and maximum interior loop endpoint 131. Maximum terminal numerator and
  denominator sizes were 88 and 93 bits, exercising the GMP fallback. The
  observed counters and task counts are far below their native widths.
- The C++ frontier is constructed before workers start. Immutable tasks are
  assigned by one atomic index, caches are thread-local, and each worker owns
  its counter object. Because the result is unsatisfiable, the early-stop flag
  is never set and all tasks are consumed.
- Python constructs disjoint depth-two prefix tasks and consumes every
  `imap_unordered` result. Parent-side prefix counts plus worker counts agree
  with the serial traversal.
- A fresh full 32-term AddressSanitizer and UndefinedBehaviorSanitizer run
  returned the exact counters with no diagnostic. The archived run in
  `erdos295_k18_gmp_sanitizer_terms32_2026-08-11.log` records the same result.
- A ThreadSanitizer run on the multi-task 31-term frontier returned the exact
  counters with no race diagnostic.

## Elementary certificates

Independent integer-LCM addition checked the 35 increasing denominators. Its
common denominator and scaled numerator were both

```text
24837411097699200.
```

Thus the reciprocal sum is exactly 1. The four inserted denominators replace
`1/17` exactly and do not collide with the other source denominators.

The largest reciprocal sum from at most 30 distinct denominators at least 18
is attained by 18 through 47. Exact arithmetic gives

```text
442017301628992345493 / 442720643463713815200 < 1.
```

This excludes every length through 30 without computation. The exhaustive
31- and 32-term exclusions then give `k(18)>=33`; the identity gives
`k(18)<=35`.

## Non-load-bearing caveats

- The GMP and Fraction programs share the same mathematical recurrence
  lineage. Their agreement is a strong arithmetic and implementation
  cross-check, but not a second cold-room mathematical method.
- The optional C++ factorization code calls a probabilistic primality test.
  It is outside the proof path: every audited 31/32 run reports
  `factored_states=0`, so every terminal interval was scanned directly.
- The C++ CLI is not certified for arbitrary parameters. Native-width
  endpoints, malformed input, and very small term counts are outside this
  result. Instrumentation establishes that the packaged runs are far from the
  relevant limits.
- A different platform's floating prefilter can retain different extra work,
  so exact counters may be platform-sensitive. The final no-solution result
  remains sound because every deletion requires an exact comparison.
- The lower bound is conditional on ordinary successful execution of the
  frozen programs. The manifest, captured logs, independent arithmetic checks,
  sanitizer checks, and package-local reproduction make that computation
  inspectable and repeatable; they do not turn it into a short hand proof.

Within those stated limits, the bundle passes.
