# Hostile audit: Erdős problem 1206 finite table, N=132..191

Audit date: 2026-08-12 UTC.

## Verdict

**PUBLISH**, explicitly as a finite computational extension only.

The frozen claim is correct:

- tau(N) = 21,22,23,24,25,26,27,28,29,30,31,32 on the twelve
  respective intervals 132--133, 134--137, 138--143, 144--155,
  156--160, 161--164, 165, 166--171, 172--173, 174--179, 180--185,
  and 186--191;
- hence g3(N)=N-tau(N) throughout, in particular g3(191)=159.

This neither proves a linear asymptotic lower bound nor constructs an
infinite positive-density set.

## Integrity and cold reproduction

`sha256sum -c SHA256SUMS` passes for all four payload files.  A completely
cold `./verify.sh` run passes all assertions and reports the same 12,893,491
recursive states as the report.  The C++ phase took 164.247 seconds; the full
command took 2:47.02 wall time and 183,580 KiB peak RSS.

Frozen hashes:

```
c215d0c7b878a8bb0e38313b8a6cbc533813ff6a95902dec25f17c5c875c0421  REPORT.md
a69e1e91bd15d63f1acf07bd27ea52e06bcd88bc83eea2a73c409431bedae80f  audit_definition.py
ad21b9fd97bc22e24103bd8db8d939b6a168a3e2bad61343b3a31bec918fad86  verify_exact.cpp
82b147bbe30b2257a488fcbbf372fd3242dcf35c0f0567669d10496b68efb686  verify.sh
4db26f68452ae09dc4280dbaf6823ef7a24a774752801fd4a528fdbea1fe879a  SHA256SUMS
```

The cold combined output is
`b72b325889a57e0eeec5db6f642bb8fd4dd21a251040b8967a57c32f8e68eb77`.

## Reduction audit

For every unordered root pair P={a,b}, including a=b, the arithmetic builder
places P in the bucket keyed by a^3+b^3.  For every two *distinct* pairs P,Q
in one bucket, the forbidden root set is P union Q.  Thus a root set contains
a repeated unordered cube sum exactly when it contains one such hyperedge.
Taking complements turns maximum independent set into minimum transversal,
so g3(N)=N-tau(H_N).

The builders enumerate all pairwise combinations in a bucket, so sums with
more than two representations are handled.  Taking the set-union is also the
right operation for a diagonal pair or overlapping representations; duplicate
unions may safely be deduplicated.  In the actual N<=191 data there are no
such special collision shapes: all 124 terminal collision groups have exactly
two representations and all terminal edges have four distinct vertices.
Diagonal pairs were nevertheless explicitly counted (exactly N of them at
each N), rather than omitted.

The hostile Python arithmetic audit rebuilt every H_N for 1<=N<=191 and
asserted the exact restriction identity

```
H_N = { e in H_191 : max(e) <= N }.
```

It checked every displayed upper cover at the interval's right endpoint and
then, independently of hypergraph coverage, inserted every unordered sum from
the complementary root set into a fresh set and found no repetition.

At N=191 it independently reproduced:

- 18,336 unordered root pairs;
- 18,212 distinct sums;
- 124 collision buckets and 124 unique edges;
- maximum two representations per bucket;
- all edges of size four and 164 active vertices;
- canonical edge SHA-256
  `644dadc2aa52bddd902f03811acff745e129add6406fac5a09be5099852fb081`.

## Lower-bound audit

The frozen search's pruning is sound:

1. greedily selected vertex-disjoint active edges require distinct future
   cover vertices, so their count is a valid lower bound;
2. if active incidence(v) is contained in active incidence(w), any cover using
   v may replace it by w, so v can be omitted from the branch edge;
3. a failed identical active-edge set at a greater or equal remaining budget
   subsumes the current state.

Every cover must select a vertex of the chosen active edge, and the search
recurses on every undominated choice, so these rules leave an exhaustive
search.

Two separate checks challenged this implementation:

- a harness compiled the exact frozen search class and compared it with
  literal subset enumeration on all 32,768 hypergraphs over four vertices,
  at every budget, plus 2,000 fixed-seed random hypergraphs on 5--12 vertices;
  all comparisons passed;
- a separate Python builder emitted a 0/1 set-cover integer program
  `min sum(x_v)` with one constraint `sum_{v in e} x_v >= 1` per freshly
  reconstructed collision edge.  CBC independently returned **Optimal** at
  all twelve lower endpoints, with objectives
  `21,22,23,24,25,26,27,28,29,30,31,32`.  Each returned cover was then
  checked against every edge and by direct unordered cube sums.

The latter run used CBC `Devel (unstable)`, build 2026-03-23, executable
SHA-256 `8f4400f2830795e88d0658f7fbf65d6c981c7c5d6eb6faacb0d9e8d5064cbc58`.
CBC did not emit a separately checkable proof certificate, so it is strong
independent corroboration rather than the primary proof artifact.  The frozen
dependency-free exhaustive search remains the reproducible lower-bound proof.

## Endpoint interpolation

For L<=N<=R, H_L is a restriction of H_N and H_N is a restriction of H_R.
Therefore the lower-endpoint result gives tau(H_N)>=tau, while the explicit
right-endpoint cover gives tau(H_N)<=tau (intersecting it with [N] if needed).
This proves every intermediate N; no untested monotonicity heuristic is being
used.  The hostile audit checked the needed restriction identity at every N.

## Live collision gate

Bright Data fetched the live problem, discussion, and proof-claims routes on
2026-08-12 UTC.  They still showed OPEN, zero claimed proofs, nobody currently
working or collaborating, two comments only (Tait's bound and the 1729
comparison example), and `No proof claims have been submitted yet.`

## Hostile audit artifacts

```
eabd5b0f5a695106eed1222f4de173f394cee2c7dfee2682194cca45de090d05  audit_arithmetic.py
6d00b847e0f085025b52e33db06fbccc799c5a39b1617b60ca0bedc2efd4ad23  audit_arithmetic.out
1ec3fc38f3df170cb9d2bddbba0a29af807b7b4140d317d4e239d0338f7fde18  audit_cbc.py
16bdc25d58432b19f38c78e9cc529247ed0127136cbafc8ccf5ffe46d2339a15  audit_cbc.out
c4527419229ddb42cdba458313d8f130c50a45cd04c06b72632028d630d99aa7  selftest_producer_search.cpp
6c6258c710257e140762c4091b232706d754bde1753e90ba19d67eee4ce710cc  selftest_producer_search.out
```

## Lean public bundle

The existing five-file frozen bundle is sufficient and appropriately lean:
`REPORT.md`, `verify_exact.cpp`, `audit_definition.py`, `verify.sh`, and
`SHA256SUMS`.  If retaining hostile-review evidence publicly, add only this
`AUDIT.md`, `audit_cbc.py`, and `audit_cbc.out`; the generated LPs, CBC
solutions/logs, abandoned SAT experiments, and search test harness are not
needed for the normal verifier.
