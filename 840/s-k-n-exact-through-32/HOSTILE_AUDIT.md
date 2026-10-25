# Hostile self-audit

Verdict: **PASS for the exact finite claim through 32; GAP/OPEN for Erdős
Problem #840.**

## Claim boundary

The package claims only that every value of

```text
s(k,n) = max{|A+A| : A subset [1,n], |A|=k}
```

is exact for `n<=32`. The included historical checker supplies the complete
independent `n<=27` baseline, while the new traversal supplies rows 28--32.
It does not claim an asymptotic improvement, a solution of #840, or
literature-first novelty. The live gate was clean, but that is only provenance.

## Attack 1: traversal completeness

A counterexample could be lost if translation or diameter prefixing were
wrong.  Translation maps any nonempty finite `A` bijectively to `A-min(A)`,
preserves `|A|` and `|A+A|`, and places it in `[0,n-1]`.  Conversely every
minimum-zero set of diameter at most `n-1` translates into `[1,n]`.  The DFS
chooses each positive element once in increasing order, so its exact node count
must be the number of subsets of 31 optional positions, `2^31`.  The frozen
and fresh runs both report exactly 2,147,483,648 nodes.

## Attack 2: incremental sumset corruption

If `x` is larger than every old element, new sums are precisely `x+A` and
`2x`; old sums persist.  This proves the recurrence.  Witness scores are also
rebuilt with ordinary Python sets.  The old `n=27` row agrees exactly with the
separate, previously published Python traversal, which uses a different
language and implementation.

## Attack 3: lower-bound gaps

The checker constructs a set of the required size and score for every cell,
not only the transition cells.  For `k<7` it takes subsets of a seven-element
Sidon witness.  At and after the full-sumset threshold it starts from the
smallest full witness and adds unused elements, which cannot shrink the
sumset.  Every resulting score is directly recomputed.

## Attack 4: SAT model could underencode counterexamples

The audit CNF uses explicit equivalences, not one-way implications:

- `z_(i,j) <-> (x_i and x_j)` for off-diagonal unordered pairs;
- diagonal pairs use `x_i` directly;
- `y_s <-> OR_{i+j=s} z_(i,j)`;
- sequential counters enforce exactly `k` selected positions and at least the
  target number of true `y_s` variables;
- `x_0` is true, which is sound by translation.

`test_sat_encoding.py` compares SAT versus direct definition-level enumeration
on 94 instances covering every cardinality through eight positions and targets
on both sides of the optimum.  All agree.  This cannot prove the generator
correct for all sizes by itself, but it strongly attacks sign, endpoint,
diagonal, OR-equivalence, and counter off-by-one errors.

## Attack 5: one solver could be wrong

The same six DIMACS instances were rejected by both CaDiCaL and Kissat.  More
importantly, CaDiCaL's proof for every instance was accepted by `drat-trim`;
the public checker independently decompressed and replayed all six after the
bundle was frozen.  Solver logs, CNFs, compressed proofs, hashes, and replay
logs are present in the closed manifest.

## Attack 6: missing upper cells

For `n=32`, the cells `k<=7` attain the pair-count cap
`binom(k+1,2)`.  The cells `k>=14` attain the interval cap `2n-1=63`.
No stronger score is mathematically possible there.  Thus only `k=8,...,13`
need machine upper certificates, and all six are present.

Rows 28--31 are primarily certified by the complete `2^31` traversal and its
full rerun; they do not each have separate SAT proofs.  The terminal n=32
audit is a decorrelated check of the algorithm at its largest domain, not a
logical substitute for understanding traversal completeness.

## Remaining risks

- No independent literature census establishes novelty; none is claimed.
- The finite data do not imply anything about the asymptotic constant.
- Compilers and hardware are trusted in the usual computational-proof sense.
- The included DRAT checker binary is not itself bundled; its SHA-256 is
  recorded, and the proof format permits replay with another `drat-trim`
  build.

With those boundaries, the exact finite result is suitable for publication as
**computational-only**, while Problem #840 remains **OPEN**.
