# Erdős problem #840: exact finite-proxy extension, 33 through 37

Date: 2026-08-12 UTC

## Verdict

**Computational-only exact finite extension.  Erdős Problem #840 remains
open.**  For

\[
s(k,n)=\max\{|A+A|:A\subseteq\{1,\ldots,n\},\ |A|=k\},
\]

this package extends the separately frozen exact frontier `n<=32` by proving
every value for `33<=n<=37`:

| n | exact row `(s(1,n),...,s(n,n))` |
|---:|:---|
| 33 | `1 3 6 10 15 21 28 35 42 51 56 61 65 65 ... 65` |
| 34 | `1 3 6 10 15 21 28 35 42 51 56 61 65 67 67 ... 67` |
| 35 | `1 3 6 10 15 21 28 36 42 51 57 63 67 69 69 ... 69` |
| 36 | `1 3 6 10 15 21 28 36 43 51 57 63 68 71 71 ... 71` |
| 37 | `1 3 6 10 15 21 28 36 43 51 59 64 69 73 73 ... 73` |

Each ellipsis repeats the last value through `k=n`; complete rows and
witnesses are in `primary_output.txt`.

This does not improve the asymptotic bounds, determine the quasi-Sidon
constant, or solve #840.  It is exact finite data for the Pikhurko proxy.  No
literature-first novelty claim is made.

## Gate and relation to the preceding checkpoint

The Bright Data transcript shows that immediately before this branch the live
page was `OPEN`, had zero claimed proofs, and listed neither a current worker
nor an interested collaborator.  The transcript is included.

The already-frozen `n<=32` bundle is not modified or incorporated by reference.
This extension's producer independently recomputes rows 27--32 before rows
33--37; its row 32 matches the frozen terminal baseline exactly.

## Complete producer

Translation preserves `|A|` and `|A+A|`.  The producer translates the minimum
to zero and visits every subset of `[0,36]` containing zero, exactly once.  Its
node count is therefore

\[
2^{36}=68,719,476,736.
\]

It uses the exact recurrence

\[
\Sigma(A\cup\{x\})=\Sigma(A)\cup(x+A)\cup\{2x\}
\]

and an unsigned 128-bit mask for the sumset (whose maximum bit index is 72).
It records optima by exact diameter and cardinality, then takes prefixes over
diameter.  The frozen run took 331.28 seconds and 3,940 KB maximum RSS.  A
fresh full rerun is available through `verify_bundle.py --rerun-primary`.

## Direct lower witnesses

The standalone verifier rebuilds every witness with ordinary Python sets,
not producer bit arithmetic.  It obtains witnesses for every extension cell:
subsets of a Sidon witness at small `k`, the explicit transition witnesses in
the output, and supersets of the first full-sumset witness afterward.

Terminal transition witnesses include:

| k | witness `A subset [37]` | `|A+A|` |
|---:|:---|---:|
| 8 | `{1,2,5,10,16,23,33,35}` | 36 |
| 9 | `{1,2,5,10,13,14,20,34,36}` | 43 |
| 10 | `{1,2,4,9,13,19,23,28,30,31}` | 51 |
| 11 | `{1,2,4,9,13,19,25,29,34,36,37}` | 59 |
| 12 | `{1,2,4,9,13,15,19,25,29,34,36,37}` | 64 |
| 13 | `{1,2,3,5,9,14,19,24,29,33,35,36,37}` | 69 |
| 14 | `{1,2,4,5,10,12,17,21,26,28,33,34,36,37}` | 73 |

The `k=14` witness covers the entire possible interval `[2,74]`; adding
elements proves all later lower bounds.

## Independent terminal audit

At `n=37`, `k<=8` attains the elementary unordered-pair cap
`binom(k+1,2)`, and `k>=14` attains the interval cap `2n-1=73`.
Consequently only five upper cells are nontrivial:

| k | exact value | rejected target |
|---:|---:|---:|
| 9 | 43 | 44 |
| 10 | 51 | 52 |
| 11 | 59 | 60 |
| 12 | 64 | 65 |
| 13 | 69 | 70 |

`sat_audit.py` constructs CNFs directly from the definition.  It has set
membership variables, explicit pair conjunctions, explicit sum disjunctions,
and Sinz counters for exact set cardinality and the forbidden target score.
The same encoder is exhaustively compared with direct enumeration for 94
minimum-zero instances through eight positions by `test_sat_encoding.py`.

The hardest cell, `k=9`, uses a transparent exhaustive diameter split.  Nine
elements have 45 unordered pairs with repetition.  A score of at least 44
therefore permits at most one sum collision.  An equality of two positive
differences maps to an equality between two unordered sums; one fixed sum
collision can arise from at most two such cross-pairings.  Hence among the 36
positive differences at most two repetitions occur, at least 34 differences
are distinct, and the diameter is at least 34.  The minimum is translated to
zero, so only exact diameters 34, 35, and 36 remain.

Each of those three definition-level CNFs fixes its top endpoint.  Dividing
all elements by their gcd preserves cardinality and distinct-sum count, so a
primitive representative may be required.  Reflection about the top endpoint
also preserves the data, so the orientation with first gap no larger than last
gap may be required.  `test_diameter_reduction.py` exhaustively checks the
reflection clauses and scaling invariance on small domains.  These reductions
change neither the covered counterexample set nor the five-cell result.

For each generic hard cell, and for all three `k=9` diameter subcases, the
frozen evidence requires:

- CaDiCaL `UNSAT`;
- Kissat `UNSAT` on the identical DIMACS file; and
- `drat-trim` `VERIFIED` on CaDiCaL's proof.

CNFs, compressed DRAT proofs, solver/replay logs, solver hashes, CNF hashes,
and uncompressed proof hashes are all frozen.  The public verifier can replay
the proofs again with `--replay-drat`.

The recorded solver executable hashes are:

| executable | SHA-256 |
|:---|:---|
| CaDiCaL | `544dbba6f5338c9d65cf99494fe73ab51892dcc2d9a2b2a3b1933a53e4378d2b` |
| Kissat | `cc867d71737c6a79c6cc03d292c971f643bf8782c426a76900a94ca287eebdc5` |
| drat-trim | `f8d971dc5956a73fa37e655a44ba8f6d128976acfedff7129f2ed251b234af1a` |

The seven proof cases are identified by these content hashes (proof hashes
refer to the uncompressed DRAT byte streams):

| case | CNF SHA-256 | proof SHA-256 |
|:---|:---|:---|
| `k=9,d=34` | `9c6281ec44021a715b50e3914417289e34c6cd952c8bc50583fb36656b74f550` | `805146202ebc3d4e7c31f31e7600833f57da125748338ee5383d5d338cb6a02e` |
| `k=9,d=35` | `2be555dc42b9b5c6ef869593cb3cb58a1bf96505a3122b6cbb801e9ebdf70a8b` | `c8e77c5beb22d230c4812e75af5400da022a8e08d6e8e7be1d16a1fcfebcca3d` |
| `k=9,d=36` | `3fdd7b1190526cb9b94a550c9f7ceececebd98f37b6fd6a8f5aa388011fa36b1` | `2d6103b4f110d0712b137d247499fd9c83732f610207a143cfe102f14e5d288e` |
| `k=10` | `a1a654009790721430a832e3a69e023f1db7bfe1ff93f78f2e6cea34300b68a3` | `3e2388dd1fe82c43ae56a1bbadfe10e599d2ec4dfaf2a9dc1c740786cad78a11` |
| `k=11` | `cf2606de9afb257a60c58fef03c3fe7b4bdf5b11ac8e7ac7083209ed3f3efacb` | `9b193936cdb76eb9f527480caa774bf47f6e71092820a3e3033336f36515f756` |
| `k=12` | `33973c969af644719bf3f05cf873b61df01732a05d0c1cddcd7efcb6b701503c` | `680daccc06090307e792839d803ecdd3c6bc4368549da7f725a5b2b07004f6be` |
| `k=13` | `e66288208a75cae1f070e29c4c453c1fba8ccb21d502b1df1d9098b2fe874797` | `108903a7e0433e6cca386b9ea81004e42f027e8aef3b9c48c773d201469346dd` |

`SHA256SUMS` is a closed manifest of every other bundle file, including the
compressed proofs and all logs.

## Reproduction

Fast integrity, gate, definition-level witness, small direct search, and
frozen SAT-evidence checks:

```sh
python3 verify_bundle.py
```

Repeat the approximately 5.5-minute traversal:

```sh
python3 verify_bundle.py --rerun-primary
```

Replay every proof:

```sh
python3 verify_bundle.py --replay-drat --drat-trim /path/to/drat-trim
```

Both expensive checks may be requested together.

## Conservative publication label

```text
PARTIAL / exact computational data: all s(k,n) through n=37 are certified;
the asymptotic quasi-Sidon problem remains open.
```
