# Problem 86: a 1531-edge C4-free subgraph of Q9

Date: 2026-08-11 UTC

This bundle proves the explicit lower bound

```text
ex(Q_9, C_4) >= 1531.
```

It does not determine `ex(Q_9,C_4)` and does not settle the asymptotic
question in Erdos Problem 86.

## Certificate

`q9_edges_1531.json` contains 1531 distinct edges of the 9-dimensional
hypercube.  `verify_q9_witness.py` checks from the definition that every row
differs in one coordinate, enumerates all

```text
C(9,2) * 2^7 = 4608
```

square faces, and confirms that none is complete.  It separately enumerates
all length-two paths and confirms that no vertex pair has two common
neighbours.  Either check proves C4-freeness; together they are decorrelated
checks of the explicit witness.

The prior site certificate had 1506 edges.  The identified external public
certificate at repository commit `74e84382...` had 1505.  Both predecessors
are frozen under `provenance/`, and `compare_frontiers.py` compares the edge
sets and fixed hashes.  This is a 25-edge improvement over the site's earlier
result and a 26-edge improvement over that identified external certificate.
It is not an unconditional priority claim over private or unindexed work.

## Search boundary

The witness was found by repeatedly asking the frozen min-conflicts generator
to add one edge, starting from the audited 1506-edge certificate.  The
heuristic generator is provenance, not proof.  A final eight-thread attempt
to add edge 1532 was stopped after 180 seconds with no witness; that bounded
miss says nothing about existence or optimality.

Run `./reproduce.sh` for the manifest, certificate, and predecessor checks.
The reproducer also rebuilds the heuristic and repeats its deterministic
one-thread 1505-to-1506 positive control. That control compares edge sets;
the JSON files intentionally retain different descriptive source-path fields.
