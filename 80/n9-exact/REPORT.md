# Erdős Problem 80: exact finite frontier at nine vertices

Research and computation date: 2026-08-12 UTC.

## Scope and status

This is a finite computational extension of the existing local Problem 80
report.  It does **not** resolve the asymptotic Erdős--Rothschild problem and
does **not** claim novelty relative to all literature.

The live page was fetched through the Bright Data browser route before the
mathematical run.  It reported:

- status `OPEN`;
- `0 claimed proofs for this problem`;
- `Interested in collaborating: None`;
- `Currently working on this problem: None`;
- `I am working on formalising the results on this problem: None`.

The statement itself is now marked formalised (`Formalised statement? Yes`),
which is distinct from there being a current formaliser.  The sole discussion
comment only points to Potechin and additional Erdős citations.  Frozen page,
discussion, and LaTeX captures are in `sources/`.

## Definition and exact result

For a graph (G), let

\[
b(G)=\max_{uv\in E(G)} |N(u)\cap N(v)|,
\]

with (b(\varnothing)=0), and define

\[
M_k(n)=\max\{e(G): |V(G)|=n,\; 
  \text{every edge of }G\text{ is in a triangle},\; b(G)\le k\}.
\]

The independently checked finite result is

\[
\boxed{(M_0(9),M_1(9),\ldots,M_7(9))
       =(0,18,21,27,28,30,32,36).}
\]

The previous local report stopped at

\[
(M_0(8),\ldots,M_6(8))=(0,12,18,21,24,24,28).
\]

## Constructions

- (k=0): the empty graph.
- (k=1): the (3\times3) rook graph (L(K_{3,3})), with 18 edges.
  Every graph edge lies in exactly one row or column triangle.
- (k=2): the explicit 21-edge graph in `producer.out`; every one of its
  21 edges has codegree exactly 2.
- (k=3): (K_{3,3,3}), with 27 edges and every edge of codegree 3.
- (k=4): the complement of (K_2\mathbin{\dot\cup}C_7), with 28 edges
  and edge codegrees 3 or 4.
- (k=5): the complement of
  (K_3\mathbin{\dot\cup}3K_2), with 30 edges and edge codegrees 4 or 5.
- (k=6): the complement of (4K_2\mathbin{\dot\cup}K_1), with 32 edges
  and edge codegrees 5 or 6.
- (k=7): (K_9), with 36 edges and edge codegree 7.

`audit.py` reconstructs all seven nonempty witnesses from these descriptions
or from the frozen SAT rows and checks every edge directly.

## Elementary upper bounds for (k\ge3)

For any (n)-vertex graph with (e>0) edges and (b(G)\le k), an edge
(uv) satisfies

\[
d(u)+d(v)-n\le |N(u)\cap N(v)|\le k.
\]

Summing over edges and then applying Cauchy--Schwarz gives

\[
\sum_v d(v)^2\le e(n+k),
\qquad
e\le\frac{n(n+k)}4. \tag{1}
\]

For (n=9,k=3), (1) gives (e\le27), matching (K_{3,3,3}).

For the remaining caps, put (H=\overline G).  If (uv\notin E(H)), then

\[
|N_G(u)\cap N_G(v)|
=7-|N_H(u)\cup N_H(v)|. \tag{2}
\]

Thus a book cap (k) forces

\[
|N_H(u)\cup N_H(v)|\ge 7-k
\quad\text{for every nonedge }uv\text{ of }H. \tag{3}
\]

For (k=4), suppose (e(G)\ge29), so (e(H)\le7).  An isolated vertex
of (H) would force all other eight degrees to be at least 3 by (3), already
giving degree sum at least 24.  Hence (H) has no isolated vertex.  Two
degree-1 vertices that are nonadjacent have neighbourhood union of size at
most 2, so every pair of degree-1 vertices must be adjacent.  There are
therefore at most two of them.  But then

\[
\sum_v d_H(v)\ge2\cdot1+7\cdot2=16>14,
\]

a contradiction.  Hence (e(G)\le28).

For (k=5), suppose (e(G)\ge31), so (e(H)\le5).  An isolated vertex
would force each other degree to be at least 2, impossible with degree sum at
most 10.  With no isolates, the only possible degree multiset at five edges
is one 2 and eight 1s.  The two degree-1 neighbours of the degree-2 vertex
are nonadjacent and have the same singleton neighbourhood, contradicting
(3).  Hence (e(G)\le30).

For (k=6), if (e(G)\ge33), then (H) has at most three edges and hence
at least three isolated vertices.  A pair of them is a nonedge with empty
neighbourhood union, contradicting (3).  Hence (e(G)\le32).

Finally (e(G)\le36) is tautological for (k=7).  Together with the listed
constructions, these prove the five rows (k=3,\ldots,7) without exhaustive
search.

## The two computational boundaries

`producer.py` uses 36 edge variables and 84 triangle-witness variables.
Its clauses have the following literal meaning.

1. A selected triangle witness implies its three graph edges.
2. Every selected graph edge implies that at least one of its seven triangle
   witnesses is selected.
3. For every edge (uv) and every ((k+1))-set (W) of possible common
   neighbours, a clause forbids (uv) and all (uw,vw) ((w\in W)) from
   being present together.
4. A standard sequential counter requires at least the target number of
   graph edges.

Consequently the CNF is satisfiable exactly when the required graph exists.
PySAT 1.9.dev7 with CaDiCaL 1.9.5 returned:

| cap | target | result | conflicts | wall time in frozen run |
|---:|---:|:---:|---:|---:|
| 1 | 18 | SAT | 45 | 0.002 s |
| 1 | 19 | UNSAT | 48,381 | 1.275 s |
| 2 | 21 | SAT | 88 | 0.003 s |
| 2 | 22 | UNSAT | 1,102,737 | 49.824 s |

The timing and solver counters are evidence only, not inputs to the stable
claim digest.  The deterministic claim payload has SHA-256

`da127236a4419ec178b4c6d72334d6335a8e352ba63b37d0224afc232ae943b5`.

## Independent definition-level enumeration

As a separate route, nauty `geng` 2.8.8 generated one graph6 representative
of every unlabelled graph on nine vertices:

- records: 274,668;
- graph6 stream SHA-256:
  `ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9`.

`independent_scan.cpp` has its own graph6 decoder.  It directly intersects
adjacency bitsets for every edge, rejects a graph when any edge has codegree
zero, and records the maximum edge count under each book cap.  It returns the
same frontier.  The numbers of unlabelled graphs (not labelled graphs) by
exact booksize (0,1,\ldots,7) are

\[
1,14,1387,13466,25335,18227,5775,1044.
\]

`audit.py` is a third implementation.  It uses NetworkX 3.6.1's graph6
decoder and Python sets for common neighbourhoods.  Its full scan reproduces
the frontier, the exact-booksize counts, the 65,249 admissible unlabelled
graphs, and both SAT witnesses.

Because the property and edge count are invariant under relabelling, scanning
one representative of every isomorphism class is exhaustive.

## Local, OEIS, and literature collision audit

The tracked MathDyad/site report for Problem 80 contains the exact frontier
only through (n=8).  Searches of the tracked trees for `M_k(9)`, `M_{k}(9)`,
and the new row found no prior local computation.

The relevant OEIS item is A396149, "Number of connected graphs on (n)
vertices where every edge is part of at least one triangle."  It gives

\[
A396149(9)=62{,}286.
\]

The author's linked data repository (audited at commit
`a6f206696f7a7aa7348f1ef2ed80d4ba6440913d`) contains 26 marginal graph
invariants, but not booksize, edge codegree, or their joint distribution with
edge count.  Its (n=9) edge-count histogram has SHA-256

`6346ddef90b1312d732608b8c7c443284e0e932e992a1dc56b38eb3c447a34f5`.

The NetworkX audit finds exactly 62,286 connected graphs and matches that
entire histogram, not merely its sum.  The 65,249 possibly disconnected
aggregate is also not a novelty claim: it is the degree-9 Euler-transform
coefficient of A396149's connected counts.  What A396149 does not itself
tabulate is the book-cap frontier above.

Frozen OEIS searches returned no entry for `booksize`, `locally linear
graph`, or the old frontier row.  A broader every-edge/triangle search found
A396149 and A396364, among unrelated entries.  These search misses are not
evidence of novelty.

The July local report already audits the original Erdős paper, Fox--Loh,
Potechin, and Alon--Shraibman.  A fresh primary-source search also found
arXiv:2607.15071 and arXiv:2608.05947, both spectral booksize results under
additional hypotheses.  Their abstracts neither enumerate this finite class
nor state (M_k(9)).  Frozen arXiv API metadata is in `sources/`.

## Translation back to (f_c(9))

Let (E=\lceil81c\rceil).  Whenever (1\le E\le36), the finite definition
gives

\[
f_c(9)=\min\{k:E\le M_k(9)\}.
\]

Therefore

\[
f_c(9)=
\begin{cases}
1,&0<c\le2/9,\\
2,&2/9<c\le7/27,\\
3,&7/27<c\le1/3,\\
4,&1/3<c\le28/81,\\
5,&28/81<c\le10/27,\\
6,&10/27<c\le32/81,\\
7,&32/81<c\le4/9.
\end{cases}
\]

For (c>4/9), no simple nine-vertex graph has at least (81c) edges, so
the universal class is empty and there is no maximal finite (m) under the
literal wording.

## Reproduction

Run:

```bash
./reproduce.sh
```

It regenerates and hashes all 274,668 graph6 records, compiles and compares
the independent C++ scan, reruns all four SAT boundaries, and runs the
NetworkX audit.  The full path took about 76 seconds on this VM, single-core.

Environment: Python 3.12.3, python-sat 1.9.dev7, NetworkX 3.6.1,
nauty 2.8.8, and g++ 13.3.0 on x86-64 Linux.

PARTIAL: Computed and independently verified the exact nine-vertex frontier
(M_k(9)=(0,18,21,27,28,30,32,36)); the asymptotic Problem 80 remains open.
