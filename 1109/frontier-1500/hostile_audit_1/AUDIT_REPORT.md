# Cold hostile audit: Erdős Problem 1109 exact frontier bundle

Audit date: 2026-08-11 UTC  
Auditor: independent scout 4  
Audited bundle: `/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11`  
Bundle manifest SHA-256: `cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9`

## Verdict

**PASS** for publication as an exact finite computational result. I found no
mathematical, implementation, certificate, provenance, or reproducibility gap
that changes the claimed theorem. The result does not address the open
asymptotic part of Problem 1109.

The only count clarification is editorial and non-blocking: the manifest has
70 payload entries and covers every bundle file other than itself, so the
directory contains 71 files when the manifest is counted. The README states
the coverage convention correctly.

## Exact theorem audited

For

`f(N) = max{|A| : A subset {1,...,N} and every a+a' with a,a' in A is squarefree}`,

the bundle proves

```text
1103 <= N <= 1254: f(N) = 39
1255 <= N <= 1276: f(N) = 40
1277 <= N <= 1292: f(N) = 41
1293 <= N <= 1334: f(N) = 42
1335 <= N <= 1406: f(N) = 43
1407 <= N <= 1500: f(N) = 44
```

Thus the next five terms of OEIS A392165, relative to the live sequence on
the audit date, are `1255, 1277, 1293, 1335, 1407`.

## Proof audit

The graph reduction is exact. Vertices are those `a <= N` for which the
diagonal sum `2a` is squarefree, equivalently the odd squarefree integers.
Distinct vertices `a,b` are adjacent exactly when `a+b` is squarefree. A set
is valid if and only if it is a clique, with the vertex predicate accounting
for every diagonal sum.

The incremental induction is complete. If the old optimum is `r`, adding an
ineligible integer changes nothing. For an eligible new vertex `N`, an
`(r+1)`-clique exists exactly when the old-neighbor graph of `N` contains an
`r`-clique. A one-vertex extension cannot increase the optimum by more than
one, so one exact target decision at every eligible `N` determines the next
optimum. There are 163 such decisions from 1104 through 1500.

The primary recursion's pruning is sound. Its greedy color classes are
independent sets, so a clique takes at most one vertex from each class. The
reverse-class bound is therefore an upper bound, not a heuristic assertion.
The include branch intersects with the exact neighbor set and the subsequent
removal supplies the exclude branch. I ported the recursion independently and
compared it with literal subset enumeration on all 1,099 labelled graphs of
orders 1 through 5 and all their candidate pools, plus 3,000 deterministic
random graph/pool pairs of orders 6 through 12. All 232,063 target decisions
agreed.

Squarefreeness is integer-exact. I compared the bundle sieve with independent
trial division for every integer through 3000. The fixed 2048-bit graph width
is safe for the 610 eligible vertices through 1500, and assertions were active.

## Independent checks

1. The manifest hash matched the supplied hash, all 70 payload hashes passed,
   and coverage was exact. `./reproduce_1109.sh quick` completed in 25.92 s
   and passed all bundled checks.
2. `cold_check.py` independently regenerated all 163 DIMACS and Matrix Market
   graphs by trial division and matched every vertex count, edge count, graph
   hash, target, decision, positive witness, and canonical decision digest.
   It also checked the induction state against the primary log and the frozen
   OEIS base. It exited 0 in 13.61 s on one core.
3. All five lower witnesses were checked directly, including diagonal sums:
   820, 861, 903, 946, and 990 sums respectively (4,520 total). Every sum is
   squarefree and each maximum element is the claimed transition index.
4. A fresh one-core build and full primary run through 1500 exited 0 in
   96.38 s, visited 41,526,965 decision nodes, and reproduced all record
   transitions. The extracted transition log has a zero-byte diff against the
   frozen log. Building from the same relative source path reproduced the
   frozen binary SHA-256 exactly:
   `84ebeca91559cfa6caaff408059731d9a35f74f6f446edde0aa807895e93bdb8`.
5. The 163 frozen Cliquer decisions and independently regenerated graphs
   reproduce digest
   `6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84`.
   The raw-log timeout footer is non-semantic: the normalized certificate
   retains all 163 completed solver records and binds the raw-log hash.
6. The 163 frozen PMC decisions and independently regenerated graphs reproduce
   digest
   `cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3`.
   I also rebuilt PMC and reran every decision, using reversed vertex order and
   dynamically updating the optimum from solver outputs. It independently
   found exactly the five transitions and exited 0 in 74.58 s on one core.

## External solver provenance

The installed Cliquer executable matched the frozen SHA-256
`d482f5756fff600b4ec646bedeaa9e685b859fc3810be2c7faf078b18ea51d93`.
Its exact-size query is sufficient because every clique of size at least `r`
contains an `r`-clique.

I downloaded the official PMC archive at commit
`06594a0ee1cde5a04f1679aff28072668da96062` and compared it with the bundled
source. The file sets and contents matched before applying the documented
compiler-only change from `return ifile;` to `return ifile.good();`. A one-core
rebuild reproduced the frozen PMC binary SHA-256 exactly:
`e64c831e961bd18242e3cdd8b167dafc3322d667c3d90907eafc75720493f62d`.
The driver emits explicit target-found or target-impossible conclusions, and
the audit rejects ambiguous output and directly rechecks every positive clique.

Negative Cliquer and PMC answers are solver transcripts rather than formally
checkable unsatisfiability certificates. That is a residual characteristic of
the computational proof, not a publication gap here: the custom exhaustive
implementation has an inspected proof of pruning, passed independent brute
force comparison, and was freshly rerun; PMC was freshly rebuilt and replayed;
and all three implementations agree on every incremental decision.

## Novelty and source scope

The live Problem 1109 page on 2026-08-11 reported `OPEN`, zero claimed proofs,
and nobody currently working. Live OEIS b-files exactly matched the frozen
copies:

```text
8b310617ac471f133d13575fdaae89f75644ab4914ceabf244c6f5bf1733bf14  A392164 b-file
db9fdc992230ab6e7f5996cb55e5d334d4bac13014711dc1f34de64316b08dbe  A392165 b-file
```

A392165 still ended with `1103 -> 39`. Searches for the proposed five-term
string, paired new values, `A392165` with `1255` or `1407`, and `f(1407)` in
the squarefree-sumset context found no prior mathematical posting. This is a
dated public-source check, not proof against private or unindexed computation.

The bundled Erdős-Sárközy 1987 scan has the claimed source hash and explicitly
quantifies over all `a,a' in A`, confirming that diagonal sums belong in the
definition. Konyagin's official 2004 record and abstract were checked against
the cited bibliographic data. The local site already treated #1109 on
2026-07-24, so the publication must describe this strictly as a new finite
extension, not a first attempt or an asymptotic advance.

## Artifact map

`cold_check.py` and `cold_check.log` contain the independent arithmetic,
graph-regeneration, transcript, digest, induction, witness, OEIS, and manifest
audit. `pruning_bruteforce.py` and its log contain the hostile recursion check.
`replay_pmc_reversed.py` and its log contain the fresh independent PMC replay.
`primary_fresh.stdout`, `primary_fresh.stderr`, and
`primary_transition_diff.log` contain the fresh primary run and comparison.
The `live_*_20260811.txt` files preserve the date-stamped public-source inputs.

