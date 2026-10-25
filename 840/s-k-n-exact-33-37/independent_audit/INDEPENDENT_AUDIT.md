# Independent hostile publication audit: Erdős #840 finite proxy, 33--37

Date: 2026-08-12 UTC

## Verdict

**PUBLISH as exact finite computational data.**  The frozen pre-audit producer
bundle had manifest hash

```text
60e28ace02014f081f2e55bbe9336152a05cc14381b672e7cef60892cdaaf6e2
```

and soundly certifies every value of

```text
s(k,n) = max{|A+A| : A subset [1,n], |A|=k}
```

for `33<=n<=37`.  It also recomputes rows 27--32, which match the separately
published checkpoint exactly.  Together with the preceding finite packages,
this moves the project's exact frontier through 37.

This is finite computational progress only.  It does not improve an
asymptotic constant, settle the quasi-Sidon growth question, or establish
literature-first novelty.  Erdős Problem #840 remains open.

That digest names the producer-only state I audited.  The public package will
add a lean subset of this independent audit and therefore must regenerate its
closed manifest; its final public manifest hash is expected to differ.  The
mathematical producer, CNFs, and proof streams should remain byte-identical.

## Definition, translation, and exhaustive coverage

Translation preserves cardinality and sumset cardinality.  A nonempty set
fitting in `[1,n]` therefore corresponds to a minimum-zero set of diameter at
most `n-1`.  The producer's increasing recursion visits each subset of
`[0,36]` containing zero once, and only once.  Its node count is the required

```text
2^36 = 68,719,476,736.
```

For a newly adjoined maximum `x`, the recurrence

```text
Sigma(A union {x}) = Sigma(A) union (x+A) union {2x}
```

is exact.  All possible sums lie in `[0,72]`, so its unsigned 128-bit storage
is wide enough.  Maxima indexed by exact diameter, followed by diameter
prefixes, have exactly the semantics of `s(k,n)`.

I separately compiled and ran a clean-room traversal whose sumset uses two
ordinary 64-bit limbs rather than `unsigned __int128`.  It visited the same
`2^36` translated sets and reproduced every producer row from 32 through 37
exactly, in 15:23.11 wall time with 3,716 KiB maximum RSS.  This matters for
the intermediate rows: 16 cells in rows 33--36 do
not follow merely from the elementary caps and the terminal `n=37`
certificates, so their upper bounds genuinely rest on the exhaustive
traversal.

A second independently compiled run stopped after cardinality 13, the last
potentially nontrivial cardinality.  It exhausted exactly 2,241,812,648
translated sets, reproduced every value for `n=32,...,37` and `k<=13`, and
finished in 27.52 wall seconds.  Together with the directly checked
full-interval witness at `k=14`, this shorter run is already a complete
independent upper-and-lower audit of all new rows.

The new output's rows 27--32 agree entry-for-entry with the frozen published
`n<=32` producer transcript.  The prior package manifest remains
`d0acee601cc2c0bc6b8afbdf0eafb7b4c76a3c764f89d1bd52777dea9d3f6c82`.

## Lower bounds and cap coverage

Every stored witness for rows 33--37 was rebuilt with ordinary Python integer
sets.  Cardinalities, domains, and claimed sumset sizes all pass.  The small
cells are supplied by subsets of a seven-element Sidon witness.  Once a set
has the full interval sumset, its supersets preserve that interval, supplying
all saturated cells.

At `n=37`, `k<=8` attains the unordered-pair cap
`binom(k+1,2)` and `k>=14` attains the interval cap `73`.  Thus the only
nontrivial terminal upper cells are exactly `k=9,...,13`, as the package
claims.

## The `k=9` diameter split

The delicate reduction is sound.  Nine elements give 45 unordered sum
representations and 36 positive-difference representations.  If at least 44
sum values occur, the representation deficit is at most one, so there is at
most one pair of colliding sum representations.

If two distinct positive-difference representations satisfy
`a-b=c-d`, cross-pairing gives the sum collision `a+d=b+c`.  Conversely, a
fixed pair of colliding unordered-sum representations has at most two such
cross-pairings.  Therefore the difference deficit is at most two and at least
34 positive differences are distinct.  Since every positive difference is
at most the diameter, the diameter is at least 34.  After translation it is
at most 36.  Exact diameters 34, 35, and 36 are consequently exhaustive.

The further reductions do not lose a counterexample:

- If all positive elements had gcd `g>1`, division by `g` would preserve
  cardinality and sumset size while producing diameter at most 18, contrary
  to the unconditional diameter-at-least-34 argument.  A hypothetical
  counterexample is therefore automatically primitive.  The prime clauses
  encode exactly this condition.
- Reflection about the fixed top endpoint preserves all relevant quantities
  and swaps the first and last gaps.  One orientation always has first gap no
  larger than last gap.  The frozen reflection clauses encode that condition
  exactly.

Beyond inspecting the proof, I exhaustively checked the sum/difference
deficit implication on 131,071 minimum-zero sets through 17 positions and
attacked the actual diameters with 300,000 deterministic random nine-sets.
No failure was found.

## SAT encoding and certificate coverage

I rebuilt the seven frozen formulas from the mathematical definition in a
separate audit program without importing or executing the producer's encoder.
Comparison as clause multisets was exact in every case:

| case | variables | clauses |
|:---|---:|---:|
| `k=9,d=34` | 4196 | 10172 |
| `k=9,d=35` | 4196 | 10204 |
| `k=9,d=36` | 4196 | 10237 |
| `k=10`, reject 52 | 3620 | 8494 |
| `k=11`, reject 60 | 3044 | 7358 |
| `k=12`, reject 65 | 2684 | 6648 |
| `k=13`, reject 70 | 2324 | 5938 |

The generic formulas assert minimum zero, exactly `k` selected coordinates,
pair conjunction equivalences, sum disjunction equivalences, and at least the
rejected target number of occurring sums.  The split formulas add the exact
top endpoint and the already-audited primitive/reflection clauses.  DIMACS
headers, maximum variable identifiers, and clause counts are consistent.

The bundled small self-test was rerun, not merely trusted as a transcript: all
94 definition/CNF comparisons through eight positions pass.  The diameter
reduction self-test also passes afresh.

CaDiCaL and Kissat both report UNSAT on each identical frozen DIMACS file.
All seven compressed CaDiCaL proof streams were decompressed and replayed
afresh with the recorded `drat-trim` executable; all seven returned
`VERIFIED`.  The solver executable hashes match the bundle, and every
uncompressed proof hash matches its frozen summary record.

## Integrity and reproduction

The pre-audit producer manifest covers all 51 producer files, with no missing
or unlisted material file, and every digest passes. The final public manifest
also binds this lean audit subset. Decompressing all seven proof files validates
their gzip streams. The public verifier passes its manifest, gate,
lower-witness, small-search, terminal certificate, and recorded-hash checks.

Independent audit artifacts are in the bundled `independent_audit/`
directory. They include the clean-room clause
rebuilder, reduction attacks, two-limb exhaustive traversal, seven fresh proof
replay logs, and their transcripts.  These were kept outside the producer
bundle throughout the audit.

## Publication wording

Use dependency-explicit language: this bundle certifies the new rows 33--37
and recomputes the published boundary rows 27--32; together with the existing
finite packages, the exact project frontier is through 37.  Retain the label

```text
PARTIAL / exact computational finite data; asymptotic Problem #840 remains open.
```
