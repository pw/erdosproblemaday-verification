# Second hostile audit: Erdos Problem 1109 exact frontier

Audit date: 2026-08-11 UTC

Frozen bundle audited:
`/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11`

Claimed bundle manifest SHA-256:
`cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9`

## Verdict

**PASS.** I found no load-bearing mathematical, implementation, certificate,
or scope gap. The bundle proves

```
f(N)=39  for 1103 <= N <= 1254
f(N)=40  for 1255 <= N <= 1276
f(N)=41  for 1277 <= N <= 1292
f(N)=42  for 1293 <= N <= 1334
f(N)=43  for 1335 <= N <= 1406
f(N)=44  for 1407 <= N <= 1500
```

and hence the next five record indices of live OEIS A392165 are exactly
`1255, 1277, 1293, 1335, 1407`, relative to the public sources checked on
2026-08-11. This is a finite exact result only. It neither improves the
known asymptotic bounds nor resolves the parent Problem 1109 conjectures.

One non-load-bearing artifact issue is recorded below: the bundle pins the
dynamically linked Cliquer executable but not `libcliquer.so.1`. I captured
and hashed the loaded library in this audit. The complete primary C++ and PMC
chains independently establish the finite theorem even if Cliquer is omitted.

## Integrity and reproduction

* The manifest itself hashes to the claimed `cbd71d...da7e9`.
* It has 70 entries, all unique, and exactly equals the set of every regular
  file below the bundle except the manifest itself. Every entry passed
  `sha256sum -c`.
* The nested order-races manifest has 32 entries and is likewise an exact
  closure of that directory except itself. Those races are correctly labeled
  non-load-bearing.
* A live `./reproduce_1109.sh quick` run exited 0 in 25.70 seconds. It checked
  the manifest, all five displayed witnesses, regenerated all 163 graphs in
  both formats, and reproduced both external result digests.
* A fresh `-O3` build was byte-identical to the frozen primary binary:
  `84ebeca91559cfa6caaff408059731d9a35f74f6f446edde0aa807895e93bdb8`.
* I ran that fresh binary through 1500 on one core. It exited 0 after 96.52
  seconds. All deterministic lines, including every decision and node count,
  all 44 witnesses, the summary, and the conclusion, exactly match the frozen
  run. The fresh raw log is `fda4a336...716e5d6`.

## Reduction from the definition

For a valid set `A`, each diagonal sum `a+a=2a` must be squarefree. Thus the
only possible vertices are the `a <= N` for which `2a` is squarefree. This is
equivalent to `a` being odd and squarefree. For distinct `a,b`, validity is
exactly the edge test that `a+b` is squarefree. Therefore valid sets and
cliques in `G_N` are in bijection, including all diagonal sums, and
`f(N)=omega(G_N)`.

The graph at an ineligible `N` is unchanged. At an eligible `N`, any clique
excluding the new vertex has size at most the known old optimum `r`; a clique
including it is the new vertex plus a clique in its old-neighbor graph. Adding
one vertex can increase a clique number by at most one, so the new optimum is
`r+1` exactly when that neighbor graph contains an `r`-clique. Starting at
`f(1)=1`, one exact decision at every eligible integer is a complete induction
over all prefixes, not merely a check at the five positive points.

The external target formula uses transitions strictly less than the current
new vertex. This correctly supplies the old optimum at a transition itself.
There are 610 eligible vertices through 1500 and exactly 163 after 1103. The
first and last external decisions are 1105 and 1499: 1104 and 1500 are both
ineligible, so neither endpoint is omitted.

## Primary implementation

The C++ squarefree table starts true, makes zero false, and marks every
multiple of every square `d^2` through `2*MAX_N`. Composite `d` values merely
repeat valid markings. No primality, randomness, or floating point is used.
Every adjacency insertion is symmetric. At 1500 there are 610 vertices, well
below the asserted 2048-bit capacity, and all sum-table indices are at most
3000.

The clique recursion is exhaustive:

1. Equality of chosen size with the target is success.
2. `chosen + popcount(pool) < target` is a valid cardinality rejection.
3. Each greedy color pass selects mutually nonadjacent vertices, so every
   color class is independent and a clique uses at most one member per class.
4. During the reverse scan, already scanned vertices have been removed from
   the local pool. The remaining candidates lie in the color prefix ending at
   the current stored color, making `chosen + color < target` a valid rejection
   of every remaining branch.
5. The include branch intersects with the selected vertex's exact adjacency.
   If it fails, resetting that vertex is the complementary exclude branch.
   Thus no candidate clique is skipped.

The build flags do not define `NDEBUG`, so capacity, old-frontier, and witness
assertions are active. I compiled the exact frozen class into an audit harness.
It passed 501,121 comparisons: every graph through order 6 (all candidate
subsets through order 5), 300 seeded random cases, returned-witness checks,
and empty/complete/disjoint-clique/complete-multipartite families across bit
boundaries 63, 64, 65, 127, 128, 129, 610, and 2048.

## Lower and interval certificates

Using an independent linear Mobius sieve, I checked every diagonal and
distinct-pair sum in all 44 primary witnesses: 15,180 sums total. The five new
displayed witnesses account for 4,520 checks and have sizes 40 through 44,
distinct sorted members, maximum elements equal to the claimed first indices,
and only squarefree sums. The five positive Cliquer witnesses and five
positive PMC witnesses, several different from the primary witnesses, also
pass direct checks.

The primary transitions are exactly the 39 frozen OEIS terms followed by the
five claimed terms. Reconstructing `f(N)` from those transitions produces the
six claimed intervals exactly. The negative decision at every other eligible
vertex supplies each interval's upper bound; the most recent positive witness
persists as its lower bound. Ineligible integers leave the graph unchanged.

## External solver chains

I regenerated all 163 old-neighbor graphs from the definition using the linear
Mobius sieve, independently of both bundle squarefree routines. For every case
I reproduced the vertex count, edge count, DIMACS hash, Matrix Market hash,
target, decision, and positive witness. A format-independent concatenation of
all semantic graphs has SHA-256
`b8c9939a1f92b90b779d05f86c182435d0b3adf13848181848ee5c831dd4ee4a`.
All ten retained late DIMACS graphs are byte-identical to my regeneration.

Cliquer is invoked unweighted with `-m r -M r`. Its own help confirms that
these are minimum and maximum clique weights, so it searches for exactly an
`r`-clique. This is equivalent to existence of a clique of size at least `r`,
because any larger clique contains an `r`-subset. The wrapper uses
`subprocess.run(..., check=True)`, recognizes the exact negative line, parses
positive vertices, maps them through the ordered neighbor list, and directly
rechecks the resulting `(r+1)`-witness.

The Cliquer raw log has 163 unique completion lines and 163 sorted records.
Its five positives are exactly the claimed transitions, and its reconstructed
record digest is
`6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84`.
The outer timeout's signal-9 timing block occurs after 143 completions; 20 more
completions and then all 163 records follow it. Thus it documents detachment of
the timeout wrapper, not termination of the Python process or solver children.
The normalized certificate reproduces the records, binds the raw-log hash
`eb871ca...ec973`, and hashes to `30047bb3...5ba`.

For PMC, I freshly fetched official Git commit
`06594a0ee1cde5a04f1679aff28072668da96062`. Its tree ID is
`0a1feff2d5fbabdec4d12a2bada977c2efc6fd75`; the frozen tar contents matched
that tree exactly. The patch changes only the obsolete implicit stream-to-bool
return to `ifile.good()`. Applying it and rebuilding produced a byte-identical
binary, SHA-256 `e64c831e...f62d`.

PMC's source confirms that `-k r` sets the stopping target to `r` and the lower
bound to `r-1`; `-a 0` selects the full exact search; `-t 1` makes each solver
instance serial. Its Matrix Market reader requires the one-based lower
triangle, which the wrapper emits. Every frozen call completed in at most
2.606 seconds, far below PMC's internal 3600-second limit, and the log contains
no timeout marker. The 163 reconstructed records have digest
`cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3`.

The Cliquer, PMC, and primary decision triples agree exactly. Additionally,
both frozen external command paths passed 104 decisions on 64 deterministic
small graphs against a separate brute-force maximum-clique implementation;
every returned witness was checked edge by edge. This smoke-test record digest
is `cf2c6f07...340dd`.

## Sanitizers

The sanitizer compile log uses `-fsanitize=address,undefined` with frame
pointers and without `NDEBUG`; the binary dynamically links both ASan and
UBSan. The run has one successful timing footer, no ASan or UBSan diagnostic,
and its complete deterministic frontier output is identical to the primary
run, including all 41,526,965 recursive nodes and all witnesses. I did not
repeat the recorded 11-minute sanitizer run because its logs, source, build
flags, binary, and comparison are all manifest-bound and the fresh ordinary
run plus direct recursion harness already exercised the exact code.

## Live novelty and scope

On 2026-08-11 the live OEIS page for A392165 still displayed 39 terms ending
`..., 889, 1003, 1055, 1067, 1103`; its live b-file is byte-identical to the
frozen copy, SHA-256 `db9fdc99...8dbe`. The live A392164 b-file still ends at
`N=425` and is byte-identical to its frozen copy, SHA-256
`8b310617...f14`. Exact searches for the five-number string, `A392165 1407`,
and `f(1407)` with the squarefree-sumset context found no competing indexed
mathematical source. This supports only the report's dated public-novelty
scope, not an absolute claim about private or unindexed computations.

The live Erdos Problems material still marks Problem 1109 open and states the
asymptotic question and Konyagin bounds. A finite computation through 1500
cannot change those asymptotics. The live ErdosProblemADay page is dated
2026-07-24, says the conjecture remains wide open and that it found no exponent
improvement, and contains none of the five new indices. The bundle therefore
correctly describes this as a finite update to a prior site attempt, not the
site's first attempt and not progress on the parent asymptotic bound.

Sources checked live:

* <https://oeis.org/A392165>
* <https://oeis.org/A392165/b392165.txt>
* <https://oeis.org/A392164>
* <https://oeis.org/A392164/b392164.txt>
* <https://www.erdosproblems.com/1109>
* <https://erdosproblemaday.com/day/1109-squarefree-sumset>

## Non-load-bearing issue

`/usr/bin/cliquer` is dynamically linked. The bundle and `reproduce_1109.sh`
pin only its executable hash `d482f575...1d93`, not the algorithm-bearing
`libcliquer.so.1`. Both installed packages report Ubuntu version
`1.21-3build1` and `dpkg -V` reports no modification; the loaded library hashes
to `b1ccfac9465a0fc084b505d7415a8322da285705aaeb4f8f33f32cf926249c4e`.
This audit freezes copies and hashes of both. Future bundle revisions should
also pin or include the library (or package/source artifact). This is not a
gap in the finite theorem because the fresh primary computation and the
source-pinned, reproducibly built PMC audit each cover the full claimed range.

## Final assessment

No exhaustive boundary case, pruning rule, graph construction step, witness,
digest, sanitizer record, or novelty/scope statement failed audit. The finite
claim is accepted exactly as stated. Verdict: **PASS**.
