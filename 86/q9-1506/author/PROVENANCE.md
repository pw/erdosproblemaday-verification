# Provenance and search boundary

Access date for online material: 2026-08-11 UTC.

## Problem status

`provenance/erdosproblems_86_live_20260811.txt` is a live rendered-text
snapshot of <https://www.erdosproblems.com/86>.  It records `OPEN - $100`,
zero claimed proofs, and no current worker or collaborator.  It also identifies
OEIS A245762.  The downloaded b-file snapshot in this bundle ends at the known
exact value for `n=6`; it has no Q9 term.

## Recent and public construction baseline

Minamo Minamoto, *New Lower Bounds for C4-Free Subgraphs of the Hypercubes Q6,
Q7, and Q8: Constructions, Structure, and Computational Method*,
arXiv:2603.29127v4 (2026), is frozen as
`provenance/minamoto_arxiv_2603.29127v4.pdf`.  It provides Q7=304 and Q8=680
explicit lower bounds, not a Q9=1506 construction.

The rendered live forum snapshot
`provenance/erdosproblems_86_forum_20260811.txt` reports Rafal Wrona's
2026-05-22 explicit Q9=1505 certificate and links
<https://github.com/rafalwronapl/erdos86-hypercube-c4>.

The public comparison material was cloned at:

```text
commit: 74e84382cbbc20b32a2ac679bff977cad3ac5d24
date:   2026-06-07T18:48:51+02:00
title:  Add claim boundary and reproduction notes
```

Its Q9=1505 certificate is frozen under `q9_upstream/`, with SHA-256
`0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338`.
The upstream README, paper draft, claim boundary, MIT license, and original
face verifier are frozen in `provenance/`.

## Generation environment

The witness was generated from the public Q9=1505 certificate by
`generator/q9_min_conflicts.cpp`, using one thread, seed `1`, and a budget of
1,000,000 swaps.  A clean rerun was byte-identical.

Frozen environment versions:

```text
g++ 13.3.0
Python 3.12.3
nlohmann-json 3.11.3
```

See `logs/generation.log`, `logs/verification.log`, and `reproduce.sh`.

## Scope and residual risk

The mathematical claim is the finite lower bound `ex(Q9,C4) >= 1506`.
The certificate makes that claim directly checkable.  Novelty is scoped to the
recent literature and public explicit-certificate frontier identified above;
an unindexed, private, or unpublished construction could have reached the same
number.  No upper bound or exactness claim is made.
