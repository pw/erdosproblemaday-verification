# Erdos problem #295: exact bounds for `k(18)`

This verification bundle supports the finite result

```text
33 <= k(18) <= 35.
```

It does not determine whether `k(18)` is 33, 34, or 35, and it does not
settle the asymptotic question in Erdos problem #295.

The upper bound is an exact 35-term identity. The lower bound combines the
elementary harmonic exclusion through 30 terms with exhaustive exact searches
excluding 31 and 32 terms. The computational claim passed a hostile source,
arithmetic, concurrency, sanitizer, and reproduction audit on 2026-08-11.

## Fast exact checks

From the repository root:

```bash
python3 verification/295/k18/check_k18_upper.py
(cd verification/295/k18 && sha256sum -c SHA256SUMS)
```

The first command checks the source identity, the four-for-one surgery that
removes denominator 17, the 35-term `k(18)` identity, strict ordering, and the
30-term harmonic cutoff using `fractions.Fraction`.

## Full reproduction

The full search requires a C++17 compiler, GMP development headers and
libraries, and Python 3:

```bash
verification/295/k18/reproduce.sh
```

The script rebuilds the GMP engine, runs both exact engines at 31 and 32
terms, checks every expected counter, and reruns the upper certificate. It
returns zero only after printing `reproduction=PASS`. Default runs use eight
C++ threads, twelve Python processes, and a depth-20 C++ frontier; these can
be changed with `THREADS`, `PYTHON_PROCS`, and `FRONTIER_DEPTH`.

Expected completed-search totals are:

| terms | engine | states | two-term states | scanned `x` values |
|---:|:---|---:|---:|---:|
| 31 | GMP and Fraction | 20,293 | 13,139 | 69,727 |
| 32 | GMP and Fraction | 14,678,224 | 11,753,049 | 114,603,091 |

The GMP executable deliberately returns status 20 for a completed
no-solution search and status 10 after finding a solution. `reproduce.sh`
checks and normalizes those statuses.

## Contents

- `AUDIT.md` records the hostile mathematical, implementation, concurrency,
  arithmetic, sanitizer, and reproduction audit.
- `erdos295_k18_exact_bounds_2026-08-11.md` gives the certificates,
  completeness proof, implementation description, results, and provenance.
- `verify_k18_gmp.cpp` is the threaded GMP search.
- `verify_k18_fraction.py` is the standard-library exact Fraction search with
  a separate multiprocessing split and terminal implementation.
- `check_k18_upper.py` checks the elementary upper certificate and cutoff.
- `reproduce.sh` rebuilds and reruns the complete package.
- `reproduction_2026-08-11.log` records a clean rerun from this publication
  directory.
- The other dated logs are the frozen build, search, sanitizer, and
  certificate records audited on 2026-08-11.

The original archival bundle also contained a nonportable x86-64 binary. It
is intentionally omitted here because `reproduce.sh` rebuilds from source.
The frozen report's binary-provenance paragraph refers to that complete
archival bundle. All copied report, source, and dated-log files remain
byte-identical to the audited originals.

## Scope and caveats

- The exclusions of 31 and 32 terms are computational certificates,
  conditional on ordinary execution of the frozen programs. The recurrence
  and every pruning inequality are proved in the report.
- The two engines share the same mathematical recurrence lineage. Their
  agreement cross-checks arithmetic, implementation, terminal handling, and
  parallel decomposition; it is not a second cold-room mathematical method.
- GMP floating point is only a prefilter. A branch is removed only after an
  exact rational comparison, so rounding can retain work but cannot create a
  false exclusion. Exact counters can therefore be platform-sensitive even
  when the no-solution result remains sound.
- The optional GMP factorization path uses probabilistic primality testing,
  but it is outside both proof runs: every 31/32 run reports
  `factored_states=0`, so all terminal intervals were scanned directly.
- The C++ generic CLI was audited only for the packaged `minimum=18`,
  `terms=31/32` runs. Arbitrary native-width endpoint and malformed/small-term
  inputs are outside this certificate.
- The frozen executable was built with GCC 13.3.0, `-march=native`, and GNU
  `unsigned __int128` on x86-64. Rebuild the source on other platforms.

`SHA256SUMS` covers every packaged artifact except itself.
