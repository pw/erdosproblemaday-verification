# Exact finite record extension for Erdos problem 222

Status: PASS.  The baseline, two primary post-anchor runs, separately written
post-anchor implementation, and local proof certificate all pass.

Audit date: 2026-08-11 UTC.

## Exact finite claim

Let

```text
S = {a^2 + b^2 : a,b are integers}.
```

The current OEIS record tables A297350 and A357018 end with a gap of 107
starting at 99,951,600,293, or 106 consecutive interior integers outside S.
An exhaustive baseline enumeration from 0 independently verifies that this is
the unique largest gap through its represented right endpoint 99,951,600,400.
A second exhaustive enumeration continues from the represented record start
through the represented endpoint 200,000,000,000 and proves:

1. The next record is

   ```text
   133858454292, 133858454404
   ```

   with difference 112, so all 111 integers strictly between the endpoints are
   outside S.
2. This is the first global gap of difference at least 108.
3. No gap ending at or before 200,000,000,000 has difference greater than 112.
4. The only gaps of difference at least 108 in the closed scanned interval are

   ```text
   112  133858454292  133858454404
   108  190766104961  190766105069
   ```

Equivalently, the finite extension proposed for A297350 is 133,858,454,292 and
the corresponding extension proposed for A357018 is 111.

This is only a bounded exact statement.  It makes no claim about the next
record after 200,000,000,000 and no asymptotic claim.

## Exhaustive enumeration proof

`sum2sq_gap_scan.cpp` divides a closed interval into disjoint chunks.  In a
chunk `[lo,hi]`, it enumerates every pair `0 <= a <= b` for which
`lo <= a^2+b^2 <= hi`, marks the corresponding integer in a packed bit vector,
and reads the marked positions in increasing order.  Every integer sum of two
integer squares has a representation with nonnegative reordered coordinates,
so this marks every member of S in the chunk.  Conversely, every mark is
created by an explicit pair and is in S.

Integer square-root estimates are corrected in both directions with exact
128-bit products.  Within-chunk gaps and each gap from the last mark of one
nonempty chunk to the first mark of the next are compared.  Therefore a gap
cannot be lost at a chunk boundary, even if a chunk were empty.

Four complete runs used different scopes, partitions, and thread counts:

| implementation | chunk width | chunks | threads | represented count | max gap |
|---|---:|---:|---:|---:|---:|
| primary, baseline 0..99,951,600,400 | 100,000,003 | 1,000 | 10 | 15,563,133,098 | 107 |
| primary | 100,000,000 | 1,001 | 12 | 15,137,795,993 | 112 |
| primary, reporting >=108 | 123,456,789 | 811 | 11 | 15,137,795,993 | 112 |
| independent, reporting >=108 | 33,333,331 | 3,002 | 2 | 15,137,795,993 | 112 |

The baseline reports exactly one gap of at least 107, namely
99,951,600,293..99,951,600,400.  The final row reports exactly the two gaps
listed above.  The distinct non-round chunk widths move all boundaries between
runs.

`sum2sq_gap_scan_independent.cpp` was written separately.  It transposes the
enumeration: the larger coordinate `b` is the outer loop, exact bounds for the
smaller `a` are derived for each `b`, and a byte array rather than packed words
stores membership.  It uses a third chunk width, 33,333,331, and static rather
than dynamic scheduling.  Its full-range count, endpoints, maximum, and entire
list of gaps of size at least 108 agree exactly with the primary implementation.

Both closed scan endpoints are represented:

```text
99951600293  = 107377^2 + 297358^2
200000000000 = 200000^2 + 400000^2.
```

Thus the enumeration has no open-boundary ambiguity for gaps ending within the
claimed frontier.

## Direct certificate for the new gap

The new endpoints have explicit representations:

```text
133858454292 = 49986^2 + 362436^2
133858454404 = 35298^2 + 364160^2.
```

`gap_133858454292_133858454404.cert` has exactly 111 rows `[n,p,e]`, one for
each interior integer in increasing order.  Each row asserts that `p` is prime,
`p == 3 (mod 4)`, and the exact p-adic valuation of `n` is the odd integer `e`.

The obstruction used here needs only the elementary necessary half of the
two-square theorem.  If a prime `p == 3 (mod 4)` divides `x^2+y^2`, then it
divides both `x` and `y`: otherwise `-1` would be a quadratic residue modulo p.
After dividing by `p^2` and repeating, the valuation of p in a sum of two
squares must be even.  An exact odd valuation therefore proves that the
certified integer is not in S.

Two independent certificate checkers pass:

- `verify_gap_certificate.py` uses the deterministic seven-base Miller--Rabin
  test valid on 64-bit inputs and computes exact valuations by division;
- `verify_gap_certificate.gp` uses PARI/GP `isprime` and `valuation` and also
  checks the endpoint arithmetic.

Their frozen logs are:

```text
PYTHON_CERTIFICATE_PASS rows=111 endpoints=133858454292,133858454404 gap=112
PARI_CERTIFICATE_PASS rows=111 endpoints=133858454292,133858454404 gap=112
```

The certificate proves this particular gap without trusting either exhaustive
scanner.  The exhaustive scans are still necessary for the record and frontier
claims, namely that no earlier or larger gap was skipped.

## Small-range decorrelation test

`verify_small_frontier.py` classifies every integer through 1,000,000 by an SPF
factorisation and the two-square prime-exponent criterion.  It agrees with both
annulus implementations on all headline values:

```text
SMALL_FRONTIER_PASS method=spf_factor_criterion range=0..1000000
represented=216342 max_gap=35 endpoints=685541,685576 scanners=2
```

This test uses neither scanner's coordinate-enumeration method.

Both C++ sources were also rebuilt with AddressSanitizer and
UndefinedBehaviorSanitizer and rerun through 1,000,000.  The frozen
`sanitizer_smoke.log` is clean and ends with `SANITIZER_SMOKE_PASS`.
`static_build.log` records warning-clean builds under `-Wall -Wextra` and
successful bytecode compilation of all five Python scripts.

## Frozen evidence

Primary run summaries:

- `baseline_scan_0_99951600400.out`
- `scan_99951600293_200000000000.out`
- `scan_report_99951600293_200000000000.out`
- `independent_scan_99951600293_200000000000.out`

Detailed chunk logs and GNU `time -v` records:

- `baseline_scan_0_99951600400.err`
- `scan_99951600293_200000000000.err`
- `scan_report_99951600293_200000000000.err`
- `independent_scan_99951600293_200000000000.err`

The baseline took 106.67 seconds wall time and 782.94 seconds user time.  The
two post-anchor primary runs took 71.10/841.30 and 92.47/862.43 seconds
wall/user time.  Their maximum RSS values were 126,124 KiB, 150,408 KiB, and
169,048 KiB.  The two-thread independent run, deliberately overlapped with
other machine load, took 762.85 seconds wall time and 1,132.04 seconds user
time with 69,392 KiB maximum RSS.  All four runs exited 0.

See `PROVENANCE.md` for the live-page, OEIS, primary-source, novelty-search,
and site-collision audit.  `MANIFEST.sha256` hashes the frozen bundle after all
full-range outputs and verification logs were completed.

## Reproduction

```bash
g++ -O3 -march=native -fopenmp -std=c++17 sum2sq_gap_scan.cpp \
  -o sum2sq_gap_scan
env OMP_NUM_THREADS=10 ./sum2sq_gap_scan \
  0 99951600400 100000003 107
env OMP_NUM_THREADS=12 ./sum2sq_gap_scan \
  99951600293 200000000000 100000000
env OMP_NUM_THREADS=11 ./sum2sq_gap_scan \
  99951600293 200000000000 123456789 108

g++ -O3 -march=native -fopenmp -std=c++17 \
  sum2sq_gap_scan_independent.cpp -o sum2sq_gap_scan_independent
env OMP_NUM_THREADS=2 ./sum2sq_gap_scan_independent \
  99951600293 200000000000 33333331 108

python3 verify_small_frontier.py
python3 verify_gap_certificate.py
gp -q verify_gap_certificate.gp
python3 verify_frozen_outputs.py
python3 audit_site_gate.py
```

Measured environment: GCC 13.3.0, Python 3.12.3, PARI/GP 2.15.4, Linux x86-64.
