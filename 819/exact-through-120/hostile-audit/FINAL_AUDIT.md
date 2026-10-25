# Cold-hostile audit: Erdős #819 exact extension through 120

Date: 2026-08-12 UTC

Frozen producer bundle: `/tmp/erdos819_exact_81_120`

## Verdict

**PUBLISH.**

The mathematical result, proof reduction, exhaustive searches, witnesses, and
forty-value table all pass.  The initial frozen report contained one false
collision-check sentence saying there was no existing #819 site entry.  The
producer replaced it with the accurate statement that the site already has a
#819 ledger entry through 80 but no dedicated `verification/819` bundle.

The amended report has SHA-256
`a8d6309385f2e58b8bf76283030565d8ee40768a01534c02f9c6df598e3e83de`.
Replacing that paragraph in memory with the original paragraph reconstructs
the original report SHA-256
`b59e5839b82f51242cce8c059223419277742963a59e1ebdd99461304a6f5258`,
proving that this was the only report change.  The refreshed producer manifest
has SHA-256
`cb5eb429d37b4dfb4e4e356fec098b32b19ba6dfdc9980ae28773c62c92d641a`,
and every listed entry passes.  There is no remaining blocker.

## Definition and loss identity

The frozen live captures and an independent web/source check agree on the
definition

```text
f(N) = max |{a+b <= N : a,b in A}|,
       A subset {1,...,N}, |A|=floor(sqrt(N)).
```

The set of sums is intended, diagonal pairs are included, and unordered pair
representations suffice.  For `P=k(k+1)/2`, partitioning the `P`
representations into overflowing representations and representations below
the cutoff gives exactly

```text
score = P - O_N(A) - C_N(A).
```

There is no ordered/unordered or multiplicity mismatch.

## Translation and auxiliary lengths

Let `s=min(A)` and normalize to marks `x=a-s`, with span `L`.  Translation
preserves all pair-sum equalities.

- If `O_N=0`, every representation is below the cutoff, so the normalized
  global collision excess is exactly `C_N`.  Also
  `L <= floor(N/2)-s <= floor(N/2)-1`.
- If `O_N+C_N<=1` and `O_N=1`, then `C_N=0`.  The sole overflowing
  representation must be the largest diagonal `2 max(A)`: any other
  overflowing pair would be accompanied by that strictly larger diagonal.
  Thus every pair sum is globally distinct.  If `q` is the penultimate mark,
  the next-largest representation is `2s+q+L`, so `q+L<=N-2`.

These are precisely the two uses of translation in the report.  Neither
quietly assumes that truncation itself is translation invariant.

The searches at one below and at each claimed threshold establish, by
monotonicity in the allowed span,

```text
g_0(8)=34, g_0(9)=44, g_1(9)=40,
g_0(10)=55, g_1(10)=50.
```

The `g_0` values also match OEIS A003022, though the bundle recomputes them.
A392461 is not the same defect condition: it bounds every difference
multiplicity separately and can allow many repeated differences.

## Exceptional overflows

For `N=81`, a score at least 44 would mean total loss at most one.

- With no overflow, normalized span is at most 39, contradicting
  `g_1(9)=40`.
- With one overflow, the ruler and its eight-mark prefix give `L>=44` and
  `q>=34`, while `q+L<=79`.  The complete integer possibilities are exactly
  `L=44,q<=35` and `L=45,q<=34`.  The two fixed-last searches exhaust those
  supersets and are infeasible.

For `N=100,101`, a score at least 54 again means loss at most one.

- With no overflow, normalized span is at most 49, contradicting
  `g_1(10)=50`.
- With one overflow, `q>=44`, `L>=55`, and `q+L<=N-2`.  This is impossible
  for `N=100`.  At `N=101`, equality forces `s=1,q=44,L=55`; the fixed-last
  search `k=10,last=55,prefix_bound=44` is exactly the required exhaustive
  search (and a harmless superset before using `q>=44`).

There is no missing overflow pattern or unexamined value of `L`.

## Ordinary interval transitions and witnesses

The fixed-cardinality pair ceilings are 45 for `81<=N<=99` and 55 for
`100<=N<=120`.

- `82<=N<=89`: ceiling 45 would require a nine-mark Sidon ruler of span at
  most 43, contrary to `g_0(9)=44`; the defect-one witness scores 44.
- `90<=N<=99`: the nine-mark Sidon witness has maximum sum 90 and scores 45.
- `102<=N<=111`: ceiling 55 would require a ten-mark Sidon ruler of span at
  most 54, contrary to `g_0(10)=55`; the defect-one witness scores 54.
- `112<=N<=120`: the ten-mark Sidon witness has maximum sum 112 and scores
  55.

Direct recomputation found the advertised witness defects and maximum sums:

```text
k=9 defect 2: one triple sum at 15; excess 2; max sum 72
k=9 defect 1: one double sum at 43; excess 1; max sum 82
k=9 defect 0: no collision; max sum 90
k=10 defect 2: one triple sum at 75; excess 2; max sum 94
k=10 defect 1: one double sum at 93; excess 1; max sum 102
k=10 defect 0: no collision; max sum 112
```

Therefore the exact table is

```text
f(81)=43
f(82..89)=44
f(90..99)=45
f(100..101)=53
f(102..111)=54
f(112..120)=55
```

The forty-value digest independently recomputes to
`d2ad1b092d5fa521efed367cbccfe256be6e68402c73749e3d69a5b046027fc4`.

## Enumeration completeness

`search_at_most` enumerates every increasing normalized mark set exactly
once.  Its only pruning condition is monotone collision excess.  Upon adding a
mark, the newly introduced sums are mutually distinct, and intersection with
the prior sum bitset counts exactly the increase in excess even if a prior sum
already had multiplicity greater than two.

`search_fixed_last` enumerates every collision-free prefix with the prescribed
penultimate bound.  Every globally Sidon candidate has a Sidon prefix, so its
prefix pruning loses no candidate.  At a leaf, all sums involving the fixed
last mark are mutually distinct and are checked against every prefix sum.

Besides the producer's 189 literal small cross-checks, I compared
`search_fixed_last` against literal combinations on 335 small parameter
triples.  All agreed (`fixed_last_literal_output.txt`).

## Reproduction

- `sha256sum -c MANIFEST.sha256`: every listed amended producer file passed.
- Fresh `python3 verify.py`: all mathematical JSON fields were byte-for-byte
  equal after removing the runtime field; the fresh runtime was 55.135558 s
  versus the frozen 56.973817 s; both ended `ALL CHECKS PASSED`.
- Fresh optimized C++ replay: byte-identical to the frozen hostile output,
  SHA-256
  `e51b7b57aa34410b69bff729195762db6f538bf064e066dd7bc94530467f627d`.
- Fresh ASan+UBSan replay: no diagnostics and byte-identical to both optimized
  outputs, with the same SHA-256.

Two exploratory CP-SAT formulations were interrupted while still `UNKNOWN`
on their first case.  They produced no result and are deliberately discarded;
they are not evidence for this verdict.

## Live and collision audit

The frozen Bright Data captures show `OPEN`, two comments, zero claimed
proofs, no current worker/collaborator, and no formalization worker.  The
current official database search/GitHub ground truth also lists #819 as open.
OEIS A003022 supplies the cited Golomb lengths.  A fresh search found a public
agentic-erdos computation at only `N=25,36`, but no exact table for
`81<=N<=120`; the report already phrases its public-table search as a search
miss rather than a priority theorem.

The corrected collision statement and all mathematical claims now pass.
