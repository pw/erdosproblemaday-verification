# Erdős problem 112: an unrestricted order-21 attack

Date: 2026-08-12 UTC

## Outcome

No 21-vertex `(I_3,L_4)`-free oriented graph was found, and no exhaustive
UNSAT certificate is claimed. The certified interval therefore remains

\[
                         21\le k(3,4)\le25.
\]

The run did produce three concrete advances for the next attack:

1. a complete six-case root-profile split for every hypothetical order-21
   witness;
2. an independent exact proof that none of the eight known cyclic order-20
   witnesses can be extended by one vertex without changing its old edges;
3. a definition-level checked order-21 near witness with no transitive
   four-tournament and exactly one independent triple.

## Live gate

The main page and dedicated proof-claim page were fetched through Bright Data
on 2026-08-12. The page was `OPEN`, with zero comments, zero claimed proofs,
no current worker, and no interested collaborator. The proof page said “No
proof claims have been submitted yet.” The live statement was unchanged.

## Six canonical root profiles

Let `v` be a vertex in a hypothetical 21-vertex `(I_3,L_4)`-free oriented
graph. Its out- and in-neighbourhoods are `(I_3,L_3)`-free, so each has size
at most 8 from the exact value `k(3,3)=9`. Its non-neighbourhood is
`(I_2,L_4)`-free, hence has size at most 7: a graph with no independent pair
is a tournament, and every tournament on 8 vertices contains a transitive
four-set. As the three neighbourhood sizes sum to 20, and reversing every arc
allows `out>=in`, the only profiles are

```text
(8,8,4), (8,7,5), (8,6,6), (7,7,6), (8,5,7), (7,6,7).
```

This is an elementary theorem-level reduction, not a solver observation.

## Definition-level SAT encoding

Each unordered vertex pair has exactly one of three states: forward arc,
reverse arc, or nonedge. Each triple receives the clause that at least one of
its pairs is an arc. For each four-set and each of its 24 linear orders, a
six-literal clause excludes the corresponding transitive tournament. The root
profile is fixed on consecutive labelled vertex blocks; arbitrary relabelling
makes this lossless. Redundant valid cardinality constraints impose
outdegree/indegree at most 8 and nondegree at most 7 at every vertex.

Each resulting profile CNF has 6,573 variables and 158,010 clauses. Parallel
Kissat probes on all six stayed unresolved and were interrupted after several
wall minutes; every result is **UNKNOWN**, not UNSAT. No proof logs were
produced, so no nonexistence conclusion is drawn from those runs.

## Exact nonextendability of the cyclic order-20 witnesses

For each of the eight cyclic witnesses from the previous report, the audit
fixes all 190 old pair states and exhaustively assigns the 20 ternary relations
from a new vertex. It rejects an assignment as soon as it creates an anchored
independent triple or transitive four-set. The independent backtracker visits
between 1,907 and 10,598 nodes per witness and finds no extension in all eight
cases. This is a finite exhaustive result checked directly from the
definition; a separate CaDiCaL encoding returned the same answers.

This does not rule out a non-Cayley order-21 witness, because such a witness
need not contain any of these fixed induced order-20 graphs.

## One-defect near witness

The local search reached defect score one repeatedly in profiles `(7,6,7)`
and `(7,7,6)`. The frozen near witness is encoded in
`verify_n21_artifacts.py` by its 210 lexicographic ternary pair states. The
definition-level audit, independent of the search score, verifies:

```text
order                         21
arcs                         137
nonedges                      73
root profile             (7,6,7)
transitive 4-tournaments       0
independent triples            1
unique independent triple  (5,13,16)
state SHA-256
  6be5046ca0dc52cbea5a6127f6f7ea8879831b7b5e325fe03b9a7955838cfa6f
```

The three vertices of the sole bad triple are exactly the vertices of
nondegree 8; every other vertex has nondegree at most 7. Thus the search lands
on the local-boundary obstruction predicted by the root-profile reduction.
Exact CaDiCaL Hamming-ball searches found no valid graph within 20 internal
pair-state changes of this near witness. A different score-one state also had
no repair within 20 changes. These Hamming-ball outcomes had no proof logs and
are recorded only as computational diagnostics.

The search also showed, without proof logging, that none of the eight cyclic
order-20 witnesses becomes extendable after at most eight changes among its
old pair states. Again, this is evidence only, not a published nonexistence
certificate.

## Reproduce the rigorous pieces

```bash
python3 verify_n21_artifacts.py
```

This uses only the Python standard library. The reference run took 4.74
seconds and printed:

```text
ROOT PROFILES: [(7, 6, 7), (7, 7, 6), (8, 5, 7), (8, 6, 6), (8, 7, 5), (8, 8, 4)]
NEAR N=21: arcs=137 nonedges=73 root_profile=(7,6,7) independent_triples=[(5,13,16)] transitive_fours=0 sha256=6be5046ca0dc52cbea5a6127f6f7ea8879831b7b5e325fe03b9a7955838cfa6f
NONEXTENDABLE C=(1, 2, 4, 14, 15, 17) backtracking_nodes=10598
NONEXTENDABLE C=(1, 2, 6, 12, 13, 15) backtracking_nodes=1907
NONEXTENDABLE C=(2, 3, 5, 6, 11, 12) backtracking_nodes=7943
NONEXTENDABLE C=(2, 4, 5, 7, 11, 14) backtracking_nodes=7008
NONEXTENDABLE C=(3, 5, 6, 16, 18, 19) backtracking_nodes=10598
NONEXTENDABLE C=(5, 7, 8, 14, 18, 19) backtracking_nodes=1907
NONEXTENDABLE C=(6, 9, 13, 15, 16, 18) backtracking_nodes=7008
NONEXTENDABLE C=(8, 9, 14, 15, 17, 18) backtracking_nodes=7943
ALL DEFINITION-LEVEL AUDITS PASSED
```

The exact CNF generator and search sources are included for continuation, but
their incomplete solver probes are not part of the proof.

PARTIAL: Every order-21 witness has one of six canonical root profiles; none
of the eight cyclic order-20 witnesses extends unchanged, and a checked
one-defect order-21 near witness has only the independent triple `(5,13,16)`;
the existence of an unrestricted order-21 witness remains unresolved.
