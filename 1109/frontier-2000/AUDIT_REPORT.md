# Hostile audit of Erdos Problem 1109 through N=2000

Audit date: 2026-08-11 UTC.

## Verdict: PASS

The exact finite extension passes hostile audit. The complete primary C++ run
exited 0, every one of its 201 post-1500 decisions agrees with the independent
PMC transcript, all reported witnesses pass direct diagonal-inclusive checks,
and the frozen base `f(1500)=44` has a separately verified manifest. No gap was
found in the graph reduction, transition convention, solver semantics, source
identity, or dated publication scope.

## Claim and exact scope

Let `f(N)` be the largest cardinality of a set
`A subseteq {1,...,N}` such that `a+a'` is squarefree for every ordered choice
`a,a' in A`. The proposed additional record indices after 1500 are:

```text
f(N)=45 first at N=1509
f(N)=46 first at N=1535
f(N)=47 first at N=1595
f(N)=48 first at N=1707
f(N)=49 first at N=1735
f(N)=50 first at N=1779
f(N)=51 first at N=1835
f(N)=52 first at N=1919
f(N)=53 first at N=1991
f(N)=54 first at N=1999
```

Equivalently, the extension claims these exact constant intervals:

```text
1501 <= N <= 1508: f(N)=44
1509 <= N <= 1534: f(N)=45
1535 <= N <= 1594: f(N)=46
1595 <= N <= 1706: f(N)=47
1707 <= N <= 1734: f(N)=48
1735 <= N <= 1778: f(N)=49
1779 <= N <= 1834: f(N)=50
1835 <= N <= 1918: f(N)=51
1919 <= N <= 1990: f(N)=52
1991 <= N <= 1998: f(N)=53
1999 <= N <= 2000: f(N)=54
```

This is a bounded exact computation. It does not improve either asymptotic
bound in Problem 1109 or resolve the conjectured subpolynomial or
polylogarithmic growth.

## Quantifiers and graph reduction

Define `G_N` with one vertex for every integer `a <= N` such that `2a` is
squarefree, and join distinct vertices `a,b` exactly when `a+b` is squarefree.
Then `f(N)=omega(G_N)`.

The vertex condition is essential: the phrase "every a,a' in A" includes
`a=a'`, so it checks every diagonal sum `2a`. An edge checks each remaining
distinct pair. Conversely, a clique satisfies every diagonal and off-diagonal
sum, so no quantifier or sum in `A+A` is dropped. The eligible vertices are
equivalently the odd squarefree integers.

Suppose the exact old value is `r=omega(G_(n-1))`.

* If `2n` is not squarefree, `G_n=G_(n-1)` and the value is unchanged.
* Otherwise, any new clique either omits `n` and has size at most `r`, or is
  `n` plus a clique in the old-neighbor graph `G_(n-1)[Gamma(n)]`.
  Consequently `f(n)=r+1` exactly when that neighbor graph has an `r`-clique.
  Adding one vertex cannot raise the optimum by more than one.

Thus one exact decision for every eligible `n`, in increasing order, is an
induction proving all prefixes. At a decision line `n=X target=r exists=1`,
the convention is that `f(X-1)=r` and `f(X)=r+1`; `X` is the first index of
the new value. Since 2000 is ineligible, `f(2000)=f(1999)`.

## Base case

The extension starts from the separate bundle
`/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11`. Its manifest
was rechecked in full with exit status 0 (`base_manifest_check.log`). Its exact
result is `f(1500)=44`, first attained at 1407, and it proves every prior
prefix from the trivial initial value. The base manifest itself has SHA-256
`cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9`.

This extension therefore does not silently assume an unpublished heuristic
at 1500. The extension-only PMC induction relies on that separately audited
computation, while the full primary run starts at 1 and recomputes the base as
well. Publication should link both bundles.

## Primary C++ verifier audit

The primary source is `verify_1109_frontier.cpp`, SHA-256
`c83925b18b75c2ba8f909503eae7e30b930c19e3ee5f123bdd9c49873b1a04e5`.
It is byte-identical to the assigned source and was compiled with Ubuntu g++
13.3.0 using `-std=c++20 -O3 -Wall -Wextra -Wpedantic`, without `NDEBUG`.
The running binary has SHA-256
`cd1525ec401080dd2c687a7b02757e3a6db1519a8a8f9a854cc98c8ed0fc3027`.
An independent rebuild using the exact source path and command is
byte-identical to the running binary (`primary_exact_rebuild`). The source path
matters because assertion expansions embed it in the executable.

The squarefree table starts true, marks 0 false, and marks every multiple of
every square `d^2`, `d>=2`, false through `2*MAX_N`. This is an exact integer
sieve. For each eligible `n`, the program creates precisely the old-neighbor
set and asks for a clique of the old optimum size. Each reported witness is
mapped back to integers, joined with `n`, sorted, and checked over all
`k(k+1)/2` sums, including the diagonal.

The clique decision is exhaustive:

1. Cardinality rejects a branch only when chosen plus remaining is too small.
2. A greedy partition of the pool into independent color classes is an upper
   bound because a clique uses at most one vertex per class.
3. Vertices are scanned in reverse color order. After higher positions have
   been excluded, every remaining vertex has color at most the current bound.
4. The include branch intersects with the exact adjacency, and after it is
   exhausted the vertex is removed for the exclude branch. These branches
   partition every possible clique.

The 2048-vertex, 32-word fixed representation is within bounds: only 811
eligible vertices occur through 2000. Candidate pools never contain the newly
added vertex, even though the word count includes its zero bit. Assertions
check capacity, all 39 published transition indices, and every positive
witness.

As a direct challenge to this reasoning, `primary_solver_fuzz.cpp` includes
the exact solver implementation and compares it with brute-force enumeration
on 4,000 deterministic random graphs (up to 12 vertices), including random
candidate subsets and every target from 0 through `n+1`. Its ASan/UBSan run
checked 34,102 decisions, found exact agreement, emitted no sanitizer
diagnostic, and exited 0.

The completed run reports `eligible_vertices=811`, `final_f=54`, and
`decision_nodes=2432586214`. It used 1:58:18 wall time, 6,669.26 user seconds,
5,052 KiB maximum resident memory, and exited 0. Its stdout and stderr SHA-256
values are
`c7a2a40d52c963d9e172bb254485a5a2c9443d07d7e1564eb9696e79e3bf69b6`
and
`c812b39784462e78ffcddc83ca4e7e1b60fb382b1c26c46377580c1c59a0b33b`.

`check_primary_completion.py` parses the closed transcripts, checks all 54
transition indices and 27,720 witness sums, confirms the final counters and
clean timing footer, and compares all 201 extension tuples `(n,target,exists)`
with PMC. They agree exactly; the tuple-only digest is
`9b47281e082359f6dbaae39e0930e37248b5ec413b44dfcce9ed25f61f54873f`.
The checker exited 0.

## Full PMC audit

The external audit uses PMC commit
`06594a0ee1cde5a04f1679aff28072668da96062`. The frozen official-source tarball
has SHA-256
`559cff717b1a05784724253714f9b82e4868627fa8935b86b9e4e2b3946bb758`.
An independent fresh clone checked out that exact commit; its `git archive`
tar stream and the decompressed frozen tarball are byte-identical, both with
SHA-256 `268702f373a9056293c18f25f33fba94a872491cb63fef43a23cb44e5195c120`.
The only patch changes the obsolete stream conversion in file-existence code
from `return ifile;` to `return ifile.good();`; its SHA-256 is
`a85d9a81fe4cd3927177cc710d3da660253a9b2b3e94aedebef9250396df94e2`.
A cold rebuild produced a byte-identical binary, SHA-256
`e64c831e961bd18242e3cdd8b167dafc3322d667c3d90907eafc75720493f62d`.

`audit_1109_1501_2000_pmc.py` recomputes squarefreeness by direct trial
division, independently generates each old-neighbor graph, writes all edges
as one-based lower-triangular Matrix Market entries, and invokes:

```text
pmc_1109_audit -f GRAPH -a 0 -k TARGET -t 1 -o kcore -v
```

The PMC reader was inspected: it consumes those lower-triangular entries and
explicitly symmetrizes them. In PMC's `-k k` mode the lower bound is set to
`k-1`, the requested upper threshold is `k`, a positive result terminates only
after finding a clique of size at least `k`, and a negative result follows
exhaustion. Here `k-1` is a decision incumbent, not a claimed witness: pruning
occurs only when a branch cannot exceed it, which is exactly the `k`-clique
decision. The verbose witness uses one-based matrix indices, exactly matching the audit's
mapping. `-t 1` makes each solver invocation single-threaded.

PMC's compiled input class defaults to a one-hour internal time limit (its
usage text is stale and says seven days), and its negative text would not by
itself distinguish a timeout. This hazard is absent in the frozen run:
all 201 processes returned normally with exit status 0, and the slowest full
subprocess wall time was 144.495 seconds. Because this timing surrounds the
entire subprocess, the 3,600-second internal limit cannot have fired. The
aggregate driver consumes rather than preserves each solver's raw text, so no
stronger claim about retained timeout-message text is made. The complete
eight-job driver used 9:19.51 wall time and exited 0.

The strict driver receives the candidate transition list to set later targets,
but this is not circular. Starting from exact `f(1500)=44`, the first omitted
real transition would produce an unexpected positive result and the first
spurious listed transition an unexpected negative result, before any later
target could be affected. It checks every one of the 201 eligible values, not
only boundary points.

The exact positive decisions are precisely

```text
1509,1535,1595,1707,1735,1779,1835,1919,1991,1999
```

and the deterministic all-record digest is
`aaaeea014ef1cc96993416d05f49e692359166b6f17e7be24211779353a3a549`.
The raw strict log has SHA-256
`9c15d3a89b7b1d74f1a6bb27e502541941bf9eeebb55fa4ef90b76fe7ec09843`.
The exact driver and GNU-time record have SHA-256 values
`b3ceb997a035f83b5f617209004088feb7086ab6380841eeb6198c1f1aff4b8c`
and `a5000d2ba35058a3e2f7c09aa486502816eadbd5bba689a95d22c15b0df3e0c8`.
The compact `pmc_positive_witnesses.txt` extracts the ten directly checkable
lower certificates from that log. The dependency-free
`check_positive_witnesses.py` checks all 12,540 required sums in milliseconds.

`cold_check_extension.py` uses a smallest-prime-factor implementation,
regenerates all 201 graphs, checks every vertex count, edge count, and graph
hash, rechecks the ten positive witnesses over 12,540 diagonal-inclusive
sums, validates targets and transition convention, recomputes the digest and
intervals, confirms the no-timeout bound and process exit, and exits 0.

## Additional hostile checks

* `pmc_variant_spot_check.py` uses PMC's different exact algorithm 1 and
  degree ordering on negative/positive pairs around the first two transitions
  and the final transition: 1501/1509, 1533/1535, and 1997/1999. It rejects
  all three tested pre-transition targets, finds valid post-transition witnesses,
  observes no time limit, and exits 0.
* `cpsat_boundary_check.py` independently formulates the neighbor problem as
  Boolean selection with one constraint per nonedge. OR-Tools CP-SAT 9.15.6755
  returns the exact `INFEASIBLE` status for a 44-clique at `n=1501` and
  `OPTIMAL` with a directly checked 45-element witness at `n=1509`. It does
  not return `UNKNOWN`; the run exits 0.
* `pmc_solver_fuzz.py` differentially tests the exact frozen PMC binary,
  lower-triangular Matrix Market parser, and `-k` decision mode on 580 targets
  from 200 deterministic random graphs of up to 14 vertices. Brute-force
  maximum-clique enumeration agrees on every decision and all returned
  witnesses; the run exits 0.
* The primary solver sanitizer fuzz described above is representation-level
  evidence independent of the number-theory graph family.

The algorithm-1 checks share PMC's graph parser and are supporting evidence,
not a third independent implementation. CP-SAT is independent but covers two
boundary decisions. The load-bearing full upper certificates are the custom
C++ search and the 201 PMC algorithm-0 decisions.

## Current source and OEIS provenance

The live rendered page <https://www.erdosproblems.com/1109> was accessed on
2026-08-11 through a browser because plain requests receive HTTP 403. The
snapshot records `OPEN`, 0 claimed proofs, nobody currently working, nobody
interested in collaborating, and last page edit 2025-12-03. Its two comments
only report an exact computation through `N=250`; neither contains the proposed
extension. The snapshots are `live_1109_20260811.txt` and
`live_1109_comments_20260811.txt`.

OEIS A392164 defines the same function; its table still ends at `N=425`.
OEIS A392165 is the record-index sequence and, as fetched on 2026-08-11, still
contains 39 terms ending

```text
...,889,1003,1055,1067,1103.
```

The exact A392164 and A392165 snapshots have SHA-256 values
`8b310617ac471f133d13575fdaae89f75644ab4914ceabf244c6f5bf1733bf14`
and
`db9fdc992230ab6e7f5996cb55e5d334d4bac13014711dc1f34de64316b08dbe`,
respectively. They are byte-identical to the base bundle's snapshots.

The downloaded primary paper is P. Erdos and A. Sarkozy, "On divisibility
properties of integers of the form a+a'", Acta Math. Hungar. 50 (1987),
117-122. Its first page explicitly requires squarefreeness for all `a in A`
and `a' in A`, hence includes `a=a'`. The PDF SHA-256 is
`179cf92b5b70a179290e00c78d03a0ec5de7d008f4189c37ed99077389f3dae3`.

The official Math-Net record for S. V. Konyagin, "Problems on the set of
squarefree numbers", Izvestiya: Mathematics 68:3 (2004), 493-520, DOI
`10.1070/IM2004v068n03ABEH000486`, defines the same `ES_N` with squarefree
`a+a'` for all two choices and supplies the current asymptotic improvement.
Its rendered abstract is frozen as `konyagin_mathnet_im486_20260811.txt`.
No checked primary source gives the proposed finite record indices.

Exact-phrase searches for the proposed term blocks and `f(2000)` found no
matching mathematical publication. This is dated search evidence, not proof
that nobody has privately computed or published the values in an unindexed
source.

## Publication-safe scope

The publication-safe claim is:

> Conditional only on the separately audited exact base `f(1500)=44`, exact
> last-vertex decisions for every eligible integer through 2000 give the ten
> further record indices 1509, 1535, 1595, 1707, 1735, 1779, 1835, 1919,
> 1991, and 1999, and prove `f(2000)=54` together with every intervening value.

Relative to the live OEIS endpoint 1103, the combined base and extension have
15 additional record indices. Only the last ten are new relative to the
already frozen/site-published through-1500 result. Do not call all 15 newly
computed by this extension, do not describe this as the first treatment of
Problem 1109, and do not claim any asymptotic advance.

## Reproduction map

The audit directory is self-contained for the extension checks. Important
commands, run from this directory, are:

```sh
./reproduce_1109_2000_quick.sh [--base-dir PATH]

# Individual checks used by quick mode:
python3 cold_check_extension.py
python3 check_positive_witnesses.py
python3 check_primary_completion.py
python3 pmc_variant_spot_check.py
python3 pmc_solver_fuzz.py
python3 cpsat_boundary_check.py
g++ -std=c++20 -O1 -g -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  primary_solver_fuzz.cpp -o primary_solver_fuzz
./primary_solver_fuzz
sha256sum -c MANIFEST.sha256
```

The CP-SAT and alternate-PMC commands are supporting reruns and can take
several minutes. Reproducing all 201 PMC decisions or the full primary run is
substantially slower; their exact sources, binaries, raw logs, timing files,
and cold checkers are frozen here.
