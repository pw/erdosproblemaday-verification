# Erdős Problem 1109: exact finite frontier through 1500

Date of computation and source check: 2026-08-11 (UTC).

## Result and scope

Let $f(N)$ be the largest size of a set
$A\subseteq\{1,\ldots,N\}$ for which every member of
$A+A=\{a+a':a,a'\in A\}$ is squarefree.  The exact new record indices are

```
f(N)=40 first at N=1255
f(N)=41 first at N=1277
f(N)=42 first at N=1293
f(N)=43 first at N=1335
f(N)=44 first at N=1407
```

Equivalently, the newly certified constant intervals are

```
1103 <= N <= 1254: f(N)=39
1255 <= N <= 1276: f(N)=40
1277 <= N <= 1292: f(N)=41
1293 <= N <= 1334: f(N)=42
1335 <= N <= 1406: f(N)=43
1407 <= N <= 1500: f(N)=44
```

The primary computation also reproduces every previously published
record index through 1103.  As checked on 2026-08-11, OEIS A392165 contained
39 terms and ended

```
..., 889, 1003, 1055, 1067, 1103.
```

Thus the finite novelty claim is exactly the next five terms

```
1255, 1277, 1293, 1335, 1407
```

of A392165, together with exact values through $N=1500$, relative to the
live OEIS and web sources checked on that date.  This does **not** improve an
asymptotic bound and does **not** resolve any part of Erdős's conjecture that
$f(N)\leq N^{o(1)}$, perhaps even $f(N)\leq(\log N)^{O(1)}$.

## Source status and provenance

* [Erdős Problems #1109](https://www.erdosproblems.com/1109), accessed
  2026-08-11, states the definition above and marks the asymptotic problem
  OPEN, with no claimed proof and nobody listed as currently working.
* [OEIS A392164](https://oeis.org/A392164), accessed 2026-08-11, is $f(N)$.
  Its linked b-file then tabulated exact values only through $N=425$.
* [OEIS A392165](https://oeis.org/A392165), accessed 2026-08-11, is the
  sequence of record indices.  Its b-file had 39 terms and ended at 1103;
  the last four terms were credited to Chai Wah Wu on 2026-01-12.
* Erdős and Sárközy, *On divisibility properties of integers of the form
  a+a'*, Acta Math. Hungar. 50 (1987), 117-122, is the primary source.  It
  includes the diagonal case $a=a'$, as does the computation here.
* Konyagin, *Problems on the set of squarefree numbers*, Izvestiya:
  Mathematics 68:3 (2004), 493-520, DOI
  `10.1070/IM2004v068n03ABEH000486`, is the source of the presently quoted
  asymptotic improvement.
* The existing ErdosProblemADay page already had an analytic #1109 attempt
  dated 2026-07-24.  This result is an exact finite update to that attempt,
  not the site's first treatment of #1109.

The frozen copies `oeis_A392164_bfile_accessed_2026-08-11.txt` and
`oeis_A392165_bfile_accessed_2026-08-11.txt` record the exact OEIS data used
for the comparison.  The downloaded primary Erdős-Sárközy PDF is
`erdos_sarkozy_1987_13.pdf`.

## Exact graph reduction

Define a graph $G_N$ as follows.

* Its vertices are the integers $a\leq N$ for which $2a$ is squarefree.
  Equivalently, these are the odd squarefree integers at most $N$.
* Two distinct vertices $a,b$ are adjacent exactly when $a+b$ is
  squarefree.

Then

\[
f(N)=\omega(G_N).
\]

Indeed, if $A$ is valid, its diagonal sum $a+a=2a$ shows that every
$a\in A$ is a vertex, and each distinct pair in $A$ is an edge.  Thus
$A$ is a clique.  Conversely, the vertex condition checks every diagonal
sum and the edge condition checks every distinct pair sum, so every clique
is a valid set $A$.  No sum in $A+A$ is omitted.

## Incremental completeness proof

Suppose the exact old optimum is $r=\omega(G_{N-1})$.

* If $2N$ is not squarefree, $N$ is not a vertex and $G_N=G_{N-1}$.
* Otherwise add the new vertex $v=N$.  A clique excluding $v$ has size at
  most $r$.  A clique including $v$ consists of $v$ plus a clique in
  the old-neighbor graph $G_{N-1}[\Gamma(v)]$.  Consequently

  \[
  \omega(G_N)=r+1
  \quad\Longleftrightarrow\quad
  \omega(G_{N-1}[\Gamma(v)])\geq r.
  \]

  The optimum can increase by at most one when one vertex is added.

Starting from the trivial base $f(1)=1$, the program applies precisely this
decision at every later eligible integer through 1500.  Induction therefore
proves the exact optimum at every prefix, not only at the five reported
record points.

## Exhaustive clique decision

The primary C++ verifier represents candidate sets and adjacencies by fixed
2048-bit arrays (only 610 vertices are used at $N=1500$).  At each recursive
node it does the following.

1. If the chosen clique already has the target size, return a witness.
2. If `chosen size + candidate count < target`, reject the node.
3. Greedily partition the candidates into independent color classes
   $C_1,\ldots,C_c$.  A clique uses at most one vertex from each class.
4. Scan the vertices in reverse class order.  Before a vertex with class
   number $j$, every remaining branch candidate lies in
   $C_1\cup\cdots\cup C_j$.  If `chosen size + j < target`, reject all
   remaining branches.
5. The include branch intersects the pool with that vertex's exact neighbor
   set.  After it returns false, removing the vertex gives the exclude
   branch.  Hence the two branches exhaust all candidate cliques.

The coloring is used only as a rigorous upper bound; it is not assumed to be
optimal.  Every other rejection is a cardinality bound.  Thus every failed
decision is an exhaustive proof that the required clique does not exist.

Squarefreeness is computed exactly by initially setting all entries through
$2N$ true and marking every multiple of every square $d^2$, $d\geq2$,
false.  There is no probabilistic primality or floating-point step.  The
build does not define `NDEBUG`, so all graph-size, published-prefix, and
witness assertions remain active.

The run at $N=1500$ used 610 eligible vertices and visited 41,526,965
recursive decision nodes.  It reproduced all 39 terms then present in
A392165 before finding the five new records.

## Lower certificates

Each line is a directly checkable clique in $G_N$, including all diagonal
sums.  The verifier checks every one of its $k(k+1)/2$ sums.

```
f(1255) >= 40:
{31,35,51,123,139,143,159,231,247,251,267,323,335,339,359,371,
443,463,467,535,555,623,647,659,663,731,751,771,843,859,863,947,
967,971,1039,1055,1163,1167,1235,1255}

f(1277) >= 41:
{5,41,53,65,77,105,141,161,213,221,249,281,293,305,321,341,353,
377,461,521,593,641,653,665,677,713,761,861,881,893,941,965,1077,
1121,1181,1193,1217,1241,1253,1265,1277}

f(1293) >= 42:
{5,41,53,65,77,105,141,161,213,221,249,281,293,305,321,341,353,
377,461,521,593,641,653,665,677,713,761,861,881,893,941,965,1077,
1121,1181,1193,1217,1241,1253,1265,1277,1293}

f(1335) >= 43:
{23,35,71,83,95,107,119,183,191,251,263,291,311,323,335,551,611,
623,635,647,671,683,695,707,719,791,851,863,911,923,1151,1163,
1211,1223,1235,1247,1263,1271,1283,1295,1307,1319,1335}

f(1407) >= 44:
{23,35,71,83,95,107,119,183,191,251,263,291,311,323,335,551,611,
623,635,647,671,683,695,707,719,791,851,863,911,923,1151,1163,
1211,1223,1235,1247,1263,1271,1283,1295,1307,1319,1335,1407}
```

Together with the exhaustive failed decisions immediately before each
transition and through $N=1500$, these witnesses prove equality throughout
the six intervals in the result table.

## Independent audit

The external audit uses the Ubuntu-packaged
[Cliquer 1.21](https://users.aalto.fi/~pat/cliquer.html) executable by
Sampo Niskanen and Patric Östergård (Ubuntu package version 1.21-3build1),
SHA-256
`d482f5756fff600b4ec646bedeaa9e685b859fc3810be2c7faf078b18ea51d93`.
It differs from the primary verifier in the two load-bearing components:

* squarefreeness is recomputed by direct trial division rather than a sieve;
* maximum-clique decisions are made by the external Cliquer implementation,
  from independently generated DIMACS graphs, rather than the custom C++
  coloring recursion.

The audit starts from the published and separately reproduced value
$f(1103)=39$.  For each of the 163 eligible new vertices
$v\in\{1104,\ldots,1500\}$, it independently generates the old-neighbor
graph and asks Cliquer whether it contains a clique of exactly the current
size $r$.  The command uses `-m r -M r`; this is sufficient because every
clique of size at least $r$ contains one of size exactly $r$.  A negative
answer therefore eliminates every $(r+1)$-clique whose largest vertex is
$v$, while a positive answer is mapped back to the original integers, joined
with $v$, and checked directly.  This decomposes all six boundary upper
checks by their largest vertex and covers every eligible vertex, not only the
five transition points.  Ineligible integers require no call because their
graphs are unchanged.

The external run asserts that its only positive decisions are exactly
1255, 1277, 1293, 1335, and 1407.  It sorts all 163 results, records the
neighbor and edge counts, SHA-256 of every generated DIMACS graph, and every
positive witness, then hashes that complete deterministic record.  Cliquer's
`reverse` vertex ordering changes only search order.  The completed digest is
`6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84`.
The normalized 163-record certificate has SHA-256
`30047bb3157b037a8122c56162e6fb89367f261aa7234604bb30fadb2aefd5ba`.

The original run was started inside a 3600-second GNU `timeout`.  At 3304
seconds the outer timeout process alone was deliberately detached so it could
not kill a still-running exact search.  The Python audit and all Cliquer
children continued, eventually printed all 163 sorted records, the digest,
and the concluding assertion.  This is why the raw log contains a signal-9
timing footer in its middle.  The raw log is retained with SHA-256
`eb871ca90a7830424f82a9f77c90bd3a6a8eada181fb80d9595c1170966ec973`;
the normalized certificate removes scheduling output but preserves every
deterministic record and explicitly binds itself to that raw-log hash.

A second complete external audit uses the exact `k`-clique mode of
[PMC](https://github.com/ryanrossi/pmc) at official commit
`06594a0ee1cde5a04f1679aff28072668da96062`.  The only semantic source change is the
documented compiler-compatibility replacement of `return ifile;` by
`return ifile.good();`; it does not touch graph parsing or search.  Its
binary has SHA-256
`e64c831e961bd18242e3cdd8b167dafc3322d667c3d90907eafc75720493f62d`.
This audit independently generates Matrix Market graphs, runs
`-a 0 -k r -t 1` for every one of the same 163 decisions, parses an explicit
found-or-no-clique result, maps every positive solver witness back to the
integers, and rechecks all of its sums by trial division.  It again found
exactly the five claimed transitions.  Its deterministic result digest is
`cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3`;
the two-worker run took 35.59 seconds and exited 0.

A final cold checker parses both external logs, regenerates all 163 graphs in
both formats by direct trial division, verifies every vertex count, edge
count, graph hash, target, decision, and positive witness, recomputes both
digests, and compares all decisions with the primary C++ log.  It reports
exact agreement and exited 0; its frozen log has SHA-256
`6d6a9b17aba63c25f173fc68edae172f1ad8916e0653b41a40e7eaeb154ae322`.

The C++ verifier was also rebuilt with AddressSanitizer and
UndefinedBehaviorSanitizer, with assertions enabled, and rerun through 1500.
That run reproduced the same frontier with no sanitizer diagnostic.

## Reproduction

Primary build and run:

```sh
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  verify_1109_frontier.cpp -o verify_1109_frontier
./verify_1109_frontier 1500
```

Independent external audit and direct witness check:

```sh
python3 audit_1109_incremental_parallel_cliquer.py --jobs 6
python3 audit_1109_incremental_pmc.py --jobs 2
python3 check_1109_witnesses.py
python3 check_1109_external_audits.py
python3 make_1109_cliquer_certificate.py
```

The arbitrary-width Python reproduction of the old public frontier is:

```sh
python3 verify_1109_frontier.py 1103
```

It is representation-independent of the fixed-width C++ implementation, but
uses the same coloring-bound recursion; it is therefore a separate
implementation check, not a separate clique algorithm.  The external
Cliquer and PMC runs supply algorithmically independent checks for the new
range.

Recorded toolchain: Ubuntu g++ 13.3.0.  The frozen primary run took 1:36.50
wall time and 4,988 KB maximum resident memory on this VM.  The exact source,
binary, compile log, run log, sanitizer logs, external-audit source and log,
source snapshots, and their SHA-256 hashes are listed in
`erdos1109_manifest_2026-08-11.sha256`.

## What remains open

This is a finite exact extension only.  Problem #1109 asks for the growth of
$f(N)$; the gap between the known asymptotic lower and upper bounds, and in
particular Erdős's $N^{o(1)}$ and polylogarithmic questions, is unchanged.
