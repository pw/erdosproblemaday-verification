# Independent hostile publication audit: Erdős #840 finite proxy through 32

Date: 2026-08-12 UTC

## Verdict

**PUBLISH, with one wording correction.** The frozen bundle soundly certifies
the exact rows of

```text
s(k,n)=max{|A+A| : A subset [1,n], |A|=k}
```

for `n=28,...,32`, and independently reproduces the previously certified
`n=27` row. Together with the prior `n<=27` package this establishes the
project's exact finite frontier through 32. This is computational finite
progress only: Erdős Problem #840 remains open, and no asymptotic or novelty
claim follows.

The audited frozen bundle originally delegated rows below 27 to the prior
package. The publication copy has since included that prior Python checker and
its fresh transcript, and its public verifier reruns both computations. It is
therefore cumulatively self-contained; the integration wording still exposes
which checker supplies each range.

## Definition and table semantics

Translation sends each nonempty `A subset [1,n]` to `A-min(A)`, preserving
cardinality and sumset cardinality, with minimum zero and diameter at most
`n-1`. Conversely every such normalized set translates into `[1,n]`.
The producer's exact-diameter maxima followed by diameter-prefix maxima are
therefore exactly `s(k,n)`.

The sumset recurrence is exact:

```text
Sigma(A union {x}) = Sigma(A) union (x+A) union {2x}
```

when `x` exceeds every old element. Its 64-bit shifts are safe at limit 32:
the largest bit is `2*31=62`. A fresh UBSan build traversed the full domain and
reported no undefined behavior.

The displayed rows are monotone in `k` and meet the elementary caps
`binom(k+1,2)` or `2n-1` where the report says they do. Every lower-bound cell
at `n=28,...,32` has a directly recomputed witness: stored transition
witnesses, subsets of a seven-element Sidon witness for smaller `k`, or
supersets of a full-interval witness after saturation.

## Producer exhaustion and independent traversal

The frozen and fresh producer runs visit exactly

```text
2^31 = 2,147,483,648
```

normalized subsets and agree on every non-timing output line. The old,
separately written Python `n<=27` verifier was also rerun: it visits exactly
`2^26=67,108,864` subsets and reproduces the boundary row byte-for-byte.

For hostile redundancy, a new C++ checker used a different include/exclude
full-binary-tree traversal rather than the producer's combination tree. It
made `2^32-1=4,294,967,295` recursive calls, reached exactly `2^31` leaves,
rebuilt 2,148 deterministically sampled sumsets directly, and reproduced all
six rows 27--32 exactly. Runtime was 25.76 seconds with 3,548 KiB maximum RSS.

## SAT semantics and proof replay

Only `n=32`, `k=8,...,13` are nontrivial at the terminal row. The other cells
attain an elementary cap. For each hard cell the bundled encoding asserts:

- `x_0`, without loss by translation;
- exactly `k` selected coordinates;
- conjunction equivalences for every off-diagonal pair;
- diagonal pair `i+i` iff `x_i`;
- sum occurrence iff the OR of all pair witnesses for that sum; and
- at least `s(k,32)+1` occurring sums.

The custom Sinz counter directions and bounds are correct. Regenerating all
six CNFs from source reproduced the frozen DIMACS files byte-for-byte; headers,
clause counts, and maximum variable identifiers are internally consistent.
The exhaustive encoding self-test covers 94 definition/target instances for
all minimum-zero sets through eight positions and passes.

CaDiCaL and Kissat both report UNSAT on every frozen CNF. More importantly,
all six compressed CaDiCaL proofs were decompressed and replayed afresh with
`drat-trim`; every replay returned `VERIFIED`. The uncompressed proof hashes
recompute exactly to those recorded in `sat_audit_output.txt`.

A completely separate PySAT encoding used totalizer counters rather than the
custom Sinz implementation and Glucose42 rather than either frozen solver. It
found each claimed optimum target SAT and each optimum-plus-one target UNSAT:

```text
k=8:  35 SAT, 36 UNSAT
k=9:  42 SAT, 43 UNSAT
k=10: 51 SAT, 52 UNSAT
k=11: 55 SAT, 56 UNSAT
k=12: 59 SAT, 60 UNSAT
k=13: 62 SAT, 63 UNSAT
```

Thus no underencoding, counter off-by-one, diagonal omission, or frozen-solver
failure was found.

## Scope gate, integrity, and reproduction

The frozen Bright Data transcript records `OPEN`, zero comments, zero claimed
proofs, `Interested in collaborating: None`, and `Currently working on this
problem: None`. A fresh public search on the audit date still exposes the page
as open with no claimed solution. This is provenance only, not mathematical
evidence.

The closed manifest covers all 42 other bundle files and passes:

```text
SHA256(SHA256SUMS) =
3856e649f649ac6a752ca33af90d6c11531f7f17dcc005460f6184f624795db4
```

The publication copy subsequently applied the wording correction requested
below, added this audit report, and bundled the freshly rerun prior checker.
Its refreshed `SHA256SUMS` is therefore the current package manifest; the new
rows and SAT/DRAT evidence files audited above are otherwise unchanged.

All staged files under the site's verification path are byte-identical to the
frozen bundle. The normal checker, quick checker, fresh producer replay, fresh
DRAT gate, gzip integrity checks, CNF regeneration, encoding self-test, and
old `n<=27` baseline all pass.

## Required integration wording

Replace the standalone sentence

```text
every value ... is certified for n<=32
```

with dependency-explicit wording such as:

```text
The exact finite proxy is extended from n<=27 through n=32. This bundle
certifies rows n=28,...,32 and independently reproduces the prior n=27
boundary row; together with the preceding n<=27 package, all s(k,n) values
are certified for n<=32. A complete 2^31-subset traversal supplies the new
rows, and the six nontrivial n=32 upper cells have independently replayed
SAT/DRAT certificates. This is finite computational progress only; Problem
#840 remains open.
```

Do not integrate the provisional `n<=37` data into this checkpoint. It lacks
the terminal SAT/DRAT audit standard used here.
