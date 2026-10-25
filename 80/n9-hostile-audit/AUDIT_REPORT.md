# Cold hostile audit of the Problem 80 order-nine frontier

Audit date: 2026-08-12 UTC.

## Verdict

**PUBLISH.**  No mathematical, provenance, collision, coverage, or
reproducibility blocker was found.  No correction is required before
publication.

The finite result audited is

\[
(M_0(9),M_1(9),\ldots,M_7(9))
=(0,18,21,27,28,30,32,36).
\]

This is correctly labelled a finite computational extension and not a
solution of the asymptotic problem or a literature-wide novelty claim.

## Provenance and live gate

The three frozen Bright Data captures agree on the Problem 80 statement and
scope.  The frozen rendered page records `OPEN`, `0 claimed proofs`, no
interested collaborator, no current worker, and no current formaliser.  It
also records `Formalised statement? Yes`; the report correctly distinguishes
formalisation of the statement from a person currently formalising results.

I independently fetched the live page through Bright Data on 2026-08-12 UTC.
The material gate fields still matched the captures: OPEN, zero claimed
proofs, and no collaborator, current worker, or formaliser.  The ordinary web
route returned HTTP 403, which is why the anti-bot route was necessary.

A tracked-tree search in both MathDyad and ErdosProblemADay found no prior
order-nine row.  The existing tracked report stops at order eight, as stated.

## Definition and translation

The package uses

\[
b(G)=\max_{uv\in E(G)}|N(u)\cap N(v)|,
\]

with `b(empty)=0`, and maximises the number of edges subject to every edge
having positive codegree and `b(G) <= k`.  This exactly expresses the finite
book-cap problem.  For positive `c`, the integer edge threshold is
`ceil(81c)`, and inversion of the frontier gives all seven reported intervals.
The open/closed endpoints and the vacuous regime `c > 4/9` are correct.

The elementary upper bounds for caps 3 through 7 were checked line by line.
The degree-square inequality is valid.  In the complement arguments the
identity

\[
|N_G(u)\cap N_G(v)|=7-|N_H(u)\cup N_H(v)|
\]

is applied only when `uv` is a nonedge of `H`, so its use is exact.  The
degree arguments for caps 4, 5, and 6 close every case.

## SAT encoding and boundaries

The SAT model has one variable for each of 36 possible edges and one auxiliary
variable for each of 84 triples.  Its logic is exact:

1. selecting a triple auxiliary forces its three edge variables;
2. selecting an edge forces at least one incident triple auxiliary;
3. for a selected edge, every `(k+1)`-subset of possible common neighbours is
   forbidden from having all required two-edge paths selected;
4. a sequential cardinality counter imposes the requested edge lower bound.

Thus there are neither false positive graph models nor false negative graph
models.  SAT at 18/21 and UNSAT at 19/22 are the adjacent monotone boundaries
for caps 1/2.  The frozen CaDiCaL jobs reproduce.  As a hostile solver-family
cross-check, PySAT's Kissat 4.0.4 backend independently returned SAT, UNSAT,
SAT, UNSAT at those same four boundaries; the hard cap-2/22 job took about 56
seconds.  The independently regenerated full graph census below also proves
both boundaries without using SAT.

## Exhaustive coverage

The producer's complete reproduction passed from scratch.  Separately, this
audit bundle:

- regenerates `nauty-geng -q 9` rather than trusting the frozen graph file;
- obtains exactly 274,668 records and the expected graph6 SHA-256;
- byte-compares the regenerated and frozen streams;
- decodes graph6 itself, without NetworkX or the producer C++ decoder;
- directly evaluates edge coverage, codegrees, booksize, edge count, and
  connectivity;
- recovers 65,249 admissible unlabelled graphs;
- recovers the frontier and exact-booksize counts
  `1,14,1387,13466,25335,18227,5775,1044`;
- recovers the 62,286 connected graphs and byte-for-byte OEIS edge histogram.

One representative per isomorphism class is exhaustive because every tested
quantity is invariant under relabelling.  The producer C++ scanner, its
NetworkX audit, and this hostile decoder therefore provide three definition-
level implementations over the complete nauty census.

All seven nonempty extremal constructions were reconstructed independently.
Their edge counts, positive minimum codegrees, and book caps pass.  The two
SAT witnesses were also recomputed directly from their frozen edge lists.

## OEIS and novelty controls

The frozen OEIS A396149 record gives 62,286 connected order-nine graphs in
which every edge belongs to a triangle.  The linked author's edge-count file,
README, and metrics file byte-match immutable GitHub commit
`a6f206696f7a7aa7348f1ef2ed80d4ba6440913d`; the histogram SHA-256 is the one
reported by the producer.  The listed 26 invariants do not include booksize or
edge codegree.  The full 65,249 count is independently recovered as the
order-nine Euler transform of A396149, so the package correctly disclaims
novelty for that aggregate.

The frozen narrow OEIS search misses are represented as JSON `null`, while the
broader search captures A396149 and A396364.  The report explicitly says those
misses are not evidence of novelty.  Its literature language is correspondingly
limited: the two recent spectral papers are described only by what their
captured abstracts do not state.

## Reproducibility and integrity

The source `SHA256SUMS` covers all 28 non-manifest files and validates fully.
Its own SHA-256 is

`81bb81f74221296c626f613fb023f7e4cea050dad3293a08e37f865713f3ac74`.

The producer's `./reproduce.sh` passed in 2026-08-12's stated environment.  It
regenerated the complete graph stream, rebuilt and compared the C++ scanner,
reran all four SAT jobs, and reran the NetworkX audit.  This hostile audit's
own reproduction is intentionally small and takes the source bundle as an
explicit argument.

Optional hardening, not a publication requirement: the producer could run
`sha256sum -c SHA256SUMS` at the start of its reproduction script.  Integrity
is already independently checkable and was checked in this audit.
