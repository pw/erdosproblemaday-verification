# Hostile self-audit of the 33--37 extension

Final frozen-bundle verdict:

```text
PASS for exact finite s(k,n), 33<=n<=37;
GAP / OPEN for the asymptotic Erdős Problem #840.
```

This verdict is valid only if `verify_bundle.py` reports all checks passed and
the closed manifest contains all seven terminal proof cases: three exact-
diameter CNFs for `k=9` and one CNF for each of `k=10,11,12,13`.

## Claim boundary

The claimed object is the finite function

```text
s(k,n)=max{|A+A| : A subset [1,n], |A|=k}.
```

No asymptotic improvement or solution is inferred, and no claim is made that
the finite rows are absent from all prior unpublished computation.

## Completeness attack

Translation to minimum zero is a bijection between translation classes of
nonempty integer sets and minimum-zero sets.  Fitting in `[1,n]` is equivalent
to diameter at most `n-1`.  The producer's recursion chooses each optional
positive element once in increasing order, so for limit 37 its prescribed
node count is exactly `2^36`.  It achieved that count and takes prefixes of the
best-by-exact-diameter table, which is the required maximum over sets fitting
in each interval.

## Arithmetic attack

For a newly adjoined maximum `x`, the new sumset is exactly the old sumset,
`x+A`, and `2x`.  A 128-bit unsigned mask is wide enough: every sum lies in
`[0,72]`.  The verifier ignores bit masks and recomputes every claimed lower
witness with Python integer sets.  The producer also reproduces the frozen
row at 32 and the older baseline at 27.

## Coverage attack

At the terminal order 37:

- `k<=8` meets the cap `binom(k+1,2)`, so no larger sumset is possible;
- `k>=14` meets the cap `2n-1=73`, so no larger sumset is possible;
- exactly `k=9,10,11,12,13` require nontrivial upper certificates.

The manifest contains one exact CNF and one compressed checked proof for each
of `k=10,11,12,13`.  The `k=9` cell is covered by three CNF/proof pairs, for
exact translated diameters 34, 35, and 36.  No terminal hard cell is inferred
merely from monotonicity.

For the diameter split, a set of size nine has 36 positive-difference
occurrences.  If its 45 unordered sum occurrences occupy at least 44 values,
there is at most one pair of colliding sum representations.  Any pair of
representations of the same positive difference gives a sum collision by
cross-pairing; a fixed pair of sum representations has at most two such
preimages.  Thus the positive-difference deficit is at most two, there are at
least 34 distinct positive differences, and the diameter is at least 34.
After translation the diameter is at most 36, proving the three-case split.

The `k=9` clauses additionally retain primitive sets and one reflection
orientation.  Division by a common gcd preserves cardinality and sumset size;
if a hypothetical diameter-34--36 witness were nonprimitive, division would
produce a diameter below 34, contradicting the preceding unconditional
difference argument.  Reflection about the fixed top endpoint preserves all
data and swaps the first and last gaps.  The small exhaustive reduction test
checks these identities and the exact reflection clauses.

## SAT-encoding attack

For each off-diagonal unordered pair, a Tseitin variable is equivalent to the
AND of its endpoint-selection variables.  A diagonal pair uses the selection
variable itself.  Each sum variable is equivalent to the OR of every pair
giving that sum.  Sequential counters impose exactly `k` selected elements
and at least the rejected target number of sums.  Setting the zero endpoint is
sound by translation.  The generic `k=10..13` cases do not require the top
endpoint; each `k=9` split case fixes it to the stated exact diameter.

The encoder is tested against direct exhaustive definition evaluation for 94
instances through eight positions, including targets just below, at, and just
above each direct optimum.  This attacks diagonal omissions, reversed
implications, literal-sign mistakes, and cardinality off-by-ones.

## Solver attack

Each identical DIMACS file must receive all three independent checks:

1. CaDiCaL returns UNSAT and emits a proof;
2. Kissat returns UNSAT;
3. `drat-trim` accepts CaDiCaL's proof as VERIFIED.

The verifier checks frozen logs, then optionally decompresses and replays each
proof again.  Solver executable hashes, CNF hashes, and uncompressed proof
hashes appear in the audit output.

## Residual trust and correct label

The exhaustive producer remains a computational proof trusting its compiler
and hardware.  Rows 33--36 do not each receive a separate SAT table; the full
enumeration proves them, while the decorrelated terminal audit attacks the
largest search domain.  The live gate is provenance only.  These limitations
support the label **exact computational finite data**, not a general theorem
about quasi-Sidon asymptotics.
