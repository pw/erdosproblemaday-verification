# Erdos Problem 86: a 1506-edge C4-free subgraph of Q9

## Exact claim

This bundle proves only

```text
ex(Q_9, C_4) >= 1506.
```

It does not determine `ex(Q_9,C_4)`, and it does not resolve the asymptotic
question in Erdos problem 86.

## Certificate proof

`q9_edges_1506.json` lists 1506 distinct pairs of vertices in `0..511`.
Every pair differs in exactly one bit, so every row is an edge of `Q9`.

A four-cycle in a hypercube alternates two coordinate directions and is
therefore one of its square 2-faces.  There are

```text
C(9,2) * 2^(9-2) = 4608
```

such faces.  `verify_faces.py` enumerates all 4608 and confirms that none has
all four edges in the certificate.  Hence the listed graph is C4-free and the
stated lower bound follows.

`verify_cherries.py` is a logically separate check: it confirms that no
unordered pair of vertices has two common neighbors.  That condition is
equivalent to C4-freeness for a simple graph.

The canonical witness hash is:

```text
883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c  q9_edges_1506.json
```

`q9_edges_1506.txt` is the same certificate as plain `u v` rows.

## Public comparison

The live problem-86 forum snapshot from 2026-08-11 reports a public explicit
Q9 certificate with 1505 edges, posted 2026-05-22.  The corresponding GitHub
certificate is frozen under `q9_upstream/` at repository commit
`74e84382cbbc20b32a2ac679bff977cad3ac5d24`.

`compare_public_frontier.py` checks the fixed hashes and exact edge sets.  The
new graph has 1506 edges; relative to that 1505-edge graph it adds 193 and
removes 192.  Thus this is a one-edge improvement over the identified public
explicit-certificate frontier.  This is not an unconditional claim that no
unlocated or unpublished 1506-edge construction exists.

## Reproduction

Requirements: Python 3.8+, `jq`, a C++20 compiler with OpenMP, and the
header-only `nlohmann/json` library.  On Ubuntu the latter is provided by
`nlohmann-json3-dev`.

Run:

```bash
./reproduce.sh
```

The script runs both verifiers, checks the public comparison and portable edge
list, compiles the frozen generator, reruns its one-thread seed-1 search, checks
that the regenerated JSON is byte-identical, and verifies `SHA256SUMS`.

The heuristic generator is provenance, not the proof.  Correctness rests on
the explicit witness and exhaustive definition-level verification.

## Contents

- `q9_edges_1506.json`: canonical witness.
- `q9_edges_1506.txt`: portable edge list.
- `verify_faces.py`: exhaustive square-face verifier.
- `verify_cherries.py`: independent common-neighbor verifier.
- `compare_public_frontier.py`: fixed-hash comparison with public Q9=1505.
- `generator/q9_min_conflicts.cpp`: deterministic generation source.
- `logs/`: generation and verification transcripts.
- `provenance/`: live snapshots, recent paper, upstream notes, and licensing.
- `PROVENANCE.md`: source and scope record.
