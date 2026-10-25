# Erdős problem #840: exact finite proxy through 32

Date: 2026-08-12 UTC

## Verdict and scope

**Computational-only finite result; Problem #840 remains open.**  Define the
finite extremal function used by Pikhurko

\[
s(k,n)=\max\{|A+A|:A\subseteq\{1,\ldots,n\},\ |A|=k\}.
\]

The included prior Python checker certifies every value through `n=27` by a
separate `2^26`-subset traversal. This package then extends that exact frontier
through `n=32`:

| n | exact row `(s(1,n),...,s(n,n))` |
|---:|:---|
| 28 | `1 3 6 10 15 21 28 34 41 47 51 55 55 ... 55` |
| 29 | `1 3 6 10 15 21 28 35 41 47 53 56 57 57 ... 57` |
| 30 | `1 3 6 10 15 21 28 35 42 49 53 57 59 59 ... 59` |
| 31 | `1 3 6 10 15 21 28 35 42 51 54 59 61 61 ... 61` |
| 32 | `1 3 6 10 15 21 28 35 42 51 55 59 62 63 63 ... 63` |

Here each ellipsis repeats the last displayed value through `k=n`.  The full
unabbreviated rows and a definition-checked witness for every nontrivial cell
are frozen in `primary_output.txt`.

This does **not** determine the asymptotic growth of the largest quasi-Sidon
subset, improve either asymptotic constant, or solve #840.  It supplies exact
finite data for the same `s(k,n)` appearing in Pikhurko's reduction.  No claim
of literature-first novelty is made: the safe claim is that it extends this
project's independently certified frontier from 27 to 32.

## Current live gate

The page was loaded through the Bright Data browser immediately before work.
`live_gate_2026-08-12.txt` records:

- status `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- `Interested in collaborating: None`;
- zero comments; last edited 19 October 2025.

Thus the no-collision gate passed on 2026-08-12.  These fields are provenance,
not mathematical evidence.

## Exhaustive upper bounds

Translation preserves cardinality and `|A+A|`.  Every nonempty set fitting in
`[1,n]` can therefore be translated to a unique set with minimum zero and
diameter at most `n-1`.  The producer visits every subset of `[0,31]`
containing zero, exactly once: `2^31 = 2,147,483,648` nodes.

For a partial set `A`, represented as a bit mask, and a newly adjoined largest
element `x`, its sumset mask is updated by the exact identity

\[
\Sigma(A\cup\{x\})=\Sigma(A)\cup(x+A)\cup\{2x\}.
\]

The traversal records the best score separately by exact diameter and
cardinality, then takes diameter prefixes to recover every `s(k,n)`.  On this
VM the frozen optimized C++ run took 5.62 seconds, used 3.9 MB maximum RSS,
visited exactly `2^31` nodes, and reproduced the previously certified `n=27`
row byte for byte.  `verify_bundle.py` recompiles and reruns this traversal by
default, ignores only the variable timing line, and compares every remaining
output line with the frozen result. It also reruns the included prior checker,
normalizes only its timing line, and compares every other line with the fresh
frozen `n<=27` transcript. Thus the package is cumulatively self-contained.

## Lower bounds and witnesses

Every displayed value has a direct witness.  The standalone checker computes
`{a+b : a,b in A}` with ordinary Python sets, independently of the producer's
bit-mask recurrence.

For `n=32`, the transition witnesses are:

| k | witness `A` | `|A+A|` |
|---:|:---|---:|
| 7 | `{1,2,5,11,19,24,26}` | 28 |
| 8 | `{1,2,8,12,21,24,26,29}` | 35 |
| 9 | `{1,2,4,8,13,23,27,29,30}` | 42 |
| 10 | `{1,2,4,9,13,19,23,28,30,31}` | 51 |
| 11 | `{1,2,3,5,10,14,20,24,29,31,32}` | 55 |
| 12 | `{1,2,4,5,10,15,17,22,27,28,30,31}` | 59 |
| 13 | `{1,2,3,4,5,10,15,20,25,28,29,31,32}` | 62 |
| 14 | `{1,2,3,4,5,6,12,16,21,23,28,29,31,32}` | 63 |

The last witness has the entire possible sum interval `[2,64]`; adding
arbitrary missing elements proves the lower bound 63 for every `k>=14`.
Subsets of the seven-element Sidon witness handle `k<=7`.  The same checks are
performed for every cell in rows 28--31.

## Independent terminal-row audit

The only nontrivial `n=32` upper cells are `k=8,...,13`.  Values for `k<=7`
equal the elementary cap `binom(k+1,2)`, while values for `k>=14` equal the
interval cap `2n-1=63`.

`sat_audit.py` independently encodes the definition for each of the six hard
cells.  Variables say which integers belong to `A`, which unordered pairs are
selected, and which sums occur.  Tseitin equivalences enforce

- each pair variable iff both endpoints are selected;
- each sum variable iff at least one selected pair gives that sum;
- `min(A)=0` (by translation), exactly `k` selected elements; and
- at least one more distinct sum than the claimed optimum.

Custom Sinz sequential counters encode the two cardinality conditions.  The
encoding was exhaustively tested against direct enumeration for all
minimum-zero models through eight positions before the frozen run.  For all
six cells:

- CaDiCaL returned `UNSAT`;
- Kissat independently returned `UNSAT` on the identical DIMACS file; and
- `drat-trim` returned `VERIFIED` on CaDiCaL's proof.

The exact CNFs, compressed DRAT proofs, three logs per case, solver hashes,
CNF hashes, uncompressed proof hashes, and compressed sizes are frozen under
`sat/` and in `sat_audit_output.txt`.  `verify_bundle.py --replay-drat`
decompresses and replays every proof afresh.

The rejected targets are:

| k | exact `s(k,32)` | independently rejected target |
|---:|---:|---:|
| 8 | 35 | 36 |
| 9 | 42 | 43 |
| 10 | 51 | 52 |
| 11 | 55 | 56 |
| 12 | 59 | 60 |
| 13 | 62 | 63 |

## Reproduction

Quick integrity, live-gate, witness, direct-small-search, and frozen SAT-log
checks:

```sh
python3 verify_bundle.py --quick
```

The normal check also recompiles the producer and re-enumerates all `2^31`
translated subsets:

```sh
python3 verify_bundle.py
```

To replay all six DRAT proofs as well:

```sh
python3 verify_bundle.py --replay-drat \
  --drat-trim /path/to/drat-trim
```

To regenerate the SAT evidence (this overwrites files in the chosen output
directory, so use a fresh directory):

```sh
python3 sat_audit.py primary_output.txt \
  --min-n 32 --max-n 32 --out /tmp/erdos840-sat-recheck --keep-cnf
```

## Files

- `primary_exact.cpp`: complete `2^31`-node producer.
- `primary_output.txt`, `primary_time.txt`: frozen result and resource record.
- `prior_n27_verify.py`, `prior_n27_fresh_output.txt`: independent historical
  baseline certifying every row through 27.
- `sat_audit.py`: independent definition-to-CNF generator and dual-solver/
  DRAT driver.
- `test_sat_encoding.py`, `sat_encoding_selftest_output.txt`: exhaustive
  definition/encoding agreement through eight positions (94 instances).
- `sat/`: six DIMACS instances, compressed proofs, and solver/replay logs.
- `verify_bundle.py`: standalone public checker.
- `live_gate_2026-08-12.txt`: rendered Bright Data transcript.
- `SHA256SUMS`: closed manifest of every other file.
